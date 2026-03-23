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

class CarEventsMixin:
    """Car events: All vehicle breakdown, repair, and consequence events"""

    # ==========================================
    # DISPATCHER — called by the event system
    # ==========================================

    def random_car_trouble(self):
        """Pick a rank-appropriate car problem at random and trigger it."""
        if self.has_item("War Wagon"):
            type.type("The " + cyan(bright("War Wagon")) + "'s engine is alive — really alive. It diagnosed the problem before you even started the car.")
            print()
            type.type("Self-repair complete. The car rumbles contentedly. Not a scratch. Not a squeak.")
            self.restore_sanity(5)
            return
        if self.has_item("Immortal Vehicle"):
            type.type("The " + cyan(bright("Immortal Vehicle")) + " self-diagnoses. Self-repairs. Your car is more reliable than gravity.")
            print()
            type.type("Problem solved before it was a problem.")
            self.restore_sanity(3)
            return
        rank = self.get_rank()
        if self.has_item("Auto Mechanic") and random.randrange(5) == 0:
            type.type("You run your daily check with the " + magenta(bright("Auto Mechanic")) + " kit before anything can go wrong.")
            print()
            type.type("A loose connection — caught and re-tightened before the car even noticed. Car trouble averted.")
            self.restore_sanity(3)
            print()
            return
        if self.has_item("Roadside Shield") and random.randrange(3) == 0:
            type.type("The " + magenta(bright("Roadside Shield")) + "'s pre-wired systems flag an issue before it becomes a problem. Minor adjustment. No event needed.")
            self.restore_sanity(2)
            print()
            return

        cheap = [
            self.corroded_battery_terminals, self.fuse_blown, self.abs_light_on,
            self.slow_tire_leak, self.headlights_burned_out, self.windshield_cracked,
            self.hail_damage, self.key_wont_turn, self.window_wont_roll_up,
            self.trunk_wont_close, self.bald_tires_noticed, self.exhaust_leak_loud,
            self.thermostat_stuck, self.nail_in_tire, self.check_engine_light_on,
            self.strange_engine_noise, self.wheel_alignment_off, self.suspension_creaking,
            self.car_wont_go_in_reverse, self.gas_pedal_sticking, self.parking_brake_stuck,
            self.frozen_door_locks,
        ]
        mid = [
            self.dead_battery_afternoon, self.engine_overheating, self.battery_acid_leak,
            self.alternator_failing, self.brake_fluid_leak, self.fuel_pump_whining,
            self.clogged_fuel_filter, self.radiator_leak, self.water_pump_failing,
            self.power_steering_failure, self.frozen_fuel_line, self.car_alarm_malfunction,
            self.starter_motor_grinding, self.brakes_squealing, self.ran_out_of_gas,
            self.mystery_breakdown, self.engine_wont_turn_over, self.engine_oil_empty,
            self.oil_leak_spotted, self.tire_blowout, self.flooded_engine,
        ]
        expensive = [
            self.catalytic_converter_stolen, self.transmission_slipping, self.stuck_in_gear,
            self.broken_ball_joint, self.flooded_engine, self.mystery_breakdown,
            self.tire_blowout, self.engine_wont_turn_over,
        ]

        # Cost weights per rank: [cheap, mid, expensive]
        # As rank increases the car is older and problems get worse,
        # but the player can also afford repairs — tension increases either way
        cost_weights = [
            [7, 2, 1],  # poor: mostly cheap annoyances
            [5, 3, 2],  # cheap: mid problems start appearing
            [3, 4, 3],  # modest: balanced
            [2, 4, 4],  # rich: expensive problems more common
            [1, 3, 6],  # doughman: car is falling apart
            [1, 2, 7],  # nearly: everything is breaking at once
        ]
        weights = cost_weights[min(rank, 5)]
        tier = random.choices(["cheap", "mid", "expensive"], weights=weights, k=1)[0]
        if tier == "cheap":
            random.choice(cheap)()
        elif tier == "mid":
            random.choice(mid)()
        else:
            random.choice(expensive)()

    # ==========================================
    # CAR TROUBLE AFTERNOON EVENTS
    # These can waste days and require items to fix
    # ==========================================

    # === BATTERY ISSUES ===
    def dead_battery_afternoon(self):
        type.type("You try to start your car to head somewhere. Click. Click. Click. Nothing.")
        print()
        type.type("The battery is dead. Completely dead.")
        print()
        if self.has_item("Jumper Cables"):
            type.type("But wait - you have " + magenta(bright("Jumper Cables")) + "!")
            print()
            type.type("You flag down a passing driver who agrees to give you a jump.")
            type.type(" After a few minutes, your engine roars back to life.")
            print()
            type.type("Crisis averted. But you should probably get that battery looked at.")
            self.restore_sanity(3)
        elif self.has_item("Portable Battery Charger"):
            type.type("Luckily, you have a " + magenta(bright("Portable Battery Charger")) + "!")
            print()
            type.type("You hook it up and wait. After twenty minutes, your car starts.")
            print()
            type.type("Thank God for preparation.")
            self.restore_sanity(5)
        elif self.has_item("Power Grid"):
            type.type("You unclip the " + magenta(bright("Power Grid")) + " from your bag and press it to the dead battery.")
            print()
            type.type("It kicks the battery back to life with contempt. Engine roars. First try.")
            print()
            type.type("You didn't even need to pop the hood all the way.")
            self.restore_sanity(7)
        else:
            type.type("You have no way to jump it. You're stuck.")
            print()
            type.type("You spend the entire afternoon trying to flag someone down for help.")
            print()
            type.type("By the time someone finally helps, " + yellow("the sun is setting") + ".")
            print()
            type.type("You've wasted the whole day.")
            self.add_travel_restriction("Wasted Afternoon")
            self.lose_sanity(8)
        print()

    def corroded_battery_terminals(self):
        type.type("Your car starts sluggishly. The engine sounds weak, struggling.")
        print()
        type.type("You pop the hood and see the problem - the battery terminals are covered in white-green corrosion.")
        print()
        if self.has_item("Battery Terminal Cleaner") or self.has_item("Baking Soda"):
            item = "Battery Terminal Cleaner" if self.has_item("Battery Terminal Cleaner") else "Baking Soda"
            type.type("Good thing you have " + magenta(bright(item)) + ".")
            print()
            type.type("You clean off the corrosion and the car starts perfectly.")
            print()
            type.type("Preventive maintenance pays off.")
            if item == "Baking Soda":
                self.use_item("Baking Soda")
        else:
            type.type("You try scraping it off with a rock, but it's caked on thick.")
            print()
            type.type("The car barely runs. You limp to a mechanic who charges you " + red("$75") + " for a five-minute fix.")
            self.change_balance(-75)
            type.type("Afternoon wasted.")
            self.add_travel_restriction("Wasted Afternoon")
        print()

    def battery_acid_leak(self):
        type.type("There's a strange smell coming from under your hood. Acidic. Burning.")
        print()
        type.type("You open it up and see battery acid dripping. The battery casing is cracked.")
        print()
        type.type("This is dangerous. The acid could damage your engine components.")
        print()
        if self.get_balance() >= 150:
            type.type("You rush to an auto shop. New battery: " + red("$150") + ".")
            print()
            type.type("Expensive, but necessary. Your afternoon is gone.")
            self.change_balance(-150)
            self.add_travel_restriction("Wasted Afternoon")
        else:
            type.type("You can't afford a new battery. You try to contain the leak with duct tape.")
            print()
            type.type("It's a temporary fix at best. And dangerous.")
            self.add_danger("Leaking Battery")
            self.lose_sanity(10)
        print()

    # === ENGINE PROBLEMS ===
    def engine_overheating(self):
        if self.has_item("All-Weather Armor"):
            type.type("Car broke down in the heat. The " + magenta(bright("All-Weather Armor")) + " keeps you comfortable until help arrives.")
            print()
            type.type("Stranded in weather? Not a problem for you.")
            self.restore_sanity(5)
            return
        if self.has_item("War Wagon"):
            type.type("The " + cyan(bright("War Wagon")) + "'s thermal management kicks in. Engine temp drops instantly.")
            print()
            type.type("Your car has opinions about its own maintenance. They are correct opinions.")
            self.restore_sanity(5)
            return
        if self.has_item("Immortal Vehicle"):
            type.type("The " + cyan(bright("Immortal Vehicle")) + " has redundant cooling. This problem was solved in the design phase.")
            print()
            self.restore_sanity(3)
            return
        if self.has_item("Roadside Shield"):
            type.type("The " + cyan(bright("Roadside Shield")) + " kit includes coolant. Crisis averted in minutes.")
            print()
            self.restore_sanity(3)
            return
        if self.has_item("Oracle's Tome") or self.has_item("Gambler's Grimoire"):
            tome = "Oracle's Tome" if self.has_item("Oracle's Tome") else "Gambler's Grimoire"
            type.type("This morning, your " + cyan(bright(tome)) + " fell open to a dog-eared page. Two words underlined in red: " + italic("'CHECK COOLANT.'"))
            print()
            type.type("So you did. You topped off the reservoir before you left. The engine runs smooth. No steam. No crisis. No lost afternoon.")
            print()
            type.type("It's not magic. It's just reading.")
            self.restore_sanity(5)
            print()
            return
        type.type("Steam billows from under your hood. Your temperature gauge is in the red.")
        print()
        type.type("The engine is overheating. You pull over immediately.")
        print()
        if self.has_item("Coolant") or self.has_item("Antifreeze"):
            item = "Coolant" if self.has_item("Coolant") else "Antifreeze"
            type.type("You have " + magenta(bright(item)) + ". Smart.")
            print()
            type.type("You wait for the engine to cool, add the fluid, and you're back on the road.")
            print()
            type.type("Lost an hour, but could have been much worse.")
            self.use_item(item)
            self.restore_sanity(5)
        elif self.has_item("Water Bottles"):
            type.type("You pour your " + magenta(bright("Water Bottles")) + " into the radiator as an emergency fix.")
            print()
            type.type("It's not ideal, but it'll get you somewhere.")
            print()
            type.type("The engine makes concerning noises, but holds.")
            self.use_item("Water Bottles")
            self.add_danger("Cooling System Damage")
        elif self.has_item("Cool Down Kit"):
            type.type("You crack open the " + magenta(bright("Cool Down Kit")) + " and dump it on the engine block.")
            print()
            type.type("Steam erupts like a geyser. The temperature gauge drops from red to somewhere reasonable.")
            print()
            type.type("There's always a risk with rapid cooling — could crack a gasket, or could actually seal better under pressure.")
            self.use_item("Cool Down Kit")
            if random.randrange(4) == 0:
                type.type("A deep tick from the engine. You cracked a gasket. It still runs, but worse than before.")
                self.add_danger("Gasket Damage")
                self.lose_sanity(5)
            else:
                type.type("The rapid cooldown actually tightened the pressure seals. The engine runs cleaner than before.")
                self.restore_sanity(5)
        else:
            type.type("You have nothing to cool it down. You sit and wait.")
            print()
            type.type("And wait. And wait. Hours pass.")
            print()
            type.type("Eventually the engine cools enough to limp to a mechanic. " + red("$200") + " for repairs.")
            if self.get_balance() >= 200:
                self.change_balance(-200)
            else:
                type.type("You can't afford it. The mechanic takes your watch as collateral.")
                self.add_danger("Unpaid Mechanic Debt")
            self.add_travel_restriction("Wasted Afternoon")
            self.lose_sanity(10)
        print()

    def check_engine_light_on(self):
        type.type("The check engine light comes on. That ominous orange glow.")
        print()
        type.type("Could be nothing. Could be catastrophic. No way to know without a diagnostic.")
        print()
        if self.has_item("OBD Scanner"):
            type.type("You have an " + magenta(bright("OBD Scanner")) + ". You plug it in.")
            print()
            codes = random.choice([
                ("loose gas cap", 0, True),
                ("oxygen sensor failing", 85, True),
                ("catalytic converter issue", 300, False),
                ("misfiring cylinder", 150, True),
                ("mass airflow sensor", 120, True)
            ])
            type.type("Code reads: " + codes[0] + ".")
            print()
            if codes[1] == 0:
                type.type("You tighten your gas cap. Light goes off. Crisis averted.")
                self.restore_sanity(6)
            elif codes[2]:
                type.type("Not cheap, but at least you know what's wrong.")
                self.restore_sanity(4)
                self.add_danger("Engine Issue: " + codes[0])
            else:
                type.type("That's a big problem. Expensive to fix.")
                self.add_danger("Serious Engine Issue")
        elif self.has_item("Fortune Cards"):
            type.type("You lay the " + magenta(bright("Fortune Cards")) + " on the dashboard.")
            print()
            type.type("THE TOWER on the brake pedal. DEATH near the exhaust. Then a card labeled THE JOURNEY slides under the seat.")
            print()
            type.type("Your car hums something that sounds almost like approval. The cards say: the next car problem will be minor. Consider this your warning.")
            self.add_status("Car Prediction")
            self.restore_sanity(4)
        else:
            type.type("You have no way to read the code. You just have to hope it's nothing serious.")
            print()
            chance = random.randrange(5)
            if chance == 0:
                type.type("Your car suddenly dies in the middle of the road.")
                print()
                type.type("It was serious. Very serious. You spend the afternoon getting towed.")
                self.add_travel_restriction("Wasted Afternoon")
                self.add_danger("Major Engine Failure")
                self.lose_sanity(15)
            else:
                type.type("For now, the car keeps running. But that light haunts you.")
        print()

    def engine_wont_turn_over(self):
        type.type("You turn the key. The engine tries to catch but fails. Again and again.")
        print()
        type.type("It's not the battery - you can hear it trying. Something else is wrong.")
        print()
        problem = random.choice(["starter motor", "fuel pump", "ignition coil", "spark plugs"])
        type.type("After some investigation, you suspect it's the " + problem + ".")
        print()
        if self.has_item("Mobile Workshop"):
            type.type("You pop the trunk and open the " + magenta(bright("Mobile Workshop")) + " case.")
            print()
            type.type("It has exactly what you need for a failing " + problem + ". Five minutes later, the engine roars to life.")
            print()
            type.type("You didn't even get your hands that dirty.")
            self.restore_sanity(8)
        elif problem == "spark plugs" and self.has_item("Spare Spark Plugs"):
            type.type("Good thing you have " + magenta(bright("Spare Spark Plugs")) + "!")
            print()
            type.type("You swap them out. The engine roars to life.")
            self.use_item("Spare Spark Plugs")
        elif self.has_item("Tool Kit"):
            type.type("With your " + magenta(bright("Tool Kit")) + ", you attempt a DIY fix.")
            print()
            if random.randrange(3) == 0:
                type.type("You actually fix it! You surprise yourself.")
                self.restore_sanity(5)
            else:
                type.type("You make it worse. Much worse. Time to call a tow truck.")
                self.add_travel_restriction("Wasted Afternoon")
                self.add_danger("Engine Damage")
                self.lose_sanity(12)
        else:
            type.type("You have no tools, no knowledge. Just frustration.")
            print()
            type.type("You call for help. The afternoon evaporates waiting for a mechanic.")
            self.add_travel_restriction("Wasted Afternoon")
            self.lose_sanity(8)
        print()

    def strange_engine_noise(self):
        if self.has_item("Lucky Medallion") or self.has_item("Lucky Coin"):
            coin = "Lucky Medallion" if self.has_item("Lucky Medallion") else "Lucky Coin"
            type.type("Your engine is making a noise. A bad noise. Grinding? Clicking? Whining?")
            print()
            type.type("You reach into your pocket and close your hand around the " + cyan(bright(coin)) + ".")
            print()
            type.type("The noise changes pitch. Then fades. Then stops.")
            print()
            type.type("You sit in puzzled silence. The engine purrs like nothing happened. You stop asking questions.")
            self.restore_sanity(5)
            print()
            return
        type.type("Your engine is making a noise. A bad noise. Grinding? Clicking? Whining?")
        print()
        noise = random.choice(["grinding", "clicking", "whining", "knocking", "squealing"])
        type.type("It's " + noise + ". Definitely " + noise + ".")
        print()
        if noise == "squealing":
            type.type("Probably a belt. Could snap at any moment.")
            if self.has_item("Serpentine Belt"):
                type.type(" But you have a spare " + magenta(bright("Serpentine Belt")) + "!")
                print()
                type.type("You swap it out. Noise gone. You're a genius.")
                self.use_item("Serpentine Belt")
            else:
                type.type(" Every mile you drive, you're gambling on that belt holding.")
                self.add_danger("Failing Belt")
        elif noise == "knocking":
            type.type("That's bad. Really bad. That's internal engine damage.")
            print()
            type.type("You might be looking at a complete engine rebuild. Or a new car.")
            self.add_danger("Engine Knock")
            self.lose_sanity(15)
        else:
            type.type("Could be many things. None of them good.")
            if random.randrange(3) == 0:
                type.type(" You ignore it. The noise stops. Lucky.")
            else:
                type.type(" You ignore it. The noise gets worse. Much worse.")
                self.add_danger("Mysterious Engine Problem")
        print()

    def engine_oil_empty(self):
        type.type("You check your oil level. The dipstick comes up bone dry.")
        print()
        type.type("No oil. None. How long have you been driving like this?")
        print()
        if self.has_item("Motor Oil"):
            type.type("Thank God you have " + magenta(bright("Motor Oil")) + ".")
            print()
            type.type("You pour it in. The engine sounds happier immediately.")
            self.use_item("Motor Oil")
        else:
            type.type("You need to get oil immediately or your engine will seize.")
            print()
            type.type("You walk to the nearest gas station. It takes two hours.")
            print()
            type.type("Oil: " + red("$30") + ". Time lost: priceless.")
            if self.get_balance() >= 30:
                self.change_balance(-30)
            else:
                type.type("You can't even afford oil. You beg. Someone takes pity.")
            self.add_travel_restriction("Wasted Afternoon")
            self.lose_sanity(5)
        print()

    def oil_leak_spotted(self):
        type.type("There's a dark puddle under your car. You touch it. Oil. Thick and black.")
        print()
        type.type("You have an oil leak. Could be a gasket, could be worse.")
        print()
        if self.has_item("Oil Stop Leak"):
            type.type("You add your " + magenta(bright("Oil Stop Leak")) + " and hope for the best.")
            print()
            type.type("The leak slows. Not fixed, but manageable.")
            self.use_item("Oil Stop Leak")
        else:
            type.type("You'll need to keep adding oil until you can afford a real fix.")
            self.add_danger("Oil Leak")
            type.type(" Every day you don't fix this costs you more.")
        print()

    # === TIRE PROBLEMS ===
    def slow_tire_leak(self):
        type.type("Your steering feels off. You get out and check - one tire is low. Not flat, but definitely losing air.")
        print()
        if self.has_item("Tire Patch Kit"):
            type.type("You have a " + magenta(bright("Tire Patch Kit")) + ". You find the nail, pull it, patch the hole.")
            print()
            type.type("Good as new. Well, good enough.")
            self.use_item("Tire Patch Kit")
        elif self.has_item("Fix-a-Flat"):
            type.type("You use your " + magenta(bright("Fix-a-Flat")) + " to seal it temporarily.")
            print()
            type.type("Should hold for a while. Maybe.")
            self.use_item("Fix-a-Flat")
        else:
            type.type("You have to keep stopping to put air in. Every gas station. Every hour.")
            print()
            type.type("Your afternoon becomes a series of air pump visits.")
            self.add_travel_restriction("Wasted Afternoon")
            self.add_danger("Slow Tire Leak")
        print()

    def tire_blowout(self):
        type.type("BANG! Your car jerks violently to one side. A tire just blew out.")
        print()
        type.type("You fight the wheel, heart pounding, and manage to pull to the shoulder.")
        print()
        if self.has_item("Tire Ready Kit"):
            type.type("You open the trunk. The " + magenta(bright("Tire Ready Kit")) + " is already assembled, sitting right there.")
            print()
            type.type("Thirty seconds. You're back on the road before the adrenaline even fades.")
            print()
            type.type("Preparation is its own kind of luck.")
            self.use_item("Tire Ready Kit")
            self.restore_sanity(10)
        elif self.has_item("Spare Tire") and self.has_item("Car Jack"):
            type.type("You have a " + magenta(bright("Spare Tire")) + " and a " + magenta(bright("Car Jack")) + ".")
            print()
            type.type("You change the tire yourself. It takes an hour, but you're back on the road.")
            self.use_item("Spare Tire")
            self.restore_sanity(10)
        elif self.has_item("Spare Tire"):
            type.type("You have a spare, but no jack. You spend hours flagging down help.")
            print()
            type.type("A trucker finally stops and helps. Afternoon gone.")
            self.use_item("Spare Tire")
            self.add_travel_restriction("Wasted Afternoon")
        else:
            type.type("No spare. No jack. You're completely stranded.")
            print()
            type.type("You call a tow truck. " + red("$150") + " and four hours later, you have a new tire.")
            if self.get_balance() >= 150:
                self.change_balance(-150)
            else:
                type.type("You can't afford it. The driver leaves you by the road.")
                self.add_danger("Stranded")
            self.add_travel_restriction("Wasted Afternoon")
            self.lose_sanity(15)
        print()

    def bald_tires_noticed(self):
        type.type("You look at your tires and wince. The tread is almost gone. Bald spots everywhere.")
        print()
        type.type("These tires are dangerous. One good rain and you'll hydroplane.")
        print()
        type.type("New tires cost around " + red("$400") + " minimum. You don't have that.")
        print()
        type.type("You'll have to risk it. But every drive is now a gamble.")
        self.add_danger("Bald Tires")
        self.lose_sanity(5)
        print()

    def nail_in_tire(self):
        type.type("Thump. Thump. Thump. Something's wrong with one of your tires.")
        print()
        type.type("You pull over and find it - a nail, embedded deep in the rubber.")
        print()
        type.type("The tire is holding for now, but if you pull it out, it'll go flat instantly.")
        print()
        answer = ask.option("What do you do? ", ["pull it out", "leave it", "drive to shop"])
        if answer == "pull it out":
            if self.has_item("Tire Patch Kit"):
                type.type("You pull the nail and quickly apply your " + magenta(bright("Tire Patch Kit")) + ".")
                print()
                type.type("The patch holds. Nice save.")
                self.use_item("Tire Patch Kit")
            else:
                type.type("PSSSSSSS. The air rushes out. You have a flat tire now.")
                print()
                if self.has_item("Spare Tire"):
                    type.type("Time to put on that spare.")
                    self.use_item("Spare Tire")
                    self.add_travel_restriction("Wasted Afternoon")
                else:
                    type.type("No spare. You're stuck.")
                    self.add_travel_restriction("Wasted Afternoon")
                    self.lose_sanity(10)
        elif answer == "leave it":
            type.type("You leave the nail. Every drive, you wonder if today's the day it fails.")
            self.add_danger("Nail in Tire")
        else:
            type.type("You drive very slowly to the nearest tire shop. They fix it for " + red("$25") + ".")
            if self.get_balance() >= 25:
                self.change_balance(-25)
                type.type("Afternoon gone, but tire fixed.")
            else:
                type.type("You can't afford it. You leave with the nail still in.")
                self.add_danger("Nail in Tire")
            self.add_travel_restriction("Wasted Afternoon")
        print()

    # === ELECTRICAL ISSUES ===
    def headlights_burned_out(self):
        type.type("Your headlights flicker and die. Both of them. At the same time.")
        print()
        type.type("You can't drive at night without headlights. That's illegal and suicidal.")
        print()
        if self.has_item("Spare Headlight Bulbs"):
            type.type("You have " + magenta(bright("Spare Headlight Bulbs")) + ". Smart thinking.")
            print()
            type.type("You replace them in the parking lot. You're back in business.")
            self.use_item("Spare Headlight Bulbs")
        else:
            type.type("Auto parts store. " + red("$40") + " for new bulbs. Plus an hour of fumbling in the engine bay.")
            if self.get_balance() >= 40:
                self.change_balance(-40)
                self.add_travel_restriction("Wasted Afternoon")
            else:
                type.type("You can't afford them. You'll have to stay put until you can.")
                self.add_travel_restriction("No Headlights")
                self.add_danger("No Headlights")
        print()

    def alternator_failing(self):
        type.type("Your dashboard dims. Your headlights flicker. Your radio cuts out.")
        print()
        type.type("The alternator is dying. Without it, your battery won't charge.")
        print()
        type.type("You might have 30 minutes of driving left. Maybe less.")
        print()
        
        if self.has_item("Power Grid"):
            type.type("You click open the Power Grid system. Diagnostic complete: failing alternator detected.")
            print()
            type.type("Electrical bypass engaged. The dashboard glows. The car runs perfectly.")
            print()
            self.use_item("Power Grid")
            self.restore_sanity(5)
            print()
            return
        
        if self.get_balance() >= 350:
            type.type("You race to a mechanic. New alternator: " + red("$350") + ". Your whole afternoon and then some.")
            self.change_balance(-350)
            self.add_travel_restriction("Wasted Afternoon")
        else:
            type.type("You can't afford a new alternator. Your car dies in a parking lot.")
            print()
            type.type("You're stuck here until you can afford repairs.")
            self.add_travel_restriction("Dead Alternator")
            self.add_danger("Dead Alternator")
            self.lose_sanity(15)
        print()

    def fuse_blown(self):
        type.type("Something electrical stopped working. Radio? Wipers? Power windows? Something.")
        print()
        type.type("You check the fuse box and find a blown fuse.")
        print()
        if self.has_item("Spare Fuses"):
            type.type("You pop in a spare from your " + magenta(bright("Spare Fuses")) + " kit. Fixed in seconds.")
            self.use_item("Spare Fuses")
        else:
            type.type("You don't have a spare. You drive to an auto shop.")
            print()
            type.type("$5 for a fuse, but an hour of your life wasted.")
            if self.get_balance() >= 5:
                self.change_balance(-5)
            self.add_travel_restriction("Wasted Afternoon")
        print()

    def car_alarm_malfunction(self):
        type.type("Your car alarm starts going off. For no reason. At 2 PM.")
        print()
        type.type("BEEP BEEP BEEP BEEP BEEP BEEP BEEP BEEP")
        print()
        type.type("You try the remote. Nothing. You try starting the car. Nothing. It just keeps screaming.")
        print()
        type.type("People are staring. Someone calls the cops. This is a nightmare.")
        print()
        if self.has_item("Tool Kit"):
            type.type("You grab your " + magenta(bright("Tool Kit")) + " and disconnect the battery to stop the noise.")
            print()
            type.type("Silence. Sweet silence. But now you need to figure out the real problem.")
            self.restore_sanity(8)
            self.add_travel_restriction("Wasted Afternoon")
        elif self.has_item("EMP Device"):
            type.type("You aim the " + magenta(bright("EMP Device")) + " at the alarm box. One pulse.")
            print()
            type.type("Silence. The car alarm is dead. The radio is also dead. Your phone needs a reboot.")
            print()
            type.type("Worth it.")
            self.use_item("EMP Device")
            self.add_danger("EMP Side Effects")
            self.restore_sanity(10)
        else:
            type.type("You have no way to disable it. The alarm runs until the battery dies.")
            print()
            type.type("Three hours. Three hours of beeping. Your sanity doesn't survive intact.")
            self.add_travel_restriction("Wasted Afternoon")
            self.lose_sanity(20)
        print()

    def starter_motor_grinding(self):
        type.type("When you turn the key, there's a horrible grinding noise from under the hood.")
        print()
        type.type("The starter motor is dying. Every start could be its last.")
        print()
        type.type("Starter motors cost around " + red("$200-400") + " to replace.")
        print()
        type.type("For now, it still works. Barely. Loudly. Worryingly.")
        self.add_danger("Failing Starter Motor")
        self.lose_sanity(5)
        print()

    # === BRAKE PROBLEMS ===
    def brakes_squealing(self):
        type.type("Your brakes are squealing. That metal-on-metal sound that means trouble.")
        print()
        type.type("The brake pads are worn. If you don't replace them, you'll damage the rotors.")
        print()
        if self.has_item("Brake Pads"):
            type.type("You have spare " + magenta(bright("Brake Pads")) + " and the knowledge to install them.")
            print()
            type.type("An hour of work later, your brakes are like new.")
            self.use_item("Brake Pads")
        else:
            type.type("New brake pads: " + red("$150-300") + " at a shop. Money you don't have.")
            print()
            type.type("You drive carefully, knowing your brakes could fail.")
            self.add_danger("Worn Brake Pads")
        print()

    def brake_fluid_leak(self):
        type.type("You press the brake pedal. It goes all the way to the floor. Almost no resistance.")
        print()
        type.type("That's brake fluid leaking. That's extremely dangerous.")
        print()
        if self.has_item("Brake Fluid"):
            type.type("You add " + magenta(bright("Brake Fluid")) + " to the reservoir. It's a temporary fix.")
            print()
            type.type("The leak will continue. You need real repairs.")
            self.use_item("Brake Fluid")
            self.add_danger("Brake Fluid Leak")
        else:
            type.type("You cannot drive this car. Not safely. Not at all.")
            print()
            type.type("You're stuck until you can fix this.")
            self.add_travel_restriction("Brake Failure")
            self.add_danger("Brake Failure")
            self.lose_sanity(15)
        print()

    def abs_light_on(self):
        type.type("The ABS warning light comes on. Your anti-lock brakes have a problem.")
        print()
        type.type("Regular brakes still work. Probably. But in an emergency...")
        print()
        type.type("You add it to the list of things wrong with your car.")
        self.add_danger("ABS Malfunction")
        self.lose_sanity(3)
        print()

    # === FUEL SYSTEM ISSUES ===
    def ran_out_of_gas(self):
        type.type("Your car sputters. Coughs. Dies. You coast to a stop.")
        print()
        type.type("Out of gas. Completely out. How did you not notice?")
        print()
        if self.has_item("SOS Kit"):
            type.type("The " + magenta(bright("SOS Kit")) + "'s smoke and mirrors flag down three passing cars in ten minutes.")
            print()
            type.type("Fastest roadside help you've ever had.")
            self.use_item("SOS Kit")
            self.restore_sanity(5)
            print()
            return
        if self.has_item("Gas Can"):
            type.type("You have an emergency " + magenta(bright("Gas Can")) + ". Enough to get to a station.")
            print()
            type.type("Crisis averted by preparation.")
            self.use_item("Gas Can")
        else:
            type.type("You have to walk to a gas station. Buy a can. Fill it. Walk back.")
            print()
            type.type("Two hours of your life, gone. Plus the cost of the can and gas: " + red("$35") + ".")
            if self.get_balance() >= 35:
                self.change_balance(-35)
                self.add_item("Gas Can")  # At least you now own a can
            else:
                type.type("You can't even afford gas. You beg strangers. Someone eventually helps.")
                self.lose_sanity(10)
            self.add_travel_restriction("Wasted Afternoon")
        print()

    def fuel_pump_whining(self):
        type.type("There's a whining noise when your car runs. Coming from the fuel tank area.")
        print()
        type.type("The fuel pump is failing. When it goes completely, your car won't run at all.")
        print()
        type.type("Fuel pumps cost " + red("$400-600") + " to replace. Plus labor.")
        print()
        type.type("Every time you start your car, you wonder if this is the last time.")
        self.add_danger("Failing Fuel Pump")
        self.lose_sanity(8)
        print()

    def clogged_fuel_filter(self):
        type.type("Your car hesitates when accelerating. Stutters. Struggles.")
        print()
        type.type("Could be a clogged fuel filter. Cheap fix if you catch it early.")
        print()
        if self.has_item("Fuel Filter"):
            type.type("You have a spare " + magenta(bright("Fuel Filter")) + ". You swap it out.")
            print()
            type.type("The car runs smoother immediately.")
            self.use_item("Fuel Filter")
        else:
            type.type("You'll need to get one. " + red("$15-30") + " for the part, plus your time.")
            if self.get_balance() >= 30:
                self.change_balance(-30)
            self.add_travel_restriction("Wasted Afternoon")
        print()

    # === TRANSMISSION PROBLEMS ===
    def transmission_slipping(self):
        type.type("Your car revs high but barely accelerates. The transmission is slipping.")
        print()
        type.type("This is bad. Transmission repairs are the most expensive fixes there are.")
        print()
        if self.has_item("Miracle Lube"):
            type.type("You pop the hood and squeeze one shot of " + magenta(bright("Miracle Lube")) + " into the transmission.")
            print()
            type.type("The grinding stops instantly. The gears shift smooth as silk.")
            print()
            type.type("You don't know how it works. You don't care.")
            self.use_item("Miracle Lube")
            self.restore_sanity(8)
        elif self.has_item("Transmission Fluid"):
            type.type("You check the fluid level. Low. You add " + magenta(bright("Transmission Fluid")) + ".")
            print()
            type.type("It helps. Temporarily. The damage is already done.")
            self.use_item("Transmission Fluid")
        else:
            type.type("You don't even want to know what this costs to fix. Thousands. Easily.")
            print()
            type.type("You drive gently and pray.")
            self.add_danger("Transmission Damage")
            self.lose_sanity(20)
        print()

    def stuck_in_gear(self):
        type.type("Your car is stuck in second gear. It won't shift up or down.")
        print()
        type.type("You can drive, technically, but not fast. And not well.")
        print()
        type.type("Every other car on the road is passing you, honking angrily.")
        print()
        type.type("You limp to a mechanic. " + red("$300") + " to fix a linkage issue.")
        if self.get_balance() >= 300:
            self.change_balance(-300)
            type.type(" At least it wasn't the transmission itself.")
        else:
            type.type(" You can't afford it. You'll have to drive like this.")
            self.add_danger("Stuck In Second")
        self.add_travel_restriction("Wasted Afternoon")
        print()

    # === COOLING SYSTEM ===
    def radiator_leak(self):
        type.type("Green fluid is pooling under your car. Antifreeze. Your radiator is leaking.")
        print()
        if self.has_item("Radiator Stop Leak"):
            type.type("You pour in " + magenta(bright("Radiator Stop Leak")) + " and cross your fingers.")
            print()
            type.type("The leak slows. Not stopped, but manageable.")
            self.use_item("Radiator Stop Leak")
            self.add_danger("Radiator Damage")
        else:
            type.type("Without coolant, your engine will overheat. And die.")
            print()
            type.type("Radiator repair: " + red("$200-400") + ". Time to start begging.")
            if self.get_balance() >= 200:
                self.change_balance(-200)
                self.add_travel_restriction("Wasted Afternoon")
            else:
                type.type("You can't afford it. Your car is essentially undriveable.")
                self.add_travel_restriction("Radiator Failure")
                self.add_danger("Radiator Failure")
            self.lose_sanity(10)
        print()

    def thermostat_stuck(self):
        type.type("Your temperature gauge is acting weird. Too cold. Too hot. Wildly swinging.")
        print()
        type.type("The thermostat is stuck. It's not regulating properly.")
        print()
        if self.has_item("Thermostat"):
            type.type("You have a spare " + magenta(bright("Thermostat")) + ". You swap it out.")
            print()
            type.type("Temperature stable again. Good catch.")
            self.use_item("Thermostat")
        else:
            type.type("It's a cheap part but takes time to replace. " + red("$50") + " at a shop.")
            if self.get_balance() >= 50:
                self.change_balance(-50)
            self.add_travel_restriction("Wasted Afternoon")
        print()

    def water_pump_failing(self):
        type.type("There's a grinding noise from your water pump. And your car is starting to overheat.")
        print()
        type.type("When the water pump goes completely, your engine will follow.")
        print()
        type.type("Water pump replacement: " + red("$300-500") + ". Not optional.")
        print()
        if self.get_balance() >= 300:
            type.type("You get it fixed immediately. Afternoon gone, but car saved.")
            self.change_balance(-300)
            self.add_travel_restriction("Wasted Afternoon")
        else:
            type.type("You can't afford it. You drive with one eye on the temperature gauge.")
            self.add_danger("Failing Water Pump")
            self.lose_sanity(12)
        print()

    # === STEERING/SUSPENSION ===
    def power_steering_failure(self):
        type.type("The steering wheel suddenly becomes incredibly hard to turn.")
        print()
        type.type("Power steering is out. Driving is now an arm workout.")
        print()
        if self.has_item("Power Steering Fluid"):
            type.type("You check the reservoir. Empty. You add " + magenta(bright("Power Steering Fluid")) + ".")
            print()
            type.type("Steering returns to normal. There's probably a leak though.")
            self.use_item("Power Steering Fluid")
            self.add_danger("Power Steering Leak")
        else:
            type.type("You can technically still drive. It just takes all your strength.")
            print()
            type.type("Your arms are going to be very sore tomorrow.")
            self.add_danger("No Power Steering")
            self.hurt(10)
        print()

    def wheel_alignment_off(self):
        type.type("Your car pulls hard to one side. You have to fight the wheel to go straight.")
        print()
        type.type("Alignment is off. Probably from all those potholes.")
        print()
        type.type("Alignment service: " + red("$75-100") + ". Plus the time.")
        print()
        if self.get_balance() >= 75:
            type.type("You get it done. Afternoon spent, but car drives straight again.")
            self.change_balance(-75)
            self.add_travel_restriction("Wasted Afternoon")
        else:
            type.type("You'll have to live with it. Your tires will wear unevenly.")
            self.add_danger("Bad Alignment")
        print()

    def suspension_creaking(self):
        type.type("Every bump makes your car creak and groan like an old house.")
        print()
        type.type("The suspension is worn. Shocks, struts, something.")
        print()
        type.type("Suspension work is expensive. " + red("$500-1000") + " or more.")
        print()
        type.type("You add it to the list of things you can't afford to fix.")
        self.add_danger("Worn Suspension")
        self.lose_sanity(5)
        print()

    def broken_ball_joint(self):
        type.type("There's a terrifying clunk from your front wheel when you turn.")
        print()
        type.type("Ball joint. If that breaks while driving, you lose the wheel. Literally.")
        print()
        type.type("This isn't optional. This is fix-now-or-die territory.")
        print()
        if self.get_balance() >= 200:
            type.type("You get it fixed immediately. " + red("$200") + ". Afternoon gone.")
            self.change_balance(-200)
            self.add_travel_restriction("Wasted Afternoon")
        else:
            type.type("You can't afford it. You drive at 10 mph, praying with every turn.")
            self.add_danger("Broken Ball Joint")
            self.lose_sanity(15)
        print()

    # === EXHAUST SYSTEM ===
    def exhaust_leak_loud(self):
        type.type("Your car sounds like a motorcycle. Or a tractor. Incredibly loud.")
        print()
        type.type("Exhaust leak. Could be a hole in the pipe or a bad muffler.")
        print()
        type.type("Everyone stares at you. Cops give you looks.")
        print()
        if self.has_item("Exhaust Tape"):
            type.type("You use " + magenta(bright("Exhaust Tape")) + " to patch the hole temporarily.")
            print()
            type.type("It's quieter. Mostly. Still louder than normal.")
            self.use_item("Exhaust Tape")
            self.add_danger("Patched Exhaust")
        else:
            type.type("Muffler replacement: " + red("$100-200") + ". Plus the embarrassment of driving there.")
            if self.get_balance() >= 100:
                self.change_balance(-100)
                self.add_travel_restriction("Wasted Afternoon")
            else:
                type.type("You'll have to drive loud and proud. Or ashamed. Mostly ashamed.")
                self.add_danger("Loud Exhaust")
        print()

    def catalytic_converter_stolen(self):
        if self.has_item("Rolling Fortress"):
            type.type("You check under the car. Someone tried to get at your catalytic converter.")
            print()
            type.type("The " + magenta(bright("Rolling Fortress")) + "'s layered underbody defenses triggered. They got a screwdriver stuck in the shield plating and fled.")
            print()
            type.type("One less repair bill. The fortress earns its name.")
            self.restore_sanity(5)
            print()
            return
        if self.has_item("Fortified Perimeter"):
            type.type("The " + cyan(bright("Fortified Perimeter")) + "'s trip-sensors activated. Thief ran.")
            print()
            self.restore_sanity(3)
            return
        type.type("You start your car and it sounds like a dragster. Way too loud.")
        print()
        type.type("You look under the car. Your catalytic converter is GONE. Someone stole it.")
        print()
        type.type("Catalytic converters contain precious metals. Thieves love them.")
        print()
        type.type("Replacement: " + red("$1000-2500") + ". You're going to be loud for a while.")
        self.add_danger("Missing Catalytic Converter")
        self.lose_sanity(20)
        type.type(" You feel violated. Someone was under your car while you slept.")
        if self.has_item("Security Bypass"):
            print()
            type.type("You use the " + magenta(bright("Security Bypass")) + " to trace the thief's route. You find their car parked a block away — and their radio is far nicer than yours.")
            print()
            type.type("Poetic justice. You pocket their stereo and call it even.")
            self.change_balance(50)
        print()

    # === WEATHER DAMAGE ===
    def hail_damage(self):
        type.type("Last night's storm left your car covered in dents. Hail damage.")
        print()
        type.type("Your hood, roof, and trunk look like a golf ball. Dimpled everywhere.")
        print()
        type.type("Cosmetic damage. Car still runs. But your pride took a hit.")
        self.add_danger("Hail Damage")
        self.lose_sanity(8)
        print()

    def flooded_engine(self):
        type.type("You drove through a deep puddle. Your engine sputtered and died.")
        print()
        type.type("Water got into the intake. The engine is hydrolocked.")
        print()
        type.type("This could be catastrophic or just need time to dry out.")
        print()
        chance = random.randrange(5)
        if chance == 0:
            type.type("The engine is destroyed. Water doesn't compress. Pistons bent.")
            print()
            type.type("Your car is dead. You need a new engine or a new car.")
            self.add_danger("Hydrolocked Engine")
            self.add_travel_restriction("Destroyed Engine")
            self.lose_sanity(30)
        else:
            type.type("After a few hours of drying, the engine starts again. Lucky.")
            print()
            type.type("There might be lingering damage. Time will tell.")
            self.add_travel_restriction("Wasted Afternoon")
            self.lose_sanity(10)
        print()

    def windshield_cracked(self):
        type.type("A rock kicked up by a truck just hit your windshield. CRACK.")
        print()
        type.type("A spiderweb of cracks spreads across your field of vision.")
        print()
        type.type("Windshield replacement: " + red("$200-400") + ". You can't afford that.")
        print()
        type.type("You'll drive with cracks. It'll get worse in the cold.")
        self.add_danger("Cracked Windshield")
        self.lose_sanity(5)
        print()

    def frozen_door_locks(self):
        if self.has_danger("It's Summer"):
            return  # Skip in summer
        type.type("The temperature dropped overnight. Your door locks are frozen solid.")
        print()
        type.type("You can't get into your own car.")
        print()
        if self.has_item("Lock De-Icer"):
            type.type("You spray " + magenta(bright("Lock De-Icer")) + " into the keyhole. A minute later, you're in.")
            self.use_item("Lock De-Icer")
        elif self.has_item("Lighter"):
            type.type("You heat your key with your " + magenta(bright("Lighter")) + " and carefully thaw the lock.")
            print()
            type.type("Primitive, but effective.")
            self.restore_sanity(3)
        else:
            type.type("You spend an hour breathing on the lock, rubbing it with your hands.")
            print()
            type.type("Eventually it thaws. But you've lost precious time.")
            self.add_travel_restriction("Wasted Afternoon")
            self.hurt(5)  # Cold damage
        print()

    def frozen_fuel_line(self):
        if self.has_danger("It's Summer"):
            return
        type.type("Your car won't start. The fuel line is frozen.")
        print()
        type.type("This happens when there's water in the fuel system and it freezes.")
        print()
        if self.has_item("Fuel Line Antifreeze"):
            type.type("You add " + magenta(bright("Fuel Line Antifreeze")) + " and wait for it to work.")
            print()
            type.type("After twenty minutes, the car starts.")
            self.use_item("Fuel Line Antifreeze")
        else:
            type.type("You have to wait for it to thaw naturally. Hours pass.")
            print()
            type.type("Your entire day is spent huddled in your cold, non-running car.")
            self.add_travel_restriction("Wasted Afternoon")
            self.hurt(15)
            self.lose_sanity(10)
        print()

    # === RANDOM BREAKDOWNS ===
    def mystery_breakdown(self):
        if self.has_item("War Wagon"):
            type.type("The " + cyan(bright("War Wagon")) + " predicts potholes and avoids them. It self-diagnoses. The 'breakdown' resolves before it becomes one.")
            print()
            type.type("The car rumbles. Satisfied.")
            self.restore_sanity(8)
            return
        if self.has_item("Immortal Vehicle"):
            type.type(cyan(bright("Immortal Vehicle")) + " — self-repairing, self-defending. Whatever was about to break fixed itself.")
            print()
            self.restore_sanity(5)
            return
        if self.has_item("Auto Mechanic"):
            type.type("The " + cyan(bright("Auto Mechanic")) + " kit has the part. Of course it does.")
            print()
            type.type("Fifteen minutes. Good as new.")
            self.restore_sanity(3)
            return
        if self.has_item("Vermin Bomb"):
            self.use_item("Vermin Bomb")
            type.type("Your car just... stops. You pop the hood. Mice. Mice have chewed through half your wiring harness.")
            print()
            type.type("You detonate the " + magenta(bright("Vermin Bomb")) + " in the back seat. The fumigation is immediate, total, and almost certainly illegal.")
            print()
            type.type("The smell will last three days. But the car is CLEAN. And mice, unlike electrical gremlins, don't come back twice.")
            self.restore_sanity(5)
            self.add_danger("Chewed Wiring")
            print()
            return
        type.type("Your car just... stops. No warning. No sound. Just dead.")
        print()
        type.type("You try everything. Key. Lights. Radio. Nothing responds.")
        print()
        type.type("It's like the entire electrical system died at once.")
        print()
        chance = random.randrange(5)
        if chance == 0:
            type.type("After sitting for an hour, it mysteriously starts again. Cars are weird.")
            self.add_travel_restriction("Wasted Afternoon")
        else:
            type.type("The car is completely dead. You need a tow. " + red("$100") + " minimum.")
            if self.get_balance() >= 100:
                self.change_balance(-100)
            else:
                type.type("You can't afford a tow. You push the car to the shoulder and hope.")
            self.add_travel_restriction("Wasted Afternoon")
            self.add_danger("Mystery Electrical Problem")
            self.lose_sanity(15)
        print()

    def key_wont_turn(self):
        type.type("You put your key in the ignition. It won't turn. At all.")
        print()
        type.type("You wiggle it, jiggle it, curse at it. Nothing.")
        print()
        if self.has_item("WD-40"):
            type.type("You spray " + magenta(bright("WD-40")) + " into the ignition. After some working, it turns.")
            self.use_item("WD-40")
        else:
            type.type("Ignition cylinder is worn. This is going to be an expensive fix.")
            print()
            type.type("After an hour of trying, it finally turns. But this will happen again.")
            self.add_danger("Worn Ignition")
            self.add_travel_restriction("Wasted Afternoon")
        print()

    def car_wont_go_in_reverse(self):
        type.type("You try to back out of a parking spot. The car won't go in reverse.")
        print()
        type.type("Forward? Fine. Reverse? Absolutely not.")
        print()
        type.type("This is going to make parking very interesting.")
        print()
        type.type("Transmission linkage or cable. " + red("$150-300") + " to fix.")
        print()
        type.type("For now, you Austin Powers your way out of the spot.")
        self.add_danger("No Reverse Gear")
        self.add_travel_restriction("Wasted Afternoon")
        print()

    def window_wont_roll_up(self):
        type.type("You roll down your window. It won't roll back up.")
        print()
        type.type("The motor is dead. Your window is stuck down.")
        print()
        if self.has_item("Plastic Wrap") or self.has_item("Garbage Bag"):
            item = "Plastic Wrap" if self.has_item("Plastic Wrap") else "Garbage Bag"
            type.type("You tape " + magenta(bright(item)) + " over the opening as a temporary fix.")
            print()
            type.type("You look homeless. More homeless than usual. But it's sealed.")
            self.use_item(item)
            self.restore_sanity(3)
            self.add_danger("Broken Window")
        else:
            type.type("Rain, bugs, thieves - everything can get in now.")
            print()
            type.type("Window motor replacement: " + red("$150-250") + ". Another thing you can't afford.")
            self.add_danger("Open Window")
            self.lose_sanity(8)
        print()

    def trunk_wont_close(self):
        type.type("Your trunk latch is broken. The trunk won't stay closed.")
        print()
        type.type("It bounces open every time you hit a bump.")
        print()
        if self.has_item("Bungee Cords") or self.has_item("Rope"):
            item = "Bungee Cords" if self.has_item("Bungee Cords") else "Rope"
            type.type("You tie it shut with " + magenta(bright(item)) + ". Ghetto, but it works.")
            self.restore_sanity(3)
            self.add_danger("Broken Trunk Latch")
        else:
            type.type("You drive holding the trunk with one arm out the window.")
            print()
            type.type("This is not sustainable.")
            self.add_travel_restriction("Wasted Afternoon")
            self.add_danger("Open Trunk")
        print()

    def gas_pedal_sticking(self):
        type.type("Your gas pedal is sticking. When you push it, it doesn't always come back up.")
        print()
        type.type("That's absolutely terrifying.")
        print()
        type.type("You're essentially driving a weapon that doesn't always respond to your commands.")
        print()
        if self.has_item("WD-40"):
            type.type("You spray " + magenta(bright("WD-40")) + " on the linkage. It helps. Mostly.")
            self.use_item("WD-40")
            self.add_danger("Sticky Gas Pedal")
        else:
            type.type("You drive with your foot ready to yank the pedal up at any moment.")
            self.add_danger("Sticky Gas Pedal")
            self.lose_sanity(15)
        print()

    def parking_brake_stuck(self):
        type.type("You release the parking brake. Nothing happens. It's stuck on.")
        print()
        type.type("Your wheels barely turn. You can hear the grinding.")
        print()
        type.type("Something is seized in the mechanism.")
        print()
        if self.has_item("Tool Kit"):
            type.type("With your " + magenta(bright("Tool Kit")) + ", you manually release the mechanism.")
            print()
            type.type("The parking brake might not work normally anymore, but you can drive.")
            self.add_danger("Broken Parking Brake")
        else:
            type.type("You can't drive like this. You need a mechanic.")
            self.add_travel_restriction("Wasted Afternoon")
            self.add_danger("Stuck Parking Brake")
            self.lose_sanity(10)
        print()

    # === FOLLOW-UP DANGER EVENTS ===
    def leaking_battery_worsens(self):
        if not self.has_danger("Leaking Battery"):
            return
        type.type("That battery leak you've been ignoring? It got worse.")
        print()
        type.type("Acid has eaten through your battery cables. No power. No start.")
        print()
        type.type("New battery plus cables: " + red("$200") + ".")
        if self.get_balance() >= 200:
            self.change_balance(-200)
            self.remove_danger("Leaking Battery")
            type.type(" Fixed. Finally.")
        else:
            type.type(" You can't afford it. You're stranded again.")
            self.add_travel_restriction("Dead Battery")
        self.add_travel_restriction("Wasted Afternoon")
        print()

    def bald_tires_hydroplane(self):
        if not self.has_danger("Bald Tires"):
            return
        type.type("It's raining. And your bald tires finally betray you.")
        print()
        type.type("Your car hydroplanes, spinning out of control.")
        print()
        chance = random.randrange(5)
        if chance == 0:
            type.type("You crash into a ditch. The car is damaged but driveable.")
            print()
            type.type("You're shaken but alive.")
            self.hurt(20)
            self.add_danger("Crash Damage")
            self.lose_sanity(15)
        elif chance < 3:
            type.type("You somehow regain control. Your heart is pounding.")
            print()
            type.type("That was close. Too close.")
            self.lose_sanity(10)
        else:
            type.type("You slide into another car. Minor collision.")
            print()
            type.type("The other driver is furious. You exchange information.")
            self.hurt(10)
            self.add_danger("Insurance Claim")
            self.add_travel_restriction("Wasted Afternoon")
        print()

    def engine_knock_worsens(self):
        if not self.has_danger("Engine Knock"):
            return
        type.type("That knocking from your engine? It's getting louder. Much louder.")
        print()
        type.type("The engine is dying. Every mile could be its last.")
        print()
        chance = random.randrange(5)
        if chance == 0:
            type.type("BANG. The engine seizes. Smoke pours from under the hood.")
            print()
            type.type("Your car is dead. Completely dead.")
            self.remove_danger("Engine Knock")
            self.add_danger("Seized Engine")
            self.add_travel_restriction("No Engine")
            self.lose_sanity(25)
        else:
            type.type("Still running. Barely. Loudly. Terrifyingly.")
        print()

    def nail_in_tire_blows(self):
        if not self.has_danger("Nail in Tire"):
            return
        type.type("Remember that nail you left in your tire? It finally won.")
        print()
        type.type("The tire is flat. Completely flat. You woke up to it.")
        print()
        self.remove_danger("Nail in Tire")
        if self.has_item("Spare Tire"):
            type.type("Time to use that spare.")
            self.use_item("Spare Tire")
        else:
            type.type("No spare. You're stuck until you can get this fixed.")
            self.add_travel_restriction("Flat Tire")
            self.lose_sanity(10)
        print()

    def failing_fuel_pump_dies(self):
        if not self.has_danger("Failing Fuel Pump"):
            return
        chance = random.randrange(5)
        if chance == 0:
            type.type("Your fuel pump finally gave up the ghost.")
            print()
            type.type("Your car is dead in the middle of nowhere.")
            print()
            type.type("Fuel pump replacement: " + red("$500") + " minimum. Plus towing.")
            self.remove_danger("Failing Fuel Pump")
            self.add_danger("Dead Fuel Pump")
            self.add_travel_restriction("Dead Car")
            self.lose_sanity(20)
        else:
            type.type("Your fuel pump is still whining. Still working. For now.")
        print()

    def broken_ball_joint_breaks(self):
        if not self.has_danger("Broken Ball Joint"):
            return
        chance = random.randrange(10)
        if chance == 0:
            type.type("The ball joint snapped while you were driving.")
            print()
            type.type("Your wheel literally fell off the car.")
            print()
            type.type("You crash. Hard.")
            self.hurt(40)
            self.add_injury("Whiplash")
            self.remove_danger("Broken Ball Joint")
            self.add_danger("Serious Crash Damage")
            self.add_travel_restriction("Totaled Car")
            self.lose_sanity(25)
        else:
            type.type("The ball joint is hanging on by a thread. Every turn is terrifying.")
        print()

    def failing_starter_dies(self):
        if not self.has_danger("Failing Starter Motor"):
            return
        chance = random.randrange(5)
        if chance == 0:
            type.type("Your starter motor has finally died. No more grinding. Just silence.")
            print()
            type.type("Starter replacement: " + red("$300") + ". You're stuck until then.")
            self.remove_danger("Failing Starter Motor")
            self.add_danger("Dead Starter")
            self.add_travel_restriction("Car Won't Start")
            self.lose_sanity(15)
        else:
            type.type("The starter still works. Barely. The grinding is ear-splitting.")
        print()

