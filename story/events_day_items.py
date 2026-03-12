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
                type.type("You cook it over a small fire. Fresh fish. Tastes like victory.")
                self.heal(12)
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

