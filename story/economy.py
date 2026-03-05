import random
import time
import sys
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\n\n"

type = typer.Type()
ask = typer.Ask()

# all the pretty colors
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

def italic(text):
    return (Style.DIM + text + Style.NORMAL)

def item(text):
    return magenta(bright(text))

def open_quote(text):
    return ("\"" + text)

def close_quote(text):
    return (text + "\"")

def quote(text):
    return ("\"" + text + "\"")

def space_quote(text):
    return ("\"" + text + "\" ")

class EconomyMixin:
    """Economy: Balance, rank, selling"""

    def sell_item_to_pawn(self, item_name, base_price):
        """Sell an item to the pawn shop"""
        modifier = self.get_pawn_price_modifier()
        final_price = int(base_price * modifier)
        
        if self.has_item(item_name):
            self.use_item(item_name)
            self._balance += final_price
            self._statistics["items_sold"] += 1
            self.change_pawn_reputation(2)  # Small reputation gain for successful sale
            return final_price
        return 0

    def get_balance(self):
        return self._balance

    def set_balance(self, value):
        self._balance = value

    def change_balance(self, value):
        print("\n")
        if (self._balance + value) <= 0:
            self._balance = 0
            type.type("Your new balance is " + red(bright("$0")))
        else:
            previous_balance = self._balance
            self._balance += value
            if value > 0:
                type.type("Your new balance is " + green(bright("${:,}".format(previous_balance) + " + ${:,}".format(value)) + bright(green(" = " + "${:,}".format(self._balance)))))
            elif value < 0:
                type.type("Your new balance is " + green(bright("${:,}".format(previous_balance))) + red(bright(" - ${:,}".format(abs(value)))) + green(bright(" = ${:,}".format(self._balance))))
        print("\n")

    def get_rank(self):
        return self._rank

    def update_rank(self):
        if(1<=self._balance<1000):
            self._rank = 0
        elif(1000<=self._balance<10000):
            self._rank = 1
        elif(10000<=self._balance<100000):
            self._rank = 2
        elif(100000<=self._balance<500000):
            self._rank = 3
        elif(500000<=self._balance<900000):
            self._rank = 4
        elif(900000<=self._balance<1000000):
            self._rank = 5
        else:
            self.status()
    
    def get_day(self):
        return self._day

    def get_gambling_stat(self, stat_name):
        """Get a specific gambling stat"""
        return self._gambling_stats.get(stat_name, 0)

    def increment_day(self): # really just for testing
        self._day+=1


