import random
import time
import sys
from colorama import Fore, Back, Style, init
init(convert=True)
import lists
import typer
import lists
import msvcrt

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""
def red(text):
    return (Fore.RED + text + Fore.WHITE)

def green(text):
    return (Fore.GREEN + text + Fore.WHITE)
            
def magenta(text):
    return (Fore.MAGENTA + text + Fore.WHITE)

def yellow(text):
    return (Fore.YELLOW + text + Fore.WHITE)

def cyan(text):
    return (Fore.CYAN + text + Fore.WHITE)
            
def bright(text):
    return (Style.BRIGHT + text + Style.NORMAL)

def open_quote(text):
    return ("\"" + text)

def close_quote(text):
    return (text + "\"")

def quote(text):
    return ("\"" + text + "\"")

def space_quote(text):
    return ("\"" + text + "\" ")

type = typer.Type()
ask = typer.Ask()

def ticket(max=10, length=5, print_ticket=False):
    type.type()
    lucky_number = ask.choose_a_number(1, max)
    matches = 0
    winning_numbers = []
    unscratched_str = ""
    for _ in range(length):
        unscratched_str += "  **"
    scratched_str = ""
    matches_str = ""
    for _ in range(length):
        new_numb = random.randint(1, max)
        winning_numbers.append(new_numb)
        if 1 <= new_numb <= 9:
            if new_numb == lucky_number:
                matches+=1
                matches_str += "  " + bright(green(str(0) + str(new_numb)))
                scratched_str += "  " + str(0) + str(new_numb)
            else:
                matches_str += "  " + str(0) + str(new_numb) 
                scratched_str += "  " + str(0) + str(new_numb)
        else:
            if new_numb == lucky_number:
                matches+=1
                matches_str += "  " + bright(green(str(new_numb)))
                scratched_str += "  " + str(new_numb)
            else:
                scratched_str += "  " + str(new_numb)
                matches_str += "  " + str(new_numb)
            

    type.slow("Your number is: " + str(lucky_number))
    print()
    type.suspense(unscratched_str[:-2])
    print("", end="\r")
    type.suspense(scratched_str[:-2])
    if matches > 0:
        for blink_count in range(3):
            time.sleep(0.6)
            print("", end="\r")
            print(matches_str, end="\r")
            time.sleep(0.6)
            if blink_count < 2:
                print("", end="\r")
                print(scratched_str, end="\r")
        print("")
        if matches == 1:
            type.type("You had " + str(matches) + " match.")
        else:
            type.type("You had " + str(matches) + " matches.")
    else:
        print("")
        type.type("Welp. Guess that one was a loser.")


def main():
    ticket(10, 30)

main()