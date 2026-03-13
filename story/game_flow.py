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

class GameFlowMixin:
    """Game flow: start_day, pest control, car trouble checks, day marking, status updates, adventure areas"""

    def start_day(self):
        print("\n")
        type.slow(bright(yellow("═" * 50)))
        type.typeover("Press a key to continue:", bright(yellow("~ ~ ~ Morning, Day " + str(self._day) + " ~ ~ ~ ")), True)
        type.slow(bright(yellow("═" * 50)))
        print("\n")

        # ============================================
        # DAILY SYSTEM UPDATES
        # ============================================
        
        # Update companions (happiness decay, check for runaways)
        self.update_companions_daily()
        
        # Update loan shark (interest, warning level escalation)
        self.update_loan_shark_daily()
        
        # Check for loan shark random encounter if debt is severe
        if self.get_loan_shark_debt() > 0 and self.get_loan_shark_warning_level() >= 2:
            if self.check_loan_shark_event():
                self.loan_shark_encounter()
        
        # Update day survival statistic
        self.increment_statistic("days_survived")
        
        # Check achievements
        self.check_achievements()

        # ============================================
        # DAILY ITEM EFFECTS (Passive triggers)
        # ============================================
        
        # Suzy's Gift - Slow sanity restoration from her kindness
        if self.apply_suzys_gift_effects():
            type.slow(cyan("You hold Suzy's Gift close. It's warm. Comforting. You feel a little more like yourself."))
            print("\n")
        
        # Necronomicon - Corrupts the soul
        if self.apply_necronomicon_effects():
            if random.randrange(3) == 0:  # Sometimes show a hint
                type.slow(red("The whispers in your skull are louder this morning. The book pulses in your bag."))
                print("\n")
        
        # Cursed Coin - Random misfortune
        if self.apply_cursed_coin_effects():
            cursed_effect = random.choice([
                "You stub your toe getting out of the car. Hard. The coin in your pocket feels warm.",
                "A bird poops directly on your windshield. Then another. Then five more. The coin jingles.",
                "You feel a strange sense of dread wash over you. The cursed coin seems to glow faintly.",
                "Your coffee was somehow already cold. You didn't even have coffee. Where did this cold coffee come from?"
            ])
            type.type(cursed_effect)
            print("\n")
            if random.randrange(5) == 0:
                small_loss = random.randint(5, 25)
                type.type("You realize you've lost " + red(bright("${:,}".format(small_loss))) + " somewhere. Weird.")
                self.change_balance(-small_loss)
        
        # Filled Locket - Quiet daily comfort from a completed memory
        if self.apply_filled_locket_effects():
            type.slow(cyan("Your eyes catch the " + bright("Filled Locket") + " hanging from the mirror. Those two faces, watching over you. You feel less alone."))
            print("\n")

        # Moon Shard - Moonlit peace
        if self.apply_moon_shard_effects():
            type.slow(cyan("The " + bright("Moon Shard") + " glows softly on the dash. Cool and white. Something about it settled your dreams."))
            print("\n")

        # Midnight Rose - Fading beauty
        if self.apply_midnight_rose_effects():
            type.slow(cyan("The " + bright("Midnight Rose") + " is still alive. Somehow. Against all odds. It smells faintly of something you can't name."))
            print("\n")

        # Rabbit's Blessing - Gentle daily luck
        if self.apply_rabbit_blessing_effects():
            type.slow(cyan("The luck of the rabbit moves through your day without fanfare. Just small things going right."))
            print("\n")

        # Championship Medal - Confidence boost
        if self.apply_championship_medal_effects():
            type.slow(cyan("You glance at the " + bright("Championship Medal") + " in your bag. You won something once. You can win again."))
            print("\n")

        # Key to the City - Occasional civic perk
        if self.apply_key_to_city_effects():
            type.slow(cyan("The " + bright("Key to the City") + " catches someone's eye. They wave you through, no charge. A small civic perk."))
            print("\n")

        # Fountain Water - Emergency auto-heal when near death
        if self.apply_fountain_water_effects():
            type.slow(cyan("The " + bright("Fountain Water") + " shimmers in its vial. You don't remember drinking it. But you feel... renewed."))
            print("\n")

        # Granny's Swamp Nectar - Consumable healing
        if self.has_item("Granny's Swamp Nectar") and self.get_health() < 50 and random.randrange(4) == 0:
            type.slow(cyan("You crack open " + bright("Granny's Swamp Nectar") + ". It smells like turpentine and old leaves. You drink it anyway."))
            print("\n")
            if random.randrange(3) == 0:
                type.type("It burns going down. Then warm. Then better. Way better.")
                self.heal(random.randint(20, 40))
                self.restore_sanity(8)
                self.use_item("Granny's Swamp Nectar")
            else:
                type.type("It burns going down. Everything burns. Oh no. Oh no no no.")
                self.hurt(random.randint(5, 15))
                self.lose_sanity(5)
                self.use_item("Granny's Swamp Nectar")
            print("\n")

        # Bear King's Respect - animals (and some humans) sense it
        if self.has_item("Bear King's Respect") and random.randrange(8) == 0:
            type.slow(cyan("People step aside today without knowing why. The " + bright("Bear King's Respect") + " carries weight even here."))
            self.restore_sanity(3)
            print("\n")

        # Kraken's Memory - ancient knowledge surfaces occasionally
        if self.has_item("Kraken's Memory") and random.randrange(7) == 0:
            type.slow(cyan("The " + bright("Kraken's Memory") + " pulses behind your eyes. A thousand years of ocean depth, compressed into a moment."))
            self.restore_sanity(4)
            self.heal(3)
            print("\n")

        # Fight Champion Belt - passive confidence
        if self.apply_fight_champion_belt_effects() and random.randrange(9) == 0:
            type.slow(cyan("The " + bright("Fight Champion Belt") + " in your bag reminds you what you're capable of. You've won before. You can win again."))
            self.restore_sanity(3)
            print("\n")

        # Deep Stone - glows faintly in the dark, calming
        if self.has_item("Deep Stone") and random.randrange(8) == 0:
            type.slow(cyan("The " + bright("Deep Stone") + " glows a faint bioluminescent blue. Cold. Deep. Ancient."))
            self.restore_sanity(3)
            print("\n")

        # Antique Ring - carries the weight of a story
        if self.has_item("Antique Ring") and random.randrange(9) == 0:
            type.slow(cyan("The " + bright("Antique Ring") + " catches morning light. Whatever story it holds, it isn't yours — but you're part of it now."))
            self.restore_sanity(2)
            print("\n")

        # Witch's Favor - emergency rescue when near death
        if self.apply_witch_favor_rescue():
            type.slow(cyan("Something intercedes. You felt it — a warmth, a pressure, a presence. The " + bright("Witch's Favor") + " crumbles to ash in your pocket."))
            type.type(" The witch called in her side of the deal.")
            print("\n")

        # Captain's Compass - navigational luck
        if self.apply_captain_compass_effects():
            type.slow(cyan("The " + bright("Captain's Compass") + " needle spins, then locks on something unexpected. You follow it."))
            self.restore_sanity(3)
            print("\n")

        # Kraken Pearl - legendary item resonates with deep-water memories
        if self.has_item("Kraken Pearl") and random.randrange(10) == 0:
            type.slow(cyan("The " + bright("Kraken Pearl") + " pulses in your bag. The deep ocean remembers you."))
            self.restore_sanity(4)
            print("\n")

        # Mermaid Crown - carries an otherworldly authority
        if self.has_item("Mermaid Crown") and random.randrange(10) == 0:
            type.slow(cyan("Light catches the " + bright("Mermaid Crown") + " through the window. Whatever you are, you've touched something larger."))
            self.restore_sanity(4)
            print("\n")

        # Hero Medal - reminds you of what you're capable of
        if self.has_item("Hero Medal") and random.randrange(9) == 0:
            type.slow(cyan("The " + bright("Hero Medal") + " sits heavy in your pocket. You earned it. That's real, even when nothing else feels real."))
            self.restore_sanity(3)
            print("\n")

        # Giant Bear Tooth - people sense something about you
        if self.has_item("Giant Bear Tooth") and random.randrange(9) == 0:
            type.slow(cyan("Someone glances at the " + bright("Giant Bear Tooth") + " on your dash and doesn't mess with you. Some trophies communicate silently."))
            self.restore_sanity(2)
            print("\n")

        # Trophy items - silent reminders of past victories
        if (self.has_item("Crab Racing Trophy") or self.has_item("Tortoise Trophy")) and random.randrange(10) == 0:
            trophy = "Crab Racing Trophy" if self.has_item("Crab Racing Trophy") else "Tortoise Trophy"
            type.slow(cyan("You glance at the " + bright(trophy) + ". You won something against all odds. Doesn't hurt to remember that."))
            self.restore_sanity(3)
            print("\n")

        # Pearls - small beauty that grounds you
        if (self.has_item("Matched Pearls") or self.has_item("Pink Pearl") or self.has_item("Mermaid Pearl")) and random.randrange(10) == 0:
            pearl = "Matched Pearls" if self.has_item("Matched Pearls") else ("Pink Pearl" if self.has_item("Pink Pearl") else "Mermaid Pearl")
            type.slow(cyan("The " + bright(pearl) + " catches morning light. The ocean made something perfect, and you found it."))
            self.restore_sanity(3)
            print("\n")

        # Ancient Sea Map - curiosity and wonder
        if self.has_item("Ancient Sea Map") and random.randrange(9) == 0:
            type.slow(cyan("The " + bright("Ancient Sea Map") + " shows coastlines that may not exist anymore. The world was different, once."))
            self.restore_sanity(3)
            print("\n")

        # Cannon Gem - strange light, strange thoughts
        if self.has_item("Cannon Gem") and random.randrange(9) == 0:
            type.slow(cyan("The " + bright("Cannon Gem") + " catches light at an angle that makes no sense. You stare at it longer than you meant to."))
            self.restore_sanity(2)
            print("\n")

        # Pirate Treasure / Treasure Chest - weight of wealth
        if (self.has_item("Pirate Treasure") or self.has_item("Treasure Chest")) and random.randrange(9) == 0:
            treasure = "Pirate Treasure" if self.has_item("Pirate Treasure") else "Treasure Chest"
            type.slow(cyan("The " + bright(treasure) + " is heavy in the back. Heavy in a satisfying way. The weight of things earned."))
            self.restore_sanity(3)
            print("\n")

        # Broken state effects at start of day
        if self._is_broken:
            print()
            self.sanity_indicator()
            if random.randrange(3) == 0:
                effect = self.get_broken_effect()
                type.slow(red(effect))
                print("\n")
        # Display sanity status at start of day
        elif self._sanity <= 75:
            print()
            self.sanity_indicator()
        
        self.update_rank()
        # ============================================
        # WAKING UP (right before the morning event)
        # ============================================
        self.process_sleep()
        sleep_quality = self.get_sleep_quality()
        sleep_text = self._lists.get_sleep_text(sleep_quality)
        type.type(sleep_text)
        print("\n")

        # MILLIONAIRE MORNING - Special visitor when you've hit $1M and still have it
        if self.is_millionaire() and self._balance >= 1000000 and not self.was_millionaire_visited():
            self.millionaire_morning_visitor()
            self.set_millionaire_visited()
            return  # Skip normal day events - this is your final day

        # ============================================
        # STORYLINE SYSTEM CHECK
        # ============================================
        # Check for sequential storyline events before random day events.
        # Only ONE storyline event fires per day. If one fires, skip random events.
        storyline_event = self._storyline_system.check_for_storyline_event()
        if storyline_event is not None:
            storyline_event()
            self.update_rank()
            return

        self.day_event()

        self.update_rank()

    def has_pests(self):
        if self.has_danger("Spider") or self.has_danger("Cockroach") or self.has_danger("Rat") or self.has_danger("Termite"):
            return True
        else:
            return False

    def kill_pests(self):
        self.use_item("Pest Control")
        if self.has_danger("Spider"):
            self.lose_danger("Spider")
        if self.has_danger("Cockroach"):
            self.lose_danger("Cockroach")
        if self.has_danger("Rat"):
            self.lose_danger("Rat")
        if self.has_danger("Termite"):
            self.lose_danger("Termite")

    def check_for_car_trouble(self):
        """Random chance for car trouble to ruin your afternoon. Returns True if car trouble occurred."""
        # Base 8% chance for any car trouble event
        if random.randrange(100) >= 8:
            return False
        
        # First check for follow-up events from existing dangers
        danger_events = []
        if self.has_danger("Leaking Battery"):
            danger_events.append("leaking_battery_worsens")
        if self.has_danger("Bald Tires"):
            danger_events.append("bald_tires_hydroplane")
        if self.has_danger("Engine Knock"):
            danger_events.append("engine_knock_worsens")
        if self.has_danger("Nail in Tire"):
            danger_events.append("nail_in_tire_blows")
        if self.has_danger("Failing Fuel Pump"):
            danger_events.append("failing_fuel_pump_dies")
        if self.has_danger("Broken Ball Joint"):
            danger_events.append("broken_ball_joint_breaks")
        if self.has_danger("Failing Starter Motor"):
            danger_events.append("failing_starter_dies")
        
        # 40% chance to trigger a danger follow-up if we have any
        if len(danger_events) > 0 and random.randrange(100) < 40:
            event = getattr(self, random.choice(danger_events))
            event()
            return True
        
        # Otherwise, random car trouble
        car_trouble_events = [
            "dead_battery_afternoon",
            "corroded_battery_terminals",
            "battery_acid_leak",
            "engine_overheating",
            "check_engine_light_on",
            "engine_wont_turn_over",
            "strange_engine_noise",
            "engine_oil_empty",
            "oil_leak_spotted",
            "slow_tire_leak",
            "tire_blowout",
            "bald_tires_noticed",
            "nail_in_tire",
            "headlights_burned_out",
            "alternator_failing",
            "fuse_blown",
            "car_alarm_malfunction",
            "starter_motor_grinding",
            "brakes_squealing",
            "brake_fluid_leak",
            "abs_light_on",
            "ran_out_of_gas",
            "fuel_pump_whining",
            "clogged_fuel_filter",
            "transmission_slipping",
            "stuck_in_gear",
            "radiator_leak",
            "thermostat_stuck",
            "water_pump_failing",
            "power_steering_failure",
            "wheel_alignment_off",
            "suspension_creaking",
            "broken_ball_joint",
            "exhaust_leak_loud",
            "catalytic_converter_stolen",
            "hail_damage",
            "flooded_engine",
            "windshield_cracked",
            "frozen_door_locks",
            "frozen_fuel_line",
            "mystery_breakdown",
            "key_wont_turn",
            "car_wont_go_in_reverse",
            "window_wont_roll_up",
            "trunk_wont_close",
            "gas_pedal_sticking",
            "parking_brake_stuck"
        ]
        
        # Pick and execute a random car trouble event
        event_name = random.choice(car_trouble_events)
        event = getattr(self, event_name)
        print()
        type.type(yellow("=== CAR TROUBLE ==="))
        print("\n")
        event()

        # If the event left the player stranded for the afternoon, give their
        # mechanic a chance to drive by and help — the roadside visit system.
        # The visit may remove "Wasted Afternoon" so the player can still go out.
        if self.has_travel_restriction("Wasted Afternoon"):
            self.roadside_mechanic_visit()

        return self.has_travel_restriction("Wasted Afternoon")

    def get_mark_index(self, mark):
        match mark:
            case "Spider Bite":
                return 0
            case "Hepatitis":
                return 1
            case "Squirrel Bite":
                return 2
            case "Squirrely Fed":
                return 3
            case "Rabies":
                return 4
            case "Rat Bite":
                return 5
            case "Snake Bite":
                return 6
            case "Sore Throat":
                return 7
            case "Cold":
                return 8
            case "Mechanic":
                return 9
            case "Ant Bites":
                return 10
            case "Flu":
                return 11
            case "Wild Rat Attack":
                return 12
        raise ValueError(f"Unknown day mark: {mark}")

    def mark_day(self, mark, time="day"):
        i = self.get_mark_index(mark)
        if time == "day":
            self._counting_days[i] = self._day
        if time == "night":
            self._counting_days[i] = self._day-1

    def get_days_elapsed(self, mark):
        i = self.get_mark_index(mark)
        return self._day - self._counting_days[i]
    
    def update_silver_value(self):
        if self.has_item("Enchanting Silver Bar"):
            return 1000

    def update_status(self):
        damage = 0
        if self._clear_all_status == True:
            type.type("Whatever the Witch Doctor gave you yesterday, it worked wonders on you. You feel amazing, as though your body had been completely cleansed.")
            print("\n")
            self._status_effects = set()
            self._injuries = set()
            self._is_sick = False
            self._is_injured = False
            self._clear_all_status = False

        # Physical Threats
        # Spider Bite
        if self.has_status("Spider Bite"):
            days_elapsed = self.get_days_elapsed("Spider Bite")
            if(self._clear_status):
                self.remove_status("Spider Bite")
                type.type("Your spider bite is starting to heal. ")
            elif days_elapsed == 0:
                damage += random.choice([1, 2])
                type.type("The fangmarks of your spider bite are faint but visible. ")
            elif days_elapsed == 1:
                damage += random.choice([3, 4, 5, 6])
                type.type("Your spider bite is sore and swolen. ")
            elif days_elapsed == 2:
                damage += random.choice([4, 5, 6, 7, 8, 9])
                type.type("Your spider bite is really painful. You don't feel good. ")
            elif days_elapsed >= 3:
                random_chance = random.randrange(4)
                if (random_chance == 0):
                    self.remove_status("Spider Bite")
                    type.type("Your spider bite is starting to heal. ")
                else:
                    damage += random.choice([7, 9, 11, 13, 15])
                    type.type("Your spider bite is purple and pussing. A trip to the doctors might be a good idea. ")
            print("\n")

            if damage >= self._health:
                self.hurt(damage)

        # Snake Bite
        if self.has_status("Snake Bite"):
            days_elapsed = self.get_days_elapsed("Snake Bite")
            if(self._clear_status):
                self.remove_status("Snake Bite")
                type.type("Your snake bite is starting to heal. ")
            elif days_elapsed == 0:
                damage += random.choice([2, 4])
                type.type("The fangmarks of your snake bite are faint but visible. There's some swelling. ")
            elif days_elapsed == 1:
                damage += random.choice([6, 8, 10, 12])
                type.type("Your snake bite is swolen, and very painful. ")
            elif days_elapsed == 2:
                damage += random.choice([8, 10, 12, 14, 16, 18])
                type.type("Your snake bite is really painful. You feel really nauseous. ")
            elif days_elapsed >= 3:
                damage += random.choice([7, 14, 18, 22, 26, 30])
                type.type("Your snake bite is turning black. A trip to the doctors is probably the right choice. ")
            print("\n")

            if damage >= self._health:
                self.hurt(damage)

        # Squirrel Bite
        if self.has_status("Squirrel Bite"):
            days_elapsed = self.get_days_elapsed("Squirrel Bite")
            if(self._clear_status):
                self.remove_status("Squirrel Bite")
                type.type("Your squirrel bite is starting to heal. ")
            elif days_elapsed == 0:
                type.type("You look at the bite mark the squirrel left on your leg, but it's hard to tell if it's infected. A trip to the doctor's would solve all your worries.")
            elif ((days_elapsed >= 1) and self.has_status("Rabies")) or (days_elapsed < 5):
                type.type("Your squirrel bite looks the same as it did yesterday.")
            elif (days_elapsed == 5):
                self.remove_status("Squirrel Bite")
                type.type("Your squirrel bite is starting to heal. ")
            print("\n")

        # Rat Bite
        if self.has_status("Rat Bite"):
            days_elapsed = self.get_days_elapsed("Rat Bite")
            if(self._clear_status):
                self.remove_status("Rat Bite")
                type.type("Your rat bite is starting to heal. ")
            elif days_elapsed == 0:
                type.type("You look at the bite mark the rat left on your ankle. It hurts like a motherfucker, ")
                type.type("but it's hard to tell if the bite infected. A trip to the doctor's is what a smart person would do.")
            elif ((days_elapsed >= 1) and self.has_status("Rabies")) or (days_elapsed < 5):
                type.type("Your rat bite looks the same as it did yesterday. It might hurt worse, but it's hard to tell.")
            elif (days_elapsed == 5):
                self.remove_status("Rat Bite")
                type.type("Your rat bite is starting to heal. ")
            print("\n")

        # Rabies
        if self.has_status("Rabies"):
            days_elapsed = self.get_days_elapsed("Rabies")
            if(self._clear_status) and (days_elapsed<=3):
                self.remove_status("Rabies")
            elif days_elapsed==3:
                type.type(red("Your mouth has begun to foam. It seems you've contracted rabies. Death is inevitable, and it's hurdling towards you."))
                damage += random.choice([10, 30, 50, 70])
                self.lose_sanity(random.choice([5, 6, 7]))  # Rabies symptoms severely drain sanity
                print("\n")
            elif days_elapsed==4:
                type.type(red("The foaming has gotten worse, to the point where you begin to choke on it. You have a seizure in your car. Life is coming to an end."))
                damage += random.choice([50, 70, 90])
                self.lose_sanity(random.choice([8, 10, 12]))  # Advanced rabies destroys your mind
                print("\n")
            elif days_elapsed==5:
                type.slow(red(bright("Your mind has gone completely insane. You start tearing at your face, ripping away chunks of skin. The foam in your mouth turns red, and you feel yourself begin to fade from existance. You pull your eyes from their sockets, and scream in agony, as you die a painful death.")))
                self.kill()

            if damage >= self._health:
                self.hurt(damage)


        # Sicknesses
        # Cold
        if self.has_status("Cold"):
            self._is_sick = True
            days_elapsed = self.get_days_elapsed("Cold")
            if(self._clear_status):
                self.remove_status("Cold")
            elif days_elapsed == 0:
                damage += random.choice([2, 3, 6])
            elif days_elapsed == 1:
                damage += random.choice([2, 5, 7])
            elif days_elapsed > 3:
                random_chance = random.randrange(2)
                if random_chance == 0:
                    self.remove_status("Cold")
                else:
                    damage += random.choice([3, 4, 5, 6, 7, 8, 9])

        # Sore Throat
        if self.has_status("Sore Throat"):
            self._is_sick = True
            days_elapsed = self.get_days_elapsed("Sore Throat")
            if(self._clear_status):
                self.remove_status("Sore Throat")
            elif self.has_item("Cough Drops"):
                type.type("With your " + bright(magenta("Cough Drops")) + " in hand, ")
                type.type("you begin to suck each drop, one by one, until the box is empty, and your throat feels nice and cool.")
                self.use_item("Cough Drops")
                self.remove_status("Sore Throat")
                self.restore_sanity(4)
            elif days_elapsed == 0:
                damage += random.choice([1, 3, 5])
            elif days_elapsed == 1:
                damage += random.choice([2, 4, 5])
            elif days_elapsed > 3:
                random_chance = random.randrange(2)
                if random_chance == 0:
                    self.remove_status("Sore Throat")
                else:
                    damage += random.choice([5, 6])

        # Hepatitis
        if self.has_status("Hepatitis"):
            self._is_sick = True
            days_elapsed = self.get_days_elapsed("Hepatitis")
            if(self._clear_status):
                self.remove_status("Hepatitis")
            elif days_elapsed == 0:
                damage += random.choice([1, 3, 5])
            elif days_elapsed == 1:
                damage += random.choice([5, 6, 7])
            elif days_elapsed == 2:
                damage += random.choice([2, 7, 10, 12])
            elif days_elapsed == 3:
                damage += random.choice([2, 8, 15, 17, 20])
            elif days_elapsed == 4:
                damage += random.choice([3, 9, 18, 20, 25])
            elif days_elapsed > 4:
                random_chance = random.randrange(4)
                if random_chance == 0:
                    self.remove_status("Hepatitis")
                else:
                    damage += random.choice([5, 10, 15, 20, 25, 30])


        # Sets is_sick to False if you don't have any sicknesses, an prints a health update
        if (self._is_sick) and not (self.has_status("Hepatitis") and not self.has_status("Sore Throat") or self.has_status("Cold")):
            if self.has_status("Rabies"):
                type.type("With rabies in your system, you're lucky to be alive.")
            elif self.has_status("Snake Bite") or self.has_status("Spider Bite"):
                type.type("You may not be 100%, but at least you don't feel under the weather anymore.")
            else:
                type.type("You feel much less sick than you did yesterday, which is always good.")
            self._is_sick = False
            print("\n")

        # if player is sick, prints a sickness update
        if self._is_sick:
            type.type(self._lists.get_sickness_update())
            print("\n")

        # If sickness kills the player, this does it.
        if damage >= self._health:
                type.slow(bright(red(self._lists.get_sickness_death())))
                self.kill()

        # Sets is_injured to True if you have 1 or more injuries
        if len(self._injuries)>0:
            self._is_injured = True

        # Sets is_injured to False if you have 0 injuries, and prints a healed update
        if (self._is_injured) and len(self._injuries)==0:
            type.type("The injuries on your body are doing much better.")
            print("\n")
            self._is_injured = False
        
        # If you're injured, prints an injury update, and adds damage
        if self._is_injured:
            damage += len(self._injuries)
            type.type(self._lists.get_injury_update())
            print("\n")

        # If you took damage, this does it.
        if damage > 0:
            self.hurt(damage)

        self._clear_status = False

        # Sprays your car with Pest Control if you have a pest
        if self.has_pests() and self.has_item("Pest Control") and (not self.has_travel_restriction("Rain")) and (not self.has_travel_restriction("Wind")):
            type.type("Believing that there may be an unwanted pest somewhere in your car, ")
            type.type("you spray your " + magenta(bright("Pest Control")) + " throughout the vehicle, hoping that it'll solve your pest issues. ")
            self.kill_pests()
            type.type("After giving the wagon a minute to air out, you get back inside.")
            self.restore_sanity(3)
            print("\n")

        # Feeds Squirrely if you have Acorns
        if self.has_item("Bag of Acorns") and self.has_item("Squirrely"):
            type.type("You give Squirrely your " + magenta(bright("Bag of Acorns")) + ", and he goes to town, munching down all of them. What a good squirrel.")
            self.use_item("Bag of Acorns")
            self.restore_sanity(3)
            print("\n")

        # Gives Squirrely Status Update
        if self.has_item("Squirrely"):
            days_elapsed = self.get_days_elapsed("Squirrely Fed")
            if self.has_travel_restriction("rain") or self.has_travel_restriction("Wind"):
                type.type(self._lists.get_worried_squirrely_update())
            if days_elapsed == 0:
                type.type("Squirrely is well-fed, and happy as can be.")
                self.restore_sanity(2)
            elif days_elapsed <= 4:
                type.type(self._lists.get_fed_squirrely_update())
                self.restore_sanity(1)
            elif days_elapsed < 6:
                type.type(self._lists.get_hungry_squirrely_update())
            elif days_elapsed >= 6:
                random_chance = random.randrange(5)
                if random_chance == 0:
                    type.type("Looking around, you can't find Squirrely anywhere. No, seriously, you can't find him anywhere. ")
                    type.type("Beginning to panic, you start to tear the car apart, hoping that you'll find him somewhere. ")
                    type.type("You call out his name, 'Squirrely', 'Squirrely', but you get no response. ")
                    type.type("Tears start falling from your eyes. Is this really it? Is this really goodbye? ")
                    type.type("Poor Squrrely, all alone. You may never see your little Squirrely ever again.")
                    self.use_item("Squirrely")
                    self.meet("Squirrely")
                    self.lose_sanity(random.choice([3, 4, 5]))  # Losing Squirrely is devastating
                elif random_chance == 1:
                    type.type("Looking around, you can't find Squirrely anywhere. No, seriously, you can't find him anywhere. ")
                    type.type("And that smell, it reeks! You begin to fear for the worst. ")
                    type.type("Tearing the car apart, you find him, laying lifeless under the passenger seat. Poor Squirrely.")
                    print("\n")
                    type.type("Using an old shirt, you pick Squirrely off the floor of the wagon. ")
                    type.type("Carrying him into the woods, you set him down, and dig a hole. ")
                    type.type("You place Squirrely inside, cover him up with dirt, and place a flower over the grave. ")
                    type.type("Goodbye, Squirrely. I loved you.")
                    self.use_item("Squirrely")
                    self.meet("Dead Squirrely")
                    self.lose_sanity(random.choice([5, 6, 7]))  # Finding Squirrely dead is traumatic
                else:
                    type.type(self._lists.get_hungry_squirrely_update())
            print("\n")

        # COMPANION BONUS EFFECTS
        companions = self.get_all_companions()
        if len(companions) > 0:
            total_sanity_restore = 0
            has_weather = self.has_travel_restriction("Rain") or self.has_travel_restriction("Wind")
            for name, data in companions.items():
                if data["status"] == "alive":
                    comp_type = data["type"]
                    happiness = data.get("happiness", 50)

                    # =====================
                    # WHISKERS (Alley Cat)
                    # =====================
                    if name == "Whiskers":
                        if has_weather:
                            type.type(self._lists.get_whiskers_weather_update())
                            print("\n")
                        elif happiness >= 70:
                            type.type(self._lists.get_whiskers_happy_update())
                            print("\n")
                            total_sanity_restore += 2
                            # Whiskers senses danger - warns you about bad events
                            if random.randrange(15) == 0:
                                type.type(cyan(bright("Whiskers")) + " suddenly hisses at the shadows, ears flat. "
                                          "She stares at something you can't see, then slowly relaxes. "
                                          "Whatever it was, it's gone now. Good kitty.")
                                self.restore_sanity(1)
                                print("\n")
                            # Whiskers catches vermin
                            if random.randrange(25) == 0:
                                type.type(cyan(bright("Whiskers")) + " drops a dead mouse at your feet "
                                          "and looks at you with absolute pride. She's providing for the family. "
                                          "You pet her head. She earned it.")
                                print("\n")
                            # Whiskers finds something
                            if random.randrange(40) == 0:
                                found = random.randint(1, 3)
                                type.type(cyan(bright("Whiskers")) + " bats something shiny out from under the seat. "
                                          "It rolls to your feet. " + green("${:,}".format(found)) + ". Not bad for a cat.")
                                self.change_balance(found)
                                print("\n")
                        elif happiness >= 40:
                            type.type(self._lists.get_whiskers_morning_update())
                            print("\n")
                            total_sanity_restore += 1
                        else:
                            type.type(self._lists.get_whiskers_unhappy_update())
                            print("\n")
                            # Very unhappy Whiskers might leave
                            if happiness <= 15 and random.randrange(8) == 0:
                                type.type(red(bright("Whiskers")) + " looks at you one last time, then slips out the window. "
                                          "You call her name. " + cyan("'Whiskers!'") + " Nothing. "
                                          "She's gone. The car feels emptier already.")
                                self.companion_dies(name)
                                self.lose_sanity(random.choice([4, 5, 6]))
                                print("\n")
                                continue

                    # =====================
                    # LUCKY (Three-Legged Dog)
                    # =====================
                    elif name == "Lucky":
                        if has_weather:
                            type.type(self._lists.get_lucky_weather_update())
                            print("\n")
                        elif happiness >= 70:
                            type.type(self._lists.get_lucky_happy_update())
                            print("\n")
                            total_sanity_restore += 3
                            # Lucky guards the car
                            if random.randrange(20) == 0:
                                type.type(cyan(bright("Lucky")) + " growls at a stranger who wandered too close to your car. "
                                          "The stranger backs off immediately. Nobody messes with a three-legged dog "
                                          "with that much heart.")
                                self.restore_sanity(2)
                                print("\n")
                            # Lucky finds buried treasure
                            if random.randrange(35) == 0:
                                found = random.randint(2, 8)
                                type.type(cyan(bright("Lucky")) + " digs up something from the dirt outside. "
                                          "He drops it at your feet, tail going crazy. " + green("${:,}".format(found)) + 
                                          "! Good boy, Lucky!")
                                self.change_balance(found)
                                print("\n")
                            # Lucky brings you comfort when injured
                            if self._is_injured and random.randrange(3) == 0:
                                type.type(cyan(bright("Lucky")) + " lies down gently next to you, pressing his warm body "
                                          "against your side. He can tell you're hurting. Dogs always know.")
                                self.restore_sanity(3)
                                print("\n")
                        elif happiness >= 40:
                            type.type(self._lists.get_lucky_morning_update())
                            print("\n")
                            total_sanity_restore += 2
                        else:
                            type.type(self._lists.get_lucky_unhappy_update())
                            print("\n")
                            # Very unhappy Lucky might leave
                            if happiness <= 15 and random.randrange(8) == 0:
                                type.type(red(bright("Lucky")) + " stands by the car door, looking at you with those big brown eyes. "
                                          "He doesn't wag his tail. He doesn't whimper. He just... walks away. "
                                          "Three legs carrying him into the distance. You couldn't even bring yourself to stop him.")
                                self.companion_dies(name)
                                self.lose_sanity(random.choice([5, 6, 7]))
                                print("\n")
                                continue

                    # =====================
                    # MR. PECKS (Crow)
                    # =====================
                    elif name == "Mr. Pecks":
                        if has_weather:
                            type.type(self._lists.get_pecks_weather_update())
                            print("\n")
                        elif happiness >= 70:
                            type.type(self._lists.get_pecks_happy_update())
                            print("\n")
                            total_sanity_restore += 1
                            # Mr. Pecks finds money (his main bonus)
                            if random.randrange(12) == 0:
                                found = random.randint(1, 10)
                                type.type(cyan(bright("Mr. Pecks")) + " swoops down from the sky and drops something shiny "
                                          "right in your lap. It's " + green("${:,}".format(found)) + "! "
                                          "Where does he find this stuff? You stopped asking.")
                                self.change_balance(found)
                                print("\n")
                            # Mr. Pecks brings you an item
                            if random.randrange(50) == 0:
                                crow_items = ["Shiny Button", "Bottle Cap", "Paper Clip", "Lucky Penny"]
                                gift = random.choice(crow_items)
                                type.type(cyan(bright("Mr. Pecks")) + " lands on the dashboard with something in his beak. "
                                          "He places it down carefully and caws once. It's a " + bright(gift) + ". "
                                          "He looks at you like it's the Crown Jewels.")
                                print("\n")
                            # Mr. Pecks warns about danger
                            if random.randrange(20) == 0:
                                type.type(cyan(bright("Mr. Pecks")) + " goes absolutely ballistic, cawing and flapping. "
                                          "You look around — there's a sketchy dude eyeing your car. Mr. Pecks dive-bombs him. "
                                          "The dude runs. " + cyan("Air support."))
                                self.restore_sanity(1)
                                print("\n")
                        elif happiness >= 40:
                            type.type(self._lists.get_pecks_morning_update())
                            print("\n")
                            total_sanity_restore += 1
                            # Reduced money finding
                            if random.randrange(25) == 0:
                                found = random.randint(1, 3)
                                type.type(cyan(bright("Mr. Pecks")) + " drops " + green("${:,}".format(found)) + 
                                          " at your feet. Not his best haul. But he's trying.")
                                self.change_balance(found)
                                print("\n")
                        else:
                            type.type(self._lists.get_pecks_unhappy_update())
                            print("\n")
                            # Very unhappy Mr. Pecks might leave
                            if happiness <= 15 and random.randrange(8) == 0:
                                type.type(red(bright("Mr. Pecks")) + " caws once — sharp, final — and takes flight. "
                                          "He circles the car once. Just once. Then he's gone, "
                                          "a black speck disappearing into the morning sky. "
                                          "He took his shiny collection with him.")
                                self.companion_dies(name)
                                self.lose_sanity(random.choice([3, 4, 5]))
                                print("\n")
                                continue

                    # =====================
                    # PATCHES (Opossum)
                    # =====================
                    elif name == "Patches":
                        if has_weather:
                            type.type(self._lists.get_patches_weather_update())
                            print("\n")
                        elif happiness >= 70:
                            type.type(self._lists.get_patches_happy_update())
                            print("\n")
                            total_sanity_restore += 2
                            # Patches is nocturnal — she reports on the night
                            if random.randrange(15) == 0:
                                type.type(cyan(bright("Patches")) + " was up all night, and she looks like she has "
                                          "something to tell you. She clicks her tongue rapidly. "
                                          "You don't speak opossum, but her tone says " + cyan("'coast is clear.'"))
                                self.restore_sanity(1)
                                print("\n")
                            # Patches plays dead to scare someone
                            if random.randrange(30) == 0:
                                type.type("A stranger peers into your car and sees " + cyan(bright("Patches")) + 
                                          " lying motionless on the seat, mouth open, tongue out. "
                                          + red("'THERE'S A DEAD RAT IN THERE!'") + " they scream, and bolt. "
                                          "Patches opens one eye. Mission accomplished.")
                                print("\n")
                            # Patches eats car pests
                            if self.has_pests() and random.randrange(5) == 0:
                                type.type(cyan(bright("Patches")) + " found something crawling under the seat and ate it. "
                                          "She looks satisfied. Your pest problem just got a little smaller.")
                                self.kill_pests()
                                print("\n")
                        elif happiness >= 40:
                            type.type(self._lists.get_patches_morning_update())
                            print("\n")
                            total_sanity_restore += 1
                        else:
                            type.type(self._lists.get_patches_unhappy_update())
                            print("\n")
                            # Very unhappy Patches plays dead and won't stop
                            if happiness <= 15 and random.randrange(8) == 0:
                                type.type(red(bright("Patches")) + " plays dead one morning. You wait an hour. Two hours. "
                                          "She doesn't get up. You poke her gently. Nothing. "
                                          "Then you realize — she's not playing. She slipped away in the night. "
                                          "Quietly. Like she always did everything.")
                                self.companion_dies(name)
                                self.lose_sanity(random.choice([4, 5, 6]))
                                print("\n")
                                continue

                    # =====================
                    # RUSTY (Raccoon)
                    # =====================
                    elif name == "Rusty":
                        if has_weather:
                            type.type(self._lists.get_rusty_weather_update())
                            print("\n")
                        elif happiness >= 70:
                            type.type(self._lists.get_rusty_happy_update())
                            print("\n")
                            total_sanity_restore += 2
                            # Rusty steals things (his main bonus)
                            if random.randrange(15) == 0:
                                type.type(cyan(bright("Rusty")) + " waddles up to you with something behind his back... ")
                                stolen_items = ["Candy Bar", "Deck of Cards", "Flashlight", "Lighter",
                                                "Bag of Chips", "Sunglasses", "Pocket Knife"]
                                item = random.choice(stolen_items)
                                if not self.has_item(item):
                                    self.add_item(item)
                                    type.type("He holds up a " + bright(magenta(item)) + " with both tiny paws. "
                                              "Where did he get that? Don't ask. Just accept the gift.")
                                else:
                                    type.type("He presents a " + bright(item) + " you already have. "
                                              "It's the thought that counts. And the crime.")
                                print("\n")
                            # Rusty finds money
                            if random.randrange(20) == 0:
                                found = random.randint(1, 8)
                                type.type(cyan(bright("Rusty")) + " empties his tiny pockets — wait, raccoons don't have pockets. "
                                          "Where was he keeping " + green("${:,}".format(found)) + "? "
                                          "The mystery of Rusty deepens.")
                                self.change_balance(found)
                                print("\n")
                            # Rusty opens something for you
                            if random.randrange(35) == 0:
                                type.type(cyan(bright("Rusty")) + " picks the lock on the glovebox. "
                                          "No, wait, it wasn't locked. He just wanted to practice. "
                                          "Those little fingers are scary good.")
                                print("\n")
                        elif happiness >= 40:
                            type.type(self._lists.get_rusty_morning_update())
                            print("\n")
                            total_sanity_restore += 1
                            # Reduced stealing
                            if random.randrange(35) == 0:
                                stolen_items = ["Candy Bar", "Lighter", "Matches"]
                                item = random.choice(stolen_items)
                                if not self.has_item(item):
                                    self.add_item(item)
                                    type.type(cyan(bright("Rusty")) + " leaves a " + bright(magenta(item)) + 
                                              " on the dashboard. No fanfare. Just a gift.")
                                    print("\n")
                        else:
                            type.type(self._lists.get_rusty_unhappy_update())
                            print("\n")
                            # Very unhappy Rusty hoards everything and leaves
                            if happiness <= 15 and random.randrange(8) == 0:
                                type.type(red(bright("Rusty")) + " gathers up every single thing he's stolen. "
                                          "Arranges them neatly. Looks at you once — those little bandit eyes, "
                                          "unreadable — then disappears out the window with his whole collection. "
                                          "The car feels robbed. In every sense.")
                                self.companion_dies(name)
                                self.lose_sanity(random.choice([4, 5, 6]))
                                print("\n")
                                continue

                    # =====================
                    # SLICK (Rat)
                    # =====================
                    elif name == "Slick":
                        if has_weather:
                            type.type(self._lists.get_slick_weather_update())
                            print("\n")
                        elif happiness >= 70:
                            type.type(self._lists.get_slick_happy_update())
                            print("\n")
                            total_sanity_restore += 1
                            # Slick finds escape routes
                            if random.randrange(18) == 0:
                                type.type(cyan(bright("Slick")) + " squeaks rapidly and gestures toward the back of the car. "
                                          "You look — there's a hole in the floor you never noticed. "
                                          "Slick already found three ways out. Just in case. Always just in case.")
                                self.restore_sanity(1)
                                print("\n")
                            # Slick warns you about danger
                            if random.randrange(20) == 0:
                                type.type(cyan(bright("Slick")) + " suddenly goes rigid, ears up, whiskers vibrating. "
                                          "He stares at the door. You lock it. Whatever he sensed, you trust his instincts.")
                                self.restore_sanity(1)
                                print("\n")
                            # Slick finds food
                            if random.randrange(30) == 0:
                                type.type(cyan(bright("Slick")) + " drags out a cracker he'd hidden behind the seat cushion. "
                                          "Then another. Then a whole stash of crumbs. He's been saving for a rainy day. "
                                          "Today, he shares.")
                                print("\n")
                        elif happiness >= 40:
                            type.type(self._lists.get_slick_morning_update())
                            print("\n")
                            total_sanity_restore += 1
                        else:
                            type.type(self._lists.get_slick_unhappy_update())
                            print("\n")
                            # Very unhappy Slick escapes
                            if happiness <= 15 and random.randrange(8) == 0:
                                type.type(red(bright("Slick")) + " squeezes through a crack in the car you didn't even know existed. "
                                          "Of course he knew. He mapped every exit on day one. "
                                          "He was always ready to leave. He was just hoping he wouldn't have to.")
                                self.companion_dies(name)
                                self.lose_sanity(random.choice([3, 4, 5]))
                                print("\n")
                                continue

                    # =====================
                    # HOPPER (Rabbit)
                    # =====================
                    elif name == "Hopper":
                        if has_weather:
                            type.type(self._lists.get_hopper_weather_update())
                            print("\n")
                        elif happiness >= 70:
                            type.type(self._lists.get_hopper_happy_update())
                            print("\n")
                            total_sanity_restore += 2
                            # Hopper brings luck
                            if random.randrange(15) == 0:
                                found = random.randint(1, 5)
                                type.type(cyan(bright("Hopper")) + " binkies right onto your lap and a " + 
                                          green("${:,}".format(found)) + " coin falls out of nowhere. "
                                          "Lucky rabbit. Literally. The luck is literal.")
                                self.change_balance(found)
                                print("\n")
                            # Hopper is therapeutic
                            if random.randrange(10) == 0:
                                type.type(cyan(bright("Hopper")) + " crawls into your lap and tooth-purrs. "
                                          "The gentle vibration is better than meditation. Better than therapy. "
                                          "This rabbit is the single most calming force in your life.")
                                self.restore_sanity(3)
                                print("\n")
                            # Hopper finds food
                            if random.randrange(30) == 0:
                                type.type(cyan(bright("Hopper")) + " digs up a patch of clover outside the car. "
                                          "She eats most of it but leaves some for you. "
                                          "You eat clover from the ground. This is your life now.")
                                print("\n")
                        elif happiness >= 40:
                            type.type(self._lists.get_hopper_morning_update())
                            print("\n")
                            total_sanity_restore += 1
                        else:
                            type.type(self._lists.get_hopper_unhappy_update())
                            print("\n")
                            # Very unhappy Hopper bolts
                            if happiness <= 15 and random.randrange(8) == 0:
                                type.type(red(bright("Hopper")) + " stares at the open car door. You see it in her eyes — "
                                          "the prey instinct, the survival override. She doesn't look at you. "
                                          "She just bolts. Fast as lightning, into the tall grass, "
                                          "and she's gone before you can even say her name.")
                                self.companion_dies(name)
                                self.lose_sanity(random.choice([4, 5, 6]))
                                print("\n")
                                continue

                    # =====================
                    # SQUIRRELLY (Companion System)
                    # =====================
                    elif name == "Squirrelly":
                        if has_weather:
                            type.type(self._lists.get_squirrelly_comp_weather_update())
                            print("\n")
                        elif happiness >= 70:
                            type.type(self._lists.get_squirrelly_comp_happy_update())
                            print("\n")
                            total_sanity_restore += 2
                            # Squirrelly hides acorns everywhere
                            if random.randrange(20) == 0:
                                type.type(cyan(bright("Squirrelly")) + " was busy last night. She buried acorns "
                                          "in your shoes, under the seat, inside the glove box, and somehow "
                                          "inside a sealed water bottle. The squirrel economy is booming.")
                                print("\n")
                            # Squirrelly finds money
                            if random.randrange(25) == 0:
                                found = random.randint(1, 4)
                                type.type(cyan(bright("Squirrelly")) + " chatters excitedly and presents you with " + 
                                          green("${:,}".format(found)) + " she found under a rock. "
                                          "She looks at you like she deserves a medal. She does.")
                                self.change_balance(found)
                                print("\n")
                            # Squirrelly makes you laugh
                            if random.randrange(12) == 0:
                                type.type(cyan(bright("Squirrelly")) + " stuffs both cheeks so full of seeds she looks like "
                                          "a tiny furry balloon. She tries to chirp and seeds spray everywhere. "
                                          "You laugh. Actually laugh. It's been a while.")
                                self.restore_sanity(2)
                                print("\n")
                        elif happiness >= 40:
                            type.type(self._lists.get_squirrelly_comp_morning_update())
                            print("\n")
                            total_sanity_restore += 1
                        else:
                            type.type(self._lists.get_squirrelly_comp_unhappy_update())
                            print("\n")
                            # Very unhappy Squirrelly runs away
                            if happiness <= 15 and random.randrange(8) == 0:
                                type.type(red(bright("Squirrelly")) + " sits on the window ledge, chittering softly. "
                                          "She looks at you once — those dark, shiny eyes — then leaps to a tree branch. "
                                          "Scampers up. Disappears into the canopy. "
                                          "You wait for an hour. She doesn't come back. She chose the trees.")
                                self.companion_dies(name)
                                self.lose_sanity(random.choice([4, 5, 6]))
                                print("\n")
                                continue

                    # =====================
                    # GENERIC / OTHER COMPANIONS
                    # =====================
                    else:
                        if happiness >= 50:
                            total_sanity_restore += 1
                        # Generic companion dialogue for any unrecognized names
                        if happiness >= 60:
                            dialogue = self._lists.get_companion_dialogue(name, "happy")
                            type.type(dialogue)
                            print("\n")
                        elif happiness < 30:
                            dialogue = self._lists.get_companion_dialogue(name, "sad")
                            type.type(dialogue)
                            print("\n")
            
            # Multi-companion interaction
            companion_count = sum(1 for n, d in companions.items() if d["status"] == "alive")
            if companion_count >= 2 and random.randrange(8) == 0:
                alive_names = [n for n, d in companions.items() if d["status"] == "alive"]
                pair = random.sample(alive_names, 2)
                interactions = [
                    cyan(bright(pair[0])) + " and " + cyan(bright(pair[1])) + " are cuddled up together in the back seat. The animal pile grows.",
                    cyan(bright(pair[0])) + " steals " + cyan(bright(pair[1])) + "'s food. A scuffle breaks out. Nobody wins. Crumbs everywhere.",
                    cyan(bright(pair[0])) + " grooms " + cyan(bright(pair[1])) + " gently. Cross-species friendship at its finest.",
                    cyan(bright(pair[0])) + " and " + cyan(bright(pair[1])) + " stare out opposite windows. Parallel lives. Same car.",
                    cyan(bright(pair[0])) + " chases " + cyan(bright(pair[1])) + " around the car. Is it playing? Is it war? Nobody knows. Both look happy.",
                    "You catch " + cyan(bright(pair[0])) + " sharing food with " + cyan(bright(pair[1])) + ". Your heart does something weird.",
                    cyan(bright(pair[0])) + " and " + cyan(bright(pair[1])) + " sleep touching noses. You take a mental photograph.",
                ]
                type.type(random.choice(interactions))
                print("\n")

            if total_sanity_restore > 0:
                if companion_count > 1:
                    type.type("Your animal family keeps you company. Their presence is comforting.")
                else:
                    alive_name = next((n for n, d in companions.items() if d["status"] == "alive"), None)
                    if alive_name:
                        type.type("Having " + cyan(bright(alive_name)) + " by your side makes the world a little less cruel.")
                self.restore_sanity(total_sanity_restore)
                print("\n")

    def get_unlocked_adventure_areas(self):
        """Returns a list of adventure areas the player can walk to.
        
        Unlock requirements:
        - The Road: Always available at rank 2+. No prerequisite events.
        - Woodlands: All 3 woodlands events (path, river, field) OR woodlands_adventure. Rank 3+ to walk.
        - Swamp: All 3 swamp events (stroll, wade, swim) OR swamp_adventure. Rank 4+ to walk.
        - Beach: All 3 beach events (stroll, swim, dive) OR beach_adventure. Rank 4+ to walk.
        - City: All 3 city events (streets, stroll, park) OR city_adventure. Rank 5 to walk.
        - Underwater: beach_adventure OR underwater_adventure. Rank 5 to walk.
        
        At rank 5, all adventures are available even if not yet visited."""
        areas = []
        rank = self.get_rank()
        
        # The Road - rank 2+ to walk, always available (no prerequisite events)
        if rank >= 2:
            areas.append(("The Road", "road_adventure"))
        
        # Check if player has completed all 3 events for each area
        all_woodlands_events = (self.has_met("Woodlands Path Event") and 
                                 self.has_met("Woodlands River Event") and 
                                 self.has_met("Woodlands Field Event"))
        
        all_swamp_events = (self.has_met("Swamp Stroll Event") and
                            self.has_met("Swamp Wade Event") and
                            self.has_met("Swamp Swim Event"))
        
        all_beach_events = (self.has_met("Beach Stroll Event") and
                            self.has_met("Beach Swim Event") and
                            self.has_met("Beach Dive Event"))
        
        all_city_events = (self.has_met("City Streets Event") and
                           self.has_met("City Stroll Event") and
                           self.has_met("City Park Event"))
        
        # Woodlands - rank 3+ to walk, must have done all 3 woodlands events OR woodlands_adventure
        if rank >= 3:
            if all_woodlands_events or self.has_met("Woodlands Adventure Event"):
                areas.append(("The Woodlands", "woodlands_adventure"))
        
        # Swamp - rank 4+ to walk, must have done all 3 swamp events OR swamp_adventure
        if rank >= 4:
            if all_swamp_events or self.has_met("Swamp Adventure Event"):
                areas.append(("The Swamp", "swamp_adventure"))
        
        # Beach - rank 4+ to walk, must have done all 3 beach events OR beach_adventure
        if rank >= 4:
            if all_beach_events or self.has_met("Beach Adventure Event"):
                areas.append(("The Beach", "beach_adventure"))
        
        # At rank 5, all adventures are available even if not visited yet
        if rank >= 5:
            # Add any not already in the list
            if ("The Woodlands", "woodlands_adventure") not in areas:
                areas.append(("The Woodlands", "woodlands_adventure"))
            if ("The Swamp", "swamp_adventure") not in areas:
                areas.append(("The Swamp", "swamp_adventure"))
            if ("The Beach", "beach_adventure") not in areas:
                areas.append(("The Beach", "beach_adventure"))
            # City - rank 5 to walk, must have done all 3 city events OR city_adventure
            if all_city_events or self.has_met("City Adventure Event"):
                areas.append(("The City", "city_adventure"))
            # Underwater - rank 5 to walk, unlocked by beach_adventure OR underwater_adventure
            if self.has_met("Beach Adventure Event") or self.has_met("Underwater Adventure Event"):
                areas.append(("The Ocean Depths", "underwater_adventure"))
        
        return areas
