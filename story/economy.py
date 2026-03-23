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

    def can_see_fraudulent_cash(self):
        return hasattr(self, "has_item") and self.has_item("Marvin's Monocle")

    def visible_fraudulent_cash(self):
        return max(0, int(getattr(self, "_fraudulent_cash", 0))) if self.can_see_fraudulent_cash() else 0

    def _consume_fraudulent_cash(self, amount, dealer_receives=False):
        amount = max(0, int(amount))
        available = max(0, int(getattr(self, "_fraudulent_cash", 0)))
        consumed = min(amount, available)
        if consumed <= 0:
            return 0
        self._fraudulent_cash -= consumed
        if dealer_receives and hasattr(self, "_dealer_fake_cash_total"):
            self._dealer_fake_cash_total += consumed
        return consumed

    def spend_balance(self, amount, dealer_receives_fraud=False):
        amount = max(0, int(amount))
        if amount <= 0:
            return 0
        spent = min(amount, max(0, int(self._balance)))
        fake_spent = self._consume_fraudulent_cash(spent, dealer_receives=dealer_receives_fraud)
        self._balance -= spent
        return fake_spent

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
        self._balance = int(value)
        if hasattr(self, "_fraudulent_cash"):
            self._fraudulent_cash = max(0, min(int(self._fraudulent_cash), self._balance))

    def change_balance(self, value):
        # Achievement tracking before balance change
        old_balance = self._balance
        print()
        if (self._balance + value) <= 0:
            self._balance = 0
            self._was_broke = True
            if old_balance >= 950000:
                self._reached_950k = True
            if hasattr(self, "_fraudulent_cash"):
                self._fraudulent_cash = 0
            type.type("Your new balance is " + red(bright("$0")))
            print()
            self.status()
            return
        else:
            previous_balance = self._balance
            if value > 0:
                self._balance = int(self._balance + value)
                type.type("Your new balance is " + green(bright("${:,}".format(previous_balance) + " + ${:,}".format(value)) + bright(green(" = " + "${:,}".format(self._balance)))))
            elif value < 0:
                self.spend_balance(abs(int(value)), dealer_receives_fraud=False)
                type.type("Your new balance is " + green(bright("${:,}".format(previous_balance))) + red(bright(" - ${:,}".format(abs(value)))) + green(bright(" = ${:,}".format(self._balance))))
            if self.can_see_fraudulent_cash():
                print()
                type.type(cyan("The monocle reveals ") + yellow(bright("${:,}".format(self.visible_fraudulent_cash()))) + cyan(" in hot money."))
        # Achievement balance tracking
        if self._balance >= 950000:
            self._reached_950k = True
        if self._balance >= 1000000:
            self._was_millionaire_ach = True
        # Track big swings (crossing 100k boundary) for yo_yo
        now_above = self._balance >= 100000
        if hasattr(self, '_last_swing_above') and now_above != self._last_swing_above:
            self._big_swing_count += 1
        self._last_swing_above = now_above
        print()

    def get_rank(self):
        return self._rank

    def update_rank(self):
        if(1<=self._balance<1000):
            self._rank = 0
        elif(1000<=self._balance<10000):
            self._rank = 1
        elif(10000<=self._balance<100000):
            self._rank = 2
        elif(100000<=self._balance<400000):
            self._rank = 3
        elif(400000<=self._balance<750000):
            self._rank = 4
        elif(750000<=self._balance<1000000):
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


