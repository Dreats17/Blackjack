import msvcrt
import time
import random
import sys
from colorama import Fore, Back, Style, init


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

class Type:
    def __init__(self):
        self.__type_speed = "Default"
        self.__skip_to_end = False

    def check_for_skip(self):
        """Check if spacebar was pressed to skip typing animation"""
        while msvcrt.kbhit():
            byte = msvcrt.getch()
            if byte == b' ':
                self.__skip_to_end = True
                return True
            elif byte == b',':
                self.__type_speed = "Default"
            elif byte == b'.':
                self.__type_speed = "Fast"
            elif byte == b'/':
                self.__type_speed = "Fastest"
            elif byte == b'p':
                self.__type_speed = "Print"
        return False

    def fast(self, *words):
        str = ''
        for item in words:
            str = str + item
        self.__skip_to_end = False
        # str += "\n"
        for i, char in enumerate(str):
            if self.__skip_to_end:
                # Print remaining text instantly
                sys.stdout.write(str[i:])
                sys.stdout.flush()
                break
            time.sleep(random.choice([
            0.03, 0.05, 0.04, 0.02,
            0.05, 0.03, 0.02, 0.05, 0.04, 0.01
            ]))
            sys.stdout.write(char)
            sys.stdout.flush()
            if ((char == ".") or (char == "!") or (char == ":")):
                time.sleep(0.5)
            if (char == ","):
                time.sleep(0.4)
            self.check_for_skip()

    def fast_clean(self, *words):
        str = ''
        for item in words:
            str = str + item
        self.__skip_to_end = False
        # str += "\n"
        for i, char in enumerate(str):
            if self.__skip_to_end:
                sys.stdout.write(str[i:])
                sys.stdout.flush()
                break
            time.sleep(random.choice([
            0.03, 0.05, 0.04, 0.02,
            0.05, 0.03, 0.02, 0.05, 0.04, 0.01
            ]))
            sys.stdout.write(char)
            sys.stdout.flush()
            if ((char == ".") or (char == "!")):
                time.sleep(0.5)
            if (char == ","):
                time.sleep(0.4)
            self.check_for_skip()

    def slow(self, *words):
        str = ''
        for item in words:
            str = str + item
        self.__skip_to_end = False
        # str += "\n"
        for i, char in enumerate(str):
            if self.__skip_to_end:
                sys.stdout.write(str[i:])
                sys.stdout.flush()
                break
            time.sleep(random.choice([
            0.06, 0.05, 0.03, 0.03,
            0.05, 0.03, 0.04, 0.05, 0.06, 0.04
            ]))
            sys.stdout.write(char)
            sys.stdout.flush()
            if ((char == ".") or (char == "!") or (char == ":") or (char == ";")):
                time.sleep(0.7)
            if (char == ","):
                time.sleep(0.4)
            self.check_for_skip()

    def slow_clean(self, *words):
        str = ''
        for item in words:
            str = str + item
        self.__skip_to_end = False
        # str += "\n"
        for i, char in enumerate(str):
            if self.__skip_to_end:
                sys.stdout.write(str[i:])
                sys.stdout.flush()
                break
            time.sleep(random.choice([
            0.06, 0.05, 0.03, 0.03,
            0.05, 0.03, 0.04, 0.05, 0.06, 0.04
            ]))
            sys.stdout.write(char)
            sys.stdout.flush()
            self.check_for_skip()

    def suspense(self, *words):
        str = ''
        for item in words:
            str = str + item
        self.__skip_to_end = False
        # str += "\n"
        for i, char in enumerate(str):
            if self.__skip_to_end:
                sys.stdout.write(str[i:])
                sys.stdout.flush()
                break
            time.sleep(random.choice([
            0.06, 0.05, 0.03, 0.03,
            0.05, 0.03, 0.04, 0.05, 0.06, 0.04
            ]) + 0.05)
            sys.stdout.write(char)
            sys.stdout.flush()
            if ((char == ".") or (char == "!") or (char == ":") or (char == ";")):
                time.sleep(0.7)
            if (char == ","):
                time.sleep(0.4)
            self.check_for_skip()

    def suspense_clean(self, *words):
        str = ''
        for item in words:
            str = str + item
        self.__skip_to_end = False
        # str += "\n"
        for i, char in enumerate(str):
            if self.__skip_to_end:
                sys.stdout.write(str[i:])
                sys.stdout.flush()
                break
            time.sleep(random.choice([
            0.06, 0.05, 0.03, 0.03,
            0.05, 0.03, 0.04, 0.05, 0.06, 0.04
            ]) + 0.05)
            sys.stdout.write(char)
            sys.stdout.flush()
            self.check_for_skip()

    def type(self, *words):
        str = ''
        for item in words:
            str = str + item
        self.__skip_to_end = False
        for i, char in enumerate(str):
            if self.__skip_to_end:
                sys.stdout.write(str[i:])
                sys.stdout.flush()
                break
            if self.__type_speed == "Default":
                time.sleep(random.choice([
                0.06, 0.05, 0.03, 0.03,
                0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                ]))
            if self.__type_speed == "Fast":
                time.sleep(random.choice([
                0.06, 0.05, 0.03, 0.03,
                0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                ]) - 0.01)
            if self.__type_speed == "Fastest":
                time.sleep(random.choice([
                0.06, 0.05, 0.03, 0.03,
                0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                ]) - 0.02)
            if self.__type_speed == "Print":
                time.sleep(0.001)

            sys.stdout.write(char)
            sys.stdout.flush()

            if self.__type_speed =="Default" and ((char == ".") or (char == "!") or (char == ";")):
                time.sleep(0.7)
            elif self.__type_speed =="Fast" and ((char == ".") or (char == "!") or (char == ";")):
                time.sleep(0.5)
            elif self.__type_speed =="Fastest" and ((char == ".") or (char == "!") or (char == ";")):
                time.sleep(0.4)

            if self.__type_speed =="Default" and (char == ","):
                time.sleep(0.4)
            elif self.__type_speed =="Fast" and (char == ","):
                time.sleep(0.3)
            elif self.__type_speed =="Fastest" and (char == ","):
                time.sleep(0.2)

            if self.__type_speed =="Default" and (char == "?") or (char == ":"):
                time.sleep(0.3)
            elif self.__type_speed =="Fast" and (char == "?") or (char == ":"):
                time.sleep(0.2)
            elif self.__type_speed =="Fastest" and (char == "?") or (char == ":"):
                time.sleep(0.1)
            
            self.check_for_skip()

    def type_clean(self, *words):
        str = ''
        for item in words:
            str = str + item
        self.__skip_to_end = False
        for i, char in enumerate(str):
            if self.__skip_to_end:
                sys.stdout.write(str[i:])
                sys.stdout.flush()
                break
            if self.__type_speed == "Default":
                time.sleep(random.choice([
                0.06, 0.05, 0.03, 0.03,
                0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                ]))
            if self.__type_speed == "Fast":
                time.sleep(random.choice([
                0.06, 0.05, 0.03, 0.03,
                0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                ]) - 0.01)
            if self.__type_speed == "Fastest":
                time.sleep(random.choice([
                0.06, 0.05, 0.03, 0.03,
                0.05, 0.03, 0.04, 0.05, 0.06, 0.04
                ]) - 0.02)
            if self.__type_speed == "Print":
                time.sleep(0.001)

            sys.stdout.write(char)
            sys.stdout.flush()

            if self.__type_speed =="Default" and (char == ","):
                time.sleep(0.4)
            elif self.__type_speed =="Fast" and (char == ","):
                time.sleep(0.3)
            elif self.__type_speed == "Fastest" and (char == ","):
                time.sleep(0.2)

            self.check_for_skip()

    def typeover(self, prompt, text, newline=False):
        """Print prompt, wait for any keypress, then overwrite the line with text."""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        # Clear keyboard buffer, then block until a key is pressed
        while msvcrt.kbhit():
            msvcrt.getch()
        msvcrt.getch()
        # Overwrite the prompt line with spaces, then carriage-return to start
        sys.stdout.write('\r' + ' ' * len(prompt) + '\r')
        sys.stdout.flush()
        self.fast(text)
        if newline:
            print()

    def cleanup(self):
        while msvcrt.kbhit():
            byte = msvcrt.getch()
            if byte == b' ':
                self.__skip_to_end = True
            elif byte == b',':
                self.__type_speed = "Default"
            elif byte == b'.':
                self.__type_speed = "Fast"
            elif byte == b'/':
                self.__type_speed = "Fastest"
            elif byte == b'p':
                self.__type_speed = "Print"

type = Type()
class Ask:
    def single_word(self, prompt=""):
        """Get a single word input (no spaces allowed). Returns the first word if multiple are entered."""
        while True:
            user_input = input(prompt).strip()
            if user_input:
                # Take only the first word (split on spaces)
                word = user_input.split()[0]
                return word
            # If empty, just return empty string
            return ""
    
    def choose_a_number(self, a, b, guess=False):
        while True:
            lucky_number = None
            while lucky_number is None:
                if guess==True:
                    type.fast_clean("What's your guess? ")
                else:
                    type.fast_clean("Choose a number between " + str(a) + " and " + str(b) + ": ")

                try:
                    lucky_number = int(input(""))
                except ValueError:
                    print("")
                    type.fast(red("That's, like, not a number."))
                    print()
            if a<=lucky_number<=b:
                return lucky_number
            elif guess==True:
                type.type("The number is between " + str(a) + " and " + str(b) + "!")
                print()
            else:
                type.type("That number isn't in the range!")
                print()

    def choose_an_option(self, options, reiterate="What? ", first_letter=True, ):
        while True:
            choice = input("").lower()
            for option in options:
                if (choice == option.lower()) or (choice == option[0].lower()):
                    return option
            type.type(reiterate) # type: ignore
    
    def option(self, prompt, options):
        """Standardized choice input - takes prompt and list of options"""
        labels = [str(option).strip() for option in options]
        option_text = "/".join(labels)
        prompt_text = prompt.strip()

        if prompt_text:
            if prompt_text.endswith(":"):
                rendered_prompt = prompt_text + " [" + option_text + "] "
            else:
                rendered_prompt = prompt_text + " [" + option_text + "]: "
        else:
            rendered_prompt = "Choose [" + option_text + "]: "
            
        attempts = 0
        while True:
            choice = input(rendered_prompt).strip().lower()
            for option in labels:
                if choice == option.lower():
                    return option
            if len(choice) == 1:
                matches = [option for option in labels if option and option[0].lower() == choice]
                if len(matches) == 1:
                    return matches[0]
            # If no match, show options again
            attempts += 1
            if attempts >= 3:
                labels.append(random.choice(["I can't choose", "You can't make me pick one", "I'm stalling because I won't play", "I don't wanna pick"]))
            type.type("Choose: " + option_text)
            print()

    def yes_or_no(self, reiterate="What? "):
        while True:
            yes_or_no = input("").strip().lower()
            if (yes_or_no in ["y", "yes", "yup", "yeah", "yep", "sure", "ok", "okay", "yay", "do it", "go for it"]):
                print()
                return "yes"
            elif (yes_or_no in ["n", "no", "nah", "nope", "nay", "not", "never"]):
                print()
                return "no"
            elif (yes_or_no in ["maybe", "idk", "not sure", "unsure"]):
                print()
                type.type(random.choice(["Maybe...Maybe not...", "Hmmmmm...I just can't make up my goddamn mind.", "Whew, all this thinking is making me dizzy!", "I suck at making decisions.", "Momma didn't raise no risk-taker..."]))
                print("\n")
                if(random.choice([True, False])):
                    return "yes"
                else:
                    return "no"
            else:
                type.type(reiterate)
                print()

    def give_cash(self, total, reiterate="How much? "):
        while True:
            try:
                value = int(input(""))
                if value < 0:
                    type.type("You can't give that!")
                    print()
                    type.type(reiterate)
                elif value > total:
                    type.type("You don't have that much cash!")
                    print()
                    type.type(reiterate)
                else:
                    print("")
                    return value
            except ValueError:
                print("")
                type.type(reiterate)

    def press_continue(self, message="Press any key to continue: "):
        type.type(message)
        is_pressed = False
        while not is_pressed:
            is_pressed = self.continue_cleanup()

    def continue_cleanup(self):
        while msvcrt.kbhit():
            return True