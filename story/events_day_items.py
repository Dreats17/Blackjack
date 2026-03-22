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
        item_count = len(self._inventory) if hasattr(self, '_inventory') else 0
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
        type.type("A man steps out from behind a dumpster, blocking your path like he's been rehearsing this moment for hours. He probably has.")
        print(PAR)
        type.type(quote("Give me your wallet. Now."))
        print(PAR)
        if self.has_item("Shiv"):
            type.type("Your hand drops to your side, finds the " + cyan(bright("Shiv")) + " tucked in your belt. You pull it out slowly. The duct tape handle catches the orange glow of a streetlight. The blade is modest, ugly, and unconditional.")
            print(PAR)
            type.type("The mugger's eyes track the blade. He takes one step back. Then another. His rehearsed speech evaporates.")
            print(PAR)
            type.type(quote("Whoa, whoa, easy. I don't want any trouble, man."))
            print(PAR)
            type.type("He turns and bolts into the alley. You never said a single word. Your hands are shaking — from adrenaline, mostly — but the " + cyan(bright("Shiv")) + " did exactly what it was made to do.")
            self.restore_sanity(2)
            print(PAR)
        elif self.has_item("Pepper Spray"):
            type.type("You whip out the " + cyan(bright("Pepper Spray")) + " and aim it at his face with the conviction of someone who has thought about this moment.")
            print(PAR)
            type.type("PSSSHHHHH!")
            print(PAR)
            type.type("The man screams, both hands clawing at his eyes, stumbling blindly into the wall and then the alley beyond it. You don't stick around to see how it resolves. One use, one save. The " + cyan(bright("Pepper Spray")) + " is spent, but so is he.")
            self.use_item("Pepper Spray")
            self.restore_sanity(3)
            print(PAR)
        else:
            type.type("You've got nothing — no shiv, no spray, no bluff good enough to sell in the dark. He shoves you hard into the dumpster and takes everything in your pockets with the brisk efficiency of a man on a schedule.")
            print(PAR)
            lost = min(random.randint(15, 50), self._balance)
            if lost > 0:
                self.change_balance(-lost)
                type.type("He got " + red("${:,}".format(lost)) + " off you. You stand there in the alley for a minute, listening to his footsteps fade, deciding what to feel.")
            self.lose_sanity(random.choice([3, 4, 5]))
            self.hurt(random.choice([5, 8, 10]))
            print(PAR)

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
        elif self.has_item("Pocket Knife") or self.has_item("Utility Blade") or self.has_item("Master Knife"):
            knife_name = "Pocket Knife" if self.has_item("Pocket Knife") else ("Utility Blade" if self.has_item("Utility Blade") else "Master Knife")
            type.type("You try to pry the lock with your " + magenta(bright(knife_name)) + ".")
            print("\n")
            if random.randrange(3) == 0:
                fallback = random.randint(5, 20)
                type.type("After ten minutes of sweating, the lock snaps. Inside: " + green("${:,}".format(fallback)) + ". Was it worth the effort? Debatable.")
                self.change_balance(fallback)
            else:
                type.type("The blade bends. The lock holds. You almost broke your knife for nothing.")
            evolved = self.track_item_use(knife_name)
            if evolved:
                print("\n")
                type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
            print("\n")
        else:
            type.type("You don't have anything to open it with. You kick it once. Nothing happens. ")
            type.type("You walk away, wondering what was inside. That's going to bother you all day.")
            self.lose_sanity(1)
            print("\n")

    def fishing_day(self):
        """Fishing rod lets you catch food at water sources"""
        type.type("You come across a quiet pond tucked behind an abandoned gas station, like nature reclaiming something that didn't deserve to exist. The water is clear enough that you can see shapes moving through it.")
        print(PAR)
        if self.has_item("Fishing Rod"):
            type.type("You grab your " + cyan(bright("Fishing Rod")) + " from the car and cast a line, then sit on the bank and let the world do whatever it's going to do. The water moves. The clouds move. You, for once, don't have to.")
            print(PAR)
            self.restore_sanity(5)
            catch = random.randrange(5)
            if catch == 0:
                type.type("A tug — a real one, not just the current — and you reel in a decent-sized bass. You hold it up and stare at each other for a moment before you wrap it up and put it on ice. Fresh fish. Actual food that came from the actual world.")
                print(PAR)
                self.add_item("Fish")
            elif catch == 1:
                type.type("You reel in an old boot. Classic. The fishing gods have a sense of humor that never gets old, apparently. At least the casting was nice.")
                print(PAR)
            elif catch == 2:
                bonus = random.randint(5, 25)
                type.type("After an hour, you hook something heavy. You pull and pull and — it's a waterlogged wallet, fat with what turns out to be " + green("${:,}".format(bonus)) + " in mostly intact bills. The fishing gods provide, in their own way.")
                self.change_balance(bonus)
                print(PAR)
            elif catch == 3:
                type.type("You catch a catfish as long as your forearm. You hold it over the water and it looks at you with a face that has no opinions and no regrets, and you decide that's something to admire. You throw it back. You feel genuinely good about that.")
                self.restore_sanity(3)
                print(PAR)
            else:
                type.type("Nothing bites. You sit there for two hours watching the line drift and the clouds change shape, and when you finally reel in, you feel better than you have all week. Doing nothing on purpose is not the same as having nothing to do.")
                print(PAR)
        else:
            type.type("You stare at the water. Fish are literally jumping — breaking the surface in lazy arcs, completely unbothered. You find a stick and try to fashion a makeshift rod. It doesn't work. You're not that kind of resourceful. You stand there for twenty minutes holding a stick before walking back to the car.")
            print(PAR)

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
        if (self.has_item("Worry Stone") and self.has_item("Dream Catcher")
                and self.has_item("Lucky Charm Bracelet")):
            self.use_item("Worry Stone")
            self.use_item("Dream Catcher")
            self.use_item("Lucky Charm Bracelet")
            type.type("You hold the " + cyan(bright("Worry Stone")) + " while the " + cyan(bright("Dream Catcher")) + " sways on your mirror and the " + cyan(bright("Lucky Charm Bracelet")) + " glints on your wrist.")
            print("\n")
            type.type("All three artifacts resonate. Something shifts, deep and irreversible.")
            print("\n")
            type.type("The anxiety. The nightmares. The bad luck. All three dissolve at once.")
            print("\n")
            type.type("You feel genuinely, completely peaceful. Not numb — peaceful. There's a difference.")
            print("\n")
            type.type("All three items turn to warm dust in your hand. You breathe. You're okay.")
            self.restore_sanity(100)
            self._sanity = min(self._sanity + 5, 100)
            print("\n")
            return

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
        elif self.has_item("Flashlight") or self.has_item("Lantern") or self.has_item("Eternal Light"):
            light_name = "Flashlight" if self.has_item("Flashlight") else ("Lantern" if self.has_item("Lantern") else "Eternal Light")
            type.type("You click on your " + magenta(bright(light_name)) + " and sweep the beam around.")
            print("\n")
            type.type("Two eyes reflect back at you from the treeline. Then they blink and vanish.")
            print("\n")
            type.type("You don't sleep great after that.")
            self.lose_sanity(1)
            evolved = self.track_item_use(light_name)
            if evolved:
                print("\n")
                type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
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
        # COMBO: Lucky Penny + Lucky Coin + Lucky Charm Bracelet = Triple Luck
        if self.has_item("Lucky Penny") and (self.has_item("Lucky Coin") or self.has_item("Lucky Medallion")) and self.has_item("Lucky Charm Bracelet"):
            coin = "Lucky Medallion" if self.has_item("Lucky Medallion") else "Lucky Coin"
            type.type("The " + cyan(bright("Lucky Penny")) + " in your pocket. The " + cyan(bright(coin)) + " around your neck. The " + cyan(bright("Lucky Charm Bracelet")) + " on your wrist.")
            print("\n")
            type.type("Triple Luck. All three artifacts pulse in unison. The air shimmers gold.")
            print("\n")
            type.type("For the next few moments, you can't lose. Literally cannot. The universe has temporarily decided you're its favorite child.")
            print("\n")
            type.type("A stranger hands you a winning scratch-off. You find $100 in a jacket you don't remember owning. A bird drops a gold ring at your feet.")
            print("\n")
            self.use_item("Lucky Penny")
            self.use_item("Lucky Charm Bracelet")
            bonus = random.randint(200, 800)
            type.type("Total windfall: " + green(bright("${:,}".format(bonus))) + ". The penny and bracelet crumble to lucky dust.")
            self.change_balance(bonus)
            self.restore_sanity(20)
            print("\n")
            return

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
        elif self.has_item("Pocket Knife") or self.has_item("Utility Blade") or self.has_item("Master Knife"):
            knife_name = "Pocket Knife" if self.has_item("Pocket Knife") else ("Utility Blade" if self.has_item("Utility Blade") else "Master Knife")
            type.type("You wedge your " + cyan(bright(knife_name)) + " into the seam and work it until the lock gives.")
            evolved = self.track_item_use(knife_name)
            if evolved:
                print("\n")
                type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
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

    def mysterious_key_lockbox_open(self):
        """Mysterious Key opens the Mysterious Lockbox for a reward"""
        if not self.has_item("Mysterious Key") or not self.has_item("Mysterious Lockbox"):
            self.day_event()
            return
        if self.has_met("Mysterious Box Opened"):
            self.day_event()
            return
        self.meet("Mysterious Box Opened")
        type.type("You've been carrying both the " + cyan(bright("Mysterious Key")) + " and the " + cyan(bright("Mysterious Lockbox")) + " for days.")
        print("\n")
        type.type("Today, on impulse, you try the key.")
        print("\n")
        type.slow("It fits.")
        print("\n")
        type.type("The box opens with a click. Inside:")
        print("\n")
        reward = random.randrange(4)
        if reward == 0:
            amount = random.randint(500, 2000)
            type.type("Cash. Bundled in rubber bands. Definitely not from a bank. You don't ask questions.")
            self.change_balance(amount)
            type.type(" " + green("${:,}".format(amount)) + ".")
        elif reward == 1:
            type.type("A handwritten letter and a photograph. Two people, clearly in love, in front of a place you don't recognize.")
            type.type(" There's no address. No name. Just: " + quote("For when you find it."))
            self.restore_sanity(15)
            self.add_item("Old Photograph")
        elif reward == 2:
            type.type("A small bag of gems. Semi-precious, but real. Each one catches the light.")
            amount = random.randint(300, 1200)
            self.change_balance(amount)
            type.type(" Worth about " + green("${:,}".format(amount)) + " at the pawn shop.")
        else:
            type.type("A folded map with a circle drawn around something outside of town. And a note: " + quote("Don't go alone."))
            self.add_item("Treasure Coordinates")
            self.restore_sanity(5)
        self.use_item("Mysterious Key")
        self.use_item("Mysterious Lockbox")
        print("\n")

    def suspicious_package_open(self):
        """Opening the Suspicious Package - consequences vary"""
        if not self.has_item("Suspicious Package"):
            self.day_event()
            return
        if self.has_met("Package Opened"):
            self.day_event()
            return
        self.meet("Package Opened")
        type.type("The " + cyan(bright("Suspicious Package")) + " has been in your car for too long. You have to know.")
        print("\n")
        answer = ask.yes_or_no("Open it? ")
        if answer == "yes":
            print("\n")
            result = random.randrange(4)
            if result == 0:
                type.type("Inside: bundles of cash. More than you expected. Way more.")
                amount = random.randint(1000, 5000)
                type.type(" " + green("${:,}".format(amount)) + " in used bills.")
                self.change_balance(amount)
                type.type(" You don't sleep well for a week. But you have the money.")
                self.lose_sanity(8)
            elif result == 1:
                type.type("Inside: photographs. Surveillance photos. Of the casino. Of the Dealer.")
                print("\n")
                type.type("Someone was watching him. And now you have their evidence.")
                self.restore_sanity(5)
                self.meet("Casino Surveillance")
            elif result == 2:
                type.type("Inside: drugs. A LOT of drugs. You immediately throw the whole thing in a dumpster.")
                print("\n")
                type.type("Your hands shake for an hour. You were carrying THAT.")
                self.lose_sanity(15)
                self.hurt(5)  # Stress response
            else:
                type.type("Inside: a birthday cake slice, wrapped in plastic, completely stale. And a note: " + quote("Happy birthday, whoever finds this."))
                print("\n")
                type.type("You eat the cake. It's terrible. It's the best thing you've had all week.")
                self.restore_sanity(10)
                self.heal(5)
            self.use_item("Suspicious Package")
        else:
            type.type("You keep it sealed. Some mysteries are better left unopened.")
            type.type(" But it keeps catching your eye in the rearview mirror.")
            self.lose_sanity(2)
        print("\n")

    def stolen_watch_recognition(self):
        """Someone recognizes the Stolen Watch"""
        if not self.has_item("Stolen Watch"):
            self.day_event()
            return
        if self.has_met("Watch Recognized"):
            self.day_event()
            return
        self.meet("Watch Recognized")
        type.type("You're glancing at the " + cyan(bright("Stolen Watch")) + " when someone nearby does a double-take.")
        print("\n")
        type.type(quote("Hey. HEY. Is that my watch?"))
        print("\n")
        type.type("A man in a rumpled suit stares at your wrist. His face cycles through confusion, recognition, and fury.")
        print("\n")
        answer = ask.yes_or_no("Give it back? ")
        if answer == "yes":
            type.type("You hand it over. He stares at it for a long moment.")
            print("\n")
            type.type(quote("Where did you find this? I lost it — I thought I lost it — "))
            print("\n")
            type.type("He's too relieved to be angry. He presses cash into your hand before you can protest.")
            reward = random.randint(50, 200)
            type.type(" " + green("${:,}".format(reward)) + ". More than it was worth.")
            self.change_balance(reward)
            self.restore_sanity(12)
            self.use_item("Stolen Watch")
        else:
            type.type("You tell him he's mistaken. His eyes say he doesn't believe you.")
            print("\n")
            type.type("He calls out as you walk away. You don't turn back.")
            self.lose_sanity(8)
        print("\n")

    def underwater_camera_photos(self):
        """Underwater Camera photos can be developed for money or memories"""
        if not self.has_item("Underwater Camera"):
            self.day_event()
            return
        if self.has_met("Camera Developed"):
            self.day_event()
            return
        self.meet("Camera Developed")
        type.type("You find a one-hour photo place still operating out of a drug store. You hand over the " + cyan(bright("Underwater Camera")) + ".")
        print("\n")
        type.type("The clerk gives you a look but doesn't ask questions.")
        print("\n")
        type.type("An hour later, you pick up the prints.")
        print("\n")
        result = random.randrange(3)
        if result == 0:
            type.type("Stunning underwater photographs. Coral. Fish. A shipwreck. These are extraordinary.")
            print("\n")
            type.type("A tourist shop next door pays good money for prints like these.")
            amount = random.randint(200, 600)
            self.change_balance(amount)
            type.type("You walk out with " + green("${:,}".format(amount)) + " and keep one photo for yourself.")
            self.restore_sanity(8)
        elif result == 1:
            type.type("Personal photos. A family vacation. Kids laughing, adults sunburned. Somebody's lost memories.")
            print("\n")
            answer = ask.yes_or_no("Post 'found photos' flyers to reunite them? ")
            if answer == "yes":
                type.type("A week later, a voicemail. They want to pay for the prints.")
                self.change_balance(random.randint(50, 150))
                self.restore_sanity(15)
            else:
                type.type("You keep the photos. Someone else's happiness, pressed in paper.")
                self.restore_sanity(5)
        else:
            type.type("The photos are mostly dark. Deep water. One photo shows... something. Something big. Far below.")
            print("\n")
            type.type("You don't know what you took a picture of. You don't want to know.")
            self.lose_sanity(5)
            self.restore_sanity(8)  # But also fascinating
        self.use_item("Underwater Camera")
        print("\n")

    def witch_ward_dark_protection(self):
        """Witch's Ward deflects a dark event"""
        if not self.has_item("Witch's Ward"):
            self.day_event()
            return
        if self.has_met("Ward Protected"):
            self.day_event()
            return
        self.meet("Ward Protected")
        type.type("Something feels wrong today. Like the air has weight.")
        print("\n")
        type.type("You reach for the bundle of herbs tied with red string — the " + cyan(bright("Witch's Ward")) + ".")
        print("\n")
        type.type("You hold it. The feeling doesn't go away completely. But something... redirects.")
        print("\n")
        type.type("Later, a neighbor tells you someone hit every car on the block but yours.")
        print("\n")
        type.type("Yours had dirt smeared on the hood. Like muddy fingerprints.")
        print("\n")
        type.type("The ward crumbles to dust in your hand that evening. Its job is done.")
        self.use_item("Witch's Ward")
        self.restore_sanity(10)
        self.heal(5)
        amount = random.randint(100, 500)
        type.type(" You also find " + green("${:,}".format(amount)) + " wedged under your seat. Found by whatever checked on you.")
        self.change_balance(amount)
        print("\n")

    def deck_of_cards_street_game(self):
        """Deck of Cards enables a street gambling event"""
        if not self.has_item("Deck of Cards"):
            self.day_event()
            return
        if self.has_met("Street Card Game"):
            self.day_event()
            return
        self.meet("Street Card Game")
        type.type("You're sitting on a curb when a group of guys sets up a folding table nearby.")
        print("\n")
        type.type("They're playing cards. Three-card monte. You can see the tells from twenty feet.")
        print("\n")
        type.type("You pull out your own " + cyan(bright("Deck of Cards")) + " and spread it meaningfully.")
        print("\n")
        type.type(quote("You know how to play, or you just carry those for decoration?"))
        print("\n")
        answer = ask.yes_or_no("Play? ")
        if answer == "yes":
            bet = min(self.get_balance() // 4, random.randint(50, 200))
            type.type("You ante up " + green("${:,}".format(bet)) + ".")
            print("\n")
            if random.randrange(3) != 0:  # 67% win (you know what you're doing)
                winnings = bet * 2
                type.type("You read them perfectly. Clean win.")
                self.change_balance(winnings - bet)  # net gain
                type.type(" +" + green("${:,}".format(winnings - bet)) + ".")
                self.restore_sanity(8)
            else:
                type.type("They had a tell you missed. Sharp guys.")
                self.change_balance(-bet)
                type.type(" -" + red("${:,}".format(bet)) + ". Respect.")
                self.restore_sanity(3)  # Still fun
        else:
            type.type("You watch. A show. Free entertainment.")
            self.restore_sanity(4)
        print("\n")

    def ace_of_spades_blackjack_omen(self):
        """Ace of Spades gives a gambling premonition"""
        if not self.has_item("Ace of Spades"):
            self.day_event()
            return
        if self.has_met("Ace Omen Used"):
            self.day_event()
            return
        self.meet("Ace Omen Used")
        type.type("The " + cyan(bright("Ace of Spades")) + " falls out of your pocket this morning. Death card. Power card. The universe's wild card.")
        print("\n")
        type.type("You hold it up. On the back someone has written more words than before. When did that happen?")
        print("\n")
        type.type(quote("Tonight, trust the first instinct. Don't second-guess. The cards know."))
        print("\n")
        type.type("You pocket it again. Head to the casino.")
        print("\n")
        type.type("At the first hand, you feel it — the pull. Like the card is warm against your leg.")
        self.add_status("Lucky")
        self.add_status("Sharp")
        type.type(" The night goes well. Very well.")
        amount = random.randint(200, 1000)
        self.change_balance(amount)
        type.type(" +" + green("${:,}".format(amount)) + " by closing time.")
        self.restore_sanity(10)
        print("\n")

    def dealer_joker_revelation(self):
        """The Dealer's Joker stirs something unsettling at the blackjack table"""
        if not self.has_item("Dealer's Joker"):
            self.day_event()
            return
        if self.has_met("Joker Revelation"):
            self.day_event()
            return
        self.meet("Joker Revelation")
        type.type("You slide the " + cyan(bright("Dealer's Joker")) + " onto the table without thinking. Habit.")
        print("\n")
        type.type("The pit boss freezes. The dealer freezes. The card doesn't belong to this casino's deck.")
        print("\n")
        type.type("But the pit boss recognizes it. His face goes pale.")
        print("\n")
        type.type(quote("Where did you get that?"))
        print("\n")
        type.type("The table clears. Quietly. Professional. The way a casino moves when something is wrong.")
        print("\n")
        type.type("Ten minutes later, a manager escorts you to a private room. They don't ask again. They just... comp you.")
        print("\n")
        amount = random.randint(500, 2000)
        type.type("A voucher. " + green("${:,}".format(amount)) + " in house chips. No questions. Please don't tell anyone about the card.")
        self.change_balance(amount)
        self.restore_sanity(15)
        self.lose_sanity(5)  # Unnerving encounter
        print("\n")

    def magic_acorn_planting(self):
        """Magic Acorn can be planted for a future reward"""
        if not self.has_item("Magic Acorn"):
            self.day_event()
            return
        if self.has_met("Acorn Planted"):
            self.day_event()
            return
        self.meet("Acorn Planted")
        type.type("The " + cyan(bright("Magic Acorn")) + " has been rattling around your glove box. The fairy said to plant it and come back in a year.")
        print("\n")
        type.type("You're probably not coming back in a year. But you find a quiet patch of earth behind the old gas station and dig a hole.")
        print("\n")
        answer = ask.yes_or_no("Plant it? ")
        if answer == "yes":
            type.type("You drop it in. Cover it. Pat the ground twice.")
            print("\n")
            type.type("Nothing happens. Of course nothing happens. It's an acorn.")
            print("\n")
            type.type("But the air smells different for a moment. Green. Old. Like standing in a forest from a long time ago.")
            self.use_item("Magic Acorn")
            self.restore_sanity(12)
            self.add_status("Nature Blessed")
            type.type(" Something small planted. Something larger, eventually.")
        else:
            type.type("You keep it. You might need it. Or want it. You're not sure why.")
            self.restore_sanity(3)
        print("\n")


    def treasure_map_follow(self):
        """Treasure Map / Joe's Map / Fairy's Secret Map leads to a small treasure"""
        has_map = (self.has_item("Treasure Map") or self.has_item("Joe's Treasure Map") or
                   self.has_item("Fairy's Secret Map") or self.has_item("Treasure Coordinates"))
        if not has_map:
            self.day_event()
            return
        if self.has_met("Treasure Map Followed"):
            self.day_event()
            return
        self.meet("Treasure Map Followed")
        if self.has_item("Fairy's Secret Map"):
            map_name = "Fairy's Secret Map"
            type.type("The " + cyan(bright("Fairy's Secret Map")) + " glows faintly. The markings shift in the light — it's leading you somewhere.")
        elif self.has_item("Treasure Coordinates"):
            map_name = "Treasure Coordinates"
            type.type("You've been sitting on these " + cyan(bright("Treasure Coordinates")) + " long enough. Today you follow them.")
        elif self.has_item("Joe's Treasure Map"):
            map_name = "Joe's Treasure Map"
            type.type("Joe's note said he never found the spot. You've got his " + cyan(bright("Joe's Treasure Map")) + " and a free afternoon.")
        else:
            map_name = "Treasure Map"
            type.type("You unfold the " + cyan(bright("Treasure Map")) + " and follow the dotted line until it ends.")
        print("\n")
        if self.has_item("Rusty Compass") or self.has_item("Golden Compass"):
            compass = "Golden Compass" if self.has_item("Golden Compass") else "Rusty Compass"
            type.type("The " + cyan(bright(compass)) + " pulls toward something buried nearby.")
            print("\n")
            type.type("You dig where it points and find more than expected.")
            bonus = random.randint(50, 200)
            self.change_balance(bonus)
            print("\n")
            type.type(green(bright("+${:,}".format(bonus))))
            print("\n")
        answer = ask.yes_or_no("Follow it now? ")
        if answer == "yes":
            type.type("You drive the route. Then walk. Then dig.")
            print("\n")
            result = random.randrange(4)
            if result == 0:
                amount = random.randint(300, 1500)
                type.type("A tin box. Rusted but intact. Inside: cash, rolled tight, and a note that just says " + quote("Good luck, stranger."))
                type.type(" " + green("${:,}".format(amount)) + ".")
                self.change_balance(amount)
                self.restore_sanity(12)
            elif result == 1:
                type.type("A glass jar full of old coins. Mostly worthless by themselves.")
                type.type(" But together, a coin dealer pays well.")
                amount = random.randint(150, 600)
                self.change_balance(amount)
                type.type(" " + green("${:,}".format(amount)) + ".")
                self.restore_sanity(8)
            elif result == 2:
                type.type("Nothing. The spot exists but there's nothing there. Already dug up, long ago.")
                print("\n")
                type.type("But you spent a few hours outside, in the open air, searching. That was something.")
                self.restore_sanity(5)
                self.heal(5)
            else:
                type.type("You find the spot. You dig. You hit something hard.")
                print("\n")
                type.type("A box. You open it. Inside: another map. This one is different. Older.")
                self.add_item("Vision Map") if not self.has_item("Vision Map") else self.change_balance(100)
                self.restore_sanity(10)
            self.use_item(map_name)
        else:
            type.type("You fold it back up. Another day.")
            self.lose_sanity(2)
        print("\n")

    def capture_fairy_release(self):
        """The Captured Fairy in your bag causes strange dreams — releasing it gives a blessing"""
        if not self.has_item("Captured Fairy"):
            self.day_event()
            return
        if self.has_met("Fairy Released"):
            self.day_event()
            return
        self.meet("Fairy Released")
        type.type("The jar in your bag has been vibrating at night. The " + cyan(bright("Captured Fairy")) + " hasn't stopped.")
        print("\n")
        type.type("You've been having strange dreams. Colors you can't name. Music with no source.")
        print("\n")
        type.type("Today you open the jar.")
        print("\n")
        answer = ask.yes_or_no("Let it go? ")
        if answer == "yes":
            type.type("The fairy hovers in the air between you. Studies you.")
            print("\n")
            type.type("Then it presses something into your palm — a tiny glowing seed — and disappears.")
            print("\n")
            type.type("The strange dreams stop. You feel lighter. The curse lifted.")
            self.use_item("Captured Fairy")
            self.remove_status("Fairy Cursed") if self.has_status("Fairy Cursed") else None
            self.restore_sanity(20)
            self.heal(15)
            self.add_status("Fairy Blessed")
            if not self.has_item("Magic Acorn"):
                self.add_item("Magic Acorn")
            type.type(" The seed looks like a " + cyan(bright("Magic Acorn")) + ".")
        else:
            type.type("You close the jar. The vibrating gets louder.")
            print("\n")
            type.type("The dreams that night are worse.")
            self.lose_sanity(8)
        print("\n")

    def lucky_lure_fishing(self):
        """Lucky Lure / Earl's Lucky Lure can be used in a fishing event"""
        has_lure = self.has_item("Lucky Lure") or self.has_item("Earl's Lucky Lure")
        if not has_lure:
            self.day_event()
            return
        if self.has_met("Lucky Lure Fished"):
            self.day_event()
            return
        self.meet("Lucky Lure Fished")
        lure = "Earl's Lucky Lure" if self.has_item("Earl's Lucky Lure") else "Lucky Lure"
        type.type("You find a spot by the water. You've got the " + cyan(bright(lure)) + " and nothing but time.")
        print("\n")
        type.type("You tie it on, cast out, and wait. The line goes taut almost immediately.")
        print("\n")
        catch = random.randrange(4)
        if catch == 0:
            type.type("Something massive. You fight it for twenty minutes. Your arms burn.")
            print("\n")
            type.type("You pull up a fish so big the lure bends. You weigh it on your car's bumper somehow.")
            self.change_balance(random.randint(100, 500))
            self.restore_sanity(20)
            self.heal(10)
            type.type(" Worth " + green("${:,}".format(random.randint(100, 500))) + " to a local fish market.")
            self.add_item("Fish") if not self.has_item("Fish") else None
        elif catch == 1:
            type.type("A nice-sized bass. Clean catch. You let it go after a moment, because that felt right.")
            self.restore_sanity(15)
            self.heal(5)
            self.reduce_fatigue(10)
        elif catch == 2:
            type.type("A boot. You caught a boot. The lure is still on it.")
            type.type(" There's a twenty-dollar bill stuffed in the boot.")
            self.change_balance(20)
            self.restore_sanity(8)
        else:
            type.type("Three fish in an hour. More than you can eat. You give some to an older man downstream who's been skunked all day.")
            print("\n")
            type.type("He starts to cry a little. Says his wife used to bring him here. It's been a hard year.")
            self.restore_sanity(18)
            self.heal(8)
            self.add_item("Live Fish") if not self.has_item("Live Fish") else None
        print("\n")

    def mysterious_code_decode(self):
        """Mysterious Code can be decoded for a clue or reward"""
        if not self.has_item("Mysterious Code"):
            self.day_event()
            return
        if self.has_met("Code Decoded"):
            self.day_event()
            return
        self.meet("Code Decoded")
        type.type("The " + cyan(bright("Mysterious Code")) + " has been nagging at you. Numbers. Symbols. A pattern.")
        print("\n")
        type.type("You spend a morning with a pen and paper, staring at it. Then it clicks.")
        print("\n")
        answer = ask.yes_or_no("Work it out now? ")
        if answer == "yes":
            result = random.randrange(3)
            if result == 0:
                type.type("It's a combination. You find a storage locker nearby that matches.")
                print("\n")
                type.type("Inside: boxes of old equipment and a cash box someone forgot to empty.")
                amount = random.randint(200, 1000)
                self.change_balance(amount)
                type.type(" " + green("${:,}".format(amount)) + " in old bills.")
                self.restore_sanity(12)
            elif result == 1:
                type.type("It's coordinates. You drive to the spot. It's a rest stop with a picnic table.")
                print("\n")
                type.type("Under the table, taped with duct tape, is an envelope. Inside: a key and a note that just says: " + quote("For emergencies."))
                self.add_item("Mysterious Key") if not self.has_item("Mysterious Key") else self.change_balance(100)
                self.restore_sanity(10)
            else:
                type.type("It's an old radio frequency. You tune in. Static. Then: a voice.")
                print("\n")
                type.type("Someone broadcasting from far away. A woman reading poetry into the dark.")
                print("\n")
                type.type("You listen for an hour.")
                self.restore_sanity(20)
            self.use_item("Mysterious Code")
        else:
            type.type("You fold it up. Maybe the mystery is the point.")
            self.restore_sanity(3)
        print("\n")

    def swamp_gold_attention(self):
        """Swamp Gold attracts attention from people who recognize what it is"""
        if not self.has_item("Swamp Gold"):
            self.day_event()
            return
        if self.has_met("Swamp Gold Spotted"):
            self.day_event()
            return
        self.meet("Swamp Gold Spotted")
        type.type("Someone at the gas station stares at the " + cyan(bright("Swamp Gold")) + " jewelry you've been keeping in the cupholder.")
        print("\n")
        type.type("They know what it is. The kind that only comes from one place. The swamp.")
        print("\n")
        approach = random.randrange(3)
        if approach == 0:
            type.type("A woman approaches. Quiet. Respectful.")
            print("\n")
            type.type(quote("That belonged to my grandmother. I thought it was gone. The flood — we lost everything."))
            print("\n")
            answer = ask.yes_or_no("Give it back? ")
            if answer == "yes":
                type.type("You hand it over without asking for anything.")
                print("\n")
                type.type("She clutches it. Cries quietly.")
                print("\n")
                type.type("Her son comes over. Presses bills into your hand. Way more than it's worth.")
                amount = random.randint(200, 600)
                self.change_balance(amount)
                self.restore_sanity(20)
                self.use_item("Swamp Gold")
            else:
                type.type("You tell her you found it, and you're keeping it. She nods, understanding but sad.")
                self.lose_sanity(10)
        elif approach == 1:
            type.type("A collector. He wants it badly. Swamp provenance means authenticity.")
            amount = random.randint(300, 900)
            type.type(" He offers " + green("${:,}".format(amount)) + ".")
            answer = ask.yes_or_no("Sell it to him? ")
            if answer == "yes":
                self.change_balance(amount)
                self.restore_sanity(5)
                self.use_item("Swamp Gold")
            else:
                type.type("You decline. The collector leaves his number.")
                self.restore_sanity(3)
        else:
            type.type("A man follows you to your car. Wants to know where you found it. His manner makes you uncomfortable.")
            print("\n")
            type.type("You get in and drive away. The swamp keeps its secrets. So do you.")
            self.lose_sanity(5)
            self.restore_sanity(3)  # Net loss of 2
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # NEW CRAFTED ITEM EVENTS — GADGETS
    # ══════════════════════════════════════════════════════════════════════

    def headlamp_night_walk(self):
        """Headlamp reveals threats during dark encounters"""
        type.type("The road ahead is pitch black. Your headlights flicker — the battery's getting weak.")
        print("\n")
        type.type("Something moves in the ditch. A shape. Too big for a dog.")
        print("\n")
        if self.has_item("Headlamp"):
            type.type("You click on your " + cyan(bright("Headlamp")) + ". The beam cuts through the dark like a spotlight.")
            print("\n")
            type.type("It's a deer. Just a deer, frozen in the light, staring at you with those big stupid eyes.")
            print("\n")
            type.type("You breathe out. The headlamp just saved you from a panic attack and a possible ditch dive.")
            self.restore_sanity(3)
        elif self.has_item("Flashlight"):
            type.type("You fumble for your flashlight, holding it in one hand while steering with the other.")
            print("\n")
            type.type("The beam wobbles everywhere. You catch a glimpse of antlers before the shape bolts into the trees.")
            type.type(" Deer. Probably. Your hands are shaking.")
            self.lose_sanity(1)
        else:
            type.type("You white-knuckle the steering wheel and pray. The shape doesn't move. You swerve around it.")
            print("\n")
            type.type("Your heart doesn't recover for twenty minutes. You never find out what it was.")
            self.lose_sanity(4)
        print("\n")

    def spotlight_hidden_path(self):
        """Spotlight reveals hidden paths during exploration"""
        type.type("A fork in the road. The sign is rusted beyond reading. Left or right.")
        print("\n")
        if self.has_item("Spotlight"):
            type.type("You pull out the " + cyan(bright("Spotlight")) + " and aim it down both paths.")
            print("\n")
            type.type("Left: roadblock, collapsed bridge, dead end. Right: clear road, and — wait. There's a THIRD path. Overgrown, almost invisible, but the spotlight catches tire tracks.")
            print("\n")
            type.type("You take the hidden path. It leads to an abandoned rest stop with untouched supplies.")
            loot = random.randint(30, 80)
            self.change_balance(loot)
            type.type(" You find " + green("${:,}".format(loot)) + " in the register and supplies in the back.")
            self.restore_sanity(3)
        else:
            choice = random.randrange(2)
            if choice == 0:
                type.type("You go left. Dead end. Collapsed bridge. You spend forty minutes turning around.")
                self.lose_sanity(2)
            else:
                type.type("You go right. Clear road, but nothing interesting. Just miles of nothing. The sign is still unreadable in your mind.")
                self.lose_sanity(1)
        print("\n")

    def evidence_kit_crime(self):
        """Evidence Kit changes a crime witness event"""
        type.type("Someone's breaking into a car across the parking lot. Broad daylight. Bold.")
        print("\n")
        type.type("They see you watching but don't care. You're one person. What are you going to do?")
        print("\n")
        if self.has_item("Evidence Kit"):
            type.type("You pull out the " + cyan(bright("Evidence Kit")) + " and start documenting. Click. Click. Click.")
            print("\n")
            type.type("The camera flashes. The signal booster transmits. The thief's face drains of color.")
            print("\n")
            type.type(quote("Delete that! DELETE THAT!"))
            print("\n")
            type.type("They sprint. Gone in ten seconds. Twenty minutes later, a cop shows up, takes your photos, and hands you a reward for the tip.")
            reward = random.randint(50, 150)
            self.change_balance(reward)
            type.type(" " + green("${:,}".format(reward)) + " for civic duty.")
            self.restore_sanity(5)
        else:
            type.type("You pull out your phone. The screen glare makes it impossible to get a clear photo.")
            print("\n")
            type.type("The thief flips you off and drives away. Nobody comes. Nobody cares. Welcome to society.")
            self.lose_sanity(3)
        print("\n")

    def radio_jammer_checkpoint(self):
        """Radio Jammer disrupts a police checkpoint"""
        type.type("Red and blue lights ahead. Checkpoint. Three cruisers parked sideways across the road.")
        print("\n")
        type.type("You're not doing anything wrong. Probably. But checkpoints make everyone nervous.")
        print("\n")
        if self.has_item("Radio Jammer"):
            type.type("You flip the " + cyan(bright("Radio Jammer")) + " under your seat. The police radios squawk and die.")
            print("\n")
            type.type("Officers look at each other, confused. Tap their earpieces. One walks to his car to check the radio. Then another.")
            print("\n")
            type.type("In the chaos of dead comms, you idle through the gap. Nobody flags you. They're too busy troubleshooting.")
            self.restore_sanity(5)
        elif self.has_item("Forged Documents"):
            type.type("You hand over your " + cyan(bright("Forged Documents")) + " with the confidence of someone who has nothing to hide.")
            print("\n")
            type.type("The officer squints. Checks the seal. Checks the photo. Nods.")
            print("\n")
            type.type(quote("Have a good evening, Mr. Torres."))
            self.restore_sanity(2)
        else:
            type.type("License and registration. You hand them over.")
            print("\n")
            if random.randrange(3) == 0:
                type.type("Everything checks out. The officer waves you through after a long, uncomfortable stare.")
            else:
                fine = random.randint(25, 75)
                type.type("Expired registration. He writes you a ticket for " + red("${:,}".format(fine)) + ".")
                self.change_balance(-fine)
            self.lose_sanity(2)
        print("\n")

    def emp_device_pursuit(self):
        """EMP Device ends a vehicle pursuit (consumed)"""
        type.type("The car behind you is gaining. Fast. They've been following since the last intersection.")
        print("\n")
        type.type("This isn't road rage. This is deliberate. Your rearview shows two people, driver and passenger, and the passenger is pointing at you.")
        print("\n")
        if self.has_item("EMP Device"):
            type.type("You grab the " + cyan(bright("EMP Device")) + " and toss it out the window.")
            print("\n")
            type.type("POP. A silent pulse. Every electronic in a 50-foot radius dies — their headlights, their engine, their power steering. The car coasts to a stop like a toy running out of battery.")
            print("\n")
            type.type("You drive away. In the rearview, they're standing in the road, staring at their dead car. Problem solved.")
            self.use_item("EMP Device")
            self.restore_sanity(8)
        elif self.has_item("Pursuit Package"):
            type.type("You lace up the " + cyan(bright("Pursuit Package")) + " shoes and blow the dog whistle out the window.")
            print("\n")
            type.type("Three neighborhood dogs go BALLISTIC, chasing the pursuing car. Their driver swerves to avoid a golden retriever and clips a mailbox. You disappear around the corner.")
            self.restore_sanity(5)
        else:
            type.type("You floor it. Red lights, stop signs, a one-way street the wrong direction — you run them all.")
            print("\n")
            type.type("They give up after four blocks. Or you lost them. Or they're taking a different route. You don't stop to find out.")
            self.lose_sanity(5)
            self.hurt(random.choice([0, 0, 5]))
        print("\n")

    def security_bypass_locked_room(self):
        """Security Bypass opens a locked building"""
        type.type("An abandoned building. Door locked. Windows boarded. But you can hear a generator humming inside.")
        print("\n")
        type.type("Someone left this place powered. That means there's something worth powering.")
        print("\n")
        if self.has_item("Security Bypass"):
            type.type("The " + cyan(bright("Security Bypass")) + " makes quick work of the lock. Four seconds, clean entry.")
            print("\n")
            type.type("Inside: a survival cache. Water, canned food, batteries, and a safe. You work the safe next.")
            loot = random.randint(50, 200)
            self.change_balance(loot)
            type.type(" " + green("${:,}".format(loot)) + " in the safe, plus supplies you can actually use.")
            self.restore_sanity(5)
            self.heal(5)
        elif self.has_item("Master Key"):
            type.type("Your " + cyan(bright("Master Key")) + " handles the door AND the safe inside. Two seconds each.")
            loot = random.randint(100, 300)
            self.change_balance(loot)
            type.type(" " + green("${:,}".format(loot)) + " and a feeling of professional satisfaction.")
            self.restore_sanity(5)
            self.heal(5)
        elif self.has_item("Lockpick Set"):
            type.type("Your " + cyan(bright("Lockpick Set")) + " gets the door open, but the safe inside defeats you.")
            loot = random.randint(10, 40)
            self.change_balance(loot)
            type.type(" You find " + green("${:,}".format(loot)) + " in a drawer. The safe haunts your dreams.")
            self.restore_sanity(2)
        else:
            type.type("You try the door. Locked. You try the windows. Boarded. You kick the door. It laughs at you.")
            print("\n")
            type.type("Whatever's inside stays inside. You walk away, generator still humming behind you.")
            self.lose_sanity(2)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # NEW CRAFTED ITEM EVENTS — DISGUISES
    # ══════════════════════════════════════════════════════════════════════

    def gentleman_charm_dinner(self):
        """Gentleman's Charm wins over a fancy establishment"""
        type.type("A restaurant. Real tablecloths. Real candles. Real pretension. You're in a parking lot.")
        print("\n")
        type.type("The host sees you approaching and starts formulating a polite rejection.")
        print("\n")
        if self.has_item("Flask of Pocket Aces") and self.has_item("Gentleman's Charm"):
            type.type("The " + cyan(bright("Flask of Pocket Aces")) + " pulses against your ribs. Two aces, burning in your pocket.")
            print("\n")
            type.type("The " + cyan(bright("Gentleman's Charm")) + " does the rest. The host's polite rejection dies before it starts.")
            print("\n")
            type.type(quote("Sir. We've been expecting you. Your usual table?"))
            print("\n")
            type.type("You don't have a usual table. You do now. Whatever you're about to do — you feel winning.")
            bonus = random.randint(100, 200)
            type.type(" Someone at the bar insists on picking up the tab. Presses " + green(bright("$" + str(bonus))) + " into your hand on the way out.")
            self.heal(15)
            self.restore_sanity(12)
            self.change_balance(bonus)
        elif self.has_item("Gentleman's Charm"):
            type.type("Then the " + cyan(bright("Gentleman's Charm")) + " hits. The cologne, the silk — the host's rejection dies on their lips.")
            print("\n")
            type.type(quote("Right this way, sir. We have a lovely table by the window."))
            print("\n")
            type.type("You sit. They bring bread. REAL bread. With butter. Someone else pays for your meal because they assume you're someone important.")
            self.heal(10)
            self.restore_sanity(8)
        elif self.has_item("Old Money Identity"):
            type.type("The " + cyan(bright("Old Money Identity")) + " opens doors that were never closed to begin with.")
            print("\n")
            type.type("The host bows. The chef comes to your table. They comp the entire meal. You leave a $5 tip because old money is notoriously cheap. Nobody questions it.")
            self.heal(15)
            self.restore_sanity(10)
        else:
            type.type("The host looks you up and down. " + quote("Perhaps you'd be more comfortable at the diner across the street?"))
            print("\n")
            type.type("You go to the diner. The coffee's better anyway. Probably.")
            self.lose_sanity(3)
        print("\n")

    def forged_documents_police(self):
        """Forged Documents avoid a police encounter"""
        type.type("Two cops. Walking toward you. Making eye contact. That purposeful walk that says you're the destination.")
        print("\n")
        type.type(quote("Excuse me. Can we see some identification?"))
        print("\n")
        if self.has_item("Forged Documents"):
            type.type("You produce the " + cyan(bright("Forged Documents")) + " with steady hands and a bored expression.")
            print("\n")
            type.type("Officer squints at the ID. Looks at you. Looks at the ID. The ballpoint government seal gleams with false authority.")
            print("\n")
            type.type(quote("Alright, Mr. Torres. Sorry to bother you."))
            print("\n")
            type.type("They walk away. You breathe. Michael Torres strikes again.")
            self.restore_sanity(5)
        elif self.has_item("New Identity"):
            type.type("The " + cyan(bright("New Identity")) + " is flawless. They don't just accept it — they apologize for stopping you.")
            self.restore_sanity(8)
        else:
            type.type("You hand over your real ID. They run it. You wait. The radio crackles.")
            print("\n")
            if random.randrange(4) == 0:
                fine = random.randint(50, 150)
                type.type("Outstanding warrant. Unpaid parking tickets. They write you up for " + red("${:,}".format(fine)) + ".")
                self.change_balance(-fine)
                self.lose_sanity(5)
            else:
                type.type("Clean. They hand it back and walk off. Your blood pressure takes twenty minutes to normalize.")
                self.lose_sanity(2)
        print("\n")

    def brass_knuckles_brawl(self):
        """Brass Knuckles end a bar fight quickly"""
        type.type("The bar is loud. Someone bumps your shoulder. Doesn't apologize. Bumps it again. Makes eye contact.")
        print("\n")
        type.type(quote("You got a problem, buddy?"))
        print("\n")
        if self.has_item("Brass Knuckles"):
            type.type("You flex your hand inside the glove. The " + cyan(bright("Brass Knuckles")) + " shift into position.")
            print("\n")
            type.type("One punch. Center mass. He folds like a lawn chair in a hurricane.")
            print("\n")
            type.type("The bar goes silent. His friends look at him. Look at you. Decide they're not his friends tonight.")
            type.type(" You finish your drink in peace.")
            self.restore_sanity(5)
        elif self.has_item("Street Fighter Set"):
            type.type("The " + cyan(bright("Street Fighter Set")) + " comes out. Shiv in one hand, knuckles in the other.")
            print("\n")
            type.type("He looks at both. Reconsiders EVERYTHING. " + quote("Hey man, my bad. Let me buy you a drink."))
            self.restore_sanity(8)
            loot = random.randint(5, 15)
            self.change_balance(loot)
        else:
            type.type("It's a bar fight. No weapons, just fists and bad decisions.")
            print("\n")
            if random.randrange(2) == 0:
                type.type("You land a lucky shot. He lands three. You leave with a black eye and a story.")
                self.hurt(8)
                self.lose_sanity(2)
            else:
                type.type("He's bigger. He's angrier. You end up on the floor. The bartender calls it.")
                self.hurt(12)
                self.lose_sanity(4)
        print("\n")

    def gas_mask_chemical(self):
        """Gas Mask protects against chemical hazards"""
        type.type("The smell hits before you see the source. Acrid. Chemical. The kind of smell that makes your eyes water from thirty feet away.")
        print("\n")
        type.type("Some kind of spill on the road ahead. Green liquid pooling. Cars are turning around.")
        print("\n")
        if self.has_item("Gas Mask") or self.has_item("Hazmat Suit"):
            used = "Hazmat Suit" if self.has_item("Hazmat Suit") else "Gas Mask"
            type.type("You strap on the " + cyan(bright(used)) + " and drive straight through.")
            print("\n")
            type.type("Inside the mask, it smells like a car dealership. Outside, it smells like the apocalypse. You smell the car dealership.")
            print("\n")
            type.type("On the other side, a police officer stares at you in disbelief. " + quote("How did you... You know what, just go."))
            self.restore_sanity(3)
        else:
            type.type("You turn around with everyone else. The detour adds forty minutes to your drive.")
            print("\n")
            type.type("Your eyes are still watering an hour later. Whatever that stuff was, it's not leaving your sinuses soon.")
            self.hurt(5)
            self.lose_sanity(2)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # NEW CRAFTED ITEM EVENTS — TONICS & CONSUMABLES
    # ══════════════════════════════════════════════════════════════════════

    def stink_bomb_escape(self):
        """Stink Bomb clears out hostiles"""
        type.type("Three men. Corner of the alley. Looking at you with the kind of interest that precedes a very bad evening.")
        print("\n")
        type.type("They start walking toward you. Casual. Confident. Organized.")
        print("\n")
        if self.has_item("Stink Bomb"):
            type.type("You crack the " + cyan(bright("Stink Bomb")) + " and roll it between them.")
            print("\n")
            type.type("The reaction is INSTANT. Gagging. Retching. One man drops to his knees. Another covers his face and runs into a wall. The smell is so aggressive it has a PERSONALITY.")
            print("\n")
            type.type("You walk past them while they're incapacitated. One of them is crying. You almost feel bad. Almost.")
            self.use_item("Stink Bomb")
            self.restore_sanity(5)
        elif self.has_item("Tear Gas"):
            type.type("The " + cyan(bright("Tear Gas")) + " hits them mid-stride. All three go down. Pepper spray AND stink chemistry.")
            print("\n")
            type.type("The Geneva Convention wasn't designed for alley encounters but it SHOULD have been.")
            self.use_item("Tear Gas")
            self.restore_sanity(8)
        else:
            type.type("You run. They follow. You're faster — barely. But the adrenaline costs you sleep tonight.")
            self.lose_sanity(4)
            self.hurt(random.choice([0, 3, 5]))
        print("\n")

    def animal_bait_companion(self):
        """Animal Bait attracts a potential companion"""
        type.type("The roadside is quiet. Too quiet for a place with this much underbrush.")
        print("\n")
        type.type("You can feel it — something is watching you from the bushes.")
        print("\n")
        if self.has_item("Animal Bait") or self.has_item("Beast Tamer Kit"):
            used = "Beast Tamer Kit" if self.has_item("Beast Tamer Kit") else "Animal Bait"
            type.type("You set out the " + cyan(bright(used)) + " and wait.")
            print("\n")
            type.type("One minute. Two. Then a nose pushes through the leaves. A stray — thin, cautious, hungry.")
            print("\n")
            type.type("It eats. Looks at you. Eats more. Looks at you with different eyes. The kind of look that says " + quote("Okay. You'll do."))
            print("\n")
            if used == "Animal Bait":
                self.use_item("Animal Bait")
            if len(self.get_all_companions()) == 0:
                dog_name = random.choice(["Scraps", "Bones", "Nomad", "Drifter"])
                type.type("The stray follows you back to the car and hops in like it owns the place. " + bright("You have a companion."))
                self.add_companion(dog_name, "Stray Dog")
            else:
                type.type("It trails behind your car for a while, then finds a better offer in someone else's trash. Fair enough.")
            self.restore_sanity(5)
        else:
            type.type("Whatever's in the bushes decides you're not worth the risk. The rustling fades. You're alone again.")
            self.lose_sanity(1)
        print("\n")

    def trail_mix_bomb_distraction(self):
        """Trail Mix Bomb creates a diversion"""
        type.type("The gas station attendant is LOSING it. Screaming at you about something you didn't do. His finger is way too close to your face.")
        print("\n")
        type.type("Behind him, his buddy is circling around. This is an ambush with extra steps.")
        print("\n")
        if self.has_item("Trail Mix Bomb"):
            type.type("You light the " + cyan(bright("Trail Mix Bomb")) + " and toss it into the parking lot.")
            print("\n")
            type.type("FWOOM! Seeds EVERYWHERE. Matches flash. A flock of pigeons materializes from the fabric of reality. The attendant's friend trips over a pigeon. The attendant looks away for one second.")
            print("\n")
            type.type("One second is all you need. You're in the car and gone before the pigeons finish their buffet.")
            self.use_item("Trail Mix Bomb")
            self.restore_sanity(5)
        else:
            type.type("You back up slowly. The attendant follows. His buddy blocks the car.")
            print("\n")
            lost = min(random.randint(20, 50), self._balance)
            if lost > 0:
                type.type("They take " + red("${:,}".format(lost)) + " for \"damages.\" You don't argue. You leave.")
                self.change_balance(-lost)
            self.lose_sanity(4)
        print("\n")

    def voice_soother_persuasion(self):
        """Voice Soother helps in a negotiation"""
        type.type("The mechanic slides a quote across the counter. You look at the number. Then look again. Then a third time, because surely there's a decimal point you missed.")
        print("\n")
        type.type("There isn't. It's that much.")
        print("\n")
        if self.has_item("Voice Soother"):
            type.type("You sip the " + cyan(bright("Voice Soother")) + ". Your voice drops an octave, smooth as midnight radio.")
            print("\n")
            type.type(quote("I appreciate the work. But I think we can find a number that works for both of us."))
            print("\n")
            type.type("The mechanic blinks. Reconsiders. Crosses out the number and writes a new one — 40% lower.")
            type.type(" Something about your voice made him WANT to be reasonable.")
            self.use_item("Voice Soother")
            self.restore_sanity(3)
        else:
            type.type("You try to negotiate. Your voice cracks mid-sentence. The mechanic doesn't budge.")
            print("\n")
            type.type("You pay full price. Your wallet weeps.")
            cost = random.randint(30, 80)
            self.change_balance(-cost)
            self.lose_sanity(2)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # NEW CRAFTED ITEM EVENTS — DARK ARTS
    # ══════════════════════════════════════════════════════════════════════

    def eldritch_candle_entity(self):
        """Eldritch Candle commands dark entities"""
        type.type("The shadows in the corner of the parking lot aren't regular shadows. They're too DARK. Too... present.")
        print("\n")
        type.type("Something is watching you from inside the darkness. You can feel its attention like weight on your shoulders.")
        print("\n")
        if self.has_item("Eldritch Candle"):
            type.type("You light the " + cyan(bright("Eldritch Candle")) + ". The green flame catches immediately. It always does.")
            print("\n")
            type.type("The shadow FLINCHES. It recognizes the flame. It recognizes the authority the flame carries.")
            print("\n")
            type.type(quote("Leave.") + " One word. The shadow obeys. The darkness retreats to regular darkness.")
            print("\n")
            type.type("Your hands are still cold. The candle relights itself in your pocket.")
            self.lose_sanity(2)
            self.restore_sanity(5)  # Net +3
        elif self.has_item("Dark Pact Reliquary"):
            type.type("The " + cyan(bright("Dark Pact Reliquary")) + " hums. The shadow doesn't flinch — it BOWS.")
            print("\n")
            type.type("The reliquary whispers something. The shadow retreats, but gently, like a servant exiting a room.")
            self.restore_sanity(2)
        else:
            type.type("The shadow reaches. Cold floods your body. Every instinct screams to run. You run.")
            print("\n")
            type.type("You make it to the car. The shadow stays where it was. Watching. Patient.")
            self.lose_sanity(8)
            self.hurt(3)
        print("\n")

    def devils_deck_gambling(self):
        """Devil's Deck cheats at a card game"""
        type.type("A man outside the bar is running a three-card monte. His hands are fast, but his eyes are smug.")
        print("\n")
        type.type(quote("Find the queen, win fifty bucks. Easy money. Unless your eyes aren't fast enough."))
        print("\n")
        if self.has_item("Devil's Deck") or self.has_item("Cheater's Insurance"):
            used = "Cheater's Insurance" if self.has_item("Cheater's Insurance") else "Devil's Deck"
            type.type("You touch the " + cyan(bright(used)) + " in your pocket. The cards on the table SHIFT. Not visibly — but you FEEL which one is the queen.")
            print("\n")
            type.type("You point. He flips. Queen. His smile dies.")
            print("\n")
            type.type("You point again. Queen again. His hands start shaking.")
            print("\n")
            type.type(quote("Best of three?") + " you ask. He packs up and leaves. You already won $100.")
            self.change_balance(100)
            self.restore_sanity(5)
        else:
            type.type("You play. You lose $20. His hands are faster than they looked.")
            self.change_balance(-20)
            self.lose_sanity(2)
        print("\n")

    def fortune_cards_warning(self):
        """Fortune Cards predict danger"""
        type.type("Nothing special about this morning. Coffee. Road. Silence.")
        print("\n")
        if self.has_item("Fortune Cards") or self.has_item("Fate Reader"):
            used = "Fate Reader" if self.has_item("Fate Reader") else "Fortune Cards"
            type.type("The " + cyan(bright(used)) + " deals itself. Three cards. Past. Present. Future.")
            print("\n")
            type.type("The Future card shows a red highway and a jackknifed truck. The image is clear. Unmistakable.")
            print("\n")
            type.type("You take the next exit. Twenty minutes later, you hear sirens. A truck jackknifed on the highway you left. The card goes blank.")
            self.restore_sanity(8)
        else:
            type.type("You drive the highway. Traffic stops. A truck jackknifed ahead. You sit for two hours.")
            self.lose_sanity(3)
        print("\n")

    def blackmail_letter_extortion(self):
        """Blackmail Letter extracts money from a wealthy NPC"""
        type.type("The businessman at the diner is sweating. His tie is loose, his phone won't stop buzzing, and he's muttering about a 'situation.'")
        print("\n")
        type.type("You overhear enough. He's in trouble. Big trouble. The kind with consequences.")
        print("\n")
        if self.has_item("Blackmail Letter"):
            type.type("You slide the " + cyan(bright("Blackmail Letter")) + " across his table. Unsigned. Elegant. Terrifying.")
            print("\n")
            type.type("He reads it. Goes white. Reads it again.")
            print("\n")
            type.type(quote("How much?") + " he whispers.")
            print("\n")
            payout = random.randint(200, 500)
            type.type("You name a number. " + green("${:,}".format(payout)) + ". He pays without blinking. Slides the cash across like it burns.")
            self.change_balance(payout)
            self.use_item("Blackmail Letter")
            self.lose_sanity(3)  # You feel dirty
        else:
            type.type("You mind your own business. The businessman makes a call, throws cash on the table, and leaves in a hurry.")
            print("\n")
            type.type("Whatever his 'situation' was, it wasn't yours. That's probably for the best.")
            self.restore_sanity(1)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # NEW CRAFTED ITEM EVENTS — LUXURY
    # ══════════════════════════════════════════════════════════════════════

    def kingpin_look_respect(self):
        """Kingpin Look commands criminal respect"""
        type.type("The alley shortcut you usually take is occupied. Three men in leather, watching the entrance like bouncers.")
        print("\n")
        type.type("They see you. One straightens up. Time to see if they charge admission.")
        print("\n")
        if self.has_item("Kingpin Look"):
            type.type("The " + cyan(bright("Kingpin Look")) + " does the talking. Gold chain catches the streetlight. Cigar smoke drifts.")
            print("\n")
            type.type("The lead man's posture changes. His chin drops slightly. Involuntary. Respect.")
            print("\n")
            type.type(quote("Boss.") + " He nods. Steps aside. The other two follow. You walk through like you own the alley.")
            print("\n")
            type.type("You don't own the alley. You own a " + cyan(bright("Kingpin Look")) + ". Close enough.")
            self.restore_sanity(5)
        elif self.has_item("Brass Knuckles"):
            type.type("Your gloved hand flexes. The metal shines. They notice.")
            print("\n")
            type.type("Minimal nod. They let you pass. Respect earned through implied violence.")
            self.restore_sanity(3)
        else:
            type.type("They block the path. " + quote("Toll's twenty bucks."))
            print("\n")
            answer = ask.yes_or_no("Pay $20? ")
            if answer == "yes":
                self.change_balance(-20)
                type.type("They step aside. You feel like a sucker.")
                self.lose_sanity(2)
            else:
                type.type("You turn around. The long way it is. Twenty extra minutes and a bruised ego.")
                self.lose_sanity(3)
        print("\n")

    def heirloom_set_recognition(self):
        """Heirloom Set grants old money treatment"""
        type.type("An antique store. The kind with a doorbell that actually chimes and a proprietor who actually looks over their glasses at you.")
        print("\n")
        type.type("The proprietor is already formulating a polite " + quote("Can I help you find the door?"))
        print("\n")
        if self.has_item("Heirloom Set"):
            type.type("Then they spot the " + cyan(bright("Heirloom Set")) + ". The watch on your wrist. The pen in your pocket.")
            print("\n")
            type.type("Their entire demeanor shifts. The glasses come OFF. " + quote("Oh. My. That watch. Is that a...?"))
            print("\n")
            type.type("You say nothing. You've learned that saying nothing with expensive accessories says everything.")
            print("\n")
            type.type("They offer you tea. REAL tea. They show you the back room. The stuff that isn't for sale. Except to you, apparently.")
            payout = random.randint(50, 150)
            self.change_balance(payout)
            type.type(" You buy low and sell high. " + green("+${:,}".format(payout)) + " profit from knowing which fork is for fish.")
            self.restore_sanity(5)
        else:
            type.type("The proprietor watches you touch things you can't afford and silently wills you to leave.")
            print("\n")
            type.type("You leave. The doorbell chimes again. It sounded judgmental.")
            self.lose_sanity(2)
        print("\n")

    def luck_totem_windfall(self):
        """Luck Totem creates passive luck effects"""
        type.type("Walking across the parking lot. Nothing special. Same cracks in the asphalt.")
        print("\n")
        if self.has_item("Luck Totem") or self.has_item("Fortune's Favor") or self.has_item("Gambler's Aura"):
            if self.has_item("Gambler's Aura"):
                used = "Gambler's Aura"
            elif self.has_item("Fortune's Favor"):
                used = "Fortune's Favor"
            else:
                used = "Luck Totem"
            type.type("The " + cyan(bright(used)) + " vibrates in your pocket. Then you look down.")
            print("\n")
            loot = random.choice([20, 20, 50, 50, 100])
            type.type("A " + green("${:,}".format(loot)) + " bill. On the ground. Just sitting there.")
            print("\n")
            type.type("You pick it up. Then you see the scratch ticket under it. You scratch it. " + green("$" + str(random.randint(5, 50))) + ". Winner.")
            print("\n")
            type.type("The totem is warm. The universe is paying its tab.")
            self.change_balance(loot)
            self.restore_sanity(5)
        else:
            type.type("You step on a piece of gum. It sticks to your shoe. It's the expensive kind that never comes off.")
            self.lose_sanity(1)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # NEW CRAFTED ITEM EVENTS — VEHICLE
    # ══════════════════════════════════════════════════════════════════════

    def tire_ready_flat(self):
        """Tire Ready Kit handles a flat tire"""
        type.type("BANG. The car lurches right. You grip the wheel. Flat tire. Of course.")
        print("\n")
        if self.has_item("Tire Ready Kit") or self.has_item("Roadside Shield"):
            used = "Roadside Shield" if self.has_item("Roadside Shield") else "Tire Ready Kit"
            type.type("The " + cyan(bright(used)) + " is pre-assembled. Jack mounted, spare ready, bolts checked.")
            print("\n")
            type.type("Four minutes. Changed. Done. You're back on the road before the sweat dries.")
            self.restore_sanity(5)
        elif self.has_item("Mobile Workshop"):
            type.type("The " + cyan(bright("Mobile Workshop")) + " has everything you need. It takes ten minutes but the tire holds.")
            self.restore_sanity(3)
        else:
            type.type("No jack. No spare. No plan.")
            print("\n")
            type.type("You call for help. It takes two hours. The sun bakes you the entire time.")
            cost = random.randint(40, 100)
            self.change_balance(-cost)
            type.type(" The tow costs " + red("${:,}".format(cost)) + ".")
            self.lose_sanity(4)
            self.hurt(3)
        print("\n")

    def miracle_lube_breakdown(self):
        """Miracle Lube prevents or fixes a mechanical failure"""
        type.type("The engine makes a noise it has never made before. A grinding, metallic complaint from deep in the block.")
        print("\n")
        type.type("This is the noise that precedes expensive repair bills and long walks.")
        print("\n")
        if self.has_item("Miracle Lube") or self.has_item("Auto Mechanic"):
            used = "Auto Mechanic" if self.has_item("Auto Mechanic") else "Miracle Lube"
            type.type("You pop the hood and apply " + cyan(bright(used)) + " to every moving part you can find.")
            print("\n")
            type.type("The grinding stops. The engine smooths out. That color-that-doesn't-exist-in-nature just saved you a mechanic visit.")
            self.restore_sanity(5)
        elif self.has_item("Mobile Workshop"):
            type.type("Your " + cyan(bright("Mobile Workshop")) + " has the tools. You tighten, adjust, and pray.")
            print("\n")
            type.type("The noise fades to a whisper. Good enough to keep driving. Barely.")
            self.restore_sanity(2)
        else:
            type.type("You drive on it anyway. The noise gets worse. Much worse. Then it gets QUIET.")
            print("\n")
            type.type("That's worse. That's the noise of something that gave up.")
            cost = random.randint(80, 200)
            self.change_balance(-cost)
            type.type(" Mechanic charges " + red("${:,}".format(cost)) + ".")
            self.lose_sanity(5)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # NEW CRAFTED ITEM EVENTS — TIER 2+ MASTERWORKS
    # ══════════════════════════════════════════════════════════════════════

    def road_warrior_ambush(self):
        """Road Warrior Armor makes you untouchable in combat"""
        type.type("An ambush. Two men with bats. They step out from behind a dumpster like this is a movie and they've rehearsed.")
        print("\n")
        type.type(quote("Wrong place, wrong time, friend."))
        print("\n")
        if self.has_item("Road Warrior Armor") or self.has_item("Beastslayer Mantle"):
            used = "Beastslayer Mantle" if self.has_item("Beastslayer Mantle") else "Road Warrior Armor"
            type.type("You turn to face them. The " + cyan(bright(used)) + " catches the light. Three weapons. Metal and fire and edges.")
            print("\n")
            type.type("They see the armor. They see what's attached to it. They look at each other.")
            print("\n")
            type.type("The bats lower. Then drop. " + quote("Wrong... we got the wrong guy. Sorry. Sorry, man."))
            print("\n")
            type.type("They leave faster than they arrived. You didn't even speak.")
            self.restore_sanity(10)
        elif self.has_item("Assassin's Kit"):
            type.type("The " + cyan(bright("Assassin's Kit")) + " comes out. Shiv and spray. They hesitate. You don't.")
            print("\n")
            type.type("Thirty seconds later, one is pepper-sprayed and the other is reconsidering his career. You walk away untouched.")
            self.restore_sanity(5)
        else:
            type.type("First bat catches your shoulder. Second gets your ribs. You go down, they take what they want, and you lie there.")
            print("\n")
            lost = min(random.randint(30, 80), self._balance)
            if lost > 0:
                self.change_balance(-lost)
                type.type("They got " + red("${:,}".format(lost)) + ".")
            self.hurt(15)
            self.lose_sanity(8)
        print("\n")

    def third_eye_foresight(self):
        """Third Eye shows outcomes before choosing"""
        type.type("Two strangers approach. One offers directions to a shortcut. The other says the shortcut is a trap.")
        print("\n")
        type.type("Both are convincing. Both could be lying.")
        print("\n")
        if self.has_item("Third Eye") or self.has_item("Seer's Chronicle"):
            used = "Seer's Chronicle" if self.has_item("Seer's Chronicle") else "Third Eye"
            type.type("The " + cyan(bright(used)) + " hums. The shimmer appears around both strangers.")
            print("\n")
            type.type("The first stranger shimmers red. Danger. The second shimmers green. Truth.")
            print("\n")
            type.type("You follow the second stranger's advice. The shortcut IS a trap — and you just avoided it.")
            type.type(" The true path leads to a rest stop with supplies and cash.")
            loot = random.randint(40, 120)
            self.change_balance(loot)
            self.restore_sanity(8)
        elif self.has_item("Fortune Cards"):
            type.type("The " + cyan(bright("Fortune Cards")) + " deal themselves. The first stranger's card shows a skull.")
            type.type(" That's... clear enough.")
            loot = random.randint(20, 60)
            self.change_balance(loot)
            self.restore_sanity(4)
        else:
            choice = random.randrange(2)
            if choice == 0:
                type.type("You pick wrong. The shortcut leads to a dead end where two more strangers are waiting. This was a setup.")
                lost = min(random.randint(20, 60), self._balance)
                if lost > 0:
                    self.change_balance(-lost)
                self.hurt(8)
                self.lose_sanity(5)
            else:
                type.type("You pick right. Lucky guess. The shortcut saves you an hour and you find a rest stop.")
                loot = random.randint(10, 40)
                self.change_balance(loot)
                self.restore_sanity(2)
        print("\n")

    def ghost_protocol_invisible(self):
        """Ghost Protocol makes you invisible to tracking"""
        type.type("Someone's asking about you. The gas station attendant, the motel clerk, the diner waitress — they've all been approached.")
        print("\n")
        type.type(quote("Tall guy? Drives a station wagon? Seen him?"))
        print("\n")
        if self.has_item("Ghost Protocol") or self.has_item("Phantom Rose"):
            used = "Phantom Rose" if self.has_item("Phantom Rose") else "Ghost Protocol"
            type.type("The " + cyan(bright(used)) + " is active. The attendant looks right at you. Through you.")
            print("\n")
            type.type(quote("Nah. Haven't seen nobody like that.") + " He means it. He's LOOKING at you and doesn't recognize you.")
            print("\n")
            type.type("The men asking leave. They drove right past your car in the parking lot. Something about you is just... irrelevant. Forgettable. Safe.")
            self.restore_sanity(10)
        elif self.has_item("New Identity"):
            type.type("The " + cyan(bright("New Identity")) + " holds. " + quote("Nope, just Michael Torres here. He's a tourist."))
            print("\n")
            type.type("They leave. Michael Torres lives another day.")
            self.restore_sanity(5)
        else:
            type.type("The attendant points at your car. The men walk toward it. You see them from the bathroom window.")
            print("\n")
            type.type("You slip out the back. Take a different route. Sleep somewhere else tonight.")
            self.lose_sanity(6)
        print("\n")

    def immortal_vehicle_breakdown(self):
        """Immortal Vehicle prevents all car trouble"""
        type.type("The dashboard lights up like a Christmas tree. Engine light. Oil light. Battery light. Temperature light. All at once.")
        print("\n")
        type.type("This is the moment every driver fears. The simultaneous system failure.")
        print("\n")
        if self.has_item("Immortal Vehicle") or self.has_item("War Wagon"):
            used = "War Wagon" if self.has_item("War Wagon") else "Immortal Vehicle"
            type.type("The " + cyan(bright(used)) + " hums. The dashboard lights flicker... and go out. One by one.")
            print("\n")
            type.type("The car diagnosed itself. The car FIXED itself. The engine smooths. The temperature drops. The battery stabilizes.")
            print("\n")
            type.type("The dashboard blinks twice. You'd swear it was winking at you.")
            self.restore_sanity(8)
        elif self.has_item("Auto Mechanic"):
            type.type("Your " + cyan(bright("Auto Mechanic")) + " setup handles three of the four. The fourth requires prayer. The prayer works.")
            self.restore_sanity(4)
        else:
            type.type("You pull over. Pop the hood. Stare at an engine you don't understand making noises you can't diagnose.")
            print("\n")
            cost = random.randint(100, 300)
            type.type("The tow truck takes two hours. The mechanic charges " + red("${:,}".format(cost)) + ". The day is ruined.")
            self.change_balance(-cost)
            self.lose_sanity(6)
        print("\n")

    def gamblers_aura_blackjack(self):
        """Gambler's Aura affects a random gambling opportunity"""
        type.type("A man at the gas station is shuffling cards. " + quote("Quick game? Five-card draw, twenty bucks buy-in."))
        print("\n")
        if self.has_item("Gambler's Aura") or self.has_item("Moonlit Fortune"):
            used = "Moonlit Fortune" if self.has_item("Moonlit Fortune") else "Gambler's Aura"
            type.type("The " + cyan(bright(used)) + " warms against your chest. Luck isn't a feeling anymore. It's physics.")
            print("\n")
            type.type("You sit. He deals. Your hand is perfect. His hand is pathetic. He didn't know the game was decided before the shuffle.")
            loot = random.randint(50, 200)
            self.change_balance(loot)
            type.type("\nYou walk away " + green("+${:,}".format(loot)) + " richer. The universe settling its debt.")
            self.restore_sanity(5)
        elif self.has_item("Devil's Deck"):
            type.type("The " + cyan(bright("Devil's Deck")) + " in your pocket whispers. You know which cards he's holding.")
            loot = random.randint(30, 100)
            self.change_balance(loot)
            type.type("\nYou win " + green("+${:,}".format(loot)) + ". The face cards grin.")
            self.restore_sanity(3)
        else:
            type.type("You play an honest hand. It's a coin flip.")
            if random.randrange(2) == 0:
                loot = random.randint(15, 40)
                self.change_balance(loot)
                type.type(" You win " + green("${:,}".format(loot)) + ". Not bad.")
                self.restore_sanity(2)
            else:
                self.change_balance(-20)
                type.type(" You lose $20. Bad cards, bad luck.")
                self.lose_sanity(1)
        print("\n")

    def guardian_angel_lethal(self):
        """Guardian Angel prevents death"""
        type.type("Everything goes wrong at once. The car spins. The world rotates. Glass breaks. Metal screams.")
        print("\n")
        type.type("Silence. Then pain. Then the realization that this might be the end.")
        print("\n")
        if self.has_item("Guardian Angel") or self.has_item("Last Breath Locket"):
            used = "Last Breath Locket" if self.has_item("Last Breath Locket") else "Guardian Angel"
            type.type("The " + cyan(bright(used)) + " activates. Three signals fire simultaneously. The locket burns warm against your chest.")
            print("\n")
            type.type("First responders arrive in eight minutes. You should be dead. You're not. The paramedic can't explain it.")
            print("\n")
            type.type(quote("I've never seen someone walk away from that.") + " You didn't walk. You were CARRIED. But you're alive.")
            self.heal(999)  # Full heal
            self.restore_sanity(15)
        else:
            type.type("You crawl from the wreck. Everything hurts. Your vision swims. But you're breathing.")
            print("\n")
            type.type("It takes forty minutes for someone to stop. The hospital takes what's left of your money.")
            self.hurt(30)
            self.lose_sanity(10)
            cost = min(random.randint(100, 300), self._balance)
            if cost > 0:
                self.change_balance(-cost)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 45A — REWRITTEN DISGUISE EVENTS
    # ══════════════════════════════════════════════════════════════════════

    def low_profile_casino_blend(self):
        """Low-Profile Outfit makes you invisible — too invisible — at a casino"""
        type.type("The casino floor buzzes with energy. Lights, sounds, the constant shuffle of chips.")
        print("\n")
        if self.has_item("Low-Profile Outfit") or self.has_item("New Identity"):
            outfit = "New Identity" if self.has_item("New Identity") else "Low-Profile Outfit"
            type.type("In your " + cyan(bright(outfit)) + ", you're invisible. TOO invisible. A cocktail waitress hands you a tray of drinks.")
            print("\n")
            type.type(quote("Table seven needs these, sweetie. Chop chop.") + " She thinks you're STAFF.")
            print("\n")
            choice = random.randrange(2)
            if choice == 0:
                type.type("You deliver the drinks. Table seven is the VIP room. You overhear a whale discussing tomorrow's private game.")
                print("\n")
                type.type("The tip? " + quote("The back room opens at midnight. Password is 'Atlas.'"))
                self.change_balance(random.randint(50, 150))
                self.restore_sanity(5)
            else:
                type.type("You set the tray down and slip to the high-roller table. One hand at maximum stakes before anyone notices.")
                print("\n")
                winnings = random.choice([-200, -100, 0, 100, 200, 500])
                if winnings >= 0:
                    type.type("You win " + green("${:,}".format(winnings)) + " and vanish before the pit boss looks twice.")
                else:
                    type.type("You lose " + red("${:,}".format(abs(winnings))) + " and vanish before the pit boss looks twice. Expensive invisibility.")
                self.change_balance(winnings)
        else:
            type.type("A pit boss locks eyes with you. " + quote("You. Table three. You've been sitting there for two hours without betting."))
            print("\n")
            type.type(quote("This isn't a library. Play or leave.") + " You leave. Embarrassing.")
            self.lose_sanity(3)
        print("\n")

    def low_profile_police_encounter(self):
        """Low-Profile Outfit creates mistaken identity at a police checkpoint"""
        type.type("Police checkpoint. Three cruisers. They're checking everyone.")
        print("\n")
        if self.has_item("Low-Profile Outfit") or self.has_item("New Identity"):
            outfit = "New Identity" if self.has_item("New Identity") else "Low-Profile Outfit"
            type.type("The cop glances at your " + cyan(bright(outfit)) + " and waves you through. Then stops.")
            print("\n")
            type.type(quote("Hold on. You match a description.") + " Not YOUR description. Someone ELSE'S. Someone who owes the mob money.")
            print("\n")
            if random.randrange(2) == 0:
                type.type("You play dumb. " + quote("Must be a coincidence, officer.") + " He squints. Then waves you on.")
                print("\n")
                type.type("Crisis averted. But somewhere, the mob is looking for a man who looks exactly like you.")
                self.restore_sanity(2)
            else:
                type.type(quote("Step out of the vehicle, sir.") + " He searches the car. Finds nothing. Lets you go.")
                print("\n")
                type.type("Forty minutes lost. But you're clean. The description thing nags at you.")
                self.lose_sanity(3)
        else:
            type.type("The cop takes one look at you and pulls you over for a " + quote("routine check."))
            print("\n")
            type.type("Nothing routine about it. Twenty minutes of questions. You're free to go, but shaken.")
            self.lose_sanity(4)
        print("\n")

    def low_profile_mugging_marcus(self):
        """Low-Profile Outfit causes mistaken identity during mugging"""
        type.type("A dark alley. Someone steps out of the shadows. Knife. Classic setup.")
        print("\n")
        if self.has_item("Low-Profile Outfit") or self.has_item("New Identity"):
            outfit = "New Identity" if self.has_item("New Identity") else "Low-Profile Outfit"
            type.type("The mugger squints at your " + cyan(bright(outfit)) + ". Pauses. His knife lowers.")
            print("\n")
            type.type(quote("Marcus? Holy crap. MARCUS? It's me, Danny!") + " He puts his knife away and starts CRYING.")
            print("\n")
            type.type(quote("I thought you were dead, man. I thought you were DEAD."))
            print("\n")
            if random.randrange(3) == 0:
                type.type("You play along. Danny becomes a contact — he knows the underground. Future discounts on shady deals.")
                self.restore_sanity(5)
                self.change_balance(30)
            else:
                type.type("You hug him silently. He gives you $30 and a phone number, walks away happy. You never see Danny again.")
                self.change_balance(30)
                self.restore_sanity(3)
        else:
            type.type(quote("Empty your pockets. Now.") + " No recognition. No mercy. Just business.")
            print("\n")
            lost = random.randint(20, 80)
            type.type("You lose " + red("${:,}".format(lost)) + " and your dignity.")
            self.change_balance(-lost)
            self.lose_sanity(5)
        print("\n")

    def low_profile_shelter_meal(self):
        """Low-Profile Outfit gets you charity at a homeless shelter"""
        type.type("A church. Warm light. Volunteers at tables handing out food. The line is long.")
        print("\n")
        if self.has_item("Low-Profile Outfit") or self.has_item("New Identity"):
            outfit = "New Identity" if self.has_item("New Identity") else "Low-Profile Outfit"
            type.type("In your " + cyan(bright(outfit)) + ", a volunteer hands you a warm meal AND a sleeping bag.")
            print("\n")
            type.type(quote("We believe in second chances,") + " she says. The food is incredible. Homemade. Grandma-level.")
            print("\n")
            type.type("She also hands you a card for a job interview. It looks... real.")
            self.heal(10)
            self.restore_sanity(5)
        else:
            type.type("The volunteer hesitates. You're too well-dressed for the shelter line. People stare.")
            print("\n")
            type.type("You take the food anyway. It's still warm. Still good. Nobody says anything.")
            self.heal(5)
            self.lose_sanity(1)
        print("\n")

    def beach_bum_yacht_party(self):
        """Beach Bum Disguise gets you mistaken for entertainment at a yacht party"""
        type.type("A yacht party. Music. Champagne. Rich people doing rich people things.")
        print("\n")
        if self.has_item("Beach Bum Disguise") or self.has_item("All-Weather Armor"):
            disguise = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Beach Bum Disguise"
            type.type("In your " + cyan(bright(disguise)) + ", the host assumes you're the hired entertainment.")
            print("\n")
            type.type("A ukulele is shoved into your hands. " + quote("Play something tropical!"))
            print("\n")
            if random.randrange(2) == 0:
                type.type("You strum. It's terrible. They LOVE it. " + quote("He's so BAD it's charming!"))
                print("\n")
                tip = random.randint(50, 150)
                type.type("Tips: " + green("${:,}".format(tip)) + ". Free food all night. Best failure of your life.")
                self.change_balance(tip)
                self.restore_sanity(8)
            else:
                type.type("You strum. It's... actually beautiful? You had no idea you could play ukulele.")
                print("\n")
                tip = random.randint(150, 300)
                type.type("Standing ovation. Tips: " + green("${:,}".format(tip)) + ". The host's wife gives you her card.")
                self.change_balance(tip)
                self.restore_sanity(10)
        else:
            type.type("Security spots you immediately. " + quote("Private event, buddy. Move along."))
            self.lose_sanity(2)
        print("\n")

    def beach_bum_heatwave(self):
        """Beach Bum Disguise thrives in extreme heat"""
        type.type("The heat is brutal. 105 degrees. Pavement is soft. Dogs are refusing to walk.")
        print("\n")
        if self.has_item("Beach Bum Disguise") or self.has_item("All-Weather Armor"):
            disguise = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Beach Bum Disguise"
            type.type("Everyone wilts. You, in the " + cyan(bright(disguise)) + ", are perfectly comfortable.")
            print("\n")
            type.type("You fall asleep on a park bench. When you wake up, someone left a donation cup in front of you.")
            print("\n")
            tips = random.randint(15, 35)
            type.type("It has " + green("${:,}".format(tips)) + " in it. A passing dog also fell asleep on your lap.")
            self.change_balance(tips)
            self.restore_sanity(5)
        else:
            type.type("You sweat through your shirt in twelve minutes. Your skin feels like it's melting. This is inhuman.")
            self.hurt(8)
            self.lose_sanity(3)
        print("\n")

    def beach_bum_tribe(self):
        """Beach Bum Disguise attracts actual beach bums"""
        type.type("A group of sunburned, sandy-haired humans wave you over from a picnic table.")
        print("\n")
        if self.has_item("Beach Bum Disguise") or self.has_item("All-Weather Armor"):
            disguise = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Beach Bum Disguise"
            type.type(quote("One of us!") + " They spotted your " + cyan(bright(disguise)) + " from across the parking lot.")
            print("\n")
            type.type("They share food (questionable), wisdom (surprisingly deep), and a scheme to sneak into the water park.")
            print("\n")
            if random.randrange(5) < 4:
                type.type("The water park scheme works. You find " + green("$80") + " in the wave pool filter. Best night in weeks.")
                self.change_balance(80)
                self.restore_sanity(8)
            else:
                type.type("Security catches you in the wave pool. " + quote("Again?") + " The fine is $40. Worth it.")
                self.change_balance(-40)
                self.restore_sanity(3)
        else:
            type.type("They look you up and down. " + quote("Tourist.") + " They turn away. You eat lunch alone.")
            self.lose_sanity(2)
        print("\n")

    def gas_mask_toxic_spill(self):
        """Gas Mask lets you walk through toxic spill for rewards"""
        type.type("The intersection is blocked. Green liquid pooling from an overturned truck. HAZMAT tape everywhere.")
        print("\n")
        type.type("Everyone is evacuating. The air burns your eyes from a block away.")
        print("\n")
        if self.has_item("Gas Mask") or self.has_item("Hazmat Suit"):
            mask = "Hazmat Suit" if self.has_item("Hazmat Suit") else "Gas Mask"
            type.type("You strap on the " + cyan(bright(mask)) + " and walk straight in. Pine-scented air while the world chokes.")
            print("\n")
            if random.randrange(3) == 0:
                type.type("You find the truck driver unconscious. Drag him to safety. He's a chemical company exec.")
                print("\n")
                reward = random.randint(200, 400)
                type.type("Grateful beyond words. " + green("${:,}".format(reward)) + " reward and his business card.")
                self.change_balance(reward)
                self.restore_sanity(5)
            else:
                loot = random.randint(100, 300)
                type.type("The unguarded truck has scattered crates of industrial chemicals. You grab what you can carry.")
                print("\n")
                type.type("Pawnable for " + green("${:,}".format(loot)) + ". Nobody's watching. Nobody CAN watch — they can't breathe.")
                self.change_balance(loot)
                self.lose_sanity(1)
        else:
            type.type("You turn around with everyone else. The detour adds an hour. Your eyes water for two.")
            self.hurt(3)
            self.lose_sanity(3)
        print("\n")

    def gas_mask_fire_rescue(self):
        """Gas Mask lets you enter a burning building"""
        type.type("Smoke. Thick, black, rolling out of a building's windows. Sirens in the distance, but not here yet.")
        print("\n")
        if self.has_item("Gas Mask") or self.has_item("Hazmat Suit"):
            mask = "Hazmat Suit" if self.has_item("Hazmat Suit") else "Gas Mask"
            type.type("You pull on the " + cyan(bright(mask)) + ". Everyone runs OUT. You walk IN.")
            print("\n")
            type.type("Through the smoke: a safe, door open. Someone left in a hurry. Also: a cat on a shelf, meowing.")
            print("\n")
            choice = random.randrange(3)
            if choice == 0:
                loot = random.randint(200, 500)
                type.type("You grab the safe's contents. " + green("${:,}".format(loot)) + " in cash and documents. The cat hisses at you on the way out.")
                self.change_balance(loot)
                self.lose_sanity(2)
            elif choice == 1:
                type.type("You save the cat. Its owner is the building manager. Eternal gratitude, free roof access.")
                self.restore_sanity(8)
            else:
                loot = random.randint(100, 250)
                type.type("You grab the cash AND the cat. You trip. Drop half the money. The cat scratches your face.")
                print("\n")
                type.type("The firefighters find you holding " + green("${:,}".format(loot)) + ", a cat, and a bleeding face. They have questions.")
                self.change_balance(loot)
                self.hurt(5)
                self.restore_sanity(3)
        else:
            type.type("You stand outside with everyone else, watching it burn. Someone is crying about their cat.")
            self.lose_sanity(3)
        print("\n")

    def storm_suit_hurricane(self):
        """Storm Suit makes you a human anchor in a hurricane"""
        type.type("Wind that screams. Rain that flies sideways. Trees bending at impossible angles.")
        print("\n")
        if self.has_item("Storm Suit") or self.has_item("All-Weather Armor"):
            suit = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Storm Suit"
            type.type("You stand in the " + cyan(bright(suit)) + " like a lighthouse. The wind hits you and slides off.")
            print("\n")
            type.type("Then a lawn chair hits you. Then a PERSON. They grab onto you because you're the only thing not moving.")
            print("\n")
            type.type(quote("DON'T LET GO!") + " You are a human anchor.")
            print("\n")
            if random.randrange(3) == 0:
                reward = random.randint(100, 200)
                type.type("After the storm: the person is a contractor. " + green("${:,}".format(reward)) + " for saving their life.")
                self.change_balance(reward)
            else:
                type.type("After the storm: they offer you $150. You refuse. They remember your face forever.")
            self.restore_sanity(8)
        else:
            type.type("You hunker in the car. It rocks. It slides. Something hits the windshield and stars it.")
            self.hurt(12)
            self.lose_sanity(5)
        print("\n")

    def storm_suit_flood(self):
        """Storm Suit protects during flash flood"""
        type.type("The water rises fast. Ankle-deep becomes knee-deep in minutes. Cars start floating.")
        print("\n")
        if self.has_item("Storm Suit") or self.has_item("All-Weather Armor"):
            suit = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Storm Suit"
            type.type("The " + cyan(bright(suit)) + " is waterproof and heavy. You wade through while others scramble for high ground.")
            print("\n")
            type.type("A submerged car ahead — trunk popped open. Something glints inside.")
            print("\n")
            loot = random.randint(80, 250)
            type.type("You reach in. " + green("${:,}".format(loot)) + " in a waterproof bag. Someone's emergency fund.")
            self.change_balance(loot)
            self.hurt(5)
            self.restore_sanity(3)
        else:
            type.type("The water reaches the door panels. You climb onto the roof. Wait. Shiver. Pray.")
            self.hurt(10)
            self.lose_sanity(6)
        print("\n")

    def storm_suit_night_bear(self):
        """Storm Suit makes you sound like a bear at night"""
        type.type("Cold night. Rain. The kind of weather that makes you question every life choice.")
        print("\n")
        if self.has_item("Storm Suit") or self.has_item("All-Weather Armor"):
            suit = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Storm Suit"
            type.type("The " + cyan(bright(suit)) + " traps your body heat perfectly. Warm while the world freezes.")
            print("\n")
            type.type("But the rustling waterproof fabric sounds like something MOVING through leaves.")
            print("\n")
            if random.randrange(4) == 0:
                type.type("A security guard flashlights your location. " + quote("Is that a BEAR?") + " He's armed.")
                print("\n")
                if self.has_item("Forged Documents"):
                    type.type("You flash your " + cyan(bright("Forged Documents")) + ". He apologizes and leaves you a coffee.")
                    self.restore_sanity(3)
                else:
                    type.type("You wave your hands. " + quote("Just a guy in a raincoat!") + " He's unconvinced but leaves.")
                    self.lose_sanity(2)
            else:
                type.type("Nobody bothers you. The rain doesn't touch you. For one night, weather is someone else's problem.")
                self.restore_sanity(5)
        else:
            type.type("You shiver through the night. Every raindrop is a tiny needle of misery.")
            self.hurt(8)
            self.lose_sanity(4)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 45B — REWRITTEN TONIC & CONSUMABLE EVENTS
    # ══════════════════════════════════════════════════════════════════════

    def antacid_business_dinner(self):
        """Antacid Brew saves you at a business dinner gone wrong"""
        type.type("The business dinner starts well. Steak. Wine. Handshakes. Then the oysters arrive.")
        print("\n")
        type.type("Something about the third oyster was... off. Your stomach immediately declares war.")
        print("\n")
        if self.has_item("Antacid Brew"):
            type.type("You excuse yourself, chug the " + cyan(bright("Antacid Brew")) + " in the bathroom, and return like nothing happened.")
            print("\n")
            type.type("Your stomach surrenders. The deal closes. " + quote("You're unshakeable,") + " they say. They have no idea.")
            self.change_balance(random.randint(100, 250))
            self.restore_sanity(5)
        else:
            type.type("You excuse yourself. You don't come back for thirty minutes. The deal is dead. So is your dignity.")
            self.lose_sanity(8)
            self.hurt(5)
        print("\n")

    def outdoor_shield_farmer(self):
        """Outdoor Shield makes you bug-proof, impressing a farmer"""
        type.type("A farmer waves you over. " + quote("Can you hold this fence post while I hammer?"))
        print("\n")
        type.type("The field is ALIVE with mosquitoes. A cloud of them. Biblical plague levels.")
        print("\n")
        if self.has_item("Outdoor Shield") or self.has_item("All-Weather Armor"):
            shield = "All-Weather Armor" if self.has_item("All-Weather Armor") else "Outdoor Shield"
            type.type("The " + cyan(bright(shield)) + " does its work. Mosquitoes approach, pivot six inches away, and crash into each other.")
            print("\n")
            type.type("The farmer stares. " + quote("How are you not getting eaten alive?"))
            print("\n")
            pay = random.randint(30, 80)
            type.type("He pays you " + green("${:,}".format(pay)) + " and gives you a jar of his homemade honey. " + quote("Bug-proof AND useful."))
            self.change_balance(pay)
            self.heal(3)
            self.restore_sanity(3)
        else:
            type.type("You hold the post for ten minutes. You get bitten 47 times. The farmer gets bitten 3 times.")
            print("\n")
            type.type(quote("City folk,") + " he mutters. He gives you $10 for your trouble and your blood sacrifice.")
            self.change_balance(10)
            self.hurt(5)
        print("\n")

    def cool_down_car_overheat(self):
        """Cool Down Kit saves an overheating car"""
        type.type("Steam. Hissing from under the hood. The temperature gauge is past red — it's in territory the gauge wasn't designed for.")
        print("\n")
        if self.has_item("Cool Down Kit"):
            type.type("You pop the hood and apply the " + cyan(bright("Cool Down Kit")) + " to the radiator cap area.")
            print("\n")
            if random.randrange(4) == 0:
                type.type("The pressure releases too fast. A gasket cracks. But the engine cools. Trade-offs.")
                self.change_balance(-random.randint(50, 100))
            else:
                type.type("The engine temperature drops like someone hit a reset button. The gauge retreats to normal.")
                print("\n")
                type.type("Mechanic would charge $200 for what you just did with a homemade cooling paste.")
                self.restore_sanity(5)
        else:
            type.type("You wait. For an hour. In the sun. The engine cools on its own schedule, not yours.")
            self.lose_sanity(4)
            self.hurt(3)
        print("\n")

    def smoke_flare_pursuit(self):
        """Smoke Flare covers an escape or creates chaos"""
        type.type("They're following you. Two cars back but definitely following. The same sedan for six blocks.")
        print("\n")
        if self.has_item("Smoke Flare") or self.has_item("SOS Kit"):
            flare = "SOS Kit" if self.has_item("SOS Kit") else "Smoke Flare"
            type.type("You crack the " + cyan(bright(flare)) + " and toss it out the window.")
            print("\n")
            type.type("Thick, angry smoke billows. You can't see. THEY can't see. Nobody can see. Three cars behind you brake hard.")
            print("\n")
            type.type("By the time the smoke clears, you've turned twice and parked in an alley. Gone.")
            if self.has_item("Smoke Flare"):
                self.use_item("Smoke Flare")
            self.restore_sanity(8)
        else:
            type.type("You speed up. They speed up. You turn. They turn. This goes on for twenty minutes.")
            print("\n")
            type.type("Eventually they lose interest. Or find someone easier. You'll never know which.")
            self.lose_sanity(6)
        print("\n")

    def vermin_bomb_car(self):
        """Vermin Bomb clears an infestation from your car"""
        type.type("Something scratches under the dashboard. Something LIVES in your car. Multiple somethings.")
        print("\n")
        type.type("A rat appears on the passenger seat. Looks at you. Doesn't run.")
        print("\n")
        if self.has_item("Vermin Bomb"):
            type.type("You crack the " + cyan(bright("Vermin Bomb")) + ", toss it in the back seat, and close all the doors.")
            print("\n")
            type.type("Thirty seconds of VIOLENCE from inside the car. Then silence. Then a smell that could strip paint.")
            print("\n")
            type.type("The car is rat-free. Also human-free, for the next hour. That smell is NOT leaving soon.")
            self.use_item("Vermin Bomb")
            self.restore_sanity(5)
            self.lose_sanity(1)
        else:
            type.type("You and the rat stare at each other. It wins. You sleep on the hood tonight.")
            self.lose_sanity(5)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 45C — REWRITTEN LUXURY EVENTS
    # ══════════════════════════════════════════════════════════════════════

    def enchanted_vintage_party(self):
        """Enchanted Vintage transforms a social gathering"""
        type.type("A gathering. People milling. The food is decent, the conversation is not.")
        print("\n")
        if self.has_item("Enchanted Vintage") or self.has_item("Master of Games"):
            vintage = "Master of Games" if self.has_item("Master of Games") else "Enchanted Vintage"
            type.type("You uncork the " + cyan(bright(vintage)) + ". The room shifts. People turn toward the scent.")
            print("\n")
            type.type("One sip and the host's eyes widen. " + quote("Where did you get this? This is BETTER than the 2003 Margaux."))
            print("\n")
            tip = random.randint(80, 250)
            type.type("By the end of the night, you're the most popular person in the room. Tips and favors: " + green("${:,}".format(tip)) + ".")
            self.change_balance(tip)
            self.restore_sanity(8)
        else:
            type.type("You sip cheap wine from a plastic cup. The host looks at you with pity. You leave early.")
            self.lose_sanity(2)
        print("\n")

    def aristocrat_cold_elegance(self):
        """Aristocrat's Touch keeps you warm and dignified in the cold"""
        type.type("Bitter cold. Everyone hunches, shivers, speeds up. The world looks miserable.")
        print("\n")
        if self.has_item("Aristocrat's Touch") or self.has_item("Old Money Identity"):
            item = "Old Money Identity" if self.has_item("Old Money Identity") else "Aristocrat's Touch"
            type.type("The " + cyan(bright(item)) + " — silk layers and leather gloves — keeps you warm with impossible elegance.")
            print("\n")
            type.type("You walk through the cold like it's a mild inconvenience. People stare. A woman stops you.")
            print("\n")
            type.type(quote("Excuse me, are you someone famous?") + " You smile. " + quote("Not yet."))
            self.restore_sanity(5)
            if random.randrange(3) == 0:
                type.type(" She insists on buying you coffee. The barista gives you the VIP cup.")
                self.heal(3)
        else:
            type.type("You shiver like everyone else. Nothing special about freezing to death.")
            self.hurt(5)
            self.lose_sanity(2)
        print("\n")

    def power_move_intimidation(self):
        """Power Move Kit intimidates during a confrontation"""
        type.type("Someone is in your face. Literally. Chest puffed, voice raised, finger pointing.")
        print("\n")
        if self.has_item("Power Move Kit") or self.has_item("King of the Road"):
            kit = "King of the Road" if self.has_item("King of the Road") else "Power Move Kit"
            type.type("You reach into your pocket. Pull out the " + cyan(bright(kit)) + "'s lighter. Snap. Light. Cigar catches.")
            print("\n")
            type.type("You take a long, deliberate drag. Blow smoke upward. Then look at them.")
            print("\n")
            type.type("Their mouth closes. The finger drops. Something about the snap-light-lean routine short-circuits aggression.")
            print("\n")
            type.type(quote("...You know what? Forget it.") + " They walk away. Power is a performance, and you just gave the Oscar clip.")
            self.restore_sanity(8)
        else:
            type.type("You stand your ground. They push. You push back. It escalates badly.")
            self.hurt(10)
            self.lose_sanity(5)
        print("\n")

    def animal_magnetism_recruit(self):
        """Animal Magnetism cologne attracts both animals and people"""
        type.type("You're walking past a park when a dog breaks free from its leash and runs straight at you.")
        print("\n")
        if self.has_item("Animal Magnetism") or self.has_item("Beast Tamer Kit"):
            item = "Beast Tamer Kit" if self.has_item("Beast Tamer Kit") else "Animal Magnetism"
            type.type("The " + cyan(bright(item)) + " works its magic. The dog skids to a halt and sits at your feet, tail wagging.")
            print("\n")
            type.type("Its owner runs up, breathless. " + quote("He NEVER does that. He hates strangers."))
            print("\n")
            if random.randrange(2) == 0:
                type.type("She's so impressed she invites you to the dog park social. Free food, connections, and a very loyal new dog friend.")
                self.restore_sanity(8)
                self.change_balance(random.randint(20, 50))
            else:
                type.type("Three more dogs appear. Then a cat. Then a pigeon lands on your shoulder.")
                print("\n")
                type.type("You're Dr. Dolittle now. The park-goers film you. It goes local viral. You're 'The Animal Guy.'")
                self.restore_sanity(10)
        else:
            type.type("The dog barks at you. Its owner apologizes. You move on. The dog barks again from a block away.")
            self.lose_sanity(1)
        print("\n")

    def animal_magnetism_predator(self):
        """Animal Magnetism cologne confuses a predator"""
        type.type("A coyote on the trail ahead. Not aggressive. Curious. Testing the wind.")
        print("\n")
        if self.has_item("Animal Magnetism") or self.has_item("Beast Tamer Kit"):
            item = "Beast Tamer Kit" if self.has_item("Beast Tamer Kit") else "Animal Magnetism"
            type.type("The " + cyan(bright(item)) + "'s scent reaches the coyote. It tilts its head. Sits down.")
            print("\n")
            type.type("It doesn't attack. It doesn't flee. It just... respects you. An understanding between species.")
            print("\n")
            type.type("The coyote escorts you to the edge of the trail and watches you leave. You nod. It nods back. Probably.")
            self.restore_sanity(5)
        else:
            type.type("The coyote bares its teeth. You back away slowly. It follows slowly. This dance goes on for a quarter mile.")
            self.lose_sanity(4)
            self.hurt(3)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 45D — REWRITTEN VEHICLE EVENTS
    # ══════════════════════════════════════════════════════════════════════

    def power_grid_dead_battery(self):
        """Power Grid jumpstarts a dead battery situation"""
        type.type("Click. Click. Click. The engine won't turn over. Dead battery. Middle of nowhere.")
        print("\n")
        if self.has_item("Power Grid") or self.has_item("Roadside Shield"):
            grid = "Roadside Shield" if self.has_item("Roadside Shield") else "Power Grid"
            type.type("You pop the trunk and pull out the " + cyan(bright(grid)) + ". Cables connected. Switch flipped.")
            print("\n")
            type.type("The dashboard lights up. The engine coughs, catches, ROARS. The distribution block you made from a lunchbox saves the day.")
            print("\n")
            type.type("A passing driver slows down to offer help, sees you already fixed it, and mouths " + quote("respect."))
            self.restore_sanity(5)
        else:
            type.type("You flag down a passing car. It takes forty minutes. The driver has cables but the wrong attitude.")
            print("\n")
            type.type(quote("$50 for the jump.") + " Highway robbery. But what choice do you have?")
            self.change_balance(-50)
            self.lose_sanity(3)
        print("\n")

    def mobile_workshop_stranger(self):
        """Mobile Workshop lets you fix a stranger's car for reward"""
        type.type("A car on the shoulder. Hood up. A person standing next to it looking like the world ended.")
        print("\n")
        if self.has_item("Mobile Workshop") or self.has_item("Auto Mechanic"):
            kit = "Auto Mechanic" if self.has_item("Auto Mechanic") else "Mobile Workshop"
            type.type("You pull over. Open the " + cyan(bright(kit)) + ". " + quote("Pop the hood. Let me look."))
            print("\n")
            type.type("Loose belt. Five-minute fix. You hand them a wrench. They hand you gratitude.")
            print("\n")
            pay = random.randint(40, 120)
            type.type(quote("I don't know how to thank you.") + " You know how: " + green("${:,}".format(pay)) + " and a handshake.")
            self.change_balance(pay)
            self.restore_sanity(5)
        else:
            type.type("You pull over. Open the hood. Stare at the engine. The engine stares back. You know nothing.")
            print("\n")
            type.type(quote("Thanks anyway,") + " they say, calling AAA. You feel useless.")
            self.lose_sanity(3)
        print("\n")

    def pursuit_package_chase(self):
        """Pursuit Package gives you an edge in a chase"""
        type.type("The rearview mirror tells a story: flashing lights. Gaining fast. This is happening.")
        print("\n")
        if self.has_item("Pursuit Package") or self.has_item("Rolling Fortress"):
            pkg = "Rolling Fortress" if self.has_item("Rolling Fortress") else "Pursuit Package"
            type.type("The " + cyan(bright(pkg)) + " kicks in. Dog whistle on the dash — you hit it.")
            print("\n")
            type.type("Every dog in a three-block radius goes BERSERK. The pursuing car swerves around six loose dogs and a very confused golden retriever.")
            print("\n")
            type.type("You take a side street. By the time they recover, you're three blocks away and invisible.")
            self.restore_sanity(8)
        else:
            type.type("You drive. They follow. The chase ends in a parking garage where you circle for ten minutes before they give up.")
            self.lose_sanity(6)
            self.hurt(3)
        print("\n")

    def pursuit_package_witness(self):
        """Pursuit Package helps you reach a scene before anyone else"""
        type.type("An accident on the highway. Smoke rising. People pulling over, but slowly. Too slowly.")
        print("\n")
        if self.has_item("Pursuit Package") or self.has_item("Rolling Fortress"):
            pkg = "Rolling Fortress" if self.has_item("Rolling Fortress") else "Pursuit Package"
            type.type("You hit the " + cyan(bright(pkg)) + "'s siren — the dog whistle modified to emit a pulse that makes drivers MOVE.")
            print("\n")
            type.type("Traffic parts. You arrive first. The driver is dazed but alive. You stabilize them until EMTs arrive.")
            print("\n")
            type.type("The news crew that shows up gets your face on camera. " + quote("Local hero saves accident victim."))
            self.restore_sanity(10)
            self.change_balance(random.randint(50, 150))
        else:
            type.type("You sit in traffic like everyone else. By the time you pass the scene, it's cleared. You'll never know.")
            self.lose_sanity(1)
        print("\n")

    # ══════════════════════════════════════════════════════════════════════
    # SECTION 44A — WILD ITEM INTERACTIONS (OFF-LABEL USES)
    # ══════════════════════════════════════════════════════════════════════

    def wild_headlamp_poker(self):
        """Headlamp accidentally reveals cards at a poker game"""
        type.type("Late night poker at a back-room table. Low stakes, high tension.")
        print("\n")
        if self.has_item("Headlamp"):
            type.type("You forgot to take off the " + cyan(bright("Headlamp")) + ". The beam catches the dealer's cards at an angle.")
            print("\n")
            type.type("For a split second, the light penetrates the card coating. You see EVERYTHING. Not cheating. Not REALLY.")
            print("\n")
            if random.randrange(5) == 0:
                type.type("The pit boss notices the glare. " + quote("What's on your head?") + " You're asked to leave. Politely. Firmly.")
                self.lose_sanity(3)
            else:
                winnings = random.randint(100, 400)
                type.type("You play the hand perfectly. " + green("${:,}".format(winnings)) + ". Nobody suspects a thing. The headlamp is your secret weapon.")
                self.change_balance(winnings)
                self.restore_sanity(3)
        else:
            type.type("You squint at your cards. Bad hand. Worse poker face. You fold and watch everyone else play.")
            self.lose_sanity(2)
        print("\n")

    def wild_emp_casino(self):
        """EMP Device kills electronic shuffler at casino"""
        type.type("The blackjack table hums with electronic precision. Automatic shuffler. Perfect randomness.")
        print("\n")
        if self.has_item("EMP Device"):
            type.type("The " + cyan(bright("EMP Device")) + " pulses in your pocket. The shuffler DIES. Sparks. Silence.")
            print("\n")
            type.type("The dealer blinks, then reaches for a manual shuffler. The old kind. The imperfect kind.")
            print("\n")
            type.type("Your odds just changed. Three hands before security traces the electronics failure.")
            winnings = random.randint(200, 800)
            type.type(" You win " + green("${:,}".format(winnings)) + " in three perfect hands.")
            self.change_balance(winnings)
            self.use_item("EMP Device")
            self.lose_sanity(2)
        else:
            type.type("The electronic shuffler is flawless. Predictable only to mathematics. You play normally.")
            self.lose_sanity(1)
        print("\n")

    def wild_radio_jammer_police(self):
        """Radio Jammer kills police backup during an encounter"""
        type.type("A cop car. Lights flashing. You're being pulled over. His partner is on the radio calling for backup.")
        print("\n")
        if self.has_item("Radio Jammer") or self.has_item("Surveillance Suite"):
            jammer = "Surveillance Suite" if self.has_item("Surveillance Suite") else "Radio Jammer"
            type.type("You flip the " + cyan(bright(jammer)) + ". The cop's radio dies mid-sentence. Static fills the cruiser.")
            print("\n")
            type.type("Dispatch hears nothing. Backup never comes. The officer alone realizes he's outgunned by silence.")
            print("\n")
            type.type("He lets you off with a warning. A very confused, very nervous warning.")
            self.restore_sanity(5)
        else:
            type.type("Backup arrives in four minutes. Two cruisers. Six officers. This is now an ordeal.")
            print("\n")
            fine = random.randint(50, 200)
            type.type("Fine: " + red("${:,}".format(fine)) + ". The whole thing takes an hour.")
            self.change_balance(-fine)
            self.lose_sanity(4)
        print("\n")

    def wild_evidence_kit_wedding(self):
        """Evidence Kit catches theft at a wedding"""
        type.type("A wedding. Beautiful. Open bar. You're photographing everything out of boredom.")
        print("\n")
        if self.has_item("Evidence Kit") or self.has_item("Intelligence Dossier"):
            kit = "Intelligence Dossier" if self.has_item("Intelligence Dossier") else "Evidence Kit"
            type.type("The " + cyan(bright(kit)) + " catches something the eye missed — the best man pocketing the ring box.")
            print("\n")
            type.type("The bride would pay $200 for that photo. The best man would pay $300 to delete it.")
            print("\n")
            if random.randrange(2) == 0:
                type.type("You show the bride. She pays " + green("$200") + " and has the best man removed. Justice served.")
                self.change_balance(200)
                self.restore_sanity(5)
            else:
                type.type("You show the best man. He pays " + green("$300") + " without a word. Silence is golden.")
                self.change_balance(300)
                self.lose_sanity(2)
        else:
            type.type("Beautiful ceremony. Decent cake. You eat three slices and leave. Nothing happened.")
            self.heal(3)
        print("\n")

    def wild_distress_beacon_casino(self):
        """Distress Beacon triggers evacuation at casino"""
        type.type("The casino floor. You're down. Way down. The cards hate you tonight.")
        print("\n")
        if self.has_item("Distress Beacon"):
            type.type("Under the table, you trigger the " + cyan(bright("Distress Beacon")) + ".")
            print("\n")
            type.type("Sixty seconds later: ambulance. Fire truck. Two cop cars. The casino evacuates in CHAOS.")
            print("\n")
            type.type("In the stampede, you pocket " + green("$500") + " in chips off the floor. Nobody's counting. Nobody CAN count.")
            self.change_balance(500)
            self.use_item("Distress Beacon")
            self.lose_sanity(5)
        else:
            type.type("You leave the table with nothing but regret and an empty wallet.")
            self.lose_sanity(4)
        print("\n")

    def wild_stink_bomb_casino_vault(self):
        """Stink Bomb triggers fire safety protocols at casino"""
        type.type("The casino floor. Packed. Loud. The perfect environment for chaos.")
        print("\n")
        if self.has_item("Stink Bomb"):
            type.type("The " + cyan(bright("Stink Bomb")) + " cracks under the table. The stench fills the floor in seconds.")
            print("\n")
            type.type("Fire alarms trigger. Sprinklers deploy. People SCATTER. In the chaos, abandoned chips litter every table.")
            print("\n")
            if random.randrange(3) == 0:
                loot = random.randint(800, 2000)
                type.type("You have exactly 90 seconds. You grab " + green("${:,}".format(loot)) + " in abandoned chips. Nobody's looking at YOU.")
                self.change_balance(loot)
                self.lose_sanity(8)
            else:
                loot = random.randint(200, 400)
                type.type("You flee with the crowd, scooping " + green("${:,}".format(loot)) + " in chips off tables as you pass.")
                self.change_balance(loot)
                self.lose_sanity(3)
            self.use_item("Stink Bomb")
        else:
            type.type("The casino takes your money with surgical precision. The house always wins. You always lose.")
            self.lose_sanity(3)
        print("\n")

    def wild_gas_mask_funeral(self):
        """Gas Mask at a funeral causes panic"""
        type.type("A funeral. Somber. Gray suits. A priest is speaking. Everything is appropriately sad.")
        print("\n")
        if self.has_item("Gas Mask") or self.has_item("Hazmat Suit"):
            mask = "Hazmat Suit" if self.has_item("Hazmat Suit") else "Gas Mask"
            type.type("You forgot you're wearing the " + cyan(bright(mask)) + ". You walk in breathing pine-scented air.")
            print("\n")
            type.type("Someone whispers: " + quote("He must know something we don't.") + " Panic spreads. People start RUNNING.")
            print("\n")
            type.type("The reception table is unguarded. Free food, " + green("$40") + " in the donation box, and an antique brooch someone left.")
            self.change_balance(40)
            self.heal(5)
            self.lose_sanity(3)
        else:
            type.type("The service is brief. The food is institutional. You eat a sandwich and feel nothing. Standard funeral.")
            self.lose_sanity(1)
        print("\n")

    def wild_eldritch_candle_gambling(self):
        """Eldritch Candle makes cards translucent at gambling table"""
        type.type("A card game. The stakes are real. The tension is thick.")
        print("\n")
        if self.has_item("Eldritch Candle") or self.has_item("Dark Pact Reliquary"):
            candle = "Dark Pact Reliquary" if self.has_item("Dark Pact Reliquary") else "Eldritch Candle"
            type.type("You set the " + cyan(bright(candle)) + " on the table. The green flame makes the cards TRANSLUCENT.")
            print("\n")
            type.type("You can see face values through the backs. The dealer stares at the flame, hypnotized.")
            print("\n")
            type.type("Other players leave. It's just you and perfect information.")
            winnings = random.randint(300, 800)
            type.type(" " + green("${:,}".format(winnings)) + " in five hands. Then the candle goes out. It won't relight for days.")
            self.change_balance(winnings)
            self.lose_sanity(5)
        else:
            type.type("You play by intuition. Intuition says fold. You fold. Correct decision, zero excitement.")
            self.lose_sanity(1)
        print("\n")

    def wild_devil_deck_children(self):
        """Devil's Deck does card tricks for children — cards move on their own"""
        type.type("A park. Kids playing. One runs up to you. " + quote("Do you know any card tricks?"))
        print("\n")
        if self.has_item("Devil's Deck") or self.has_item("Dark Pact Reliquary"):
            deck = "Dark Pact Reliquary" if self.has_item("Dark Pact Reliquary") else "Devil's Deck"
            type.type("You pull out the " + cyan(bright(deck)) + ". The cards move on their own — floating, reshuffling, changing suits.")
            print("\n")
            type.type("The kids are AMAZED. Their parents are TERRIFIED. One mother drags her child away.")
            print("\n")
            tip = random.randint(30, 80)
            type.type("Another parent hands you " + green("${:,}".format(tip)) + ". " + quote("That was incredible. What's your secret?"))
            print("\n")
            type.type(quote("Ancient Sumerian conjuration,") + " you say. They laugh. You don't.")
            self.change_balance(tip)
            self.restore_sanity(5)
            self.lose_sanity(1)
        else:
            type.type(quote("Sorry, kid. No tricks today.") + " The kid's face falls. You feel like a monster.")
            self.lose_sanity(2)
        print("\n")

    def wild_binding_portrait_shopkeeper(self):
        """Binding Portrait hypnotizes a shopkeeper for discounts"""
        type.type("The shopkeeper quotes a price. It's too high. WAY too high. He knows it. You know it.")
        print("\n")
        if self.has_item("Binding Portrait"):
            type.type("You show the " + cyan(bright("Binding Portrait")) + " to the shopkeeper. Their pupils dilate.")
            print("\n")
            type.type(quote("I'll give you whatever you want,") + " they say in a voice that isn't entirely theirs.")
            print("\n")
            discount = random.randint(100, 300)
            type.type("Everything is half price. You save " + green("${:,}".format(discount)) + ". The shopkeeper seems fine. Mostly.")
            self.change_balance(discount)
            self.lose_sanity(4)
        else:
            type.type("You haggle. He's better at it. You pay full price and feel defeated.")
            self.lose_sanity(1)
        print("\n")

    def wild_fortune_cards_car(self):
        """Fortune Cards predict car trouble"""
        type.type("Idling in a parking lot. The car is making a noise. A new noise. The kind of noise that costs money.")
        print("\n")
        if self.has_item("Fortune Cards") or self.has_item("Fate Reader"):
            cards = "Fate Reader" if self.has_item("Fate Reader") else "Fortune Cards"
            type.type("You lay " + cyan(bright(cards)) + " on the dashboard. The car vibrates. The cards arrange themselves.")
            print("\n")
            type.type("THE TOWER on the brake pedal. DEATH on the exhaust pipe. A card you've never seen slides under the seat: THE JOURNEY.")
            print("\n")
            type.type("The car hums. Approval? You pat the dashboard. The noise stops. Whatever the cards did, it worked.")
            self.restore_sanity(5)
        else:
            type.type("The noise continues. You turn up the radio. The noise gets louder. This is a tomorrow problem.")
            self.lose_sanity(2)
        print("\n")

    def wild_blackmail_letter_companion(self):
        """Blackmail Letter used on your companion — dark choice"""
        type.type("Your companion has been... distant. Unreliable. They're thinking about leaving.")
        print("\n")
        if self.has_item("Blackmail Letter"):
            type.type("You show the " + cyan(bright("Blackmail Letter")) + " to your companion. It's blank.")
            print("\n")
            type.type("The blackmail isn't on paper — it's in the implication. Your companion freezes.")
            print("\n")
            type.type(quote("You wouldn't.") + " You would. They know it.")
            print("\n")
            type.type(quote("Fine. I'll stay. I'll do whatever you want.") + " The obedience in their voice is... unsettling.")
            print("\n")
            type.type("Your companion stays. Mechanically. Perfectly. Something in their eyes dies.")
            self.restore_sanity(3)
            self.lose_sanity(8)
        else:
            type.type("You can't make them stay. If they want to go, they'll go. That's what freedom means.")
            self.lose_sanity(3)
        print("\n")

    def lottery_ticket_check(self):
        """Lottery Ticket — scratch-off moment of hope"""
        if not self.has_item("Lottery Ticket"):
            self.day_event()
            return
        type.type("You find the " + cyan(bright("Lottery Ticket")) + " in your pocket. Crumpled. Forgotten. A $5 dream.")
        print("\n")
        type.type("You scratch it with your thumbnail. Silver flakes dust your lap.")
        print("\n")
        # Odds: 5% jackpot ($500-$5000), 20% small win ($10-$50), 75% loss
        result = random.randrange(20)
        if result == 0:
            winnings = random.choice([500, 1000, 2000, 5000])
            type.type("Three sevens. " + green("${:,}".format(winnings)) + ".")
            print("\n")
            type.type("You stare at the ticket. Then at the sky. Then at the ticket again.")
            print("\n")
            type.type("Your hands are shaking. This changes things. This changes everything.")
            self.change_balance(winnings)
            self.restore_sanity(15)
        elif result < 5:
            winnings = random.choice([10, 20, 50])
            type.type("A small winner. " + green("${:,}".format(winnings)) + ". Enough for a meal. Enough for hope.")
            self.change_balance(winnings)
            self.restore_sanity(3)
        else:
            type.type("Nothing. Three different symbols. Not even close.")
            print("\n")
            type.type("You crumple the ticket and let it fall. Five dollars, gone. The lottery giveth not.")
            self.lose_sanity(1)
        self.use_item("Lottery Ticket")
        print("\n")
