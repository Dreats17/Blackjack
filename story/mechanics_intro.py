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

class MechanicsIntroMixin:
    """Mechanic intro events: Tom, Frank, Oswald story introductions"""

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

    def update_story_event_prereqs(self):
        if(self._balance>=200):
            self._prereqs[0] = True
        if self.has_item("Car"):
            self._prereqs_done[0] = True


