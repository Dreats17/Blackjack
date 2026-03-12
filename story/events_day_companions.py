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

class DayCompanionsMixin:
    """Companion events: all companion-specific encounters and bonds"""

    def companion_reunion(self):
        # SECRET: Have 3+ companions - they all show up at once
        companion_count = len(self._companions) if hasattr(self, '_Player__companions') else 0
        if companion_count < 3:
            self.day_event()
            return
        type.type("You're sitting in your car outside the casino when you see something strange.")
        print("\n")
        type.type("All of your friends. All of them. Walking toward you together.")
        print("\n")
        type.type("The stray cat. The crow. The people you've met along the way.")
        print("\n")
        type.type("They don't say anything. They just... gather around you.")
        print("\n")
        type.type("For a moment, you're not alone. Not a solo gambler living in a car.")
        print("\n")
        type.type("You're someone with PEOPLE. Connections. A weird, misfit family.")
        print("\n")
        type.type("The moment passes. Everyone drifts away. But the warmth stays.")
        self.restore_sanity(20)
        self.heal(10)
        print("\n")

    def the_cat_knows(self):
        # SECRET: Have the stray cat companion - they lead you to something
        if not self.has_companion("Stray Cat"):
            self.day_event()
            return
        type.type("Your stray cat is acting strange. Meowing insistently. Tugging at your shoelace.")
        print("\n")
        type.type("It wants you to follow. So you do.")
        print("\n")
        type.type("Through the parking lot. Behind the dumpsters. Into a drainage culvert.")
        print("\n")
        type.type("There, hidden in the darkness, you find a small box.")
        print("\n")
        type.type("Inside: " + green(bright("$75")) + " in cash, a locket with no picture, and a note:")
        print("\n")
        type.type(quote("For whoever needs this more than I did. -M"))
        print("\n")
        type.type("The cat purrs. You don't know how it knew. Cats are weird like that.")
        self.change_balance(75)
        self.add_item("Empty Locket")
        self.restore_sanity(5)
        print("\n")

    def lucky_guards_car(self):
        # EVENT: Lucky the three-legged dog protects your car from a thief
        # CONDITION: Must have Lucky alive
        if not self.has_companion("Lucky") or self.get_companion("Lucky")["status"] != "alive":
            self.day_event()
            return
        type.type("You come back to your car after a walk. Something's wrong.")
        print("\n")
        type.type("A man is crouched by your window. Slim jim in hand. Trying to break in.")
        print("\n")
        type.type("Then you hear it. A growl. Low, deep, primal.")
        print("\n")
        type.type(bright("Lucky") + " is standing between the thief and your car. Three legs planted. Teeth bared.")
        print("\n")
        type.type("The thief looks at this three-legged dog and has a moment of calculation.")
        print("\n")
        type.type("Lucky barks once. It echoes off every car in the lot. The thief drops the slim jim and bolts.")
        print("\n")
        type.type("Lucky trots over to you, tail wagging like nothing happened. Hero behavior.")
        print("\n")
        type.type("You kneel down and hug him. He licks your ear.")
        print("\n")
        type.type(green("Lucky protected your car! Good boy."))
        self.restore_sanity(8)
        self.pet_companion("Lucky")
        self.pet_companion("Lucky")  # Double pet for being a hero
        print("\n")

    def mr_pecks_treasure(self):
        # EVENT: Mr. Pecks the crow brings you money or valuables
        # CONDITION: Must have Mr. Pecks alive
        if not self.has_companion("Mr. Pecks") or self.get_companion("Mr. Pecks")["status"] != "alive":
            self.day_event()
            return
        companion = self.get_companion("Mr. Pecks")
        type.type("You hear tapping on your car window. " + bright("Mr. Pecks") + " is outside, something in his beak.")
        print("\n")
        
        if companion["bonded"]:
            # Bonded Mr. Pecks finds REALLY good stuff
            roll = random.randrange(4)
            if roll == 0:
                amount = random.randint(50, 200)
                type.type("He drops a crumpled bill through the window crack. Then another. And another.")
                print("\n")
                type.type("Mr. Pecks has been COLLECTING. There's a small pile of bills.")
                print("\n")
                type.type("You count it up: " + green(bright("${:,}".format(amount))) + ".")
                print("\n")
                type.type("Where did he get all this? You know what, don't ask. Just appreciate the crow.")
                self.change_balance(amount)
            elif roll == 1:
                type.type("He drops a golden ring into your lap. It's real. Actual gold.")
                print("\n")
                type.type("Mr. Pecks caws proudly. He knows exactly what he found.")
                print("\n")
                type.type("You could probably sell this...")
                if not self.has_item("Golden Ring"):
                    self.add_item("Golden Ring")
                    type.type(magenta(bright(" +Golden Ring")))
                else:
                    amount = random.randint(100, 300)
                    type.type(" You pocket it and figure it's worth about " + green(bright("${:,}".format(amount))) + ".")
                    self.change_balance(amount)
            elif roll == 2:
                type.type("He drops a credit card. Then looks at you. Then at the credit card.")
                print("\n")
                type.type("You look at the name. It's nobody you know. This is stolen property.")
                print("\n")
                answer = ask.option("What do you do? ", ["use it", "throw it away", "return it"])
                if answer == "use it":
                    amount = random.randint(20, 100)
                    type.type("You buy a few things before the card gets declined. About " + green(bright("${:,}".format(amount))) + " worth.")
                    self.change_balance(amount)
                    self.lose_sanity(5)
                    type.type("You feel a little guilty. But Mr. Pecks looks proud.")
                elif answer == "return it":
                    type.type("You find the owner's address and mail it back. Good karma.")
                    self.restore_sanity(10)
                else:
                    type.type("You snap it in half. Mr. Pecks cocks his head, confused. Why waste good treasure?")
            else:
                amount = random.randint(20, 80)
                type.type("A handful of coins tumble from his beak. Quarters, dimes, a few dollar coins.")
                print("\n")
                type.type("About " + green(bright("${:,}".format(amount))) + " worth. Not bad for a bird.")
                self.change_balance(amount)
        else:
            # Non-bonded Mr. Pecks finds smaller stuff
            roll = random.randrange(3)
            if roll == 0:
                amount = random.randint(5, 30)
                type.type("A crumpled bill drops from his beak. A few coins follow.")
                print("\n")
                type.type(green(bright("${:,}".format(amount))) + ". Not much, but the gesture means everything.")
                self.change_balance(amount)
            elif roll == 1:
                type.type("He drops a bottle cap in your lap. Stares at you expectantly.")
                print("\n")
                type.type("It's... worthless. But he's so PROUD of it. You act impressed.")
                print("\n")
                type.type("Mr. Pecks caws with satisfaction and flies off to find more treasures.")
                self.restore_sanity(3)
            else:
                type.type("He drops a shiny button. Then a paperclip. Then a key to... something.")
                print("\n")
                type.type("You have no idea what any of this opens or does. But you keep it all.")
                print("\n")
                type.type("Mr. Pecks' treasure collection grows. So does your heart.")
                self.restore_sanity(5)
        
        self.pet_companion("Mr. Pecks")
        print("\n")

    def rusty_midnight_heist(self):
        # EVENT: Rusty the raccoon steals something useful while you weren't looking
        # CONDITION: Must have Rusty alive
        if not self.has_companion("Rusty") or self.get_companion("Rusty")["status"] != "alive":
            self.day_event()
            return
        companion = self.get_companion("Rusty")
        type.type("You wake up to find " + bright("Rusty") + " sitting on the dashboard with something.")
        print("\n")
        type.type("They chitter excitedly, tiny paws wrapped around their latest acquisition.")
        print("\n")
        
        if companion["bonded"]:
            roll = random.randrange(5)
            if roll == 0:
                amount = random.randint(50, 150)
                type.type("It's a wallet. Not yours. Someone else's.")
                print("\n")
                type.type("There's " + green(bright("${:,}".format(amount))) + " inside. Plus a driver's license.")
                print("\n")
                answer = ask.option("What do you do? ", ["keep the cash", "return it all"])
                if answer == "keep the cash":
                    type.type("You pocket the cash and toss the wallet. Rusty approves. Crime family values.")
                    self.change_balance(amount)
                    self.lose_sanity(3)
                else:
                    type.type("You find the owner. They're so grateful they give you a reward.")
                    reward = random.randint(20, 50)
                    self.change_balance(reward)
                    self.restore_sanity(8)
                    type.type("Rusty seems confused by your morality. But they love you anyway.")
            elif roll == 1:
                type.type("It's a whole sandwich. Still in the wrapper. Still warm. Where did Rusty get a warm sandwich?!")
                print("\n")
                type.type("You eat half. Rusty eats half. You make eye contact. This is the good life.")
                self.heal(10)
                self.feed_companion("Rusty")
            elif roll == 2:
                type.type("It's a set of car keys. To a car much nicer than yours.")
                print("\n")
                type.type("You put them on the roof of a random car in the lot. Probably the right one.")
                print("\n")
                type.type("Rusty chitters in protest. That was GOOD loot!")
                self.restore_sanity(3)
            elif roll == 3:
                type.type("It's a smartphone. Cracked screen, but it works.")
                print("\n")
                type.type("You could sell this... or do the right thing.")
                answer = ask.option("What do you do? ", ["sell it", "turn it in"])
                if answer == "sell it":
                    amount = random.randint(30, 80)
                    type.type("You sell it to a guy. " + green(bright("${:,}".format(amount))) + ". Rusty nods approvingly.")
                    self.change_balance(amount)
                else:
                    type.type("You turn it in to lost and found. Rusty sulks for an hour.")
                    self.restore_sanity(5)
            else:
                type.type("It's a bag of beef jerky. Opened, but mostly full. Raccoon tax: two pieces missing.")
                print("\n")
                type.type("You share the rest. Rusty washes each piece in your water bottle first. Of course they do.")
                self.heal(5)
                self.restore_sanity(3)
        else:
            roll = random.randrange(3)
            if roll == 0:
                type.type("It's... a sock. One sock. Wet. Rusty is very proud.")
                print("\n")
                type.type("You accept the sock with the gravity it deserves. This is a gift.")
                self.restore_sanity(2)
            elif roll == 1:
                type.type("It's a half-eaten candy bar. Rusty took one bite, then decided you should have the rest.")
                print("\n")
                type.type("Sharing is caring, raccoon-style.")
                self.heal(3)
            else:
                amount = random.randint(1, 10)
                type.type("It's a handful of coins they dug out of a fountain. " + green(bright("${:,}".format(amount))) + ".")
                print("\n")
                type.type("Rusty is learning. They'll be a master thief soon.")
                self.change_balance(amount)
        
        self.pet_companion("Rusty")
        print("\n")

    def whiskers_sixth_sense(self):
        # EVENT: Whiskers senses danger and warns you
        # CONDITION: Must have Whiskers alive
        if not self.has_companion("Whiskers") or self.get_companion("Whiskers")["status"] != "alive":
            self.day_event()
            return
        type.type("You're about to leave the car when " + bright("Whiskers") + " does something unusual.")
        print("\n")
        type.type("They plant themselves on your lap. Claws out. Not moving.")
        print("\n")
        type.type("You try to stand up. Whiskers hisses. Not at you. At the door. At what's outside.")
        print("\n")
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("You wait. Five minutes pass. Then you hear it.")
            print("\n")
            type.type("Shouting. A fight breaks out in the parking lot. Two men, fists and blood.")
            print("\n")
            type.type("If you'd walked out five minutes ago, you'd have been right in the middle of it.")
            print("\n")
            type.type("Whiskers purrs. " + cyan("Danger avoided."))
            self.restore_sanity(10)
        elif roll == 1:
            type.type("You stay put. Through the window, you see a police cruiser pull into the lot.")
            print("\n")
            type.type("They're checking cars. Asking questions. Looking for someone.")
            print("\n")
            type.type("They spend ten minutes searching, then leave. Whatever they were looking for, it wasn't you.")
            print("\n")
            type.type("Whiskers relaxes. You can go now. The coast is clear.")
            self.restore_sanity(5)
        elif roll == 2:
            type.type("You stay. Twenty minutes later, the sky opens up. Torrential rain. Lightning.")
            print("\n")
            type.type("The parking lot floods in minutes. If you'd been walking, you'd be soaked and miserable.")
            print("\n")
            type.type("Whiskers curls up on your lap and purrs. Warm. Dry. Safe.")
            self.restore_sanity(8)
            self.heal(5)
        else:
            type.type("You listen to the cat. Something about their urgency makes you trust them completely.")
            print("\n")
            type.type("A truck blows through the parking lot way too fast. Right through the spot where you'd have been standing.")
            print("\n")
            type.type("Your blood goes cold. Whiskers saved your life. Actually saved your life.")
            print("\n")
            type.type("You hold the cat tight. They tolerate the hug. Just this once.")
            self.restore_sanity(15)
        
        self.pet_companion("Whiskers")
        print("\n")

    def slick_escape_route(self):
        # EVENT: Slick the rat knows every escape route and saves you from trouble
        # CONDITION: Must have Slick alive
        if not self.has_companion("Slick") or self.get_companion("Slick")["status"] != "alive":
            self.day_event()
            return
        type.type("You're walking near the back of the casino when two guys step out of an alley.")
        print("\n")
        type.type(quote("Hey. You. Come here."))
        print("\n")
        type.type("They don't look friendly. Your heart rate spikes.")
        print("\n")
        type.type("Then " + bright("Slick") + " starts squeaking frantically from your pocket. They're tugging your shirt.")
        print("\n")
        type.type("Left. Slick wants you to go left. Into what looks like a dead end.")
        print("\n")
        type.type("You trust the rat. You run left.")
        print("\n")
        type.type("It's not a dead end. There's a gap between the buildings. Barely wide enough for a person.")
        print("\n")
        type.type("You squeeze through. Behind you, the two guys try to follow but they're too big.")
        print("\n")
        type.type(quote("Get back here!"))
        print("\n")
        type.type("You emerge on a busy street. People everywhere. Safe.")
        print("\n")
        type.type("Slick peeks out of your pocket and bruxes contentedly. They knew. They always know.")
        print("\n")
        type.type(green("Slick knew the escape route! They always do."))
        self.restore_sanity(10)
        self.pet_companion("Slick")
        print("\n")

    def hopper_lucky_day(self):
        # EVENT: Hopper the rabbit brings you luck
        # CONDITION: Must have Hopper alive
        if not self.has_companion("Hopper") or self.get_companion("Hopper")["status"] != "alive":
            self.day_event()
            return
        type.type(bright("Hopper") + " binkies around the car this morning. Full of energy. Full of... something.")
        print("\n")
        type.type("You can feel it in the air. Today is going to be a good day.")
        print("\n")
        
        roll = random.randrange(4)
        if roll == 0:
            amount = random.randint(20, 100)
            type.type("You find money in your coat pocket you forgot about. " + green(bright("${:,}".format(amount))) + ".")
            print("\n")
            type.type("Then a stranger holds the door for you. Then the vending machine gives you two sodas for the price of one.")
            print("\n")
            type.type("Little things. But they add up. Hopper's luck is infectious.")
            self.change_balance(amount)
            self.restore_sanity(5)
        elif roll == 1:
            type.type("Someone drops a scratch ticket. It lands right at your feet.")
            print("\n")
            type.type("You pick it up. Haven't scratched it yet.")
            print("\n")
            amount = random.randint(50, 500)
            type.type("You scratch it off with a coin. " + green(bright("${:,}".format(amount))) + " WINNER!")
            print("\n")
            type.type("You look at Hopper. Hopper twitches their nose. Luck incarnate.")
            self.change_balance(amount)
            self.restore_sanity(5)
        elif roll == 2:
            type.type("Every green light. Every parking spot open. Every coin in the meter.")
            print("\n")
            type.type("It's not one big lucky thing. It's twenty small lucky things.")
            print("\n")
            type.type("Hopper rides in your lap, nose twitching, and you swear the world bends around this rabbit.")
            self.restore_sanity(10)
            self.heal(5)
        else:
            type.type("A woman stops you in the street.")
            print("\n")
            type.type(quote("Is that a rabbit? Can I pet it?"))
            print("\n")
            type.type("Hopper is, for once, perfectly behaved. Lets the woman pet them. Makes her day.")
            print("\n")
            type.type("She's so happy she insists on buying you coffee. You end up talking for an hour.")
            print("\n")
            type.type("Human connection. Warmth. Kindness. Thanks to a rabbit.")
            self.restore_sanity(12)
        
        self.pet_companion("Hopper")
        print("\n")

    def patches_night_watch(self):
        # EVENT: Patches the opossum notices something at night that helps you during the day
        # CONDITION: Must have Patches alive
        if not self.has_companion("Patches") or self.get_companion("Patches")["status"] != "alive":
            self.day_event()
            return
        type.type(bright("Patches") + " was up all night. As usual. But this morning, they're insistent about something.")
        print("\n")
        type.type("Patches keeps pawing at the window, looking toward the back of the parking lot.")
        print("\n")
        type.type("You follow the opossum's lead and investigate.")
        print("\n")
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("Behind a dumpster, hidden under cardboard: a stash. Someone's stash.")
            print("\n")
            amount = random.randint(50, 200)
            type.type("Cash. " + green(bright("${:,}".format(amount))) + " in a rubber-banded roll. Drug money? Emergency fund? Who knows.")
            print("\n")
            answer = ask.option("What do you do? ", ["take it", "leave it"])
            if answer == "take it":
                type.type("Finders keepers. Patches found it first, technically.")
                self.change_balance(amount)
            else:
                type.type("You leave it. Not your money. Not your problem.")
                self.restore_sanity(5)
        elif roll == 1:
            type.type("Patches saw someone tampering with your car last night. Tire's been loosened.")
            print("\n")
            type.type("If you'd driven without checking, the wheel could have come off at speed.")
            print("\n")
            type.type("You tighten it back. Thank the opossum. Patches plays dead from the compliment.")
            print("\n")
            type.type(green("Patches might have saved your life with their night watch."))
            self.restore_sanity(10)
        elif roll == 2:
            type.type("There's a kitten. Tiny. Alone. Crying under a car.")
            print("\n")
            type.type("Patches heard it last night but waited for you to help. Smart possum.")
            print("\n")
            type.type("You rescue the kitten. It's shaking, cold, starving.")
            print("\n")
            answer = ask.yes_or_no("Keep the kitten? ")
            if answer == "yes" and not self.has_companion("Whiskers"):
                type.type("You name the kitten Whiskers. Patches seems to approve - a nocturnal friend.")
                self.add_companion("Whiskers", "Alley Cat")
            elif answer == "yes":
                type.type("You already have Whiskers. But you find a good home for the kitten nearby.")
                self.restore_sanity(10)
            else:
                type.type("You bring the kitten to a shelter. They'll take care of it. You can't take care of everything.")
                self.restore_sanity(5)
        else:
            type.type("Patches saw people setting up a free breakfast event at the church across the street!")
            print("\n")
            type.type("Pancakes, eggs, coffee. All free. All you can eat.")
            print("\n")
            type.type("You eat until you're actually full. When was the last time that happened?")
            print("\n")
            type.type("Patches had some too. They ate scrambled eggs with their tiny hands. People stared. Worth it.")
            self.heal(15)
            self.restore_sanity(5)
            self.feed_companion("Patches")
        
        self.pet_companion("Patches")
        print("\n")

    def squirrelly_stash(self):
        # EVENT: Squirrelly's hoarding habit leads to a discovery
        # CONDITION: Must have Squirrelly alive
        if not self.has_companion("Squirrelly") or self.get_companion("Squirrelly")["status"] != "alive":
            self.day_event()
            return
        type.type(bright("Squirrelly") + " has been burying things around the parking lot for weeks.")
        print("\n")
        type.type("Today, they dig something up and bring it to you. Chattering excitedly.")
        print("\n")
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("It's an acorn. Just an acorn. But Squirrelly presents it like it's the Hope Diamond.")
            print("\n")
            type.type("You hold it solemnly. Squirrelly chatters with approval. You have been deemed worthy.")
            print("\n")
            type.type("It's just a nut. But the love behind it is real.")
            self.restore_sanity(5)
        elif roll == 1:
            amount = random.randint(5, 40)
            type.type("It's a collection of coins Squirrelly buried over the last few weeks.")
            print("\n")
            type.type("Nickels, quarters, a few half-dollars. About " + green(bright("${:,}".format(amount))) + " total.")
            print("\n")
            type.type("Squirrelly was SAVING for you. Squirrel investment portfolio.")
            self.change_balance(amount)
            self.restore_sanity(3)
        elif roll == 2:
            type.type("They unearthed a small jewelry box. Tarnished. Old. Someone buried it here years ago.")
            print("\n")
            type.type("Inside: a locket with a faded photo. Two people, smiling. From another era.")
            print("\n")
            type.type("You don't know their story. But you hope they were happy.")
            self.restore_sanity(8)
        else:
            type.type("Squirrelly dug up... more acorns. A LOT of acorns. A mountain of acorns.")
            print("\n")
            type.type("They've been burying acorns all season. The parking lot is basically an acorn mine now.")
            print("\n")
            type.type("Squirrelly sits atop the acorn pile like a dragon on their hoard. Majestic.")
            print("\n")
            type.type("You are witnessing peak squirrel. This is their life's work.")
            self.restore_sanity(5)
        
        self.pet_companion("Squirrelly")
        print("\n")

    def companion_sick_day(self):
        # EVENT: One of your companions gets sick
        # CONDITION: Must have at least one companion
        living = self.get_all_companions()
        if len(living) == 0:
            self.day_event()
            return
        
        # Pick a random living companion
        name = random.choice(list(living.keys()))
        companion = living[name]
        comp_type = companion.get("type", "companion")
        
        type.type("Something's wrong with " + bright(name) + ".")
        print("\n")
        
        if comp_type in ["Three-Legged Dog", "Alley Cat"]:
            type.type("They won't eat. Won't drink. Just lying there, breathing shallow.")
        elif comp_type in ["Crow"]:
            type.type("Their feathers are puffed up. Not moving much. Eyes half-closed.")
        elif comp_type in ["Squirrel", "Rabbit"]:
            type.type("They're lethargic. No energy. No binkies. No chattering. Just... still.")
        elif comp_type in ["Raccoon", "Opossum"]:
            type.type("They're not getting into anything. Not rummaging. Not stealing. Something's very wrong.")
        elif comp_type in ["Rat"]:
            type.type("Slick is puffed up, barely moving. Their breathing is rapid and shallow.")
        else:
            type.type("They're not acting normal. Sluggish. Distant. Something is off.")
        print("\n")
        
        type.type("Your companion is sick. What do you do?")
        print("\n")
        
        if self.has_item("Cough Drops"):
            type.type("1. Use your " + magenta(bright("Cough Drops")) + " to help")
        else:
            type.type("1. Try to help with what you have")
        type.type("2. Rush to a vet (costs $50-200)")
        type.type("3. Wait it out and hope for the best")
        type.type("4. Give them extra food and water")
        print("\n")
        
        choice = input("Choose: ").strip()
        
        if choice == "1" and self.has_item("Cough Drops"):
            type.type("You crush up some cough drops and mix them with water. Not exactly veterinary medicine.")
            print("\n")
            type.type(name + " drinks. Slowly. After a few hours, they seem a little better.")
            print("\n")
            type.type("Not great. But alive. That's what matters.")
            self.use_item("Cough Drops")
            self.pet_companion(name)
            self.restore_sanity(5)
        elif choice == "2":
            vet_cost = random.randint(50, 200)
            if self.get_balance() >= vet_cost:
                type.type("You rush " + name + " to the nearest vet. Emergency appointment.")
                print("\n")
                type.type("The vet examines them. Medication. Fluids. The works.")
                print("\n")
                type.type("Cost: " + red(bright("${:,}".format(vet_cost))) + ". Worth every penny.")
                print("\n")
                type.type(name + " perks up by evening. The medication worked. They're going to be okay.")
                self.change_balance(-vet_cost)
                self.pet_companion(name)
                self.pet_companion(name)
                self.restore_sanity(10)
            else:
                type.type("You don't have enough money for a vet. You try your best with what you have.")
                print("\n")
                type.type(name + " looks at you with trusting eyes. You feel like you're failing them.")
                self.lose_sanity(10)
                # 50/50 chance they pull through
                if random.randrange(2) == 0:
                    type.type("By morning, " + name + " is drinking water again. They're tough. They'll make it.")
                    self.pet_companion(name)
                else:
                    type.type("By morning, " + name + " is worse. Much worse.")
                    self.companion_dies(name, "illness")
        elif choice == "3":
            type.type("You decide to wait. Nature will take its course.")
            print("\n")
            chance = random.randrange(3)
            if chance == 0:
                type.type("By the next morning, " + name + " bounces back. Whatever it was, they fought it off.")
                self.pet_companion(name)
                self.restore_sanity(3)
            elif chance == 1:
                type.type(name + " stays sick for days. Weak. Fragile. But they hang on. Barely.")
                print("\n")
                # Lose a lot of happiness
                self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 20)
                self.lose_sanity(8)
            else:
                type.type(name + " doesn't make it through the night.")
                print("\n")
                type.type("You wake up and they're gone. Still. Cold.")
                print("\n")
                type.type("You could have done something. Should have done something.")
                self.companion_dies(name, "illness")
        else:
            type.type("You give " + name + " extra food and fresh water. Stay close. Keep them warm.")
            print("\n")
            self.feed_companion(name)
            if random.randrange(3) != 0:
                type.type(name + " eats a little. Drinks. By evening, they're moving around more.")
                print("\n")
                type.type("Not 100%. But better. Your care made the difference.")
                self.pet_companion(name)
                self.restore_sanity(5)
            else:
                type.type(name + " won't eat. Won't drink. They're getting worse.")
                self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 15)
                self.lose_sanity(5)
        print("\n")

    def companion_rivalry(self):
        # EVENT: Two of your companions fight each other
        # CONDITION: Must have 2+ companions
        living = self.get_all_companions()
        if len(living) < 2:
            self.day_event()
            return
        
        names = list(living.keys())
        random.shuffle(names)
        comp1 = names[0]
        comp2 = names[1]
        type1 = living[comp1].get("type", "companion")
        type2 = living[comp2].get("type", "companion")
        
        type.type("You wake up to chaos.")
        print("\n")
        type.type(bright(comp1) + " and " + bright(comp2) + " are fighting.")
        print("\n")
        
        # Flavor based on types
        if "Cat" in type1 or "Cat" in type2:
            type.type("Hissing. Yowling. The kind of sounds that make your blood curdle.")
        elif "Dog" in type1 or "Dog" in type2:
            type.type("Growling. Barking. Snapping jaws and bared teeth.")
        elif "Crow" in type1 or "Crow" in type2:
            type.type("Cawing. Wing-beating. Pecking. Feathers everywhere.")
        else:
            type.type("Chattering. Squealing. Tiny fury unleashed.")
        print("\n")
        
        type.type("They're going at it over territory. Your car only has so much space.")
        print("\n")
        type.type("What do you do?")
        type.type("1. Break it up carefully")
        type.type("2. Separate them permanently (release one)")
        type.type("3. Let them sort it out")
        type.type("4. Bribe both with food")
        print("\n")
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            type.type("You carefully intervene. Separating them with a blanket between them.")
            print("\n")
            if random.randrange(3) == 0:
                type.type("You get scratched/bitten in the process. Ouch.")
                self.hurt(5)
            type.type("They glare at each other from opposite sides of the car. Tense, but calm.")
            print("\n")
            type.type("This is a fragile peace. But it's peace.")
            self._companions[comp1]["happiness"] = max(0, self._companions[comp1]["happiness"] - 5)
            self._companions[comp2]["happiness"] = max(0, self._companions[comp2]["happiness"] - 5)
        elif choice == "2":
            type.type("You can't keep them both. One has to go.")
            print("\n")
            type.type(f"1. Release {comp1}")
            type.type(f"2. Release {comp2}")
            type.type("3. Never mind, I'll figure it out")
            print("\n")
            release_choice = input("Choose: ").strip()
            if release_choice == "1":
                type.type("You carry " + comp1 + " outside. Set them down gently.")
                print("\n")
                type.type("They look back at you once. Then they're gone. Into the world. Without you.")
                print("\n")
                self._companions[comp1]["status"] = "lost"
                self.lose_sanity(15)
            elif release_choice == "2":
                type.type("You carry " + comp2 + " outside. Set them down gently.")
                print("\n")
                type.type("They look back at you once. Then they're gone. Into the world. Without you.")
                print("\n")
                self._companions[comp2]["status"] = "lost"
                self.lose_sanity(15)
            else:
                type.type("You can't do it. You'll make this work somehow.")
                self._companions[comp1]["happiness"] = max(0, self._companions[comp1]["happiness"] - 10)
                self._companions[comp2]["happiness"] = max(0, self._companions[comp2]["happiness"] - 10)
        elif choice == "3":
            type.type("You let nature take its course. Survival of the fittest.")
            print("\n")
            if random.randrange(4) == 0:
                # One gets seriously hurt
                loser = random.choice([comp1, comp2])
                winner = comp2 if loser == comp1 else comp1
                type.type(bright(loser) + " gets the worst of it. They're limping. Bleeding.")
                print("\n")
                type.type(bright(winner) + " claims the back seat. Dominance established.")
                print("\n")
                type.type("But " + loser + " might not recover from those injuries...")
                self._companions[loser]["happiness"] = max(0, self._companions[loser]["happiness"] - 25)
                if random.randrange(4) == 0:
                    type.type(loser + " didn't survive the injuries.")
                    self.companion_dies(loser, "fight with " + winner)
            else:
                type.type("After a lot of noise and fury, they settle into an uneasy truce.")
                print("\n")
                type.type("Opposite corners. Cold shoulders. But alive.")
                self._companions[comp1]["happiness"] = max(0, self._companions[comp1]["happiness"] - 8)
                self._companions[comp2]["happiness"] = max(0, self._companions[comp2]["happiness"] - 8)
        else:
            type.type("You break out the food. Two separate piles. Equal portions.")
            print("\n")
            type.type("The fighting stops immediately. Food > territory disputes.")
            print("\n")
            type.type("They eat side by side. Not friends yet. But not enemies anymore.")
            self.feed_companion(comp1)
            self.feed_companion(comp2)
            self.restore_sanity(3)
        
        self.lose_sanity(5)
        print("\n")

    def companion_hero_moment(self):
        # EVENT: A companion saves you from a dangerous situation
        # CONDITION: Must have at least one companion
        living = self.get_all_companions()
        if len(living) == 0:
            self.day_event()
            return
        
        # Pick the best candidate based on bonuses
        protector = None
        warner = None
        any_companion = random.choice(list(living.keys()))
        
        for name in living:
            comp_data = self._lists.get_companion_type(name)
            if comp_data:
                bonuses = comp_data.get("bonuses", {})
                if bonuses.get("protection"):
                    protector = name
                if bonuses.get("danger_warning"):
                    warner = name
        
        hero = protector or warner or any_companion
        hero_data = living[hero]
        hero_type = hero_data.get("type", "companion")
        
        type.type("Today almost went very, very wrong.")
        print("\n")
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("A stray dog. Big one. Aggressive. Foam around its mouth. Coming right at you.")
            print("\n")
            if hero == "Lucky":
                type.type(bright("Lucky") + " launches himself at the stray. Three legs, but zero hesitation.")
                print("\n")
                type.type("The two dogs collide. Lucky is smaller. Weaker. But he fights like his life depends on it.")
                print("\n")
                type.type("Because YOUR life depends on it.")
                print("\n")
                type.type("The stray backs off. Slinks away. Lucky stands over you, bleeding from a scratch, tail wagging.")
                self.hurt(0)
                self._companions["Lucky"]["happiness"] = max(0, self._companions["Lucky"]["happiness"] - 3)
            elif "Cat" in hero_type:
                type.type(bright(hero) + " leaps onto the dog's face. Claws extended. A feline missile.")
                print("\n")
                type.type("The dog yelps, shakes its head, can't get the cat off. Runs away howling.")
                print("\n")
                type.type(hero + " lands gracefully. Licks a paw. Walks away like nothing happened.")
            elif "Crow" in hero_type:
                type.type(bright(hero) + " dive-bombs the dog. Over and over. Cawing. Pecking. Relentless.")
                print("\n")
                type.type("An entire murder of crows joins in. The dog is overwhelmed. Retreats.")
                print("\n")
                type.type(hero + " lands on your shoulder and caws once. You're welcome.")
            else:
                type.type(bright(hero) + " makes enough noise to attract attention. People come running.")
                print("\n")
                type.type("The stray bolts. " + hero + " chatters/squeaks with relief. Their alarm saved you.")
            print("\n")
            type.type(green(hero + " protected you!"))
            self.restore_sanity(12)
            
        elif roll == 1:
            type.type("You're about to step into the street. Earbuds in. Not paying attention.")
            print("\n")
            type.type(bright(hero) + " suddenly goes WILD. Biting your shoelace. Pulling your pants. Screaming bloody murder.")
            print("\n")
            type.type("You stop. Annoyed. Look up.")
            print("\n")
            type.type("A truck blows through the intersection. Red light. Seventy miles an hour.")
            print("\n")
            type.type("Right where you would have been standing.")
            print("\n")
            type.type("You sit down on the curb. Shaking. " + hero + " climbs into your lap.")
            print("\n")
            type.type("They knew. Somehow, they knew.")
            self.restore_sanity(15)
            
        elif roll == 2:
            type.type("You're sleeping in your car. Middle of the night. Something wakes you.")
            print("\n")
            type.type(bright(hero) + " is agitated. Frantic. Pawing at the door.")
            print("\n")
            type.type("You get out. Groggy. Confused. Then you smell it.")
            print("\n")
            type.type("Gas. Your car is leaking gas. The engine is hot. One spark and...")
            print("\n")
            type.type("You back away. Far away. The car doesn't explode, but it could have. With you in it.")
            print("\n")
            type.type(hero + " saved your life. No question about it.")
            self.restore_sanity(15)
            self.add_danger("Fuel Leak")
            
        else:
            type.type("A man approaches you. Friendly enough. Asking for directions.")
            print("\n")
            type.type("But " + bright(hero) + " starts growling/hissing/squeaking aggressively at him.")
            print("\n")
            type.type("You notice: his hand is behind his back. Something metal glints.")
            print("\n")
            type.type("You step back. Say you don't know the area. Walk away quickly.")
            print("\n")
            type.type("You look back once. He's moved on to someone else. You see the knife now.")
            print("\n")
            type.type(hero + "'s instinct was right. They read people better than you do.")
            self.restore_sanity(10)
        
        self.pet_companion(hero)
        self.pet_companion(hero)
        print("\n")

    def companion_death_sacrifice(self):
        # EVENT: A companion sacrifices themselves to save you (RARE, DEVASTATING)
        # CONDITION: Must have a bonded companion
        living = self.get_all_companions()
        bonded_companions = [name for name, data in living.items() if data.get("bonded")]
        
        if len(bonded_companions) == 0:
            self.day_event()
            return
        
        hero = random.choice(bonded_companions)
        hero_data = living[hero]
        hero_type = hero_data.get("type", "companion")
        days = hero_data.get("days_owned", 0)
        
        type.type("You need to hear this story. All of it. Even the ending.")
        print("\n")
        time.sleep(1)
        
        type.type("It happened fast. Walking near the road. Lost in thought. Not paying attention.")
        print("\n")
        type.type("The car came out of nowhere. Hit-and-run driver. Barreling right at you.")
        print("\n")
        time.sleep(1)
        
        if "Dog" in hero_type:
            type.type(bright(hero) + " hit you from the side. All three legs pushing. Everything they had.")
            print("\n")
            type.type("You went left. " + hero + " went right. Into the path of the car.")
        elif "Cat" in hero_type:
            type.type(bright(hero) + " yowled. That horrible, blood-curdling cat scream. You instinctively jumped back.")
            print("\n")
            type.type("But " + hero + " didn't jump back. " + hero + " jumped forward. Into the road. Drawing the car's attention.")
        elif "Crow" in hero_type:
            type.type(bright(hero) + " flew directly at the windshield. Wings spread. A living shield.")
            print("\n")
            type.type("The driver swerved. Missed you by inches. Didn't miss " + hero + ".")
        else:
            type.type(bright(hero) + " threw themselves in front of you. Pushed you. Bit you. Did everything they could to move you.")
            print("\n")
            type.type("You stumbled. Fell. The car missed you. It didn't miss " + hero + ".")
        
        print("\n")
        time.sleep(2)
        type.type("You scrambled to " + hero + ". Knelt down. Held them.")
        print("\n")
        type.type("They were still warm. Still breathing. Barely.")
        print("\n")
        time.sleep(1)
        
        if "Dog" in hero_type:
            type.type(hero + "'s tail wagged. One last time. Weak. But there.")
            print("\n")
            type.type("Good boy. The best boy. The best boy who ever lived.")
        elif "Cat" in hero_type:
            type.type(hero + " purred. Even now. Even like this. Purring against your chest.")
            print("\n")
            type.type("Cats purr when they're happy. They also purr when they're dying. A final comfort.")
        elif "Crow" in hero_type:
            type.type(hero + " looked at you with one intelligent eye. No sound. Just... recognition.")
            print("\n")
            type.type("They recognized you. Until the very end.")
        elif "Rabbit" in hero_type:
            type.type(hero + " twitched their nose. Once. Twice. Then went still.")
            print("\n")
            type.type("So fast. Rabbits are so fast. But not fast enough.")
        else:
            type.type(hero + " looked at you. You looked at them. And you both knew.")
        
        print("\n")
        time.sleep(2)
        type.type(hero + " died in your arms.")
        print("\n")
        time.sleep(1)
        type.type(str(days) + " days together. Every single one mattered.")
        print("\n")
        type.type("They chose you. And in the end, they chose to die for you.")
        print("\n")
        time.sleep(1)
        type.type(red(bright(hero + " is gone.")))
        print("\n")
        
        self._companions[hero]["status"] = "dead"
        self.lose_sanity(35)
        self.hurt(10)
        
        # But you lived
        type.type("You're alive. Because of them. And you have to live with that.")
        print("\n")
        type.type("You bury " + hero + " somewhere quiet. Somewhere they'd like.")
        print("\n")
        type.type("You sit there for a long time.")
        print("\n")
        
        if not self.has_achievement("faithful_friend"):
            self.unlock_achievement("faithful_friend")
            type.type(yellow(bright("🏆 ACHIEVEMENT UNLOCKED: Faithful Friend - Lost a bonded companion who saved your life")))
            print("\n")
        print("\n")

    def companion_milestone(self):
        # EVENT: Celebrate a companion milestone (50 or 100 days together)
        # CONDITION: Must have a companion with 50+ days
        living = self.get_all_companions()
        milestone_companion = None
        milestone_days = 0
        
        for name, data in living.items():
            days = data.get("days_owned", 0)
            if days >= 100 and not self.has_met(f"{name}_100_days"):
                milestone_companion = name
                milestone_days = 100
                break
            elif days >= 50 and not self.has_met(f"{name}_50_days"):
                milestone_companion = name
                milestone_days = 50
                break
        
        if not milestone_companion:
            self.day_event()
            return
        
        self.meet(f"{milestone_companion}_{milestone_days}_days")
        companion = living[milestone_companion]
        comp_type = companion.get("type", "companion")
        
        type.type(cyan(bright("═══════════════════════════════════════")))
        print()
        type.type(cyan(bright(f"    {milestone_days} DAYS WITH {milestone_companion.upper()}")))
        print()
        type.type(cyan(bright("═══════════════════════════════════════")))
        print("\n")
        
        if milestone_days == 100:
            type.type("One hundred days. You and " + bright(milestone_companion) + ". Through everything.")
            print("\n")
            type.type("A hundred sunrises. A hundred nights. A hundred moments where having them")
            type.type(" was the only thing keeping you going.")
            print("\n")
            type.type("They chose you when nobody else would. And you chose them back.")
            print("\n")
            
            if "Dog" in comp_type:
                type.type("Lucky licks your face. He doesn't know what a hundred days means.")
                type.type(" He just knows that every single one of them included you.")
            elif "Cat" in comp_type:
                type.type("Whiskers headbutts your chin. Hard. This is the most affection a cat can show.")
                type.type(" It means more than words ever could.")
            elif "Crow" in comp_type:
                type.type("Mr. Pecks drops something in your lap. A gold coin. Real gold. Saving his best for today.")
            elif "Squirrel" in comp_type:
                type.type("Squirrelly presents you with the PERFECT acorn. They've been searching for a hundred days.")
            elif "Raccoon" in comp_type:
                type.type("Rusty washes your face with their tiny hands. Tenderly. Like a parent.")
            elif "Rabbit" in comp_type:
                type.type("Hopper does the biggest binky you've ever seen. Three feet of pure joy.")
            elif "Opossum" in comp_type:
                type.type("Patches doesn't play dead. Not even for a second. Total trust. Absolute faith in you.")
            elif "Rat" in comp_type:
                type.type("Slick falls asleep in your hand. Their whole body fits in your palm. Trusting you with everything.")
            else:
                type.type(milestone_companion + " stays close today. Closer than usual. They know.")
            
            print("\n")
            self.restore_sanity(25)
            self.heal(15)
            self.pet_companion(milestone_companion)
            self.pet_companion(milestone_companion)
            self.pet_companion(milestone_companion)
        else:
            type.type("Fifty days. Half a hundred. You and " + bright(milestone_companion) + ".")
            print("\n")
            type.type("They've been with you through the ups and downs. The wins and losses.")
            print("\n")
            type.type("You share your food. Your space. Your loneliness.")
            print("\n")
            type.type("In return, they give you the most valuable thing anyone can: their presence.")
            print("\n")
            self.restore_sanity(15)
            self.heal(10)
            self.pet_companion(milestone_companion)
            self.pet_companion(milestone_companion)
        
        print("\n")

    def companion_brings_friend(self):
        # EVENT: A companion brings another animal to you
        # CONDITION: Must have at least one companion, don't have all 8
        living = self.get_all_companions()
        if len(living) == 0:
            self.day_event()
            return
        
        # Check which base companions we DON'T have
        all_base = ["Squirrelly", "Whiskers", "Lucky", "Mr. Pecks", "Patches", "Rusty", "Slick", "Hopper"]
        missing = [name for name in all_base if not self.has_companion(name)]
        
        if len(missing) == 0:
            self.day_event()
            return
        
        # Pick a living companion as the "introducer"
        introducer = random.choice(list(living.keys()))
        new_friend = random.choice(missing)
        new_type = self._lists.get_companion_type(new_friend)
        
        if not new_type:
            self.day_event()
            return
        
        friend_type = new_type["type"]
        
        type.type(bright(introducer) + " shows up with a friend today.")
        print("\n")
        type.type("A " + friend_type.lower() + ". Scraggly. Wary. But following " + introducer + " closely.")
        print("\n")
        type.type(introducer + " seems to be... introducing you? Animals don't normally do this.")
        print("\n")
        type.type("The " + friend_type.lower() + " watches you carefully. Sizing you up.")
        print("\n")
        
        answer = ask.yes_or_no(f"Try to befriend the {friend_type.lower()}? ")
        
        if answer == "yes":
            type.type("You crouch down. Hold out your hand. Stay still. Wait.")
            print("\n")
            
            if random.randrange(3) != 0:  # 67% success
                type.type("Minutes pass. The " + friend_type.lower() + " approaches. Sniffs your hand.")
                print("\n")
                type.type("Then they look at " + introducer + ". Back at you. And they stay.")
                print("\n")
                type.type("Congratulations. " + bright(new_friend) + " has joined your growing family.")
                print("\n")
                self.add_companion(new_friend, friend_type)
                self.restore_sanity(10)
                type.type(introducer + " seems proud. They brought you a friend. What a concept.")
            else:
                type.type("The " + friend_type.lower() + " gets within arm's reach... then bolts.")
                print("\n")
                type.type(introducer + " chases after them briefly, then comes back to you.")
                print("\n")
                type.type("Can't win them all. But " + introducer + " tried. That counts.")
                self.restore_sanity(3)
        else:
            type.type("You're not ready for another companion. The " + friend_type.lower() + " seems to understand.")
            print("\n")
            type.type("They disappear back where they came from. " + introducer + " looks at you, puzzled.")
            print("\n")
            type.type("Maybe next time.")
            self.restore_sanity(2)
        print("\n")

    def companion_food_crisis(self):
        # EVENT: All your companions are hungry and you don't have much food
        # CONDITION: Must have 3+ companions, low balance
        living = self.get_all_companions()
        if len(living) < 3:
            self.day_event()
            return
        
        companion_names = list(living.keys())
        
        type.type("Morning. Your companions are hungry. All " + str(len(living)) + " of them.")
        print("\n")
        type.type("They look at you with expectant eyes. Hopeful eyes. Trusting eyes.")
        print("\n")
        type.type("You check your food situation. It's... not great.")
        print("\n")
        
        # Check for food items
        has_food = False
        food_items = ["Candy Bar", "Bag of Chips", "Turkey Sandwich", "Beef Jerky", 
                      "Cup Noodles", "Granola Bar", "Hot Dog", "Microwave Burrito",
                      "Dog Food", "Cat Food", "Birdseed", "Bag of Acorns", "Carrot", "Cheese"]
        available_food = [item for item in food_items if self.has_item(item)]
        
        if len(available_food) > 0:
            type.type("You have some food: " + ", ".join([magenta(bright(f)) for f in available_food[:3]]) + ".")
            print("\n")
            type.type("But not enough for everyone.")
            print("\n")
        else:
            type.type("You have nothing. Not a crumb.")
            print("\n")
        
        type.type("What do you do?")
        type.type("1. Share everything you have equally")
        type.type("2. Feed your favorites first")
        type.type("3. Go hungry yourself so they can all eat (costs $20)")
        type.type("4. Scrounge for food together")
        print("\n")
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            type.type("You divide what you have. Equal portions. Even if it means less for you.")
            print("\n")
            for name in companion_names:
                self.feed_companion(name)
            type.type("Nobody's full. But nobody's starving either. That's the best you can do.")
            print("\n")
            type.type("They all look at you with gratitude. You're doing your best.")
            self.restore_sanity(5)
            self.hurt(5)  # You went hungry
        elif choice == "2":
            type.type("You feed your closest companions first. The ones who've been with you longest.")
            print("\n")
            # Sort by days owned
            sorted_companions = sorted(companion_names, key=lambda n: living[n].get("days_owned", 0), reverse=True)
            fed = 0
            for name in sorted_companions:
                if fed < 2:  # Only feed top 2
                    self.feed_companion(name)
                    type.type(name + " eats. Grateful.")
                    print()
                    fed += 1
                else:
                    self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 3)
            print("\n")
            type.type("The ones who didn't get fed watch with hurt eyes. They remember.")
            self.lose_sanity(5)
        elif choice == "3":
            if self.get_balance() >= 20:
                type.type("You spend $20 at the gas station. Cheap stuff. But enough for all of them.")
                print("\n")
                self.change_balance(-20)
                for name in companion_names:
                    self.feed_companion(name)
                type.type("Every single one of your companions eats today. You don't.")
                print("\n")
                type.type("Your stomach growls. But they're fed. That's what matters.")
                self.hurt(8)
                self.restore_sanity(10)
            else:
                type.type("You don't even have $20. You search your pockets, the car, everywhere.")
                print("\n")
                type.type("You find enough for maybe one meal split between all of them.")
                for name in companion_names:
                    self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 2)
                self.lose_sanity(8)
        else:
            type.type("You take your whole crew out to scrounge. It's a sight - you and your animals, picking through the world together.")
            print("\n")
            if random.randrange(3) != 0:
                type.type("Behind a restaurant: day-old bread. Wilted salad. Some meat scraps.")
                print("\n")
                type.type("It's not gourmet. But it's food. You all eat together in the parking lot.")
                for name in companion_names:
                    self.feed_companion(name)
                self.heal(5)
                self.restore_sanity(8)
                type.type("This weird, misfit family meal is the happiest you've been in weeks.")
            else:
                type.type("Nothing. The dumpsters are empty. The world is cruel.")
                print("\n")
                type.type("You all go to bed hungry. Together. There's some comfort in that.")
                for name in companion_names:
                    self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 3)
                self.lose_sanity(5)
        print("\n")

    def companion_lost_adventure(self):
        # EVENT: A companion wanders off and you must search for them
        # CONDITION: Must have at least one companion
        living = self.get_all_companions()
        if len(living) == 0:
            self.day_event()
            return
        
        lost_name = random.choice(list(living.keys()))
        lost_data = living[lost_name]
        comp_type = lost_data.get("type", "companion")
        
        type.type("Something's wrong. " + bright(lost_name) + " is gone.")
        print("\n")
        type.type("You check the car. Under the seats. The trunk. The parking lot.")
        print("\n")
        type.type("Gone. Your " + comp_type.lower() + " is just... gone.")
        print("\n")
        type.type("Your heart sinks. Did they run away? Get taken? Get hurt?")
        print("\n")
        
        type.type("What do you do?")
        type.type("1. Search the immediate area")
        type.type("2. Search further out (takes hours)")
        type.type("3. Put up signs and wait")
        type.type("4. Accept they're gone")
        print("\n")
        
        choice = input("Choose: ").strip()
        
        if choice == "1":
            type.type("You search everywhere within two blocks. Calling their name. Looking in every corner.")
            print("\n")
            if random.randrange(3) != 0:
                if "Cat" in comp_type:
                    type.type("You find " + lost_name + " on a roof. Just sitting there. Watching you search. Judging.")
                elif "Dog" in comp_type:
                    type.type("You find " + lost_name + " in a neighbor's yard. Getting belly rubs from a stranger. The betrayal.")
                elif "Crow" in comp_type:
                    type.type("A caw from above. " + lost_name + " lands on your head. They were following you the entire time.")
                elif "Rabbit" in comp_type:
                    type.type("You find " + lost_name + " in a garden, eating someone's vegetables. Look of pure innocence.")
                elif "Raccoon" in comp_type:
                    type.type("You find " + lost_name + " in a dumpster. Of course. Living their best life.")
                elif "Rat" in comp_type:
                    type.type(lost_name + " appears from a drain. Clean. Smug. They had adventures down there.")
                elif "Squirrel" in comp_type:
                    type.type(lost_name + " drops from a tree onto your shoulder. Showoff.")
                else:
                    type.type(lost_name + " was hiding nearby the whole time. Came out when they heard your voice.")
                print("\n")
                type.type("Relief floods through you. " + lost_name + " is okay. You hug them (whether they want it or not).")
                self.restore_sanity(10)
                self.pet_companion(lost_name)
            else:
                type.type("No sign of them. Anywhere. Your calls echo off empty buildings.")
                print("\n")
                type.type("You head back to the car, defeated. And there they are. Sitting on the hood. Waiting for YOU.")
                print("\n")
                type.type("They were home the whole time. YOU were the one who was lost.")
                self.restore_sanity(8)
                self.pet_companion(lost_name)
        elif choice == "2":
            type.type("You spend three hours searching. Every alley. Every park. Every hiding spot.")
            print("\n")
            self.add_fatigue(3)
            if random.randrange(4) != 0:
                type.type("You find " + lost_name + " by the river. Calm. Peaceful. Like they just needed some alone time.")
                print("\n")
                type.type("Animals need space too. You get it. You scoop them up and head home.")
                self.restore_sanity(10)
                self.pet_companion(lost_name)
            else:
                type.type("You find signs of them. Tracks. Fur. But no " + lost_name + ".")
                print("\n")
                type.type("Exhausted, you head back to the car.")
                print("\n")
                if random.randrange(2) == 0:
                    type.type("The next morning, " + lost_name + " is back. Scratched up. Tired. But alive.")
                    self.restore_sanity(5)
                else:
                    type.type(lost_name + " doesn't come back. Not that night. Not the next morning.")
                    print("\n")
                    type.type("They're gone.")
                    self._companions[lost_name]["status"] = "lost"
                    self.lose_sanity(20)
        elif choice == "3":
            type.type("You make signs. MISSING: " + comp_type.upper() + ". ANSWERS TO " + lost_name.upper() + ".")
            print("\n")
            type.type("You tape them to poles. Wait by the car. Hope.")
            print("\n")
            if random.randrange(3) != 0:
                type.type("Hours later, a kid shows up. " + lost_name + " in their arms.")
                print("\n")
                type.type(quote("Is this yours? They were eating out of my trash."))
                print("\n")
                type.type("You've never been so grateful to a child in your life.")
                self.restore_sanity(10)
                self.pet_companion(lost_name)
            else:
                type.type("Nobody calls. Nobody comes. The signs flutter in the wind.")
                print("\n")
                type.type("You wait until dark. Then you go inside and try not to cry.")
                if random.randrange(2) == 0:
                    type.type(" " + lost_name + " shows up at dawn, like nothing happened. RELIEF.")
                    self.restore_sanity(5)
                else:
                    self._companions[lost_name]["status"] = "lost"
                    self.lose_sanity(20)
        else:
            type.type("You close your eyes. Take a breath. They're gone. Animals come and go.")
            print("\n")
            type.type("You tell yourself it's fine. You've lost things before. What's one more?")
            print("\n")
            type.type("It's not fine. But you pretend it is.")
            self._companions[lost_name]["status"] = "lost"
            self.lose_sanity(15)
        print("\n")

    def companion_bonded_moment(self):
        # EVENT: Special moment with a bonded companion
        # CONDITION: Must have at least one bonded companion
        living = self.get_all_companions()
        bonded = [name for name, data in living.items() if data.get("bonded")]
        
        if len(bonded) == 0:
            self.day_event()
            return
        
        name = random.choice(bonded)
        companion = living[name]
        comp_type = companion.get("type", "companion")
        days = companion.get("days_owned", 0)
        
        type.type("Late afternoon. The sun is going down. It's quiet.")
        print("\n")
        type.type(bright(name) + " is beside you. As always.")
        print("\n")
        
        mood = self._lists.get_companion_dialogue(name, "bonded")
        type.type(mood)
        print("\n")
        
        type.type("You've been together for " + str(days) + " days now. Through everything.")
        print("\n")
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("You remember the day you met. How scared they were. How scared YOU were.")
            print("\n")
            type.type("Neither of you is scared anymore. Not when you're together.")
        elif roll == 1:
            type.type("You talk to " + name + " sometimes. About your day. Your fears. Your dreams.")
            print("\n")
            type.type("They don't understand the words. But they understand the tone. The need.")
            print("\n")
            type.type("Sometimes that's all therapy is. Someone who listens without judgment.")
        elif roll == 2:
            type.type("There's a moment where you make eye contact. Long, slow, steady.")
            print("\n")
            type.type("In that moment, something passes between you. Not human. Not animal. Something else.")
            print("\n")
            type.type("A bond. Ancient and simple. 'I am with you. You are with me. That is enough.'")
        else:
            type.type("You realize something: you'd give up the million for " + name + ".")
            print("\n")
            type.type("Not in a sentimental way. In a real, concrete, mathematical way.")
            print("\n")
            type.type("Some things are worth more than money. " + name + " is one of them.")
        
        print("\n")
        self.restore_sanity(15)
        self.heal(10)
        self.pet_companion(name)
        print("\n")

    def companion_learns_trick(self):
        # EVENT: A bonded companion learns a useful trick
        # CONDITION: Must have a bonded companion
        living = self.get_all_companions()
        bonded = [name for name, data in living.items() if data.get("bonded")]
        
        if len(bonded) == 0:
            self.day_event()
            return
        
        name = random.choice(bonded)
        companion = living[name]
        comp_type = companion.get("type", "companion")
        
        type.type(bright(name) + " has been with you long enough to pick up some new tricks.")
        print("\n")
        
        if "Dog" in comp_type:
            roll = random.randrange(3)
            if roll == 0:
                type.type(name + " learned to bark once for 'yes' and twice for 'no.'")
                print("\n")
                type.type("You ask if they love you. One bark. Very loud.")
                self.restore_sanity(8)
            elif roll == 1:
                type.type(name + " learned to fetch specific items from the car. Like a furry butler.")
                print("\n")
                type.type("You say 'get the blanket.' " + name + " brings the blanket. Mind. Blown.")
                self.restore_sanity(5)
            else:
                type.type(name + " learned to alert you when someone approaches the car.")
                print("\n")
                type.type("One low growl for strangers. Happy whine for people they trust.")
                print("\n")
                type.type("You have a security system now. A three-legged, tail-wagging security system.")
                self.restore_sanity(8)
        elif "Cat" in comp_type:
            type.type(name + " learned to open the car door. From the INSIDE.")
            print("\n")
            type.type("This is either impressive or terrifying. They can leave whenever they want.")
            print("\n")
            type.type("They never do. That's the point. They choose to stay.")
            self.restore_sanity(10)
        elif "Crow" in comp_type:
            type.type(name + " learned to mimic your voice. They say 'hello' when you approach.")
            print("\n")
            type.type("It's haunting and wonderful. A crow that greets you. By name.")
            print("\n")
            type.type("Other people think it's creepy. You think it's the best thing ever.")
            self.restore_sanity(8)
        elif "Raccoon" in comp_type:
            type.type(name + " learned to sort your coins by type. Quarters, dimes, nickels.")
            print("\n")
            type.type("Then they tried to teach YOU. Apparently your sorting is insufficient.")
            print("\n")
            type.type("Raccoons have standards. Who knew?")
            self.restore_sanity(5)
            self.change_balance(random.randint(2, 10))
        elif "Rat" in comp_type:
            type.type(name + " learned to navigate mazes. Any maze. Every maze.")
            print("\n")
            type.type("You made one out of cardboard. They solved it in 8 seconds.")
            print("\n")
            type.type("Then they looked at you like 'really? That's the best you've got?'")
            self.restore_sanity(5)
        elif "Rabbit" in comp_type:
            type.type(name + " learned to come when you call their name. Rabbits don't usually do that.")
            print("\n")
            type.type("You call. They binky over. Every time. Without fail.")
            print("\n")
            type.type("It's like having a dog but softer and with better ears.")
            self.restore_sanity(8)
        elif "Opossum" in comp_type:
            type.type(name + " learned to play dead on command. Wait, they already did that.")
            print("\n")
            type.type("But now they play dead AND then 'resurrect' dramatically when you say 'alive!'")
            print("\n")
            type.type("It's a whole performance. You clap every time. " + name + " takes a bow.")
            self.restore_sanity(8)
        elif "Squirrel" in comp_type:
            type.type(name + " learned to bury and retrieve things on command.")
            print("\n")
            type.type("You can say 'hide this' and they'll bury it. Say 'find it' and they bring it back.")
            print("\n")
            type.type("You now have a squirrel safe deposit box. The world is amazing.")
            self.restore_sanity(5)
        else:
            type.type(name + " seems to understand more words now. 'Food.' 'Walk.' 'Stay.' 'Love.'")
            print("\n")
            type.type("Especially 'love.' They always react to that one.")
            self.restore_sanity(5)
        
        self.pet_companion(name)
        print("\n")

    def companion_nightmare(self):
        # EVENT: A companion has a nightmare and you comfort them
        # CONDITION: Must have at least one companion
        living = self.get_all_companions()
        if len(living) == 0:
            self.day_event()
            return
        
        name = random.choice(list(living.keys()))
        companion = living[name]
        comp_type = companion.get("type", "companion")
        
        type.type("The middle of the night. Something wakes you.")
        print("\n")
        type.type(bright(name) + " is making sounds in their sleep. Small, frightened sounds.")
        print("\n")
        
        if "Dog" in comp_type:
            type.type("Whimpering. Running legs. Lucky is chasing something in his dreams. Or being chased.")
            print("\n")
            type.type("You know he had a life before you. A harder life. One that took his leg.")
        elif "Cat" in comp_type:
            type.type("Twitching. Hissing softly. Whiskers is fighting something in their sleep.")
            print("\n")
            type.type("Street cats see things. Bad things. Those memories don't go away.")
        elif "Crow" in comp_type:
            type.type("Soft caws. Wings fluttering. Mr. Pecks is dreaming of flying. Or falling.")
        elif "Rabbit" in comp_type:
            type.type("Thumping. Fast breathing. Hopper is running from something in their dream.")
            print("\n")
            type.type("Rabbits are prey animals. Their nightmares are about one thing: not being fast enough.")
        elif "Raccoon" in comp_type:
            type.type("Chattering. Thrashing. Rusty is having a bad one.")
        elif "Rat" in comp_type:
            type.type("Squeaking. Trembling. Even in sleep, Slick is afraid.")
        elif "Opossum" in comp_type:
            type.type("Even in sleep, Patches is 'playing dead.' Body rigid. Instinct runs deep.")
        elif "Squirrel" in comp_type:
            type.type("Chirping softly. Paws moving. Squirrelly is burying something. Or losing something.")
        else:
            type.type("Small, frightened sounds. " + name + " is having a nightmare.")
        print("\n")
        
        type.type("You reach out. Gently. Carefully. And you stroke their fur/feathers.")
        print("\n")
        type.type("Slowly, the shaking stops. The whimpering fades. They press closer to you.")
        print("\n")
        type.type("You whisper: " + quote("It's okay. I'm here. You're safe."))
        print("\n")
        type.type("They can't understand the words. But they understand the warmth. The touch. The safety.")
        print("\n")
        type.type("You stay awake until they're peaceful. It costs you sleep.")
        print("\n")
        type.type("It's worth it.")
        self.pet_companion(name)
        self.restore_sanity(8)
        self.add_fatigue(2)
        print("\n")

    # ==========================================
    # CRAFTED ITEM EVENTS
    # ==========================================

    def companion_bed_bonus(self):
        """Companion bed improves companion rest and happiness"""
        companions = self.get_all_companions()
        alive = {n: d for n, d in companions.items() if d["status"] == "alive"}
        if len(alive) == 0:
            type.type("The car is quiet tonight. Just you and your thoughts.")
            print("\n")
            return

        name = random.choice(list(alive.keys()))
        if self.has_item("Companion Bed"):
            bed_texts = [
                cyan(bright(name)) + " climbs into the " + cyan(bright("Companion Bed")) + " you made, turns around three times, and flops down with a contented sigh. They're asleep in seconds.",
                "You watch " + cyan(bright(name)) + " discover the " + cyan(bright("Companion Bed")) + " again, as if for the first time. Same reaction every night: sniff, circle, plop, sleep.",
                cyan(bright(name)) + " has claimed the " + cyan(bright("Companion Bed")) + " as sovereign territory. No other creature may use it. This is law.",
                "The " + cyan(bright("Companion Bed")) + " is working wonders. " + cyan(bright(name)) + " sleeps deeper, eats better, and looks at you with something dangerously close to love.",
                cyan(bright(name)) + " drags a sock into the " + cyan(bright("Companion Bed")) + ". Your sock. It's theirs now. Interior decorating.",
            ]
            type.type(random.choice(bed_texts))
            self.pet_companion(name)
            self.restore_sanity(2)
            print("\n")
        else:
            type.type(cyan(bright(name)) + " tries to find a comfortable spot in the car. ")
            type.type("They shift. And shift again. And again. The car isn't built for sleeping. ")
            type.type("Neither are you. You're in this together.")
            print("\n")

    def pet_toy_playtime(self):
        """Playing with companion using the pet toy"""
        companions = self.get_all_companions()
        alive = {n: d for n, d in companions.items() if d["status"] == "alive"}
        if len(alive) == 0:
            return
        name = random.choice(list(alive.keys()))
        if self.has_item("Pet Toy"):
            play_texts = [
                "You toss the " + cyan(bright("Pet Toy")) + " and " + cyan(bright(name)) + " goes BALLISTIC. Chasing, pouncing, shaking it side to side. Absolute carnage. Maximum joy.",
                cyan(bright(name)) + " finds the " + cyan(bright("Pet Toy")) + " and brings it to you, dropping it at your feet. Throw it. THROW IT. They're vibrating with anticipation.",
                "You squeak the " + cyan(bright("Pet Toy")) + " once. " + cyan(bright(name)) + " materializes from nowhere. How did they move that fast? Science can't explain it.",
                "You play tug-of-war with " + cyan(bright(name)) + " using the " + cyan(bright("Pet Toy")) + ". They're surprisingly strong. You might actually lose this.",
                cyan(bright(name)) + " has been carrying the " + cyan(bright("Pet Toy")) + " around all day like a trophy. Won't let it go. Won't share. Mine. ALL MINE.",
            ]
            type.type(random.choice(play_texts))
            self.pet_companion(name)
            self.restore_sanity(3)
            print("\n")
        else:
            type.type(cyan(bright(name)) + " looks bored. They nudge a random object across the floor. ")
            type.type("They need a toy. Something to play with. You make a mental note.")
            print("\n")

    def feeding_station_morning(self):
        """Feeding station makes morning companion care easier"""
        companions = self.get_all_companions()
        alive = {n: d for n, d in companions.items() if d["status"] == "alive"}
        if len(alive) == 0:
            return

        name = random.choice(list(alive.keys()))
        if self.has_item("Feeding Station"):
            station_texts = [
                "The " + cyan(bright("Feeding Station")) + " is doing its job. " + cyan(bright(name)) + " eats at their own pace, no mess, no fuss. You almost feel like a responsible pet owner.",
                cyan(bright(name)) + " is already eating when you wake up. The " + cyan(bright("Feeding Station")) + " keeps their food clean and accessible. One less thing to worry about.",
                "You refill the " + cyan(bright("Feeding Station")) + ". " + cyan(bright(name)) + " watches you do it with intense focus, tail wagging. They know what that container means.",
                "The " + cyan(bright("Feeding Station")) + " has paid for itself ten times over. " + cyan(bright(name)) + " is healthier, happier, and less likely to eat your socks. Win-win-win.",
            ]
            type.type(random.choice(station_texts))
            self.pet_companion(name)
            self.restore_sanity(1)
            print("\n")
        else:
            type.type("You tear off a piece of whatever you have and set it on the floor for " + cyan(bright(name)) + ". ")
            type.type("They eat it off the ground. You feel a pang of guilt. They deserve better.")
            print("\n")

