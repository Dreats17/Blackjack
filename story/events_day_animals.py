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

class DayAnimalsMixin:
    """Animal events: creature encounters not tied to a companion"""

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
    
    def raccoon_gang_raid(self):
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
        self.restore_sanity(5)
        self.change_balance(random.randint(10, 50))
        print("\n")

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
            self.add_item("Squirrely")
            self.add_companion("Squirrelly", "Squirrel")
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.mark_day("Squirrely Fed")
            print("\n")
            return
        
        if self.has_item("Bag of Acorns"):
            self.use_item("Bag of Acorns")
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
                self.add_companion("Squirrelly", "Squirrel")
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

        if self.has_item("Pepper Spray"):
            type.type("You grab your " + cyan(bright("Pepper Spray")) + " and give the rat a direct blast.")
            print("\n")
            type.type("Blinded and thoroughly unhappy, it leaps off the backseat and vanishes under the door before you can blink.")
            print("\n")
            type.type("No bite. No damage. Just a very offended rat and a car that smells like pepper for a week.")
            self.use_item("Pepper Spray")
            self.lose_danger("Rat")
            self.lose_sanity(1)
            print("\n")
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
    
    def grimy_gus_discovery(self):
        # EVENT: Meet Grimy Gus, a shady pawn shop owner who buys unusual items
        # CONDITION: One-time event (must not have met "Grimy Gus")
        # EFFECTS: Unlocks Grimy Gus's Pawn Emporium shop for selling collectibles
        # One-Time - Discover the pawn shop
        if not self.has_item("Car") or self.has_met("Grimy Gus"):
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

    def seagull_attack(self):
        type.type("A seagull dive-bombs your car")

        # Pack Call: both whistles together speak every animal's language at once
        if self.has_item("Animal Whistle") and self.has_item("Dog Whistle"):
            type.type(" — then freezes mid-dive.")
            print("\n")
            type.type("You blow both the " + cyan(bright("Animal Whistle")) + " and the " + cyan(bright("Dog Whistle")) + " at the same time.")
            print("\n")
            type.type("A sound no animal has ever heard before.")
            print("\n")
            type.type("Every creature within earshot looks up. The seagull stalls in the air. The pigeons on the roof go still. A dog three blocks away sits.")
            print("\n")
            type.type("The seagull lands on your hood slowly, carefully, and looks at you with something like cautious respect.")
            print("\n")
            type.type("You just spoke every animal's language at once. They heard you. All of them.")
            living = self.get_all_companions()
            if len(living) > 0:
                for name in living:
                    self._companions[name]["happiness"] = 100
                type.type("Your companion" + ("s" if len(living) > 1 else "") + " feel" + ("" if len(living) > 1 else "s") + " the resonance too. A wave of warmth passes through them.")
                print("\n")
            self.restore_sanity(8)
            print("\n")
            return

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

        if self.has_item("Slingshot"):
            type.type(" — but you're ready.")
            print("\n")
            type.type("You step out with your " + cyan(bright("Slingshot")) + ". A well-aimed stone makes your position absolutely clear.")
            print("\n")
            type.type("The seagull veers off at the last second, screaming. It does NOT come back.")
            print("\n")
            self.restore_sanity(3)
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
            self.change_balance(1)
            type.type("It's just a penny. But hey, every cent counts!")
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
            self.add_companion("Whiskers", "Stray Cat")
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
            self.add_companion("Lucky", "Three-Legged Dog")
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
            self.change_balance(1)
            self.add_companion("Mr. Pecks", "Crow")
            self.increment_statistic("companions_befriended")
            if not self.has_achievement("first_friend"):
                self.unlock_achievement("first_friend")
        elif self.has_item("Birdseed") or self.has_item("Bread"):
            item = "Birdseed" if self.has_item("Birdseed") else "Bread"
            answer = ask.yes_or_no("Offer it some " + item + "? ")
            if answer == "yes":
                self.use_item(item)
                type.type("You toss some " + item + " on the hood. The crow gobbles it up eagerly.")
                print("\n")
                type.type("Then it does something strange. It bows. An actual bow, like a little gentleman.")
                print("\n")
                type.type("From that moment on, the crow follows you everywhere. You name him " + cyan(bright("Mr. Pecks")) + ".")
                self.change_balance(1)
                self.add_companion("Mr. Pecks", "Crow")
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
            self.change_balance(1)
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
        if self.has_item("Cheese") or self.has_item("Sandwich") or self.has_item("Turkey Sandwich"):
            if self.has_item("Cheese"):
                item = "Cheese"
            elif self.has_item("Turkey Sandwich"):
                item = "Turkey Sandwich"
            else:
                item = "Sandwich"
            answer = ask.yes_or_no("Offer it some food? ")
            if answer == "yes":
                type.type("You toss a bit of " + item + " near the drain. The rat grabs it and disappears.")
                print("\n")
                type.type("But the next day, you find a small pile of coins near your car. And the rat, sitting nearby, watching.")
                print("\n")
                type.type("This continues for a week. You feed the rat, it brings you coins.")
                print("\n")
                type.type("Eventually, the rat just... moves in. You call it " + cyan(bright("Slick")) + ". It's very good at finding money.")
                self.use_item(item)
                self.change_balance(random.randint(5, 15))
                self.restore_sanity(8)
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

    def wild_rat_attack(self):
        # EVENT: A bold city rat charges you with intent — embarrassing and surprisingly dangerous
        # EFFECTS: Lose 5-10 HP, 1-3 sanity; 25% chance of Rat Bite if no Rabies already
        # Can only happen once per day (mark_day guard)
        if self.has_met_today("Wild Rat Attack"):
            self.day_event()
            return
        self.mark_day("Wild Rat Attack")

        type.type("You're standing outside a nice restaurant, checking your phone, feeling like you belong here finally.")
        print("\n")
        type.type("Then you hear it. A sound from the alley. A skittering. Fast.")
        print("\n")
        type.type("A rat — massive, glossy, city-fat — launches itself off a dumpster directly at your ankles.")
        print("\n")
        type.type("Not scurrying past. Not fleeing. " + italic("At you.") + " On purpose.")
        print("\n")

        if self.has_item("Running Shoes") or self.has_item("Pursuit Package"):
            item_name = "Running Shoes" if self.has_item("Running Shoes") else "Pursuit Package"
            type.type("Your " + cyan(bright(item_name)) + " are already on.")
            print("\n")
            type.type("The rat never closes the gap. You're half a block gone before it leaves the dumpster.")
            print("\n")
            type.type("You jog back to your car at a dignified pace. Nobody saw anything.")
            self.restore_sanity(3)
            print("\n")
            return

        answer = ask.option("What do you do? ", ["kick it away", "run", "stand your ground"])
        if answer == "kick it away":
            type.type("You swat at it with your foot. It latches onto your shoe, shakes it, and then — finally — releases.")
            print("\n")
            type.type("A well-dressed couple walking past pretends not to see. You try to pretend it didn't happen.")
            self.lose_hp(random.choice([5, 6, 7]))
            self.lose_sanity(2)
            if not self.has_status("Rabies") and random.randrange(4) == 0:
                type.type("That thing definitely broke skin. You're going to need to watch that.")
                print("\n")
                self.add_status("Rat Bite")
        elif answer == "run":
            type.type("You sprint half a block before realizing a rat is not chasing you.")
            print("\n")
            type.type("It stopped at the alley entrance and is just... watching. You are out of breath. In front of a valet stand.")
            self.lose_hp(random.choice([3, 4, 5]))
            self.lose_sanity(3)
        else:
            type.type("You hold your ground. The rat stops. You stare at each other.")
            print("\n")
            type.type("It rears up on its hind legs. You do not flinch.")
            print("\n")
            type.type("Slowly, the rat retreats. You win. But your hands are shaking.")
            self.lose_hp(random.choice([5, 8, 10]))
            self.lose_sanity(1)
        print("\n")

    # === BRIDGE ANGEL CHAIN ===

