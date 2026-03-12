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

class DayItemsMixin:
    """Item events: events triggered by specific inventory items"""

    def item_hoarder(self):
        # SECRET: Have 10+ items - you realize you've become a collector
        item_count = len(self._items) if hasattr(self, '_Player__items') else 0
        if item_count < 10:
            self.day_event()
            return
        type.type("You look in your car and realize something: you've accumulated a LOT of stuff.")
        print("\n")
        type.type("Random items. Mementos. Things you've found, bought, been given.")
        print("\n")
        type.type("Your car is basically a rolling museum of your journey.")
        print("\n")
        type.type("Is this hoarding? Or is this... meaning? Every item tells a story.")
        print("\n")
        type.type("You pick up a random item and smile. You remember where you got it.")
        print("\n")
        type.type("Yeah. These aren't just things. They're proof you've lived.")
        self.restore_sanity(8)
        print("\n")

    def shiv_confrontation(self):
        """Having the Shiv changes a mugging encounter"""
        type.type("A man steps out from behind a dumpster, blocking your path.")
        print("\n")
        type.type(quote("Give me your wallet. Now."))
        print("\n")
        if self.has_item("Shiv"):
            type.type("Your hand drops to your side where the " + cyan(bright("Shiv")) + " is tucked into your belt.")
            print("\n")
            type.type("You pull it out slowly. The duct tape handle catches the light. The blade gleams.")
            print("\n")
            type.type("The mugger's eyes go wide. He takes one step back. Then another.")
            print("\n")
            type.type(quote("Whoa, whoa, easy. I don't want any trouble, man."))
            print("\n")
            type.type("He turns and bolts into the alley. You never even said a word.")
            print("\n")
            type.type("Your hands are shaking, but the " + cyan(bright("Shiv")) + " did its job.")
            self.restore_sanity(2)
            print("\n")
        elif self.has_item("Pepper Spray"):
            type.type("You whip out the " + cyan(bright("Pepper Spray")) + " and aim it at his face.")
            print("\n")
            type.type("PSSSHHHHH!")
            print("\n")
            type.type("The man screams, clawing at his eyes, stumbling blindly into the alley. ")
            type.type("You don't stick around to see if he's okay. Spoiler: he's not.")
            print("\n")
            type.type("The " + cyan(bright("Pepper Spray")) + " worked perfectly. One use, one save.")
            self.use_item("Pepper Spray")
            self.restore_sanity(3)
            print("\n")
        else:
            type.type("You don't have anything to defend yourself with. ")
            type.type("He shoves you, takes everything in your pockets, and disappears.")
            lost = min(random.randint(15, 50), self._balance)
            if lost > 0:
                self.change_balance(-lost)
                type.type(" He got " + red("${:,}".format(lost)) + " off you.")
            self.lose_sanity(random.choice([3, 4, 5]))
            self.hurt(random.choice([5, 8, 10]))
            print("\n")

    def lockpick_opportunity(self):
        """Finding a locked container — lockpick set changes outcome"""
        type.type("While walking near the railroad tracks, you spot a rusted metal box half-buried in the gravel.")
        print("\n")
        type.type("It's got a padlock on it. Old, but solid.")
        print("\n")
        if self.has_item("Lockpick Set"):
            type.type("You pull out your " + cyan(bright("Lockpick Set")) + " and go to work.")
            print("\n")
            type.type("The hook slides in. You feel for the pins. One... two... three... ")
            type.slow("click.")
            print("\n")
            type.type("The padlock falls open. You lift the lid.")
            print("\n")
            loot_table = [
                ("Cash", random.randint(20, 100)),
                ("Pocket Knife", 0),
                ("Flashlight", 0),
                ("Old Photograph", 0),
                ("Mysterious Envelope", 0),
                ("Gold Chain", 0),
            ]
            loot = random.choice(loot_table)
            if loot[0] == "Cash":
                type.type("Inside: " + green("${:,}".format(loot[1])) + " in crumpled bills. Not bad for a lockbox.")
                self.change_balance(loot[1])
            elif not self.has_item(loot[0]):
                type.type("Inside: a " + magenta(bright(loot[0])) + "! Finders keepers.")
                self.add_item(loot[0])
            else:
                fallback = random.randint(10, 30)
                type.type("Inside: " + green("${:,}".format(fallback)) + " and some old receipts. Could be worse.")
                self.change_balance(fallback)
            self.restore_sanity(2)
            print("\n")
        elif self.has_item("Pocket Knife"):
            type.type("You try to pry the lock with your " + magenta(bright("Pocket Knife")) + ".")
            print("\n")
            if random.randrange(3) == 0:
                fallback = random.randint(5, 20)
                type.type("After ten minutes of sweating, the lock snaps. Inside: " + green("${:,}".format(fallback)) + ". Was it worth the effort? Debatable.")
                self.change_balance(fallback)
            else:
                type.type("The blade bends. The lock holds. You almost broke your knife for nothing.")
            print("\n")
        else:
            type.type("You don't have anything to open it with. You kick it once. Nothing happens. ")
            type.type("You walk away, wondering what was inside. That's going to bother you all day.")
            self.lose_sanity(1)
            print("\n")

    def fishing_day(self):
        """Fishing rod lets you catch food at water sources"""
        type.type("You come across a quiet pond tucked behind an abandoned gas station. ")
        type.type("The water is clear. Something's moving under the surface.")
        print("\n")
        if self.has_item("Fishing Rod"):
            type.type("You grab your " + cyan(bright("Fishing Rod")) + " from the car and cast a line.")
            print("\n")
            type.type("You sit on the bank, watching the line sway gently in the water. ")
            type.type("The world is quiet. Just you, the pond, and the sky.")
            print("\n")
            self.restore_sanity(5)
            catch = random.randrange(5)
            if catch == 0:
                type.type("A tug! You reel it in — a decent-sized bass. Not bad!")
                print("\n")
                type.type("You wrap it up and put it on ice in the cooler. Fresh fish — good for eating or bartering.")
                self.add_item("Fish")  # Used in adventures.py for Deathclaw race and Kraken encounter
                print("\n")
            elif catch == 1:
                type.type("You reel in... an old boot. Classic. At least the casting was relaxing.")
                print("\n")
            elif catch == 2:
                type.type("After an hour, you hook something heavy. You pull and pull and — ")
                type.type("it's a waterlogged wallet. Inside: " + green("${:,}".format(random.randint(5, 25))) + ". ")
                type.type("The fishing gods provide.")
                self.change_balance(random.randint(5, 25))
                print("\n")
            elif catch == 3:
                type.type("You catch a catfish as long as your forearm. You stare at it. It stares at you. ")
                type.type("You throw it back. Some creatures deserve their freedom. You feel... good about that.")
                self.restore_sanity(3)
                print("\n")
            else:
                type.type("Nothing bites. But honestly? The quiet was worth it. ")
                type.type("Sometimes doing nothing is the most productive thing you can do.")
                print("\n")
        else:
            type.type("You stare at the water. Fish are literally jumping. ")
            type.type("If only you had a fishing rod... You pick up a stick and try to fashion one. ")
            type.type("It doesn't work. Of course it doesn't. You're not that resourceful. Yet.")
            print("\n")

    def trap_night_thief(self):
        """Improvised Trap or Car Alarm Rigging prevents theft"""
        type.type("You wake to a sound outside the car. Footsteps. Slow, careful footsteps.")
        print("\n")
        if self.has_item("Car Alarm Rigging"):
            type.type("BWAAAAAAP! Your " + cyan(bright("Car Alarm Rigging")) + " goes off! ")
            type.type("The horn blasts into the night like an angry foghorn.")
            print("\n")
            type.type("You hear the thief curse, stumble, and sprint away into the darkness.")
            print("\n")
            type.type("You reset the alarm and go back to sleep with a grin. Money well spent. ")
            type.type("Well, not money. Bungee cords and spare fuses. Same difference.")
            self.restore_sanity(2)
            print("\n")
        elif self.has_item("Improvised Trap"):
            type.type("CLANG-CLANG-CLANG! The cans on your " + cyan(bright("Improvised Trap")) + " rattle violently!")
            print("\n")
            type.type("You sit up and see a shadowy figure tangled in the fishing line, cursing and flailing.")
            print("\n")
            if self.has_item("Flashlight"):
                type.type("You flip on your flashlight. ")
            else:
                type.type("You squint into the dark. ")
            type.type("The thief panics and bolts, tripping over the wire one more time for good measure.")
            print("\n")
            type.type("Your stuff is safe. Your trap is a mess, but it'll reset.")
            self.restore_sanity(2)
            print("\n")
        else:
            type.type("The car door opens. Someone reaches in. You pretend to be asleep.")
            print("\n")
            stolen = random.choice(["Flashlight", "Lighter", "Matches", "Sunglasses", "Deck of Cards"])
            if self.has_item(stolen):
                self.use_item(stolen)
                type.type("When you finally dare to look, your " + magenta(bright(stolen)) + " is gone.")
                self.lose_sanity(random.choice([2, 3, 4]))
            else:
                type.type("They rifle through your stuff but don't find much worth taking. Lucky you.")
                self.lose_sanity(2)
            print("\n")

    def dream_catcher_night(self):
        """Dream catcher affects dream quality"""
        if self.has_item("Dream Catcher"):
            dreams = [
                "You dream of a field of wildflowers. Warm sun. Gentle breeze. "
                "The " + cyan(bright("Dream Catcher")) + " sways in the window, and your dreams are soft tonight.",
                "You dream of flying over the city. No fear. Just freedom. "
                "When you wake, the " + cyan(bright("Dream Catcher")) + " is spinning slowly. Catching something.",
                "You dream of a conversation with someone you loved. They smile at you. "
                "You wake up with tears on your face and peace in your chest. The " + cyan(bright("Dream Catcher")) + " did its job.",
                "You dream of nothing. Beautiful, empty nothing. No nightmares. No memories. "
                "Just rest. The " + cyan(bright("Dream Catcher")) + " hangs still. The bad dreams didn't make it through.",
                "You dream of a warm meal, a real bed, and a roof that doesn't leak. "
                "It's not real. But for eight hours, it felt real. The " + cyan(bright("Dream Catcher")) + " gave you that.",
            ]
            type.type(random.choice(dreams))
            self.restore_sanity(random.choice([3, 4, 5]))
            print("\n")
        else:
            nightmares = [
                "You dream of teeth falling out. One by one. Into your hands. You can feel each one leave.",
                "You dream of running down an endless hallway. Something's behind you. You never see what.",
                "You dream you're back at work. Your old job. Your old life. You wake up and don't know which is real.",
                "You dream of drowning in money. Literally drowning. Coins filling your lungs.",
                "You dream of the car shrinking. The walls closing in. You can't breathe. You can't move.",
            ]
            type.type(random.choice(nightmares))
            self.lose_sanity(random.choice([2, 3]))
            print("\n")

    def slingshot_bird_hunt(self):
        """Using the slingshot during the day"""
        type.type("A flock of birds lands on a fence near the parking lot. ")
        type.type("They're loud. Obnoxious. Pooping on everything.")
        print("\n")
        if self.has_item("Slingshot"):
            type.type("You pull out your " + cyan(bright("Slingshot")) + " and load a pebble.")
            print("\n")
            type.type("1. Fire a warning shot (scare them off)")
            print()
            type.type("2. Try to hit one (free food?)")
            print()
            type.type("3. Put it away (they're just birds)")
            print()
            type.type("Choose: ")
            choice = None
            while choice is None:
                try:
                    choice = int(input())
                except ValueError:
                    type.type("Pick a number: ")
            print()
            if choice == 1:
                type.type("TWANG! The pebble zips past the birds. They scatter, squawking in outrage.")
                print("\n")
                type.type("Peace and quiet at last.")
                self.restore_sanity(1)
                print("\n")
            elif choice == 2:
                if random.randrange(3) == 0:
                    type.type("Direct hit! A pigeon drops. You pick it up, feeling a complicated mix of guilt and hunger.")
                    print("\n")
                    type.type("You cook it over a small fire. Pigeon. It tastes like... pigeon.")
                    self.heal(8)
                    print("\n")
                else:
                    type.type("The pebble sails wide. The birds look at you. Judgmentally.")
                    print("\n")
                    type.type("They don't even fly away. They just stare. You've never felt more judged by wildlife.")
                    print("\n")
            else:
                type.type("You put the slingshot away. They're just birds. Let them poop in peace.")
                print("\n")
        else:
            type.type("You throw a rock at them. It misses by ten feet. The birds don't even flinch. ")
            type.type("You are not a threat to wildlife.")
            print("\n")

    def signal_mirror_rescue(self):
        """Signal mirror attracts help during a bad situation"""
        type.type("Your car breaks down on a stretch of road with no cell service. ")
        type.type("The sun beats down. You're stuck.")
        print("\n")
        if self.has_item("Signal Mirror"):
            type.type("You grab your " + cyan(bright("Signal Mirror")) + " and angle it toward the sun.")
            print("\n")
            type.type("Flash. Flash. Flash. The beam shoots across the landscape like a lighthouse.")
            print("\n")
            type.type("After twenty minutes, a truck appears on the horizon. It pulls over.")
            print("\n")
            trucker = random.choice(["Big Dave", "Mama Lu", "Silent Jim", "Wendy"])
            type.type(quote("Saw your signal from a mile away. Name's " + trucker + ". Need a tow?"))
            print("\n")
            type.type("They give you a lift to the nearest gas station. Your car follows behind, rattling all the way.")
            print("\n")
            type.type("Sometimes the simplest tools save the day.")
            self.restore_sanity(3)
            print("\n")
        elif self.has_item("Smoke Signal Kit"):
            type.type("You pull out your " + cyan(bright("Smoke Signal Kit")) + " and light it.")
            print("\n")
            type.type("Black smoke billows into the sky. Within thirty minutes, a fire truck arrives.")
            print("\n")
            type.type("The firefighters look annoyed when they realize you're not actually on fire. ")
            type.type("But they call you a tow truck. The " + cyan(bright("Smoke Signal Kit")) + " is spent.")
            self.use_item("Smoke Signal Kit")
            self.restore_sanity(2)
            print("\n")
        elif self.has_item("Broken Compass"):
            type.type("You dig through your bag. No signal mirror, but you do have a " + cyan(bright("Broken Compass")) + ".")
            print("\n")
            type.type("The glass face is still intact. You crack it open, polish the glass on your jeans, and hold it up.")
            print("\n")
            type.type("It's not a great mirror, but it catches the light well enough.")
            print("\n")
            type.type("A passing truck slows. They drive you to the nearest town.")
            type.type(" Next time, you think, you'll craft a proper Signal Mirror from this.")
            self.restore_sanity(2)
            print("\n")
        else:
            type.type("You sit on the hood and wait. And wait. And wait.")
            print("\n")
            type.type("Three hours later, someone finally stops. ")
            type.type("They charge you " + red("$25") + " for the ride. At least you're not dead.")
            self.change_balance(-min(25, self._balance))
            self.lose_sanity(3)
            self.add_fatigue(5)
            print("\n")

    def rain_collector_bonus(self):
        """Rain collector provides water during rainy days"""
        type.type("The rain hammers the roof of your car all morning. ")
        type.type("Normally, rainy days just make everything worse.")
        print("\n")
        if self.has_item("Rain Collector"):
            type.type("But your " + cyan(bright("Rain Collector")) + " is doing its thing. ")
            type.type("Clean water drips into the bottle, drop by steady drop.")
            print("\n")
            type.type("You drink the fresh rainwater. It's cold. It's clean. It's free.")
            print("\n")
            type.type("Sometimes the best inventions are the simplest ones.")
            self.heal(5)
            self.restore_sanity(2)
            print("\n")
        else:
            type.type("You cup your hands outside the window and try to catch some. ")
            type.type("Most of it runs down your arms. You drink what you can. Mostly just arm sweat.")
            print("\n")

    def fire_starter_campfire(self):
        """Fire starter kit enables campfire events"""
        type.type("The evening air is cold. The kind of cold that gets into your bones.")
        print("\n")
        if self.has_item("Fire Starter Kit"):
            type.type("You pull out your " + cyan(bright("Fire Starter Kit")) + " and gather some sticks.")
            print("\n")
            type.type("The tinder catches immediately. Within minutes, you have a proper campfire going.")
            print("\n")
            type.type("You sit by the flames, watching them dance. The warmth seeps into your hands, your face, your chest.")
            print("\n")
            companions = self.get_all_companions()
            alive = [n for n, d in companions.items() if d["status"] == "alive"]
            if len(alive) > 0:
                companion = random.choice(alive)
                type.type(cyan(bright(companion)) + " curls up next to you by the fire. The glow reflects in their eyes.")
                print("\n")
                self.pet_companion(companion)
            type.type("For a moment, just a moment, everything is okay.")
            self.heal(5)
            self.restore_sanity(5)
            print("\n")
        else:
            type.type("You try rubbing two sticks together. Nothing. You blow on them. Nothing. ")
            type.type("You watch survival videos in your head. None of them help.")
            print("\n")
            type.type("You pull the blanket tighter and shiver through the night.")
            self.lose_sanity(2)
            print("\n")

    def worry_stone_moment(self):
        """Worry stone provides a brief sanity moment"""
        if self.has_item("Worry Stone"):
            moments = [
                "Your thumb finds the " + cyan(bright("Worry Stone")) + " in your pocket without thinking. Smooth. Warm. The anxiety retreats, just a little.",
                "You're spiraling. Brain going a hundred miles an hour. Your hand closes around the " + cyan(bright("Worry Stone")) + ". You rub your thumb across it. Breathe. You're okay.",
                "The " + cyan(bright("Worry Stone")) + " is wearing thin where your thumb meets it. A groove, shaped by a thousand anxious moments. It's become part of you.",
                "Someone says something that sets you off. Your heart races. Your hand reaches for the " + cyan(bright("Worry Stone")) + ". The warmth grounds you. You stay calm.",
                "In the middle of the night, you can't sleep. You reach for the " + cyan(bright("Worry Stone")) + " and just... hold it. The weight in your palm says: you exist. You're here. That's enough.",
            ]
            type.type(random.choice(moments))
            self.restore_sanity(random.choice([2, 3]))
            print("\n")
        else:
            type.type("The anxiety hits you like a wave. No warning. No trigger. Just... dread.")
            print("\n")
            type.type("You grip the steering wheel until your knuckles turn white. It passes. Eventually. It always passes.")
            self.lose_sanity(random.choice([1, 2]))
            print("\n")

    def snare_trap_catch(self):
        """Snare trap catches something during an adventure"""
        if self.has_item("Snare Trap"):
            type.type("You set up your " + cyan(bright("Snare Trap")) + " near a rabbit trail earlier today.")
        else:
            type.type("You notice animal tracks in the mud near your car.")
        print("\n")
        if self.has_item("Snare Trap"):
            catch = random.randrange(4)
            if catch == 0:
                type.type("When you check it, there's a rabbit in the snare, looking at you with big, terrified eyes.")
                print("\n")
                type.type("1. Take the rabbit (food)")
                print()
                type.type("2. Free the rabbit")
                print()
                type.type("Choose: ")
                choice = None
                while choice is None:
                    try:
                        choice = int(input())
                    except ValueError:
                        type.type("Pick a number: ")
                print()
                if choice == 1:
                    type.type("You take the rabbit. It's not pleasant, but you're hungry. ")
                    type.type("Rabbit stew over a small fire. Protein.")
                    self.heal(15)
                    print("\n")
                else:
                    type.type("You open the snare. The rabbit bolts into the underbrush without looking back.")
                    print("\n")
                    type.type("You feel... good about that. Some things matter more than food.")
                    self.restore_sanity(3)
                    print("\n")
            elif catch == 1:
                type.type("Something took the bait and shredded the trap. Big animal tracks lead away from the wreck.")
                print("\n")
                type.type("Whatever it was, it's bigger than you want to deal with. You quietly pack up.")
                self.lose_sanity(1)
                print("\n")
            elif catch == 2:
                type.type("The trap caught... a shoe. Someone's old, muddy sneaker. ")
                type.type("Not exactly dinner. But you did technically trap something.")
                print("\n")
            else:
                type.type("The trap is empty but disturbed. Something investigated it and was smart enough to avoid it.")
                print("\n")
                type.type("You're either dealing with a genius squirrel or something that's been hunted before.")
                print("\n")
        else:
            type.type("The tracks lead into the woods. You don't follow them. You don't have the tools.")
            print("\n")

    def binocular_scope_discovery(self):
        """Binocular scope reveals something in the distance"""
        type.type("Something catches your eye on the horizon. A glint. A movement.")
        print("\n")
        if self.has_item("Binocular Scope"):
            type.type("You flip down the " + cyan(bright("Binocular Scope")) + " mounted on your visor and zoom in.")
            print("\n")
            discovery_roll = random.randrange(5)
            if discovery_roll == 0:
                reward = random.randint(10, 40)
                type.type("You spot a " + green("yard sale") + " two blocks away. Among the junk: something shiny.")
                print("\n")
                type.type("You drive over and score " + green("${:,}".format(reward)) + " worth of useful stuff.")
                self.change_balance(reward)
            elif discovery_roll == 1:
                type.type("You see a " + red("suspicious van") + " casing the parking lot. Time to move your car.")
                print("\n")
                type.type("You quietly start your engine and leave before they notice you. Crisis averted.")
                self.restore_sanity(2)
            elif discovery_roll == 2:
                type.type("You notice a " + yellow("hidden trail") + " behind the gas station that leads into the woods. Could be an adventure.")
                print("\n")
                type.type("Just watching the world from a distance, safely. It's oddly therapeutic.")
                self.restore_sanity(3)
            elif discovery_roll == 3:
                type.type("You spot " + cyan("someone in trouble") + " — a person waving for help on the roadside.")
                print("\n")
                type.type("1. Drive over and help")
                print()
                type.type("2. Mind your own business")
                print()
                type.type("Choose: ")
                choice = input().strip()
                print()
                if choice == "1":
                    reward = random.randint(10, 30)
                    type.type("You pull up. They had a flat tire. You help them change it.")
                    print("\n")
                    type.type("They thank you profusely and hand you " + green("${:,}".format(reward)) + ".")
                    self.change_balance(reward)
                    self.restore_sanity(3)
                else:
                    type.type("You drive the other way. Not your problem.")
            else:
                type.type("You see " + magenta("a stray cat") + " stalking a bird in the field. Nature documentary, live.")
                print("\n")
                type.type("Just watching the world from a distance, safely. It's oddly therapeutic.")
                self.restore_sanity(2)
            print("\n")
        else:
            type.type("You squint. You can't make it out. It's too far. ")
            type.type("Could be something. Could be nothing. You'll never know.")
            print("\n")

    def emergency_blanket_cold_night(self):
        """Emergency blanket helps during cold weather"""
        type.type("Tonight is brutally cold. You can see your breath inside the car.")
        print("\n")
        if self.has_item("Emergency Blanket"):
            type.type("You pull the " + cyan(bright("Emergency Blanket")) + " over yourself. ")
            type.type("It crinkles like a bag of chips, but God is it warm. ")
            type.type("The duct tape insulation traps your body heat like a cocoon.")
            print("\n")
            type.type("You sleep well. Better than well. You sleep like you have a home.")
            self.restore_sanity(3)
            self.heal(3)
            print("\n")
        else:
            type.type("You curl into a ball on the back seat, pulling your jacket over your head. ")
            type.type("Every exhale fogs the windows. Your hands go numb. Your toes go numb.")
            print("\n")
            type.type("Morning can't come soon enough.")
            self.hurt(random.choice([3, 5]))
            self.lose_sanity(2)
            print("\n")

    def lucky_charm_streak(self):
        """Lucky Charm Bracelet gives you a lucky day"""
        if self.has_item("Lucky Charm Bracelet"):
            type.type("You glance at the " + cyan(bright("Lucky Charm Bracelet")) + " on your wrist. The penny catches the light.")
            print("\n")
            reward = random.randint(5, 20)
            lucky_roll = random.randrange(5)
            if lucky_roll == 0:
                type.type("You find " + green("${:,}".format(reward)) + " in the pocket of a jacket you haven't worn in weeks.")
                self.change_balance(reward)
            elif lucky_roll == 1:
                type.type("A stranger bumps into you and apologizes by buying you coffee. Free coffee is the best coffee.")
            elif lucky_roll == 2:
                type.type("Every traffic light you hit is green. EVERY. SINGLE. ONE.")
            elif lucky_roll == 3:
                type.type("You step on a scratch-off someone threw away. It's worth " + green("${:,}".format(reward)) + ". Literally found money.")
                self.change_balance(reward)
            else:
                type.type("A bird poops on your car instead of on you. Small victories.")
            self.restore_sanity(1)
            print("\n")
        else:
            type.type("Today feels unlucky. Not bad-luck unlucky. Just... meh-luck. The kind of day where nothing goes right, but nothing goes catastrophically wrong either.")
            print("\n")

    def water_purifier_use(self):
        """Water purifier provides clean water from dirty sources"""
        type.type("You're parched. The nearest store is miles away, but there's a creek nearby.")
        print("\n")
        if self.has_item("Water Purifier"):
            type.type("You scoop creek water into your " + cyan(bright("Water Purifier")) + " and let the sun do its work.")
            print("\n")
            type.type("Thirty minutes later: clean, drinkable water. You drink deeply.")
            print("\n")
            type.type("Science. Saving lives since forever.")
            self.heal(8)
            self.restore_sanity(1)
            print("\n")
        else:
            type.type("You stare at the murky water. You're thirsty, but not that thirsty. ")
            type.type("You drive to the store instead and buy a water bottle for $3.")
            if self._balance >= 3:
                self.change_balance(-3)
            print("\n")

    def home_remedy_illness(self):
        """Home Remedy cures illness or injury"""
        type.type("You wake up feeling awful. Head pounding. Body aching. Something's wrong.")
        print("\n")
        if self.has_item("Home Remedy"):
            type.type("You reach for the " + cyan(bright("Home Remedy")) + " you made. ")
            type.type("A mix of first aid supplies and cough drops — not exactly FDA approved, but it works.")
            print("\n")
            type.type("You dose yourself and lie back down. Within an hour, the worst of it passes.")
            print("\n")
            type.type("Not medicine. But close enough when you're living out of a car.")
            self.heal(15)
            self.restore_sanity(2)
            print("\n")
        elif self.has_item("Wound Salve"):
            type.type("You slather some " + cyan(bright("Wound Salve")) + " on the worst of it. ")
            type.type("It stings. But the throbbing fades.")
            self.heal(8)
            print("\n")
        elif self.has_item("Smelling Salts"):
            type.type("You crack the " + cyan(bright("Smelling Salts")) + " under your nose. ")
            type.type("WHOA. Your eyes snap open. Your brain boots up like a computer. ")
            type.type("You're not healed, but you're AWAKE.")
            self.restore_sanity(5)
            print("\n")
        else:
            type.type("You have nothing. No medicine. No remedy. No relief.")
            print("\n")
            type.type("You tough it out. You always tough it out. That's all you can do.")
            self.hurt(random.choice([5, 8, 10]))
            self.lose_sanity(3)
            print("\n")

    def road_flare_torch_encounter(self):
        """Using the Road Flare Torch to scare off a threat at night"""
        type.type("Something large is moving near your car in the dark. Heavy breathing. Branches snapping.")
        print("\n")
        if self.has_item("Road Flare Torch"):
            type.type("You light the " + cyan(bright("Road Flare Torch")) + ". ")
            type.type("Red light floods the darkness, turning the world into a scene from a horror movie.")
            print("\n")
            type.type("But the horror is for whatever's out there. The creature — bear? dog? person? — ")
            type.type("recoils from the flame and crashes away through the brush.")
            print("\n")
            type.type("You hold the torch high until the sounds disappear. Your heart hammers. But you're safe.")
            self.restore_sanity(2)
            print("\n")
        elif self.has_item("Flashlight"):
            type.type("You click on your " + magenta(bright("Flashlight")) + " and sweep the beam around.")
            print("\n")
            type.type("Two eyes reflect back at you from the treeline. Then they blink and vanish.")
            print("\n")
            type.type("You don't sleep great after that.")
            self.lose_sanity(1)
            print("\n")
        else:
            type.type("You freeze. Every sound is amplified. Every shadow is alive.")
            print("\n")
            type.type("Eventually, the sounds fade. Whatever it was, it moved on. This time.")
            self.lose_sanity(random.choice([3, 4, 5]))
            print("\n")

    def splint_injury_event(self):
        """Splint prevents further damage from an injury"""
        type.type("You trip on a cracked sidewalk and land hard. Pain shoots through your ankle.")
        print("\n")
        if self.has_item("Splint"):
            type.type("You reach for the " + cyan(bright("Splint")) + " you crafted. ")
            type.type("Duct tape and rope — ugly, but functional.")
            print("\n")
            type.type("You wrap your ankle tight. It hurts, but you can walk. The support holds.")
            print("\n")
            type.type("Not a hospital. Not a doctor. But good enough.")
            self.hurt(3)
            print("\n")
        else:
            type.type("You try to stand. The ankle screams. You stumble and catch yourself on a wall.")
            print("\n")
            type.type("No splint. No brace. Nothing. You limp for the rest of the day.")
            self.hurt(random.choice([8, 10, 12]))
            self.add_fatigue(3)
            print("\n")

    # ==========================================
    # CHAIN 1: THE HERMIT'S TRAIL (5 events)
    # Worn Map → find hermit camp → Journal → 
    # Walking Stick → Herbal Pouch → Hollow Tree Stash
    # ==========================================

    def herbal_pouch_remedy(self):
        """Herbal Pouch provides healing during illness"""
        if not self.has_item("Herbal Pouch"):
            self.day_event()
            return
        
        type.type("You're feeling off today. Headache. Nausea. The usual.")
        print("\n")
        type.type("You open the " + cyan(bright("Herbal Pouch")) + " and brew a quick tea from the dried herbs.")
        print("\n")
        teas = [
            "Chamomile tea. The steam rises and you breathe it in. The headache fades like fog in sunlight.",
            "Willow bark tea. Bitter as regret, but effective. The pain recedes within minutes.",
            "Mint and plantain leaf tea. It tastes like a garden and settles your stomach immediately.",
            "A blend of everything in the pouch. You have no idea what it is. But it works. That's enough.",
        ]
        type.type(random.choice(teas))
        self.heal(random.choice([8, 10, 12]))
        self.restore_sanity(2)
        print("\n")

    def walking_stick_hike(self):
        """Carved Walking Stick makes exploration events better"""
        if not self.has_item("Carved Walking Stick"):
            self.day_event()
            return
        
        type.type("You take a walk with the " + cyan(bright("Carved Walking Stick")) + ". ")
        type.type("Your pace is steady. Your grip is sure. The notches press against your palm.")
        print("\n")
        
        hike_events = [
            ("You climb a hill you'd never have attempted without the stick. At the top: a view of the whole valley. Worth every step.",
             5, 0),
            ("A loose trail gives way under your foot. The stick catches you, jams into the dirt, holds you upright. " +
             "Without it, you'd have twisted an ankle.",
             3, 5),
            ("You use the stick to ford a shallow creek. On the other side: blackberry bushes, heavy with fruit. Free food.",
             4, 8),
            ("An aggressive stray dog blocks the trail. You plant the stick and stand tall. The dog backs off. " +
             "Confidence is a weapon.",
             4, 0),
            ("You walk for two hours. No destination. Just walking. The stick marks a rhythm. Step, tap, step, tap. " +
             "Meditation with your legs.",
             6, 0),
        ]
        
        event = random.choice(hike_events)
        type.type(event[0])
        self.restore_sanity(event[1])
        if event[2] > 0:
            self.heal(event[2])
        print("\n")

    def tinfoil_hat_event(self):
        """Tinfoil Hat from Radio Nowhere — weird protection"""
        if not self.has_item("Tinfoil Hat"):
            self.day_event()
            return
        
        type.type("You put on the " + cyan(bright("Tinfoil Hat")) + ". Just for a minute. Nobody's watching.")
        print("\n")
        
        hat_events = [
            "Immediately, the intrusive thoughts stop. Complete silence. Either the hat works or the placebo effect is incredible. Either way: peace.",
            "A conspiracy theorist on the street corner sees you and gives you a solemn nod. " +
            quote("One of us.") + " You nod back. You've never felt more accepted.",
            "You wear it while tuning the radio. Station 108.7 comes in crystal clear. " +
            "Vera's voice: " + quote("Tinfoil crew, checking in.") + " You laugh. First real laugh in days.",
            "A kid sees you and yells: " + quote("COOL HAT!") + " You give them a thumbs up. They give you one back. " +
            "Adulthood could learn something from kids.",
            "You catch your reflection in the car window. Tinfoil hat. Wrinkled clothes. Five-day stubble. " +
            "And the biggest smile you've worn in weeks. You look ridiculous. You look happy.",
        ]
        type.type(random.choice(hat_events))
        self.restore_sanity(random.choice([3, 4, 5]))
        print("\n")

    def junkyard_crown_moment(self):
        """Junkyard Crown provides dignity moments"""
        if not self.has_item("Junkyard Crown"):
            self.day_event()
            return
        
        type.type("The " + cyan(bright("Junkyard Crown")) + " sits on your dashboard, catching the morning light.")
        print("\n")
        
        crown_events = [
            "A kid at the gas station sees it and gasps. " + quote("ARE YOU A KING?") +
            " You pause. " + quote("Some days.") + " The kid nods like that's the most reasonable answer in the world.",
            "You put it on before walking into the casino. The pit boss gives you a look. " +
            "The dealer gives you a grin. " + quote("Nice crown.") + " You tip your head regally.",
            "Gideon would be proud. You've kept it polished. The gears and springs gleam. " +
            "Every piece of junk in it used to be something else. Just like you.",
            "You hold it in your hands. Feel the weight of it. The brass fittings from a boat. " +
            "The copper wire from a lamp. The springs from a watch. Time. Water. Light. " +
            "All compressed into something that fits on your head.",
        ]
        type.type(random.choice(crown_events))
        self.restore_sanity(random.choice([3, 4, 5]))
        print("\n")

    def reunion_photo_comfort(self):
        """Reunion Photo provides comfort during tough times"""
        if not self.has_item("Reunion Photo"):
            self.day_event()
            return
        
        type.type("You flip down the visor and the " + cyan(bright("Reunion Photo")) + " falls into your lap.")
        print("\n")
        
        photo_events = [
            "Five dogs. One you. Everyone smiling. You remember that day — the block party, the dumplings, " +
            "the blanket. People who didn't have to be kind, choosing to be kind anyway.",
            "Biscuit's little beagle face stares up at you from the photo. That dog loved everyone. " +
            "Even the kid who took them. Maybe especially the kid who took them.",
            "You look at your own face in the photo. Who IS that person? They look... happy. " +
            "You didn't know you could still look like that.",
            "The photo is getting worn at the edges from being handled so much. " +
            "That's okay. That's what photos are for.",
        ]
        type.type(random.choice(photo_events))
        self.restore_sanity(random.choice([3, 4]))
        print("\n")

    def scrap_armor_event(self):
        """If you have Artisan's Toolkit you can make Scrap Armor at the junkyard"""
        if not self.has_item("Artisan's Toolkit"):
            self.day_event()
            return
        if self.has_item("Scrap Armor"):
            self.day_event()
            return
        if self.has_met("Scrap Armor Made"):
            self.day_event()
            return
        
        type.type("You're at the junkyard with the " + cyan(bright("Artisan's Toolkit")) + ". Gideon isn't here today.")
        print("\n")
        type.type("But you know what you're doing now. You eye the scrap pile. Car panels. Steel mesh. Rivets.")
        print("\n")
        type.type("An idea forms. It's stupid. It's brilliant. It's both.")
        print("\n")
        type.type("You spend three hours cutting, bending, and riveting. When you're done, you're holding ")
        type.type("a crude but functional vest made of layered metal strips and mesh.")
        print("\n")
        type.type("It won't stop a bullet. But it'll absorb a punch, deflect a dog bite, keep you warmer than your jacket.")
        print("\n")
        type.type("You made " + cyan(bright("Scrap Armor")) + ". Gideon would be proud.")
        self.add_item("Scrap Armor")
        self.meet("Scrap Armor Made")
        self.restore_sanity(5)
        print("\n")


    # ============================================================
    # ITEM USE EVENTS - events that activate specific held items
    # ============================================================

    def mystery_potion_effect(self):
        """Mystery Potion has a random effect when the player thinks about drinking it"""
        if not self.has_item("Mystery Potion"):
            self.day_event()
            return
        type.type("You dig through your bag and find the " + cyan(bright("Mystery Potion")) + " you've been carrying around.")
        print("\n")
        type.type("It's been staring at you for days. Glowing faintly. Smelling of something you can't identify.")
        print("\n")
        type.type("You decide: today's the day. You open it and drink.")
        print("\n")
        self.use_item("Mystery Potion")
        effect = random.randrange(6)
        if effect == 0:
            type.type("It tastes like childhood. Like the smell of rain on concrete. Like a memory you forgot you had.")
            print("\n")
            type.type("You feel... good. Really good. Restored.")
            self.heal(random.randint(20, 40))
            self.restore_sanity(15)
        elif effect == 1:
            type.type("It tastes like battery acid and regret. Your whole body shudders.")
            print("\n")
            type.type("Then, after five horrible seconds, you feel absolutely fine. Better than fine.")
            self.heal(random.randint(10, 25))
        elif effect == 2:
            amount = random.randint(50, 300)
            type.type("It tastes like money. Like ambition. Like a promise.")
            print("\n")
            type.type("You find " + green("${:,}".format(amount)) + " in your pocket that wasn't there a minute ago. You don't question it.")
            self.change_balance(amount)
            self.restore_sanity(5)
        elif effect == 3:
            type.type("It tastes... completely normal. Like water. Like literally nothing.")
            print("\n")
            type.type("Maybe it was just water. Maybe that's fine. You're hydrated.")
            self.heal(5)
        elif effect == 4:
            type.type("It tastes incredible. Like the best meal you've ever had, compressed into a single swallow.")
            print("\n")
            type.type("Your fatigue vanishes. Your aches vanish. Whatever was in that bottle, it WORKED.")
            self.heal(random.randint(15, 30))
            self.reduce_fatigue(random.randint(15, 30))
        else:
            type.type("It tastes like nothing. Then it hits you. Your vision blurs. The world tilts.")
            print("\n")
            type.type("You wake up an hour later, $" + str(random.randint(20, 80)) + " richer and with no memory of what happened.")
            type.type(" The potion works in mysterious ways.")
            self.change_balance(random.randint(20, 80))
            self.restore_sanity(3)
        print("\n")

    def love_potion_use(self):
        """Love Potion creates a positive NPC encounter"""
        if not self.has_item("Love Potion"):
            self.day_event()
            return
        type.type("You've been carrying the " + cyan(bright("Love Potion")) + " long enough. Today feels like the day.")
        print("\n")
        type.type("You find a coffee shop. You order two coffees. You add a single drop to one.")
        print("\n")
        self.use_item("Love Potion")
        outcome = random.randrange(4)
        if outcome == 0:
            type.type("The barista tries your coffee by accident. They look at you with sudden warmth.")
            print("\n")
            type.type(quote("This is on the house. And hey — come back anytime."))
            print("\n")
            type.type("Free coffee. A new friend, maybe. The swamp witch knows her stuff.")
            self.restore_sanity(10)
            self.change_balance(random.randint(50, 150))
        elif outcome == 1:
            type.type("You meet someone at the counter. Eyes meet. A conversation starts that shouldn't end.")
            print("\n")
            type.type("You talk for three hours. You miss two events you were planning. Worth it.")
            self.restore_sanity(20)
        elif outcome == 2:
            type.type("Nothing happens. The potion might have been a placebo. Or maybe the magic needs more faith.")
            print("\n")
            type.type("You get a normal coffee. A normal day. Sometimes normal is what you needed.")
            self.restore_sanity(5)
        else:
            type.type("Someone spills their coffee on you. They apologize profusely, buy you a replacement, and then invite you to dinner to make up for it.")
            print("\n")
            type.type("The love potion, it turns out, works best through chaos.")
            self.restore_sanity(15)
            self.change_balance(random.randint(20, 80))
        print("\n")

    def feelgood_bottle_moment(self):
        """Feelgood Bottle restores sanity and gives a mood boost"""
        if not self.has_item("Feelgood Bottle"):
            self.day_event()
            return
        type.type("You reach for the " + cyan(bright("Feelgood Bottle")) + " in your glove compartment.")
        print("\n")
        type.type("The label says nothing. The liquid inside looks like afternoon light through amber glass.")
        print("\n")
        type.type("You take a sip. It tastes like the last day of summer. Like a song you loved at seventeen.")
        print("\n")
        self.use_item("Feelgood Bottle")
        self.restore_sanity(random.randint(15, 25))
        self.heal(random.randint(5, 15))
        self.reduce_fatigue(10)
        type.type("Whatever was in that bottle — it was exactly what you needed. Everything feels lighter.")
        print("\n")
        type.type("Not solved. Not fixed. Just... lighter.")
        print("\n")

    def persistent_bottle_refill(self):
        """Persistent Bottle provides clean water repeatedly"""
        if not self.has_item("Persistent Bottle"):
            self.day_event()
            return
        type.type("You're thirsty. Parched. You reach into the backseat for the " + cyan(bright("Persistent Bottle")) + ".")
        print("\n")
        type.type("You remember finding this at the bottom of the fountain. It was bone-dry then.")
        print("\n")
        type.type("It's full now. It's always full. You've stopped questioning it.")
        print("\n")
        type.type("You drink deeply. Cool, clean water. Perfect.")
        self.heal(5)
        self.restore_sanity(3)
        self.reduce_fatigue(5)
        print("\n")

    def silver_horseshoe_luck(self):
        """Silver Horseshoe gives a lucky break"""
        if not self.has_item("Silver Horseshoe"):
            self.day_event()
            return
        type.type("You glance at the " + cyan(bright("Silver Horseshoe")) + " hanging from your rearview mirror.")
        print("\n")
        type.type("It catches the light. Old. Worn. Heavy with years.")
        print("\n")
        type.type(quote("Luckier than anything you'll find in a casino.") + " That's what Jameson said.")
        print("\n")
        outcome = random.randrange(4)
        if outcome == 0:
            amount = random.randint(50, 200)
            type.type("You glance down and see a folded bill on the sidewalk. Then another. Then another.")
            print("\n")
            type.type("You count " + green("${:,}".format(amount)) + " total. Today, the horseshoe delivers.")
            self.change_balance(amount)
        elif outcome == 1:
            type.type("Your car starts first try. The traffic parts ahead of you. Every light is green.")
            print("\n")
            type.type("Nothing remarkable. Nothing terrible. Just a perfect, frictionless day. The horseshoe at work.")
            self.restore_sanity(8)
        elif outcome == 2:
            type.type("You're about to pull into a parking spot when a car cuts you off. You honk.")
            print("\n")
            type.type("Then you notice: the spot they took has a citation on the meter. Your luck held.")
            self.restore_sanity(5)
            self.change_balance(random.randint(10, 40))
        else:
            type.type("You find a scratch-off on the ground. Win it all back and then some: " + green("${:,}".format(random.randint(20, 100))) + ".")
            self.change_balance(random.randint(20, 100))
        print("\n")

    def road_talisman_protection(self):
        """Road Talisman keeps you safe on the road"""
        if not self.has_item("Road Talisman"):
            self.day_event()
            return
        type.type("Something feels wrong today. You can't name it. A weight. A tremor in the air.")
        print("\n")
        type.type("Your hand moves to the " + cyan(bright("Road Talisman")) + " hanging from the mirror. Warm to the touch.")
        print("\n")
        outcome = random.randrange(3)
        if outcome == 0:
            type.type("A truck runs a red light right where you would have been. But you'd stopped to adjust the talisman.")
            print("\n")
            type.type("The truck blows past at sixty miles an hour. Three feet in front of you.")
            print("\n")
            type.type("You sit there, shaking. The talisman is cool now.")
            self.restore_sanity(5)
        elif outcome == 1:
            type.type("You get a flat tire. Annoying. But you'd packed your kit this morning, guided by some instinct.")
            print("\n")
            type.type("Twenty minutes later, you're rolling again. The talisman glows, faintly, in approval.")
            self.restore_sanity(3)
        else:
            type.type("Nothing bad happens today. Nothing at all.")
            print("\n")
            type.type("You drive for hours without incident. Clean roads. Good weather. A kind stranger waves you into traffic.")
            print("\n")
            type.type("Maybe the talisman works by preventing the invisible troubles. The ones you never see coming.")
            self.restore_sanity(8)
            self.heal(5)
        print("\n")

    def ritual_token_ceremony(self):
        """Ritual Token provides a mystical benefit"""
        if not self.has_item("Ritual Token"):
            self.day_event()
            return
        if self.has_met("Ritual Token Used"):
            self.day_event()
            return
        self.meet("Ritual Token Used")
        type.type("You've been carrying the " + cyan(bright("Ritual Token")) + " for a while. Small. Carved wood.")
        print("\n")
        type.type("The shaman who gave it to you said: " + quote("Use it when the need is greatest. Only once."))
        print("\n")
        type.type("You're not sure this is the greatest need. But then again — when would be?")
        print("\n")
        answer = ask.yes_or_no("Use the Ritual Token? ")
        if answer == "yes":
            self.use_item("Ritual Token")
            type.type("You hold the token and close your eyes. You think about where you've been.")
            print("\n")
            type.type("You think about where you're going.")
            print("\n")
            type.slow("...")
            print("\n")
            ritual_gift = random.randrange(4)
            if ritual_gift == 0:
                amount = random.randint(200, 800)
                type.type("When you open your eyes, there's an envelope under your wiper blade. Cash inside: " + green("${:,}".format(amount)) + ".")
                print("\n")
                type.type("No explanation. The shaman said 'the need.' The road provides.")
                self.change_balance(amount)
            elif ritual_gift == 1:
                type.type("The world feels clear. Sharp. Like a fog has lifted.")
                print("\n")
                type.type("Your body aches less. Your mind races less. Everything is quiet.")
                self.heal(30)
                self.restore_sanity(20)
            elif ritual_gift == 2:
                type.type("A warmth spreads from your chest outward. You feel protected. Guided.")
                print("\n")
                type.type("For the next few days, nothing bad will find you. The shaman's word.")
                self.add_status("Ritual Protection")
            else:
                type.type("You feel... connected. To the road. To everyone on it.")
                print("\n")
                type.type("The token crumbles to dust in your hand. But something remains in your chest.")
                self.restore_sanity(25)
                self.heal(20)
                self.change_balance(random.randint(100, 400))
            print("\n")
        else:
            type.type("Not yet. You put the token back. The road will tell you when.")
            print("\n")

    def council_feather_blessing(self):
        """Council Feather brings a mystical blessing"""
        if not self.has_item("Council Feather"):
            self.day_event()
            return
        if self.has_met("Council Feather Blessed"):
            self.day_event()
            return
        self.meet("Council Feather Blessed")
        type.type("The " + cyan(bright("Council Feather")) + " in your rearview mirror sways though the windows are closed.")
        print("\n")
        type.type("It's jet-black with an oily sheen. A crow gave it to you. Not many people get crow gifts.")
        print("\n")
        type.type("You feel a presence at the edge of things. Watching. Not threatening. Curious.")
        print("\n")
        type.type("The day unfolds differently. Like something cleared a path for you.")
        self.restore_sanity(12)
        self.heal(10)
        amount = random.randint(50, 250)
        type.type("You find " + green("${:,}".format(amount)) + " in a parking lot. The crow was right: you're favored today.")
        self.change_balance(amount)
        print("\n")

    def cowboy_jacket_encounter(self):
        """Cowboy Jacket makes NPCs more respectful"""
        if not self.has_item("Cowboy Jacket"):
            self.day_event()
            return
        type.type("You pull on the " + cyan(bright("Cowboy Jacket")) + " before heading out today. Old leather. Horse smell. Character.")
        print("\n")
        type.type("People look at you differently. Not rich-differently. Not dangerous-differently.")
        print("\n")
        type.type("Dependable-differently. Like you're someone who keeps their word.")
        print("\n")
        outcome = random.randrange(3)
        if outcome == 0:
            type.type("A man at the diner insists on buying your coffee.")
            print("\n")
            type.type(quote("My grandfather had a jacket like that. Good man. Figured you might be too."))
            self.restore_sanity(8)
            self.change_balance(random.randint(5, 20))
        elif outcome == 1:
            type.type("You get waved to the front of a long line at the car wash.")
            print("\n")
            type.type(quote("Nice jacket. Go ahead, friend."))
            print("\n")
            type.type("A small kindness. The jacket earns it.")
            self.restore_sanity(5)
        else:
            type.type("A mechanic charges you half price on an oil check, talking the whole time about his ranch days.")
            print("\n")
            type.type("The jacket speaks before you do. It says: " + quote("This one's good people."))
            self.change_balance(random.randint(30, 80))
            self.restore_sanity(5)
        print("\n")

    def found_phone_call(self):
        """Found Phone lets you make an anonymous call"""
        if not self.has_item("Found Phone"):
            self.day_event()
            return
        if self.has_met("Found Phone Used"):
            self.day_event()
            return
        self.meet("Found Phone Used")
        type.type("You still have the " + cyan(bright("Found Phone")) + " you picked up. Battery's dying.")
        print("\n")
        type.type("There are unread messages. Family stuff. People who love whoever had this phone.")
        print("\n")
        type.type("You scroll to the emergency contact. A name: 'Mom'.")
        print("\n")
        answer = ask.yes_or_no("Call them? Tell them you found the phone? ")
        if answer == "yes":
            type.type("The phone rings. A woman answers, voice tight with worry.")
            print("\n")
            type.type(quote("Hello? Who is this? Do you have—"))
            print("\n")
            type.type("You explain. The relief in her voice is immediate. Overwhelming.")
            print("\n")
            type.type(quote("Oh thank God. THANK GOD. He's been missing for two days. Where did you find it?"))
            print("\n")
            type.type("You tell her. She cries. You almost cry. It's a lot.")
            print("\n")
            type.type("She offers to mail you a reward. You give her a P.O. box. Two weeks later, an envelope appears.")
            self.change_balance(random.randint(100, 500))
            self.restore_sanity(20)
            self.use_item("Found Phone")
        else:
            type.type("You can't bring yourself to do it. You put the phone back.")
            print("\n")
            type.type("Maybe tomorrow. Maybe when you find the right words.")
        print("\n")

    def alien_crystal_event(self):
        """Alien Crystal has a surreal effect"""
        if not self.has_item("Alien Crystal"):
            self.day_event()
            return
        type.type("The " + cyan(bright("Alien Crystal")) + " is glowing. It wasn't glowing yesterday.")
        print("\n")
        type.type("It pulses softly — blue-white, like a star seen through water.")
        print("\n")
        outcome = random.randrange(4)
        if outcome == 0:
            type.type("You hold it up to the light. The world inverts. For one second, everything is the negative image of itself.")
            print("\n")
            type.type("When it snaps back, there's a " + green("${:,}".format(random.randint(100, 500))) + " on the seat beside you.")
            print("\n")
            type.type("You stare at it for a long time. Then you pocket it.")
            self.change_balance(random.randint(100, 500))
            self.restore_sanity(5)
        elif outcome == 1:
            type.type("The crystal vibrates in your hand. A sound — not a sound, more like a feeling of sound — fills the car.")
            print("\n")
            type.type("You wake up. Your body feels fixed. Like it was taken apart and reassembled correctly, finally.")
            self.heal(30)
            self.restore_sanity(10)
        elif outcome == 2:
            type.type("You dream of a vast emptiness, and a voice in it that says: " + quote("You are doing fine."))
            print("\n")
            type.type("It doesn't feel like a dream. It feels like information.")
            self.restore_sanity(20)
            self.reduce_fatigue(20)
        else:
            type.type("The crystal goes dark. Then it shatters silently, leaving no shards. Just gone.")
            print("\n")
            type.type("In your pocket: a folded note. " + quote("You have been acknowledged. Continue."))
            print("\n")
            type.type("You don't know what it means. But it makes you feel less alone.")
            self.use_item("Alien Crystal")
            self.restore_sanity(15)
            self.heal(15)
        print("\n")

    def dimensional_coin_flip(self):
        """Dimensional Coin has unusual flip outcomes"""
        if not self.has_item("Dimensional Coin"):
            self.day_event()
            return
        type.type("You're at a crossroads — literal and figurative. You pull out the " + cyan(bright("Dimensional Coin")) + ".")
        print("\n")
        type.type("This coin doesn't have heads or tails. Both sides are identical. Featureless silver.")
        print("\n")
        type.type("You flip it anyway.")
        print("\n")
        result = random.randrange(3)
        if result == 0:
            type.type("It lands standing on its edge. Perfectly. Impossibly.")
            print("\n")
            type.type("You choose neither path. You find a third option you hadn't considered.")
            print("\n")
            type.type("The third option leads to " + green("${:,}".format(random.randint(200, 800))) + ".")
            self.change_balance(random.randint(200, 800))
            self.restore_sanity(10)
        elif result == 1:
            type.type("The coin lands heads. Or tails. You can't tell the difference, which somehow helps you make the decision.")
            print("\n")
            type.type("The right one. You knew it all along. The coin just confirmed it.")
            self.restore_sanity(12)
            self.heal(8)
        else:
            type.type("The coin vanishes mid-flip. Just gone.")
            print("\n")
            type.type("You search everywhere. Nothing. But you feel lucky, inexplicably, for the rest of the day.")
            self.use_item("Dimensional Coin")
            self.restore_sanity(8)
            self.change_balance(random.randint(50, 200))
        print("\n")

    def radio_numbers_broadcast(self):
        """Radio Numbers leads to a mysterious find"""
        if not self.has_item("Radio Numbers"):
            self.day_event()
            return
        if self.has_met("Radio Numbers Decoded"):
            self.day_event()
            return
        self.meet("Radio Numbers Decoded")
        type.type("You've been carrying the " + cyan(bright("Radio Numbers")) + " for days. Numbers. Coordinates. Something.")
        print("\n")
        if self.has_item("Radio Logbook"):
            type.type("You cross-reference with the " + cyan(bright("Radio Logbook")) + " you recovered. The patterns match.")
            print("\n")
            type.type("This isn't random. These numbers are a cipher for GPS coordinates.")
            print("\n")
        else:
            type.type("Today, on a whim, you punch the numbers into your phone as GPS coordinates.")
            print("\n")
        type.type("It takes you to an empty field thirty minutes away.")
        print("\n")
        type.type("You almost leave. Then you notice: a rusted box half-buried at the coordinates.")
        print("\n")
        found = random.randrange(3)
        # Having the logbook gives a cash bonus
        logbook_bonus = 500 if self.has_item("Radio Logbook") else 0
        if found == 0:
            amount = random.randint(500, 2000) + logbook_bonus
            type.type("Inside the box: cash. Old bills, rubber-banded in stacks. " + green("${:,}".format(amount)) + " total.")
            print("\n")
            type.type("Someone buried this and never came back. Their loss. Your gain.")
            self.change_balance(amount)
        elif found == 1:
            type.type("Inside: a journal. Someone else's story. Someone who also wandered, also searched, also sat in parking lots eating gas station food.")
            print("\n")
            type.type("Reading their words, you feel less alone in the universe.")
            self.restore_sanity(25)
            if logbook_bonus:
                type.type("The logbook fills in gaps in their story. A fuller picture. A completed life.")
                self.restore_sanity(10)
            print("\n")
        else:
            type.type("Inside: a map. More numbers. Another coordinate. You pocket it.")
            print("\n")
            type.type("Maybe this goes somewhere better. Maybe it's a game. Maybe it's a life.")
            self.add_item("Vision Map")
            self.restore_sanity(10)
            if logbook_bonus:
                self.change_balance(logbook_bonus)
        print("\n")

    def mysterious_envelope_reveal(self):
        """Mysterious Envelope reveals its contents"""
        if not self.has_item("Mysterious Envelope"):
            self.day_event()
            return
        if self.has_met("Envelope Opened"):
            self.day_event()
            return
        self.meet("Envelope Opened")
        type.type("The " + cyan(bright("Mysterious Envelope")) + " has been unopened in your glovebox for days.")
        print("\n")
        type.type("You've been afraid to open it. Or maybe just saving it. Today: you open it.")
        print("\n")
        contents = random.randrange(4)
        self.use_item("Mysterious Envelope")
        if contents == 0:
            amount = random.randint(200, 1000)
            type.type("Inside: a cashier's check made out to " + quote("Bearer") + " for " + green("${:,}".format(amount)) + ".")
            print("\n")
            type.type("You stare at it. Valid. Signed. Yours.")
            self.change_balance(amount)
            self.restore_sanity(10)
        elif contents == 1:
            type.type("Inside: a note. In handwriting you don't recognize.")
            print("\n")
            type.type(quote("You've been chosen. Not randomly. For reasons that will become clear. Keep going."))
            print("\n")
            type.type("That's all. No signature. No return address.")
            self.restore_sanity(15)
        elif contents == 2:
            type.type("Inside: a photograph. A picture of your car. From above. From today.")
            print("\n")
            type.type("You look at the sky. Nothing there. Nothing you can see, anyway.")
            self.restore_sanity(5)
            self.add_status("Being Watched")
        else:
            type.type("Inside: a key. Small, brass, old. And a note: " + quote("Safety deposit box. Bank of the Endless Highway. Ask for Pete."))
            print("\n")
            type.type("You've never heard of that bank. But the key goes in your pocket anyway.")
            self.change_balance(random.randint(50, 300))
            self.restore_sanity(8)
        print("\n")

    def lockbox_contents(self):
        """Lockbox can be opened for its contents"""
        if not self.has_item("Lockbox"):
            self.day_event()
            return
        if self.has_met("Lockbox Opened"):
            self.day_event()
            return
        self.meet("Lockbox Opened")
        type.type("The " + cyan(bright("Lockbox")) + " is still locked. It's been locked since you got it.")
        print("\n")
        if self.has_item("Lockpick Set"):
            type.type("You take out your " + cyan(bright("Lockpick Set")) + ". This is what it was made for.")
            print("\n")
            type.type("Five minutes of careful work. A click. The lid opens.")
            print("\n")
        elif self.has_item("Pocket Knife"):
            type.type("You wedge your " + cyan(bright("Pocket Knife")) + " into the seam and work it until the lock gives.")
            print("\n")
        else:
            type.type("You try every key you have. Nothing. You drive it to a locksmith.")
            print("\n")
            type.type("Twenty dollars and five minutes later, it opens.")
            self.change_balance(-20)
        amount = random.randint(100, 600)
        self.use_item("Lockbox")
        type.type("Inside: " + green("${:,}".format(amount)) + " in cash and a note: " + quote("Good luck, stranger."))
        self.change_balance(amount)
        self.restore_sanity(8)
        print("\n")

    def hollow_tree_stash_find(self):
        """Open the Hollow Tree Stash"""
        if not self.has_item("Hollow Tree Stash"):
            self.day_event()
            return
        if self.has_met("Hollow Tree Opened"):
            self.day_event()
            return
        self.meet("Hollow Tree Opened")
        type.type("You pull over near the woods and dig out the " + cyan(bright("Hollow Tree Stash")) + " you collected.")
        print("\n")
        type.type("A sealed container, hidden in a rotted tree trunk. Someone's cache.")
        print("\n")
        type.type("Emergency supplies. Food, tools, some cash.")
        self.use_item("Hollow Tree Stash")
        amount = random.randint(50, 300)
        self.change_balance(amount)
        self.heal(10)
        type.type("You find " + green("${:,}".format(amount)) + " in small bills, some preserved food, and a matchbook.")
        print("\n")
        type.type("Whoever stashed this never came back. You leave the matchbook out of respect.")
        self.restore_sanity(5)
        print("\n")

    def vision_map_navigate(self):
        """Vision Map leads to a hidden location or shortcut"""
        if not self.has_item("Vision Map"):
            self.day_event()
            return
        if self.has_met("Vision Map Used"):
            self.day_event()
            return
        self.meet("Vision Map Used")
        type.type("You spread the " + cyan(bright("Vision Map")) + " on your steering wheel. It shows roads that aren't on any GPS.")
        print("\n")
        type.type("You follow one. It winds through emptiness, past forgotten places.")
        print("\n")
        type.type("Then it opens into something you didn't expect.")
        print("\n")
        destination = random.randrange(3)
        if destination == 0:
            amount = random.randint(200, 800)
            type.type("An abandoned gas station. Inside, behind the counter: a floor safe. Open. Cash inside.")
            print("\n")
            type.type("The map knew. " + green("${:,}".format(amount)) + " for following the strange road.")
            self.change_balance(amount)
            self.restore_sanity(10)
        elif destination == 1:
            type.type("A clearing with a perfect view of the valley. You didn't know this place existed.")
            print("\n")
            type.type("You sit here for an hour. No noise. No stress. Just the view.")
            self.restore_sanity(20)
            self.heal(15)
            self.reduce_fatigue(20)
        else:
            type.type("A small community of people, off-grid. They're surprised to see you.")
            print("\n")
            type.type("You share a meal. Share stories. Share the road.")
            self.restore_sanity(15)
            self.heal(10)
            self.change_balance(random.randint(50, 200))
        print("\n")

    def secret_route_shortcut(self):
        """Secret Route Map provides a road benefit"""
        if not self.has_item("Secret Route Map"):
            self.day_event()
            return
        if self.has_met("Secret Route Used"):
            self.day_event()
            return
        self.meet("Secret Route Used")
        type.type("You unfold the " + cyan(bright("Secret Route Map")) + " the trucker sold you. Back roads. Shortcuts.")
        print("\n")
        type.type("You follow it. It bypasses three construction zones, two traffic jams, and a weigh station.")
        print("\n")
        type.type("You save two hours. Maybe three. And you find a roadside diner on the route that's not in any app.")
        print("\n")
        type.type("Best pie you've ever had. And the owner tips you off to something worth knowing.")
        amount = random.randint(50, 300)
        type.type("He points you toward an opportunity: " + green("${:,}".format(amount)) + " in it for you.")
        self.change_balance(amount)
        self.restore_sanity(10)
        print("\n")

    def street_cat_ally_benefit(self):
        """Street Cat Ally watches your back"""
        if not self.has_item("Street Cat Ally"):
            self.day_event()
            return
        type.type("The cat from last night is still with you. You've been calling it " + cyan(bright("The Ally")) + ".")
        print("\n")
        type.type("It sits on your dashboard like a hood ornament with opinions.")
        print("\n")
        outcome = random.randrange(3)
        if outcome == 0:
            type.type("It hisses before you open the car door. You pause. A man was lurking nearby, waiting.")
            print("\n")
            type.type("The hiss. The pause. The man moves on. The cat saved you from something.")
            self.restore_sanity(10)
        elif outcome == 1:
            type.type("The cat finds something in the seat cushion you didn't know was there.")
            amount = random.randint(10, 60)
            type.type("Coins. And a crumpled bill. " + green("${:,}".format(amount)) + " total.")
            self.change_balance(amount)
            self.restore_sanity(5)
        else:
            type.type("It curls up on your lap while you drive. Purring.")
            print("\n")
            type.type("You're not a cat person. You're a car person. But this cat understands something about living on the road.")
            self.restore_sanity(12)
        print("\n")

    def old_photograph_memory(self):
        """Old Photograph triggers a memory and sanity effect"""
        if not self.has_item("Old Photograph"):
            self.day_event()
            return
        if self.has_met("Old Photo Remembered"):
            self.day_event()
            return
        self.meet("Old Photo Remembered")
        type.type("The " + cyan(bright("Old Photograph")) + " falls out of your glovebox. You must have forgotten it was there.")
        print("\n")
        type.type("Two people in it. Happy. Somewhere warm.")
        print("\n")
        type.type("You don't know who they are. But they look like the kind of happy you're working toward.")
        print("\n")
        outcome = random.randrange(2)
        if outcome == 0:
            type.type("You tuck it into the visor. Something to look at on the bad days.")
            print("\n")
            type.type("Today, inexplicably, is a good day.")
            self.restore_sanity(15)
        else:
            type.type("You flip it over. On the back, in faded pencil: " + quote("Don't stop."))
            print("\n")
            type.type("You aren't going to.")
            self.restore_sanity(20)
            self.heal(10)
        print("\n")

    def beach_romance_call(self):
        """Beach Romance Number can be called"""
        if not self.has_item("Beach Romance Number"):
            self.day_event()
            return
        if self.has_met("Beach Romance Called"):
            self.day_event()
            return
        self.meet("Beach Romance Called")
        type.type("The " + cyan(bright("Beach Romance Number")) + " has been sitting in your pocket.")
        print("\n")
        type.type("You've almost called it twelve times. Today, you actually dial.")
        print("\n")
        result = random.randrange(3)
        if result == 0:
            type.type("They pick up on the second ring. Remember you immediately.")
            print("\n")
            type.type(quote("I was wondering if you'd ever call."))
            print("\n")
            type.type("You talk for an hour. Maybe two. You feel like a person again. A whole one.")
            self.restore_sanity(25)
            self.change_balance(random.randint(50, 200))
        elif result == 1:
            type.type("Voicemail. A warm voice. You leave a message.")
            print("\n")
            type.type("They never call back. But the message — the act of leaving it — feels right.")
            self.restore_sanity(10)
        else:
            type.type("Number disconnected. You stare at your phone.")
            print("\n")
            type.type("Some things from the beach stay on the beach. You let it go.")
            self.restore_sanity(5)
        self.use_item("Beach Romance Number")
        print("\n")

    def apartment_key_visit(self):
        """Apartment Key can be used to visit/rest"""
        if not self.has_item("Apartment Key"):
            self.day_event()
            return
        if self.has_met("Apartment Visited"):
            self.day_event()
            return
        self.meet("Apartment Visited")
        type.type("You've been driving past this building every day with the " + cyan(bright("Apartment Key")) + " in your pocket.")
        print("\n")
        type.type("Today you stop. You go up. You try the key.")
        print("\n")
        type.type("It works.")
        print("\n")
        type.type("Empty apartment. Clean. Someone left the essentials.")
        print("\n")
        type.type("A shower. A bed. A night off from the car.")
        print("\n")
        type.type("You sleep for twelve hours. You dream of something other than the road.")
        self.heal(25)
        self.restore_sanity(20)
        self.reduce_fatigue(40)
        print("\n")

    def fake_flower_gift(self):
        """Fake Flower can be gifted to cheer someone up"""
        if not self.has_item("Fake Flower"):
            self.day_event()
            return
        if self.has_met("Fake Flower Given"):
            self.day_event()
            return
        self.meet("Fake Flower Given")
        type.type("You're carrying a " + cyan(bright("Fake Flower")) + " that someone made for you. Cloth petals. Wire stem. Perfectly imperfect.")
        print("\n")
        type.type("You see a kid crying on the sidewalk. Lost. Upset. Waiting for someone who's late.")
        print("\n")
        answer = ask.yes_or_no("Give them the flower? ")
        if answer == "yes":
            type.type("You hand it over. The kid stops crying to look at it.")
            print("\n")
            type.type("Then smiles. A real one. The kind that breaks your chest open a little.")
            print("\n")
            type.type("Their parent arrives. Sees you. Mouths: " + quote("thank you."))
            print("\n")
            type.type("You didn't do much. But you did something. That's worth more than you know.")
            self.use_item("Fake Flower")
            self.restore_sanity(20)
        else:
            type.type("You can't give up the only flower you have. You drive on, trying not to think about the crying kid.")
            self.lose_sanity(5)
        print("\n")

    def empty_locket_memory(self):
        """Empty Locket holds a meaningful memory when combined with Old Photograph"""
        if not self.has_item("Empty Locket"):
            self.day_event()
            return
        if self.has_met("Locket Filled"):
            self.day_event()
            return
        if self.has_item("Old Photograph"):
            self.meet("Locket Filled")
            type.type("You hold the " + cyan(bright("Empty Locket")) + " and the " + cyan(bright("Old Photograph")) + " together.")
            print("\n")
            type.type("The photo fits. Perfectly. Like it was always meant to go there.")
            print("\n")
            type.type("You hang the locket from your rearview mirror. Those two strangers, watching over you now.")
            self.use_item("Old Photograph")
            self.use_item("Empty Locket")
            self.add_item("Filled Locket")
            self.restore_sanity(15)
            print("\n")
        else:
            type.type("The " + cyan(bright("Empty Locket")) + " sits in your hand. Small. Waiting.")
            print("\n")
            type.type("It needs something to hold. A picture. A memory. Something to protect.")
            print("\n")
            type.type("You don't have anything to put in it. Not yet. But you will.")
            self.restore_sanity(3)
            print("\n")

    def stack_of_flyers_opportunity(self):
        """Stack of Flyers leads to a money-making opportunity"""
        if not self.has_item("Stack of Flyers"):
            self.day_event()
            return
        if self.has_met("Flyers Distributed"):
            self.day_event()
            return
        self.meet("Flyers Distributed")
        type.type("You have a " + cyan(bright("Stack of Flyers")) + " you picked up. Could use these for something.")
        print("\n")
        type.type("You spend the morning putting them up around town: telephone poles, laundromats, coffee shops.")
        print("\n")
        type.type("By afternoon, your phone has three calls. Two spam. One legitimate.")
        print("\n")
        type.type("A local business wants exactly the kind of help you can offer.")
        self.use_item("Stack of Flyers")
        amount = random.randint(100, 400)
        type.type("Two hours of work. " + green("${:,}".format(amount)) + " in your pocket.")
        self.change_balance(amount)
        self.restore_sanity(8)
        print("\n")

