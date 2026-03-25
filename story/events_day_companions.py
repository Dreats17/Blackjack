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

class DayCompanionsMixin:
    """Companion events: all companion-specific encounters and bonds"""

    def companion_reunion(self):
        # SECRET: Have 3+ companions - they all show up at once
        companion_count = len(self._companions) if hasattr(self, '_companions') else 0
        if companion_count < 3:
            self.day_event()
            return
        type.type("You're sitting in your car outside the casino when you see something strange.")
        print(PAR)
        type.type("All of your friends. All of them. Walking toward you together.")
        print(PAR)
        type.type("The stray cat. The crow. The people you've met along the way.")
        print(PAR)
        type.type("They don't say anything. They just... gather around you.")
        print(PAR)
        type.type("For a moment, you're not alone. Not a solo gambler living in a car.")
        print(PAR)
        type.type("You're someone with PEOPLE. Connections. A weird, misfit family.")
        print(PAR)
        type.type("The moment passes. Everyone drifts away. But the warmth stays.")
        self.restore_sanity(20)
        self.heal(10)
        print(PAR)

        print(PAR)
        return
    def the_cat_knows(self):
        # SECRET: Have the stray cat companion - they lead you to something
        if not self.has_companion("Stray Cat"):
            self.day_event()
            return
        type.type("Your stray cat is acting strange. Meowing insistently. Tugging at your shoelace.")
        print(PAR)
        type.type("It wants you to follow. So you do.")
        print(PAR)
        type.type("Through the parking lot. Behind the dumpsters. Into a drainage culvert.")
        print(PAR)
        type.type("There, hidden in the darkness, you find a small box.")
        print(PAR)
        type.type("Inside: " + green(bright("$75")) + " in cash, a locket with no picture, and a note:")
        print(PAR)
        type.type(quote("For whoever needs this more than I did. -M"))
        print(PAR)
        type.type("The cat purrs. You don't know how it knew. Cats are weird like that.")
        self.change_balance(75)
        self.add_item("Empty Locket")
        self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def lucky_guards_car(self):
        # EVENT: Lucky the three-legged dog protects your car from a thief
        # CONDITION: Must have Lucky alive
        if not self.has_companion("Lucky") or self.get_companion("Lucky")["status"] != "alive":
            self.day_event()
            return
        type.type("You come back to your car after a walk. Something's wrong.")
        print(PAR)
        type.type("A man is crouched by your window. Slim jim in hand. Trying to break in.")
        print(PAR)
        type.type("Then you hear it. A growl. Low, deep, primal.")
        print(PAR)
        type.type(bright("Lucky") + " is standing between the thief and your car. Three legs planted. Teeth bared.")
        print(PAR)
        type.type("The thief looks at this three-legged dog and has a moment of calculation.")
        print(PAR)
        type.type("Lucky barks once. It echoes off every car in the lot. The thief drops the slim jim and bolts.")
        print(PAR)
        type.type("Lucky trots over to you, tail wagging like nothing happened. Hero behavior.")
        print(PAR)
        type.type("You kneel down and hug him. He licks your ear.")
        print(PAR)
        type.type(green("Lucky protected your car! Good boy."))
        self.restore_sanity(8)
        self.pet_companion("Lucky")
        self.pet_companion("Lucky")  # Double pet for being a hero
        print(PAR)

        print(PAR)
        return
    def mr_pecks_treasure(self):
        # EVENT: Mr. Pecks the crow brings you money or valuables
        # CONDITION: Must have Mr. Pecks alive
        if not self.has_companion("Mr. Pecks") or self.get_companion("Mr. Pecks")["status"] != "alive":
            self.day_event()
            return
        companion = self.get_companion("Mr. Pecks")
        type.type("You hear tapping on your car window. " + bright("Mr. Pecks") + " is outside, something in his beak.")
        print(PAR)

        if self.has_item("Marvin's Monocle"):
            amount = random.randint(120, 280) if companion["bonded"] else random.randint(40, 90)
            type.type("You slip on " + cyan(bright("Marvin's Monocle")) + " before opening the window. Through the smoky lens, the pile in Mr. Pecks' beak stops looking like random shiny garbage and starts looking like a ledger.")
            print(PAR)
            type.type("Clean cash. Pawnable metal. Hot wallet. Sentimental trash. You sort the whole bundle in seconds while Mr. Pecks watches like an assistant expecting praise.")
            print(PAR)
            type.type("You keep the clean valuables and ditch the trouble. Total safe haul: " + green(bright("${:,}".format(amount))) + ".")
            self.change_balance(amount)
            self.restore_sanity(5 if companion["bonded"] else 3)
            self.pet_companion("Mr. Pecks")
            if self.has_item("Disposable Camera"):
                print(PAR)
                type.type("You grab your " + cyan(bright("Disposable Camera")) + " and catch Mr. Pecks puffing up beside the sorted loot like a career professional.")
                print(PAR)
                type.type("Click. Evidence of excellent teamwork and technically deniable crime.")
                self.restore_sanity(4)
            print(PAR)
            return
        
        if companion["bonded"]:
            # Bonded Mr. Pecks finds REALLY good stuff
            roll = random.randrange(4)
            if roll == 0:
                amount = random.randint(50, 200)
                type.type("He drops a crumpled bill through the window crack. Then another. And another.")
                print(PAR)
                type.type("Mr. Pecks has been COLLECTING. There's a small pile of bills.")
                print(PAR)
                type.type("You count it up: " + green(bright("${:,}".format(amount))) + ".")
                print(PAR)
                type.type("Where did he get all this? You know what, don't ask. Just appreciate the crow.")
                self.change_balance(amount)
            elif roll == 1:
                type.type("He drops a golden ring into your lap. It's real. Actual gold.")
                print(PAR)
                type.type("Mr. Pecks caws proudly. He knows exactly what he found.")
                print(PAR)
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
                print(PAR)
                type.type("You look at the name. It's nobody you know. This is stolen property.")
                print(PAR)
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
                print(PAR)
                type.type("About " + green(bright("${:,}".format(amount))) + " worth. Not bad for a bird.")
                self.change_balance(amount)
        else:
            # Non-bonded Mr. Pecks finds smaller stuff
            roll = random.randrange(3)
            if roll == 0:
                amount = random.randint(5, 30)
                type.type("A crumpled bill drops from his beak. A few coins follow.")
                print(PAR)
                type.type(green(bright("${:,}".format(amount))) + ". Not much, but the gesture means everything.")
                self.change_balance(amount)
            elif roll == 1:
                type.type("He drops a bottle cap in your lap. Stares at you expectantly.")
                print(PAR)
                type.type("It's... worthless. But he's so PROUD of it. You act impressed.")
                print(PAR)
                type.type("Mr. Pecks caws with satisfaction and flies off to find more treasures.")
                self.restore_sanity(3)
            else:
                type.type("He drops a shiny button. Then a paperclip. Then a key to... something.")
                print(PAR)
                type.type("You have no idea what any of this opens or does. But you keep it all.")
                print(PAR)
                type.type("Mr. Pecks' treasure collection grows. So does your heart.")
                self.restore_sanity(5)
        
        self.pet_companion("Mr. Pecks")
        if self.has_item("Disposable Camera"):
            print(PAR)
            type.type("You grab your " + cyan(bright("Disposable Camera")) + " and catch Mr. Pecks mid-strut, beak up, completely self-satisfied.")
            print(PAR)
            type.type("Click. That's a perfect photograph. A crow with a treasure and a man who needed one. Both very pleased.")
            self.restore_sanity(4)
        print(PAR)

        print(PAR)
        return
    def rusty_midnight_heist(self):
        # EVENT: Rusty the raccoon steals something useful while you weren't looking
        # CONDITION: Must have Rusty alive
        if not self.has_companion("Rusty") or self.get_companion("Rusty")["status"] != "alive":
            self.day_event()
            return
        companion = self.get_companion("Rusty")
        type.type("You wake up to find " + bright("Rusty") + " sitting on the dashboard with something.")
        print(PAR)
        type.type("They chitter excitedly, tiny paws wrapped around their latest acquisition.")
        print(PAR)
        
        if companion["bonded"]:
            roll = random.randrange(5)
            if roll == 0:
                amount = random.randint(50, 150)
                type.type("It's a wallet. Not yours. Someone else's.")
                print(PAR)
                type.type("There's " + green(bright("${:,}".format(amount))) + " inside. Plus a driver's license.")
                print(PAR)
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
                print(PAR)
                type.type("You eat half. Rusty eats half. You make eye contact. This is the good life.")
                self.heal(10)
                self.feed_companion("Rusty")
            elif roll == 2:
                type.type("It's a set of car keys. To a car much nicer than yours.")
                print(PAR)
                type.type("You put them on the roof of a random car in the lot. Probably the right one.")
                print(PAR)
                type.type("Rusty chitters in protest. That was GOOD loot!")
                self.restore_sanity(3)
            elif roll == 3:
                type.type("It's a smartphone. Cracked screen, but it works.")
                print(PAR)
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
                print(PAR)
                type.type("You share the rest. Rusty washes each piece in your water bottle first. Of course they do.")
                self.heal(5)
                self.restore_sanity(3)
        else:
            roll = random.randrange(3)
            if roll == 0:
                type.type("It's... a sock. One sock. Wet. Rusty is very proud.")
                print(PAR)
                type.type("You accept the sock with the gravity it deserves. This is a gift.")
                self.restore_sanity(2)
            elif roll == 1:
                type.type("It's a half-eaten candy bar. Rusty took one bite, then decided you should have the rest.")
                print(PAR)
                type.type("Sharing is caring, raccoon-style.")
                self.heal(3)
            else:
                amount = random.randint(1, 10)
                type.type("It's a handful of coins they dug out of a fountain. " + green(bright("${:,}".format(amount))) + ".")
                print(PAR)
                type.type("Rusty is learning. They'll be a master thief soon.")
                self.change_balance(amount)
        
        self.pet_companion("Rusty")
        print(PAR)

        print(PAR)
        return
    def whiskers_sixth_sense(self):
        # EVENT: Whiskers senses danger and warns you
        # CONDITION: Must have Whiskers alive
        if not self.has_companion("Whiskers") or self.get_companion("Whiskers")["status"] != "alive":
            self.day_event()
            return
        type.type("You're about to leave the car when " + bright("Whiskers") + " does something unusual.")
        print(PAR)
        type.type("They plant themselves on your lap. Claws out. Not moving.")
        print(PAR)
        type.type("You try to stand up. Whiskers hisses. Not at you. At the door. At what's outside.")
        print(PAR)
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("You wait. Five minutes pass. Then you hear it.")
            print(PAR)
            type.type("Shouting. A fight breaks out in the parking lot. Two men, fists and blood.")
            print(PAR)
            type.type("If you'd walked out five minutes ago, you'd have been right in the middle of it.")
            print(PAR)
            type.type("Whiskers purrs. " + cyan("Danger avoided."))
            self.restore_sanity(10)
        elif roll == 1:
            type.type("You stay put. Through the window, you see a police cruiser pull into the lot.")
            print(PAR)
            type.type("They're checking cars. Asking questions. Looking for someone.")
            print(PAR)
            type.type("They spend ten minutes searching, then leave. Whatever they were looking for, it wasn't you.")
            print(PAR)
            type.type("Whiskers relaxes. You can go now. The coast is clear.")
            self.restore_sanity(5)
        elif roll == 2:
            type.type("You stay. Twenty minutes later, the sky opens up. Torrential rain. Lightning.")
            print(PAR)
            type.type("The parking lot floods in minutes. If you'd been walking, you'd be soaked and miserable.")
            print(PAR)
            type.type("Whiskers curls up on your lap and purrs. Warm. Dry. Safe.")
            self.restore_sanity(8)
            self.heal(5)
        else:
            type.type("You listen to the cat. Something about their urgency makes you trust them completely.")
            print(PAR)
            type.type("A truck blows through the parking lot way too fast. Right through the spot where you'd have been standing.")
            print(PAR)
            type.type("Your blood goes cold. Whiskers saved your life. Actually saved your life.")
            print(PAR)
            type.type("You hold the cat tight. They tolerate the hug. Just this once.")
            self.restore_sanity(15)
        
        self.pet_companion("Whiskers")
        print(PAR)

        print(PAR)
        return
    def slick_escape_route(self):
        # EVENT: Slick the rat knows every escape route and saves you from trouble
        # CONDITION: Must have Slick alive
        if not self.has_companion("Slick") or self.get_companion("Slick")["status"] != "alive":
            self.day_event()
            return
        type.type("You're walking near the back of the casino when two guys step out of an alley.")
        print(PAR)
        type.type(quote("Hey. You. Come here."))
        print(PAR)
        type.type("They don't look friendly. Your heart rate spikes.")
        print(PAR)
        type.type("Then " + bright("Slick") + " starts squeaking frantically from your pocket. They're tugging your shirt.")
        print(PAR)
        type.type("Left. Slick wants you to go left. Into what looks like a dead end.")
        print(PAR)
        type.type("You trust the rat. You run left.")
        print(PAR)
        type.type("It's not a dead end. There's a gap between the buildings. Barely wide enough for a person.")
        print(PAR)
        type.type("You squeeze through. Behind you, the two guys try to follow but they're too big.")
        print(PAR)
        type.type(quote("Get back here!"))
        print(PAR)
        type.type("You emerge on a busy street. People everywhere. Safe.")
        print(PAR)
        type.type("Slick peeks out of your pocket and bruxes contentedly. They knew. They always know.")
        print(PAR)
        type.type(green("Slick knew the escape route! They always do."))
        self.restore_sanity(10)
        self.pet_companion("Slick")
        print(PAR)

        print(PAR)
        return
    def hopper_lucky_day(self):
        # EVENT: Hopper the rabbit brings you luck
        # CONDITION: Must have Hopper alive
        if not self.has_companion("Hopper") or self.get_companion("Hopper")["status"] != "alive":
            self.day_event()
            return
        type.type(bright("Hopper") + " binkies around the car this morning. Full of energy. Full of... something.")
        print(PAR)
        type.type("You can feel it in the air. Today is going to be a good day.")
        print(PAR)
        
        roll = random.randrange(4)
        if roll == 0:
            amount = random.randint(20, 100)
            type.type("You find money in your coat pocket you forgot about. " + green(bright("${:,}".format(amount))) + ".")
            print(PAR)
            type.type("Then a stranger holds the door for you. Then the vending machine gives you two sodas for the price of one.")
            print(PAR)
            type.type("Little things. But they add up. Hopper's luck is infectious.")
            self.change_balance(amount)
            self.restore_sanity(5)
        elif roll == 1:
            type.type("Someone drops a scratch ticket. It lands right at your feet.")
            print(PAR)
            type.type("You pick it up. Haven't scratched it yet.")
            print(PAR)
            amount = random.randint(50, 500)
            type.type("You scratch it off with a coin. " + green(bright("${:,}".format(amount))) + " WINNER!")
            print(PAR)
            type.type("You look at Hopper. Hopper twitches their nose. Luck incarnate.")
            self.change_balance(amount)
            self.restore_sanity(5)
        elif roll == 2:
            type.type("Every green light. Every parking spot open. Every coin in the meter.")
            print(PAR)
            type.type("It's not one big lucky thing. It's twenty small lucky things.")
            print(PAR)
            type.type("Hopper rides in your lap, nose twitching, and you swear the world bends around this rabbit.")
            self.restore_sanity(10)
            self.heal(5)
        else:
            type.type("A woman stops you in the street.")
            print(PAR)
            type.type(quote("Is that a rabbit? Can I pet it?"))
            print(PAR)
            type.type("Hopper is, for once, perfectly behaved. Lets the woman pet them. Makes her day.")
            print(PAR)
            type.type("She's so happy she insists on buying you coffee. You end up talking for an hour.")
            print(PAR)
            type.type("Human connection. Warmth. Kindness. Thanks to a rabbit.")
            self.restore_sanity(12)
        
        self.pet_companion("Hopper")
        print(PAR)

        print(PAR)
        return
    def patches_night_watch(self):
        # EVENT: Patches the opossum notices something at night that helps you during the day
        # CONDITION: Must have Patches alive
        if not self.has_companion("Patches") or self.get_companion("Patches")["status"] != "alive":
            self.day_event()
            return
        type.type(bright("Patches") + " was up all night. As usual. But this morning, they're insistent about something.")
        print(PAR)
        type.type("Patches keeps pawing at the window, looking toward the back of the parking lot.")
        print(PAR)
        type.type("You follow the opossum's lead and investigate.")
        print(PAR)
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("Behind a dumpster, hidden under cardboard: a stash. Someone's stash.")
            print(PAR)
            amount = random.randint(50, 200)
            type.type("Cash. " + green(bright("${:,}".format(amount))) + " in a rubber-banded roll. Drug money? Emergency fund? Who knows.")
            print(PAR)
            answer = ask.option("What do you do? ", ["take it", "leave it"])
            if answer == "take it":
                type.type("Finders keepers. Patches found it first, technically.")
                self.change_balance(amount)
            else:
                type.type("You leave it. Not your money. Not your problem.")
                self.restore_sanity(5)
        elif roll == 1:
            type.type("Patches saw someone tampering with your car last night. Tire's been loosened.")
            print(PAR)
            type.type("If you'd driven without checking, the wheel could have come off at speed.")
            print(PAR)
            type.type("You tighten it back. Thank the opossum. Patches plays dead from the compliment.")
            print(PAR)
            type.type(green("Patches might have saved your life with their night watch."))
            self.restore_sanity(10)
        elif roll == 2:
            type.type("There's a kitten. Tiny. Alone. Crying under a car.")
            print(PAR)
            type.type("Patches heard it last night but waited for you to help. Smart possum.")
            print(PAR)
            type.type("You rescue the kitten. It's shaking, cold, starving.")
            print(PAR)
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
            print(PAR)
            type.type("Pancakes, eggs, coffee. All free. All you can eat.")
            print(PAR)
            type.type("You eat until you're actually full. When was the last time that happened?")
            print(PAR)
            type.type("Patches had some too. They ate scrambled eggs with their tiny hands. People stared. Worth it.")
            self.heal(15)
            self.restore_sanity(5)
            self.feed_companion("Patches")
        
        self.pet_companion("Patches")
        print(PAR)

        print(PAR)
        return
    def squirrelly_stash(self):
        # EVENT: Squirrelly's hoarding habit leads to a discovery
        # CONDITION: Must have Squirrelly alive
        if not self.has_companion("Squirrelly") or self.get_companion("Squirrelly")["status"] != "alive":
            self.day_event()
            return
        type.type(bright("Squirrelly") + " has been burying things around the parking lot for weeks.")
        print(PAR)
        type.type("Today, they dig something up and bring it to you. Chattering excitedly.")
        print(PAR)
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("It's an acorn. Just an acorn. But Squirrelly presents it like it's the Hope Diamond.")
            print(PAR)
            type.type("You hold it solemnly. Squirrelly chatters with approval. You have been deemed worthy.")
            print(PAR)
            type.type("It's just a nut. But the love behind it is real.")
            self.restore_sanity(5)
        elif roll == 1:
            amount = random.randint(5, 40)
            type.type("It's a collection of coins Squirrelly buried over the last few weeks.")
            print(PAR)
            type.type("Nickels, quarters, a few half-dollars. About " + green(bright("${:,}".format(amount))) + " total.")
            print(PAR)
            type.type("Squirrelly was SAVING for you. Squirrel investment portfolio.")
            self.change_balance(amount)
            self.restore_sanity(3)
        elif roll == 2:
            type.type("They unearthed a small jewelry box. Tarnished. Old. Someone buried it here years ago.")
            print(PAR)
            type.type("Inside: a locket with a faded photo. Two people, smiling. From another era.")
            print(PAR)
            type.type("You don't know their story. But you hope they were happy.")
            self.restore_sanity(8)
        else:
            type.type("Squirrelly dug up... more acorns. A LOT of acorns. A mountain of acorns.")
            print(PAR)
            type.type("They've been burying acorns all season. The parking lot is basically an acorn mine now.")
            print(PAR)
            type.type("Squirrelly sits atop the acorn pile like a dragon on their hoard. Majestic.")
            print(PAR)
            type.type("You are witnessing peak squirrel. This is their life's work.")
            self.restore_sanity(5)
        
        self.pet_companion("Squirrelly")
        print(PAR)

        print(PAR)
        return
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
        print(PAR)
        
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
        print(PAR)
        
        type.type("Your companion is sick. What do you do?")
        print(PAR)

        if self.has_item("Flask of Anti-Virus"):
            type.type("You uncork the " + cyan(bright("Flask of Anti-Virus")) + " and place a drop on " + bright(name) + "'s tongue.")
            print(PAR)
            type.type("The flask fights the infection before it can take hold. Within an hour, " + bright(name) + " is eating again.")
            print(PAR)
            type.type("The flask still has plenty left.")
            self.pet_companion(name)
            self.restore_sanity(8)
            print(PAR)
            return

        if self.has_item("Flask of Anti-Venom"):
            type.type("You apply the " + cyan(bright("Flask of Anti-Venom")) + " carefully. Whatever got into " + bright(name) + " doesn't stand a chance.")
            print(PAR)
            type.type("The recovery is faster than you expected. " + bright(name) + " shakes it off by nightfall.")
            print(PAR)
            type.type("The flask still has plenty left.")
            self.pet_companion(name)
            self.restore_sanity(8)
            print(PAR)
            return

        if self.has_item("Splint"):
            type.type("You notice " + bright(name) + " favoring one leg. Not sick — injured.")
            print(PAR)
            type.type("You grab your " + cyan(bright("Splint")) + " and carefully brace the limb. Duct tape and care.")
            print(PAR)
            type.type(bright(name) + " tests the leg. Gingerly. Then again. It holds.")
            print(PAR)
            type.type("Not a vet. But good enough for the road.")
            self.pet_companion(name)
            self.restore_sanity(5)
            print(PAR)
            return

        choice = ask.option("Your choice?", ["help", "vet", "wait", "food"])
        
        if choice == "help" and self.has_item("Cough Drops"):
            type.type("You crush up some cough drops and mix them with water. Not exactly veterinary medicine.")
            print(PAR)
            type.type(name + " drinks. Slowly. After a few hours, they seem a little better.")
            print(PAR)
            type.type("Not great. But alive. That's what matters.")
            self.use_item("Cough Drops")
            self.pet_companion(name)
            self.restore_sanity(5)
        elif choice == "vet":
            vet_cost = random.randint(50, 200)
            if self.get_balance() >= vet_cost:
                type.type("You rush " + name + " to the nearest vet. Emergency appointment.")
                print(PAR)
                type.type("The vet examines them. Medication. Fluids. The works.")
                print(PAR)
                type.type("Cost: " + red(bright("${:,}".format(vet_cost))) + ". Worth every penny.")
                print(PAR)
                type.type(name + " perks up by evening. The medication worked. They're going to be okay.")
                self.change_balance(-vet_cost)
                self.pet_companion(name)
                self.pet_companion(name)
                self.restore_sanity(10)
            else:
                type.type("You don't have enough money for a vet. You try your best with what you have.")
                print(PAR)
                type.type(name + " looks at you with trusting eyes. You feel like you're failing them.")
                self.lose_sanity(10)
                # 50/50 chance they pull through
                if random.randrange(2) == 0:
                    type.type("By morning, " + name + " is drinking water again. They're tough. They'll make it.")
                    self.pet_companion(name)
                else:
                    type.type("By morning, " + name + " is worse. Much worse.")
                    self.companion_dies(name, "illness")
        elif choice == "wait":
            type.type("You decide to wait. Nature will take its course.")
            print(PAR)
            chance = random.randrange(3)
            if chance == 0:
                type.type("By the next morning, " + name + " bounces back. Whatever it was, they fought it off.")
                self.pet_companion(name)
                self.restore_sanity(3)
            elif chance == 1:
                type.type(name + " stays sick for days. Weak. Fragile. But they hang on. Barely.")
                print(PAR)
                # Lose a lot of happiness
                self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 20)
                self.lose_sanity(8)
            else:
                type.type(name + " doesn't make it through the night.")
                print(PAR)
                type.type("You wake up and they're gone. Still. Cold.")
                print(PAR)
                type.type("You could have done something. Should have done something.")
                self.companion_dies(name, "illness")
        else:
            type.type("You give " + name + " extra food and fresh water. Stay close. Keep them warm.")
            print(PAR)
            self.feed_companion(name)
            if random.randrange(3) != 0:
                type.type(name + " eats a little. Drinks. By evening, they're moving around more.")
                print(PAR)
                type.type("Not 100%. But better. Your care made the difference.")
                self.pet_companion(name)
                self.restore_sanity(5)
            else:
                type.type(name + " won't eat. Won't drink. They're getting worse.")
                self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 15)
                self.lose_sanity(5)
        print(PAR)

        print(PAR)
        return
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
        print(PAR)
        type.type(bright(comp1) + " and " + bright(comp2) + " are fighting.")
        print(PAR)
        
        # Flavor based on types
        if "Cat" in type1 or "Cat" in type2:
            type.type("Hissing. Yowling. The kind of sounds that make your blood curdle.")
        elif "Dog" in type1 or "Dog" in type2:
            type.type("Growling. Barking. Snapping jaws and bared teeth.")
        elif "Crow" in type1 or "Crow" in type2:
            type.type("Cawing. Wing-beating. Pecking. Feathers everywhere.")
        else:
            type.type("Chattering. Squealing. Tiny fury unleashed.")
        print(PAR)
        
        type.type("They're going at it over territory. Your car only has so much space.")
        print(PAR)
        type.type("What do you do?")
        choice = ask.option("Your choice?", ["break", "release", "let", "bribe"])
        
        if choice == "break":
            type.type("You carefully intervene. Separating them with a blanket between them.")
            print(PAR)
            if random.randrange(3) == 0:
                type.type("You get scratched/bitten in the process. Ouch.")
                self.hurt(5)
            type.type("They glare at each other from opposite sides of the car. Tense, but calm.")
            print(PAR)
            type.type("This is a fragile peace. But it's peace.")
            self._companions[comp1]["happiness"] = max(0, self._companions[comp1]["happiness"] - 5)
            self._companions[comp2]["happiness"] = max(0, self._companions[comp2]["happiness"] - 5)
        elif choice == "release":
            type.type("You can't keep them both. One has to go.")
            print(PAR)
            type.type(f"Release {comp1}, release {comp2}, or never mind?")
            release_choice = ask.option("Which one do you release?", ["first", "second", "nevermind"])
            if release_choice == "first":
                type.type("You carry " + comp1 + " outside. Set them down gently.")
                print(PAR)
                type.type("They look back at you once. Then they're gone. Into the world. Without you.")
                print(PAR)
                self._companions[comp1]["status"] = "lost"
                self.lose_sanity(15)
            elif release_choice == "second":
                type.type("You carry " + comp2 + " outside. Set them down gently.")
                print(PAR)
                type.type("They look back at you once. Then they're gone. Into the world. Without you.")
                print(PAR)
                self._companions[comp2]["status"] = "lost"
                self.lose_sanity(15)
            else:
                type.type("You can't do it. You'll make this work somehow.")
                self._companions[comp1]["happiness"] = max(0, self._companions[comp1]["happiness"] - 10)
                self._companions[comp2]["happiness"] = max(0, self._companions[comp2]["happiness"] - 10)
        elif choice == "let":
            type.type("You let nature take its course. Survival of the fittest.")
            print(PAR)
            if random.randrange(4) == 0:
                # One gets seriously hurt
                loser = random.choice([comp1, comp2])
                winner = comp2 if loser == comp1 else comp1
                type.type(bright(loser) + " gets the worst of it. They're limping. Bleeding.")
                print(PAR)
                type.type(bright(winner) + " claims the back seat. Dominance established.")
                print(PAR)
                type.type("But " + loser + " might not recover from those injuries...")
                self._companions[loser]["happiness"] = max(0, self._companions[loser]["happiness"] - 25)
                if random.randrange(4) == 0:
                    type.type(loser + " didn't survive the injuries.")
                    self.companion_dies(loser, "fight with " + winner)
            else:
                type.type("After a lot of noise and fury, they settle into an uneasy truce.")
                print(PAR)
                type.type("Opposite corners. Cold shoulders. But alive.")
                self._companions[comp1]["happiness"] = max(0, self._companions[comp1]["happiness"] - 8)
                self._companions[comp2]["happiness"] = max(0, self._companions[comp2]["happiness"] - 8)
        else:
            type.type("You break out the food. Two separate piles. Equal portions.")
            print(PAR)
            type.type("The fighting stops immediately. Food > territory disputes.")
            print(PAR)
            type.type("They eat side by side. Not friends yet. But not enemies anymore.")
            self.feed_companion(comp1)
            self.feed_companion(comp2)
            self.restore_sanity(3)
        
        self.lose_sanity(5)
        print(PAR)

        print(PAR)
        return
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
        print(PAR)
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("A stray dog. Big one. Aggressive. Foam around its mouth. Coming right at you.")
            print(PAR)
            if hero == "Lucky":
                type.type(bright("Lucky") + " launches himself at the stray. Three legs, but zero hesitation.")
                print(PAR)
                type.type("The two dogs collide. Lucky is smaller. Weaker. But he fights like his life depends on it.")
                print(PAR)
                type.type("Because YOUR life depends on it.")
                print(PAR)
                type.type("The stray backs off. Slinks away. Lucky stands over you, bleeding from a scratch, tail wagging.")
                self.hurt(0)
                self._companions["Lucky"]["happiness"] = max(0, self._companions["Lucky"]["happiness"] - 3)
            elif "Cat" in hero_type:
                type.type(bright(hero) + " leaps onto the dog's face. Claws extended. A feline missile.")
                print(PAR)
                type.type("The dog yelps, shakes its head, can't get the cat off. Runs away howling.")
                print(PAR)
                type.type(hero + " lands gracefully. Licks a paw. Walks away like nothing happened.")
            elif "Crow" in hero_type:
                type.type(bright(hero) + " dive-bombs the dog. Over and over. Cawing. Pecking. Relentless.")
                print(PAR)
                type.type("An entire murder of crows joins in. The dog is overwhelmed. Retreats.")
                print(PAR)
                type.type(hero + " lands on your shoulder and caws once. You're welcome.")
            else:
                type.type(bright(hero) + " makes enough noise to attract attention. People come running.")
                print(PAR)
                type.type("The stray bolts. " + hero + " chatters/squeaks with relief. Their alarm saved you.")
            print(PAR)
            type.type(green(hero + " protected you!"))
            self.restore_sanity(12)
            
        elif roll == 1:
            type.type("You're about to step into the street. Earbuds in. Not paying attention.")
            print(PAR)
            type.type(bright(hero) + " suddenly goes WILD. Biting your shoelace. Pulling your pants. Screaming bloody murder.")
            print(PAR)
            type.type("You stop. Annoyed. Look up.")
            print(PAR)
            type.type("A truck blows through the intersection. Red light. Seventy miles an hour.")
            print(PAR)
            type.type("Right where you would have been standing.")
            print(PAR)
            type.type("You sit down on the curb. Shaking. " + hero + " climbs into your lap.")
            print(PAR)
            type.type("They knew. Somehow, they knew.")
            self.restore_sanity(15)
            
        elif roll == 2:
            type.type("You're sleeping in your car. Middle of the night. Something wakes you.")
            print(PAR)
            type.type(bright(hero) + " is agitated. Frantic. Pawing at the door.")
            print(PAR)
            type.type("You get out. Groggy. Confused. Then you smell it.")
            print(PAR)
            type.type("Gas. Your car is leaking gas. The engine is hot. One spark and...")
            print(PAR)
            type.type("You back away. Far away. The car doesn't explode, but it could have. With you in it.")
            print(PAR)
            type.type(hero + " saved your life. No question about it.")
            self.restore_sanity(15)
            self.add_danger("Fuel Leak")
            
        else:
            type.type("A man approaches you. Friendly enough. Asking for directions.")
            print(PAR)
            type.type("But " + bright(hero) + " starts growling/hissing/squeaking aggressively at him.")
            print(PAR)
            type.type("You notice: his hand is behind his back. Something metal glints.")
            print(PAR)
            type.type("You step back. Say you don't know the area. Walk away quickly.")
            print(PAR)
            type.type("You look back once. He's moved on to someone else. You see the knife now.")
            print(PAR)
            type.type(hero + "'s instinct was right. They read people better than you do.")
            self.restore_sanity(10)
        
        self.pet_companion(hero)
        self.pet_companion(hero)
        print(PAR)

        print(PAR)
        return
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
        print(PAR)
        time.sleep(1)
        
        type.type("It happened fast. Walking near the road. Lost in thought. Not paying attention.")
        print(PAR)
        type.type("The car came out of nowhere. Hit-and-run driver. Barreling right at you.")
        print(PAR)
        time.sleep(1)
        
        if "Dog" in hero_type:
            type.type(bright(hero) + " hit you from the side. All three legs pushing. Everything they had.")
            print(PAR)
            type.type("You went left. " + hero + " went right. Into the path of the car.")
        elif "Cat" in hero_type:
            type.type(bright(hero) + " yowled. That horrible, blood-curdling cat scream. You instinctively jumped back.")
            print(PAR)
            type.type("But " + hero + " didn't jump back. " + hero + " jumped forward. Into the road. Drawing the car's attention.")
        elif "Crow" in hero_type:
            type.type(bright(hero) + " flew directly at the windshield. Wings spread. A living shield.")
            print(PAR)
            type.type("The driver swerved. Missed you by inches. Didn't miss " + hero + ".")
        else:
            type.type(bright(hero) + " threw themselves in front of you. Pushed you. Bit you. Did everything they could to move you.")
            print(PAR)
            type.type("You stumbled. Fell. The car missed you. It didn't miss " + hero + ".")
        
        print(PAR)
        time.sleep(2)
        type.type("You scrambled to " + hero + ". Knelt down. Held them.")
        print(PAR)
        type.type("They were still warm. Still breathing. Barely.")
        print(PAR)
        time.sleep(1)
        
        if "Dog" in hero_type:
            type.type(hero + "'s tail wagged. One last time. Weak. But there.")
            print(PAR)
            type.type("Good boy. The best boy. The best boy who ever lived.")
        elif "Cat" in hero_type:
            type.type(hero + " purred. Even now. Even like this. Purring against your chest.")
            print(PAR)
            type.type("Cats purr when they're happy. They also purr when they're dying. A final comfort.")
        elif "Crow" in hero_type:
            type.type(hero + " looked at you with one intelligent eye. No sound. Just... recognition.")
            print(PAR)
            type.type("They recognized you. Until the very end.")
        elif "Rabbit" in hero_type:
            type.type(hero + " twitched their nose. Once. Twice. Then went still.")
            print(PAR)
            type.type("So fast. Rabbits are so fast. But not fast enough.")
        else:
            type.type(hero + " looked at you. You looked at them. And you both knew.")
        
        print(PAR)
        time.sleep(2)
        type.type(hero + " died in your arms.")
        print(PAR)
        time.sleep(1)
        type.type(str(days) + " days together. Every single one mattered.")
        print(PAR)
        type.type("They chose you. And in the end, they chose to die for you.")
        print(PAR)
        time.sleep(1)
        type.type(red(bright(hero + " is gone.")))
        print(PAR)
        
        self._companions[hero]["status"] = "dead"
        self.lose_sanity(35)
        self.hurt(10)
        
        # But you lived
        type.type("You're alive. Because of them. And you have to live with that.")
        print(PAR)
        type.type("You bury " + hero + " somewhere quiet. Somewhere they'd like.")
        print(PAR)
        type.type("You sit there for a long time.")
        print(PAR)
        
        if not self.has_achievement("faithful_friend"):
            self.unlock_achievement("faithful_friend")
            type.type(yellow(bright("🏆 ACHIEVEMENT UNLOCKED: Faithful Friend - Lost a bonded companion who saved your life")))
            print(PAR)
        print(PAR)

        print(PAR)
        return
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
        print(PAR)
        type.type(cyan(bright(f"    {milestone_days} DAYS WITH {milestone_companion.upper()}")))
        print(PAR)
        type.type(cyan(bright("═══════════════════════════════════════")))
        print(PAR)
        
        if milestone_days == 100:
            type.type("One hundred days. You and " + bright(milestone_companion) + ". Through everything.")
            print(PAR)
            type.type("A hundred sunrises. A hundred nights. A hundred moments where having them")
            type.type(" was the only thing keeping you going.")
            print(PAR)
            type.type("They chose you when nobody else would. And you chose them back.")
            print(PAR)
            
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
            
            print(PAR)
            self.restore_sanity(25)
            self.heal(15)
            self.pet_companion(milestone_companion)
            self.pet_companion(milestone_companion)
            self.pet_companion(milestone_companion)
        else:
            type.type("Fifty days. Half a hundred. You and " + bright(milestone_companion) + ".")
            print(PAR)
            type.type("They've been with you through the ups and downs. The wins and losses.")
            print(PAR)
            type.type("You share your food. Your space. Your loneliness.")
            print(PAR)
            type.type("In return, they give you the most valuable thing anyone can: their presence.")
            print(PAR)
            self.restore_sanity(15)
            self.heal(10)
            self.pet_companion(milestone_companion)
            self.pet_companion(milestone_companion)
        
        print(PAR)

        print(PAR)
        return
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
        print(PAR)
        type.type("A " + friend_type.lower() + ". Scraggly. Wary. But following " + introducer + " closely.")
        print(PAR)
        type.type(introducer + " seems to be... introducing you? Animals don't normally do this.")
        print(PAR)
        type.type("The " + friend_type.lower() + " watches you carefully. Sizing you up.")
        print(PAR)
        
        answer = ask.yes_or_no(f"Try to befriend the {friend_type.lower()}? ")
        
        if answer == "yes":
            type.type("You crouch down. Hold out your hand. Stay still. Wait.")
            print(PAR)
            
            if random.randrange(3) != 0:  # 67% success
                type.type("Minutes pass. The " + friend_type.lower() + " approaches. Sniffs your hand.")
                print(PAR)
                type.type("Then they look at " + introducer + ". Back at you. And they stay.")
                print(PAR)
                type.type("Congratulations. " + bright(new_friend) + " has joined your growing family.")
                print(PAR)
                self.add_companion(new_friend, friend_type)
                self.restore_sanity(10)
                type.type(introducer + " seems proud. They brought you a friend. What a concept.")
            else:
                type.type("The " + friend_type.lower() + " gets within arm's reach... then bolts.")
                print(PAR)
                type.type(introducer + " chases after them briefly, then comes back to you.")
                print(PAR)
                type.type("Can't win them all. But " + introducer + " tried. That counts.")
                self.restore_sanity(3)
        else:
            type.type("You're not ready for another companion. The " + friend_type.lower() + " seems to understand.")
            print(PAR)
            type.type("They disappear back where they came from. " + introducer + " looks at you, puzzled.")
            print(PAR)
            type.type("Maybe next time.")
            self.restore_sanity(2)
        print(PAR)

        print(PAR)
        return
    def companion_food_crisis(self):
        # EVENT: All your companions are hungry and you don't have much food
        # CONDITION: Must have 3+ companions, low balance
        living = self.get_all_companions()
        if len(living) < 3:
            self.day_event()
            return
        
        companion_names = list(living.keys())
        
        if self.has_item("Provider's Kit"):
            type.type("The " + magenta(bright("Provider's Kit")) + " provides for two. Companion eats well.")
            print(PAR)
            type.type("Rabbit in the trap, fish on the line. Everyone fed.")
            print(PAR)
            for name in companion_names:
                self.feed_companion(name)
            self.restore_sanity(5)
            print(PAR)
            return
        
        type.type("Morning. Your companions are hungry. All " + str(len(living)) + " of them.")
        print(PAR)
        type.type("They look at you with expectant eyes. Hopeful eyes. Trusting eyes.")
        print(PAR)
        type.type("You check your food situation. It's... not great.")
        print(PAR)
        
        # Check for food items
        has_food = False
        food_items = ["Candy Bar", "Bag of Chips", "Turkey Sandwich", "Beef Jerky", 
                      "Cup Noodles", "Granola Bar", "Hot Dog", "Microwave Burrito",
                      "Dog Food", "Cat Food", "Birdseed", "Bag of Acorns", "Carrot", "Cheese"]
        available_food = [item for item in food_items if self.has_item(item)]
        
        if len(available_food) > 0:
            type.type("You have some food: " + ", ".join([magenta(bright(f)) for f in available_food[:3]]) + ".")
            print(PAR)
            type.type("But not enough for everyone.")
            print(PAR)
        else:
            type.type("You have nothing. Not a crumb.")
            print(PAR)
        
        type.type("What do you do?")
        choice = ask.option("Your choice?", ["share", "favorites", "hungry", "scrounge"])
        
        if choice == "share":
            type.type("You divide what you have. Equal portions. Even if it means less for you.")
            print(PAR)
            for name in companion_names:
                self.feed_companion(name)
            type.type("Nobody's full. But nobody's starving either. That's the best you can do.")
            print(PAR)
            type.type("They all look at you with gratitude. You're doing your best.")
            self.restore_sanity(5)
            self.hurt(5)  # You went hungry
        elif choice == "favorites":
            type.type("You feed your closest companions first. The ones who've been with you longest.")
            print(PAR)
            # Sort by days owned
            sorted_companions = sorted(companion_names, key=lambda n: living[n].get("days_owned", 0), reverse=True)
            fed = 0
            for name in sorted_companions:
                if fed < 2:  # Only feed top 2
                    self.feed_companion(name)
                    type.type(name + " eats. Grateful.")
                    print(PAR)
                    fed += 1
                else:
                    self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 3)
            print(PAR)
            type.type("The ones who didn't get fed watch with hurt eyes. They remember.")
            self.lose_sanity(5)
        elif choice == "hungry":
            if self.get_balance() >= 20:
                type.type("You spend $20 at the gas station. Cheap stuff. But enough for all of them.")
                print(PAR)
                self.change_balance(-20)
                for name in companion_names:
                    self.feed_companion(name)
                type.type("Every single one of your companions eats today. You don't.")
                print(PAR)
                type.type("Your stomach growls. But they're fed. That's what matters.")
                self.hurt(8)
                self.restore_sanity(10)
            else:
                type.type("You don't even have $20. You search your pockets, the car, everywhere.")
                print(PAR)
                type.type("You find enough for maybe one meal split between all of them.")
                for name in companion_names:
                    self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 2)
                self.lose_sanity(8)
        else:
            type.type("You take your whole crew out to scrounge. It's a sight - you and your animals, picking through the world together.")
            print(PAR)
            if random.randrange(3) != 0:
                type.type("Behind a restaurant: day-old bread. Wilted salad. Some meat scraps.")
                print(PAR)
                type.type("It's not gourmet. But it's food. You all eat together in the parking lot.")
                for name in companion_names:
                    self.feed_companion(name)
                self.heal(5)
                self.restore_sanity(8)
                type.type("This weird, misfit family meal is the happiest you've been in weeks.")
            else:
                type.type("Nothing. The dumpsters are empty. The world is cruel.")
                print(PAR)
                type.type("You all go to bed hungry. Together. There's some comfort in that.")
                for name in companion_names:
                    self._companions[name]["happiness"] = max(0, self._companions[name]["happiness"] - 3)
                self.lose_sanity(5)
        print(PAR)

        print(PAR)
        return
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
        print(PAR)
        type.type("You check the car. Under the seats. The trunk. The parking lot.")
        print(PAR)
        type.type("Gone. Your " + comp_type.lower() + " is just... gone.")
        print(PAR)
        type.type("Your heart sinks. Did they run away? Get taken? Get hurt?")
        print(PAR)
        
        type.type("What do you do?")
        choice = ask.option("Your choice?", ["search", "far", "signs", "accept"])
        
        if choice == "search":
            type.type("You search everywhere within two blocks. Calling their name. Looking in every corner.")
            print(PAR)
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
                print(PAR)
                type.type("Relief floods through you. " + lost_name + " is okay. You hug them (whether they want it or not).")
                self.restore_sanity(10)
                self.pet_companion(lost_name)
            else:
                type.type("No sign of them. Anywhere. Your calls echo off empty buildings.")
                print(PAR)
                type.type("You head back to the car, defeated. And there they are. Sitting on the hood. Waiting for YOU.")
                print(PAR)
                type.type("They were home the whole time. YOU were the one who was lost.")
                self.restore_sanity(8)
                self.pet_companion(lost_name)
        elif choice == "far":
            type.type("You spend three hours searching. Every alley. Every park. Every hiding spot.")
            print(PAR)
            self.add_fatigue(3)
            if random.randrange(4) != 0:
                type.type("You find " + lost_name + " by the river. Calm. Peaceful. Like they just needed some alone time.")
                print(PAR)
                type.type("Animals need space too. You get it. You scoop them up and head home.")
                self.restore_sanity(10)
                self.pet_companion(lost_name)
            else:
                type.type("You find signs of them. Tracks. Fur. But no " + lost_name + ".")
                print(PAR)
                type.type("Exhausted, you head back to the car.")
                print(PAR)
                if random.randrange(2) == 0:
                    type.type("The next morning, " + lost_name + " is back. Scratched up. Tired. But alive.")
                    self.restore_sanity(5)
                else:
                    type.type(lost_name + " doesn't come back. Not that night. Not the next morning.")
                    print(PAR)
                    type.type("They're gone.")
                    self._companions[lost_name]["status"] = "lost"
                    self.lose_sanity(20)
        elif choice == "signs":
            type.type("You make signs. MISSING: " + comp_type.upper() + ". ANSWERS TO " + lost_name.upper() + ".")
            print(PAR)
            type.type("You tape them to poles. Wait by the car. Hope.")
            print(PAR)
            if random.randrange(3) != 0:
                type.type("Hours later, a kid shows up. " + lost_name + " in their arms.")
                print(PAR)
                type.type(quote("Is this yours? They were eating out of my trash."))
                print(PAR)
                type.type("You've never been so grateful to a child in your life.")
                self.restore_sanity(10)
                self.pet_companion(lost_name)
            else:
                type.type("Nobody calls. Nobody comes. The signs flutter in the wind.")
                print(PAR)
                type.type("You wait until dark. Then you go inside and try not to cry.")
                if random.randrange(2) == 0:
                    type.type(" " + lost_name + " shows up at dawn, like nothing happened. RELIEF.")
                    self.restore_sanity(5)
                else:
                    self._companions[lost_name]["status"] = "lost"
                    self.lose_sanity(20)
        else:
            type.type("You close your eyes. Take a breath. They're gone. Animals come and go.")
            print(PAR)
            type.type("You tell yourself it's fine. You've lost things before. What's one more?")
            print(PAR)
            type.type("It's not fine. But you pretend it is.")
            self._companions[lost_name]["status"] = "lost"
            self.lose_sanity(15)
        print(PAR)

        print(PAR)
        return
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

        # COMBO: Pet Toy + Companion Bed + Feeding Station = Perfect Home
        if self.has_item("Pet Toy") and self.has_item("Companion Bed") and self.has_item("Feeding Station"):
            type.type(cyan(bright("Perfect Home.")) + " The " + cyan(bright("Companion Bed")) + " is soft. The " + cyan(bright("Feeding Station")) + " is full. The " + cyan(bright("Pet Toy")) + " is within reach.")
            print(PAR)
            type.type(bright(name) + " is living their absolute best life. Better than most humans, honestly.")
            print(PAR)
            type.type("They eat, they play, they sleep in a bed that smells like you. Their tail hasn't stopped wagging in days.")
            print(PAR)
            type.type("Happiness doesn't decay when you've built a home this good. " + bright(name) + " is content. Permanently.")
            self._companions[name]["happiness"] = 100
            self.restore_sanity(20)
            self.pet_companion(name)
            print(PAR)
            return
        
        type.type("Late afternoon. The sun is going down. It's quiet.")
        print(PAR)
        type.type(bright(name) + " is beside you. As always.")
        print(PAR)
        
        mood = self._lists.get_companion_dialogue(name, "bonded")
        type.type(mood)
        print(PAR)
        
        type.type("You've been together for " + str(days) + " days now. Through everything.")
        print(PAR)
        
        roll = random.randrange(4)
        if roll == 0:
            type.type("You remember the day you met. How scared they were. How scared YOU were.")
            print(PAR)
            type.type("Neither of you is scared anymore. Not when you're together.")
        elif roll == 1:
            type.type("You talk to " + name + " sometimes. About your day. Your fears. Your dreams.")
            print(PAR)
            type.type("They don't understand the words. But they understand the tone. The need.")
            print(PAR)
            type.type("Sometimes that's all therapy is. Someone who listens without judgment.")
        elif roll == 2:
            type.type("There's a moment where you make eye contact. Long, slow, steady.")
            print(PAR)
            type.type("In that moment, something passes between you. Not human. Not animal. Something else.")
            print(PAR)
            type.type("A bond. Ancient and simple. 'I am with you. You are with me. That is enough.'")
        else:
            type.type("You realize something: you'd give up the million for " + name + ".")
            print(PAR)
            type.type("Not in a sentimental way. In a real, concrete, mathematical way.")
            print(PAR)
            type.type("Some things are worth more than money. " + name + " is one of them.")
        
        print(PAR)
        self.restore_sanity(15)
        self.heal(10)
        self.pet_companion(name)
        if self.has_item("Delight Indicator") or self.has_item("Delight Manipulator"):
            gauge = "Delight Manipulator" if self.has_item("Delight Manipulator") else "Delight Indicator"
            print(PAR)
            type.type("The " + cyan(bright(gauge)) + " reads " + green("'Content'") + " for the first time in weeks.")
            print(PAR)
            type.type("Maybe that's enough. Maybe that's everything.")
        if self.has_item("Beast Tamer Kit"):
            print(PAR)
            type.type("The " + cyan(bright("Beast Tamer Kit")) + " hasn't left your bag. " + bright(name) + " senses it — the bait, the toy, the whole philosophy of 'patience and treats.'")
            print(PAR)
            type.type("They look at you with new respect.")
            self._companions[name]["happiness"] = min(100, self._companions[name].get("happiness", 50) + 10)
            self.restore_sanity(4)
        if self.has_item("Deck of Cards"):
            print(PAR)
            type.type("You shuffle the " + cyan(bright("Deck of Cards")) + " absently. " + bright(name) + " watches the cards with total animal focus.")
            print(PAR)
            type.type("You fan them out, flip them over, riffle them back together. Their eyes track every card like it's the most important thing in the world.")
            print(PAR)
            type.type("Maybe it is. Maybe you both needed something simple to look at.")
            self.restore_sanity(4)
        print(PAR)

        print(PAR)
        return
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
        print(PAR)

        if self.has_item("Ark Master's Horn"):
            type.type("The " + cyan(bright("Ark Master's Horn")) + " bonds you to " + bright(name) + " at the deepest level. Unbreakable loyalty.")
            print(PAR)
            type.type(bright(name) + " doesn't just learn one trick — they learn everything. Sit. Guard. Fetch. Attack. Heal. All at once.")
            print(PAR)
            type.type("The bond is permanent. " + bright(name) + " will never leave your side.")
            self.restore_sanity(15)
            self.pet_companion(name)
            print(PAR)
            return

        if self.has_item("Dog Whistle") and "Dog" in comp_type:
            type.type("You pull out the " + cyan(bright("Dog Whistle")) + " and blow a short, clean note. " + bright(name) + " snaps to attention.")
            print(PAR)
            type.type("You run through the motions once. Sit. Stay. Come. The whistle cuts through every distraction.")
            print(PAR)
            type.type(bright(name) + " nails every command on the first try. You didn't know they had that in them.")
            print(PAR)
            type.type("Turns out, neither did they.")
            self.restore_sanity(10)
            self.pet_companion(name)
            print(PAR)
            return

        if "Dog" in comp_type:
            roll = random.randrange(3)
            if roll == 0:
                type.type(name + " learned to bark once for 'yes' and twice for 'no.'")
                print(PAR)
                type.type("You ask if they love you. One bark. Very loud.")
                self.restore_sanity(8)
            elif roll == 1:
                type.type(name + " learned to fetch specific items from the car. Like a furry butler.")
                print(PAR)
                type.type("You say 'get the blanket.' " + name + " brings the blanket. Mind. Blown.")
                self.restore_sanity(5)
            else:
                type.type(name + " learned to alert you when someone approaches the car.")
                print(PAR)
                type.type("One low growl for strangers. Happy whine for people they trust.")
                print(PAR)
                type.type("You have a security system now. A three-legged, tail-wagging security system.")
                self.restore_sanity(8)
        elif "Cat" in comp_type:
            type.type(name + " learned to open the car door. From the INSIDE.")
            print(PAR)
            type.type("This is either impressive or terrifying. They can leave whenever they want.")
            print(PAR)
            type.type("They never do. That's the point. They choose to stay.")
            self.restore_sanity(10)
        elif "Crow" in comp_type:
            type.type(name + " learned to mimic your voice. They say 'hello' when you approach.")
            print(PAR)
            type.type("It's haunting and wonderful. A crow that greets you. By name.")
            print(PAR)
            type.type("Other people think it's creepy. You think it's the best thing ever.")
            self.restore_sanity(8)
        elif "Raccoon" in comp_type:
            type.type(name + " learned to sort your coins by type. Quarters, dimes, nickels.")
            print(PAR)
            type.type("Then they tried to teach YOU. Apparently your sorting is insufficient.")
            print(PAR)
            type.type("Raccoons have standards. Who knew?")
            self.restore_sanity(5)
            self.change_balance(random.randint(2, 10))
        elif "Rat" in comp_type:
            type.type(name + " learned to navigate mazes. Any maze. Every maze.")
            print(PAR)
            type.type("You made one out of cardboard. They solved it in 8 seconds.")
            print(PAR)
            type.type("Then they looked at you like 'really? That's the best you've got?'")
            self.restore_sanity(5)
        elif "Rabbit" in comp_type:
            type.type(name + " learned to come when you call their name. Rabbits don't usually do that.")
            print(PAR)
            type.type("You call. They binky over. Every time. Without fail.")
            print(PAR)
            type.type("It's like having a dog but softer and with better ears.")
            self.restore_sanity(8)
        elif "Opossum" in comp_type:
            type.type(name + " learned to play dead on command. Wait, they already did that.")
            print(PAR)
            type.type("But now they play dead AND then 'resurrect' dramatically when you say 'alive!'")
            print(PAR)
            type.type("It's a whole performance. You clap every time. " + name + " takes a bow.")
            self.restore_sanity(8)
        elif "Squirrel" in comp_type:
            type.type(name + " learned to bury and retrieve things on command.")
            print(PAR)
            type.type("You can say 'hide this' and they'll bury it. Say 'find it' and they bring it back.")
            print(PAR)
            type.type("You now have a squirrel safe deposit box. The world is amazing.")
            self.restore_sanity(5)
        else:
            type.type(name + " seems to understand more words now. 'Food.' 'Walk.' 'Stay.' 'Love.'")
            print(PAR)
            type.type("Especially 'love.' They always react to that one.")
            self.restore_sanity(5)
        
        self.pet_companion(name)
        if self.has_item("Devil's Deck"):
            print(PAR)
            type.type("You produce the " + cyan(bright("Devil's Deck")) + ". The cards float and shuffle themselves in front of " + bright(name) + ".")
            print(PAR)
            type.type("They are transfixed. Not scared. Just absolutely riveted.")
            self._companions[name]["happiness"] = min(100, self._companions[name].get("happiness", 50) + 10)
            self.restore_sanity(5)
        elif self.has_item("Fortune Cards"):
            print(PAR)
            type.type("You deal the " + cyan(bright("Fortune Cards")) + " for " + bright(name) + ". Their card comes up: " + italic("THE FAITHFUL") + ".")
            print(PAR)
            type.type("It's accurate. Uncomfortably accurate.")
            self.restore_sanity(4)
        print(PAR)
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
        print(PAR)
        type.type(bright(name) + " is making sounds in their sleep. Small, frightened sounds.")
        print(PAR)
        
        if "Dog" in comp_type:
            type.type("Whimpering. Running legs. Lucky is chasing something in his dreams. Or being chased.")
            print(PAR)
            type.type("You know he had a life before you. A harder life. One that took his leg.")
        elif "Cat" in comp_type:
            type.type("Twitching. Hissing softly. Whiskers is fighting something in their sleep.")
            print(PAR)
            type.type("Street cats see things. Bad things. Those memories don't go away.")
        elif "Crow" in comp_type:
            type.type("Soft caws. Wings fluttering. Mr. Pecks is dreaming of flying. Or falling.")
        elif "Rabbit" in comp_type:
            type.type("Thumping. Fast breathing. Hopper is running from something in their dream.")
            print(PAR)
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
        print(PAR)
        
        type.type("You reach out. Gently. Carefully. And you stroke their fur/feathers.")
        print(PAR)
        type.type("Slowly, the shaking stops. The whimpering fades. They press closer to you.")
        print(PAR)
        type.type("You whisper: " + quote("It's okay. I'm here. You're safe."))
        print(PAR)
        type.type("They can't understand the words. But they understand the warmth. The touch. The safety.")
        print(PAR)
        type.type("You stay awake until they're peaceful. It costs you sleep.")
        print(PAR)
        type.type("It's worth it.")
        self.pet_companion(name)
        self.restore_sanity(8)
        self.add_fatigue(2)
        if self.has_item("Night Scope") or self.has_item("Flashlight") or self.has_item("Headlamp"):
            light_name = "Night Scope" if self.has_item("Night Scope") else ("Flashlight" if self.has_item("Flashlight") else "Headlamp")
            print(PAR)
            type.type("You sweep the " + cyan(bright(light_name)) + " around your sleeping companion. Nothing threatening within 100 yards.")
            print(PAR)
            type.type("You go back to sleep.")
            self.restore_sanity(3)
        print(PAR)

    # ==========================================
    # CRAFTED ITEM EVENTS
    # ==========================================

        print(PAR)
        return
    def companion_bed_bonus(self):
        """Companion bed improves companion rest and happiness"""
        companions = self.get_all_companions()
        alive = {n: d for n, d in companions.items() if d["status"] == "alive"}
        if len(alive) == 0:
            type.type("The car is quiet tonight. Just you and your thoughts.")
            print(PAR)
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
            print(PAR)
        else:
            type.type(cyan(bright(name)) + " tries to find a comfortable spot in the car. ")
            type.type("They shift. And shift again. And again. The car isn't built for sleeping. ")
            type.type("Neither are you. You're in this together.")
            print(PAR)

        print(PAR)
        return
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
            print(PAR)
        else:
            type.type(cyan(bright(name)) + " looks bored. They nudge a random object across the floor. ")
            type.type("They need a toy. Something to play with. You make a mental note.")
            print(PAR)

        print(PAR)
        return
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
            print(PAR)
        else:
            type.type("You tear off a piece of whatever you have and set it on the floor for " + cyan(bright(name)) + ". ")
            type.type("They eat it off the ground. You feel a pang of guilt. They deserve better.")
            print(PAR)

        print(PAR)
        return
    def buddy_dog_whistle_synergy(self):
        """Buddy (Dog) + Dog Whistle synergy event"""
        if not self.has_companion("Buddy") or not self.has_item("Dog Whistle"):
            self.day_event()
            return
        type.type("You pull out the " + cyan(bright("Dog Whistle")) + " without thinking.")
        print(PAR)
        type.type(cyan(bright("Buddy")) + " goes absolutely berserk. Spinning. Leaping. Barking at nothing. At everything.")
        print(PAR)
        type.type("When he finally stops spinning, he shoves his nose under a bush and digs furiously.")
        print(PAR)
        reward = random.randint(20, 50)
        roll = random.randrange(3)
        if roll == 0:
            type.type("He emerges with a crumpled " + green(bright("$" + str(reward))) + " in his mouth. Tail wagging. Very proud.")
            self.change_balance(reward)
        elif roll == 1:
            type.type("He emerges with a " + cyan(bright("Granola Bar")) + ". Slightly slobbery. Still sealed.")
            self.add_item("Granola Bar")
        else:
            type.type("He emerges with a " + cyan(bright("Bandage")) + " still in the wrapper. You'll take it.")
            self.add_item("Bandage")
        print(PAR)
        type.type("Good boy.")
        self._companions["Buddy"]["happiness"] = min(100, self._companions["Buddy"]["happiness"] + 10)
        print(PAR)

        print(PAR)
        return
    def thunder_running_shoes_synergy(self):
        """Thunder (Horse) + Running Shoes synergy event"""
        if not self.has_companion("Thunder") or not self.has_item("Running Shoes"):
            self.day_event()
            return
        type.type("You lace up your " + cyan(bright("Running Shoes")) + " and start down the road at a jog.")
        print(PAR)
        type.type(cyan(bright("Thunder")) + " falls in beside you without being asked.")
        print(PAR)
        type.type("Matching your pace exactly. Glancing sideways at you. Hooves on asphalt, shoes on asphalt.")
        print(PAR)
        type.type("You've never felt this fast. This light. Like the road belongs to both of you.")
        print(PAR)
        type.type("You run until your lungs burn. " + cyan(bright("Thunder")) + " could go forever.")
        self._companions["Thunder"]["happiness"] = min(100, self._companions["Thunder"]["happiness"] + 10)
        self.restore_sanity(8)
        print(PAR)

        print(PAR)
        return
    def grace_dream_catcher_synergy(self):
        """Grace (Deer) + Dream Catcher synergy event"""
        if not self.has_companion("Grace") or not self.has_item("Dream Catcher"):
            self.day_event()
            return
        type.type(cyan(bright("Grace")) + " noses the " + cyan(bright("Dream Catcher")) + " hanging from your mirror.")
        print(PAR)
        type.type("She turns it slowly with her muzzle. Studies it. Seems satisfied.")
        print(PAR)
        type.type("She settles beside your car with her eyes closed. Still. Peaceful.")
        print(PAR)
        type.type("No nightmares tonight. You're sure of it.")
        self._companions["Grace"]["happiness"] = min(100, self._companions["Grace"]["happiness"] + 10)
        self.restore_sanity(10)
        print(PAR)

        print(PAR)
        return
    def echo_camera_synergy(self):
        """Echo (Cat) + Disposable Camera synergy event"""
        if not self.has_companion("Echo") or not self.has_item("Disposable Camera"):
            self.day_event()
            return
        type.type(cyan(bright("Echo")) + " notices the " + cyan(bright("Disposable Camera")) + ".")
        print(PAR)
        type.type("She poses on the hood. Paw extended. Chin lifted. Then the trunk. Then the tire.")
        print(PAR)
        type.type("She KNOWS the camera is there. She has always known.")
        print(PAR)
        type.type("You take every shot. You don't regret a single one.")
        self._companions["Echo"]["happiness"] = min(100, self._companions["Echo"]["happiness"] + 10)
        self.restore_sanity(8)
        print(PAR)

        print(PAR)
        return
    def shellbert_worry_stone_synergy(self):
        """Shellbert (Turtle) + Worry Stone synergy event"""
        if not self.has_companion("Shellbert") or not self.has_item("Worry Stone"):
            self.day_event()
            return
        type.type("You're turning the " + cyan(bright("Worry Stone")) + " over in your hand when " + cyan(bright("Shellbert")) + " climbs onto your lap.")
        print(PAR)
        type.type("He presses against it. Still. Patient. The patience of something that has outlived entire civilizations.")
        print(PAR)
        type.type("Both of you just... sit. The stone warm between you.")
        print(PAR)
        type.type("The worry doesn't disappear. It just gets smaller.")
        self._companions["Shellbert"]["happiness"] = min(100, self._companions["Shellbert"]["happiness"] + 10)
        self.restore_sanity(12)
        print(PAR)

        print(PAR)
        return
    def bear_scrap_armor_synergy(self):
        """Ursus/Bruno (Bear) + Scrap Armor synergy event"""
        bear_name = None
        if self.has_companion("Ursus"):
            bear_name = "Ursus"
        elif self.has_companion("Bruno"):
            bear_name = "Bruno"
        if not bear_name or not self.has_item("Scrap Armor"):
            self.day_event()
            return
        type.type("You leave the " + cyan(bright("Scrap Armor")) + " out by the car.")
        print(PAR)
        type.type(cyan(bright(bear_name)) + " investigates it. Sniffs it. Then drapes it across his shoulders like a cape.")
        print(PAR)
        type.type("He walks around the parking lot wearing it. The other animals notice.")
        print(PAR)
        type.type("A crow lands on a dumpster and stares. A stray dog crosses the street to avoid him.")
        print(PAR)
        type.type("Nobody is starting anything tonight.")
        self._companions[bear_name]["happiness"] = min(100, self._companions[bear_name]["happiness"] + 15)
        self._skip_animal_threat = True
        print(PAR)

        print(PAR)
        return
    def buddy_passive_find(self):
        """Buddy (Dog) finds a random useful item while out exploring."""
        if not self.has_companion("Buddy") or self.get_companion("Buddy")["status"] != "alive":
            self.day_event()
            return
        companion = self.get_companion("Buddy")
        type.type(bright("Buddy") + " comes bounding back from behind a dumpster, tail going like a propeller.")
        print(PAR)
        type.type("He drops something at your feet and sits. Expectant. Proud.")
        print(PAR)
        if companion.get("bonded"):
            roll = random.randrange(4)
            if roll == 0:
                amount = random.randint(10, 40)
                type.type("It's a crumpled wad of bills. " + green(bright("${:,}".format(amount))) + ". Slightly damp. You don't ask why.")
                self.change_balance(amount)
            elif roll == 1:
                type.type("A perfectly good " + cyan(bright("Bandage")) + ". Still in the wrapper. Buddy has standards.")
                if not self.has_item("Bandage"):
                    self.add_item("Bandage")
                else:
                    type.type(" You already have one, so you pocket the cash equivalent.")
                    self.change_balance(8)
            elif roll == 2:
                type.type("A " + cyan(bright("Granola Bar")) + " that's only slightly chewed on one corner. He's sharing.")
                if not self.has_item("Granola Bar"):
                    self.add_item("Granola Bar")
                else:
                    self.heal(3)
                    type.type(" You eat it together. Bonding over trash food.")
            else:
                type.type("An old tennis ball. No monetary value. But Buddy's eyes are shining.")
                print(PAR)
                type.type("You throw it. He brings it back. You throw it again. Twenty minutes vanish.")
                self.restore_sanity(5)
        else:
            roll = random.randrange(3)
            if roll == 0:
                amount = random.randint(5, 20)
                type.type("A few coins and a crumpled bill. " + green(bright("${:,}".format(amount))) + ". The thought counts.")
                self.change_balance(amount)
            elif roll == 1:
                type.type("A stick. A really good stick. He's very proud of it. You accept the gift with appropriate gravitas.")
                self.restore_sanity(4)
            else:
                type.type("Someone's lost shoe. One shoe. Left foot. Men's size 11.")
                print(PAR)
                type.type("You pat his head anyway. Good dog.")
                self.restore_sanity(3)
        self.pet_companion("Buddy")
        print(PAR)

        print(PAR)
        return
    def slick_passive_find(self):
        """Slick (Rat) finds something useful in the walls and shadows."""
        if not self.has_companion("Slick") or self.get_companion("Slick")["status"] != "alive":
            self.day_event()
            return
        companion = self.get_companion("Slick")
        type.type(bright("Slick") + " emerges from a crack in the wall you didn't even see. Something glints between their teeth.")
        print(PAR)
        if companion.get("bonded"):
            roll = random.randrange(4)
            if roll == 0:
                amount = random.randint(15, 55)
                type.type("Coins. A rolled-up bill. A casino chip someone dropped between the floorboards. " + green(bright("${:,}".format(amount))) + " total.")
                print(PAR)
                type.type("Slick chittered the whole way back. This was a big score by rat standards.")
                self.change_balance(amount)
            elif roll == 1:
                type.type("A " + cyan(bright("Lucky Penny")) + " they found wedged in a crack. The penny is warm.")
                if not self.has_item("Lucky Penny"):
                    self.add_item("Lucky Penny")
                else:
                    type.type(" You already have one. Slick looks deflated. You flip it for good luck anyway.")
                    self.restore_sanity(2)
            elif roll == 2:
                type.type("A " + cyan(bright("Pocket Knife")) + " that fell behind a vending machine. Blade still sharp.")
                if not self.has_item("Pocket Knife"):
                    self.add_item("Pocket Knife")
                else:
                    type.type(" You already have one. You sell the duplicate for a few bucks.")
                    self.change_balance(10)
            else:
                type.type("A scrap of paper with numbers on it. Lottery numbers? A safe combination? A phone number?")
                print(PAR)
                type.type("You'll never know. But Slick looks like they cracked the Da Vinci Code.")
                self.restore_sanity(3)
        else:
            roll = random.randrange(3)
            if roll == 0:
                amount = random.randint(3, 15)
                type.type("A few coins. " + green(bright("${:,}".format(amount))) + ". Slick drops them and vanishes back into the wall.")
                self.change_balance(amount)
            elif roll == 1:
                type.type("A bottle cap. Slick holds it out like a crown jewel.")
                print(PAR)
                type.type("You accept it. Rat kingdom economics are different.")
                self.restore_sanity(3)
            else:
                type.type("A piece of cheese. From somewhere. You don't eat it. Slick does.")
                print(PAR)
                type.type("Fair trade. They did the work.")
                self.restore_sanity(2)
        self.pet_companion("Slick")
        print(PAR)

        print(PAR)
        return
    def hopper_passive_find(self):
        """Hopper (Rabbit) finds strange lucky trinkets in the tall grass."""
        if not self.has_companion("Hopper") or self.get_companion("Hopper")["status"] != "alive":
            self.day_event()
            return
        companion = self.get_companion("Hopper")
        type.type(bright("Hopper") + " emerges from a patch of tall grass, nose twitching. Something is clamped in their little mouth.")
        print(PAR)
        if companion.get("bonded"):
            roll = random.randrange(4)
            if roll == 0:
                type.type("A four-leaf clover. Actual four-leaf clover. Hopper found it in seconds.")
                print(PAR)
                type.type("You press it between your fingers. It feels warm. Lucky.")
                self.restore_sanity(7)
                self.add_status("Lucky")
            elif roll == 1:
                amount = random.randint(8, 25)
                type.type("A crumpled bill that blew into the grass. " + green(bright("${:,}".format(amount))) + ". Wind-delivered income.")
                self.change_balance(amount)
            elif roll == 2:
                type.type("A small, smooth " + cyan(bright("Worry Stone")) + " from the riverbed. Hopper nuzzles it toward you.")
                if not self.has_item("Worry Stone"):
                    self.add_item("Worry Stone")
                else:
                    type.type(" You already have one. But the gesture is everything.")
                    self.restore_sanity(3)
            else:
                type.type("A dandelion. Whole, intact, ready to blow.")
                print(PAR)
                type.type("You hold it up. Hopper watches. You blow. Seeds scatter on the wind.")
                print(PAR)
                type.type("You made a wish. Hopper binkied. Something about this moment feels... right.")
                self.restore_sanity(5)
        else:
            roll = random.randrange(3)
            if roll == 0:
                type.type("A small acorn. Hopper drops it at your feet and hops backward, watching.")
                print(PAR)
                type.type("It's just an acorn. But Hopper chose you to give it to. That means something.")
                self.restore_sanity(4)
            elif roll == 1:
                type.type("A tuft of soft grass. Hopper arranged it in a tiny pile. A gift? A nest? Art?")
                print(PAR)
                type.type("You'll never know. But you keep the grass.")
                self.restore_sanity(3)
            else:
                type.type("A shiny pebble. Hopper nudges it with their nose, then binkies away.")
                print(PAR)
                type.type("Moon-smooth and warm from the ground. You pocket it.")
                self.restore_sanity(3)
        self.pet_companion("Hopper")
        print(PAR)

        print(PAR)
        return
