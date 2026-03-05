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

class DayEventsMixin:
    """Day events: All random day events"""

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
        print("\n")
        bill = random.choice([5, 10, 20, 50, 100])
        type.type("That's another " + green(bright("$" + str(bill))) + " dollars.")
        self.change_balance(bill)

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
        print("\n")

    def estranged_dog(self):
        # EVENT: A friendly dog visits and cheers you up
        # EFFECTS: Heal 5-10 HP normally, 15-20 with Dog Treat item
        # RARE (5%): Ghost dog variant heals 50 HP
        # Alt dialogue for repeated event + rare special variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% RARE VARIANT - The Ghost Dog
            type.type("There's barking outside-but something's off. It sounds... hollow. Distant, even though it's right outside.")
            print("\n")
            type.type("Through your window, you see a dog. It's translucent. You can see right through it to the trees behind. A ghost dog.")
            print("\n")
            type.type("The spectral canine tilts its head at you, tongue lolling, then passes straight through your car door and into the seat beside you.")
            print("\n")
            type.type("You feel a warm presence, despite the chill. The ghost dog rests its head on your lap for just a moment...")
            print("\n")
            type.type("And then it's gone. But the warmth remains.")
            print("\n")
            self.heal(50)
            type.type(yellow(bright("You feel like someone's watching over you.")))
            print("\n")
            return
        
        # Normal variants
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up to the sound of barking outside your car. You get up, to see a golden retriever licking your window. ")
            type.type("You open the door, and pet the doggo on the head. He seems happy. You're happy, too.")
        elif variant == 1:
            type.type("Something wet touches your hand through the cracked window. You panic-then see the fluffy face of a happy dog staring at you. ")
            type.type("A German Shepherd this time, tail wagging so hard its whole body shakes. You can't help but smile.")
        else:
            type.type("You're woken by excited yipping. A small corgi is doing zoomies around your car, clearly having the time of its life. ")
            type.type("When you open the door, it immediately jumps into your lap and starts covering your face in kisses.")
        print("\n")
        
        # Animal Whistle auto-befriend
        if self.has_item("Animal Whistle") and not self.has_companion("Buddy"):
            type.type("The " + magenta(bright("Animal Whistle")) + " hums softly in your pocket. The dog's ears perk up.")
            print()
            type.type("Something changes in its eyes. Recognition. Trust. It sits beside you, leaning against your leg.")
            print()
            type.type("This dog... it's not leaving. It's choosing to stay.")
            print()
            self.add_companion("Buddy", "Stray Dog")
            self.heal(random.choice([15, 20]))
            return
        
        if self.has_item("Dog Treat"):
            self.use_item("Dog Treat")
            type.type("You throw your " + bright(magenta("Dog Treat")) + " into the air, ")
            type.type("and the dog jumps up, and catches it in his mouth. He wags his tail in excitement. It's super cute.")
            print("\n")
            self.heal(random.choice([15, 20]))
        else:
            self.heal(random.choice([5, 10]))
        type.type("Before you get a chance to check the dog's collar to see where it came from, the dog bolts down the road, eager to cheer up someone else. It was a good dog.")
        print("\n")
        return
    
    def freight_truck(self):
        # EVENT: A trucker wakes you up by honking at your car
        # EFFECTS: Usually just annoying
        # RARE (3%): Guilty trucker apologizes and gives $200-500
        # Alt dialogue for repeated event + rare special variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 3:  # 3% RARE VARIANT - The Guilt Trip
            type.type("A horn blares right outside your car, rattling the windows. Looking out, you see a man in a freight truck.")
            print("\n")
            type.type("But something's different. He's not laughing. He's... crying?")
            print("\n")
            type.type(quote("I'm sorry... I'm so sorry for all those times I honked at you. "))
            type.type(quote("I was going through some stuff, man. My wife left me. My dog died. My truck? Also dying."))
            print("\n")
            type.type("He wipes his nose with his sleeve.")
            print("\n")
            type.type(quote("Here. Take this. It's not much, but... I want to make things right."))
            print("\n")
            type.type("The trucker hands you a wad of cash through the window, still sniffling.")
            print("\n")
            self.change_balance(random.randint(200, 500))
            type.type(quote("Drive safe, friend. Drive safe."))
            print("\n")
            type.type("And with that, the freight truck slowly pulls away, the horn playing a sad melody into the distance.")
            print("\n")
            return
        
        # Normal variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("A deafening horn blast shakes your entire car. ")
            type.type("Looking out your window, you see a man, in a bright red hat, ")
            type.type("inside of a freight truck that's parked just outside of your vehicle.")
            print("\n")
            type.type(quote("Hey, you. Wake the fuck up! Hahahaha!"))
            print("\n")
            type.type("You watch as the man honks his horn one more time, laughs, and drives off into the distance. What a jerk.")
        elif variant == 1:
            type.type("HOOOOOOONK! You nearly hit the roof of your car as a freight truck blasts past, the driver giving you a middle finger out the window.")
            print("\n")
            type.type(quote("GET A HOUSE, LOSER!"))
            print("\n")
            type.type("The truck disappears, leaving you with ringing ears and a sour mood.")
        elif variant == 2:
            type.type("The unmistakable sound of an airhorn tears through your dreams. You bolt upright to see a trucker parked RIGHT next to your car, grinning like an idiot.")
            print("\n")
            type.type(quote("Rise and shine, buttercup! Time to face another day!"))
            print("\n")
            type.type("He gives you a thumbs up, hits the horn three more times for good measure, then drives off cackling.")
        else:
            type.type("Rhythmic honking fills the air. HONK HONK HONK-HONK-HONK. Is that... Shave and a Haircut?")
            print("\n")
            type.type("A trucker waves at you from his cab, waiting expectantly. When you don't respond with 'two bits,' he shrugs and drives off, disappointed.")
            print("\n")
            type.type(quote("No culture these days...") + " you hear him mutter.")
        print("\n")
        return

    # Conditional
    def sore_throat(self):
        # EVENT: Player wakes up with a sore throat coughing fit
        # CONDITION: Only triggers if player doesn't already have "Sore Throat" status
        # EFFECTS: Cough Drops item cures it, otherwise adds "Sore Throat" status
        if self.has_status("Sore Throat"):
            self.day_event()
            return

        type.type("A violent coughing fit hits you out of nowhere. Your throat is dry, and super sore. ")
        print("\n")
        if self.has_item("Cough Drops"):
            self.use_item("Cough Drops")
            type.type("Luckily, you have some " + magenta(bright("Cough Drops")) + " on hand, ")
            type.type("and you empty the box into your mouth. Almost like magic, your throat doesn't hurt anymore.")
            print("\n")
            return
        else:
            self.add_status("Sore Throat")
            self.mark_day("Sore Throat")
            type.type("You cough, and cough, and cough some more, but the burning itch in your throat just won't go away.")
            print("\n")
            return

    def spider_bite(self):
        # EVENT: A spider that got into the car bites the player
        # CONDITION: Requires "Spider" danger to exist, and no existing "Spider Bite"
        # EFFECTS: Pest Control kills spider; otherwise lose 1-2 sanity
        # Always adds "Spider Bite" status
        if not self.has_danger("Spider") or self.has_status("Spider Bite"):
            self.day_event()
            return

        type.type("A sharp pain shoots through your arm! ")
        type.type("Swinging your arm to scratch the pain, you watch as a spider jumps to your dashboard. ")
        print("\n")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the spider. ")
            type.type("A cloud of white liquid covers the spider, and you watch as it slows, and dies. ")
            type.type("Hopefully, that's the end of your spider problems.")
            print("\n")
        else:
            type.type("You attempt to swat it with your hand, but it sneaks into your heater. ")
            type.type("You start the engine and blast the heat, but you aren't sure if the spider has died, or if it has a family nearby. This sucks.")
            print("\n")
            self.lose_sanity(random.choice([1, 2]))  # Creature attack drains sanity
        self.add_status("Spider Bite")
        self.mark_day("Spider Bite")
        print("\n")


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
        print("\n")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the cockroach. ")
            type.type("A cloud of white liquid covers the cockroach, and you watch as it slows down, twitches, and dies. ")
            type.type("Hopefully, that's the end of your cockroach problems.")
            print("\n")
        else:
            type.type("You attempt to swat it with your hand, but it falls under your car seat. ")
            type.type("You stick your head under the seat, but you aren't sure where the cockroach went, or if it has a family nearby. This is terrible.")
            print("\n")
        type.type("The cockroach ate through some of your money. ")
        losses = int(self.get_balance() * (random.randint(10, 40)/100))
        type.type("You lost " + green(bright("${:,}".format(losses))) + ".")
        self.change_balance(-losses)

    # One-Time
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
        print("\n")
        type.type("He's riding a magnificent horse, muscular, but nimble, each step powerful, but precise. ")
        type.type("The man reaches your window, and in a deep southern accent, he begins to talk to you.")
        print("\n")
        
        # Animal Whistle lets you befriend the horse
        if self.has_item("Animal Whistle") and not self.has_companion("Thunder"):
            type.type("The " + magenta(bright("Animal Whistle")) + " resonates from your pocket. The horse whinnies and stamps its hooves.")
            print("\n")
            type.type("Jameson looks surprised. " + quote("Well I'll be. My horse NEVER acts like this. He... he likes you!"))
            print("\n")
            type.type("The horse nuzzles your hand through the window. Jameson dismounts, shaking his head in wonder.")
            print("\n")
            type.type(quote("I've had Thunder for ten years, and I've never seen him bond with anyone like this. "))
            type.type(quote("Tell ya what, partner - Thunder's yours now. He's chosen you. "))
            type.type(quote("You treat him right, ya hear?"))
            print("\n")
            type.type("You've just been given a HORSE by a cowboy. The horse's name is " + cyan(bright("Thunder")) + ".")
            print("\n")
            type.type("Jameson tips his hat, wipes a tear, and walks off down the road whistling. ")
            type.type("Thunder follows your wagon now, proud and free.")
            self.add_companion("Thunder", "Horse")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.add_item("Carrot")  # He still gives you the carrot
            print("\n")
            return
        
        type.type(open_quote("Howdy, partner! The name's Jameson. Davey Jameson. "))
        type.type(quote("I happen to notice you were admiring my steed. He's a beauty, isn't he. "))
        type.type(quote("You see, it's common courtesy when a cowboy rides by, "))
        type.type(close_quote("to give their mighty steed a carrot, as a way to express your gratitude for their hardwork and commitment to the job."))
        print("\n")
        type.type(quote("You my friend, you are carrotless. That's quite a disrespectful showing towards my steed. "))
        type.type(quote("My, my, this can't do at all. What if another cowboy comes by, you're just gonna disrespect their steed, too? "))
        type.type(quote("Tell you what, I happen to have one spare carrot in my pouch. Take this, and be ready. "))
        type.type(quote("You never know when a cowboy's gonna come trotting by."))
        print("\n")
        self.add_item("Carrot")
        type.type("Davey Jameson hands you his " + bright(magenta("Carrot")) + ", and smiles.")
        print("\n")
        type.type(quote("See, with this carrot in your possession, you're ready for anytime a cowboy strolls on down this road. "))
        type.type(quote("Just give their steed a carrot, and they'll be very grateful."))
        print("\n")
        type.type("And with that, Jameson reins his horse high into the air, gives you a yee-haw, then dashes off down the road.")
        print("\n")

    def whats_my_name(self):
        # EVENT: Little girl Suzy asks your name (establishes player name)
        # ONE-TIME: Only happens if player name is not yet set
        # EFFECTS: Sets player __name variable based on input
        if not self._name == None:
            self.day_event()
            return

        type.type("Sneakers scrape against the concrete outside-rhythmic, getting closer. ")
        type.type("As you sit up from your seat, you notice a little girl, with blonde hair and pigtails, jump roping towards you.")
        print("\n")
        type.type(space_quote("Howdy stranger! My name's Suzy! Do you like my name?"))
        answer = ask.yes_or_no("\"What was that?\" ")
        if answer == "yes":
            type.type(quote("Thanks! My mom gave it to me, before she disappeared. Who knows where she ran off to!"))
        elif answer == "no":
            type.type(quote("Wow! That's not very nice of you. You're rude, stranger."))

        print("\n")
        type.type(space_quote("Hey, what's your name, anyways?"))
        while True:
            name = str(input())
            type.type(space_quote("So your name is " + name + "?"))
            answer = ask.yes_or_no(space_quote("What was that?"))
            if answer == "yes":
                self._name = name
                type.type("\"" + name + "...I like that name! Hello, " + name + "!\"")
                print("\n")
                type.type(space_quote("Well, " + name + ", I've got to get going now. Wouldn't want the bears to eat me!"))
                type.type("And with that, Suzy, without missing a beat, continues to jump rope down the street.")
                print("\n")
                break
            elif answer == "no":
                type.type(quote("So you lied to me? You're a liar, stranger!"))
                print("\n")
                type.type(space_quote("Come on, tell me your real name!"))
    

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
        print("\n")
        type.type("The man sees you, and walks up to you.")
        print("\n")
        type.type(quote("You. You're awake. Good. You know that you aren't supposed to be here? "))
        type.type(quote("This isn't a spot for people to live. This is a road for people to drive. I hope you know this."))
        print("\n")
        type.type(space_quote("Do you know this?"))
        answer = ask.yes_or_no(space_quote("Do you? Know this?"))
        if answer == "yes":
            type.type(quote("So you do know this. Then why do you live here? You shouldn't. It's not right, man. "))
            type.type(quote("I'd suggest you stop living here. Maybe live somewhere else instead. Just not here."))
            print("\n")
        elif answer == "no":
            type.type(quote("You don't know this? How don't you know this? It's super obvious stuff, man. "))
            type.type(quote("People don't live at places where they're not supposed to, and that's exactly what you're doing right now. "))
            type.type(quote("I'd suggest you stop it, right this instant."))
            print("\n")
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 20 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return

    # ==========================================
    # NEW POOR DAY EVENTS - Everytime
    # ==========================================
    
    def morning_stretch(self):
        # EVENT: Player does morning stretches and exercise outside the car
        # EFFECTS: Heal 3, 5, or 8 HP randomly
        # Everytime - simple healing event with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("Your neck has a terrible kink from sleeping at a weird angle. You step out of the car and do some stretches, cracking joints you didn't know you had.")
            print("\n")
            type.type("After a few minutes of yoga poses you half-remember from a video you watched once, you actually feel... pretty good?")
        elif variant == 1:
            type.type("The morning sun beckons you outside. You do some jumping jacks, touch your toes (or at least try to), and take a few deep breaths of fresh air.")
            print("\n")
            type.type("Your body thanks you for remembering it exists.")
        elif variant == 2:
            type.type("You tumble out of the car, groaning. Everything hurts. You're not as young as you used to be.")
            print("\n")
            type.type("But after some careful stretching and a short walk, the aches start to fade. Not bad.")
        else:
            type.type("An old man jogs past your car and waves. Inspired (or shamed), you get out and do some light exercise.")
            print("\n")
            type.type("The old man laps you twice before you give up, but hey, you tried.")
        print("\n")
        self.heal(random.choice([3, 5, 8]))

    def ant_invasion(self):
        # EVENT: Ants invade your car while you sleep
        # EFFECTS: Pest Control kills them; otherwise adds "Ants" danger
        # Everytime - potential danger event
        variant = random.randrange(3)
        if variant == 0:
            type.type("An itching sensation crawls all over your legs. Ants! Dozens of them, crawling up from the floor of your car!")
            print("\n")
            type.type("You leap out and spend the next hour brushing them off and stomping around like a maniac.")
        elif variant == 1:
            type.type("Something tickles your ear. You reach up and feel... legs. Many legs. You look at your hand-ants.")
            print("\n")
            type.type("Your screaming probably woke up everyone within a mile radius.")
        else:
            type.type("A line of ants marches across your dashboard with military precision. They seem to be heading for your snack stash.")
            print("\n")
            type.type("You watch in horror as they disassemble a crumb and carry it away. Impressive, but concerning.")
        print("\n")
        if self.has_item("Pest Control"):
            type.type("You grab your " + bright(magenta("Pest Control")) + " and wage chemical warfare on the tiny invaders.")
            self.kill_pests()
            type.type("Victory is yours. For now.")
        else:
            type.type("Without pest control, you just have to shake them out and hope they don't come back.")
            self.add_danger("Ants")
        print("\n")

    def bird_droppings(self):
        # EVENT: Birds poop on your windshield
        # EFFECTS: 10% chance to find lottery ticket worth $20-100 in the mess
        # Everytime - comedic event
        variant = random.randrange(3)
        if variant == 0:
            type.type("SPLAT. Something wet and chunky hits your windshield. A pigeon sits on a branch above, looking very satisfied with itself.")
            print("\n")
            type.type("Great. Just great.")
        elif variant == 1:
            type.type("Your entire windshield is covered in bird droppings. Like, COVERED. Did a whole flock decide your car was the designated bathroom?")
            print("\n")
            type.type("This is going to take forever to clean.")
        else:
            type.type("A crow lands on your hood and stares at you through the windshield. It tilts its head. Then, maintaining eye contact, it poops.")
            print("\n")
            type.type("You've been disrespected by a bird. A new low.")
        print("\n")
        chance = random.randrange(10)
        if chance == 0:
            type.type("Wait... is that a lottery ticket stuck in the mess? Someone must have thrown it out their window.")
            print("\n")
            type.type("You carefully extract it, wipe it off, and check the numbers... ")
            win = random.randint(20, 100)
            type.type("It's a " + green(bright("$" + str(win))) + " winner! Gross, but lucky!")
            self.change_balance(win)
        print("\n")

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
            print("\n")
            type.type("Must've run over something sharp. Just your luck.")
        elif variant == 1:
            type.type("The car is listing to one side. Upon inspection: flat tire. Very flat. Like, pancake flat.")
            print("\n")
            type.type("You kick it in frustration, which doesn't help at all.")
        else:
            type.type("A hissing sound wakes you up. It's not a snake-it's your tire, slowly deflating before your eyes.")
            print("\n")
            type.type("You watch helplessly as your wheel becomes a sad rubber puddle.")
        print("\n")
        if self.has_item("Spare Tire"):
            type.type("Good thing you have a " + bright(magenta("Spare Tire")) + "! You spend the next hour changing it out.")
            self.use_item("Spare Tire")
            type.type("Not how you wanted to start the day, but at least you're not stranded.")
        else:
            type.type("Without a spare, you're going to have to walk to get this fixed. That'll cost time and money.")
            self.add_travel_restriction("Flat Tire")
            self.change_balance(-random.randint(50, 150))
        print("\n")

    def mysterious_note(self):
        # EVENT: Find a cryptic threatening note on your car
        # EFFECTS: Atmospheric/creepy - no mechanical effects
        # Everytime - cryptic event
        variant = random.randrange(4)
        if variant == 0:
            type.type("There's a note tucked under your windshield wiper. It reads: " + quote("I know what you did."))
            print("\n")
            type.type("What did you do? You don't even know. This is unsettling.")
        elif variant == 1:
            type.type("You find a crumpled note on your dashboard. In messy handwriting: " + quote("The dealer always wins. Always."))
            print("\n")
            type.type("A chill runs down your spine.")
        elif variant == 2:
            type.type("A small piece of paper is stuck to your window. It says: " + quote("You're being watched."))
            print("\n")
            type.type("You look around nervously. No one's there. At least, no one you can see.")
        else:
            type.type("There's a note on your seat that definitely wasn't there last night. It reads: " + quote("Wake up."))
            print("\n")
            type.type("You ARE awake. Aren't you?")
        print("\n")

    def radio_static(self):
        # EVENT: Radio plays creepy static, voices, or backwards songs
        # EFFECTS: Atmospheric/creepy - no mechanical effects
        # Everytime - atmospheric event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You turn on the radio for some company, but all you get is static. Then, for just a moment, you hear a voice.")
            print("\n")
            type.type(quote("...don't go to the casino...") + " it whispers, before dissolving back into white noise.")
            print("\n")
            type.type("You turn the radio off. Probably just interference. Probably.")
        elif variant == 1:
            type.type("The radio crackles to life on its own. You don't remember turning it on.")
            print("\n")
            type.type("A song plays-one you almost recognize, but not quite. The lyrics are backwards, or maybe in another language.")
            print("\n")
            type.type("You yank the power cord. The music keeps playing for three seconds before stopping.")
        else:
            type.type("You fiddle with the radio dial, searching for anything other than static. Finally, a clear station!")
            print("\n")
            type.type("It's playing your least favorite song. Of course it is.")
            print("\n")
            type.type("You turn it off in disgust.")
        print("\n")

    # ==========================================
    # NEW POOR DAY EVENTS - Conditional
    # ==========================================
    
    def ant_bite(self):
        # EVENT: The ants that invaded your car are now biting you
        # CONDITION: Requires "Ants" danger to exist
        # EFFECTS: Pest Control = 10 damage; otherwise 20 damage; adds "Ant Bites" status
        # Conditional - requires Ant danger
        if not self.has_danger("Ants"):
            self.day_event()
            return
        
        type.type("You're COVERED in angry red welts. The ants that invaded your car yesterday? They didn't leave. They multiplied.")
        print("\n")
        type.type("And they're BITING.")
        print("\n")
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
        print("\n")

    # ==========================================
    # NEW POOR DAY EVENTS - One-Time
    # ==========================================
    
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
        print("\n")
        type.type(quote("You there! Young person! I've been walking this road for sixty years "))
        type.type(quote("and I've never seen someone sleeping in their CAR before! What's the world coming to?"))
        print("\n")
        type.type("You try to explain your situation, but he just waves his cane dismissively.")
        print("\n")
        type.type(quote("In my day, we slept in DITCHES like RESPECTABLE vagrants! Cars! Bah! Too fancy! "))
        type.type(quote("Back in the Depression, we didn't even have wheels-we just rolled places with our own two legs!"))
        print("\n")
        type.type("He rants for a solid ten minutes about the good old days of homelessness.")
        print("\n")
        type.type(quote("Here, take this. You'll need it more than me. I'm 97 years old and I've never spent a dime I didn't have to."))
        print("\n")
        gift = random.randint(25, 75)
        type.type("Old Man Jenkins hands you " + green(bright("$" + str(gift))) + " in coins, mostly pennies and nickels.")
        self.change_balance(gift)
        print("\n")
        type.type("And with that, he hobbles off down the road, still muttering about kids these days.")
        print("\n")

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
        print("\n")
        type.type("The mime stares at you. You stare back.")
        print("\n")
        type.type("Without a word (obviously), the mime begins to act out a scene. He's pretending to be trapped in a box. Classic.")
        print("\n")
        type.type("Then he mimes... crying? Counting money? Losing at cards?")
        print("\n")
        type.type("Wait. Is he acting out YOUR life?")
        print("\n")
        type.type("The mime finishes with a dramatic death scene, tongue out and everything, then springs back up and takes a bow.")
        print("\n")
        answer = ask.yes_or_no("Do you applaud? ")
        if answer == "yes":
            type.type("The mime beams and hands you an invisible flower. You pretend to smell it.")
            print("\n")
            type.type("He then gives you a very real " + green(bright("$20")) + " bill from his pocket, waves, and walks away into an invisible wall.")
            self.change_balance(20)
            self.heal(5)
        else:
            type.type("The mime looks devastated. He mimes a single tear rolling down his cheek, then slowly backs away, never breaking eye contact.")
            print("\n")
            type.type("You feel kind of bad about that.")
        print("\n")

    # ==========================================
    # SECRET EVENTS - POOR TIER
    # ==========================================
    
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
        print("\n")
        type.type("A figure stands outside your window. Tall. Thin. Its face is in shadow, but you can see its smile-too wide, too many teeth.")
        print("\n")
        type.type(red(quote("Six hundred and sixty-six dollars. How fitting.")))
        print("\n")
        type.type("You blink, and the figure is inside your car, sitting in the passenger seat.")
        print("\n")
        type.type(red(quote("I've been watching you, gambler. I like your style. Tell you what-I'll make you an offer.")))
        print("\n")
        type.type(quote("Double or nothing. I flip a coin. Heads, I double your money. Tails... well. Let's just say you'll owe me."))
        print("\n")
        answer = ask.yes_or_no("Accept the devil's offer? ")
        if answer == "yes":
            if random.randrange(2) == 0:
                type.type(red("The figure flips a coin that seems to be made of pure darkness. It spins impossibly slow..."))
                print("\n")
                type.type(green(bright("HEADS.")))
                print("\n")
                type.type(red(quote("Lucky you. This time.")))
                print("\n")
                type.type("You blink again, and the figure is gone. But your money pile has doubled.")
                self.change_balance(666)
            else:
                type.type(red("The figure flips a coin that seems to be made of pure darkness. It spins impossibly slow..."))
                print("\n")
                type.type(red(bright("TAILS.")))
                print("\n")
                type.type(red(quote("A deal's a deal. Don't worry-I won't collect today. But I WILL collect. Eventually.")))
                print("\n")
                type.type("You blink, and the figure is gone. Your money is untouched, but you feel like you've lost something far more valuable.")
                self.add_danger("Devil's Debt")
                self.lose_sanity(random.choice([2, 3]))  # Losing to devil further drains sanity
        else:
            type.type("The figure laughs, a sound like breaking glass.")
            print("\n")
            type.type(red(quote("Wise. Or cowardly. Time will tell which.")))
            print("\n")
            type.type("When you blink, the figure is gone. The sun is rising. Was it a dream?")
        print("\n")
        type.type(yellow(bright("Something about that encounter will stay with you forever.")))
        print("\n")

    def perfect_hand(self):
        # SECRET EVENT: The universe rewards you for having exactly $21 (Blackjack!)
        # TRIGGER: Balance must be exactly $21
        # EFFECTS: Adds "Lucky" status, adds "Ace of Spades" item
        # SECRET - Only triggers if you have EXACTLY 21 dollars
        if self.get_balance() != 21:
            self.day_event()
            return
        
        type.type("You count your money this morning and realize you have exactly " + green(bright("$21")) + ". Blackjack.")
        print("\n")
        type.type("As if on cue, a single playing card flutters down from nowhere and lands in your lap. The Ace of Spades.")
        print("\n")
        type.type("You look up. There's no one there. No birds, no trees. Just clear sky.")
        print("\n")
        type.type("On the back of the card, someone has written: " + quote("The universe deals you a winner."))
        print("\n")
        type.type(yellow(bright("You feel inexplicably lucky today.")))
        self.add_status("Lucky")
        self.add_item("Ace of Spades")
        print("\n")

    # Cheap Day Events (1,000 - 10,000)
    # Everytime
    def sun_visor_bills(self):
        # EVENT: Find money hidden in your sun visor
        # EFFECTS: Normally gain $3-300
        # RARE (5%): Jackpot variant gives $800-2000
        # Alt dialogue for repeated event + rare variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% RARE VARIANT - The Jackpot Visor
            type.type("You flip down the sun visor to block the morning sun and-")
            print("\n")
            type.type("HOLY SHIT.")
            print("\n")
            type.type("Bills cascade down like a waterfall. Twenties, fifties, even some hundreds, all stuffed into the visor like it was a makeshift piggy bank.")
            print("\n")
            type.type("Did you do this? Did past-you do this and forget? Is this some kind of divine intervention?")
            print("\n")
            bill = random.randint(800, 2000)
            type.type("After counting it all, you find " + green(bright("${:,}".format(bill))) + " dollars!")
            print("\n")
            type.type(yellow("You have no idea where this came from, but you're not complaining."))
            print("\n")
            self.change_balance(bill)
            print("\n")
            return
        
        # Normal variants
        variant = random.randrange(3)
        if variant == 0:
            type.type("You wake up in the front seat, dripping in sweat. ")
            print("\n")
            type.type("As the sun shines through the car window, you notice a few bright green bills above you, peeking out of the sun visor. How long have they been there? ")
            print("\n")
        elif variant == 1:
            type.type("The sun glares through your windshield, and you reach for the visor. As you flip it down, something flutters into your lap. ")
            print("\n")
            type.type("Money! You check the visor again-there's more. ")
            print("\n")
        else:
            type.type("You sit up, rubbing your eyes, and accidentally bump the sun visor. Cash rains down on you. ")
            print("\n")
            type.type("You forgot you hid emergency funds up there! Past-you was actually smart for once. ")
            print("\n")
        bill = random.choice([3, 15, 30, 60, 150, 300])
        type.type("That's another " + green(bright("$" + str(bill))) + " dollars.")
        print("\n")
        self.change_balance(bill)
        print("\n")

    def strong_winds(self):
        # EVENT: Severe wind storm keeps you trapped in the car
        # EFFECTS: Adds "Wind" travel restriction normally
        # RARE (3%): Wind blows in $300-800 cash from somewhere
        # Alt dialogue for repeated event + rare variant
        rare_chance = random.randrange(100)
        
        if rare_chance < 3:  # 3% RARE VARIANT - Wind Brings Gifts
            type.type("Howling wind is rattling your wagon. Branches are falling, leaves are flying, and-")
            print("\n")
            type.type("THUNK.")
            print("\n")
            type.type("Something lands on your roof. Then another thunk. And another.")
            print("\n")
            type.type("You cautiously step outside, bracing against the gusts. ")
            type.type("On the ground around your car... money. Bills, blowing in from god-knows-where, plastering themselves against your vehicle.")
            print("\n")
            type.type("You spend the next hour chasing down wind-blown cash like the world's most chaotic Easter egg hunt.")
            print("\n")
            windfall = random.randint(300, 800)
            type.type("In the end, you manage to snag " + green(bright("${:,}".format(windfall))) + "!")
            print("\n")
            self.change_balance(windfall)
            self.add_travel_restriction("Wind")
            print("\n")
            return
        
        # Normal variants
        variant = random.randrange(3)
        if variant == 0:
            type.type("A loud snap rings out above you, followed by a massive branch crashing down from the treetops and into the street. ")
            type.type("The wind echoes throughout the trees around you, and many of them look to be on the verge of falling.")
            print("\n")
            type.type("With the weather being this bad, you make the executive decision to just chill in the wagon for the day.")
            print("\n")
        elif variant == 1:
            type.type("Your car rocks violently, waking you from a deep sleep. Outside, it's chaos-trees bending, debris flying, the sky an angry gray.")
            print("\n")
            type.type("Yeah, no. You're not going out in that. Time to hunker down.")
            print("\n")
        else:
            type.type("The sound is deafening-wind screaming past your windows, your wagon shaking like it might flip over.")
            print("\n")
            type.type("A trash can tumbles past your windshield, followed by what looks like someone's lawn chair. ")
            print("\n")
            type.type("Today is officially an 'inside day.'")
            print("\n")
        self.add_travel_restriction("Wind")
        print("\n")

    # Conditional
    def got_a_cold(self):
        # EVENT: You wake up with a cold
        # CONDITION: Only triggers if you don't already have "Cold" status
        # EFFECTS: Adds "Cold" status
        if self.has_status("Cold"):
            self.day_event()
            return
        
        type.type("A sneeze rips through you in your car seat, followed by your nose running, droplets falling down from your chin and onto your shirt. Damn, must be a cold.")
        print("\n")
        self.add_status("Cold")
        self.mark_day("Cold")
        print("\n")

    # ==========================================
    # NEW CHEAP DAY EVENTS - Everytime
    # ==========================================
    
    def morning_fog(self):
        # EVENT: Dense fog blankets the area
        # EFFECTS: Usually atmospheric; one variant deals 5 damage (walk into mirror)
        # Everytime - atmospheric with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("Fog so thick you can barely see your hood has swallowed the world in white.")
            print("\n")
            type.type("You wait an hour for it to clear. Two hours. Finally, around noon, you can see the road again.")
            print("\n")
        elif variant == 1:
            type.type("The fog this morning is eerie. Shapes seem to move in it-people? Animals? You can't tell.")
            print("\n")
            type.type("By the time the fog lifts, you're convinced you saw at least three ghosts. Or maybe just trees. Hopefully trees.")
            print("\n")
        elif variant == 2:
            type.type("A heavy mist blankets everything. You step outside and immediately lose sight of your car.")
            print("\n")
            type.type("After ten minutes of wandering in circles, you find it again. That was embarrassing.")
            print("\n")
        else:
            type.type("The fog is so dense this morning that you walk face-first into your own side mirror.")
            print("\n")
            type.type("Ow.")
            print("\n")
            self.hurt(5)
        print("\n")

    def car_wont_start(self):
        # EVENT: Car engine won't start (dead battery or mechanical issues)
        # EFFECTS: 33% chance it starts anyway; otherwise adds travel restriction
        # Everytime - potential restriction event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You turn the key and... nothing. Click click click. The engine won't catch.")
            print("\n")
            type.type("Dead battery. Great.")
            print("\n")
        elif variant == 1:
            type.type("The engine makes a sound like a dying whale when you try to start it. Then silence.")
            print("\n")
            type.type("Something's definitely wrong under the hood.")
            print("\n")
        else:
            type.type("Your car starts, sputters, coughs, and dies. It sounds like it's given up on life. You relate.")
            print("\n")
        
        if random.randrange(3) == 0:
            type.type("After some jiggling and praying, it starts back up! Crisis averted.")
            print("\n")
        else:
            type.type("Looks like you're not driving anywhere until this gets fixed.")
            print("\n")
            self.add_travel_restriction("Car Trouble")
            if self.has_met("Tom"):
                type.type("Maybe Tom can help with this...")
                print("\n")
        print("\n")

    def raccoon_raid(self):
        # EVENT: Raccoons raid your car looking for food/valuables
        # EFFECTS: Normally may lose $20-80
        # RARE (5%): Raccoon Mafia demands $100-300 tribute
        # Everytime - creature event with variants
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% RARE VARIANT - Raccoon Gang
            type.type("Your car is SURROUNDED by raccoons. Not one or two. DOZENS.")
            print("\n")
            type.type("They're organized. One stands on your hood, clearly the leader. It chatters at you-a demand, not a greeting.")
            print("\n")
            type.type("The Raccoon Mafia wants tribute.")
            print("\n")
            
            # Animal Whistle befriends the boss
            if self.has_item("Animal Whistle") and not self.has_companion("Don"):
                type.type("The " + magenta(bright("Animal Whistle")) + " suddenly glows bright in the moonlight.")
                print()
                type.type("The boss raccoon's ears perk up. It stops chattering. Its gang falls silent.")
                print()
                type.type("The boss hops off your hood and approaches. It sniffs the whistle, then... bows.")
                print()
                type.type("The entire raccoon mafia bows with it. You've earned their respect.")
                print()
                type.type("The boss raccoon-now " + cyan(bright("Don")) + "-climbs into your car. The gang disperses.")
                print()
                self.add_companion("Don", "Raccoon Boss")
                return
            
            tribute = random.randint(100, 300)
            type.type("You reluctantly throw " + green(bright("${:,}".format(tribute))) + " out the window. The leader inspects it, nods, and the whole gang scurries away.")
            print("\n")
            self.change_balance(-tribute)
            type.type(yellow("You've made some interesting enemies today."))
            print("\n")
            return
        
        variant = random.randrange(3)
        if variant == 0:
            type.type("A fat raccoon is sitting on your hood, eating what appears to be your snack stash. It stares at you defiantly.")
            print("\n")
            type.type("You bang on the window. It doesn't care.")
            print("\n")
        elif variant == 1:
            type.type("Scratch marks all over your trunk. Something tried to break in last night. Raccoon prints everywhere.")
            print("\n")
            type.type("Those little bandits!")
            print("\n")
        else:
            type.type("You open your door and a raccoon FALLS OUT. It was hiding IN YOUR CAR. How?! WHEN?!")
            print("\n")
            type.type("It hisses at you, grabs something shiny, and bolts.")
            print("\n")
            loss = random.randint(20, 80)
            type.type("It stole " + green(bright("$" + str(loss))) + " from you!")
            print("\n")
            self.change_balance(-loss)
        print("\n")

    def beautiful_sunrise(self):
        # EVENT: You wake up to a beautiful sunrise
        # EFFECTS: Heal 5-15 HP, restore 1-3 sanity
        # Purely positive event with no downsides
        # Everytime - purely positive event
        variant = random.randrange(3)
        if variant == 0:
            type.type("The sunrise catches your eye through the windshield. Pink and gold paint the sky, and for a moment, everything feels... okay.")
            print("\n")
            type.type("Sometimes you have to appreciate the little things.")
            print("\n")
        elif variant == 1:
            type.type("The dawn light streams through your windshield, warm and golden. Birds are singing. The air smells fresh.")
            print("\n")
            type.type("Today might actually be a good day.")
            print("\n")
        else:
            type.type("You watch the sun come up over the hills, painting everything in shades of orange and red.")
            print("\n")
            type.type("It's beautiful enough to make you forget, just for a moment, that you live in a car.")
            print("\n")
        self.heal(random.choice([5, 10, 15]))
        self.restore_sanity(random.choice([1, 2, 3]))  # Restores sanity
        print("\n")

    # ==========================================
    # ITEM-USING EVENTS - Items get consumed
    # ==========================================
    
    def mosquito_swarm(self):
        # EVENT: Mosquitoes swarm your car and bite you
        # EFFECTS: Bug Spray prevents damage (consumed); otherwise 10-20 damage
        # Bug Spray can save you from damage
        type.type("The buzzing fills your car. First one mosquito, then ten, then what feels like a thousand.")
        print("\n")
        type.type("They swarm your car, slipping through every crack and crevice.")
        print("\n")
        
        if self.has_item("Bug Spray"):
            type.type("But wait - you have " + magenta(bright("Bug Spray")) + "!")
            print("\n")
            type.type("You grab the can and spray yourself down liberally. The mosquitoes keep their distance, buzzing angrily but unable to bite.")
            print("\n")
            type.type("The spray is used up, but you're bite-free.")
            self.use_item("Bug Spray")
            print("\n")
        else:
            type.type("You spend the night swatting and scratching. By morning, you're covered in itchy welts.")
            print("\n")
            self.hurt(random.randint(10, 20))
            type.type("Bug spray would have been really helpful right about now.")
        print("\n")

    def scorching_sun(self):
        # EVENT: Extremely hot sun causes heat damage
        # EFFECTS: Cheap Sunscreen prevents damage (consumed); Umbrella reduces to 5;
        #          otherwise 15-25 damage from sunburn
        # Cheap Sunscreen / Sunglasses can help
        type.type("It's hot. Really hot. The sun beats down mercilessly, and your car becomes an oven.")
        print("\n")
        
        if self.has_item("Cheap Sunscreen"):
            type.type("Good thing you have " + magenta(bright("Cheap Sunscreen")) + "!")
            print("\n")
            type.type("You slather it on and step outside. It's still hot, but at least you won't turn into a lobster.")
            print("\n")
            type.type("The tiny bottle is empty now, but worth it.")
            self.use_item("Cheap Sunscreen")
        elif self.has_item("Umbrella"):
            type.type("You grab your " + magenta(bright("Umbrella")) + " and use it as a sun shade.")
            print("\n")
            type.type("It provides some relief from the blazing sun.")
            self.hurt(5)
        else:
            type.type("You try to stay in the shade, but there's no escaping this heat.")
            print("\n")
            type.type("By the end of the day, your skin is red and painful.")
            self.hurt(random.randint(15, 25))
            type.type("Sunscreen would have prevented this.")
        print("\n")

    def sudden_downpour(self):
        # EVENT: Sudden heavy rainstorm catches you outside
        # EFFECTS: Umbrella or Plastic Poncho prevents damage/cold;
        #          otherwise 10 damage and adds "Cold" status
        # Umbrella or Plastic Poncho prevents damage/getting sick
        type.type("The sky opens up without warning. Rain hammers down so hard you can barely hear yourself think.")
        print("\n")
        
        if self.has_item("Umbrella"):
            type.type("You grab your " + magenta(bright("Umbrella")) + " and step out, staying relatively dry.")
            print("\n")
            type.type("The storm passes after an hour, and you're no worse for wear.")
        elif self.has_item("Plastic Poncho"):
            type.type("You pull out your " + magenta(bright("Plastic Poncho")) + " and throw it on!")
            print("\n")
            type.type("It crinkles loudly with every movement, but it keeps you dry.")
            print("\n")
            type.type("By the time the rain stops, the cheap poncho has torn in three places. Time to toss it.")
            self.use_item("Plastic Poncho")
        else:
            type.type("You get soaked to the bone. The chill seeps into you.")
            print("\n")
            self.hurt(10)
            if random.randrange(3) == 0:
                type.type("You feel a cold coming on...")
                self.add_status("Cold")
                self.mark_day("Cold")
        print("\n")

    def freezing_night(self):
        # EVENT: Freezing cold night threatens to give you hypothermia
        # EFFECTS: Hand Warmers prevent damage (consumed); fire source = 5 damage;
        #          otherwise 15-25 damage and 25% chance of "Cold" status
        # Hand Warmers can help survive
        type.type("The temperature plummets. Frost forms on your windshield, and you can see your breath inside the car.")
        print("\n")
        
        if self.has_item("Hand Warmers"):
            type.type("You crack open your " + magenta(bright("Hand Warmers")) + " and hold them close.")
            print("\n")
            type.type("The chemical heat spreads through your fingers, your hands, your whole body. Warmth.")
            print("\n")
            type.type("You survive the night comfortably. The warmers are spent by morning.")
            self.use_item("Hand Warmers")
        elif self.has_fire_source():
            type.type("You manage to generate some warmth with what you have. It's not comfortable, but you survive.")
            self.hurt(5)
        else:
            type.type("You shiver through the entire night, curled up in a ball, teeth chattering.")
            print("\n")
            self.hurt(random.randint(15, 25))
            if random.randrange(4) == 0:
                type.type("You feel a cold coming on...")
                self.add_status("Cold")
                self.mark_day("Cold")
        print("\n")

    def car_smell(self):
        # EVENT: Your car smells terrible
        # EFFECTS: Air Freshener restores 3 sanity (consumed); otherwise lose 2-4 sanity
        # Air Freshener removes bad smell status
        type.type("Something in your car STINKS. You can't tell if it's the old food, the musty seats, or just... you.")
        print("\n")
        
        if self.has_item("Air Freshener"):
            type.type("You hang up your " + magenta(bright("Air Freshener")) + " and take a deep breath.")
            print("\n")
            type.type("Ahhh. Pine fresh. Much better.")
            print("\n")
            type.type("The freshener will fade over time, but for now, it's a major improvement.")
            self.use_item("Air Freshener")
            self.restore_sanity(3)
        else:
            type.type("You try to air it out by opening the windows, but the smell lingers.")
            print("\n")
            type.type("Living in this stench is demoralizing.")
            self.lose_sanity(random.randint(2, 4))
        print("\n")

    def roadside_breakdown(self):
        # EVENT: Car breaks down on the side of the road
        # EFFECTS: Road Flares get help quickly (consumed); Flashlight helps a bit;
        #          otherwise $100-200 tow cost and travel restriction
        # Road Flares help get assistance
        type.type("Your car makes a horrible grinding noise and coasts to a stop on the side of the road. This is bad.")
        print("\n")
        
        if self.has_item("Road Flares"):
            type.type("You grab your " + magenta(bright("Road Flares")) + " and set them up behind your car.")
            print("\n")
            type.type("The bright red flames are visible for miles. Within an hour, a passing truck stops to help.")
            print("\n")
            type.type(quote("Saw your flares from way back. Smart thinking! Let me take a look..."))
            print("\n")
            type.type("The trucker helps you get the car started again. The flares are spent, but crisis averted.")
            self.use_item("Road Flares")
        elif self.has_item("Flashlight"):
            type.type("You wave your " + magenta(bright("Flashlight")) + " at passing cars. After an hour, someone finally stops.")
            print("\n")
            type.type("They help jumpstart your car. It could have been worse.")
            self.add_travel_restriction("Car Trouble")
        else:
            type.type("You sit there for hours, trying to flag down help. Most cars just speed past.")
            print("\n")
            type.type("Finally, by nightfall, a tow truck comes. But it costs you.")
            tow_cost = random.randint(100, 200)
            type.type("You pay " + green(bright("${:,}".format(tow_cost))) + " for the tow.")
            self.change_balance(-tow_cost)
            self.add_travel_restriction("Car Trouble")
        print("\n")

    def broken_belonging(self):
        # EVENT: One of your belongings breaks
        # EFFECTS: Super Glue or Duct Tape fixes it (consumed); otherwise lose 2 sanity
        # Super Glue or Duct Tape can fix things
        type.type("You hear a crack. One of your belongings has broken - a part snapped clean off.")
        print("\n")
        
        if self.has_item("Super Glue"):
            type.type("But you have " + magenta(bright("Super Glue")) + "!")
            print("\n")
            type.type("A few drops, some careful pressing, and... good as new. Almost.")
            print("\n")
            type.type("The glue tube is empty now, but at least you saved your stuff.")
            self.use_item("Super Glue")
        elif self.has_item("Duct Tape"):
            type.type("Nothing a little " + magenta(bright("Duct Tape")) + " can't fix!")
            print("\n")
            type.type("It's not pretty, but it holds. Duct tape: the universal solution.")
            print("\n")
            type.type("You used the last of the roll, but hey, it worked.")
            self.use_item("Duct Tape")
        else:
            type.type("Without anything to fix it, you just have to accept the loss.")
            print("\n")
            type.type("Sometimes things just break and stay broken.")
            self.lose_sanity(2)
        print("\n")

    def social_encounter(self):
        # EVENT: Someone important approaches and you need to make a good impression
        # EFFECTS: Breath Mints = $50 (consumed); Expensive Cologne = $100 (consumed);
        #          otherwise lose 3 sanity from humiliation
        # Breath Mints or Expensive Cologne help with social situations
        type.type("Someone important-looking approaches your car. They seem friendly, but you're suddenly aware of... yourself.")
        print("\n")
        type.type("When's the last time you showered? How's your breath?")
        print("\n")
        
        if self.has_item("Breath Mints"):
            type.type("You quickly pop a " + magenta(bright("Breath Mint")) + " before they get close.")
            print("\n")
            type.type("Minty fresh! You greet them with confidence.")
            print("\n")
            type.type("They turn out to be a philanthropist who gives you " + green(bright("$50")) + " for being so friendly.")
            self.change_balance(50)
            self.use_item("Breath Mints")
        elif self.has_item("Expensive Cologne"):
            type.type("You spritz some " + magenta(bright("Expensive Cologne")) + " on yourself.")
            print("\n")
            type.type("Now you smell like money. Fake it till you make it.")
            print("\n")
            type.type("They're impressed by your style and give you " + green(bright("$100")) + " along with their business card.")
            self.change_balance(100)
            self.use_item("Expensive Cologne")
        else:
            type.type("You try to be friendly, but they wrinkle their nose and quickly make an excuse to leave.")
            print("\n")
            type.type("That was humiliating.")
            self.lose_sanity(3)
        print("\n")

    def important_document(self):
        # EVENT: Find a form that needs signing and could be worth money
        # EFFECTS: Fancy Pen = $100-300 reward (consumed); otherwise form is rejected
        # Fancy Pen makes a difference
        type.type("You find a form wedged under your car seat. Something important - could be worth money.")
        print("\n")
        type.type("But you need to sign it to make it official.")
        print("\n")
        
        if self.has_item("Fancy Pen"):
            type.type("You pull out your " + magenta(bright("Fancy Pen")) + " and sign with a flourish.")
            print("\n")
            type.type("The signature looks professional. Important. Legitimate.")
            print("\n")
            reward = random.randint(100, 300)
            type.type("The form turns out to be valid, and you receive " + green(bright("${:,}".format(reward))) + "!")
            self.change_balance(reward)
            # Pen doesn't get consumed - it's reusable
        else:
            type.type("You scrounge around for something to write with. An old crayon? A stubby pencil?")
            print("\n")
            type.type("Your signature looks like a child wrote it. The form is rejected.")
            print("\n")
            type.type("Opportunity lost.")
        print("\n")

    def caught_fishing(self):
        # EVENT: Park near a river with fish swimming
        # EFFECTS: Fishing Line = 67% chance heal 20 HP + 3 sanity (consumed);
        #          otherwise just watch fish hungrily
        # Fishing Line lets you catch fish
        type.type("You park near a river. The water is clear, and you can see fish swimming lazily beneath the surface.")
        print("\n")
        
        # Animal Whistle lets you befriend a fish
        if self.has_item("Animal Whistle") and not self.has_companion("Bubbles"):
            type.type("The " + magenta(bright("Animal Whistle")) + " resonates with the water. The fish stop swimming and rise to the surface.")
            print("\n")
            type.type("One particularly large, golden koi swims right up to you. It splashes, then opens its mouth - like it's talking.")
            print("\n")
            type.type("You dip your hand in the water. The koi nuzzles your palm. It's... following you?")
            print("\n")
            type.type("The koi leaps into a bucket you didn't realize you had. Magic is weird.")
            print("\n")
            type.type("You've befriended a fish. You decide to call it " + cyan(bright("Bubbles")) + ".")
            print("\n")
            type.type("Bubbles will travel with you in a perpetually full bucket. Don't ask how it works.")
            self.add_companion("Bubbles", "Koi Fish")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.restore_sanity(5)
            print("\n")
            return
        
        if self.has_item("Fishing Line"):
            type.type("You have " + magenta(bright("Fishing Line")) + "! Time to try your luck.")
            print("\n")
            type.type("You fashion a makeshift rod from a branch, attach the line, and cast out.")
            print("\n")
            if random.randrange(3) == 0:
                type.type("After an hour of waiting... nothing. The fish aren't biting today.")
                print("\n")
                type.type("The line got tangled and snapped. Frustrating.")
            else:
                type.type("You feel a tug! You pull hard, and land a decent-sized bass!")
                print("\n")
                type.type("Fresh fish for dinner. You feel accomplished.")
                self.heal(20)
                self.restore_sanity(3)
            self.use_item("Fishing Line")
        else:
            type.type("You watch the fish swim by, tantalizingly close. If only you had something to catch them with...")
            print("\n")
            type.type("Your stomach rumbles.")
        print("\n")

    def robbery_attempt(self):
        # EVENT: Someone tries to break into your car at night
        # EFFECTS: Padlock protects (NOT consumed); Pocket Knife scares them;
        #          otherwise lose $50-200
        # COMPANION INTEGRATION: Lucky/protection companion scares off thief, danger_warning companions alert you
        type.type("There's someone trying to break into your car!")
        print("\n")
        
        # COMPANION: Protection check first
        protector = self._lists.has_companion_with_bonus(self, "protection")
        if protector and self.get_companion(protector)["status"] == "alive":
            comp_type = self.get_companion(protector).get("type", "")
            if "Dog" in comp_type:
                type.type(bright(protector) + " erupts into ferocious barking. Deep, loud, terrifying.")
                print("\n")
                type.type("The thief looks in the window and sees teeth. Lots of teeth.")
            else:
                type.type(bright(protector) + " goes absolutely berserk inside the car, making enough noise to wake the dead.")
            print("\n")
            type.type("The would-be thief sprints away like they've seen a ghost.")
            print("\n")
            type.type(green(protector + " scared off the thief! Guardian of the car."))
            self.pet_companion(protector)
            self.restore_sanity(3)
        elif self.has_item("Padlock"):
            type.type("But you secured everything with your " + magenta(bright("Padlock")) + "!")
            print("\n")
            type.type("The thief struggles with it for a minute, then gives up and runs off.")
            print("\n")
            type.type("Close call. The padlock saved you.")
            # Padlock doesn't get consumed - it's protection
        elif self.has_item("Pocket Knife"):
            type.type("You grab your " + magenta(bright("Pocket Knife")) + " and brandish it!")
            print("\n")
            type.type(quote("Back off!"))
            print("\n")
            type.type("The thief sees the blade glinting and decides you're not worth the trouble. They bolt.")
        else:
            loss = random.randint(50, 200)
            type.type("Before you can react, they grab some of your stuff and run!")
            print("\n")
            type.type("You lost " + green(bright("${:,}".format(loss))) + " worth of cash!")
            self.change_balance(-loss)
        print("\n")

    def photo_opportunity(self):
        # EVENT: Something beautiful happens that's worth capturing
        # EFFECTS: Disposable Camera = 5 sanity (10% chance consumed);
        #          otherwise 2 sanity from memory alone
        # Disposable Camera captures a moment
        type.type("You look through your windshield and something incredible catches your eye - a double rainbow, a deer and its fawn, the most beautiful scene you've ever seen.")
        print("\n")
        
        if self.has_item("Disposable Camera"):
            type.type("You grab your " + magenta(bright("Disposable Camera")) + " and start snapping!")
            print("\n")
            type.type("Click. Click. Click. You capture the moment forever.")
            print("\n")
            type.type("When you develop these someday, they'll be worth remembering.")
            self.restore_sanity(5)
            if random.randrange(10) == 0:
                type.type("You got the last shot on the roll. Camera's done.")
                self.use_item("Disposable Camera")
        else:
            type.type("You try to memorize every detail. But memories fade.")
            print("\n")
            type.type("If only you had a camera...")
            self.restore_sanity(2)
        print("\n")

    def classy_encounter(self):
        # EVENT: A rich person asks for directions
        # EFFECTS: Leather Gloves/Silk Handkerchief/Gold Chain/Pocket Watch = $100-300 tip;
        #          otherwise ignored rudely
        # Leather Gloves, Silk Handkerchief, Gold Chain help impress
        type.type("A fancy car pulls up next to yours. The window rolls down, revealing someone in expensive clothes.")
        print("\n")
        type.type(quote("Excuse me, could you direct me to the casino?"))
        print("\n")
        
        has_class = (self.has_item("Leather Gloves") or self.has_item("Silk Handkerchief") or 
                     self.has_item("Gold Chain") or self.has_item("Antique Pocket Watch"))
        
        if has_class:
            if self.has_item("Silk Handkerchief"):
                type.type("You dab your brow with your " + magenta(bright("Silk Handkerchief")) + " in a refined manner.")
            elif self.has_item("Antique Pocket Watch"):
                type.type("You casually check your " + magenta(bright("Antique Pocket Watch")) + ".")
            elif self.has_item("Leather Gloves"):
                type.type("You adjust your " + magenta(bright("Leather Gloves")) + " with casual elegance.")
            else:
                type.type("Your " + magenta(bright("Gold Chain")) + " catches their eye.")
            print("\n")
            type.type("They look at you with newfound respect.")
            print("\n")
            type.type(quote("Ah, a person of taste! Here, for your trouble."))
            print("\n")
            tip = random.randint(100, 300)
            type.type("They hand you " + green(bright("${:,}".format(tip))) + " and drive off.")
            self.change_balance(tip)
        else:
            type.type("You point them in the right direction. They barely acknowledge you before driving off.")
            print("\n")
            type.type("Not even a thank you. Typical rich people.")
        print("\n")

    def wine_and_dine(self):
        # EVENT: Bond with another car-dweller around a campfire
        # CONDITION: Requires Vintage Wine or Silver Flask
        # EFFECTS: Vintage Wine = 10 sanity + 10 HP (consumed); Silver Flask = 5 sanity
        # Vintage Wine or Silver Flask for special occasions
        if not self.has_item("Vintage Wine") and not self.has_item("Silver Flask"):
            self.day_event()
            return
        
        type.type("You step out of your car and meet someone interesting - another car-dweller, sharing stories around a small campfire.")
        print("\n")
        
        if self.has_item("Vintage Wine"):
            type.type("You pull out your " + magenta(bright("Vintage Wine")) + ".")
            print("\n")
            type.type(quote("1987? You've been holding onto this?"))
            print("\n")
            type.type("You share the bottle, swapping tales of better days and worse ones.")
            print("\n")
            type.type("By the time it's empty, you've made a real friend.")
            self.use_item("Vintage Wine")
            self.restore_sanity(10)
            self.heal(10)
        elif self.has_item("Silver Flask"):
            type.type("You offer a swig from your " + magenta(bright("Silver Flask")) + ".")
            print("\n")
            type.type("They accept gratefully. You share drinks and stories until the fire dies down.")
            self.restore_sanity(5)
        print("\n")

    def cigar_circle(self):
        # EVENT: Bond with locals at a barbershop using cigars
        # CONDITION: Requires Fancy Cigars item
        # EFFECTS: 5 sanity + 5 HP, get local knowledge (consumed)
        # Fancy Cigars for bonding
        if not self.has_item("Fancy Cigars"):
            self.day_event()
            return
        
        type.type("You step out of your car and find a group of older men sitting outside a barbershop, talking politics and sports.")
        print("\n")
        type.type("One of them eyes you suspiciously. You're clearly not from around here.")
        print("\n")
        type.type("You pull out your " + magenta(bright("Fancy Cigars")) + " and offer them around.")
        print("\n")
        type.type(quote("Cuban? Well, well. Maybe you're alright after all."))
        print("\n")
        type.type("You spend the afternoon smoking and talking. They give you tips on where to park safely, where to find cheap food.")
        print("\n")
        type.type("Local knowledge is priceless.")
        self.use_item("Fancy Cigars")
        self.restore_sanity(5)
        self.heal(5)
        print("\n")

    def need_fire(self):
        # EVENT: Desperately need fire for warmth/cooking/light
        # EFFECTS: Monogrammed Lighter works (not consumed); Lighter works 80% (may run out);
        #          Road Flares work (consumed); otherwise 10 damage + 3 sanity loss
        # Lighter or Monogrammed Lighter or Road Flares starts fire
        type.type("You're shivering in your car. You need fire. Desperately. Maybe to warm up, maybe to cook, maybe just to see.")
        print("\n")
        
        if self.has_item("Monogrammed Lighter"):
            type.type("You pull out your " + magenta(bright("Monogrammed Lighter")) + " and flick it open.")
            print("\n")
            type.type("Flame. Reliable, elegant flame. You get what you need done.")
            # Premium lighter doesn't run out
        elif self.has_item("Lighter"):
            type.type("You pull out your " + magenta(bright("Lighter")) + " and click it.")
            print("\n")
            if random.randrange(5) == 0:
                type.type("Click. Click. Click... it's out of fluid.")
                print("\n")
                type.type("Useless now.")
                self.use_item("Lighter")
            else:
                type.type("Flame. You get what you need done.")
        elif self.has_item("Road Flares"):
            type.type("You light one of your " + magenta(bright("Road Flares")) + ". It's overkill, but it works.")
            print("\n")
            type.type("The flare burns itself out. Not the most efficient use.")
            self.use_item("Road Flares")
        else:
            type.type("You have no way to make fire. You sit in the cold and dark.")
            self.hurt(10)
            self.lose_sanity(3)
        print("\n")

    def lucky_rabbit_encounter(self):
        # EVENT: A rabbit encounters you while you have a rabbit's foot
        # CONDITION: Requires Lucky Rabbit Foot item
        # EFFECTS: Adds "Lucky" status
        # Lucky Rabbit Foot triggers
        if not self.has_item("Lucky Rabbit Foot"):
            self.day_event()
            return
        
        type.type("You step out of your car for some fresh air and a rabbit hops across your path.")
        print("\n")
        type.type("It stops. Turns. Looks directly at you. Then at the purple " + magenta(bright("Lucky Rabbit Foot")) + " dangling from your pocket.")
        print("\n")
        type.type("For a long moment, you both stare.")
        print("\n")
        
        # Animal Whistle befriend with Carrot bonus
        if self.has_item("Animal Whistle") and not self.has_companion("Clover"):
            type.type("The " + magenta(bright("Animal Whistle")) + " around your neck begins to glow softly.")
            print()
            type.type("The rabbit's eyes widen. It hops closer, cautiously at first, then with more confidence.")
            print()
            if self.has_item("Carrot"):
                self.use_item("Carrot")
                type.type("You offer the " + magenta(bright("Carrot")) + ". The rabbit accepts it gently, then nuzzles your hand.")
                print()
            type.type("The rabbit sits beside you. This is no ordinary rabbit. This is luck incarnate.")
            print()
            self.add_companion("Clover", "Lucky Rabbit")
            self.add_status("Lucky")
            return
        
        type.type("The rabbit makes a sound that might be a sigh, then hops away.")
        print("\n")
        type.type("You feel... guilty? But also lucky. Definitely lucky.")
        self.add_status("Lucky")
        print("\n")

    def penny_luck(self):
        # EVENT: Find another lucky penny while carrying one
        # CONDITION: Requires Lucky Penny item
        # EFFECTS: Adds "Lucky" status
        # Lucky Penny effect
        if not self.has_item("Lucky Penny"):
            self.day_event()
            return
        
        type.type("Stepping out of your car, you're about to step on a crack in the sidewalk when something makes you pause.")
        print("\n")
        type.type("You look down. Another penny, heads up, right next to the crack.")
        print("\n")
        type.type("You pick it up. Now you have two lucky pennies... but you can only carry one.")
        print("\n")
        type.type("You flip your old " + magenta(bright("Lucky Penny")) + " into a fountain as an offering to whatever luck gods exist.")
        print("\n")
        type.type("The new penny feels luckier. Is that possible?")
        self.add_status("Lucky")
        print("\n")

    def rubber_band_save(self):
        # EVENT: Rubber bands save the day by holding things together
        # CONDITION: Requires Rubber Bands item
        # EFFECTS: 20% chance item is consumed
        # Rubber Bands have a use
        if not self.has_item("Rubber Bands"):
            self.day_event()
            return
        
        type.type("Something in your car is about to fall apart. A stack of papers. A bundle of bills. A bag that won't stay closed.")
        print("\n")
        type.type("You grab some " + magenta(bright("Rubber Bands")) + " from your stash.")
        print("\n")
        type.type("Snap. Snap. Snap. Everything's secured.")
        print("\n")
        type.type("Sometimes the simplest solutions are the best.")
        if random.randrange(5) == 0:
            type.type(" That was the last of them.")
            self.use_item("Rubber Bands")
        print("\n")

    # ==========================================
    # NEW CHEAP DAY EVENTS - Conditional
    # ==========================================
    
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
        print("\n")
        type.type("This isn't just a cold anymore. This is the flu.")
        print("\n")
        self.lose_status("Cold")
        self.add_status("Flu")
        self.mark_day("Flu")
        self.hurt(15)

    # ==========================================
    # NEW CHEAP DAY EVENTS - One-Time
    # ==========================================
    
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
        print("\n")
        type.type("An ice cream truck pulls up right next to your car. The driver, a heavyset man with a handlebar mustache, leans out the window.")
        print("\n")
        type.type(quote("You look like you could use some ice cream, friend! First one's on the house!"))
        print("\n")
        type.type("He hands you a rocket pop. You haven't had one since you were a kid.")
        print("\n")
        type.type("It tastes like summer. Like childhood. Like things were simpler.")
        print("\n")
        self.heal(15)
        type.type(quote("Keep your chin up! Life's too short not to have dessert!"))
        print("\n")
        type.type("The ice cream truck drives away, its jingle fading into the distance.")
        print("\n")

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
        print("\n")
        type.type(quote("Whoa... do you LIVE in your car? That's so COOL!"))
        print("\n")
        type.type("You're not sure 'cool' is the word you'd use, but okay.")
        print("\n")
        type.type(quote("I wish I could live in a car! No bedtime, no vegetables, no homework! You're living the DREAM, mister!"))
        print("\n")
        type.type("Before you can correct him, he pedals off, yelling about how he's going to tell his friends about the 'cool car guy.'")
        print("\n")
        type.type("You feel... strangely validated?")
        print("\n")
        self.heal(5)

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
        print("\n")
        type.type(quote("Excuse me! We're trying to find the highway? Our GPS died three towns ago!"))
        print("\n")
        type.type("You give them directions as best you can. The dad looks so relieved he might cry.")
        print("\n")
        type.type(quote("Thank you so much! Here, take this-for your trouble!"))
        print("\n")
        tip = random.randint(20, 50)
        type.type("He hands you " + green(bright("$" + str(tip))) + " before speeding off, kids still screaming.")
        self.change_balance(tip)
        print("\n")
        type.type("Good deed for the day: done.")
        print("\n")

    # ==========================================
    # SECRET EVENTS - CHEAP TIER  
    # ==========================================
    
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
        print("\n")
        type.type("The clouds are the same. The breeze is the same. Even the bird on that branch is the same.")
        print("\n")
        type.type("Deja vu? Or something more?")
        print("\n")
        type.type("A strange certainty washes over you: today, something significant will happen at the casino.")
        print("\n")
        self.add_status("Lucky")
        type.type(yellow(bright("You feel like the universe is trying to tell you something.")))
        print("\n")

    def exactly_1111(self):
        # SECRET EVENT: Make a wish with $1,111
        # TRIGGER: Balance must be exactly $1,111
        # EFFECTS: Random - heal 50 HP, or +$100-300, or "Lucky" status
        # SECRET - Triggers at exactly $1,111
        if self.get_balance() != 1111:
            self.day_event()
            return
        
        type.type("You count your money and realize you have exactly " + green(bright("$1,111")) + ". One-one-one-one. Make a wish.")
        print("\n")
        type.type("The moment feels charged, electric. Like the universe is listening.")
        print("\n")
        type.type("You close your eyes and make a wish.")
        print("\n")
        
        # Random positive effect
        effect = random.randrange(3)
        if effect == 0:
            type.type("A warm feeling spreads through your chest. ")
            type.type(yellow(bright("Your wish for health has been granted.")))
            self.heal(50)
        elif effect == 1:
            type.type("A gust of wind blows a crumpled bill against your window. Then another. Then another.")
            print("\n")
            bonus = random.randint(100, 300)
            type.type(yellow(bright("Your wish for wealth has been partially granted.")) + " " + green(bright("+${:,}".format(bonus))))
            self.change_balance(bonus)
        else:
            type.type("You feel luckier than you have in months.")
            type.type(yellow(bright("Your wish for fortune has been granted.")))
            self.add_status("Lucky")
        print("\n")

    # One-Time
    def turn_to_god(self):
        # EVENT: Father Ezekiel offers you a Bible and asks about your faith
        # ONE-TIME: Only happens once (checks "Ezekiel" met status)
        # EFFECTS: If accept, becomes religious (affects some events/dialogue)
        if self.has_met("Ezekiel"):
            self.day_event()
            return
        
        self.meet("Ezekiel")
        type.type("There's a knock on your window. You sit up to see a man holding a bible, wearing a cross on a chain around his neck.")
        print("\n")
        type.type(quote("Hello! I'm Father Ezekiel. You seem to be in a tough spot, living in your car? "))
        type.type(quote("I was just wondering if you wanted me to give you my copy of The Bible. "))
        type.type(quote("It has the word of God, and I hope it could help you understand that you aren't alone on this journey of life."))
        print()
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
        print("\n")
        type.type("And with that, Father Ezekiel walks down the road, and out of sight.")
        print("\n")
        return
    
    def hungry_cow(self):
        # EVENT: Betsy the cow demands money from you
        # ONE-TIME: Only happens once (checks "Betsy" met status)
        # EFFECTS: Feed $100 per moo (multiple times possible) until satisfied;
        #          Refuse = 40 damage + "Broken Leg" injury
        # CHAIN: Adds "Betsy Tractor" danger for future Betsy events
        if self.has_met("Betsy"):
            self.day_event()
            return
        
        self.meet("Betsy")
        self.add_danger("Betsy Tractor")
        type.type("Your whole car is shaking. As you jump up from your seat, you see a beautiful black and white cow, staring you down through your window. ")
        type.type("The cow moos at you aggressively, and you open the door. On its back is a note that reads 'This is Betsy. Betsy gets hungry. Please feed Betsy.'")
        print("\n")
        
        # Animal Whistle befriends Betsy
        if self.has_item("Animal Whistle") and not self.has_companion("Betsy"):
            type.type("The " + magenta(bright("Animal Whistle")) + " chimes. Betsy's aggressive moo turns into a gentle lowing.")
            print("\n")
            type.type("The cow approaches slowly, then... headbutts you gently. Affectionately. Like a giant, bovine cat.")
            print("\n")
            type.type("Betsy doesn't want your money. Betsy wants your friendship.")
            print("\n")
            type.type("You pat Betsy's head. She moos happily and settles down next to your wagon.")
            print("\n")
            type.type("You've befriended a cow. Her name is " + cyan(bright("Betsy")) + ", according to the note.")
            print("\n")
            type.type("Betsy will follow you around now, occasionally providing milk and existential cow wisdom.")
            self.add_companion("Betsy", "Cow")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            print("\n")
            return
        
        type.type("Betsy stares into your soul, then looks over at the seat next to you. It appears Betsy is interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy? ")
        while True:
            answer = ask.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You put a " + green(bright("$100")) + " dollar bill into Betsy's mouth. She chews it up, then spits it out in front of you.")
                self.change_balance(-100)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self._balance < 500):
                    type.type("Betsy moos, then smiles. She walks down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. She doesn't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then charges at you. She slams into your wagon hard, and your leg gets caught in the door. That hurt. Really, really bad.")
                print("\n")
                self.hurt(40)
                self.add_injury("Broken Leg")
                type.type("Betsy moos loudly, wags her tail, then walks down the road. Oh well.")
                break
        print("\n")

    # One-Time Conditional
    # DREAM SEQUENCES - CHEAP TIER
    def remember_rebecca(self):
        # DREAM EVENT: Tom's story - Part 1 of 3
        # NOW FIRES AT NIGHT — replaces day summary
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

    def dealers_anger(self):
        # DREAM EVENT: Frank's story - Part 1 of 3
        # NOW FIRES AT NIGHT — replaces day summary
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

    def casino_bar(self):
        # DREAM EVENT: Oswald's story - Part 1 of 3
        # NOW FIRES AT NIGHT — replaces day summary
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

    # Modest Day Events (10,000 - 100,000)
    # Everytime
    def left_door_open(self):
        # EVENT: Car door was left open all night
        # EFFECTS: 50% chance Spider danger, 17% chance Squirrel danger
        type.type("A chill runs through your entire body. ")
        type.type("Had the passenger door really been open all night? ")
        type.type("Hopefully nothing had gotten in. ")
        type.type("You reach over and close the door, just to be safe.")
        random_chance = random.randrange(6)
        if random_chance <= 2:
                self.add_danger("Spider")
        elif random_chance == 3:
                self.add_danger("Squirrel")
        print("\n")   

    # Conditional
    def another_spider_bite(self):
        # EVENT: Spider bites you again on the neck
        # CONDITION: Requires "Spider" danger, not already having "Spider Bite"
        # EFFECTS: Pest Control kills spider; adds "Spider Bite" status
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
        else:
            type.type("The spider, now out of reach, crawls off the seat and onto the floor. ")
            type.type("You stick your head out back, but you aren't sure where the spider went, or if it has a family nearby. This is unfortunate.")
        self.add_status("Spider Bite")
        self.mark_day("Spider Bite")
        print("\n")

    def squirrel_invasion(self):
        # EVENT: Squirrel got into your car and might bite you
        # CONDITION: Requires "Squirrel" danger, not having bite/rabies/companion
        # EFFECTS: Bag of Acorns befriends "Squirrelly" companion; otherwise bite + rabies chance
        if not self.has_danger("Squirrel") or self.has_status("Squirrel Bite") or self.has_status("Rabies") or self.has_item("Squirrely") or self.has_met("Squirrely"):
            self.day_event()
            return

        self.lose_danger("Squirrel")
        
        # Animal Whistle automatically befriends the squirrel without needing acorns
        if self.has_item("Animal Whistle") and not self.has_met("Squirrelly") and not self.has_met("Dead Squirrely"):
            type.type("Something is rummaging through your car. ")
            type.type("Looking in the backseat, you notice a little squirrel, chittering away.")
            print("\n")
            type.type("The " + magenta(bright("Animal Whistle")) + " sings softly. The squirrel stops, ears perked.")
            print("\n")
            type.type("The squirrel bounds over to you and climbs onto your shoulder, chattering excitedly. ")
            type.type("It finds an acorn in your hair (where did that come from?) and offers it to you.")
            print("\n")
            type.type("You've been adopted by a squirrel. You decide to call it " + cyan(bright("Squirrelly")) + ".")
            print("\n")
            type.type("Squirrelly will ride around in your car now, hiding acorns in increasingly creative places.")
            self.add_item("Squirrelly")
            self.add_companion("Squirrelly")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.mark_day("Squirrely Fed")
            print("\n")
            return
        
        if self.has_item("Bag of Acorns"):
            self.use("Bag of Acorns")
            type.type("Something is rummaging through your car. ")
            type.type("Looking in the backseat, you notice a little squirrel, chewing through your " + bright(magenta("Bag of Acorns")) + ". He looks pretty cute.")
            print("\n")
            if self.has_met("Dead Squirrely"):
                type.type("The squirrel notices you, and jumps from the bag, and over to your center console. ")
                type.type("He peers up at you, but your eyes are filled with tears. Nothing can ever replace Squirrely. ")
                type.type("You pick up the squirrel, open the door, and let it free.")
                print("\n")
                return
            else:
                type.type("The squirrel notices you, and jumps from the bag, and over to your center console. ")
                type.type("He peers up at you, with an acorn in hand, holding it up in your direction. ")
                type.type("You stick your hand out, and the squirrel gives you the acorn. This must be a sign of peace.")
                print("\n")
                type.type("After an hour of watching the squirrel eat the acorns, climb around your car, ")
                type.type("and jump from your arm to the dashboard over and over, you decide that this squirrel is now yours. ")
                type.type("You name him " + cyan(bright("'Squirrelly'")) + ", in honor of him being a squirrel.")
                print("\n")
                self.add_item("Squirrely")
                self.add_companion("Squirrelly")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                self.mark_day("Squirrely Fed")
                return
        else:
            type.type("A sharp pain shoots through your leg! ")
            type.type("You swing the hurt leg, and you watch as a squirrel goes flying into the air. ")
            type.type("The little rodent starts climbing around your car, scurrying around the walls, desperately trying to get out. ")
            type.type("You open the backseat windows, and the squirrel jumps out, and darts into the woods. Hopefully, that bite isn't too serious.")
            self.add_status("Squirrel Bite")
            random_chance = random.randrange(4)
            if random_chance == 1:
                self.add_status("Rabies")
                self.mark_day("Rabies")
            self.mark_day("Squirrel Bite")
            print("\n") 
            return
    
    # ==========================================
    # NEW MODEST DAY EVENTS - Everytime
    # ==========================================
    
    def street_performer(self):
        # Everytime - random encounter
        variant = random.randrange(4)
        if variant == 0:
            type.type("A man with a guitar sits down near your car and starts playing. He's actually pretty good.")
            print("\n")
            type.type("You listen for a while. When he finishes, you toss him a few bucks. He tips his hat and moves on.")
            self.change_balance(-random.randint(1, 5))
        elif variant == 1:
            type.type("A one-man-band contraption walks by-drums, harmonica, cymbals, the whole nine yards. The noise is incredible.")
            print("\n")
            type.type("He plays for exactly three minutes, then disappears around the corner. What a strange morning.")
        elif variant == 2:
            type.type("A magician approaches your car window and does a card trick. You have no idea how he did it.")
            print("\n")
            type.type(quote("Pick a card, any card!") + " he says. You pick the three of hearts.")
            print("\n")
            type.type("He makes it disappear, reappear in his mouth, then reveals it was in your pocket the whole time.")
            print("\n")
            type.type("Wait. How did he get it in your pocket?")
        else:
            type.type("A mime follows your car for three blocks. You finally shake him when you run a yellow light.")
            print("\n")
            type.type("Mimes are weird.")
        print("\n")

    def power_outage_area(self):
        # Everytime - atmospheric event
        variant = random.randrange(3)
        if variant == 0:
            type.type("The entire block goes dark. Power outage. The streetlights, the shops, everything.")
            print("\n")
            type.type("You sit in your car, watching people stumble around with flashlights, and feel strangely superior. You don't need electricity. You're already off the grid.")
        elif variant == 1:
            type.type("Traffic lights are out. An intersection nearby becomes chaos. Cars honking, people yelling.")
            print("\n")
            type.type("You watch the disaster unfold from the safety of your parked wagon. Entertainment.")
        else:
            type.type("A transformer explodes somewhere nearby. Sparks shower into the street.")
            print("\n")
            type.type("Beautiful, in a terrifying sort of way.")
        print("\n")

    def construction_noise(self):
        # Everytime - minor annoyance
        variant = random.randrange(3)
        if variant == 0:
            type.type("BANG BANG BANG. Construction starts at 6 AM. Right next to your car. Of course.")
            print("\n")
            type.type("You move to a different spot. The construction sounds follow you. Are they... expanding?")
        elif variant == 1:
            type.type("A jackhammer starts up nearby. Your teeth are literally vibrating.")
            print("\n")
            type.type("You cover your ears and wait for it to stop. It takes four hours.")
            self.hurt(5)
        else:
            type.type("The sound of a cement mixer becomes your alarm clock this morning. Not the most peaceful wake-up.")
            print("\n")
            type.type("At least they wave at you when they notice you're awake.")
        print("\n")

    # ==========================================
    # NEW MODEST DAY EVENTS - Conditional
    # ==========================================
    
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
        print("\n")
        type.type(quote("Word on the street is you've been meeting some interesting folks. The cowboy. The preacher. Even that crazy cow."))
        print("\n")
        type.type("He grins, showing missing teeth.")
        print("\n")
        type.type(quote("We've got a network, you know. Us street folks. We share info. And some of that info might be useful to someone in your... unique situation."))
        print("\n")
        type.type("He offers to tell you about a shortcut to the casino that avoids the main roads. Better for someone trying to stay under the radar.")
        print("\n")
        answer = ask.yes_or_no("Pay him $50 for the info? ")
        if answer == "yes":
            self.change_balance(-50)
            type.type("He pockets the money and tells you about a back road that cuts travel time significantly.")
            print("\n")
            type.type(quote("Good luck out there. We're all rooting for you."))
            self.add_item("Secret Route Map")
        else:
            type.type("He shrugs. " + quote("Your loss. The offer stands if you change your mind."))
        print("\n")

    # ==========================================
    # NEW MODEST DAY EVENTS - One-Time
    # ==========================================
    
    def the_photographer(self):
        # One-Time - documentary
        if self.has_met("The Photographer"):
            self.day_event()
            return
        
        self.meet("The Photographer")
        type.type("A woman with a professional camera approaches your car, clearly excited.")
        print("\n")
        type.type(quote("Hi! I'm doing a photo documentary on alternative lifestyles. Living in your car is EXACTLY the kind of story I'm looking for!"))
        print("\n")
        type.type("She's practically bouncing with enthusiasm.")
        print("\n")
        type.type(quote("Would you mind if I took some photos? I can pay you for your time!"))
        print("\n")
        answer = ask.yes_or_no("Allow the photoshoot? ")
        if answer == "yes":
            type.type("You pose with your wagon, trying to look dignified. She snaps dozens of photos.")
            print("\n")
            type.type(quote("These are PERFECT! The lighting, the composition, the story they tell!"))
            print("\n")
            type.type("She pays you " + green(bright("$200")) + " for your time.")
            self.change_balance(200)
            print("\n")
            type.type(quote("If this gets published, you might be famous! In a niche art magazine, anyway."))
        else:
            type.type(quote("Oh. Okay. I understand, privacy is important."))
            print("\n")
            type.type("She walks away, looking disappointed.")
        print("\n")

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
        print("\n")
        type.type("The owner leans out the window and spots you.")
        print("\n")
        type.type(quote("Hey! You been living in that car long? I see you parked here sometimes."))
        print("\n")
        type.type("Before you can answer, he's already preparing something.")
        print("\n")
        type.type(quote("Here. On the house. Everyone deserves a good meal."))
        print("\n")
        type.type("He hands you a massive burrito, overflowing with everything good in the world.")
        print("\n")
        type.type("It's the best thing you've eaten in months.")
        self.heal(30)
        print("\n")
        type.type(quote("Come by anytime. We look out for each other around here."))
        print("\n")

    # ==========================================
    # SECRET EVENTS - MODEST TIER
    # ==========================================
    
    def exactly_50000(self):
        # SECRET EVENT: Halfway to Rich celebration
        # TRIGGER: Balance must be exactly $50,000
        # EFFECTS: Heal 25 HP, pigeons applaud you
        # SECRET - Halfway to Rich
        if self.get_balance() != 50000:
            self.day_event()
            return
        
        type.type("Fifty thousand dollars. " + green(bright("$50,000")) + ". Halfway to the Rich tier.")
        print("\n")
        type.type("You never thought you'd see this much money in your life, let alone in the passenger seat of your car.")
        print("\n")
        type.type("A pigeon lands on your roof. Then another. Then five more. They coo in what sounds almost like... applause?")
        print("\n")
        type.type("The universe is weird sometimes.")
        print("\n")
        type.type(yellow(bright("The halfway point. The journey continues.")))
        self.heal(25)
        print("\n")

    # One-Time
            
    # One-Time Conditional
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
        print("\n")
        type.type("The man sees you, and walks up to you, with a clipboard in his hand.")
        print("\n")
        type.type(space_quote("You. You're awake. Good. You see this clipboard? It says you can't be here."))
        type.type("You begin to read the paper on the clipboard. It's a message, written in Comic Sans.")
        print("\n")
        type.type("It reads 'This offical message from the government and the military and the army says that you can't be here. ")
        type.type("That's right, you, the person reading this message right now, living on this land right here. ")
        type.type("It's not for you. It won't ever be for you. So, you can't live here. You need to move right now, or I'll be very very angry.'")
        print("\n")
        type.type(space_quote("Did you read it?"))
        answer = ask.yes_or_no(space_quote("Did you? Read it?"))
        if answer == "yes":
            type.type(quote("Good, so you know that all these powerful people want yo- are demanding that you move from where you're currently living, right this instant! "))
            type.type(quote("I'd suggest you do so. I certainly wouldn't want to upset the government."))
            print()
        elif answer == "no":
            type.type(quote("You didn't read it? Come on, I worked so hard on it. You really should read a clipboard with words on it if someone asks you to. "))
            type.type(quote("Regardless, it says that you need to move! Or the consequences will be scary!"))
            print()
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 25 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return

    # DREAM SEQUENCES - MODEST TIER
    def remember_nathan(self):
        # DREAM EVENT: Tom's story - Part 2 of 3
        # NOW FIRES AT NIGHT — replaces day summary
        # STORY: Vision of baby Nathan in nursery, fades when touched
        # EFFECTS: Advances tom_dreams to 2, player cries
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
        self.advance_tom_dreams()
        print("\n")

    def dealers_scar(self):
        # DREAM EVENT: Frank's story - Part 2 of 3
        # NOW FIRES AT NIGHT — replaces day summary
        # STORY: See Dealer's scarred face and jade green glass eye
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
        self.advance_frank_dreams()
        self.lose_sanity(random.choice([2, 3]))  # Disturbing dream drains sanity
        print("\n")

    def casino_table(self):
        # DREAM EVENT: Oswald's story - Part 2 of 3
        # NOW FIRES AT NIGHT — replaces day summary
        # STORY: Play blackjack against dealer who looks exactly like you
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
        self.lose_sanity(random.choice([3, 4]))  # Identity confusion severely drains sanity
        print("\n")
        type.type(yellow("The line between player and dealer feels blurrier than before."))
        self.advance_oswald_dreams()
        print("\n")
        
    # Rich Day Events (100,000 - 500,000)
    # Everytime
    def left_trunk_open(self):
        # EVENT: Trunk was left open all night
        # EFFECTS: 33% chance Rat danger, 33% chance Termite danger
        type.type("A cold draft fills the whole wagon. ")
        type.type("Had the trunk really been open all night? ")
        type.type("Hopefully nothing had gotten in. ")
        type.type("You get out of the car and close the trunk, just to be safe.")
        random_chance = random.randrange(6)
        if random_chance < 2:
                self.add_danger("Rat")
        elif random_chance < 4:
                self.add_danger("Termite")
        print("\n")    

    # Conditional
    def rat_bite(self):
        # EVENT: A rat bites your ankle and laughs at you
        # CONDITION: Requires "Rat" danger, not having rabies or existing bite
        # EFFECTS: Pest Control kills rat; lose 1-3 sanity, possible rabies
        if self.has_status("Rabies") or not self.has_danger("Rat") or self.has_status("Rat Bite"):
            self.day_event()
            return

        type.type("A sharp pain shoots through your ankle! ")
        type.type("You look down to see a skinny gray rat nibbling your foot. You kick at it, but the little rodent runs under the seat. ")
        print("\n")
        type.type("The rat jumps up onto your backseat, and begins to laugh at you. Now that's just cruel. This rat must be crazy.")
        print("\n")
        
        # Animal Whistle befriend the laughing rat
        if self.has_item("Animal Whistle") and not self.has_companion("Slick"):
            type.type("Wait. The " + magenta(bright("Animal Whistle")) + " vibrates against your chest.")
            print()
            type.type("The rat stops laughing. It tilts its head, looking at you with intelligent eyes.")
            print()
            type.type("Slowly, it approaches. Sniffs your hand. Then... climbs onto your shoulder.")
            print()
            type.type("This rat isn't crazy. It's brilliant. And it's yours now.")
            print()
            self.add_companion("Slick", "Clever Rat")
            self.lose_danger("Rat")
            return
        
        self.lose_sanity(random.choice([1, 2, 3]))  # A laughing rat? That's unsettling
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray the rat down. ")
            type.type("A cloud of white liquid covers the rat, and you watch as it spazzes out, and dies. ")
            type.type("Hopefully, that's it for your rat problems. Except for that bite. You might wanna get that checked out.")
        else:
            type.type("You jump at the seat towards the rat, but it sneaks back under the passenger seat, and you can't find it. ")
            type.type("That damn rat. Hopefully, the bite isn't too serious, but it's probably worth getting checked out.")
        self.add_status("Rat Bite")
        random_chance = random.randrange(2)
        if random_chance == 1:
            self.add_status("Rabies")
            self.mark_day("Rabies")
            self.lose_sanity(random.choice([2, 3]))  # Rabies infection further drains sanity
        self.mark_day("Rat Bite")
        print("\n") 
        return       
        

    def hungry_termites(self):
        random_choice = random.randrange(2)
        if (random_choice != 0) or not self.has_danger("Termite"):
            self.day_event()
            return

        # EVENT: Termites found eating your money pile
        # CONDITION: Must have "termite danger" status
        # EFFECTS: Lose 20-50% of balance to termite damage; Pest Control item can kill them
        type.type("A clicking sound. You look around-it's coming from your pile of money. ")
        type.type("You jump up to check your cash, and you find a termite eating away at your cash. ")
        if self.has_item("Pest Control"):
            self.kill_pests()
            type.type("You grab your " + magenta(bright("Pest Control")) + " and spray in the direction of the termite. ")
            type.type("A cloud of white liquid covers the termite, and you watch as it slows down, twitches, and dies. ")
            type.type("Hopefully, that's the end of your termite problems.")
        else:
            type.type("You attempt to swat it with your hand, but it falls under your car seat. ")
            type.type("You stick your head under the seat, but you aren't sure where the termite went, or if it has a family nearby. This is just brutal.")
        print("\n")
        type.type("The termite ate through a lot of your money. ")
        losses = int(self.get_balance() * (random.randint(20, 50)/100))
        type.type("You lost " + green(bright("${:,}".format(losses))) + ".")
        self.change_balance(-losses)

    # ==========================================
    # NEW RICH DAY EVENTS - Everytime
    # ==========================================
    
    def luxury_car_passes(self):
        # EVENT: Luxury cars pass by your wagon, reminding you of wealth disparity
        # EFFECTS: Mostly atmospheric; Rolls-Royce variant heals 5 HP if owner nods respectfully
        # Everytime - atmospheric event with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("A Lamborghini roars past your wagon, going at least twice the speed limit. The driver doesn't even glance at you.")
            print("\n")
            type.type("Must be nice. You count your own money pile. Someday, maybe.")
        elif variant == 1:
            type.type("A stretch limo cruises by slowly. Through the tinted windows, you swear you see someone pointing at your car and laughing.")
            print("\n")
            type.type("Okay, that stings a little.")
        elif variant == 2:
            type.type("A Ferrari parks right next to your wagon. The owner gets out, takes one look at your car, and moves his Ferrari further away.")
            print("\n")
            type.type("Rude. But also, fair.")
        else:
            type.type("A Rolls-Royce glides past like a ghost. For a moment, you lock eyes with the elderly man in the back seat.")
            print("\n")
            type.type("He nods at you. Just a simple nod. But it feels... respectful?")
            self.heal(5)
        print("\n")

    def paparazzi_mistake(self):
        # EVENT: Photographers/tourists mistake you for someone famous (or not)
        # EFFECTS: 5% rare chance to earn $1,000-3,000 from "exclusive interview"; otherwise just comedic
        # Everytime - comedic event with variants + rare
        rare_chance = random.randrange(100)
        
        if rare_chance < 5:  # 5% - Actually famous
            type.type("A van screeches to a halt. Photographers pour out, cameras flashing!")
            print("\n")
            type.type(quote("IT'S THEM! THE MYSTERIOUS GAMBLING LEGEND!"))
            print("\n")
            type.type("Wait, what? They... think you're famous?")
            print("\n")
            type.type("Before you can correct them, they're shoving microphones in your face, asking about your 'secrets to success.'")
            print("\n")
            type.type("You just roll with it. Why not?")
            print("\n")
            type.type("They leave you with a payment for an 'exclusive interview' you apparently just gave.")
            self.change_balance(random.randint(1000, 3000))
            print("\n")
            return
        
        variant = random.randrange(3)
        if variant == 0:
            type.type("Someone with a camera runs up to your window, snapping photos frantically.")
            print("\n")
            type.type(quote("Excuse me, are you-") + " They look at their phone. Then at you. " + quote("Oh. Sorry. Wrong car."))
            print("\n")
            type.type("They shuffle away, embarrassed. You're not sure whether to be relieved or insulted.")
        elif variant == 1:
            type.type("A group of tourists takes pictures of your wagon. You hear one say, " + quote("Authentic American poverty!"))
            print("\n")
            type.type("You're a tourist attraction now. Great.")
        else:
            type.type("Someone knocks on your window holding an autograph book. They take one look at your face and say, " + quote("Never mind."))
            print("\n")
            type.type("Ouch.")
        print("\n")

    def investment_opportunity(self):
        # EVENT: Scammers try to sell you fake investment opportunities
        # EFFECTS: Purely atmospheric - player wisely ignores all scam attempts
        # Everytime - risky event
        variant = random.randrange(3)
        if variant == 0:
            type.type("A man in a cheap suit approaches your car, waving a stack of papers.")
            print("\n")
            type.type(quote("Hey buddy! You look like someone who appreciates a good opportunity! How'd you like to get in on the ground floor of-"))
            print("\n")
            type.type("You roll up your window. He keeps talking through the glass.")
        elif variant == 1:
            type.type("Someone slides a business card under your windshield wiper. It says 'GUARANTEED RETURNS - NOT A SCAM.'")
            print("\n")
            type.type("The fact that it says 'NOT A SCAM' makes you think it's definitely a scam.")
        else:
            type.type("Your phone buzzes with a text from an unknown number: " + quote("Congratulations! You've been selected for an exclusive investment opportunity!"))
            print("\n")
            type.type("You delete it immediately. Street smarts.")
        print("\n")

    def expensive_taste(self):
        # EVENT: Temptations to spend money on luxury items (real estate, restaurants, jewelry)
        # EFFECTS: Atmospheric only - player resists spending and stays focused on the goal
        # Everytime - lifestyle creep event
        variant = random.randrange(3)
        if variant == 0:
            type.type("Sitting in your car, you catch yourself looking at real estate listings on your phone. Apartments that cost more per month than your entire life savings used to be.")
            print("\n")
            type.type("Snap out of it. You live in a car. Focus on the goal.")
        elif variant == 1:
            type.type("You see a fancy restaurant and your stomach growls. You could afford to eat there now. Probably.")
            print("\n")
            type.type("No. The casino money goes TO the casino. Stay disciplined.")
        else:
            type.type("A jewelry store window catches your eye. A gold watch gleams inside. You have the money...")
            print("\n")
            type.type("But you came here to win a million dollars, not spend the ones you have. Keep moving.")
        print("\n")

    def news_van(self):
        # EVENT: News crews appear near your car - might be covering you or something else
        # EFFECTS: Atmospheric tension; hints that your gambling exploits are becoming newsworthy
        # Everytime - media event with variants
        variant = random.randrange(4)
        if variant == 0:
            type.type("A news van pulls up near your spot. Your heart races-are they here for you?")
            print("\n")
            type.type("No. They're filming a story about a pothole two blocks away. You've never been so relieved about a pothole.")
        elif variant == 1:
            type.type("A reporter sets up right next to your car to do a live shot. You duck down and pray they don't pan the camera your way.")
            print("\n")
            type.type("They do. Your mom is definitely going to see this.")
        elif variant == 2:
            type.type("A news crew is interviewing locals. They approach you with a microphone.")
            print("\n")
            type.type(quote("Excuse me sir, do you have any thoughts on the local-"))
            print("\n")
            type.type("You're already driving away. No comments. No interviews. No paper trail.")
        else:
            type.type("The evening news is playing on a TV in a nearby shop window. The anchor is talking about 'the anonymous gambler making waves at local casinos.'")
            print("\n")
            type.type("Is that... you? That could be you.")
            print("\n")
            type.type("You're not sure how you feel about that.")
        print("\n")

    # ==========================================
    # NEW RICH DAY EVENTS - Conditional
    # ==========================================
    
    def wealth_anxiety(self):
        # EVENT: Nightmares and paranoia about losing your massive fortune
        # CONDITION: Balance must be > $200,000
        # EFFECTS: Lose 1-2 sanity; 50% chance take 10 damage from exhaustion, 50% chance heal 5 HP from calming down
        # Conditional - triggers only if balance > $200,000
        if self.get_balance() < 200000:
            self.day_event()
            return
        
        type.type("You sit up in your car, drenched in cold sweat. Nightmares about losing all your money.")
        print("\n")
        type.type("It's getting harder to sleep with this much cash just... sitting there. What if someone steals it? What if you lose it all in one bad night?")
        print("\n")
        type.type("The anxiety gnaws at you all morning. ")
        self.lose_sanity(random.choice([1, 2]))  # Money anxiety chips away at sanity
        print("\n")
        if random.randrange(2) == 0:
            type.type("You spend the day paranoid, jumping at every sound. It's exhausting.")
            self.hurt(10)
        else:
            type.type("But then you take a deep breath. You've come this far. You can go further. The money is a tool, not a burden.")
            self.heal(5)
        print("\n")

    def tax_man(self):
        # EVENT: IRS agent visits to question your unreported income (one-time)
        # CONDITION: Balance must be > $150,000 + 10% random chance + must not have met "Tax Man Visit"
        # EFFECTS: Tense encounter with choice to lie or stay silent; atmospheric threat of government attention
        # Conditional - triggers randomly when balance is high
        if self.get_balance() < 150000 or random.randrange(10) != 0:
            self.day_event()
            return
        
        if self.has_met("Tax Man Visit"):
            self.day_event()
            return
        
        self.meet("Tax Man Visit")
        type.type("A sedan with government plates pulls up. A man in a gray suit steps out, holding a clipboard.")
        print("\n")
        type.type(quote("Excuse me. I'm from the IRS. We've noticed some... unusual financial activity in this area."))
        print("\n")
        type.type("Your blood runs cold. He peers into your car at the pile of cash.")
        print("\n")
        type.type(quote("That's quite a sum you've got there. All reported income, I assume?"))
        print("\n")
        answer = ask.yes_or_no("Lie and say yes? ")
        if answer == "yes":
            type.type(quote("Mm-hmm.") + " He scribbles something on his clipboard. " + quote("Well, everything seems to be in order. For now."))
            print("\n")
            type.type("He hands you his card before driving away. You tear it up immediately.")
        else:
            type.type("You don't say anything. He sighs.")
            print("\n")
            type.type(quote("Look, I don't want to make this complicated. Just... keep your head down, okay? There are bigger fish to fry."))
            print("\n")
            type.type("He drives away. You let out a breath you didn't know you were holding.")
        print("\n")

    # ==========================================
    # NEW RICH DAY EVENTS - One-Time
    # ==========================================
    
    def the_rival(self):
        # EVENT: Meet Victoria, a professional gambler who sees you as competition
        # CONDITION: One-time event (must not have met "The Rival")
        # EFFECTS: Introduces recurring antagonist; foreshadows future conflict
        # CHAIN: Victoria storyline Part 1
        # One-Time - introduces a recurring antagonist
        if self.has_met("The Rival"):
            self.day_event()
            return
        
        self.meet("The Rival")
        type.type("A motorcycle pulls up next to your wagon. The rider-a woman in a leather jacket-removes her helmet and gives you an appraising look.")
        print("\n")
        type.type(quote("So. You're the one everyone's talking about. The car-dweller who's been cleaning up at the blackjack tables."))
        print("\n")
        type.type("She smirks.")
        print("\n")
        type.type(quote("I'm Victoria. I've been working these casinos for five years. Never seen anyone run as hot as you."))
        print("\n")
        type.type("She leans in, her eyes sharp.")
        print("\n")
        type.type(quote("Enjoy it while it lasts. The house always wins in the end. And if the house doesn't get you..."))
        print("\n")
        type.type("She revs her engine.")
        print("\n")
        type.type(quote("I will."))
        print("\n")
        type.type("She speeds off before you can respond. Something tells you this won't be the last you see of Victoria.")
        print("\n")

    def the_bodyguard_offer(self):
        # EVENT: Bruno, a massive bodyguard, offers protection services
        # CONDITION: One-time event (must not have met "Bodyguard Offer")
        # EFFECTS: Can hire for $50/day, adds "Bodyguard Bruno" item for protection
        # One-Time - protection event
        if self.has_met("Bodyguard Offer"):
            self.day_event()
            return
        
        self.meet("Bodyguard Offer")
        type.type("A massive man-easily six and a half feet tall and built like a tank-approaches your car.")
        print("\n")
        type.type(quote("Hey. You're the gambling guy, right? Word on the street is you've got a lot of cash on you."))
        print("\n")
        type.type("You tense up, ready for trouble. But he holds up his hands.")
        print("\n")
        type.type(quote("Easy. I'm not here to rob you. I'm here to offer my services. Protection. Fifty bucks a day and nobody messes with you."))
        print("\n")
        answer = ask.yes_or_no("Hire the bodyguard? ")
        if answer == "yes":
            type.type(quote("Smart choice. Name's Bruno. I'll be around."))
            print("\n")
            type.type("He settles into a spot nearby, looking menacing. You feel safer already.")
            self.add_item("Bodyguard Bruno")
            self.change_balance(-50)
        else:
            type.type(quote("Your loss. But if you change your mind, just holler. I'll hear you."))
            print("\n")
            type.type("He lumbers off. You hope you didn't just make a mistake.")
        print("\n")

    def high_roller_invitation(self):
        # EVENT: Casino management invites you to the VIP High Roller Lounge
        # CONDITION: One-time event (must not have met "High Roller Invite")
        # EFFECTS: Receive "VIP Invitation" item for higher stakes/better odds access
        # One-Time - casino event
        if self.has_met("High Roller Invite"):
            self.day_event()
            return
        
        self.meet("High Roller Invite")
        type.type("A man in an expensive suit approaches your wagon, holding an envelope.")
        print("\n")
        type.type(quote("Excuse me. I represent the casino management. We've noticed your... consistent performance at our tables."))
        print("\n")
        type.type("He hands you the envelope. Inside is an invitation to the 'VIP High Roller Lounge.'")
        print("\n")
        type.type(quote("Consider this a courtesy. Higher stakes. Better odds. Private tables. The high roller experience."))
        print("\n")
        type.type("He adjusts his cufflinks.")
        print("\n")
        type.type(quote("Of course, the minimum bet is considerably higher. But for someone of your... caliber, that shouldn't be a problem."))
        print("\n")
        type.type("He walks away, leaving you with the invitation. This could be interesting.")
        self.add_item("VIP Invitation")
        print("\n")

    def old_friend_recognition(self):
        # EVENT: Someone from your old life recognizes you and thought you were dead
        # CONDITION: One-time event (must not have met "Old Friend")
        # EFFECTS: Choice to tell truth (+$500 gift) or deny identity (emotional weight)
        # One-Time - emotional event
        if self.has_met("Old Friend"):
            self.day_event()
            return
        
        self.meet("Old Friend")
        type.type("Someone knocks on your window. You look up to see a vaguely familiar face-someone from your old life, before all this.")
        print("\n")
        type.type(quote("Holy shit... is that you? I thought you were dead! Everyone thought you were dead!"))
        print("\n")
        type.type("The memories come flooding back. A life you left behind. People who probably still wonder what happened to you.")
        print("\n")
        type.type(quote("What are you doing living in a CAR? What happened to you?"))
        print("\n")
        answer = ask.yes_or_no("Tell them the truth? ")
        if answer == "yes":
            type.type("You tell them everything. The gambling. The car. The dream of hitting a million dollars.")
            print("\n")
            type.type("They listen in silence, then shake their head slowly.")
            print("\n")
            type.type(quote("You always were a crazy one. Here-take this. For old times' sake."))
            print("\n")
            type.type("They press some money into your hand. " + green(bright("$500")) + ".")
            self.change_balance(500)
            print("\n")
            type.type(quote("Good luck. And... don't be a stranger, okay?"))
        else:
            type.type(quote("I think you've got the wrong person,") + " you say, looking away.")
            print("\n")
            type.type("They stare at you for a long moment, then shake their head and walk away.")
            print("\n")
            type.type("Some doors are better left closed.")
        print("\n")

    # ==========================================
    # SECRET EVENTS - RICH TIER
    # ==========================================
    
    def exactly_250000(self):
        # EVENT: Secret milestone - quarter million dollar celebration
        # CONDITION: Balance must be EXACTLY $250,000
        # EFFECTS: Golden butterfly leaves gold dust worth $1,000 + "Lucky" status
        # SECRET EVENT - Quarter million celebration
        if self.get_balance() != 250000:
            self.day_event()
            return
        
        type.type("You count your money for the third time. Exactly " + green(bright("$250,000")) + ". A quarter of a million dollars.")
        print("\n")
        type.type("A quarter of the way to your goal.")
        print("\n")
        type.type("As if the universe acknowledges this milestone, a golden butterfly lands on your dashboard. ")
        type.type("It sits there for a long moment, wings slowly opening and closing.")
        print("\n")
        type.type("Then it flies away, leaving a small pile of gold dust behind.")
        print("\n")
        type.type("Wait, that's real gold.")
        print("\n")
        self.change_balance(1000)
        type.type(yellow(bright("The universe rewards those who persist.")))
        self.add_status("Lucky")
        print("\n")

    def dealer_in_dreams(self):
        # DREAM EVENT: Frank dream chain COMPLETE — Dealer gives you the Joker
        # NOW FIRES AT NIGHT — replaces day summary
        # EFFECTS: Receive "Dealer's Joker" item
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

    # One-Time
    def grimy_gus_discovery(self):
        # EVENT: Meet Grimy Gus, a shady pawn shop owner who buys unusual items
        # CONDITION: One-time event (must not have met "Grimy Gus")
        # EFFECTS: Unlocks Grimy Gus's Pawn Emporium shop for selling collectibles
        # One-Time - Discover the pawn shop
        if self.has_met("Grimy Gus"):
            self.day_event()
            return
        
        self.meet("Grimy Gus")
        type.type("A sharp knock on your window. You look up to see a gaunt man ")
        type.type("in a stained trench coat peering at you through the glass. His teeth are yellow, his eyes are bloodshot, ")
        type.type("and he's holding a pocket watch that looks far too expensive for someone dressed like him.")
        print("\n")
        type.type("You roll down the window just a crack.")
        print("\n")
        type.type(quote("Nice pile of cash you got there,") + " he rasps, nodding at the money in your passenger seat. ")
        type.type(quote("You look like a collector. A finder of rare things."))
        print("\n")
        type.type("He glances around nervously, then leans closer.")
        print("\n")
        type.type(quote("Name's Gus. Grimy Gus, they call me. Got a little shop down on Fifth and Nowhere. "))
        type.type(quote("If you ever find yourself with... unusual items... things that don't belong in the light of day... I can make them disappear. For a fair price."))
        print("\n")
        type.type("He taps his nose conspiratorially.")
        print("\n")
        type.type(quote("Collectibles, trinkets, treasures. Things you picked up on your... adventures. I don't ask questions. Just cash on the barrel."))
        print("\n")
        type.type("He hands you a grimy business card through the crack in the window. It reads: " + cyan(bright("\"Grimy Gus's Pawn Emporium - We Buy What Others Won't\"")))
        print("\n")
        type.type(quote("Come by sometime. You won't regret it. Probably."))
        print("\n")
        type.type("He shuffles off into the morning mist before you can respond.")
        print("\n")
        type.type(yellow(bright("A new shop has been unlocked: Grimy Gus's Pawn Emporium")))
        print("\n")

            
    # One-Time Conditional
    def starving_cow(self):
        # EVENT: Betsy returns driving a tractor, demanding money or causing massive damage
        # CONDITION: Must have met "Betsy" AND have "Betsy Tractor" danger
        # EFFECTS: Feed Betsy $10k stacks until satisfied, or refuse and take 80 damage + "Fractured Spine" injury
        # CHAIN: Betsy storyline Part 2 - sets up "Betsy Army" danger for Part 3
        # One-Time Conditional
        if not self.has_met("Betsy") or not self.has_danger("Betsy Tractor"):
            self.day_event()
            return

        self.add_danger("Betsy Army")
        self.lose_danger("Betsy Tractor")
        type.type("The sound of a tractor barrels closer. As you jump up from your seat, you see the tractor getting closer to your wagon. ")
        type.type("The tractor drives beside your vehicle, and pushes right up against you, grinding the paint off your car. That's just mean. ")
        print("\n")
        type.type("You look up at the driver to see a beautiful black and white cow. Good god, it's Betsy. Why, Betsy, why. ")
        type.type("The cow moos at you aggressively, and you roll down the window. ")
        print("\n")
        type.type("Betsy stares into your soul, then looks over at the seat next to you. It appears Betsy is interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy? ")
        while True:
            answer = ask.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You reach out your window, and put a stack of bills, worth " + green(bright("$10,000")) + " into Betsy's mouth. ")
                type.type("She chews them up, then spits them out into your wagon.")
                self.change_balance(-10000)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self._balance <50000):
                    type.type("Betsy moos, then smiles. She pulls away from the car, and drives the tractor down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. She doesn't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then backs the tractor up. She then proceeds to step on the gas, ")
                type.type("and drives the tractor forward at your vehicle, slamming into the front of your wagon hard. ")
                type.type("She moos and moos and moos, pushing your car further back. ")
                type.type("The jolt of the vehicles smashing into each other kills, and your spine begins to fracture.")
                print("\n")
                self.hurt(80)
                self.add_injury("Fractured Spine")
                type.type("Betsy laughs a laugh, almost maniacal, before driving the tractor down the road.")
                break
        print("\n")

    # Doughman Days (500,000 - 900,000)
    # Everytime
    def thunderstorm(self):
        # EVENT: Major thunderstorm traps you in your car for the day
        # EFFECTS: Adds "Rain" travel restriction, preventing casino travel
        self.add_travel_restriction("Rain")
        # Alt dialogue for repeated event
        variant = random.randrange(3)
        if variant == 0:
            type.type("Raindrops begin hitting the roof of your wagon. ")
            type.type("It starts with a couple, then a few, and before you even get the chance to stretch, it begins to pour. ")
            type.type("The sky is a dark, dark gray, and streams start to form along the road.")
            print("\n")
            type.type("The pitter-patter of the rain on your car lulls you back to sleep. ")
            type.type("When a strike of lightning wakes you once more, you look out the windows to see a few inches of rain covering the street. ")
            type.type("Welp, there goes your plans for the day.")
        elif variant == 1:
            type.type("Thunder. BOOM. You're awake now.")
            print("\n")
            type.type("Rain hammers the roof like it's trying to break through. Lightning illuminates the sky every few seconds. It's biblical out there.")
            print("\n")
            type.type("You're not going anywhere today.")
        else:
            type.type("The storm came out of nowhere. One minute, clear skies. The next, your car is being pelted by rain and hail.")
            print("\n")
            type.type("You watch a trash can blow down the street like a tumbleweed. Nature is angry today.")
        print("\n")
        return
    
    # ==========================================
    # NEW DOUGHMAN DAY EVENTS - Everytime
    # ==========================================
    
    def high_stakes_feeling(self):
        # EVENT: Internal monologue about the weight and thrill of having $500k+
        # EFFECTS: Atmospheric only - builds tension as you approach the million dollar goal
        # Everytime - internal monologue
        variant = random.randrange(4)
        if variant == 0:
            type.type("You sit up in your car and feel it immediately: today is going to be big. Good or bad, you're not sure. But BIG.")
            print("\n")
            type.type("Half a million dollars sits next to you. More money than most people save in a decade. And you're going to risk it. Again.")
            print("\n")
            type.type("The thought should terrify you. Instead, it excites you.")
        elif variant == 1:
            type.type("You count your money. Then count it again. It's real. It's all real.")
            print("\n")
            type.type("Sometimes you still can't believe you've made it this far. A homeless gambler with half a million dollars.")
            print("\n")
            type.type("What a world.")
        elif variant == 2:
            type.type("The morning light catches your pile of cash and it almost glows. All those hours at the tables. All those wins. All those near-misses.")
            print("\n")
            type.type("This is what it's all been building to.")
        else:
            type.type("You feel like you're in the final act of a movie. The climax is coming. You can feel it in your bones.")
            print("\n")
            type.type("Whether it's a happy ending or a tragedy... well. That's up to you.")
        print("\n")

    def casino_security(self):
        # EVENT: Security cars and surveillance suggest you're being watched
        # EFFECTS: Atmospheric paranoia - hints that the casino is tracking your wins
        # Everytime - paranoia event
        variant = random.randrange(3)
        if variant == 0:
            type.type("A security car does a slow drive-by. The guard makes eye contact with you, holds it for a beat too long, then drives on.")
            print("\n")
            type.type("They're watching you. You can feel it.")
        elif variant == 1:
            type.type("You spot the same car parked across the street three days in a row. Different driver each time.")
            print("\n")
            type.type("Coincidence? You're not sure you believe in coincidences anymore.")
        else:
            type.type("Your phone gets a notification: 'Someone tried to access your location.' You don't remember giving anyone permission.")
            print("\n")
            type.type("You turn off location services. Paranoid? Maybe. But you didn't get this far by being careless.")
        print("\n")

    def wealthy_doubts(self):
        # EVENT: Existential thoughts about why you're still gambling and what comes after
        # EFFECTS: Atmospheric psychological reflection on greed, pride, and purpose
        # Everytime - psychological event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You're sitting in your car, staring at nothing. You could stop now. Walk away with over half a million dollars. Live comfortably for years.")
            print("\n")
            type.type("But that's not why you're here.")
            print("\n")
            type.type("You're here for a million. Nothing less will do.")
        elif variant == 1:
            type.type("What are you even going to DO with a million dollars? Buy a house? Invest? Travel?")
            print("\n")
            type.type("You realize you've been so focused on the goal, you never thought about what comes after.")
            print("\n")
            type.type("Something to think about. After you win.")
        else:
            type.type("Is it greed that keeps you going? Or pride? Or something else entirely?")
            print("\n")
            type.type("You've spent so long chasing this dream, you're not sure you'd know what to do without it.")
        print("\n")

    def people_watching(self):
        # EVENT: Observing regular people and their money problems while you sit on $500k+
        # EFFECTS: One variant costs $20 (giving money to homeless); otherwise atmospheric
        # Everytime - observation event
        variant = random.randrange(4)
        if variant == 0:
            type.type("Through your car window, you watch a businessman walk by, talking loudly on his phone about a 'big deal' worth $50,000.")
            print("\n")
            type.type("You have ten times that in your car. The thought makes you smile.")
        elif variant == 1:
            type.type("A couple argues about money outside a restaurant. Something about not being able to afford the bill.")
            print("\n")
            type.type("You could pay that bill a thousand times over. But you don't. That's not what the money is for.")
        elif variant == 2:
            type.type("A homeless man asks you for change. You give him a twenty.")
            print("\n")
            type.type("He looks at you like you're crazy. You probably are.")
            self.change_balance(-20)
        else:
            type.type("You watch people come and go from the casino across the street. Winners celebrating. Losers sulking.")
            print("\n")
            type.type("Tonight, you'll be one of them. You know which one you're betting on.")
        print("\n")

    # ==========================================
    # NEW DOUGHMAN DAY EVENTS - Conditional
    # ==========================================
    
    def the_temptation(self):
        # EVENT: Real estate agent tries to convince you to buy a home instead of gambling
        # CONDITION: Balance must be > $600,000 + 33% random chance
        # EFFECTS: Atmospheric temptation; player stays focused on the million dollar goal
        # Conditional - balance specific
        if self.get_balance() < 600000:
            self.day_event()
            return
        
        if random.randrange(3) != 0:
            self.day_event()
            return
        
        type.type("A real estate agent knocks on your window.")
        print("\n")
        type.type(quote("Excuse me! I couldn't help but notice you've been living here for a while. "))
        type.type(quote("Did you know that with your... apparent savings... you could afford a nice apartment? Maybe even a house?"))
        print("\n")
        type.type("They slide a business card through the crack in your window.")
        print("\n")
        type.type(quote("Think about it! " + green(bright("${:,}".format(self.get_balance()))) + " could buy you a real home! A real life!"))
        print("\n")
        type.type("They walk away, leaving you with their card and a nagging thought.")
        print("\n")
        type.type("A real home. A real life. Is that what you want? Or do you want the million?")
        print("\n")
        type.type("You crumple the card and throw it away. You know the answer.")
        print("\n")

    # ==========================================
    # NEW DOUGHMAN DAY EVENTS - One-Time
    # ==========================================
    
    def the_veteran(self):
        # EVENT: Old gambler shares his cautionary tale - got to $800k then lost it all in one night
        # CONDITION: One-time event (must not have met "The Veteran")
        # EFFECTS: Wisdom and warning; atmospheric foreshadowing of potential failure
        # One-Time - wisdom NPC
        if self.has_met("The Veteran"):
            self.day_event()
            return
        
        self.meet("The Veteran")
        type.type("An old man shuffles up to your car. His clothes are worn but clean. His eyes are sharp.")
        print("\n")
        type.type(quote("You're the one, aren't you? The gambler everyone's talking about."))
        print("\n")
        type.type("He leans against your car with a sigh.")
        print("\n")
        type.type(quote("I used to be like you. Thirty years ago. Had a system. Thought I could beat the house."))
        print("\n")
        type.type("He's quiet for a moment.")
        print("\n")
        type.type(quote("Got up to eight hundred thousand. Then lost it all in one night. Pride. Impatience. Stupidity. Take your pick."))
        print("\n")
        type.type(quote("You've got further than I ever did. Don't make my mistakes."))
        print("\n")
        type.type("He pats your car and walks away, disappearing into the crowd.")
        print("\n")
        type.type(yellow("His words echo in your mind."))
        print("\n")

    def the_journalist(self):
        # EVENT: Tribune journalist wants to interview you about your gambling career
        # CONDITION: One-time event (must not have met "The Journalist")
        # EFFECTS: Grant interview = earn $300; decline = no reward
        # One-Time - media attention
        if self.has_met("The Journalist"):
            self.day_event()
            return
        
        self.meet("The Journalist")
        type.type("A woman with a notepad and recorder approaches your car.")
        print("\n")
        type.type(quote("Hi! I'm writing a piece on professional gamblers for the Tribune. Mind if I ask you a few questions?"))
        print("\n")
        answer = ask.yes_or_no("Grant the interview? ")
        if answer == "yes":
            type.type("You tell her your story. The car, the casino, the dream of a million dollars.")
            print("\n")
            type.type("She scribbles furiously, eyes wide.")
            print("\n")
            type.type(quote("This is incredible! The readers are going to love this!"))
            print("\n")
            type.type("She pays you " + green(bright("$300")) + " for the interview and promises to send you a copy when it's published.")
            self.change_balance(300)
        else:
            type.type(quote("I understand. Privacy is important."))
            print("\n")
            type.type("She walks away, looking disappointed.")
        print("\n")

    def the_offer_refused(self):
        # EVENT: Casino floor manager offers VIP treatment in exchange for exclusive play
        # CONDITION: One-time event (must not have met "Casino Manager")
        # EFFECTS: Accept = "Casino VIP Card" item; Decline = make an enemy of the casino
        # One-Time - casino pressure
        if self.has_met("Casino Manager"):
            self.day_event()
            return
        
        self.meet("Casino Manager")
        type.type("A man in an expensive suit knocks on your window. His smile doesn't reach his eyes.")
        print("\n")
        type.type(quote("Good morning. I'm the floor manager at the casino. We've noticed your... impressive winning streak."))
        print("\n")
        type.type("He clasps his hands together.")
        print("\n")
        type.type(quote("I've been authorized to offer you a complimentary room at our hotel. Free meals. Free drinks. VIP treatment."))
        print("\n")
        type.type("His smile widens.")
        print("\n")
        type.type(quote("All we ask is that you continue playing at OUR tables. Exclusively."))
        print("\n")
        answer = ask.yes_or_no("Accept the VIP treatment? ")
        if answer == "yes":
            type.type(quote("Excellent! We'll have everything arranged. Welcome to the family."))
            print("\n")
            type.type("He hands you a VIP keycard. You feel like you've just made a deal with the devil.")
            self.add_item("Casino VIP Card")
        else:
            type.type("His smile falters, just for a second.")
            print("\n")
            type.type(quote("I see. Well, the offer stands if you change your mind."))
            print("\n")
            type.type("He walks away. You get the feeling you've just made an enemy.")
        print("\n")

    # ==========================================
    # SECRET EVENTS - DOUGHMAN TIER
    # ==========================================
    
    def exactly_777777(self):
        # EVENT: Secret milestone - lucky sevens celebration (six 7s in a row)
        # CONDITION: Balance must be EXACTLY $777,777
        # EFFECTS: "Lucky" status + heal 30 HP; slot machine jackpot sounds in distance
        # SECRET EVENT - Lucky sevens
        if self.get_balance() != 777777:
            self.day_event()
            return
        
        type.type("You count your money. " + green(bright("$777,777")) + ". All sevens.")
        print("\n")
        type.type("Seven is the luckiest number. Everyone knows that.")
        print("\n")
        type.type("And you have six of them.")
        print("\n")
        type.type("The air around you seems to shimmer. A slot machine somewhere in the distance hits a jackpot-you can hear the bells.")
        print("\n")
        type.type("This is a sign. It has to be.")
        print("\n")
        self.add_status("Lucky")
        self.heal(30)
        type.type(yellow(bright("Lucky sevens. The universe is on your side.")))
        print("\n")

    # Conditional
            
    # One-Time
    def likely_death(self):
        # EVENT: Gunman threatens to kill you unless you pay him off - Russian roulette
        # CONDITION: One-time event (must not have met "Gunman")
        # EFFECTS: Lose 4-6 sanity immediately; must pay to reduce death % from 80%; refuse = high chance of instant death
        # BRUTAL: Can cause death by "Gunshot to the Head"
        # One-Time
        if self.has_met("Gunman"):
            self.day_event()
            return
        
        self.meet("Gunman")
        self.lose_sanity(random.choice([4, 5, 6]))  # Near-death experience severely drains sanity
        type.type("A gunshot rings out. You sit up, scanning the area. ")
        type.type("As you look out your windshield, you see a figure, in a black trench coat. ")
        type.type("He walks to the front window, and beckons for you to roll it down. ")
        type.type("As you crank the window lower, he peers his head inside. ")
        type.type("You can smell the food between his teeth, and the alcohol on his breath. ")
        type.type("He has a gun in his hand, and he points it at you.")
        print("\n")
        percentage = 80
        type.type(quote("I'd say there's about an " + red(bright("80%")) + " chance that I blow your brains out. Right now. Wanna change that?") + " ")
        while True:
            answer = ask.yes_or_no("You gonna answer me? ")
            if answer == "yes":
                type.type("You nod your head, knowing exactly what he wants. As your hand shakes, you reach into your pocket. How much money do you give him? ")
                value = ask.give_cash(self.get_balance(), "How much money do you give him? ")
                if value == 0:
                    type.type("You tell him that you don't have any money left. A dissapointed look crosses his face.")
                    print("\n")
                    answer = "no"
                elif value == self.get_balance():
                    type.type("You hand him all of your money. He laughs, and pushes the gun against your forehead. " + quote("Night night, kiddo."))
                    type.slow(red(bright("The gunman pulls the trigger, and you hear a click, followed by a loud ringing in your ears, and a warm liquid dripping down your face. You reach up, and feel a hole in your skull, blood pouring out of it. You try to scream, but you can't. You can't even breathe. You fall to the ground, and everything goes black.")))
                    self.kill("Gunshot to the Head")
                else:
                    type.type("You hand him " + green(bright("${:,}".format(value))) + ".")
                    percentage -= int((value / self.get_balance()) * 100)
                    self.change_balance(-value)
                    if percentage <= 0:
                        type.type("He smiles, and puts the gun down. He laughs, and walks away, leaving you quite poor, but still alive.")
                        print("\n")
                        self.lose_sanity(random.choice([1, 2]))  # Surviving still leaves a mark
                        return
                    if percentage in (8, 18):
                        type.type(quote("Okay, now it's about an " + red(bright(str(percentage) + "%")) + " chance that I blow your brains out. Want that even lower?") + " ")
                    else: type.type(quote("Okay, now it's about a " + red(bright(str(percentage) + "%")) + " chance that I blow your brains out. Want that even lower?") + " ")
            elif answer == "no":
                type.type(quote("Okay, welp, guess we're gonna go gambling!") + " He laughs, and pushes the gun against your forehead. ")
                type.type("You can feel the cold metal against your skin, sweat dripping off the barrel, and into your eyes. ")
                type.type("You close them. Breathing in, slowly breathing out, you prepare for the worst. ")
                type.type("Not that you've ever been scared to face the odds.")

                print("\n")
                if random.randrange(100) > percentage:
                    type.slow(red(bright("The gunman pulls the trigger, and you hear a click.")))
                    type.type(" You open your eyes, and see that the gun is empty. He laughs, and puts the gun down. He walks away. Somehow, you're still alive. What a nightmare")
                    print("\n")
                    self.lose_sanity(random.choice([2, 3, 4]))  # Surviving Russian roulette leaves a mark
                    return
                else:
                    type.slow(red(bright("The gunman pulls the trigger, and you hear a click, followed by a loud ringing in your ears, and a warm liquid dripping down your face. You reach up, and feel a hole in your skull, blood pouring out of it. You try to scream, but you can't. You can't even breathe. You fall to the ground, and everything goes black.")))
                    self.kill("Gunshot to the Head")
            
    # One-Time Conditional
    def even_further_interrogation(self):
        # EVENT: The interrogator returns with a fake FBI/CIA badge demanding you move
        # CONDITION: Must have met "Interrogator" AND have "Even Further Interrogation" danger
        # EFFECTS: Removes "Even Further Interrogation" danger, adds "Final Interrogation" danger
        # CHAIN: Interrogation storyline Part 3
        # One-Time Conditional
        if not self.has_met("Interrogator") or not self.has_danger("Even Further Interrogation"):
            self.day_event()
            return

        self.lose_danger("Even Further Interrogation")
        self.add_danger("Final Interrogation")
        type.type("Through the windshield, a car is parked right in front of you. ")
        type.type("Not this again. As you open the door and get out of your car, ")
        type.type("you notice the man in his bright red suit, once again peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you, with a badge in his hand.")
        print("\n")
        type.type(space_quote("You. You're awake. Good. You see this badge? It says I have the authority to make you not live here."))
        type.type("You look at the badge. It's a piece of paper, colored gold, with the letters 'FBI' and 'CIA' written in pencil.")
        print("\n")
        type.type(quote("See? I'm allowed to make you leave. And I'm invoking my right to do this right now!"))
        print("\n")
        type.type(space_quote("Are you gonna leave?"))
        answer = ask.yes_or_no(space_quote("Are you? Gonna leave?"))
        if answer == "yes":
            type.type(quote("Good, you better do what I say, I'm super powerful. "))
            type.type(quote("I hope you actually move and stop living here, because it's really getting on my nerves. "))
            type.type(quote("I'll be back to make sure you do it, mark my words."))
            print()
        elif answer == "no":
            type.type(quote("What? But you have to! This badge says so! You better listen to me, because I'm really starting to get upset. "))
            type.type(quote("I'll be back, and if you haven't moved yet, I'll make you, mark my words."))
            print()
        type.type("After the man tells you this, he looks up, and stares at the sun. And after about 30 seconds, he rubs his eyes, walks back to his car, and drives off.")
        print("\n")
        return

    # DREAM SEQUENCES - DOUGHMAN TIER
    def remember_johnathan(self):
        # DREAM EVENT: Tom's story - Part 3 of 3
        # NOW FIRES AT NIGHT — replaces day summary
        # EFFECTS: Advances Tom dreams to 3; profound revelation of player's true identity
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

    def dealers_revolver(self):
        # DREAM EVENT: Frank's story - Part 3 of 3
        # NOW FIRES AT NIGHT — replaces day summary
        # EFFECTS: Escalating tension with the Dealer; he reaches for his revolver
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

    def casino_riches(self):
        # DREAM EVENT: Oswald's story - Part 3 of 3
        # NOW FIRES AT NIGHT — replaces day summary
        # EFFECTS: Advances Oswald dreams to 3; tempting vision of eternal wealth
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
        
    # Nearly There Days (900,000+)
    # ==========================================
    # NEW NEARLY DAY EVENTS - Everytime
    # ==========================================
    
    def almost_there(self):
        # EVENT: Motivational morning reflections as you approach the million dollar goal
        # EFFECTS: Atmospheric tension and hope; counting money obsessively
        # Everytime - motivational event with variants
        variant = random.randrange(5)
        if variant == 0:
            type.type("You count your money. Again. Just to make sure it's real.")
            print("\n")
            type.type(green(bright("${:,}".format(self.get_balance()))) + ". So close to a million dollars. So close to freedom.")
            print("\n")
            type.type("Your hands shake a little as you put the money back. Not from fear. From anticipation.")
        elif variant == 1:
            type.type("The morning sun hits your pile of money and it almost glows. All those bills. All that progress.")
            print("\n")
            type.type("You've come so far. From nothing to... almost everything.")
            print("\n")
            type.type("One more good night. Maybe two. That's all it'll take.")
        elif variant == 2:
            type.type("You stare at your reflection in the rearview mirror. Dark circles under your eyes. Hair a mess. But there's something else there too.")
            print("\n")
            type.type("Hope. You see hope.")
            print("\n")
            type.type("The finish line is in sight.")
        elif variant == 3:
            type.type("You dream about what you'll do with a million dollars. A real house. A real bed. Real food that doesn't come from a gas station.")
            print("\n")
            type.type("But first, you have to actually WIN it. No counting chickens before they hatch.")
        else:
            type.type("Your phone buzzes. A notification: 'Motivational quote of the day: Success is not final, failure is not fatal.'")
            print("\n")
            type.type("You stare at it for a long moment. Then delete it. You don't need motivational quotes. You need one more win.")
        print("\n")

    def the_weight_of_wealth(self):
        # EVENT: Paranoid behaviors as you guard nearly a million dollars
        # EFFECTS: One variant causes 5 damage from sleep deprivation; otherwise atmospheric
        # Everytime - paranoia event
        variant = random.randrange(4)
        if variant == 0:
            type.type("You've moved your parking spot three times today. Just in case someone was watching yesterday.")
            print("\n")
            type.type("Paranoia? Maybe. But you're sitting on almost a million dollars in a car. A little paranoia seems reasonable.")
        elif variant == 1:
            type.type("Every person who walks by makes you tense up. Are they looking at your car? Do they know what's inside?")
            print("\n")
            type.type("Probably not. But probably isn't definitely.")
        elif variant == 2:
            type.type("You've started sleeping in shifts. An hour here, an hour there. Never fully unconscious. Never truly rested.")
            print("\n")
            type.type("The money has made you rich in cash and poor in sleep.")
            self.hurt(5)
        else:
            type.type("A car parks nearby. You watch it for an hour. Nothing happens. They were just parking.")
            print("\n")
            type.type("You really need to relax. But how can you relax with this much at stake?")
        print("\n")

    def casino_knows(self):
        # EVENT: Signs that the casino is watching/tracking your winning streak
        # EFFECTS: Atmospheric ominous tension; black SUVs, mysterious calls, security guards
        # Everytime - ominous event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You notice a black SUV drive past your wagon. Slowly. Too slowly.")
            print("\n")
            type.type("The windows are tinted. You can't see who's inside. It doesn't stop. But it comes by twice more throughout the day.")
            print("\n")
            type.type("The casino knows. They have to know.")
        elif variant == 1:
            type.type("Your phone rings from an unknown number. You answer cautiously.")
            print("\n")
            type.type("Silence. Then, a click. They hung up.")
            print("\n")
            type.type("Wrong number? Or something else?")
        else:
            type.type("There's a new security guard at the casino entrance. He watches you enter. Watches you leave. Takes notes on a clipboard.")
            print("\n")
            type.type("Maybe it's nothing. Maybe it's everything.")
        print("\n")

    def last_stretch(self):
        # EVENT: The final stretch before hitting $1 million
        # EFFECTS: 33% chance to heal 10 HP from inner peace; otherwise just tension
        # Everytime - tension building
        type.type("You sit in your car and exhale. This is it. The final stretch. Everything you've worked for comes down to these last few nights.")
        print("\n")
        type.type("Your entire body feels electric. Every nerve is alive. This is what you were born to do.")
        print("\n")
        if random.randrange(3) == 0:
            type.type("A calm settles over you. Whatever happens, happens. You've done everything you can.")
            self.heal(10)
        else:
            type.type("But the pressure... the pressure is immense. One wrong move and it all comes crashing down.")
        print("\n")

    def strange_visitors(self):
        # EVENT: Mysterious people appear around your car with cryptic behavior
        # EFFECTS: Atmospheric surreal encounters; hints at supernatural awareness of your journey
        # Everytime - mysterious encounters
        variant = random.randrange(4)
        if variant == 0:
            type.type("A man in a white suit walks past your car, tips his hat, and keeps walking. You've never seen him before.")
            print("\n")
            type.type("Something about his smile was wrong. Too knowing.")
        elif variant == 1:
            type.type("Two women in matching pantsuits photograph your license plate. When you confront them, they claim to be 'researchers.'")
            print("\n")
            type.type("They refuse to elaborate. Then they're gone.")
        elif variant == 2:
            type.type("A child peers through your window. You didn't hear them approach.")
            print("\n")
            type.type(quote("My daddy says you're going to win,") + " they whisper. Then they run away.")
            print("\n")
            type.type("Who is their daddy? How does he know? WHAT does he know?")
        else:
            type.type("You wake up to find a single rose on your windshield. Red. Perfect. No card.")
            print("\n")
            type.type("Is this romantic? Threatening? You genuinely can't tell.")
        print("\n")

    # ==========================================
    # NEW NEARLY DAY EVENTS - Conditional
    # ==========================================
    
    def too_close_to_quit(self):
        # EVENT: Less than $50k away from the million - surge of motivation
        # CONDITION: Balance must be >= $950,000
        # EFFECTS: Heal 20 HP + gain "Lucky" status; destiny calls
        # Conditional - balance specific motivation
        if self.get_balance() < 950000:
            self.day_event()
            return
        
        type.type("You're gripping the steering wheel. Less than " + green(bright("$50,000")) + " to go. LESS THAN FIFTY THOUSAND DOLLARS.")
        print("\n")
        type.type("You could walk away right now with " + green(bright("${:,}".format(self.get_balance()))) + ". That's life-changing money for most people.")
        print("\n")
        type.type("But you didn't come this far to come this far.")
        print("\n")
        type.type("Tonight. Tonight could be THE night.")
        print("\n")
        self.heal(20)
        self.add_status("Lucky")
        type.type(yellow(bright("Destiny awaits.")))
        print("\n")

    def victoria_returns(self):
        # EVENT: Victoria the rival returns to acknowledge your skill and make peace
        # CONDITION: Must have met "The Rival" AND not have met "Victoria Confrontation"
        # EFFECTS: Shake hand = heal 10 HP; refuse = she warns of pride before a fall
        # CHAIN: Victoria storyline Part 2
        # Conditional - requires having met The Rival
        if not self.has_met("The Rival"):
            self.day_event()
            return
        
        if self.has_met("Victoria Confrontation"):
            self.day_event()
            return
        
        self.meet("Victoria Confrontation")
        type.type("The motorcycle pulls up. Victoria removes her helmet, but she's not smirking this time.")
        print("\n")
        type.type(quote("I'll be honest. I didn't think you'd make it this far."))
        print("\n")
        type.type("She leans against her bike, studying you.")
        print("\n")
        type.type(quote("I've been doing this for years and never got close to a million. You? A few months in a car and you're almost there."))
        print("\n")
        type.type("She shakes her head.")
        print("\n")
        type.type(quote("I was wrong about you. You're not just running hot. You've got something. Skill, luck, divine intervention-I don't know what. But you've got it."))
        print("\n")
        type.type("She extends her hand.")
        print("\n")
        type.type(quote("No hard feelings?"))
        print("\n")
        answer = ask.yes_or_no("Shake her hand? ")
        if answer == "yes":
            type.type("You shake. Her grip is firm.")
            print("\n")
            type.type(quote("Good luck tonight. You're going to need it."))
            print("\n")
            type.type("She drives off. You feel... lighter, somehow.")
            self.heal(10)
        else:
            type.type("You leave her hanging. She pulls her hand back, expression unreadable.")
            print("\n")
            type.type(quote("Fine. Have it your way. But remember-pride comes before the fall."))
            print("\n")
            type.type("She speeds off without another word.")
        print("\n")

    # ==========================================
    # NEW NEARLY DAY EVENTS - One-Time
    # ==========================================
    
    def the_warning(self):
        # EVENT: Blind old woman delivers cryptic prophecy about fire, cards, and a defining choice
        # CONDITION: One-time event (must not have met "The Warning")
        # EFFECTS: Atmospheric ominous foreshadowing; warns the million is just the beginning
        # One-Time - ominous NPC encounter
        if self.has_met("The Warning"):
            self.day_event()
            return
        
        self.meet("The Warning")
        type.type("An old woman shuffles up to your car. Her eyes are milky white-blind, or close to it.")
        print("\n")
        type.type(quote("You're the one,") + " she whispers. " + quote("I've seen you in my dreams."))
        print("\n")
        type.type("She presses a gnarled hand against your window.")
        print("\n")
        type.type(quote("The million isn't the end. It's the beginning. Of what, I don't know. But I see fire. I see cards. I see a choice that will define everything."))
        print("\n")
        type.type("She coughs-a wet, rattling sound.")
        print("\n")
        type.type(quote("Be careful what you wish for. Sometimes the universe gives you exactly what you ask for. And sometimes that's the worst thing that could happen."))
        print("\n")
        type.type("She shuffles away before you can respond, disappearing around a corner.")
        print("\n")
        type.type("You sit in silence for a long time, thinking about her words.")
        print("\n")

    def the_celebration(self):
        # EVENT: People mistakenly try to celebrate with you (wrong car) but leave cake behind
        # CONDITION: One-time event (must not have met "Premature Celebration")
        # EFFECTS: Heal 10 HP from eating dropped chocolate cake
        # One-Time - premature celebration
        if self.has_met("Premature Celebration"):
            self.day_event()
            return
        
        self.meet("Premature Celebration")
        type.type("A group of people approach your car. They're carrying a cake and balloons.")
        print("\n")
        type.type(quote("CONGRATULATIONS!") + " they shout.")
        print("\n")
        type.type("You blink. Did you already hit a million and forget?")
        print("\n")
        type.type("The leader of the group checks his phone, then looks at your car, then back at his phone.")
        print("\n")
        type.type(quote("Oh. Wrong car. Sorry."))
        print("\n")
        type.type("They shuffle away with their cake and balloons, leaving you very confused.")
        print("\n")
        type.type("But hey, they did drop a slice of cake in your lap. It's chocolate.")
        print("\n")
        self.heal(10)

    def final_dream(self):
        # DREAM EVENT: Combined dream sequence culmination
        # NOW FIRES AT NIGHT — replaces day summary
        # EFFECTS: Gain "Lucky" status; cryptic message about the ending
        if self.has_met("Final Dream"):
            return
        
        if self.get_tom_dreams() < 2 or self.get_frank_dreams() < 2 or self.get_oswald_dreams() < 2:
            return
        
        self.meet("Final Dream")
        type.type("You fall asleep and find yourself in a vast, empty casino. The lights are off. The slot machines are silent. The tables are empty.")
        print("\n")
        type.type("Except one.")
        print("\n")
        type.type("The Dealer sits at a blackjack table, illuminated by a single overhead lamp. He beckons you forward.")
        print("\n")
        type.type(quote("You've come a long way,") + " he says. " + quote("Farther than most."))
        print("\n")
        type.type("He shuffles the cards.")
        print("\n")
        type.type(quote("But the final test isn't about skill. It isn't about luck. It's about something else entirely."))
        print("\n")
        type.type("He deals you a hand. You look at your cards. They're blank.")
        print("\n")
        type.type(quote("The cards only show what you already know,") + " he says. " + quote("And you already know how this ends."))
        print("\n")
        type.type("You wake up with a certainty that wasn't there before.")
        print("\n")
        type.type(yellow(bright("Whatever happens tonight, you're ready.")))
        self.add_status("Lucky")
        print("\n")

    def the_offer(self):
        # EVENT: Mysterious limo offers to double your money if you walk away and never gamble again
        # CONDITION: One-time event (must not have met "The Offer")
        # EFFECTS: Accept = double your balance but hollow victory; Decline = continue toward true goal
        # One-Time - final temptation
        if self.has_met("The Offer"):
            self.day_event()
            return
        
        self.meet("The Offer")
        type.type("A limousine pulls up next to your wagon. The back window rolls down, revealing a distinguished-looking man in an expensive suit.")
        print("\n")
        type.type(quote("You're the one who's been winning. I've heard a lot about you."))
        print("\n")
        type.type("He smiles, but it doesn't reach his eyes.")
        print("\n")
        type.type(quote("I represent... certain interested parties. We've been watching your progress with great interest."))
        print("\n")
        type.type(quote("Here's my offer: walk away right now, and I'll double whatever you have. Cash. No questions asked."))
        print("\n")
        current = self.get_balance()
        type.type("That would be " + green(bright("${:,}".format(current * 2))) + ". More than your goal.")
        print("\n")
        answer = ask.yes_or_no("Accept the offer? ")
        if answer == "yes":
            type.type("The man smiles.")
            print("\n")
            type.type(quote("Smart. Very smart."))
            print("\n")
            type.type("A briefcase is pushed out the window. It's full of cash.")
            print("\n")
            type.type(quote("Pleasure doing business with you. I suggest you leave town immediately. And never come back to any casino. Ever."))
            print("\n")
            type.type("The limo drives away.")
            print("\n")
            type.type("You stare at the briefcase. You won. But... did you really?")
            print("\n")
            self.change_balance(current)
            type.type(yellow(bright("You got what you wanted. But something feels hollow.")))
        else:
            type.type("The man's smile fades.")
            print("\n")
            type.type(quote("Interesting. Most people would've taken the money."))
            print("\n")
            type.type("He leans forward.")
            print("\n")
            type.type(quote("You're either very brave or very stupid. Time will tell which."))
            print("\n")
            type.type("The window rolls up and the limo drives away.")
            print("\n")
            type.type("You made your choice. Now you have to live with it.")
            print("\n")
            type.type(yellow(bright("The true test lies ahead.")))
        print("\n")

    # ==========================================
    # SECRET EVENTS - NEARLY TIER
    # ==========================================
    
    def exactly_999999(self):
        # EVENT: Secret milestone - one dollar away from a million, universe provides the last dollar
        # CONDITION: Balance must be EXACTLY $999,999
        # EFFECTS: Wind blows a $1 bill to you, instantly reaching $1,000,000
        # SECRET EVENT - One dollar away
        if self.get_balance() != 999999:
            self.day_event()
            return
        
        type.type("You count your money. Once. Twice. Three times.")
        print("\n")
        type.type(green(bright("$999,999")) + ".")
        print("\n")
        type.type("One dollar. You are ONE DOLLAR away from a million.")
        print("\n")
        type.type("The universe has a cruel sense of humor.")
        print("\n")
        type.type("As if in response to your thoughts, a single dollar bill blows against your window, carried by the wind.")
        print("\n")
        type.type("You scramble out of the car and grab it before it can fly away.")
        print("\n")
        type.type(green(bright("$1,000,000.")))
        print("\n")
        type.type("You did it. You actually did it.")
        print("\n")
        self.change_balance(1)
        type.type(yellow(bright("ONE. MILLION. DOLLARS.")))
        print("\n")
        type.type(yellow(bright("But your story isn't over yet...")))
        print("\n")

    def all_dreams_complete(self):
        # EVENT: Secret - All three dream storylines complete, full revelation of your identity
        # CONDITION: Tom/Frank/Oswald dreams must all be at 3 (complete)
        # EFFECTS: Full heal (100 HP) + "Lucky" status; you know who you are and why you're here
        # SECRET EVENT - All three dream sequences complete
        if self.get_tom_dreams() != 3 or self.get_frank_dreams() != 3 or self.get_oswald_dreams() != 3:
            self.day_event()
            return
        
        if self.has_met("All Dreams Complete"):
            self.day_event()
            return
        
        self.meet("All Dreams Complete")
        type.type("There are tears on your face. But not from sadness.")
        print("\n")
        type.type("You remember everything now. Rebecca. Nathan. Johnathan.")
        print("\n")
        type.type("The Dealer. His rage. His scar. His glass eye.")
        print("\n")
        type.type("The casino. The money. The drink. The double.")
        print("\n")
        type.type("It all makes sense now. Every dream was a piece of a puzzle you didn't know you were solving.")
        print("\n")
        type.type(yellow(bright("You know who you are.")))
        print("\n")
        type.type(yellow(bright("You know why you're here.")))
        print("\n")
        type.type(yellow(bright("And you know what you have to do.")))
        print("\n")
        self.heal(100)
        self.add_status("Lucky")
        print("\n")
        
    # Conditional
        
    # One-Time
        
    # One-Time Conditional
    def cow_army(self):
        # EVENT: Betsy returns with an army of cows demanding massive payment or death
        # CONDITION: Must have met "Betsy" AND have "Betsy Army" danger
        # EFFECTS: Feed $100k stacks until satisfied, or refuse and DIE to cow army
        # CHAIN: Betsy storyline FINALE - can be lethal
        # BRUTAL: Refusing causes death
        # One-Time Conditional
        if not self.has_met("Betsy") or not self.has_danger("Betsy Army"):
            self.day_event()
            return

        self.lose_danger("Betsy Army")
        type.type("Thousands of hoofsteps are getting closer to your wagon. ")
        type.type("You jump out of your seat, to see the street flooded with cows, all getting closer to your vehicle. ")
        type.type("At the front of the crowd, is a cow, distinct from the rest. It's Betsy. Of course, it's Betsy. God fucking dammit.")
        print("\n")
        type.type("Betsy leads the herd to your wagon, and as you roll the window down, all you can hear are the hundreds upon hundreds of moos, from each of the angry cows. ")
        print("\n")
        type.type("Betsy, and the rest of the cows, all stare into your soul, then look over at the seat next to you. ")
        type.type("It appears Betsy and her friends are interested in your pile of money. ")
        print()
        type.type("Do you feed Betsy and her friends? ")
        while True:
            answer = ask.yes_or_no("Moo? ")
            if answer == "yes":
                type.type("You throw a bunch of bills into the crowd of cows, worth " + green(bright("$100,000")) + ". ")
                type.type("Betsy catches a bill, chews it up, then spits it out into your face.")
                self.change_balance(-100000)
                random_chance = random.randrange(4)
                if (random_chance == 0) or (self._balance <100001):
                    type.type("Betsy moos, then smiles. The rest of the cows moo in harmony, and the crowd begins to march down the road, happy as can be.")
                    break
                else:
                    type.type("Betsy moos, then stares you down. The rest of the cows begin to moo. They don't seem to be done with you.")
                    print()
                    type.type("Do you feed Betsy? ")
            elif answer == "no":
                type.type("Betsy moos, then charges your vehicle. ")
                type.type("The rest of the cows start attacking your wagon, shattering the windows, knocking off the tires, and pummeling the doors.")
                print("\n")
                type.slow(red(bright("A pane of glass explodes next to you, sending shards into your face. One catches your eye, and you scream in pain. The cows continue to attack you, and your money is spiraling all around. Unable to see, and covered in blood, you close your eyes, and let yourself succumb to the army of cows. You won, Betsy, you won.")))
                self.kill()
                break
        print("\n")

    def final_interrogation(self):
        # EVENT: Interrogator returns with a gun - final deadly confrontation
        # CONDITION: Must have met "Interrogator" AND have "Final Interrogation" danger
        # EFFECTS: Either die (25% chance) or steal his gun and confront him
        # CHAIN: Interrogation storyline FINALE - can be lethal
        # BRUTAL: 25% chance of instant death from gunshots
        # One-Time Conditional
        if not self.has_met("Interrogator") or not self.has_danger("Final Interrogation"):
            self.day_event()
            return

        self.lose_danger("Final Interrogation")
        type.type("Through the windshield-again-a car is parked right in front of you. ")
        type.type("You can feel your blood start to boil. What's this guy's problem? ")
        type.type("As you open the door and get out of your car, you notice the man in his bright red suit, once again peering into your trunk.")
        print("\n")
        type.type("The man sees you, and walks up to you, with a pistol holstered to his waist.")
        print("\n")
        type.type(space_quote("You. I'm done playing around. It's time to move. I mean it."))
        type.type("You look down at the gun on his waist. It looks fancy, and certainly deadly.")
        print("\n")
        type.type(quote("I wouldn't test me if I were you. It's time to go, now."))
        print("\n")
        type.type(space_quote("Will you leave?"))
        answer = ask.yes_or_no(space_quote("Answer me. "))
        if answer == "yes":
            type.type(quote("That's great. Fantastic. But I don't believe a word that comes out of your filthy mouth. Prove it. Leave. Go away. GET OUT."))
            print("\n")
            type.type("You are fueled with anger. Who is this guy, and what gives him the right to harass you? ")
            type.type("All for being homeless? No longer. You reach for the gun on his waist.")
            print("\n")
            random_chance = random.randrange(4)
            if random_chance == 0:
                type.slow(red("Before you get the chance to grab it, the man steps back, unholsters the pistol, then fires three shots into your chest. The glass behind you shatters, and you fall to your knees in the street."))
                print("\n")
                type.slow(red(quote("You should've just listened to me man! All you had to do was listen! Move, live somewhere else. Find a home, anything. But no! You just had to live in your car, like the homeless piece of shit that you are!")))
                print("\n")
                type.slow(red(bright("The man kicks you down, and steps on your chest, causing the bullet holes to leak blood onto the concrete below you. As you feel yourself beginning to fade away, you watch the man lift his pistol to your head, and pull the trigger.")))
                self.kill()
            else:
                type.type("You snatch the gun from his holster, and he tackles you to the ground. ")
                type.type("You fight and struggle, each of you with both hands on the pistol. ")
                type.type("In the distance, you hear the horn of a freight truck beginning to drive closer. ")
                type.type("The man punches you in the arm, and it stings. ")
                type.type("Without thinking twice, you give the man a headbutt, and he falls backwards into the road. ")
                type.type("You point the gun at the man, and he begins to cry.")
                print("\n")
                type.type(quote("Please, I'm sorry. I didn't mean to cause any of this. "))
                type.type(quote("I just, I hate seeing people living on the streets, all alone. "))
                type.type(quote("I was just trying to help you. Just, please, for the love of god, don't hurt me."))
                print("\n")
                type.type("As the man begs for his life, the freight truck continues to draw closer, and the horn gets louder. ")
                type.type("You point at the truck in the distance, but the man can't see through the tears in his eyes.")
                print("\n")
                type.type(space_quote("Please, I have a family. I have children. My name is Phil. I don't wanna die. I'm too young. I can't die. I can't die. I ca-"))
                type.type("You watch as the freight truck crushes Phil, and continues down the road. ")
                type.type("Nothing remained but the splotches of blood that splattered the road where he once stood.")
                print("\n")
                type.type("After sitting a while, and recollecting your thoughts, you bring the pistol over to Phil's car, and throw it onto the passenger seat. ")
                type.type("Looking inside, the car has dice hanging on the mirror, and is filled to the brim with red suits. ")
                type.type("On the dashboard sits a photo of Phil, his wife, and his three kids, all wearing bright red suits. ")
                type.type("Phil might've been crazy, but at least he was consistent.")
                print("\n")
                type.type("You get in the car, and drive it down the road, before turning into the woods. ")
                type.type("You drive a mile in, before parking the car before the lake. ")
                type.type("You get out, and push the car into the water, watching as it submerges.")
                print("\n")
                return
        elif answer == "no":
            type.type(quote("Really? You really want to do that? I warned you, man."))
            print("\n")
            type.type("The man pulls out his pistol, and points it at you. You lift your hands above your head, before quickly reaching for the pistol.")
            print("\n")
            random_chance = random.randrange(3)
            if random_chance == 0:
                type.slow(red("Before you get the chance to grab it, the man steps back, then fires three shots into your chest. The glass behind you shatters, and you fall to your knees in the street."))
                print("\n")
                type.slow(red(quote("Nice try, man! You should've just listened to me! All you had to do was listen! Move, live somewhere else. Find a home, anything. But no! You just had to live in your car, like the homeless piece of shit that you are!")))
                print("\n")
                type.slow(red(bright("The man kicks you down, and steps on your chest, causing the bullet holes to leak blood onto the concrete below you. As you feel yourself beginning to fade away, you watch the man lift his pistol to your hand, and pull the trigger.")))
                self.kill()
            else:
                type.type("You snatch the gun from his hands, and he tackles you to the ground. ")
                type.type("You fight and struggle, each of you with both hands on the pistol. ")
                type.type("The man punches you in the arm, and it stings. ")
                type.type("Without thinking twice, you give the man a headbutt, and he falls backwards into the road. ")
                type.type("You point the gun at the man, and he begins to cry.")
                print("\n")
                type.type(quote("Please, I'm sorry. I didn't mean to cause any of this. "))
                type.type(quote("I just, I hate seeing people living on the streets, all alone. "))
                type.type(quote("I was just trying to help you. Just, please, for the love of god, don't hurt me."))
                print("\n")
                type.type("As the man begs for his life, you cock the gun. You point pistol at the man, and he continues to cry.")
                print("\n")
                type.type(space_quote("Please, I have a family. I have children. My name is Phil. I don't wanna die. I'm too young. I can't die. I can't die. I ca-"))
                type.type("You pull the trigger, and Phil becomes quiet. His blood covers the street, but at least his red suit still looks good as new.")
                print("\n")
                type.type("After sitting a while, and recollecting your thoughts, you drag Phil over to his car. ")
                type.type("You stuff him into the trunk, and throw his pistol onto the passenger seat. ")
                type.type("Looking inside, the car has dice hanging on the mirror, and is filled to the brim with red suits. ")
                type.type("On the dashboard sits a photo, of Phil, his wife, and his three kids, all wearing bright red suits. ")
                type.type("Phil might've been crazy, but at least he was consistent.")
                print("\n")
                type.type("You get in the car, and drive it down the road, before turning into the woods. ")
                type.type("You drive a mile in, before parking the car before the lake. ")
                type.type("You get out, and push the car into the water, watching as it submerges.")
                print("\n")
                return

    # SUZY STORYLINE - NEARLY THERE DAY (FINALE)
    def gift_from_suzy(self):
        # EVENT: Suzy's GOOD ending - she gives you a handmade stuffed animal gift
        # CONDITION: Must have completed Suzy storyline (has favorite animal) AND not met "Suzy Finale"
        # EFFECTS: Receive "Suzy's Gift" item + restore 5-8 sanity; emotional farewell as Suzy moves away
        # CHAIN: Suzy Storyline GOOD FINALE
        # Only triggers if Suzy storyline is complete (has favorite animal)
        # This is the GOOD ending - requires having been kind to Suzy
        if self.get_favorite_animal() == None or self.has_met("Suzy Finale"):
            self.day_event()
            return
        
        self.meet("Suzy Finale")
        
        type.type("An unusual sound-not sneakers on concrete, but the crunch of grass. ")
        type.type("You sit up and see Suzy standing outside your wagon, holding something behind her back.")
        print("\n")
        type.type("She's not jump roping. For the first time ever, she's standing completely still.")
        print("\n")
        type.type(quote("Hi, " + self._name + ". I made you something."))
        print("\n")
        type.type("Suzy pulls out a small stuffed animal from behind her back. ")
        type.type("It's a " + self.get_favorite_animal() + ", crudely sewn together with mismatched fabric, but clearly made with love. ")
        type.type("The fabric is " + self.get_favorite_color() + ", your favorite color.")
        print("\n")
        type.type(quote("I remembered everything you told me. Your favorite color, your favorite animal. I made it myself! Do you like it?"))
        print("\n")
        type.type("You take the stuffed " + self.get_favorite_animal() + ". Despite its imperfect stitching, it's one of the most thoughtful gifts anyone has ever given you.")
        print("\n")
        type.type(quote("I wanted to say thank you. For always being nice to me. "))
        type.type(quote("Most grown-ups ignore me, or tell me to go away. But you always talked to me like I was a real person."))
        print("\n")
        type.type("Suzy sniffles a little.")
        print("\n")
        type.type(quote("I hope you find what you're looking for, " + self._name + ". I really do."))
        print("\n")
        type.type("Before you can respond, Suzy picks up her jump rope and starts bouncing away.")
        print("\n")
        type.type(quote("Bye bye! Maybe I'll see you again someday! But probably not. "))
        type.type(quote("I'm moving away with my aunt. She found me! She's really nice. "))
        type.type(quote("I'll think of you when I see " + self.get_favorite_animal() + "s!"))
        print("\n")
        type.type("And with that, Suzy jump ropes into the distance for the last time, disappearing around the corner. ")
        type.type("You look down at the stuffed " + self.get_favorite_animal() + " in your hands.")
        print("\n")
        type.type(yellow(bright("Some goodbyes are harder than others.")))
        self.add_item("Suzy's Gift")
        self.restore_sanity(random.choice([5, 6, 7, 8]))  # Deeply restores sanity
        print("\n")

    def suzy_the_snitch(self):
        # EVENT: Suzy's BAD ending - she reports you to police using info you shared
        # CONDITION: Must have completed Suzy storyline (has favorite animal) AND not met "Suzy Finale"
        # EFFECTS: INSTANT DEATH - arrested and jailed based on info you told Suzy
        # CHAIN: Suzy Storyline BAD FINALE
        # BRUTAL: Causes death
        # Only triggers if Suzy storyline is complete AND this is checked
        # This is the BAD ending - happens if player was mean to Suzy
        if self.get_favorite_animal() == None or self.has_met("Suzy Finale"):
            self.day_event()
            return
        
        self.meet("Suzy Finale")
        
        type.type("A car engine and flashing lights. Right outside. A police cruiser has pulled up right next to your wagon. Your heart sinks.")
        print("\n")
        type.type("A cop steps out, notepad in hand. And there, in the passenger seat of the cruiser, sits Suzy, still holding her jump rope.")
        print("\n")
        type.type("The cop approaches your window.")
        print("\n")
        type.type(quote("Are you " + self._name + "? This young lady here says she knows you."))
        print("\n")
        type.type("Suzy waves at you through the window, an innocent smile on her face.")
        print("\n")
        type.type(quote("That's him, officer! The homeless man I told you about! "))
        type.type(quote("His favorite color is " + self.get_favorite_color() + " and his favorite animal is a " + self.get_favorite_animal() + "! He told me EVERYTHING!"))
        print("\n")
        type.type("The cop looks at his notepad, then back at you.")
        print("\n")
        type.type(quote("Sir, we've had reports of someone matching your description involved in some... questionable activities in this area. "))
        type.type(quote("We're going to need you to come with us for questioning."))
        print("\n")
        type.type("Suzy presses her face against the police car window.")
        print("\n")
        type.type(quote("Bye bye, " + self._name + "! I hope you enjoy jail! They probably have " + self.get_favorite_animal() + "s there! Maybe!"))
        print("\n")
        type.type("Before you can protest or explain, you're in handcuffs and being led to the back of the cruiser. Suzy waves at you the whole time.")
        print("\n")
        type.slow(red(bright("You spend the rest of your days in a cell, thinking about how you probably shouldn't have trusted a jump-roping little girl with all your personal information. The last thing you remember before everything fades to black is the distant sound of sneakers on concrete, and a jump rope hitting the ground.")))
        print("\n")
        self.kill()


    # ADDITIONAL NEW EVENTS
    # ==========================================

    # POOR DAY EVENTS - Everytime
    def vending_machine_luck(self):
        type.type("You step out of your car and find a vending machine outside an abandoned gas station. The display is cracked, but the lights are still on.")
        print("\n")
        type.type("You don't have any change, but you give it a hopeful kick anyway.")
        print("\n")
        chance = random.randrange(4)
        if chance == 0:
            type.type("CLUNK. A candy bar falls out! It's only slightly expired.")
            print("\n")
            type.type("You eat it anyway. Your standards have lowered significantly since this whole adventure started.")
            self.heal(5)
        elif chance == 1:
            type.type("CLUNK CLUNK CLUNK. A cascade of coins rattles out! Someone's quarters finally came home to roost.")
            amount = random.randint(3, 15)
            type.type(" You collect " + green(bright("$" + str(amount))) + " in loose change.")
            self.change_balance(amount)
        elif chance == 2:
            type.type("The machine groans, shudders, and then falls silent. You've killed it.")
            print("\n")
            type.type("Add 'vending machine murderer' to your growing list of moral failures.")
        else:
            type.type("Nothing happens. The machine stares back at you, judging silently.")
            print("\n")
            type.type("Even inanimate objects are disappointed in you now.")
        print("\n")

    def talking_to_yourself(self):
        type.type("You've been alone in this car for too long. You start talking to yourself.")
        print("\n")
        type.type(quote("Hey, me. How's it going?"))
        print()
        type.type(quote("Oh, you know. Living the dream. Sleeping in a car. Gambling addiction. The usual."))
        print()
        type.type(quote("Cool, cool. Wanna play twenty questions?"))
        print()
        type.type(quote("I already know all your answers, idiot. We're the same person."))
        print("\n")
        type.type("The conversation devolves into an argument about whose fault this all is. You both lose.")
        print("\n")
        sanity_change = random.choice([-3, -2, 1, 2])
        if sanity_change > 0:
            type.type("Oddly, the self-deprecating banter makes you feel a little better.")
            self.restore_sanity(sanity_change)
        else:
            type.type("This probably isn't healthy.")
            self.lose_sanity(abs(sanity_change))
        print("\n")

    def wrong_number(self):
        type.type("Your phone buzzes from the passenger seat. You have a text from an unknown number.")
        print("\n")
        messages = [
            quote("Hey babe, I left my keys at your place. Can you leave them under the mat?"),
            quote("This is your doctor. Your test results are in. Please call us immediately."),
            quote("We've been trying to reach you about your car's extended warranty."),
            quote("Grandma passed away. The funeral is Saturday."),
            quote("I know what you did. Meet me at the pier at midnight. Come alone.")
        ]
        type.type(random.choice(messages))
        print("\n")
        type.type("You stare at your phone for a long moment, then remember you don't recognize this number at all.")
        print("\n")
        answer = ask.yes_or_no("Reply anyway? ")
        if answer == "yes":
            type.type("You type back: " + quote("Wrong number, buddy."))
            print("\n")
            chance = random.randrange(5)
            if chance == 0:
                type.type("They reply: " + quote("OMG I'm so sorry! Here's $10 for the trouble via cash app!"))
                print("\n")
                type.type("Wait, that actually worked? You got " + green(bright("$10")) + "!")
                self.change_balance(10)
            else:
                type.type("They don't reply. Probably embarrassed.")
        else:
            type.type("You ignore it. Not your circus, not your monkeys.")
        print("\n")

    def cloud_watching(self):
        type.type("You lie on the hood of your car and stare at the clouds. It's surprisingly peaceful.")
        print("\n")
        clouds = [
            "That one looks like a bunny. Or maybe a dog. Or a bunny-dog hybrid. A bunny-dog? A dog-bunny?",
            "That one definitely looks like the Dealer's face. Great, even the sky is judging you now.",
            "That one looks like a pile of money. Your brain really can't think about anything else, can it?",
            "That one looks like your ex. You try not to think about that too hard.",
            "That one looks like nothing. It's just a cloud. Not everything needs to be symbolic.",
            "That one looks like a middle finger. Nature is mocking you specifically."
        ]
        type.type(random.choice(clouds))
        print("\n")
        type.type("After an hour of this, you feel strangely refreshed. Maybe doing nothing is underrated.")
        self.restore_sanity(random.choice([2, 3, 4]))
        print("\n")

    def car_alarm_symphony(self):
        type.type("Every car alarm in a five-block radius goes off simultaneously, jolting you upright in your seat.")
        print("\n")
        type.type("BEEP BEEP BEEP HONK HONK WEEEOOOWEEEOO BEEP BEEP")
        print()
        type.type("You try to cover your ears, but it's no use. The symphony of chaos plays on.")
        print("\n")
        type.type("After twenty agonizing minutes, they all stop at once. The silence is somehow worse.")
        print("\n")
        self.lose_sanity(random.choice([1, 2, 3]))
        self.hurt(5)
        print("\n")

    # CHEAP DAY EVENTS - Everytime
    def fortune_cookie(self):
        type.type("You find an old fortune cookie in your glove compartment. It's from that Chinese place you went to... three months ago?")
        print("\n")
        type.type("Against your better judgment, you crack it open.")
        print("\n")
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
        print("\n")
        type.type("The cookie itself is stale beyond recognition, but you eat it anyway. Waste not, want not.")
        print("\n")

    def deja_vu_again(self):
        type.type("The strangest feeling hits you as you sit in your car. You've done this exact thing before.")
        print("\n")
        type.type("Same sunrise. Same ache in your back. Same existential dread.")
        print("\n")
        type.type("Wait, have you? The days are starting to blur together. Was yesterday real? Is TODAY real?")
        print("\n")
        type.type("You pinch yourself. It hurts. Okay, probably real.")
        print("\n")
        self.lose_sanity(1)
        print("\n")

    def street_musician(self):
        type.type("A street musician has set up shop near your parking spot. He's playing the saxophone.")
        print("\n")
        type.type("He's... not great. But he's trying. Oh god, is he coming over here?")
        print("\n")
        type.type("He stops right next to your window and launches into what you think is meant to be 'Careless Whisper.'")
        print("\n")
        answer = ask.yes_or_no("Give him some money to make him go away? ")
        if answer == "yes":
            amount = random.randint(5, 15)
            if self.get_balance() >= amount:
                type.type("You hand him " + green(bright("$" + str(amount))) + ". He tips his hat and moves on to torture someone else.")
                self.change_balance(-amount)
                self.restore_sanity(2)
            else:
                type.type("You show him your empty wallet. He plays a sad trombone sound effect on his phone and walks away disappointed.")
        else:
            type.type("You close your eyes and pretend to be asleep. He plays louder. This goes on for forty-five minutes.")
            self.lose_sanity(3)
        print("\n")

    def roadkill_philosophy(self):
        type.type("Through your car window, you spot a dead possum on the side of the road. It makes you think about mortality.")
        print("\n")
        type.type("We're all just possums, really. Going about our business until life runs us over with a metaphorical pickup truck.")
        print("\n")
        type.type("Or maybe you're just sleep-deprived and reading too much into roadkill. That's also possible.")
        print("\n")
        type.type("Either way, you feel strangely philosophical for the next hour.")
        self.restore_sanity(1)
        print("\n")

    # MODEST DAY EVENTS - Everytime
    def fancy_coffee(self):
        type.type("You head out from your car and treat yourself to a coffee from the fancy place downtown. The one with seventeen syllable drink names.")
        print("\n")
        type.type(quote("I'll have a... uh... the brown one?"))
        print()
        type.type("The barista sighs the sigh of someone who went to art school for this.")
        print("\n")
        cost = random.randint(8, 15)
        type.type("Your 'brown one' costs " + green(bright("$" + str(cost))) + ". That's absurd. You pay anyway.")
        self.change_balance(-cost)
        print("\n")
        type.type("It's... actually really good. You feel temporarily sophisticated.")
        self.restore_sanity(3)
        self.heal(5)
        print("\n")

    def parking_ticket(self):
        type.type("You return to your car to find a parking ticket on the windshield.")
        print("\n")
        type.type("$75 for 'Overnight Parking in Non-Designated Area.' Also known as: existing while poor.")
        print("\n")
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
        print("\n")

    def found_phone(self):
        type.type("You find a smartphone on the ground next to your car. It's cracked but still working.")
        print("\n")
        type.type("The lock screen shows 47 missed calls from 'Mom' and the battery is at 3%.")
        print("\n")
        answer = ask.yes_or_no("Try to return it to the owner? ")
        if answer == "yes":
            type.type("You call 'Mom' back. She's very grateful and sends her son to pick it up.")
            print("\n")
            type.type("He gives you " + green(bright("$50")) + " as a thank you. " + quote("You're a good person,") + " he says.")
            print("\n")
            type.type("The praise feels strange. When's the last time someone called you good?")
            self.change_balance(50)
            self.restore_sanity(5)
        else:
            type.type("You pocket it. Maybe you can sell it later. You try not to think about the crying mom.")
            self.add_item("Found Phone")
            self.lose_sanity(2)
        print("\n")

    # RICH DAY EVENTS - Everytime
    def luxury_problems(self):
        type.type("Sitting in your car, you realize you have money problems now. Rich people money problems.")
        print("\n")
        type.type("Like: which pocket do you keep your money in? It's getting heavy. Your pants are sagging.")
        print("\n")
        type.type("Or: people keep asking you for loans. Random strangers. They can SMELL wealth, apparently.")
        print("\n")
        type.type("Or: you're worried about getting robbed. You're literally sleeping in a car full of cash.")
        print("\n")
        type.type("Somehow, having money is stressful in entirely new ways. Who knew?")
        self.lose_sanity(1)
        print("\n")

    def imposter_syndrome(self):
        type.type("You check your balance from your car and feel... weird. This much money? You? The car-sleeping gambler?")
        print("\n")
        type.type("Surely this is a mistake. Surely someone's going to show up and demand it all back.")
        print("\n")
        type.type("'I'm sorry sir, there's been an error. You were never supposed to succeed. Please return to being poor.'")
        print("\n")
        type.type("The money stays. The anxiety doesn't.")
        self.lose_sanity(2)
        print("\n")

    def charity_opportunity(self):
        type.type("You step out of your car and a woman approaches you with a clipboard. " + quote("Hi! Would you like to donate to the Children's Hospital Foundation?"))
        print("\n")
        type.type("She has the aggressive cheerfulness of someone who does this professionally.")
        print("\n")
        answer = ask.yes_or_no("Donate $100 to charity? ")
        if answer == "yes":
            if self.get_balance() >= 100:
                type.type("You hand over " + green(bright("$100")) + ". The woman beams. " + quote("You're making a real difference!"))
                print("\n")
                type.type("You feel warm inside. Is this what being a good person feels like?")
                self.change_balance(-100)
                self.restore_sanity(10)
                self.heal(10)
            else:
                type.type("You reach for your wallet and realize... you don't actually have that much liquid. Awkward.")
        else:
            type.type("You mumble something about being late for an appointment and speed-walk away.")
            print("\n")
            type.type("Her disappointed gaze follows you. The guilt follows you too.")
            self.lose_sanity(3)
        print("\n")

    # DOUGHMAN DAY EVENTS - Everytime
    def money_counting_ritual(self):
        type.type("You've developed a ritual of counting your money in the car every morning. It takes a while now.")
        print("\n")
        type.type("...four hundred fifty-three thousand, seven hundred twenty-two... twenty-three... twenty-four...")
        print("\n")
        type.type("You lose count and have to start over. Twice.")
        print("\n")
        type.type("By the time you're done, two hours have passed. Was this a good use of time? No. Did it feel good? Also no. Will you do it again tomorrow? Absolutely.")
        print("\n")

    def nervous_habits(self):
        type.type("Sitting in your car, you notice you've started developing nervous habits now that you have something to lose.")
        print("\n")
        variant = random.randrange(4)
        if variant == 0:
            type.type("You check your pockets every thirty seconds to make sure the money is still there.")
        elif variant == 1:
            type.type("You've started talking to your money. Giving it pep talks. Telling it you believe in it.")
        elif variant == 2:
            type.type("You keep making backup plans. If you lose it all, you can always... wait, no, you can't. There's no backup plan.")
        else:
            type.type("You've started having nightmares about the Dealer. He's laughing. He's always laughing.")
        print("\n")
        type.type("This level of wealth-related anxiety probably isn't normal.")
        self.lose_sanity(2)
        print("\n")

    def millionaire_fantasy(self):
        type.type("Sitting in your car, you're so close to a million dollars that you can taste it. You start fantasizing about what you'll do.")
        print("\n")
        fantasies = [
            "Buy a real house. With walls. And a roof that doesn't leak gasoline fumes.",
            "Get health insurance. Maybe see a doctor about that thing on your elbow.",
            "Take a vacation. Somewhere with beaches. Or mountains. Or literally anywhere that isn't a casino parking lot.",
            "Pay off your debts. All of them. Tell the collectors to go pound sand.",
            "Buy a new car. One where you don't have to live in it.",
            "Help your family. If they'll still talk to you after all this."
        ]
        type.type(random.choice(fantasies))
        print("\n")
        type.type("But first, you have to actually WIN. Back to the tables.")
        self.restore_sanity(3)
        print("\n")

    # ==========================================
    # ONE-TIME EVENTS
    # ==========================================

    def the_hitchhiker(self):
        # One-Time - Cheap tier
        if self.has_met("Hitchhiker"):
            self.day_event()
            return
        
        self.meet("Hitchhiker")
        type.type("You're pulling out of your parking spot when you see a young woman by the side of the road, thumb out. She looks tired. Desperate, even.")
        print("\n")
        type.type("She sees your car slow down and her eyes light up with hope.")
        print("\n")
        answer = ask.yes_or_no("Pick her up? ")
        if answer == "yes":
            type.type("You unlock the door. She slides in, smelling faintly of campfire smoke and bad decisions.")
            print("\n")
            type.type(quote("Thank you SO much. I've been out here for hours. Name's Maya."))
            print("\n")
            type.type("You drive her to the next town over. She talks the whole way-")
            type.type("about a boyfriend who left her stranded, about dreams of being a singer, ")
            type.type("about how she's going to make it big someday.")
            print("\n")
            type.type("When you drop her off, she reaches into her bag.")
            print("\n")
            type.type(quote("I don't have much, but take this. For luck."))
            print("\n")
            type.type("She hands you a worn guitar pick with a four-leaf clover on it.")
            print("\n")
            type.type("You got " + magenta(bright("Maya's Pick")) + "! It feels strangely warm in your pocket.")
            self.add_item("Maya's Pick")
            self.restore_sanity(5)
        else:
            type.type("You drive past. In the rearview mirror, you see her shoulders slump.")
            print("\n")
            type.type("It was probably the safe choice. Probably.")
            self.lose_sanity(2)
        print("\n")

    def the_prophet(self):
        # One-Time - Modest tier
        if self.has_met("Street Prophet"):
            self.day_event()
            return
        
        self.meet("Street Prophet")
        type.type("You step out of your car and spot a man in tattered robes on a street corner, holding a cardboard sign that reads: 'THE END IS NIGH (FOR YOUR WALLET)'")
        print("\n")
        type.type("He spots you and his eyes go wide.")
        print("\n")
        type.type(quote("YOU! Yes, YOU! I have foreseen your coming!"))
        print("\n")
        type.type("Great. A crazy person who's noticed you specifically.")
        print("\n")
        type.type(quote("The cards whisper to me, traveler. They speak of a gambler who sleeps in their chariot, who dances with fortune and tragedy alike!"))
        print("\n")
        type.type("Okay, that's... actually pretty accurate.")
        print("\n")
        type.type(quote("I offer you a prophecy! One glimpse into your possible future! For the low, low price of...") + " He squints at you, assessing. ")
        type.type(quote("Twenty bucks."))
        print("\n")
        answer = ask.yes_or_no("Pay $20 for a prophecy? ")
        if answer == "yes":
            if self.get_balance() >= 20:
                self.change_balance(-20)
                print("\n")
                type.type("He takes your money, closes his eyes, and begins to hum.")
                print("\n")
                prophecies = [
                    quote("I see... a great victory! But beware the fifth hand after sunset. The Dealer's smile will mean danger."),
                    quote("You will face a choice between wealth and wisdom. Choose wisely, for you cannot have both."),
                    quote("There is a rabbit in your future. Do not trust the rabbit."),
                    quote("The numbers 7, 11, and 21 will guide you. Or destroy you. Same difference, really."),
                    quote("I see... I see... actually, I can't see anything. I'm making this up. But hey, twenty bucks is twenty bucks.")
                ]
                type.type(random.choice(prophecies))
                print("\n")
                type.type("He opens his eyes and grins a toothless grin. " + quote("May fortune favor you, gambler. Or not. I'm a prophet, not a miracle worker."))
            else:
                type.type("You check your pockets. Twenty bucks is more than you can spare.")
                type.type(" The prophet sighs. " + quote("The universe provides for those who can afford it."))
        else:
            type.type("You politely decline. He shrugs and goes back to shouting at passersby.")
        print("\n")

    def the_gambler_ghost(self):
        # One-Time - Rich tier, spooky
        if self.has_met("Gambler Ghost"):
            self.day_event()
            return
        
        self.meet("Gambler Ghost")
        self.lose_sanity(random.choice([3, 4, 5]))
        type.type("You sit up in your car seat. Something feels... wrong.")
        print("\n")
        type.type("You look in your rearview mirror and freeze.")
        print("\n")
        type.type("There's a man in your back seat.")
        print("\n")
        type.type("He's dressed in a vintage suit, the kind people wore in the 1920s. His face is pale. Too pale. And you can see right through him.")
        print("\n")
        type.type(quote("Don't be alarmed,") + " he says, his voice like static. " + quote("I just wanted to talk to a fellow gambler."))
        print("\n")
        type.type("You are VERY alarmed.")
        print("\n")
        type.type(quote("I lost everything at this casino, you know. 1928. Bet my house, my car, my wife's jewelry. Lost it all on one hand."))
        print("\n")
        type.type("He laughs, but there's no humor in it.")
        print("\n")
        type.type(quote("They found me the next morning in the river. I've been here ever since, watching others make the same mistakes."))
        print("\n")
        type.type("You don't know what to say. What DO you say to a ghost?")
        print("\n")
        type.type(quote("You're different, though. I can see it. You might actually make it out."))
        print("\n")
        type.type("He starts to fade.")
        print("\n")
        type.type(quote("Just remember: the house always wins. Unless you know when to walk away."))
        print("\n")
        type.type("And then he's gone. You don't sleep the rest of the night.")
        print("\n")

    def the_doppelganger(self):
        # One-Time - Doughman tier, very unsettling
        if self.has_met("Doppelganger"):
            self.day_event()
            return
        
        self.meet("Doppelganger")
        self.lose_sanity(random.choice([5, 6, 7]))
        type.type("You step out of your car in the casino parking lot and see yourself.")
        print("\n")
        type.type("Not a mirror. Not a reflection. YOU. Standing about fifty feet away, staring back at you.")
        print("\n")
        type.type("Same clothes. Same face. Same confused expression.")
        print("\n")
        type.type("You blink. Your double blinks.")
        print("\n")
        type.type("You take a step forward. It takes a step forward.")
        print("\n")
        type.type("You wave. It waves.")
        print("\n")
        type.type("And then it smiles-a smile you've never made, too wide, too knowing-and walks behind a van.")
        print("\n")
        type.type("You run over. Nothing. No one. Just empty parking spaces.")
        print("\n")
        type.type("You stand there for a long time, heart pounding, wondering if you're finally losing your mind.")
        print("\n")
        type.type("Maybe you are.")
        print("\n")

    # ==========================================
    # CONDITIONAL EVENTS
    # ==========================================

    def mayas_luck(self):
        # Conditional - requires Maya's Pick
        if not self.has_item("Maya's Pick"):
            self.day_event()
            return
        
        type.type("Your pocket feels warm. You reach in and pull out Maya's Pick.")
        print("\n")
        type.type("It's glowing. Actually glowing. A soft, golden light.")
        print("\n")
        type.type("You hear a voice, distant but clear: " + quote("Thank you for believing in me. I made it. I'm actually singing now."))
        print("\n")
        type.type("The glow fades, but you feel strangely blessed. Like luck is on your side today.")
        print("\n")
        bonus = random.randint(100, 500)
        type.type("You find " + green(bright("$" + str(bonus))) + " in your coat pocket that you're SURE wasn't there before.")
        self.change_balance(bonus)
        self.restore_sanity(5)
        print("\n")

    def unpaid_ticket_consequence(self):
        # Conditional - requires Unpaid Tickets danger
        if not self.has_danger("Unpaid Tickets"):
            self.day_event()
            return
        
        type.type("Blue lights flash behind you. Your heart drops.")
        print("\n")
        type.type("A police officer walks up to your window. " + quote("License and registration, please."))
        print("\n")
        type.type("He runs your plates. His expression darkens.")
        print("\n")
        type.type(quote("Sir, it appears you have... seventeen unpaid parking tickets. That's a $500 fine."))
        print("\n")
        if self.get_balance() >= 500:
            answer = ask.yes_or_no("Pay the $500 fine? ")
            if answer == "yes":
                type.type("You hand over the money, wincing. The officer tips his hat.")
                print("\n")
                type.type(quote("Have a nice day. And maybe invest in a parking app."))
                self.change_balance(-500)
                self.remove_danger("Unpaid Tickets")
            else:
                type.type("The officer sighs. " + quote("Then I'll have to impound your vehicle."))
                print("\n")
                type.type("Just kidding, he doesn't. But he DOES slap a boot on your tire.")
                print("\n")
                type.type("You spend the next three hours dealing with bureaucracy to get it removed.")
                self.lose_sanity(10)
        else:
            type.type("You show him your empty wallet. He sighs.")
            print("\n")
            type.type(quote("Look, I'm gonna let you off with a warning this time. But get those tickets paid."))
            print("\n")
            type.type("You got lucky. Very lucky.")
        print("\n")

    # ==========================================
    # MEGA EVENT BATCH - POOR TIER
    # ==========================================

    def trash_treasure(self):
        type.type("You head out from your car to the dumpster behind a convenience store. Don't judge. Times are tough.")
        print("\n")
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
        print("\n")

    def coin_flip_stranger(self):
        type.type("A man in a trench coat approaches your car. He flips a coin in his hand, over and over.")
        print("\n")
        type.type(quote("Call it."))
        print("\n")
        type.type("You don't know why, but you feel compelled to answer.")
        print("\n")
        answer = ask.option("Heads or tails? ", ["heads", "tails"])
        flip = random.choice(["heads", "tails"])
        type.type("He flips. It lands on " + bright(flip) + ".")
        print("\n")
        if answer == flip:
            amount = random.randint(20, 50)
            type.type(quote("Lucky.") + " He hands you " + green(bright("$" + str(amount))) + " and walks away without another word.")
            self.change_balance(amount)
        else:
            type.type(quote("Unlucky.") + " He takes nothing, but you feel like you've lost something anyway.")
            self.lose_sanity(3)
        print("\n")

    def seagull_attack(self):
        type.type("A seagull dive-bombs your car")
        
        # Animal Whistle turns an attack into friendship
        if self.has_item("Animal Whistle") and not self.has_companion("Squawk"):
            type.type(" - but the " + magenta(bright("Animal Whistle")) + " hums and the bird pulls up at the last second!")
            print("\n")
            type.type("The seagull lands on your hood, head tilted, examining you with one beady eye.")
            print("\n")
            type.type("FRIEND? FRIEND! FRIEND!")
            print("\n")
            type.type("You toss it some of your breakfast. The seagull wolfs it down and does a little dance on your hood.")
            print("\n")
            type.type("You've just gained the loyalty of a seagull. You decide to call it " + cyan(bright("Squawk")) + ".")
            print("\n")
            type.type("Squawk will ride on your roof now, screaming at anyone who looks at you funny.")
            self.add_companion("Squawk", "Seagull")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            print("\n")
            return
        
        type.type(" and steals your breakfast right out of your hand.")
        print("\n")
        type.type("MINE! MINE! MINE!")
        print("\n")
        type.type("You chase it for half a block before giving up. Seagulls are nature's assholes.")
        print("\n")
        self.hurt(3)
        self.lose_sanity(2)
        print("\n")

    def lucky_penny(self):
        type.type("You step out of your car and find a penny on the ground. Heads up. That's lucky, right?")
        print("\n")
        type.type("You pick it up and put it in your pocket. Every little bit helps.")
        print("\n")
        chance = random.randrange(10)
        if chance == 0:
            type.type("Wait, this isn't a penny. It's a rare coin worth way more!")
            amount = random.randint(50, 150)
            type.type(" You sell it later for " + green(bright("$" + str(amount))) + "!")
            self.change_balance(amount)
        else:
            self.change_balance(0.01)
            type.type("It's just a penny. But hey, that's 0.01% closer to a million!")
        print("\n")

    def stray_cat(self):
        type.type("A scraggly stray cat jumps onto your hood and stares at you through the windshield.")
        print("\n")
        type.type("It meows. Loudly. Insistently. Like it's judging your entire existence.")
        print("\n")
        answer = ask.yes_or_no("Feed it some of your food? ")
        if answer == "yes":
            type.type("You share your meager rations. The cat purrs and curls up on your hood.")
            print("\n")
            type.type("It's still there when you wake up the next morning. You have a friend now.")
            print("\n")
            type.type("You decide to call it " + cyan(bright("Whiskers")) + ".")
            self.restore_sanity(5)
            self.meet("Stray Cat Friend")
            self.add_companion("Whiskers")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
        else:
            type.type("You shoo it away. It gives you a look of pure feline contempt before leaving.")
            print("\n")
            type.type("You feel like you've made an enemy.")
        print("\n")

    def three_legged_dog(self):
        """Encounter with Lucky the three-legged dog"""
        if self.has_companion("Lucky"):
            self.day_event()
            return
        
        type.type("You step out of your car and hear whimpering coming from behind a dumpster. Curious, you investigate.")
        print("\n")
        type.type("There, huddled against the cold concrete, is a scruffy dog. ")
        type.type("He's missing his front left leg, but his tail starts wagging the moment he sees you.")
        print("\n")
        type.type("Despite his condition, his eyes are bright and hopeful. He limps toward you, tail wagging furiously.")
        print("\n")
        
        # Animal Whistle automatically befriends
        if self.has_item("Animal Whistle"):
            type.type("The " + magenta(bright("Animal Whistle")) + " hums softly in your pocket. The dog's ears perk up.")
            print("\n")
            type.type("He bounds toward you without fear, tail wagging so hard his whole body shakes.")
            print("\n")
            type.type("You don't even need to ask. He's already chosen you.")
            answer = "yes"
        else:
            answer = ask.yes_or_no("Take him in? ")
        
        if answer == "yes":
            type.type("You scoop him up carefully. He licks your face, tail wagging so hard his whole body shakes.")
            print("\n")
            type.type("He seems like a fighter. A survivor. Just like you.")
            print("\n")
            type.type("You decide to call him " + cyan(bright("Lucky")) + ". Because against all odds, he found you.")
            self.restore_sanity(10)
            self.add_companion("Lucky")
            self.increment_statistic("companions_befriended")
            if not self.has_achievement("first_friend"):
                self.unlock_achievement("first_friend")
        else:
            type.type("You back away slowly. The dog whimpers, but doesn't follow.")
            print("\n")
            type.type("His hopeful eyes haunt you for the rest of the day.")
            self.lose_sanity(5)
        print("\n")
    
    def crow_encounter(self):
        """Encounter with Mr. Pecks the crow"""
        if self.has_companion("Mr. Pecks"):
            self.day_event()
            return
        
        type.type("A large black crow lands on your car's side mirror and stares at you.")
        print("\n")
        type.type("It tilts its head, studying you with an intelligence that seems almost... unnatural.")
        print("\n")
        type.type("The crow hops to your hood and drops something shiny. A quarter.")
        print("\n")
        type.type("It caws expectantly, like it's waiting for something in return.")
        print("\n")
        
        # Animal Whistle automatically befriends
        if self.has_item("Animal Whistle"):
            type.type("The " + magenta(bright("Animal Whistle")) + " hums. The crow tilts its head, then flies to your shoulder.")
            print("\n")
            type.type("It bows. An actual bow, like a little gentleman.")
            print("\n")
            type.type("From that moment on, the crow follows you everywhere. You name him " + cyan(bright("Mr. Pecks")) + ".")
            self.change_balance(0.25)
            self.add_companion("Mr. Pecks")
            self.increment_statistic("companions_befriended")
            if not self.has_achievement("first_friend"):
                self.unlock_achievement("first_friend")
        elif self.has_item("Birdseed") or self.has_item("Bread"):
            item = "Birdseed" if self.has_item("Birdseed") else "Bread"
            answer = ask.yes_or_no("Offer it some " + item + "? ")
            if answer == "yes":
                self.use(item)
                type.type("You toss some " + item + " on the hood. The crow gobbles it up eagerly.")
                print("\n")
                type.type("Then it does something strange. It bows. An actual bow, like a little gentleman.")
                print("\n")
                type.type("From that moment on, the crow follows you everywhere. You name him " + cyan(bright("Mr. Pecks")) + ".")
                self.change_balance(0.25)
                self.add_companion("Mr. Pecks")
                self.increment_statistic("companions_befriended")
                if not self.has_achievement("first_friend"):
                    self.unlock_achievement("first_friend")
            else:
                type.type("You ignore the crow. It lets out an indignant CAW and flies away with its quarter.")
                print("\n")
        else:
            type.type("You don't have any food to offer. The crow waits a moment longer, then flies away.")
            print("\n")
            type.type("You pocket the quarter though. Every bit helps.")
            self.change_balance(0.25)
        print("\n")
    
    def opossum_in_trash(self):
        """Encounter with Patches the opossum"""
        if self.has_companion("Patches"):
            self.day_event()
            return
        
        type.type("You step out of your car and hear rustling in a nearby garbage can. Something's in there.")
        print("\n")
        type.type("You approach cautiously and peer inside. Two beady eyes stare back at you.")
        print("\n")
        type.type("It's an opossum. A fat, ugly, beautiful opossum. It hisses at you, then plays dead.")
        print("\n")
        type.type("After a moment, one eye cracks open to see if you're still there.")
        print("\n")
        
        # Animal Whistle automatically befriends
        if self.has_item("Animal Whistle"):
            type.type("The " + magenta(bright("Animal Whistle")) + " hums softly. The opossum stops playing dead.")
            print("\n")
            type.type("It climbs out of the trash and waddles over to your car, like you're old friends.")
            print("\n")
            type.type("You name it " + cyan(bright("Patches")) + " because of the distinctive marks on its fur.")
            self.restore_sanity(5)
            self.add_companion("Patches")
            self.increment_statistic("companions_befriended")
            if not self.has_achievement("first_friend"):
                self.unlock_achievement("first_friend")
            print("\n")
            return
        
        answer = ask.yes_or_no("Try to befriend the trash gremlin? ")
        if answer == "yes":
            type.type("You slowly reach in with some food scraps. The opossum sniffs... then gently takes them from your hand.")
            print("\n")
            type.type("It climbs out of the trash and waddles over to your car, like it already owns the place.")
            print("\n")
            type.type("You name it " + cyan(bright("Patches")) + " because of the distinctive marks on its fur.")
            type.type(" It immediately curls up in your backseat and falls asleep.")
            self.restore_sanity(5)
            self.add_companion("Patches")
            self.increment_statistic("companions_befriended")
            if not self.has_achievement("first_friend"):
                self.unlock_achievement("first_friend")
        else:
            type.type("You back away slowly. The opossum continues playing dead until you're gone.")
            print("\n")
        print("\n")
    
    def raccoon_raid(self):
        """Encounter with Rusty the raccoon"""
        if self.has_companion("Rusty"):
            self.day_event()
            return
        
        type.type("A raccoon has somehow gotten into your car.")
        print("\n")
        type.type("It's sitting in the passenger seat, going through your things with its creepy little hands.")
        print("\n")
        type.type("When it notices you're awake, it freezes. You both stare at each other.")
        print("\n")
        answer = ask.yes_or_no("Try to catch it? ")
        if answer == "yes":
            chance = random.randrange(3)
            if chance == 0:
                type.type("The raccoon bites you and escapes out the window! That little thief!")
                print("\n")
                self.hurt(10)
                loss = random.randint(5, 20)
                type.type("You notice it stole " + red(bright("${:,}".format(loss))) + " from your stash!")
                self.change_balance(-loss)
            else:
                type.type("You manage to corner it with a blanket. It hisses and chitters angrily.")
                print("\n")
                type.type("But then... it calms down. It actually seems to like the warmth of the blanket.")
                print("\n")
                type.type("Over the next few hours, the raccoon refuses to leave. ")
                type.type("It keeps bringing you small objects. A bottle cap. A button. A tiny key.")
                print("\n")
                type.type("You name it " + cyan(bright("Rusty")) + " for its reddish-brown fur. It's your problem child now.")
                self.restore_sanity(5)
                self.add_companion("Rusty")
                self.increment_statistic("companions_befriended")
                if not self.has_achievement("first_friend"):
                    self.unlock_achievement("first_friend")
        else:
            type.type("You open the door and shoo it out. It takes its time leaving, like it's doing YOU a favor.")
            print("\n")
        print("\n")
    
    def sewer_rat(self):
        """Encounter with Slick the rat"""
        if self.has_companion("Slick"):
            self.day_event()
            return
        
        type.type("Through your car window, you spot a rat watching you from a storm drain. It seems... curious.")
        print("\n")
        type.type("Most rats run away. This one stays, twitching its whiskers.")
        print("\n")
        if self.has_item("Cheese") or self.has_item("Sandwich"):
            item = "Cheese" if self.has_item("Cheese") else "Sandwich"
            answer = ask.yes_or_no("Offer it some food? ")
            if answer == "yes":
                type.type("You toss a bit of " + item + " near the drain. The rat grabs it and disappears.")
                print("\n")
                type.type("But the next day, you find a small pile of coins near your car. And the rat, sitting nearby, watching.")
                print("\n")
                type.type("This continues for a week. You feed the rat, it brings you coins.")
                print("\n")
                type.type("Eventually, the rat just... moves in. You call it " + cyan(bright("Slick")) + ". It's very good at finding money.")
                self.change_balance(random.randint(5, 15))
                self.add_companion("Slick")
                self.increment_statistic("companions_befriended")
                if not self.has_achievement("first_friend"):
                    self.unlock_achievement("first_friend")
            else:
                type.type("You ignore the rat. It squeaks once, almost disappointed, and vanishes into the drain.")
                print("\n")
        else:
            type.type("You don't have any food to spare. The rat loses interest and scurries away.")
            print("\n")
        print("\n")
    
    def garden_rabbit(self):
        """Encounter with Hopper the rabbit"""
        if self.has_companion("Hopper"):
            self.day_event()
            return
        
        type.type("A fluffy white rabbit is nibbling on some weeds near your car.")
        print("\n")
        type.type("It's clearly someone's pet - it has a collar with no tag. But there's no owner in sight.")
        print("\n")
        type.type("The rabbit hops over to you, nose twitching. It seems friendly.")
        print("\n")
        answer = ask.yes_or_no("Take the rabbit with you? ")
        if answer == "yes":
            type.type("You gently pick up the rabbit. It doesn't struggle, just nestles into your arms.")
            print("\n")
            type.type("Something about its calm presence makes you feel... luckier.")
            print("\n")
            type.type("You name it " + cyan(bright("Hopper")) + ". Because of course you do.")
            self.restore_sanity(8)
            self.add_companion("Hopper")
            self.increment_statistic("companions_befriended")
            if not self.has_achievement("first_friend"):
                self.unlock_achievement("first_friend")
        else:
            type.type("You leave the rabbit be. It watches you drive away with those big, sad eyes.")
            print("\n")
            self.lose_sanity(2)
        print("\n")

    def conspiracy_theorist(self):
        type.type("A wild-eyed man knocks frantically on your car window.")
        print("\n")
        type.type(quote("THEY'RE LISTENING! THE BIRDS AREN'T REAL! THE CASINO IS A FRONT FOR THE LIZARD PEOPLE!"))
        print("\n")
        type.type("You nod politely while slowly rolling up your window.")
        print("\n")
        type.type(quote("DON'T TRUST THE DEALER! HE'S ONE OF THEM! HIS EYES—HAVE YOU SEEN HIS EYES?!"))
        print("\n")
        type.type("The window is fully up now. He keeps talking. You pretend to be asleep.")
        print("\n")
        self.lose_sanity(random.choice([2, 3, 4]))
        print("\n")

    def dropped_ice_cream(self):
        type.type("You step out of your car and treat yourself to an ice cream cone. A small luxury.")
        print("\n")
        type.type("You take one lick. One beautiful, perfect lick.")
        print("\n")
        type.type("And then it falls. Splat. Right onto the hot pavement.")
        print("\n")
        type.type("You stare at it. It stares back, melting. A metaphor for your dreams.")
        print("\n")
        self.lose_sanity(3)
        print("\n")

    def motivational_graffiti(self):
        type.type("Someone has spray-painted a message on the wall near your car:")
        print("\n")
        messages = [
            quote("YOU GOT THIS!") + " ...thanks, wall.",
            quote("BELIEVE IN YOURSELF!") + " Easy for you to say, you're concrete.",
            quote("THE HOUSE ALWAYS WINS") + " ...less motivational, more threatening.",
            quote("GARY WAS HERE") + " Cool, Gary. Good for you.",
            quote("THEY'RE WATCHING") + " That's... not helpful."
        ]
        type.type(random.choice(messages))
        print("\n")
        self.restore_sanity(1)
        print("\n")

    # ==========================================
    # MEGA EVENT BATCH - CHEAP TIER
    # ==========================================

    def yard_sale_find(self):
        type.type("You step out of your car and stumble upon a yard sale. The kind where everything costs a dollar.")
        print("\n")
        type.type("Most of it is junk, but one item catches your eye...")
        print("\n")
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
        print("\n")
        chance = random.randrange(3)
        if chance == 0:
            type.type("Later, you realize it's actually valuable! You sell it for " + green(bright("$" + str(random.randint(20, 75)))) + "!")
            self.change_balance(random.randint(20, 75))
        else:
            type.type("It's worthless, but it makes you feel lucky.")
            self.restore_sanity(2)
        print("\n")

    def broken_atm(self):
        type.type("You step out of your car and find an ATM that's clearly malfunctioning. The screen is glitching wildly.")
        print("\n")
        type.type("As you watch, it spits out a single $20 bill onto the ground.")
        print("\n")
        answer = ask.yes_or_no("Take the money? ")
        if answer == "yes":
            type.type("You grab it and run. Free money!")
            self.change_balance(20)
            print("\n")
            chance = random.randrange(5)
            if chance == 0:
                type.type("A security camera blinks red. You might have been seen...")
                self.add_danger("ATM Theft")
        else:
            type.type("You leave it. Someone else will take it. Honesty doesn't pay, but at least you can sleep at night.")
            self.restore_sanity(5)
        print("\n")

    def friendly_drunk(self):
        type.type("A very drunk man stumbles up to your car and starts talking to you like you're old friends.")
        print("\n")
        type.type(quote("BUDDY! There you are! I've been looking EVERYWHERE for you!"))
        print("\n")
        type.type("You've never met this person in your life.")
        print("\n")
        type.type(quote("Remember that time we... we did the thing? At the place? LEGENDARY!"))
        print("\n")
        type.type("He laughs hysterically, slaps your car twice, and wanders off into the night.")
        print("\n")
        chance = random.randrange(3)
        if chance == 0:
            type.type("Wait, he left his wallet on your hood. There's " + green(bright("$" + str(random.randint(15, 40)))) + " inside.")
            print("\n")
            answer = ask.yes_or_no("Keep it? ")
            if answer == "yes":
                self.change_balance(random.randint(15, 40))
            else:
                type.type("You chase him down and return it. He cries and hugs you. Awkward, but wholesome.")
                self.restore_sanity(5)
        print("\n")

    def car_wash_encounter(self):
        type.type("You take your car through an automatic car wash. The cheapest one, of course.")
        print("\n")
        type.type("As the brushes spin around you, you have a moment of zen. Just you and the suds.")
        print("\n")
        type.type("For three minutes, you forget about your problems. The water washes away your worries.")
        print("\n")
        self.restore_sanity(5)
        cost = random.randint(5, 10)
        type.type("It cost " + green(bright("$" + str(cost))) + ", but it was worth it.")
        self.change_balance(-cost)
        print("\n")

    def lottery_scratch(self):
        type.type("You head out from your car and buy a scratch-off lottery ticket. Just one. You can afford one, right?")
        print("\n")
        cost = 5
        if self.get_balance() < cost:
            type.type("Actually, you can't. You put it back. Sad.")
            print("\n")
            return
        self.change_balance(-cost)
        type.type("You scratch it with a coin, heart pounding...")
        print("\n")
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
        print("\n")

    def free_sample_spree(self):
        type.type("You leave your car and spend the morning hitting up grocery stores for free samples.")
        print("\n")
        type.type("Cheese cubes. Crackers. Some kind of dip. Tiny cups of juice.")
        print("\n")
        type.type("By the end, you've essentially eaten a full meal without spending a dime.")
        print("\n")
        type.type("The employees recognize you now. You can never go back. Worth it.")
        self.heal(15)
        self.restore_sanity(3)
        print("\n")

    def parking_lot_poker(self):
        if self.get_balance() < 20:
            self.day_event()
            return
        type.type("You step out of your car and see some guys playing poker on the hood of a truck in the parking lot.")
        print("\n")
        type.type(quote("Hey, you wanna join? Twenty bucks to buy in."))
        print("\n")
        answer = ask.yes_or_no("Join the game? ")
        if answer == "yes":
            self.change_balance(-20)
            print("\n")
            type.type("You play for an hour. It's fun. Reminds you why you got into this whole gambling thing.")
            print("\n")
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
        print("\n")

    def phone_scam_call(self):
        type.type("Your phone rings from the dashboard. Unknown number.")
        print("\n")
        type.type(quote("Hello! This is the IRS! You owe us $10,000 in back taxes! Pay immediately or go to jail!"))
        print("\n")
        answer = ask.yes_or_no("Hang up? ")
        if answer == "yes":
            type.type("You hang up. Obviously a scam. Your blood pressure is still elevated though.")
            self.lose_sanity(1)
        else:
            type.type(quote("Sir? Sir? Are you still there? Sir, we need your credit card—"))
            print("\n")
            type.type("You tell them exactly where they can shove their fake IRS, in creative detail.")
            print("\n")
            type.type("They hang up on YOU. Victory.")
            self.restore_sanity(3)
        print("\n")

    # ==========================================
    # MEGA EVENT BATCH - MODEST TIER
    # ==========================================

    def street_performer_duel(self):
        type.type("You step out of your car and see two street performers having a turf war. A violinist and a guy with a bucket drum.")
        print("\n")
        type.type("They're playing AT each other, trying to drown the other out. It's chaos.")
        print("\n")
        type.type("A crowd has gathered. This is the most entertainment this town has seen in weeks.")
        print("\n")
        answer = ask.option("Who do you tip? ", ["violinist", "drummer", "neither"])
        if answer == "violinist":
            type.type("You tip the violinist. She nods gracefully. The drummer flips you off.")
            self.change_balance(-5)
        elif answer == "drummer":
            type.type("You tip the drummer. He gives you a drumroll. The violinist looks betrayed.")
            self.change_balance(-5)
        else:
            type.type("You back away slowly. This isn't your fight.")
        print("\n")
        self.restore_sanity(3)
        print("\n")

    def compliment_stranger(self):
        type.type("You step out of your car when a random stranger stops you.")
        print("\n")
        compliments = [
            quote("Hey! I just wanted to say, you have really kind eyes."),
            quote("Excuse me, but you look like someone who's going through some stuff. Hang in there."),
            quote("I like your vibe. Keep doing whatever you're doing."),
            quote("You look like a main character. Whatever you're going through, you'll make it."),
            quote("Nice shoes!") + " (You're not even wearing nice shoes, but still.)"
        ]
        type.type(random.choice(compliments))
        print("\n")
        type.type("They walk away before you can respond. You stand there, oddly touched.")
        self.restore_sanity(random.choice([5, 7, 10]))
        print("\n")

    def forgotten_birthday(self):
        type.type("Your phone buzzes from the passenger seat. A Facebook notification.")
        print("\n")
        type.type("'Today is your birthday!'")
        print("\n")
        type.type("Oh. It... it IS your birthday. You completely forgot.")
        print("\n")
        type.type("You're alone. In a car. On your birthday. Living the dream.")
        print("\n")
        answer = ask.yes_or_no("Buy yourself a cupcake? ")
        if answer == "yes" and self.get_balance() >= 5:
            type.type("You buy a sad little cupcake from a gas station and stick a match in it.")
            print("\n")
            type.type("Happy birthday to you. Happy birthday to you...")
            print("\n")
            type.type("You blow it out. You wish for a million dollars. Obviously.")
            self.change_balance(-5)
            self.restore_sanity(5)
            self.heal(5)
        else:
            type.type("You don't celebrate. Just another day. You're one year closer to death. Fun.")
            self.lose_sanity(5)
        print("\n")

    def book_club_invite(self):
        type.type("You step out of your car and a woman hands you a flyer. 'JOIN OUR BOOK CLUB! Free snacks!'")
        print("\n")
        type.type("You haven't read a book since high school. But free snacks...")
        print("\n")
        answer = ask.yes_or_no("Attend the book club? ")
        if answer == "yes":
            type.type("You show up. The book is something about a woman finding herself in Tuscany.")
            print("\n")
            type.type("You haven't read it. Nobody has. Everyone just talks about their problems.")
            print("\n")
            type.type("The snacks ARE really good though. And the company isn't bad.")
            self.heal(10)
            self.restore_sanity(8)
        else:
            type.type("You crumple the flyer. Social interaction is for people with stable housing.")
        print("\n")

    def car_compliment(self):
        type.type("Someone taps on your window. You tense up, expecting trouble.")
        print("\n")
        type.type(quote("Hey man, nice car! Is this a classic?"))
        print("\n")
        type.type("It's not. It's a beat-up wagon held together by duct tape and prayer.")
        print("\n")
        type.type(quote("They don't make 'em like this anymore!"))
        print("\n")
        type.type("They're right, actually. Nobody makes cars this bad anymore. But you smile anyway.")
        self.restore_sanity(5)
        print("\n")

    def dog_walker_collision(self):
        type.type("You step out of your car and start walking when a pack of dogs on leashes barrels toward you.")
        print("\n")
        type.type("The dog walker—a small woman being dragged by six large dogs—yells " + quote("SORRY! THEY'RE FRIENDLY!"))
        print("\n")
        type.type("You get knocked over. You're covered in dog slobber. A golden retriever is standing on your chest.")
        print("\n")
        type.type("You've never been happier.")
        self.restore_sanity(10)
        self.heal(5)
        print("\n")

    def coffee_shop_philosopher(self):
        type.type("You head out from your car to grab a cheap coffee. You're nursing it when a philosophy student sits across from you, uninvited.")
        print("\n")
        type.type(quote("Have you ever considered that reality is just a simulation? That nothing we do matters?"))
        print("\n")
        type.type("You're a gambling addict who lives in a car. You've considered it.")
        print("\n")
        type.type(quote("Like, what if the universe is just a game? And we're all NPCs?"))
        print("\n")
        type.type("You excuse yourself before he can explain more. Your existential dread didn't need company.")
        self.lose_sanity(3)
        print("\n")

    def food_truck_festival(self):
        type.type("You step out of your car and stumble upon a food truck festival! Dozens of trucks, all kinds of cuisine.")
        print("\n")
        type.type("Tacos. Barbecue. Korean fusion. Some kind of gourmet grilled cheese situation.")
        print("\n")
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
        print("\n")

    # ==========================================
    # MEGA EVENT BATCH - RICH TIER
    # ==========================================

    def fancy_restaurant_mistake(self):
        type.type("You step out of your car and accidentally walk into a very fancy restaurant, thinking it's a diner.")
        print("\n")
        type.type("The maître d' looks at you with barely concealed horror.")
        print("\n")
        type.type(quote("Do you have a... reservation?"))
        print("\n")
        if self.get_balance() >= 200:
            answer = ask.yes_or_no("Stay and eat? ($200) ")
            if answer == "yes":
                type.type("You sit down. Order something French. Pretend you belong here.")
                print("\n")
                type.type("The food is incredible. Tiny portions, but incredible.")
                print("\n")
                type.type("You tip 20% because you're not a monster. Total: " + green(bright("$200")) + ".")
                self.change_balance(-200)
                self.heal(30)
                self.restore_sanity(15)
            else:
                type.type(quote("I'm just looking for the bathroom.") + " You leave with your dignity barely intact.")
        else:
            type.type("You mutter something about wrong building and flee.")
        print("\n")

    def autograph_request(self):
        type.type("You step out of your car and a teenager runs up to you. " + quote("OH MY GOD! Can I get a photo?!"))
        print("\n")
        type.type("You have no idea why. You're not famous. Are you?")
        print("\n")
        type.type(quote("You're... you're that guy from the thing! Right?!"))
        print("\n")
        answer = ask.yes_or_no("Play along? ")
        if answer == "yes":
            type.type("You pose for the photo. Sign an autograph. Make something up.")
            print("\n")
            type.type(quote("Oh wow, thank you so much! Wait till I show my friends!"))
            print("\n")
            type.type("They run off, thrilled. You have no idea who they thought you were.")
            self.restore_sanity(10)
        else:
            type.type(quote("I think you have the wrong person."))
            print("\n")
            type.type("Their face falls. " + quote("Oh... sorry...") + " They walk away, embarrassed.")
            type.type(" You feel bad for crushing their excitement.")
        print("\n")

    def casino_regular(self):
        type.type("You step out of your car and head to the casino. One of the regulars recognizes you. An old woman with way too much jewelry.")
        print("\n")
        type.type(quote("You! I remember you! You're the one who won big last week!"))
        print("\n")
        type.type("She grabs your arm with surprising strength.")
        print("\n")
        type.type(quote("Touch my chips for luck! You're my good luck charm now!"))
        print("\n")
        type.type("You awkwardly touch her chips. She wins $50. She gives you $20 for your trouble.")
        self.change_balance(20)
        print("\n")
        type.type("You're not sure how to feel about being a human rabbit's foot.")
        print("\n")

    def mysterious_package(self):
        type.type("You return to your car to find a package on the hood. No label. No note. Just a box.")
        print("\n")
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
                print("\n")
                type.type("You throw it away and check over your shoulder for the rest of the day.")
                self.lose_sanity(5)
            elif chance == 2:
                type.type("Inside: a single playing card. The Ace of Spades. No explanation.")
                print("\n")
                type.type("It feels significant. Or maybe someone's messing with you.")
                self.lose_sanity(3)
            else:
                type.type("It's empty. Completely empty. That's somehow worse than anything.")
                self.lose_sanity(7)
        else:
            type.type("You throw it away without opening it. Some mysteries are better left unsolved.")
        print("\n")

    def rich_persons_problems(self):
        type.type("You step out of your car and overhear two rich people complaining at a café.")
        print("\n")
        type.type(quote("My Maserati is in the shop AGAIN. I have to drive my backup Porsche."))
        print()
        type.type(quote("Ugh, I know. My yacht needs new curtains and my decorator is on vacation in BALI."))
        print("\n")
        type.type("You make eye contact with a barista. They roll their eyes. Solidarity.")
        self.restore_sanity(3)
        print("\n")

    def investment_pitch(self):
        type.type("You step out of your car and a guy in a cheap suit corners you with a 'business opportunity.'")
        print("\n")
        type.type(quote("Crypto. NFTs. AI. Blockchain. Web3. It's gonna be HUGE. I just need investors."))
        print("\n")
        type.type("He's sweating. You recognize the desperation. You've seen it in the mirror.")
        print("\n")
        answer = ask.yes_or_no("Give him $100 to make him go away? ")
        if answer == "yes" and self.get_balance() >= 100:
            type.type("You hand over the money. He promises you'll get 10x returns.")
            print("\n")
            type.type("You'll never see him or that money again. But at least he's gone.")
            self.change_balance(-100)
        else:
            type.type("You decline. He follows you for half a block before giving up.")
        print("\n")

    # ==========================================
    # MEGA EVENT BATCH - DOUGHMAN TIER
    # ==========================================

    def wealth_paranoia(self):
        type.type("You've started hiding money in weird places. Under the floor mat. In the glove box. In your shoes.")
        print("\n")
        type.type("You can't remember where you put all of it. Was it $500 in the spare tire? Or $700?")
        print("\n")
        type.type("You spend an hour searching your own car like a crazy person.")
        print("\n")
        chance = random.randrange(3)
        if chance == 0:
            amount = random.randint(50, 150)
            type.type("You find an extra " + green(bright("$" + str(amount))) + " you forgot about! Nice!")
            self.change_balance(amount)
        else:
            type.type("You find nothing. Either you already counted it, or you're losing your mind.")
            self.lose_sanity(3)
        print("\n")

    def high_roller_room(self):
        if self.has_met("High Roller Room"):
            self.day_event()
            return
        self.meet("High Roller Room")
        type.type("You step out of your car and a casino employee approaches you with unusual deference.")
        print("\n")
        type.type(quote("Sir, based on your... recent activities... we'd like to invite you to our High Roller Lounge."))
        print("\n")
        type.type("They hand you a black keycard.")
        print("\n")
        type.type(quote("Free drinks. Private tables. Higher limits. You've earned it."))
        print("\n")
        type.type("You pocket the card. You're not sure if this is an honor or a trap.")
        self.add_item("High Roller Keycard")
        print("\n")

    def old_rival_returns(self):
        if self.has_met("Old Rival"):
            self.day_event()
            return
        self.meet("Old Rival")
        type.type("You step out of your car and head to the casino. A familiar face appears. Someone from your past.")
        print("\n")
        type.type("Jake Morrison. You used to work together, before... everything.")
        print("\n")
        type.type(quote("Well, well. Look who it is. Still chasing the dragon, huh?"))
        print("\n")
        type.type("He looks good. Successful. Happy. Everything you're not.")
        print("\n")
        type.type(quote("I heard you were doing... this.") + " He gestures vaguely at your existence. " + quote("Good luck with that."))
        print("\n")
        type.type("He walks away. The smugness lingers like a bad smell.")
        self.lose_sanity(10)
        print("\n")

    def casino_comps(self):
        type.type("You find a gift bag on your car's hood. The casino sent you free stuff. Trying to keep you gambling, obviously.")
        print("\n")
        items = [
            ("a free buffet voucher", 0, 20, 0),
            ("a free hotel room for the night", 0, 0, 15),
            ("$50 in free chips", 50, 0, 5),
            ("a branded jacket that's actually pretty nice", 0, 0, 10),
            ("tickets to a show you have no interest in", 0, 0, 3)
        ]
        item, money, health, sanity = random.choice(items)
        type.type("Today's gift: " + item + ".")
        print("\n")
        if money > 0:
            type.type("The chips are worth " + green(bright("$" + str(money))) + " if you cash out.")
            self.change_balance(money)
        if health > 0:
            type.type("The buffet is incredible. You eat like a king.")
            self.heal(health)
        if sanity > 0:
            type.type("You feel oddly appreciated. Even if it's just manipulation.")
            self.restore_sanity(sanity)
        print("\n")

    def millionaire_milestone(self):
        if self.get_balance() >= 900000 and not self.has_met("Almost There Moment"):
            self.meet("Almost There Moment")
            type.type("Sitting in your car, you're looking at your balance. It's so close to a million. SO close.")
            print("\n")
            type.type("Your hands are shaking. You can barely breathe.")
            print("\n")
            type.type("One more good night. One more lucky streak. One more...")
            print("\n")
            type.type("What will you even do when you win? You've been chasing this for so long.")
            print("\n")
            type.type("You realize you haven't thought that far ahead. You've only ever thought about winning.")
            print("\n")
            type.type("What happens after?")
            self.lose_sanity(5)
            self.restore_sanity(10)  # Net positive, but conflicted
            print("\n")
        else:
            self.day_event()

    # ==========================================
    # MEGA EVENT BATCH - NEARLY THERE TIER
    # ==========================================

    def the_final_temptation(self):
        type.type("A stranger approaches your car outside the casino. Well-dressed. Confident. Unsettling.")
        print("\n")
        type.type(quote("You're close, aren't you? I can tell. The million."))
        print("\n")
        type.type("How does he know? You didn't tell anyone.")
        print("\n")
        type.type(quote("I can guarantee your victory. Tonight. One hand. You'll win everything."))
        print("\n")
        type.type("He leans in. His eyes are... wrong. Too dark. Too deep.")
        print("\n")
        type.type(quote("All it costs is something small. Something you won't even miss."))
        print("\n")
        answer = ask.yes_or_no("Accept his offer? ")
        if answer == "yes":
            type.type("You shake his hand. It's ice cold.")
            print("\n")
            type.type(quote("Excellent. I'll see you at the tables."))
            print("\n")
            type.type("He disappears into the crowd. You feel different. Lighter. Emptier.")
            self.lose_sanity(25)
            self.add_danger("Devil's Bargain")
            self.change_balance(random.randint(10000, 50000))
        else:
            type.type("You walk away. He doesn't follow. When you look back, he's gone.")
            print("\n")
            type.type("The right choice. Probably. Maybe.")
            self.restore_sanity(10)
        print("\n")

    def reporters_found_you(self):
        type.type("A reporter has tracked you down to your car. Camera crew and everything.")
        print("\n")
        type.type(quote("Local Gambler Attempts Million Dollar Challenge! How do you feel about your chances?"))
        print("\n")
        type.type("They shove a microphone in your face.")
        print("\n")
        answer = ask.option("What do you say? ", ["confident", "humble", "no comment"])
        if answer == "confident":
            type.type(quote("I've got this. The million is mine. Watch me."))
            print("\n")
            type.type("You'll either look like a legend or an idiot tomorrow.")
        elif answer == "humble":
            type.type(quote("I'm just taking it one day at a time. Anything can happen."))
            print("\n")
            type.type("Boring, but safe.")
        else:
            type.type("You push past them without a word.")
            print("\n")
            type.type(quote("Mysterious! We love it! The Silent Gambler!"))
        print("\n")
        type.type("Great. Now everyone knows who you are.")
        self.meet("Media Attention")
        print("\n")

    def casino_owner_meeting(self):
        if self.has_met("Casino Owner"):
            self.day_event()
            return
        self.meet("Casino Owner")
        type.type("You step out of your car and head to the casino. An employee pulls you aside. " + quote("The owner would like to meet you."))
        print("\n")
        type.type("You're led to a private office. Leather furniture. Cigar smoke. Old money.")
        print("\n")
        type.type("The owner is ancient. Wrinkled. Eyes like a shark.")
        print("\n")
        type.type(quote("You're quite the player. I've been watching you."))
        print("\n")
        type.type("He offers you a drink. You're not sure if this is hospitality or intimidation.")
        print("\n")
        type.type(quote("Make your million. Take your victory lap. But remember—the house always wins eventually."))
        print("\n")
        type.type("He smiles, but it doesn't reach his eyes.")
        print("\n")
        type.type(quote("Come back anytime. We'll be waiting."))
        self.lose_sanity(10)
        print("\n")

    # ==========================================
    # NEW CREATIVE EVENTS - SILLY, WEIRD, DARK, GOOFY
    # Imported from new_creative_events.py
    # ==========================================

    # SILLY EVENTS
    def duck_army(self):
        # EVENT: A parade of 30+ ducks in formation appears, led by one with a tiny top hat
        # EFFECTS: Follow = led to fountain with coins (50% chance +$15-50), +3 sanity; Decline = miss something magical
        type.type("You hear it before you see it through your windshield. Quacking. So much quacking.")
        print("\n")
        type.type("Around the corner comes a parade of ducks. At least thirty of them, waddling in perfect formation.")
        print("\n")
        type.type("The lead duck - wearing what appears to be a tiny top hat - stops in front of you and quacks authoritatively.")
        print("\n")
        
        # Animal Whistle befriends the duck general
        if self.has_item("Animal Whistle") and not self.has_companion("General Quackers"):
            type.type("The " + magenta(bright("Animal Whistle")) + " sounds. All thirty ducks stop and turn toward you in perfect unison.")
            print("\n")
            type.type("The top hat duck waddles forward and salutes with one wing. The entire army salutes.")
            print("\n")
            type.type("The general has recognized you as their commander. The duck waddles up and settles at your feet.")
            print("\n")
            type.type("You've been given command of a duck army. The general's name is " + cyan(bright("General Quackers")) + ".")
            print("\n")
            type.type("General Quackers will ride with you now. The rest of the army disperses, awaiting your orders.")
            self.add_companion("General Quackers", "Duck Commander")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.restore_sanity(5)
            print("\n")
            return
        
        answer = ask.yes_or_no("Follow the duck parade? ")
        if answer == "yes":
            type.type("You fall in line behind the ducks. People stare. You don't care.")
            print("\n")
            type.type("The parade leads you through alleys, across a parking lot, and finally to... a fountain full of coins.")
            print("\n")
            type.type("The top hat duck looks at you, then at the fountain, then quacks approvingly.")
            print("\n")
            if random.random() < 0.5:
                amount = random.randint(15, 50)
                type.type("You fish out " + green(bright("$" + str(amount))) + " in loose change. The ducks quack in celebration.")
                self.change_balance(amount)
            else:
                type.type("Before you can grab any coins, a security guard chases you off. The ducks scatter, laughing in quacks.")
            self.restore_sanity(3)
        else:
            type.type("You wave goodbye to the duck parade. The top hat duck gives you a disapproving quack.")
            print("\n")
            type.type("Somehow, you feel like you've missed out on something magical.")
        print("\n")

    def sentient_sandwich(self):
        # EVENT: Your sandwich becomes sentient and yells at you before being eaten
        # EFFECTS: Eat = +10 HP, -5 sanity; Apologize = +3 sanity; Throw = -3 sanity
        type.type("Sitting in your car, you're about to bite into your sandwich when it speaks.")
        print("\n")
        type.type(quote("Hey buddy, whatcha doing there?"))
        print("\n")
        type.type("You freeze, sandwich inches from your mouth.")
        print("\n")
        type.type(quote("I said, WHATCHA DOING? You were about to eat me, weren't you? WEREN'T YOU?!"))
        print("\n")
        answer = ask.option("What do you do? ", ["eat it anyway", "apologize", "throw it"])
        if answer == "eat it anyway":
            type.type("You take a defiant bite. The sandwich screams. You keep chewing.")
            print("\n")
            type.type(quote("THIS IS NOT HOW I WANTED TO GO!"))
            print("\n")
            type.type("You finish eating in uncomfortable silence. The sandwich was delicious.")
            self.heal(10)
            self.lose_sanity(5)
        elif answer == "apologize":
            type.type(quote("I'm... sorry? I didn't know you were sentient."))
            print("\n")
            type.type("The sandwich sighs. " + quote("That's what they all say. Look, just put me down somewhere nice. With a view."))
            print("\n")
            type.type("You place the sandwich on a park bench facing the sunset. It seems happy.")
            print("\n")
            type.type("You're still hungry, though.")
            self.restore_sanity(3)
        else:
            type.type("You hurl the sandwich as far as you can. It screams the whole way.")
            print("\n")
            type.type(quote("WORTH IIIIIIIT!"))
            print("\n")
            type.type("A distant splat. Then silence. You decide to skip lunch today.")
            self.lose_sanity(3)
        print("\n")

    def motivational_raccoon(self):
        # EVENT: A fat raccoon gives you an inspirational pep talk about life
        # EFFECTS: +10 sanity from trash panda wisdom
        type.type("A fat raccoon waddles up to your car and sits on the hood. It stares at you through the windshield with beady, knowing eyes.")
        print("\n")
        type.type("Then, impossibly, it speaks.")
        print("\n")
        type.type(quote("Hey. You. Yeah, you. The gambler living in a car."))
        print("\n")
        type.type("You blink. The raccoon continues.")
        print("\n")
        type.type(quote("Look, I eat garbage for a living. GARBAGE. And you know what? I'm happy. You know why?"))
        print("\n")
        type.type("You shake your head, dumbfounded.")
        print("\n")
        type.type(quote("Because I don't compare myself to other raccoons. I just do my thing. Eat trash. Wash my hands. Live my life."))
        print("\n")
        type.type(quote("You? You're out here chasing a million dollars. That's YOUR garbage. And that's beautiful, man."))
        print("\n")
        type.type("The raccoon stands up, brushes off its fur, and waddles away.")
        print("\n")
        type.type(quote("Go get that garbage, champ!"))
        print("\n")
        type.type("You... you feel strangely inspired.")
        self.restore_sanity(10)
        print("\n")

    def pigeon_mafia(self):
        # EVENT: 30+ pigeons land on your car led by one with a tiny hat, demanding tribute
        # EFFECTS: Pay = -$5 or give granola bar, get bottle cap gift; Refuse = -$30 cleaning + -5 sanity
        type.type("A pigeon lands on your car. Then another. Then thirty more.")
        print("\n")
        type.type("They're all staring at you. Cooing in unison. It's unsettling.")
        print("\n")
        type.type("One pigeon - bigger than the others, wearing a tiny hat - steps forward.")
        print("\n")
        type.type("It coos menacingly.")
        print("\n")
        
        # Animal Whistle befriends the pigeon boss
        if self.has_item("Animal Whistle") and not self.has_companion("Don Coo"):
            type.type("The " + magenta(bright("Animal Whistle")) + " hums. All thirty pigeons go silent. They look at each other in confusion.")
            print("\n")
            type.type("The boss pigeon tilts its tiny-hatted head. Then, slowly, it bows.")
            print("\n")
            type.type("You've earned the respect of the Pigeon Mafia. The boss pigeon hops onto your shoulder.")
            print("\n")
            type.type("You decide to call the pigeon boss " + cyan(bright("Don Coo")) + ".")
            print("\n")
            type.type("Don Coo will ride with you now. The other pigeons salute as you drive away. ")
            type.type("You're protected by the family now.")
            self.add_companion("Don Coo", "Pigeon Boss")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.add_status("Pigeon King")
            print("\n")
            return
        
        type.type("Somehow, you understand perfectly: this is pigeon territory. You owe the pigeon boss.")
        print("\n")
        answer = ask.yes_or_no("Throw them some bread/money as tribute? ")
        if answer == "yes":
            type.type("You scramble to find something - anything - to offer.")
            print("\n")
            if random.random() < 0.5:
                type.type("You toss " + green(bright("$5")) + " worth of crumbs and loose change.")
                self.change_balance(-5)
                print("\n")
                type.type("The pigeon boss nods sagely. The flock disperses. You're safe. For now.")
            else:
                type.type("You throw your last granola bar. The boss tastes it... and approves!")
                print("\n")
                type.type("The pigeons leave a shiny bottle cap as a gift. It's worthless. You're touched anyway.")
        else:
            type.type("You refuse to pay tribute to BIRDS.")
            print("\n")
            type.type("The boss pigeon coos once. The entire flock takes off.")
            print("\n")
            type.type("Your car is COVERED in... you don't want to think about what your car is covered in.")
            type.type(" Cleaning it costs you " + red("$30") + ".")
            self.change_balance(-30)
            self.lose_sanity(5)
        print("\n")

    def sock_puppet_therapist(self):
        # EVENT: Man with sock puppet "Dr. Socksworth" offers therapy (low sanity only)
        # CONDITION: Sanity < 60
        # EFFECTS: Accept = pour heart out, +15 sanity; Refuse = -2 sanity from judgment
        if self.get_sanity() >= 60:
            self.day_event()
            return
        type.type("You step out of your car and a man sits down next to you on the curb. He has a sock puppet on his hand. It's wearing tiny glasses.")
        print("\n")
        type.type("The puppet turns to you. " + quote("You look troubled. Want to talk about it?"))
        print("\n")
        type.type("You're about to walk away when the man speaks: " + quote("Dr. Socksworth is a licensed therapist. Technically."))
        print("\n")
        answer = ask.yes_or_no("Talk to... Dr. Socksworth? ")
        if answer == "yes":
            type.type("You pour your heart out to a sock puppet. This is your life now.")
            print("\n")
            type.type("Dr. Socksworth listens attentively. " + quote("Mm-hmm. Yes. I see. And how does that make you feel?"))
            print("\n")
            type.type("Somehow, against all odds, you feel BETTER.")
            print("\n")
            type.type("The sock puppet gives you a tiny pamphlet: 'COPING MECHANISMS FOR GAMBLERS: A SOCK'S GUIDE'")
            print("\n")
            type.type("You keep it. It's strangely helpful.")
            self.restore_sanity(15)
        else:
            type.type("You walk away. Dr. Socksworth calls after you:")
            print("\n")
            type.type(quote("RUNNING FROM YOUR PROBLEMS WON'T SOLVE ANYTHING!"))
            print("\n")
            type.type("A sock has never made you feel so judged.")
            self.lose_sanity(2)
        print("\n")

    # WEIRD EVENTS
    def time_loop(self):
        # EVENT: Experience the same morning 3 times, must break the loop
        # EFFECTS: Save bird = +$50, meet "Time Bird"; Ignore phone = +5 sanity; Scream = -5 sanity
        type.type("The clock on your car dashboard says 8:47 AM.")
        print("\n")
        type.type("You go to brush your teeth. A bird hits the window. Your phone buzzes.")
        print("\n")
        type.type("You wake up. The clock says 8:47 AM.")
        print("\n")
        type.type("Wait. What?")
        print("\n")
        type.type("You go to brush your teeth. You KNOW a bird is about to hit the window. It does. Your phone buzzes.")
        print("\n")
        type.type("You wake up. The clock says 8:47 AM.")
        print("\n")
        type.type("This is the third time. You're sure of it now.")
        print("\n")
        answer = ask.option("What do you do differently? ", ["save the bird", "ignore your phone", "scream"])
        if answer == "save the bird":
            type.type("You stand at the window, waiting. The bird approaches. You OPEN the window!")
            print("\n")
            type.type("The bird flies through, circles your head, and drops something shiny before flying away.")
            print("\n")
            type.type("A golden coin. Worth " + green(bright("$50")) + ". The loop breaks.")
            self.change_balance(50)
            self.meet("Time Bird")
        elif answer == "ignore your phone":
            type.type("You don't check your phone. The buzzing stops. The loop... freezes.")
            print("\n")
            type.type("For a moment, time itself seems to hold its breath.")
            print("\n")
            type.type("Then everything resumes. Normal. But you remember all three loops.")
            self.restore_sanity(5)
        else:
            type.type("You SCREAM at 8:47 AM. The neighbors probably hate you.")
            print("\n")
            type.type("But it works! The loop shatters. You stumble forward, free.")
            print("\n")
            type.type("You've lost 3 hours somewhere. Or gained them? Time is weird now.")
            self.lose_sanity(5)
        print("\n")

    def mirror_stranger(self):
        # EVENT: Your reflection acts independently and holds up a sign saying "SOON"
        # EFFECTS: 30% find encouraging note from reflection (+5 sanity); 70% avoid mirrors all day (-8 sanity)
        type.type("You catch your reflection in the car mirror. It smiles.")
        print("\n")
        type.type("You're not smiling.")
        print("\n")
        type.type("The reflection waves. You don't move your hand.")
        print("\n")
        type.type("It holds up a sign. Written in what might be blood: 'SOON.'")
        print("\n")
        type.type("You blink. The reflection is normal again. Just you, looking terrified.")
        print("\n")
        if random.random() < 0.3:
            type.type("In the back seat, you notice something that wasn't there before.")
            type.type(" A note, in your own handwriting: 'You're doing fine. Keep going.'")
            print("\n")
            type.type("Did the reflection... leave it?")
            self.restore_sanity(5)
        else:
            type.type("You avoid mirrors for the rest of the day. Just to be safe.")
            self.lose_sanity(8)
        print("\n")

    def the_glitch(self):
        # EVENT: Reality glitches around you (low sanity only)
        # CONDITION: Sanity < 50
        # EFFECTS: Random - money change (-$100 to +$200), health (-15 to +25), time skip, or identity confusion (-10 sanity)
        if self.get_sanity() >= 50:
            self.day_event()
            return
        type.type("Sitting in your car, reality... stutters.")
        print("\n")
        type.type("The colors around you shift. Blue becomes green. Green becomes screaming.")
        print("\n")
        type.type("Wait, that's not right.")
        print("\n")
        type.type("You look at your hands. You have seven fingers. No, six. No, the normal amount. Maybe.")
        print("\n")
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
        print("\n")
        type.type("Reality snaps back. Everything is normal. Everything is fine.")
        print("\n")
        type.type("Is it?")
        print("\n")

    def wrong_universe(self):
        # EVENT: Slip into alternate dimension with purple sky and floating cars
        # EFFECTS: Meet alternate rich self, get Dimensional Coin item (50%) or $100-300 (50%), -10 sanity
        type.type("You step out of your car and around a corner. The world changes.")
        print("\n")
        type.type("The sky is purple. The buildings are organic, pulsing like living things.")
        type.type(" Cars float. People have too many eyes. A dog speaks fluent French.")
        print("\n")
        type.type("This is not your world.")
        print("\n")
        type.type("A version of yourself approaches. They're taller, more confident. Richer, clearly.")
        print("\n")
        type.type(quote("Ah, another me. Let me guess - you're from a world where you're still struggling?"))
        print("\n")
        type.type("You nod, dumbstruck.")
        print("\n")
        type.type(quote("Pathetic. Well, take this. It won't help much, but it's something."))
        print("\n")
        if random.random() < 0.5:
            type.type("They hand you a strange coin. It hums with otherworldly energy.")
            self.add_item("Dimensional Coin")
            type.type(" You got a " + magenta(bright("Dimensional Coin")) + "!")
        else:
            amount = random.randint(100, 300)
            type.type("They hand you a wad of bills. The denominations don't exist in your world, but...")
            type.type(" Somehow they translate to " + green(bright("$" + str(amount))) + "!")
            self.change_balance(amount)
        print("\n")
        type.type("The world flickers. Shifts. You're back in the normal universe.")
        print("\n")
        type.type("Was any of that real?")
        self.lose_sanity(10)
        print("\n")

    def fourth_wall_break(self):
        # EVENT: A stranger becomes aware they're in a game, breaks the fourth wall
        # EFFECTS: -15 sanity from existential dread
        type.type("A stranger approaches your car. They look... worried.")
        print("\n")
        type.type(quote("Hey. You. Can you keep a secret?"))
        print("\n")
        type.type("Before you can answer, they lean in close.")
        print("\n")
        type.type(quote("I think... I think none of this is real. I think we're in some kind of... game. Or story."))
        print("\n")
        type.type("You laugh nervously. " + quote("That's crazy talk."))
        print("\n")
        type.type(quote("Is it? Think about it. The same things happen over and over. There's a PATTERN. And you..."))
        print("\n")
        type.type(quote("You're the main character, aren't you? Everyone else is just... background."))
        print("\n")
        type.type("The stranger starts crying.")
        print("\n")
        type.type(quote("Am I even real? Do I exist when you're not looking at me?"))
        print("\n")
        type.type("They walk away, still crying. You stand there, deeply unsettled.")
        print("\n")
        type.type("...")
        print("\n")
        type.type("You glance at the 'player.' The one reading this. Just for a second.")
        print("\n")
        self.lose_sanity(15)
        print("\n")

    # DARK EVENTS
    def the_collector(self):
        # EVENT: Man in black suit collects debts, favors, and "souls"
        # EFFECTS: Meet "The Collector", various sanity loss based on choice
        type.type("You look up from your car. A man in a black suit steps out of the shadows. His smile doesn't reach his eyes.")
        print("\n")
        type.type(quote("You've been making moves. Big moves. People notice."))
        print("\n")
        type.type("He produces a small notebook and flips through it.")
        print("\n")
        type.type(quote("According to my records, you owe... well, you don't owe ME anything. Yet."))
        print("\n")
        type.type(quote("But I'm here to offer a service. I collect things. Debts. Favors. Souls, sometimes."))
        print("\n")
        type.type("He chuckles. It's not a friendly sound.")
        print("\n")
        answer = ask.option("What do you say? ", ["not interested", "what are you offering", "souls?"])
        if answer == "not interested":
            type.type("He shrugs. " + quote("Everyone says that at first. I'll be around."))
            print("\n")
            type.type("He vanishes into the shadows. You didn't see him go. He was just... gone.")
            self.meet("The Collector")
        elif answer == "what are you offering":
            type.type(quote("Information. Protection. Future knowledge. Whatever you need, I can provide."))
            print("\n")
            type.type(quote("My price is... flexible. Sometimes money. Sometimes favors. Sometimes..."))
            print("\n")
            type.type("He leans in close. " + quote("...years."))
            print("\n")
            type.type("You step back. He laughs.")
            print("\n")
            type.type(quote("Not ready yet. That's fine. When you are, I'll know."))
            self.meet("The Collector")
            self.lose_sanity(10)
        else:
            type.type(quote("Souls? Oh, that's mostly a metaphor. Mostly."))
            print("\n")
            type.type("His smile widens just a bit too far.")
            print("\n")
            type.type(quote("Don't worry about souls. You've still got yours. For now."))
            self.meet("The Collector")
            self.lose_sanity(15)
        print("\n")

    def the_empty_room(self):
        # EVENT: Find a door that shouldn't exist, leads to infinite white void with creature
        # CONDITION: Sanity < 40
        # EFFECTS: -20 sanity, gain "Glimpsed the Void" status
        if self.get_sanity() >= 40:
            self.day_event()
            return
        type.type("You step out of your car and notice a door you've never seen before. It's in a wall that shouldn't have a door.")
        print("\n")
        type.type("Something tells you not to open it. Something screams at you to run.")
        print("\n")
        type.type("You open it anyway. Of course you do.")
        print("\n")
        type.type("Inside is... empty. Completely, perfectly empty. No floor, no walls, no ceiling.")
        type.type(" Just white. Endless white in every direction.")
        print("\n")
        type.type("You step inside. Your footsteps make no sound. You are nowhere.")
        print("\n")
        type.type("And then you see it.")
        print("\n")
        type.type("In the distance. Getting closer. Something that has too many limbs and not enough face.")
        print("\n")
        type.type("You run. Back through the door. SLAM it shut.")
        print("\n")
        type.type("When you turn around, the door is gone. The wall is smooth. Like the door never existed.")
        print("\n")
        type.type("But you can still hear scratching from inside the wall.")
        self.lose_sanity(20)
        self.add_status("Glimpsed the Void")
        print("\n")

    def blood_moon_bargain(self):
        # EVENT: On a blood red moon, dark forces offer one night of perfect luck for one year of life
        # EFFECTS: Accept = "Blood Moon Luck" + "Year Shorter" status, -20 sanity; Reject = +5 sanity
        type.type("Through your windshield, the sky is wrong. The light filtering in is red. Blood red. The color of things that shouldn't be.")
        print("\n")
        type.type("You hear a voice inside your car. It comes from nowhere and everywhere.")
        print("\n")
        type.type(cyan(quote("GAMBLER. WE HAVE WATCHED YOU.")))
        print("\n")
        type.type("You look around. There's no one there. Just shadows that move wrong.")
        print("\n")
        type.type(cyan(quote("WE OFFER A BARGAIN. ONE NIGHT OF PERFECT LUCK. EVERY HAND A WINNER.")))
        print("\n")
        type.type(cyan(quote("IN EXCHANGE... ONE YEAR OF YOUR LIFE. BURNED FROM THE END. GONE FOREVER.")))
        print("\n")
        answer = ask.yes_or_no("Accept the blood moon bargain? ")
        if answer == "yes":
            type.type("You speak into the darkness. " + quote("I accept."))
            print("\n")
            type.type("The shadows LAUGH. A contract burns itself into your arm. It's painless, somehow worse than pain.")
            print("\n")
            type.type(cyan(quote("DONE. TONIGHT, YOU CANNOT LOSE. BUT TOMORROW, YOU WILL FEEL IT. THE MISSING TIME.")))
            print("\n")
            type.type("The red moon seems to glow brighter. You feel different. Powerful. Cursed.")
            self.add_status("Blood Moon Luck")
            self.add_status("Year Shorter")
            self.lose_sanity(20)
        else:
            type.type("You shake your head. " + quote("No. I'll take my chances the normal way."))
            print("\n")
            type.type("The shadows hiss in displeasure.")
            print("\n")
            type.type(cyan(quote("FOOLISH. BUT BRAVE. WE WILL WATCH. WE ARE ALWAYS WATCHING.")))
            print("\n")
            type.type("The red moon fades to normal. You've made an enemy tonight. Or escaped one.")
            self.restore_sanity(5)
            self.meet("Rejected the Shadows")
        print("\n")

    # GOOFY EVENTS
    def alien_abduction(self):
        # EVENT: Briefly abducted by aliens at 2 AM, returned with missing time
        # EFFECTS: Random - money (+$50-200), health (+30 HP, +10 sanity), Alien Crystal item, or nothing (-10 sanity)
        type.type("A bright light floods your car. You float up. Through the roof. This shouldn't be possible.")
        print("\n")
        type.type("Everything goes white.")
        print("\n")
        type.type("...")
        print("\n")
        type.type("You wake up three hours later in your car. You don't remember anything.")
        print("\n")
        type.type("But there's a new mark on your arm: a tiny UFO tattoo that wasn't there before.")
        print("\n")
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
        print("\n")

    def dance_battle(self):
        # EVENT: Street gang challenges you to a dance-off
        # EFFECTS: Win (score >= 2) = +$25-75, +5 sanity; Tie = pass with respect; Lose = -$15, -3 sanity
        type.type("You step out of your car and a group of teenagers blocks your path. Their leader steps forward.")
        print("\n")
        type.type(quote("Yo! This is our turf. You wanna pass? You gotta DANCE."))
        print("\n")
        type.type("A boombox appears. Music starts playing. The crowd forms a circle.")
        print("\n")
        type.type("It's dance battle time. What's your move?")
        print("\n")
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
        print("\n")
        if score >= 2:
            type.type("You WIN the dance battle! The gang cheers!")
            print("\n")
            reward = random.randint(25, 75)
            type.type("They shower you with singles. You collect " + green(bright("$" + str(reward))) + "!")
            self.change_balance(reward)
            self.restore_sanity(5)
        elif score >= 0:
            type.type("It's a TIE! The gang respects your effort.")
            print("\n")
            type.type(quote("You got moves, old timer. You can pass."))
        else:
            type.type("You LOSE. The gang boos you mercilessly.")
            print("\n")
            type.type("They take your lunch money. Literally. " + red("(-$15)"))
            self.change_balance(-15)
            self.lose_sanity(3)
        print("\n")

    # ==========================================
    # NEW SECRET EVENTS - HIDDEN TRIGGERS
    # ==========================================

    def exactly_100(self):
        # SECRET: Have exactly $100 - a crisp benjamin
        if self.get_balance() != 100:
            self.day_event()
            return
        type.type("You count your money. Exactly " + green(bright("$100")) + ". One crisp Benjamin Franklin.")
        print("\n")
        type.type("As you hold the bill up to the light, you swear Ben winks at you.")
        print("\n")
        type.type(quote("Keep going, kid. You've got this."))
        print("\n")
        type.type("You blink. The bill is normal. But you feel strangely confident.")
        self.restore_sanity(5)
        self.add_status("Benjamin's Blessing")
        print("\n")

    def exactly_420(self):
        # SECRET: Have exactly $420 - the funny number
        if self.get_balance() != 420:
            self.day_event()
            return
        type.type("You count your money. Exactly " + green(bright("$420")) + ".")
        print("\n")
        type.type("Nice.")
        print("\n")
        type.type("A nearby stranger looks at your money, then at you, and nods approvingly.")
        print("\n")
        type.type(quote("Nice."))
        print("\n")
        type.type("A bird flies overhead and tweets something that sounds like 'nice.'")
        print("\n")
        type.type("You feel at peace with the universe.")
        self.restore_sanity(4)
        self.heal(20)
        print("\n")

    def exactly_1234(self):
        # SECRET: Have exactly $1,234 - sequential numbers
        if self.get_balance() != 1234:
            self.day_event()
            return
        type.type("You count your money. " + green(bright("$1,234")) + ". One, two, three, four.")
        print("\n")
        type.type("The numbers are in perfect sequence. This feels significant somehow.")
        print("\n")
        type.type("A child walks by counting: " + quote("One, two, three, four, five..."))
        print("\n")
        type.type("Everything feels orderly. Like the universe is counting with you.")
        self.restore_sanity(5)
        self.add_status("Sequential Luck")
        print("\n")

    def exactly_7777(self):
        # SECRET: Have exactly $7,777 - lucky 7s
        if self.get_balance() != 7777:
            self.day_event()
            return
        type.type("You count your money. " + green(bright("$7,777")) + ". Four sevens.")
        print("\n")
        type.type("In the distance, a slot machine hits jackpot. You hear the bells.")
        print("\n")
        type.type("A four-leaf clover blows against your window and sticks there.")
        print("\n")
        type.type("A black cat crosses your path... then turns around and walks WITH you instead.")
        print("\n")
        type.type("Today is your day.")
        self.add_status("Lucky")
        self.heal(20)
        self.restore_sanity(7)
        print("\n")

    def exactly_13(self):
        # SECRET: Have exactly $13 - unlucky number
        if self.get_balance() != 13:
            self.day_event()
            return
        type.type("You count your money. " + red(bright("$13")) + ". The unlucky number.")
        print("\n")
        type.type("A black cat hisses at you. You walk under a ladder without noticing.")
        print("\n")
        type.type("A mirror cracks as you walk past it.")
        print("\n")
        type.type("You should probably be careful today.")
        self.lose_sanity(5)
        self.add_status("Cursed")
        print("\n")

    def exactly_69420(self):
        # SECRET: Have exactly $69,420 - the ultimate meme number
        if self.get_balance() != 69420:
            self.day_event()
            return
        type.type("You count your money. " + green(bright("$69,420")) + ".")
        print("\n")
        type.type("...")
        print("\n")
        type.type("Nice.")
        print("\n")
        type.type("NICE.")
        print("\n")
        type.type(yellow(bright("N I C E.")))
        print("\n")
        type.type("The universe itself seems to vibrate with approval.")
        print("\n")
        type.type("Somewhere, a choir of angels sings 'nice' in perfect harmony.")
        self.heal(69)
        self.restore_sanity(10)
        self.add_status("Maximum Nice")
        print("\n")

    def day_palindrome(self):
        # SECRET: It's a palindrome day (day 11, 22, 33, etc)
        if self._day % 11 != 0 or self._day == 0:
            self.day_event()
            return
        type.type("Sitting in your car, you realize something interesting: it's day " + str(self._day) + ".")
        print("\n")
        type.type("A palindrome. The same forwards and backwards.")
        print("\n")
        type.type("Everything feels balanced today. Symmetrical. Perfect.")
        print("\n")
        type.type("You feel like the universe is in alignment.")
        self.restore_sanity(5)
        self.heal(11)
        print("\n")

    def prime_day(self):
        # SECRET: It's a prime number day
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        if not is_prime(self._day):
            self.day_event()
            return
        type.type("You're sitting in your car. Day " + str(self._day) + ". A prime number.")
        print("\n")
        type.type("Indivisible. Unique. Like you.")
        print("\n")
        type.type("You feel mathematically superior to yesterday.")
        self.restore_sanity(3)
        print("\n")

    def same_as_health(self):
        # SECRET: Balance equals current health
        if self.get_balance() != self.get_health():
            self.day_event()
            return
        type.type("Sitting in your car, you realize something strange: you have exactly " + green(bright("$" + str(self.get_balance()))) + "...")
        print("\n")
        type.type("And your health is at exactly " + red(bright(str(self.get_health()))) + ".")
        print("\n")
        type.type("The same number. That's... oddly specific.")
        print("\n")
        type.type("Are you worth exactly one dollar per hit point? Probably not. But it's a weird coincidence.")
        self.restore_sanity(5)
        print("\n")

    def full_moon_madness(self):
        # SECRET: Every 28th day (lunar cycle)
        if self._day % 28 != 0 or self._day == 0:
            self.night_event()
            return
        type.type("The morning light hits different today. Something in the air. You feel... different.")
        print("\n")
        type.type("More alive. More reckless. More HUNGRY.")
        print("\n")
        type.type("Not for food. For victory. For money. For the thrill of the game.")
        print("\n")
        type.type("Something inside you howls for action.")
        self.add_status("Lunar Frenzy")
        self.restore_sanity(10)
        print("\n")

    # ==========================================
    # NON-NUMBER SECRET EVENTS - CONDITION-BASED
    # ==========================================

    def the_veteran_gambler(self):
        # SECRET: Played for 100+ days - an old timer recognizes a kindred spirit
        if self._day < 100:
            self.day_event()
            return
        type.type("An old man approaches you in the parking lot. His eyes are knowing. Tired.")
        print("\n")
        type.type(quote("I can tell. You've been at this a while, haven't you?"))
        print("\n")
        type.type("He sits down next to you uninvited. You don't mind.")
        print("\n")
        type.type(quote("Fifty years. That's how long I played. Won big. Lost bigger. Won again."))
        print("\n")
        type.type(quote("You want to know the secret? There isn't one. It's all just... time. Patience. Survival."))
        print("\n")
        type.type("He presses something into your hand. A worn poker chip.")
        print("\n")
        type.type(quote("My lucky chip. Hasn't been lucky in decades. But maybe for you..."))
        print("\n")
        type.type("He walks away. You never see him again.")
        self.add_item("Veteran's Lucky Chip")
        self.restore_sanity(15)
        self.meet("The Old Timer")
        print("\n")

    def perfect_health_moment(self):
        # SECRET: At exactly 100 health - a moment of perfect physical being
        if self.get_health() != 100:
            self.day_event()
            return
        type.type("You stretch in your car seat. Something feels... different.")
        print("\n")
        type.type("No aches. No pains. No stiffness. Nothing hurts.")
        print("\n")
        type.type("You feel PERFECT. Truly, genuinely perfect.")
        print("\n")
        type.type("When was the last time you felt this good? Years ago? Ever?")
        print("\n")
        type.type("You take a deep breath. The air tastes sweet. The sun is warm but not hot.")
        print("\n")
        type.type("Today is going to be a good day. You can feel it in your bones.")
        self.restore_sanity(10)
        self.add_status("Perfect Condition")
        print("\n")

    def rock_bottom(self):
        # SECRET: Health AND sanity both below 20 - hitting absolute rock bottom
        if self.get_health() >= 20 or self.get_sanity() >= 20:
            self.day_event()
            return
        type.type("You sit in your car, staring at nothing. Everything hurts. Inside and out.")
        print("\n")
        type.type("This is rock bottom. You're sure of it. It can't get worse than this.")
        print("\n")
        type.type("...")
        print("\n")
        type.type("And then, strangely, you laugh. A small, broken laugh.")
        print("\n")
        type.type("If this is the bottom, then there's only one way to go: up.")
        print("\n")
        type.type("Something shifts inside you. Not hope, exactly. But... determination.")
        print("\n")
        type.type("You've survived this far. You'll survive further.")
        self.restore_sanity(5)
        self.heal(5)
        self.add_status("Survivor's Resolve")
        print("\n")

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

    def haunted_by_losses(self):
        # SECRET: Lost 10+ times in a row at blackjack - the ghosts of bad hands
        if not hasattr(self, '_Player__loss_streak') or self._loss_streak < 10:
            self.day_event()
            return
        type.type("You sit in your car, staring at the dashboard. The cards won't leave you alone.")
        print("\n")
        type.type("16 against a dealer 10. Hit. Bust.")
        type.type(" 15 against a 7. Stand. Dealer hits 21.")
        type.type(" 20. Dealer blackjack.")
        print("\n")
        type.type("The losses replay in your mind. Over and over. A casino of nightmares.")
        print("\n")
        type.type("You see the dealer's smirk. The cards mocking you. The chips sliding away.")
        print("\n")
        type.type("When you finally open your eyes, you're covered in cold sweat.")
        print("\n")
        type.type("But there's something else. A cold fury. A NEED to win.")
        self.lose_sanity(10)
        self.add_status("Vengeance Mode")
        print("\n")

    def first_sunrise(self):
        # SECRET: Day 1 only - watching your first sunrise as a gambler
        if self._day != 1:
            self.day_event()
            return
        type.type("You watch the sun rise over the casino parking lot.")
        print("\n")
        type.type("This is it. Day one. The beginning of everything.")
        print("\n")
        type.type("You have nothing but a dream and whatever's in your pocket.")
        print("\n")
        type.type("A million dollars. That's the goal. It sounds impossible.")
        print("\n")
        type.type("But as the golden light washes over your car, you feel something.")
        print("\n")
        type.type("Hope. Pure, stupid, wonderful hope.")
        print("\n")
        type.type("Let's do this.")
        self.restore_sanity(10)
        self.add_status("Fresh Start")
        print("\n")

    def insomniac_revelation(self):
        # SECRET: Have the "Insomnia" status - a 3 AM epiphany
        if not self.has_status("Insomnia"):
            self.night_event()
            return
        type.type("You're sitting in your car, wide awake. You haven't slept in... how long? You've lost count.")
        print("\n")
        type.type("Your thoughts are racing. Random. Disconnected. And then—")
        print("\n")
        type.type("Clarity. Perfect, crystalline clarity.")
        print("\n")
        type.type("You suddenly understand something. About the game. About yourself. About everything.")
        print("\n")
        type.type("...")
        print("\n")
        type.type("And then it's gone. You can't remember what you understood.")
        print("\n")
        type.type("But you feel different. Changed somehow.")
        if random.random() < 0.5:
            self.restore_sanity(15)
            type.type(" The revelation brought peace.")
        else:
            self.lose_sanity(10)
            type.type(" The revelation terrified you.")
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

    def completely_broke_wisdom(self):
        # SECRET: Have exactly $0 - a moment of zen poverty
        if self.get_balance() != 0:
            self.day_event()
            return
        type.type("You sit in your car and check your wallet. Empty. Your pockets. Empty. Your car. Nothing.")
        print("\n")
        type.type("You have exactly " + red(bright("$0")) + ". Not even a penny.")
        print("\n")
        type.type("...")
        print("\n")
        type.type("And somehow, it's freeing.")
        print("\n")
        type.type("You have nothing to lose. Literally nothing. You are at absolute zero.")
        print("\n")
        type.type("The only direction from here is up. The only option is forward.")
        print("\n")
        type.type("A strange calm washes over you. This is the beginning. Again.")
        self.restore_sanity(10)
        self.add_status("Nothing Left to Lose")
        print("\n")

    def the_crow_council(self):
        # SECRET: Have the crow companion - crows gather for a meeting
        if not self.has_companion("The Crow"):
            self.day_event()
            return
        type.type("Your crow friend lands on your car and caws loudly. Then again. And again.")
        print("\n")
        type.type("From the trees, from the rooftops, from everywhere—crows appear.")
        print("\n")
        type.type("Dozens of them. Maybe a hundred. They perch in a circle around your car.")
        print("\n")
        type.type("They're... having a meeting? About YOU?")
        print("\n")
        type.type("The cawing intensifies. Debates? Arguments? You can't tell.")
        print("\n")
        type.type("Finally, your crow hops forward and drops something at your feet.")
        print("\n")
        if random.random() < 0.5:
            type.type("A shiny button. Then another crow drops a coin. Then another. " + green(bright("+$23")) + " in random shinies.")
            self.change_balance(23)
        else:
            type.type("A small, jet-black feather. It shimmers with an oily iridescence. It feels important.")
            self.add_item("Council Feather")
        print("\n")
        type.type("The crows disperse as suddenly as they gathered. Your crow stays, looking smug.")
        print("\n")

    def the_sleeping_stranger(self):
        # SECRET: Sanity between 40-50 - a stranger sleeps in the same lot
        if self.get_sanity() < 40 or self.get_sanity() > 50:
            self.night_event()
            return
        type.type("You notice another car in the lot this morning. Someone sleeping inside, just like you.")
        print("\n")
        type.type("For a moment, you watch them. They're restless. Bad dreams, maybe.")
        print("\n")
        type.type("You realize: you're not the only one. There are others like you.")
        print("\n")
        type.type("Living in cars. Chasing something. Running from something else.")
        print("\n")
        type.type("You feel less alone. And also more alone. It's complicated.")
        print("\n")
        type.type("In the morning, the car is gone. You never saw their face.")
        self.restore_sanity(3)
        print("\n")

    def birthday_forgotten(self):
        # SECRET: Day 365 - it's been exactly one year
        if self._day != 365:
            self.day_event()
            return
        type.type("You're sitting in your car when you check your phone. The date hits you like a truck.")
        print("\n")
        type.type("It's been exactly ONE YEAR since you started this journey.")
        print("\n")
        type.type("365 days of gambling. Of winning and losing. Of living in your car.")
        print("\n")
        type.type("A whole year of your life, spent chasing a million dollars.")
        print("\n")
        type.type("Was it worth it? You don't know. You're still here. That's something.")
        print("\n")
        type.type("Happy anniversary to... whatever this is.")
        print("\n")
        if self.get_balance() > 500000:
            type.type("You're more than halfway there. The finish line is in sight.")
            self.restore_sanity(20)
        elif self.get_balance() > 100000:
            type.type("You've made progress. Real progress. Keep going.")
            self.restore_sanity(10)
        else:
            type.type("It's been a hard year. But you're still fighting. That counts for something.")
            self.lose_sanity(5)
        print("\n")

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

    def rain_on_the_roof(self):
        # SECRET: Random 5% chance during any night - just rain, and peace
        if random.random() > 0.05:
            self.night_event()
            return
        type.type("It starts raining. Softly at first, then harder.")
        print("\n")
        type.type("You lie back in your car and listen to the droplets on the roof.")
        print("\n")
        type.type("Tap. Tap-tap. Tap. Tap-tap-tap-tap.")
        print("\n")
        type.type("The rhythm is hypnotic. Peaceful. The world outside blurs into water and light.")
        print("\n")
        type.type("For once, you're not thinking about money. Or cards. Or tomorrow.")
        print("\n")
        type.type("You're just... here. Present. Listening to the rain.")
        print("\n")
        type.type("It's the most peaceful you've felt in a long time.")
        self.restore_sanity(15)
        self.heal(5)
        print("\n")

    # ==========================================
    # DRASTIC DOUGHMAN/NEARLY THERE EVENTS
    # Violence, Medical, Mental Health, Addiction, Death themes
    # ==========================================

    def loan_shark_visit(self):
        # EVENT: A loan shark you borrowed from finds you - demands payment with interest
        # CONDITION: Balance >= $100,000 (you look like you have money now)
        # EFFECTS: Pay = lose large sum; Refuse = brutal beating, possible death
        # BRUTAL: Can result in missing finger or death
        if self.get_balance() < 100000:
            self.day_event()
            return
        type.type("A black SUV pulls up next to your car. Two men get out. You recognize the tattoos.")
        print("\n")
        type.type("Before you can react, they're dragging you out of your car.")
        print("\n")
        type.type(quote("Remember us? Remember the money you borrowed to start this little gambling hobby of yours?"))
        print("\n")
        type.type("You don't remember. But looking at their faces, you're starting to.")
        print("\n")
        type.type(quote("$50,000. Plus interest. That's $75,000 now. You got two days."))
        print("\n")
        type.type("One of them pulls out a pair of bolt cutters. " + quote("Or we start taking fingers."))
        print("\n")
        answer = ask.option("What do you do? ", ["pay now", "beg for time", "refuse"])
        if answer == "pay now":
            if self.get_balance() >= 75000:
                type.type("You hand over " + red(bright("$75,000")) + ". Every dollar feels like a piece of your soul.")
                self.change_balance(-75000)
                print("\n")
                type.type(quote("Pleasure doing business. Don't borrow again unless you can pay."))
                print("\n")
                type.type("They leave. You're poorer, but you have all your fingers.")
                self.lose_sanity(15)
            else:
                type.type(quote("That's not enough. You're short."))
                print("\n")
                type.type("Before you can explain, one of them grabs your hand and spreads your fingers on the hood of your car.")
                print("\n")
                type.type(red(bright("CRUNCH.")))
                print("\n")
                type.type("You scream. Your pinky finger is gone. Blood pools on the hood.")
                print("\n")
                type.type(quote("That's the interest. Now pay the rest, or lose more."))
                taken = self.get_balance()
                self.change_balance(-taken)
                self.hurt(40)
                self.lose_sanity(30)
                self.add_status("Missing Finger")
                self.add_danger("Severed Finger")
        elif answer == "beg for time":
            type.type(quote("Please, I just need a few more days. I'm so close to a big win-"))
            print("\n")
            type.type("The bigger one punches you in the stomach. You double over, gasping.")
            print("\n")
            type.type(quote("Two days. Not three. Two. And we're adding another 10K for wasting our time."))
            print("\n")
            type.type("They get back in the SUV and drive away. You have 48 hours.")
            self.hurt(20)
            self.lose_sanity(20)
            self.add_danger("Loan Shark Deadline")
        else:
            type.type(quote("I'm not paying you anything. I don't even remember borrowing-"))
            print("\n")
            type.type("The bolt cutters flash. Pain explodes in your hand.")
            print("\n")
            type.type(red(bright("Your ring finger hits the pavement with a wet sound.")))
            print("\n")
            type.type("You scream. They keep hitting you. Ribs crack. Teeth loosen.")
            print("\n")
            if random.random() < 0.3:
                type.type("One of them stomps on your head. Everything goes dark.")
                print("\n")
                type.type("You don't wake up.")
                self.die("Beat to death by loan sharks. They took your fingers as souvenirs.")
                return
            else:
                type.type("Eventually, they stop. You're lying in a pool of your own blood.")
                print("\n")
                type.type(quote("We'll be back. And next time, we take the whole hand."))
                self.hurt(70)
                self.lose_sanity(40)
                self.add_status("Missing Finger")
                self.add_danger("Loan Shark Revenge")
        print("\n")

    def the_desperate_gambler(self):
        # EVENT: A man begs you for money - he's in deep to the wrong people
        # EFFECTS: Help = lose money but save a life (or be scammed); Refuse = witness his fate
        # DARK: Witness suicide if you refuse
        type.type("A man approaches your car. He's shaking. Crying. Desperate.")
        print("\n")
        type.type(quote("Please. Please, you have to help me. I owe them money. So much money."))
        print("\n")
        type.type(quote("If I don't pay by midnight, they're going to kill me. Please. I have a daughter."))
        print("\n")
        type.type("He shows you a photo. A little girl with pigtails and a gap-toothed smile.")
        print("\n")
        answer = ask.yes_or_no("Give him money? ")
        if answer == "yes":
            amount = min(self.get_balance(), random.randint(500, 2000))
            type.type("You hand over " + red(bright("$" + str(amount))) + ". It's a lot. But his eyes...")
            self.change_balance(-amount)
            print("\n")
            if random.random() < 0.7:
                type.type(quote("Thank you. Thank you so much. You saved my life. I'll pay you back someday."))
                print("\n")
                type.type("He runs off. You never see him again. But you hope he made it.")
                self.restore_sanity(10)
                self.meet("The Desperate Man")
            else:
                type.type("He takes the money... and laughs.")
                print("\n")
                type.type(quote("Sucker. There's one born every minute."))
                print("\n")
                type.type("He walks away, counting the bills. The photo was probably fake too.")
                self.lose_sanity(15)
        else:
            type.type(quote("I'm sorry. I can't. I need every dollar I have."))
            print("\n")
            type.type("The man's face crumbles. " + quote("Then I'm already dead."))
            print("\n")
            type.type("He walks away. Toward the bridge.")
            print("\n")
            type.type("...")
            print("\n")
            type.type("An hour later, you hear sirens. You don't look. You can't look.")
            print("\n")
            type.type("But you know.")
            self.lose_sanity(25)
            self.add_status("Witnessed Death")
        print("\n")

    def withdrawal_nightmare(self):
        # EVENT: Severe gambling withdrawal - your body and mind rebel
        # CONDITION: Sanity below 30
        # EFFECTS: Physical and mental symptoms, risk of self-harm
        if self.get_sanity() >= 30:
            self.night_event()
            return
        type.type("You're drenched in sweat in your car seat. Your hands are shaking. Your heart is racing.")
        print("\n")
        type.type("You NEED to gamble. The urge is overwhelming. It's not a want. It's a NEED.")
        print("\n")
        type.type("But the casino is closed. It's 3 AM. You can't. You CAN'T.")
        print("\n")
        type.type("Your skin crawls. You scratch your arms until they bleed. It doesn't help.")
        print("\n")
        type.type("You punch the steering wheel. Again. Again. Your knuckles split open.")
        print("\n")
        answer = ask.option("What do you do? ", ["ride it out", "drive to casino anyway", "hurt yourself more"])
        if answer == "ride it out":
            type.type("You grip the steering wheel until your fingers go white. You breathe. In. Out. In. Out.")
            print("\n")
            type.type("Hours pass. The sun rises. The shaking stops, eventually.")
            print("\n")
            type.type("You survived. But you know it'll happen again.")
            self.hurt(10)
            self.lose_sanity(10)
        elif answer == "drive to casino anyway":
            type.type("You drive. 90 miles an hour. Running red lights. You don't care.")
            print("\n")
            type.type("The casino is dark. Closed. You pound on the doors until security comes.")
            print("\n")
            type.type(quote("Sir, we're closed. You need to leave or we'll call the police."))
            print("\n")
            type.type("You sit in the parking lot until they open. Four hours. Just waiting.")
            self.lose_sanity(20)
        else:
            type.type("You need to feel something else. Anything else.")
            print("\n")
            type.type("The pain helps, for a moment. Then it doesn't.")
            print("\n")
            type.type("You look at your arms. At the blood. At what you've become.")
            self.hurt(25)
            self.lose_sanity(15)
            self.add_danger("Self-Harm Wounds")
        print("\n")

    def organ_harvester(self):
        # EVENT: Someone offers to buy your kidney - you're worth more in parts
        # CONDITION: Balance below $1,000 (desperate) OR health below 30
        # EFFECTS: Accept = money but permanent health loss; Refuse = nothing
        # DARK: Selling body parts for gambling money
        if self.get_balance() >= 1000 and self.get_health() >= 30:
            self.day_event()
            return
        type.type("A clean-looking van pulls up. A man in scrubs steps out. He's smiling.")
        print("\n")
        type.type(quote("You look like someone who could use some money. Am I right?"))
        print("\n")
        type.type("He pulls out a business card. 'ORGAN SOLUTIONS - We Pay Top Dollar.'")
        print("\n")
        type.type(quote("One kidney. $40,000. Cash. Tonight. You won't even miss it."))
        print("\n")
        answer = ask.yes_or_no("Sell your kidney? ")
        if answer == "yes":
            type.type("You get in the van. Part of you knows this is insane. The rest of you needs the money.")
            print("\n")
            type.type("...")
            print("\n")
            type.type("You wake up in a motel room. There's a fresh scar on your side. An envelope on the nightstand.")
            print("\n")
            type.type(green(bright("$40,000")) + " in cash. Just like they promised.")
            self.change_balance(40000)
            print("\n")
            type.type("You're lighter now. In more ways than one. Your maximum health is permanently reduced.")
            self.hurt(30)
            self.add_status("One Kidney")
            self.lose_sanity(20)
        else:
            type.type(quote("No thanks. I'm not that desperate yet."))
            print("\n")
            type.type("The man shrugs. " + quote("Yet. I like that word. Here's my card if you change your mind."))
            print("\n")
            type.type("He drives away. You throw the card in the trash. Then you fish it back out.")
            print("\n")
            type.type("Just in case.")
        print("\n")

    def casino_overdose(self):
        # EVENT: Find someone ODing in the casino bathroom
        # EFFECTS: Help = risk getting blamed, possibly save a life; Ignore = they die, lose sanity
        # DARK: Drug use and death in casinos
        type.type("You head into the casino and walk into the bathroom. You freeze.")
        print("\n")
        type.type("Someone's on the floor. Blue lips. Needle still in their arm. Foam at the mouth.")
        print("\n")
        type.type("They're not breathing. Or barely breathing. You can't tell.")
        print("\n")
        answer = ask.option("What do you do? ", ["call for help", "try to help yourself", "walk away"])
        if answer == "call for help":
            type.type("You run out screaming for help. Security comes. Paramedics arrive.")
            print("\n")
            if random.random() < 0.6:
                type.type("They stabilize her. She's going to make it. Barely.")
                print("\n")
                type.type("A security guard pats you on the shoulder. " + quote("You saved her life."))
                self.restore_sanity(5)
            else:
                type.type("It's too late. She's gone before the paramedics even arrive.")
                print("\n")
                type.type("You watch them cover her body with a sheet. She was young. Maybe 25.")
                self.lose_sanity(20)
                self.add_status("Witnessed Death")
        elif answer == "try to help yourself":
            type.type("You check for a pulse. Faint. You start CPR, trying to remember how it works.")
            print("\n")
            type.type("Chest compressions. Mouth to mouth. Chest compressions. Her lips are cold.")
            print("\n")
            if random.random() < 0.4:
                type.type("She gasps. Coughs. Vomits. But she's BREATHING.")
                print("\n")
                type.type("Someone finally notices and calls 911. By the time they arrive, she's conscious.")
                print("\n")
                type.type(quote("You... saved me...") + " she whispers. Her eyes are hollow. But alive.")
                self.restore_sanity(15)
                self.meet("Casino Survivor")
            else:
                type.type("She doesn't respond. You keep trying. Keep pushing. Keep breathing.")
                print("\n")
                type.type("But she's gone. You feel the moment she leaves.")
                print("\n")
                type.type("Her eyes are still open. Staring at nothing.")
                self.lose_sanity(30)
                self.add_status("CPR Failure")
        else:
            type.type("You back out slowly. Pretend you didn't see anything. It's not your problem.")
            print("\n")
            type.type("You go back to the tables. Try to focus on the cards. Try not to think about it.")
            print("\n")
            type.type("An hour later, you hear the sirens. Too late. You know it's too late.")
            print("\n")
            type.type("You keep playing. What else can you do?")
            self.lose_sanity(25)
            self.add_status("Ignored Death")
        print("\n")

    def cancer_diagnosis(self):
        # EVENT: A cough that won't go away leads to a devastating diagnosis
        # CONDITION: Health below 50 OR has "Chronic Cough" status
        # EFFECTS: Major health reduction, sanity loss, expensive treatment choice
        # MEDICAL: Terminal illness
        if self.get_health() >= 50 and not self.has_status("Chronic Cough"):
            self.day_event()
            return
        type.type("Sitting in your car, the cough has been getting worse. You finally drive to a clinic.")
        print("\n")
        type.type("X-rays. Blood tests. Waiting. So much waiting.")
        print("\n")
        type.type("The doctor sits down. She doesn't meet your eyes.")
        print("\n")
        type.type(quote("I'm sorry. It's cancer. Stage 3 lung cancer."))
        print("\n")
        type.type("The world goes silent. Your ears ring. This isn't real.")
        print("\n")
        type.type(quote("Without treatment, you have maybe six months. With treatment... maybe two years."))
        print("\n")
        type.type(quote("Treatment will cost around $50,000. We can discuss payment plans..."))
        print("\n")
        answer = ask.option("What do you do? ", ["pay for treatment", "refuse treatment", "break down"])
        if answer == "pay for treatment":
            if self.get_balance() >= 50000:
                type.type("You hand over " + red(bright("$50,000")) + ". Your life savings. For a chance at life.")
                self.change_balance(-50000)
                self.add_status("Chemotherapy")
                type.type(" The chemotherapy starts next week.")
            else:
                type.type(quote("I... I don't have enough."))
                print("\n")
                type.type("The doctor sighs. " + quote("There are... other options. Experimental treatments. Clinical trials."))
                print("\n")
                type.type("You sign up for everything. Anything.")
                self.add_status("Experimental Treatment")
            self.lose_sanity(30)
        elif answer == "refuse treatment":
            type.type(quote("No. No treatment. If I'm going to die, I'm going to die on my terms."))
            print("\n")
            type.type("The doctor nods. She's seen this before. " + quote("It's your choice. I'm sorry."))
            print("\n")
            type.type("You walk out. Six months. Maybe less. Better make it count.")
            self.lose_sanity(25)
            self.add_status("Terminal")
            self.add_danger("Cancer Untreated")
        else:
            type.type("You break down. Right there in the office. Sobbing. Screaming.")
            print("\n")
            type.type("The doctor holds your hand. Lets you cry. She's seen this before too.")
            print("\n")
            type.type("Eventually, the tears stop. You're empty. Hollow.")
            print("\n")
            type.type(quote("Take some time. Think about it. Come back when you're ready."))
            self.lose_sanity(40)
        print("\n")

    def the_bridge_call(self):
        # EVENT: At your lowest point, the bridge calls to you
        # CONDITION: Sanity below 15
        # EFFECTS: Player must make a choice - potentially fatal
        # MENTAL HEALTH: Suicidal ideation - explicit content warning
        if self.get_sanity() >= 15:
            self.night_event()
            return
        type.type("You start your car and drive. You don't know where. Just... driving.")
        print("\n")
        type.type("The bridge appears ahead. The big one. The one over the gorge.")
        print("\n")
        type.type("Your car slows. Stops in the middle. You get out.")
        print("\n")
        type.type("The wind is cold. The water is far below. Black and quiet.")
        print("\n")
        type.type("It would be so easy. Just climb over the railing. One step.")
        print("\n")
        type.type("No more gambling. No more losing. No more living in a car like an animal.")
        print("\n")
        type.type("No more...")
        print("\n")
        answer = ask.option("", ["climb the railing", "call someone", "walk away"])
        if answer == "climb the railing":
            type.type("You climb over the railing. The metal is cold. The wind pushes at you.")
            print("\n")
            type.type("You look down. It's so far. So final.")
            print("\n")
            if random.random() < 0.6:
                type.type("A car stops. A woman runs toward you.")
                print("\n")
                type.type(quote("DON'T! Please! Please don't!"))
                print("\n")
                type.type("She's crying. A stranger, crying for you. When did you last have someone cry for you?")
                print("\n")
                type.type("She talks you down. Holds your hand. Calls for help.")
                print("\n")
                type.type("Hours later, you're in a hospital bed. Alive. You're not sure how you feel about that.")
                self.add_status("Survived Attempt")
                self.lose_sanity(10)
                self.meet("Bridge Angel")
            else:
                type.type("You lean forward. Let go.")
                print("\n")
                type.type("The fall is longer than you expected. Almost peaceful.")
                print("\n")
                type.type("The last thing you see is the stars above, spinning.")
                self.die("Jumped from the bridge. The chase for a million ended here.")
                return
        elif answer == "call someone":
            type.type("You pull out your phone. Who do you even call?")
            print("\n")
            type.type("You dial the suicide hotline. Your hands are shaking so bad you can barely hit the numbers.")
            print("\n")
            type.type("Someone answers. A voice. Calm. Kind.")
            print("\n")
            type.type(quote("Hello. You've reached the crisis line. You're not alone. Can you tell me your name?"))
            print("\n")
            type.type("You talk. For hours. Until the sun comes up.")
            print("\n")
            type.type("You're still here. Still breathing. That's something.")
            self.restore_sanity(10)
            self.add_status("Called for Help")
        else:
            type.type("You step back. Get in your car. Drive away.")
            print("\n")
            type.type("Not tonight. Not like this.")
            print("\n")
            type.type("You don't know why. You don't feel better. You don't feel anything.")
            print("\n")
            type.type("But you're still here. And tomorrow is another day.")
            self.restore_sanity(5)
        print("\n")

    def the_relapse(self):
        # EVENT: After a big win, the addiction demands MORE
        # CONDITION: Won big recently (balance increased by 50K+ today)
        # EFFECTS: Risk losing everything chasing the high
        # ADDICTION: The insatiable need for more
        if not hasattr(self, '_Player__today_winnings') or self._today_winnings < 50000:
            self.day_event()
            return
        type.type("You're sitting in your car outside the casino. You won big today. Really big. You should walk away.")
        print("\n")
        type.type("But the cards are still there. The dealer is waiting. The chips are calling.")
        print("\n")
        type.type("Just one more hand. One more. You're HOT right now.")
        print("\n")
        type.type("Your hands are shaking. Not from fear. From NEED.")
        print("\n")
        answer = ask.yes_or_no("Go back to the tables? ")
        if answer == "yes":
            type.type("You sit back down. The dealer smiles. " + quote("Back for more?"))
            print("\n")
            type.type("Hours pass. You don't notice. The world shrinks to just you and the cards.")
            print("\n")
            outcome = random.randint(1, 10)
            if outcome <= 3:
                winnings = random.randint(10000, 50000)
                type.type("Lady luck is still with you. You walk out with another " + green(bright("$" + str(winnings))) + "!")
                self.change_balance(winnings)
                type.type(" The high is incredible. Nothing else matters.")
                self.lose_sanity(10)
            elif outcome <= 7:
                losses = random.randint(20000, 60000)
                actual_loss = min(self.get_balance(), losses)
                type.type("It all goes wrong. Every hand. Every bet. You can't stop.")
                print("\n")
                type.type("When you finally stand up, you've lost " + red(bright("$" + str(int(actual_loss)))) + ".")
                self.change_balance(-actual_loss)
                self.lose_sanity(20)
            else:
                type.type("You don't stop. You CAN'T stop. Hand after hand. Bet after bet.")
                print("\n")
                type.type("When security finally kicks you out, you're broke. Everything. Gone.")
                print("\n")
                type.type(quote("I'll win it back. I'll win it all back tomorrow."))
                self.change_balance(-self.get_balance())
                self.lose_sanity(35)
        else:
            type.type("You force yourself to walk away. Every step is agony.")
            print("\n")
            type.type("The cards call to you. The chips whisper your name.")
            print("\n")
            type.type("But you keep walking. Tonight, you won.")
            print("\n")
            type.type("The battle, at least. The war continues.")
            self.restore_sanity(15)
        print("\n")

    def casino_hitman(self):
        # EVENT: You've won too much - the casino sends someone to "talk" to you
        # CONDITION: Balance >= $800,000
        # EFFECTS: Various outcomes including death, injury, or escape
        # VIOLENCE: Professional intimidation/assassination
        if self.get_balance() < 800000:
            self.day_event()
            return
        type.type("You're at the casino bar when a man sits down next to you. You didn't hear him approach.")
        print("\n")
        type.type(quote("That's a lot of money you've won. Almost a million. Impressive."))
        print("\n")
        type.type("He's not smiling. His eyes are dead. Professional.")
        print("\n")
        type.type(quote("The house doesn't like to lose. You understand that, right?"))
        print("\n")
        type.type("Under the bar, you feel something cold press against your ribs. A gun.")
        print("\n")
        type.type(quote("You have two choices. Walk away now. Leave the state. Never come back."))
        type.type(quote(" Or..."))
        print("\n")
        type.type("He doesn't finish the sentence. He doesn't have to.")
        print("\n")
        answer = ask.option("What do you do? ", ["agree to leave", "offer money", "fight back"])
        if answer == "agree to leave":
            type.type(quote("Smart. I like smart people. They live longer."))
            print("\n")
            type.type("He stands up. The gun disappears.")
            print("\n")
            type.type(quote("You have 24 hours to leave. Take your money. Don't come back."))
            print("\n")
            type.type("You watch him walk away. Your hands won't stop shaking.")
            self.lose_sanity(25)
            self.add_danger("Casino Exile")
        elif answer == "offer money":
            type.type(quote("How much to make this go away?"))
            print("\n")
            type.type("He considers. " + quote("$200,000. Now. And you don't come back for a year."))
            print("\n")
            if self.get_balance() >= 200000:
                answer2 = ask.yes_or_no("Pay $200,000? ")
                if answer2 == "yes":
                    type.type("You transfer the money. He checks his phone. Nods.")
                    self.change_balance(-200000)
                    print("\n")
                    type.type(quote("Pleasure doing business. See you in a year."))
                    self.lose_sanity(15)
                else:
                    type.type("His expression doesn't change. The gun presses harder.")
                    print("\n")
                    type.type(quote("Wrong answer."))
                    print("\n")
                    type.type(red(bright("BANG.")))
                    print("\n")
                    type.type("The bar goes silent. You're on the floor. Blood pooling beneath you.")
                    print("\n")
                    if random.random() < 0.4:
                        type.type("The last thing you hear is screaming. It might be yours.")
                        self.die("Shot by casino enforcement. The house always wins.")
                        return
                    else:
                        type.type("You survive. Barely. The bullet missed anything vital.")
                        print("\n")
                        type.type("Weeks later, you wake up in a hospital. Your money is gone. All of it.")
                        self.change_balance(-self.get_balance())
                        self.hurt(80)
                        self.lose_sanity(40)
            else:
                type.type(quote("I don't have that much."))
                print("\n")
                type.type(quote("Then I guess we go with option two."))
                print("\n")
                if random.random() < 0.5:
                    type.type("The gun fires. You don't even feel it.")
                    self.die("Executed by the casino. Too successful for your own good.")
                    return
                else:
                    type.type("But he pauses. Sighs. " + quote("Get out. Now. Before I change my mind."))
                    print("\n")
                    type.type("You run. You've never run so fast in your life.")
                    self.lose_sanity(30)
        else:
            type.type("You knock the gun away and throw a punch.")
            print("\n")
            chance = random.randint(1, 10)
            if chance <= 2:
                type.type("The hit connects. He staggers. You grab a bottle and swing.")
                print("\n")
                type.type("He goes down. People are screaming. You run.")
                print("\n")
                type.type("You don't know if he's dead. You don't want to know.")
                self.hurt(15)
                self.lose_sanity(20)
                self.add_danger("Casino Enemy")
            elif chance <= 6:
                type.type("He's faster. The gun comes up and fires.")
                print("\n")
                type.type("Your shoulder explodes in pain. You hit the floor.")
                print("\n")
                type.type("He stands over you, gun aimed at your head.")
                print("\n")
                type.type(quote("Stupid."))
                print("\n")
                type.type("But he doesn't fire again. Just walks away. A warning.")
                self.hurt(50)
                self.lose_sanity(30)
                self.add_danger("Gunshot Wound")
            else:
                type.type("He's faster. Much faster.")
                print("\n")
                type.type("Three shots. Chest. Chest. Head.")
                print("\n")
                type.type("You're dead before you hit the floor.")
                self.die("Killed by a professional. The casino doesn't forgive.")
                return
        print("\n")

    def the_confession(self):
        # EVENT: A dying man confesses his sins to you - you're the only one who will listen
        # EFFECTS: Hear terrible things, gain money, lose sanity
        # DARK: Hearing about horrible deeds
        type.type("An old man grabs your sleeve in the casino parking lot. He's pale. Sweating.")
        print("\n")
        type.type(quote("Please. I need to tell someone. Before I die. I need to confess."))
        print("\n")
        type.type("He looks like death. His grip is surprisingly strong.")
        print("\n")
        answer = ask.yes_or_no("Listen to him? ")
        if answer == "yes":
            type.type("He talks. For an hour. Two. You wish you hadn't listened.")
            print("\n")
            type.type("Murder. Fraud. Things you can't unhear. Victims you can't forget.")
            print("\n")
            type.type("When he's done, he presses a key into your hand.")
            print("\n")
            type.type(quote("Storage unit. 47B. Take it all. I don't need it anymore."))
            print("\n")
            type.type("He walks away. You find the storage unit. Inside: " + green(bright("$150,000")) + " in cash.")
            self.change_balance(150000)
            print("\n")
            type.type("Blood money. Does it matter? Money is money.")
            print("\n")
            type.type("But you can't forget what he told you. You never will.")
            self.lose_sanity(25)
            self.add_status("Confessor's Burden")
        else:
            type.type(quote("I'm sorry. I can't."))
            print("\n")
            type.type("His face falls. " + quote("Then it dies with me. All of it."))
            print("\n")
            type.type("He walks away. You never see him again.")
            print("\n")
            type.type("Part of you wonders what he would have said.")
            print("\n")
            type.type("Most of you is glad you don't know.")
            self.restore_sanity(5)
        print("\n")

    def the_high_roller_suicide(self):
        # EVENT: Witness a high roller's complete breakdown and suicide
        # CONDITION: Balance >= $500,000 (you're in the high roller areas)
        # EFFECTS: Witness death, major sanity loss
        # MENTAL HEALTH: Witnessing suicide
        if self.get_balance() < 500000:
            self.day_event()
            return
        type.type("You head to the casino. In the high roller room, a man starts laughing. It's not a happy sound.")
        print("\n")
        type.type("He's lost everything. EVERYTHING. His chips are gone. His marker is maxed.")
        print("\n")
        type.type(quote("Twenty million. I lost TWENTY MILLION DOLLARS."))
        print("\n")
        type.type("He's still laughing. Crying too. Security approaches carefully.")
        print("\n")
        type.type(quote("My wife will leave me. My kids won't... they won't understand."))
        print("\n")
        type.type("He pulls out a gun. Everyone screams. Dives for cover.")
        print("\n")
        type.type("But he doesn't aim at anyone else.")
        print("\n")
        type.type(quote("This is what gambling does. Remember that."))
        print("\n")
        type.type(red(bright("BANG.")))
        print("\n")
        type.type("The room goes silent. He falls. It's over that fast.")
        print("\n")
        type.type("You can't move. Can't look away. His blood spreads across the green felt.")
        print("\n")
        type.type("Security rushes in. Someone throws a jacket over him. The game is over.")
        print("\n")
        type.type("But you can still hear the shot. You'll always hear the shot.")
        self.lose_sanity(40)
        self.add_status("Witnessed Suicide")
        print("\n")

    def the_dying_dealer(self):
        # EVENT: Your favorite dealer is dying - they have one last game to play
        # CONDITION: Met "The Dealer" (someone you've played with many times)
        # EFFECTS: Emotional final game, potential gift or loss
        if not self.has_met("The Dealer"):
            self.day_event()
            return
        type.type("You head to the casino. Your regular dealer isn't at his usual table. You ask around.")
        print("\n")
        type.type("Cancer. Stage 4. He has weeks, maybe days.")
        print("\n")
        type.type("But he asked about you. Left an address. A request.")
        print("\n")
        answer = ask.yes_or_no("Visit him? ")
        if answer == "yes":
            type.type("He's at home. Hospice care. He looks so small in the hospital bed.")
            print("\n")
            type.type(quote("You came. I wasn't sure you would."))
            print("\n")
            type.type("He gestures to a deck of cards on the nightstand.")
            print("\n")
            type.type(quote("One last game? For old times' sake?"))
            print("\n")
            type.type("You play. Slowly. The cards feel heavy. Important.")
            print("\n")
            type.type("He wins, of course. He was always the best.")
            print("\n")
            type.type(quote("Take these.") + " He presses his lucky chips into your hand. " + quote("You'll need them more than I will."))
            print("\n")
            type.type("You stay until he falls asleep. His breathing is shallow.")
            print("\n")
            type.type("A week later, you hear he passed. Peacefully. Cards in his hand.")
            self.add_item("Dealer's Lucky Chips")
            self.restore_sanity(5)
            self.lose_sanity(15)  # Net -10, grief
        else:
            type.type("You can't. It's too hard. You tell yourself you'll go tomorrow.")
            print("\n")
            type.type("Three days later, you hear he passed.")
            print("\n")
            type.type("You never said goodbye.")
            self.lose_sanity(25)
        print("\n")

    # ==========================================
    # MORE SECRET EVENTS - CONDITION BASED
    # ==========================================

    def the_anniversary_loss(self):
        # SECRET: Lost someone close - anniversary of their death
        if not self.has_status("Widowed") and not self.has_status("Lost Child"):
            self.day_event()
            return
        type.type("You sit up in your car. You immediately know what day it is.")
        print("\n")
        type.type("The anniversary. One year since they died.")
        print("\n")
        type.type("You try to distract yourself. Casino. Cards. Anything.")
        print("\n")
        type.type("But you see their face everywhere. In strangers. In reflections.")
        print("\n")
        type.type("By evening, you're crying in the parking lot. Alone. Always alone.")
        self.lose_sanity(20)
        print("\n")

    def survivor_guilt(self):
        # SECRET: Survived something others didn't
        if not self.has_status("Witnessed Death") and not self.has_status("Survivor's Resolve"):
            self.day_event()
            return
        type.type("You sit in your car and the faces come back. The ones who didn't make it.")
        print("\n")
        type.type("Why you? Why did YOU survive when they didn't?")
        print("\n")
        type.type("You don't deserve this. Any of this. The money, the life, any of it.")
        print("\n")
        type.type("...But maybe that's why you keep gambling. Waiting to lose it all.")
        print("\n")
        type.type("Waiting to get what you deserve.")
        self.lose_sanity(15)
        print("\n")

    def the_scar_story(self):
        # SECRET: Have a scar-related status - someone asks about it
        if not self.has_status("Missing Finger") and not self.has_status("Burn Scars") and not self.has_danger("Knife Wound"):
            self.day_event()
            return
        type.type("You step out of your car. A child points at your scars. " + quote("What happened to you?"))
        print("\n")
        type.type("Their mother pulls them away, apologizing. But the damage is done.")
        print("\n")
        type.type("What DID happen to you? How did you end up here? Scarred, gambling, living in a car?")
        print("\n")
        type.type("You remember every wound. Every story. Every mistake.")
        print("\n")
        type.type("The scars are just the ones you can see.")
        self.lose_sanity(8)
        print("\n")

    def the_winning_streak_paranoia(self):
        # SECRET: Won more than $100,000 in a single day
        if not hasattr(self, '_Player__today_winnings') or self._today_winnings < 100000:
            self.night_event()
            return
        type.type("You're wide awake in your car. Too much adrenaline. Too much paranoia.")
        print("\n")
        type.type("That's a lot of money. People kill for less.")
        print("\n")
        type.type("Every noise is a threat. Every shadow is an enemy.")
        print("\n")
        type.type("You clutch your cash like a lifeline. Eyes darting. Heart pounding.")
        print("\n")
        type.type("Is that car following you? Was that footsteps?")
        print("\n")
        type.type("Morning comes. You're exhausted but alive. Was anyone ever really after you?")
        print("\n")
        type.type("Does it matter? The fear was real.")
        self.lose_sanity(10)
        print("\n")

    def old_gambling_buddy(self):
        # SECRET: Day 200+ - run into someone from your past gambling life
        if self._day < 200:
            self.day_event()
            return
        type.type("You step out of your car when a voice calls your name. Your REAL name. One you haven't heard in months.")
        print("\n")
        type.type("You turn and see a face from another life. An old gambling buddy.")
        print("\n")
        type.type(quote("I can't believe it's you! We all thought you were dead! Or in prison!"))
        print("\n")
        type.type("He looks good. Clean. Healthy. Normal.")
        print("\n")
        type.type(quote("I quit, you know. Two years clean. Got a job, a family. Real life stuff."))
        print("\n")
        type.type("He looks at you. At your car. At your clothes. At what you've become.")
        print("\n")
        type.type(quote("Oh. You're still...") + " He trails off. The pity in his eyes is worse than any insult.")
        print("\n")
        type.type(quote("Good luck, man. I hope you find your way out."))
        print("\n")
        type.type("He walks away. Back to his normal life. You stay.")
        self.lose_sanity(15)
        print("\n")

    # ==========================================
    # ==========================================
    # BRUTAL EVENTS - DEATH POSSIBLE
    # These events can result in player death. High risk, high stakes encounters.
    # ==========================================

    def back_alley_shortcut(self):
        # EVENT: Mugged in a dark alley with three armed men
        # EFFECTS: Comply = lose $100-500 + 15 damage + 10 sanity; Run = escape or die; Fight = win or die
        # COMPANION INTEGRATION: danger_warning companions detect the ambush, protection companions fight
        # DEATH POSSIBLE - Mugging gone wrong
        
        # COMPANION: Danger warning check (Whiskers, Slick)
        warner = self._lists.has_companion_with_bonus(self, "danger_warning")
        if warner and self.get_companion(warner)["status"] == "alive":
            type.type("You're about to take a shortcut through a dark alley when " + bright(warner) + " goes absolutely crazy.")
            print("\n")
            if "Cat" in self.get_companion(warner).get("type", ""):
                type.type(warner + " arches their back and hisses at the alley entrance. Ears flat. Tail puffed.")
            elif "Rat" in self.get_companion(warner).get("type", ""):
                type.type(warner + " starts squeaking frantically, biting your collar, pulling you backward.")
            else:
                type.type(warner + " makes alarmed sounds, physically trying to stop you from entering.")
            print("\n")
            type.type("You hesitate. Peer into the darkness. And you see them.")
            print("\n")
            type.type("Three figures. Waiting. One has something that catches the streetlight. A knife.")
            print("\n")
            type.type("You back away slowly. They don't see you. " + warner + " just saved you from a mugging.")
            print("\n")
            type.type(green(warner + "'s danger sense kicked in! Ambush avoided!"))
            self.restore_sanity(5)
            self.pet_companion(warner)
            print("\n")
            return
        
        type.type("You step out of your car and decide to take a shortcut through a dark alley. Faster than going around.")
        print("\n")
        type.type("Halfway through, you hear footsteps behind you. Heavy. Fast. Getting closer.")
        print("\n")
        type.type("You turn around. Three men. Hoodies pulled low. One has a knife that catches the streetlight.")
        print("\n")
        type.type(quote("Wallet. Phone. Everything. Now."))
        print("\n")
        answer = ask.option("What do you do? ", ["comply", "run", "fight"])
        print("\n")
        if answer == "comply":
            stolen = min(self.get_balance(), random.randint(100, 500))
            type.type("You hand over everything. They rifle through your pockets, take what they want.")
            print("\n")
            type.type("One of them punches you in the gut anyway. Just because he can.")
            print("\n")
            type.type(quote("Stay down. Count to a hundred. Don't look at our faces."))
            print("\n")
            type.type("You do what they say. When you finally look up, they're gone.")
            print("\n")
            type.type("You lost " + red(bright("$" + str(int(stolen)))) + ".")
            self.change_balance(-stolen)
            self.hurt(15)
            self.lose_sanity(10)
        elif answer == "run":
            type.type("You bolt. Legs pumping. Heart screaming. The alley seems to stretch forever.")
            print("\n")
            chance = random.randrange(10)
            if chance < 6:
                type.type("You burst onto the main street. People. Cars. Safety.")
                print("\n")
                type.type("You don't stop running for three blocks. When you finally look back, no one's following.")
                print("\n")
                type.type("Your lungs burn. Your hands shake. But you're alive. You're alive.")
                self.hurt(5)
                self.lose_sanity(8)
            elif chance < 9:
                type.type("You trip. Garbage bag. Your ankle twists and you go down hard.")
                print("\n")
                type.type("They're on you in seconds. Kicks. Punches. The knife flashes.")
                print("\n")
                type.type("You curl into a ball and take it. It feels like forever.")
                print("\n")
                type.type("When they finally leave, you're bleeding from a gash on your arm. Your ribs scream.")
                stolen = min(self.get_balance(), random.randint(200, 800))
                type.type(" They took " + red(bright("$" + str(int(stolen)))) + ".")
                self.change_balance(-stolen)
                self.hurt(35)
                self.lose_sanity(15)
                self.add_danger("Knife Wound")
            else:
                type.type("You don't make it.")
                print("\n")
                type.type("The knife catches you between the shoulder blades. You feel the cold before the pain.")
                print("\n")
                type.type("Your legs stop working. The ground rushes up to meet you.")
                print("\n")
                type.type("The last thing you see is the dirty concrete. The last thing you hear is their footsteps fading.")
                print("\n")
                type.type("The last thing you think is: " + italic("I should have just given them the money."))
                print("\n")
                self.die("Stabbed in a back alley. Another body. Another statistic.")
                return
        else:  # fight
            # COMPANION: Protection check (Lucky)
            protector = self._lists.has_companion_with_bonus(self, "protection")
            if protector and self.get_companion(protector)["status"] == "alive":
                type.type("Something snaps inside you. And " + bright(protector) + " feels it too.")
                print("\n")
                type.type(protector + " launches at the nearest mugger. Snarling. Biting. Three legs of fury.")
                print("\n")
                type.type("The mugger screams. His buddies hesitate. You grab a trash can lid and swing.")
                print("\n")
                type.type("Between you and " + protector + ", the three of them decide it's not worth it. They run.")
                print("\n")
                type.type("You stand there, chest heaving. " + protector + " stands beside you, growling at the empty alley.")
                print("\n")
                type.type(green(protector + " fought alongside you! Together you're unstoppable."))
                self.hurt(5)
                self.restore_sanity(5)
                self.pet_companion(protector)
                # Lucky might get hurt
                if random.randrange(3) == 0:
                    type.type(protector + " took a kick in the side. They're limping a little. But they're okay.")
                    self._companions[protector]["happiness"] = max(0, self._companions[protector]["happiness"] - 5)
            else:
                type.type("Something snaps inside you. You're tired. Tired of being afraid. Tired of being nothing.")
            print("\n")
            type.type("You charge at them, screaming. Pure animal rage.")
            print("\n")
            chance = random.randrange(10)
            if chance < 2:
                type.type("They weren't expecting that. The first one goes down when your fist connects with his nose.")
                print("\n")
                type.type("Blood sprays. The other two hesitate. You grab a trash can lid and swing.")
                print("\n")
                type.type("They run. They actually run. You stand there, chest heaving, covered in someone else's blood.")
                print("\n")
                type.type("You won. Somehow. You have no idea how.")
                self.hurt(10)
                self.restore_sanity(5)  # Cathartic
            elif chance < 7:
                type.type("You get one good hit in. Then the knife finds your stomach.")
                print("\n")
                type.type("It doesn't hurt at first. Just pressure. Then heat. Then agony.")
                print("\n")
                type.type("You collapse. They take everything and run.")
                print("\n")
                type.type("You drag yourself to the street, leaving a trail of blood. Someone calls an ambulance.")
                stolen = self.get_balance()
                self.change_balance(-stolen)
                self.hurt(60)
                self.lose_sanity(20)
                self.add_danger("Gut Wound")
            else:
                type.type("The knife goes into your throat before you can even swing.")
                print("\n")
                type.type("You try to scream but it comes out as a gurgle. Blood. So much blood.")
                print("\n")
                type.type("You fall. The world tilts. The stars above blur into smears of light.")
                print("\n")
                type.type("Your last thought is that you never got to make your million.")
                print("\n")
                self.die("Bled out in an alley. The muggers split your cash three ways.")
                return
        print("\n")

    def gas_station_robbery(self):
        # EVENT: Caught in a gas station during an armed robbery
        # EFFECTS: Comply = potential hostage situation; Hide = escape or get caught; Hero = save day or die
        # COMPANION INTEGRATION: danger_warning companions give early warning, Slick finds escape route
        # DEATH POSSIBLE - Wrong place, wrong time
        
        # COMPANION: Danger warning check - avoid the situation entirely
        warner = self._lists.has_companion_with_bonus(self, "danger_warning")
        if warner and self.get_companion(warner)["status"] == "alive" and random.randrange(3) == 0:
            type.type("You're about to walk into the gas station when " + bright(warner) + " starts acting strange.")
            print("\n")
            type.type("Agitated. Pulling at you. Refusing to let you go in.")
            print("\n")
            type.type("You hesitate at the door. Then you hear it from inside: " + quote("EVERYBODY ON THE GROUND!"))
            print("\n")
            type.type("Your blood goes cold. There's a robbery happening. Right now. Right where you almost walked in.")
            print("\n")
            type.type("You back away slowly. Call 911 from the parking lot. The police handle it.")
            print("\n")
            type.type(green(warner + " sensed the danger! You avoided the robbery entirely!"))
            self.pet_companion(warner)
            self.restore_sanity(5)
            print("\n")
            return
        
        type.type("You drive your car to a gas station for supplies. Just snacks. Maybe some coffee.")
        print("\n")
        type.type("You're browsing the chips when the door slams open.")
        print("\n")
        type.type(quote("EVERYBODY ON THE GROUND! NOW!"))
        print("\n")
        type.type("A man with a shotgun. Ski mask. Shaking hands. This is really happening.")
        print("\n")
        type.type("The cashier freezes. A mother clutches her child. An old man drops his coffee.")
        print("\n")
        type.type("The robber swings the gun around, wild-eyed.")
        print("\n")
        answer = ask.option("What do you do? ", ["comply", "hide", "hero"])
        print("\n")
        if answer == "comply":
            type.type("You drop to the floor. Face down. Hands visible. Make yourself small.")
            print("\n")
            type.type("The robber empties the register. Grabs cigarettes. His eyes keep darting to the door.")
            print("\n")
            type.type("He's scared. That makes him dangerous.")
            print("\n")
            chance = random.randrange(10)
            if chance < 8:
                type.type("Sirens in the distance. He panics. Runs. Gone.")
                print("\n")
                type.type("You stay on the floor for a long time after. Just breathing. Just existing.")
                self.lose_sanity(12)
            else:
                type.type("He decides he needs a hostage. His hand grabs your collar.")
                print("\n")
                type.type("You're dragged toward the door. The shotgun barrel is cold against your temple.")
                print("\n")
                type.type("Outside. Police lights. He's screaming. They're screaming. Everyone's screaming.")
                print("\n")
                chance2 = random.randrange(3)
                if chance2 == 0:
                    type.type("The sniper takes the shot. The robber's head snaps back.")
                    print("\n")
                    type.type("His blood is in your mouth. On your face. You're screaming.")
                    print("\n")
                    type.type("They pry you from his body. You can't stop shaking for hours.")
                    self.lose_sanity(30)
                    self.hurt(5)
                else:
                    type.type("His finger twitches. The gun goes off.")
                    print("\n")
                    type.type("The world goes white. Then nothing.")
                    print("\n")
                    self.die("Wrong place. Wrong time. Hostage situation gone wrong.")
                    return
        elif answer == "hide":
            type.type("You duck behind a shelf. Slowly, carefully, you crawl toward the back.")
            print("\n")
            type.type("The robber is focused on the register. You're almost to the storage room...")
            print("\n")
            chance = random.randrange(10)
            if chance < 7:
                type.type("You make it. Hide behind boxes of toilet paper and canned goods.")
                print("\n")
                type.type("You can hear everything. The shouting. The crying. The crash of the register hitting the floor.")
                print("\n")
                type.type("Then sirens. Running footsteps. Silence.")
                print("\n")
                type.type("The police find you an hour later, still hiding. Curled up like a child.")
                self.lose_sanity(15)
            else:
                type.type("A chip bag crinkles under your knee. The robber spins.")
                print("\n")
                type.type(quote("I SEE YOU! GET OUT HERE!"))
                print("\n")
                type.type("The shotgun is pointed right at you. You raise your hands and step out.")
                print("\n")
                type.type(quote("Think you're smart? Think you can hide from me?"))
                print("\n")
                type.type("He hits you with the stock. Your vision explodes into stars.")
                self.hurt(25)
                self.lose_sanity(15)
        else:  # hero
            type.type("There's a fire extinguisher on the wall. Three feet away. You could make it.")
            print("\n")
            type.type("The robber's back is turned. Yelling at the cashier. Now or never.")
            print("\n")
            chance = random.randrange(10)
            if chance < 3:
                type.type("You grab it. Swing. Connect with his skull. He goes down like a sack of meat.")
                print("\n")
                type.type("The shotgun clatters to the floor. You kick it away. Stand over him, chest heaving.")
                print("\n")
                type.type("The other customers stare at you like you're insane. Maybe you are.")
                print("\n")
                type.type("The police call you a hero. The cashier gives you $100 from his own pocket.")
                self.change_balance(100)
                self.restore_sanity(10)
                self.meet("Gas Station Hero")
            elif chance < 7:
                type.type("He turns too fast. Sees you reaching. The shotgun comes up.")
                print("\n")
                type.type("BANG.")
                print("\n")
                type.type("The blast catches your shoulder. You spin. Hit the floor. The pain is unreal.")
                print("\n")
                type.type("But you're alive. He runs. Sirens are close.")
                print("\n")
                type.type("You'll never have full use of that arm again.")
                self.hurt(50)
                self.lose_sanity(20)
                self.add_danger("Shoulder Destroyed")
            else:
                type.type("You're too slow. Way too slow.")
                print("\n")
                type.type("The shotgun blast takes you in the chest. The world goes red, then black.")
                print("\n")
                type.type("You tried to be a hero. Heroes die young.")
                print("\n")
                self.die("Shot trying to stop a robbery. They put your picture on the news.")
                return
        print("\n")

    def carbon_monoxide(self):
        # EVENT: Carbon monoxide leak while sleeping in car
        # EFFECTS: 50% escape (30 damage + 20 sanity); 30% rescued (45 damage + 25 sanity + $500 hospital); 20% death
        # BRUTAL: Adds "Damaged Exhaust" danger if survived
        # DEATH POSSIBLE - Silent killer
        type.type("A pounding headache. The worst you've ever had.")
        print("\n")
        type.type("Your thoughts are sluggish. Thick. Like wading through mud.")
        print("\n")
        type.type("Something's wrong. The car smells... off. Exhaust. How long have you been breathing this?")
        print("\n")
        type.type("Your hands feel so far away. Moving them takes forever.")
        print("\n")
        chance = random.randrange(10)
        if chance < 5:
            type.type("Some survival instinct kicks in. You fumble for the door handle. Miss. Try again.")
            print("\n")
            type.type("The door opens. Fresh air hits your face. You fall out onto the pavement.")
            print("\n")
            type.type("You lay there, gasping, staring at the sky, for what feels like hours.")
            print("\n")
            type.type("Your exhaust pipe has a hole. It's been leaking carbon monoxide into the car.")
            print("\n")
            type.type("You almost died in your sleep. You almost didn't wake up at all.")
            self.hurt(30)
            self.lose_sanity(20)
            self.add_danger("Damaged Exhaust")
        elif chance < 8:
            type.type("You try to move but your body won't cooperate. Too tired. Just... so tired.")
            print("\n")
            type.type("Maybe if you close your eyes for just a second...")
            print("\n")
            type.type("...")
            print("\n")
            type.type("A tap on the window. Muffled shouting. Someone's breaking the glass.")
            print("\n")
            type.type("Fresh air. Screaming sirens. The inside of an ambulance.")
            print("\n")
            type.type("The doctors say you were minutes away from brain damage. Or death.")
            self.hurt(45)
            self.lose_sanity(25)
            self.add_danger("Damaged Exhaust")
            if self.get_balance() >= 500:
                type.type("Hospital bill: " + red(bright("$500")) + ". They saved your life, so.")
                self.change_balance(-500)
        else:
            type.type("You're so tired. The headache is fading. Everything is fading.")
            print("\n")
            type.type("This isn't so bad. Peaceful, almost. Like sinking into warm water.")
            print("\n")
            type.type("Your eyes close. Your breathing slows. Your heart follows.")
            print("\n")
            type.type("They find your body two days later. The car is still running.")
            print("\n")
            self.die("Carbon monoxide poisoning. They say it's painless. They hope it's painless.")
            return
        print("\n")

    def drowning_dream(self):
        # EVENT: Surreal drowning nightmare that may become reality
        # BRUTAL: Dream-like sequence with potential death
        # DEATH POSSIBLE - Dream or reality?
        type.type("Sitting in your car, your mind drifts. You dream of water. Dark water. Deep water. Rising water.")
        print("\n")
        type.type("You're in a car—your car—and water is pouring in through every crack.")
        print("\n")
        type.type("You can't open the doors. The pressure is too much. The windows won't break.")
        print("\n")
        type.type("The water reaches your waist. Your chest. Your neck. Your mouth.")
        print("\n")
        type.type("You scream but water fills your lungs instead of air.")
        print("\n")
        type.type("...")
        print("\n")
        chance = random.randrange(10)
        if chance < 7:
            type.type("You wake up GASPING. Clawing at your throat. Soaking wet with sweat.")
            print("\n")
            type.type("Just a dream. Just a dream. Just a—")
            print("\n")
            type.type("Your feet are wet. You look down.")
            print("\n")
            type.type("Rain. It's raining. Water leaked through a crack in your window.")
            print("\n")
            type.type("Just rain. You're fine. You're fine. You're fine.")
            self.lose_sanity(15)
            self.hurt(5)
        elif chance < 9:
            type.type("You wake up underwater.")
            print("\n")
            type.type("THIS ISN'T A DREAM. Your car is IN THE RIVER. You must have rolled down the embankment while sleeping.")
            print("\n")
            type.type("The water is at your waist. Rising fast. You fumble for the window crank.")
            print("\n")
            type.type("It's stuck. You slam your elbow against the glass. Again. Again. AGAIN.")
            print("\n")
            type.type("It cracks. Shatters. Water rushes in but you have an opening.")
            print("\n")
            type.type("You squeeze through, cutting yourself on the glass, and kick toward the surface.")
            print("\n")
            type.type("Air. Sweet, precious air. You drag yourself onto the bank and collapse.")
            print("\n")
            type.type("Your car is gone. Everything you own is gone. But you're alive.")
            self.hurt(40)
            self.lose_sanity(25)
            self.remove_item("Car")
            lost = self.get_balance() * 0.3
            self.change_balance(-lost)
        else:
            type.type("You never wake up.")
            print("\n")
            type.type("The car rolled into the river while you slept. By the time the water woke you, it was too late.")
            print("\n")
            type.type("You fight. God, how you fight. But the doors won't open and the windows won't break.")
            print("\n")
            type.type("Your last breath comes as a desperate gasp. Water fills the void.")
            print("\n")
            type.type("They find the car three days later. Your hands are still on the door handle.")
            print("\n")
            self.die("Drowned in your car. Some nightmares are real.")
            return
        print("\n")

    def heart_attack_scare(self):
        # EVENT: Stress-induced cardiac event while walking to casino
        # EFFECTS: 50% panic attack (15 dmg + 20 sanity + $300); 30% mild heart attack (40 dmg + "Heart Condition" + $2000); 20% death
        # BRUTAL: Can result in instant death from massive heart attack
        # DEATH POSSIBLE - The stress catches up
        type.type("You step out of your car and head toward the casino when it hits. Pain. Crushing pain in your chest.")
        print("\n")
        type.type("You can't breathe. Your left arm is tingling. Your vision is going gray at the edges.")
        print("\n")
        type.type("This is it. This is how it ends. Not at the table. In a parking lot.")
        print("\n")
        type.type("You collapse against your car. Hand clutching your chest. People are staring.")
        print("\n")
        chance = random.randrange(10)
        if chance < 5:
            type.type("Someone calls 911. Paramedics. Hospital. Tests.")
            print("\n")
            type.type("It wasn't a heart attack. Panic attack. Severe anxiety. Stress.")
            print("\n")
            type.type("The doctor looks at you with something like pity.")
            print("\n")
            type.type(quote("Sir, if you keep living like this, next time it WILL be a heart attack."))
            print("\n")
            type.type("He gives you pills. You can't afford to fill the prescription.")
            self.hurt(15)
            self.lose_sanity(20)
            if self.get_balance() >= 300:
                type.type("ER visit: " + red(bright("$300")) + ".")
                self.change_balance(-300)
        elif chance < 8:
            type.type("It IS a heart attack. A mild one, they say. Like that's supposed to be comforting.")
            print("\n")
            type.type("You spend three days in the hospital. They put a stent in your artery.")
            print("\n")
            type.type("The doctor tells you to change your lifestyle. Eat better. Stress less. Exercise.")
            print("\n")
            type.type("You're a homeless gambling addict. Lifestyle changes aren't really an option.")
            self.hurt(40)
            self.lose_sanity(25)
            self.add_danger("Heart Condition")
            if self.get_balance() >= 2000:
                type.type("Hospital bill: " + red(bright("$2000")) + ". Worth it to be alive, you guess.")
                self.change_balance(-2000)
        else:
            type.type("It's a heart attack. A big one. The kind that kills people.")
            print("\n")
            type.type("You try to call for help but no sound comes out. Your body won't cooperate.")
            print("\n")
            type.type("People walk past. They think you're drunk. Or crazy. They don't stop.")
            print("\n")
            type.type("The world gets very small. Just you and the pain and the fading light.")
            print("\n")
            type.type("Your last thought is about cards. You were so close. So close.")
            print("\n")
            self.die("Heart attack. The stress finally won. The house always wins.")
            return
        print("\n")

    def drug_dealer_encounter(self):
        # EVENT: Drug dealers mistake you for a buyer/informant
        # EFFECTS: Various - can buy cocaine ($500), get beaten (15-45 damage), or shot and killed
        # BRUTAL: Running has high death chance; can acquire "Bag of Cocaine" item
        # DEATH POSSIBLE - Wrong crowd
        type.type("A car pulls up next to you. Windows tinted black. Engine rumbling.")
        print("\n")
        type.type("The window rolls down. A face stares out. Cold eyes. Gold teeth.")
        print("\n")
        type.type(quote("You the one been asking around? Looking for... product?"))
        print("\n")
        type.type("You haven't been asking around. This is a case of mistaken identity.")
        print("\n")
        answer = ask.option("What do you say? ", ["wrong person", "play along", "run"])
        print("\n")
        if answer == "wrong person":
            type.type(quote("I think you've got the wrong guy. I don't—"))
            print("\n")
            type.type("He cuts you off. " + quote("Don't play dumb. Marcus said you was looking."))
            print("\n")
            type.type("You don't know any Marcus. Your heart is pounding.")
            print("\n")
            chance = random.randrange(10)
            if chance < 6:
                type.type(quote("Nah, this ain't him.") + " The passenger leans over, squinting. " + quote("Wrong car. My bad."))
                print("\n")
                type.type("The window rolls up. The car drives away. You nearly collapse with relief.")
                self.lose_sanity(10)
            else:
                type.type("He doesn't believe you. Door opens. He gets out. He's holding something metal.")
                print("\n")
                type.type(quote("You talked to the cops, didn't you? You a snitch?"))
                print("\n")
                type.type("Before you can answer, his fist connects with your face. Then again. Then the metal thing—a pipe.")
                print("\n")
                type.type("You go down. They beat you until you stop moving. Take your wallet. Leave you bleeding.")
                self.hurt(45)
                self.lose_sanity(20)
                stolen = min(self.get_balance(), random.randint(200, 500))
                self.change_balance(-stolen)
        elif answer == "play along":
            type.type("Some insane survival instinct kicks in. You play along.")
            print("\n")
            type.type(quote("Yeah, that's me. What you got?"))
            print("\n")
            type.type("He grins. Shows you a bag of white powder. Wants $500.")
            print("\n")
            if self.get_balance() >= 500:
                answer2 = ask.yes_or_no("Buy the drugs? ($500) ")
                if answer2 == "yes":
                    type.type("You hand over the money. Take the bag. The car drives away.")
                    print("\n")
                    type.type("You're holding cocaine. What the hell are you supposed to do with cocaine?")
                    print("\n")
                    self.change_balance(-500)
                    self.add_item("Bag of Cocaine")
                else:
                    type.type(quote("Actually, I'm good. Changed my mind."))
                    print("\n")
                    type.type("His face hardens. " + quote("You wasting my time?"))
                    print("\n")
                    chance = random.randrange(3)
                    if chance == 0:
                        type.type("He spits on your car and drives off. Lucky.")
                        self.lose_sanity(8)
                    else:
                        type.type("He gets out. Punches you once, hard. " + quote("Don't waste my time again."))
                        self.hurt(15)
                        self.lose_sanity(12)
            else:
                type.type(quote("I don't have enough cash on me right now..."))
                print("\n")
                type.type(quote("Then why you wastin' my time?"))
                print("\n")
                type.type("He slaps you across the face and drives off. You got off easy.")
                self.hurt(5)
                self.lose_sanity(10)
        else:  # run
            type.type("You turn and bolt. Stupid. So stupid. But instinct takes over.")
            print("\n")
            type.type("Behind you, car doors open. Footsteps. Shouting.")
            print("\n")
            chance = random.randrange(10)
            if chance < 4:
                type.type("You're faster than you thought. Or they're lazier than expected.")
                print("\n")
                type.type("You cut through an alley, over a fence, through someone's yard.")
                print("\n")
                type.type("When you finally stop running, you're lost. But alive. Definitely alive.")
                self.hurt(5)
                self.lose_sanity(12)
            elif chance < 8:
                type.type("They catch you in thirty seconds. You're not fast. You're not young.")
                print("\n")
                type.type("The beating is methodical. Professional. They know how to hurt without killing.")
                print("\n")
                type.type("When they leave, you crawl to a gas station and call for help.")
                self.hurt(40)
                self.lose_sanity(20)
                stolen = self.get_balance()
                self.change_balance(-stolen)
            else:
                type.type("You hear the gunshot before you feel it. Your leg goes out from under you.")
                print("\n")
                type.type("Then another. Your back. Hot and wet and wrong.")
                print("\n")
                type.type("You hit the ground. The sky is very blue today, you notice.")
                print("\n")
                type.type("Footsteps approach. A face looks down at you. Disappointed, almost.")
                print("\n")
                type.type(quote("Shouldn't have run."))
                print("\n")
                type.type("One more shot. The sky goes dark.")
                print("\n")
                self.die("Shot while running from drug dealers. Wrong place. Wrong time. Wrong identity.")
                return
        print("\n")

    def bridge_contemplation(self):
        # EVENT: Dark suicidal thoughts at a bridge (low sanity trigger)
        # CONDITION: Sanity must be <= 30
        # EFFECTS: Step back = restore sanity; Stay = stranger saves you; Call hotline = restore 25 sanity
        # NOTE: Sensitive mental health content handled respectfully
        # DEATH POSSIBLE - Dark thoughts
        if self.get_sanity() > 30:
            self.day_event()
            return
        type.type("You find yourself on a bridge. You don't remember leaving your car.")
        print("\n")
        type.type("You're standing at the railing. Looking down at the water. So far down.")
        print("\n")
        type.type("Your hands are on the cold metal. When did you get out of the car?")
        print("\n")
        type.type("The water looks peaceful. Dark and cold and peaceful. No more debt. No more hunger.")
        print("\n")
        type.type("No more losing. No more trying. Just... nothing.")
        print("\n")
        type.type("A voice in your head says: " + italic("It would be so easy. Just let go."))
        print("\n")
        answer = ask.option("What do you do? ", ["step back", "stay", "call for help"])
        print("\n")
        if answer == "step back":
            type.type("You force yourself to step back. One step. Then another.")
            print("\n")
            type.type("Your hands are shaking. You're crying. When did you start crying?")
            print("\n")
            type.type("You get back in your car. You drive away. You don't look back.")
            print("\n")
            type.type("You're not okay. But you're alive. Today, that's enough.")
            self.lose_sanity(10)
            self.restore_sanity(15)  # Net positive for choosing life
        elif answer == "stay":
            type.type("You stay at the railing. Minutes pass. Maybe hours.")
            print("\n")
            type.type("A car stops. Someone gets out. A woman's voice, soft and scared.")
            print("\n")
            type.type(quote("Hey. Hey there. Are you okay? Please step back from the edge."))
            print("\n")
            type.type("You look at her. She looks terrified. Terrified for YOU.")
            print("\n")
            type.type("When's the last time anyone was scared for you? When's the last time anyone cared?")
            print("\n")
            type.type("You step back. She holds you while you cry. A stranger. Holding you while you fall apart.")
            self.restore_sanity(20)
            self.meet("Bridge Angel")
        else:  # call for help
            type.type("With shaking hands, you pull out your phone. 988. The suicide hotline.")
            print("\n")
            type.type("A voice answers. Calm. Kind. They talk to you for an hour.")
            print("\n")
            type.type("They don't judge. They don't tell you you're being stupid. They just... listen.")
            print("\n")
            type.type("When you finally hang up, you're sitting in your car. Still on the bridge. But back from the edge.")
            print("\n")
            type.type("You're not fixed. But you're here. That matters.")
            self.restore_sanity(25)
        print("\n")

    def food_poisoning(self):
        # EVENT: Severe food poisoning from gas station food
        # EFFECTS: 60% survive (25 dmg + 10 sanity); 30% hospitalized (45 dmg + $800 + "Weakened Immune System"); 10% death from sepsis
        # BRUTAL: Can cause death from bacterial sepsis
        # DEATH POSSIBLE - Bad luck
        type.type("You're hunched over in your car seat. You ate something from a gas station. In retrospect, that was a mistake.")
        print("\n")
        type.type("The first cramp hits around 2 AM. Then another. Then the real fun begins.")
        print("\n")
        type.type("You're vomiting. You're... the other thing too. Your body is emptying itself from both ends.")
        print("\n")
        type.type("The pain is unreal. Your stomach feels like it's being stabbed from the inside.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("It goes on for hours. You lose count of how many times you throw up.")
            print("\n")
            type.type("But by dawn, it's fading. Your body has expelled the poison.")
            print("\n")
            type.type("You lie on the cold ground next to your car, exhausted, dehydrated, but alive.")
            print("\n")
            type.type("You'll never eat gas station sushi again. Lesson learned.")
            self.hurt(25)
            self.lose_sanity(10)
        elif chance < 9:
            type.type("By morning, you're seeing double. Your heart is racing. This is bad. Really bad.")
            print("\n")
            type.type("Someone finds you passed out next to your car and calls 911.")
            print("\n")
            type.type("The hospital pumps your stomach. IV fluids. They say you had severe dehydration.")
            print("\n")
            type.type("Two more hours and your organs would have started failing.")
            self.hurt(45)
            self.lose_sanity(15)
            self.add_danger("Weakened Immune System")
            if self.get_balance() >= 800:
                type.type("Hospital bill: " + red(bright("$800")) + ".")
                self.change_balance(-800)
        else:
            type.type("The vomiting stops. That's not a good sign. Your body has given up fighting.")
            print("\n")
            type.type("You can't move. Can't speak. Can barely see.")
            print("\n")
            type.type("The bacteria has reached your bloodstream. Sepsis. Multiple organ failure.")
            print("\n")
            type.type("You die in your car, alone, because you ate a $3.99 egg salad sandwich.")
            print("\n")
            self.die("Food poisoning. Death by gas station sushi. An ignoble end.")
            return
        print("\n")

    def attacked_by_dog(self):
        # DEATH POSSIBLE - Animal attack
        # COMPANION INTEGRATION: Lucky/protection companion fights the stray
        
        # COMPANION: Lucky specifically can fight off the dog
        if self.has_companion("Lucky") and self.get_companion("Lucky")["status"] == "alive":
            type.type("You step out of your car when you hear growling. A big stray dog. Teeth bared.")
            print("\n")
            type.type("Before you can react, " + bright("Lucky") + " is already between you and the stray.")
            print("\n")
            type.type("Three-legged but fearless. Lucky stands his ground, growling back.")
            print("\n")
            type.type("The two dogs have a standoff. Circling. Snarling. Your heart is in your throat.")
            print("\n")
            if random.randrange(3) != 0:
                type.type("Lucky barks once. A sharp, commanding sound. The stray flinches.")
                print("\n")
                type.type("Then the stray backs down. Tucks its tail. Trots away.")
                print("\n")
                type.type("Lucky doesn't relax until the stray is completely out of sight. Then he turns to you and wags his tail.")
                print("\n")
                type.type(green("Lucky protected you from the stray! Best boy."))
                self.pet_companion("Lucky")
                self.restore_sanity(5)
            else:
                type.type("The stray lunges. Lucky meets it head-on. Fur flies. Blood draws.")
                print("\n")
                type.type("It's over in seconds. The stray yelps and runs. Lucky stands victorious.")
                print("\n")
                type.type("But he's hurt. A gash on his side. He limps over to you, tail still wagging.")
                print("\n")
                type.type("You patch him up. He licks your hand. This dog would die for you.")
                self.hurt(5)  # You got scratched too
                self._companions["Lucky"]["happiness"] = max(0, self._companions["Lucky"]["happiness"] - 5)
                self.pet_companion("Lucky")
                self.pet_companion("Lucky")
                self.restore_sanity(3)
            print("\n")
            return
        
        type.type("You step out of your car and head toward a convenience store when you hear it. Growling. Deep and low.")
        print("\n")
        type.type("A dog. Big. Rottweiler or pit bull, you can't tell. No leash. No owner. Just teeth.")
        print("\n")
        type.type("It's staring at you. Hackles raised. Drool dripping from its jaws.")
        print("\n")
        type.type("You freeze. Don't run. Don't make eye contact. You remember reading that somewhere.")
        print("\n")
        chance = random.randrange(10)
        if chance < 4:
            type.type("The dog watches you. Sniffs the air. Decides you're not worth the effort.")
            print("\n")
            type.type("It trots away, looking for something more interesting.")
            print("\n")
            type.type("You don't move for five minutes. Then you walk VERY quickly to your car.")
            self.lose_sanity(8)
        elif chance < 8:
            type.type("It charges. Ninety pounds of muscle and fury coming right at you.")
            print("\n")
            type.type("You throw your arms up. Its jaws close on your forearm. You SCREAM.")
            print("\n")
            type.type("It shakes its head, tearing flesh. You punch it. Kick it. Nothing works.")
            print("\n")
            type.type("Someone runs over with a stick. Beats the dog off you. It finally lets go and runs.")
            print("\n")
            type.type("Your arm is a mess of blood and torn muscle. You can see bone.")
            self.hurt(40)
            self.lose_sanity(15)
            self.add_danger("Dog Bite Wound")
            if self.get_balance() >= 600:
                type.type("ER stitches: " + red(bright("$600")) + ".")
                self.change_balance(-600)
        else:
            type.type("It goes for your throat. Instinct. Predator targeting the kill zone.")
            print("\n")
            type.type("You get your arm up just in time. It bites deep. You fall.")
            print("\n")
            type.type("Then it's on top of you. Biting. Tearing. You're screaming. So much blood.")
            print("\n")
            type.type("It finds your throat eventually. They always do.")
            print("\n")
            type.type("Your last sight is the blue sky through red haze. Your last sound is growling.")
            print("\n")
            self.die("Mauled to death by a stray dog. Not every monster is human.")
            return
        print("\n")

    def electrocution_hazard(self):
        # DEATH POSSIBLE - Freak accident
        type.type("It's raining hard. You jump out of your car and run for cover under an awning.")
        print("\n")
        type.type("There's a puddle. A big one. And an old electrical box on the wall, sparking.")
        print("\n")
        type.type("You don't notice until it's too late. Your foot hits the water.")
        print("\n")
        chance = random.randrange(10)
        if chance < 5:
            type.type("A jolt runs through you. Painful but brief. The breaker must have tripped.")
            print("\n")
            type.type("You jump back, heart pounding. That could have killed you.")
            print("\n")
            type.type("You report the hazard to the shop owner. They seem unimpressed.")
            self.hurt(10)
            self.lose_sanity(8)
        elif chance < 8:
            type.type("The current grabs you. Your muscles seize. You can't move. Can't breathe.")
            print("\n")
            type.type("Someone tackles you away from the puddle. A stranger. Saved your life.")
            print("\n")
            type.type("Your heart is racing. Irregular. Your hands won't stop shaking.")
            print("\n")
            type.type("The hospital keeps you overnight for observation. Arrhythmia.")
            self.hurt(35)
            self.lose_sanity(15)
            if self.get_balance() >= 500:
                type.type("Hospital: " + red(bright("$500")) + ".")
                self.change_balance(-500)
        else:
            type.type("The current hits you like a freight train. Every muscle in your body contracts at once.")
            print("\n")
            type.type("You can't scream. Can't move. Just the electricity, burning through you.")
            print("\n")
            type.type("Your heart stops. It tries to start again. Stops. Starts. Stops.")
            print("\n")
            type.type("By the time someone kicks you free of the puddle, you're gone.")
            print("\n")
            self.die("Electrocution. A faulty wire and a puddle. That's all it took.")
            return
        print("\n")

    def car_explosion(self):
        # DEATH POSSIBLE - Mechanical failure
        type.type("You turn the key in the ignition. The engine makes a strange noise. A ticking.")
        print("\n")
        type.type("Something smells wrong. Gas. Strong and getting stronger.")
        print("\n")
        type.type("Instinct screams at you: GET OUT. GET OUT NOW.")
        print("\n")
        answer = ask.option("What do you do? ", ["bail out", "investigate", "ignore it"])
        print("\n")
        if answer == "bail out":
            type.type("You throw yourself out of the car and run. Don't look back. Just run.")
            print("\n")
            chance = random.randrange(3)
            if chance == 0:
                type.type("You're ten feet away when the engine catches fire. Fifteen when it explodes.")
                print("\n")
                type.type("The shockwave knocks you flat. Heat washes over you. Debris rains down.")
                print("\n")
                type.type("Your car—your home—is a fireball. Everything you owned is gone.")
                print("\n")
                type.type("But you're alive. Somehow. Alive.")
                self.hurt(20)
                self.lose_sanity(25)
                self.remove_item("Car")
                lost = self.get_balance() * 0.2
                self.change_balance(-lost)
            else:
                type.type("Nothing explodes. The engine just... dies. Smoke pours out.")
                print("\n")
                type.type("False alarm. Fuel line leak. Bad, but not explosive.")
                print("\n")
                type.type("You feel foolish. But also glad you trusted your gut.")
                self.add_danger("Fuel Leak")
                self.lose_sanity(10)
        elif answer == "investigate":
            type.type("You pop the hood. Lean in to look. The gas smell is overwhelming.")
            print("\n")
            chance = random.randrange(10)
            if chance < 7:
                type.type("There's the problem. A cracked fuel line. Gas dripping onto hot metal.")
                print("\n")
                type.type("You back away slowly. Very slowly. Get some distance.")
                print("\n")
                type.type("You disconnect the battery and let it cool down. Crisis averted.")
                self.add_danger("Fuel Leak")
                self.lose_sanity(10)
            else:
                type.type("The spark happens while you're leaning over the engine.")
                print("\n")
                type.type("The last thing you see is a flash of orange. The last thing you feel is heat.")
                print("\n")
                type.type("They find your body twenty feet from the wreckage.")
                print("\n")
                self.die("Car explosion. Mechanical failure meets human curiosity. Boom.")
                return
        else:  # ignore it
            type.type("It's probably nothing. This car always makes weird noises.")
            print("\n")
            type.type("You turn the key again. The ticking gets louder.")
            print("\n")
            chance = random.randrange(10)
            if chance < 4:
                type.type("The engine catches. Runs rough, but runs. The smell fades.")
                print("\n")
                type.type("You should really get that checked out. You won't, but you should.")
                self.add_danger("Fuel Leak")
            else:
                type.type("The fireball is instantaneous. You don't even have time to scream.")
                print("\n")
                type.type("Glass and metal and fire, all at once. The car becomes your coffin.")
                print("\n")
                self.die("Died in a car explosion. Should have bailed. Should have investigated. Did neither.")
                return
        print("\n")

    def knife_wound_infection(self):
        # CONDITIONAL DEATH - Consequence of earlier event
        if not self.has_danger("Knife Wound"):
            self.day_event()
            return
        type.type("You check yourself in the car mirror. That knife wound from the mugging isn't healing right.")
        print("\n")
        type.type("It's red. Swollen. Hot to the touch. Pus oozing from the edges.")
        print("\n")
        type.type("You're running a fever. Shaking. This is bad.")
        print("\n")
        chance = random.randrange(10)
        if chance < 5:
            type.type("You drag yourself to a free clinic. They take one look and rush you to a hospital.")
            print("\n")
            type.type("Antibiotics. IV drip. They save your arm. Barely.")
            self.hurt(25)
            self.remove_danger("Knife Wound")
        elif chance < 8:
            type.type("The infection has spread. Sepsis. Your blood is poisoned.")
            print("\n")
            type.type("Three days in the ICU. They're not sure you're going to make it.")
            print("\n")
            type.type("You do. Barely. But you'll never forget how close you came.")
            self.hurt(50)
            self.lose_sanity(20)
            self.remove_danger("Knife Wound")
            if self.get_balance() >= 3000:
                type.type("Hospital bill: " + red(bright("$3000")) + ".")
                self.change_balance(-3000)
        else:
            type.type("You wait too long. The infection reaches your heart.")
            print("\n")
            type.type("Endocarditis. By the time the ambulance arrives, you're barely conscious.")
            print("\n")
            type.type("You die on the operating table. A stupid knife wound. A stupid delay.")
            print("\n")
            self.die("Died from an infected knife wound. Should have seen a doctor sooner.")
            return
        print("\n")

    def gut_wound_complications(self):
        # CONDITIONAL DEATH - Consequence of earlier event
        if not self.has_danger("Gut Wound"):
            self.day_event()
            return
        type.type("You shift in your car seat and wince. Your gut wound has been getting worse. Much worse.")
        print("\n")
        type.type("The stitches popped. You can see... things you shouldn't be seeing.")
        print("\n")
        type.type("The pain is constant now. You can't eat. Can barely drink.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("You make it to an ER. Emergency surgery. They have to remove part of your intestine.")
            print("\n")
            type.type("Recovery takes weeks. But you survive. Somehow.")
            self.hurt(40)
            self.lose_sanity(20)
            self.remove_danger("Gut Wound")
        else:
            type.type("The wound has gone septic. Your organs are failing.")
            print("\n")
            type.type("You die in the back of your car, alone, holding your stomach together with your hands.")
            print("\n")
            self.die("Gut wound complications. Internal bleeding. Organ failure. Game over.")
            return
        print("\n")

    def devils_bargain_consequence(self):
        # CONDITIONAL EVENT - The devil collects
        if not self.has_danger("Devil's Bargain"):
            self.day_event()
            return
        if self.has_met("Devil's Collection"):
            self.day_event()
            return
        self.meet("Devil's Collection")
        type.type("The stranger from before is back. Standing by your car. Waiting.")
        print("\n")
        type.type(quote("You've done well. Very well. But it's time to pay what you owe."))
        print("\n")
        type.type("You try to run but your legs won't move. You try to scream but nothing comes out.")
        print("\n")
        type.type("He walks toward you. Slowly. That smile never reaching those dark, dead eyes.")
        print("\n")
        type.type(quote("Don't worry. This won't hurt."))
        print("\n")
        type.type("He reaches into your chest. No wound. No blood. Just... cold.")
        print("\n")
        type.type("When he withdraws his hand, he's holding something small and bright. Your... something.")
        print("\n")
        type.type(quote("A pleasure doing business."))
        print("\n")
        type.type("He's gone. You feel... empty. Hollow. Like a part of you is missing.")
        print("\n")
        type.type("You'll never feel truly happy again. That was the price.")
        self.lose_sanity(50)
        self.add_danger("Soulless")
        print("\n")

    # ==========================================
    # CONNECTED & CONDITIONAL EVENTS - MEGA BATCH
    # ==========================================

    # === SOULLESS CONSEQUENCES (Devil's Bargain Chain) ===
    def soulless_emptiness(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("You leave your car and head to the casino. You win at the tables. The dealer pushes chips toward you.")
        print("\n")
        type.type("You should feel something. Joy. Triumph. Relief. Anything.")
        print("\n")
        type.type("You feel nothing. Absolutely nothing. Just... hollow.")
        print("\n")
        type.type("The other gamblers are celebrating, crying, raging. You just exist.")
        print("\n")
        type.type("Is this what you traded for? Was it worth it?")
        self.lose_sanity(5)
        print("\n")

    def soulless_mirror(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("You catch your reflection in your car window. Something's wrong.")
        print("\n")
        type.type("Your eyes. They're darker than they should be. Empty. Dead.")
        print("\n")
        type.type("You look away quickly. You don't want to see what you've become.")
        self.lose_sanity(8)
        print("\n")

    def soulless_recognition(self):
        if not self.has_danger("Soulless"):
            self.day_event()
            return
        type.type("A child points at you from across the parking lot.")
        print("\n")
        type.type("Their mother pulls them close, hurrying away. But you heard what the kid said:")
        print("\n")
        type.type(quote("Mommy, why doesn't that man have a shadow?"))
        print("\n")
        type.type("You look down. Your shadow is... faint. Barely there. Flickering.")
        print("\n")
        type.type("When did that start happening?")
        self.lose_sanity(12)
        print("\n")

    # === DOG BITE WOUND CHAIN ===
    def dog_bite_rabies_scare(self):
        if not self.has_danger("Dog Bite Wound"):
            self.day_event()
            return
        type.type("You look at your arm in the car. Your dog bite wound is healing, but something else is wrong.")
        print("\n")
        type.type("You're feverish. Light hurts your eyes. Water makes you gag.")
        print("\n")
        type.type("Oh God. Rabies. The dog had rabies.")
        print("\n")
        type.type("You race to the hospital. They test you. Hours of waiting.")
        print("\n")
        chance = random.randrange(10)
        if chance < 8:
            type.type("Negative. No rabies. Just a regular infection and paranoia.")
            print("\n")
            type.type("They give you antibiotics and tell you to calm down.")
            self.hurt(10)
            self.lose_sanity(15)
        else:
            type.type("Positive. The dog had rabies. You have rabies.")
            print("\n")
            type.type("They start the shots immediately. Painful. Expensive. Necessary.")
            print("\n")
            type.type("You'll live, but you'll never forget the two weeks of waiting to die.")
            self.hurt(30)
            self.lose_sanity(25)
            if self.get_balance() >= 2000:
                type.type("Rabies treatment: " + red(bright("$2000")) + ".")
                self.change_balance(-2000)
        self.remove_danger("Dog Bite Wound")
        print("\n")

    # === FUEL LEAK CHAIN ===
    def fuel_leak_fire(self):
        if not self.has_danger("Fuel Leak"):
            self.day_event()
            return
        type.type("You smell gas again. Stronger this time. Much stronger.")
        print("\n")
        type.type("Then you see the spark. A wire rubbing against metal.")
        print("\n")
        type.type("You have maybe three seconds to react.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("You bail out. Hit the ground rolling. Keep going.")
            print("\n")
            type.type("The car doesn't explode. But it does catch fire. Your home is burning.")
            print("\n")
            type.type("You watch helplessly as everything you own goes up in flames.")
            self.remove_item("Car")
            self.remove_danger("Fuel Leak")
            self.lose_sanity(30)
            lost = self.get_balance() * 0.25
            self.change_balance(-lost)
        else:
            type.type("Too slow. The fire starts before you're out.")
            print("\n")
            type.type("Your clothes catch. Your hair. You're screaming and rolling on the ground.")
            print("\n")
            type.type("Someone puts you out with a fire extinguisher. But the damage is done.")
            self.hurt(50)
            self.lose_sanity(35)
            self.remove_item("Car")
            self.remove_danger("Fuel Leak")
            self.add_danger("Burn Scars")
        print("\n")

    def fuel_leak_fixed(self):
        if not self.has_danger("Fuel Leak"):
            self.day_event()
            return
        if self.get_balance() < 150:
            self.day_event()
            return
        type.type("A mechanic notices your car leaking gas in the parking lot.")
        print("\n")
        type.type(quote("Hey buddy, you know your fuel line is busted? That's a fire hazard."))
        print("\n")
        type.type(quote("I can fix it for $150. Cash. Right now. Before you blow yourself up."))
        print("\n")
        answer = ask.yes_or_no("Pay the mechanic? ($150) ")
        if answer == "yes":
            type.type("He works for an hour. Gets covered in grease. But he fixes it.")
            print("\n")
            type.type(quote("There. No more kaboom.") + " He grins.")
            self.change_balance(-150)
            self.remove_danger("Fuel Leak")
        else:
            type.type("He shrugs. " + quote("Your funeral, man."))
            self.lose_sanity(5)
        print("\n")

    # === HEART CONDITION CHAIN ===
    def heart_condition_flare(self):
        if not self.has_danger("Heart Condition"):
            self.day_event()
            return
        type.type("You grip the steering wheel. Your chest tightens. Not again. Not now.")
        print("\n")
        type.type("You fumble for the pills the doctor gave you. Can't find them.")
        print("\n")
        type.type("The pain spreads. Down your arm. Up your jaw. Can't breathe.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("Found them. You swallow two dry and wait.")
            print("\n")
            type.type("Slowly, the pain fades. The pressure eases. You're okay. This time.")
            self.hurt(15)
            self.lose_sanity(10)
        elif chance < 9:
            type.type("Someone sees you clutching your chest. Calls 911.")
            print("\n")
            type.type("Hospital. Another stent. Another lecture about stress.")
            self.hurt(35)
            self.lose_sanity(15)
            if self.get_balance() >= 1500:
                type.type("Bill: " + red(bright("$1500")) + ".")
                self.change_balance(-1500)
        else:
            type.type("This one is worse. Much worse. The big one.")
            print("\n")
            type.type("You collapse. Everything goes gray. Then black.")
            print("\n")
            self.die("Heart attack. Your body couldn't take the stress anymore.")
            return
        print("\n")

    # === SHOULDER DESTROYED CHAIN ===
    def shoulder_chronic_pain(self):
        if not self.has_danger("Shoulder Destroyed"):
            self.day_event()
            return
        type.type("You try to adjust your car seat and wince. Your shoulder is on fire today. Some days are worse than others.")
        print("\n")
        type.type("You can barely lift your arm. Simple things—opening doors, reaching for chips—agony.")
        print("\n")
        type.type("This is your life now. Chronic pain. Forever.")
        self.hurt(10)
        self.lose_sanity(5)
        print("\n")

    def shoulder_painkiller_addiction(self):
        if not self.has_danger("Shoulder Destroyed"):
            self.day_event()
            return
        if self.has_met("Painkiller Offer"):
            self.day_event()
            return
        self.meet("Painkiller Offer")
        type.type("A guy in the parking lot notices you wincing, rubbing your shoulder.")
        print("\n")
        type.type(quote("Bad injury? I got something for that. Take the edge off."))
        print("\n")
        type.type("He shows you a bottle of pills. Oxycodone. Not his prescription.")
        print("\n")
        if self.get_balance() >= 100:
            answer = ask.yes_or_no("Buy the painkillers? ($100) ")
            if answer == "yes":
                type.type("You hand over the money. Pop two pills.")
                print("\n")
                type.type("Twenty minutes later, the pain is... gone. Just warmth and peace.")
                print("\n")
                type.type("This is dangerous. You know this is dangerous. But God, it feels good.")
                self.change_balance(-100)
                self.hurt(-20)  # Heals temporarily
                self.restore_sanity(15)
                self.add_danger("Painkiller Dependency")
            else:
                type.type("You shake your head. He shrugs and walks away.")
        else:
            type.type("You can't afford them anyway. Small mercies.")
        print("\n")

    # === PAINKILLER DEPENDENCY CHAIN ===
    def painkiller_withdrawal(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("You're sitting in your car, shaking. You're out of pills. Have been for two days.")
        print("\n")
        type.type("Your body is screaming. Sweating. Shaking. Nausea. Everything hurts MORE than before.")
        print("\n")
        type.type("This is withdrawal. This is what addiction feels like.")
        print("\n")
        self.hurt(25)
        self.lose_sanity(20)
        print("\n")

    def painkiller_dealer_returns(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("A tap on your car window - the pill guy is back. Like he knew you'd need him.")
        print("\n")
        type.type(quote("Looking rough, friend. Need a refill?"))
        print("\n")
        if self.get_balance() >= 150:
            answer = ask.yes_or_no("Buy more pills? ($150 - prices went up) ")
            if answer == "yes":
                type.type("You pay. You take. The pain goes away. The cycle continues.")
                self.change_balance(-150)
                self.hurt(-15)
                self.restore_sanity(10)
            else:
                type.type("You say no. It's the hardest thing you've ever done.")
                print("\n")
                type.type("He'll be back. They always come back.")
        else:
            type.type("You don't have the money. He walks away. The withdrawal continues.")
            self.hurt(10)
            self.lose_sanity(10)
        print("\n")

    def painkiller_overdose(self):
        if not self.has_danger("Painkiller Dependency"):
            self.day_event()
            return
        type.type("Sitting in your car, you take an extra pill. Then another. The pain is so bad today.")
        print("\n")
        type.type("Then another. When did you take the last one? You can't remember.")
        print("\n")
        type.type("Everything feels slow. Warm. Your breathing is shallow.")
        print("\n")
        chance = random.randrange(10)
        if chance < 7:
            type.type("You fall asleep. Wake up twelve hours later, covered in sweat, but alive.")
            print("\n")
            type.type("That was close. Too close. Maybe you should stop.")
            self.hurt(20)
            self.lose_sanity(15)
        else:
            type.type("You stop breathing. Simple as that. The pills take you under and you don't come back up.")
            print("\n")
            self.die("Overdose. Another statistic. Another preventable death.")
            return
        print("\n")

    # === BURN SCARS CHAIN ===
    def burn_scars_stares(self):
        if not self.has_danger("Burn Scars"):
            self.day_event()
            return
        type.type("You step out of your car. People stare at your scars. They try to hide it, but they stare.")
        print("\n")
        type.type("Children point. Adults look away too quickly. Nobody meets your eyes.")
        print("\n")
        type.type("You used to be invisible. Now you're a spectacle.")
        self.lose_sanity(8)
        print("\n")

    def burn_scars_infection(self):
        if not self.has_danger("Burn Scars"):
            self.day_event()
            return
        type.type("You check yourself in the car mirror. Your burn scars are weeping. Infected, probably. You can't afford proper care.")
        print("\n")
        type.type("You clean them with water and hope. That's all you have.")
        print("\n")
        chance = random.randrange(5)
        if chance == 0:
            type.type("The infection spreads. You need real help.")
            self.hurt(30)
            self.add_danger("Infected Burns")
        else:
            type.type("It seems to be okay. For now.")
            self.hurt(10)
        print("\n")

    # === ATM THEFT CHAIN ===
    def atm_theft_police(self):
        if not self.has_danger("ATM Theft"):
            self.day_event()
            return
        type.type("A police car pulls up next to you. Your heart stops.")
        print("\n")
        type.type(quote("Sir, can you step out of the vehicle?"))
        print("\n")
        type.type("They have photos. Security footage. The ATM. You taking the money.")
        print("\n")
        chance = random.randrange(10)
        if chance < 5:
            type.type("They give you a ticket. $200 fine for petty theft. Consider yourself lucky.")
            self.change_balance(-200)
            self.remove_danger("ATM Theft")
        elif chance < 8:
            type.type("They arrest you. A night in jail. You make bail with everything you have.")
            lost = min(self.get_balance(), 500)
            self.change_balance(-lost)
            self.lose_sanity(20)
            self.remove_danger("ATM Theft")
        else:
            type.type("The bank is pressing charges. Felony theft. You spend three months in jail.")
            print("\n")
            type.type("When you get out, you're broke. Broken. But free.")
            self.change_balance(-self.get_balance())
            self.lose_sanity(50)
            self.hurt(30)
            self.remove_danger("ATM Theft")
        print("\n")

    # === WEAKENED IMMUNE SYSTEM CHAIN ===
    def weakened_immune_cold(self):
        if not self.has_danger("Weakened Immune System"):
            self.day_event()
            return
        type.type("Sitting in your car, you catch a cold. Nothing serious, normally.")
        print("\n")
        type.type("But with your weakened immune system, it hits hard. Very hard.")
        print("\n")
        type.type("You're bedridden for a week. In your car. Miserable.")
        self.hurt(25)
        self.lose_sanity(10)
        print("\n")

    def weakened_immune_pneumonia(self):
        if not self.has_danger("Weakened Immune System"):
            self.day_event()
            return
        type.type("You're shivering in your car. That cold turned into something worse. Pneumonia.")
        print("\n")
        type.type("You can't breathe. You're coughing blood. This is bad.")
        print("\n")
        chance = random.randrange(10)
        if chance < 7:
            type.type("Hospital. Antibiotics. Oxygen. They save you.")
            self.hurt(40)
            self.lose_sanity(15)
            if self.get_balance() >= 1000:
                type.type(" Bill: " + red(bright("$1000")) + ".")
                self.change_balance(-1000)
        else:
            type.type("Your lungs fill with fluid. You drown in your own body.")
            print("\n")
            self.die("Pneumonia. Your immune system couldn't fight anymore.")
            return
        print("\n")

    # === COCAINE CHAIN (from drug dealer event) ===
    def cocaine_temptation(self):
        if not self.has_item("Bag of Cocaine"):
            self.day_event()
            return
        type.type("You're sitting in your car. You still have that bag of cocaine. It's been staring at you.")
        print("\n")
        type.type("You've never tried it. But you're tired. So tired. And it promises energy.")
        print("\n")
        answer = ask.option("What do you do? ", ["try it", "sell it", "throw it away"])
        print("\n")
        if answer == "try it":
            type.type("You snort a line. Your first time.")
            print("\n")
            type.type("...")
            print("\n")
            type.type("Oh. OH. This is... this is AMAZING.")
            print("\n")
            type.type("Colors are brighter. You're invincible. Every problem seems solvable.")
            print("\n")
            type.type("You don't sleep for 36 hours. When you crash, you crash HARD.")
            self.hurt(-30)  # Temporary boost
            self.restore_sanity(20)  # Temporary
            self.remove_item("Bag of Cocaine")
            self.add_danger("Cocaine User")
        elif answer == "sell it":
            type.type("You find a buyer. Some desperate guy in the casino bathroom.")
            print("\n")
            type.type("You sell it for $300. Not a great deal, but you're not a drug dealer.")
            self.change_balance(300)
            self.remove_item("Bag of Cocaine")
        else:
            type.type("You flush it. Watch it swirl away. Good riddance.")
            print("\n")
            type.type("Part of you wonders what it would have been like. Most of you is relieved.")
            self.remove_item("Bag of Cocaine")
            self.restore_sanity(5)
        print("\n")

    def cocaine_crash(self):
        if not self.has_danger("Cocaine User"):
            self.day_event()
            return
        type.type("You're slumped in your car seat. The crash comes. And it's BRUTAL.")
        print("\n")
        type.type("Depression. Paranoia. Your teeth won't stop chattering.")
        print("\n")
        type.type("You need more. Your body NEEDS more. But you don't have any.")
        self.hurt(30)
        self.lose_sanity(25)
        print("\n")

    def cocaine_heart_attack(self):
        if not self.has_danger("Cocaine User"):
            self.day_event()
            return
        type.type("You're gripping the steering wheel. Your heart is racing. Has been for hours. Something's wrong.")
        print("\n")
        type.type("Chest pain. Arm pain. The cocaine was cut with something. Something bad.")
        print("\n")
        chance = random.randrange(10)
        if chance < 6:
            type.type("It passes. Slowly. You lie in your car, convinced you're dying, but you don't.")
            self.hurt(35)
            self.lose_sanity(20)
            self.remove_danger("Cocaine User")
        else:
            type.type("Your heart gives out. Cocaine-induced cardiac arrest.")
            print("\n")
            self.die("Drug overdose. The coke was cut with fentanyl. You never had a chance.")
            return
        print("\n")

    # === STRAY CAT FRIEND CHAIN ===
    def stray_cat_sick(self):
        if not self.has_met("Stray Cat Friend"):
            self.day_event()
            return
        if self.has_met("Cat Died"):
            self.day_event()
            return
        type.type("Your stray cat friend looks rough today. Skinnier than usual. Coughing.")
        print("\n")
        type.type("It's sick. Really sick. And you can't afford a vet.")
        print("\n")
        if self.get_balance() >= 200:
            answer = ask.yes_or_no("Take the cat to a vet? ($200) ")
            if answer == "yes":
                type.type("The vet says it's an infection. Treatable. They give you medicine.")
                print("\n")
                type.type("The cat purrs weakly as you carry it back to your car. You saved it.")
                self.change_balance(-200)
                self.restore_sanity(15)
                self.meet("Cat Saved")
            else:
                type.type("You can't. You just can't afford it. You hope it gets better on its own.")
                self.lose_sanity(10)
        else:
            type.type("You can't afford a vet. All you can do is keep it warm and hope.")
            self.lose_sanity(10)
        print("\n")

    def stray_cat_dies(self):
        if not self.has_met("Stray Cat Friend"):
            self.day_event()
            return
        if self.has_met("Cat Saved"):
            self.day_event()
            return
        if self.has_met("Cat Died"):
            self.day_event()
            return
        self.meet("Cat Died")
        type.type("The cat is lying next to your car. Not moving.")
        print("\n")
        type.type("You know before you touch it. You know. But you touch it anyway.")
        print("\n")
        type.type("Cold. Stiff. Gone.")
        print("\n")
        type.type("You bury it behind a gas station. Mark the spot with a rock.")
        print("\n")
        type.type("It was just a stray. Just a cat. But it was YOUR cat. And now it's gone.")
        self.lose_sanity(25)
        print("\n")

    def stray_cat_has_kittens(self):
        if not self.has_met("Cat Saved"):
            self.day_event()
            return
        if self.has_met("Cat Had Kittens"):
            self.day_event()
            return
        self.meet("Cat Had Kittens")
        type.type("Your cat is acting strange. Nesting. Meowing constantly.")
        print("\n")
        type.type("Oh. OH. She's not sick. She's pregnant. WAS pregnant.")
        print("\n")
        type.type("Tiny mewling sounds. Three kittens. Eyes closed. Perfect.")
        print("\n")
        type.type("Great. Now you have four cats. In your car. What is your life?")
        self.restore_sanity(20)
        print("\n")

    # === BRIDGE ANGEL CHAIN ===
    def bridge_angel_returns(self):
        if not self.has_met("Bridge Angel"):
            self.day_event()
            return
        if self.has_met("Bridge Angel Returns"):
            self.day_event()
            return
        self.meet("Bridge Angel Returns")
        type.type("You step out of your car and see her again. The woman from the bridge. The one who stopped you.")
        print("\n")
        type.type("She recognizes you too. Walks over. Smiles.")
        print("\n")
        type.type(quote("Hey. You're still here. I'm glad."))
        print("\n")
        type.type("She gives you her number. " + quote("If you ever need to talk. About anything. Call me."))
        print("\n")
        type.type("You put it in your pocket. It feels like it weighs a hundred pounds.")
        self.add_item("Angel's Number")
        self.restore_sanity(15)
        print("\n")

    def call_bridge_angel(self):
        if not self.has_item("Angel's Number"):
            self.day_event()
            return
        type.type("Bad day. Really bad. Sitting in your car, you dig out that number. Your hands are shaking.")
        print("\n")
        type.type("She answers on the second ring.")
        print("\n")
        type.type(quote("Hey. I was hoping you'd call. Talk to me. What's going on?"))
        print("\n")
        type.type("You talk for two hours. About everything. The gambling. The car. The fear.")
        print("\n")
        type.type("She doesn't judge. Doesn't lecture. Just listens.")
        print("\n")
        type.type(quote("You're stronger than you think. I believe in you."))
        self.restore_sanity(30)
        print("\n")

    # === GAS STATION HERO CHAIN ===
    def gas_station_hero_recognized(self):
        if not self.has_met("Gas Station Hero"):
            self.day_event()
            return
        type.type("You head out from your car to a convenience store. Someone points at you.")
        print("\n")
        type.type(quote("That's him! That's the guy who stopped the robbery!"))
        print("\n")
        type.type("People start clapping. The cashier gives you free coffee.")
        print("\n")
        type.type("You feel like a fraud. You just reacted. Didn't think. Could have died.")
        print("\n")
        type.type("But the coffee is nice.")
        self.restore_sanity(10)
        print("\n")

    def gas_station_hero_interview(self):
        if not self.has_met("Gas Station Hero"):
            self.day_event()
            return
        if self.has_met("Hero Interview"):
            self.day_event()
            return
        self.meet("Hero Interview")
        type.type("You're sitting in your car when a news van pulls up. A local station wants to interview you about the robbery.")
        print("\n")
        answer = ask.yes_or_no("Do the interview? ")
        if answer == "yes":
            type.type("They film you by your car. Which is... not a great look.")
            print("\n")
            type.type("The segment runs on the evening news. " + quote("Local Homeless Man Stops Armed Robbery!"))
            print("\n")
            type.type("The comments online are split between calling you a hero and mocking your living situation.")
            self.restore_sanity(5)
            self.lose_sanity(5)  # Mixed feelings
            self.meet("Media Known")
        else:
            type.type("You decline. You're not a hero. You just did what anyone would do.")
        print("\n")

    # === HIGH ROLLER KEYCARD CHAIN ===
    def high_roller_room_visit(self):
        if not self.has_item("High Roller Keycard"):
            self.day_event()
            return
        type.type("You leave your car and head to the casino. You use your High Roller Keycard. The doors slide open.")
        print("\n")
        type.type("It's another world in here. Velvet ropes. Crystal chandeliers. Free champagne.")
        print("\n")
        type.type("The other high rollers barely glance at you. You don't belong here. They know it.")
        print("\n")
        type.type("But for one night, you pretend.")
        self.restore_sanity(10)
        self.heal(10)
        print("\n")

    def high_roller_whale(self):
        if not self.has_item("High Roller Keycard"):
            self.day_event()
            return
        if self.has_met("Met the Whale"):
            self.day_event()
            return
        self.meet("Met the Whale")
        type.type("You head to the casino. A massive man in a tailored suit sits next to you at the high roller bar.")
        print("\n")
        type.type(quote("You're new here. I can tell. What's your story?"))
        print("\n")
        type.type("You give him the short version. The million dollar goal. The car. All of it.")
        print("\n")
        type.type("He laughs. Not cruelly. Almost fondly.")
        print("\n")
        type.type(quote("I started the same way. Sleeping in a truck. Now look at me."))
        print("\n")
        type.type("He slides you a chip. Black. Worth $500.")
        print("\n")
        type.type(quote("Consider it a loan from a kindred spirit. Pay it forward someday."))
        self.change_balance(500)
        self.restore_sanity(15)
        print("\n")

    # === OLD RIVAL CHAIN ===
    def old_rival_encounter(self):
        if not self.has_met("Old Rival"):
            self.day_event()
            return
        if self.has_met("Rival Confrontation"):
            self.day_event()
            return
        self.meet("Rival Confrontation")
        type.type("You step out of your car and head to the casino. You see Jake Morrison again. This time, you're not letting him walk away.")
        print("\n")
        type.type(quote("Jake. Wait."))
        print("\n")
        type.type("He turns. That same smug expression. " + quote("What do you want?"))
        print("\n")
        answer = ask.option("What do you say? ", ["apologize", "confront", "ask for help"])
        print("\n")
        if answer == "apologize":
            type.type(quote("I'm sorry. For... everything. Back then."))
            print("\n")
            type.type("His expression softens. Just a little.")
            print("\n")
            type.type(quote("Yeah. Me too. Take care of yourself, man."))
            self.restore_sanity(10)
        elif answer == "confront":
            type.type(quote("You think you're better than me? You're just luckier."))
            print("\n")
            type.type("He laughs. " + quote("Keep telling yourself that. I'll be in my house. You'll be in your car."))
            print("\n")
            type.type("He walks away. You stand there, fists clenched, trembling with rage.")
            self.lose_sanity(15)
        else:
            type.type(quote("I need help. I'm... I'm in trouble. Bad trouble."))
            print("\n")
            type.type("For a moment, something flickers in his eyes. Pity? Concern?")
            print("\n")
            type.type(quote("I can't help you, man. I'm sorry. Get some real help."))
            print("\n")
            type.type("He leaves. At least he said sorry. That's something.")
            self.lose_sanity(5)
        print("\n")

    # === MEDIA KNOWN CHAIN ===
    def media_known_harassed(self):
        if not self.has_met("Media Known"):
            self.day_event()
            return
        type.type("You step out of your car and someone recognizes you from the news. They're filming you with their phone.")
        print("\n")
        type.type(quote("This is the homeless hero guy! He's gambling! Isn't that ironic?!"))
        print("\n")
        type.type("They're laughing. Mocking you. You try to leave but they follow.")
        print("\n")
        type.type(quote("Homeless hero is GAMBLING! Content! Pure CONTENT!"))
        print("\n")
        type.type("Security finally escorts them out. But the damage is done. You feel exposed.")
        self.lose_sanity(15)
        print("\n")

    def media_known_documentary(self):
        if not self.has_met("Media Known"):
            self.day_event()
            return
        if self.has_met("Documentary Offer"):
            self.day_event()
            return
        self.meet("Documentary Offer")
        type.type("A filmmaker approaches your car. Says they want to make a documentary about you.")
        print("\n")
        type.type(quote("Your story is compelling. The struggle. The goal. The hope."))
        print("\n")
        type.type(quote("We'll pay you $5000 for your participation."))
        print("\n")
        answer = ask.yes_or_no("Agree to the documentary? ")
        if answer == "yes":
            type.type("They film you for weeks. The good days. The bad days. All of it.")
            print("\n")
            type.type("It's exposing. Humiliating sometimes. But $5000 is $5000.")
            self.change_balance(5000)
            self.lose_sanity(10)
            self.restore_sanity(5)  # Mixed feelings
        else:
            type.type("You decline. Some things aren't for sale.")
        print("\n")

    # === DAMAGED EXHAUST CHAIN ===
    def damaged_exhaust_fixed(self):
        if not self.has_danger("Damaged Exhaust"):
            self.day_event()
            return
        if self.get_balance() < 100:
            self.day_event()
            return
        type.type("A mechanic spots your exhaust problem while you're parked.")
        print("\n")
        type.type(quote("That's leaking carbon monoxide into your car. You'll die in your sleep."))
        print("\n")
        type.type(quote("I can patch it for $100. Not perfect, but safe."))
        print("\n")
        answer = ask.yes_or_no("Pay for the repair? ($100) ")
        if answer == "yes":
            type.type("Fixed. You'll live to see another day.")
            self.change_balance(-100)
            self.remove_danger("Damaged Exhaust")
        else:
            type.type("He shakes his head. " + quote("Your funeral."))
        print("\n")

    def damaged_exhaust_again(self):
        if not self.has_danger("Damaged Exhaust"):
            self.day_event()
            return
        type.type("A headache again. That familiar exhaust smell.")
        print("\n")
        type.type("The carbon monoxide is still leaking. You're slowly poisoning yourself.")
        print("\n")
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
            print("\n")
            self.die("Carbon monoxide poisoning. You knew the exhaust was broken. You didn't fix it.")
            return
        print("\n")

    # === UNPAID TICKETS EXTENDED CHAIN ===
    def unpaid_tickets_boot(self):
        if not self.has_danger("Unpaid Tickets"):
            self.day_event()
            return
        if self.has_met("Car Booted"):
            self.day_event()
            return
        self.meet("Car Booted")
        type.type("You return to your car to find a boot on your wheel.")
        print("\n")
        type.type("A bright yellow wheel clamp. Can't drive. Can't move. Trapped.")
        print("\n")
        type.type("The fine is $300 to get it removed. Plus your unpaid tickets.")
        print("\n")
        if self.get_balance() >= 300:
            answer = ask.yes_or_no("Pay to remove the boot? ($300) ")
            if answer == "yes":
                type.type("You pay. The city tow guy removes it without a word.")
                self.change_balance(-300)
                self.remove_danger("Unpaid Tickets")
            else:
                type.type("You can't afford it. You sleep next to a booted car. Wonderful.")
                self.remove_item("Car")  # Can't use it while booted
                self.add_danger("Booted Car")
        else:
            type.type("You can't afford it. Your home is now an immobile brick.")
            self.remove_item("Car")
            self.add_danger("Booted Car")
        print("\n")

    def booted_car_impound(self):
        if not self.has_danger("Booted Car"):
            self.day_event()
            return
        type.type("The tow truck arrives. They're impounding your car.")
        print("\n")
        type.type(quote("Unpaid tickets plus boot removal plus impound fee. That's $800 to get it back."))
        print("\n")
        if self.get_balance() >= 800:
            answer = ask.yes_or_no("Pay to get your car back? ($800) ")
            if answer == "yes":
                type.type("You empty your savings. They give you your car back.")
                self.change_balance(-800)
                self.remove_danger("Booted Car")
                self.remove_danger("Unpaid Tickets")
                self.add_item("Car")
            else:
                type.type("You watch them tow your home away. Everything you own. Gone.")
                lost = self.get_balance() * 0.3
                self.change_balance(-lost)
                self.lose_sanity(40)
                self.remove_danger("Booted Car")
        else:
            type.type("You don't have $800. You watch helplessly as they take everything.")
            self.lose_sanity(50)
            self.remove_danger("Booted Car")
        print("\n")

    # === RANDOM SMALL EVENTS ===
    def found_twenty(self):
        type.type("You step out of your car and find a $20 bill on the ground. No one around. Just luck.")
        self.change_balance(20)
        type.type(" Nice.")
        print("\n")

    def lost_wallet(self):
        if self.get_balance() < 50:
            self.day_event()
            return
        type.type("You shift in your car seat and realize your pocket feels light. Your wallet is gone.")
        print("\n")
        type.type("You retrace your steps. Nothing. Someone must have taken it.")
        lost = min(self.get_balance(), random.randint(50, 200))
        type.type(" You lost " + red(bright("$" + str(int(lost)))) + ".")
        self.change_balance(-lost)
        self.lose_sanity(10)
        print("\n")

    def sunburn(self):
        type.type("You fell asleep with the window cracked. In direct sunlight.")
        print("\n")
        type.type("Your arm is bright red. Blistering. You look like a lobster.")
        self.hurt(15)
        print("\n")

    def mosquito_bite_infection(self):
        type.type("You scratch your arm in the car. That mosquito bite you kept scratching? It's infected now.")
        print("\n")
        type.type("Red, swollen, oozing. You need to stop scratching it.")
        self.hurt(10)
        print("\n")

    def good_hair_day(self):
        type.type("You check yourself in the car mirror. Against all odds, your hair looks good today. How is that possible?")
        print("\n")
        type.type("You live in a car. You shower at truck stops. But today? Fabulous.")
        self.restore_sanity(5)
        print("\n")

    def bad_hair_day(self):
        type.type("You glance in the car mirror. Your hair is a disaster. A matted, greasy catastrophe.")
        print("\n")
        type.type("You try to fix it. Make it worse. Give up.")
        self.lose_sanity(3)
        print("\n")

    def found_gift_card(self):
        type.type("You find a gift card on the ground next to your car. Fast food place. Has $15 on it.")
        print("\n")
        type.type("Free food! The universe provides. Sometimes.")
        self.heal(15)
        print("\n")

    def car_battery_dead(self):
        type.type("Your car won't start. Dead battery. Of course.")
        print("\n")
        type.type("You spend an hour trying to get someone to give you a jump.")
        print("\n")
        type.type("Finally, a kind trucker helps you out. Crisis averted.")
        self.lose_sanity(8)
        print("\n")

    def flat_tire_again(self):
        type.type("Another flat tire. You're starting to think the universe hates you.")
        print("\n")
        if self.get_balance() >= 50:
            type.type("You pay a guy $50 to fix it. Whatever. Just fix it.")
            self.change_balance(-50)
        else:
            type.type("You can't afford to fix it. You sleep with a flat tire. Again.")
            self.lose_sanity(10)
        print("\n")

    def nice_weather(self):
        type.type("Perfect weather today. Not too hot. Not too cold. Just right.")
        print("\n")
        type.type("You sit outside your car and just... breathe. It's nice.")
        self.restore_sanity(8)
        print("\n")

    def terrible_weather(self):
        type.type("The weather is miserable. Rain sideways. Wind shaking your car.")
        print("\n")
        type.type("You huddle in your seat and wait for it to pass. For hours.")
        self.lose_sanity(5)
        print("\n")

    def weird_noise(self):
        type.type("Your car is making a new noise. A concerning noise.")
        print("\n")
        type.type("Clunk. Clunk. Clunk. Every time you turn.")
        print("\n")
        type.type("You have no idea what it is. You ignore it and hope for the best.")
        self.add_danger("Mystery Car Problem")
        print("\n")

    def mystery_car_problem_worsens(self):
        if not self.has_danger("Mystery Car Problem"):
            self.day_event()
            return
        type.type("That noise is getting worse. Much worse. The car shudders now too.")
        print("\n")
        chance = random.randrange(5)
        if chance == 0:
            type.type("Something FALLS OFF the car. You don't even know what it was.")
            print("\n")
            type.type("A piece of metal, clattering away down the road. Cool. Cool cool cool.")
            self.hurt(5)
            self.lose_sanity(10)
        else:
            type.type("It's probably fine. Probably.")
        print("\n")

    def got_a_tan(self):
        type.type("You catch your reflection in the car mirror. All this outdoor living has given you a nice tan.")
        print("\n")
        type.type("Silver linings. You look healthy, even if you're not.")
        self.restore_sanity(3)
        print("\n")

    def someone_stole_your_stuff(self):
        type.type("Someone broke into your car while you were at the casino.")
        print("\n")
        type.type("They didn't take money—you had that on you. But they took... things.")
        print("\n")
        type.type("A jacket. Some food. Your sense of security.")
        self.lose_sanity(15)
        self.hurt(5)
        print("\n")

    def back_pain(self):
        type.type("Your back is KILLING you. Sleeping in a car seat isn't good for the spine.")
        print("\n")
        type.type("You're getting old. And broken. This life is breaking you.")
        self.hurt(15)
        print("\n")

    def stretching_helps(self):
        type.type("You do some stretches. Yoga-ish movements. Look like an idiot in a parking lot.")
        print("\n")
        type.type("But you know what? You feel better. Less like a rusty robot.")
        self.hurt(-10)
        self.restore_sanity(5)
        print("\n")

    def random_kindness(self):
        type.type("Someone hands you a bag of groceries. Doesn't say anything. Just smiles and leaves.")
        print("\n")
        type.type("Inside: bread, peanut butter, water bottles. Basic stuff.")
        print("\n")
        type.type("Your eyes are wet. When did you become someone who needs charity?")
        self.heal(20)
        self.restore_sanity(10)
        self.lose_sanity(5)  # Mixed feelings
        print("\n")

    def random_cruelty(self):
        type.type("Some teenagers throw something at your car. Laughing. Running away.")
        print("\n")
        type.type("It's a milkshake. All over your windshield. Sticky and dripping.")
        print("\n")
        type.type("You clean it up in silence. What else can you do?")
        self.lose_sanity(12)
        print("\n")

    def prayer_answered(self):
        type.type("You're sitting in your car. You prayed last night. For something. Anything.")
        print("\n")
        type.type("Today, things went your way. Small things. But things.")
        print("\n")
        type.type("Coincidence? Divine intervention? Does it matter?")
        self.restore_sanity(15)
        print("\n")

    def prayer_ignored(self):
        type.type("You're sitting in your car. You prayed last night. Begged, really. For help.")
        print("\n")
        type.type("Today was worse than yesterday. The heavens are silent.")
        print("\n")
        type.type("Maybe no one's listening. Or maybe you're not worth listening to.")
        self.lose_sanity(10)
        print("\n")

    def found_old_photo(self):
        type.type("You find an old photo in your glove box. You forgot it was there.")
        print("\n")
        type.type("It's you. From before. Smiling. Happy. With people who loved you.")
        print("\n")
        type.type("You stare at it for a long time. Who was that person?")
        self.lose_sanity(10)
        self.restore_sanity(5)  # Bittersweet
        print("\n")

    def threw_out_old_photo(self):
        if not self.has_met("Found Old Photo"):
            self.day_event()
            return
        type.type("Sitting in your car, you look at that photo again. The happy you. The old you.")
        print("\n")
        answer = ask.yes_or_no("Throw it away? ")
        if answer == "yes":
            type.type("You rip it up. Throw the pieces out the window. Watch them scatter.")
            print("\n")
            type.type("That person is gone. Time to move on.")
            self.lose_sanity(5)
        else:
            type.type("You put it back. Can't let go. Not yet.")
        print("\n")

    def empty_event(self):
        type.type("This day's events are empty. Therefore, this played. Thank you.")
        print("\n")

    # ==========================================
    # COMPANION DAY EVENTS
    # ==========================================

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

