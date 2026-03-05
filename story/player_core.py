import random
import time
import sys
import lists
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\n\n"

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
from story.events_day import DayEventsMixin
from story.events_night import NightEventsMixin
from story.adventures import AdventuresMixin
from story.mechanics_intro import MechanicsIntroMixin
from story.game_flow import GameFlowMixin
from story.locations import LocationsMixin
from story.durability import DurabilityMixin
from story.event_dispatch import EventDispatchMixin
from story.endings import EndingsMixin
from story.medical import MedicalMixin
from story.car_events import CarEventsMixin

class Player(
    SystemsMixin,
    EconomyMixin,
    DayCycleMixin,
    DayEventsMixin,
    NightEventsMixin,
    AdventuresMixin,
    MechanicsIntroMixin,
    GameFlowMixin,
    LocationsMixin,
    DurabilityMixin,
    EventDispatchMixin,
    EndingsMixin,
    MedicalMixin,
    CarEventsMixin,
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
        self._broken_inventory = set()
        self._repairing_inventory = set()
        self._dangers = set()
        self._met = set()
        self._mechanic_visits = 0
        self._health = 100
        self._balance = 50
        self._previous_balance = 50
        self._rank = 0
        self._day = 1
        self._counting_days = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
        self._is_millionaire = False  # True when player hits $1M for the first time
        self._millionaire_visited = False  # True after the special morning visitor comes
        self._chosen_mechanic = None  # Which mechanic the visitor tells you to see ("Tom", "Frank", or "Oswald")
        self._gus_items_sold = set()  # Tracks which collectibles have been sold to Gus
        self._sanity = 100  # Visible stat - starts at 100, decreases with trauma
        self._fatigue = 0  # 0-100: 0=well-rested, 100=exhausted. Affects sleep quality and event access.
        self._sanity_warnings_shown = 0  # Tracks how many sanity warnings have been shown
        self._faced_madness = False  # True after surviving the confrontation
        self._is_broken = False  # True when sanity hits 0 and you survive
        
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
            "times_robbed": 0,
            "times_hospitalized": 0,
            "mechanic_visits": 0,
            "doctor_visits": 0,
            "casino_visits": 0,
            "pawn_shop_visits": 0,
        }
        
        # COMPANION SYSTEM - Tracks active companions and their states
        self._companions = {
            # "name": {"status": "alive/dead/lost", "happiness": 0-100, "days_owned": 0, "fed_today": False}
        }
        
        # LOAN SHARK SYSTEM
        self._loan_shark_debt = 0
        self._loan_shark_days_overdue = 0
        self._loan_shark_warning_level = 0  # 0=none, 1=warning, 2=threat, 3=violence, 4=death
        
        # PAWN SHOP REPUTATION
        self._pawn_shop_reputation = 50  # 0-100, affects prices
        
        # COMPANION BETRAYAL TRACKING
        self._companions_sold_count = 0  # Track how many companions sold to Gus for the dark ending
        
        # FRAUDULENT CASH SYSTEM (Loan Shark)
        self._fraudulent_cash = 0  # Fake money from loan shark - needs to be "blended" through gambling
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
            type.type("They patch you up and send you on your way. Your LifeAlert has been used up.")
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
        print("\n")
        self.update_health_indicator_durability()

    def status(self, cause_of_death=None):
        if not self._alive:
            print("\n")
            type.slow("You have died!")
            print()
            if self._day == 1: type.slow("You didn't even last " + bright(yellow(str(self._day) + " day")) + ". That's embarrassing.")
            elif self._day == 2: type.slow("You lasted " + bright(yellow(str(self._day-1) + " day")) + ".")
            else: type.slow("You lasted " + bright(yellow(str(self._day) + " days")) + "!")
            print()
            type.slow("You met your fate with a final balance of " + green(bright("${:,}".format(self._balance))))
            print()
            self.display_final_achievements()
            type.slow("The police were able to recover your body, but nobody cared enough to show up to your funeral.")
            quit()
        elif (self._balance == 0):
            print("\n")
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
            print("\n")
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

    def has_flask_effect(self, flask):
        return flask in self._flask_effects
    
    def remove_flask_effect(self, flask):
        self._flask_effects.remove(flask)

    def len_flasks(self):
        return len(self._flask_effects)

    def add_status(self, status):
        self._status_effects.add(status)

    def has_status(self, status):
        return status in self._status_effects
    
    def remove_status(self, status):
        self._status_effects.remove(status)

    def add_injury(self, injury):
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
        self._inventory.add(item)

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
        self._inventory.remove(item)

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
        """The Necronomicon slowly corrupts you."""
        if self.has_item("Necronomicon"):
            if random.randrange(5) == 0:  # 20% chance per day
                self.lose_sanity(random.choice([1, 2, 3]))
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
    
    def has_fire_source(self):
        """Check if player can make fire."""
        return (self.has_item("Lighter") or self.has_item("Matches") or 
                self.has_item("Monogrammed Lighter") or self.has_item("Road Flares"))
    
    def has_cutting_tool(self):
        """Check if player has something sharp."""
        return self.has_item("Pocket Knife") or self.has_item("Golden Trident") or self.has_item("Golden Shovel")

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
        self._dangers.remove(danger)

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
            "Golden Trident", "Kraken Pearl", "Mermaid Crown", "Kraken's Memory",
            "Ancient Sea Map", "Deep Stone", "Pirate Treasure", "Treasure Coordinates",
            "Captain's Compass", "Cannon Gem", "Sailor's Lockbox", "Mermaid's Pearl",
            "Mermaid Pearl", "Matched Pearls", "Pink Pearl", "Giant Oyster",
            "Live Fish", "Moon Shard",
            # Beach Events (7 items)
            "Golden Shovel", "Underwater Camera", "Crab Racing Trophy", 
            "Championship Medal", "Antique Ring", "Treasure Chest", "Midnight Rose",
            # Woodlands Adventure (8 items)
            "Hunter's Mark", "Bear King's Respect", "Giant Bear Tooth", "Bear's Gold Coin",
            "Witch's Favor", "Magic Acorn", "Fairy's Secret Map", "Captured Fairy",
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
            "Fountain Water", "Treasure Map", "Joe's Treasure Map",
            # Secret Items (2 items)
            "Dealer's Joker", "Ace of Spades"
        ]
    
    def get_collectible_prices(self):
        """Returns dictionary of all collectible prices"""
        return {
            # Underwater/Beach Adventure - Legendary
            "Golden Trident": 80000,
            "Kraken Pearl": 100000,
            "Mermaid Crown": 75000,
            "Kraken's Memory": 50000,
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
            "Bear King's Respect": 50000,
            "Giant Bear Tooth": 15000,
            "Bear's Gold Coin": 5000,
            "Witch's Favor": 12000,
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
            "Fountain Water": 8000,
            "Treasure Map": 5000,
            "Joe's Treasure Map": 3000,
            # Secret Items
            "Dealer's Joker": 50000,
            "Ace of Spades": 1000,
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
            print("\n")
            type.type(random.choice([
                "The caffeine hits like a freight train. You're AWAKE now.",
                "Tastes like battery acid and ambition. You're good to go.",
                "Your heart does a little kickflip. Energy restored.",
                "It's disgusting. It's beautiful. You can see sounds now.",
                "The exhaustion evaporates. Temporarily. You'll pay for this later.",
            ]))
            print("\n")
            return False

        return would_block

