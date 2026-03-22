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

class NightEventsMixin:
    """Night events, dreams, and nocturnal encounters by rank tier.
    
    Includes: walking events, dreams, rabbit chase chain,
    Suzy storyline night parts (favorite_color, favorite_animal),
    location-themed night events (woodlands, swamp, beach, city).
    """

    # Poor Nights (1 - 1,000)
    # Everytime
    def ditched_wallet(self):
        # EVENT: Find an abandoned wallet on the side of the road during a night walk
        # EFFECTS: Gain $65-120 (50%) or $7-50 (50%); Flask of Fortunate Night gives 5% chance bonus
        type.type("Bored out of your mind, you decide to wander along the side of the road, just to get a change of scenery from the dusty leather seats of your wagon. ")
        type.type("As you take step after step over the asphalt, you notice a ditched wallet, just laying there. I guess it's yours now. ")
        print("\n")
        random_chance = random.randrange(2)
        if random_chance == 0:
            worth = random.randint(65, 120)
        else:
            worth = random.randint(7, 50)
        type.type("Inside the wallet, you find " + green(bright("$" + str(worth))) + " dollars.")
        self.change_balance(worth)
        if self.has_item("Flask of Fortunate Night") and random.randrange(20) == 0:
            bonus = random.randint(50, 100)
            print("\n")
            type.type("The " + cyan(bright("Flask of Fortunate Night")) + " hums warm in your pocket. Fate tips its hat tonight.")
            print("\n")
            type.type("You check again — there's a folded bill tucked behind the ID. Another " + green(bright("$" + str(bonus))) + ".")
            self.change_balance(bonus)

    def went_jogging(self):
        # EVENT: Go jogging to pass the time and get exercise
        # EFFECTS: 33% chance scrape knee (5-15 damage + "Scraped Knee" injury); 67% chance heal 5-15 HP
        type.type("After spending an hour sitting in your car doing nothing, you feel like you should get some exercise. ")
        type.type("You get out of the wagon, and begin to jog down the road.")
        print("\n")
        type.type("A couple hours go by, and while jogging back, you see the wagon in the distance. ")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("But, right as you get to your car, you trip over a stone on the ground, and scrape your knee hard. Blood begins to drip down your leg. That's a bummer.")
            print("\n")
            self.hurt(random.choice([5, 10, 15]))
            self.add_injury("Scraped Knee")
            return
        else:
            type.type("You get back to the car, and get in, out of breath from your trip. You start the wagon and run the AC, and you feel good inside.")
            print("\n")
            self.heal(random.choice([5, 10, 15]))
            return

    def woodlands_path(self):
        # EVENT: Wander deep into the woods on a natural path with multiple outcomes
        # EFFECTS: 33% meet friendly deer family; 33% find dead body (search for $100-150 or risk Hepatitis); 33% uneventful
        self.meet("Woodlands Path Event")
        type.type("After wandering from your vehicle, you find yourself deep in the woods. ")
        type.type("Squirrels run by and up into the trees. The sun hits every branch and casts a shadow below. ")
        type.type("And you wander on a natural path, journeying into the unknown.")
        print("\n")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("As you walk along the path, you find a mother deer, with two children, walking the path towards you. ")
            type.type("As you get closer, the mother appears cautious, but then runs in your direction, before stopping before you. ")
            type.type("Her two children follow behind, and before you know it, the three of them wait in front of you.")
            print("\n")
            type.type("You put your hand out, and pet the mother deer. She makes a happy squeak noise, and wags her tail. ")
            type.type("She touches her head to yours, then continues down the path, with her two children following.")
            print("\n")
            
            # Animal Whistle makes the deer stay as a companion
            if self.has_item("Animal Whistle") and not self.has_companion("Grace"):
                type.type("But then - the " + magenta(bright("Animal Whistle")) + " sings softly. The mother deer stops.")
                print("\n")
                type.type("She turns back, her two fawns at her side. She looks at you with those deep, gentle eyes.")
                print("\n")
                type.type("You kneel down and the deer family approaches. The mother nuzzles your cheek. The fawns play around your feet.")
                print("\n")
                type.type("They've accepted you into their herd. You decide to call the mother " + cyan(bright("Grace")) + ".")
                print("\n")
                type.type("Grace and her fawns will follow your journey now, bringing peace wherever they go.")
                self.add_companion("Grace", "Deer")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                self.restore_sanity(8)  # Bonus sanity for magical deer moment
                print("\n")
            
            type.type("Eventually, you get to the end of the path, and find the main road. You follow it back to your wagon, and take a seat, to rest for a moment.")
            print("\n")
            return
        elif random_chance == 1:
            type.type("As you walk along the path, you notice someone leaning against a tree in front of you. ")
            type.type("As you get closer, you notice that the person's face is blue, their eyes are bloodshot, and they don't appear to be breathing.")
            print("\n")
            # ITEM: Headlamp - spot danger before it becomes a threat
            if self.has_item("Headlamp"):
                type.type("The " + magenta(bright("Headlamp")) + " cuts through the dark undergrowth ahead.")
                print("\n")
                type.type("The beam sweeps left, right, and then lands on the figure against the tree.")
                print("\n")
                type.type("You see it from fifteen feet away instead of three. Something glints near the body. Something moved.")
                print("\n")
                type.type("You stop. You back up slowly. You take the long way around.")
                print("\n")
                type.type("You make it back to the road. Shaken, but safe. Some things are better left in the dark.")
                self.restore_sanity(5)
                print("\n")
                return
            type.type("You begin to panic, before thinking through the situation. ")
            type.type("They're already dead, so there's nothing you can do to help them. ")
            type.type("Maybe they had some money on them? I mean, they're not gonna use it. Why shouldn't you?")
            print()
            type.type("Do you search the body? ")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("You rummage through the pockets, trying to find anything worthwhile. ")
                random_chance = random.randrange(4)
                if random_chance == 0:
                    self.add_status("Hepatitis")
                    type.type("As you do so, you notice the body begin to move. ")
                    type.type("It looks up at you, screams, then coughs blood all over you. ")
                    type.type("You freak out, before running back down the path the way you came.")
                    print("\n")
                    type.type("You make it back to your car, and find some old clothes to wipe the blood off your face. Great, just great. You already start to feel under the weather.")
                    print("\n")
                    return
                else:
                    type.type("After a minute of digging, you manage to find a wallet. Score!")
                    print("\n")
                    worth = random.randint(100, 150)
                    type.type("Inside the wallet, you find " + green(bright("$" + str(worth))) + " dollars.")
                    self.change_balance(worth)
                    type.type("You leave the dead body, and continue down the path, ")
                    type.type("until the forest opens up to the main road. You follow the road back to your wagon, with your winnings in hand.")
                    print("\n")
                    return
            elif answer == "no":
                type.type("While this body might be the body of a rich man, judging by the situation, it's very unlikely. ")
                type.type("Plus, dead bodies tend to be unsanitary. No, this body was simply not worth searching.")
                print("\n")
                type.type("You continue down the path, before the forest opens up to the main road. You follow the road back to your wagon, and sit. You rest for a while.")
                print("\n")
                return
        else:
            type.type("You walk, and walk, and walk further down the path, before the forest opens up to the main road. ")
            type.type("You follow the road back to your wagon, wondering if there was anything you missed. ")
            type.type("At least you made it back safe and sound.")
            print("\n")
            return

    # RABBIT CHASE CHAIN - POOR NIGHT
    def chase_the_rabbit(self):
        # EVENT: Rabbit Chase Part 1 - Spot a white rabbit and give chase (always fails)
        # CONDITION: Rabbit chase counter must be 0 (first attempt)
        # EFFECTS: Chase fails, rabbit escapes; advances rabbit chase counter
        # CHAIN: Rabbit Chase Part 1 of 4
        # First rabbit chase - always fails, starts the chain
        if self.get_rabbit_chase() != 0:
            self.night_event()
            return
        
        type.type("As you're walking along the side of the road, something catches your eye. A flash of white, darting between the bushes. A rabbit!")
        print("\n")
        type.type("Without thinking, you give chase. The little creature bounds ahead of you, zigging and zagging through the underbrush with seemingly effortless grace.")
        print("\n")
        type.type("You run and run, but no matter how fast you go, the rabbit stays just out of reach. Its white tail bobs mockingly in the moonlight.")
        print("\n")
        type.type("Finally, you stop, hands on your knees, gasping for breath. When you look up, the rabbit is gone, vanished into the night like it was never there.")
        print("\n")
        type.type(yellow("You trudge back to your wagon, defeated. But something tells you this isn't the last time you'll see that rabbit."))
        self.advance_rabbit_chase()
        print("\n")
                
    # Cheap Nights (1,000 - 10,000)
    # Everytime
    def woodlands_river(self):
        # EVENT: Wander along a river in the woods - encounter bear, treasure chest, or nothing
        # EFFECTS: 33% bear attack (75 damage + "Severed Skin", unless have Quiet Sneakers/Slippers); 33% find Map item (if not owned); 33% uneventful
        self.meet("Woodlands River Event")
        type.type("After wandering from your vehicle, you find yourself deep in the woods. ")
        type.type("Deer dart by you. Trees branches sway back and forth. ")
        type.type("And you wander along a river, journeying into the unknown.")
        print("\n")
        random_chance = random.randrange(3)
        if random_chance == 0:
            type.type("As you walk further, you stumble across a large brown bear, bathing in the river. ")
            
            # Animal Whistle can befriend the bear
            if self.has_item("Animal Whistle") and not self.has_companion("Bruno"):
                print("\n")
                type.type("The " + magenta(bright("Animal Whistle")) + " pulses warmly in your pocket. The bear's ears twitch.")
                print("\n")
                type.type("The massive creature turns its head toward you. For a moment, you lock eyes.")
                print("\n")
                type.type("Then, slowly, the bear stands up from the water - not threatening, but... curious. ")
                type.type("It approaches you with surprising gentleness, water dripping from its thick fur.")
                print("\n")
                type.type("The bear sits down in front of you like an enormous dog. You reach out and touch its wet nose. ")
                type.type("It makes a low, contented sound and leans into your hand.")
                print("\n")
                type.type("You've just made friends with a brown bear. You decide to call it " + cyan(bright("Bruno")) + ".")
                print("\n")
                type.type("Bruno shakes off the water (drenching you in the process) and follows you back to your wagon.")
                self.add_companion("Bruno", "Brown Bear")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                print("\n")
                return
            
            if self.has_item("Quiet Bunny Slippers"):
                print("\n")
                type.type("Thank goodness you're wearing your " + cyan(bright("Quiet Bunny Slippers")) + "!")
                print("\n")
                type.type("Your feet make absolutely no sound as you pirouette gracefully away from danger. ")
                type.type("The bear doesn't even twitch. ")
                type.type("You practically float back to your car, silent as a ghost in fuzzy pink footwear.")
                print("\n")
                self.restore_sanity(8)
                self.update_quiet_sneakers_durability()
                return
            elif self.has_item("Quiet Sneakers"):
                print("\n")
                type.type("Thank goodness you're wearing your " + magenta(bright("Quiet Sneakers")) + "!")
                print("\n")
                type.type("You turn and run back up the riverbank, never looking back. Eventually, you make it out of the woods, and return to your car, safe and sound.")
                print("\n")
                self.restore_sanity(5)
                self.update_quiet_sneakers_durability()
                return
            else:
                type.type("Right as you're about to turn around, you step on a branch, which makes a loud crunching noise. ")
                print("\n")
                random_chance_2 = random.randrange(2)
                if random_chance_2 == 0:
                    type.type("The bear sits up from the water, and glares at you. ")
                    type.type("Before you get a chance to react, the bear charges at you. ")
                    type.type("He swipes at your leg. He bites your arm. He punches your neck. ")
                    type.type("My, what a beating he gave you.")
                    print("\n")
                    self.hurt(75)
                    type.type("Thankfully, you're able to play dead, just long enough for the bear to walk away without killing you. ")
                    type.type("Somehow, you get up, and limp your way back to your wagon.")
                    print("\n")
                    type.type("The damage inflicted from the bear is serious and severe. ")
                    type.type("It's probably a good idea to see the doctor tomorrow, when they're open again. ")
                    type.type("In the meantime, you wrap yourself up with spare clothes, and go on with your life.")
                    self.add_injury("Severed Skin")
                    print("\n")
                    return
                elif random_chance_2 == 1:
                    type.type("Thankfully, it seems that the bear doesn't notice you. ")
                    type.type("You quietly step away, before running back up the riverbank. ")
                    type.type("Eventually, you make it out of the woods, and back to your wagon, safe and sound. ")
                    type.type("That could've gone a lot worse!")
                    print("\n")
                    return
        elif (random_chance == 1) and not (self.has_item("Map")):
            type.type("As you walk further, you stumble across an old treasure chest, sitting in the river, the water flowing around it. ")
            type.type("Walking closer, you wade the water to get to the chest, and open up the lid. ")
            type.type("Inside, you find a large paper drawing. Opening it up, you realize that it's a map that resembles the town you're parked just outside of. ")
            type.type("Down one of the side roads, there's an old bridge with a star underneath it. ")
            type.type("The caption reads 'To those who wish to visit Marvin, just go to the bridge, and follow the stars.'")
            print("\n")
            self.add_item("Map")
            type.type("You got the " + magenta(bright("Map")) + "! You can now drive to Marvin's Mystical Merchandise!")
            type.type("Without a second thought, you pocket the map, and turn back, following the riverbank home.")
            print("\n")
            return
        elif self.has_item("Fishing Rod"):
            type.type("You drop a line into the river. Something big takes it almost immediately.")
            print("\n")
            type.type("The rod bends hard. You brace your feet and pull. Whatever this is, it is fighting.")
            print("\n")
            type.type("Twenty minutes later, you haul out an enormous catfish and stare at each other in mutual disbelief.")
            print("\n")
            earnings = random.randint(30, 60)
            type.type("You sell it at the first roadside stand you find. " + green(bright("$" + str(earnings))) + ". Not bad for a night at the river.")
            self.earn_money(earnings)
            self.restore_sanity(random.choice([5, 7, 8]))
            print("\n")
            return
        else:
            type.type("You keep walking, and keep walking, and keep walking, and eventually, the woods clear up, and you're back on the main road. ")
            type.type("You follow it back to your car, wondering if there was anything else to see. Well, at least you're home, safe and sound.")
            print("\n")
            return

    def woodlands_field(self):
        # EVENT: Explore a wide open field at night with multiple random encounters
        # EFFECTS: Various - find money ($50-800), encounter mysterious figure, abandoned campsite, or wasp attack (10-20 damage)
        self.meet("Woodlands Field Event")
        type.type("After wandering from your vehicle, you find yourself in a wide open field. ")
        type.type("The grass comes up to your waist, golden and dry, rustling with every breeze. ")
        type.type("Crickets sing their evening song.")
        print("\n")
        random_chance = random.randrange(4)
        if random_chance == 0:
            type.type("As you wade through the tall grass, you notice something odd. ")
            type.type("About fifty yards ahead, there's a figure standing perfectly still. Just... standing there. Watching you.")
            print("\n")
            type.type("You stop walking. The figure doesn't move. It's too far to make out any details, just a dark silhouette against the fading sky.")
            print("\n")
            type.type("Do you approach the figure?")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("You push through the grass toward the figure. As you get closer, you realize...")
                print("\n")
                reveal = random.randrange(3)
                if reveal == 0:
                    type.type("It's a scarecrow. An old, rotting scarecrow. You laugh at yourself. But as you turn to leave, you notice something glinting at its base.")
                    print("\n")
                    worth = random.randint(150, 400)
                    type.type("Someone stashed a tin box here. Inside: " + green(bright("$" + str(worth))) + ".")
                    self.change_balance(worth)
                    print("\n")
                elif reveal == 1:
                    type.type("It's a person. A man, elderly, with a shotgun. He squints at you.")
                    print("\n")
                    type.type(quote("This is private property. Road's that way. Don't come back."))
                    print("\n")
                else:
                    type.type("It's a wooden post with old clothes hanging from it. Not a person at all.")
                    print("\n")
            else:
                type.type("You decide not to risk it. You turn and walk back the way you came.")
                print("\n")
        elif random_chance == 1:
            type.type("Your foot catches on something hidden in the grass - a battered duffle bag.")
            print("\n")
            type.type("Do you open it?")
            answer = ask.yes_or_no()
            if answer == "yes":
                outcome = random.randrange(3)
                if outcome == 0:
                    worth = random.randint(300, 800)
                    type.type("Inside: bundles of cash. You pocket " + green(bright("$" + str(worth))) + ".")
                    self.change_balance(worth)
                    print("\n")
                elif outcome == 1:
                    type.type("Inside: old clothes and a photograph of a family you don't recognize. You leave it.")
                    print("\n")
                else:
                    type.type("Wasps pour out in an angry swarm. You sprint through the field, getting stung.")
                    self.hurt(random.randint(10, 20))
                    print("\n")
            else:
                type.type("You leave the bag alone. Nothing good ever came from opening mysterious bags.")
                print("\n")
        elif random_chance == 2:
            type.type("You stumble upon an abandoned campsite. A collapsed tent, empty beer cans, scattered belongings.")
            print("\n")
            type.type("Do you search it?")
            search = ask.yes_or_no()
            if search == "yes":
                find = random.randrange(3)
                if find == 0:
                    type.type("You find a cooler with some sodas still cold. You also pocket a rusty pocket knife.")
                    self.heal(random.randint(5, 15))
                    print("\n")
                elif find == 1:
                    type.type("As you're rummaging, you hear a click. A tripwire. Nothing happens, but you run anyway.")
                    print("\n")
                else:
                    worth = random.randint(50, 150)
                    type.type("You find a wallet with " + green(bright("$" + str(worth))) + " inside.")
                    self.change_balance(worth)
                    print("\n")
            else:
                type.type("You leave the campsite undisturbed. Some places are better left alone.")
                print("\n")
        else:
            type.type("You walk through the field until it gives way to a dirt road. The stars are coming out.")
            print("\n")
            type.type("You follow the road back to your wagon, feeling small under the vast sky.")
            print("\n")

    def swamp_stroll(self):
        # EVENT: Explore a dangerous swamp with snakes, bodies, and a lonely banjo player
        # EFFECTS: Various - snake bite (15-30 damage + sanity loss), find money ($50-500), lose sanity from corpse, or uneventful
        self.meet("Swamp Stroll Event")
        type.type("After wandering from your vehicle, you find yourself at the edge of a swamp. ")
        type.type("The air is thick and humid, smelling of rot and growing things. ")
        type.type("Cypress trees rise from the murky water, draped in Spanish moss.")
        print("\n")
        random_chance = random.randrange(4)
        if random_chance == 0:
            type.type("A massive snake, thick as your arm, slithers across your path. It stops, coils, and watches you.")
            print("\n")
            
            # Animal Whistle befriends the snake
            if self.has_item("Animal Whistle") and not self.has_companion("Noodle"):
                type.type("The " + magenta(bright("Animal Whistle")) + " hums, low and steady. The snake's tongue flicks out, tasting the air.")
                print("\n")
                type.type("Slowly, the snake uncoils and approaches. You hold out your hand - terrifying, but somehow right.")
                print("\n")
                type.type("The snake slides up your arm, coiling gently around your shoulders. Warm. Smooth. Alive.")
                print("\n")
                type.type("You've just befriended a swamp serpent. You decide to call it " + cyan(bright("Noodle")) + ".")
                print("\n")
                type.type("Noodle will ride with you now, a living scarf that occasionally hisses at strangers.")
                self.add_companion("Noodle", "Snake")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                print("\n")
                return
            
            type.type("Do you try to go around it, or wait for it to move?")
            choice = input("(around/wait): ").strip().lower()
            if choice == "around":
                if random.random() < 0.6:
                    type.type("You give the snake a wide berth. It watches but doesn't strike. You make it past.")
                    print("\n")
                else:
                    type.type("The snake lunges. Fangs sink into your calf. You stumble away as it slithers off.")
                    self.hurt(random.randint(15, 30))
                    self.lose_sanity(random.choice([2, 3, 4]))  # Sudden violence is disturbing
                    print("\n")
            else:
                type.type("You stand perfectly still. After an eternity, the snake uncurls and slides into the water.")
                print("\n")
        elif random_chance == 1:
            type.type("You spot something pale floating in the water. At first you think it's a log, but then you see the fingers.")
            print("\n")
            type.type("It's a body. Face down, bloated. Do you search it?")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("You wade in and flip the body over. The face is... not something you want to remember.")
                self.lose_sanity(random.choice([3, 4, 5]))  # Dead body is traumatic
                print("\n")
                search_result = random.randrange(3)
                if search_result == 0:
                    worth = random.randint(200, 500)
                    type.type("You find a waterlogged wallet with " + green(bright("$" + str(worth))) + " inside.")
                    self.change_balance(worth)
                    print("\n")
                elif search_result == 1:
                    type.type("Something moves in the water nearby. A pair of eyes. Alligator. You back away slowly.")
                    print("\n")
                else:
                    type.type("The body has nothing of value. Just a dead man in a swamp.")
                    print("\n")
            else:
                type.type("You're not touching that. You find another path.")
                print("\n")
        elif random_chance == 2:
            type.type("You hear music. Faint, plucking strings. A banjo? Out here?")
            print("\n")
            type.type("You find an old man on a stump, playing a battered instrument. No teeth. Clothes more patches than fabric.")
            print("\n")
            type.type("He stops when he sees you. " + quote("Don't get many visitors out here."))
            print("\n")
            type.type("Do you sit and listen?")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("The music is haunting, beautiful. When he finishes, he hands you some crumpled bills.")
                print("\n")
                type.type(quote("For your company. Gets lonely out here."))
                worth = random.randint(50, 150)
                type.type("You pocket the " + green(bright("$" + str(worth))) + ".")
                self.change_balance(worth)
                print("\n")
            else:
                type.type(quote("Suit yourself.") + " He goes back to playing as you walk away.")
                print("\n")
        else:
            type.type("You wander the edge of the swamp, watching for gators. Nothing eventful happens.")
            print("\n")
            type.type("Eventually you find your way back to your wagon, mud caked on your shoes.")
            print("\n")

    # SUZY STORYLINE - CHEAP NIGHT
    def whats_my_favorite_color(self):
        # EVENT: Suzy asks your favorite color (Part 2 of Suzy storyline)
        # CONDITION: Must have met Suzy (know player name) AND favorite color not yet set
        # EFFECTS: Sets player's favorite color for Suzy finale; atmospheric character building
        # CHAIN: Suzy Storyline Part 2 of 3
        # Only triggers if Suzy has been met and favorite color not yet set
        if self._name == None or self.get_favorite_color() != None:
            self.night_event()
            return
        
        type.type("As you're sitting in your wagon, watching the sunset paint the sky in brilliant hues, ")
        type.type("you hear a familiar sound-sneakers scratching against concrete, accompanied by the rhythmic slap of a jump rope.")
        print("\n")
        type.type(quote("Hey! " + self._name + "! It's me, Suzy!"))
        print("\n")
        type.type("Suzy skips over to your window, pigtails bouncing, still jump roping in place.")
        print("\n")
        type.type(quote("I was just thinking about you! I have a SUPER important question. Ready?"))
        print("\n")
        type.type(quote("What's your favorite color?"))
        print("\n")
        
        color = str(input("Your favorite color: "))
        self.set_favorite_color(color)
        
        type.type(quote(color + "? That's a great color! That's like... the color of... um..."))
        print("\n")
        type.type("Suzy squints, thinking really hard.")
        print("\n")
        type.type(quote("The color of " + color + " things! Yeah! I knew that."))
        print("\n")
        type.type(quote("Okay, gotta go! The stars are coming out and mom says I shouldn't be out when it's dark. "))
        type.type(quote("Even though she's not here to tell me that anymore. Bye " + self._name + "!"))
        print("\n")
        type.type("Suzy continues jump roping down the road, disappearing into the twilight.")
        print("\n")

    # RABBIT CHASE CHAIN - CHEAP NIGHT
    def chase_the_second_rabbit(self):
        # EVENT: Rabbit Chase Part 2 - Chase the white rabbit again (still fails)
        # CONDITION: Rabbit chase counter must be 1 (first chase complete)
        # EFFECTS: Chase fails again, rabbit seems to be playing with you; advances rabbit chase counter
        # CHAIN: Rabbit Chase Part 2 of 4
        # Second rabbit chase - still fails
        if self.get_rabbit_chase() != 1:
            self.night_event()
            return
        
        type.type("There it is again. That same white rabbit, sitting in the middle of the road, watching you with those beady little eyes.")
        print("\n")
        type.type(quote("You again!") + " you mutter, already breaking into a run.")
        print("\n")
        type.type("The rabbit springs away, leading you on another wild chase through the brush. ")
        type.type("This time, you're determined. You've learned its tricks. You anticipate its zigs and zags.")
        print("\n")
        type.type("But still, every time you get close enough to grab it, it slips away. It's almost like it's playing with you.")
        print("\n")
        type.type("Once again, you end up empty-handed, watching the rabbit disappear into a thicket. It almost looks like it's... laughing?")
        print("\n")
        type.type(yellow("You return to your wagon, once again defeated. But you're not giving up. Not yet."))
        self.advance_rabbit_chase()
        print("\n")
   
    # Modest Nights (10,000 - 100,000)
    # Everytime
    def swamp_wade(self):
        # EVENT: Wade through a dangerous swamp with leeches, magical nectar, witch encounters, and sunken rowboats
        # EFFECTS: Various - leech damage (5-20), Granny's Swamp Nectar healing/damage, witch blessings/curses, money ($200-600), sanity loss from corpse
        self.meet("Swamp Wade Event")
        type.type("You wade waist-deep through the swamp, the water cold and thick with silt. ")
        type.type("Every step is a struggle, and unseen things brush against your legs. ")
        type.type("The air is heavy with the scent of decay and blooming lilies. ")
        type.type("Fireflies blink in the darkness like tiny green stars.")
        print("\n")
        # ITEM: Storm Suit - swamp weather immunity, wade through unharmed
        if self.has_item("Storm Suit"):
            type.type("The " + magenta(bright("Storm Suit")) + " seals around you perfectly. Nothing gets in. Not the water, not the chill, not the leeches.")
            print("\n")
            type.type("You wade through the swamp like it's a shopping mall. Confident. Dry. Mildly overdressed.")
            print("\n")
            type.type("On the far bank you find a waterlogged bag that some unlucky soul must have dropped. You open it.")
            print("\n")
            found = random.randint(80, 200)
            type.type("Inside: " + green(bright("$" + str(found))) + " in damp but spendable bills, and a sense of supreme competence.")
            self.change_balance(found)
            self.restore_sanity(6)
            print("\n")
            return
        event = random.choice(["leech", "nectar", "witch", "rowboat", "none"])
        if event == "leech":
            type.type("Something latches onto your leg. Then another. And another. LEECHES.")
            print("\n")
            type.type("Do you try to pull them off, or burn them off with your lighter?")
            choice = input("(pull/burn): ").strip().lower()
            if choice == "burn":
                type.type("You flick your lighter and hold it near your skin. The leeches squirm and drop off one by one, but you burn yourself in the process.")
                print("\n")
                self.hurt(random.randint(5, 10))
                type.type("At least you got them all. The welts itch for days.")
            else:
                type.type("You rip them off one by one, gagging. Each one takes a little chunk of you with it.")
                print("\n")
                self.hurt(random.randint(10, 20))
                type.type("You check yourself obsessively for hours afterwards. You HATE leeches.")
            print("\n")
        elif event == "nectar":
            type.type("Your foot kicks something solid in the murky water. ")
            type.type("You reach down and pull up an old mason jar, sealed tight. ")
            type.type("Inside is a thick, golden liquid - honey? Some kind of moonshine?")
            print("\n")
            type.type("The label is faded but you can make out: 'Granny's Swamp Nectar - For What Ails Ya'")
            print("\n")
            type.type("Do you drink it, save it, or toss it?")
            choice = input("(drink/save/toss): ").strip().lower()
            if choice == "drink":
                outcome = random.randrange(3)
                if outcome == 0:
                    type.type("It tastes like honey and gasoline. Your throat burns, but then... warmth spreads through your body. You feel incredible.")
                    self.heal(random.randint(25, 50))
                    print("\n")
                elif outcome == 1:
                    type.type("It's just honey. Really old, fermented honey. You feel a pleasant buzz and your cuts seem to heal faster.")
                    self.heal(random.randint(10, 25))
                    print("\n")
                else:
                    type.type("You gag and spit it out. That was NOT honey. You spend the next hour doubled over in the reeds.")
                    self.hurt(random.randint(5, 15))
                    print("\n")
            elif choice == "save":
                type.type("You pocket the jar. Could be useful. Could be poison. Only one way to find out, and it won't be tonight.")
                self.add_item("Granny's Swamp Nectar")
                print("\n")
            else:
                type.type("You toss it back into the swamp. Some things are better left unknown.")
                print("\n")
        elif event == "witch":
            type.type("A small wooden shack emerges from the fog, perched on stilts above the waterline. ")
            type.type("Candles flicker in the window, and hanging from the porch are bundles of dried herbs, animal bones, ")
            type.type("and what looks disturbingly like human teeth.")
            print("\n")
            type.type("A woman's voice calls out: " + quote("I know you're out there, sugar. Come on up. The water ain't safe at night."))
            print("\n")
            type.type("Do you approach the witch's shack?")
            choice = ask.yes_or_no()
            if choice == "yes":
                if not self.has_met("Witch"):
                    self.meet("Witch")
                type.type("You climb the rickety ladder. The witch is ancient, her skin like dried leather, but her eyes are sharp and knowing. ")
                type.type("She's stirring a pot that smells like... chicken soup?")
                print("\n")
                type.type(quote("Sit. Eat. Then we'll talk about what you owe me."))
                print("\n")
                type.type("Do you eat her soup?")
                eat = ask.yes_or_no()
                if eat == "yes":
                    self.heal(random.randint(15, 30))
                    type.type("The soup is delicious. Best thing you've eaten in weeks. The witch watches you with a crooked smile.")
                    print("\n")
                    type.type(quote("Now, for payment. Give me something interesting, or I'll take something interesting."))
                    print("\n")
                    fate = random.choice(["blessing", "curse", "riddle"])
                    if fate == "blessing":
                        type.type("You empty your pockets - lint, a button, a few coins. She plucks a single hair from your head.")
                        print("\n")
                        type.type(quote("This'll do. Now get. And don't die out there. I hate wasted meals."))
                        print("\n")
                        type.type("You feel oddly... lucky.")
                        self.add_status("Witch's Blessing")
                    elif fate == "curse":
                        type.type("She takes a button from your shirt and bites it, then spits into her pot.")
                        print("\n")
                        type.type(quote("Mm. You've got a darkness in you. We'll meet again."))
                        print("\n")
                        type.type("A chill runs down your spine that doesn't go away.")
                        self.add_status("Marked")
                    else:
                        type.type("She hands you a folded paper with strange symbols.")
                        print("\n")
                        type.type(quote("You'll know when you need this. Maybe. If you're clever."))
                        self.add_item("Witch's Riddle")
                else:
                    type.type("You politely decline. The witch's eyes narrow.")
                    print("\n")
                    type.type(quote("Suit yourself. Get out. And watch the water - the gators are hungry tonight."))
            else:
                type.type("You wade past quickly, pretending you didn't hear anything. The candlelight follows you for an uncomfortably long time.")
                print("\n")
        elif event == "rowboat":
            type.type("You nearly trip over something beneath the surface - the edge of a sunken rowboat, half-buried in the muck.")
            print("\n")
            type.type("Do you try to pull it up and search it?")
            search = ask.yes_or_no()
            if search == "yes":
                type.type("You wrestle the rotting boat to the surface. Inside, tangled in algae and crawfish, you find...")
                print("\n")
                find = random.randrange(4)
                if find == 0:
                    worth = random.randint(200, 600)
                    type.type("A waterproof pouch with cash inside. " + green(bright("$" + str(worth))) + ". Someone's emergency fund, now yours.")
                    self.change_balance(worth)
                elif find == 1:
                    type.type("A rusted tackle box full of fishing lures. Worthless to you, but you pocket a pretty one anyway.")
                    self.add_item("Lucky Lure")
                elif find == 2:
                    type.type("A skeleton. An actual human skeleton, grinning up at you. You scramble backwards, nearly drowning.")
                    self.lose_sanity(random.choice([2, 3, 4]))  # Finding human remains
                    print("\n")
                    type.type("In its bony hand is a watch that still ticks. You don't take it. Some things are cursed.")
                else:
                    type.type("Nothing but rot, mud, and a family of very angry crawfish. One pinches your finger hard enough to draw blood.")
                    self.hurt(random.randint(3, 8))
                print("\n")
            else:
                type.type("You leave the boat where it lies. Some secrets are better left at the bottom of the swamp.")
                print("\n")
        else:
            type.type("You make it through, muddy but unharmed. A bullfrog croaks somewhere in the darkness, like it's laughing at you. The swamp keeps its secrets tonight.")
        print("\n")

    def swamp_swim(self):
        # EVENT: Dive into deep swamp waters with alligator encounters, treasure, witch, and fishing shack
        # EFFECTS: Various - alligator attack (15-50 damage + major sanity loss), treasure ($800-2500), witch charms, Gator Tooth Necklace protects from gators
        self.meet("Swamp Swim Event")
        type.type("You dive into the deeper waters of the swamp, the murky green closing over your head. ")
        type.type("Down here, the world is muffled and strange. Catfish scatter at your approach. ")
        type.type("Something large moves in the shadows - probably just a log. Probably.")
        print("\n")
        
        event = random.choice(["alligator", "treasure", "witch", "fishing_shack", "none"])
        if event == "alligator":
            # Animal Whistle automatically befriends the gator
            if self.has_item("Animal Whistle") and not self.has_companion("Chomper"):
                type.type("You surface for air and find yourself face-to-face with a pair of ancient, unblinking eyes. An alligator. At least ten feet long.")
                print("\n")
                type.type("The " + magenta(bright("Animal Whistle")) + " hums from your pocket. The water itself seems to vibrate with the tone.")
                print("\n")
                type.type("The gator's eyes soften. It swims closer, then gently bumps its massive snout against your arm - like a dog asking for pets.")
                print("\n")
                type.type("You reach out and run your hand along its ancient, armored head. It rumbles contentedly, a sound like distant thunder.")
                print("\n")
                type.type("The gator has chosen you. You decide to call it " + cyan(bright("Chomper")) + ".")
                print("\n")
                type.type("Chomper follows you back to shore and settles near your wagon like a prehistoric guard dog.")
                self.add_companion("Chomper", "Alligator")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                print("\n")
                return
            # Gator Tooth Necklace makes gators respect you
            elif self.has_item("Gator Tooth Necklace"):
                type.type("You surface for air and find yourself face-to-face with a pair of ancient, unblinking eyes. An alligator. At least ten feet long.")
                print("\n")
                type.type("But then it sees your necklace - teeth from one of its own. It lets out a low rumble... and slowly backs away.")
                type.type(" The swamp creatures know who you are now. They won't bother you.")
                print("\n")
                self.restore_sanity(10)
                self.add_status("Swamp Respected")
            else:
                type.type("You surface for air and find yourself face-to-face with a pair of ancient, unblinking eyes. An alligator. At least ten feet long. Neither of you moves.")
                print("\n")
                type.type("What do you do?")
                choice = input("(freeze/splash/swim): ").strip().lower()
                
                if choice == "freeze":
                    type.type("You float perfectly still, heart hammering, as the gator drifts closer. Its snout brushes your arm. You don't breathe.")
                    print("\n")
                    if random.randrange(100) < 65:  # 65% chance
                        type.type("After an eternity, it loses interest and glides away into the murk. You don't move for another five minutes.")
                        print("\n")
                    else:
                        type.type("It lunges. You thrash backwards, but not fast enough. Its jaws graze your leg as you scramble for shore.")
                        self.hurt(random.randint(15, 35))
                        self.lose_sanity(random.choice([3, 4, 5]))  # Prehistoric terror
                        print("\n")
                elif choice == "splash":
                    type.type("You slap the water hard, trying to scare it off. The gator startles - ")
                    if random.randrange(100) < 50:  # 50% chance
                        type.type("and retreats! It sinks beneath the surface and disappears. You swim for shore like your life depends on it. Because it does.")
                        print("\n")
                    else:
                        type.type("but it's not scared, it's ANGRY. It surges at you, jaws snapping. You barely escape, bleeding from a dozen cuts.")
                        self.hurt(random.randint(25, 45))
                        self.lose_sanity(random.choice([4, 5, 6]))  # Nearly eaten alive
                        print("\n")
                else:
                    type.type("You swim for it, arms and legs pumping. The gator follows, impossibly fast - ")
                    if random.randrange(100) < 40:  # 40% chance
                        type.type("but you reach the shallows first. You claw up onto solid ground, gasping. The gator watches from the water, patient. It'll be there next time.")
                        print("\n")
                    else:
                        type.type("and catches your ankle. You kick free, but it's already torn through your boot and into skin. You make it to shore, but you're bleeding badly.")
                        self.hurt(random.randint(30, 50))
                        self.lose_sanity(random.choice([5, 6, 7]))  # Death grip terror
                        print("\n")
        elif event == "treasure":
            type.type("Your foot touches something metallic on the bottom. You dive down and pull up a lockbox, heavy and crusted with mud. The lock is rusted but intact.")
            print("\n")
            type.type("Do you try to force it open, or take it with you?")
            choice = input("(force/take): ").strip().lower()
            if choice == "force":
                type.type("You find a rock and bash at the lock. It takes a while, but finally it gives.")
                print("\n")
                outcome = random.randrange(4)
                if outcome == 0:
                    worth = random.randint(800, 2500)
                    type.type("CASH. Wet, moldy cash, but cash. " + green(bright("$" + str(worth))) + " worth.")
                    self.change_balance(worth)
                elif outcome == 1:
                    type.type("Old photographs and letters, ruined by water damage. Someone's memories, lost forever. You say a quiet word and let the water take them back.")
                elif outcome == 2:
                    type.type("A gun. Probably dropped here on purpose by someone who didn't want it found. You leave it where it is. You don't need those kinds of problems.")
                else:
                    type.type("Gold jewelry - a wedding band, a bracelet, a locket with a faded photo inside. You feel weird taking it, but you do.")
                    self.add_item("Swamp Gold")
                print("\n")
            else:
                type.type("You tuck the lockbox under your arm. You'll open it later, somewhere dry, where you can take your time.")
                self.add_item("Mysterious Lockbox")
                print("\n")
        elif event == "witch":
            type.type("A small boat drifts out of the fog - a pirogue, poled by a figure in a hooded cloak. ")
            type.type("The witch of the swamp. She stops next to you, looking down with eyes that have seen too much.")
            print("\n")
            type.type(quote("You're far from shore, child. Looking for something?"))
            print("\n")
            type.type("Do you ask her for help, ask her what she's selling, or swim away?")
            choice = input("(help/buy/swim): ").strip().lower()
            if choice == "help":
                if not self.has_met("Witch"):
                    self.meet("Witch")
                type.type(quote("Help don't come free in these waters. But I like your face. Grab on."))
                print("\n")
                type.type("She pulls you into her boat and poles you to shore. As you climb out, she hands you something - a small bundle of herbs tied with red string.")
                print("\n")
                type.type(quote("For protection. You'll need it."))
                self.add_item("Witch's Ward")
                print("\n")
            elif choice == "buy":
                if not self.has_met("Witch"):
                    self.meet("Witch")
                type.type("She grins, revealing teeth filed to points.")
                print("\n")
                type.type(quote("I sell charms. Luck, love, revenge. What's your poison?"))
                print("\n")
                type.type("Do you buy a luck charm, a love charm, or a revenge charm?")
                charm = input("(luck/love/revenge): ").strip().lower()
                cost = random.randint(100, 400)
                if self.get_balance() >= cost:
                    self.change_balance(-cost)
                    if charm == "luck":
                        type.type("She ties a rabbit's foot around your wrist. You feel the swamp's favor settle on you.")
                        self.add_status("Swamp Lucky")
                    elif charm == "love":
                        type.type("She gives you a vial of something pink. " + quote("Put it in their drink. Don't blame me for what happens."))
                        self.add_item("Love Potion")
                    else:
                        type.type("She hands you a small wax doll. " + quote("You know what to do with this. Don't come crying when it works."))
                        self.add_item("Voodoo Doll")
                    print("\n")
                else:
                    type.type(quote("You can't afford my prices, sugar. Maybe next time."))
                    print("\n")
            else:
                type.type("You start swimming away. Her laughter follows you, echoing off the cypress trees.")
                print("\n")
                type.type(quote("Swim fast, child. The gators are hungry tonight."))
                print("\n")
        elif event == "fishing_shack":
            type.type("You spot a fishing shack on stilts, half-collapsed into the water. It looks abandoned, but there's a light inside.")
            print("\n")
            type.type("Do you swim over to investigate?")
            investigate = ask.yes_or_no()
            if investigate == "yes":
                type.type("You pull yourself onto the rickety porch. Inside, you find an old man drinking from a mason jar, a fishing pole propped against the wall.")
                print("\n")
                type.type(quote("Well hell, didn't expect visitors. Come in, come in. Name's Earl. Want some 'shine?"))
                print("\n")
                drink = ask.yes_or_no("Accept Earl's moonshine?")
                if drink == "yes":
                    type.type("The moonshine hits you like a freight train. Your eyes water. Your chest burns. But you feel... alive.")
                    self.heal(random.randint(10, 25))
                    print("\n")
                    type.type("Earl laughs and slaps your back. " + quote("You're alright, stranger. Here, take this."))
                    print("\n")
                    gift = random.choice(["money", "lure", "tip"])
                    if gift == "money":
                        worth = random.randint(100, 300)
                        type.type("He hands you some crumpled bills. " + green(bright("$" + str(worth))) + ".")
                        self.change_balance(worth)
                    elif gift == "lure":
                        type.type("He gives you his lucky fishing lure. " + quote("Caught a 50-pound catfish with that. Swear to God."))
                        self.add_item("Earl's Lucky Lure")
                    else:
                        type.type(quote("Stay away from the north end of the swamp. Something ain't right there. Something... wrong."))
                else:
                    type.type("Earl shrugs. " + quote("Suit yourself. More for me.") + " He goes back to his drinking, and you slip back into the water.")
                print("\n")
            else:
                type.type("You swim past. Some places are best left alone.")
                print("\n")
        else:
            type.type("You swim back, heart pounding, but nothing happens. The swamp keeps its secrets tonight. ")
            type.type("You emerge covered in algae and duck weed, smelling like something died. ")
            type.type("Which, in this swamp, something probably did.")
        print("\n")

    def beach_stroll(self):
        self.meet("Beach Stroll Event")
        type.type("You walk along the shoreline at dusk, the sand cool beneath your feet. ")
        type.type("The ocean stretches out forever, dark and restless under the fading sky. ")
        type.type("Seagulls cry in the distance. The salt air fills your lungs.")
        print("\n")
        random_chance = random.randrange(4)
        if random_chance == 0:
            type.type("You spot something in the wet sand ahead. As you get closer, you realize it's a person - lying face down at the waterline, waves lapping at their legs.")
            print("\n")
            type.type("Do you check on them?")
            answer = ask.yes_or_no()
            if answer == "yes":
                outcome = random.randrange(3)
                if outcome == 0:
                    type.type("You roll them over. They're alive - barely. A tourist who got caught in a riptide, from the looks of it. They cough up seawater and grab your arm.")
                    print("\n")
                    type.type(quote("Thank you... thank you...") + " They press something into your hand - a soggy wallet.")
                    print("\n")
                    type.type(quote("Take it. I don't care. You saved my life."))
                    worth = random.randint(100, 300)
                    type.type("Inside is " + green(bright("$" + str(worth))) + ". You help them to their feet and point them toward the boardwalk.")
                    self.change_balance(worth)
                    print("\n")
                elif outcome == 1:
                    type.type("They're dead. Have been for a while, from the look of them. Drowned, probably. The ocean took them and then gave them back.")
                    self.lose_sanity(random.choice([2, 3, 4]))  # Finding a corpse
                    print("\n")
                    type.type("You check their pockets - nothing. You leave the body where it lies. Someone else will find it.")
                    print("\n")
                else:
                    type.type("They're alive, and VERY drunk. They sit up, blinking at you, then start laughing.")
                    print("\n")
                    type.type(quote("Oh man... I thought I was dying! Just taking a nap, friend!"))
                    print("\n")
                    type.type("They stumble off toward the boardwalk, still laughing. Some people.")
                    print("\n")
            else:
                type.type("You walk past without stopping. Probably just a drunk sleeping it off. Not your problem either way.")
                print("\n")
        elif random_chance == 1:
            type.type("A hunched figure is walking along the tideline ahead of you, picking things up and putting them in a bucket. An old man, collecting shells.")
            print("\n")
            type.type("As you pass, he looks up at you. " + quote("Help an old man fill his bucket? I'll make it worth your while."))
            print("\n")
            type.type("Do you help him collect shells?")
            answer = ask.yes_or_no()
            if answer == "yes":
                type.type("You spend the next half hour walking the beach with the old man, picking up shells and listening to his stories. ")
                type.type("He used to be a fisherman, he says. Forty years on the water.")
                print("\n")
                type.type("When his bucket is full, he hands you some crumpled bills.")
                print("\n")
                type.type(quote("For your time. Gets lonely out here."))
                worth = random.randint(50, 150)
                type.type("You pocket the " + green(bright("$" + str(worth))) + " and say goodbye.")
                self.change_balance(worth)
                print("\n")
            else:
                type.type(quote("Suit yourself.") + " The old man goes back to his shells, and you continue down the beach, alone.")
                print("\n")
        elif random_chance == 2:
            type.type("You find a bonfire up ahead, surrounded by a group of teenagers drinking beer and playing music too loud. One of them waves you over.")
            print("\n")
            type.type(quote("Hey! Come hang out!"))
            print("\n")
            type.type("Do you join them?")
            answer = ask.yes_or_no()
            if answer == "yes":
                if random.random() < 0.6:
                    type.type("You sit by the fire for a while, sharing a beer. They're just kids, really. Enjoying the summer.")
                    print("\n")
                    type.type("When you leave, you feel a little lighter. Sometimes human connection is all you need.")
                    self.heal(random.randint(5, 15))
                    print("\n")
                else:
                    type.type("One of them starts asking too many questions. Where you're from. What you do. Where you're staying. You make an excuse and leave quickly.")
                    print("\n")
            else:
                type.type("You wave and keep walking. You're not in the mood for company tonight.")
                print("\n")
        else:
            type.type("You walk the beach until the sun disappears completely. The stars come out over the water.")
            print("\n")
            type.type("Eventually you head back to your wagon, sand in your shoes and salt on your skin.")
            print("\n")

    # RABBIT CHASE CHAIN - MODEST NIGHT
    def chase_the_third_rabbit(self):
        # Third rabbit chase - small chance to catch, can use carrot
        if self.get_rabbit_chase() != 2:
            self.night_event()
            return
        
        type.type("You're starting to think you're going crazy. Because there, sitting on a rock in the moonlight, is that same white rabbit. Again.")
        print("\n")
        type.type("It twitches its nose at you, almost daring you to try.")
        print("\n")
        
        # Animal Whistle can befriend the magical rabbit
        if self.has_item("Animal Whistle") and not self.has_companion("Moonwhisker"):
            type.type("The " + magenta(bright("Animal Whistle")) + " begins to glow with an ethereal light.")
            print("\n")
            type.type("The rabbit's ears perk up. Its eyes, which were red, suddenly flash with iridescent colors.")
            print("\n")
            type.type("This is no ordinary rabbit. This is a creature of magic and moonlight.")
            print("\n")
            type.type("The rabbit hops toward you, not fleeing for once. It circles you three times, leaving a trail of shimmering sparkles.")
            print("\n")
            type.type("Then it poops - but instead of coins, it poops a small glowing crystal. A " + magenta(bright("Moon Shard")) + ".")
            print("\n")
            type.type("The rabbit... smiles? Do rabbits smile? This one does. It hops onto your shoulder.")
            print("\n")
            type.type("You've befriended a magical moon rabbit. You call it " + cyan(bright("Moonwhisker")) + ".")
            print("\n")
            self.add_companion("Moonwhisker", "Moon Rabbit")
            self.add_item("Moon Shard")
            self.restore_sanity(12)
            self.increment_statistic("companions_befriended")
            self.unlock_achievement("first_friend")
            self.advance_rabbit_chase()
            print("\n")
            return
        
        if self.has_item("Carrot"):
            type.type("Wait. You have a " + magenta(bright("Carrot")) + " in your pocket. Maybe you can lure it?")
            print("\n")
            use_carrot = ask.yes_or_no("Use the carrot to lure the rabbit?")
            if use_carrot == "yes":
                self.use_item("Carrot")
                catch_chance = random.randrange(3)  # 33% chance with carrot
                if catch_chance == 0:
                    type.type("You hold out the carrot, and incredibly, the rabbit hops over. It nibbles on the carrot, and you slowly reach down... and GRAB it!")
                    print("\n")
                    type.type(green(bright("You caught the rabbit!")))
                    print("\n")
                    type.type("The rabbit squeaks in surprise. Then, something magical happens. It poops out a handful of coins, and in a flash of sparkles, disappears into thin air.")
                    print("\n")
                    coins = random.randint(500, 2000)
                    type.type("You're left holding " + green(bright("$" + str(coins))) + " and wondering what just happened.")
                    self.change_balance(coins)
                    self.advance_rabbit_chase()
                    self.meet("Caught Rabbit")
                    return
                else:
                    type.type("The rabbit takes one bite of the carrot, then bolts, taking your carrot with it!")
                    print("\n")
                    type.type(yellow("Well, that was a waste of a perfectly good carrot."))
                    self.advance_rabbit_chase()
                    print("\n")
                    return
        
        type.type("You give chase once more. This time, you get close. SO close. Your fingers brush its fur...")
        print("\n")
        
        catch_chance = random.randrange(10)  # 10% chance without carrot
        if catch_chance == 0:
            type.type(green(bright("GOT IT!")))
            print("\n")
            type.type("The rabbit squeaks in your hands. Then, something magical happens. It poops out a handful of coins, and in a flash of sparkles, disappears into thin air.")
            print("\n")
            coins = random.randint(500, 2000)
            type.type("You're left holding " + green(bright("$" + str(coins))) + " and wondering what just happened.")
            self.change_balance(coins)
            self.meet("Caught Rabbit")
        else:
            type.type("...but it slips away yet again. You swear that rabbit is supernatural.")
            print("\n")
            type.type(yellow("The hunt continues. You WILL catch that rabbit. Eventually."))
        
        self.advance_rabbit_chase()
        print("\n")
        
    # Rich Nights (100,000 - 500,000)
    def beach_swim(self):
        self.meet("Beach Swim Event")
        type.type("You wade into the ocean at night, the water black and endless. ")
        type.type("The waves push and pull at your body. Above you, the stars are scattered across the sky like spilled salt. ")
        type.type("Bioluminescence glows blue-green around your feet with each step.")
        print("\n")
        random_chance = random.randrange(5)
        if random_chance == 0:
            type.type("A sudden, searing pain wraps around your leg - jellyfish. The tentacles burn like fire as you thrash toward shore.")
            print("\n")
            type.type("Do you try to tough it out in the water, or scramble for the beach?")
            print("\n")
            choice = input("(tough/beach): ").strip().lower()
            if choice == "tough":
                if random.random() < 0.4:
                    type.type("You grit your teeth and keep swimming, the pain slowly fading to a dull throb. Mind over matter.")
                    print("\n")
                    type.type("When you finally walk out of the water, the welts are already rising on your skin, but you feel oddly proud of yourself.")
                    print("\n")
                else:
                    type.type("The pain gets worse, not better. You barely make it to shore before collapsing, your leg on fire.")
                    print("\n")
                    self.hurt(random.randint(15, 30))
                    type.type("You lie on the sand, gasping, waiting for the burning to stop. It takes a long time.")
                    print("\n")
            else:
                type.type("You splash frantically for shore, the jellyfish still wrapped around your calf. You rip it off and hurl it back into the water.")
                print("\n")
                self.hurt(random.randint(10, 20))
                type.type("The sting leaves angry red welts, but at least you're out of the water. You find some wet sand and pack it on. Old fisherman's trick.")
                print("\n")
        elif random_chance == 1:
            type.type("You float on your back, letting the waves rock you gently. The stars wheel overhead. ")
            type.type("For a few minutes, you forget everything - the wagon, the gambling, the debt, all of it.")
            print("\n")
            type.type("A shooting star streaks across the sky. You make a wish without thinking.")
            print("\n")
            type.type("When you finally swim back to shore, you feel... peaceful. Centered. Like maybe things will be okay.")
            print("\n")
            self.heal(random.randint(20, 35))
            self.add_status("At Peace")
            self.restore_sanity(random.choice([2, 3, 4]))  # Restores sanity
        elif random_chance == 2:
            type.type("A current catches you, stronger than you expected. The undertow pulls at your legs, dragging you away from shore. The beach lights grow smaller.")
            print("\n")
            type.type("Do you fight the current directly, swim parallel to the beach, or relax and float?")
            print("\n")
            choice = input("(fight/parallel/float): ").strip().lower()
            if choice == "parallel":
                type.type("You remember some old advice and swim sideways, parallel to the beach. Slowly, the current releases you, and you make your way back to shore.")
                print("\n")
                type.type("Smart thinking. Fighting a riptide is how people drown.")
                print("\n")
            elif choice == "float":
                type.type("You force yourself to relax, letting the current carry you. Eventually, it weakens, and you're able to swim back at an angle.")
                print("\n")
                type.type("Calm saved your life. Panic kills people in the ocean.")
                print("\n")
            else:
                if random.random() < 0.3:
                    type.type("You fight like hell, arms burning, lungs screaming. Somehow, you make it back to shore.")
                    print("\n")
                    self.hurt(random.randint(10, 20))
                    type.type("You collapse on the sand, exhausted. That was too close.")
                    print("\n")
                else:
                    type.type("The current is too strong. You're swept down the beach, tumbling in the waves, before finally washing up on shore a hundred yards from where you started.")
                    print("\n")
                    self.hurt(random.randint(20, 35))
                    self.lose_sanity(random.choice([3, 4, 5]))  # Near-death experience
                    type.type("You lie there, coughing up seawater, feeling like you almost died. Because you almost did.")
                    print("\n")
        elif random_chance == 3:
            type.type("Something brushes against your leg in the darkness. Then again. Then something GRABS your ankle.")
            print("\n")
            type.type("You kick wildly - and your foot connects with something that squeaks and lets go. A sea otter surfaces, looking offended.")
            print("\n")
            
            # Animal Whistle befriends the sea otter
            if self.has_item("Animal Whistle") and not self.has_companion("Scooter"):
                type.type("The " + magenta(bright("Animal Whistle")) + " sings out across the water. The otter's expression changes.")
                print("\n")
                type.type("It paddles closer, curious now instead of offended. Then it rolls onto its back and floats there, waiting.")
                print("\n")
                type.type("You reach out and the otter takes your hand with its tiny paws. It chirps happily.")
                print("\n")
                type.type("You've befriended a sea otter. You decide to call it " + cyan(bright("Scooter")) + ".")
                print("\n")
                type.type("Scooter will follow your adventures now, occasionally bringing you shiny rocks and shellfish.")
                self.add_companion("Scooter", "Sea Otter")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                self.heal(random.randint(10, 20))
                print("\n")
                return
            
            type.type("It floats there, staring at you with its little hands folded on its chest, like you ruined its evening.")
            print("\n")
            type.type(quote("Sorry, buddy."))
            print("\n")
            type.type("The otter makes a chittering noise that sounds suspiciously like profanity, then swims away. You can't help but laugh.")
            self.heal(random.randint(5, 10))
            print("\n")
        else:
            type.type("You swim for a while, enjoying the cool water and the darkness. The moon rises over the water, turning the waves silver.")
            print("\n")
            type.type("You find a sandbar and stand there for a while, waist-deep in the ocean, feeling like the only person in the world.")
            print("\n")
            type.type("You dry off and head back to your wagon, smelling like salt and feeling cleaner than you have in days.")
            print("\n")

    def beach_dive(self):
        self.meet("Beach Dive Event")
        type.type("You dive beneath the waves, the world above disappearing into blue-green silence. ")
        type.type("Down here, the light filters through the water like something from a dream. ")
        type.type("The ocean floor is littered with shells, sand dollars, and the occasional piece of sea glass. ")
        type.type("A school of silver fish parts around you like a curtain.")
        print("\n")
        random_chance = random.randrange(5)
        if random_chance == 0:
            type.type("Your hand closes around something smooth and round, half-buried in the sand. You dig it out - an oyster, massive and ancient-looking, the size of your fist.")
            print("\n")
            type.type("Do you pry it open now, or save it for later?")
            choice = input("(open/save): ").strip().lower()
            if choice == "open":
                type.type("You surface and use a rock to crack it open. Inside...")
                print("\n")
                outcome = random.randrange(3)
                if outcome == 0:
                    type.type("A PEARL. Not perfect - lumpy, with a slight pink hue - but real. You can feel its weight, its worth.")
                    self.add_item("Pink Pearl")
                    type.type("This could be worth hundreds. Maybe more to the right buyer.")
                elif outcome == 1:
                    type.type("...nothing but oyster meat. You eat it raw, feeling like a pirate. It's actually pretty good.")
                    self.heal(random.randint(5, 10))
                else:
                    type.type("TWO pearls. Small, but matched. A pair. You grin like an idiot.")
                    self.add_item("Matched Pearls")
                print("\n")
            else:
                type.type("You tuck the oyster away. Patience. The pearl isn't going anywhere.")
                self.add_item("Giant Oyster")
                print("\n")
        elif random_chance == 1:
            type.type("You spot something metallic glinting in the sand below. You dive deeper, lungs burning, and your fingers close around a handle.")
            print("\n")
            type.type("It's a waterproof case, the kind divers use. Still sealed. Do you open it?")
            answer = ask.yes_or_no()
            if answer == "yes":
                outcome = random.randrange(4)
                if outcome == 0:
                    type.type("Inside is cash - a lot of it, wrapped in plastic. Someone's emergency fund, lost to the sea.")
                    worth = random.randint(800, 2000)
                    type.type("You count " + green(bright("$" + str(worth))) + ". Not bad for a swim.")
                    self.change_balance(worth)
                    print("\n")
                elif outcome == 1:
                    type.type("An underwater camera, still working. You scroll through the photos - vacation shots, a wedding proposal, a woman crying happy tears.")
                    print("\n")
                    type.type("There's an address on the case. Do you keep it or return it?")
                    keep = input("(keep/return): ").strip().lower()
                    if keep == "return":
                        type.type("You'll mail it back. It's the right thing to do.")
                        print("\n")
                        type.type("A few days later, a check arrives in the mail. " + green(bright("$500")) + " and a thank you note. 'These memories meant everything.'")
                        self.change_balance(500)
                    else:
                        type.type("You keep the camera. Nice piece of equipment. The memories on it aren't yours anyway.")
                        self.add_item("Underwater Camera")
                elif outcome == 2:
                    type.type("Inside is a rusted pistol and some soggy documents. Nothing useful, and probably evidence of something you don't want to know about.")
                    print("\n")
                    type.type("You toss it back into the deep water and swim away. Fast.")
                    print("\n")
                else:
                    type.type("The case is full of sand and a very confused hermit crab. It pinches you before scuttling away.")
                    self.hurt(random.randint(1, 3))
                    print("\n")
            else:
                type.type("You leave it where it is. Nothing good ever came from treasure found at the bottom of the ocean.")
                print("\n")
        elif random_chance == 2:
            type.type("A shadow passes over you. You look up and your blood runs cold - a shark, maybe six feet long, circling lazily above. ")
            type.type("A blacktip, from the look of it. Probably not a man-eater. Probably.")
            print("\n")
            type.type("Do you swim slowly to shore, stay completely still, or try to scare it off?")
            print("\n")
            choice = input("(swim/still/scare): ").strip().lower()
            if choice == "still":
                type.type("You freeze, barely breathing, watching the shark through the wavering water. It circles once, twice, then loses interest and glides away into the blue.")
                print("\n")
                type.type("You wait until you can't see it anymore, then swim to shore as calmly as you can manage. Your hands don't stop shaking for an hour.")
                print("\n")
            elif choice == "scare":
                type.type("You puff yourself up and make yourself look big, spreading your arms wide. The shark pauses, curious.")
                if random.random() < 0.6:
                    type.type("It decides you're not worth the trouble and swims off. You feel like a badass.")
                    print("\n")
                else:
                    type.type("It bumps you with its nose - testing. You punch it in the face. It swims away, annoyed. You swim away, terrified.")
                    self.hurt(random.randint(5, 10))
                    print("\n")
            else:
                if random.random() < 0.7:
                    type.type("You swim for shore with slow, deliberate strokes, trying not to splash. The shark follows for a moment, then veers off.")
                    print("\n")
                    type.type("You make it to the beach and collapse on the sand, heart pounding. Too close.")
                    print("\n")
                else:
                    type.type("The shark bumps you - testing, curious. You feel its rough skin scrape against your side. You thrash for shore, panic overwhelming caution.")
                    print("\n")
                    self.hurt(random.randint(15, 30))
                    type.type("You make it out, but your side is scraped raw. Could have been so much worse.")
                    print("\n")
        elif random_chance == 3:
            # Dolphin encounter
            type.type("A sudden movement catches your eye - something large, gliding through the water with effortless grace.")
            print("\n")
            type.type("A DOLPHIN. It circles you once, twice, clicking and chirping. Curious. Playful.")
            print("\n")
            
            # Animal Whistle can befriend the dolphin
            if self.has_item("Animal Whistle") and not self.has_companion("Echo"):
                type.type("The " + magenta(bright("Animal Whistle")) + " resonates underwater, creating ripples of sound.")
                print("\n")
                type.type("The dolphin's eyes widen. It chirps excitedly and begins circling you faster, swimming loops around your body.")
                print("\n")
                type.type("You reach out. The dolphin nudges your hand with its rostrum - gentle, intelligent, aware.")
                print("\n")
                type.type("This creature understands you. And you understand it.")
                print("\n")
                type.type("You surface together, and the dolphin leaps clear out of the water, spinning in the air before splashing back down.")
                print("\n")
                type.type("You've befriended a wild dolphin. You decide to call them " + cyan(bright("Echo")) + ".")
                print("\n")
                type.type("Echo will follow your wagon when you're near the coast, surfing in the waves alongside the road.")
                self.add_companion("Echo", "Dolphin")
                self.restore_sanity(15)
                self.heal(20)
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                print("\n")
                return
            
            type.type("You swim alongside it for a moment - a brief, magical connection. Then it dives deep and is gone.")
            print("\n")
            type.type("You float there, grinning like an idiot. You just swam with a dolphin. Life is amazing sometimes.")
            self.restore_sanity(12)
            self.heal(15)
            print("\n")
        
        elif random_chance == 4:
            type.type("You find a coral formation, alive with color and movement. ")
            type.type("Fish dart in and out of the crevices. An octopus watches you from its den, changing colors nervously.")
            print("\n")
            type.type("You float there, watching the reef ecosystem, until your lungs force you to surface. ")
            type.type("For a moment, you weren't a gambler living in a wagon. You were just... part of the ocean.")
            print("\n")
            self.heal(random.randint(10, 20))
            type.type("You feel connected to something bigger than yourself.")
            self.add_status("Ocean-Blessed")
            print("\n")
        else:
            type.type("You dive and explore for a while, finding nothing but shells and the occasional startled fish. A moray eel gives you the stink-eye from its hole.")
            print("\n")
            type.type("Eventually you surface and swim back to shore, tired but content. The underwater world is peaceful, alien, beautiful.")
            print("\n")

    def city_streets(self):
        self.meet("City Streets Event")
        type.type("You wander the city's labyrinth of neon and shadow, where every alley whispers a different story. ")
        type.type("The air is thick with exhaust, food cart smoke, and the promise of trouble. ")
        type.type("A pigeon watches you from a fire escape like it knows something you don't.")
        print("\n")
        event = random.choice(["drug_dealer", "stray_cat", "rent_bike", "food_cart", "busker", "none"])
        if event == "drug_dealer":
            type.type("A gaunt figure in a hoodie steps from a flickering doorway, eyes darting like a nervous bird. ")
            type.type(quote("Looking for a little edge?") + " he asks, holding out a small bag. The city seems to hold its breath.")
            print("\n")
            type.type("Do you accept, decline politely, or tell him to get lost?")
            choice = input("(accept/decline/scram): ").strip().lower()
            if choice == "accept":
                outcome = random.choice(["buff", "bad_trip", "police", "fake"])
                if outcome == "buff":
                    type.type("You slip the contents under your tongue. The world sharpens - colors brighter, sounds clearer. For a while, you feel invincible, your luck uncanny.")
                    self.add_status("Energized")
                elif outcome == "bad_trip":
                    type.type("Your heart races, the world tilts, and you stagger into the street. ")
                    type.type("You lose track of time - and some money. When you come to, your pockets are lighter and your head aches.")
                    self.hurt(random.randint(15, 30))
                    self.change_balance(-random.randint(200, 800))
                elif outcome == "police":
                    type.type("Suddenly, blue lights flash. " + quote("Police! Hands up!") + " You drop the bag and run, barely escaping. You lose some money in the chaos.")
                    self.change_balance(-random.randint(100, 400))
                else:
                    type.type("It's oregano. He sold you cooking herbs. You feel like an idiot, but at least you're not high.")
                print("\n")
            elif choice == "scram":
                type.type("You tell him where he can shove his product. He looks hurt, actually hurt, then slinks back into the shadows.")
                print("\n")
                type.type(quote("Man, you don't gotta be like that..."))
                print("\n")
            else:
                type.type("You shake your head and move on. The dealer shrugs and lights a cigarette, already looking for his next mark.")
                print("\n")
        elif event == "stray_cat":
            type.type("A scruffy, one-eyed cat weaves between your legs, meowing with a raspy voice like it's been smoking since kittenhood. ")
            type.type("Its fur is matted, but its gaze is sharp and knowing.")
            print("\n")
            type.type("Do you pet it, feed it (if you have food), or ignore it?")
            choice = input("(pet/feed/ignore): ").strip().lower()
            if choice == "pet":
                fate = random.choice(["lucky", "scratch", "ally", "fleas"])
                if fate == "lucky":
                    type.type("The cat purrs like a tiny motor, rubbing its head against your hand. ")
                    type.type("It leaves a whisker in your palm. You feel luckier, as if the city itself is watching over you.")
                    self.add_status("Street Lucky")
                elif fate == "scratch":
                    type.type("The cat hisses and claws your hand before darting away. You wince, blood trickling from the scratch. Typical.")
                    self.hurt(random.randint(3, 10))
                elif fate == "ally":
                    type.type("The cat follows you for blocks, scaring off a would-be pickpocket with a ferocious hiss. You gain a furry guardian for the night.")
                    self.add_item("Street Cat Ally")
                else:
                    type.type("The cat nuzzles you... and you immediately start itching. Fleas. Of course. You spend the next hour scratching.")
                    self.hurt(random.randint(2, 5))
                print("\n")
            elif choice == "feed":
                if self.has_item("Can of Tuna"):
                    type.type("You crack open your can of tuna. The cat goes WILD, purring and rubbing against you, then devouring the fish.")
                    self.use_item("Can of Tuna")
                    print("\n")
                    type.type("Other cats start appearing from everywhere - alleys, dumpsters, fire escapes. ")
                    type.type("Soon you're surrounded by a dozen grateful felines. You feel blessed by the street cat gods.")
                    self.add_status("Cat Whisperer")
                else:
                    type.type("You don't have any food. The cat gives you a disappointed look and walks away, tail high.")
                print("\n")
            else:
                type.type("You ignore the cat. It stares at your back as you walk away, judging you silently.")
                print("\n")
        elif event == "rent_bike":
            type.type("You spot a row of rental bikes, some more battered than others. The city traffic is a snarl of taxis and delivery trucks, but on two wheels, you could fly.")
            print("\n")
            type.type("Do you rent a nice one ($50), a cheap one ($20), or skip it?")
            choice = input("(nice/cheap/skip): ").strip().lower()
            if choice == "nice":
                if self.get_balance() >= 50:
                    self.change_balance(-50)
                    type.type("You pick the sleekest bike in the row. It rides like a dream, weaving through traffic like water through rocks.")
                    print("\n")
                    self.add_status("Refreshed")
                    type.type("You arrive at your destination exhilarated, wind-blown, and feeling alive.")
                else:
                    type.type("You don't have enough cash. The bike attendant shrugs sympathetically.")
                print("\n")
            elif choice == "cheap":
                if self.get_balance() >= 20:
                    self.change_balance(-20)
                    outcome = random.choice(["fine", "crash", "stolen"])
                    if outcome == "fine":
                        type.type("The bike squeaks and wobbles, but it gets you where you're going. Not elegant, but effective.")
                    elif outcome == "crash":
                        type.type("The brakes fail. You crash into a hot dog cart, sending wieners flying. You escape with bruises and mustard stains.")
                        self.hurt(random.randint(8, 18))
                    else:
                        type.type("You stop to rest, and when you turn around, some kid is pedaling away on YOUR bike. You don't even bother chasing.")
                else:
                    type.type("Even the cheap bike is too rich for your blood right now.")
                print("\n")
            else:
                type.type("You decide to walk. The city's rhythm sets your pace. Sometimes slow is safe.")
                print("\n")
        elif event == "food_cart":
            type.type("The smell hits you first - garlic, grease, something spicy. ")
            type.type("A food cart, wedged between a dumpster and a parked car, manned by a guy who looks like he hasn't slept in days.")
            print("\n")
            type.type(quote("Best gyro in the city. Five bucks. You want or no?"))
            print("\n")
            buy = ask.yes_or_no("Buy the gyro?")
            if buy == "yes":
                if self.get_balance() >= 5:
                    self.change_balance(-5)
                    outcome = random.randrange(3)
                    if outcome == 0:
                        type.type("It IS the best gyro in the city. Holy crap. The tzatziki sauce alone is life-changing. You feel restored.")
                        self.heal(random.randint(15, 30))
                    elif outcome == 1:
                        type.type("It's... fine. Food is food. You eat it standing on the curb, watching the city go by.")
                        self.heal(random.randint(5, 10))
                    else:
                        type.type("Something was NOT right with that lamb. You spend the next hour in a public bathroom, questioning your life choices.")
                        self.hurt(random.randint(10, 20))
                else:
                    type.type(quote("No money, no gyro. Come back when you got five bucks."))
            else:
                type.type(quote("Your loss, my friend. Your loss."))
            print("\n")
        elif event == "busker":
            type.type("A street musician plays saxophone under a flickering streetlight, the notes winding through the night air like smoke. ")
            type.type("A few people have stopped to listen. His case is open, a handful of coins inside.")
            print("\n")
            type.type("Do you stop to listen, tip him, or keep walking?")
            choice = input("(listen/tip/walk): ").strip().lower()
            if choice == "listen":
                type.type("You lean against a wall and let the music wash over you. ")
                type.type("It's jazz, slow and melancholy, the kind of song that makes you think about everyone you've ever lost.")
                print("\n")
                type.type("When it ends, you feel... lighter. Like you let something go.")
                self.heal(random.randint(5, 15))
                print("\n")
            elif choice == "tip":
                tip = random.randint(5, 20)
                if self.get_balance() >= tip:
                    self.change_balance(-tip)
                    type.type("You drop " + str(tip) + " bucks in his case. He nods at you, a silent thanks, and launches into an upbeat number just for you.")
                    print("\n")
                    type.type("You walk away feeling generous. It's a good feeling.")
                    self.add_status("Generous")
                else:
                    type.type("You pat your pockets apologetically. He winks and keeps playing anyway.")
                print("\n")
            else:
                type.type("You keep walking. The music fades behind you, replaced by car horns and distant sirens.")
                print("\n")
        else:
            type.type("Tonight, the city is just a city. Neon reflections in puddles. Distant laughter. The hum of a thousand lives you'll never know.")
            print("\n")
            type.type("You wander, lost in thought, until you find yourself back at your wagon, unsure how you got there.")
            print("\n")

    # SUZY STORYLINE - RICH NIGHT
    def whats_my_favorite_animal(self):
        # Only triggers if favorite color is set but favorite animal is not
        if self.get_favorite_color() == None or self.get_favorite_animal() != None:
            self.night_event()
            return
        
        type.type("The city lights are starting to dim as people head home for the night. ")
        type.type("But through the fading glow, you hear a sound that's become strangely comforting-")
        type.type("sneakers on concrete, a jump rope slapping the ground.")
        print("\n")
        type.type(quote(self._name + "! There you are! I've been looking EVERYWHERE for you!"))
        print("\n")
        type.type("Suzy bounces over, somehow still full of energy despite the late hour.")
        print("\n")
        type.type(quote("Okay okay okay, I have another question. This one's even MORE important than the color one."))
        print("\n")
        type.type("She stops jump roping for the first time you've ever seen, looking at you with complete seriousness.")
        print("\n")
        type.type(quote("What's your favorite animal?"))
        print("\n")
        
        animal = str(input("Your favorite animal: "))
        self.set_favorite_animal(animal)
        
        type.type(quote("A " + animal + "?! NO WAY! That's MY favorite animal too!"))
        print("\n")
        type.type("Suzy starts jumping up and down excitedly.")
        print("\n")
        type.type(quote("We're like... BEST FRIENDS now! " + animal + " buddies forever!"))
        print("\n")
        type.type(quote("Oh! I almost forgot! I made you something. But it's not done yet. I'll give it to you when I see you again, okay? PROMISE you'll be around?"))
        print("\n")
        answer = ask.yes_or_no("Do you promise?")
        if answer == "yes":
            type.type(quote("YAY! Okay! Pinky promise! Don't break it or you'll have bad luck FOREVER!"))
        else:
            type.type(quote("Hmm... well, I'll find you anyway. I'm REALLY good at finding people!"))
        print("\n")
        type.type("Suzy resumes jump roping and bounces off into the night, humming a tune you can't quite place.")
        print("\n")

    # RABBIT CHASE CHAIN - RICH NIGHT
    def chase_the_fourth_rabbit(self):
        # Fourth rabbit chase - another chance to catch
        if self.get_rabbit_chase() != 3 or self.has_met("Caught Rabbit"):
            self.night_event()
            return
        
        type.type("It's become a ritual at this point. You see the flash of white fur in your peripheral vision, and your legs start moving before your brain catches up.")
        print("\n")
        type.type("The rabbit leads you through the city streets this time, darting under parked cars and around corners. ")
        type.type("People stare at you chasing what they probably think is nothing.")
        print("\n")
        type.type("Finally, you corner it in an alley. There's nowhere for it to go.")
        print("\n")
        type.type(quote("Got you now, you little..."))
        print("\n")
        
        catch_chance = random.randrange(5)  # 20% chance
        if catch_chance == 0:
            type.type("You lunge, and miraculously, your hands close around the rabbit's soft fur!")
            print("\n")
            type.type(green(bright("FINALLY!")))
            print("\n")
            type.type("The rabbit squeaks, poops out a shower of coins, and vanishes in a burst of sparkles. ")
            type.type("You're left sitting in an alley, covered in money, laughing like a maniac.")
            print("\n")
            coins = random.randint(2000, 5000)
            type.type("You collect " + green(bright("$" + str(coins))) + " from the ground.")
            self.change_balance(coins)
            self.meet("Caught Rabbit")
        else:
            type.type("The rabbit looks at you, twitches its nose, and then... walks straight through the wall. Just phases right through solid brick.")
            print("\n")
            type.type(quote("...What."))
            print("\n")
            type.type(yellow("That rabbit is definitely not a normal rabbit. The hunt continues."))
        
        self.advance_rabbit_chase()
        print("\n")
        
    # Doughman Nights (500,000 - 900,000)
    def city_stroll(self):
        self.meet("City Stroll Event")
        type.type("You wander the city streets at dusk, neon signs buzzing to life as the sky turns purple. ")
        type.type("The sidewalks are crowded with people heading home, heading out, heading somewhere. You're just... heading. ")
        type.type("Trees planted in sidewalk grates rustle their leaves, the only nature brave enough to survive here.")
        print("\n")
        event = random.choice(["bank_robbery", "dog_walker", "mugging", "street_performer", "lost_tourist", "none"])
        if event == "bank_robbery":
            type.type("BANG. Glass shatters. Alarms scream. Three people in masks burst out of the bank across the street, bags in hand. Cops aren't here yet.")
            print("\n")
            type.type("What do you do?")
            action = input("(help/run/sneak/film): ").strip().lower()
            if action == "help":
                type.type("You sprint toward them like an idiot hero. One robber turns - ")
                if random.random() < 0.3:
                    type.type("and you clothesline him into the pavement. His bag splits open. You grab a handful of cash before the cops arrive.")
                    print("\n")
                    type.type("They question you for an hour but eventually let you go with thanks and a reward.")
                    self.change_balance(random.randint(1000, 3000))
                else:
                    type.type("and clocks you in the jaw with a pistol. You go down HARD. When you wake up, cops are everywhere and your head is ringing.")
                    self.hurt(random.randint(20, 40))
                    self.lose_sanity(random.choice([2, 3, 4]))  # Sudden violence
                print("\n")
            elif action == "sneak":
                type.type("You circle around the chaos, moving low. A bag dropped in the confusion...")
                if random.random() < 0.4:
                    type.type("You snag it and walk away like nothing happened. Inside: " + green(bright("$" + str(random.randint(500, 2000)))) + ".")
                    self.change_balance(random.randint(500, 2000))
                else:
                    type.type("A cop spots you with the bag. You spend the night in a cell explaining yourself. Costs you lawyer fees.")
                    self.change_balance(-random.randint(500, 1500))
                print("\n")
            elif action == "film":
                type.type("You pull out your phone and start recording. The video goes viral. Local news pays you for the footage.")
                self.change_balance(random.randint(200, 800))
                print("\n")
            else:
                type.type("You run like a sensible person. The chaos fades behind you. You hear sirens, then nothing.")
                print("\n")
        elif event == "dog_walker":
            type.type("A dog walker rounds the corner, pulled along by SIX dogs of various sizes. ")
            type.type("A Great Dane, a corgi, a poodle, a mutt, a husky, and something that might be a small bear.")
            print("\n")
            type.type("They see you and SURGE forward, tails wagging. The walker loses her grip on two leashes.")
            print("\n")
            type.type("Do you help catch them, let them tackle you with love, or dodge?")
            action = input("(help/love/dodge): ").strip().lower()
            if action == "love":
                type.type("You drop to your knees and let the dogs swarm you. Tongues everywhere. So much fur. Pure joy.")
                print("\n")
                self.heal(random.randint(15, 30))
                type.type("The walker apologizes profusely while you laugh, covered in dog hair and feeling better than you have in weeks.")
                self.add_status("Dog Blessed")
                self.restore_sanity(random.choice([2, 3, 4]))  # Restores sanity
            elif action == "help":
                type.type("You snag the trailing leashes and help wrangle the pack. The walker is VERY grateful.")
                print("\n")
                type.type(quote("Oh my god, thank you! Here, let me give you something for your trouble."))
                self.change_balance(random.randint(50, 150))
            else:
                type.type("You sidestep like a matador. The dogs rocket past you. The walker chases after them, screaming names. You feel like you missed out on something special.")
            print("\n")
        elif event == "mugging":
            if self.has_item("Rolling Fortress"):
                type.type("A figure emerges from an alley. Then another. Then a third. They move toward your car.")
                print("\n")
                type.type("The " + cyan(bright("Rolling Fortress")) + "'s defense layers trigger. Would-be thieves approach, assess, and retreat. Nobody is taking anything tonight.")
                print("\n")
                self.restore_sanity(8)
            elif self.has_item("Fortified Perimeter"):
                type.type("A figure moves in from the shadows. Another follows.")
                print("\n")
                type.type("The " + cyan(bright("Fortified Perimeter")) + "'s trip-wires trigger. An alarm sounds. The night goes quiet.")
                print("\n")
                self.restore_sanity(5)
            elif self.has_item("Road Warrior Armor"):
                type.type("They came with intent. The " + cyan(bright("Road Warrior Armor")) + "'s harness glints under the streetlamp.")
                print("\n")
                type.type("The intent evaporates.")
                self.restore_sanity(5)
            elif self.has_item("Guardian Angel"):
                type.type("A figure emerges from an alley. Then another. Then a third. They fan out, blocking your path.")
                print("\n")
                type.type("The " + cyan(bright("Guardian Angel")) + "'s layered signal-to-perimeter system was already tracking this threat. It ends before it starts.")
                print("\n")
                self.restore_sanity(10)
            elif self.has_item("Distress Beacon"):
                type.type("A figure emerges from an alley. Then another. Then a third. They fan out, blocking your path.")
                print("\n")
                type.type("You trigger the " + cyan(bright("Distress Beacon")) + ". In the confusion of arriving vehicles, your threat disappears.")
                print("\n")
                self.use_item("Distress Beacon")
                self.restore_sanity(7)
            # Check for Bodyguard Bruno - complete protection
            elif self.has_item("Bodyguard Bruno"):
                type.type("A figure emerges from an alley. Then another. Then a third. They fan out, blocking your path.")
                print("\n")
                type.type("Before they can speak, Bruno steps out of the shadows behind them.")
                print("\n")
                type.type(quote("Evening, gentlemen. My friend here is under my protection."))
                print("\n")
                type.type("The muggers exchange nervous glances. One by one, they back away and disappear into the night.")
                type.type(" Bruno nods at you. " + quote("Stay safe out there."))
                print("\n")
                self.restore_sanity(12)
            elif self.has_item("Tattered Cloak") or self.has_item("Invisible Cloak"):
                cloak = "Tattered Cloak" if self.has_item("Tattered Cloak") else "Invisible Cloak"
                type.type("A figure emerges from an alley. Then another. Then a third.")
                print("\n")
                type.type("You pull the " + cyan(bright(cloak)) + " tight. The nearest mugger squints directly at you.")
                print("\n")
                type.type(quote("The hell — where'd he go?"))
                print("\n")
                type.type("Their eyes slide right past you. You walk out the far end of the alley without breathing.")
                print("\n")
                type.type("You don't stop until you're two blocks away, hands shaking, invisible, alive.")
                self.restore_sanity(10)
            elif self.has_item("Lucky Medallion") or self.has_item("Lucky Coin"):
                coin = "Lucky Medallion" if self.has_item("Lucky Medallion") else "Lucky Coin"
                type.type("A figure emerges from an alley. Then another. Then a third. One has a knife that catches the streetlight.")
                print("\n")
                type.type("You reach into your pocket. The " + cyan(bright(coin)) + " is warm in your hand.")
                print("\n")
                type.type("You flip it without thinking. Heads.")
                print("\n")
                type.type("The coin bounces off the pavement and rolls perfectly under the lead mugger's foot. He stumbles.")
                print("\n")
                type.type("You vault the nearby fence. A heartbeat later, the alley is behind you. The coin is gone, but you're not.")
                self.restore_sanity(8)
            else:
                type.type("A figure emerges from an alley. Then another. Then a third. They fan out, blocking your path. One has a knife.")
                print("\n")
                type.type(quote("Wallet. Phone. Now. Don't make this difficult."))
                print("\n")
                type.type("What's your move?")
                action = input("(fight/talk/comply/run): ").strip().lower()
                
                if action == "fight":
                    # Brass Knuckles - instant deterrence before the fight even starts
                    if self.has_item("Brass Knuckles"):
                        type.type("You raise your fist. The brass knuckles catch the streetlight at exactly the right angle.")
                        print("\n")
                        type.type("The mugger looks at your hand, then at your face, then makes a decision about his life goals.")
                        print("\n")
                        type.type("He leaves. Fast.")
                        print("\n")
                        type.type("His friends follow without a word.")
                        self.restore_sanity(8)
                        print("\n")
                    # Pocket Knife gives you a real edge (consumed)
                    elif self.has_item("Pocket Knife"):
                        self.use_item("Pocket Knife")
                        type.type("You pull out your pocket knife. The blade catches the streetlight.")
                        print("\n")
                        type.type("The muggers hesitate. That moment of doubt is all you need - you slash at the closest one, and they scatter.")
                        print("\n")
                        type.type("You're left standing in the alley, breathing hard. The knife is bent - useless now - but you're alive.")
                        print("\n")
                    else:
                        type.type("You've had enough of this city taking from you. You throw the first punch - ")
                        if random.randrange(100) < 30:  # 30% base chance
                            type.type("and it connects beautifully. In the chaos, they scatter like roaches when the lights come on. You stand alone, fists shaking, alive.")
                        else:
                            type.type("but they're three and you're one. You go down swinging, but you go down.")
                            self.hurt(random.randint(25, 45))
                            self.change_balance(-random.randint(500, 1500))
                            self.lose_sanity(random.choice([3, 4, 5]))
                        print("\n")
                elif action == "talk":
                    type.type("You start talking, fast, making stuff up. You're a cop. Your brother is in the mob. You have a disease that spreads by touch.")
                    if random.randrange(100) < 40:  # 40% base chance
                        type.type(" Something works. They exchange glances, suddenly unsure. They back off.")
                    else:
                        type.type(" The one with the knife laughs. " + quote("Nice try.") + " They take your stuff anyway.")
                        self.change_balance(-random.randint(300, 800))
                    print("\n")
                elif action == "run":
                    type.type("You BOLT. Pure animal instinct. Behind you, footsteps - ")
                    if random.randrange(100) < 55:  # 55% base chance to escape
                        type.type("that fade as you outrun them. You don't stop until you're ten blocks away, gasping, but free.")
                    else:
                        type.type("and a hand grabs your collar. You hit the ground. They take what they want and leave you there.")
                        self.hurt(random.randint(10, 25))
                        self.change_balance(-random.randint(200, 600))
                        self.lose_sanity(random.choice([2, 3]))
                    print("\n")
                else:
                    type.type("You hand over your wallet. Not worth dying over. They grab it and disappear into the city.")
                    self.change_balance(-random.randint(100, 400))
                    print("\n")
        elif event == "street_performer":
            type.type("A street performer has gathered a crowd - a man painted entirely silver, standing motionless on a crate. ")
            type.type("He hasn't moved in the ten minutes you've been watching. Is he even breathing?")
            print("\n")
            type.type("A kid throws a coin. The man LUNGES forward, making robot sounds. The crowd laughs.")
            print("\n")
            type.type("Do you tip him, try to make him flinch, or just watch?")
            action = input("(tip/flinch/watch): ").strip().lower()
            if action == "tip":
                self.change_balance(-random.randint(1, 5))
                type.type("You drop some cash in his bucket. He salutes you in slow motion, then freezes again. Worth every penny.")
                self.add_status("Amused")
            elif action == "flinch":
                type.type("You wave your hand in front of his face. Make sudden movements. Nothing. This guy is a PROFESSIONAL.")
                print("\n")
                type.type("Finally, you give up. As you walk away, you hear him whisper: " + quote("Better luck next time."))
            else:
                type.type("You watch the crowd tip him, try to mess with him, take photos. ")
                type.type("The whole city walks past this moment of weird magic. Eventually you move on, but you're smiling.")
            print("\n")
        elif event == "lost_tourist":
            type.type("A family of tourists blocks the sidewalk, spinning in circles, staring at their phones, looking increasingly panicked. ")
            type.type("Mom, Dad, two kids, all wearing matching 'I HEART THE CITY' shirts.")
            print("\n")
            type.type(quote("Excuse me? Do you know where the... um...") + " the dad holds up his phone, showing an address that's literally two blocks away.")
            print("\n")
            type.type("Do you help them, ignore them, or intentionally send them the wrong way?")
            action = input("(help/ignore/trick): ").strip().lower()
            if action == "help":
                type.type("You walk them there yourself. Takes five minutes. The mom tries to give you money but you wave it off. The kids wave goodbye.")
                print("\n")
                type.type("You feel... good? Like, genuinely good. Weird.")
                self.heal(random.randint(5, 15))
                self.add_status("Good Samaritan")
            elif action == "trick":
                type.type("You give them completely wrong directions with a smile. They thank you profusely and head off into a part of the city they should NOT be in.")
                print("\n")
                type.type("You feel like a jerk. Because you are one.")
            else:
                type.type("You pretend to be on your phone and brush past them. Someone else will help. Probably.")
            print("\n")
        else:
            type.type("Tonight, the city is just background noise. ")
            type.type("You walk and walk, past closed shops and flickering signs, past sleeping homeless and busy taxis, ")
            type.type("until your legs are tired and your mind is empty.")
            print("\n")
            type.type("A raccoon waddles across your path, looks at you like you're the intruder here, and disappears into a storm drain. Fair enough.")
            print("\n")

    def city_park(self):
        self.meet("City Park Event")
        type.type("You step into the city park, an oasis of green amidst concrete and steel. ")
        type.type("Ancient oak trees stretch overhead, their leaves whispering secrets. ")
        type.type("Fireflies blink in the bushes. Somewhere, an owl hoots. ")
        type.type("It's like the forest never left - it just learned to hide.")
        print("\n")
        event = random.choice(["pigeons", "hobo_joe", "free_pizza", "pond", "chess_hustler", "midnight_gardener", "none"])
        
        if event == "pigeons":
            type.type("You sit on a bench. Immediately, pigeons materialize. Dozens of them. They strut toward you like a feathered army, heads bobbing, eyes hungry.")
            print("\n")
            type.type("One lands on your shoulder. Another on your head. This is getting out of hand.")
            print("\n")
            type.type("Do you feed them, flee, or assert dominance?")
            choice = input("(feed/flee/dominance): ").strip().lower()
            if choice == "feed":
                type.type("You tear up some bread from your pocket (you always have bread, don't question it). ")
                type.type("The pigeons go INSANE with joy. More come. The ground becomes a sea of cooing feathers.")
                print("\n")
                if random.random() < 0.7:
                    type.type("An old man watches from another bench, smiling. " + quote("They like you. That's good luck."))
                    self.add_status("Pigeon Blessed")
                else:
                    type.type("One of them poops on your shoe. Still worth it.")
                print("\n")
            elif choice == "dominance":
                type.type("You stand up, spread your arms, and make direct eye contact with the alpha pigeon. You hold your ground.")
                print("\n")
                type.type("The pigeons... back off. They respect your energy. One bows its head. You have established yourself in the pecking order.")
                self.add_status("Pigeon King")
                print("\n")
            else:
                type.type("You sprint. They follow for half a block before giving up. You look ridiculous. Several people recorded you.")
                print("\n")
        
        elif event == "hobo_joe":
            type.type("A figure waves from a bench beneath a willow tree. It's Hobo Joe, a man you've seen around - ")
            type.type("scraggly beard, army jacket, kind eyes, a harmonica that's seen better days.")
            print("\n")
            type.type(quote("Hey friend. Got time for an old man?"))
            print("\n")
            type.type("Do you sit with him, give him money, or keep walking?")
            choice = input("(sit/money/walk): ").strip().lower()
            if choice == "sit":
                type.type("You sit. Joe plays a tune on his harmonica - slow, sad, beautiful. When he finishes, he tells you a story.")
                print("\n")
                story = random.choice(["war", "love", "treasure"])
                if story == "war":
                    type.type(quote("I was in the war. Saw things no man should see. But you know what got me through? "))
                    type.type(quote("Kindness. Random kindness from strangers. That's the only magic that's real."))
                    self.add_status("Wise")
                elif story == "love":
                    type.type(quote("Had a wife once. Beautiful woman. Lost her to cancer twenty years ago. "))
                    type.type(quote("Still talk to her every night, right here under this tree. She answers sometimes, in the wind."))
                    self.heal(random.randint(10, 20))
                else:
                    type.type(quote("You know there's money buried in this park? From the old days. Bank robbers. I've been looking for years. Maybe you'll have better luck."))
                    self.add_item("Joe's Treasure Map")
                print("\n")
            elif choice == "money":
                give = random.randint(10, 50)
                if self.get_balance() >= give:
                    self.change_balance(-give)
                    type.type("You hand him some cash. He looks at you, really looks, and nods.")
                    print("\n")
                    type.type(quote("Bless you. Here, take this. Found it in the fountain. Probably worth more than what you gave me."))
                    self.add_item("Lucky Coin")
                else:
                    type.type("You don't have much to give, but you give what you can. Joe understands.")
                print("\n")
            else:
                type.type("You walk past. Joe doesn't take it personally. He starts playing another tune, for no one and everyone.")
                print("\n")
        
        elif event == "free_pizza":
            type.type("A food truck is parked by the fountain with a sign: 'FREE PIZZA - GRAND OPENING!' There's already a line, but it's moving fast.")
            print("\n")
            type.type("Do you get in line, cut the line, or resist the siren call of free cheese?")
            choice = input("(line/cut/resist): ").strip().lower()
            if choice == "line":
                type.type("You wait your turn like a civilized person. Twenty minutes later, you're holding a slice of the best pizza you've ever tasted.")
                self.heal(random.randint(15, 30))
                print("\n")
            elif choice == "cut":
                type.type("You slip to the front. A guy in a gym shirt grabs your arm.")
                print("\n")
                type.type(quote("Hey! Back of the line, pal!"))
                print("\n")
                if random.random() < 0.5:
                    type.type("You talk your way out of it - emergency, low blood sugar, etc. You get your pizza, but you feel like a jerk.")
                    self.heal(random.randint(10, 20))
                else:
                    type.type("He shoves you. You shove back. Security shows up. No pizza for you.")
                    self.hurt(random.randint(5, 10))
                print("\n")
            else:
                type.type("You walk past. The pizza smells amazing. You tell yourself it probably has too many carbs anyway. You don't believe yourself.")
                print("\n")
        
        elif event == "pond":
            type.type("You find yourself at the park's pond, a mirror of black water reflecting the city lights. ")
            type.type("Ducks sleep along the edge. Koi fish circle lazily in the shallows. A turtle watches you from a rock.")
            print("\n")
            
            # Animal Whistle lets you befriend the pond turtle
            if self.has_item("Animal Whistle") and not self.has_companion("Shellbert"):
                type.type("The " + magenta(bright("Animal Whistle")) + " hums. The dignified turtle turns its ancient head toward you.")
                print("\n")
                type.type("Slowly - very slowly - the turtle slides into the water and paddles over to you.")
                print("\n")
                type.type("It climbs onto the bank at your feet and extends its head. You pet its shell. The turtle closes its eyes contentedly.")
                print("\n")
                type.type("You've befriended the pond's wisest resident. You call it " + cyan(bright("Shellbert")) + ".")
                print("\n")
                type.type("Shellbert will accompany you now, offering ancient wisdom at a glacial pace.")
                self.add_companion("Shellbert", "Wise Turtle")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                self.heal(random.randint(20, 35))
                self.restore_sanity(8)
                print("\n")
                return
            
            type.type("Do you feed the ducks, skip stones, or just... sit and breathe?")
            choice = input("(feed/skip/sit): ").strip().lower()
            if choice == "feed":
                type.type("You toss some crumbs into the water. The ducks wake up, quacking excitedly. The koi surge to the surface. The turtle doesn't move - too dignified.")
                print("\n")
                type.type("For a moment, you're the center of this little ecosystem. It feels nice to be needed.")
                self.heal(random.randint(5, 15))
                print("\n")
            elif choice == "skip":
                type.type("You find a flat stone and send it skipping across the pond. Three skips. Four. Five!")
                print("\n")
                type.type("A kid watching nearby claps. You feel unreasonably proud.")
                self.add_status("Simple Joy")
                print("\n")
            else:
                type.type("You sit on the bank and just... exist. No gambling. No wagon. No past or future. Just you, the water, and the sound of the city breathing around you.")
                print("\n")
                self.heal(random.randint(15, 30))
                self.add_status("Centered")
                print("\n")
        
        elif event == "chess_hustler":
            type.type("A man sits at a stone table with a chess board, pieces mid-game. He sees you looking.")
            print("\n")
            type.type(quote("Twenty bucks says you can't beat me. Fifty if you can."))
            print("\n")
            type.type("Do you play, watch someone else play, or decline?")
            choice = input("(play/watch/decline): ").strip().lower()
            if choice == "play":
                if self.get_balance() >= 20:
                    self.change_balance(-20)
                    type.type("You sit down. The game is intense. He's good. Really good.")
                    if random.random() < 0.3:
                        type.type("But you're better. Somehow, you see the winning move. Checkmate.")
                        print("\n")
                        type.type(quote("Well damn.") + " He hands you fifty bucks, grinning. " + quote("Come back anytime."))
                        self.change_balance(50)
                    else:
                        type.type("He destroys you in twelve moves. You didn't even see it coming.")
                        print("\n")
                        type.type(quote("Good game. Want to go again?") + " You decline.")
                else:
                    type.type("You don't have twenty bucks to spare. He shrugs and waits for the next sucker.")
                print("\n")
            elif choice == "watch":
                type.type("You watch him demolish three different challengers. The man is a shark. You learn something about patience and sacrifice.")
                self.add_status("Strategic")
                print("\n")
            else:
                type.type(quote("Scared money don't make money,") + " he calls after you. You don't look back.")
                print("\n")
        
        elif event == "midnight_gardener":
            type.type("In a far corner of the park, you spot someone tending to the flower beds. At midnight. With a headlamp on.")
            print("\n")
            type.type("It's an old woman, kneeling in the dirt, whispering to the roses.")
            print("\n")
            type.type("Do you approach her, watch from a distance, or leave her alone?")
            choice = input("(approach/watch/leave): ").strip().lower()
            if choice == "approach":
                type.type("She looks up as you approach, not startled at all. Her eyes are sharp despite her age.")
                print("\n")
                type.type(quote("The flowers grow best when no one's watching. Like people, really."))
                print("\n")
                type.type("She hands you a small cutting - a rose, dark red, still fresh.")
                print("\n")
                type.type(quote("Plant this somewhere. Keep something alive."))
                self.add_item("Midnight Rose")
                print("\n")
            elif choice == "watch":
                type.type("You watch her work for a while. There's something meditative about it - the careful attention, the gentle hands. You feel calmer just watching.")
                self.heal(random.randint(5, 10))
                print("\n")
            else:
                type.type("You leave her to her work. Some people and their magic are best left undisturbed.")
                print("\n")
        
        else:
            type.type("The park is quiet tonight. You find a bench beneath an ancient elm and sit, watching the fireflies blink their slow morse code.")
            print("\n")
            type.type("A squirrel watches you from a branch. A bat flutters overhead. The city rumbles on, but here, in this bubble of green, you can almost forget where you are.")
            print("\n")
            self.heal(random.randint(5, 10))

    # RABBIT CHASE CHAIN - DOUGHMAN NIGHT
    def chase_the_fifth_rabbit(self):
        # Fifth rabbit chase - getting desperate
        if self.get_rabbit_chase() != 4 or self.has_met("Caught Rabbit"):
            self.night_event()
            return
        
        type.type("You've lost count of how many times you've chased this rabbit. It's become personal. An obsession, some might say.")
        print("\n")
        type.type("Tonight, you spot it in the park, sitting on a bench like it owns the place. It's almost like it's waiting for you.")
        print("\n")
        type.type("You approach slowly this time. No running. No chasing. Maybe that's been your mistake all along.")
        print("\n")
        type.type("The rabbit watches you, those dark eyes gleaming with something that might be intelligence. You're within arm's reach...")
        print("\n")
        
        catch_chance = random.randrange(4)  # 25% chance
        if catch_chance == 0:
            type.type("You move like lightning, and for once, the rabbit doesn't react in time!")
            print("\n")
            type.type(green(bright("VICTORY!")))
            print("\n")
            type.type("The rabbit squeaks once, poops out an absolute fortune in coins, and explodes into a cloud of glitter. You're showered in money and sparkles.")
            print("\n")
            coins = random.randint(5000, 15000)
            type.type("When the sparkles settle, you've collected " + green(bright("$" + str(coins))) + "!")
            self.change_balance(coins)
            self.meet("Caught Rabbit")
        else:
            type.type("The rabbit lets out what can only be described as a sigh, then simply... blinks out of existence. One second it's there, the next it's gone.")
            print("\n")
            type.type(yellow("You sit on the bench for a long time, questioning reality. Is any of this real? Is the rabbit real? Are YOU real?"))
            print("\n")
            type.type(yellow("The hunt must continue. You're too deep now to quit."))
        
        self.advance_rabbit_chase()
        print("\n")

    # NIGHT EVENTS - Various Tiers
    def stargazing(self):
        # Poor/Cheap night event
        variant = random.randrange(3)
        if variant == 0:
            type.type("You step out of your car to look at the stars. It's a clear night.")
            print("\n")
            type.type("Somewhere up there, billions of years ago, a star exploded so that you could exist.")
            print("\n")
            type.type("And here you are, using that cosmic gift to gamble at a casino. The universe must be so proud.")
        elif variant == 1:
            type.type("The sky is obscene tonight. Purple-black and crusted with stars. More than you've ever seen.")
            print("\n")
            type.type("It's the kind of sky city people never see because there's always a Walgreens sign drowning it out.")
            print("\n")
            type.type("But out here, parked behind a gas station at the edge of nowhere? You get the whole show.")
        else:
            type.type("You lean against the hood of the wagon and look up. You find Orion's Belt. The Big Dipper. That's... all you know.")
            print("\n")
            type.type("But it doesn't matter. The names don't matter. What matters is that something enormous and ancient is looking back at you.")
            print("\n")
            type.type("And it doesn't care about your problems. Somehow, that's comforting.")
        print("\n")
        if self.has_item("Binoculars"):
            type.type("You pull out your " + magenta(bright("Binoculars")) + " and point them up. The moon's craters snap into focus. You can see the rings of... wait, is that Saturn?")
            print("\n")
            type.type("You spend an hour mapping constellations. For a guy living in a car, you've never felt richer.")
            self.restore_sanity(random.choice([8, 10, 12]))
            if self.has_item("Lucky Charm Bracelet"):
                print("\n")
                type.type("The " + cyan(bright("Lucky Charm Bracelet")) + " tingles on your wrist. You see something falling from the sky — a shooting star.")
                print("\n")
                type.type("You make a wish that feels exactly right. Not desperate. Not greedy. Just... right.")
                self.restore_sanity(5)
        else:
            type.type("Still, it's beautiful. You feel small, but in a comforting way.")
            self.restore_sanity(random.choice([3, 4, 5]))
            if self.has_item("Night Scope"):
                print("\n")
                type.type("Through the " + cyan(bright("Night Scope")) + ", the darkness becomes transparent. You watch a raccoon carry a hotdog from three blocks away. You feel omniscient.")
                print("\n")
                self.restore_sanity(6)
            if self.has_item("Spotlight"):
                print("\n")
                type.type("You sweep the " + cyan(bright("Spotlight")) + " in a wide arc. Everything in range is illuminated. A deer freezes. The deer is extremely visible.")
                print("\n")
                self.restore_sanity(4)
        print("\n")

    def midnight_snack_run(self):
        # Cheap/Modest night event
        type.type("You can't sleep. Your stomach is growling. Time for a midnight snack run.")
        print("\n")
        type.type("The only thing open is a sketchy gas station that looks like it was last cleaned during the Reagan administration.")
        print("\n")
        type.type("You buy a hot dog of uncertain age and a energy drink that might be radioactive.")
        print("\n")
        cost = random.randint(5, 12)
        type.type("It costs " + green(bright("$" + str(cost))) + ". Highway robbery, but you're desperate.")
        self.change_balance(-cost)
        print("\n")
        chance = random.randrange(3)
        if chance == 0:
            type.type("The hot dog fights back. You spend the next hour regretting everything.")
            self.hurt(10)
        else:
            type.type("Surprisingly, it hits the spot. Junk food at 2 AM hits different.")
            self.heal(5)
        print("\n")

    def mysterious_lights(self):
        # Modest night event
        type.type("You see strange lights in the sky. They're moving in patterns that don't make sense.")
        print("\n")
        type.type("UFO? Government experiment? Your imagination? All equally possible at this point.")
        print("\n")
        type.type("You watch them dance across the stars for what feels like hours. Then, suddenly, they're gone.")
        print("\n")
        type.type("You don't tell anyone about this. Who would believe you?")
        self.lose_sanity(random.choice([1, 2, 3]))
        print("\n")

    def late_night_radio(self):
        # Rich night event
        type.type("You turn on the radio. At this hour, the only thing playing is a conspiracy theory call-in show.")
        print("\n")
        type.type("A caller is explaining how the government is putting mind control chemicals in playing cards.")
        print("\n")
        type.type(quote("The Dealer knows, man. They ALL know. It's in the ink!"))
        print("\n")
        type.type("You laugh, but then you think about the Dealer's eyes. The way he always seems to know what you're thinking...")
        print("\n")
        type.type("You turn off the radio. Some rabbit holes are better left unexplored.")
        self.lose_sanity(1)
        print("\n")

    # ==========================================
    # MEGA NIGHT EVENT BATCH
    # ==========================================

    def dream_of_winning(self):
        variant = random.randrange(4)
        if variant == 0:
            type.type("You dream of winning. The moment the million hits your account.")
            print("\n")
            type.type("Confetti. Champagne. People cheering your name.")
            print("\n")
            type.type("The Dealer shakes your hand. His grip is warm. He says, " + quote("I always knew you'd make it."))
            print("\n")
            type.type("You wake up smiling. Then you check your balance. Still not there.")
            print("\n")
            type.type("But soon. Soon.")
        elif variant == 1:
            type.type("In the dream, you walk into a bank. A real bank. With your name on the door.")
            print("\n")
            type.type("The teller asks how much you'd like to deposit. You say " + quote("All of it.") + " She doesn't blink.")
            print("\n")
            type.type("You sign papers. Buy a house. A car that isn't also your bedroom. You eat at a restaurant with cloth napkins.")
            print("\n")
            type.type("Then you wake up. The steering wheel is digging into your ribs. But the smile lingers.")
        elif variant == 2:
            type.type("You dream about the day after. Not the winning itself — the day after.")
            print("\n")
            type.type("You're in an apartment. Sunlight through clean windows. Coffee that didn't come from a gas station.")
            print("\n")
            type.type("There's a bookshelf. When did you start reading again? It doesn't matter. In the dream, everything is possible.")
            print("\n")
            type.type("You wake up reaching for a coffee mug that isn't there. The absence stings.")
        else:
            type.type("The dream is simple this time. You're just... not worried. About anything.")
            print("\n")
            type.type("No Dealer. No casino. No car. Just a warm room and the knowledge that tomorrow will be okay.")
            print("\n")
            type.type("That's the dream. Not a million dollars. Just " + yellow("okay") + ".")
            print("\n")
            type.type("You wake up and the " + yellow("okay") + " evaporates. But you remember what it felt like.")
        self.restore_sanity(5)
        print("\n")

    def nightmare_of_losing(self):
        if self.has_item("Dream Catcher"):
            type.type("The " + cyan(bright("Dream Catcher")) + " glows faintly on the rearview mirror.")
            print(PAR)
            type.type("The nightmare can't take hold. Whatever was waiting for you in the dark dissolves before it can form. You sleep clean through to morning.")
            print(PAR)
            type.type("You wake up rested. Unsettled in a vague way — like you know something tried and failed — but rested.")
            self.restore_sanity(4)
            print(PAR)
            return
        variant = random.randrange(4)
        if variant == 0:
            type.type("You dream of losing everything. Not slowly — all at once, in a single hand, the balance hitting zero and then going negative like the game has decided to start billing you for the privilege of losing. The Dealer laughs. Then everyone laughs. Then you're being dragged out by your collar while the chips scatter across the floor.")
            print(PAR)
            type.type("You wake up drenched in sweat, gasping like you surfaced from deep water. You check your balance. It's still there. It's fine. It's fine. It's fine.")
        elif variant == 1:
            type.type("In the nightmare, the cards are blank. Every single one — you flip them over and they're just white, featureless, like the deck was printed wrong or maybe the meaning has been removed from things.")
            print(PAR)
            type.type("The Dealer keeps dealing blank cards. You keep losing anyway. " + quote("Hit or stand?") + " he asks, and you scream, but no sound comes out, and he deals another blank card and you bust on nothing.")
            print(PAR)
            type.type("You jolt awake. Your mouth tastes like copper. Your heart is trying to exit your chest via the fastest route available.")
        elif variant == 2:
            type.type("The nightmare is familiar. You're at the table. You bet everything. You bust. But this time the floor opens under your chair and you fall — through the floor, through the building, into absolute nothing.")
            print(PAR)
            type.type("You keep falling. The Dealer's voice echoes down from somewhere above, warm and professional: " + quote("Better luck next time.") + " You hit the ground. You wake up. You're in your car. You're always in your car.")
        else:
            type.type("You dream that you've been playing for a hundred years. Your clothes are dust. Your beard drags on the casino floor. The other patrons are all skeletons in evening wear, betting chips made of bone.")
            print(PAR)
            type.type("The Dealer hasn't aged at all. He still has that smile — the one that says he has all the time in the world because time doesn't apply to him.")
            print(PAR)
            type.type(quote("One more hand?") + " he asks. You nod. What else would you do? What else have you ever done?")
            print(PAR)
            type.type("You wake up and check the mirror. No beard. But your eyes look a hundred years old.")
        if self.has_item("Third Eye"):
            type.type("The " + cyan(bright("Third Eye")) + " sees the nightmare for what it is — probability, not prophecy. You wake knowing the difference.")
            print(PAR)
            self.restore_sanity(5)
        elif self.has_item("Mind Shield"):
            type.type("The " + cyan(bright("Mind Shield")) + " filters the nightmare. It still reaches you, but muted. Distant.")
            print(PAR)
            self.lose_sanity(2)
        else:
            self.lose_sanity(5)
        print(PAR)

    def insomnia_night(self):
        variant = random.randrange(3)
        if variant == 0:
            type.type("You can't sleep. Your brain won't stop running the math — if I bet X and win Y, and then double down on Z, carry the loss from Tuesday, factor in the streak pattern, account for the Dealer's tell when he pauses... no, wait, that's not right. Start over.")
            print(PAR)
            type.type("You stare at the ceiling until the sky goes gray. Thinking. Always thinking. The math never adds up to freedom, but that never stopped you from trying.")
        elif variant == 1:
            type.type("Three AM. Four AM. Five AM. You've watched every hour tick over on the dashboard clock like you're being paid to witness it. Your body is doing that thing where it's so tired it stopped knowing how to sleep.")
            print(PAR)
            type.type("Your brain is throwing a party. An awful, private party where every guest is a decision you made wrong and the music is the specific silence of a car park at 4 AM. At 5:47 you finally drift off. Your alarm goes off at 6:00.")
        else:
            type.type("Sleep won't come. You try counting sheep. The sheep turn into cards. The cards turn into debts. The debts turn into a math problem you already know the answer to but keep solving anyway, hoping the answer changes.")
            print(PAR)
            type.type("You lie there, eyes open, listening to your own breathing and the distant hum of a highway that exists for people going somewhere. Somewhere out there, people are sleeping in actual beds, in actual houses, with mortgages that embarrass them and futures they take for granted.")
            print(PAR)
            type.type("You wonder if they know. How lucky the ordinary is. How you'd give everything you're chasing just to feel that ordinary again. Probably not. Nobody ever knows until it's already gone and they're lying in a car in the dark making deals with the ceiling.")
        if self.has_item("Delight Manipulator") or self.has_item("Delight Indicator"):
            gauge = "Delight Manipulator" if self.has_item("Delight Manipulator") else "Delight Indicator"
            print("\n")
            type.type("The " + cyan(bright(gauge)) + " on your wrist glows faintly in the dark. The needle points to zero.")
            print("\n")
            type.type("It's been a long time since it moved. You're not sure what happiness feels like anymore.")
            self.lose_sanity(1)
        if self.has_item("Survival Bivouac"):
            print(PAR)
            type.type("You unroll the " + magenta(bright("Survival Bivouac")) + " across the back seat.")
            print(PAR)
            type.type("It's rated for negative forty degrees. In a casino parking lot in June, it is perhaps slightly overkill.")
            print(PAR)
            type.type("You are asleep in four minutes. You sleep like a rock. You sleep like someone who has solved the problem of sleep completely and will never think about it again.")
            print(PAR)
            type.type("You wake up rested. Genuinely, embarrassingly rested. The brain math can wait.")
            self.restore_sanity(8)
            self.heal(10)
            print(PAR)
            return
        elif self.has_item("Gambler's Chalice") or self.has_item("Overflowing Goblet"):
            goblet = "Gambler's Chalice" if self.has_item("Gambler's Chalice") else "Overflowing Goblet"
            print(PAR)
            type.type("You reach for the " + cyan(bright(goblet)) + " and pour one drink, then another. The goblet never empties. The night is still sleepless, but something about the silver light on the rim makes it bearable — like the dark has agreed to be a little less dark, just for you, just for tonight.")
            self.restore_sanity(6)
            print(PAR)
            return
        elif self.has_item("Deck of Cards"):
            print(PAR)
            type.type("You reach for the " + cyan(bright("Deck of Cards")) + " and deal yourself a hand of solitaire.")
            print(PAR)
            type.type("The cards are familiar. The ritual is familiar. Shuffle, deal, turn over. Shuffle, deal, turn over. Your brain math dissolves into something simpler — red on black, black on red.")
            print(PAR)
            type.type("Sleep comes eventually. Not quickly. But eventually.")
            self.restore_sanity(4)
            print(PAR)
            return
        self.lose_sanity(3)
        self.hurt(5)
        print(PAR)

    def peaceful_night(self):
        if self.has_item("Nomad's Camp"):
            type.type("The " + cyan(bright("Nomad's Camp")) + " at night: fire crackles, traps set, feast prepared.")
            print("\n")
            type.type("The wilderness is your home. You sleep like a king and wake fully restored.")
            self.heal(50)
            self.restore_sanity(20)
            return
        # COMBO: Lucid Dreaming Kit + Fortune Cards = Dream Gambling
        if self.has_item("Lucid Dreaming Kit") and self.has_item("Fortune Cards"):
            if not self.has_met("Dream Gambling"):
                self.mark_met("Dream Gambling")
                type.type("In the dream, the " + cyan(bright("Fortune Cards")) + " become a full casino. You gamble in your sleep.")
                print("\n")
                type.type("The dream dealer looks like you, but older. " + quote("High card wins,") + " they say.")
                print("\n")
                player_card = random.randint(1, 13)
                dealer_card = random.randint(1, 13)
                if player_card > dealer_card:
                    type.type("Your card is higher. Tomorrow comes with a gift.")
                    self.add_status("Dream Win")
                    self.restore_sanity(8)
                elif player_card < dealer_card:
                    type.type("The dealer's card is higher. Tomorrow will be harder.")
                    self.add_danger("Dream Loss")
                    self.lose_sanity(3)
                else:
                    type.type("A push. The older you leans forward. " + italic(quote("The event after next — take the second option.")))
                    self.restore_sanity(5)
                print("\n")

        variant = random.randrange(3)
        if variant == 0:
            type.type("For once, you sleep peacefully. No dreams. No nightmares. Just rest.")
            print("\n")
            type.type("You wake up feeling... good? Is this what normal people feel like?")
            print("\n")
            type.type("It won't last, but you appreciate it while it does.")
        elif variant == 1:
            type.type("Rain on the roof. Not a storm — just rain. The soft kind. The kind that taps a lullaby on the metal above you.")
            print("\n")
            type.type("For the first time in weeks, your brain shuts up. No calculations. No strategies. No what-ifs.")
            print("\n")
            type.type("Just you, the rain, and eight uninterrupted hours.")
            print("\n")
            type.type("You wake up and for three seconds — three beautiful seconds — you forget where you are.")
        else:
            type.type("The temperature is perfect. Not too hot, not too cold. The car seat cradles you like it was designed for sleeping.")
            print("\n")
            type.type("It wasn't. But tonight, everything conspires to give you rest. The parking lot is quiet. No sirens. No drunks. No existential dread.")
            print("\n")
            type.type("You sleep like a baby. A baby who lives in a car, but a well-rested baby nonetheless.")
        self.restore_sanity(10)
        self.heal(15)
        if self.has_item("Fire Starter Kit") or self.has_item("Survival Bivouac"):
            item_name = "Fire Starter Kit" if self.has_item("Fire Starter Kit") else "Survival Bivouac"
            print("\n")
            type.type("The " + cyan(bright(item_name)) + " is doing its job. A small fire burns at the car's perimeter. The warmth is extraordinary. The stars are extraordinary. Everything is fine.")
            self.restore_sanity(5)
            self.heal(5)
        if self.has_item("Vintage Wine") or self.has_item("Silver Flask"):
            wine = "Vintage Wine" if self.has_item("Vintage Wine") else "Silver Flask"
            print("\n")
            type.type("You pour a glass from the " + cyan(bright(wine)) + ". The stars come out. For a while, everything is quiet and expensive.")
            print("\n")
            type.type("You didn't earn this night. Nobody earns a night like this. You just got lucky enough to be awake for it.")
            self.restore_sanity(5)
            self.heal(5)
        if self.has_item("Sneaky Peeky Goggles") or self.has_item("Sneaky Peeky Shades"):
            lenses = "Sneaky Peeky Goggles" if self.has_item("Sneaky Peeky Goggles") else "Sneaky Peeky Shades"
            print("\n")
            type.type("You put on the " + cyan(bright(lenses)) + " and look up at the stars.")
            print("\n")
            type.type("The enchanted lenses show you things the naked eye can't see — satellites drifting, shooting stars too faint for normal eyes, the Milky Way in impossible detail.")
            print("\n")
            type.type("For a moment, you understand why people look up.")
            self.restore_sanity(3)
        print("\n")

    def stray_cat_returns(self):
        if not self.has_met("Stray Cat Friend"):
            self.night_event()
            return
        type.type("You hear scratching at your window. It's your cat friend!")
        print("\n")
        type.type("The scraggly stray has returned, meowing insistently.")
        print("\n")
        type.type("You open the window a crack. It pushes its head through and purrs.")
        print("\n")
        type.type("You're not alone. Not entirely.")
        self.restore_sanity(8)
        print("\n")

    def midnight_walk(self):
        if self.has_item("Rusty Compass") or self.has_item("Golden Compass"):
            compass = "Golden Compass" if self.has_item("Golden Compass") else "Rusty Compass"
            if self.has_item("Golden Compass"):
                type.type("A faint golden glow from the " + cyan(bright(compass)) + " leads you back to your car.")
            else:
                type.type("The " + cyan(bright(compass)) + " tugs gently in your pocket, pulling you back toward your car.")
            print("\n")
            type.type("The needle always knows where home is. Even in total darkness.")
            self.restore_sanity(5)
            print("\n")
            return
        variant = random.randrange(3)
        if variant == 0:
            type.type("You can't sleep, so you walk. The city is different at this hour — quieter, more honest, the neon signs humming a frequency that only works on insomniacs and people with nothing left to protect.")
            print(PAR)
            type.type("You pass closed shops and sleeping houses. Everyone behind those walls has a bed. A fridge. A door that locks from the inside. You walk past all of it without slowing down, because the rhythm is the only thing that works — step, step, step, forward, one direction, don't stop.")
        elif variant == 1:
            type.type("Midnight. You lace your shoes and walk into the dark. A cat crosses your path, sits down, and watches you approach with the calm of something that has never worried about anything in its life.")
            print(PAR)
            type.type("You nod at the cat. It blinks once, slow and deliberate. You keep walking. Three miles in a familiar loop — past the casino, past the gas station, past the diner that smells like breakfast even at midnight, back to the wagon. The same orbit, every time.")
        else:
            type.type("You step out of the car and into the cool night air. Every joint in your body pops in sequence, like a xylophone built from bad decisions.")
            print(PAR)
            type.type("You walk along the shoulder of the highway. Headlights sweep over you at intervals — two seconds of being visible, then darkness again. Nobody slows. Nobody cares, which tonight feels like a gift. Just a silhouette on the roadside that exists briefly in someone's headlights and then doesn't. It's nice, being no one.")
        print(PAR)
        type.type("When you get back to your car, you're tired in the right way for once. The kind of tired that actually leads to sleep.")
        self.restore_sanity(random.choice([5, 7, 10]))
        if self.has_item("Binoculars"):
            print(PAR)
            type.type("You stop at the edge of a parking garage and pull out your " + cyan(bright("Binoculars")) + ". Scan the skyline.")
            print(PAR)
            type.type("The city looks different at distance. Smaller. More manageable. All those lit windows — every one of them a problem someone thinks is unique. From here, they're just lights.")
            self.restore_sanity(4)
        print(PAR)

    def raccoon_invasion(self):
        type.type("You wake up to scratching noises. Something is ON your car.")
        print("\n")
        type.type("You look up. A family of raccoons is making themselves at home on your roof.")
        print("\n")
        type.type("Mom raccoon. Dad raccoon. Three baby raccoons. All staring at you through the windshield with those little bandit masks.")
        print("\n")
        # Check if player has a Dog companion
        dog_name = None
        living = self.get_all_companions()
        for name, data in living.items():
            if data.get("type") in ["Dog", "Three-Legged Dog"]:
                dog_name = name
                break
        if dog_name:
            type.type(dog_name + " wakes up, sees the raccoons, and loses their entire mind.")
            print("\n")
            type.type("Barking. Howling. Clawing at the window. The raccoons scatter like furry grenades.")
            print("\n")
            type.type("Gone in three seconds. " + dog_name + " looks at you, tail wagging, enormously proud. You give them a pat. Earned.")
            self.restore_sanity(3)
            print("\n")
            return
        if self.has_item("Snare Trap"):
            type.type("You set the " + cyan(bright("Snare Trap")) + " around the food before bed. Classic precaution.")
            print("\n")
            type.type("In the morning, you've caught one very surprised raccoon. It stares at you. You stare at it.")
            print("\n")
            type.type("You relocate it to a field two miles down the road. It seems personally offended by this, but it's fine.")
            self.restore_sanity(4)
            print("\n")
            return
        if self.has_item("Pest Control"):
            type.type("You grab your " + magenta(bright("Pest Control")) + " and crack the window. One spritz. The raccoons look personally offended.")
            print("\n")
            type.type("They leave, but slowly. Deliberately. As if to say: " + quote("We'll be back."))
            print("\n")
            self.restore_sanity(4)
            return
        if self.has_item("Slingshot"):
            type.type("You step outside with your " + cyan(bright("Slingshot")) + ".")
            print("\n")
            type.type("Twelve seconds of chaos. Three panicked raccoons departing at full speed for safer territories.")
            print("\n")
            type.type("The babies fall off the roof, land safely in the grass, and scurry after their parents. No harm done. Just a lesson in property rights.")
            self.restore_sanity(5)
            print("\n")
            return
        variant = random.randrange(2)
        if variant == 0:
            type.type("You decide to let them have this one. You go back to sleep.")
            print("\n")
            type.type("In the morning, they're gone. So is your windshield wiper. So is the antenna. And half a sandwich you forgot about.")
            print("\n")
            type.type("Raccoons. Nature's tiny, adorable home invaders.")
        else:
            type.type("You honk the horn. They don't flinch. You honk again. The babies yawn.")
            print("\n")
            type.type("You stare at each other for a full minute. They're not leaving. This is their car now.")
            print("\n")
            type.type("You go back to sleep. In the morning, they've left a dead mouse on your hood. A gift? A threat? Both?")
        self.lose_sanity(2)
        print("\n")

    def police_checkpoint(self):
        type.type("You're driving late at night when you hit a police checkpoint.")
        print("\n")
        type.type(quote("License and registration. Where are you headed this late?"))
        print("\n")
        type.type("You explain that you're just... driving. Living in your car. The usual.")
        print("\n")
        type.type("The officer gives you a long look. Decides you're not worth the paperwork.")
        print("\n")
        type.type(quote("Drive safe.") + " He waves you through.")
        print("\n")
        self.lose_sanity(3)
        print("\n")

    def satellite_falling(self):
        type.type("You see a streak of light across the sky. A shooting star? No... too slow.")
        print("\n")
        type.type("It's a satellite, burning up on reentry. Pieces of space junk falling to earth.")
        print("\n")
        type.type("It's oddly beautiful. Destruction can be beautiful, you realize.")
        print("\n")
        type.type("A metaphor for something, probably. You're too tired to figure out what.")
        self.restore_sanity(3)
        print("\n")

    def nice_dream(self):
        variant = random.randrange(4)
        if variant == 0:
            type.type("You have a nice dream for once. About the life you used to have.")
            print("\n")
            type.type("A kitchen. Morning sunlight. Coffee in a real mug, not a gas station cup. Someone calls your name from another room.")
            print("\n")
            type.type("Waking up is hard. The contrast between the dream and the dashboard is a knife in the chest.")
        elif variant == 1:
            type.type("You dream about your mother's cooking. The smell fills the entire car. Garlic, butter, something on the stove.")
            print("\n")
            type.type("You wake up. The car smells like old upholstery and regret. But for a second — just a second — it smelled like home.")
        elif variant == 2:
            type.type("In the dream, you're a kid again. Riding your bike down a hill. No brakes. No fear. Just speed and laughter.")
            print("\n")
            type.type("You hit the bottom of the hill and keep going, faster and faster, until you're flying.")
            print("\n")
            type.type("You wake up in a reclined car seat. Not flying. But the feeling lingers. Light. Free.")
        else:
            type.type("You dream about a dog you used to have. Good dog. Patient dog. The kind that sat with you when things were bad.")
            print("\n")
            type.type("In the dream, you're both on a porch. Nowhere specific. Just a porch. Just sitting.")
            print("\n")
            type.type("You wake up reaching for fur that isn't there. Your hand finds cold vinyl.")
        self.restore_sanity(5)
        self.lose_sanity(3)  # Bittersweet
        print("\n")

    def nightmare(self):
        # COMBO: Devil's Deck + Binding Portrait = The Soul Game
        if self.has_item("Devil's Deck") and self.has_item("Binding Portrait"):
            type.type("You deal from the " + cyan(bright("Devil's Deck")) + ". You wager the " + cyan(bright("Binding Portrait")) + ".")
            print("\n")
            type.type("Your opponent wagers a memory. When you win — and you do — their memory enters the portrait.")
            print("\n")
            type.type("They forget meeting you. You keep the memory. It's not yours, but you can watch it whenever you want.")
            self.add_item("Stolen Memory")
            self.restore_sanity(3)
            print("\n")
            return

        if self.has_item("Necronomicon") and self.has_item("Dream Catcher"):
            type.type("The " + cyan(bright("Necronomicon")) + " and the " + cyan(bright("Dream Catcher")) + " create a feedback loop.")
            print("\n")
            type.type("The nightmare becomes a stage set. The monsters become furniture. You direct. You control.")
            print("\n")
            type.type("You rewrite the ending. The drowning car fills with light. The faceless Dealer bows and leaves. The teeth fall out and become pearls.")
            print("\n")
            type.type("You wake up refreshed. You learned something from that dream. You're not sure what yet. But it feels important.")
            self.restore_sanity(15)
            print("\n")
            return

        if self.has_item("Necronomicon") and not self.has_item("Dream Catcher"):
            type.type("The " + cyan(bright("Necronomicon")) + " rustles at 3 AM. The nightmare gets... educational.")
            print("\n")
            type.type("Something in the dark uses your sleeping mind as a classroom. You don't choose to attend. You don't get a say.")
            print("\n")
            type.type("You learn something. You don't have words for it yet. It costs you, but you learn it.")
            print("\n")
            type.type(italic("You understand something you didn't before. Whether that's good is a separate question."))
            self.add_status("Dark Knowledge")
            self.lose_sanity(5)
            print("\n")
            return

        variant = random.randrange(4)
        if variant == 0:
            type.type("Nightmares again. The usual. Losing everything. Dying alone in a parking lot that nobody remembers the name of.")
            print("\n")
            type.type("You wake up gasping. Takes a while to remember where you are. Takes longer to decide if that's better or worse.")
        elif variant == 1:
            type.type("In the nightmare, the Dealer has your face. He deals with your hands. He smiles with your mouth.")
            print("\n")
            type.type("You sit across from yourself and lose every hand. You can't beat yourself. You never could.")
            print("\n")
            type.type("You wake up and avoid the mirror for the rest of the morning.")
        elif variant == 2:
            type.type("The dream is about water. Rising water. You're in the car and it's filling up. First your feet. Then your lap. Then your chest.")
            print("\n")
            type.type("You can't open the doors. The windows are locked. The water is warm, which is somehow worse.")
            print("\n")
            type.type("You gasp awake. Bone dry. Heart hammering. You open the car door just to prove you can.")
        else:
            type.type("You dream about teeth falling out. One by one, into your cupped hands. There's no pain, just the awful clicking sound of enamel on enamel.")
            print("\n")
            type.type("You try to put them back. They don't fit anymore. Like the dream is telling you: some things can't be undone.")
            print("\n")
            type.type("You wake up and run your tongue along your teeth. All there. But the dream leaves a residue that takes hours to shake.")
        if self.has_item("Third Eye"):
            type.type("The " + cyan(bright("Third Eye")) + " sees the nightmare for what it is — probability, not prophecy. You wake knowing the difference.")
            print("\n")
            self.restore_sanity(5)
        elif self.has_item("Mind Shield"):
            type.type("The " + cyan(bright("Mind Shield")) + " filters the nightmare. It still reaches you, but muted. Distant.")
            print("\n")
            self.lose_sanity(4)
        else:
            self.lose_sanity(8)
        print("\n")

    def giant_oyster_opening(self):
        """Giant Oyster can be cracked open for a pearl or a meal"""
        if not self.has_item("Giant Oyster"):
            self.night_event()
            return
        if self.has_met("Oyster Opened"):
            self.night_event()
            return
        self.meet("Oyster Opened")
        type.type("The " + cyan(bright("Giant Oyster")) + " has been in the back of your car. Tonight the smell is too strong. You have to deal with it.")
        print("\n")
        answer = ask.yes_or_no("Open it? ")
        if answer == "yes":
            type.type("You pry it open with your pocket knife.")
            print("\n")
            result = random.randrange(3)
            if result == 0:
                type.type("A PEARL. Massive. Perfect. Like nothing you've seen in any store.")
                print("\n")
                type.type("This is worth more than it should be to the right buyer.")
                self.add_item("Pink Pearl")
                self.change_balance(random.randint(200, 500))
                self.restore_sanity(15)
            elif result == 1:
                type.type("Two pearls. Small, mismatched, but genuine.")
                self.add_item("Matched Pearls")
                self.restore_sanity(10)
            else:
                type.type("Oyster meat. A lot of it. Briny and fresh. You eat it all.")
                self.heal(random.randint(15, 25))
                self.restore_sanity(8)
            self.use_item("Giant Oyster")
        else:
            type.type("You drive it to the water and throw it back in. It deserves better than your back seat.")
            self.restore_sanity(5)
            self.use_item("Giant Oyster")
        print("\n")
