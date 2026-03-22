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

class MechanicsStorylineMixin:
    """Mechanic storyline events: first meetings with Tom, Frank, Oswald and their full dream-chain arcs"""

    def trusty_tom(self):
        self.meet("Tom Event")
        type.type("A blaring engine roars down the road towards you. ")
        type.type("As you scratch your eyes awake, you read \'Tom's Trusty Trucks and Tires\' painted on the hood of a bright gold truck. ")
        type.type("Waving the vehicle down, the truck slows, then halts, and an old, jolly man jumps out. ")
        print("\n")
        type.type("\"Well, howdy! The name's Tom. It appears you've gotten yourself in a bit of a pickle, ya think?\" ")
        type.type("Tom pulls a big red wrench out of his pocket, and walks to the hood of your beaten down wagon. ")
        repair_price = random.choice([150, 200, 250, 300, 350])
        type.type("\"Yep, this thing's busted alright! Tell ya what, for, I don't know, " + green(bright(str(repair_price) + " bucks")) + ", ")
        type.type("I'll get this thing replaced for ya, good as new! Whaddya say?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"Really? No dice, huh. Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                type.type("Tom has a sad look in his eye. It's clear that he wanted to help you. ")
                type.type("You watch as his big golden truck stutters, starts, then drives away.")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self._balance >= repair_price:
                    self.meet("Tom")
                    self.set_car_mechanic("Tom")
                    type.type("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                    type.type("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                    self.change_balance(-repair_price)
                    self.add_item("Car")
                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                    print("\n")
                    type.type("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                    print("\n")
                    return
                else:
                    type.type("\"Aww man, sorry to tell you, but you just don't got enough funds for this, yunno?\" ")
                    random_chance = random.randrange(2)
                    # Broke, and Tom offers discount
                    if random_chance == 0:
                        print("\n")
                        type.type("\"You know what? I'm feelin' generous, and the shop's been doing well lately. ")
                        type.type("Tell ya what, I can take the offer down " + green(bright(str(50) + " dollars")) + " just for you. ")
                        type.type("Could ya do " + green(bright(str(repair_price-50) + " bucks")) + "?\" ")
                        while True:
                            yes_or_no_2 = input("").lower()
                            print()
                            # Declining Tom's second offer
                            if(yes_or_no_2 == "n") or (yes_or_no_2=="no"):
                                print()
                                type.type("\"Really? No dice, huh. Even with the discount? Yunno, I think you're makin' a mistake, but I ain't one to judge. You have a nice day now.\" ")
                                type.type("Tom has a dissapointed look in his eye. It's clear that he wanted to help you. ")
                                type.type("You watch as his big golden truck stutters, starts, then drives away.")
                                print("\n")
                                return
                            elif((yes_or_no_2 == "y") or (yes_or_no_2 == "yes")):
                                if self._balance >= (repair_price-50):
                                    self.meet("Tom")
                                    self.set_car_mechanic("Tom")
                                    type.type("\"Really? Awesome! I'll be the best dang mechanic this ol' automobile has ever seen!\" ")
                                    type.type("You watch in awe, as Tom, a man who has clearly perfected his craft, fixes up your wagon in no time. Sweet. ")
                                    self.change_balance(-(repair_price-50))
                                    self.add_item("Car")
                                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                                    print("\n")
                                    type.type("\"Well, gee, this has been fun. Be seein' you around, ya know?\" ")
                                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                                    print("\n")
                                    return
                                else:
                                    type.type("\"Still can't afford it? That's a real shame. I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                                    type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                                    print("\n")
                                return
                            else:
                                type.type("\"Whaddya say?\" ")

                    # Broke, and Tom can't offer discount
                    elif random_chance == 1:
                        print("\n")
                        type.type("\"I really wish there was something I could do. Best of luck my friend. Be seeing ya around, ya know?\" ")
                        type.type("And with that, you watch as his big golden truck stutters, starts, then drives away.")
                        print("\n")
                        return
            else:
                type.type("\"Whaddya say?\" ")

    def filthy_frank(self):
        self.meet("Frank Event")
        type.type("A roaring engine blasts into your eardrums. ")
        type.type("As you jump up out of the front seat, you read \'Filthy Frank's Flawless Fixtures\' painted on the hood of a...well...a beater. ")
        type.type("Waving the vehicle down, the beater slows, then appears to break down, ")
        type.type("and an old man with tattoo sleeves and long black hair steps out. ")
        type.type("He kicks his car, and the engine starts blaring once more. ")
        print("\n")
        type.type("\"Hello, the name's Frank. Now I've got a baseball game to catch, but it looks like you could use some help.\" ")
        type.type("Frank pulls a shiny silver hammer out of his pocket, and walks to the hood of your beaten down wagon. ")
        repair_price = random.choice([50, 75, 100])
        type.type("\"My god. This is just awful. Tell you what, I can fix this up for like " + green(bright(str(repair_price) + " bucks")) + ", ")
        type.type("and your engine will be runnin' just as good as mine. You game?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"What?! How could you not accept my service? I'm the cheapest damn autoshop worker on this here planet! ")
                type.type("But NOOOO, NOT FRANK! Never Frank. He Voted For Trump! ")
                type.type("Let's all ridicule frank for his political party. You god damn liberals.\" ")
                type.type("Frank spits in your face, and get back in his truck. ")
                print("\n")
                type.type("You watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon. ")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self._balance >= repair_price:
                    type.type("\"Darn tootin! Lemme just do my thing.\" ")
                    type.type("You watch in terror as Frank takes the hammer, and begins to beat the living daylight out of your wagon's engine. ")
                    type.type("Each swing causes you to wince more and more. ")
                    self.change_balance(-repair_price)
                    random_chance = random.randrange(5)
                    if random_chance < 2:
                        self.meet("Frank")
                        self.set_car_mechanic("Frank")
                        self.add_item("Car")
                        type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                        print("\n")
                        type.type("\"Ah, I love fixin people's cars. You sure do drive a shitty vehicle, ")
                        type.type("but I'm just glad I can help get you back up and going to your job every day. ")
                        type.type("Gotta do something to help in this economy, you know?\" ")
                        print("\n")
                        type.type("And with that, you watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon.")
                        print("\n")
                        return
                    else: 
                        type.type("You notice Frank beginning to sweat while trying to fix your car. ")
                        type.type("Each swing of his hammer is getting louder and louder, and Frank is clearly beginning to panic. ")
                        type.type("Frank turns towards you, with tears streaming down his face. Or maybe it's just sweat.")
                        print("\n")
                        type.type("\"Oh man, listen, I'm so sorry about this, you know? I really thought if I just gave it the old hammer whirl that would do the trick. ")
                        type.type("Hold on, maybe I have something in my truck. Stay right here!\"")
                        print("\n")
                        type.type("You watch Frank runs over to his truck, kicks the side of it, gets in, revs his engine, and speeds off into the horizon. God Dammit.")
                        print("\n")
                        return
                else:
                    self.add_danger("Frank")
                    type.type("\"Are you tryna rip me off? Clearly you don't have enough money to afford my services, which is honestly pathetic, since I have the cheapest services around! ")
                    type.type("I don't get what it is with you young folk and not working, just staying home and smoking weed. ")
                    type.type("It's miserable. You're miserable. Dontchu know I know people on the inside! I'll remember this one.\"")
                    print("\n")
                    type.type("You watch as he revs his engine, gets out of his truck, kicks his beater, gets back in, revs his engine, and speeds off into the horizon.")
                    print("\n")
                    return
            else:
                type.type("\"Speak up! You're mumbling. \" ")

    def optimal_oswald(self):
        self.meet("Oswald Event")
        type.type("A glossy black limousine is quietly approaching your wagon. ")
        type.type("As you sit up from your slumber, you read \'Oswald's Optimal Outoparts\' cursively engraved in gold letters on the side of the limo. ")
        type.type("Waving the vehicle down, the limo slows, then stops before you. ")
        type.type("The door opens vertically, and a large red carpet is rolled out onto the street. ")
        type.type("You watch in awe as a man, with a combover and a tuxedo, walks out before you. He coughs, then speaks.")
        print("\n")
        type.type("\"Why hello there! The name's Oswald, as you can see by my nametag. ")
        type.type("Do you like my bowtie? Well of course you do! It appears your limousine has broken down.\" ")
        type.type("Oswald pulls a gold whistle out of his pocket, and blows into it deeply. ")
        type.type("\"Oh Stuart!\" You watch as a bald man in a tailcoat suit, no taller than 4 feet, hobbles over to Oswald's side.")
        print("\n")
        type.type("\"This is Stuart! He will fix your limousine up for a fair price. ")
        type.type("Let's say, I don't know, I suppose a fair price is " + green(bright("500,000 dollars")) + ". ")
        repair_price = random.choice([800, 850, 900])
        type.type("Okay, the look on your face says that I'm making a big mistake. ")
        type.type("Let's try " + green(bright("$" + str(repair_price))) + ", and Stuart here will get you back on the road! Do you accept?\" ")
        while(True):
            yes_or_no = input("").lower()
            print()
            if(yes_or_no == "n") or (yes_or_no == "no"):
                type.type("\"Really? You don't want my services? I'm so sorry Stuart, But it appears they don't want our services.\" ")
                type.type("Stuart begins to break down into tears, and he runs quickly back into the limo. ")
                type.type("\"Shame on you! Shame on you! I hope to never see the likes of you again.\"")
                print("\n")
                type.type("You watch as Oswald rolls up the red carpet, gets back in the limo, and drives off into the distance.")
                print("\n")
                return
            elif((yes_or_no == "y") or (yes_or_no == "yes")):
                if self._balance >= repair_price:
                    self.meet("Oswald")
                    self.set_car_mechanic("Oswald")
                    type.type("\"Jolly good! Stuart!\" ")
                    type.type("You watch as the little man walks to the front of your wagon, opens the hood, and jumps in. ")
                    type.type("You can't really see what's going on, but after a couple of minutes, Stuart jumps back out, covered in oil.")
                    self.change_balance(-repair_price)
                    self.add_item("Car")
                    type.type(magenta(bright("Your car has been fixed! You can now drive around!")))
                    print("\n")
                    type.type("\"Oh my Stuart! Someone got a little too excited, didn't you? ")
                    type.type("Yep, you're getting a bath as soon as we get back to the shop. ")
                    type.type("Thanks again, stranger, it's been a pleasure doing business with you. ")
                    type.type("I recall it's good custom to tip after events like this, yes? Here, take this.\" ")
                    tip = random.choice([50, 100])
                    type.type("Oswald hands you a bright green bill, worth " + green(bright("$" + str(tip))) + ".")
                    self.change_balance(tip)
                    type.type("And with that, you watch as Stuart rolls up the red carpet. Oswald and Stuart get back in the limo, and drive off into the distance.")
                    print("\n")
                    return
                else:
                    type.type("\"Why, it appears you're far too poor to attain my services. I'm truly sorry about this. ")
                    type.type("Tell you what, here's a little something to get you back on your feet.\" ")
                    tip = random.choice([50, 100])
                    type.type("Oswald hands you a bright green bill, worth " + green(bright("$" + str(tip))) + ".")
                    self.change_balance(tip)
                    type.type("And with that, you watch as Stuart rolls up the red carpet. Oswald and Stuart get back in the limo, and drive off into the distance. ")
                    if self._balance > repair_price:
                        type.type("Looking down, you see that after Oswald's tip, you had enough money to pay for the repair service after all, but it was too late. Oh well.")
                    print("\n")
                    return
            else:
                type.type("\"Come again?\" ")

    # ═══════════════════════════════════════════════════════════════════
    # MECHANIC DREAM CHAINS  (fire at night via night event pool)
    # Each method guards itself on the exact dream-counter stage required.
    # Tom  → get_tom_dreams()     0→1 (Rebecca) 1→2 (Nathan) 2→3 (Johnathan)
    # Frank → get_frank_dreams()  0→1 (anger)   1→2 (scar)   2→3 (revolver)  3=complete (dealer_in_dreams)
    # Oswald → get_oswald_dreams() 0→1 (bar)     1→2 (table)  2→3 (riches)
    # ═══════════════════════════════════════════════════════════════════

    # ── TOM DREAMS ──────────────────────────────────────────────────────

    def remember_rebecca(self):
        # DREAM EVENT: Tom's story - Part 1 of 3
        # STORY: Vision of Rebecca in sunlit meadow, can't reach her
        # EFFECTS: Advances tom_dreams to 1
        if self.get_tom_dreams() != 0:
            return
        type.type("As you drift off to sleep, you find yourself standing at the edge of a sunlit meadow. ")
        type.type("The grass sways gently in the breeze, and in the distance, you see a figure waiting for you.")
        print("\n")
        type.type("You can't make out her face, but somehow, you know her name.")
        print("\n")
        type.type(bright("Rebecca."))
        print("\n")
        type.type("You have faint memories of that name. She sounds lovely. ")
        type.type("You try to walk towards her, but the closer you get, the further away she seems. ")
        type.type("You reach out your hand, but before you can touch her...")
        print("\n")
        type.type("You wake up.")
        print("\n")
        type.type(yellow("Something stirs in the back of your mind. A memory you'd rather forget."))
        self.advance_tom_dreams()
        print("\n")

    def remember_nathan(self):
        # DREAM EVENT: Tom's story - Part 2 of 3
        # STORY: Vision of baby Nathan in nursery, fades when touched
        # EFFECTS: Advances tom_dreams to 2
        if self.get_tom_dreams() != 1:
            return
        type.type("Your eyes grow heavy, and once again you find yourself in a dream. ")
        type.type("This time, you're in a nursery. Soft blue walls surround you, ")
        type.type("and a mobile of stars and moons spins lazily above a crib.")
        print("\n")
        type.type("You walk to the crib and peer inside. A baby boy looks up at you with bright, curious eyes. He reaches up towards you, tiny fingers grasping at the air.")
        print("\n")
        type.type("You know his name, somehow. " + bright("Nathan."))
        print("\n")
        type.type("He sounds so sweet. You reach down to pick him up, but as your hands touch him, he fades away like morning mist. ")
        type.type("The nursery crumbles around you, and you're left standing in darkness.")
        print("\n")
        type.type("You wake up with tears on your cheeks that you don't remember crying.")
        print("\n")
        type.type(yellow("The name 'Nathan' feels like a wound that never healed."))
        if not self.has_item("Tom's Wrench"):
            type.type(yellow("A heavy wrench appears on the passenger seat when you wake. Tom's initials scratched into the handle."))
            print("\n")
            self.add_item("Tom's Wrench")
        self.advance_tom_dreams()
        print("\n")

    def remember_johnathan(self):
        # DREAM EVENT: Tom's story - Part 3 of 3
        # STORY: Mirror reveals player's true identity — Johnathan
        # EFFECTS: Advances tom_dreams to 3
        if self.get_tom_dreams() != 2:
            return
        type.type("The dream is clearer this time. You're standing in front of a mirror, but the reflection looking back at you seems... different. Older. Tired. Broken.")
        print("\n")
        type.type("Behind your reflection, you see them. Rebecca, holding Nathan. They're waving at you through the glass, smiling, reaching out.")
        print("\n")
        type.type(quote("Come home,") + " Rebecca mouths. " + quote("We miss you."))
        print("\n")
        type.type("You press your hand against the mirror, and your reflection does the same. But as your palms meet, you finally see your reflection's face clearly.")
        print("\n")
        type.type("And you remember your name.")
        print("\n")
        type.type(bright("Johnathan."))
        print("\n")
        type.type(bright("Is that me? Am I Johnathan?"))
        print("\n")
        type.type("The mirror cracks, and the dream shatters. You wake up, knowing exactly who you are, and exactly what you've lost.")
        print("\n")
        type.type(yellow(bright("The memories won't stay buried forever. Maybe it's time to go home.")))
        self.advance_tom_dreams()
        print("\n")

    # ── FRANK DREAMS ─────────────────────────────────────────────────────

    def dealers_anger(self):
        # DREAM EVENT: Frank's story - Part 1 of 3
        # STORY: Dream of winning blackjack, Dealer rages at you
        # EFFECTS: Advances frank_dreams to 1
        if self.get_frank_dreams() != 0:
            return
        type.type("As you fall asleep, you dream of sitting at a blackjack table. ")
        type.type("The familiar green felt stretches out before you, and across from you sits the Dealer, ")
        type.type("shuffling cards with practiced ease.")
        print("\n")
        type.type("You're dealt a hand. A King and an Ace. " + green(bright("Blackjack.")))
        print("\n")
        type.type("But instead of paying out, the Dealer's face contorts with rage. He slams his fist on the table.")
        print("\n")
        type.type(red(quote("You think you can just WIN?! You think it's that EASY?!")))
        print("\n")
        type.type("His yelling gets louder and louder. At first he's yelling at himself, muttering about odds and luck. But then, he turns to you. His eyes bore into yours.")
        print("\n")
        type.type(red(quote("This is YOUR fault. ALL OF IT.")))
        print("\n")
        type.type("The screaming grows deafening until you jolt awake, heart pounding.")
        print("\n")
        type.type(yellow("The Dealer's rage echoes in your mind long after you wake."))
        self.advance_frank_dreams()
        print("\n")

    def dealers_scar(self):
        # DREAM EVENT: Frank's story - Part 2 of 3
        # STORY: Dealer's scarred face and jade green glass eye revealed
        # EFFECTS: Advances frank_dreams to 2, lose 2-3 sanity
        if self.get_frank_dreams() != 1:
            return
        type.type("Sleep takes you to the casino again. The same blackjack table, the same green felt, the same Dealer sitting across from you.")
        print("\n")
        type.type("But something's different this time. The Dealer leans forward, into the flickering light of the overhead lamp.")
        print("\n")
        type.type("And you see his face clearly for the first time.")
        print("\n")
        type.type("The left side is a ruin of scar tissue, twisted and grotesque. ")
        type.type("Where his left eye should be, there sits a " + cyan(bright("jade green glass eye")) + ", cold and unblinking. ")
        type.type("It catches the light and seems to stare right through you.")
        print("\n")
        type.type(red(quote("See something you like?")))
        print("\n")
        type.type("His voice is mocking, bitter. You try to look away, but you can't. The glass eye holds you frozen until you wake, gasping for air.")
        print("\n")
        type.type(yellow("You can still feel that glass eye watching you."))
        if not self.has_item("Frank's Flask"):
            type.type(yellow("A battered flask rolls out from under your seat as you wake. Engraved: 'F.H.' Smells like bourbon. Frank's."))
            print("\n")
            self.add_item("Frank's Flask")
        self.advance_frank_dreams()
        self.lose_sanity(random.choice([2, 3]))
        print("\n")

    def dealers_revolver(self):
        # DREAM EVENT: Frank's story - Part 3 of 3
        # STORY: Dealer reaches for his revolver — BANG
        # EFFECTS: Advances frank_dreams to 3
        if self.get_frank_dreams() != 2:
            return
        type.type("The casino dream returns, but the atmosphere has changed. The air is thick with tension, and the Dealer's hands tremble as he shuffles the cards.")
        print("\n")
        type.type("He's furious. You don't understand why, but his rage fills the room like smoke.")
        print("\n")
        type.type(red(quote("You just keep winning, don't you? You just keep TAKING and TAKING.")))
        print("\n")
        type.type("You try to explain that it's just a game, just luck, but the words die in your throat.")
        print("\n")
        type.type("The Dealer reaches down slowly. His scarred hand wraps around the grip of a revolver at his waist. ")
        type.type("The jade glass eye catches the light as he raises the gun.")
        print("\n")
        type.type(red(quote("Let's see how lucky you really are.")))
        print("\n")
        type.type(red(bright("BANG.")))
        print("\n")
        type.type("You jolt awake, clutching your chest, certain for a moment that you'd been shot. Your heart pounds so hard you can hear it in your ears.")
        print("\n")
        type.type(yellow(bright("The Dealer isn't just angry. He's dangerous. And something tells you this isn't over.")))
        self.advance_frank_dreams()
        print("\n")

    def dealer_in_dreams(self):
        # DREAM EVENT: Frank dream chain COMPLETE — Dealer gives you the Joker
        # EFFECTS: Receive "Dealer's Joker" item (one-time)
        if self.get_frank_dreams() != 3:
            return
        if self.has_met("Dealer Dream Complete"):
            return
        self.meet("Dealer Dream Complete")
        type.type("You fall asleep and find yourself in the familiar casino dreamscape. But this time, something is different.")
        print("\n")
        type.type("The Dealer sits across from you, but he's not angry. He looks... tired. Old.")
        print("\n")
        type.type(quote("You're still here,") + " he says quietly. " + quote("After everything. You're still playing."))
        print("\n")
        type.type("He shuffles the cards slowly, methodically.")
        print("\n")
        type.type(quote("I've been dealing cards for longer than you can imagine. Watching people win. Watching them lose. "))
        type.type(quote("Watching them destroy themselves chasing something they'll never catch."))
        print("\n")
        type.type("He looks at you with his jade glass eye.")
        print("\n")
        type.type(quote("But you... you're different. I don't know if that's good or bad yet."))
        print("\n")
        type.type("He deals you a single card. The Joker.")
        print("\n")
        type.type(quote("Keep it. A gift. Or a warning. Interpret it however you want."))
        print("\n")
        type.type("You wake up with a playing card in your hand. A Joker. It wasn't there before.")
        self.add_item("Dealer's Joker")
        type.type(yellow(bright("The line between dreams and reality grows thinner.")))
        print("\n")

    # ── OSWALD DREAMS ────────────────────────────────────────────────────

    def casino_bar(self):
        # DREAM EVENT: Oswald's story - Part 1 of 3
        # STORY: Dream of luxury casino bar, ordering expensive drinks
        # EFFECTS: Advances oswald_dreams to 1
        if self.get_oswald_dreams() != 0:
            return
        type.type("You drift into a dream, and find yourself sitting at a bar inside a grand casino. ")
        type.type("Crystal chandeliers hang from the ceiling, their light dancing across marble floors. ")
        type.type("The air smells of expensive cigars and possibility.")
        print("\n")
        type.type("You're chatting it up with the person next to you-someone important, though you can't quite remember who. A bartender in a crisp white shirt approaches.")
        print("\n")
        type.type(quote("What'll it be?"))
        print("\n")
        type.type("You order a drink. The bartender raises an eyebrow.")
        print("\n")
        type.type(quote("That's gonna cost you. Expensive taste you've got."))
        print("\n")
        type.type("You wave your hand dismissively. Money is no object. Not here. Not in this place.")
        print("\n")
        type.type("The bartender shrugs and pours your drink. As he slides it across the bar, he says:")
        print("\n")
        type.type(quote("Well, it's your drink after all."))
        print("\n")
        type.type("You wake up, the phantom taste of bourbon lingering on your tongue.")
        print("\n")
        type.type(yellow("You can almost hear the slot machines in the distance."))
        self.advance_oswald_dreams()
        print("\n")

    def casino_table(self):
        # DREAM EVENT: Oswald's story - Part 2 of 3
        # STORY: Play blackjack against a dealer who looks exactly like you
        # EFFECTS: Advances oswald_dreams to 2, lose 3-4 sanity
        if self.get_oswald_dreams() != 1:
            return
        type.type("The dream takes you back to the casino. But this time, you're not at the bar. ")
        type.type("You're sitting at a blackjack table, a drink in your hand. ")
        type.type("The ice clinks against the glass as you take a sip.")
        print("\n")
        type.type(quote("Care to be dealt in?"))
        print("\n")
        type.type("You look up at the dealer, and your blood runs cold.")
        print("\n")
        type.type("The dealer looks " + bright("exactly like you."))
        print("\n")
        type.type("Same face. Same eyes. Same everything. They smile at you-your own smile, but somehow wrong. Twisted.")
        print("\n")
        type.type(quote("Is something the matter?"))
        print("\n")
        type.type("You shake your head. " + quote("No. Nothing's wrong."))
        print("\n")
        type.type("You smile back and take a long sip of your drink. The other you deals the cards, ")
        type.type("and you play in silence, the only sound being the shuffle of cards and the clink of chips.")
        print("\n")
        type.type("You wake up, unsure which one of you was the real one.")
        if not self.has_item("Oswald's Dice"):
            type.type(yellow("Two weighted dice sit in your palm when you wake. A sticker on the bottom: 'O.O.' Oswald's lucky pair."))
            print("\n")
            self.add_item("Oswald's Dice")
        self.lose_sanity(random.choice([3, 4]))
        print("\n")
        type.type(yellow("The line between player and dealer feels blurrier than before."))
        self.advance_oswald_dreams()
        print("\n")

    def casino_riches(self):
        # DREAM EVENT: Oswald's story - Part 3 of 3
        # STORY: Tempting vision of eternal wealth — the other you offers forever
        # EFFECTS: Advances oswald_dreams to 3
        if self.get_oswald_dreams() != 2:
            return
        type.type("You're back at the casino table. Your double sits across from you, dealing cards with mechanical precision. ")
        type.type("You take a sip of bourbon and look at your cards.")
        print("\n")
        type.type(green(bright("Blackjack.")))
        print("\n")
        type.type("The table erupts in cheers. People you don't recognize clap you on the back, shake your hand, toast to your success. ")
        type.type("You down your drink and slam the glass on the table.")
        print("\n")
        type.type("And then the ceiling opens up.")
        print("\n")
        type.type("Hundred dollar bills begin to rain down from above. They fall like snow, piling up on the table, on the floor, in your lap. ")
        type.type("Everyone is laughing, grabbing at the money, stuffing their pockets.")
        print("\n")
        type.type("You've never felt so " + green(bright("rich")) + ". So " + green(bright("powerful")) + ". So " + green(bright("fantastic")) + ".")
        print("\n")
        type.type("The other you catches your eye and smiles. " + quote("This could all be yours, you know. Forever."))
        print("\n")
        type.type("You wake up with your fist clenched, as if still holding onto bills that were never there.")
        print("\n")
        type.type(yellow(bright("The promise of wealth echoes in your mind. What would you sacrifice to feel that way forever?")))
        self.advance_oswald_dreams()
        print("\n")

    # ════════════════════════════════════════════════════════════════════
    # ROADSIDE MECHANIC VISIT — late-game car-trouble intervention
    # ════════════════════════════════════════════════════════════════════

    def roadside_mechanic_visit(self):
        """
        After car trouble strands the player, the mechanic who sold them their
        car has a chance to drive by and offer a discounted roadside repair.

        Returns True if the mechanic visited (afternoon partially recovered).
        Returns False if no mechanic was available or the roll missed.
        """
        # Only fires when the player actually has a car and has met at least one mechanic
        if not self.has_item("Car"):
            return False

        # 45 % chance per eligible trouble event — likely enough to matter for longevity
        if random.randrange(100) >= 45:
            return False

        # Build the pool of mechanics the player has actually done business with
        eligible = []
        if self.has_met("Tom"):
            eligible.append("tom")
        if self.has_met("Frank"):
            eligible.append("frank")
        if self.has_met("Oswald"):
            eligible.append("oswald")

        if not eligible:
            return False

        mechanic = random.choice(eligible)

        if mechanic == "tom":
            self._roadside_visit_tom()
        elif mechanic == "frank":
            self._roadside_visit_frank()
        else:
            self._roadside_visit_oswald()

        return True

    def _roadside_visit_tom(self):
        repair_cost = random.choice([100, 150, 200])
        type.type("A familiar gold truck rolls up and parks behind you. Tom jumps out, wiping his hands on a rag.")
        print("\n")
        type.type(quote("Well I'll be. Didn't I just sell you this thing? What'd you do to it?"))
        print("\n")
        type.type("He circles the car, muttering to himself, then crouches down and peers underneath.")
        print("\n")
        type.type(quote("I can patch this up right here. Won't take long. Call it ") + green(bright("${:,}".format(repair_cost))) + quote(" for the trouble."))
        print("\n")
        type.type("Repair for " + green(bright("${:,}".format(repair_cost))) + "? ")
        yes_or_no = ask.yes_or_no("")
        print()
        if yes_or_no == "yes":
            if self._balance >= repair_cost:
                self.change_balance(-repair_cost)
                self.remove_travel_restriction("Wasted Afternoon")
                type.type(quote("Good as new. Almost. Don't push it so hard next time."))
                print("\n")
                type.type("Tom tosses his rag back in the truck and drives off. Your afternoon is yours again.")
                print("\n")
            else:
                random_chance = random.randrange(2)
                if random_chance == 0:
                    discounted = repair_cost - 50
                    type.type(quote("Yunno, I can see you're in a bad way. Tell ya what — ") + green(bright("${:,}".format(discounted))) + quote("?"))
                    print("\n")
                    yes_or_no_2 = ask.yes_or_no("")
                    print()
                    if yes_or_no_2 == "yes" and self._balance >= discounted:
                        self.change_balance(-discounted)
                        self.remove_travel_restriction("Wasted Afternoon")
                        type.type(quote("Alright! Good as new. Be seein' ya around, ya know?"))
                        print("\n")
                    else:
                        type.type(quote("I really wish there was something more I could do. Best of luck, my friend."))
                        print("\n")
                        type.type("Tom gives a sad wave and drives away.")
                        print("\n")
                else:
                    type.type(quote("I really wish there was something I could do. Best of luck my friend."))
                    print("\n")
                    type.type("Tom gives a sad wave and drives away.")
                    print("\n")
        else:
            type.type(quote("Suit yourself. Just don't let it get worse."))
            print("\n")
            type.type("Tom shrugs, hops back in the truck, and rolls away.")
            print("\n")

    def _roadside_visit_frank(self):
        repair_cost = random.choice([75, 100, 150])
        type.type("A rusty van with a hand-painted \'Frank's\' on the door rattles to a stop beside you.")
        print("\n")
        type.type("Frank leans out the window, goggles pushed up on his forehead.")
        print("\n")
        type.type(quote("Yo, is that MY car? I mean — the one I fixed? Dude. What happened?"))
        print("\n")
        type.type("He hops out and starts poking at things without asking.")
        print("\n")
        type.type(quote("Okay okay okay — I can do this. ") + green(bright("${:,}".format(repair_cost))) + quote(". Parts are cheap, labour is love."))
        print("\n")
        type.type("Let Frank fix it for " + green(bright("${:,}".format(repair_cost))) + "? ")
        yes_or_no = ask.yes_or_no("")
        print()
        if yes_or_no == "yes":
            if self._balance >= repair_cost:
                self.change_balance(-repair_cost)
                success_chance = random.randrange(5)
                if success_chance < 2:
                    self.remove_travel_restriction("Wasted Afternoon")
                    type.type(quote("NAILED IT. Bam. Done. You're welcome, universe."))
                    print("\n")
                    type.type("Frank does a little bow, trips over his own toolbox, and drives off. Car's running.")
                    print("\n")
                else:
                    type.type(quote("Okay so it's... slightly different than before. But it WORKS. Probably."))
                    print("\n")
                    type.type("You're not sure what he changed, but the car starts. The afternoon is still gone, though.")
                    print("\n")
            else:
                # Frank adds danger when you say yes but can't pay — consistent with intro
                self.add_danger("Frank")
                type.type(quote("Are you KIDDING me? You can't afford that? That's like the cheapest I go! I'll remember this."))
                print("\n")
                type.type("Frank kicks your bumper and speeds away.")
                print("\n")
        else:
            type.type(quote("Your loss, man. Literally."))
            print("\n")
            type.type("Frank shakes his head and drives off.")
            print("\n")

    def _roadside_visit_oswald(self):
        repair_cost = random.choice([150, 200, 250])
        type.type("A sleek black limousine glides to a stop. The door opens vertically. Oswald steps out.")
        print("\n")
        type.type(quote("My goodness. I was simply passing through when I recognized my handiwork. What a small world."))
        print("\n")
        type.type("He produces a leather-bound toolkit from inside the limo and gets straight to work.")
        print("\n")
        type.type(quote("A professional rate for a repeat customer — ") + green(bright("${:,}".format(repair_cost))) + quote(". Shall we?"))
        print("\n")
        type.type("Accept Oswald's roadside repair for " + green(bright("${:,}".format(repair_cost))) + "? ")
        yes_or_no = ask.yes_or_no("")
        print()
        if yes_or_no == "yes":
            if self._balance >= repair_cost:
                self.change_balance(-repair_cost)
                self.remove_travel_restriction("Wasted Afternoon")
                tip = random.choice([50, 100])
                type.type(quote("Splendid. Good as new. I do insist on quality. And do allow me —"))
                print("\n")
                self.change_balance(tip)
                type.type("Oswald presses " + green(bright("${:,}".format(tip))) + " into your hand.")
                print("\n")
                type.type("He packs his kit, adjusts his bowtie, and the limo glides away. Afternoon saved.")
                print("\n")
            else:
                type.type(quote("Your funds are insufficient. However — "))
                print("\n")
                tip = random.choice([50, 100])
                type.type("Oswald reaches into his breast pocket and produces a crisp bill.")
                print("\n")
                type.type(quote("Consider this a gesture of goodwill. Do get that seen to properly."))
                print("\n")
                self.change_balance(tip)
                type.type("You received " + green(bright("${:,}".format(tip))) + " from Oswald.")
                print("\n")
        else:
            type.type(quote("Very well. Safe travels."))
            print("\n")
            type.type("Oswald tips his hat and the limo glides away.")
            print("\n")

    # ════════════════════════════════════════════════════════════════════

    def update_story_event_prereqs(self):
        if(self._balance>=200):
            self._prereqs[0] = True
        if self.has_item("Car"):
            self._prereqs_done[0] = True


