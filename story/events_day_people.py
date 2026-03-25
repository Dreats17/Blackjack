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

class DayPeopleMixin:
    """People events: human social encounters, strangers, and NPCs"""

    def freight_truck(self):
        # EVENT: A trucker wakes you up by honking at your car
        # EFFECTS: Usually just annoying
        # RARE (3%): Guilty trucker apologizes and gives $200-500
        # Alt dialogue for repeated event + rare special variant
        rare_chance = random.randrange(100)
        
        if self.has_item("Binocular Scope"):
            type.type("You spot the freight truck approaching from a mile away with your " + cyan(bright("Binocular Scope")) + ". The driver looks like he's having a rough morning.")
            print(PAR)
            type.type("You have time to prepare yourself before the inevitable honking.")
            self.restore_sanity(1)
            print(PAR)
        
        if rare_chance < 3:  # 3% RARE VARIANT - The Guilt Trip
            type.type("A horn blares right outside your car, rattling the windows. Looking out, you see a man in a freight truck.")
            print(PAR)
            type.type("But something's different. He's not laughing. He's... crying?")
            print(PAR)
            type.type(quote("I'm sorry... I'm so sorry for all those times I honked at you. "))
            type.type(quote("I was going through some stuff, man. My wife left me. My dog died. My truck? Also dying."))
            print(PAR)
            type.type("He wipes his nose with his sleeve.")
            print(PAR)
            type.type(quote("Here. Take this. It's not much, but... I want to make things right."))
            print(PAR)
            type.type("The trucker hands you a wad of cash through the window, still sniffling.")
            print(PAR)
            if self.has_item("Enchanting Silver Bar"):
                payout = random.randint(300, 600)
                type.type("Then he notices the " + cyan(bright("Enchanting Silver Bar")) + " on your seat. The metal catches the sunrise and throws silver light across his windshield.")
                print(PAR)
                type.type(quote("Don't sell that today,") + " he says, suddenly serious. " + quote("Give it two more suns. Silver like that gets hungry before it gets generous."))
                print(PAR)
                type.type("He stuffs a larger wad of bills into your hand like he's paying an apology and a consultation fee at the same time.")
                self.change_balance(payout)
                self.restore_sanity(3)
            else:
                self.change_balance(random.randint(200, 500))
            type.type(quote("Drive safe, friend. Drive safe."))
            print(PAR)
            type.type("And with that, the freight truck slowly pulls away, the horn playing a sad melody into the distance.")
            print(PAR)
            return
        
        # Normal variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("A deafening horn blast shakes your entire car. ")
            type.type("Looking out your window, you see a man, in a bright red hat, ")
            type.type("inside of a freight truck that's parked just outside of your vehicle.")
            print(PAR)
            type.type(quote("Hey, you. Wake the fuck up! Hahahaha!"))
            print(PAR)
            type.type("You watch as the man honks his horn one more time, laughs, and drives off into the distance. What a jerk.")
        elif variant == 1:
            type.type("HOOOOOOONK! You nearly hit the roof of your car as a freight truck blasts past, the driver giving you a middle finger out the window.")
            print(PAR)
            type.type(quote("GET A HOUSE, LOSER!"))
            print(PAR)
            type.type("The truck disappears, leaving you with ringing ears and a sour mood.")
        elif variant == 2:
            type.type("The unmistakable sound of an airhorn tears through your dreams. You bolt upright to see a trucker parked RIGHT next to your car, grinning like an idiot.")
            print(PAR)
            type.type(quote("Rise and shine, buttercup! Time to face another day!"))
            print(PAR)
            type.type("He gives you a thumbs up, hits the horn three more times for good measure, then drives off cackling.")
        else:
            type.type("Rhythmic honking fills the air. HONK HONK HONK-HONK-HONK. Is that... Shave and a Haircut?")
            print(PAR)
            type.type("A trucker waves at you from his cab, waiting expectantly. When you don't respond with 'two bits,' he shrugs and drives off, disappointed.")
            print(PAR)
            type.type(quote("No culture these days...") + " you hear him mutter.")
        print(PAR)
        return

    # Conditional

        print(PAR)
        return
    def lone_cowboy(self):
        # EVENT: Meet Davey Jameson the cowboy who gives you a carrot for horses
        # ONE-TIME: Only happens once (checks "Cowboy" met status)
        # EFFECTS: Adds "Carrot" item to inventory
        if self.has_met("Cowboy"):
            self.day_event()
            return

        self.meet("Cowboy")
        type.type("The sound of hooves trotting on pavement drifts through your window, along with some distant whistling. ")
        type.type("You sit up, and through your windshield, you see a man wearing a full cowboy suit, ")
        type.type("with matching black hat and boots, and a short brown beard. ")
        print(PAR)
        type.type("He's riding a magnificent horse, muscular, but nimble, each step powerful, but precise. ")
        type.type("The man reaches your window, and in a deep southern accent, he begins to talk to you.")
        print(PAR)
        
        # Animal Whistle lets you befriend the horse
        if self.has_item("Animal Whistle") and not self.has_companion("Thunder"):
            type.type("The " + magenta(bright("Animal Whistle")) + " resonates from your pocket. The horse whinnies and stamps its hooves.")
            print(PAR)
            type.type("Jameson looks surprised. " + quote("Well I'll be. My horse NEVER acts like this. He... he likes you!"))
            print(PAR)
            type.type("The horse nuzzles your hand through the window. Jameson dismounts, shaking his head in wonder.")
            print(PAR)
            type.type(quote("I've had Thunder for ten years, and I've never seen him bond with anyone like this. "))
            type.type(quote("Tell ya what, partner - Thunder's yours now. He's chosen you. "))
            type.type(quote("You treat him right, ya hear?"))
            print(PAR)
            type.type("You've just been given a HORSE by a cowboy. The horse's name is " + cyan(bright("Thunder")) + ".")
            print(PAR)
            type.type("Jameson tips his hat, wipes a tear, and walks off down the road whistling. ")
            type.type("Thunder follows your wagon now, proud and free.")
            self.add_companion("Thunder", "Horse")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.add_item("Carrot")  # He still gives you the carrot
            print(PAR)
            return
        
        type.type(open_quote("Howdy, partner! The name's Jameson. Davey Jameson. "))
        type.type(quote("I happen to notice you were admiring my steed. He's a beauty, isn't he. "))
        type.type(quote("You see, it's common courtesy when a cowboy rides by, "))
        type.type(close_quote("to give their mighty steed a carrot, as a way to express your gratitude for their hardwork and commitment to the job."))
        print(PAR)
        type.type(quote("You my friend, you are carrotless. That's quite a disrespectful showing towards my steed. "))
        type.type(quote("My, my, this can't do at all. What if another cowboy comes by, you're just gonna disrespect their steed, too? "))
        type.type(quote("Tell you what, I happen to have one spare carrot in my pouch. Take this, and be ready. "))
        type.type(quote("You never know when a cowboy's gonna come trotting by."))
        print(PAR)
        self.add_item("Carrot")
        type.type("Davey Jameson hands you his " + bright(magenta("Carrot")) + ", and smiles.")
        print(PAR)
        type.type(quote("See, with this carrot in your possession, you're ready for anytime a cowboy strolls on down this road. "))
        type.type(quote("Just give their steed a carrot, and they'll be very grateful."))
        print(PAR)
        type.type("And with that, Jameson reins his horse high into the air, gives you a yee-haw, then dashes off down the road.")
        print(PAR)

        print(PAR)
        return
    def whats_my_name(self):
        # EVENT: Little girl Suzy asks your name (establishes player name)
        # ONE-TIME: Only happens if player name is not yet set
        # EFFECTS: Sets player __name variable based on input
        if not self._name == None:
            self.day_event()
            return

        type.type("Sneakers scrape against the concrete outside-rhythmic, getting closer. ")
        type.type("As you sit up from your seat, you notice a little girl, with blonde hair and pigtails, jump roping towards you.")
        print(PAR)
        type.type(space_quote("Howdy stranger! My name's Suzy! Do you like my name?"))
        answer = ask.yes_or_no("\"What was that?\" ")
        if answer == "yes":
            type.type(quote("Thanks! My mom gave it to me, before she disappeared. Who knows where she ran off to!"))
        elif answer == "no":
            type.type(quote("Wow! That's not very nice of you. You're rude, stranger."))

        print(PAR)
        type.type(space_quote("Hey, what's your name, anyways?"))
        while True:
            name = str(input())
            type.type(space_quote("So your name is " + name + "?"))
            answer = ask.yes_or_no(space_quote("What was that?"))
            if answer == "yes":
                self._name = name
                type.type("\"" + name + "...I like that name! Hello, " + name + "!\"")
                print(PAR)
                type.type(space_quote("Well, " + name + ", I've got to get going now. Wouldn't want the bears to eat me!"))
                type.type("And with that, Suzy, without missing a beat, continues to jump rope down the street.")
                print(PAR)
                break
            elif answer == "no":
                type.type(quote("So you lied to me? You're a liar, stranger!"))
                print(PAR)
                type.type(space_quote("Come on, tell me your real name!"))
    
        print(PAR)
        return
    def interrogation(self):
        # EVENT: Man in red suit interrogates you about living in your car
        # ONE-TIME: Only happens once (checks "Interrogator" met status)
        # EFFECTS: Adds "Further Interrogation" danger, lose 1-2 sanity
        # CHAIN: First of the interrogation storyline
        if self.has_met("Interrogator"):
            self.day_event()
            return

        self.meet("Interrogator")
        self.add_danger("Further Interrogation")
        self.lose_sanity(random.choice([1, 2]))  # Harassment drains sanity
        type.type("Through your windshield, there's a car parked right in front of you. That wasn't there before. ")
        type.type("Confused, and dazed, you sit up. As you open the door and get out of your car, ")
        type.type("you notice a man, in a bright red suit, peering into your trunk.")
        print(PAR)
        type.type("The man sees you, and walks up to you.")
        print(PAR)
        if self.has_item("Marvin's Monocle"):
            type.type("You raise " + cyan(bright("Marvin's Monocle")) + " to your eye before he speaks. The smoky lens catches no badge, no weapon, no backup car. Just a municipal clipboard, a tired jaw, and a man bluffing authority because it's all he has.")
            print(PAR)
            type.type("Useful to know. This is harassment, not a raid.")
            print(PAR)
        type.type(quote("You. You're awake. Good. You know that you aren't supposed to be here? "))
        type.type(quote("This isn't a spot for people to live. This is a road for people to drive. I hope you know this."))
        print(PAR)
        type.type(space_quote("Do you know this?"))
        answer = ask.yes_or_no(space_quote("Do you? Know this?"))
        if answer == "yes":
            type.type(quote("So you do know this. Then why do you live here? You shouldn't. It's not right, man. "))
            type.type(quote("I'd suggest you stop living here. Maybe live somewhere else instead. Just not here."))
            print(PAR)
        elif answer == "no":
            type.type(quote("You don't know this? How don't you know this? It's super obvious stuff, man. "))
            type.type(quote("People don't live at places where they're not supposed to, and that's exactly what you're doing right now. "))
            type.type(quote("I'd suggest you stop it, right this instant."))
            print(PAR)
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 20 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print(PAR)
        if self.has_item("Marvin's Monocle"):
            type.type("You watch him leave through the monocle and catch one last tell: relief. He wanted you rattled, not removed. The distinction helps.")
            self.restore_sanity(3)
            print(PAR)
        return

    # ==========================================
    # NEW POOR DAY EVENTS - Everytime
    # ==========================================
    
        print(PAR)
        return
    def old_man_jenkins(self):
        # EVENT: Meet Old Man Jenkins who rants about old-timey homelessness
        # ONE-TIME: Only happens once (checks "Old Man Jenkins" met status)
        # EFFECTS: Gives $25-75 in coins
        # One-Time - quirky NPC
        if self.has_met("Old Man Jenkins"):
            self.day_event()
            return
        
        self.meet("Old Man Jenkins")
        type.type("Someone is rapping on your window with a cane. An ancient man peers in at you, his face like a crumpled paper bag.")
        print(PAR)
        type.type(quote("You there! Young person! I've been walking this road for sixty years "))
        type.type(quote("and I've never seen someone sleeping in their CAR before! What's the world coming to?"))
        print(PAR)
        type.type("You try to explain your situation, but he just waves his cane dismissively.")
        print(PAR)
        type.type(quote("In my day, we slept in DITCHES like RESPECTABLE vagrants! Cars! Bah! Too fancy! "))
        type.type(quote("Back in the Depression, we didn't even have wheels-we just rolled places with our own two legs!"))
        print(PAR)
        type.type("He rants for a solid ten minutes about the good old days of homelessness.")
        print(PAR)
        type.type(quote("Here, take this. You'll need it more than me. I'm 97 years old and I've never spent a dime I didn't have to."))
        print(PAR)
        gift = random.randint(25, 75)
        if self.has_item("Pocket Watch") or self.has_item("Grandfather Clock"):
            watch = "Grandfather Clock" if self.has_item("Grandfather Clock") else "Pocket Watch"
            if watch == "Grandfather Clock":
                bonus = random.randint(60, 120)
                type.type("Then he spots the " + cyan(bright("Grandfather Clock")) + " bulging impossibly in your pocket and squints hard enough to rewrite history.")
                print(PAR)
                type.type(quote("Now THAT'S proper craftsmanship. Completely unreasonable size. I respect it."))
                print(PAR)
                type.type("He digs deeper into his coat and adds a second fistful of old bills and transit tokens just for showing him something that ridiculous.")
                gift += bonus
                self.restore_sanity(4)
            else:
                bonus = random.randint(25, 60)
                type.type("Your " + cyan(bright("Pocket Watch")) + " ticks just loud enough for him to hear. He stops mid-rant and smiles for the first time.")
                print(PAR)
                type.type(quote("Rail yard timepiece, huh? My brother carried one just like it. Kept us fed three winters running."))
                print(PAR)
                type.type("He presses a few extra folded bills into your hand for reminding him of somebody who knew how to keep moving.")
                gift += bonus
                self.restore_sanity(2)
            self.update_pocket_watch_durability()
            print(PAR)
        type.type("Old Man Jenkins hands you " + green(bright("$" + str(gift))) + " in coins, mostly pennies and nickels.")
        self.change_balance(gift)
        print(PAR)
        type.type("And with that, he hobbles off down the road, still muttering about kids these days.")
        print(PAR)

        print(PAR)
        return
    def the_mime(self):
        # EVENT: A mime acts out your sad life story silently
        # ONE-TIME: Only happens once (checks "Mime" met status)
        # EFFECTS: Applauding gives $20 and heals 5 HP
        # One-Time - weird NPC
        if self.has_met("Mime"):
            self.day_event()
            return
        
        self.meet("Mime")
        type.type("You step out of your car and nearly collide with... a mime? Full striped shirt, white face paint, the whole nine yards.")
        print(PAR)
        type.type("The mime stares at you. You stare back.")
        print(PAR)
        type.type("Without a word (obviously), the mime begins to act out a scene. He's pretending to be trapped in a box. Classic.")
        print(PAR)
        type.type("Then he mimes... crying? Counting money? Losing at cards?")
        print(PAR)
        type.type("Wait. Is he acting out YOUR life?")
        print(PAR)
        type.type("The mime finishes with a dramatic death scene, tongue out and everything, then springs back up and takes a bow.")
        print(PAR)
        answer = ask.yes_or_no("Do you applaud? ")
        if answer == "yes":
            type.type("The mime beams and hands you an invisible flower. You pretend to smell it.")
            print(PAR)
            type.type("He then gives you a very real " + green(bright("$20")) + " bill from his pocket, waves, and walks away into an invisible wall.")
            self.change_balance(20)
            self.heal(5)
        else:
            type.type("The mime looks devastated. He mimes a single tear rolling down his cheek, then slowly backs away, never breaking eye contact.")
            print(PAR)
            type.type("You feel kind of bad about that.")
        print(PAR)

    # ==========================================
    # SECRET EVENTS - POOR TIER
    # ==========================================
    
        print(PAR)
        return
    def midnight_visitor(self):
        # SECRET EVENT: The Devil appears when you have exactly $666
        # TRIGGER: Balance must be exactly $666
        # EFFECTS: Offers double-or-nothing coin flip
        #   - Win: Double your money (+$666)
        #   - Lose: Adds "Devil's Debt" danger, lose 2-3 sanity
        #   - Decline: Nothing happens, just creepy atmosphere
        # SECRET - Only triggers at exactly $666 balance
        if self.get_balance() != 666:
            self.day_event()
            return
        
        self.lose_sanity(random.choice([3, 4, 5]))  # Supernatural encounter severely drains sanity
        type.type("The light outside your car dims. The air grows thick and cold, like the sun never fully rose.")
        print(PAR)
        type.type("A figure stands outside your window. Tall. Thin. Its face is in shadow, but you can see its smile-too wide, too many teeth.")
        print(PAR)
        type.type(red(quote("Six hundred and sixty-six dollars. How fitting.")))
        print(PAR)
        type.type("You blink, and the figure is inside your car, sitting in the passenger seat.")
        print(PAR)
        type.type(red(quote("I've been watching you, gambler. I like your style. Tell you what-I'll make you an offer.")))
        print(PAR)
        type.type(quote("Double or nothing. I flip a coin. Heads, I double your money. Tails... well. Let's just say you'll owe me."))
        print(PAR)
        answer = ask.yes_or_no("Accept the devil's offer? ")
        if answer == "yes":
            if not self.has_achievement("devils_deal"): self.unlock_achievement("devils_deal")
            if self.has_item("Lucky Medallion"):
                type.type("Your " + cyan(bright("Lucky Medallion")) + " turns hot enough to sting. The devil's coin jerks midair like it hit an invisible wire.")
                print(PAR)
                type.type("It lands on its edge. Wobbles. Falls to " + green(bright("HEADS")) + ".")
                print(PAR)
                type.type(red(quote("Now that's cheating. I should be offended. Instead, I'm impressed.")))
                print(PAR)
                type.type("The figure laughs, tips an invisible hat, and leaves you with doubled money and a very unsettled pulse.")
                self.change_balance(666)
                self.update_lucky_coin_durability()
            elif self.has_item("Lucky Coin"):
                type.type("Your " + cyan(bright("Lucky Coin")) + " rattles in your pocket like it wants to be part of this.")
                print(PAR)
                type.type("The devil notices. " + red(quote("Fine. One charm against one curse. Call it twice.")))
                print(PAR)
                flip_one = random.choice(["heads", "tails"])
                flip_two = random.choice(["heads", "tails"])
                type.type("The first dark coin lands on " + bright(flip_one) + ". The second lands on " + bright(flip_two) + ".")
                print(PAR)
                if "heads" in (flip_one, flip_two):
                    type.type(red(quote("You brought your own luck. Annoying, but effective.")))
                    print(PAR)
                    type.type("One of the two impossible flips went your way. The figure honors the bargain and vanishes.")
                    self.change_balance(666)
                else:
                    type.type(red(quote("Two tails. Some debts are enthusiastic.")))
                    print(PAR)
                    type.type("Even with the charm, the darkness wins both tosses. You keep your money, but the debt follows you anyway.")
                    self.add_danger("Devil's Debt")
                    self.lose_sanity(2)
                self.update_lucky_coin_durability()
            elif self.has_item("Lucky Charm Bracelet"):
                type.type("Your " + cyan(bright("Lucky Charm Bracelet")) + " tingles on your wrist, the charms rattling like tiny bells.")
                print(PAR)
                type.type("The devil notices. " + red(quote("A bracelet of trinkets? How quaint. But luck is luck.")))
                print(PAR)
                type.type("The dark coin lands on " + green(bright("HEADS")) + " after an impossible wobble.")
                print(PAR)
                type.type(red(quote("Fine. Take your winnings. But remember who you cheated.")))
                print(PAR)
                type.type("The figure vanishes, leaving you with doubled money and a bracelet that feels heavier.")
                self.change_balance(666)
            elif random.randrange(2) == 0:
                type.type(red("The figure flips a coin that seems to be made of pure darkness. It spins impossibly slow..."))
                print(PAR)
                type.type(green(bright("HEADS.")))
                print(PAR)
                type.type(red(quote("Lucky you. This time.")))
                print(PAR)
                type.type("You blink again, and the figure is gone. But your money pile has doubled.")
                self.change_balance(666)
            else:
                type.type(red("The figure flips a coin that seems to be made of pure darkness. It spins impossibly slow..."))
                print(PAR)
                type.type(red(bright("TAILS.")))
                print(PAR)
                type.type(red(quote("A deal's a deal. Don't worry-I won't collect today. But I WILL collect. Eventually.")))
                print(PAR)
                type.type("You blink, and the figure is gone. Your money is untouched, but you feel like you've lost something far more valuable.")
                self.add_danger("Devil's Debt")
                self.lose_sanity(random.choice([2, 3]))  # Losing to devil further drains sanity
        else:
            type.type("The figure laughs, a sound like breaking glass.")
            print(PAR)
            type.type(red(quote("Wise. Or cowardly. Time will tell which.")))
            print(PAR)
            type.type("When you blink, the figure is gone. The sun is rising. Was it a dream?")
        print(PAR)
        type.type(yellow(bright("Something about that encounter will stay with you forever.")))
        print(PAR)

        print(PAR)
        return
    def social_encounter(self):
        # EVENT: Someone important approaches and you need to make a good impression
        # EFFECTS: Breath Mints = $50 (consumed); Expensive Cologne = $100 (consumed);
        #          otherwise lose 3 sanity from humiliation
        # Breath Mints or Expensive Cologne help with social situations

        # T4 — auto-triggers (legendary, no choice)
        if self.has_item("King of the Road"):
            type.type(cyan(bright("King of the Road")) + " enters. Conversations stop. Every person in the vicinity wants to be you or know you.")
            print(PAR)
            type.type("The interaction goes perfectly. It always does, now.")
            self.restore_sanity(10)
            self.change_balance(random.randint(100, 300))
            return

        # T3 — auto-triggers
        if self.has_item("Master of Games"):
            type.type("The " + cyan(bright("Master of Games")) + " is at work. Charming, wealthy, impossible to refuse.")
            print(PAR)
            type.type("Every social vector closes in your favor.")
            self.restore_sanity(8)
            self.change_balance(random.randint(50, 200))
            return

        # ── PLAYER CHOICE: multiple T2/social items ──
        _social_options = [
            ("Intelligence Dossier", "Leverage secrets to control the conversation"),
            ("Fate Reader", "Read their fortune to disarm them"),
            ("Old Money Identity", "Let inherited wealth speak for itself"),
            ("Tear Gas", "Evacuate the room and walk out"),
        ]
        _available = [(n, d) for n, d in _social_options if self.has_item(n)]
        if len(_available) >= 2:
            _chosen = self._offer_item_choice(_available)
            if _chosen == "Intelligence Dossier":
                type.type("The " + cyan(bright("Intelligence Dossier")) + " has them in it. You know three things about this person they've never told anyone.")
                print(PAR)
                type.type("The conversation cuts straight to trust.")
                self.restore_sanity(5)
                self.change_balance(100)
                return
            elif _chosen == "Fate Reader":
                type.type("You read their fortune with the " + magenta(bright("Fate Reader")) + ". Their face goes pale. " + quote("How did you know that?"))
                print(PAR)
                type.type("NPC manipulation at its finest.")
                self.restore_sanity(5)
                self.change_balance(75)
                return
            elif _chosen == "Old Money Identity":
                type.type(magenta(bright("Old Money Identity")) + ". People defer before you speak. Waiters appear. Doors open.")
                print(PAR)
                type.type("You auto-win every social encounter just by existing.")
                self.restore_sanity(6)
                self.change_balance(100)
                return
            elif _chosen == "Tear Gas":
                type.type("You pop the " + magenta(bright("Tear Gas")) + ". Everyone evacuates. In the chaos, you walk out the back.")
                print(PAR)
                self.use_item("Tear Gas")
                self.restore_sanity(6)
                print(PAR)
                return

        # Single T2 item — auto-triggers
        if self.has_item("Tear Gas"):
            type.type("You pop the " + magenta(bright("Tear Gas")) + ". Everyone evacuates. In the chaos, you walk out the back.")
            print(PAR)
            self.use_item("Tear Gas")
            self.restore_sanity(6)
            print(PAR)
            return
        if self.has_item("Intelligence Dossier"):
            type.type("The " + cyan(bright("Intelligence Dossier")) + " has them in it. You know three things about this person they've never told anyone.")
            print(PAR)
            type.type("The conversation cuts straight to trust.")
            self.restore_sanity(5)
            self.change_balance(100)
            return
        if self.has_item("Fate Reader"):
            type.type("You read their fortune with the " + magenta(bright("Fate Reader")) + ". Their face goes pale. " + quote("How did you know that?"))
            print(PAR)
            type.type("NPC manipulation at its finest.")
            self.restore_sanity(5)
            self.change_balance(75)
            return
        if self.has_item("Old Money Identity"):
            type.type(magenta(bright("Old Money Identity")) + ". People defer before you speak. Waiters appear. Doors open.")
            print(PAR)
            type.type("You auto-win every social encounter just by existing.")
            self.restore_sanity(6)
            self.change_balance(100)
            return

        if self.has_item("Flask of Split Serum"):
            type.type("You crack the " + cyan(bright("Flask of Split Serum")) + " and the conversation seems to fork in your head.")
            print(PAR)
            type.type("Path one: impress them. Path two: understand them. You run both and pick the better line each time.")
            print(PAR)
            reward = random.randint(80, 170)
            type.type("By the end, you've got the deal and " + green(bright("${:,}".format(reward))) + ". " + quote("Call me first next time."))
            self.change_balance(reward)
            self.restore_sanity(3)
            print(PAR)
            return

        # COMBO: Gas Mask + Voice Soother = The Voice of God
        if self.has_item("Gas Mask") and self.has_item("Voice Soother"):
            type.type("The " + cyan(bright("Gas Mask")) + " distorts your " + cyan(bright("Voice Soother")) + "-enhanced voice into something deep, resonant, and inhuman.")
            print(PAR)
            type.type("You say " + quote("Excuse me.") + " People freeze. One person kneels. They heard a commandment from another dimension.")
            print(PAR)
            type.type("The crowd parts. Everything auto-succeeds.")
            print(PAR)
            self.restore_sanity(8)
            self.add_status("Voice of God")
            self.change_balance(random.randint(50, 150))
            print(PAR)
            return

        # COMBO: Deck of Cards + Dealer's Mercy = Dealer's Game
        if self.has_item("Deck of Cards") and (self.has_item("Dealer's Mercy") or self.has_item("Dealer's Grudge")):
            mercy = "Dealer's Mercy" if self.has_item("Dealer's Mercy") else "Dealer's Grudge"
            type.type("You pull out your " + cyan(bright("Deck of Cards")) + ". The " + cyan(bright(mercy)) + " pulses in your pocket.")
            print(PAR)
            type.type(quote("Care for a game?") + " you ask. The stranger looks at the cards. Something in your eyes makes them say yes.")
            print(PAR)
            type.type("Dealer's Game. You deal with the confidence of someone backed by supernatural authority. The cards obey.")
            print(PAR)
            if random.randrange(3) != 0:
                reward = random.randint(100, 500)
                type.type("You win. Of course you win. The stranger pays up — " + green(bright("${:,}".format(reward))) + " — and walks away shaking their head.")
                self.change_balance(reward)
                self.restore_sanity(8)
            else:
                type.type("The stranger wins. Impossible — but it happened. They tip their hat and vanish into the crowd.")
                print(PAR)
                type.type("You check your pocket. The " + cyan(bright(mercy)) + " is cold. Even the Dealer loses sometimes.")
                self.lose_sanity(3)
            print(PAR)
            return

        if self.has_item("Vintage Wine") and (self.has_item("Gambler's Chalice") or self.has_item("Overflowing Goblet")):
            chalice = "Overflowing Goblet" if self.has_item("Overflowing Goblet") else "Gambler's Chalice"
            self.use_item("Vintage Wine")
            type.type("You pour from the " + cyan(bright("Vintage Wine")) + " into the " + cyan(bright(chalice)) + ".")
            print(PAR)
            type.type("The ritual is absurd and perfect. The wine catches the light like something holy.")
            print(PAR)
            type.type("Whoever you meet today will give you something. They always do, when you look like someone who has everything.")
            print(PAR)
            type.type("The important-looking stranger stops. Stares. Then reaches into their coat.")
            print(PAR)
            gift = random.randint(200, 500)
            type.type(quote("I don't know why, but... take this.") + " They hand you " + green(bright("${:,}".format(gift))) + " and walk away looking lighter somehow.")
            self.change_balance(gift)
            self.restore_sanity(12)
            print(PAR)
            return

        # COMBO: Brass Knuckles + Gentleman's Charm = Civilized Violence
        if self.has_item("Brass Knuckles") and self.has_item("Gentleman's Charm"):
            type.type("A man insults you. You dab the " + cyan(bright("Gentleman's Charm")) + " cologne on your " + magenta(bright("Brass Knuckles")) + ".")
            print(PAR)
            type.type(quote("I'm terribly sorry about this,") + " you say with genuine politeness.")
            print(PAR)
            type.type("One punch. He goes down elegantly. The crowd applauds.")
            print(PAR)
            type.type("It was the classiest beatdown anyone has ever witnessed. His friends buy you a drink.")
            self.change_balance(50)
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Heirloom Set"):
            type.type("The stranger's eyes go straight to the " + cyan(bright("Heirloom Set")) + " — the pen in your pocket, the watch on your wrist, the quiet signal of inherited confidence.")
            print(PAR)
            type.type(quote("Old family money?") + " they ask, already half-convinced.")
            print(PAR)
            type.type("You neither confirm nor deny. Turns out that is exactly the right answer.")
            print(PAR)
            reward = random.randint(120, 260)
            type.type("They press a card and " + green(bright("${:,}".format(reward))) + " into your hand. " + quote("For your time. Let's talk again soon."))
            self.change_balance(reward)
            self.restore_sanity(8)
            print(PAR)
            return

        if self.has_item("Power Move Kit"):
            type.type("You flick open the lighter from the " + cyan(bright("Power Move Kit")) + ", let the flame hang for a beat, then offer a cigar like you do this every day.")
            print(PAR)
            type.type("The whole conversation changes shape instantly. Slower. Smoother. More expensive.")
            print(PAR)
            reward = random.randint(90, 180)
            type.type("By the time the cigar burns halfway down, they've called you " + quote("the kind of person worth knowing") + " and slipped you " + green(bright("${:,}".format(reward))) + ".")
            self.change_balance(reward)
            self.restore_sanity(6)
            print(PAR)
            return

        if self.has_item("Animal Magnetism"):
            type.type("The " + cyan(bright("Animal Magnetism")) + " hits before your words do. A nearby dog stops pulling at its leash. A stranger turns toward you like they were already listening.")
            print(PAR)
            type.type("This should be unsettling. Instead, it feels effortless. Like charisma with a scent trail.")
            print(PAR)
            reward = random.randint(70, 140)
            type.type("The conversation goes perfectly. Even the dog seems charmed. The stranger leaves you with " + green(bright("${:,}".format(reward))) + " and an oddly warm handshake.")
            self.change_balance(reward)
            self.restore_sanity(7)
            print(PAR)
            return

        if self.has_item("Golden Watch") or self.has_item("Sapphire Watch"):
            watch = "Sapphire Watch" if self.has_item("Sapphire Watch") else "Golden Watch"
            type.type("The stranger's eyes flick to the " + cyan(bright(watch)) + " on your wrist and stay there a beat too long.")
            print(PAR)
            if watch == "Sapphire Watch":
                type.type(quote("Oh. I didn't realize you were that kind of client.") + " Their posture changes instantly. The whole conversation upgrades itself around you.")
                reward = random.randint(130, 240)
                self.restore_sanity(7)
            else:
                type.type(quote("That's a serious watch.") + " They assume success, discipline, old money, or some convincing imitation of all three.")
                reward = random.randint(80, 170)
                self.restore_sanity(4)
            print(PAR)
            type.type("By the time they leave, you've got a card, a promise to call, and " + green(bright("${:,}".format(reward))) + " for lunch " + quote("next time you talk business."))
            self.change_balance(reward)
            self.update_golden_watch_durability()
            print(PAR)
            return

        if self.has_item("Delight Indicator") or self.has_item("Delight Manipulator"):
            gauge = "Delight Manipulator" if self.has_item("Delight Manipulator") else "Delight Indicator"
            type.type("Before you say a word, you glance at the " + cyan(bright(gauge)) + ".")
            print(PAR)
            if gauge == "Delight Manipulator":
                type.type("The reading spikes at the exact moment you smile. You tilt the dial with your thumb and watch their shoulders drop half an inch.")
                print(PAR)
                type.type("Now the conversation has a tailwind. Warmth. Curiosity. Easy laughter. Nothing forced enough to feel like cheating. Almost nothing.")
                reward = random.randint(110, 210)
                self.restore_sanity(6)
            else:
                type.type("It gives you what you needed: nervous, eager to impress, secretly relieved you spoke first.")
                print(PAR)
                type.type("Armed with that tiny emotional map, you guide the conversation away from danger and straight into rapport.")
                reward = random.randint(60, 130)
                self.restore_sanity(3)
            print(PAR)
            type.type("You part on unusually good terms, with " + green(bright("${:,}".format(reward))) + " in your pocket and the distinct sense that you just out-read a whole human being.")
            self.change_balance(reward)
            self.update_delight_indicator_durability()
            print(PAR)
            return

        if self.has_item("Twin's Locket") or self.has_item("Mirror of Duality"):
            locket = "Mirror of Duality" if self.has_item("Mirror of Duality") else "Twin's Locket"
            type.type("Your fingers brush the " + cyan(bright(locket)) + " before you speak. The metal warms, and suddenly the stranger seems doubled.")
            print(PAR)
            if locket == "Mirror of Duality":
                type.type("One version of them smiles with polished confidence. The other is tired, lonely, desperate to be understood. You answer the second person and ignore the first.")
                print(PAR)
                type.type("The conversation becomes unnervingly intimate in under a minute. By the end, they're thanking you for seeing them correctly.")
                reward = random.randint(120, 220)
                self.restore_sanity(7)
            else:
                type.type("The " + cyan(bright("Twin's Locket")) + " gives you a flash of contradiction: practiced confidence over genuine nerves. You speak gently to the nerves and watch the whole interaction soften.")
                reward = random.randint(70, 140)
                self.restore_sanity(4)
            print(PAR)
            type.type("When they leave, you've got " + green(bright("${:,}".format(reward))) + " and the odd feeling that you just negotiated with a public self and a private one at the same time.")
            self.change_balance(reward)
            self.update_twins_locket_durability()
            print(PAR)
            return

        if self.has_item("Dirty Old Hat") or self.has_item("Unwashed Hair"):
            hat = "Unwashed Hair" if self.has_item("Unwashed Hair") else "Dirty Old Hat"
            type.type("The stranger starts with the sort of careful politeness people use on someone they think has had a harder week than they have.")
            print(PAR)
            type.type("Then they notice the " + cyan(bright(hat)) + ". Whatever impression they formed, it works in your favor.")
            print(PAR)
            if hat == "Unwashed Hair":
                type.type(quote("You look like you know how this city really works.") + " They trust grime faster than polish. You file that fact away.")
                reward = random.randint(70, 140)
                self.restore_sanity(4)
            else:
                type.type(quote("You seem honest.") + " It is a ridiculous conclusion, but people believe strange things about old hats.")
                reward = random.randint(40, 90)
                self.restore_sanity(2)
            print(PAR)
            type.type("They slip you " + green(bright("${:,}".format(reward))) + " and a useful tip before leaving. Looking broke keeps paying weird dividends.")
            self.change_balance(reward)
            self.update_dirty_old_hat_durability()
            print(PAR)
            return

        if self.has_item("Worn Gloves") or self.has_item("Velvet Gloves"):
            gloves = "Velvet Gloves" if self.has_item("Velvet Gloves") else "Worn Gloves"
            type.type("Your handshake, firm through " + cyan(bright(gloves)) + ", seals the deal before you speak.")
            print(PAR)
            if gloves == "Velvet Gloves":
                type.type("The velvet touch reads like old-money confidence. They start negotiating against themselves before you even ask.")
                self.change_balance(random.randint(110, 220))
                self.restore_sanity(4)
            else:
                type.type("Something about a gloved hand makes people trust you. And sign faster.")
                self.change_balance(random.randint(50, 150))
                self.restore_sanity(2)
            self.update_worn_gloves_durability()
            print(PAR)
            return

        type.type("Someone important-looking approaches your car. They seem friendly, but you're suddenly aware of... yourself.")
        print(PAR)
        type.type("When's the last time you showered? How's your breath?")
        print(PAR)
        
        if self.has_item("Breath Mints"):
            type.type("You quickly pop a " + magenta(bright("Breath Mint")) + " before they get close.")
            print(PAR)
            type.type("Minty fresh! You greet them with confidence.")
            print(PAR)
            type.type("They turn out to be a philanthropist who gives you " + green(bright("$50")) + " for being so friendly.")
            self.change_balance(50)
            self.use_item("Breath Mints")
        elif self.has_item("Expensive Cologne"):
            type.type("You spritz some " + magenta(bright("Expensive Cologne")) + " on yourself.")
            print(PAR)
            type.type("Now you smell like money. Fake it till you make it.")
            print(PAR)
            type.type("They're impressed by your style and give you " + green(bright("$100")) + " along with their business card.")
            self.change_balance(100)
            self.use_item("Expensive Cologne")
        elif self.has_item("Deck of Cards"):
            type.type("You pull out your " + cyan(bright("Deck of Cards")) + " and fan them smoothly between your fingers.")
            print(PAR)
            type.type(quote("Oh, you play?") + " they ask. Their whole demeanor changes.")
            print(PAR)
            type.type("You deal a quick hand right on the hood of your car. Two strangers sharing cards in a parking lot. Somehow it works.")
            print(PAR)
            winnings = random.randint(20, 60)
            type.type("They lose gracefully and press " + green(bright("$" + str(winnings))) + " into your palm as they leave. " + quote("Best meeting I've had all week."))
            self.change_balance(winnings)
            self.restore_sanity(5)
        elif self.has_item("Necronomicon"):
            type.type("The important-looking stranger gets close enough to see what's in your lap. Their eyes fix on the " + cyan(bright("Necronomicon")) + ".")
            print(PAR)
            type.type(quote("Is that... is that what I think it is?"))
            print(PAR)
            type.type("They're a collector. A professor. Someone who has spent decades chasing things that shouldn't exist.")
            print(PAR)
            type.type("Their hands are shaking slightly.")
            print(PAR)
            type.type(quote("I'll give you two thousand dollars for it. Right now. Cash."))
            print(PAR)
            answer = ask.yes_or_no("Sell the Necronomicon for $2,000? ")
            if answer == "yes":
                type.type("You hand it over. They clutch it like a holy relic and practically sprint to their car.")
                print(PAR)
                type.type("Two thousand dollars lands in your hand. You feel lighter. Slightly.")
                self.change_balance(2000)
                self.use_item("Necronomicon")
                self.restore_sanity(5)
            else:
                type.type("You shake your head. " + quote("It's not for sale."))
                print(PAR)
                type.type("They look devastated. They leave their card anyway. You don't call.")
                print(PAR)
                type.type("The book seems heavier now. More present. Like it heard the offer and made a note of it.")
                self.lose_sanity(5)
        elif self.has_item("Gentleman's Charm"):
            type.type("The " + cyan(bright("Gentleman's Charm")) + " — silk handkerchief, expensive cologne, cufflinks that catch the light.")
            print(PAR)
            type.type("You straighten your collar and smile. Something about the smile — the bearing, the sheer absurd confidence — short-circuits their entire plan.")
            print(PAR)
            type.type(quote("Who WAS that?") + " they mutter as you walk away.")
            print(PAR)
            type.type("You leave with $200 and an open invitation to their next party.")
            self.change_balance(200)
            self.restore_sanity(6)
        else:
            type.type("You try to be friendly, but they wrinkle their nose and quickly make an excuse to leave.")
            print(PAR)
            type.type("That was humiliating.")
            self.lose_sanity(3)
        print(PAR)

        print(PAR)
        return
    def caught_fishing(self):
        # EVENT: Park near a river with fish swimming
        # EFFECTS: Fishing Line = 67% chance heal 20 HP + 3 sanity (consumed);
        #          otherwise just watch fish hungrily
        # Fishing Line lets you catch fish
        type.type("You park near a river. The water is clear, and you can see fish swimming lazily beneath the surface.")
        print(PAR)
        
        # Animal Whistle lets you befriend a fish
        if self.has_item("Animal Whistle") and not self.has_companion("Bubbles"):
            type.type("The " + magenta(bright("Animal Whistle")) + " resonates with the water. The fish stop swimming and rise to the surface.")
            print(PAR)
            type.type("One particularly large, golden koi swims right up to you. It splashes, then opens its mouth - like it's talking.")
            print(PAR)
            type.type("You dip your hand in the water. The koi nuzzles your palm. It's... following you?")
            print(PAR)
            type.type("The koi leaps into a bucket you didn't realize you had. Magic is weird.")
            print(PAR)
            type.type("You've befriended a fish. You decide to call it " + cyan(bright("Bubbles")) + ".")
            print(PAR)
            type.type("Bubbles will travel with you in a perpetually full bucket. Don't ask how it works.")
            self.add_companion("Bubbles", "Koi Fish")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.restore_sanity(5)
            print(PAR)
            return
        
        if self.has_item("Fishing Line"):
            type.type("You have " + magenta(bright("Fishing Line")) + "! Time to try your luck.")
            print(PAR)
            type.type("You fashion a makeshift rod from a branch, attach the line, and cast out.")
            print(PAR)
            if random.randrange(3) == 0:
                type.type("After an hour of waiting... nothing. The fish aren't biting today.")
                print(PAR)
                type.type("The line got tangled and snapped. Frustrating.")
            else:
                type.type("You feel a tug! You pull hard, and land a decent-sized bass!")
                print(PAR)
                type.type("Fresh fish for dinner. You feel accomplished.")
                self.heal(20)
                self.restore_sanity(3)
            self.use_item("Fishing Line")
        else:
            type.type("You watch the fish swim by, tantalizingly close. If only you had something to catch them with...")
            print(PAR)
            type.type("Your stomach rumbles.")
        print(PAR)

        print(PAR)
        return
    def robbery_attempt(self):
        # EVENT: Someone tries to break into your car at night
        # EFFECTS: Padlock protects (NOT consumed); Pocket Knife scares them;
        #          otherwise lose $50-200
        # COMPANION INTEGRATION: Lucky/protection companion scares off thief, danger_warning companions alert you
        type.type("There's someone trying to break into your car!")
        print(PAR)
        
        if self.has_item("Street Fighter Set"):
            type.type("Word spreads about the " + magenta(bright("Street Fighter Set")) + ". Nobody picks a fight with you anymore.")
            print(PAR)
            type.type("The thief sees you. Sees what you're capable of. Thinks twice. Walks away.")
            self.restore_sanity(5)
            return
        
        if self.has_item("Road Warrior Armor"):
            type.type("The robber looks at the " + cyan(bright("Road Warrior Armor")) + ", at the weapon components visible on the harness, then back at you.")
            print(PAR)
            type.type("They leave. Without a word. Wisely.")
            self.restore_sanity(8)
            return
        if self.has_item("Ghost Protocol"):
            type.type("The robber approaches. " + cyan(bright("Ghost Protocol")) + " makes you... unfocusable. They can't remember why they walked over.")
            print(PAR)
            type.type("They drift away, confused. You wave.")
            self.restore_sanity(5)
            return
        if self.has_item("Assassin's Kit"):
            type.type("You hold up the " + cyan(bright("Assassin's Kit")) + " — both components visible. Blade. Spray.")
            print(PAR)
            type.type("The math is immediate. They run.")
            self.restore_sanity(5)
            return
        if self.has_item("Sneaky Peeky Goggles") or self.has_item("Sneaky Peeky Shades"):
            lenses = "Sneaky Peeky Goggles" if self.has_item("Sneaky Peeky Goggles") else "Sneaky Peeky Shades"
            type.type("Through your " + cyan(bright(lenses)) + ", you spot the thief before they spot you. The lenses reveal their approach angle, their weapon hand, everything.")
            print(PAR)
            type.type("You calmly walk to the car from the other side. The thief never knew you were there.")
            self.restore_sanity(4)
            print(PAR)
            return
        # COMPANION: Protection check first
        protector = self._lists.has_companion_with_bonus(self, "protection")
        if protector and self.get_companion(protector)["status"] == "alive":
            comp_type = self.get_companion(protector).get("type", "")
            if "Dog" in comp_type:
                type.type(bright(protector) + " erupts into ferocious barking. Deep, loud, terrifying.")
                print(PAR)
                type.type("The thief looks in the window and sees teeth. Lots of teeth.")
            else:
                type.type(bright(protector) + " goes absolutely berserk inside the car, making enough noise to wake the dead.")
            print(PAR)
            type.type("The would-be thief sprints away like they've seen a ghost.")
            print(PAR)
            type.type(green(protector + " scared off the thief! Guardian of the car."))
            self.pet_companion(protector)
            self.restore_sanity(3)
        elif self.has_item("Padlock"):
            type.type("But you secured everything with your " + magenta(bright("Padlock")) + "!")
            print(PAR)
            type.type("The thief struggles with it for a minute, then gives up and runs off.")
            print(PAR)
            type.type("Close call. The padlock saved you.")
            self.restore_sanity(6)
        elif self.has_item("Brass Knuckles") and self.has_item("Gentleman's Charm"):
            type.type("You dab the " + cyan(bright("Gentleman's Charm")) + " cologne onto your " + cyan(bright("Brass Knuckles")) + ".")
            print(PAR)
            type.type(quote("I'm terribly sorry about this,") + " you say with genuine politeness.")
            print(PAR)
            type.type("You punch him once. He goes down elegantly. The crowd applauds.")
            print(PAR)
            type.type("It was the classiest beatdown anyone has ever witnessed.")
            print(PAR)
            self.change_balance(50)
            self.add_status("The Gentleman")
            type.type(green("You win the confrontation. +$50 from impressed bystanders."))
            self.restore_sanity(5)
        elif self.has_item("Brass Knuckles"):
            type.type("You spin around and face the thief, fist raised.")
            print(PAR)
            type.type("The brass knuckles catch the afternoon light. The thief gets a very clear look at them.")
            print(PAR)
            type.type("He reassesses his life choices in real time and takes off running.")
            print(PAR)
            type.type("Your stuff is safe. Your hand barely even moved.")
            self.restore_sanity(5)
        elif self.has_item("Shiv"):
            type.type("You whip out your " + cyan(bright("Shiv")) + " and hold it low, blade catching the light.")
            print(PAR)
            type.type(quote("You really want to do this?"))
            print(PAR)
            type.type("The thief freezes, eyes locked on the makeshift blade. He backs away slowly, hands up.")
            print(PAR)
            type.type("Without another word, he turns and disappears down the street. Coward.")
            print(PAR)
            type.type("Your car is safe. The shiv worked its ugly magic.")
            self.restore_sanity(4)
        elif self.has_item("Pocket Knife"):
            type.type("You grab your " + magenta(bright("Pocket Knife")) + " and brandish it!")
            print(PAR)
            type.type(quote("Back off!"))
            print(PAR)
            type.type("The thief sees the blade glinting and decides you're not worth the trouble. They bolt.")
        else:
            loss = random.randint(50, 200)
            type.type("Before you can react, they grab some of your stuff and run!")
            print(PAR)
            type.type("You lost " + green(bright("${:,}".format(loss))) + " worth of cash!")
            self.change_balance(-loss)
        print(PAR)

        print(PAR)
        return
    def photo_opportunity(self):
        # EVENT: Something beautiful happens that's worth capturing
        # EFFECTS: Disposable Camera = 5 sanity (10% chance consumed);
        #          otherwise 2 sanity from memory alone
        # Disposable Camera captures a moment
        type.type("You look through your windshield and something incredible catches your eye - a double rainbow, a deer and its fawn, the most beautiful scene you've ever seen.")
        print(PAR)
        
        if self.has_item("Disposable Camera"):
            type.type("You grab your " + magenta(bright("Disposable Camera")) + " and start snapping!")
            print(PAR)
            type.type("Click. Click. Click. You capture the moment forever.")
            print(PAR)
            type.type("When you develop these someday, they'll be worth remembering.")
            self.restore_sanity(5)
            if random.randrange(10) == 0:
                type.type("You got the last shot on the roll. Camera's done.")
                self.use_item("Disposable Camera")
        else:
            type.type("You try to memorize every detail. But memories fade.")
            print(PAR)
            type.type("If only you had a camera...")
            self.restore_sanity(2)
        print(PAR)

        print(PAR)
        return
    def classy_encounter(self):
        # EVENT: A rich person asks for directions
        # EFFECTS: Leather Gloves/Silk Handkerchief/Gold Chain/Pocket Watch = $100-300 tip;
        #          otherwise ignored rudely
        # Leather Gloves, Silk Handkerchief, Gold Chain help impress
        type.type("A fancy car pulls up next to yours. The window rolls down, revealing someone in expensive clothes.")
        print(PAR)
        type.type(quote("Excuse me, could you direct me to the casino?"))
        print(PAR)
        
        has_class = (self.has_item("Leather Gloves") or self.has_item("Silk Handkerchief") or 
                     self.has_item("Gold Chain") or self.has_item("Antique Pocket Watch") or
                     self.has_item("Gentleman's Charm") or self.has_item("Aristocrat's Touch") or
                     self.has_item("Fancy Cigars") or self.has_item("Vintage Wine") or
                     self.has_item("Worn Gloves") or self.has_item("Velvet Gloves"))
        
        if has_class:
            if self.has_item("Aristocrat's Touch"):
                type.type("You lean slightly toward them. Old money. They can tell.")
                print(PAR)
                type.type("The way you hold yourself. The way you don't explain yourself. The quiet certainty that everything is, and always has been, under control.")
                print(PAR)
                type.type(quote("Good lord. I'm sorry to have troubled you."))
                print(PAR)
                tip = random.randint(400, 800)
                type.type("They hand you " + green(bright("${:,}".format(tip))) + " as if they owe you something. They drive off without another word.")
                self.change_balance(tip)
                self.restore_sanity(12)
                print(PAR)
                return
            elif self.has_item("Gentleman's Charm"):
                type.type("You give them your full attention. The cufflinks catch the light at exactly the right moment.")
                print(PAR)
                type.type("Their eyes flick down, then back up. Something shifts.")
                print(PAR)
                type.type(quote("You know, I think I'm going to get your card. In case I'm ever in the area again."))
                print(PAR)
                tip = random.randint(200, 500)
                type.type("They hand you " + green(bright("${:,}".format(tip))) + " and drive off looking slightly dazed.")
                self.change_balance(tip)
                self.restore_sanity(10)
                print(PAR)
                return
            elif self.has_item("Silk Handkerchief"):
                type.type("You dab your brow with your " + magenta(bright("Silk Handkerchief")) + " in a refined manner.")
            elif self.has_item("Antique Pocket Watch"):
                type.type("You casually check your " + magenta(bright("Antique Pocket Watch")) + ".")
            elif self.has_item("Leather Gloves"):
                type.type("You adjust your " + magenta(bright("Leather Gloves")) + " with casual elegance.")
            elif self.has_item("Velvet Gloves"):
                type.type("You smooth your " + cyan(bright("Velvet Gloves")) + " and offer directions like you're directing staff at your own gala.")
                print(PAR)
                type.type(quote("I knew it. Old money."))
                tip = random.randint(200, 380)
                type.type("They press " + green(bright("${:,}".format(tip))) + " into your hand before you even finish the route.")
                self.change_balance(tip)
                self.restore_sanity(8)
                self.update_worn_gloves_durability()
                print(PAR)
                return
            elif self.has_item("Worn Gloves"):
                type.type("You tug on your " + cyan(bright("Worn Gloves")) + " and gesture with practical confidence. It reads as competence more than class.")
                print(PAR)
                tip = random.randint(110, 240)
                type.type("They nod, trust the directions, and tip you " + green(bright("${:,}".format(tip))) + " for being unexpectedly solid.")
                self.change_balance(tip)
                self.restore_sanity(4)
                self.update_worn_gloves_durability()
                print(PAR)
                return
            elif self.has_item("Fancy Cigars"):
                type.type("You produce a " + cyan(bright("Fancy Cigar")) + " and offer one across.")
                print(PAR)
                type.type("They take it. Light it. Breathe in.")
                print(PAR)
                type.type(quote("Cuban?"))
                print(PAR)
                type.type("You shrug as if to say: naturally.")
            elif self.has_item("Vintage Wine"):
                type.type("You mention the " + cyan(bright("Vintage Wine")) + " you've been saving for the right occasion.")
                print(PAR)
                type.type(quote("1987? You're carrying a '87? In your car?"))
                print(PAR)
                type.type("They look at you differently now. The way people look at someone who understands something they thought only they understood.")
            else:
                type.type("Your " + magenta(bright("Gold Chain")) + " catches their eye.")
            print(PAR)
            type.type("They look at you with newfound respect.")
            print(PAR)
            type.type(quote("Ah, a person of taste! Here, for your trouble."))
            print(PAR)
            tip = random.randint(100, 300)
            type.type("They hand you " + green(bright("${:,}".format(tip))) + " and drive off.")
            self.change_balance(tip)
            self.restore_sanity(8)
        else:
            type.type("You point them in the right direction. They barely acknowledge you before driving off.")
            print(PAR)
            type.type("Not even a thank you. Typical rich people.")
        print(PAR)

        print(PAR)
        return
    def wine_and_dine(self):
        # EVENT: Bond with another car-dweller around a campfire
        # CONDITION: Requires Vintage Wine or Silver Flask
        # EFFECTS: Vintage Wine = 10 sanity + 10 HP (consumed); Silver Flask = 5 sanity
        # Vintage Wine or Silver Flask for special occasions
        if not self.has_item("Vintage Wine") and not self.has_item("Silver Flask"):
            self.day_event()
            return
        
        type.type("You step out of your car and meet someone interesting - another car-dweller, sharing stories around a small campfire.")
        print(PAR)
        
        if self.has_item("Vintage Wine"):
            type.type("You pull out your " + magenta(bright("Vintage Wine")) + ".")
            print(PAR)
            type.type(quote("1987? You've been holding onto this?"))
            print(PAR)
            type.type("You share the bottle, swapping tales of better days and worse ones.")
            print(PAR)
            type.type("By the time it's empty, you've made a real friend.")
            self.use_item("Vintage Wine")
            self.restore_sanity(10)
            self.heal(10)
        elif self.has_item("Silver Flask"):
            type.type("You offer a swig from your " + magenta(bright("Silver Flask")) + ".")
            print(PAR)
            type.type("They accept gratefully. You share drinks and stories until the fire dies down.")
            self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def cigar_circle(self):
        # EVENT: Bond with locals at a barbershop using cigars
        # CONDITION: Requires Fancy Cigars item
        # EFFECTS: 5 sanity + 5 HP, get local knowledge (consumed)
        # Fancy Cigars for bonding
        if not self.has_item("Fancy Cigars"):
            self.day_event()
            return
        
        type.type("You step out of your car and find a group of older men sitting outside a barbershop, talking politics and sports.")
        print(PAR)
        type.type("One of them eyes you suspiciously. You're clearly not from around here.")
        print(PAR)
        type.type("You pull out your " + magenta(bright("Fancy Cigars")) + " and offer them around.")
        print(PAR)
        type.type(quote("Cuban? Well, well. Maybe you're alright after all."))
        print(PAR)
        type.type("You spend the afternoon smoking and talking. They give you tips on where to park safely, where to find cheap food.")
        print(PAR)
        type.type("Local knowledge is priceless.")
        self.use_item("Fancy Cigars")
        self.restore_sanity(5)
        self.heal(5)
        print(PAR)

        print(PAR)
        return
    def ice_cream_truck(self):
        # EVENT: Ice cream truck driver gives you a free rocket pop
        # ONE-TIME: Only happens once (checks "Ice Cream Man" met status)
        # EFFECTS: Heal 15 HP, nostalgic moment
        # One-Time - positive event
        if self.has_met("Ice Cream Man"):
            self.day_event()
            return
        
        self.meet("Ice Cream Man")
        type.type("Is that... music? That familiar jingle that haunts every childhood summer?")
        print(PAR)
        type.type("An ice cream truck pulls up right next to your car. The driver, a heavyset man with a handlebar mustache, leans out the window.")
        print(PAR)
        type.type(quote("You look like you could use some ice cream, friend! First one's on the house!"))
        print(PAR)
        type.type("He hands you a rocket pop. You haven't had one since you were a kid.")
        print(PAR)
        type.type("It tastes like summer. Like childhood. Like things were simpler.")
        print(PAR)
        self.heal(15)
        type.type(quote("Keep your chin up! Life's too short not to have dessert!"))
        print(PAR)
        type.type("The ice cream truck drives away, its jingle fading into the distance.")
        print(PAR)

        print(PAR)
        return
    def kid_on_bike(self):
        # EVENT: A kid thinks living in a car is "cool"
        # ONE-TIME: Only happens once (checks "Kid on Bike" met status)
        # EFFECTS: Heal 5 HP from feeling validated
        # One-Time - random NPC
        if self.has_met("Kid on Bike"):
            self.day_event()
            return
        
        self.meet("Kid on Bike")
        type.type("A kid on a bike rides past your car, then stops. He circles back, staring at you with wide eyes.")
        print(PAR)
        type.type(quote("Whoa... do you LIVE in your car? That's so COOL!"))
        print(PAR)
        type.type("You're not sure 'cool' is the word you'd use, but okay.")
        print(PAR)
        type.type(quote("I wish I could live in a car! No bedtime, no vegetables, no homework! You're living the DREAM, mister!"))
        print(PAR)
        type.type("Before you can correct him, he pedals off, yelling about how he's going to tell his friends about the 'cool car guy.'")
        print(PAR)
        type.type("You feel... strangely validated?")
        print(PAR)
        self.heal(5)

        print(PAR)
        return
    def lost_tourist(self):
        # EVENT: Give directions to lost family, get tipped
        # ONE-TIME: Only happens once (checks "Lost Tourist" met status)
        # EFFECTS: Gain $20-50 tip
        # One-Time - helpful NPC
        if self.has_met("Lost Tourist"):
            self.day_event()
            return
        
        self.meet("Lost Tourist")
        type.type("A minivan pulls up next to you. The window rolls down to reveal a frazzled-looking family. ")
        type.type("Dad's driving, Mom's got a map upside down, and three kids are screaming in the back.")
        print(PAR)
        type.type(quote("Excuse me! We're trying to find the highway? Our GPS died three towns ago!"))
        print(PAR)
        if self.has_item("Rusty Compass") or self.has_item("Golden Compass"):
            compass = "Golden Compass" if self.has_item("Golden Compass") else "Rusty Compass"
            type.type("You pull out the " + cyan(bright(compass)) + ". The needle swings once, then settles with total confidence.")
            print(PAR)
            if compass == "Golden Compass":
                type.type("You don't just send them to the highway. You give them the clean route around construction, the fast gas station exit, and the one stretch of road where the kids will finally stop screaming because the view opens up.")
                tip = random.randint(60, 120)
                self.restore_sanity(5)
            else:
                type.type("You trace the turns in the air from instinct and magnetism both. Not perfect directions. Better: lived-in directions. The kind that actually get a family home.")
                tip = random.randint(35, 80)
                self.restore_sanity(3)
            print(PAR)
            type.type("The dad stares like you just translated fate itself.")
            print(PAR)
            type.type(quote("Take this. Seriously. You just saved our whole day."))
            print(PAR)
            type.type("He hands you " + green(bright("$" + str(tip))) + " before the van peels away in the right direction for once.")
            self.change_balance(tip)
            self.update_rusty_compass_durability()
            print(PAR)
            type.type("Good deed for the day: upgraded by navigation magic.")
            print(PAR)
            return
        type.type("You give them directions as best you can. The dad looks so relieved he might cry.")
        print(PAR)
        type.type(quote("Thank you so much! Here, take this-for your trouble!"))
        print(PAR)
        tip = random.randint(20, 50)
        type.type("He hands you " + green(bright("$" + str(tip))) + " before speeding off, kids still screaming.")
        self.change_balance(tip)
        print(PAR)
        type.type("Good deed for the day: done.")
        print(PAR)

    # ==========================================
    # SECRET EVENTS - CHEAP TIER  
    # ==========================================
    
        print(PAR)
        return
    def street_performer(self):
        # Everytime - random encounter
        variant = random.randrange(4)
        if variant == 0:
            type.type("A man with a guitar sits down near your car and starts playing. He's actually pretty good.")
            print(PAR)
            type.type("You listen for a while. When he finishes, you toss him a few bucks. He tips his hat and moves on.")
            self.change_balance(-random.randint(1, 5))
        elif variant == 1:
            type.type("A one-man-band contraption walks by-drums, harmonica, cymbals, the whole nine yards. The noise is incredible.")
            print(PAR)
            type.type("He plays for exactly three minutes, then disappears around the corner. What a strange morning.")
        elif variant == 2:
            type.type("A magician approaches your car window and does a card trick. You have no idea how he did it.")
            print(PAR)
            type.type(quote("Pick a card, any card!") + " he says. You pick the three of hearts.")
            print(PAR)
            type.type("He makes it disappear, reappear in his mouth, then reveals it was in your pocket the whole time.")
            print(PAR)
            type.type("Wait. How did he get it in your pocket?")
        else:
            type.type("A mime follows your car for three blocks. You finally shake him when you run a yellow light.")
            print(PAR)
            type.type("Mimes are weird.")
        print(PAR)

        print(PAR)
        return
    def homeless_network(self):
        # Conditional - only triggers if player has met multiple NPCs
        if not (self.has_met("Cowboy") or self.has_met("Ezekiel") or self.has_met("Betsy")):
            self.day_event()
            return
        
        if self.has_met("Homeless Network"):
            self.day_event()
            return
        
        self.meet("Homeless Network")
        type.type("A scruffy-looking man approaches your car. He's clearly homeless, but there's an intelligence in his eyes.")
        print(PAR)
        type.type(quote("Word on the street is you've been meeting some interesting folks. The cowboy. The preacher. Even that crazy cow."))
        print(PAR)
        type.type("He grins, showing missing teeth.")
        print(PAR)
        type.type(quote("We've got a network, you know. Us street folks. We share info. And some of that info might be useful to someone in your... unique situation."))
        print(PAR)
        type.type("He offers to tell you about a shortcut to the casino that avoids the main roads. Better for someone trying to stay under the radar.")
        print(PAR)
        answer = ask.yes_or_no("Pay him $50 for the info? ")
        if answer == "yes":
            self.change_balance(-50)
            type.type("He pockets the money and tells you about a back road that cuts travel time significantly.")
            print(PAR)
            type.type(quote("Good luck out there. We're all rooting for you."))
            self.add_item("Secret Route Map")
        else:
            type.type("He shrugs. " + quote("Your loss. The offer stands if you change your mind."))
        if self.has_item("Deck of Cards"):
            print(PAR)
            type.type("Before he walks off you pull out your " + cyan(bright("Deck of Cards")) + ".")
            print(PAR)
            type.type("He stops. Looks at the deck. Looks at you.")
            print(PAR)
            type.type("You sit down on the curb and deal a hand. For an hour, you're not a man trying to make a million dollars. You're just a guy playing cards.")
            print(PAR)
            type.type("He beats you three games straight. He has the satisfied smile of someone who is still very good at something.")
            self.restore_sanity(6)
        if self.has_item("Outdoor Shield"):
            print(PAR)
            type.type("You hand over your spare " + cyan(bright("Outdoor Shield")) + " supplies.")
            print(PAR)
            type.type("The man takes them with genuine gratitude. " + quote("This'll make a real difference tonight. Thank you."))
            self.restore_sanity(4)
        elif self.has_item("Cool Down Kit"):
            print(PAR)
            type.type("The summer heat is brutal. You pass him the " + cyan(bright("Cool Down Kit")) + ".")
            print(PAR)
            type.type(quote("You didn't have to do that,") + " he says, eyes wide. You shrug.")
            self.use_item("Cool Down Kit")
            self.restore_sanity(4)
        print(PAR)

    # ==========================================
    # NEW MODEST DAY EVENTS - One-Time
    # ==========================================
    
        print(PAR)
        return
    def the_photographer(self):
        # One-Time - documentary
        if self.has_met("The Photographer"):
            self.day_event()
            return
        
        self.meet("The Photographer")
        type.type("A woman with a professional camera approaches your car, clearly excited.")
        print(PAR)
        type.type(quote("Hi! I'm doing a photo documentary on alternative lifestyles. Living in your car is EXACTLY the kind of story I'm looking for!"))
        print(PAR)
        type.type("She's practically bouncing with enthusiasm.")
        print(PAR)
        type.type(quote("Would you mind if I took some photos? I can pay you for your time!"))
        print(PAR)
        answer = ask.yes_or_no("Allow the photoshoot? ")
        if answer == "yes":
            type.type("You pose with your wagon, trying to look dignified. She snaps dozens of photos.")
            print(PAR)
            type.type(quote("These are PERFECT! The lighting, the composition, the story they tell!"))
            print(PAR)
            type.type("She pays you " + green(bright("$200")) + " for your time.")
            self.change_balance(200)
            print(PAR)
            type.type(quote("If this gets published, you might be famous! In a niche art magazine, anyway."))
        else:
            type.type(quote("Oh. Okay. I understand, privacy is important."))
            print(PAR)
            type.type("She walks away, looking disappointed.")
        print(PAR)

        print(PAR)
        return
    def the_food_truck(self):
        # EVENT: Food truck owner gives you a free massive burrito
        # ONE-TIME: Only happens once (checks "Food Truck" met status)
        # EFFECTS: Heal 30 HP
        # One-Time - wholesome
        if self.has_met("Food Truck"):
            self.day_event()
            return
        
        self.meet("Food Truck")
        type.type("A food truck parks right next to your wagon. The smell of cooking meat is intoxicating.")
        print(PAR)
        type.type("The owner leans out the window and spots you.")
        print(PAR)
        type.type(quote("Hey! You been living in that car long? I see you parked here sometimes."))
        print(PAR)
        type.type("Before you can answer, he's already preparing something.")
        print(PAR)
        type.type(quote("Here. On the house. Everyone deserves a good meal."))
        print(PAR)
        type.type("He hands you a massive burrito, overflowing with everything good in the world.")
        print(PAR)
        type.type("It's the best thing you've eaten in months.")
        self.heal(30)
        print(PAR)
        type.type(quote("Come by anytime. We look out for each other around here."))
        print(PAR)

    # ==========================================
    # SECRET EVENTS - MODEST TIER
    # ==========================================
    
        print(PAR)
        return
    def further_interrogation(self):
        # EVENT: Red suit man returns with fake clipboard "from the government"
        # CHAIN: Part 2 of interrogation storyline
        # CONDITION: Met "Interrogator" and has "Further Interrogation" danger
        # EFFECTS: Removes current danger, adds "Even Further Interrogation" danger
        if not self.has_met("Interrogator") or not self.has_danger("Further Interrogation"):
            self.day_event()
            return

        self.lose_danger("Further Interrogation")
        self.add_danger("Even Further Interrogation")
        type.type("Through the windshield, a car is parked right in front of you again. ")
        type.type("Tired and concerned, you sit up. As you open the door and step out, ")
        type.type("you notice a man you've met before, in his bright red suit, once again peering into your trunk.")
        print(PAR)
        type.type("The man sees you, and walks up to you, with a clipboard in his hand.")
        print(PAR)
        type.type(space_quote("You. You're awake. Good. You see this clipboard? It says you can't be here."))
        type.type("You begin to read the paper on the clipboard. It's a message, written in Comic Sans.")
        print(PAR)
        type.type("It reads 'This offical message from the government and the military and the army says that you can't be here. ")
        type.type("That's right, you, the person reading this message right now, living on this land right here. ")
        type.type("It's not for you. It won't ever be for you. So, you can't live here. You need to move right now, or I'll be very very angry.'")
        print(PAR)
        type.type(space_quote("Did you read it?"))
        answer = ask.yes_or_no(space_quote("Did you? Read it?"))
        if answer == "yes":
            type.type(quote("Good, so you know that all these powerful people want yo- are demanding that you move from where you're currently living, right this instant! "))
            type.type(quote("I'd suggest you do so. I certainly wouldn't want to upset the government."))
            print(PAR)
        elif answer == "no":
            type.type(quote("You didn't read it? Come on, I worked so hard on it. You really should read a clipboard with words on it if someone asks you to. "))
            type.type(quote("Regardless, it says that you need to move! Or the consequences will be scary!"))
            print(PAR)
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 25 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print(PAR)
        return

    # DREAM SEQUENCES - MODEST TIER

        print(PAR)
        return
    def vending_machine_luck(self):
        type.type("You step out of your car and find a vending machine outside an abandoned gas station. The display is cracked, but the lights are still on.")
        print(PAR)
        type.type("You don't have any change, but you give it a hopeful kick anyway.")
        print(PAR)
        chance = random.randrange(4)
        if chance == 0:
            type.type("CLUNK. A candy bar falls out! It's only slightly expired.")
            print(PAR)
            type.type("You eat it anyway. Your standards have lowered significantly since this whole adventure started.")
            self.heal(5)
        elif chance == 1:
            type.type("CLUNK CLUNK CLUNK. A cascade of coins rattles out! Someone's quarters finally came home to roost.")
            amount = random.randint(3, 15)
            type.type(" You collect " + green(bright("$" + str(amount))) + " in loose change.")
            self.change_balance(amount)
        elif chance == 2:
            type.type("The machine groans, shudders, and then falls silent. You've killed it.")
            print(PAR)
            type.type("Add 'vending machine murderer' to your growing list of moral failures.")
        else:
            type.type("Nothing happens. The machine stares back at you, judging silently.")
            print(PAR)
            type.type("Even inanimate objects are disappointed in you now.")
        print(PAR)

        print(PAR)
        return
    def talking_to_yourself(self):
        type.type("You've been alone in this car for too long. You start talking to yourself.")
        print(PAR)
        type.type(quote("Hey, me. How's it going?"))
        print(PAR)
        type.type(quote("Oh, you know. Living the dream. Sleeping in a car. Gambling addiction. The usual."))
        print(PAR)
        type.type(quote("Cool, cool. Wanna play twenty questions?"))
        print(PAR)
        type.type(quote("I already know all your answers, idiot. We're the same person."))
        print(PAR)
        type.type("The conversation devolves into an argument about whose fault this all is. You both lose.")
        print(PAR)
        sanity_change = random.choice([-3, -2, 1, 2])
        if sanity_change > 0:
            type.type("Oddly, the self-deprecating banter makes you feel a little better.")
            self.restore_sanity(sanity_change)
        else:
            type.type("This probably isn't healthy.")
            self.lose_sanity(abs(sanity_change))
        print(PAR)

        print(PAR)
        return
    def wrong_number(self):
        type.type("Your phone buzzes from the passenger seat. You have a text from an unknown number.")
        print(PAR)
        messages = [
            quote("Hey babe, I left my keys at your place. Can you leave them under the mat?"),
            quote("This is your doctor. Your test results are in. Please call us immediately."),
            quote("We've been trying to reach you about your car's extended warranty."),
            quote("Grandma passed away. The funeral is Saturday."),
            quote("I know what you did. Meet me at the pier at midnight. Come alone.")
        ]
        type.type(random.choice(messages))
        print(PAR)
        type.type("You stare at your phone for a long moment, then remember you don't recognize this number at all.")
        print(PAR)
        answer = ask.yes_or_no("Reply anyway? ")
        if answer == "yes":
            type.type("You type back: " + quote("Wrong number, buddy."))
            print(PAR)
            chance = random.randrange(5)
            if chance == 0:
                type.type("They reply: " + quote("OMG I'm so sorry! Here's $10 for the trouble via cash app!"))
                print(PAR)
                type.type("Wait, that actually worked? You got " + green(bright("$10")) + "!")
                self.change_balance(10)
            else:
                type.type("They don't reply. Probably embarrassed.")
        else:
            type.type("You ignore it. Not your circus, not your monkeys.")
        print(PAR)

        print(PAR)
        return
    def cloud_watching(self):
        type.type("You lie on the hood of your car and stare at the clouds. It's surprisingly peaceful.")
        print(PAR)
        clouds = [
            "That one looks like a bunny. Or maybe a dog. Or a bunny-dog hybrid. A bunny-dog? A dog-bunny?",
            "That one definitely looks like the Dealer's face. Great, even the sky is judging you now.",
            "That one looks like a pile of money. Your brain really can't think about anything else, can it?",
            "That one looks like your ex. You try not to think about that too hard.",
            "That one looks like nothing. It's just a cloud. Not everything needs to be symbolic.",
            "That one looks like a middle finger. Nature is mocking you specifically."
        ]
        type.type(random.choice(clouds))
        print(PAR)
        type.type("After an hour of this, you feel strangely refreshed. Maybe doing nothing is underrated.")
        self.restore_sanity(random.choice([2, 3, 4]))
        print(PAR)

        print(PAR)
        return
    def car_alarm_symphony(self):
        if self.has_item("EMP Device"):
            type.type("You activate the " + cyan(bright("EMP Device")) + " just as the alarms start. A pulse ripples out.")
            print(PAR)
            type.type("Every car alarm in the radius sputters and dies. Silence returns immediately.")
            print(PAR)
            type.type("You sit back, smug. Technology bows to you.")
            self.restore_sanity(3)
            print(PAR)
            return
        type.type("Every car alarm in a five-block radius goes off simultaneously, jolting you upright in your seat.")
        print(PAR)
        type.type("BEEP BEEP BEEP HONK HONK WEEEOOOWEEEOO BEEP BEEP")
        print(PAR)
        type.type("You try to cover your ears, but it's no use. The symphony of chaos plays on.")
        print(PAR)
        type.type("After twenty agonizing minutes, they all stop at once. The silence is somehow worse.")
        print(PAR)
        self.lose_sanity(random.choice([1, 2, 3]))
        self.hurt(5)
        print(PAR)

    # CHEAP DAY EVENTS - Everytime

        print(PAR)
        return
    def fortune_cookie(self):
        type.type("You find an old fortune cookie in your glove compartment. It's from that Chinese place you went to... three months ago?")
        print(PAR)
        type.type("Against your better judgment, you crack it open.")
        print(PAR)
        fortunes = [
            quote("Your lucky numbers are 4, 8, 15, 16, 23, 42.") + " Helpful.",
            quote("A great opportunity will present itself soon.") + " Like that's ever happened.",
            quote("You will find what you seek in the last place you look.") + " Technically true for everything.",
            quote("Today is a good day to gamble.") + " They know you too well.",
            quote("Help! I'm trapped in a fortune cookie factory!") + " ...concerning.",
            quote("Your addiction will consume you.") + " That's... unusually specific.",
            quote("The Dealer remembers everything.") + " How does a fortune cookie know about the Dealer?!"
        ]
        type.type(random.choice(fortunes))
        print(PAR)
        type.type("The cookie itself is stale beyond recognition, but you eat it anyway. Waste not, want not.")
        print(PAR)

        print(PAR)
        return
    def street_musician(self):
        type.type("A street musician has set up shop near your parking spot. He's playing the saxophone.")
        print(PAR)
        type.type("He's... not great. But he's trying. Oh god, is he coming over here?")
        print(PAR)
        type.type("He stops right next to your window and launches into what you think is meant to be 'Careless Whisper.'")
        print(PAR)
        answer = ask.yes_or_no("Give him some money to make him go away? ")
        if answer == "yes":
            amount = random.randint(5, 15)
            if self.get_balance() >= amount:
                type.type("You hand him " + green(bright("$" + str(amount))) + ". He tips his hat and moves on to torture someone else.")
                self.change_balance(-amount)
                self._total_given_away += amount
                self.restore_sanity(2)
            else:
                type.type("You show him your empty wallet. He plays a sad trombone sound effect on his phone and walks away disappointed.")
        else:
            type.type("You close your eyes and pretend to be asleep. He plays louder. This goes on for forty-five minutes.")
            self.lose_sanity(3)
        print(PAR)

        print(PAR)
        return
    def roadkill_philosophy(self):
        type.type("Through your car window, you spot a dead possum on the side of the road. It makes you think about mortality.")
        print(PAR)
        type.type("We're all just possums, really. Going about our business until life runs us over with a metaphorical pickup truck.")
        print(PAR)
        type.type("Or maybe you're just sleep-deprived and reading too much into roadkill. That's also possible.")
        print(PAR)
        type.type("Either way, you feel strangely philosophical for the next hour.")
        self.restore_sanity(1)
        print(PAR)

    # MODEST DAY EVENTS - Everytime

        print(PAR)
        return
    def fancy_coffee(self):
        type.type("You head out from your car and treat yourself to a coffee from the fancy place downtown. The one with seventeen syllable drink names.")
        print(PAR)
        type.type(quote("I'll have a... uh... the brown one?"))
        print(PAR)
        type.type("The barista sighs the sigh of someone who went to art school for this.")
        print(PAR)
        cost = random.randint(8, 15)
        type.type("Your 'brown one' costs " + green(bright("$" + str(cost))) + ". That's absurd. You pay anyway.")
        self.change_balance(-cost)
        print(PAR)
        type.type("It's... actually really good. You feel temporarily sophisticated.")
        self.restore_sanity(3)
        self.heal(5)
        print(PAR)

        print(PAR)
        return
    def parking_ticket(self):
        if self.has_item("Dirty Old Hat") or self.has_item("Unwashed Hair"):
            hat = "Unwashed Hair" if self.has_item("Unwashed Hair") else "Dirty Old Hat"
            type.type("You return to your car to find a bright orange envelope under the wiper.")
            print(PAR)
            type.type("Then you notice a second note tucked beneath it. The parking officer must have gotten a better look at you after spotting the " + cyan(bright(hat)) + ".")
            print(PAR)
            if hat == "Unwashed Hair":
                type.type(quote("Official warning only. Please seek assistance.") + " The ticket itself has been voided. Apparently looking catastrophically broke activates a little mercy in the bureaucracy.")
                self.restore_sanity(4)
            else:
                type.type(quote("Move along by tonight and we forget this happened.") + " The hat makes you look less like a criminal and more like a man the city already defeated.")
                self.restore_sanity(2)
            self.update_dirty_old_hat_durability()
            print(PAR)
            return
        type.type("You return to your car to find a parking ticket on the windshield.")
        print(PAR)
        type.type("$75 for 'Overnight Parking in Non-Designated Area.' Also known as: existing while poor.")
        print(PAR)
        answer = ask.yes_or_no("Pay the ticket? ")
        if answer == "yes":
            if self.get_balance() >= 75:
                type.type("You grumble but pay the fine. Being a law-abiding citizen is expensive.")
                self.change_balance(-75)
            else:
                type.type("You can't afford it. The ticket goes in the glove compartment with the others.")
                self.add_danger("Unpaid Tickets")
        else:
            type.type("You crumple it up and throw it in the back seat. Future you's problem.")
            self.add_danger("Unpaid Tickets")
        print(PAR)

        print(PAR)
        return
    def found_phone(self):
        type.type("You find a smartphone on the ground next to your car. It's cracked but still working.")
        print(PAR)
        type.type("The lock screen shows 47 missed calls from 'Mom' and the battery is at 3%.")
        print(PAR)
        answer = ask.yes_or_no("Try to return it to the owner? ")
        if answer == "yes":
            type.type("You call 'Mom' back. She's very grateful and sends her son to pick it up.")
            print(PAR)
            type.type("He gives you " + green(bright("$50")) + " as a thank you. " + quote("You're a good person,") + " he says.")
            print(PAR)
            type.type("The praise feels strange. When's the last time someone called you good?")
            self.change_balance(50)
            self.restore_sanity(5)
        else:
            type.type("You pocket it. Maybe you can sell it later. You try not to think about the crying mom.")
            self.add_item("Found Phone")
            self.lose_sanity(2)
        print(PAR)

    # RICH DAY EVENTS - Everytime

        print(PAR)
        return
    def the_hitchhiker(self):
        # One-Time - Cheap tier
        if self.has_met("Hitchhiker"):
            self.day_event()
            return
        
        self.meet("Hitchhiker")
        type.type("You're pulling out of your parking spot when you see a young woman by the side of the road, thumb out. She looks tired. Desperate, even.")
        print(PAR)
        type.type("She sees your car slow down and her eyes light up with hope.")
        print(PAR)
        answer = ask.yes_or_no("Pick her up? ")
        if answer == "yes":
            type.type("You unlock the door. She slides in, smelling faintly of campfire smoke and bad decisions.")
            print(PAR)
            type.type(quote("Thank you SO much. I've been out here for hours. Name's Maya."))
            print(PAR)
            type.type("You drive her to the next town over. She talks the whole way-")
            type.type("about a boyfriend who left her stranded, about dreams of being a singer, ")
            type.type("about how she's going to make it big someday.")
            print(PAR)
            type.type("When you drop her off, she reaches into her bag.")
            print(PAR)
            type.type(quote("I don't have much, but take this. For luck."))
            print(PAR)
            type.type("She hands you a worn guitar pick with a four-leaf clover on it.")
            print(PAR)
            type.type("You got " + magenta(bright("Maya's Pick")) + "! It feels strangely warm in your pocket.")
            self.add_item("Maya's Pick")
            self.restore_sanity(5)
        else:
            type.type("You drive past. In the rearview mirror, you see her shoulders slump.")
            print(PAR)
            type.type("It was probably the safe choice. Probably.")
            self.lose_sanity(2)
        print(PAR)

        print(PAR)
        return
    def the_prophet(self):
        # One-Time - Modest tier
        if self.has_met("Street Prophet"):
            self.day_event()
            return
        
        self.meet("Street Prophet")
        type.type("You step out of your car and spot a man in tattered robes on a street corner, holding a cardboard sign that reads: 'THE END IS NIGH (FOR YOUR WALLET)'")
        print(PAR)
        type.type("He spots you and his eyes go wide.")
        print(PAR)

        if self.has_item("Eldritch Candle"):
            type.type("His gaze drops to the " + cyan(bright("Eldritch Candle")) + " poking out of your bag. His eyes go very wide.")
            print(PAR)
            type.type(quote("You need to leave. Right now. Do not ask questions."))
            print(PAR)
            type.type("You leave. Outside, on the steps where he was standing, you find $100.")
            print(PAR)
            type.type("You don't ask questions.")
            self.change_balance(100)
            self.restore_sanity(5)
            print(PAR)
            return

        if self.has_item("Binding Portrait"):
            type.type("He starts his pitch. Then he sees the " + cyan(bright("Binding Portrait")) + " under your arm.")
            print(PAR)
            type.type("He stares into it for a long time. Long enough that it gets uncomfortable.")
            print(PAR)
            type.type("Finally, he shakes himself and waves you closer. " + quote("No charge. Consider this... professional courtesy."))
            print(PAR)
            type.type("He gives you the full reading for free. Whatever he saw in that portrait, it changed his pricing policy.")
            print(PAR)
            prophecies_free = [
                quote("I see... a great victory! But beware the fifth hand after sunset. The Dealer's smile will mean danger."),
                quote("You will face a choice between wealth and wisdom. Choose wisely, for you cannot have both."),
                quote("The numbers 7, 11, and 21 will guide you. Or destroy you. Same difference, really."),
            ]
            type.type(random.choice(prophecies_free))
            self.restore_sanity(6)
            print(PAR)
            return

        if self.has_item("Oracle's Tome") or self.has_item("Gambler's Grimoire"):
            tome = "Oracle's Tome" if self.has_item("Oracle's Tome") else "Gambler's Grimoire"
            type.type("His sales pitch dies the second he spots the " + cyan(bright(tome)) + " tucked under your arm.")
            print(PAR)
            if tome == "Oracle's Tome":
                type.type(quote("Oh. You already brought the answer key."))
                print(PAR)
                type.type("The " + cyan(bright("Oracle's Tome")) + " falls open on its own. The pages rearrange themselves into a clean list of warnings, dates, and dealer tells.")
                print(PAR)
                type.type("The prophet reads over your shoulder instead of charging you. By the end, he's taking notes.")
                print(PAR)
                type.type(quote("Skip the smiling stranger. Trust the third invitation. Leave the table when your chest goes cold."))
                self.add_status("Lucky")
                self.restore_sanity(7)
            else:
                type.type("The " + cyan(bright("Gambler's Grimoire")) + " flips itself open and writes, " + quote("Local prophet: 83% confidence, 100% dramatic.") )
                print(PAR)
                type.type("He squints at the line, offended for exactly three seconds, then nods with professional respect.")
                print(PAR)
                type.type(quote("Sarcastic book. Good instincts, though. You should listen to it more than you listen to me."))
                self.restore_sanity(5)
            self.update_gamblers_grimoire_durability()
            print(PAR)
            return

        type.type(quote("YOU! Yes, YOU! I have foreseen your coming!"))
        print(PAR)
        type.type("Great. A crazy person who's noticed you specifically.")
        print(PAR)
        type.type(quote("The cards whisper to me, traveler. They speak of a gambler who sleeps in their chariot, who dances with fortune and tragedy alike!"))
        print(PAR)
        type.type("Okay, that's... actually pretty accurate.")
        print(PAR)
        type.type(quote("I offer you a prophecy! One glimpse into your possible future! For the low, low price of...") + " He squints at you, assessing. ")
        type.type(quote("Twenty bucks."))
        print(PAR)
        answer = ask.yes_or_no("Pay $20 for a prophecy? ")
        if answer == "yes":
            if self.get_balance() >= 20:
                self.change_balance(-20)
                print(PAR)
                type.type("He takes your money, closes his eyes, and begins to hum.")
                print(PAR)
                prophecies = [
                    quote("I see... a great victory! But beware the fifth hand after sunset. The Dealer's smile will mean danger."),
                    quote("You will face a choice between wealth and wisdom. Choose wisely, for you cannot have both."),
                    quote("There is a rabbit in your future. Do not trust the rabbit."),
                    quote("The numbers 7, 11, and 21 will guide you. Or destroy you. Same difference, really."),
                    quote("I see... I see... actually, I can't see anything. I'm making this up. But hey, twenty bucks is twenty bucks.")
                ]
                type.type(random.choice(prophecies))
                print(PAR)
                type.type("He opens his eyes and grins a toothless grin. " + quote("May fortune favor you, gambler. Or not. I'm a prophet, not a miracle worker."))
            else:
                type.type("You check your pockets. Twenty bucks is more than you can spare.")
                type.type(" The prophet sighs. " + quote("The universe provides for those who can afford it."))
        else:
            type.type("You politely decline. He shrugs and goes back to shouting at passersby.")
        print(PAR)

        print(PAR)
        return
    def the_gambler_ghost(self):
        # One-Time - Rich tier, spooky
        if self.has_met("Gambler Ghost"):
            self.day_event()
            return
        
        self.meet("Gambler Ghost")
        self.lose_sanity(random.choice([3, 4, 5]))
        type.type("You sit up in your car seat. Something feels... wrong.")
        print(PAR)
        type.type("You look in your rearview mirror and freeze.")
        print(PAR)
        type.type("There's a man in your back seat.")
        print(PAR)
        type.type("He's dressed in a vintage suit, the kind people wore in the 1920s. His face is pale. Too pale. And you can see right through him.")
        print(PAR)
        type.type(quote("Don't be alarmed,") + " he says, his voice like static. " + quote("I just wanted to talk to a fellow gambler."))
        print(PAR)
        type.type("You are VERY alarmed.")
        print(PAR)
        type.type(quote("I lost everything at this casino, you know. 1928. Bet my house, my car, my wife's jewelry. Lost it all on one hand."))
        print(PAR)
        type.type("He laughs, but there's no humor in it.")
        print(PAR)
        type.type(quote("They found me the next morning in the river. I've been here ever since, watching others make the same mistakes."))
        print(PAR)
        type.type("You don't know what to say. What DO you say to a ghost?")
        print(PAR)
        type.type(quote("You're different, though. I can see it. You might actually make it out."))
        print(PAR)
        type.type("He starts to fade.")
        print(PAR)
        type.type(quote("Just remember: the house always wins. Unless you know when to walk away."))
        print(PAR)
        type.type("And then he's gone. You don't sleep the rest of the night.")
        print(PAR)

        print(PAR)
        return
    def the_doppelganger(self):
        # One-Time - Doughman tier, very unsettling
        if self.has_met("Doppelganger"):
            self.day_event()
            return
        
        self.meet("Doppelganger")
        self.lose_sanity(random.choice([5, 6, 7]))
        type.type("You step out of your car in the casino parking lot and see yourself.")
        print(PAR)
        type.type("Not a mirror. Not a reflection. YOU. Standing about fifty feet away, staring back at you.")
        print(PAR)
        type.type("Same clothes. Same face. Same confused expression.")
        print(PAR)
        type.type("You blink. Your double blinks.")
        print(PAR)
        type.type("You take a step forward. It takes a step forward.")
        print(PAR)
        type.type("You wave. It waves.")
        print(PAR)
        if self.has_item("Twin's Locket") or self.has_item("Mirror of Duality"):
            locket = "Mirror of Duality" if self.has_item("Mirror of Duality") else "Twin's Locket"
            type.type("The " + cyan(bright(locket)) + " snaps open on its own.")
            print(PAR)
            if locket == "Mirror of Duality":
                type.type("For a split second, you see two doubles instead of one: the gambler who kept going, and the person who could still leave. The false smile lands on the wrong one.")
                print(PAR)
                type.type("That is somehow enough. When it smiles too wide, you already know which version of you it isn't.")
                self.restore_sanity(5)
            else:
                type.type("Inside the " + cyan(bright("Twin's Locket")) + ", the tiny mirrored portrait shows you something impossible: your own face, but calm. Not happy. Just unafraid.")
                print(PAR)
                type.type("When you look back up, the thing by the van feels less like your reflection and more like an impersonation. Still terrifying. But not authoritative.")
                self.restore_sanity(2)
            self.update_twins_locket_durability()
            print(PAR)
        type.type("And then it smiles-a smile you've never made, too wide, too knowing-and walks behind a van.")
        print(PAR)
        type.type("You run over. Nothing. No one. Just empty parking spaces.")
        print(PAR)
        type.type("You stand there for a long time, heart pounding, wondering if you're finally losing your mind.")
        print(PAR)
        type.type("Maybe you are.")
        print(PAR)

    # ==========================================
    # CONDITIONAL EVENTS
    # ==========================================

        print(PAR)
        return
    def mayas_luck(self):
        # Conditional - requires Maya's Pick
        if not self.has_item("Maya's Pick"):
            self.day_event()
            return
        
        type.type("Your pocket feels warm. You reach in and pull out Maya's Pick.")
        print(PAR)
        type.type("It's glowing. Actually glowing. A soft, golden light.")
        print(PAR)
        type.type("You hear a voice, distant but clear: " + quote("Thank you for believing in me. I made it. I'm actually singing now."))
        print(PAR)
        type.type("The glow fades, but you feel strangely blessed. Like luck is on your side today.")
        print(PAR)
        bonus = random.randint(100, 500)
        type.type("You find " + green(bright("$" + str(bonus))) + " in your coat pocket that you're SURE wasn't there before.")
        self.change_balance(bonus)
        self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def trash_treasure(self):
        type.type("You head out from your car to the dumpster behind a convenience store. Don't judge. Times are tough.")
        print(PAR)
        chance = random.randrange(5)
        if chance == 0:
            type.type("Jackpot! Someone threw away a perfectly good sandwich. Only slightly stale.")
            self.heal(10)
        elif chance == 1:
            amount = random.randint(5, 25)
            type.type("You find a wallet! Empty, except for " + green(bright("$" + str(amount))) + " wedged in a hidden pocket.")
            self.change_balance(amount)
        elif chance == 2:
            type.type("You find... a dead rat. Cool. Very cool. You wash your hands in a puddle.")
            self.hurt(5)
        elif chance == 3:
            type.type("An employee catches you and chases you off with a broom. The indignity.")
            self.lose_sanity(2)
        else:
            type.type("Nothing useful. Just garbage. Like your life choices.")
        print(PAR)

        print(PAR)
        return
    def coin_flip_stranger(self):
        type.type("A man in a trench coat approaches your car. He flips a coin in his hand, over and over.")
        print(PAR)
        type.type(quote("Call it."))
        print(PAR)
        type.type("You don't know why, but you feel compelled to answer.")
        print(PAR)
        if self.has_item("Lucky Medallion") or self.has_item("Lucky Coin"):
            coin = "Lucky Medallion" if self.has_item("Lucky Medallion") else "Lucky Coin"
            type.type("Your " + cyan(bright(coin)) + " feels heavy in your pocket, like it already knows the result.")
            print(PAR)
        answer = ask.option("Heads or tails? ", ["heads", "tails"])
        flip = random.choice(["heads", "tails"])
        if self.has_item("Lucky Medallion"):
            flip = answer
        elif self.has_item("Lucky Coin") and random.randrange(3) == 0:
            flip = answer
        type.type("He flips. It lands on " + bright(flip) + ".")
        print(PAR)
        if answer == flip:
            amount = random.randint(20, 50)
            if self.has_item("Lucky Medallion"):
                amount += 25
                type.type(quote("That wasn't luck. That was interference.") + " He still pays.")
                print(PAR)
                self.update_lucky_coin_durability()
            elif self.has_item("Lucky Coin"):
                type.type(quote("You brought a friendly coin to a coin fight. Bold move."))
                print(PAR)
                self.update_lucky_coin_durability()
            type.type(quote("Lucky.") + " He hands you " + green(bright("$" + str(amount))) + " and walks away without another word.")
            self.change_balance(amount)
        else:
            type.type(quote("Unlucky.") + " He takes nothing, but you feel like you've lost something anyway.")
            self.lose_sanity(3)
        print(PAR)

        print(PAR)
        return
    def conspiracy_theorist(self):
        if self.has_item("Sneaky Peeky Goggles") or self.has_item("Sneaky Peeky Shades"):
            lenses = "Sneaky Peeky Goggles" if self.has_item("Sneaky Peeky Goggles") else "Sneaky Peeky Shades"
            type.type("A wild-eyed man knocks frantically on your car window.")
            print(PAR)
            type.type(quote("THEY'RE LISTENING! THE BIRDS AREN'T REAL! THE CASINO IS A FRONT FOR THE LIZARD PEOPLE!"))
            print(PAR)
            if lenses == "Sneaky Peeky Goggles":
                type.type("Through the " + cyan(bright("Sneaky Peeky Goggles")) + ", you catch the glint of an earpiece and the reflection of a parked sedan mirroring every movement here.")
                print(PAR)
                type.type("He isn't just ranting. He's clocked surveillance you missed. You leave before the sedan can settle on your plate number.")
                self.restore_sanity(4)
            else:
                type.type("Through the " + cyan(bright("Sneaky Peeky Shades")) + ", you notice the fake bird-shaped microphone bolted to the streetlamp above him.")
                print(PAR)
                type.type("He's still unhinged. But not entirely wrong. You stop rolling your eyes and roll up the window faster.")
                self.restore_sanity(2)
            self.update_sneaky_peeky_glasses_durability()
            print(PAR)
            return
        type.type("A wild-eyed man knocks frantically on your car window.")
        print(PAR)
        type.type(quote("THEY'RE LISTENING! THE BIRDS AREN'T REAL! THE CASINO IS A FRONT FOR THE LIZARD PEOPLE!"))
        print(PAR)
        type.type("You nod politely while slowly rolling up your window.")
        print(PAR)
        type.type(quote("DON'T TRUST THE DEALER! HE'S ONE OF THEM! HIS EYES—HAVE YOU SEEN HIS EYES?!"))
        print(PAR)
        type.type("The window is fully up now. He keeps talking. You pretend to be asleep.")
        print(PAR)
        self.lose_sanity(random.choice([2, 3, 4]))
        print(PAR)

        print(PAR)
        return
    def dropped_ice_cream(self):
        type.type("You step out of your car and treat yourself to an ice cream cone. A small luxury.")
        print(PAR)
        type.type("You take one lick. One beautiful, perfect lick.")
        print(PAR)
        type.type("And then it falls. Splat. Right onto the hot pavement.")
        print(PAR)
        type.type("You stare at it. It stares back, melting. A metaphor for your dreams.")
        print(PAR)
        self.lose_sanity(3)
        print(PAR)

        print(PAR)
        return
    def motivational_graffiti(self):
        type.type("Someone has spray-painted a message on the wall near your car:")
        print(PAR)
        messages = [
            quote("YOU GOT THIS!") + " ...thanks, wall.",
            quote("BELIEVE IN YOURSELF!") + " Easy for you to say, you're concrete.",
            quote("THE HOUSE ALWAYS WINS") + " ...less motivational, more threatening.",
            quote("GARY WAS HERE") + " Cool, Gary. Good for you.",
            quote("THEY'RE WATCHING") + " That's... not helpful."
        ]
        type.type(random.choice(messages))
        print(PAR)
        self.restore_sanity(1)
        print(PAR)

    # ==========================================
    # MEGA EVENT BATCH - CHEAP TIER
    # ==========================================

        print(PAR)
        return
    def yard_sale_find(self):
        type.type("You step out of your car and stumble upon a yard sale. The kind where everything costs a dollar.")
        print(PAR)
        type.type("Most of it is junk, but one item catches your eye...")
        print(PAR)
        items = [
            ("a vintage poker chip", 2, 15),
            ("an old horseshoe", 3, 10),
            ("a rabbit's foot keychain", 4, 8),
            ("a 'How to Win at Blackjack' book from 1987", 1, 5),
            ("a velvet pouch that smells like cigarettes", 5, 20)
        ]
        item, heal_amt, sanity_amt = random.choice(items)
        type.type("You buy " + item + " for $1.")
        self.change_balance(-1)
        print(PAR)
        chance = random.randrange(3)
        if chance == 0:
            type.type("Later, you realize it's actually valuable! You sell it for " + green(bright("$" + str(random.randint(20, 75)))) + "!")
            self.change_balance(random.randint(20, 75))
        else:
            type.type("It's worthless, but it makes you feel lucky.")
            self.restore_sanity(2)
        print(PAR)

        print(PAR)
        return
    def broken_atm(self):
        type.type("You step out of your car and find an ATM that's clearly malfunctioning. The screen is glitching wildly.")
        print(PAR)
        type.type("As you watch, it spits out a single $20 bill onto the ground.")
        print(PAR)
        answer = ask.yes_or_no("Take the money? ")
        if answer == "yes":
            type.type("You grab it and run. Free money!")
            self.change_balance(20)
            print(PAR)
            chance = random.randrange(5)
            if chance == 0:
                type.type("A security camera blinks red. You might have been seen...")
                self.add_danger("ATM Theft")
        else:
            type.type("You leave it. Someone else will take it. Honesty doesn't pay, but at least you can sleep at night.")
            self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def friendly_drunk(self):
        type.type("A very drunk man stumbles up to your car and starts talking to you like you're old friends.")
        print(PAR)
        type.type(quote("BUDDY! There you are! I've been looking EVERYWHERE for you!"))
        print(PAR)
        type.type("You've never met this person in your life.")
        print(PAR)
        type.type(quote("Remember that time we... we did the thing? At the place? LEGENDARY!"))
        print(PAR)
        type.type("He laughs hysterically, slaps your car twice, and wanders off into the night.")
        print(PAR)
        chance = random.randrange(3)
        if chance == 0:
            type.type("Wait, he left his wallet on your hood. There's " + green(bright("$" + str(random.randint(15, 40)))) + " inside.")
            print(PAR)
            answer = ask.yes_or_no("Keep it? ")
            if answer == "yes":
                self.change_balance(random.randint(15, 40))
            else:
                type.type("You chase him down and return it. He cries and hugs you. Awkward, but wholesome.")
                self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def car_wash_encounter(self):
        type.type("You take your car through an automatic car wash. The cheapest one, of course.")
        print(PAR)
        type.type("As the brushes spin around you, you have a moment of zen. Just you and the suds.")
        print(PAR)
        type.type("For three minutes, you forget about your problems. The water washes away your worries.")
        print(PAR)
        self.restore_sanity(5)
        cost = random.randint(5, 10)
        type.type("It cost " + green(bright("$" + str(cost))) + ", but it was worth it.")
        self.change_balance(-cost)
        print(PAR)

        print(PAR)
        return
    def lottery_scratch(self):
        type.type("You head out from your car and buy a scratch-off lottery ticket. Just one. You can afford one, right?")
        print(PAR)
        cost = 5
        if self.get_balance() < cost:
            type.type("Actually, you can't. You put it back. Sad.")
            print(PAR)
            return
        self.change_balance(-cost)
        type.type("You scratch it with a coin, heart pounding...")
        print(PAR)
        chance = random.randrange(20)
        if chance == 0:
            win = random.randint(100, 500)
            type.type("WINNER! You won " + green(bright("$" + str(win))) + "!!")
            self.change_balance(win)
            self.restore_sanity(10)
        elif chance < 5:
            win = random.randint(5, 20)
            type.type("Small winner! You got " + green(bright("$" + str(win))) + " back. Better than nothing.")
            self.change_balance(win)
        else:
            type.type("Nothing. Another $5 down the drain. The house always wins.")
            self.lose_sanity(1)
        print(PAR)

        print(PAR)
        return
    def free_sample_spree(self):
        type.type("You leave your car and spend the morning hitting up grocery stores for free samples.")
        print(PAR)
        type.type("Cheese cubes. Crackers. Some kind of dip. Tiny cups of juice.")
        print(PAR)
        type.type("By the end, you've essentially eaten a full meal without spending a dime.")
        print(PAR)
        type.type("The employees recognize you now. You can never go back. Worth it.")
        self.heal(15)
        self.restore_sanity(3)
        print(PAR)

        print(PAR)
        return
    def parking_lot_poker(self):
        if self.get_balance() < 20:
            self.day_event()
            return
        type.type("You step out of your car and see some guys playing poker on the hood of a truck in the parking lot.")
        print(PAR)
        type.type(quote("Hey, you wanna join? Twenty bucks to buy in."))
        print(PAR)
        answer = ask.yes_or_no("Join the game? ")
        if answer == "yes":
            self.change_balance(-20)
            print(PAR)
            type.type("You play for an hour. It's fun. Reminds you why you got into this whole gambling thing.")
            print(PAR)
            chance = random.randrange(3)
            if chance == 0:
                win = random.randint(50, 120)
                type.type("You clean them out! You walk away with " + green(bright("$" + str(win))) + "!")
                self.change_balance(win)
            elif chance == 1:
                type.type("You break even. Nobody wins, nobody loses. A metaphor for life.")
                self.change_balance(20)
            else:
                type.type("You lose it all. One of the guys laughs. " + quote("Stick to blackjack, buddy."))
                self.lose_sanity(3)
        else:
            type.type("You pass. They shrug and deal without you.")
        print(PAR)

        print(PAR)
        return
    def phone_scam_call(self):
        type.type("Your phone rings from the dashboard. Unknown number.")
        print(PAR)
        type.type(quote("Hello! This is the IRS! You owe us $10,000 in back taxes! Pay immediately or go to jail!"))
        print(PAR)
        answer = ask.yes_or_no("Hang up? ")
        if answer == "yes":
            type.type("You hang up. Obviously a scam. Your blood pressure is still elevated though.")
            self.lose_sanity(1)
        else:
            type.type(quote("Sir? Sir? Are you still there? Sir, we need your credit card—"))
            print(PAR)
            type.type("You tell them exactly where they can shove their fake IRS, in creative detail.")
            print(PAR)
            type.type("They hang up on YOU. Victory.")
            self.restore_sanity(3)
        print(PAR)

        print(PAR)
        return
    def vinnie_referral_card(self):
        if not self.has_item("Car") or self.has_met("Vinnie") or self.get_loan_shark_debt() > 0 or self.get_day() < 3:
            self.day_event()
            return

        self.meet("Vinnie")
        type.type("You come back to your car and find a cream-colored business card tucked beneath the wiper blade. ")
        type.type("The paper is thick, expensive, and somehow greasy at the same time.")
        print(PAR)
        type.type("On the front, embossed in gold, it reads: " + cyan(bright("Vinnie's Back Alley Loans")))
        print(PAR)
        type.type("On the back is a handwritten note: " + quote("If the banks don't believe in you, I might. Come alone."))
        print(PAR)
        type.type("You glance up and notice a black sedan idling at the far end of the lot. The driver gives you a two-finger salute and pulls away before you can get a plate.")
        print(PAR)
        type.type("The whole thing feels like a terrible idea. Which probably means it'll be useful someday.")
        print(PAR)
        type.type(yellow(bright("A new shop has been unlocked: Vinnie's Back Alley Loans")))
        print(PAR)

        print(PAR)
        return
    def windblown_worn_map(self):
        if not self.has_item("Car") or self.has_item("Map") or self.has_item("Worn Map") or self.get_day() < 3 or self.has_met("Windblown Worn Map"):
            self.day_event()
            return

        self.meet("Windblown Worn Map")
        type.type("A sheet of paper slaps against your windshield while you're sitting in the parking lot. ")
        type.type("At first you think it's trash, but the paper is thick and weathered.")
        print(PAR)
        type.type("You peel it free and unfold it carefully. It's an old trail map, hand-marked with stars, circles, and notes in the margins.")
        print(PAR)
        type.type("Somebody used this thing hard. Which means it probably leads somewhere worth finding.")
        print(PAR)
        type.type("You got the " + cyan(bright("Worn Map")) + "!")
        print(PAR)
        self.add_item("Worn Map")
        type.type(yellow(bright("A new shop has been unlocked: Marvin's Mystical Merchandise")))
        print(PAR)

        print(PAR)
        return
    def flea_market_route_map(self):
        if not self.has_item("Car") or self.has_item("Map") or self.has_item("Worn Map") or self.get_day() < 4 or self.has_met("Flea Market Route Map"):
            self.day_event()
            return

        self.meet("Flea Market Route Map")
        type.type("At a flea market, wedged between old VHS tapes and cracked hubcaps, you spot a folded road atlas with handwritten arrows sticking out of it. ")
        print(PAR)
        type.type("The seller shrugs and says some drifter kept coming back to update it until he stopped showing up.")
        print(PAR)
        type.type("Every useful note is clustered around one route, circled again and again like somebody couldn't afford to forget it.")
        print(PAR)
        type.type("You got the " + cyan(bright("Worn Map")) + "!")
        print(PAR)
        self.add_item("Worn Map")
        type.type(yellow(bright("A new shop has been unlocked: Marvin's Mystical Merchandise")))
        print(PAR)

        print(PAR)
        return
    def laundromat_bulletin_map(self):
        if not self.has_item("Car") or self.has_item("Map") or self.has_item("Worn Map") or self.get_day() < 7 or self.has_met("Laundromat Bulletin Map"):
            self.day_event()
            return

        self.meet("Laundromat Bulletin Map")
        type.type("You're killing time in a laundromat when you notice a brittle piece of paper pinned behind a flyer for guitar lessons.")
        print(PAR)
        type.type("It's a faded local map with someone's notes scribbled all over it: bridge, stars, after dark, don't trust the obvious road.")
        print(PAR)
        type.type("Whoever left it behind either found something valuable or didn't make it back for their laundry.")
        print(PAR)
        type.type("You pocket it before anyone else notices.")
        print(PAR)
        type.type("You got the " + cyan(bright("Worn Map")) + "!")
        print(PAR)
        self.add_item("Worn Map")
        type.type(yellow(bright("A new shop has been unlocked: Marvin's Mystical Merchandise")))
        print(PAR)

        print(PAR)
        return
    def witch_doctor_matchbook(self):
        if not self.has_item("Car") or self.has_met("Witch") or self.get_day() < 8 or self.has_met("Witch Doctor Matchbook"):
            self.day_event()
            return

        self.meet("Witch Doctor Matchbook")
        self.meet("Witch")
        type.type("At a gas station counter, you spot a black matchbook mixed in with the free local church flyers. ")
        print(PAR)
        type.type("Stamped on the cover in curling green ink: " + cyan(bright("The Witch Doctor's Tower")))
        print(PAR)
        type.type("Inside is a hand-drawn route through the marsh and a note that reads, " + quote("Bring cash, blood, or a good story."))
        print(PAR)
        type.type("The cashier sees you reading it and mutters that the old woman out there fixes things hospitals can't.")
        print(PAR)
        self.restore_sanity(2)
        type.type(yellow(bright("A new shop has been unlocked: Witch Doctor's Tower")))
        print(PAR)

        print(PAR)
        return
    def roadside_bone_chimes(self):
        if not self.has_item("Car") or self.has_met("Witch") or self.get_day() < 12 or self.has_met("Roadside Bone Chimes"):
            self.day_event()
            return

        self.meet("Roadside Bone Chimes")
        self.meet("Witch")
        type.type("You pass a fence strung with bone chimes, dried herbs, and little jars that catch the wind instead of sunlight. ")
        print(PAR)
        type.type("An old woman on the porch doesn't wave. She just points a long finger down the road toward the swamp and says, " + quote("You look half-dead already. Come see me before that gets expensive."))
        print(PAR)
        type.type("Then she disappears back into the shack like she was never there at all.")
        print(PAR)
        self.add_item("Granny's Swamp Nectar")
        type.type("She left a jar on the fence post. You take it.")
        print(PAR)
        type.type(yellow(bright("A new shop has been unlocked: Witch Doctor's Tower")))
        print(PAR)

        print(PAR)
        return
    def trusty_tom_coupon_mailer(self):
        if self.has_met("Tom") or self.get_day() < 8 or self.has_met("Trusty Tom Coupon Mailer"):
            self.day_event()
            return

        self.meet("Trusty Tom Coupon Mailer")
        self.meet("Tom Event")
        self.meet("Tom")
        type.type("You find a grease-smudged coupon mailer tucked under your windshield wiper. ")
        type.type("Half the page is tire ads, but one gold box is circled three times in red marker.")
        print(PAR)
        type.type(quote("TRUSTY TOM'S TRUCKS AND TIRES - honest work, fair rates, no appointment needed."))
        print(PAR)
        type.type("Someone wrote a phone number on the edge and added, ")
        type.type(quote("Tell Tom the wagon guy sent you."))
        print(PAR)
        type.type("You fold the mailer and keep it. If your ride ever needs real help, you know where to go.")
        print(PAR)
        type.type(yellow(bright("A new shop has been unlocked: Trusty Tom's Trucks and Tires")))
        print(PAR)

        print(PAR)
        return
    def filthy_frank_radio_giveaway(self):
        if self.has_met("Frank") or self.get_day() < 12 or self.has_met("Filthy Frank Radio Giveaway"):
            self.day_event()
            return

        self.meet("Filthy Frank Radio Giveaway")
        self.meet("Frank Event")
        self.meet("Frank")
        type.type("A local AM station cuts through the static just long enough for a furious voice to start shouting about brake jobs and patriot discounts. ")
        print(PAR)
        type.type("Before you can change the dial, the host announces that the first caller wins a free diagnostics voucher from Filthy Frank.")
        print(PAR)
        type.type("You call on a whim. Frank picks up himself, rants for a full minute, then tells you to stop by whenever your car starts making ")
        type.type(quote("coward sounds"))
        type.type(" again.")
        print(PAR)
        type.type("You scribble down the address mostly out of spite.")
        print(PAR)
        type.type(yellow(bright("A new shop has been unlocked: Filthy Frank's Flawless Fixtures")))
        print(PAR)

        print(PAR)
        return
    def oswald_concierge_card(self):
        if self.has_met("Oswald") or self.get_day() < 16 or self.has_met("Oswald Concierge Card"):
            self.day_event()
            return

        self.meet("Oswald Concierge Card")
        self.meet("Oswald Event")
        self.meet("Oswald")
        type.type("A valet in white gloves mistakes you for someone important and hands you a heavy black business card before hurrying off. ")
        print(PAR)
        type.type("The lettering is embossed in gold: ")
        type.type(quote("Oswald's Optimal Outoparts - precision service for discerning motorists."))
        print(PAR)
        type.type("On the back, in perfect handwriting, is a note promising ")
        type.type(quote("discreet service regardless of presentation."))
        print(PAR)
        type.type("It's absurdly fancy for your situation, which probably means it's worth remembering.")
        print(PAR)
        type.type(yellow(bright("A new shop has been unlocked: Oswald's Optimal Outoparts")))
        print(PAR)

    # ==========================================
    # MEGA EVENT BATCH - MODEST TIER
    # ==========================================

        print(PAR)
        return
    def street_performer_duel(self):
        type.type("You step out of your car and see two street performers having a turf war. A violinist and a guy with a bucket drum.")
        print(PAR)
        type.type("They're playing AT each other, trying to drown the other out. It's chaos.")
        print(PAR)
        type.type("A crowd has gathered. This is the most entertainment this town has seen in weeks.")
        print(PAR)
        answer = ask.option("Who do you tip? ", ["violinist", "drummer", "neither"])
        if answer == "violinist":
            type.type("You tip the violinist. She nods gracefully. The drummer flips you off.")
            self.change_balance(-5)
        elif answer == "drummer":
            type.type("You tip the drummer. He gives you a drumroll. The violinist looks betrayed.")
            self.change_balance(-5)
        else:
            type.type("You back away slowly. This isn't your fight.")
        print(PAR)
        self.restore_sanity(3)
        print(PAR)

        print(PAR)
        return
    def compliment_stranger(self):
        type.type("You step out of your car when a random stranger stops you.")
        print(PAR)
        compliments = [
            quote("Hey! I just wanted to say, you have really kind eyes."),
            quote("Excuse me, but you look like someone who's going through some stuff. Hang in there."),
            quote("I like your vibe. Keep doing whatever you're doing."),
            quote("You look like a main character. Whatever you're going through, you'll make it."),
            quote("Nice shoes!") + " (You're not even wearing nice shoes, but still.)"
        ]
        type.type(random.choice(compliments))
        print(PAR)
        type.type("They walk away before you can respond. You stand there, oddly touched.")
        self.restore_sanity(random.choice([5, 7, 10]))
        print(PAR)

        print(PAR)
        return
    def forgotten_birthday(self):
        type.type("Your phone buzzes from the passenger seat. A Facebook notification.")
        print(PAR)
        type.type("'Today is your birthday!'")
        print(PAR)
        type.type("Oh. It... it IS your birthday. You completely forgot.")
        print(PAR)
        type.type("You're alone. In a car. On your birthday. Living the dream.")
        print(PAR)
        answer = ask.yes_or_no("Buy yourself a cupcake? ")
        if answer == "yes" and self.get_balance() >= 5:
            type.type("You buy a sad little cupcake from a gas station and stick a match in it.")
            print(PAR)
            type.type("Happy birthday to you. Happy birthday to you...")
            print(PAR)
            type.type("You blow it out. You wish for a million dollars. Obviously.")
            self.change_balance(-5)
            self.restore_sanity(5)
            self.heal(5)
        else:
            type.type("You don't celebrate. Just another day. You're one year closer to death. Fun.")
            self.lose_sanity(5)
        print(PAR)

        print(PAR)
        return
    def book_club_invite(self):
        type.type("You step out of your car and a woman hands you a flyer. 'JOIN OUR BOOK CLUB! Free snacks!'")
        print(PAR)
        type.type("You haven't read a book since high school. But free snacks...")
        print(PAR)
        answer = ask.yes_or_no("Attend the book club? ")
        if answer == "yes":
            type.type("You show up. The book is something about a woman finding herself in Tuscany.")
            print(PAR)
            type.type("You haven't read it. Nobody has. Everyone just talks about their problems.")
            print(PAR)
            type.type("The snacks ARE really good though. And the company isn't bad.")
            self.heal(10)
            self.restore_sanity(8)
        else:
            type.type("You crumple the flyer. Social interaction is for people with stable housing.")
        print(PAR)

        print(PAR)
        return
    def car_compliment(self):
        type.type("Someone taps on your window. You tense up, expecting trouble.")
        print(PAR)
        type.type(quote("Hey man, nice car! Is this a classic?"))
        print(PAR)
        type.type("It's not. It's a beat-up wagon held together by duct tape and prayer.")
        print(PAR)
        type.type(quote("They don't make 'em like this anymore!"))
        print(PAR)
        type.type("They're right, actually. Nobody makes cars this bad anymore. But you smile anyway.")
        self.restore_sanity(5)
        print(PAR)

        print(PAR)
        return
    def dog_walker_collision(self):
        type.type("You step out of your car and start walking when a pack of dogs on leashes barrels toward you.")
        print(PAR)
        type.type("The dog walker—a small woman being dragged by six large dogs—yells " + quote("SORRY! THEY'RE FRIENDLY!"))
        print(PAR)
        type.type("You get knocked over. You're covered in dog slobber. A golden retriever is standing on your chest.")
        print(PAR)
        type.type("You've never been happier.")
        self.restore_sanity(10)
        self.heal(5)
        print(PAR)

        print(PAR)
        return
    def coffee_shop_philosopher(self):
        type.type("You head out from your car to grab a cheap coffee. You're nursing it when a philosophy student sits across from you, uninvited.")
        print(PAR)
        type.type(quote("Have you ever considered that reality is just a simulation? That nothing we do matters?"))
        print(PAR)
        type.type("You're a gambling addict who lives in a car. You've considered it.")
        print(PAR)
        type.type(quote("Like, what if the universe is just a game? And we're all NPCs?"))
        print(PAR)
        type.type("You excuse yourself before he can explain more. Your existential dread didn't need company.")
        self.lose_sanity(3)
        print(PAR)

        print(PAR)
        return
    def food_truck_festival(self):
        type.type("You step out of your car and stumble upon a food truck festival! Dozens of trucks, all kinds of cuisine.")
        print(PAR)
        type.type("Tacos. Barbecue. Korean fusion. Some kind of gourmet grilled cheese situation.")
        print(PAR)
        if self.get_balance() >= 25:
            answer = ask.yes_or_no("Treat yourself to a feast? ($25) ")
            if answer == "yes":
                type.type("You go wild. A little bit of everything. It's the best meal you've had in months.")
                self.change_balance(-25)
                self.heal(25)
                self.restore_sanity(15)
            else:
                type.type("You walk through, smelling everything, buying nothing. The struggle is real.")
        else:
            type.type("You can't afford anything. You just walk through and smell things. Sad.")
            self.lose_sanity(2)
        print(PAR)

    # ==========================================
    # MEGA EVENT BATCH - RICH TIER
    # ==========================================

        print(PAR)
        return
    def fancy_restaurant_mistake(self):
        type.type("You step out of your car and accidentally walk into a very fancy restaurant, thinking it's a diner.")
        print(PAR)
        type.type("The maître d' looks at you with barely concealed horror.")
        print(PAR)
        type.type(quote("Do you have a... reservation?"))
        print(PAR)
        if self.has_item("Expensive Cologne"):
            type.type("They pause. Sniff the air. The " + magenta(bright("Expensive Cologne")) + " precedes you like a velvet introduction.")
            print(PAR)
            type.type(quote("Ah, my apologies sir. Right this way.") + " The scent alone gets you a table.")
            print(PAR)
            type.type("The chef sends out a complimentary appetizer. The sommelier pours you a sample. You are, for one meal, a man who belongs here.")
            print(PAR)
            type.type("Dinner on the house. A memory you can't afford.")
            self.heal(25)
            self.restore_sanity(15)
            self.use_item("Expensive Cologne")
            print(PAR)
            return
        if self.get_balance() >= 200:
            answer = ask.yes_or_no("Stay and eat? ($200) ")
            if answer == "yes":
                type.type("You sit down. Order something French. Pretend you belong here.")
                print(PAR)
                type.type("The food is incredible. Tiny portions, but incredible.")
                print(PAR)
                type.type("You tip 20% because you're not a monster. Total: " + green(bright("$200")) + ".")
                self.change_balance(-200)
                self.heal(30)
                self.restore_sanity(15)
            else:
                type.type(quote("I'm just looking for the bathroom.") + " You leave with your dignity barely intact.")
        else:
            type.type("You mutter something about wrong building and flee.")
        print(PAR)

        print(PAR)
        return
    def autograph_request(self):
        type.type("You step out of your car and a teenager runs up to you. " + quote("OH MY GOD! Can I get a photo?!"))
        print(PAR)
        type.type("You have no idea why. You're not famous. Are you?")
        print(PAR)
        type.type(quote("You're... you're that guy from the thing! Right?!"))
        print(PAR)
        answer = ask.yes_or_no("Play along? ")
        if answer == "yes":
            type.type("You pose for the photo. Sign an autograph. Make something up.")
            print(PAR)
            type.type(quote("Oh wow, thank you so much! Wait till I show my friends!"))
            print(PAR)
            type.type("They run off, thrilled. You have no idea who they thought you were.")
            self.restore_sanity(10)
        else:
            type.type(quote("I think you have the wrong person."))
            print(PAR)
            type.type("Their face falls. " + quote("Oh... sorry...") + " They walk away, embarrassed.")
            type.type(" You feel bad for crushing their excitement.")
        print(PAR)

        print(PAR)
        return
    def casino_regular(self):
        type.type("You step out of your car and head to the casino. One of the regulars recognizes you. An old woman with way too much jewelry.")
        print(PAR)
        type.type(quote("You! I remember you! You're the one who won big last week!"))
        print(PAR)
        type.type("She grabs your arm with surprising strength.")
        print(PAR)
        type.type(quote("Touch my chips for luck! You're my good luck charm now!"))
        print(PAR)
        type.type("You awkwardly touch her chips. She wins $50. She gives you $20 for your trouble.")
        self.change_balance(20)
        print(PAR)
        type.type("You're not sure how to feel about being a human rabbit's foot.")
        print(PAR)

        print(PAR)
        return
    def mysterious_package(self):
        type.type("You return to your car to find a package on the hood. No label. No note. Just a box.")
        print(PAR)
        answer = ask.yes_or_no("Open it? ")
        if answer == "yes":
            chance = random.randrange(4)
            if chance == 0:
                amount = random.randint(100, 300)
                type.type("Inside: cash. " + green(bright("$" + str(amount))) + " in crisp bills. No explanation.")
                self.change_balance(amount)
                type.type(" You look around nervously. Who left this? Why?")
            elif chance == 1:
                type.type("Inside: a dead fish. A message? A threat? Just a weird prank?")
                print(PAR)
                type.type("You throw it away and check over your shoulder for the rest of the day.")
                self.lose_sanity(5)
            elif chance == 2:
                type.type("Inside: a single playing card. The Ace of Spades. No explanation.")
                print(PAR)
                type.type("It feels significant. Or maybe someone's messing with you.")
                self.lose_sanity(3)
            else:
                type.type("It's empty. Completely empty. That's somehow worse than anything.")
                self.lose_sanity(7)
        else:
            type.type("You throw it away without opening it. Some mysteries are better left unsolved.")
        print(PAR)

        print(PAR)
        return
    def the_sleeping_stranger(self):
        # SECRET: Sanity between 40-50 - a stranger sleeps in the same lot
        if self.get_sanity() < 40 or self.get_sanity() > 50:
            self.night_event()
            return
        type.type("You notice another car in the lot this morning. Someone sleeping inside, just like you.")
        print(PAR)
        type.type("For a moment, you watch them. They're restless. Bad dreams, maybe.")
        print(PAR)
        type.type("You realize: you're not the only one. There are others like you.")
        print(PAR)
        type.type("Living in cars. Chasing something. Running from something else.")
        print(PAR)
        type.type("You feel less alone. And also more alone. It's complicated.")
        print(PAR)
        type.type("In the morning, the car is gone. You never saw their face.")
        self.restore_sanity(3)
        print(PAR)

        print(PAR)
        return
    def birthday_forgotten(self):
        # SECRET: Day 365 - it's been exactly one year
        if self._day != 365:
            self.day_event()
            return
        type.type("You're sitting in your car when you check your phone. The date hits you like a truck.")
        print(PAR)
        type.type("It's been exactly ONE YEAR since you started this journey.")
        print(PAR)
        type.type("365 days of gambling. Of winning and losing. Of living in your car.")
        print(PAR)
        type.type("A whole year of your life, spent chasing a million dollars.")
        print(PAR)
        type.type("Was it worth it? You don't know. You're still here. That's something.")
        print(PAR)
        type.type("Happy anniversary to... whatever this is.")
        print(PAR)
        if self.get_balance() > 500000:
            type.type("You're more than halfway there. The finish line is in sight.")
            self.restore_sanity(20)
        elif self.get_balance() > 100000:
            type.type("You've made progress. Real progress. Keep going.")
            self.restore_sanity(10)
        else:
            type.type("It's been a hard year. But you're still fighting. That counts for something.")
            self.lose_sanity(5)
        print(PAR)

    # ==========================================
    # WRONG ITEM COMEDY EVENTS
    # ==========================================

        print(PAR)
        return
    def wrong_item_pest_control_romance(self):
        if not self.has_item("Pest Control"):
            self.day_event()
            return
        type.type("You're having a genuinely nice conversation when a cockroach scuttles across the table.")
        print(PAR)
        type.type("Without thinking, you whip out the " + cyan(bright("Pest Control")) + " and blast the table.")
        print(PAR)
        type.type("The cockroach dies. So does the mood. And possibly the tablecloth.")
        print(PAR)
        type.type("Your companion stares at you. " + quote("Why do you carry that?"))
        print(PAR)
        self.lose_sanity(15)
        type.type("You pocket the can. " + quote("No reason,") + " you say, too quickly.")
        print(PAR)

        print(PAR)
        return
    def wrong_item_vermin_bomb_romance(self):
        if not self.has_item("Vermin Bomb"):
            self.day_event()
            return
        type.type("You're sharing a park bench with someone attractive. Things are going well. Eye contact. Genuine laughter.")
        print(PAR)
        type.type("Then a pigeon lands nearby. Without thinking, your hand goes to the " + cyan(bright("Vermin Bomb")) + ".")
        print(PAR)
        type.type("The cloud is immediate. Green, acrid, and all-encompassing.")
        print(PAR)
        type.type("The pigeon is fine. It just stares at you from the fog.")
        print(PAR)
        type.type("Your date, however, is gone. Physically gone. Already across the park and accelerating.")
        print(PAR)
        type.type("You sit alone in a cloud of chemical warfare. The pigeon coos. It almost sounds like pity.")
        self.lose_sanity(12)
        self.use_item("Vermin Bomb")
        print(PAR)

        print(PAR)
        return
    def wrong_item_dirty_hat_dinner(self):
        if not self.has_item("Dirty Old Hat") and not self.has_item("Unwashed Hair"):
            self.day_event()
            return
        offending_item = "Unwashed Hair" if self.has_item("Unwashed Hair") else "Dirty Old Hat"
        type.type("You arrive at the formal dinner wearing the " + cyan(bright(offending_item)) + ".")
        print(PAR)
        type.type("The ma\u00eetre d' physically recoils. " + quote("Sir, we have a dress code."))
        print(PAR)
        type.type("You adjust it. " + quote("This IS my dress code."))
        print(PAR)
        type.type("You're escorted out before the appetizers arrive.")
        print(PAR)
        self.lose_sanity(10)
        type.type("On the way out, a busboy slips you a bread roll. Solidarity.")
        print(PAR)

        print(PAR)
        return
