import random
import time
import sys
import lists
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\n"

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""
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

from story import storylines

# ============================================
# FOOD & CONSUMABLE ITEM DATA
# ============================================
# Each food: heal, sanity, fatigue_reduce, energy (bool), companion_food (bool)
FOOD_DATA = {
    "Candy Bar":         {"heal": 5,  "sanity": 1, "fatigue_reduce": 0,  "energy": False, "companion_food": True},
    "Bag of Chips":      {"heal": 8,  "sanity": 0, "fatigue_reduce": 0,  "energy": False, "companion_food": False},
    "Turkey Sandwich":   {"heal": 15, "sanity": 2, "fatigue_reduce": 0,  "energy": False, "companion_food": True},
    "Energy Drink":      {"heal": 3,  "sanity": 0, "fatigue_reduce": 25, "energy": True,  "companion_food": False},
    "Beef Jerky":        {"heal": 12, "sanity": 0, "fatigue_reduce": 0,  "energy": False, "companion_food": True},
    "Cup Noodles":       {"heal": 10, "sanity": 2, "fatigue_reduce": 0,  "energy": False, "companion_food": False},
    "Granola Bar":       {"heal": 7,  "sanity": 0, "fatigue_reduce": 0,  "energy": False, "companion_food": True},
    "Hot Dog":           {"heal": 8,  "sanity": 0, "fatigue_reduce": 0,  "energy": False, "companion_food": True},
    "Microwave Burrito": {"heal": 9,  "sanity": 0, "fatigue_reduce": 0,  "energy": False, "companion_food": False},
}

from story.systems import SystemsMixin
from story.economy import EconomyMixin
from story.day_cycle import DayCycleMixin
from story.events_day_survival import DaySurvivalMixin
from story.events_day_people import DayPeopleMixin
from story.events_day_animals import DayAnimalsMixin
from story.mechanics_intro import MechanicsStorylineMixin
from story.events_day_casino import DayCasinoMixin
from story.events_day_wealth import DayWealthMixin
from story.events_day_dark import DayDarkMixin
from story.events_day_companions import DayCompanionsMixin
from story.events_day_items import DayItemsMixin
from story.events_day_surreal import DaySurrealMixin
from story.events_day_numbers import DayNumbersMixin
from story.events_day_storylines import DayStorylinesMixin
from story.events_illness import IllnessMixin
from story.events_car import CarEventsMixin
from story.events_night import NightEventsMixin
from story.adventures import AdventuresMixin
from story.game_flow import GameFlowMixin
from story.locations import LocationsMixin
from story.durability import DurabilityMixin
from story.event_dispatch import EventDispatchMixin
from story.endings import EndingsMixin

class Player(
    SystemsMixin,
    EconomyMixin,
    DayCycleMixin,
    DaySurvivalMixin,
    DayPeopleMixin,
    DayAnimalsMixin,
    MechanicsStorylineMixin,
    DayCasinoMixin,
    DayWealthMixin,
    DayDarkMixin,
    DayCompanionsMixin,
    DayItemsMixin,
    DaySurrealMixin,
    DayNumbersMixin,
    DayStorylinesMixin,
    IllnessMixin,
    CarEventsMixin,
    NightEventsMixin,
    AdventuresMixin,
    GameFlowMixin,
    LocationsMixin,
    DurabilityMixin,
    EventDispatchMixin,
    EndingsMixin,
):

    def __init__(self):
        self._name = None
        self._alive = True
        self._is_sick = False
        self._is_injured = False
        self._flask_effects = set()
        self._status_effects = set()
        self._injuries = set()
        self._travel_restrictions = set()
        self._clear_status = False
        self._clear_all_status = False
        self._inventory = set()
        self._item_use_counts = {}
        self._broken_inventory = set()
        self._repairing_inventory = set()
        self._dangers = set()
        self._met = set()
        self._mechanic_visits = 0
        self._health = 100
        self._balance = 50
        self._previous_balance = 50
        self._today_winnings = 0
        self._balance_at_day_start = 50
        self._rank = 0
        self._day = 1
        self._counting_days = [0] * 13
        self._item_durability = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # [delight_indicator, health_indicator, dirty_old_hat, golden_watch, enchanting_silver_bar, sneaky_peeky_shades, quiet_sneakers, faulty_insurance, lucky_coin, worn_gloves, tattered_cloak, rusty_compass, pocket_watch, gamblers_chalice, twins_locket, white_feather, dealers_grudge, gamblers_grimoire]
        self._flask_durability = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # [no_bust, imminent_blackjack, dealers_whispers, bonus_fortune, anti_venom, anti_virus, fortunate_day, fortunate_night, second_chance, split_serum, dealers_hesitation, pocket_aces]
        self._round_count = 3
        self._is_religious = False
        self._prereqs = [False, False, False, False, False]
        self._prereqs_done = [False, False, False, False, False]
        self._convenience_store_inventory = []
        self._tom_dreams = 0      # 0=none, 1=rebecca, 2=nathan, 3=johnathan (ready for ending)
        self._frank_dreams = 0    # 0=none, 1=dealers_anger, 2=dealers_scar, 3=dealers_revolver (ready for ending)
        self._oswald_dreams = 0   # 0=none, 1=casino_bar, 2=casino_table, 3=casino_riches (ready for ending)
        self._visited_tanya = 0   # Tracks how many times player has visited Tanya's therapy office
        self._tanya_skip_night = False  # If True, player stays in car tonight instead of gambling
        self._skip_blackjack_tonight = False  # Signal to Blackjack.play_round() to skip
        # Gambling stats for Gambler's Grimoire
        self._gambling_stats = {
            "total_hands": 0,
            "wins": 0,
            "losses": 0,
            "blackjacks": 0,
            "busts": 0,
            "ties": 0,
            "biggest_win": 0,
            "biggest_loss": 0,
            "current_streak": 0,
            "best_win_streak": 0,
            "worst_loss_streak": 0,
            "total_won": 0,
            "total_lost": 0,
            "double_downs_won": 0,
            "splits_won": 0,
            "surrenders_used": 0,
            "insurance_collected": 0
        }
        self._favorite_color = None
        self._favorite_animal = None
        self._rabbit_chase = 0    # 0-6 tracking which rabbit chase event is next
        self._recent_events = []  # Track last 3 day event names for time_loop achievement
        self._is_millionaire = False  # True when player hits $1M for the first time
        self._millionaire_visited = False  # True after the special morning visitor comes
        self._chosen_mechanic = None  # Which mechanic the millionaire visitor tells you to see ("Tom", "Frank", or "Oswald")
        self._necronomicon_readings = 0  # Cumulative Necronomicon use counter - increases madness
        self._car_mechanic = None  # Which mechanic actually fixed the player's car during progression
        self._gus_items_sold = set()  # Tracks which collectibles have been sold to Gus
        self._sanity = 100  # Visible stat - starts at 100, decreases with trauma
        self._fatigue = 0  # 0-100: 0=well-rested, 100=exhausted. Affects sleep quality and event access.
        self._sanity_warnings_shown = 0  # Tracks how many sanity warnings have been shown
        self._faced_madness = False  # True after surviving the confrontation
        self._is_broken = False  # True when sanity hits 0 and you survive
        
        # ACHIEVEMENT TRACKING — flags, counters, and sets for achievement triggers
        self._was_broke = False              # Set when balance hits 0 (for rock_bottom)
        self._was_low_sanity = False          # Set when sanity < 25 (for sanity_saved)
        self._reached_950k = False            # Set when balance >= 950k (for near_miss)
        self._was_millionaire_ach = False     # Set when balance >= 1M (for broke_millionaire)
        self._big_swing_count = 0             # Times balance crossed 100k threshold (for yo_yo)
        self._last_swing_above = False        # Was last big-swing state above 100k?
        self._consecutive_injury_days = 0     # Consecutive days with injury (for injured_survival)
        self._consecutive_sick_days = 0       # Consecutive days while sick (for sick_survival)
        self._days_low_health = 0             # Days under 25 health (for low_health_master)
        self._days_low_sanity = 0             # Days under 30 sanity (for sanity_master)
        self._days_dealer_low = 0             # Days with dealer happiness < 5 (for zero_happiness_survivor)
        self._days_dealer_high = 0            # Consecutive days with dealer >= 90 (for dealer_friend)
        self._days_with_cursed = 0            # Days holding a cursed item (for cursed_survival)
        self._night_events_count = 0          # Total night events experienced (for night_owl)
        self._day_events_count = 0            # Total day events experienced (for morning_person - counts day events)
        self._unique_events_seen = set()      # Unique event function names (for event_collector)
        self._flask_types_used = set()        # Flask types ever used (for flask_connoisseur)
        self._items_ever_owned = set()        # All items ever owned (for every_item)
        self._items_ever_used = set()         # All items ever consumed (for item_master)
        self._companion_types_owned = set()   # Companion types ever owned (for every_companion)
        self._total_shop_spending = 0         # Total money spent at shops (for shop_spender)
        self._total_given_away = 0            # Total money given away (for philanthropist)
        self._sanity_ever_below_50 = False    # Flag for iron_will (set when sanity drops below 50)
        self._ever_took_loan = False          # Flag for no_loans
        self._ever_gave_gift = False          # Flag for no_gifts
        self._ever_bought_item = False        # Flag for never_shop
        self._companions_lost_count = 0       # Companions that ran away (for pet_cemetery)
        self._dealer_happiness_day_start = 50 # Snapshot for happiness_rollercoaster
        self._debt_spiral_count = 0           # Times took loan while in debt (for debt_spiral)
        self._tony_survived_count = 0         # Times survived Tony (for tony_survivor)
        self._bad_gifts_given = 0             # Gifts that lowered dealer happiness (for gift_of_death)
        self._last_dollar_bets = 0            # Times bet last dollar (for suicide_gambler)
        self._achievement_check_count = 0     # Times checked achievements (for achievement_hunter)
        self._shops_visited_today = set()     # Shops visited today (for all_shops_one_day / shop_hopper)
        self._locations_visited_today = set() # Locations visited today (for nomad)
        self._days_at_camp = 0                # Consecutive days staying at camp (for hermit)
        self._days_not_spending = 0           # Consecutive days at 500k+ without spending (for money_hoarder)
        self._oswald_upgrades = 0             # Total Oswald upgrades done (for oswald_masterwork)
        self._daily_hands_won = 0             # Hands won today (for perfect_day)
        self._daily_hands_lost = 0            # Hands lost today (for worst_day)
        self._daily_hands_total = 0           # Total hands today
        self._ever_lost_hand = False          # Flag for perfect_record
        self._ever_bet_above_min = False      # Flag for minimum_bet
        self._blackjack_recent = []           # Recent 10 hand results for blackjack_streak
        self._no_bust_count = 0               # Consecutive hands without busting (for no_bust_streak/never_bust)
        self._dealer_bust_streak = 0          # Consecutive dealer busts (for dealer_bust_streak)
        self._dealer_bj_losses = 0            # Times lost to dealer blackjack (for dealer_blackjack_victim)
        self._insurance_failures = 0          # Insurance taken without dealer BJ (for insurance_failure)
        self._twenty_one_pushes = 0           # Push with 21 count (for twenty_one_push)
        self._natural_blackjacks = 0          # Total natural blackjacks (for blackjack_natural)
        
        # ACHIEVEMENT SYSTEM - Tracks unlocked achievements
        self._achievements = set()
        
        # STATISTICS TRACKING
        self._statistics = {
            "days_survived": 0,
            "total_money_earned": 0,
            "total_money_spent": 0,
            "highest_balance": 50,
            "lowest_balance": 50,
            "items_collected": 0,
            "items_sold": 0,
            "events_experienced": 0,
            "people_met": 0,
            "injuries_sustained": 0,
            "illnesses_contracted": 0,
            "near_death_experiences": 0,
            "companions_befriended": 0,
            "loans_taken": 0,
            "loans_repaid": 0,
            "total_borrowed": 0,
            "total_repaid": 0,
            "times_robbed": 0,
            "times_hospitalized": 0,
            "mechanic_visits": 0,
            "doctor_visits": 0,
            "witch_doctor_visits": 0,
            "casino_visits": 0,
            "pawn_shop_visits": 0,
            "marvin_visits": 0,
            "loan_shark_visits": 0,
        }
        
        # COMPANION SYSTEM - Tracks active companions and their states
        self._companions = {
            # "name": {"status": "alive/dead/lost", "happiness": 0-100, "days_owned": 0, "fed_today": False}
        }
        
        # LOAN SHARK SYSTEM
        self._loan_shark_debt = 0
        self._loan_shark_days_overdue = 0
        self._loan_shark_warning_level = 0  # 0=none, 1=warning, 2=threat, 3=violence, 4=death
        self._loan_shark_interest_rate = 0.20
        self._loan_shark_fee_rate = 0.0
        self._loan_shark_monocle_penalty_triggered = False
        
        # PAWN SHOP REPUTATION
        self._pawn_shop_reputation = 50  # 0-100, affects prices
        
        # COMPANION BETRAYAL TRACKING
        self._companions_sold_count = 0  # Track how many companions sold to Gus for the dark ending
        
        # WITCH DOCTOR SYSTEM
        self._witch_doctor_declined_count = 0  # Tracks how many times player has declined her services
        self._witch_doctor_killed = False  # True if player has killed the witch doctor
        # FRAUDULENT CASH SYSTEM (Loan Shark)
        self._fraudulent_cash = 0  # Hot money hidden inside the visible bankroll
        self._dealer_fake_cash_total = 0  # How much fake cash the Dealer has accumulated
        
        # DEALER HAPPINESS SYSTEM
        self._dealer_happiness = 50  # 0-100, affects his behavior and dialogue
        
        # GIFT WRAPPING SYSTEM (Kyle's Convenience Store)
        self._gift_wrapped_item = None  # Currently wrapped gift to give to Dealer
        self._convenience_store_purchases = 0  # Track purchases to unlock gift system
        self._gift_system_unlocked = False  # Unlocks after 3-5 purchases + out of poor rank
        
        self._lists = lists.Lists(self)
        
        # STORYLINE SYSTEM - Manages sequential multi-part narrative events
        self._storyline_system = storylines.StorylineSystem(self)
        self._storyline_system.sync_with_existing_state()

    def kill(self, cause_of_death=None):
        self._alive = False
        self.status()

    def hurt(self, value):
        # First Aid Kit can be used to reduce a big hit (consumed)
        if self.has_item("First Aid Kit") and value >= 15:
            self.use_item("First Aid Kit")
            reduced = value // 2
            value = value - reduced
            type.type("You use your " + magenta(bright("First Aid Kit")) + " to patch yourself up!")
            print()
        
        # LifeAlert can save you from death once
        if (self._health - value <= 0) and self.has_item("LifeAlert"):
            self.use_item("LifeAlert")
            type.slow(red(bright("You collapse... but your LifeAlert activates!")))
            print()
            type.type("Emergency services arrive just in time. You're rushed to the hospital.")
            print()
            self.increment_statistic("times_hospitalized")
            self.increment_statistic("near_death_experiences")
            self.lose_sanity(8)

            emergency_bill = int((random.randint(15, 35) / 100) * self._balance)
            if self.has_item("Real Insurance"):
                type.type("You barely manage to flash your " + bright(cyan("Real Insurance")) + " card before they wheel you inside.")
                print()
                type.type("They patch you up and waive the bill. Your LifeAlert has been used up.")
                self.update_faulty_insurance_durability()
            elif self.has_item("Faulty Insurance"):
                type.type("You shakily hand over your " + bright(magenta("Faulty Insurance")) + " card while the paramedics argue with admissions.")
                print()
                emergency_bill = int((random.randint(5, 20) / 100) * self._balance)
                type.type("They patch you up and slap you with a reduced emergency bill of " + red(bright("${:,}".format(emergency_bill))) + ".")
                self.change_balance(-emergency_bill)
                self.update_faulty_insurance_durability()
            else:
                type.type("They patch you up and send you on your way. Your LifeAlert has been used up.")
                print()
                if emergency_bill > 0:
                    type.type("Emergency bill: " + red(bright("${:,}".format(emergency_bill))) + ".")
                    self.change_balance(-emergency_bill)
            self._health = 25  # Survive with 25 health
            print()
            return
        
        if(self._health - value <= 0):
            self._health = 0
            type.slow(red(bright("You have succumbed to your wounds.")))
            self.kill()
        else:
            self._health -= value
        if self.has_item("Health Manipulator"):
            type.type("The " + cyan(bright("Health Manipulator")) + " embedded in your arm pulses with warning.")
            print()
            type.type("You took damage!")
            print()
            self.health_indicator()
        elif self.has_item("Health Indicator"):
            type.type("The " + magenta(bright("Health Indicator")) + " on your wrist makes a loud beep.")
            print()
            type.type("You took damage!")
            print()
            self.health_indicator()

    def heal(self, value):
        if(self._health + value >= 100):
            self._health = 100
        else:
            self._health += value
        if self.has_item("Health Manipulator"):
            type.type("The " + cyan(bright("Health Manipulator")) + " embedded in your arm hums with satisfaction.")
            print()
            type.type("You regained health!")
            print()
            self.health_indicator()
        elif self.has_item("Health Indicator"):
            type.type("The " + magenta(bright("Health Indicator")) + " on your wrist makes a subtle vibration.")
            print()
            type.type("You regained health!")
            print()
            self.health_indicator()

    def set_health(self, value):
        self._health = value

    def get_health(self):
        return self._health

    def health_indicator(self):
        if self._health > 66:
            type.type("Your current health: " + bright(green(str(self._health) + "%")))
        elif self._health > 33:
            type.type("Your current health: " + bright(yellow(str(self._health) + "%")))
        else:
            type.type("Your current health: " + bright(red(str(self._health) + "%")))
        print()
        self.update_health_indicator_durability()

    def status(self, cause_of_death=None):
        if not self._alive:
            print()
            type.slow("You have died!")
            print()
            if self._day == 1: type.slow("You didn't even last " + bright(yellow(str(self._day) + " day")) + ". That's embarrassing.")
            elif self._day == 2: type.slow("You lasted " + bright(yellow(str(self._day-1) + " day")) + ".")
            else: type.slow("You lasted " + bright(yellow(str(self._day) + " days")) + "!")
            print()
            type.slow("You met your fate with a final balance of " + green(bright("${:,}".format(self._balance))))
            print()
            if self._day <= 5:
                self.unlock_achievement("quick_death")
            self.display_final_achievements()
            type.slow("The police were able to recover your body, but nobody cared enough to show up to your funeral.")
            quit()
        elif (self._balance == 0):
            print()
            type.slow("You have run out of money!")
            print()
            if self._day == 1: type.slow("You didn't even last " + bright(yellow(str(self._day) + " day")) + ". That's absurdly sad.")
            elif self._day == 2: type.slow("You lasted " + bright(yellow(str(self._day-1) + " day")) + ".")
            else: type.slow("You lasted " + bright(yellow(str(self._day) + " days")) + "!")
            print()
            type.slow("With no cash left to play Blackjack, your source of income has been rendered useless.")
            print()
            self.display_final_achievements()
            type.slow("You spend your remaining days going hungry, wondering what life could've been, if you didn't lose that one hand.")
            quit()
        elif (self._balance >= 1000000) and (not self._is_millionaire):
            # First time hitting $1M - set flag but don't end game yet
            self._is_millionaire = True
            print()
            type.slow(green(bright("You've done it. You've hit $1,000,000.")))
            print()
            type.slow("The Dealer stares at you with an expression you've never seen before. Is that... " + yellow("respect?"))
            print()
            type.slow("Something tells you that tomorrow morning is going to be different.")
            print()
    
    def get_name(self):
        return self._name

    def is_religious(self):
        return self._is_religious
    
    def lists(self):
        return self._lists
    
    def add_travel_restriction(self, restriction):
        self._travel_restrictions.add(restriction)

    def has_travel_restriction(self, restriction):
        return restriction in self._travel_restrictions
    
    def remove_travel_restriction(self, restriction):
        self._travel_restrictions.remove(restriction)

    def add_flask(self, flask):
        self._flask_effects.add(flask)
        self._flask_types_used.add(flask)
        if not self.has_achievement("first_flask"): self.unlock_achievement("first_flask")

    def has_flask_effect(self, flask):
        return flask in self._flask_effects
    
    def remove_flask_effect(self, flask):
        self._flask_effects.remove(flask)

    def len_flasks(self):
        return len(self._flask_effects)

    def add_status(self, status):
        if status not in self._status_effects:
            self.increment_statistic("illnesses_contracted")
        self._status_effects.add(status)

    def has_status(self, status):
        return status in self._status_effects
    
    def remove_status(self, status):
        self._status_effects.remove(status)

    def add_injury(self, injury):
        if injury not in self._injuries:
            self.increment_statistic("injuries_sustained")
        self._injuries.add(injury)

    def has_injury(self, injury):
        return injury in self._injuries
    
    def heal_injury(self, injury):
        self._injuries.remove(injury)

    def len_status(self):
        return len(self._status_effects)
    
    def get_rounds(self):
        return self._round_count
    
    def set_rounds(self, value):
        self._round_count = value

    def add_item(self, item):
        # Items sold to Gus have been garbled into grime — they can't exist again.
        if self.has_sold_to_gus(item):
            print()
            type.type(yellow("The ") + magenta(bright(item)) + yellow(" crumbles to ash in your hands before you can hold it."))
            print()
            type.type(italic("It was already garbled. Some things can't come back."))
            print()
            return
        self._inventory.add(item)
        self._items_ever_owned.add(item)

    def has_item(self, item):
        return item in self._inventory
    
    def has_broken_item(self, item):
        return item in self._broken_inventory
    
    def is_repairing_item(self, item):
        return item in self._repairing_inventory
    
    def repair_item(self, item):
        self._repairing_inventory.add(item)
        self._broken_inventory.remove(item)

    def return_item(self, item):
        self._repairing_inventory.remove(item)
        self._broken_inventory.add(item)
    
    def use_item(self, item):
        self._inventory.discard(item)
        self._items_ever_used.add(item)

    def track_item_use(self, item_name):
        """Track item usage for evolution chains. Returns (old, new) tuple if evolved, else None."""
        if item_name not in self._inventory:
            return None
        self._item_use_counts[item_name] = self._item_use_counts.get(item_name, 0) + 1
        return self._check_item_evolution(item_name)

    def _check_item_evolution(self, item_name):
        """Check if an item should evolve based on use count."""
        count = self._item_use_counts.get(item_name, 0)
        evolutions = {
            "Pocket Knife": (10, "Utility Blade"),
            "Utility Blade": (15, "Master Knife"),
            "Flashlight": (10, "Lantern"),
            "Lantern": (15, "Eternal Light"),
            "Scrap Armor": (5, "Plated Vest"),
            "Plated Vest": (10, "Road Warrior Plate"),
            "Lucky Penny": (20, "Lucky Coin"),
            "Lucky Coin": (10, "Fortune's Token"),
            "Worn Map": (5, "Rusty Compass"),
            "Rusty Compass": (10, "Golden Compass"),
        }
        if item_name in evolutions:
            threshold, evolved_name = evolutions[item_name]
            if count >= threshold:
                self._inventory.discard(item_name)
                self._inventory.add(evolved_name)
                del self._item_use_counts[item_name]
                return (item_name, evolved_name)
        return None

    def get_evolution_text(self, old_name, new_name):
        """Get narrative text for item evolution."""
        texts = {
            ("Pocket Knife", "Utility Blade"): "Your POCKET KNIFE has been through enough to earn a promotion. The blade is sharper, the handle fits your palm perfectly. It's become a UTILITY BLADE.",
            ("Utility Blade", "Master Knife"): "The UTILITY BLADE transcends its origins. Every edge honed by use. Every scratch a lesson. This is a MASTER KNIFE.",
            ("Flashlight", "Lantern"): "Your FLASHLIGHT has been your eyes in the dark so many times it's grown stronger. The beam is wider, warmer. It's become a LANTERN.",
            ("Lantern", "Eternal Light"): "The LANTERN burns with a light that won't die. You've carried it through so much darkness that it refused to go out. This is ETERNAL LIGHT.",
            ("Scrap Armor", "Plated Vest"): "Your SCRAP ARMOR has taken so many hits it's molded to your body. The dents have become reinforcement. It's now a PLATED VEST.",
            ("Plated Vest", "Road Warrior Plate"): "The PLATED VEST is barely recognizable. Layered, scarred, unbreakable. This is ROAD WARRIOR PLATE.",
            ("Lucky Penny", "Lucky Coin"): "Your LUCKY PENNY has been rubbed so many times it's changed. The copper gleams gold now. It's become a LUCKY COIN.",
            ("Lucky Coin", "Fortune's Token"): "The LUCKY COIN hums with accumulated fortune. Every flip, every gamble, every prayer — crystallized. This is FORTUNE'S TOKEN.",
            ("Worn Map", "Rusty Compass"): "Your WORN MAP has been unfolded so many times the creases are roads themselves. It's transformed into a RUSTY COMPASS.",
            ("Rusty Compass", "Golden Compass"): "The RUSTY COMPASS needle no longer just points north. It points to where you need to be. This is a GOLDEN COMPASS.",
        }
        return texts.get((old_name, new_name), old_name + " has evolved into " + new_name + "!")

    def remove_item(self, item):
        self._inventory.discard(item)

    def lose_item(self, item):
        self.remove_item(item)

    def break_item(self, item):
        self._broken_inventory.add(item)
        self._inventory.remove(item)

    def fix_item(self, item):
        self._inventory.add(item)
        if self.is_repairing_item(item):
            self._repairing_inventory.remove(item)
        if self.has_broken_item(item):
            self._broken_inventory.remove(item)

    # ============================================
    # ITEM EFFECTS - Trap items and utility checks
    # ============================================
    
    def apply_necronomicon_effects(self):
        """The Necronomicon slowly corrupts you. Madness scales with cumulative readings."""
        if self.has_item("Necronomicon"):
            madness = self._necronomicon_readings  # 0, 1, 2, 3...
            roll = random.randrange(10)
            if roll == 0:  # 10% chance: dark vision — money, but heavy sanity cost
                amount = random.randint(100, 500)
                self.change_balance(amount)
                base_loss = random.choice([8, 10, 12])
                self.lose_sanity(base_loss + madness * 2)
                return True
            elif roll <= 2:  # rolls 1 or 2 → 20% chance: simple corruption
                base_loss = random.choice([2, 3, 5])
                self.lose_sanity(base_loss + madness)
                return True
            elif madness >= 3 and roll == 3:  # 10% at 3+ readings: whispers
                self.lose_sanity(madness)
                self.add_status("Necronomicon Madness")
                return True
        return False
    
    def apply_cursed_coin_effects(self):
        """The Cursed Coin brings misfortune."""
        if self.has_item("Cursed Coin"):
            if random.randrange(4) == 0:  # 25% chance
                return True  # Triggers bad luck
        return False
    
    def apply_suzys_gift_effects(self):
        """Suzy's Gift provides comfort and slowly restores sanity."""
        if self.has_item("Suzy's Gift"):
            if random.randrange(3) == 0:  # 33% chance per day
                self.restore_sanity(1)
                return True
        return False

    def apply_daily_item_flavor(self):
        """Once per ~3 days, one carried collectible gets a quiet passive moment.
        Returns (item_name, text_with_{item}_placeholder) or None. Applies its stat effect."""
        if random.randrange(3) != 0:
            return None

        # (item, flavor_text_with_{item}, effect_type, effect_val)
        # effect_type: "sanity" | "heal" | "sanity_heal" | "money" | "sanity_money"
        candidates = [
            ("Filled Locket",       "Your eyes catch the {item} hanging from the mirror. Those two faces, watching over you. You feel less alone.",         "sanity",       2),
            ("Moon Shard",          "The {item} glows softly on the dash. Cool and white. Something about it settled your dreams.",                          "sanity_heal",  (3, 2)),
            ("Midnight Rose",       "The {item} is still alive. Somehow. Against all odds. It smells faintly of something you can't name.",                  "sanity",       2),
            ("Rabbit's Blessing",   "You find a few dollars in a jacket pocket you forgot. The {item}, working quietly.",                                    "sanity_money", (2, 5, 25)),
            ("Championship Medal",  "You glance at the {item} in your bag. You won something once. That's real.",                                           "sanity",       2),
            ("Key to the City",     "The {item} catches someone's eye at the counter. They wave off the fee.",                                              "money",        (25, 100)),

            ("Fight Champion Belt", "The {item} in your bag reminds you what you're capable of. You've won before. You can win again.",                      "sanity",       3),
            ("Deep Stone",          "The {item} glows faint bioluminescent blue. Cold. Deep. Ancient. Calming.",                                            "sanity",       3),
            ("Antique Ring",        "The {item} catches morning light. Whatever story it holds, it isn't yours — but you're part of it now.",                "sanity",       2),
            ("Kraken Pearl",        "The {item} pulses in your bag. The deep ocean remembers you.",                                                         "sanity",       4),
            ("Mermaid Crown",       "Light catches the {item} through the window. Whatever you are, you've touched something larger.",                       "sanity",       4),
            ("Hero Medal",          "The {item} sits heavy in your pocket. You earned it. That's real, even when nothing else feels real.",                  "sanity",       3),
            ("Giant Bear Tooth",    "Someone glances at the {item} on your dash and doesn't mess with you. Some trophies communicate silently.",             "sanity",       2),
            ("Crab Racing Trophy",  "You glance at the {item}. You won something against all odds. Doesn't hurt to remember that.",                         "sanity",       3),
            ("Tortoise Trophy",     "You glance at the {item}. Slow and steady somehow won. You're still here.",                                            "sanity",       3),
            ("Matched Pearls",      "The {item} catch morning light. The ocean made something perfect, and you found both of them.",                         "sanity",       3),
            ("Pink Pearl",          "The {item} catches morning light. Something beautiful from the deep, riding in your pocket.",                           "sanity",       3),
            ("Mermaid Pearl",       "The {item} sits warm in your palm. A gift from another world entirely.",                                               "sanity",       3),
            ("Ancient Sea Map",     "The {item} shows coastlines that may not exist anymore. The world was different, once.",                                "sanity",       3),
            ("Cannon Gem",          "The {item} catches light at an angle that makes no sense. You stare at it longer than you meant to.",                   "sanity",       2),
            ("Pirate Treasure",     "The {item} is heavy in the back. Heavy in a satisfying way. The weight of things earned.",                             "sanity",       3),
            ("Treasure Chest",      "The {item} sits in the back, locked. Something good inside. Yours.",                                                   "sanity",       3),
        ]

        available = [(item, text, etype, eval_) for item, text, etype, eval_ in candidates if self.has_item(item)]
        if not available:
            return None

        item_name, text, effect_type, val = random.choice(available)

        if effect_type == "sanity":
            self.restore_sanity(val)
        elif effect_type == "heal":
            self.heal(val)
        elif effect_type == "sanity_heal":
            self.restore_sanity(val[0])
            self.heal(val[1])
        elif effect_type == "money":
            self.change_balance(random.randint(val[0], val[1]))
        elif effect_type == "sanity_money":
            self.restore_sanity(val[0])
            self.change_balance(random.randint(val[1], val[2]))

        return (item_name, text)

    def has_fire_source(self):
        """Check if player can make fire."""
        return (self.has_item("Lighter") or self.has_item("Matches") or 
                self.has_item("Monogrammed Lighter") or self.has_item("Road Flares"))
    
    def has_cutting_tool(self):
        """Check if player has something sharp."""
        return self.has_item("Pocket Knife") or self.has_item("Golden Trident") or self.has_item("Golden Shovel")

    def _offer_item_choice(self, items_with_desc):
        """When player has multiple applicable items, let them choose which to use.
        Args: items_with_desc - list of (item_name, short_description) tuples
              for items the player currently has
        Returns: chosen item_name, or None if skipped/empty
        """
        if not items_with_desc:
            return None
        if len(items_with_desc) == 1:
            return items_with_desc[0][0]
        type.type("You have options:")
        print()
        for i, (name, desc) in enumerate(items_with_desc, 1):
            type.type("  " + str(i) + ". " + item(name) + " — " + desc)
        print()
        choice = ask.option("Choose an item", [str(i) for i in range(1, len(items_with_desc) + 1)] + ["skip"]).lower()
        if choice == "skip":
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(items_with_desc):
                return items_with_desc[idx][0]
        except (ValueError, IndexError):
            pass
        return items_with_desc[0][0]

    # ============================================
    # FOOD ITEM CATEGORIZATION HELPERS
    # ============================================

    def is_food_item(self, item_name):
        """Check if an item is a food item."""
        return item_name in FOOD_DATA

    def is_energy_food(self, item_name):
        """Check if a food item is an energy food (reduces fatigue)."""
        return FOOD_DATA.get(item_name, {}).get("energy", False)

    def is_companion_food(self, item_name):
        """Check if a food item can be fed to companions."""
        return FOOD_DATA.get(item_name, {}).get("companion_food", False)

    def has_any_food(self):
        """Check if player has any food item in inventory."""
        return any(self.has_item(food) for food in FOOD_DATA)

    def has_energy_food_item(self):
        """Check if player has any energy food in inventory."""
        return any(self.has_item(food) for food in FOOD_DATA if FOOD_DATA[food]["energy"])

    def get_food_data(self, item_name):
        """Get all data for a food item. Returns None if not food."""
        return FOOD_DATA.get(item_name, None)

    def get_inventory_food(self):
        """Get list of all food items currently in inventory."""
        return [food for food in FOOD_DATA if self.has_item(food)]

    def eat_food(self, item_name):
        """Eat a food item. Applies healing, sanity, fatigue effects and shows text.
        Removes from inventory if present. Returns True if eaten."""
        if not self.is_food_item(item_name):
            return False

        data = FOOD_DATA[item_name]

        # Remove from inventory if saved there
        if self.has_item(item_name):
            self.use_item(item_name)

        # Apply effects
        if data["heal"] > 0:
            self.heal(data["heal"])
        if data["sanity"] > 0:
            self.restore_sanity(data["sanity"])
        if data["fatigue_reduce"] > 0:
            self.reduce_fatigue(data["fatigue_reduce"])

        # Eating flavor text
        eat_texts = {
            "Candy Bar": "You chomp down the candy bar. Its sweet chocolate and caramel fill your stomach, and you feel a little better.",
            "Bag of Chips": "You tear open the bag of chips. Its salty potato goodness fills your stomach, and you feel better.",
            "Turkey Sandwich": "You chomp down the turkey sandwich. Its savory turkey and provolone fill your stomach, and you feel much better.",
            "Energy Drink": "You crack it open and chug. The caffeine hits you like a truck. You feel wired.",
            "Beef Jerky": "Tough, chewy, and delicious. Pure protein. You feel stronger.",
            "Cup Noodles": "Warm, salty, comforting. Like a hug for your insides.",
            "Granola Bar": "Healthy and crunchy. You feel responsible for once.",
            "Hot Dog": "It's been a while on that roller, but it still tastes... fine. Mostly.",
            "Microwave Burrito": "Scalding on the outside, frozen in the middle. Classic.",
        }
        type.type(eat_texts.get(item_name, "You eat it. It's food."))
        print()

        # Hot dog special risk
        if item_name == "Hot Dog" and random.randrange(10) == 0:
            type.type("Actually, your stomach gurgles ominously...")
            self.hurt(3)
            print()

        # Energy food fatigue message
        if data["energy"] and data["fatigue_reduce"] > 0:
            type.type(yellow("The exhaustion lifts. You feel like you could actually function today."))
            print()

        return True

    def add_danger(self, danger):
        self._dangers.add(danger)

    def has_danger(self, danger):
        return danger in self._dangers
    
    def lose_danger(self, danger):
        self._dangers.discard(danger)

    def remove_danger(self, danger):
        self._dangers.discard(danger)

    # Dream sequence tracking
    def get_tom_dreams(self):
        return self._tom_dreams
    
    def advance_tom_dreams(self):
        self._tom_dreams += 1
    
    def get_frank_dreams(self):
        return self._frank_dreams
    
    def advance_frank_dreams(self):
        self._frank_dreams += 1
    
    def get_oswald_dreams(self):
        return self._oswald_dreams
    
    def advance_oswald_dreams(self):
        self._oswald_dreams += 1

    # Tanya therapy tracking
    def get_visited_tanya(self):
        return self._visited_tanya
    
    def increment_visited_tanya(self):
        self._visited_tanya += 1
    
    def get_tanya_skip_night(self):
        return self._tanya_skip_night
    
    def set_tanya_skip_night(self, value):
        self._tanya_skip_night = value

    # Suzy storyline tracking
    def get_favorite_color(self):
        return self._favorite_color
    
    def set_favorite_color(self, color):
        self._favorite_color = color
    
    def get_favorite_animal(self):
        return self._favorite_animal
    
    def set_favorite_animal(self, animal):
        self._favorite_animal = animal

    # Rabbit chase tracking
    def get_rabbit_chase(self):
        return self._rabbit_chase
    
    def advance_rabbit_chase(self):
        self._rabbit_chase += 1

    # Millionaire ending tracking
    def is_millionaire(self):
        return self._is_millionaire
    
    def was_millionaire_visited(self):
        return self._millionaire_visited
    
    def set_millionaire_visited(self):
        self._millionaire_visited = True
    
    def get_chosen_mechanic(self):
        return self._chosen_mechanic
    
    def set_chosen_mechanic(self, mechanic):
        self._chosen_mechanic = mechanic

    def get_car_mechanic(self):
        return self._car_mechanic

    def set_car_mechanic(self, mechanic):
        self._car_mechanic = mechanic

    # Gus Pawn Shop tracking
    def get_gus_items_sold(self):
        return len(self._gus_items_sold)
    
    def sell_item_to_gus(self, item_name):
        self._gus_items_sold.add(item_name)
    
    def has_sold_to_gus(self, item_name):
        return item_name in self._gus_items_sold
    
    def get_all_collectibles_list(self):
        """Returns the master list of all collectibles Gus will buy"""
        return [
            # Underwater/Beach Adventure (18 items)
            "Golden Trident", "Kraken Pearl", "Mermaid Crown",
            "Ancient Sea Map", "Deep Stone", "Pirate Treasure", "Treasure Coordinates",
            "Captain's Compass", "Cannon Gem", "Sailor's Lockbox", "Mermaid's Pearl",
            "Mermaid Pearl", "Matched Pearls", "Pink Pearl", "Giant Oyster",
            "Live Fish", "Moon Shard",
            # Beach Events (7 items)
            "Golden Shovel", "Underwater Camera", "Crab Racing Trophy", 
            "Championship Medal", "Antique Ring", "Treasure Chest", "Midnight Rose",
            # Woodlands Adventure (8 items)
            "Hunter's Mark", "Giant Bear Tooth", "Bear's Gold Coin",
            "Magic Acorn", "Fairy's Secret Map", "Captured Fairy",
            # Swamp Adventure (11 items)
            "Gator Tooth Necklace", "Tortoise Trophy", "Ogre's Gemstone", "Ogre's Gift",
            "Swamp Gold", "Witch's Riddle", "Witch's Ward", "Voodoo Doll",
            "Lucky Lure", "Earl's Lucky Lure", "Granny's Swamp Nectar",
            # City Adventure (5 items)
            "Key to the City", "Hero Medal", "Fight Champion Belt", 
            "Stolen Watch", "Suspicious Package",
            # Rabbit Events (4 items)
            "Lucky Penny", "Lucky Rabbit Foot", "Carrot", "Rabbit's Blessing",
            # Misc Adventure (6 items)
            "Mysterious Lockbox", "Mysterious Key", "Mysterious Code",
            "Treasure Map", "Joe's Treasure Map",
            # Secret Items (2 items)
            "Dealer's Joker", "Ace of Spades",
            # Sentimental Items
            "Filled Locket",
            # Zone Reward Items (6 items)
            "Road Warrior Badge", "Druid's Staff", "Swamp Rune",
            "Sea Glass", "Depth Charm", "Underground Pass",
            # Storyline Keepsakes (9 items)
            "Martinez's Card", "Stuart's Number", "Grandpa's Chili Recipe",
            "Grandma's Scarf", "Dealer's Coin", "Edgar's Letter",
            "Edgar's List", "Dealer's Lucky Chips", "Veteran's Lucky Chip",
            # Functional Adventure Items (17 items)
            "Road Talisman", "Silver Horseshoe", "Cowboy Jacket", "Council Feather",
            "Dimensional Coin", "Alien Crystal", "Mystery Potion", "Persistent Bottle",
            "Stolen Marlin", "Hermit's Journal", "Carved Walking Stick", "Junkyard Crown",
            "Scrap Metal Rose", "Ritual Token", "Old Photograph", "Reunion Photo", "Suzy's Gift",
            # Story/Character Items (20 items)
            "Fake Flower", "Feelgood Pill", "Feelgood Bottle", "Radio Numbers",
            "Radio Logbook", "Carnival Token", "Professor Bear", "Lockbox",
            "Apartment Key", "Tanya's Number", "Angel's Number", "Grandma's Number",
            "Beach Romance Number", "Rich Friend's Number",
            "Herbal Pouch", "Hollow Tree Stash", "Blanket", "Torn Collar",
            "Artisan's Toolkit", "Stack of Flyers",
            # Companion/Encounter Items (8 items)
            "Empty Locket", "Golden Ring", "Worry Stone", "Found Phone",
            "Maya's Pick", "Secret Route Map", "Worn Map", "Love Potion",
            # Dark/Criminal Items (4 items)
            "Casino OD Evidence", "Bag of Cocaine", "Building Manager Key", "Stolen Memory",
            # Surreal/Occult Items (5 items)
            "Spoon Satellite", "Necronomicon", "Tinfoil Hat", "Vision Map", "Cursed Coin",
            # NPC Signature Items (3 items)
            "Tom's Wrench", "Frank's Flask", "Oswald's Dice",
            # Wealth/Status Items (4 items)
            "VIP Invitation", "Casino VIP Card", "High Roller Keycard", "Tony's Gun",
            # Radio/Pirate Items (4 items)
            "Night Vision Scope", "Strange Frequency Dial", "Pirate Radio Flyer", "Static Recorder",
            # Scrap/Craft Components (3 items)
            "Scrap Armor", "Signal Booster",
            # Luxury Shop Items (9 items)
            "Expensive Cologne", "Fancy Cigars", "Gold Chain", "Vintage Wine",
            "Fancy Pen", "Silk Handkerchief", "Monogrammed Lighter",
            "Antique Pocket Watch", "Silver Flask",
            # Basic Shop Gear (15 items)
            "Flashlight", "Binoculars", "Tool Kit", "First Aid Kit", "Deck of Cards",
            "Sunglasses", "Leather Gloves", "LifeAlert", "Dog Whistle",
            "Jumper Cables", "Portable Battery Charger", "Car Jack",
            "Rope", "Padlock", "Mysterious Envelope",
            # Auto Parts (21 items)
            "Spare Tire", "Motor Oil", "Coolant", "Antifreeze", "Brake Fluid",
            "Brake Pads", "Power Steering Fluid", "Transmission Fluid",
            "Fix-a-Flat", "Tire Patch Kit", "Gas Can", "Fuel Filter",
            "Fuel Line Antifreeze", "Serpentine Belt", "OBD Scanner",
            "Spare Fuses", "Spare Headlight Bulbs", "Spare Spark Plugs",
            "Oil Stop Leak", "Radiator Stop Leak", "Lock De-Icer",
            "Exhaust Tape", "Thermostat", "WD-40", "Welding Goggles",
            # Cheap Consumables/Supplies (24 items)
            "Bandage", "Granola Bar", "Can of Tuna", "Fish", "Lettuce",
            "Dog Treat", "Bag of Acorns", "Cough Drops", "Breath Mints",
            "Rubber Bands", "Bug Spray", "Cheap Sunscreen", "Plastic Poncho",
            "Water Bottles", "Lighter", "Duct Tape", "Disposable Camera",
            "Road Flares", "Air Freshener", "Hand Warmers", "Super Glue",
            "Fishing Line", "Pest Control", "Umbrella",
            "Bungee Cords", "Garbage Bag", "Plastic Wrap", "Pocket Knife",
            # Unique Misc (5 items)
            "Map", "Lucky Coin", "Broken Compass", "Gus's Precious Grime"
        ]
    
    def get_collectible_prices(self):
        """Returns dictionary of all collectible prices"""
        return {
            # Underwater/Beach Adventure - Legendary
            "Golden Trident": 80000,
            "Kraken Pearl": 100000,
            "Mermaid Crown": 75000,

            "Ancient Sea Map": 25000,
            "Deep Stone": 40000,
            "Pirate Treasure": 60000,
            "Treasure Coordinates": 15000,
            "Captain's Compass": 12000,
            "Cannon Gem": 20000,
            "Sailor's Lockbox": 8000,
            "Mermaid's Pearl": 8000,
            "Mermaid Pearl": 6000,
            "Matched Pearls": 5000,
            "Pink Pearl": 3000,
            "Giant Oyster": 2000,
            "Live Fish": 1000,
            "Moon Shard": 15000,
            # Beach Events
            "Golden Shovel": 15000,
            "Underwater Camera": 1500,
            "Crab Racing Trophy": 3000,
            "Championship Medal": 5000,
            "Antique Ring": 4000,
            "Treasure Chest": 10000,
            "Midnight Rose": 2500,
            # Woodlands Adventure
            "Hunter's Mark": 8000,

            "Giant Bear Tooth": 15000,
            "Bear's Gold Coin": 5000,

            "Magic Acorn": 6000,
            "Fairy's Secret Map": 8000,
            "Captured Fairy": 25000,
            # Swamp Adventure
            "Gator Tooth Necklace": 5000,
            "Tortoise Trophy": 4000,
            "Ogre's Gemstone": 30000,
            "Ogre's Gift": 20000,
            "Swamp Gold": 10000,
            "Witch's Riddle": 3000,
            "Witch's Ward": 5000,
            "Voodoo Doll": 8000,
            "Lucky Lure": 2000,
            "Earl's Lucky Lure": 4000,
            "Granny's Swamp Nectar": 1500,
            # City Adventure
            "Key to the City": 25000,
            "Hero Medal": 15000,
            "Fight Champion Belt": 10000,
            "Stolen Watch": 3000,
            "Suspicious Package": 5000,
            # Rabbit Events
            "Lucky Penny": 50,
            "Lucky Rabbit Foot": 1500,
            "Carrot": 5,
            "Rabbit's Blessing": 10000,
            # Misc Adventure
            "Mysterious Lockbox": 2000,
            "Mysterious Key": 1500,
            "Mysterious Code": 3000,

            "Treasure Map": 5000,
            "Joe's Treasure Map": 3000,
            # Secret Items
            "Dealer's Joker": 50000,
            "Ace of Spades": 1000,
            # Sentimental Items
            "Filled Locket": 500,
            # Zone Reward Items
            "Road Warrior Badge": 5000,
            "Druid's Staff": 8000,
            "Swamp Rune": 6000,
            "Sea Glass": 4000,
            "Depth Charm": 10000,
            "Underground Pass": 7000,
            # Storyline Keepsakes
            "Martinez's Card": 500,
            "Stuart's Number": 500,
            "Grandpa's Chili Recipe": 2000,
            "Grandma's Scarf": 1500,
            "Dealer's Coin": 15000,
            "Edgar's Letter": 1000,
            "Edgar's List": 1000,
            "Dealer's Lucky Chips": 8000,
            "Veteran's Lucky Chip": 3000,
            # Functional Adventure Items
            "Road Talisman": 8000,
            "Silver Horseshoe": 12000,
            "Cowboy Jacket": 5000,
            "Council Feather": 3000,
            "Dimensional Coin": 20000,
            "Alien Crystal": 25000,
            "Mystery Potion": 3000,
            "Persistent Bottle": 15000,
            "Stolen Marlin": 10000,
            "Hermit's Journal": 5000,
            "Carved Walking Stick": 4000,
            "Junkyard Crown": 6000,
            "Scrap Metal Rose": 5000,
            "Ritual Token": 8000,
            "Old Photograph": 2000,
            "Reunion Photo": 1500,
            "Suzy's Gift": 2000,
            # Story/Character Items
            "Fake Flower": 200,
            "Feelgood Pill": 500,
            "Feelgood Bottle": 2000,
            "Radio Numbers": 1000,
            "Radio Logbook": 1500,
            "Carnival Token": 300,
            "Professor Bear": 3000,
            "Lockbox": 1000,
            "Apartment Key": 500,
            "Tanya's Number": 200,
            "Angel's Number": 500,
            "Grandma's Number": 100,
            "Beach Romance Number": 100,
            "Rich Friend's Number": 500,
            "Herbal Pouch": 2000,
            "Hollow Tree Stash": 1500,
            "Blanket": 100,
            "Torn Collar": 50,
            "Artisan's Toolkit": 3000,
            "Stack of Flyers": 50,
            # Companion/Encounter Items
            "Empty Locket": 500,
            "Golden Ring": 3000,
            "Worry Stone": 1000,
            "Found Phone": 500,
            "Maya's Pick": 1000,
            "Secret Route Map": 2000,
            "Worn Map": 1000,
            "Love Potion": 3000,
            # Dark/Criminal Items
            "Casino OD Evidence": 5000,
            "Bag of Cocaine": 10000,
            "Building Manager Key": 2000,
            "Stolen Memory": 2000,
            # Surreal/Occult Items
            "Spoon Satellite": 1000,
            "Necronomicon": 20000,
            "Tinfoil Hat": 500,
            "Vision Map": 3000,
            "Cursed Coin": 2000,
            # NPC Signature Items
            "Tom's Wrench": 2000,
            "Frank's Flask": 3000,
            "Oswald's Dice": 5000,
            # Wealth/Status Items
            "VIP Invitation": 5000,
            "Casino VIP Card": 8000,
            "High Roller Keycard": 10000,
            "Tony's Gun": 15000,
            # Radio/Pirate Items
            "Night Vision Scope": 3000,
            "Strange Frequency Dial": 2000,
            "Pirate Radio Flyer": 500,
            "Static Recorder": 1500,
            # Scrap/Craft Components
            "Scrap Armor": 2000,
            "Signal Booster": 1500,
            # Luxury Shop Items
            "Expensive Cologne": 800,
            "Fancy Cigars": 600,
            "Gold Chain": 2000,
            "Vintage Wine": 1500,
            "Fancy Pen": 300,
            "Silk Handkerchief": 200,
            "Monogrammed Lighter": 500,
            "Antique Pocket Watch": 1500,
            "Silver Flask": 500,
            # Basic Shop Gear
            "Flashlight": 100,
            "Binoculars": 200,
            "Tool Kit": 500,
            "First Aid Kit": 200,
            "Deck of Cards": 100,
            "Sunglasses": 75,
            "Leather Gloves": 100,
            "LifeAlert": 150,
            "Dog Whistle": 50,
            "Jumper Cables": 100,
            "Portable Battery Charger": 150,
            "Car Jack": 100,
            "Rope": 50,
            "Padlock": 75,
            "Mysterious Envelope": 1000,
            # Auto Parts
            "Spare Tire": 100,
            "Motor Oil": 30,
            "Coolant": 25,
            "Antifreeze": 25,
            "Brake Fluid": 20,
            "Brake Pads": 50,
            "Power Steering Fluid": 20,
            "Transmission Fluid": 25,
            "Fix-a-Flat": 30,
            "Tire Patch Kit": 40,
            "Gas Can": 50,
            "Fuel Filter": 30,
            "Fuel Line Antifreeze": 20,
            "Serpentine Belt": 40,
            "OBD Scanner": 100,
            "Spare Fuses": 10,
            "Spare Headlight Bulbs": 15,
            "Spare Spark Plugs": 20,
            "Oil Stop Leak": 15,
            "Radiator Stop Leak": 15,
            "Lock De-Icer": 10,
            "Exhaust Tape": 15,
            "Thermostat": 25,
            "WD-40": 15,
            "Welding Goggles": 50,
            # Cheap Consumables/Supplies
            "Bandage": 10,
            "Granola Bar": 5,
            "Can of Tuna": 10,
            "Fish": 5,
            "Lettuce": 3,
            "Dog Treat": 5,
            "Bag of Acorns": 5,
            "Cough Drops": 15,
            "Breath Mints": 10,
            "Rubber Bands": 5,
            "Bug Spray": 10,
            "Cheap Sunscreen": 10,
            "Plastic Poncho": 15,
            "Water Bottles": 10,
            "Lighter": 15,
            "Duct Tape": 15,
            "Disposable Camera": 50,
            "Road Flares": 40,
            "Air Freshener": 5,
            "Hand Warmers": 20,
            "Super Glue": 10,
            "Fishing Line": 15,
            "Pest Control": 20,
            "Umbrella": 25,
            "Bungee Cords": 15,
            "Garbage Bag": 5,
            "Plastic Wrap": 5,
            "Pocket Knife": 50,
            # Unique Misc
            "Map": 3000,
            "Lucky Coin": 5000,
            "Broken Compass": 1000,
            "Gus's Precious Grime": 1,
        }
    
    def get_gus_total_collectibles(self):
        """Returns total number of unique collectibles Gus wants"""
        return len(self.get_all_collectibles_list())

    # Sanity tracking system (visible stat)

    # ============================================
    # FATIGUE / SLEEP SYSTEM
    # ============================================

    def get_fatigue(self):
        return self._fatigue

    def add_fatigue(self, value):
        """Increase fatigue (0-100). Higher = more exhausted."""
        self._fatigue = min(100, self._fatigue + value)

    def reduce_fatigue(self, value):
        """Decrease fatigue. Lower = more rested."""
        self._fatigue = max(0, self._fatigue - value)

    def get_sleep_quality(self):
        """Returns sleep quality tier based on current fatigue after processing sleep."""
        if self._fatigue <= 10:
            return "refreshed"
        elif self._fatigue <= 25:
            return "well_rested"
        elif self._fatigue <= 40:
            return "decent"
        elif self._fatigue <= 55:
            return "restless"
        elif self._fatigue <= 70:
            return "poor"
        elif self._fatigue <= 85:
            return "terrible"
        else:
            return "wrecked"

    def process_sleep(self):
        """Process a night of sleep. Reduces fatigue based on conditions.
        Called at the start of each new day (waking up)."""
        # Base sleep recovery - generous enough that normal play stays comfortable
        recovery = random.randint(35, 50)

        # Companions help you sleep better (companionship = comfort)
        companions = self.get_all_companions()
        alive_companions = sum(1 for c in companions.values() if c["status"] == "alive")
        if alive_companions > 0:
            recovery += min(alive_companions * 3, 12)  # Up to +12 from companions

        # Being sick makes sleep slightly worse
        if self._is_sick:
            recovery -= random.randint(3, 8)

        # Being injured makes sleep slightly worse
        if self._is_injured:
            recovery -= random.randint(2, 6)

        # Low sanity disrupts sleep
        if self._sanity <= 25:
            recovery -= random.randint(5, 12)
        elif self._sanity <= 50:
            recovery -= random.randint(3, 7)

        # Broken state = rough sleep
        if self._is_broken:
            recovery -= random.randint(8, 15)

        # Minimum recovery of 10 (you always get decent rest)
        recovery = max(10, recovery)

        self.reduce_fatigue(recovery)

    def fatigue_blocks_event(self):
        """Returns True if fatigue causes the player to miss a positive day event.
        Running Shoes passively prevent this. Energy Drink is consumed if needed."""
        if self.has_item("Running Shoes"):
            return False
        if self._fatigue >= 95:
            would_block = random.randrange(100) < 35  # 35% chance only at extreme exhaustion
        elif self._fatigue >= 85:
            would_block = random.randrange(100) < 20  # 20%
        elif self._fatigue >= 75:
            would_block = random.randrange(100) < 10  # 10%
        else:
            return False

        if would_block and self.has_item("Energy Drink"):
            # Consume the Energy Drink to power through
            self.remove_item("Energy Drink")
            self.reduce_fatigue(25)
            type.type("You're so exhausted you can barely keep your eyes open... but wait. ")
            type.type("You crack open your " + magenta(bright("Energy Drink")) + " and chug the whole thing.")
            print()
            type.type(random.choice([
                "The caffeine hits like a freight train. You're AWAKE now.",
                "Tastes like battery acid and ambition. You're good to go.",
                "Your heart does a little kickflip. Energy restored.",
                "It's disgusting. It's beautiful. You can see sounds now.",
                "The exhaustion evaporates. Temporarily. You'll pay for this later.",
            ]))
            print()
            return False

        return would_block

