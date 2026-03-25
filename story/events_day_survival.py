import random
import time
import sys
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\n"

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

class DaySurvivalMixin:
    """Survival events: car trouble, weather, health, mundane daily life"""

    def seat_cash(self):
        # EVENT: Player finds money hidden in car seat cushions
        # EFFECTS: Gain $5-100 randomly
        # Alt dialogue for repeated event
        variant = random.randrange(4)
        if variant == 0:
            type.type("The heat is suffocating. Sweat drips down your face and soaks into the seat beneath you. ")
            type.type("As the sun shines through the car window, you notice a bright green bill tucked between the seat cushions. Must be your lucky day. ")
        elif variant == 1:
            type.type("Your eyes flutter open to blinding sunlight. As you shield your face, something crinkles beneath your fingers. ")
            type.type("Cash! Wedged right there in the crack of the seat like it was waiting for you. ")
        elif variant == 2:
            type.type("You stretch awake, your back aching from another night in the wagon. While adjusting your seat, your hand brushes against something papery. ")
            type.type("Well, well, well. Looks like past-you stashed some emergency funds and forgot about it. ")
        else:
            type.type("The morning sun hits your face like a slap. Groaning, you shift in your seat-and hear a crinkle. ")
            type.type("Money? In YOUR seat cushions? It's more likely than you think. ")
        print(PAR)
        bill = random.choice([5, 10, 20, 50, 100])
        type.type("That's another " + green(bright("$" + str(bill))) + " dollars.")
        self.change_balance(bill)

        print(PAR)
        return
    def left_window_down(self):
        # EVENT: Window was left open all night, something might have gotten in
        # EFFECTS: 20% chance to add Spider danger, 20% chance to add Cockroach danger
        # Alt dialogue for repeated event
        variant = random.randrange(3)
        if variant == 0:
            type.type("A chill runs down your spine. The air in the car is way too cold. ")
            type.type("Had the window really been open all night? ")
            type.type("Hopefully nothing had gotten in. ")
            type.type("You roll the window up, just to be safe. ")
        elif variant == 1:
            type.type("A cold breeze tickles your face. You crack one eye open-the window's wide open. ")
            type.type("How long has it been like that? You could've frozen to death! Or worse... ")
            type.type("You crank it shut, scanning the car interior nervously. ")
        else:
            type.type("You jolt awake to the sound of crickets. WAY too close. ")
            type.type("The passenger window is down. Great. Just great. ")
            type.type("You slam it shut, but the damage might already be done. ")
        random_chance = random.randrange(5)
        if random_chance == 0:
                self.add_danger("Spider")
        elif random_chance == 1:
                self.add_danger("Cockroach")
        print(PAR)

        print(PAR)
        return
    def sore_throat(self):
        # EVENT: Player wakes up with a sore throat coughing fit
        # CONDITION: Only triggers if player doesn't already have "Sore Throat" status
        # EFFECTS: Cough Drops item cures it, otherwise adds "Sore Throat" status
        if self.has_status("Sore Throat"):
            self.day_event()
            return

        type.type("A violent coughing fit hits you out of nowhere. Your throat is dry, and super sore. ")
        print(PAR)
        if self.has_item("Cough Drops"):
            self.use_item("Cough Drops")
            type.type("Luckily, you have some " + magenta(bright("Cough Drops")) + " on hand, ")
            type.type("and you empty the box into your mouth. Almost like magic, your throat doesn't hurt anymore.")
            print(PAR)
            return
        else:
            self.add_status("Sore Throat")
            self.mark_day("Sore Throat")
            type.type("You cough, and cough, and cough some more, but the burning itch in your throat just won't go away.")
            print(PAR)
            return

    def spider_bite(self):
        # EVENT: A spider that got into the car bites the player
        # CONDITION: Requires "Spider" danger to exist, and no existing "Spider Bite"
        # EFFECTS: Pest Control kills spider; Flask of Anti-Venom neutralizes venom; otherwise lose 1-2 sanity
        # Always adds "Spider Bite" status
        if not self.has_danger("Spider") or self.has_status("Spider Bite"):
            self.day_event()
            return

        type.type("A sharp pain shoots through your arm! ")
        type.type("Swinging your arm to scratch the pain, you watch as a spider jumps to your dashboard. ")
        print(PAR)
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
            type.type("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
            type.type("Hopefully, that's the end of your spider problems.")
            print(PAR)
        elif self.has_item("Flask of Anti-Venom"):
            self.use_item("Flask of Anti-Venom")
            type.type("The bite stings. You reach for the " + cyan(bright("Flask of Anti-Venom")) + " and uncork it.")
            print(PAR)
            type.type("A quick sip. The burning in your arm stops almost instantly. The venom loses its grip.")
            print(PAR)
            type.type("The spider disappears into a vent. But it doesn't matter. Its venom is already beaten.")
            self.heal(5)
            print(PAR)
        elif self.has_item("Improvised Trap"):
            type.type("You set up your " + cyan(bright("Improvised Trap")) + " near the vent. The spider crawls right into it.")
            print(PAR)
            type.type("CLANG! The trap snaps shut. Problem solved.")
            self.restore_sanity(2)
            print(PAR)
        elif self.has_item("Slingshot"):
            type.type("You grab your " + cyan(bright("Slingshot")) + " and take careful aim at the spider on the dashboard.")
            print(PAR)
            type.type("TWANG! The pebble hits true. The spider is smashed flat against the windshield.")
            print(PAR)
            type.type("Ranged pest control. Effective and satisfying.")
            self.restore_sanity(3)
            print(PAR)
        else:
            type.type("You attempt to swat it with your hand, but it sneaks into your heater. ")
            type.type("You start the engine and blast the heat, but you aren't sure if the spider has died, or if it has a family nearby. This sucks.")
            print(PAR)
            self.lose_sanity(random.choice([1, 2]))  # Creature attack drains sanity
        self.add_status("Spider Bite")
        self.mark_day("Spider Bite")
        print(PAR)

        print(PAR)
        return
    def hungry_cockroach(self):
        # EVENT: A cockroach eats some of your money while you sleep
        # CONDITION: Requires "Cockroach" danger, 50% chance to trigger
        # EFFECTS: Pest Control kills it; otherwise loses 10-40% of balance
        random_choice = random.randrange(2)
        if (random_choice != 0) or not self.has_danger("Cockroach"):
            self.day_event()
            return

        type.type("A nasty hiss rises from your pile of money. Something is in there. ")
        type.type("You jump up to check your cash, and you find a cockroach eating away at your cash. ")
        print(PAR)
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the cockroach. ")
            type.type("A cloud of white liquid covers the cockroach, and you watch as it slows down, twitches, and dies. ")
            type.type("Hopefully, that's the end of your cockroach problems.")
            print(PAR)
        else:
            type.type("You attempt to swat it with your hand, but it falls under your car seat. ")
            type.type("You stick your head under the seat, but you aren't sure where the cockroach went, or if it has a family nearby. This is terrible.")
            print(PAR)
        type.type("The cockroach ate through some of your money. ")
        losses = int(self.get_balance() * (random.randint(10, 40)/100))
        type.type("You lost " + green(bright("${:,}".format(losses))) + ".")
        self.change_balance(-losses)

    # One-Time

        print(PAR)
        return
    def morning_stretch(self):
        # EVENT: Player does morning stretches and exercise outside the car
        # EFFECTS: Heal 3, 5, or 8 HP randomly
        # Everytime - simple healing event with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("Your neck has a terrible kink from sleeping at a weird angle. You step out of the car and do some stretches, cracking joints you didn't know you had.")
            print(PAR)
            type.type("After a few minutes of yoga poses you half-remember from a video you watched once, you actually feel... pretty good?")
        elif variant == 1:
            type.type("The morning sun beckons you outside. You do some jumping jacks, touch your toes (or at least try to), and take a few deep breaths of fresh air.")
            print(PAR)
            type.type("Your body thanks you for remembering it exists.")
        elif variant == 2:
            type.type("You tumble out of the car, groaning. Everything hurts. You're not as young as you used to be.")
            print(PAR)
            type.type("But after some careful stretching and a short walk, the aches start to fade. Not bad.")
        else:
            type.type("An old man jogs past your car and waves. Inspired (or shamed), you get out and do some light exercise.")
            print(PAR)
            type.type("The old man laps you twice before you give up, but hey, you tried.")
        print(PAR)
        self.heal(random.choice([3, 5, 8]))
        if self.has_item("Running Shoes") or self.has_item("Pursuit Package"):
            item_name = "Running Shoes" if self.has_item("Running Shoes") else "Pursuit Package"
            print(PAR)
            type.type("The " + cyan(bright(item_name)) + " grip the pavement perfectly. You actually break into a real run. Five good minutes. Your lungs open up. You feel good.")
            self.heal(5)
            self.restore_sanity(3)

        print(PAR)
        return
    def ant_invasion(self):
        # EVENT: Ants invade your car while you sleep
        # EFFECTS: Pest Control kills them; otherwise adds "Ants" danger
        # Everytime - potential danger event
        if self.has_item("Tear Gas"):
            type.type(magenta(bright("Tear Gas")) + " through the window. Wait two minutes. Walk in. The building is yours.")
            print(PAR)
            type.type("The ants scatter. Everything scatters.")
            self.use_item("Tear Gas")
            self.restore_sanity(5)
            print(PAR)
            return
        variant = random.randrange(3)
        if variant == 0:
            type.type("An itching sensation crawls all over your legs. Ants! Dozens of them, crawling up from the floor of your car!")
            print(PAR)
            type.type("You leap out and spend the next hour brushing them off and stomping around like a maniac.")
        elif variant == 1:
            type.type("Something tickles your ear. You reach up and feel... legs. Many legs. You look at your hand-ants.")
            print(PAR)
            type.type("Your screaming probably woke up everyone within a mile radius.")
        else:
            type.type("A line of ants marches across your dashboard with military precision. They seem to be heading for your snack stash.")
            print(PAR)
            type.type("You watch in horror as they disassemble a crumb and carry it away. Impressive, but concerning.")
        print(PAR)
        if self.has_item("Pest Control"):
            type.type("You grab your " + bright(magenta("Pest Control")) + " and wage chemical warfare on the tiny invaders.")
            self.kill_pests()
            type.type("Victory is yours. For now.")
        else:
            type.type("Without pest control, you just have to shake them out and hope they don't come back.")
            self.add_danger("Ants")
        print(PAR)

        print(PAR)
        return
    def bird_droppings(self):
        # EVENT: Birds poop on your windshield
        # EFFECTS: 10% chance to find lottery ticket worth $20-100 in the mess
        # Everytime - comedic event
        variant = random.randrange(3)
        if variant == 0:
            type.type("SPLAT. Something wet and chunky hits your windshield. A pigeon sits on a branch above, looking very satisfied with itself.")
            print(PAR)
            type.type("Great. Just great.")
        elif variant == 1:
            type.type("Your entire windshield is covered in bird droppings. Like, COVERED. Did a whole flock decide your car was the designated bathroom?")
            print(PAR)
            type.type("This is going to take forever to clean.")
        else:
            type.type("A crow lands on your hood and stares at you through the windshield. It tilts its head. Then, maintaining eye contact, it poops.")
            print(PAR)
            type.type("You've been disrespected by a bird. A new low.")
        print(PAR)
        chance = random.randrange(10)
        if chance == 0:
            type.type("Wait... is that a lottery ticket stuck in the mess? Someone must have thrown it out their window.")
            print(PAR)
            type.type("You carefully extract it, wipe it off, and check the numbers... ")
            win = random.randint(20, 100)
            type.type("It's a " + green(bright("$" + str(win))) + " winner! Gross, but lucky!")
            self.change_balance(win)
        print(PAR)

        print(PAR)
        return
    def flat_tire(self):
        # EVENT: Your car has a flat tire
        # EFFECTS: Spare Tire item fixes it; otherwise $50-150 cost and travel restriction
        # Once per day (checks "Flat Tire Today")
        # Everytime - negative event with variants
        if self.has_met("Flat Tire Today"):
            self.day_event()
            return
        self.meet("Flat Tire Today")
        
        variant = random.randrange(3)
        if variant == 0:
            type.type("You step out of your car and immediately notice something wrong. Your front tire is completely flat.")
            print(PAR)
            type.type("Must've run over something sharp. Just your luck.")
        elif variant == 1:
            type.type("The car is listing to one side. Upon inspection: flat tire. Very flat. Like, pancake flat.")
            print(PAR)
            type.type("You kick it in frustration, which doesn't help at all.")
        else:
            type.type("A hissing sound wakes you up. It's not a snake-it's your tire, slowly deflating before your eyes.")
            print(PAR)
            type.type("You watch helplessly as your wheel becomes a sad rubber puddle.")
        print(PAR)
        if self.has_item("Spare Tire"):
            type.type("Good thing you have a " + bright(magenta("Spare Tire")) + "! You spend the next hour changing it out.")
            self.use_item("Spare Tire")
            type.type("Not how you wanted to start the day, but at least you're not stranded.")
        else:
            type.type("Without a spare, you're going to have to walk to get this fixed. That'll cost time and money.")
            self.add_travel_restriction("Flat Tire")
            self.change_balance(-random.randint(50, 150))
        print(PAR)

        print(PAR)
        return
    def mysterious_note(self):
        # EVENT: Find a cryptic threatening note on your car
        # EFFECTS: Atmospheric/creepy - no mechanical effects
        # Everytime - cryptic event
        variant = random.randrange(4)
        if variant == 0:
            type.type("There's a note tucked under your windshield wiper. It reads: " + quote("I know what you did."))
            print(PAR)
            type.type("What did you do? You don't even know. This is unsettling.")
        elif variant == 1:
            type.type("You find a crumpled note on your dashboard. In messy handwriting: " + quote("The dealer always wins. Always."))
            print(PAR)
            type.type("A chill runs down your spine.")
        elif variant == 2:
            type.type("A small piece of paper is stuck to your window. It says: " + quote("You're being watched."))
            print(PAR)
            type.type("You look around nervously. No one's there. At least, no one you can see.")
        else:
            type.type("There's a note on your seat that definitely wasn't there last night. It reads: " + quote("Wake up."))
            print(PAR)
            type.type("You ARE awake. Aren't you?")
        print(PAR)

        print(PAR)
        return
    def radio_static(self):
        # EVENT: Radio plays creepy static, voices, or backwards songs
        # EFFECTS: Atmospheric/creepy - no mechanical effects
        # Everytime - atmospheric event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You turn on the radio for some company, but all you get is static. Then, for just a moment, you hear a voice.")
            print(PAR)
            type.type(quote("...don't go to the casino...") + " it whispers, before dissolving back into white noise.")
            print(PAR)
            type.type("You turn the radio off. Probably just interference. Probably.")
        elif variant == 1:
            type.type("The radio crackles to life on its own. You don't remember turning it on.")
            print(PAR)
            type.type("A song plays-one you almost recognize, but not quite. The lyrics are backwards, or maybe in another language.")
            print(PAR)
            type.type("You yank the power cord. The music keeps playing for three seconds before stopping.")
        else:
            type.type("You fiddle with the radio dial, searching for anything other than static. Finally, a clear station!")
            print(PAR)
            type.type("It's playing your least favorite song. Of course it is.")
            print(PAR)
            type.type("You turn it off in disgust.")
        print(PAR)

    # ==========================================
    # NEW POOR DAY EVENTS - Conditional
    # ==========================================
    
        print(PAR)
        return
    def ant_bite(self):
        # EVENT: The ants that invaded your car are now biting you
        # CONDITION: Requires "Ants" danger to exist
        # EFFECTS: Pest Control = 10 damage; otherwise 20 damage; adds "Ant Bites" status
        # Conditional - requires Ant danger
        if not self.has_danger("Ants"):
            self.day_event()
            return
        
        type.type("You're COVERED in angry red welts. The ants that invaded your car yesterday? They didn't leave. They multiplied.")
        print(PAR)
        type.type("And they're BITING.")
        print(PAR)
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + bright(magenta("Pest Control")) + " and go absolutely nuclear on the tiny terrors.")
            type.type(" Victory at last-but the bites still sting.")
            self.hurt(10)
        else:
            type.type("Without pest control, you can only flee the car and brush them off. They'll probably be back.")
            self.hurt(20)
        self.add_status("Ant Bites")
        self.mark_day("Ant Bites")
        print(PAR)

    # ==========================================
    # NEW POOR DAY EVENTS - One-Time
    # ==========================================
    
        print(PAR)
        return
    def sun_visor_bills(self):
        # EVENT: Find money hidden in your sun visor
        # EFFECTS: Normally gain $3-300
        # RARE (5%): Jackpot variant gives $800-2000
        # Alt dialogue for repeated event + rare variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% RARE VARIANT - The Jackpot Visor
            type.type("You flip down the sun visor to block the morning sun and-")
            print(PAR)
            type.type("HOLY SHIT.")
            print(PAR)
            type.type("Bills cascade down like a waterfall. Twenties, fifties, even some hundreds, all stuffed into the visor like it was a makeshift piggy bank.")
            print(PAR)
            type.type("Did you do this? Did past-you do this and forget? Is this some kind of divine intervention?")
            print(PAR)
            bill = random.randint(800, 2000)
            type.type("After counting it all, you find " + green(bright("${:,}".format(bill))) + " dollars!")
            print(PAR)
            type.type(yellow("You have no idea where this came from, but you're not complaining."))
            print(PAR)
            self.change_balance(bill)
            print(PAR)
            return
        
        # Normal variants
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up in the front seat, dripping in sweat. ")
            print(PAR)
            type.type("As the sun shines through the car window, you notice a few bright green bills above you, peeking out of the sun visor. How long have they been there? ")
            print(PAR)
        elif variant == 1:
            type.type("The sun glares through your windshield, and you reach for the visor. As you flip it down, something flutters into your lap. ")
            print(PAR)
            type.type("Money! You check the visor again-there's more. ")
            print(PAR)
        else:
            type.type("You sit up, rubbing your eyes, and accidentally bump the sun visor. Cash rains down on you. ")
            print(PAR)
            type.type("You forgot you hid emergency funds up there! Past-you was actually smart for once. ")
            print(PAR)
        bill = random.choice([3, 15, 30, 60, 150, 300])
        type.type("That's another " + green(bright("$" + str(bill))) + " dollars.")
        print(PAR)
        self.change_balance(bill)
        if self.has_item("Flask of Fortunate Day"):
            bonus = random.randint(20, 80)
            print(PAR)
            type.type("The " + cyan(bright("Flask of Fortunate Day")) + " hums warm in your pocket. Fate tips its hat.")
            print(PAR)
            type.type("You check one more time and find a few extra bills tucked behind a receipt. Another " + green(bright("$" + str(bonus))) + ".")
            self.change_balance(bonus)
        print(PAR)

        print(PAR)
        return
    def strong_winds(self):
        # EVENT: Severe wind storm keeps you trapped in the car
        # EFFECTS: Adds "Wind" travel restriction normally
        # RARE (3%): Wind blows in $300-800 cash from somewhere
        # Alt dialogue for repeated event + rare variant
        if self.has_item("Fortified Perimeter"):
            type.type("Animals, thieves, weather — the " + magenta(bright("Fortified Perimeter")) + " handles them all.")
            print(PAR)
            type.type("Camp secured. The storm rages outside but nothing gets through.")
            self.restore_sanity(5)
            print(PAR)
            return
        rare_chance = random.randrange(100)
        
        if rare_chance < 3:  # 3% RARE VARIANT - Wind Brings Gifts
            type.type("Howling wind is rattling your wagon. Branches are falling, leaves are flying, and-")
            print(PAR)
            type.type("THUNK.")
            print(PAR)
            type.type("Something lands on your roof. Then another thunk. And another.")
            print(PAR)
            type.type("You cautiously step outside, bracing against the gusts. ")
            type.type("On the ground around your car... money. Bills, blowing in from god-knows-where, plastering themselves against your vehicle.")
            print(PAR)
            type.type("You spend the next hour chasing down wind-blown cash like the world's most chaotic Easter egg hunt.")
            print(PAR)
            windfall = random.randint(300, 800)
            type.type("In the end, you manage to snag " + green(bright("${:,}".format(windfall))) + "!")
            print(PAR)
            self.change_balance(windfall)
            self.add_travel_restriction("Wind")
            print(PAR)
            return
        
        # Normal variants
        variant = random.randrange(3)
        if variant == 0:
            type.type("A loud snap rings out above you, followed by a massive branch crashing down from the treetops and into the street. ")
            type.type("The wind echoes throughout the trees around you, and many of them look to be on the verge of falling.")
            print(PAR)
            type.type("With the weather being this bad, you make the executive decision to just chill in the wagon for the day.")
            print(PAR)
        elif variant == 1:
            type.type("Your car rocks violently, waking you from a deep sleep. Outside, it's chaos-trees bending, debris flying, the sky an angry gray.")
            print(PAR)
            type.type("Yeah, no. You're not going out in that. Time to hunker down.")
            print(PAR)
        else:
            type.type("The sound is deafening-wind screaming past your windows, your wagon shaking like it might flip over.")
            print(PAR)
            type.type("A trash can tumbles past your windshield, followed by what looks like someone's lawn chair. ")
            print(PAR)
            type.type("Today is officially an 'inside day.'")
            print(PAR)
        self.add_travel_restriction("Wind")
        print(PAR)

    # Conditional

        print(PAR)
        return
    def got_a_cold(self):
        # EVENT: You wake up with a cold
        # CONDITION: Only triggers if you don't already have "Cold" status
        # EFFECTS: Adds "Cold" status; Cough Drops prevent it
        if self.has_status("Cold"):
            self.day_event()
            return
        if self.has_item("Hydration Station"):
            type.type("The " + cyan(bright("Hydration Station")) + " flushes the virus before it sets. Clean water, constant stream.")
            print(PAR)
            type.type("No cold. Just a brief, concerned sneeze.")
            self.heal(5)
            return
        if self.has_item("Voice Soother"):
            self.use_item("Voice Soother")
            type.type("The " + cyan(bright("Voice Soother")) + " coats the throat in relief. The cold doesn't stand a chance.")
            print(PAR)
            self.heal(10)
            return
        if self.has_item("Home Remedy"):
            self.use_item("Home Remedy")
            type.type("The " + cyan(bright("Home Remedy")) + " fights the cold with old chemistry.")
            print(PAR)
            self.heal(8)
            return
        variant = random.randrange(3)
        if variant == 0:
            type.type("A sneeze rips through you in your car seat, followed by your nose running, droplets falling down from your chin and onto your shirt. Damn, must be a cold.")
        elif variant == 1:
            type.type("You wake up and your throat feels like sandpaper wrapped in barbed wire. Your nose is a faucet. Your head is a bowling ball.")
            print(PAR)
            type.type("Cold. The boring, inevitable kind. The kind that reminds you that living in a car has consequences.")
        else:
            type.type("The first sneeze catches you off guard. The second one rattles your teeth. By the fifth, you've accepted your fate.")
            print(PAR)
            type.type("You're sick. Nose running, eyes watering, the whole miserable package.")
        print(PAR)
        if self.has_item("Cough Drops"):
            type.type("You pop a " + magenta(bright("Cough Drop")) + " and let it dissolve. Menthol floods your sinuses like a chemical sunrise.")
            print(PAR)
            type.type("It's not a cure, but it takes the edge off. You might dodge the worst of this.")
            print(PAR)
            if random.randrange(2) == 0:
                type.type("The cough drop does its job. By afternoon, you feel almost human. Crisis averted.")
                print(PAR)
                return
            else:
                type.type("But the cold is stubborn. It settles in despite your best efforts. At least it's not as bad as it could be.")
        self.add_status("Cold")
        self.mark_day("Cold")
        print(PAR)

    # ==========================================
    # NEW CHEAP DAY EVENTS - Everytime
    # ==========================================
    
        print(PAR)
        return
    def morning_fog(self):
        # EVENT: Dense fog blankets the area
        # EFFECTS: Usually atmospheric; one variant deals 5 damage (walk into mirror)
        # Everytime - atmospheric with variants
        if self.has_item("Rusty Compass") or self.has_item("Golden Compass"):
            compass = "Golden Compass" if self.has_item("Golden Compass") else "Rusty Compass"
            type.type("The " + cyan(bright(compass)) + " hums warmly in your pocket. You were never truly lost.")
            print(PAR)
            type.type("It guides you through the trees to a shortcut you wouldn't have found alone.")
            self.restore_sanity(5)
            if compass == "Rusty Compass":
                evolved = self.track_item_use("Rusty Compass")
                if evolved:
                    print(PAR)
                    type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
            print(PAR)
            return
        variant = random.randrange(4)
        if variant == 0:
            type.type("Fog so thick you can barely see your hood has swallowed the world in white.")
            print(PAR)
            type.type("You wait an hour for it to clear. Two hours. Finally, around noon, you can see the road again.")
            print(PAR)
        elif variant == 1:
            type.type("The fog this morning is eerie. Shapes seem to move in it-people? Animals? You can't tell.")
            print(PAR)
            if self.has_item("Binocular Scope"):
                type.type("You pull out your " + cyan(bright("Binocular Scope")) + " and peer through the fog.")
                print(PAR)
                type.type("The shapes resolve: just trees swaying in the wind. No ghosts today.")
                self.restore_sanity(3)
                print(PAR)
            type.type("By the time the fog lifts, you're convinced you saw at least three ghosts. Or maybe just trees. Hopefully trees.")
            print(PAR)
        elif variant == 2:
            type.type("A heavy mist blankets everything. You step outside and immediately lose sight of your car.")
            print(PAR)
            type.type("After ten minutes of wandering in circles, you find it again. That was embarrassing.")
            print(PAR)
        else:
            type.type("The fog is so dense this morning that you walk face-first into your own side mirror.")
            print(PAR)
            type.type("Ow.")
            print(PAR)
            self.hurt(5)
        print(PAR)

        print(PAR)
        return
    def car_wont_start(self):
        # EVENT: Car engine won't start (dead battery or mechanical issues)
        # EFFECTS: 33% chance it starts anyway; otherwise adds travel restriction
        # Everytime - potential restriction event
        if self.has_item("SOS Kit"):
            type.type(magenta(bright("SOS Kit")) + " deployed. Mirror flashes catch the sun, smoke marks your position. Rescue in under an hour.")
            print(PAR)
            type.type("Guaranteed rescue. You're back on the road.")
            self.use_item("SOS Kit")
            self.restore_sanity(5)
            print(PAR)
            return
        variant = random.randrange(3)
        if variant == 0:
            type.type("You turn the key and... nothing. Click click click. The engine won't catch.")
            print(PAR)
            type.type("Dead battery. Great.")
            print(PAR)
        elif variant == 1:
            type.type("The engine makes a sound like a dying whale when you try to start it. Then silence.")
            print(PAR)
            type.type("Something's definitely wrong under the hood.")
            print(PAR)
        else:
            type.type("Your car starts, sputters, coughs, and dies. It sounds like it's given up on life. You relate.")
            print(PAR)
        
        if random.randrange(3) == 0:
            type.type("After some jiggling and praying, it starts back up! Crisis averted.")
            print(PAR)
        else:
            type.type("Looks like you're not driving anywhere until this gets fixed.")
            print(PAR)
            self.add_travel_restriction("Car Trouble")
            if self.has_met("Tom"):
                type.type("Maybe Tom can help with this...")
                print(PAR)
        print(PAR)

        print(PAR)
        return
    def beautiful_sunrise(self):
        # EVENT: You wake up to a beautiful sunrise
        # EFFECTS: Heal 5-15 HP, restore 1-3 sanity
        # Purely positive event with no downsides
        # Everytime - purely positive event
        variant = random.randrange(3)
        if variant == 0:
            type.type("The sunrise catches your eye through the windshield. Pink and gold paint the sky, and for a moment, everything feels... okay.")
            print(PAR)
            type.type("Sometimes you have to appreciate the little things.")
            print(PAR)
        elif variant == 1:
            type.type("The dawn light streams through your windshield, warm and golden. Birds are singing. The air smells fresh.")
            print(PAR)
            type.type("Today might actually be a good day.")
            print(PAR)
        else:
            type.type("You watch the sun come up over the hills, painting everything in shades of orange and red.")
            print(PAR)
            type.type("It's beautiful enough to make you forget, just for a moment, that you live in a car.")
            print(PAR)
        if self.has_item("Flask of Fortunate Day"):
            print(PAR)
            type.type("The " + cyan(bright("Flask of Fortunate Day")) + " pulses with golden light. The sun feels warmer. The road feels shorter. Everything feels... manageable.")
            self.restore_sanity(2)
        self.heal(random.choice([5, 10, 15]))
        self.restore_sanity(random.choice([1, 2, 3]))  # Restores sanity
        print(PAR)

    # ==========================================
    # ITEM-USING EVENTS - Items get consumed
    # ==========================================
    
        print(PAR)
        return
    def mosquito_swarm(self):
        # EVENT: Mosquitoes swarm your car and bite you
        # EFFECTS: Smoke Flare prevents damage (consumed); Bug Spray prevents damage (consumed); otherwise 10-20 damage
        # Smoke Flare and Bug Spray can save you from damage
        type.type("The buzzing fills your car. First one mosquito, then ten, then what feels like a thousand.")
        print(PAR)
        type.type("They swarm your car, slipping through every crack and crevice.")
        print(PAR)
        
        if self.has_item("Smoke Flare"):
            type.type("You pull out the " + magenta(bright("Smoke Flare")) + " and light it.")
            print(PAR)
            type.type("Thick white smoke billows through the car. The mosquitoes panic and flee.")
            print(PAR)
            type.type("Smoke clears. Buzzing gone. You're bite-free and victorious.")
            self.use_item("Smoke Flare")
            self.restore_sanity(3)
            print(PAR)
            return
        elif self.has_item("Bug Spray"):
            type.type("But wait - you have " + magenta(bright("Bug Spray")) + "!")
            print(PAR)
            type.type("You grab the can and spray yourself down liberally. The mosquitoes keep their distance, buzzing angrily but unable to bite.")
            print(PAR)
            type.type("The spray is used up, but you're bite-free.")
            self.use_item("Bug Spray")
            print(PAR)
        else:
            type.type("You spend the night swatting and scratching. By morning, you're covered in itchy welts.")
            print(PAR)
            self.hurt(random.randint(10, 20))
            type.type("Bug spray would have been really helpful right about now.")
        print(PAR)

        print(PAR)
        return
    def scorching_sun(self):
        # EVENT: Extremely hot sun causes heat damage
        # EFFECTS: Cheap Sunscreen prevents damage (consumed); Umbrella reduces to 5;
        #          otherwise 15-25 damage from sunburn
        # Cheap Sunscreen / Sunglasses can help
        type.type("It's hot. Really hot. The sun beats down mercilessly, and your car becomes an oven.")
        print(PAR)

        # ── T3 AUTO ──
        if self.has_item("Health Manipulator"):
            type.type("Your " + cyan(bright("Health Manipulator")) + " starts running thermal compensation before you overheat.")
            print(PAR)
            type.type("Pulse down. Breathing paced. Core temperature stabilized just enough to stay sharp.")
            self.hurt(2)
            self.restore_sanity(3)
            self.update_health_indicator_durability()
            print(PAR)
            return

        if self.has_item("All-Weather Armor") or self.has_item("Hazmat Suit"):
            item_name = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Hazmat Suit"
            type.type("The " + cyan(bright(item_name)) + " handles the heat without breaking a sweat. You barely notice the sun.")
            print(PAR)
            self.restore_sanity(3)
            print(PAR)
            return

        # ── T2 AUTO (diagnostic) ──
        if self.has_item("Health Indicator"):
            type.type("Your " + cyan(bright("Health Indicator")) + " goes red early. You move before heat stroke can set the terms.")
            print(PAR)
            self.hurt(5)
            self.restore_sanity(1)
            self.update_health_indicator_durability()
            print(PAR)
            return

        # ── PLAYER CHOICE: multiple T2 heat-protection items ──
        _t2_options = [
            ("Cool Down Kit", "Stay perfectly cool (consumed)"),
            ("Beach Bum Disguise", "Embrace the heat in style"),
            ("Outdoor Shield", "Block the sun's worst"),
        ]
        _available = [(n, d) for n, d in _t2_options if self.has_item(n)]
        if len(_available) >= 2:
            _chosen = self._offer_item_choice(_available)
            if _chosen == "Cool Down Kit":
                self.use_item("Cool Down Kit")
                type.type("The " + cyan(bright("Cool Down Kit")) + " keeps you perfectly cool. The heat is someone else's problem today.")
                print(PAR)
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Beach Bum Disguise":
                type.type("In the " + cyan(bright("Beach Bum Disguise")) + ", you're perfectly comfortable — the sunscreen is doing god's work.")
                print(PAR)
                type.type("Too comfortable. You fall asleep on a park bench. When you wake up, someone has left a donation cup in front of you. It has $23 in it.")
                print(PAR)
                type.type("A passing dog has also fallen asleep on your lap.")
                self.change_balance(23)
                self.restore_sanity(5)
                print(PAR)
                return
            elif _chosen == "Outdoor Shield":
                type.type("The " + cyan(bright("Outdoor Shield")) + "'s sun protection does its job. You're warm but undamaged.")
                print(PAR)
                self.heal(3)
                print(PAR)
                return

        # Single T2/T1/base — sequential fallback
        if self.has_item("Cool Down Kit"):
            self.use_item("Cool Down Kit")
            type.type("The " + cyan(bright("Cool Down Kit")) + " keeps you perfectly cool. The heat is someone else's problem today.")
            print(PAR)
            self.restore_sanity(5)
        elif self.has_item("Beach Bum Disguise"):
            type.type("In the " + cyan(bright("Beach Bum Disguise")) + ", you're perfectly comfortable — the sunscreen is doing god's work.")
            print(PAR)
            type.type("Too comfortable. You fall asleep on a park bench. When you wake up, someone has left a donation cup in front of you. It has $23 in it.")
            print(PAR)
            type.type("A passing dog has also fallen asleep on your lap.")
            self.change_balance(23)
            self.restore_sanity(5)
        elif self.has_item("Outdoor Shield"):
            type.type("The " + cyan(bright("Outdoor Shield")) + "'s sun protection does its job. You're warm but undamaged.")
            print(PAR)
            self.heal(3)
        elif self.has_item("Premium Sunscreen"):
            type.type("The " + cyan(bright("Premium Sunscreen")) + " blocks the worst of it.")
            print(PAR)
            self.hurt(3)
        elif self.has_item("Cheap Sunscreen"):
            type.type("Good thing you have " + magenta(bright("Cheap Sunscreen")) + "!")
            print(PAR)
            type.type("You slather it on and step outside. It's still hot, but at least you won't turn into a lobster.")
            print(PAR)
            type.type("The tiny bottle is empty now, but worth it.")
            self.use_item("Cheap Sunscreen")
        elif self.has_item("Umbrella"):
            type.type("You grab your " + magenta(bright("Umbrella")) + " and use it as a sun shade.")
            print(PAR)
            type.type("It provides some relief from the blazing sun.")
            self.hurt(5)
        else:
            type.type("You try to stay in the shade, but there's no escaping this heat.")
            print(PAR)
            type.type("By the end of the day, your skin is red and painful.")
            self.hurt(random.randint(15, 25))
            type.type("Sunscreen would have prevented this.")
        print(PAR)

        print(PAR)
        return
    def sudden_downpour(self):
        # EVENT: Sudden heavy rainstorm catches you outside
        # EFFECTS: Umbrella or Plastic Poncho prevents damage/cold;
        #          otherwise 10 damage and adds "Cold" status
        # Umbrella or Plastic Poncho prevents damage/getting sick
        
        # ITEM: Binoculars - spotted the storm coming early
        if self.has_item("Binoculars"):
            type.type("Through the " + cyan(bright("Binoculars")) + ", you saw the weather front building twenty minutes ago.")
            print(PAR)
            type.type("You're already parked under a bridge. Dry. Comfortable. A little smug.")
            print(PAR)
            type.type("The rain hammers the road twenty feet away. Doesn't touch you.")
            self.restore_sanity(3)
            print(PAR)
            return

        if self.has_item("All-Weather Armor"):
            type.type("The " + cyan(bright("All-Weather Armor")) + " laughs at rain. You step out, completely dry, into a biblical downpour.")
            print(PAR)
            self.restore_sanity(5)
            return
        if self.has_item("Storm Suit"):
            type.type("The " + cyan(bright("Storm Suit")) + " was built for exactly this. You walk through the deluge untouched.")
            print(PAR)
            self.restore_sanity(3)
            return
        type.type("The sky opens up without warning. Rain hammers down so hard you can barely hear yourself think.")
        print(PAR)
        
        if self.has_item("Umbrella"):
            type.type("You grab your " + magenta(bright("Umbrella")) + " and step out, staying relatively dry.")
            print(PAR)
            type.type("The storm passes after an hour, and you're no worse for wear.")
        elif self.has_item("Plastic Poncho"):
            type.type("You pull out your " + magenta(bright("Plastic Poncho")) + " and throw it on!")
            print(PAR)
            type.type("It crinkles loudly with every movement, but it keeps you dry.")
            print(PAR)
            type.type("By the time the rain stops, the cheap poncho has torn in three places. Time to toss it.")
            self.use_item("Plastic Poncho")
        else:
            type.type("You get soaked to the bone. The chill seeps into you.")
            print(PAR)
            self.hurt(10)
            if random.randrange(3) == 0:
                type.type("You feel a cold coming on...")
                self.add_status("Cold")
                self.mark_day("Cold")
        if self.has_item("Water Purifier"):
            print(PAR)
            type.type("At least the downpour let you fill up with your " + cyan(bright("Water Purifier")) + ". Clean drinking water — a silver lining to a miserable day.")
            self.restore_sanity(2)
            self.heal(3)
        print(PAR)

        print(PAR)
        return
    def freezing_night(self):
        # EVENT: Freezing cold night threatens to give you hypothermia
        # EFFECTS: Hand Warmers prevent damage (consumed); fire source = 5 damage;
        #          otherwise 15-25 damage and 25% chance of "Cold" status
        # Hand Warmers can help survive
        type.type("The temperature plummets. Frost forms on your windshield, and you can see your breath inside the car.")
        print(PAR)

        # Survival Bivouac checked first (T3, full protection, no items consumed).
        # Sacred Flame combo (Phoenix Feather + Fire Starter Kit) is checked next: it consumes Fire Starter Kit, so it must precede
        # the Emergency Blanket + Fire Starter Kit combo below.
        if self.has_item("Survival Bivouac"):
            type.type("The " + cyan(bright("Survival Bivouac")) + " turns your car into a warm cocoon. You sleep through the cold front without a shiver.")
            print(PAR)
            self.restore_sanity(5)
            return

        if self.has_item("Worn Gloves") or self.has_item("Velvet Gloves"):
            gloves = "Velvet Gloves" if self.has_item("Velvet Gloves") else "Worn Gloves"
            type.type("The enchanted " + cyan(bright(gloves)) + " keep your fingers nimble in the cold.")
            print(PAR)
            if gloves == "Velvet Gloves":
                type.type("Velvet-lined control turns your hands into tiny furnaces. You tie knots, seal drafts, and keep your pulse steady while the temperature crashes.")
                self.restore_sanity(5)
                self.heal(4)
            else:
                type.type("Where others fumble, you work with precision. The cold can't reach your hands.")
                self.restore_sanity(3)
                self.heal(2)
            self.update_worn_gloves_durability()
            print(PAR)
            return

        if self.has_item("Flask of No Bust"):
            self.use_item("Flask of No Bust")
            type.type("You swallow the " + cyan(bright("Flask of No Bust")) + " as the cold starts chewing through your focus.")
            print(PAR)
            type.type("The freeze still hurts, but your body refuses to collapse. You make it to dawn by force of chemistry and stubbornness.")
            self.hurt(6)
            self.restore_sanity(2)
            print(PAR)
            return
        if self.has_item("Phoenix Feather") and self.has_item("Fire Starter Kit"):
            self.use_item("Phoenix Feather")
            self.use_item("Fire Starter Kit")
            type.type("The " + cyan(bright("Fire Starter Kit")) + " sparks.")
            print(PAR)
            type.type("The " + cyan(bright("Phoenix Feather")) + " ignites.")
            print(PAR)
            type.type("Sacred amber fire fills the air around you. Not cold fire. Not cruel fire. The other kind.")
            print(PAR)
            type.type("Every wound seals. Every pain ceases. The frostbite, the bruises, the exhaustion — gone.")
            print(PAR)
            type.type("Both items are ash. But you are whole.")
            self.heal(100)
            self.restore_sanity(50)
            print(PAR)
            return

        if self.has_item("Emergency Blanket") and self.has_item("Fire Starter Kit"):
            type.type("You wrap yourself in the " + cyan(bright("Emergency Blanket")) + " and get the " + cyan(bright("Fire Starter Kit")) + " going outside.")
            print(PAR)
            type.type("The reflective foil bounces the fire's heat right back at you. You're in a warm cocoon. Fortress mode.")
            print(PAR)
            type.type("The cold never had a chance. You sleep well. Genuinely, impressively well.")
            self.heal(10)
            self.restore_sanity(5)
            print(PAR)
            return
        if self.has_item("Hand Warmers"):
            type.type("You crack open your " + magenta(bright("Hand Warmers")) + " and hold them close.")
            print(PAR)
            type.type("The chemical heat spreads through your fingers, your hands, your whole body. Warmth.")
            print(PAR)
            type.type("You survive the night comfortably. The warmers are spent by morning.")
            self.use_item("Hand Warmers")
        elif self.has_fire_source():
            type.type("You manage to generate some warmth with what you have. It's not comfortable, but you survive.")
            self.hurt(5)
        elif self.has_item("Blanket"):
            type.type("You wrap yourself in the " + magenta(bright("Blanket")) + " and pull it tight.")
            print(PAR)
            type.type("Not perfect. But enough. You make it through.")
            self.hurt(8)
        else:
            type.type("You shiver through the entire night, curled up in a ball, teeth chattering.")
            print(PAR)
            self.hurt(random.randint(15, 25))
            if random.randrange(4) == 0:
                type.type("You feel a cold coming on...")
                self.add_status("Cold")
                self.mark_day("Cold")
        print(PAR)

        print(PAR)
        return
    def car_smell(self):
        # EVENT: Your car smells terrible
        # EFFECTS: Air Freshener restores 3 sanity (consumed); otherwise lose 2-4 sanity
        # Air Freshener removes bad smell status
        type.type("Something in your car STINKS. You can't tell if it's the old food, the musty seats, or just... you.")
        print(PAR)
        
        if self.has_item("Air Freshener"):
            type.type("You hang up your " + magenta(bright("Air Freshener")) + " and take a deep breath.")
            print(PAR)
            type.type("Ahhh. Pine fresh. Much better.")
            print(PAR)
            type.type("The freshener will fade over time, but for now, it's a major improvement.")
            self.use_item("Air Freshener")
            self.restore_sanity(3)
        else:
            type.type("You try to air it out by opening the windows, but the smell lingers.")
            print(PAR)
            type.type("Living in this stench is demoralizing.")
            self.lose_sanity(random.randint(2, 4))
            if self.has_item("Smelling Salts"):
                type.type("The stench is overwhelming. You crack the " + cyan(bright("Smelling Salts")) + " under your nose.")
                print(PAR)
                type.type("The sharp ammonia jolt cuts through the fog. Your head clears, at least for now.")
                self.restore_sanity(3)
                print(PAR)
        print(PAR)

        print(PAR)
        return
    def roadside_breakdown(self):
        # EVENT: Car breaks down on the side of the road
        # EFFECTS: Road Flares get help quickly (consumed); Flashlight helps a bit;
        #          otherwise $100-200 tow cost and travel restriction
        # Road Flares help get assistance
        type.type("Your car makes a horrible grinding noise and coasts to a stop on the side of the road. This is bad.")
        print(PAR)
        
        if self.has_item("Road Flares"):
            type.type("You grab your " + magenta(bright("Road Flares")) + " and set them up behind your car.")
            print(PAR)
            type.type("The bright red flames are visible for miles. Within an hour, a passing truck stops to help.")
            print(PAR)
            type.type(quote("Saw your flares from way back. Smart thinking! Let me take a look..."))
            print(PAR)
            type.type("The trucker helps you get the car started again. The flares are spent, but crisis averted.")
            self.use_item("Road Flares")
        elif self.has_item("Smoke Signal Kit"):
            type.type("You assemble your " + cyan(bright("Smoke Signal Kit")) + " and light the special mixture.")
            print(PAR)
            type.type("Thick, colored smoke billows up, visible for miles against the clear sky.")
            print(PAR)
            type.type("A highway patrol car spots it and pulls over. " + quote("That's one hell of a signal, friend. What's the trouble?"))
            print(PAR)
            type.type("They help you get the car running again. The kit is spent, but you're back on the road.")
            self.use_item("Smoke Signal Kit")
        elif self.has_item("Flashlight") or self.has_item("Lantern") or self.has_item("Eternal Light"):
            if self.has_item("Eternal Light"):
                light_name = "Eternal Light"
            elif self.has_item("Lantern"):
                light_name = "Lantern"
            else:
                light_name = "Flashlight"
            type.type("You wave your " + magenta(bright(light_name)) + " at passing cars. After an hour, someone finally stops.")
            print(PAR)
            type.type("They help jumpstart your car. It could have been worse.")
            self.add_travel_restriction("Car Trouble")
            evolved = self.track_item_use(light_name)
            if evolved:
                print(PAR)
                type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
        else:
            type.type("You sit there for hours, trying to flag down help. Most cars just speed past.")
            print(PAR)
            type.type("Finally, by nightfall, a tow truck comes. But it costs you.")
            tow_cost = random.randint(100, 200)
            type.type("You pay " + green(bright("${:,}".format(tow_cost))) + " for the tow.")
            self.change_balance(-tow_cost)
            self.add_travel_restriction("Car Trouble")
        print(PAR)

        print(PAR)
        return
    def broken_belonging(self):
        # EVENT: One of your belongings breaks
        # EFFECTS: Super Glue or Duct Tape fixes it (consumed); otherwise lose 2 sanity
        # Super Glue or Duct Tape can fix things
        type.type("You hear a crack. One of your belongings has broken - a part snapped clean off.")
        print(PAR)
        
        if self.has_item("Super Glue"):
            type.type("But you have " + magenta(bright("Super Glue")) + "!")
            print(PAR)
            type.type("A few drops, some careful pressing, and... good as new. Almost.")
            print(PAR)
            type.type("The glue tube is empty now, but at least you saved your stuff.")
            self.use_item("Super Glue")
        elif self.has_item("Duct Tape"):
            type.type("Nothing a little " + magenta(bright("Duct Tape")) + " can't fix!")
            print(PAR)
            type.type("It's not pretty, but it holds. Duct tape: the universal solution.")
            print(PAR)
            type.type("You used the last of the roll, but hey, it worked.")
            self.use_item("Duct Tape")
        else:
            type.type("Without anything to fix it, you just have to accept the loss.")
            print(PAR)
            type.type("Sometimes things just break and stay broken.")
            self.lose_sanity(2)
        print(PAR)

        print(PAR)
        return
    def important_document(self):
        # EVENT: Find a form that needs signing and could be worth money
        # EFFECTS: Fancy Pen = $100-300 reward (consumed); otherwise form is rejected
        # Fancy Pen makes a difference
        type.type("You find a form wedged under your car seat. Something important - could be worth money.")
        print(PAR)
        type.type("But you need to sign it to make it official.")
        print(PAR)
        
        if self.has_item("Fancy Pen"):
            type.type("You pull out your " + magenta(bright("Fancy Pen")) + " and sign with a flourish.")
            print(PAR)
            type.type("The signature looks professional. Important. Legitimate.")
            print(PAR)
            reward = random.randint(100, 300)
            type.type("The form turns out to be valid, and you receive " + green(bright("${:,}".format(reward))) + "!")
            self.change_balance(reward)
            # Pen doesn't get consumed - it's reusable
        else:
            type.type("You scrounge around for something to write with. An old crayon? A stubby pencil?")
            print(PAR)
            type.type("Your signature looks like a child wrote it. The form is rejected.")
            print(PAR)
            type.type("Opportunity lost.")
        print(PAR)

        print(PAR)
        return
    def need_fire(self):
        # EVENT: Desperately need fire for warmth/cooking/light
        # EFFECTS: Monogrammed Lighter works (not consumed); Lighter works 80% (may run out);
        #          Road Flares work (consumed); otherwise 10 damage + 3 sanity loss
        # Lighter or Monogrammed Lighter or Road Flares starts fire
        type.type("You're shivering in your car. You need fire. Desperately. Maybe to warm up, maybe to cook, maybe just to see.")
        print(PAR)

        # COMBO: Fire Launcher + Animal Bait = The BBQ Trap
        if self.has_item("Fire Launcher") and self.has_item("Animal Bait"):
            self.use_item("Animal Bait")
            type.type("Set the " + cyan(bright("Animal Bait")) + ". Wait. Light the " + cyan(bright("Fire Launcher")) + ".")
            print(PAR)
            type.type("What follows is technically hunting, technically cooking, and technically a war crime against the local squirrel population.")
            print(PAR)
            type.type("But you eat like a king tonight.")
            self.heal(50)
            self.restore_sanity(5)
            self.add_danger("PETA List")
            print(PAR)
            return

        if self.has_item("Nomad's Camp"):
            type.type("The " + cyan(bright("Nomad's Camp")) + " provides. You will never go hungry. Not anymore.")
            print(PAR)
            self.heal(30)
            self.restore_sanity(10)
            return
        if self.has_item("Provider's Kit"):
            type.type("The " + cyan(bright("Provider's Kit")) + " has you covered. Trap on land, rod in water.")
            print(PAR)
            type.type("You eat like a king in the apocalypse.")
            self.heal(25)
            self.restore_sanity(8)
            return

        if self.has_item("Monogrammed Lighter"):
            type.type("You pull out your " + magenta(bright("Monogrammed Lighter")) + " and flick it open.")
            print(PAR)
            type.type("Flame. Reliable, elegant flame. You get what you need done.")
            # Premium lighter doesn't run out
        elif self.has_item("Lighter"):
            type.type("You pull out your " + magenta(bright("Lighter")) + " and click it.")
            print(PAR)
            if random.randrange(5) == 0:
                type.type("Click. Click. Click... it's out of fluid.")
                print(PAR)
                type.type("Useless now.")
                self.use_item("Lighter")
            else:
                type.type("Flame. You get what you need done.")
        elif self.has_item("Road Flares"):
            type.type("You light one of your " + magenta(bright("Road Flares")) + ". It's overkill, but it works.")
            print(PAR)
            type.type("The flare burns itself out. Not the most efficient use.")
            self.use_item("Road Flares")
        else:
            type.type("You have no way to make fire. You sit in the cold and dark.")
            self.hurt(10)
            self.lose_sanity(3)
            print(PAR)
            return
        
        # If you got fire and have Fishing Rod, you can catch and cook fish
        if self.has_item("Fishing Rod"):
            type.type("With fire going, you grab your " + cyan(bright("Fishing Rod")) + " and head to the nearest water source.")
            print(PAR)
            type.type("A few casts later, you land a decent-sized fish. You cook it over the flames.")
            print(PAR)
            type.type("Hot, fresh fish. Not bad for a desperate situation.")
            self.heal(20)
            self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def penny_luck(self):
        # EVENT: Find another lucky penny while carrying one
        # CONDITION: Requires Lucky Penny item
        # EFFECTS: Adds "Lucky" status
        # Lucky Penny effect
        if not self.has_item("Lucky Penny"):
            self.day_event()
            return
        
        type.type("Stepping out of your car, you're about to step on a crack in the sidewalk when something makes you pause.")
        print(PAR)
        type.type("You look down. Another penny, heads up, right next to the crack.")
        print(PAR)
        type.type("You pick it up. Now you have two lucky pennies... but you can only carry one.")
        print(PAR)
        type.type("You flip your old " + magenta(bright("Lucky Penny")) + " into a fountain as an offering to whatever luck gods exist.")
        evolved = self.track_item_use("Lucky Penny")
        if evolved:
            print(PAR)
            type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
        print(PAR)
        type.type("The new penny feels luckier. Is that possible?")
        if self.has_item("Flask of Bonus Fortune"):
            type.type("The " + cyan(bright("Flask of Bonus Fortune")) + " warms in your pocket. The coin catches the light like a tiny jackpot.")
            print(PAR)
            self.change_balance(random.randint(30, 90))
            self.restore_sanity(2)
        if self.has_item("Flask of Imminent Blackjack"):
            type.type("Your " + cyan(bright("Flask of Imminent Blackjack")) + " gives you that same pre-deal certainty. Today is a good-odds day.")
            print(PAR)
            self.add_status("Lucky")
            self.restore_sanity(2)
        self.add_status("Lucky")
        self.change_balance(random.randint(5, 20))
        self.restore_sanity(3)
        print(PAR)

        print(PAR)
        return
    def rubber_band_save(self):
        # EVENT: Rubber bands save the day by holding things together
        # CONDITION: Requires Rubber Bands item
        # EFFECTS: 20% chance item is consumed
        # Rubber Bands have a use
        if not self.has_item("Rubber Bands"):
            self.day_event()
            return
        
        type.type("Something in your car is about to fall apart. A stack of papers. A bundle of bills. A bag that won't stay closed.")
        print(PAR)
        type.type("You grab some " + magenta(bright("Rubber Bands")) + " from your stash.")
        print(PAR)
        type.type("Snap. Snap. Snap. Everything's secured.")
        print(PAR)
        type.type("Sometimes the simplest solutions are the best.")
        if random.randrange(5) == 0:
            type.type(" That was the last of them.")
            self.use_item("Rubber Bands")
        print(PAR)

    # ==========================================
    # NEW CHEAP DAY EVENTS - Conditional
    # ==========================================
    
        print(PAR)
        return
    def cold_gets_worse(self):
        # EVENT: Your cold progresses into the flu
        # CONDITION: Requires "Cold" status, not already having "Flu"
        # EFFECTS: Removes "Cold", adds "Flu" status, deals 15 damage
        # Conditional - requires Cold status
        if not self.has_status("Cold"):
            self.day_event()
            return
        
        if self.has_status("Flu"):
            self.day_event()
            return
        
        type.type("You're curled up in your car seat. Your cold has gotten worse. Much worse. You're shivering, sweating, and your whole body aches.")
        print(PAR)
        type.type("This isn't just a cold anymore. This is the flu.")
        print(PAR)
        self.lose_status("Cold")
        self.add_status("Flu")
        self.mark_day("Flu")
        self.hurt(15)

    # ==========================================
    # NEW CHEAP DAY EVENTS - One-Time
    # ==========================================
    
        print(PAR)
        return
    def deja_vu(self):
        # SECRET EVENT: Weekly deja vu on multiples of day 7
        # TRIGGER: Day count is multiple of 7
        # EFFECTS: Adds "Lucky" status
        # SECRET - Only triggers if player's day count is a multiple of 7 (weekly)
        if self.get_day() % 7 != 0 or self.get_day() == 0:
            self.day_event()
            return
        
        if self.has_met("Deja Vu " + str(self.get_day())):
            self.day_event()
            return
        
        self.meet("Deja Vu " + str(self.get_day()))
        
        type.type("Sitting in your car, something feels... off. Familiar. Like you've lived this exact moment before.")
        print(PAR)
        type.type("The clouds are the same. The breeze is the same. Even the bird on that branch is the same.")
        print(PAR)
        type.type("Deja vu? Or something more?")
        print(PAR)
        type.type("A strange certainty washes over you: today, something significant will happen at the casino.")
        print(PAR)
        if self.has_item("Flask of Pocket Aces"):
            type.type("The " + cyan(bright("Flask of Pocket Aces")) + " taps twice against your ribs. Two clean beats. Two hidden aces waiting somewhere in the day.")
            print(PAR)
            bonus = random.randint(20, 60)
            type.type("You find " + green(bright("$" + str(bonus))) + " under the seat before noon and take it as confirmation.")
            self.change_balance(bonus)
            self.restore_sanity(3)
            print(PAR)
        self.add_status("Lucky")
        type.type(yellow(bright("You feel like the universe is trying to tell you something.")))
        print(PAR)

        print(PAR)
        return
    def left_door_open(self):
        # EVENT: Car door was left open all night
        # EFFECTS: 50% chance Spider danger, 17% chance Squirrel danger; Pest Control can prevent infestation
        variant = random.randrange(3)
        if variant == 0:
            type.type("A chill runs through your entire body. ")
            type.type("Had the passenger door really been open all night? ")
            type.type("The seat is cold. There are leaves on the floor. Something was definitely in here.")
            print(PAR)
            type.type("You reach over and close the door, trying not to think about what might still be under the seat.")
        elif variant == 1:
            type.type("You jolt awake to the sound of birds. Not outside birds. INSIDE birds. No wait — that's a squirrel.")
            print(PAR)
            type.type("The passenger door is wide open. Nature has accepted your invitation.")
            print(PAR)
            type.type("You shoo everything out — or try to — and slam the door shut. Your heart is racing.")
        else:
            type.type("Morning light pours through the open passenger door. The WIDE open passenger door.")
            print(PAR)
            type.type("How long has it been like that? All night? Your entire car is basically a motel room with no door.")
            print(PAR)
            type.type("You close it and check every surface for stowaways.")
        print(PAR)
        if self.has_item("Pest Control"):
            type.type("You give the interior a precautionary spray with your " + magenta(bright("Pest Control")) + ". Whatever crawled in is about to regret it.")
            print(PAR)
            return
        random_chance = random.randrange(6)
        if random_chance <= 2:
                self.add_danger("Spider")
        elif random_chance == 3:
                self.add_danger("Squirrel")
        print(PAR)

    # Conditional

        print(PAR)
        return
    def another_spider_bite(self):
        # EVENT: Spider bites you again on the neck
        # CONDITION: Requires "Spider" danger, not already having "Spider Bite"
        # EFFECTS: Pest Control kills spider; Flask of Anti-Venom neutralizes venom; adds "Spider Bite" status
        if not self.has_danger("Spider") or self.has_status("Spider Bite"):
            self.day_event()
            return
        
        type.type("A sharp pain stings your neck! ")
        type.type("Swinging your arm to scratch the pain, you watch as a spider jumps to the backseat. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
            type.type("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
            type.type("Hopefully, that's the end of your spider problems.")
        elif self.has_item("Flask of Anti-Venom"):
            self.use_item("Flask of Anti-Venom")
            print(PAR)
            type.type("You reach for the " + cyan(bright("Flask of Anti-Venom")) + " before the venom can spread.")
            print(PAR)
            type.type("The burning stops. You feel it working — neutralizing whatever that spider injected into you.")
            print(PAR)
            type.type("The spider disappears under the seat. But you've already won this one.")
            self.heal(5)
        else:
            type.type("The spider, now out of reach, crawls off the seat and onto the floor. ")
            type.type("You stick your head out back, but you aren't sure where the spider went, or if it has a family nearby. This is unfortunate.")
        self.add_status("Spider Bite")
        self.mark_day("Spider Bite")
        print(PAR)

        print(PAR)
        return
    def power_outage_area(self):
        # Everytime - atmospheric event
        variant = random.randrange(3)
        if variant == 0:
            type.type("The entire block goes dark. Power outage. The streetlights, the shops, everything.")
            print(PAR)
            type.type("You sit in your car, watching people stumble around with flashlights, and feel strangely superior. You don't need electricity. You're already off the grid.")
        elif variant == 1:
            type.type("Traffic lights are out. An intersection nearby becomes chaos. Cars honking, people yelling.")
            print(PAR)
            type.type("You watch the disaster unfold from the safety of your parked wagon. Entertainment.")
        else:
            type.type("A transformer explodes somewhere nearby. Sparks shower into the street.")
            print(PAR)
            type.type("Beautiful, in a terrifying sort of way.")
        print(PAR)

        print(PAR)
        return
    def construction_noise(self):
        # Everytime - minor annoyance
        variant = random.randrange(3)
        if variant == 0:
            type.type("BANG BANG BANG. Construction starts at 6 AM. Right next to your car. Of course.")
            print(PAR)
            type.type("You move to a different spot. The construction sounds follow you. Are they... expanding?")
        elif variant == 1:
            type.type("A jackhammer starts up nearby. Your teeth are literally vibrating.")
            print(PAR)
            type.type("You cover your ears and wait for it to stop. It takes four hours.")
            self.hurt(5)
        else:
            type.type("The sound of a cement mixer becomes your alarm clock this morning. Not the most peaceful wake-up.")
            print(PAR)
            type.type("At least they wave at you when they notice you're awake.")
        print(PAR)

    # ==========================================
    # NEW MODEST DAY EVENTS - Conditional
    # ==========================================
    
        print(PAR)
        return
    def left_trunk_open(self):
        # EVENT: Trunk was left open all night
        # EFFECTS: 33% chance Rat danger, 33% chance Termite danger; Pest Control prevents infestation
        variant = random.randrange(3)
        if variant == 0:
            type.type("A cold draft fills the whole wagon. ")
            type.type("Had the trunk really been open all night? ")
            type.type("You get out and walk around back. Yep. Wide open. Like a gaping invitation to every critter in a five-mile radius.")
        elif variant == 1:
            type.type("You hear a THUNK from the back. Then scratching. Then silence.")
            print(PAR)
            type.type("The trunk is open. Something was in there. Maybe still is.")
            print(PAR)
            type.type("You close it slowly, carefully, like defusing a bomb made of wildlife.")
        else:
            type.type("The trunk latch must have popped in the night. It's happened before, but this time the smell of damp earth wafts through the car.")
            print(PAR)
            type.type("Something tracked mud into the trunk. Paw prints. Small ones. You close it and hope for the best.")
        print(PAR)
        if self.has_item("Pest Control"):
            type.type("You give the trunk a thorough blast of " + magenta(bright("Pest Control")) + ". Chemical warfare. Nothing survives.")
            print(PAR)
            type.type("Whatever was in there, it's not anymore. Or it's dead. Either works.")
            print(PAR)
            return
        random_chance = random.randrange(6)
        if random_chance < 2:
                self.add_danger("Rat")
        elif random_chance < 4:
                self.add_danger("Termite")
        print(PAR)

    # Conditional

        print(PAR)
        return
    def deja_vu_again(self):
        type.type("The strangest feeling hits you as you sit in your car. You've done this exact thing before.")
        print(PAR)
        type.type("Same sunrise. Same ache in your back. Same existential dread.")
        print(PAR)
        type.type("Wait, have you? The days are starting to blur together. Was yesterday real? Is TODAY real?")
        print(PAR)
        type.type("You pinch yourself. It hurts. Okay, probably real.")
        print(PAR)
        self.lose_sanity(1)
        print(PAR)

        print(PAR)
        return
    def damaged_exhaust_fixed(self):
        if not self.has_danger("Damaged Exhaust"):
            self.day_event()
            return
        if self.get_balance() < 100:
            self.day_event()
            return
        type.type("A mechanic spots your exhaust problem while you're parked.")
        print(PAR)
        type.type(quote("That's leaking carbon monoxide into your car. You'll die in your sleep."))
        print(PAR)
        type.type(quote("I can patch it for $100. Not perfect, but safe."))
        print(PAR)
        answer = ask.yes_or_no("Pay for the repair? ($100) ")
        if answer == "yes":
            type.type("Fixed. You'll live to see another day.")
            self.change_balance(-100)
            self.remove_danger("Damaged Exhaust")
        else:
            type.type("He shakes his head. " + quote("Your funeral."))
        print(PAR)

        print(PAR)
        return
    def damaged_exhaust_again(self):
        if not self.has_danger("Damaged Exhaust"):
            self.day_event()
            return
        type.type("A headache again. That familiar exhaust smell.")
        print(PAR)
        type.type("The carbon monoxide is still leaking. You're slowly poisoning yourself.")
        print(PAR)
        chance = random.randrange(10)
        if chance < 7:
            type.type("You open all the windows and air out the car. Headache fades.")
            self.hurt(10)
            self.lose_sanity(5)
        elif chance < 9:
            type.type("You nearly pass out before getting the door open. Too close. Again.")
            self.hurt(25)
            self.lose_sanity(15)
        else:
            type.type("This time you don't wake up in time.")
            print(PAR)
            self.kill("Carbon monoxide poisoning. You knew the exhaust was broken. You didn't fix it.")
            return
        print(PAR)

    # === UNPAID TICKETS EXTENDED CHAIN ===

        print(PAR)
        return
    def found_twenty(self):
        variant = random.randrange(4)
        if variant == 0:
            type.type("You step out of your car and your shoe lands on something papery. A twenty, face-up, staring at you like Andrew Jackson himself is offering it.")
            print(PAR)
            type.type("No one around. No wallet in sight. Just the universe cutting you a break for once.")
        elif variant == 1:
            type.type("The wind picks up and slaps a bill against your windshield. You peel it off. Twenty bucks.")
            print(PAR)
            type.type("Somewhere, someone is cursing the wind. But that's not your problem.")
        elif variant == 2:
            type.type("You're digging between the seats for a pen — don't ask why — and your fingers close around a crumpled bill.")
            print(PAR)
            type.type("A twenty. Past-you was apparently a squirrel, hiding nuts for winter.")
        else:
            type.type("A twenty-dollar bill tumbles across the parking lot like a tumbleweed. You chase it. Step on it. Victory.")
            print(PAR)
            type.type("An old man on a bench watches you celebrate catching a piece of paper. He doesn't judge. He's been there.")
        self.change_balance(20)
        print(PAR)

        print(PAR)
        return
    def lost_wallet(self):
        if self.get_balance() < 50:
            self.day_event()
            return
        variant = random.randrange(3)
        if variant == 0:
            type.type("You shift in your car seat and realize your pocket feels light. Your wallet is gone.")
            print(PAR)
            type.type("You check the other pocket. Under the seat. Between the cushions. Nothing. NOTHING.")
            print(PAR)
            type.type("That sinking feeling in your stomach? That's not hunger. That's the universe pickpocketing you.")
        elif variant == 1:
            type.type("You reach for your wallet at the gas station. It's not there. You check again. Not there.")
            print(PAR)
            type.type("You pat every pocket. Turn your pants inside out in the parking lot. A woman shields her child's eyes.")
            print(PAR)
            type.type("It's gone. Must have fallen out. Or been pulled out.")
        else:
            type.type("Your wallet has vanished. Poof. Gone. Like it never existed.")
            print(PAR)
            type.type("You spend twenty minutes on your hands and knees searching the car, the pavement, the bushes. You find a quarter. Not helpful.")
        print(PAR)
        if self.has_item("Signal Mirror"):
            print(PAR)
            type.type("You catch the sun with your " + cyan(bright("Signal Mirror")) + ". The reflected beam flashes across the horizon like a lighthouse on land.")
            print(PAR)
            type.type("Someone, somewhere, sees the light. Help is closer than you think.")
            self.restore_sanity(3)
        lost = min(self.get_balance(), random.randint(50, 200))
        type.type("You lost " + red(bright("${:,}".format(int(lost)))) + ".")
        self.change_balance(-lost)
        self.lose_sanity(10)
        print(PAR)

        print(PAR)
        return
    def sunburn(self):
        if self.has_item("Cheap Sunscreen") or self.has_item("Premium Sunscreen"):
            screen = "Premium Sunscreen" if self.has_item("Premium Sunscreen") else "Cheap Sunscreen"
            type.type("You fell asleep with the window cracked. In direct sunlight. Like an idiot.")
            print(PAR)
            type.type("But past-you was smarter than present-you — the " + magenta(bright(screen)) + " on your arm took the hit.")
            print(PAR)
            type.type("Slight redness. Could've been way worse. Thank you, past-you.")
            self.hurt(3)
            self.restore_sanity(4)
            print(PAR)
            return
        if self.has_item("Sunglasses"):
            type.type("You fell asleep with the window cracked, but at least you'd had your " + magenta(bright("Sunglasses")) + " on.")
            print(PAR)
            type.type("Your arms got scorched, but your eyes are fine. Small mercy. You look vaguely cool while suffering.")
            self.hurt(8)
            self.restore_sanity(2)
            print(PAR)
            return
        if self.has_item("Umbrella"):
            type.type("You fell asleep with the window cracked, but your " + magenta(bright("Umbrella")) + " was propped against the window.")
            print(PAR)
            type.type("Half your arm is burnt, half is fine. The umbrella line is visible. You look ridiculous but functional.")
            self.hurt(7)
            self.restore_sanity(2)
            print(PAR)
            return
        variant = random.randrange(3)
        if variant == 0:
            type.type("You fell asleep with the window cracked. In direct sunlight.")
            print(PAR)
            type.type("Your arm is bright red. Blistering. You look like a lobster who made bad life choices.")
        elif variant == 1:
            type.type("The sun found you. Through the cracked window, it cooked your forearm like a steak on a dashboard grill.")
            print(PAR)
            type.type("You peel your arm off the armrest. Some skin stays behind. Lovely.")
        else:
            type.type("You wake up and immediately know something is wrong. Your neck is on fire. Not metaphorically.")
            print(PAR)
            type.type("Sunburn. The kind that hurts when you think about it. The kind where shirts become your enemy.")
        if self.has_item("Splint"):
            print(PAR)
            type.type("The " + cyan(bright("Splint")) + " braces your aching joints. Crude, but effective. You can keep moving.")
            self.heal(5)
        self.hurt(15)
        print(PAR)

        print(PAR)
        return
    def mosquito_bite_infection(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("You scratch your arm in the car. That mosquito bite you kept scratching? It's infected now.")
            print(PAR)
            type.type("Red, swollen, oozing. You know you shouldn't have scratched it. But you did. Because you're you.")
        elif variant == 1:
            type.type("Your arm itches. It's been itching for two days. You finally look at it.")
            print(PAR)
            type.type("The mosquito bite has turned into something that belongs in a medical textbook. The gross chapter.")
        else:
            type.type("Remember that mosquito? The one you let bite you because you were too tired to swat it?")
            print(PAR)
            type.type("Well, it left you a gift. An angry, infected, weeping gift. On your elbow. Right where the seat rubs.")
        print(PAR)
        if self.has_item("Wound Salve"):
            type.type("You dig out the " + cyan(bright("Wound Salve")) + " and smear it over the bite. The sting fades almost instantly.")
            print(PAR)
            type.type("By morning, the swelling is gone. That homemade gunk actually works.")
            self.hurt(2)
            self.restore_sanity(2)
            print(PAR)
            return
        if self.has_item("First Aid Kit"):
            type.type("Good thing you have that " + magenta(bright("First Aid Kit")) + ". You clean it, disinfect it, bandage it. Almost like a real adult.")
            self.hurt(3)
            self.restore_sanity(3)
        else:
            type.type("You don't have anything to treat it with. You tear off a piece of your shirt and wrap it. Field medicine at its finest.")
            self.hurt(10)
        print(PAR)

        print(PAR)
        return
    def good_hair_day(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("You check yourself in the car mirror. Against all odds, your hair looks good today.")
            print(PAR)
            type.type("You live in a car. You shower at truck stops. But today? You could be on a magazine cover. A very specific, niche magazine. But still.")
        elif variant == 1:
            type.type("The truck stop shower this morning had actual water pressure. REAL water pressure. Like a normal person shower.")
            print(PAR)
            type.type("Your hair is clean, fluffy, and cooperating. You keep touching it. Is this what happiness feels like?")
        else:
            type.type("You catch your reflection in the side mirror and do a double take. Who IS that handsome devil?")
            print(PAR)
            type.type("Oh. It's you. With inexplicably great hair. The Dealer's gonna be intimidated tonight.")
        self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def bad_hair_day(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("You glance in the car mirror. Your hair is a disaster. A matted, greasy catastrophe.")
            print(PAR)
            type.type("You try to fix it. Somehow make it worse. The laws of physics should not allow what your hair is doing right now.")
        elif variant == 1:
            type.type("A bird lands on your car. Sees your hair. Considers building a nest in it.")
            print(PAR)
            type.type("You shoo it away, but you can't shoo away the truth: you look like you were electrocuted in your sleep.")
        else:
            type.type("You haven't looked in a mirror in three days. You finally do.")
            print(PAR)
            type.type("Your hair has formed an alliance with gravity, grease, and the concept of defeat. It hangs there, mocking you.")
            print(PAR)
            type.type("You put on a hat. Problem solved. Problem hidden.")
        self.lose_sanity(3)
        print(PAR)

        print(PAR)
        return
    def found_gift_card(self):
        type.type("You find a gift card on the ground next to your car. Fast food place. Has $15 on it.")
        print(PAR)
        type.type("Free food! The universe provides. Sometimes.")
        self.heal(15)
        print(PAR)

        print(PAR)
        return
    def car_battery_dead(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("You turn the key. Click. Click. Nothing. The battery is dead. Stone dead.")
            print(PAR)
            type.type("You try again. And again. As if the fifteenth attempt will be the charm. It won't.")
        elif variant == 1:
            type.type("The engine makes a sound like a dying animal and gives up. Battery.")
            print(PAR)
            type.type("You left the interior light on all night. Again. Because you're your own worst enemy.")
        else:
            type.type("Nothing. Not a sound. Not a click. Not a whimper. The car is dead and it's your fault.")
            print(PAR)
            type.type("You sit there for a minute, key in the ignition, staring at the dashboard like it betrayed you. It didn't. You betrayed it.")
        print(PAR)
        if self.has_item("Tool Kit"):
            type.type("Luckily, your " + magenta(bright("Tool Kit")) + " has cables in it. You flag someone down and get a jump in ten minutes.")
            print(PAR)
            type.type("Having tools makes you feel like a competent human being. The bar is low, but you cleared it.")
            self.restore_sanity(5)
        else:
            type.type("You stand on the roadside, holding imaginary cables, hoping someone takes pity on you.")
            print(PAR)
            random_chance = random.randrange(3)
            if random_chance == 0:
                type.type("A trucker pulls over after an hour. Doesn't say much. Just jumps you and drives off. Angels come in 18-wheelers.")
            elif random_chance == 1:
                type.type("It takes two hours. TWO. You stand there like a scarecrow holding a sign that says " + quote("PLEASE.") + " Finally, a minivan stops.")
                self.lose_sanity(5)
            else:
                type.type("Nobody stops. For three hours. You end up walking to a gas station and buying a jump pack for $40.")
                if self.get_balance() >= 40:
                    self.change_balance(-40)
                else:
                    type.type("...which you can't afford. The attendant takes pity and lets you borrow one. Humiliating.")
                    self.lose_sanity(8)
            self.lose_sanity(3)
        print(PAR)

        print(PAR)
        return
    def flat_tire_again(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("Another flat tire. You're starting to think the universe has a personal vendetta against your wheels.")
        elif variant == 1:
            type.type("You step out of the wagon and immediately feel the lean. Flat. Again. You don't even get mad anymore.")
        else:
            type.type("THWAP. That sound. You know that sound. It's the sound of your afternoon disappearing into a rubber pancake.")
        print(PAR)
        if self.has_item("Spare Tire"):
            type.type("But wait — you've got a " + magenta(bright("Spare Tire")) + ". Twenty minutes of grunting and swearing later, you're back on four wheels.")
            print(PAR)
            type.type("Competence feels good. Rare, but good.")
            self.use_item("Spare Tire")
        elif self.has_item("Duct Tape"):
            type.type("You look at the tire. You look at your " + magenta(bright("Duct Tape")) + ". You look at the tire again.")
            print(PAR)
            type.type("This is a terrible idea. You do it anyway. It holds. Barely. You drive like you're transporting a soufflé.")
            self.hurt(3)
        elif self.get_balance() >= 50:
            type.type("You flag down a guy with a truck. He fixes it for $50. Doesn't make conversation. Doesn't need to.")
            self.change_balance(-50)
        else:
            type.type("You can't afford to fix it. No spare. No tape. No money. No options.")
            print(PAR)
            type.type("You sit on the curb next to your crippled wagon and watch the traffic go by. Everyone else is going somewhere.")
            self.lose_sanity(10)
        print(PAR)

        print(PAR)
        return
    def nice_weather(self):
        if self.has_item("Wanderer's Rest"):
            type.type("Perfect weather at the " + cyan(bright("Wanderer's Rest")) + ". The tree has grown another branch overnight. An apple falls into your hand.")
            print(PAR)
            self.heal(15)
            self.restore_sanity(20)
            return
        if self.has_item("Nomad's Camp"):
            type.type("The " + cyan(bright("Nomad's Camp")) + " thrives in perfect weather. You're more at home here than anywhere with walls.")
            print(PAR)
            self.heal(10)
            self.restore_sanity(15)
            return
        type.type("Perfect weather today. Not too hot. Not too cold. Just right.")
        print(PAR)
        type.type("You sit outside your car and just... breathe. It's nice.")
        self.restore_sanity(8)
        print(PAR)

        print(PAR)
        return
    def terrible_weather(self):
        type.type("The weather is miserable. Rain sideways. Wind shaking your car.")
        print(PAR)
        type.type("You huddle in your seat and wait for it to pass. For hours.")
        if self.has_item("Storm Suit") or self.has_item("All-Weather Armor"):
            item_name = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Storm Suit"
            type.type("The " + cyan(bright(item_name)) + " shrugs at terrible weather like it's a light mist.")
            print(PAR)
            self.restore_sanity(3)
            return
        elif self.has_item("Umbrella") or self.has_item("Poncho"):
            gear = "Umbrella" if self.has_item("Umbrella") else "Poncho"
            type.type("Your " + cyan(bright(gear)) + " makes the terrible weather merely annoying instead of miserable.")
            print(PAR)
            self.lose_sanity(2)
            return
        self.lose_sanity(5)
        print(PAR)

        print(PAR)
        return
    def weird_noise(self):
        type.type("Your car is making a new noise. A concerning noise.")
        print(PAR)
        type.type("Clunk. Clunk. Clunk. Every time you turn.")
        print(PAR)
        type.type("You have no idea what it is. You ignore it and hope for the best.")
        self.add_danger("Mystery Car Problem")
        print(PAR)

        print(PAR)
        return
    def mystery_car_problem_worsens(self):
        if not self.has_danger("Mystery Car Problem"):
            self.day_event()
            return
        type.type("That noise is getting worse. Much worse. The car shudders now too.")
        print(PAR)
        chance = random.randrange(5)
        if chance == 0:
            type.type("Something FALLS OFF the car. You don't even know what it was.")
            print(PAR)
            type.type("A piece of metal, clattering away down the road. Cool. Cool cool cool.")
            self.hurt(5)
            self.lose_sanity(10)
        else:
            type.type("It's probably fine. Probably.")
        print(PAR)

        print(PAR)
        return
    def got_a_tan(self):
        type.type("You catch your reflection in the car mirror. All this outdoor living has given you a nice tan.")
        print(PAR)
        type.type("Silver linings. You look healthy, even if you're not.")
        self.restore_sanity(3)
        print(PAR)

        print(PAR)
        return
    def someone_stole_your_stuff(self):
        if self.has_item("Binoculars"):
            variant = random.randrange(2)
            if variant == 0:
                type.type("From across the parking lot, you catch movement with your " + magenta(bright("Binoculars")) + ". Someone circling your car.")
                print(PAR)
                type.type("You walk over, casual. They scatter before you arrive.")
                type.type(" Nothing taken. The binoculars paid for themselves.")
                self.restore_sanity(5)
            else:
                type.type("You spot a figure trying your door handle through your " + magenta(bright("Binoculars")) + " from fifty yards.")
                print(PAR)
                type.type("You sprint back. They run. Nobody wins, nobody loses.")
                self.restore_sanity(4)
            print(PAR)
            return
        if self.has_item("Padlock") or self.has_item("Car Alarm Rigging"):
            device = "Car Alarm Rigging" if self.has_item("Car Alarm Rigging") else "Padlock"
            variant = random.randrange(2)
            if variant == 0:
                type.type("You come back to the wagon and see scratch marks around the door handle. Someone tried to break in.")
                print(PAR)
                type.type("Tried. Your " + magenta(bright(device)) + " held. There's a screwdriver on the ground — they dropped it and ran.")
                print(PAR)
                type.type("Nice try, buddy. Not today.")
            else:
                type.type("A shadow moves away from your wagon as you approach. Someone was casing it.")
                print(PAR)
                type.type("They see your " + magenta(bright(device)) + " and think better of it. Smart.")
                print(PAR)
                type.type("You make a mental note to sleep lighter anyway.")
            self.restore_sanity(5)
            print(PAR)
            return
        variant = random.randrange(3)
        if variant == 0:
            type.type("Someone broke into your car while you were at the casino.")
            print(PAR)
            type.type("They didn't take money — you had that on you. But they took... things.")
            print(PAR)
            type.type("A jacket. Some food. Your sense of security. That last one hurts the most.")
        elif variant == 1:
            type.type("The window is smashed. Glass everywhere. Your stuff is tossed around like a tornado hit.")
            print(PAR)
            type.type("They took your blanket. Your BLANKET. What kind of monster steals a homeless man's blanket?")
            print(PAR)
            type.type("You spend the afternoon cleaning glass out of your seat. Every piece is a little shard of betrayal.")
        else:
            type.type("Everything's wrong. The glove box is open. The trunk is popped. Stuff is missing.")
            print(PAR)
            type.type("You do a mental inventory. Food — gone. Spare clothes — gone. That weird rock you liked — gone.")
            print(PAR)
            type.type("The rock hurts the most. You'd had it since day one. It was a good rock.")
        self.lose_sanity(15)
        self.hurt(5)
        print(PAR)

        print(PAR)
        return
    def back_pain(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("Your back is KILLING you. Sleeping in a car seat isn't good for the spine. Shocking revelation.")
            print(PAR)
            type.type("You try to straighten up. Something pops. Not the good kind of pop. The kind that makes you question your mortality.")
        elif variant == 1:
            type.type("You can't turn your neck. At all. It's locked in place, like your spine has unionized and is staging a protest.")
            print(PAR)
            type.type("Every movement is a negotiation with pain. Pain is winning.")
        else:
            type.type("Getting out of the car takes three attempts. Your lower back has decided it hates you. Specifically you. Personally.")
            print(PAR)
            type.type("You stand in the parking lot bent at a 45-degree angle like a question mark. People stare. You deserve it.")
        print(PAR)
        if self.has_item("First Aid Kit"):
            type.type("You dig out the " + magenta(bright("First Aid Kit")) + " and find a heat pack buried in the bottom. You slap it on your lower back.")
            print(PAR)
            type.type("It's not physical therapy, but it's the next best thing when your chiropractor is a steering wheel.")
            self.hurt(5)
        else:
            self.hurt(15)
        print(PAR)

        print(PAR)
        return
    def stretching_helps(self):
        type.type("You do some stretches. Yoga-ish movements. Look like an idiot in a parking lot.")
        print(PAR)
        type.type("But you know what? You feel better. Less like a rusty robot.")
        self.hurt(-10)
        self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def random_kindness(self):
        variant = random.randrange(4)
        if variant == 0:
            type.type("Someone hands you a bag of groceries. Doesn't say anything. Just smiles and leaves.")
            print(PAR)
            type.type("Inside: bread, peanut butter, water bottles. Basic stuff.")
            print(PAR)
            type.type("Your eyes are wet. When did you become someone who needs charity?")
        elif variant == 1:
            type.type("An old woman knocks on your window. You flinch. She holds up a thermos.")
            print(PAR)
            type.type(quote("Coffee. Cream and sugar already in it. You looked like you needed it."))
            print(PAR)
            type.type("She walks away before you can say thank you. The coffee is perfect. Impossibly perfect.")
            print(PAR)
            type.type("You drink it slowly, because some things shouldn't be rushed.")
        elif variant == 2:
            type.type("A guy in a pickup pulls up beside you and tosses a blanket through the window.")
            print(PAR)
            type.type(quote("Been there, brother.") + " That's all he says. Then he drives off.")
            print(PAR)
            type.type("The blanket smells like fabric softener. You bury your face in it and breathe deep.")
            print(PAR)
            type.type("Three words and a blanket. That's all it takes to remind you that people can be good.")
        else:
            type.type("You're counting change in the gas station parking lot. A woman watches you from across the lot.")
            print(PAR)
            type.type("She walks over, tucks a twenty into your shirt pocket, and squeezes your shoulder.")
            print(PAR)
            type.type(quote("You're gonna be alright.") + " Her eyes are so certain. Like she knows something you don't.")
            print(PAR)
            type.type("You almost believe her.")
            self.change_balance(20)
        self.heal(20)
        self.restore_sanity(10)
        self.lose_sanity(5)  # Mixed feelings
        print(PAR)

        print(PAR)
        return
    def random_cruelty(self):
        variant = random.randrange(4)
        if variant == 0:
            type.type("Some teenagers throw something at your car. Laughing. Running away.")
            print(PAR)
            type.type("It's a milkshake. All over your windshield. Sticky and dripping.")
            print(PAR)
            type.type("You get out. They're already gone. Just the sound of their laughter echoing off the parking garage.")
        elif variant == 1:
            type.type("Someone keyed your car. A long, deep scratch from the hood to the trunk.")
            print(PAR)
            type.type("It's not even a good car. Who keys a car this bad? What did they gain from this?")
            print(PAR)
            type.type("You run your finger along the scratch. It's the only straight line in your life right now.")
        elif variant == 2:
            type.type("A group of college kids walks by your wagon. One of them takes a picture.")
            print(PAR)
            type.type(quote("Bro, look at this guy. Living in a car. L-M-A-O."))
            print(PAR)
            type.type("They laugh. You hear it through the window. They're not trying to be quiet about it.")
            print(PAR)
            type.type("You slide lower in your seat and wait for them to leave. They take their time.")
        else:
            type.type("Somebody stuck a note under your wiper blade. You pull it off, hopeful. Maybe it's kind. Maybe someone noticed you.")
            print(PAR)
            type.type("It reads: " + quote("GET A JOB, LOSER."))
            print(PAR)
            type.type("You crumple it up. Hold it for a while. Then let it drop.")
        self.lose_sanity(12)
        print(PAR)

        print(PAR)
        return
    def prayer_answered(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("You're sitting in your car. You prayed last night. For something. Anything.")
            print(PAR)
            type.type("Today, things went your way. Small things. But things.")
            print(PAR)
            type.type("The gas station had free coffee. A stranger held the door. Nobody looked at you like you were garbage.")
            print(PAR)
            type.type("Coincidence? Divine intervention? Does it matter?")
        elif variant == 1:
            type.type("Last night you whispered into the dark: " + quote("Just let tomorrow be better. That's it. Just... better."))
            print(PAR)
            type.type("And it was. Not great. Not fixed. But better. The sun came out. Your back didn't hurt as much. You found a $5 bill in the cupholder.")
            print(PAR)
            type.type("Is someone listening? You look up at the sky. It doesn't answer. But it doesn't rain, either.")
            self.change_balance(5)
        else:
            type.type("You prayed last night. Not to anyone specific. Just... out into the universe.")
            print(PAR)
            type.type("Today, a butterfly landed on your steering wheel. Sat there for ten minutes. Orange and black and utterly unbothered by your problems.")
            print(PAR)
            type.type("It's not what you asked for. It's not money or shelter or a way out. But it's something. Proof that beauty exists even in parking lots.")
        self.restore_sanity(15)
        print(PAR)

        print(PAR)
        return
    def prayer_ignored(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("You're sitting in your car. You prayed last night. Begged, really. For help. For a sign. For anything.")
            print(PAR)
            type.type("Today was worse than yesterday. The heavens are silent.")
            print(PAR)
            type.type("Maybe no one's listening. Or maybe you're not worth listening to.")
        elif variant == 1:
            type.type("Last night you said the words. All of them. The please and the help me and the I'll do anything.")
            print(PAR)
            type.type("The ceiling of your car stared back. Same as always.")
            print(PAR)
            type.type("Today a bird crapped on your windshield. If that's a sign, you don't want to decode it.")
        else:
            type.type("You prayed for a miracle. Got a parking ticket instead.")
            print(PAR)
            type.type("You crumple the ticket up. What are they going to do, take your car? You live in it. That's cruel and unusual punishment, probably.")
            print(PAR)
            type.type("You look up at the sky. " + quote("Very funny.") + " The sky says nothing. As usual.")
        self.lose_sanity(10)
        print(PAR)

        print(PAR)
        return
    def found_old_photo(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("You find an old photo in your glove box. You forgot it was there.")
            print(PAR)
            type.type("It's you. From before. Smiling. Happy. With people who loved you.")
            print(PAR)
            type.type("You stare at it for a long time. Who was that person? Where did they go? Are they in here somewhere, buried under the gambling and the car-sleeping and the existential dread?")
        elif variant == 1:
            type.type("A photo slips out from behind the sun visor. Lands in your lap. Face up.")
            print(PAR)
            type.type("You in a kitchen. Flour on your nose. Laughing at something someone said. The light through the window is warm and golden.")
            print(PAR)
            type.type("You can't remember what was funny. You can't remember whose kitchen. But you remember the feeling. And feeling it again, even just the echo, hurts more than any bust at the table.")
        else:
            type.type("While digging for napkins, your fingers close on a Polaroid.")
            print(PAR)
            type.type("It's faded. Overexposed. A birthday party. Yours, maybe. There's a cake. Candles. Hands around you.")
            print(PAR)
            type.type("You hold the photo at arm's length, like it might bite. The past is a country you were deported from.")
        self.mark_met("Found Old Photo")
        self.lose_sanity(10)
        self.restore_sanity(5)  # Bittersweet
        print(PAR)

        print(PAR)
        return
    def threw_out_old_photo(self):
        if not self.has_met("Found Old Photo"):
            self.day_event()
            return
        type.type("Sitting in your car, you look at that photo again. The happy you. The old you.")
        print(PAR)
        answer = ask.yes_or_no("Throw it away? ")
        if answer == "yes":
            type.type("You rip it up. Throw the pieces out the window. Watch them scatter.")
            print(PAR)
            type.type("That person is gone. Time to move on.")
            self.lose_sanity(5)
        else:
            type.type("You put it back. Can't let go. Not yet.")
        print(PAR)

        print(PAR)
        return
    def empty_event(self):
        variant = random.randrange(5)
        if variant == 0:
            type.type("Nothing happens today. Not a single thing. You sit in your car and exist.")
            print(PAR)
            type.type("It should be peaceful. Instead, it's terrifying. When nothing happens, you have to think. And thinking is dangerous.")
            self.lose_sanity(2)
        elif variant == 1:
            type.type("The day passes like a held breath. Morning becomes afternoon becomes evening, and you've done nothing.")
            print(PAR)
            type.type("Not because you couldn't. Because you didn't want to. The weight of it all just... pinned you to the seat.")
            self.lose_sanity(3)
        elif variant == 2:
            type.type("You stare at the ceiling of your wagon for six straight hours. You count the stains. Forty-seven.")
            print(PAR)
            type.type("At some point, you fall asleep with your eyes open. When you snap out of it, the sun is setting.")
            print(PAR)
            type.type("Where did the day go? Where did any of them go?")
        elif variant == 3:
            type.type("A quiet day. Suspiciously quiet. Like the world is loading the next catastrophe.")
            print(PAR)
            type.type("You spend it waiting for the other shoe to drop. It doesn't. Somehow that's worse.")
        else:
            type.type("You do laundry at a laundromat. Watch your clothes spin. It's oddly meditative.")
            print(PAR)
            type.type("Warm clothes out of a dryer might be the closest thing to a hug you've had in weeks.")
            self.restore_sanity(3)
        print(PAR)

    # ==========================================
    # COMPANION DAY EVENTS
    # ==========================================

        print(PAR)
        return
    def turn_to_god(self):
        # EVENT: Father Ezekiel offers you a Bible and asks about your faith
        # ONE-TIME: Only happens once (checks "Ezekiel" met status)
        # EFFECTS: If accept, becomes religious (affects some events/dialogue)
        if self.has_met("Ezekiel"):
            self.day_event()
            return
        
        self.meet("Ezekiel")
        type.type("There's a knock on your window. You sit up to see a man holding a bible, wearing a cross on a chain around his neck.")
        print(PAR)
        type.type(quote("Hello! I'm Father Ezekiel. You seem to be in a tough spot, living in your car? "))
        type.type(quote("I was just wondering if you wanted me to give you my copy of The Bible. "))
        type.type(quote("It has the word of God, and I hope it could help you understand that you aren't alone on this journey of life."))
        print(PAR)
        type.type(space_quote("Do you accept my offer, and Jesus as your savior?"))
        answer = ask.yes_or_no(space_quote("Do you?"))
        if answer == "yes":
            self._is_religious = True
            type.type(space_quote("Why, that's wonderful!"))
            type.type("Father Ezekiel hands you his bible. ")
            type.type(quote("I will pray for you, and I know that Jesus will always be with you. Amen."))
        elif answer == "no":
            type.type(open_quote("Well, to each their own. I certainly cast no judgments. "))
            type.type(close_quote("I will pray for you, and I know that Jesus will always be with you. Amen."))
        print(PAR)
        type.type("And with that, Father Ezekiel walks down the road, and out of sight.")
        print(PAR)
        return
    
    def thunderstorm(self):
        # EVENT: Major thunderstorm traps you in your car for the day
        # EFFECTS: Adds "Rain" travel restriction, preventing casino travel; Umbrella/Poncho can override
        variant = random.randrange(3)
        if variant == 0:
            type.type("Raindrops begin hitting the roof of your wagon. ")
            type.type("It starts with a couple, then a few, and before you even get the chance to stretch, it begins to pour. ")
            type.type("The sky is a dark, dark gray, and streams start to form along the road.")
            print(PAR)
            type.type("The pitter-patter of the rain on your car lulls you back to sleep. ")
            type.type("When a strike of lightning wakes you once more, you look out the windows to see a few inches of rain covering the street. ")
            type.type("Welp, there goes your plans for the day.")
        elif variant == 1:
            type.type("Thunder. BOOM. You're awake now.")
            print(PAR)
            type.type("Rain hammers the roof like it's trying to break through. Lightning illuminates the sky every few seconds. It's biblical out there.")
            print(PAR)
            type.type("You're not going anywhere today.")
        else:
            type.type("The storm came out of nowhere. One minute, clear skies. The next, your car is being pelted by rain and hail.")
            print(PAR)
            type.type("You watch a trash can blow down the street like a tumbleweed. Nature is angry today.")
        print(PAR)
        if self.has_item("All-Weather Armor"):
            type.type("The " + cyan(bright("All-Weather Armor")) + " was designed for apocalyptic weather. The storm is aesthetically unpleasant and functionally irrelevant.")
            print(PAR)
            self.restore_sanity(5)
            return
        if self.has_item("Storm Suit"):
            type.type("The " + cyan(bright("Storm Suit")) + " is exactly for this. You step out into the storm. You don't get wet. You arrive at the casino like a weathered professional.")
            print(PAR)
            self.restore_sanity(3)
            return
        if self.has_item("Umbrella") or self.has_item("Poncho") or self.has_item("Plastic Poncho"):
            if self.has_item("Poncho"):
                gear = "Poncho"
            elif self.has_item("Plastic Poncho"):
                gear = "Plastic Poncho"
            else:
                gear = "Umbrella"
            type.type("Good thing you've got that " + magenta(bright(gear)) + ". You're not letting a little apocalyptic weather ruin your plans.")
            print(PAR)
            type.type("You suit up, step out into the deluge, and walk to the casino like a soggy but determined lunatic.")
            print(PAR)
            type.type("People in the parking lot stare at you. You don't care. You have places to be and money to lose.")
            print(PAR)
            self.restore_sanity(5)
            return
        self.add_travel_restriction("Rain")
        return
    
    # ==========================================
    # WRONG ITEM COMEDY EVENTS
    # ==========================================

        print(PAR)
        return
    def wrong_item_bug_spray_campfire(self):
        if not self.has_item("Bug Spray"):
            self.day_event()
            return
        type.type("You're sitting by the campfire when a mosquito buzzes past. You grab the " + cyan(bright("Bug Spray")) + " and give a quick spritz.")
        print(PAR)
        type.type("The spray hits the flames. WHOOOMP. A fireball erupts.")
        print(PAR)
        type.type("Your eyebrows are gone. Both of them.")
        print(PAR)
        self.hurt(20)
        self.use_item("Bug Spray")
        type.type("On the bright side, no more mosquitoes.")
        print(PAR)

    # ==========================================
    # NEW DOUGHMAN DAY EVENTS - Everytime
    # ==========================================
    
        print(PAR)
        return
