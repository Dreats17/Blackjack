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

class DayCycleMixin:
    """Day cycle: end_day, first_setup, opening_lines, start_night"""

    def end_day(self):
        if(self.has_danger("Angry Dealer")):
            self.lose_danger("Angry Dealer")
            self.end_day_angry_dealer()
        elif(self._day==1):
            self.end_day_1()
        elif(not self.has_item("Car")):
            self.end_day_car_broken()
        else:
            self.end_day_car_fixed()

        # Durability updates always happen
        self.update_dirty_old_hat_durability()
        self.update_golden_watch_durability()

        # Check for dream event — replaces the day summary entirely
        # Stats still update behind the scenes, but the player misses out on the info
        dream = self._get_pending_dream()
        if dream is not None:
            # Silent stat updates — no summary text shown
            self._day += 1
            self._previous_balance = self._balance
            self.heal(random.choice([1, 3, 5]))
            # Show the dream instead of the summary
            print("\n")
            dream()
            ask.press_continue("Press a key to continue: ")
            return

        # Normal day summary
        print("\n")
        type.fast(bright(green("═" * 50)))
        type.fast(bright(green("            ~ ~ ~ Day Summary ~ ~ ~")))
        type.fast(bright(green("═" * 50)))
        print("\n")

        # Starting cheer (eg. Yippee!)
        type.type(self._lists.get_cheer())

        # Tells day count and previous day's balance
        if self._day == 1:
            type.type(" You've survived " + yellow(bright(str(self._day) + " day")) + "!")
            print("\n")
            type.type("You started your journey with just " + green(bright("$" + str(self._previous_balance))) + ". ")
        else:
            type.type(" You've survived " + yellow(bright(str(self._day) + " days")) + "!")
            print("\n")
            type.type("Yesterday, at this time, you had " + green(bright("$" + str(self._previous_balance))) + ". ")
        # increments day
        self._day += 1

        print("")

        # Tells you the change in your balance, and if you gained or lost money
        change_in_balance = self._balance - self._previous_balance
        if change_in_balance > 0: type.type("Since then, you've accumulated " + green(bright("$" + str(change_in_balance))) + ". ")
        elif change_in_balance < 0: type.type("Since then, you've managed to lose " + red(bright("$" + str(abs(change_in_balance)))) + ". ")
        else: type.type("Somehow, your net earnings today was 0. Goose egg. No money. Disappointing. ")

        # Sets previous balance to current balance, so that it's ready for next day
        self._previous_balance = self._balance

        print("")

        # Tells you your current balance
        type.type("That brings you to a grand total of " + green(bright("$" + str(self._balance))) + "! ")

        type.type(self._lists.get_rank_comment(self._rank))

        print("\n")

        # Gives a little personal advice, support, etc
        type.type(self._lists.get_advice())

        print()

        # Gives one last quote before starting the next day
        type.type(self._lists.get_quote_setup())
        type.type(self._lists.get_quote())

        # Heals the player before the next day
        print("\n")
        self.heal(random.choice([1, 3, 5]))

        ask.press_continue("Press a key to continue: ")

    def _get_pending_dream(self):
        """Check if a dream event should fire tonight, replacing the day summary.
        Dreams are tied to wealth tiers matching when they originally appeared.
        Returns the dream event method or None."""
        eligible = []
        balance = self.get_balance()

        # Tom dream chain
        if self.get_tom_dreams() == 0 and balance >= 1000:
            eligible.append(self.remember_rebecca)
        elif self.get_tom_dreams() == 1 and balance >= 10000:
            eligible.append(self.remember_nathan)
        elif self.get_tom_dreams() == 2 and balance >= 500000:
            eligible.append(self.remember_johnathan)

        # Frank dream chain
        if self.get_frank_dreams() == 0 and balance >= 1000:
            eligible.append(self.dealers_anger)
        elif self.get_frank_dreams() == 1 and balance >= 10000:
            eligible.append(self.dealers_scar)
        elif self.get_frank_dreams() == 2 and balance >= 500000:
            eligible.append(self.dealers_revolver)
        elif self.get_frank_dreams() == 3 and balance >= 100000 and not self.has_met("Dealer Dream Complete"):
            eligible.append(self.dealer_in_dreams)

        # Oswald dream chain
        if self.get_oswald_dreams() == 0 and balance >= 1000:
            eligible.append(self.casino_bar)
        elif self.get_oswald_dreams() == 1 and balance >= 10000:
            eligible.append(self.casino_table)
        elif self.get_oswald_dreams() == 2 and balance >= 500000:
            eligible.append(self.casino_riches)

        # Combined finale — requires significant progress in all chains
        if (self.get_tom_dreams() >= 2 and self.get_frank_dreams() >= 2 and
            self.get_oswald_dreams() >= 2 and balance >= 900000 and
            not self.has_met("Final Dream")):
            eligible.append(self.final_dream)

        if not eligible:
            return None

        # 30% chance a dream fires on any given night
        if random.randrange(100) < 30:
            return random.choice(eligible)

        return None


    # Opening
    def first_setup(self):

        while (True):
            type.type("Type 'y' or 'yes', not case sensitive, to say yes to a question: ")
            yes_or_no = input("").lower()
            if (yes_or_no == "y") or (yes_or_no == "yes"):
                break
            else:
                print()
        print("\n")

        while (True):
            type.type("Type 'n' or 'no', not case sensitive, to say no to a question: ")
            yes_or_no = input("").lower()
            if (yes_or_no == "n") or (yes_or_no == "no"):
                break
            else:
                print()
        print("\n")

        while (True):
            type.type("Type 'h' or 'hit', not case sensitive, to hit your hand: ")
            hit_or_stand = input("").lower()
            if (hit_or_stand == "h") or (hit_or_stand == "hit"):
                break
            else:
                print()
        print("\n")

        while (True):
            type.type("Type 's' or 'stand', not case sensitive, to stand with your hand's value: ")
            hit_or_stand = input("").lower()
            if (hit_or_stand == "s") or (hit_or_stand == "stand"):
                break
            else:
                print()
        print("\n")

    def opening_lines(self):

        type.type("\"Ugh, not again,\" you spout as the old wagon shutters, then dies. ")
        type.type("Stranded on the road again, but this time, your money has gone dry. ")
        type.type("All but your 50 dollar bill that Grandma gave you on her last Christmas. ")
        type.type("You've been saving it for when you needed it most, but surely, it won't be enough.")
        print("\n")

        type.type("The door creaks open, and you step out into the night sky, coughing up the smoke from your fried vehicle. ")
        type.type("After pushing your car off the road and between the trees, there isn't much else left for you to do, ")
        type.type("so you begin to wander down the dark, lonely street.")
        print("\n")

        type.type("But at the end of the road, where concrete turned to stone turned to dirt, you notice a light up ahead, on the top of a hill. ")
        print("\n")

        type.type("As you waltz into the old, wooden shack, your eyes begin to light up with the fire of a thousand suns. ")
        type.type("Roulette wheels! Poker tables! And in a dark corner of the abandoned casino, sits a dealer, shuffling cards for a new round of Blackjack. ")
        type.type("That 50 dollars might just come in handy after all. Thanks, Grandma!")
        print("\n")

        type.type("As you go to sit down at the table, you hear the Dealer cough, then watch as he sits up.")
        print("\n")

        type.type("In a deep, and yet strained voice, the Dealer, cloaked in darkness, poses a question to you.")
        print("\n")
        self.start_night()

    # End Days
    def end_day_1(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questioning his word, and with your winnings in hand, you scurry to the door, eager to get some sleep after such a long day. ")
        type.type("Making it back to your car, ditched on the side of the road, but no longer engulfed in smoke, you lay down, and close your eyes. It's time to rest.")

    def end_day_car_broken(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questioning his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")

    def end_day_car_fixed(self):
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questioning his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("You make it to your car and drive away from the casino, ")
        type.type("and you park in a little alcove on the side of the road. ")
        type.type("You lay down, and close your eyes. It's time to rest.")

    def end_day_wind(self):
        self.remove_travel_restriction("Wind")
        type.type("After playing a few rounds of Blackjack, the dealer points to the door. ")
        type.type("Without questioning his word, and with your winnings in hand, you scurry to the door, eager to get some sleep. ")
        type.type("Stepping outside, you notice that the wind has calmed down. That's a relief. ")
        type.type("Making it back to your car, ditched on the side of the road, you lay down, and close your eyes. It's time to rest.")


    def end_day_angry_dealer(self):
        type.type("You've never seen the dealer quite so angry. Fortunately, you make it back to your car, and immediately pass out for the night. It's time to rest.")

    def start_night(self):
        if(self._day==1):
            self.start_night_1()
        elif self.has_travel_restriction("Wind"):
            self.end_day_wind()
        elif(not self.has_item("Car")):
            self.start_night_car()
        else:
            self.start_night_car_fixed()

    def start_night_1(self):
        type.slow(red("Would you like to play a game of Blackjack? "))
        yes_or_no = input("").lower()
        print()
        if (yes_or_no == "n") or (yes_or_no == "no"):
            type.slow(red(bright("Well that's just too bad, isn't it. ")))
            type.slow(red("The Dealer fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take the last 50 dollars from your lifeless body."))
            self.kill()

    def start_night_car(self):
        type.type("As the sun begins to set, and the stars light up in the night sky, you walk to the casino, eager to play more Blackjack. ")
        print("\n")
        # Broken state casino perception
        if self._is_broken:
            broken_casino = random.choice([
                "The casino looks different tonight. The walls are wrong. The angles don't make sense. You go in anyway.",
                "You can hear the slot machines screaming. No one else seems to notice.",
                "The casino is upside down. No. It's not. It never was. You're fine. You're fine.",
                "Every patron in the casino has your face. You blink. They don't anymore. Did they ever?",
                "The door opens before you touch it. It was expecting you."
            ])
            type.slow(red(broken_casino))
            print("\n")
        # Low sanity affects how you perceive the casino
        elif self._sanity <= 50:
            type.slow(cyan("The casino lights seem too bright. Too hungry. They're watching you."))
            print("\n")
        elif self._sanity <= 75:
            type.type("You feel " + yellow(self.get_sanity_description()) + " tonight.")
            print("\n")
        self.grandfather_clock_dialogue()
        type.slow(red(self._lists.get_dealer_welcome()))
        print("\n")

    def start_night_car_fixed(self):
        type.type("As the sun begins to set, and the stars light up in the night sky, you drive over to the casino, eager to play more Blackjack. ")
        print("\n")
        # Broken state casino perception
        if self._is_broken:
            broken_casino = random.choice([
                "You don't remember driving here. You don't remember getting in the car. You're at the casino now.",
                "The steering wheel felt like bones under your fingers. Human bones. Car bones. Same thing.",
                "The casino is on fire. No. It's just the sunset. Probably.",
                "Your reflection in the car window stayed behind when you got out. It's fine. You don't need it.",
                "The parking lot has too many cars. They're all yours. From timelines that didn't happen."
            ])
            type.slow(red(broken_casino))
            print("\n")
        # Low sanity affects how you perceive the casino
        elif self._sanity <= 50:
            type.slow(cyan("The neon signs blur together. For a moment, you can't remember why you came here."))
            print("\n")
        elif self._sanity <= 75:
            type.type("You feel " + yellow(self.get_sanity_description()) + " tonight.")
            print("\n")
        self.grandfather_clock_dialogue()
        type.slow(red(self._lists.get_dealer_welcome()))
        print("\n")

    def grandfather_clock_dialogue(self):
        if self.has_item("Grandfather Clock") and random.randrange(10) == 0:
            dialogue = random.choice([
                "The Dealer stares at the massive clock bulging out of your pocket. " + quote("Is that a grandfather clock in your pocket, or are you just happy to see me?") + " He pauses. " + quote("Wait. That's actually a grandfather clock. Why do you have that."),
                "The Dealer squints at your pocket. " + quote("Son, I've seen a lot of things in my years, but I ain't never seen a man stuff a whole grandfather clock down his pants. You got issues."),
                "As you sit down, the Grandfather Clock lets out a loud " + bright("BONG") + ". The Dealer flinches. " + quote("Jesus Christ, boy! You trying to give an old man a heart attack? Keep that thing quiet or I'll use it as firewood."),
                "The Dealer watches you struggle to sit down with the clock. " + quote("You know, most folks just check the time on their phone. But I respect the commitment to being absolutely ridiculous."),
                "The Grandfather Clock chimes midnight. The Dealer looks at his watch. " + quote("It's 7 PM.") + " He sighs. " + quote("That thing's about as reliable as my ex-wife.")
            ])
            type.slow(red(dialogue))
            print("\n")



    # Poor Day Events (1 - 1,000)
    # Everytime

