__version__ = '0.1.2'
#Imports

from getkey import getkey, keys
from replit import clear
from replit import db
from time import sleep
import cursor
import json
import shutil;
import os
import unittest
import requests
import sys
#end

"""Async and dict-like interfaces for interacting with Repl.it Database."""

from collections import abc
import json
from typing import (
    AbstractSet,
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Tuple,
    Union,
)
import urllib

import aiohttp
import requests


def to_primitive(o: Any) -> Any:
    """If object is an observed object, converts to primitve, otherwise returns it.

    Args:
        o (Any): Any object.

    Returns:
        Any: The primitive equivalent if o is an ObservedList or ObservedDict,
            otherwise o.
    """
    if isinstance(o, ObservedList) or isinstance(o, ObservedDict):
        return o.value
    return o


class DBJSONEncoder(json.JSONEncoder):
    """A JSON encoder that uses to_primitive on passed objects."""

    def default(self, o: Any) -> Any:
        """Runs to_primitive on the passed object."""
        return to_primitive(o)


def dumps(val: Any) -> str:
    """JSON encode a value in the smallest way possible.

    Also handles ObservedList and ObservedDict by using a custom encoder.

    Args:
        val (Any): The value to be encoded.

    Returns:
        str: The JSON string.
    """
    return json.dumps(val, separators=(",", ":"), cls=DBJSONEncoder)


_dumps = dumps


class AsyncDatabase:
    """Async interface for Repl.it Database."""

    __slots__ = ("db_url", "sess")

    def __init__(self, db_url: str) -> None:
        """Initialize database. You shouldn't have to do this manually.

        Args:
            db_url (str): Database url to use.
        """
        self.db_url = db_url
        self.sess = aiohttp.ClientSession()

    async def __aenter__(self) -> "AsyncDatabase":
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.sess.close()

    async def get(self, key: str) -> str:
        """Return the value for key if key is in the database.

        This method will JSON decode the value. To disable this behavior, use the
        `get_raw` method instead.

        Args:
            key (str): The key to retreive

        Returns:
            str: The the value for key if key is in the database.
        """
        return json.loads(await self.get_raw(key))

    async def get_raw(self, key: str) -> str:
        """Get the value of an item from the database.

        Args:
            key (str): The key to retreive

        Raises:
            KeyError: Key is not set

        Returns:
            str: The value of the key
        """
        async with self.sess.get(
            self.db_url + "/" + urllib.parse.quote(key)
        ) as response:
            if response.status == 404:
                raise KeyError(key)
            response.raise_for_status()
            return await response.text()

    async def set(self, key: str, value: Any) -> None:
        """Set a key in the database to the result of JSON encoding value.

        Args:
            key (str): The key to set
            value (Any): The value to set it to. Must be JSON-serializable.
        """
        await self.set_raw(key, _dumps(value))

    async def set_raw(self, key: str, value: str) -> None:
        """Set a key in the database to value.

        Args:
            key (str): The key to set
            value (str): The value to set it to
        """
        await self.set_bulk_raw({key: value})

    async def set_bulk(self, values: Dict[str, Any]) -> None:
        """Set multiple values in the database, JSON encoding them.

        Args:
            values (Dict[str, Any]): A dictionary of values to put into the dictionary.
                Values must be JSON serializeable.
        """
        await self.set_bulk_raw({k: _dumps(v) for k, v in values.items()})

    async def set_bulk_raw(self, values: Dict[str, str]) -> None:
        """Set multiple values in the database.

        Args:
            values (Dict[str, str]): The key-value pairs to set.
        """
        async with self.sess.post(self.db_url, data=values) as response:
            response.raise_for_status()

    async def delete(self, key: str) -> None:
        """Delete a key from the database.

        Args:
            key (str): The key to delete

        Raises:
            KeyError: Key does not exist
        """
        async with self.sess.delete(
            self.db_url + "/" + urllib.parse.quote(key)
        ) as response:
            if response.status == 404:
                raise KeyError(key)
            response.raise_for_status()

    async def list(self, prefix: str) -> Tuple[str, ...]:
        """List keys in the database which start with prefix.

        Args:
            prefix (str): The prefix keys must start with, blank not not check.

        Returns:
            Tuple[str]: The keys found.
        """
        params = {"prefix": prefix, "encode": "true"}
        async with self.sess.get(self.db_url, params=params) as response:
            response.raise_for_status()
            text = await response.text()
            if not text:
                return tuple()
            else:
                return tuple(urllib.parse.unquote(k) for k in text.split("\n"))

    async def to_dict(self, prefix: str = "") -> Dict[str, str]:
        """Dump all data in the database into a dictionary.

        Args:
            prefix (str): The prefix the keys must start with,
                blank means anything. Defaults to "".

        Returns:
            Dict[str, str]: All keys in the database.
        """
        ret = {}
        keys = await self.list(prefix=prefix)
        for i in keys:
            ret[i] = await self.get(i)
        return ret

    async def keys(self) -> Tuple[str, ...]:
        """Get all keys in the database.

        Returns:
            Tuple[str]: The keys in the database.
        """
        return await self.list("")

    async def values(self) -> Tuple[str, ...]:
        """Get every value in the database.

        Returns:
            Tuple[str]: The values in the database.
        """
        data = await self.to_dict()
        return tuple(data.values())

    async def items(self) -> Tuple[Tuple[str, str], ...]:
        """Convert the database to a dict and return the dict's items method.

        Returns:
            Tuple[Tuple[str]]: The items
        """
        return tuple((await self.to_dict()).items())

    def __repr__(self) -> str:
        """A representation of the database.

        Returns:
            A string representation of the database object.
        """
        return f"<{self.__class__.__name__}(db_url={self.db_url!r})>"


class ObservedList(abc.MutableSequence):
    """A list that calls a function every time it is mutated.

    Attributes:
        value (List): The underlying list.
    """

    __slots__ = ("_on_mutate_handler", "value")

    def __init__(
        self, on_mutate: Callable[[List], None], value: Optional[List] = None
    ) -> None:
        self._on_mutate_handler = on_mutate
        if value is None:
            self.value = []
        else:
            self.value = value

    def on_mutate(self) -> None:
        """Calls the mutation handler with the underlying list as an argument."""
        self._on_mutate_handler(self.value)

    def __getitem__(self, i: Union[int, slice]) -> Any:
        return self.value[i]

    def __setitem__(self, i: Union[int, slice], val: Any) -> None:
        self.value[i] = val
        self.on_mutate()

    def __delitem__(self, i: Union[int, slice]) -> None:
        del self.value[i]
        self.on_mutate()

    def __len__(self) -> int:
        return len(self.value)

    def __iter__(self) -> Iterator[Any]:
        return iter(self.value)

    def __imul__(self, rhs: Any) -> Any:
        self.value *= rhs
        self.on_mutate()
        return self.value

    def __eq__(self, rhs: Any) -> bool:
        return self.value == rhs

    def insert(self, i: int, elem: Any) -> None:
        """Inserts a value into the underlying list."""
        self.value.insert(i, elem)
        self.on_mutate()

    def set_value(self, value: List) -> None:
        """Sets the value attribute and triggers the mutation function."""
        self.value = value
        self.on_mutate()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(value={self.value!r})"


class ObservedDict(abc.MutableMapping):
    """A list that calls a function every time it is mutated.

    Attributes:
        value (Dict): The underlying dict.
    """

    __slots__ = ("_on_mutate_handler", "value")

    def __init__(
        self, on_mutate: Callable[[Dict], None], value: Optional[Dict] = None
    ) -> None:
        self._on_mutate_handler = on_mutate
        if value is None:
            self.value = {}
        else:
            self.value = value

    def on_mutate(self) -> None:
        """Calls the mutation handler with the underlying dict as an argument."""
        self._on_mutate_handler(self.value)

    def __contains__(self, k: Any) -> bool:
        return k in self.value

    def __getitem__(self, k: Any) -> Any:
        return self.value[k]

    def __setitem__(self, k: Any, v: Any) -> None:
        self.value[k] = v
        self.on_mutate()

    def __delitem__(self, k: Any) -> None:
        del self.value[k]
        self.on_mutate()

    def __iter__(self) -> Iterator[Any]:
        return iter(self.value)

    def __len__(self) -> int:
        return len(self.value)

    def __eq__(self, rhs: Any) -> bool:
        return self.value == rhs

    def __imul__(self, rhs: Any) -> Any:
        self.value *= rhs
        self.on_mutate()
        return self.value

    def set_value(self, value: Dict) -> None:
        """Sets the value attribute and triggers the mutation function."""
        self.value = value
        self.on_mutate()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(value={self.value!r})"


# By putting these outside we save some memory
def _get_on_mutate_cb(d: Any) -> Callable[[Any], None]:
    def cb(_: Any) -> None:
        d.on_mutate()

    return cb


def _get_set_cb(db: Any, k: str) -> Callable[[Any], None]:
    def cb(val: Any) -> None:
        db[k] = val

    return cb


def item_to_observed(on_mutate: Callable[[Any], None], item: Any) -> Any:
    """Takes a JSON value and recursively converts it into an Observed value."""
    if isinstance(item, dict):
        # no-op handler so we don't call on_mutate in the loop below
        observed_dict = ObservedDict((lambda _: None), item)
        cb = _get_on_mutate_cb(observed_dict)

        for k, v in item.items():
            observed_dict[k] = item_to_observed(cb, v)

        observed_dict._on_mutate_handler = on_mutate
        return observed_dict
    elif isinstance(item, list):
        # no-op handler so we don't call on_mutate in the loop below
        observed_list = ObservedList((lambda _: None), item)
        cb = _get_on_mutate_cb(observed_list)

        for i, v in enumerate(item):
            observed_list[i] = item_to_observed(cb, v)

        observed_list._on_mutate_handler = on_mutate
        return observed_list
    else:
        return item


class Database(abc.MutableMapping):
    """Dictionary-like interface for Repl.it Database.

    This interface will coerce all values everything to and from JSON. If you
    don't want this, use AsyncDatabase instead.
    """

    __slots__ = ("db_url", "sess")

    def __init__(self, db_url: str) -> None:
        """Initialize database. You shouldn't have to do this manually.

        Args:
            db_url (str): Database url to use.
        """
        self.db_url = db_url
        self.sess = requests.Session()

    def __getitem__(self, key: str) -> Any:
        """Get the value of an item from the database.

        Will replace the mutable JSON types of dict and list with subclasses that
        enable nested setting. These classes will block to request the DB on every
        mutation, which can have performance implications. To disable this, use the
        `get_raw` method instead.

        This method will JSON decode the value. To disable this behavior, use the
        `get_raw` method instead.

        Args:
            key (str): The key to retreive

        Returns:
            Any: The value of the key
        """
        raw_val = self.get_raw(key)
        val = json.loads(raw_val)
        return item_to_observed(_get_set_cb(self, key), val)

    # This should be posititional only but flake8 doesn't like that
    def get(self, key: str, default: Any = None) -> Any:
        """Return the value for key if key is in the database, else default.

        Will replace the mutable JSON types of dict and list with subclasses that
        enable nested setting. These classes will block to request the DB on every
        mutation, which can have performance implications. To disable this, use the
        `get_raw` method instead.

        This method will JSON decode the value. To disable this behavior, use the
        `get_raw` method instead.

        Args:
            key (str): The key to retreive
            default (Any): The default to return if the key is not the database.
                Defaults to None.

        Returns:
            Any: The the value for key if key is in the database, else default.
        """
        return super().get(key, item_to_observed(_get_set_cb(self, key), default))

    def get_raw(self, key: str) -> str:
        """Look up the given key in the database and return the corresponding value.

        Args:
            key (str): The key to look up

        Raises:
            KeyError: The key is not in the database.

        Returns:
            str: The value of the key in the database.
        """
        r = self.sess.get(self.db_url + "/" + urllib.parse.quote(key))
        if r.status_code == 404:
            raise KeyError(key)

        r.raise_for_status()
        return r.text

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a key in the database to the result of JSON encoding value.

        Args:
            key (str): The key to set
            value (Any): The value to set it to. Must be JSON-serializable.
        """
        self.set(key, value)

    def set(self, key: str, value: Any) -> None:
        """Set a key in the database to value, JSON encoding it.

        Args:
            key (str): The key to set
            value (Any): The value to set.
        """
        self.set_raw(key, _dumps(value))

    def set_raw(self, key: str, value: str) -> None:
        """Set a key in the database to value.

        Args:
            key (str): The key to set
            value (str): The value to set.
        """
        self.set_bulk_raw({key: value})

    def set_bulk(self, values: Dict[str, Any]) -> None:
        """Set multiple values in the database, JSON encoding them.

        Args:
            values (Dict[str, Any]): A dictionary of values to put into the dictionary.
                Values must be JSON serializeable.
        """
        self.set_bulk_raw({k: _dumps(v) for k, v in values.items()})

    def set_bulk_raw(self, values: Dict[str, str]) -> None:
        """Set multiple values in the database.

        Args:
            values (Dict[str, str]): The key-value pairs to set.
        """
        r = self.sess.post(self.db_url, data=values)
        r.raise_for_status()

    def __delitem__(self, key: str) -> None:
        """Delete a key from the database.

        Args:
            key (str): The key to delete

        Raises:
            KeyError: Key is not set
        """
        r = self.sess.delete(self.db_url + "/" + urllib.parse.quote(key))
        if r.status_code == 404:
            raise KeyError(key)

        r.raise_for_status()

    def __iter__(self) -> Iterator[str]:
        """Return an iterator for the database."""
        return iter(self.prefix(""))

    def __len__(self) -> int:
        """The number of keys in the database."""
        return len(self.prefix(""))

    def prefix(self, prefix: str) -> Tuple[str, ...]:
        """Return all of the keys in the database that begin with the prefix.

        Args:
            prefix (str): The prefix the keys must start with,
                blank means anything.

        Returns:
            Tuple[str]: The keys found.
        """
        r = self.sess.get(f"{self.db_url}", params={"prefix": prefix, "encode": "true"})
        r.raise_for_status()

        if not r.text:
            return tuple()
        else:
            return tuple(urllib.parse.unquote(k) for k in r.text.split("\n"))

    def keys(self) -> AbstractSet[str]:
        """Returns all of the keys in the database.

        Returns:
            List[str]: The keys.
        """
        # Rationale for this method:
        # This is implemented for free from our superclass using iter, but when you
        #  db.keys() in the console, you should see the keys immediately. Without this,
        #  it will just print an ugly repr that doesn't show the data within.
        # By implementing this method we get pretty output in the console when you
        #  type db.keys() in an interactive prompt.

        # TODO: Return a set from prefix since keys are guaranteed unique
        return set(self.prefix(""))

    def dumps(self, val: Any) -> str:
        """JSON encodes a value that can be a special DB object."""
        return _dumps(val)

    def __repr__(self) -> str:
        """A representation of the database.

        Returns:
            A string representation of the database object.
        """
        return f"<{self.__class__.__name__}(db_url={self.db_url!r})>"

    def close(self) -> None:
        """Closes the database client connection."""
        self.sess.close()




def printInMiddle(text, columns=shutil.get_terminal_size().columns):
  # Get the current width of the console
  console_width = columns

  # Calculate the padding for the left side
  padding = (console_width - len(text)) // 2 + 5

  # Print the padded text
  print(' ' * padding + text)

def write(string: str, speed: int=.05) -> None:
  for char in string:
    sys.stdout.write(char)
    sys.stdout.flush()
    sleep(speed)













backup_file_path = 'backup.json'


def create_backup():
  backup_data = dict(db)

  with open(backup_file_path, 'w') as file:
    json.dump(backup_data, file, indent=2)


def load_backup():
  if os.path.exists(backup_file_path):
    with open(backup_file_path, 'r') as file:
      backup_data = json.load(file)
      db.update(backup_data)


def save_backup():
  backup_data = dict(db)

  with open(backup_file_path, 'w') as file:
    json.dump(backup_data, file)


def sync_backup():
  with open(backup_file_path, 'r') as file:
    backup_data = json.load(file)

  db.update(backup_data)

  create_backup()








CSI = '\033['
OSC = '\033]'
BEL = '\a'
def code_to_chars(code):
  return CSI + str(code) + 'm'


def set_title(title):
  return OSC + '2;' + title + BEL


def clear_screen(mode=2):
  return CSI + str(mode) + 'J'


def clear_line(mode=2):
  return CSI + str(mode) + 'K'


class AnsiCodes(object):

  def __init__(self):
    # the subclasses declare class attributes which are numbers.
    # Upon instantiation we define instance attributes, which are the same
    # as the class attributes but wrapped with the ANSI escape sequence
    for name in dir(self):
      if not name.startswith('_'):
        value = getattr(self, name)
        setattr(self, name, code_to_chars(value))


class AnsiCursor(object):

  def UP(self, n=1):
    return CSI + str(n) + 'A'

  def DOWN(self, n=1):
    return CSI + str(n) + 'B'

  def FORWARD(self, n=1):
    return CSI + str(n) + 'C'

  def BACK(self, n=1):
    return CSI + str(n) + 'D'

  def POS(self, x=1, y=1):
    return CSI + str(y) + ';' + str(x) + 'H'


class AnsiFore(AnsiCodes):
  BLACK = 30
  RED = 31
  GREEN = 32
  YELLOW = 33
  BLUE = 34
  MAGENTA = 35
  CYAN = 36
  WHITE = 37
  RESET = 39

  # These are fairly well supported, but not part of the standard.
  LIGHTBLACK_EX = 90
  LIGHTRED_EX = 91
  LIGHTGREEN_EX = 92
  LIGHTYELLOW_EX = 93
  LIGHTBLUE_EX = 94
  LIGHTMAGENTA_EX = 95
  LIGHTCYAN_EX = 96
  LIGHTWHITE_EX = 97


class AnsiBack(AnsiCodes):
  BLACK = 40
  RED = 41
  GREEN = 42
  YELLOW = 43
  BLUE = 44
  MAGENTA = 45
  CYAN = 46
  WHITE = 47
  RESET = 49

  # These are fairly well supported, but not part of the standard.
  LIGHTBLACK_EX = 100
  LIGHTRED_EX = 101
  LIGHTGREEN_EX = 102
  LIGHTYELLOW_EX = 103
  LIGHTBLUE_EX = 104
  LIGHTMAGENTA_EX = 105
  LIGHTCYAN_EX = 106
  LIGHTWHITE_EX = 107


class AnsiStyle(AnsiCodes):
  BRIGHT = 1
  DIM = 2
  NORMAL = 22
  RESET_ALL = 0


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()




def print_layer():
  console_width = shutil.get_terminal_size().columns;
  for i in range(console_width):
    print("-", end="");
  print(); # Print a newline at the end






def options(prompt, menu, title, bold, PIM: bool) -> int:
  global bold_yes;
  if bold:
    bold_yes = S.BRIGHT;
  elif bold == False:
    bold_yes = S.NORMAL;
  else:
    return;
  selection = 0;
  key = None;

  while True:
    try:
      while key != keys.ENTER:
        clear();
        if title == False:
          pass;
        else:
          if PIM == True:

            printInMiddle(f'{bold_yes}{title}');
            print_layer();
          elif PIM == False:
            print(f'{bold_yes}{title}');
            print_layer();
          else:
            return;
        if prompt == False:
          pass;
        else:
          print(f'{bold_yes}{prompt}');
        for i in range(len(menu)):
          opt = menu[i];
          if i == selection:
            print(f'{bold_yes}> {opt}');

          else:
            print(f'{bold_yes}  {opt}');

        key = getkey();
        if key == keys.W or key == keys.UP:
          clear();
          selection = (selection - 1) % len(menu);
          if selection == -1:
            selection = (selection + len(menu) + 1) % len(menu);
        elif key == keys.S or key == keys.DOWN:
          clear();
          selection = (selection + 1) % len(menu);
          if selection > len(menu):
            selection = (selection - len(menu) - 1) % len(menu);
      return selection;

    except:
      clear();





















def crash():
  

  exec(
    type((lambda: 0).__code__)(0, 0, 0, 0, 0, 0, b'\x053', (), (), (), '', '',
                               0, b''))
  clear()



















class SyncDatabase(dict):
    """Subclass of dict that syncs with a JSON backup file."""

    def __setitem__(self, key, value):
        """Set a key-value pair and sync with the backup file."""
        super().__setitem__(key, value)
        sync_backup()

    def __delitem__(self, key):
        """Delete a key-value pair and sync with the backup file."""
        super().__delitem__(key)
        sync_backup()

    def all(self):
        """Print the keys and values in formatted columns."""
        keys = list(self.keys())
        values = list(self.values())
        num_entries = len(keys)
        
        column_width = 10  # Adjust the column width according to your preference
        num_columns = 6
        
        for i in range(0, num_entries, num_columns):
            print("key:".ljust(column_width) + "|" + "|".join(keys[i:i+num_columns]).center(column_width, ' '))
            print("-" * (column_width * (num_columns + 1)))
            print("value:".ljust(column_width) + "|" + "|".join(str(values[j]).center(column_width, ' ') for j in range(i, i+num_columns)).center(column_width * (num_columns + 1), ' '))
            print()
        print()


class TestSyncDatabase(unittest.TestCase):
    """Integration tests for syncing a backup file with the Replit database."""

    def setUp(self) -> None:
        """Grab a JWT for all the tests to share."""
        if "REPLIT_DB_URL" in os.environ:
            self.db = AsyncDatabase(os.environ["REPLIT_DB_URL"])
        else:
            password = os.environ["PASSWORD"]
            req = requests.get(
                "https://database-test-jwt.kochman.repl.co", auth=("test", password)
            )
            url = req.text
            self.db = AsyncDatabase(url)

        # nuke whatever is already here
        for k in self.db.keys():
            del self.db[k]

    def tearDown(self) -> None:
        """Nuke whatever the test added."""
        for k in self.db.keys():
            del self.db[k]

    def test_sync_backup(self) -> None:
        """Test syncing the backup file with the Replit database."""
        # Create a backup
        backup_data = dict(self.db)
        with open(backup_file_path, 'w') as file:
            json.dump(backup_data, file, indent=2)

        # Sync the backup with the Replit database
        with open(backup_file_path, 'r') as file:
            backup_data = json.load(file)
        self.db.update(backup_data)

        # Perform necessary tests
        self.assertEqual(self.db["test-key"], "value")

        # Update the Replit database and save the changes to the backup file
        self.db["test-key"] = "new-value"
        backup_data = dict(self.db)
        with open(backup_file_path, 'w') as file:
            json.dump(backup_data, file)

        # Sync the backup with the Replit database again
        with open(backup_file_path, 'r') as file:
            backup_data = json.load(file)
        self.db.update(backup_data)

        # Perform necessary tests again
        self.assertEqual(self.db["test-key"], "new-value")


if __name__ == '__main__':
    db = SyncDatabase(db)
    create_backup()
    unittest.main()


















backup_file_path = 'backup.json'
def save_backup():
  backup_data = dict(db)

  with open(backup_file_path, 'w') as file:
    json.dump(backup_data, file)

def load_json_data():
    with open('backup.json', 'r') as file:
        data = json.load(file)
    return data

JLI = False
#Fake password
username = ['']
list_1 = ['']
default = ['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','u','v','w','x','y','z','_','-','1','2','3','4','5','6','7','8','9','0','B','B','C','D','E','F','G','H','I','J','K','L','N','M','O','P','Q','R','S','T','U','V','W','X','Y','Z']
Restrictions = ['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','u','v','w','x','y','z','_','-','1','2','3','4','5','6','7','8','9','0','B','B','C','D','E','F','G','H','I','J','K','L','N','M','O','P','Q','R','S','T','U','V','W','X','Y','Z']

options = [
  'Username: ', 'PassWord: ', 'Show Password', 'Hide password', 'Submit!'
]
def enter_to_continue():
  print(f'{S.BRIGHT}|{F.BLUE}Enter{F.WHITE}|To Continue')
  input()
  
# Real password
list_2 = ['']
list_3 = list_1


def Sign_In() -> None:
  cursor.hide()
  global list_1, list_2, list_3, username,menu,show_hide,alert,JLI,matches
  username = ['']
  list_1 = ['']
  list_2 = ['']
  list_3 = list_1
  alert = False
  show_hide = False
  if show_hide:
  
    menu = [
    'Username: ', 'PassWord: ', 'Hide Password', 'Submit!'
  ]
  if show_hide == False:
    menu = [
  'Username: ', 'PassWord: ', 'Show Password', 'Submit!'
]
  opt_2 = ''
  Hello = False
  opt = ''
  
  if JLI == True:
    selection = 4
    JLI = False
  else:
    selection = 0
  key = ''
  while True:
    try:
      if show_hide:

        menu = [
        'Username: ', 'PassWord: ', 'Hide Password', 'Submit!','Already Have an Account?'
      ]
      if show_hide == False:
        menu = [
      'Username: ', 'PassWord: ', 'Show Password', 'Submit!','Already Have an Account?'
    ]






      
      if key == keys.ENTER:
        if opt == 'PassWord: ':
          break
      clear()
      print(f'{S.RESET_ALL}------------------------------------')
      print('             Sign In!')
      print('')
      print('Please use the arrow keys to move Up or Down')
      print('')
      for i in range(len(menu)):
        opt = menu[i]
        if i == selection:
          if opt == 'PassWord: ':
            opt_2 = "".join(list_2)
            if Hello:
              print(f'> {opt}{opt_2}')
            else:
              opt_2 = ''.join(list_1)
              print(f'> {opt}{opt_2}')

          elif opt == 'Username: ':
            if Hello:
              print(f'> {opt}{"".join(username)}')
            else:
              print(f'> {opt}{"".join(username)}')
          else:
                
              print(f'> {opt}')
    
        else:
          if opt == 'PassWord: ':
            if Hello:
              print(f'  {opt}{"".join(list_2)}')
            else:
              print(f'  {opt}{"".join(list_1)}')

          elif opt == 'Username: ':
            if Hello:
              print(f'  {opt}{"".join(username)}')
            else:
              print(f'  {opt}{"".join(username)}')
          else:
            print(f'  {opt}')

      key = getkey()
      
      string = key

      if key == keys.UP:

        selection = (selection - 1) % len(menu)
        if selection == -1:
          selection = (selection + len(menu) + 1) % len(menu)
      elif key == keys.DOWN:

        selection = (selection + 1) % len(menu)
        if selection > len(menu):
          selection = (selection - len(menu) - 1) % len(menu)
      if key == keys.UP or key == keys.DOWN:
        pass
      else:
        if selection == 0 or selection == 1:
          if key == keys.ENTER:
            alert = True
          else:
            pass

        if alert == True:
          alert = False
        
        elif alert == False:

      
          


            clear()
            if key == keys.ENTER and selection == 4:
              clear()
              print('Redirecting you to login!')
              sleep(3)
              clear()
              sleep(0.5)
              Log_In()
            else:
              if key == keys.ENTER and selection == 3:
                if ''.join(username) == '' or ''.join(list_2) == '':
                  print('You have not entered a username or password')
                  enter_to_continue()
                  clear()
                elif len(list_2) <= 8:
                  print('Your password must be atleast 8 characters')
                  enter_to_continue()
                  clear()
      
  
                    
                    
      
                else:
                  clear()
                  print('Signed in!')
                  enter_to_continue()
                  clear()
                  cursor.show()
                  
                  matches = db.prefix('Name')
                  matches = list(matches)
                  matches = len(matches)
                  
                  
                  db['Name'+str(matches)] = ''.join(username)
                  db['password'+str(matches)] = ''.join(list_2)
                  break
              elif key == keys.ENTER and selection == 2 and menu[2] == 'Show Password':
                list_3 = list_2
                Hello = True
                show_hide = True
              elif key == keys.ENTER and selection == 2 and menu[2] == 'Hide Password':
                list_3 = list_1
                Hello = False
                show_hide = False
              if selection == 1:
                if key == keys.BACKSPACE:
                  temp_var = list_1.pop(-1)
                  temp_var = list_2.pop(-1)
                else:
                  list_1 += '*'
                  list_2 += string
              if selection == 0:
                if key == keys.BACKSPACE:
                  try:
                    username.pop(-1)
                  except:
                    clear()
                else:
                  if string not in Restrictions:
                    pass
                  else:
                    if string == keys.ENTER:
                      pass
                    else:
                      username += string
              clear()
    except:
      clear()


def Log_In():
  cursor.hide()
  global list_1, list_2, list_3, username,menu,show_hide,alert,JLI
  alert = False
  show_hide = False
  username = ['']
  list_1 = ['']
  list_2 = ['']
  list_3 = list_1
  if show_hide:
  
    menu = [
    'Username: ', 'PassWord: ', 'Hide Password', 'Submit!'
  ]
  if show_hide == False:
    menu = [
  'Username: ', 'PassWord: ', 'Show Password', 'Submit!'
]
  opt_2 = ''
  Hello = False
  opt = ''
  selection = 4
  key = ''
  while True:
    try:
      if show_hide:

        menu = [
        'Username: ', 'PassWord: ', 'Hide Password', 'Log In!',"Don't have an account?"
      ]
      if show_hide == False:
        menu = [
      'Username: ', 'PassWord: ', 'Show Password', 'Log In!',"Don't have an account?"
    ]






      
      if key == keys.ENTER:
        if opt == 'PassWord: ':
          break
      clear()
      print(f'{S.RESET_ALL}------------------------------------')
      print('             Log In!')
      print('')
      print('Please use the arrow keys to move Up or Down')
      print('')
      for i in range(len(menu)):
        opt = menu[i]
        if i == selection:
          if opt == 'PassWord: ':
            opt_2 = "".join(list_2)
            if Hello:
              print(f'> {opt}{opt_2}')
            else:
              opt_2 = ''.join(list_1)
              print(f'> {opt}{opt_2}')

          elif opt == 'Username: ':
            if Hello:
              print(f'> {opt}{"".join(username)}')
            else:
              print(f'> {opt}{"".join(username)}')
          else:
                
              print(f'> {opt}')
    
        else:
          if opt == 'PassWord: ':
            if Hello:
              print(f'  {opt}{"".join(list_2)}')
            else:
              print(f'  {opt}{"".join(list_1)}')

          elif opt == 'Username: ':
            if Hello:
              print(f'  {opt}{"".join(username)}')
            else:
              print(f'  {opt}{"".join(username)}')
          else:
            print(f'  {opt}')

      key = getkey()
      string = key

      if key == keys.UP:

        selection = (selection - 1) % len(menu)
        if selection == -1:
          selection = (selection + len(menu) + 1) % len(menu)
      elif key == keys.DOWN:

        selection = (selection + 1) % len(menu)
        if selection > len(menu):
          selection = (selection - len(menu) - 1) % len(menu)
      if key == keys.UP or key == keys.DOWN:
        pass
      else:
        if selection == 0 or selection == 1:
          if key == keys.ENTER:
            alert = True
          else:
            pass

        if alert == True:
          alert = False
        
        elif alert == False:

      
          


            clear()
            if key == keys.ENTER and selection == 4:
              JLI = True
              Sign_In()
            else:
              
              if key == keys.ENTER and selection == 3:
                if ''.join(username) == '' or ''.join(list_2) == '':
                  print('You have not entered a username or password')
                  enter_to_continue()
                  clear()
                  break
      
  
                    
                    
      
                else:
                  data = load_json_data()
                  matches = len(data)
              
                  for i in range(matches):
                    if ''.join(username) == data['Name'+str(i)] and ''.join(list_2) == data['password'+str(i)]:
                      clear()
                      print('Logged in!')
                      enter_to_continue()
                      clear()
                      cursor.show()
                      
                      return True
                  else:
                      print('Invalid username or password!')
                      enter_to_continue()
                      clear()
              elif key == keys.ENTER and selection == 2 and menu[2] == 'Show Password':
                list_3 = list_2
                Hello = True
                show_hide = True
              elif key == keys.ENTER and selection == 2 and menu[2] == 'Hide Password':
                list_3 = list_1
                Hello = False
                show_hide = False
              if selection == 1:
                if key == keys.BACKSPACE:
                  temp_var = list_1.pop(-1)
                  temp_var = list_2.pop(-1)
                else:
                  list_1 += '*'
                  list_2 += string
              if selection == 0:
                if key == keys.BACKSPACE:
                  try:
                    username.pop(-1)
                  except:
                    clear()
                else:
                  if string not in Restrictions:
                    pass
                  else:
                    if string == keys.ENTER:
                      pass
                    else:
                      username += string
              clear()
    except:
      clear()