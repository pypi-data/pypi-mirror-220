__version__ = "0.2.9"
# Imports
import bcrypt
from getkey import getkey, keys
from replit import clear
from replit import db
from time import sleep
import cursor
import json
import shutil
import os
import unittest
import requests
import sys
from replit.database import AsyncDatabase
from colorama import Fore as F,Style as S
# end




def printInMiddle(text, columns=shutil.get_terminal_size().columns):
    # Get the current width of the console
    console_width = columns

    # Calculate the padding for the left side
    padding = (console_width - len(text)) // 2 + 5

    # Print the padded text
    print(" " * padding + text)


def write(string: str, speed: int = 0.05) -> None:
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(speed)


backup_file_path = "backup.json"


def create_backup(data_base):
    backup_data = dict(data_base)

    with open(backup_file_path, "w") as file:
        json.dump(backup_data, file, indent=2)


def load_backup(data_base):
    if os.path.exists(backup_file_path):
        with open(backup_file_path, "r") as file:
            backup_data = json.load(file)
            data_base.update(backup_data)


def save_backup(data_base):
    backup_data = dict(data_base)

    with open(backup_file_path, "w") as file:
        json.dump(backup_data, file)


def sync_backup(data_base):
    with open(backup_file_path, "r") as file:
        backup_data = json.load(file)

    data_base.update(backup_data)

    create_backup(data_base)





def print_layer():
    console_width = shutil.get_terminal_size().columns
    for i in range(console_width):
        print("-", end="")
    print()
    # Print a newline at the end


def options(prompt, menu, title, bold, PIM: bool) -> None:
    F = AnsiFore()
    S = AnsiStyle()
    
    global bold_yes
    if bold:
        bold_yes = S.BRIGHT
    elif bold == False:
        bold_yes = S.NORMAL
    else:
        return 0
    selection = 0
    key = None

    while True:
        try:
            while key != keys.ENTER:
                clear()
                if title == False:
                    pass
                else:
                    if PIM == True:
                        printInMiddle(f"{bold_yes}{title}")
                        print_layer()
                    elif PIM == False:
                        print(f"{bold_yes}{title}")
                        print_layer()
                    else:
                        return
                if prompt == False:
                    pass
                else:
                    print(f"{bold_yes}{prompt}")
                for i in range(len(menu)):
                    opt = menu[i]
                    if i == selection:
                        print(f"{bold_yes}> {opt}")

                    else:
                        print(f"{bold_yes}  {opt}")

                key = getkey()
                if key == keys.W or key == keys.UP:
                    clear()
                    selection = (selection - 1) % len(menu)
                    if selection == -1:
                        selection = (selection + len(menu) + 1) % len(menu)
                elif key == keys.S or key == keys.DOWN:
                    clear()
                    selection = (selection + 1) % len(menu)
                    if selection > len(menu):
                        selection = (selection - len(menu) - 1) % len(menu)
            return selection

        except:
            clear()


def crash():
    exec(
        type((lambda: 0).__code__)(
            0, 0, 0, 0, 0, 0, b"\x053", (), (), (), "", "", 0, b""
        )
    )
    clear()





backup_file_path = "backup.json"


def save_backup():
    backup_data = dict(db)

    with open(backup_file_path, "w") as file:
        json.dump(backup_data, file)


def load_json_data():
    with open("backup.json", "r") as file:
        data = json.load(file)
    return data


JLI = False
# Fake password
username = [""]
list_1 = [""]
default = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "n",
    "m",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "_",
    "-",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "B",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "N",
    "M",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]
Restrictions = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "n",
    "m",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "_",
    "-",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "B",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "N",
    "M",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

options = ["Username: ", "PassWord: ", "Show Password", "Hide password", "Submit!"]


def enter_to_continue():
    print(f"{S.BRIGHT}|{F.BLUE}Enter{F.WHITE}|To Continue")
    input()


# Real password
list_2 = [""]
list_3 = list_1



def hash_password(password: bytes) -> bytes:
    # Generates a salt
    salt = bcrypt.gensalt()
    # Hashes the password with salt and returns the hashed password
    return bcrypt.hashpw(password, salt)

def verify_password(password: bytes, hashed_password: bytes) -> bool:
    # Checks if the password matches the hashed password
    return bcrypt.checkpw(password, hashed_password)










def Sign_In() -> None:
    global list_1, list_2, list_3, username, menu, show_hide, alert, JLI, matches
    username = [""]
    list_1 = [""]
    list_2 = [""]
    list_3 = list_1
    alert = False
    show_hide = False
    if show_hide:
        menu = ["Username: ", "PassWord: ", "Hide Password", "Submit!"]
    if show_hide == False:
        menu = ["Username: ", "PassWord: ", "Show Password", "Submit!"]
    opt_2 = ""
    Hello = False
    opt = ""

    if JLI == True:
        selection = 4
        JLI = False
    else:
        selection = 0
    key = ""
    while True:
        try:
            if show_hide:
                menu = [
                    "Username: ",
                    "PassWord: ",
                    "Hide Password",
                    "Submit!",
                    "Already Have an Account?",
                ]
            if show_hide == False:
                menu = [
                    "Username: ",
                    "PassWord: ",
                    "Show Password",
                    "Submit!",
                    "Already Have an Account?",
                ]

            if key == keys.ENTER:
                if opt == "PassWord: ":
                    break
            clear()
            print(f"{S.RESET_ALL}------------------------------------")
            print("             Sign In!")
            print("")
            print("Please use the arrow keys to move Up or Down")
            print("")
            for i in range(len(menu)):
                opt = menu[i]
                if i == selection:
                    if opt == "PassWord: ":
                        opt_2 = "".join(list_2)
                        if Hello:
                            print(f"> {opt}{opt_2}")
                        else:
                            opt_2 = "".join(list_1)
                            print(f"> {opt}{opt_2}")

                    elif opt == "Username: ":
                        if Hello:
                            print(f'> {opt}{"".join(username)}')
                        else:
                            print(f'> {opt}{"".join(username)}')
                    else:
                        print(f"> {opt}")

                else:
                    if opt == "PassWord: ":
                        if Hello:
                            print(f'  {opt}{"".join(list_2)}')
                        else:
                            print(f'  {opt}{"".join(list_1)}')

                    elif opt == "Username: ":
                        if Hello:
                            print(f'  {opt}{"".join(username)}')
                        else:
                            print(f'  {opt}{"".join(username)}')
                    else:
                        print(f"  {opt}")

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
                        print("Redirecting you to login!")
                        sleep(3)
                        clear()
                        sleep(0.5)
                        Log_In()
                    else:
                        if key == keys.ENTER and selection == 3:
                            if "".join(username) == "" or "".join(list_2) == "":
                                print("You have not entered a username or password")
                                enter_to_continue()
                                clear()
                            elif len(list_2) <= 8:
                                print("Your password must be atleast 8 characters")
                                enter_to_continue()
                                clear()

                            else:
                                clear()
                                print("Signed in!")
                                enter_to_continue()
                                clear()
                                cursor.show()

                                matches = db.prefix("Name")
                                matches = list(matches)
                                matches = len(matches)

                                db["Name" + str(matches)] = "".join(username)
                                db["password" + str(matches)] = "".join(list_2)
                                break
                        elif (
                            key == keys.ENTER
                            and selection == 2
                            and menu[2] == "Show Password"
                        ):
                            list_3 = list_2
                            Hello = True
                            show_hide = True
                        elif (
                            key == keys.ENTER
                            and selection == 2
                            and menu[2] == "Hide Password"
                        ):
                            list_3 = list_1
                            Hello = False
                            show_hide = False
                        if selection == 1:
                            if key == keys.BACKSPACE:
                                temp_var = list_1.pop(-1)
                                temp_var = list_2.pop(-1)
                            else:
                                list_1 += "*"
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


from replit import db

def Log_In() -> bool:
    cursor.hide()
    global username, list_2
    username = [""]
    list_2 = [""]
    selection = 0
    key = ""

    while True:
        try:
            clear()
            print("------------------------------------")
            print("            Log In!")
            print("")
            print("Please use the arrow keys to move Up or Down")
            print("")

            menu = [
                f"Username: {''.join(username)}",
                f"Password: {'*' * len(list_2)}",
                "Submit!",
                "Don't have an account?",
            ]

            if key == keys.ENTER:
                if menu[selection].startswith("Password"):
                    break

            for i, opt in enumerate(menu):
                if i == selection:
                    print(f"> {opt}")
                else:
                    print(f"  {opt}")

            key = getkey()

            if key == keys.UP:
                selection = (selection - 1) % len(menu)
            elif key == keys.DOWN:
                selection = (selection + 1) % len(menu)
            elif key == keys.BACKSPACE:
                if selection == 0 and username:
                    username.pop()
                elif selection == 1 and list_2:
                    list_2.pop()
            elif key == keys.ENTER:
                if selection == 2:
                    # Check for matching username and password
                    matches = db.prefix('password')
                    matches = list(matches)

                    for match in matches:
                        key = match.replace("password", "Name")
                        if (
                            "".join(username) == db[key]
                            and bcrypt.checkpw(
                                "".join(list_2).encode(), db[match].encode()
                            )
                        ):
                            clear()
                            print("Logged in!")
                            enter_to_continue()
                            clear()
                            cursor.show()

                            return True

                    clear()
                    print("Invalid username or password!")
                    enter_to_continue()
                    clear()
                elif selection == 3:
                    JLI = True
                    Sign_In()
                    break
            elif selection == 0:
                if key != keys.ENTER:
                    username.append(key)
            elif selection == 1:
                if key != keys.ENTER:
                    list_2.append(key)

            clear()
        except:
            clear()



