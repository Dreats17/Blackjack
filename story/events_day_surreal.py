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

class DaySurrealMixin:
    """Surreal events: meta, absurd, and fourth-wall-breaking moments"""

    def sock_puppet_therapist(self):
        # EVENT: Man with sock puppet "Dr. Socksworth" offers therapy (low sanity only)
        # CONDITION: Sanity < 60
        # EFFECTS: Accept = pour heart out, +15 sanity; Refuse = -2 sanity from judgment
        if self.get_sanity() >= 60:
            self.day_event()
            return
        type.type("You step out of your car and a man sits down next to you on the curb. He has a sock puppet on his hand — tiny wire-rimmed glasses, a little felt collar, the works. It turns toward you with an expression of profound, almost clinical concern.")
        print(PAR)
        type.type(quote("You look troubled. Want to talk about it?") + " You're already backing away when the man adds, quietly: " + quote("Dr. Socksworth is a licensed therapist. Technically."))
        print(PAR)
        answer = ask.yes_or_no("Talk to... Dr. Socksworth? ")
        if answer == "yes":
            type.type("You pour your heart out to a sock puppet. Not because you think it'll help — because there's nobody else, and the alternative is sitting alone in a car doing math about your failures again. Dr. Socksworth listens with genuine, unnerving attentiveness.")
            print(PAR)
            type.type(quote("Mm-hmm. Yes. I see. And how does that make you feel?"))
            print(PAR)
            type.type("Somehow, against everything you believe about psychology and textiles, you feel BETTER. He produces a tiny pamphlet from somewhere — 'COPING MECHANISMS FOR GAMBLERS: A SOCK'S GUIDE' — and you take it without shame. It's strangely, embarrassingly helpful.")
            self.restore_sanity(15)
        else:
            type.type("You walk away. Dr. Socksworth calls after you from across the parking lot:")
            print(PAR)
            type.type(quote("RUNNING FROM YOUR PROBLEMS WON'T SOLVE ANYTHING!"))
            print(PAR)
            type.type("You have been judged by a sock. You will think about this for days.")
            self.lose_sanity(2)
        print(PAR)

    # WEIRD EVENTS

    def time_loop(self):
        # EVENT: Experience the same morning 3 times, must break the loop
        # EFFECTS: Save bird = +$50, meet "Time Bird"; Ignore phone = +5 sanity; Scream = -5 sanity

        # COMBO: Oracle's Tome + Deck of Cards = Fortune Reading
        if (self.has_item("Oracle's Tome") or self.has_item("Gambler's Grimoire")) and self.has_item("Deck of Cards"):
            tome = "Oracle's Tome" if self.has_item("Oracle's Tome") else "Gambler's Grimoire"
            type.type("You open the " + cyan(bright(tome)) + " and lay three cards from your " + cyan(bright("Deck of Cards")) + " on top of it.")
            print(PAR)
            type.type("Fortune Reading. The pages drink the card faces and replace them with prophecy:")
            print(PAR)
            type.type("Card one: " + italic("'A friend in trouble. Help them.'"))
            print(PAR)
            type.type("Card two: " + italic("'Money on the ground. Take it.'"))
            print(PAR)
            type.type("Card three: " + italic("'The Dealer watches. He always watches.'"))
            print(PAR)
            type.type("The cards go blank. The book snaps shut. You don't know if the future changed or if it was always going to happen this way.")
            self.restore_sanity(12)
            self.change_balance(random.randint(50, 200))
            print(PAR)
            return

        if self.has_item("Pocket Watch") or self.has_item("Grandfather Clock"):
            watch = "Pocket Watch" if self.has_item("Pocket Watch") else "Grandfather Clock"
            type.type("The clock on your car dashboard says 8:47 AM. You go to brush your teeth. A bird hits the window. Your phone buzzes. You wake up. The clock says 8:47 AM.")
            print(PAR)
            type.type("You pull out the " + cyan(bright(watch)) + ". Its hands are spinning backwards. You remember this — all of it. Every loop, every iteration. You've been here before.")
            print(PAR)
            if watch == "Grandfather Clock":
                type.type("The " + cyan(bright("Grandfather Clock")) + " booms once — a deep house-sized chime from a device that should not fit in your pocket. The whole loop winces.")
                print(PAR)
                type.type("You do not merely remember this morning. You overrule it. At 8:46, you open the window, silence the phone, and step aside before the universe can make its move.")
                print(PAR)
                type.type("The bird glides through. The loop collapses like rotten scaffolding. Time, embarrassed, pretends it meant to do that.")
                self.change_balance(100)
                self.restore_sanity(12)
            else:
                type.type("You step outside at 8:46 and open the window. The bird flies safely through. The loop shatters. First try. The watch ticks forward. You pocket it without ceremony. Some problems only need the right tool.")
                self.change_balance(50)
                self.restore_sanity(8)
            self.update_pocket_watch_durability()
            self.meet("Time Bird")
            print(PAR)
            return
        if self.has_item("Oracle's Tome"):
            type.type("The " + cyan(bright("Oracle's Tome")) + " has been writing this paragraph for six days. You're finally catching up to it.")
            print(PAR)
            type.type("The handwriting — yours, somehow — fills the margins: " + italic("'8:47. Bird. Phone. Third time. You'll know what to do.'"))
            print(PAR)
            type.type("You step outside at 8:46 and open the window. The bird glides safely through. The loop shatters without drama. The Tome closes with a satisfied thud.")
            self.restore_sanity(5)
            self.change_balance(50)
            self.meet("Time Bird")
            print(PAR)
            return
        if self.has_item("Fortune Cards"):
            type.type("You lay the " + cyan(bright("Fortune Cards")) + " on the dashboard. They spread themselves.")
            print(PAR)
            type.type("THE LOOP card faces up. It says: " + italic("'...you've done this before.'"))
            print(PAR)
            type.type("Not in metaphor. Not as a warning. As a statement of fact delivered by a card that has been here every loop, watching.")
            print(PAR)
            type.type("You pocket the cards. The loop breaks. But the cards remember, and now you know they do.")
            self.lose_sanity(3)
            self.meet("Time Bird")
            self.add_status("Remembered the Loop")
            print(PAR)
            return
        type.type("The clock on your car dashboard says 8:47 AM. You go to brush your teeth. A bird hits the window. Your phone buzzes.")
        print(PAR)
        type.type("You wake up. The clock says 8:47 AM.")
        print(PAR)
        type.type("Wait. What?")
        print(PAR)
        type.type("You go to brush your teeth. You KNOW a bird is about to hit the window. It does. Your phone buzzes. You wake up. The clock says 8:47 AM. This is the third time. You're absolutely certain now.")
        print(PAR)
        if self.has_item("Dream Catcher"):
            type.type("The " + cyan(bright("Dream Catcher")) + " on your mirror is spinning furiously, catching fragments of the loop.")
            print(PAR)
            type.type("It whispers to you: the bird needs saving, the phone needs ignoring, the scream needs... not happening.")
            print(PAR)
            type.type("You choose wisely. The loop unravels like a bad dream.")
            self.restore_sanity(8)
            self.change_balance(25)
            print(PAR)
            return
        answer = ask.option("What do you do differently? ", ["save the bird", "ignore your phone", "scream"])
        if answer == "save the bird":
            type.type("You stand at the window before dawn, waiting. The bird approaches. You OPEN the window. It flies through, circles your head once like it's thanking you, and drops something shiny before disappearing into the morning.")
            print(PAR)
            type.type("A golden coin. Worth " + green(bright("$50")) + ". The loop breaks like a fever.")
            self.change_balance(50)
            self.meet("Time Bird")
        elif answer == "ignore your phone":
            type.type("You don't check your phone. The buzzing stops. The loop... freezes — time itself holding its breath, waiting to see if you'll flinch.")
            print(PAR)
            type.type("Then everything resumes. You're free, and you remember all three loops with perfect clarity. The memory feels like something you earned.")
            self.restore_sanity(5)
        else:
            type.type("You SCREAM at 8:47 AM. Raw, wordless, absolutely unhinged. The neighbors definitely hear it. But it works — the loop shatters, reality stumbles forward like a drunk finding a wall.")
            print(PAR)
            type.type("You've lost three hours somewhere. Or gained them. Time is a different thing now and you've decided to be okay with that.")
            self.lose_sanity(5)
        print(PAR)

    def mirror_stranger(self):
        # EVENT: Your reflection acts independently and holds up a sign saying "SOON"
        # EFFECTS: 30% find encouraging note from reflection (+5 sanity); 70% avoid mirrors all day (-8 sanity)
        if self.has_item("Seer's Chronicle"):
            type.type("The " + cyan(bright("Seer's Chronicle")) + "'s pages turn to this moment. The stranger in the mirror — you've already read this part.")
            print()
            type.type("You wave. They wave. You know exactly what they are: a future self. A warning.")
            type.type(" You heed it.")
            self.restore_sanity(10)
            self.heal(10)
            return
        if self.has_item("Third Eye"):
            type.type("The " + cyan(bright("Third Eye")) + " opens. You see what's really happening.")
            print()
            type.type("The stranger isn't a stranger. It's a probability wave — one version of you that took a different turn.")
            type.type(" You acknowledge it, and it disperses.")
            self.restore_sanity(8)
            return
        type.type("You catch your reflection in the car mirror. It smiles. You are not smiling. The reflection waves. You don't move your hand.")
        print(PAR)
        type.type("It holds up a sign. Written in what might be blood: 'SOON.'")
        print(PAR)
        type.type("You blink. The reflection is normal again — just you, looking the way a person looks when they've seen something they cannot explain.")
        print(PAR)
        if self.has_item("Flask of Split Serum"):
            print()
            type.type("The " + cyan(bright("Flask of Split Serum")) + " fizzes in your pocket. For a moment you see TWO of everything — two roads, two choices, two versions of yourself.")
            print()
            type.type("Both of them are you. Neither of them is sure which is real.")
            self.restore_sanity(1)
            print(PAR)
        if self.has_item("Twin's Locket") or self.has_item("Mirror of Duality"):
            locket = "Mirror of Duality" if self.has_item("Mirror of Duality") else "Twin's Locket"
            type.type("You reach for the " + cyan(bright(locket)) + " around your neck. It falls open on its own. Inside: two tiny portraits facing each other, and in both portraits, the reflection is also looking back at you.")
            print(PAR)
            if locket == "Mirror of Duality":
                type.type("Your reflection does not just recognize it. It smiles with relief. Then it swaps places with the fear in your chest so fast you feel the motion happen.")
                print(PAR)
                type.type("For one impossible second, you are the one behind the glass and the calmer version of you is out here, steadying your hands, fixing your posture, handing your terror back in smaller pieces.")
                print(PAR)
                type.type("When reality settles, the sign is gone. So is the worst of the dread. The mirror keeps your panic. You keep moving.")
                self.restore_sanity(12)
            else:
                type.type("Your reflection in the mirror tilts its head, studying the locket with something that looks almost like recognition. It points. It seems satisfied. It puts the sign down.")
                print(PAR)
                type.type("The sign is gone. Whatever it needed from you, it found it in the locket instead.")
                self.restore_sanity(8)
            self.update_twins_locket_durability()
            print(PAR)
            return
        if self.has_item("Marvin's Monocle"):
            type.type("You raise the " + cyan(bright("Marvin's Monocle")) + " to your eye. Through its smoky lens, the mirror shows something different — not a sign, not a threat.")
            print(PAR)
            type.type("Your reflection is sitting down. Having coffee. Completely at peace with existence in a way you are not.")
            print(PAR)
            type.type("It raises its mug in a small toast. You lower the monocle. The SOON sign is gone. The monocle sees things the mirror doesn't, and apparently that was enough.")
            self.restore_sanity(6)
            print(PAR)
            return
        if self.has_item("Gambler's Grimoire"):
            type.type("The " + cyan(bright("Gambler's Grimoire")) + " flips open in your bag. You pick it up. It's running a calculation you didn't ask for.")
            print(PAR)
            type.type(italic("PROBABILITY OF REFLECTION BEING YOU: 73%"))
            print(PAR)
            type.type("You stare at your reflection. It stares back. 73%. That leaves 27% unaccounted for. The Grimoire does not explain what the other 27% is.")
            print(PAR)
            type.type("The number haunts you for the rest of the day. You keep doing the math. It keeps coming out wrong.")
            self.lose_sanity(1)
            self.add_status("Probability Haunted")
            print(PAR)
        if random.random() < 0.3:
            type.type("In the back seat, you notice something that wasn't there before — a note, in your own handwriting: 'You're doing fine. Keep going.'")
            print(PAR)
            type.type("Did the reflection leave it? You fold it carefully and put it in your pocket. You don't throw it away.")
            self.restore_sanity(5)
        else:
            type.type("You avoid mirrors for the rest of the day. Some information is worse than not knowing.")
            self.lose_sanity(8)
        print(PAR)

    def the_glitch(self):
        # EVENT: Reality glitches around you (low sanity only)
        # CONDITION: Sanity < 50
        # EFFECTS: Random - money change (-$100 to +$200), health (-15 to +25), time skip, or identity confusion (-10 sanity)
        if self.get_sanity() >= 50:
            self.day_event()
            return
        if self.has_item("Smelling Salts"):
            type.type("Reality stutters. Colors shift. Your vision swims.")
            print()
            type.type("You crack the " + cyan(bright("Smelling Salts")) + " under your nose. One whiff and reality snaps back into focus.")
            print()
            type.type("The glitch dissolves. Your brain reboots. Whatever that was, it's over.")
            self.restore_sanity(3)
            print()
            return
        type.type("Sitting in your car, reality... stutters.")
        print()
        type.type("The colors around you shift. Blue becomes green. Green becomes screaming.")
        print()
        type.type("Wait, that's not right.")
        print()
        type.type("You look at your hands. You have seven fingers. No, six. No, the normal amount. Maybe.")
        print()
        glitch = random.choice(["money", "health", "time", "identity"])
        if glitch == "money":
            change = random.randint(-100, 200)
            if change >= 0:
                type.type("Your wallet glitches. Suddenly, there's more money in it. " + green(bright("+$" + str(change))))
                self.change_balance(change)
            else:
                type.type("Your wallet glitches. Some of your money is gone. " + red(str(change)))
                self.change_balance(change)
        elif glitch == "health":
            change = random.randint(-15, 25)
            if change >= 0:
                type.type("Your body glitches. You feel BETTER than before. " + green(bright("+" + str(change) + " HP")))
                self.heal(change)
            else:
                type.type("Your body glitches. Something hurts now. " + red(str(change) + " HP"))
                self.hurt(abs(change))
        elif glitch == "time":
            type.type("You blink and it's suddenly six hours later. What happened?")
            type.type(" You don't know. You'll never know.")
        else:
            type.type("For a moment, you forget who you are. Then it comes back, but... different.")
            type.type(" Were you always left-handed? You don't remember.")
            self.lose_sanity(10)
        print()
        type.type("Reality snaps back. Everything is normal. Everything is fine.")
        print()
        type.type("Is it?")
        print()

    def wrong_universe(self):
        # EVENT: Slip into alternate dimension with purple sky and floating cars
        # EFFECTS: Meet alternate rich self, get Dimensional Coin item (50%) or $100-300 (50%), -10 sanity
        if self.has_item("Third Eye"):
            type.type("The " + cyan(bright("Third Eye")) + " sees through the illusion. The wrong universe is just a probability fold — a glitch in local reality.")
            print()
            type.type("You step back into the right one with the grace of someone who does this regularly.")
            self.restore_sanity(8)
            return
        if self.has_item("Fate Reader"):
            type.type("The " + cyan(bright("Fate Reader")) + " showed this in the cards. You recognized the fold the moment it started.")
            print()
            type.type("The universe corrects itself. You barely notice.")
            self.restore_sanity(5)
            return
        type.type("You step out of your car and around a corner. The world changes.")
        print()
        type.type("The sky is purple. The buildings are organic, pulsing like living things.")
        type.type(" Cars float. People have too many eyes. A dog speaks fluent French.")
        print()
        type.type("This is not your world.")
        print()
        type.type("A version of yourself approaches. They're taller, more confident. Richer, clearly.")
        print()
        type.type(quote("Ah, another me. Let me guess - you're from a world where you're still struggling?"))
        print()
        type.type("You nod, dumbstruck.")
        print()
        type.type(quote("Pathetic. Well, take this. It won't help much, but it's something."))
        print()
        if random.random() < 0.5:
            type.type("They hand you a strange coin. It hums with otherworldly energy.")
            self.add_item("Dimensional Coin")
            type.type(" You got a " + magenta(bright("Dimensional Coin")) + "!")
        else:
            amount = random.randint(100, 300)
            type.type("They hand you a wad of bills. The denominations don't exist in your world, but...")
            type.type(" Somehow they translate to " + green(bright("$" + str(amount))) + "!")
            self.change_balance(amount)
        print()
        type.type("The world flickers. Shifts. You're back in the normal universe.")
        print()
        type.type("Was any of that real?")
        self.lose_sanity(10)
        print()

    def fourth_wall_break(self):
        # EVENT: A stranger becomes aware they're in a game, breaks the fourth wall
        # EFFECTS: -15 sanity from existential dread
        type.type("A stranger approaches your car. They look... worried.")
        print()
        type.type(quote("Hey. You. Can you keep a secret?"))
        print()
        type.type("Before you can answer, they lean in close.")
        print()
        type.type(quote("I think... I think none of this is real. I think we're in some kind of... game. Or story."))
        print()
        type.type("You laugh nervously. " + quote("That's crazy talk."))
        print()
        type.type(quote("Is it? Think about it. The same things happen over and over. There's a PATTERN. And you..."))
        print()
        type.type(quote("You're the main character, aren't you? Everyone else is just... background."))
        print()
        type.type("The stranger starts crying.")
        print()
        type.type(quote("Am I even real? Do I exist when you're not looking at me?"))
        print()
        type.type("They walk away, still crying. You stand there, deeply unsettled.")
        print()
        type.type("...")
        print()
        type.type("You glance at the 'player.' The one reading this. Just for a second.")
        print()
        self.lose_sanity(15)
        self.unlock_achievement("fourth_wall")
        print()

    # DARK EVENTS

    def the_collector(self):
        # EVENT: Man in black suit collects debts, favors, and "souls"
        # EFFECTS: Meet "The Collector", various sanity loss based on choice
        type.type("You look up from your car. A man in a black suit steps out of the shadows. His smile doesn't reach his eyes.")
        print()
        type.type(quote("You've been making moves. Big moves. People notice."))
        print()
        type.type("He produces a small notebook and flips through it.")
        print()
        type.type(quote("According to my records, you owe... well, you don't owe ME anything. Yet."))
        print()
        type.type(quote("But I'm here to offer a service. I collect things. Debts. Favors. Souls, sometimes."))
        print()
        type.type("He chuckles. It's not a friendly sound.")
        print()
        answer = ask.option("What do you say? ", ["not interested", "what are you offering", "souls?"])
        if answer == "not interested":
            type.type("He shrugs. " + quote("Everyone says that at first. I'll be around."))
            print()
            type.type("He vanishes into the shadows. You didn't see him go. He was just... gone.")
            self.meet("The Collector")
        elif answer == "what are you offering":
            type.type(quote("Information. Protection. Future knowledge. Whatever you need, I can provide."))
            print()
            type.type(quote("My price is... flexible. Sometimes money. Sometimes favors. Sometimes..."))
            print()
            type.type("He leans in close. " + quote("...years."))
            print()
            type.type("You step back. He laughs.")
            print()
            type.type(quote("Not ready yet. That's fine. When you are, I'll know."))
            self.meet("The Collector")
            self.lose_sanity(10)
        else:
            type.type(quote("Souls? Oh, that's mostly a metaphor. Mostly."))
            print()
            type.type("His smile widens just a bit too far.")
            print()
            type.type(quote("Don't worry about souls. You've still got yours. For now."))
            self.meet("The Collector")
            self.lose_sanity(15)
        print()

    def the_empty_room(self):
        # EVENT: Find a door that shouldn't exist, leads to infinite white void with creature
        # CONDITION: Sanity < 40
        # EFFECTS: -20 sanity, gain "Glimpsed the Void" status
        if self.get_sanity() >= 40:
            self.day_event()
            return
        type.type("You step out of your car and notice a door you've never seen before. It's in a wall that shouldn't have a door.")
        print()
        type.type("Something tells you not to open it. Something screams at you to run.")
        print()
        type.type("You open it anyway. Of course you do.")
        print()
        type.type("Inside is... empty. Completely, perfectly empty. No floor, no walls, no ceiling.")
        type.type(" Just white. Endless white in every direction.")
        print()
        type.type("You step inside. Your footsteps make no sound. You are nowhere.")
        print()
        type.type("And then you see it.")
        print()
        type.type("In the distance. Getting closer. Something that has too many limbs and not enough face.")
        print()
        type.type("You run. Back through the door. SLAM it shut.")
        print()
        type.type("When you turn around, the door is gone. The wall is smooth. Like the door never existed.")
        print()
        type.type("But you can still hear scratching from inside the wall.")
        if self.has_item("Delight Indicator") or self.has_item("Delight Manipulator"):
            gauge = "Delight Manipulator" if self.has_item("Delight Manipulator") else "Delight Indicator"
            print()
            type.type("Your " + cyan(bright(gauge)) + " displays a reading you've never seen before: " + yellow("'UNDEFINED.'"))
            print()
            type.type("Some feelings don't have names. The device wasn't built for this.")
        self.lose_sanity(20)
        self.add_status("Glimpsed the Void")
        print()

    def blood_moon_bargain(self):
        # EVENT: On a blood red moon, dark forces offer one night of perfect luck for one year of life
        # EFFECTS: Accept = "Blood Moon Luck" + "Year Shorter" status, -20 sanity; Reject = +5 sanity
        if self.has_item("Soul Forge"):
            type.type("The " + cyan(bright("Soul Forge")) + " glows in the blood-moon light. The entity recognizes it.")
            print()
            type.type(quote("You've brought the rewriting tool,") + " it whispers. " + quote("The pact is unnecessary. Name what you want changed."))
            print()
            if not self.has_met("Soul Forge Used"):
                self.mark_met("Soul Forge Used")
                type.type("You name it. Whatever it was. The past rewrites. The blood moon fades.")
                self.heal(50)
                self.restore_sanity(25)
                self.change_balance(5000)
            else:
                type.type("You've already used the Forge. The entity nods. " + quote("The price was paid."))
                self.restore_sanity(10)
            return
        if self.has_item("Dark Pact Reliquary"):
            type.type("The " + cyan(bright("Dark Pact Reliquary")) + " glows. The entity recognizes the toolkit.")
            print()
            type.type(quote("You've done your homework,") + " it says. The terms shift heavily in your favor.")
            print()
            type.type("You walk away with more than you asked for. Somehow, you feel like you still lost something small.")
            self.heal(20)
            self.restore_sanity(10)
            self.change_balance(1000)
            return
        if self.has_item("Mind Shield"):
            type.type("The " + magenta(bright("Mind Shield")) + " holds your sanity together. Reality warps but you don't.")
            print()
            type.type("The blood moon's whispers crash against your mental walls and shatter.")
            self.restore_sanity(10)
            return
        type.type("Through your windshield, the sky is wrong. The light filtering in is red. Blood red. The color of things that shouldn't be.")
        print()
        type.type("You hear a voice inside your car. It comes from nowhere and everywhere.")
        print()
        type.type(cyan(quote("GAMBLER. WE HAVE WATCHED YOU.")))
        print()
        type.type("You look around. There's no one there. Just shadows that move wrong.")
        print()
        type.type(cyan(quote("WE OFFER A BARGAIN. ONE NIGHT OF PERFECT LUCK. EVERY HAND A WINNER.")))
        print()
        type.type(cyan(quote("IN EXCHANGE... ONE YEAR OF YOUR LIFE. BURNED FROM THE END. GONE FOREVER.")))
        print()
        if self.has_item("Oracle's Tome") or self.has_item("Gambler's Grimoire"):
            tome = "Oracle's Tome" if self.has_item("Oracle's Tome") else "Gambler's Grimoire"
            type.type("Your " + cyan(bright(tome)) + " thrashes in your bag, pages turning in a violent frenzy.")
            print()
            type.type("Every page reads the same thing: " + italic("DO NOT ACCEPT. DO NOT ACCEPT. DO NOT ACCEPT."))
            print()
            type.type("You close it. It falls open again. Your hands won't stop shaking.")
            self.restore_sanity(5)
            print()
        if self.has_item("Dealer's Grudge") or self.has_item("Dealer's Mercy"):
            item_name = "Dealer's Grudge" if self.has_item("Dealer's Grudge") else "Dealer's Mercy"
            type.type("The " + cyan(bright(item_name)) + " burns white-hot against your leg.")
            print()
            type.type("From somewhere behind the red light, another voice cuts through — familiar, cold, and possessive.")
            print()
            type.type(quote("Not this one. They're mine."))
            print()
            type.type("The shadows recoil. The entity that made the offer goes very quiet.")
            print()
            type.type(cyan(quote("...ANOTHER TIME, THEN.")))
            print()
            type.type("The red moon fades before you can accept or refuse. The Dealer's claim supersedes even blood moon bargains.")
            self.restore_sanity(15)
            print()
            return
        if self.has_item("Necronomicon"):
            type.type("The " + cyan(bright("Necronomicon")) + " opens itself. The blood moon's light reflects off the pages.")
            print()
            type.type("Whatever entity is making the offer sees the book and recalibrates. The shadows go very quiet for a moment.")
            print()
            type.type(cyan(quote("...YOU CARRY THAT BOOK. THE DEAL... CHANGES.")))
            print()
            type.type("The contract burns itself into the air — revised. Better terms. Much better terms.")
            print()
            type.type("One night of perfect luck. No years burned. Just a debt you'll feel in your bones someday.")
            print()
            type.type("You take it. The book snaps shut, satisfied.")
            self.add_status("Blood Moon Luck")
            self.restore_sanity(25)
            self.change_balance(500)
            print()
            return
        if self.has_item("Eldritch Candle") and self.has_item("Fortune Cards"):
            type.type("The " + cyan(bright("Eldritch Candle")) + " lights on its own. You didn't touch it. The flame is green.")
            print()
            type.type("Your " + cyan(bright("Fortune Cards")) + " spread themselves across the car seat. The red light catches them at an angle that reveals cards that aren't in any normal deck.")
            print()
            type.type(italic("THE PLAYER. THE ENGINE. THE SAVE FILE."))
            print()
            type.type("One card shows tomorrow. Not in metaphor. Literally — there you are, standing somewhere you haven't been yet, doing something you haven't decided to do yet. The image is clear and terrible.")
            print()
            type.type("The blood moon dims, unsettled. Even the entity that made the bargain has gone quiet. This is above its pay grade.")
            print()
            type.type("The green flame goes out. The cards are face-down. You already know what tomorrow looks like. You wish you didn't.")
            self.lose_sanity(5)
            self.add_status("Saw Tomorrow")
            print()
            return
        if self.has_item("Flask of Dealer's Whispers"):
            type.type("The " + cyan(bright("Flask of Dealer's Whispers")) + " grows cold in your pocket. A whisper, barely audible over the entity's offer: " + italic("Do not accept. The house always wins.") + " Or is it " + italic("Accept. The shadows play fair.") + "?")
            print()
            type.type("The flask's advice is contradictory. The Dealer speaks in riddles, even here.")
            self.restore_sanity(2)
            print()
        answer = ask.yes_or_no("Accept the blood moon bargain? ")
        if answer == "yes":
            type.type("You speak into the darkness. " + quote("I accept."))
            print()
            type.type("The shadows LAUGH. A contract burns itself into your arm. It's painless, somehow worse than pain.")
            print()
            type.type(cyan(quote("DONE. TONIGHT, YOU CANNOT LOSE. BUT TOMORROW, YOU WILL FEEL IT. THE MISSING TIME.")))
            print()
            type.type("The red moon seems to glow brighter. You feel different. Powerful. Cursed.")
            self.add_status("Blood Moon Luck")
            self.add_status("Year Shorter")
            self.lose_sanity(20)
        else:
            type.type("You shake your head. " + quote("No. I'll take my chances the normal way."))
            print()
            type.type("The shadows hiss in displeasure.")
            print()
            type.type(cyan(quote("FOOLISH. BUT BRAVE. WE WILL WATCH. WE ARE ALWAYS WATCHING.")))
            print()
            type.type("The red moon fades to normal. You've made an enemy tonight. Or escaped one.")
            self.restore_sanity(5)
            self.meet("Rejected the Shadows")
        print()

    # GOOFY EVENTS

    def alien_abduction(self):
        # EVENT: Briefly abducted by aliens at 2 AM, returned with missing time
        # EFFECTS: Random - money (+$50-200), health (+30 HP, +10 sanity), Alien Crystal item, or nothing (-10 sanity)
        type.type("A bright light floods your car. You float up. Through the roof. This shouldn't be possible.")
        print()
        type.type("Everything goes white.")
        print()
        type.type("...")
        print()
        type.type("You wake up three hours later in your car. You don't remember anything.")
        print()
        type.type("But there's a new mark on your arm: a tiny UFO tattoo that wasn't there before.")
        print()
        if self.has_item("Mobile Workshop") and random.randrange(5) == 0:
            type.type("You look around. Something is different. Outside your car, partially unfolded on the asphalt, is a structure you have no memory of building.")
            print()
            type.type("It looks like a satellite dish. Made entirely of spoons. Hundreds of spoons, welded and bent and somehow perfectly functional.")
            print()
            type.type("Your " + cyan(bright("Mobile Workshop")) + " is folded back beside it, its tools warm to the touch. Whatever happened, the workshop was involved.")
            print()
            type.type("You put your ear near the dish. It's receiving a signal. A weather forecast for a city whose name you don't recognize and can't quite pronounce.")
            print()
            type.type(italic("'...mostly cloudy over Vorthenne, with a 40% chance of lateral rain. Current temperature: seventeen degrees in the wrong direction.'"))
            print()
            self.add_item("Spoon Satellite")
            type.type("You got a " + cyan(bright("Spoon Satellite")) + "!")
            print()
            self.add_status("Builds Things")
            if random.randrange(2) == 0:
                type.type(green("Something about this feels right. In a deeply wrong way."))
                self.restore_sanity(1)
            else:
                type.type(red("You will never be able to explain this. Not to anyone."))
                self.lose_sanity(1)
            print()
            return
        effect = random.choice(["money", "health", "item", "nothing"])
        if effect == "money":
            amount = random.randint(50, 200)
            type.type("Your wallet is heavier. You have " + green(bright("$" + str(amount))) + " more than before.")
            type.type(" Alien money? Space bribe?")
            self.change_balance(amount)
        elif effect == "health":
            type.type("You feel... better? Healthier? Did they FIX something?")
            self.heal(30)
            self.restore_sanity(10)
        elif effect == "item":
            type.type("There's a glowing crystal in your pocket. You don't know what it does.")
            self.add_item("Alien Crystal")
            type.type(" You got an " + magenta(bright("Alien Crystal")) + "!")
        else:
            type.type("Nothing seems different. But you can't shake the feeling you've been... studied.")
            self.lose_sanity(10)
        print()

    def dance_battle(self):
        # EVENT: Street gang challenges you to a dance-off
        # EFFECTS: Win (score >= 2) = +$25-75, +5 sanity; Tie = pass with respect; Lose = -$15, -3 sanity
        type.type("You step out of your car and a group of teenagers blocks your path. Their leader steps forward.")
        print()
        type.type(quote("Yo! This is our turf. You wanna pass? You gotta DANCE."))
        print()
        type.type("A boombox appears. Music starts playing. The crowd forms a circle.")
        print()
        type.type("It's dance battle time. What's your move?")
        print()
        moves = ["worm", "robot", "spin move", "moonwalk", "interpretive dance"]
        move = ask.option("Your opening move: ", moves)
        score = 0
        if move == "worm":
            if random.random() < 0.6:
                type.type("You hit the floor and worm like your life depends on it! The crowd goes WILD!")
                score += 2
            else:
                type.type("You hit the floor and... just kind of wiggle sadly. Like a dying fish.")
                score -= 1
        elif move == "robot":
            type.type("You bust out crisp, mechanical movements. " + quote("BEEP BOOP!"))
            score += 1
        elif move == "spin move":
            if random.random() < 0.5:
                type.type("You spin so fast you become a BLUR! The crowd screams!")
                score += 3
            else:
                type.type("You spin... and fall over. Dizzy and embarrassed.")
                score -= 2
        elif move == "moonwalk":
            type.type("You glide backwards like you're on ice. Smooth. Real smooth.")
            score += 2
        else:
            type.type("You... interpret. Dance? The crowd is confused but intrigued.")
            score += random.choice([-1, 0, 1, 2, 3])
        print()
        if score >= 2:
            type.type("You WIN the dance battle! The gang cheers!")
            print()
            reward = random.randint(25, 75)
            type.type("They shower you with singles. You collect " + green(bright("$" + str(reward))) + "!")
            self.change_balance(reward)
            self.restore_sanity(5)
        elif score >= 0:
            type.type("It's a TIE! The gang respects your effort.")
            print()
            type.type(quote("You got moves, old timer. You can pass."))
        else:
            type.type("You LOSE. The gang boos you mercilessly.")
            print()
            type.type("They take your lunch money. Literally. " + red("(-$15)"))
            self.change_balance(-15)
            self.lose_sanity(3)
        print()

    # ==========================================
    # NEW SECRET EVENTS - HIDDEN TRIGGERS
    # ==========================================

