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

class EventDispatchMixin:
    """Event dispatch: day_event() and night_event() random event dispatchers"""

    def day_event(self):
        self.update_rank()
        
        # Broken state has random gameplay effects
        if self._is_broken and random.randrange(4) == 0:
            effect_type, value, message = self.broken_gameplay_effect()
            print()
            type.slow(red(message))
            if effect_type == "money_loss":
                type.type(red(" (-$" + str(value) + ")"))
            elif effect_type == "money_gain":
                type.type(green(" (+$" + str(value) + ")"))
            print()
            time.sleep(1)
        
        # Check for madness confrontation (rare, requires low sanity)
        if self.check_madness_confrontation():
            self.madness_confrontation()
            if not self._alive:
                return
            # If survived, continue to normal day event
        
        # Show sanity status if sanity is below 75
        if self._sanity <= 75 and random.randrange(5) == 0 and not self._is_broken:
            print()
            type.type("You feel " + yellow(self.get_sanity_description()) + ".")
            print()
        
        # Occasionally show sanity effects (more frequent at low sanity)
        if self.should_show_sanity_effect() and not self._is_broken:
            print()
            type.slow(cyan(self.get_sanity_effect()))
            print()
            time.sleep(1)
        
        # FATIGUE CHECK - Exhaustion can cause you to miss events
        if self.fatigue_blocks_event():
            type.type(self._lists.get_fatigue_blocked_text())
            print()
            return
        
        # COMPANION PASSIVE BONUSES - Applied each day
        self.apply_companion_day_bonuses()
        
        # HOARDING CONSEQUENCES - Too many items weigh you down
        item_count = len(self._inventory)
        if item_count >= 50:
            if random.randrange(3) == 0:
                type.type(yellow("Your car is bursting at the seams. Your companion can barely fit. Everything takes longer."))
                print()
                self.lose_sanity(5)
        elif item_count >= 40:
            if random.randrange(4) == 0:
                type.type(yellow("People stare at your overloaded car. You look like a hoarder on wheels."))
                print()
                self.lose_sanity(3)
        elif item_count >= 30:
            if random.randrange(5) == 0:
                type.type(yellow("The weight of your possessions slows you down. Finding anything takes time."))
                print()
                self.lose_sanity(2)
        elif item_count >= 20:
            if random.randrange(8) == 0:
                type.type(yellow("Your car is packed. You spend five minutes looking for your keys under all the stuff."))
                print()
        
        dayEvent = getattr(self, self._lists.get_day_event(), None)
        if dayEvent is None:
            type.type("The day passes uneventfully.")
            print()
            return
        # Track event for time_loop achievement
        event_name = dayEvent.__name__
        self._recent_events.append(event_name)
        if len(self._recent_events) > 3:
            self._recent_events.pop(0)
        if len(self._recent_events) == 3 and self._recent_events[0] == self._recent_events[1] == self._recent_events[2]:
            self.unlock_achievement("time_loop")
        # Track unique events and day event count
        self._unique_events_seen.add(event_name)
        self._day_events_count += 1
        dayEvent()
        return

    def night_event(self):
        self.update_rank()
        
        # Broken state has random effects at night too
        if self._is_broken and random.randrange(3) == 0:
            effect_type, value, message = self.broken_gameplay_effect()
            print()
            type.slow(red(message))
            if effect_type == "money_loss":
                type.type(red(" (-$" + str(value) + ")"))
            elif effect_type == "money_gain":
                type.type(green(" (+$" + str(value) + ")"))
            print()
            time.sleep(1)
        
        # Occasionally show sanity effects at night too (dreams are worse)
        if self.should_show_sanity_effect() and not self._is_broken:
            print()
            type.slow(cyan(self.get_sanity_effect()))
            print()
            time.sleep(1)
        
        nightEvent = getattr(self, self._lists.get_night_event(), None)
        if nightEvent is None:
            type.type("The night passes quietly.")
            print()
            self.add_fatigue(random.randint(2, 6))
            self.apply_companion_night_bonuses()
            self.update_rank()
            self.start_night()
            return
        # Track night events
        self._night_events_count += 1
        self._unique_events_seen.add(nightEvent.__name__)
        nightEvent()

        # Night events add mild fatigue (staying up doing things)
        self.add_fatigue(random.randint(2, 6))

        # COMPANION: Patches night_bonus - restore sanity at night
        self.apply_companion_night_bonuses()

        self.update_rank()
        self.start_night()


