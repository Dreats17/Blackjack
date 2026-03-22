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

class AdventuresMixin:
    """Adventure areas unlocked as the player progresses.
    
    Includes: The Road (rank 2+), Woodlands, Swamp, Beach, Underwater, City adventures
    and the final rabbit chase event.
    """

    # Modest Afternoons (10,000+)
    def road_adventure(self):
        """
        Simulates a random road adventure event, presenting narrative choices
        such as encountering street dice games, hitchhikers, shrines, a
        broken-down bus, stray dogs, or a solitary walk. Each scenario offers
        interactive decisions that affect the player's stats, inventory,
        companions, and story progression.
        """
        self.meet("Road Adventure Event")
        self.add_fatigue(random.randint(5, 10))
        type.type("You don't drive anywhere in particular. You just... drive. ")
        type.type("The wagon rattles along a stretch of highway that doesn't seem to end. ")
        type.type("No destination. No map. Just you and the dotted yellow line disappearing under your hood.")
        print("\n")
        type.type("Eventually, the gas gauge reminds you that freedom isn't free, and you pull over. ")
        type.type("But the road has something for you today.")
        print("\n")
        type.type(yellow(bright("=== THE ROAD ===")))
        print("\n")
        event = random.choice([
            "street_dice", "hitchhiker", "roadside_shrine", "broken_down_bus", "road_dog", "casual_walk"
        ])

        if event == "street_dice":
            type.type("Under an overpass, where the concrete pillars are covered in old graffiti and older prayers, you see them. ")
            type.type("Four guys hunched in a circle, sitting on milk crates and overturned buckets. ")
            type.type("The sound of dice hitting pavement echoes off the walls.")
            print("\n")
            type.type("One of them looks up. Missing teeth, sunburned face, eyes that have seen better decades. ")
            type.type("He grins.")
            print("\n")
            type.type(quote("Well, well. Another lost soul. You wanna roll, or you just here to watch us be poor?"))
            print("\n")
            type.type("The game is " + yellow(bright("Cee-lo")) + " — street dice. Three dice, simple rules. ")
            type.type("Roll 4-5-6 and you win automatically. Roll 1-2-3 and you lose automatically. ")
            type.type("Roll a pair and the odd die out is your point. Highest point wins. Trips are instant winners.")
            print("\n")
            type.type("The pot in the middle is a sad pile of crumpled bills and loose change. ")
            type.type("These guys aren't playing for glory. They're playing because it's the only game left.")
            print("\n")

            action = input("(play/watch/leave): ").strip().lower()

            if action == "play":
                type.type("You squat down and join the circle. The concrete is warm from the afternoon sun. ")
                type.type("The guy with no teeth - they call him " + cyan("Dice") + " - hands you three worn dice. One of them has a chipped corner.")
                print("\n")
                type.type(quote("Ante up. Minimum's fifty bucks. Maximum's whatever you got the guts to put down."))
                print("\n")

                try:
                    bet = int(input("Your bet: $"))
                    if bet < 50:
                        type.type("Dice shakes his head. " + quote("Fifty minimum, chief. We ain't rolling for pennies."))
                        print("\n")
                        return
                    if bet > self.get_balance():
                        type.type("Dice counts the bills you put down and laughs. " + quote("You ain't got that, brother. I can smell broke from a mile away."))
                        print("\n")
                        return
                except:
                    type.type("Dice stares at you. " + quote("You gonna bet or you gonna stutter?"))
                    print("\n")
                    return

                self.change_balance(-bet)

                # Opponent bets
                type.type("Dice matches your bet from the group pot. The other three lean in. One of them lights a cigarette that smells like regret.")
                print("\n")

                # === ROUND 1: THE ROLL ===
                type.type(yellow("=== ROUND 1: YOUR ROLL ==="))
                print("\n")
                type.type("You shake the dice in your fist. The sound is almost musical. You let them fly.")
                print("\n")

                d1, d2, d3 = random.randint(1,6), random.randint(1,6), random.randint(1,6)
                dice_sorted = sorted([d1, d2, d3])
                type.type("The dice tumble across the concrete: " + yellow(bright(str(d1) + " - " + str(d2) + " - " + str(d3))))
                print("\n")

                # Evaluate player roll
                player_result = self._evaluate_ceelo(dice_sorted)

                if player_result == "instant_win":
                    if dice_sorted == [4, 5, 6]:
                        type.type(yellow(bright("4-5-6! That's an automatic WIN!")))
                    else:
                        type.type(yellow(bright("TRIPS! " + str(dice_sorted[0]) + "-" + str(dice_sorted[1]) + "-" + str(dice_sorted[2]) + "! Automatic WIN!")))
                    print("\n")
                    type.type("Dice's jaw drops. The other three start hollering.")
                    print("\n")
                    type.type(quote("Oh you GOTTA be kidding me. First roll? FIRST ROLL?"))
                    print("\n")
                    winnings = bet * 2
                    type.type("You scoop " + green(bright("${:,}".format(winnings))) + " off the concrete.")
                    self.change_balance(winnings)
                    print("\n")

                    # Double or nothing?
                    type.type("Dice leans forward. His eyes have that look — the one you know too well.")
                    print("\n")
                    type.type(quote("Double or nothing. One more roll. You and me."))
                    print("\n")
                    again = input("(double/walk): ").strip().lower()
                    if again == "double":
                        type.type("You're both idiots. This is how it always starts.")
                        print("\n")
                        self._ceelo_showdown(bet * 2)
                    else:
                        type.type("You stand up, pocketing the cash. Dice nods slowly.")
                        print("\n")
                        type.type(quote("Smart man. Smarter than me, anyway. That's a low bar."))
                    print("\n")

                elif player_result == "instant_loss":
                    type.type(red(bright("1-2-3. Automatic LOSS.")))
                    print("\n")
                    type.type("The circle erupts. One guy slaps the concrete. Dice grins like Christmas morning.")
                    print("\n")
                    type.type(quote("Ohhh that's ROUGH, brother. The road giveth and the road taketh."))
                    print("\n")
                    type.type("Your " + red("${:,}".format(bet)) + " is gone.")
                    print("\n")

                    # Offer to try again
                    type.type("Dice sees the look on your face. He knows that look.")
                    print("\n")
                    type.type(quote("You wanna go again? Same stakes?"))
                    again = input("(again/leave): ").strip().lower()
                    if again == "again" and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        type.type("You're chasing losses under an overpass with strangers. Rock bottom has a basement.")
                        print("\n")
                        self._ceelo_showdown(bet)
                    else:
                        type.type("You stand up and dust off your knees. The concrete has left marks.")
                        print("\n")
                        type.type(quote("See you around, chief. The road always brings people back."))
                    print("\n")

                else:
                    # Player got a point
                    player_point = player_result
                    type.type("Your point is " + yellow(bright(str(player_point))) + ".")
                    print("\n")
                    type.type("Now it's Dice's turn. He blows on the dice, kisses them, whispers something you can't hear.")
                    print("\n")

                    # Dice rolls
                    self._ceelo_showdown_with_point(bet, player_point)

            elif action == "watch":
                type.type("You lean against a pillar and watch. The game is hypnotic — the rattle of dice, the slap of bills, the groans and cheers.")
                print("\n")
                type.type("Dice is good. Really good. He reads the other players like a book, knows when to push, when to fold. ")
                type.type("But even he loses sometimes. The dice don't care about skill.")
                print("\n")
                type.type("After an hour, one of the players goes bust. He stands up, stares at his empty hands, and walks away without a word. ")
                type.type("Nobody watches him go. They've all been him.")
                print("\n")
                type.type("Dice sees you watching and nods. " + quote("You learn more from the rail than the table, yunno. ") + "He flips you a coin. " + quote("For the education."))
                self.change_balance(random.randint(10, 50))
                self.restore_sanity(3)
                print("\n")

            else:
                type.type("You walk past. The sound of dice on concrete follows you for a while, then fades. ")
                type.type("Some games aren't worth playing. Some are.")
                print("\n")

        elif event == "hitchhiker":
            type.type("You spot her on the shoulder of the road about a quarter mile ahead. Thumb out, backpack sagging, hair whipping in the wind from passing trucks.")
            print("\n")
            type.type("As you get closer, you can see she's young — maybe 19, maybe 25, hard to tell. Sun-worn. Road-worn. Life-worn.")
            print("\n")
            type.type("She sees your wagon slowing down and her face does that thing — hope battling with the knowledge that hope is dangerous.")
            print("\n")
            action = input("(stop/honk/drive_past): ").strip().lower()

            if action == "stop":
                type.type("You pull over. She jogs up, opens the door, and slides in before you can change your mind.")
                print("\n")
                type.type(quote("Thanks. Name's Marla. I've been out here since dawn."))
                print("\n")
                type.type("She smells like sunscreen and gas station coffee. Her backpack clinks with what sounds like canned food.")
                print("\n")
                type.type(quote("Where you headed?"))
                print("\n")
                type.type("You tell her the truth. Nowhere. Everywhere. The casino, eventually.")
                print("\n")
                type.type("She laughs. It sounds like it surprises her.")
                print("\n")
                type.type(quote("A gambler, huh? My dad was a gambler. Lost everything. The house, the car, us. "))
                type.type(quote("He used to say the next hand would fix everything. It never did."))
                print("\n")
                type.type("The car is quiet for a while. Just the engine and the road.")
                print("\n")
                type.type(quote("You can drop me at the next town. There's a shelter there I've been to before. They know me."))
                print("\n")
                type.type("What do you do?")
                print("\n")
                action2 = input("(drop_her_off/give_money/offer_food/talk_more): ").strip().lower()

                if action2 == "give_money":
                    type.type("You pull out some cash. She stares at it.")
                    print("\n")
                    amount = random.choice([50, 100, 200])
                    type.type(quote("I can't take that."))
                    print("\n")
                    type.type(quote("Yeah you can."))
                    print("\n")
                    type.type("She takes it. Folds it carefully. Puts it in her shoe — not her pocket. She's been robbed before.")
                    self.change_balance(-amount)
                    print("\n")
                    type.type(quote("You're not like my dad. He never gave anything away. Just took and took and took."))
                    print("\n")
                    type.type("She gets out at the next town. Waves once. Disappears into a building with no sign on it.")
                    print("\n")
                    type.type("You drive back feeling lighter. Or heavier. Hard to tell the difference sometimes.")
                    self.restore_sanity(8)
                    print("\n")

                elif action2 == "offer_food":
                    if self.has_item("Turkey Sandwich") or self.has_item("Beef Jerky") or self.has_item("Granola Bar"):
                        food = None
                        if self.has_item("Turkey Sandwich"):
                            food = "Turkey Sandwich"
                        elif self.has_item("Beef Jerky"):
                            food = "Beef Jerky"
                        else:
                            food = "Granola Bar"
                        type.type("You hand her your " + magenta(bright(food)) + ". She unwraps it immediately and eats like she hasn't in days. Because she probably hasn't.")
                        self.use_item(food)
                        print("\n")
                        type.type(quote("God, that's good. You have no idea."))
                        print("\n")
                        type.type("She finishes every crumb. Wipes her mouth with the back of her hand. Looks at you like you just saved her life. Maybe you did.")
                        self.restore_sanity(5)
                    else:
                        type.type("You don't have any food to give. She notices you checking your pockets and shakes her head.")
                        print("\n")
                        type.type(quote("It's okay. I'm used to it."))
                        print("\n")
                        type.type("That sentence hits harder than it should.")
                    print("\n")
                    type.type("You drop her off at the shelter. She thanks you quietly and walks inside.")
                    self.restore_sanity(3)
                    print("\n")

                elif action2 == "talk_more":
                    type.type("You drive slow. She talks. You listen.")
                    print("\n")
                    type.type("She tells you about her father. How he'd come home at 4 AM smelling like cigarettes and carpet cleaner — the casino kind. ")
                    type.type("How her mother would be asleep on the couch with the TV on, pretending she hadn't been waiting up. ")
                    type.type("How one day he just didn't come home at all.")
                    print("\n")
                    type.type(quote("I think he loved the cards more than us. Not because he was a bad person. "))
                    type.type(quote("Because the cards never asked him to be better. They just let him be."))
                    print("\n")
                    type.type("You don't say anything. What could you say?")
                    print("\n")
                    type.type("She gets out at the shelter. Pauses with the door open.")
                    print("\n")
                    type.type(quote("Hey. Whatever you're running from — it'll still be there when the money runs out. You know that, right?"))
                    print("\n")
                    type.type("The door closes. You sit there for a long time before you start driving again.")
                    self.restore_sanity(12)
                    self.add_fatigue(5)
                    print("\n")

                else:
                    type.type("You drop her at the shelter. She thanks you, grabs her backpack, and disappears inside. ")
                    type.type("Simple. Clean. No strings.")
                    print("\n")
                    type.type("You drive away wondering if that's what kindness is supposed to feel like — easy and forgettable. ")
                    type.type("You hope it's not forgettable for her.")
                    self.restore_sanity(3)
                    print("\n")

            elif action == "honk":
                type.type("You lay on the horn as you pass. She flinches, then flips you off with both hands.")
                print("\n")
                type.type("Fair enough.")
                print("\n")
                type.type("In the rearview mirror, she's already got her thumb back out. Resilient. More than you, probably.")
                print("\n")

            else:
                type.type("You drive past. Don't even slow down. Her face blurs into all the other faces you've driven past.")
                print("\n")
                type.type("A mile later, you pull over anyway. Not to go back. Just to sit there and wonder what kind of person you're becoming.")
                print("\n")
                type.type("The engine idles. You idle with it.")
                self.drain_sanity(3)
                print("\n")

        elif event == "roadside_shrine":
            type.type("You almost miss it. A small wooden cross on the shoulder, surrounded by plastic flowers that have faded from red to pink to almost white. ")
            type.type("Someone died here. A long time ago, judging by the state of things.")
            print("\n")
            type.type("But there's something else. Behind the cross, half-hidden by weeds, is a stone. ")
            type.type("Not a gravestone. Something older. Smoother. Covered in symbols you don't recognize.")
            print("\n")
            type.type("The air around it feels... thick. Heavy. Like the space between heartbeats.")
            print("\n")
            type.type(yellow("=== ROADSIDE SHRINE ==="))
            print("\n")
            action = input("(touch_stone/pray/leave_offering/read_symbols/walk_away): ").strip().lower()

            if action == "touch_stone":
                type.type("You reach out. Your fingertips brush the surface.")
                print("\n")
                type.type("The world... stutters. Like a skipping record. For half a second, you're somewhere else — a road that stretches forever, ")
                type.type("lined with the ghosts of every car that ever broke down, every driver who ever got lost, every passenger who was never found.")
                print("\n")
                outcome = random.randrange(4)
                if outcome == 0:
                    type.type("The vision breaks. You're back. But something is different — you feel LUCKY. Impossibly, dangerously lucky. ")
                    type.type("Like the road itself has decided to protect you. For now.")
                    self.add_status("Road Blessed")
                    self.heal(random.randint(15, 30))
                    print("\n")
                elif outcome == 1:
                    type.type("The stone burns. You yank your hand back. There's a mark on your palm — a symbol that fades even as you watch it.")
                    print("\n")
                    type.type("Your head pounds. Your vision swims. Something was given to you, but something was also taken.")
                    self.drain_sanity(random.randint(5, 10))
                    self.change_balance(random.randint(1000, 5000))
                    print("\n")
                elif outcome == 2:
                    type.type("Nothing happens. The stone is just a stone. Or maybe it already gave you what it wanted to give, and you won't know until later.")
                    print("\n")
                else:
                    type.type("A voice. In your skull, not your ears. One word, in a language you don't speak but somehow understand:")
                    print("\n")
                    type.slow(yellow(bright("\"ENDURE.\"")))
                    print("\n")
                    type.type("The mark fades. You feel healed. Changed. Afraid. All at once.")
                    self.heal(random.randint(30, 50))
                    self.restore_sanity(10)
                    print("\n")

            elif action == "pray":
                type.type("You kneel. You're not sure who you're praying to — God, the universe, the road, whoever left that cross here. ")
                type.type("It doesn't matter. The act of kneeling is what matters.")
                print("\n")
                type.type("You close your eyes. For a moment, everything is still. No wind. No traffic. No thoughts.")
                print("\n")
                if random.random() < 0.5:
                    type.type("When you open your eyes, there's a coin on the stone that wasn't there before. Old. Heavy. Warm.")
                    print("\n")
                    type.type("You pocket it. It feels like permission.")
                    self.change_balance(random.randint(500, 2000))
                    self.restore_sanity(8)
                else:
                    type.type("When you open your eyes, nothing has changed. But you feel lighter. The weight you've been carrying — some of it is gone.")
                    print("\n")
                    type.type("Not all of it. Never all of it. But enough to keep walking.")
                    self.restore_sanity(15)
                    self.heal(random.randint(10, 20))
                print("\n")

            elif action == "leave_offering":
                type.type("You dig through your pockets. What do you leave?")
                print("\n")
                if self.get_balance() >= 100:
                    type.type("You lay a hundred-dollar bill under the cross. The wind tries to take it, but it stays. Like it's supposed to be there.")
                    self.change_balance(-100)
                    print("\n")
                    if random.random() < 0.6:
                        type.type("The plastic flowers seem to get a little brighter. Probably the sunlight. Probably.")
                        print("\n")
                        type.type("As you walk back to your wagon, you find something in the grass — a keychain with a small rabbit's foot attached. Lucky, supposedly.")
                        self.add_item("Road Talisman")
                        self.restore_sanity(5)
                    else:
                        type.type("Nothing happens. The money sits there. The dead stay dead. But you did a decent thing, and maybe that's worth more than whatever you could've bought with it.")
                        self.restore_sanity(8)
                else:
                    type.type("You don't have anything worth leaving. You stand there, empty-pocketed, feeling useless.")
                    print("\n")
                    type.type("You leave a pebble instead. It's the thought that counts. It has to be.")
                    self.restore_sanity(3)
                print("\n")

            elif action == "read_symbols":
                type.type("You squat down and study the stone. The symbols are worn, but you can make out patterns — circles within circles, lines that branch like trees or veins or cracks in the road.")
                print("\n")
                type.type("You pull out your phone to take a picture, but the camera refuses to focus. The symbols seem to shift when you look at them from different angles.")
                print("\n")
                if random.random() < 0.4:
                    type.type("Then you see it. One symbol you recognize — it's the same shape as the crack in your windshield. The exact same shape.")
                    print("\n")
                    type.type("Your blood runs cold. You back away from the stone.")
                    print("\n")
                    type.type("Some things are better left unread.")
                    self.drain_sanity(5)
                else:
                    type.type("After a while, they start to look like directions. A map, maybe. Or a warning. Hard to tell the difference on the road.")
                    print("\n")
                    type.type("You memorize what you can and head back. The symbols stay in your head all day, rearranging themselves behind your eyelids.")
                    self.restore_sanity(3)
                print("\n")

            else:
                type.type("You leave the shrine alone. Some things are sacred. Some things are dangerous. Some things are both, and you're too tired to figure out which.")
                print("\n")
                type.type("The plastic flowers watch you go. Or they don't. They're plastic flowers. Get a grip.")
                print("\n")

        elif event == "broken_down_bus":
            type.type("A Greyhound bus sits dead on the shoulder, hazard lights blinking weakly. The driver is on the hood, staring at the engine like it owes him money.")
            print("\n")
            type.type("About fifteen passengers are scattered along the roadside. Some sitting on luggage, some pacing, some arguing into phones that may or may not have signal.")
            print("\n")
            type.type("A woman with two kids is trying to keep them from running into traffic. An old man is asleep against the rear tire. A teenager is filming everything for social media.")
            print("\n")
            type.type("The driver sees you and waves you over.")
            print("\n")
            type.type(quote("Hey! Hey, you got jumper cables? A phone? Anything?"))
            print("\n")
            action = input("(help/sell_water/entertain/rob/ignore): ").strip().lower()

            if action == "help":
                type.type("You pull over and pop your hood. Between your wagon and the bus, maybe you can jury-rig something.")
                print("\n")
                if self.has_item("Duct Tape") or self.has_item("Tool Kit"):
                    tool = "Tool Kit" if self.has_item("Tool Kit") else "Duct Tape"
                    type.type("Your " + magenta(bright(tool)) + " comes in handy. You and the driver spend an hour under the hood, ")
                    type.type("sweating, cursing, and performing what can only be described as mechanical prayer.")
                    print("\n")
                    type.type("The engine coughs. Sputters. Then ROARS to life. The passengers cheer. The driver grabs your hand and shakes it like he's trying to detach it.")
                    print("\n")
                    type.type(quote("You're a goddamn saint! Here — the passengers pooled together."))
                    print("\n")
                    tip = random.randint(200, 800)
                    type.type("He presses " + green(bright("${:,}".format(tip))) + " into your palm.")
                    self.change_balance(tip)
                    self.restore_sanity(10)
                    print("\n")
                    type.type("The woman with the kids mouths " + quote("thank you") + " through the window as the bus pulls away. ")
                    type.type("The old man is still asleep.")
                    print("\n")
                else:
                    type.type("You don't have any tools, but you try anyway. You stare at the engine. It stares back.")
                    print("\n")
                    type.type("After twenty minutes of pretending you know what you're doing, a tow truck arrives. The driver thanks you for trying.")
                    print("\n")
                    type.type(quote("Effort counts for something, man. Here."))
                    tip = random.randint(50, 150)
                    type.type("He gives you " + green(bright("$" + str(tip))) + ".")
                    self.change_balance(tip)
                    self.restore_sanity(5)
                print("\n")

            elif action == "sell_water":
                type.type("You have a case of bottled water in the back of the wagon. It's warm, but it's wet.")
                print("\n")
                type.type("The sun is brutal. These people are desperate. You could be a saint or an entrepreneur.")
                print("\n")
                type.type("How much per bottle?")
                print("\n")
                price_choice = input("($1/free/$5): ").strip().lower()
                if price_choice == "free":
                    type.type("You hand out water to everyone who needs it. The mother almost cries. The old man wakes up long enough to drink and nod at you before falling back asleep.")
                    print("\n")
                    type.type("The teenager films you and calls you " + quote("lowkey a W human being") + " to his 47 followers.")
                    print("\n")
                    type.type("You don't get paid, but something in your chest unclenches. Something you didn't know was tight.")
                    self.restore_sanity(15)
                    self.heal(random.randint(5, 10))
                    print("\n")
                elif price_choice == "$5":
                    type.type("Five bucks a bottle in this heat. You're not proud of it.")
                    print("\n")
                    type.type("Most of them pay. The mother hesitates. You watch her count coins. She buys one bottle and splits it between her two kids.")
                    print("\n")
                    earnings = random.randint(40, 75)
                    type.type("You make " + green(bright("$" + str(earnings))) + ". It feels like less than that.")
                    self.change_balance(earnings)
                    self.drain_sanity(5)
                    print("\n")
                else:
                    type.type("A dollar a bottle. Fair. Human. The passengers are grateful without being indebted. The driver buys three.")
                    print("\n")
                    earnings = random.randint(12, 20)
                    type.type("You make " + green(bright("$" + str(earnings))) + " and a clean conscience.")
                    self.change_balance(earnings)
                    self.restore_sanity(5)
                    print("\n")

            elif action == "entertain":
                type.type("You don't have cables or tools, but you've got a mouth and too much free time. You start talking to people.")
                print("\n")
                if self.has_item("Deck of Cards"):
                    type.type("You pull out your " + magenta(bright("Deck of Cards")) + " and start doing tricks for the kids. They're terrible tricks, but the kids don't know that.")
                    print("\n")
                    type.type("The mother laughs — a real laugh, not the polite kind. The teenager puts his phone down. The old man opens one eye and smirks.")
                    print("\n")
                    type.type("You spend an hour doing card tricks, telling road stories, and making an old man laugh so hard he coughs.")
                    print("\n")
                    type.type("When the tow truck finally comes, the mother presses something into your hand. " + quote("For being kind when you didn't have to be."))
                    tip = random.randint(100, 300)
                    self.change_balance(tip)
                    self.restore_sanity(12)
                    print("\n")
                else:
                    type.type("You tell stories. Road stories. Gambling stories. The one about the time you almost hit a deer at 3 AM. ")
                    type.type("The one about the Dealer who definitely wanted to kill you.")
                    print("\n")
                    type.type("People listen. Not because the stories are good, but because waiting is worse than listening.")
                    print("\n")
                    type.type("The tow truck comes. People disperse. Nobody tips you, but the old man winks as he boards the replacement bus.")
                    self.restore_sanity(6)
                print("\n")

            elif action == "rob":
                type.type("The luggage is just sitting there. Unattended. Everyone's distracted.")
                print("\n")
                type.type("You don't think about it. You just do it. Grab a bag, walk to your wagon, and drive.")
                print("\n")
                if random.random() < 0.6:
                    type.type("Nobody notices. Or if they do, they're too exhausted to chase you.")
                    print("\n")
                    loot = random.randint(100, 500)
                    type.type("Inside the bag: clothes you'll never wear, a phone charger, and " + green(bright("$" + str(loot))) + " in a wallet.")
                    self.change_balance(loot)
                    self.drain_sanity(10)
                    print("\n")
                    type.type("You drive away fast. The rearview mirror shows you the mother, still trying to keep her kids safe, now with one less bag.")
                    print("\n")
                    type.type("The guilt hits about three miles later. It doesn't leave.")
                    print("\n")
                else:
                    type.type("The teenager sees you. " + quote("YO! THAT GUY'S STEALING!"))
                    print("\n")
                    type.type("The driver — who is apparently built like a linebacker in his spare time — tackles you before you reach your wagon.")
                    self.hurt(random.randint(15, 30))
                    self.drain_sanity(8)
                    print("\n")
                    type.type("He takes the bag back. The passengers stare at you with a mixture of disgust and pity. ")
                    type.type("You slink back to your wagon and drive away, bruised in more ways than one.")
                    print("\n")

            else:
                type.type("You drive past. Fifteen people watch your taillights disappear.")
                print("\n")
                type.type("None of them are surprised. This is what the road teaches you — most people keep going.")
                print("\n")

        elif event == "road_dog":
            type.type("You see it from a hundred yards away. A dog, walking the white line of the road like it's a tightrope. Methodical. Patient. Alone.")
            print("\n")
            type.type("It's a mutt — some kind of shepherd mix, big paws, one ear up and one ear down. Ribs showing. ")
            type.type("But it's not running. Not scared. Just... walking. Like it has somewhere to be.")
            print("\n")

            if self.has_item("Animal Whistle") and not self.has_companion("Asphalt"):
                type.type("The " + magenta(bright("Animal Whistle")) + " vibrates in your pocket. Not a song this time — a low, steady hum. Like a heartbeat.")
                print("\n")
                type.type("You pull over. The dog stops. Turns its head. Looks at you with one brown eye and one blue eye.")
                print("\n")
                type.type("You get out of the wagon. The dog doesn't run. Doesn't flinch. Just waits, like it's been waiting for exactly you.")
                print("\n")
                type.type("You kneel. The dog walks over, slow and deliberate, and sits at your feet. Its tail wags once. Twice. Then it presses its head into your palm.")
                print("\n")
                type.type("This dog has walked a thousand miles. You can see it in the pads of its paws, worn smooth as river stones. ")
                type.type("It chose the road a long time ago. Just like you.")
                print("\n")
                type.type("You call it " + cyan(bright("Asphalt")) + ". Because that's where you found each other.")
                print("\n")
                type.type("Asphalt hops into the wagon like he's done it before. He curls up in the passenger seat, sighs once, and closes his eyes. ")
                type.type("Home isn't a place. It's whoever stops for you.")
                self.add_companion("Asphalt", "Dog")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                self.restore_sanity(10)
                print("\n")
                return

            type.type("You slow down. The dog glances at your wagon, considers it, and keeps walking. It has its own business.")
            print("\n")
            action = input("(stop/toss_food/follow/drive_past): ").strip().lower()

            if action == "stop":
                type.type("You pull over and get out. The dog stops and watches you from twenty feet away.")
                print("\n")
                type.type("You crouch. Hold out your hand. The universal language of " + quote("I'm not gonna hurt you."))
                print("\n")
                if random.random() < 0.5:
                    type.type("The dog approaches. Sniffs your hand. Licks it once.")
                    print("\n")
                    type.type("Then it turns and keeps walking. It wasn't looking for a friend. It was just being polite.")
                    print("\n")
                    type.type("You watch it disappear around a bend. Some things walk alone by choice. You understand that.")
                    self.restore_sanity(5)
                else:
                    type.type("The dog comes all the way over. Sits at your feet. You scratch behind its one-up ear and it leans into it.")
                    print("\n")
                    type.type("It follows you back to the wagon. Hops in the passenger seat.")
                    print("\n")
                    type.type("It stays with you for the drive back. When you park, it gets out, stretches, and trots off into the brush without looking back.")
                    print("\n")
                    type.type("You sit there for a minute, staring at the warm spot it left in the seat.")
                    self.restore_sanity(8)
                    self.heal(random.randint(5, 10))
                print("\n")

            elif action == "toss_food":
                if self.has_item("Beef Jerky") or self.has_item("Hot Dog"):
                    food = "Beef Jerky" if self.has_item("Beef Jerky") else "Hot Dog"
                    type.type("You toss your " + magenta(bright(food)) + " out the window. The dog stops, sniffs, and eats it in two bites.")
                    self.use_item(food)
                    print("\n")
                    type.type("It looks at your wagon. Looks at the road. Looks back at your wagon.")
                    print("\n")
                    type.type("It chooses the road. But it barks once — a thank-you bark, if such a thing exists.")
                    self.restore_sanity(5)
                else:
                    type.type("You don't have anything to toss. You make throwing motions out the window anyway. The dog is not fooled.")
                print("\n")

            elif action == "follow":
                type.type("You idle the wagon behind the dog, matching its pace. Five miles an hour. ")
                type.type("The dog doesn't seem to mind. Or maybe it doesn't care.")
                print("\n")
                type.type("You follow it for almost a mile before it turns off the road and disappears into a field. ")
                type.type("For a second, silhouetted against the sky, it looks like every dog from every painting of loneliness you've ever seen.")
                print("\n")
                type.type("Then it's gone. And you're alone on the road again. Same as always.")
                self.restore_sanity(3)
                self.add_fatigue(3)
                print("\n")

            else:
                type.type("You drive past. The dog doesn't watch you go. It's already looking ahead. ")
                type.type("Road dogs don't look back. Maybe you should learn from that.")
                print("\n")

        else:
            # casual_walk
            type.type("You walk along the shoulder of the road for a while. No destination. No purpose. Just movement for the sake of movement.")
            print("\n")
            type.type("A semi blows past and nearly takes your hat off. A crow watches you from a power line. ")
            type.type("Somewhere in the distance, a train horn sounds — long and low and full of places you'll never go.")
            print("\n")
            type.type("You find a guardrail and sit on it. The metal is warm from the sun. ")
            type.type("You watch the heat shimmer on the asphalt and think about all the people driving past who have somewhere to be. ")
            type.type("Houses. Jobs. Families.")
            print("\n")
            type.type("You have a wagon with a cracked windshield and a gambling problem. But you also have this — ")
            type.type("a warm guardrail, a patient crow, and an afternoon that belongs to nobody but you.")
            print("\n")
            type.type("Sometimes that's enough. Not often. But sometimes.")
            self.heal(random.randint(10, 25))
            self.restore_sanity(random.randint(5, 10))
            print("\n")

    def _evaluate_ceelo(self, dice_sorted):
        """Evaluate a Cee-lo roll. Returns 'instant_win', 'instant_loss', or the point value (1-6)."""
        d1, d2, d3 = dice_sorted
        # 4-5-6 = instant win
        if dice_sorted == [4, 5, 6]:
            return "instant_win"
        # 1-2-3 = instant loss
        if dice_sorted == [1, 2, 3]:
            return "instant_loss"
        # Trips = instant win
        if d1 == d2 == d3:
            return "instant_win"
        # Pair + point
        if d1 == d2:
            return d3
        if d2 == d3:
            return d1
        if d1 == d3:
            return d2
        # No pair, no sequence = re-roll (meaningless, treat as low point)
        return 0

    def _ceelo_showdown(self, pot):
        """A full Cee-lo showdown round — both roll, compare results."""
        type.type(yellow("=== SHOWDOWN ==="))
        print("\n")

        # Player roll
        type.type("You shake and throw.")
        print("\n")
        p1, p2, p3 = random.randint(1,6), random.randint(1,6), random.randint(1,6)
        p_sorted = sorted([p1, p2, p3])
        type.type("Your dice: " + yellow(bright(str(p1) + " - " + str(p2) + " - " + str(p3))))
        print("\n")
        p_result = self._evaluate_ceelo(p_sorted)

        # Opponent roll
        type.type("Dice blows on his knuckles, rattles the dice, and lets 'em fly.")
        print("\n")
        o1, o2, o3 = random.randint(1,6), random.randint(1,6), random.randint(1,6)
        o_sorted = sorted([o1, o2, o3])
        type.type("Dice's dice: " + red(bright(str(o1) + " - " + str(o2) + " - " + str(o3))))
        print("\n")
        o_result = self._evaluate_ceelo(o_sorted)

        # Compare
        self._ceelo_compare(p_result, o_result, pot)

    def _ceelo_showdown_with_point(self, pot, player_point):
        """Opponent rolls against the player's established point."""
        # Opponent may need multiple rolls to establish a point
        max_rolls = 3
        for i in range(max_rolls):
            o1, o2, o3 = random.randint(1,6), random.randint(1,6), random.randint(1,6)
            o_sorted = sorted([o1, o2, o3])
            type.type("Dice rolls: " + red(bright(str(o1) + " - " + str(o2) + " - " + str(o3))))
            print("\n")
            o_result = self._evaluate_ceelo(o_sorted)

            if o_result == "instant_win":
                type.type(red(bright("Dice hits an automatic winner!")))
                print("\n")
                type.type(quote("Read 'em and weep, chief."))
                print("\n")
                type.type("Your " + red("${:,}".format(pot)) + " belongs to the concrete now.")
                print("\n")
                return
            elif o_result == "instant_loss":
                type.type(yellow(bright("Dice rolls 1-2-3! Automatic LOSS!")))
                print("\n")
                type.type("Dice slams his palm on the ground. " + quote("Are you SERIOUS right now?!"))
                print("\n")
                winnings = pot * 2
                type.type("You scoop " + green(bright("${:,}".format(winnings))) + " off the ground.")
                self.change_balance(winnings)
                print("\n")
                return
            elif o_result == 0:
                if i < max_rolls - 1:
                    type.type("No point. Dice rolls again.")
                    print("\n")
                else:
                    type.type("No point after three rolls. " + quote("Dice forfeits!"))
                    print("\n")
                    winnings = pot * 2
                    type.type("You win " + green(bright("${:,}".format(winnings))) + " by default!")
                    self.change_balance(winnings)
                    print("\n")
                    return
            else:
                opponent_point = o_result
                type.type("Dice's point: " + red(bright(str(opponent_point))))
                print("\n")
                if player_point > opponent_point:
                    type.type(yellow(bright(str(player_point) + " beats " + str(opponent_point) + "! You WIN!")))
                    print("\n")
                    type.type("Dice shakes his head. " + quote("Man. You got the touch today."))
                    print("\n")
                    winnings = pot * 2
                    type.type("You collect " + green(bright("${:,}".format(winnings))) + ".")
                    self.change_balance(winnings)
                elif player_point < opponent_point:
                    type.type(red(bright(str(opponent_point) + " beats " + str(player_point) + ". You LOSE.")))
                    print("\n")
                    type.type(quote("Better luck next time, chief. The road's always here."))
                    print("\n")
                    type.type("Your " + red("${:,}".format(pot)) + " is gone.")
                else:
                    type.type(cyan(bright("Tied! " + str(player_point) + " vs " + str(opponent_point) + ". Push — money goes back.")))
                    print("\n")
                    type.type(quote("A tie? On the ROAD? That's gotta be an omen."))
                    self.change_balance(pot)
                print("\n")
                return

    def _ceelo_compare(self, p_result, o_result, pot):
        """Compare two Cee-lo results and resolve the pot."""
        # Both instant
        if p_result == "instant_win" and o_result == "instant_win":
            type.type(cyan(bright("DOUBLE AUTOMATICS! It's a push!")))
            print("\n")
            type.type(quote("I ain't never seen that before. Take your money back."))
            self.change_balance(pot)
            print("\n")
            return
        if p_result == "instant_win":
            type.type(yellow(bright("Your automatic beats everything!")))
            print("\n")
            winnings = pot * 2
            type.type("You collect " + green(bright("${:,}".format(winnings))) + "!")
            self.change_balance(winnings)
            print("\n")
            return
        if o_result == "instant_win":
            type.type(red(bright("Dice hits an automatic winner. You're done.")))
            print("\n")
            type.type(quote("Nothing personal, chief. Just dice."))
            print("\n")
            return
        if p_result == "instant_loss" and o_result == "instant_loss":
            type.type(cyan(bright("You BOTH rolled 1-2-3?! Push!")))
            type.type(quote("The road is drunk today."))
            self.change_balance(pot)
            print("\n")
            return
        if p_result == "instant_loss":
            type.type(red(bright("Your 1-2-3 is an automatic loss.")))
            print("\n")
            return
        if o_result == "instant_loss":
            type.type(yellow(bright("Dice rolls 1-2-3! You win!")))
            winnings = pot * 2
            self.change_balance(winnings)
            print("\n")
            return

        # Both got points (or 0)
        p_val = p_result if isinstance(p_result, int) else 0
        o_val = o_result if isinstance(o_result, int) else 0
        if p_val > o_val:
            type.type(yellow(bright(str(p_val) + " beats " + str(o_val) + "! You WIN!")))
            print("\n")
            winnings = pot * 2
            type.type("You take " + green(bright("${:,}".format(winnings))) + ".")
            self.change_balance(winnings)
        elif o_val > p_val:
            type.type(red(bright(str(o_val) + " beats " + str(p_val) + ". You lose.")))
            print("\n")
            type.type(quote("Tough break, brother."))
        else:
            type.type(cyan(bright("Tied at " + str(p_val) + ". Push.")))
            self.change_balance(pot)
        print("\n")

    # Nearly There Nights (900,000+)
    def woodlands_adventure(self):
        """
        Handles a random narrative event in the woodlands, presenting the player
        with unique scenarios such as a hunting competition, a legendary bear
        encounter, a mystical fountain, or a hermit’s cabin. Each event offers
        interactive choices that can affect the player's status, inventory,
        health, and balance, with outcomes determined by user input and random
        chance.
        """
        self.meet("Woodlands Adventure Event")
        self.add_fatigue(random.randint(8, 15))  # Trekking through the woods
        type.type("The forest is different tonight. Older. Deeper. The trees seem to lean in, listening. An owl hoots three times - an omen, the old folks say.")
        print("\n")
        type.type("You sense this night will be... significant.")
        print("\n")
        type.type(yellow(bright("=== WOODLANDS ADVENTURE ===")))
        print("\n")
        if self.has_item("Rusty Compass") or self.has_item("Golden Compass"):
            compass = "Golden Compass" if self.has_item("Golden Compass") else "Rusty Compass"
            type.type("The " + cyan(bright(compass)) + " needle spins wildly, then points east with sudden certainty.")
            print("\n")
            type.type("Something valuable lies in that direction. The compass knows things you don't.")
            self.restore_sanity(3)
            print("\n")
        event = random.choice([
            "hunting_competition", "gigantic_bear", "fountain_of_youth", "hermit_cabin", "casual_day"
        ])
        
        if event == "hunting_competition":
            type.type("Torchlight flickers through the trees. ")
            type.type("You follow it to a clearing where a dozen hunters have gathered, their faces hard and weathered. ")
            type.type("A man with a scar across his eye addresses the crowd.")
            print("\n")
            type.type(quote("The Midnight Hunt begins. Last one standing with a trophy wins the pot. "))
            type.type(quote("Entry fee is $5,000. Rules are simple: no killing other hunters. Everything else is fair game."))
            print("\n")
            type.type("The pot looks huge. Do you enter the competition, bet on a hunter, or just observe?")
            print("\n")
            action = input("(enter/bet/observe): ").strip().lower()
            
            if action == "enter":
                if self.get_balance() >= 5000:
                    self.change_balance(-5000)
                    type.type("You pay the entry fee and receive a hunting knife. The other hunters size you up - most of them dismiss you immediately. Their mistake.")
                    print("\n")
                    type.type(yellow("=== ROUND 1: THE STALKING ==="))
                    print("\n")
                    type.type("You split off into the darkness. The forest is alive with sounds - animals, or other hunters pretending to be animals. You spot movement ahead.")
                    print("\n")
                    type.type("Do you track it, set a trap, or climb a tree for a better view?")
                    r1 = input("(track/trap/climb): ").strip().lower()
                    
                    hunter_score = 0
                    
                    if r1 == "track":
                        if random.random() < 0.5:
                            type.type("You move silently through the underbrush, following the trail. It's a deer - a big one. You mark its position.")
                            hunter_score += 1
                        else:
                            type.type("You follow the movement right into another hunter's trap. You escape, but you've wasted valuable time.")
                    elif r1 == "trap":
                        if random.random() < 0.4:
                            type.type("You rig a snare using vines and your knife. Within an hour, you've caught a rabbit. Small, but it counts.")
                            hunter_score += 1
                        else:
                            type.type("Your trap fails. You're losing time.")
                    else:
                        if random.random() < 0.6:
                            type.type("From the tree, you spot a wild boar rooting in a clearing. You mark the location and climb down.")
                            hunter_score += 2
                        else:
                            type.type("You climb, but the branches are rotten. You fall and make a ton of noise. Every animal in a mile radius knows where you are.")
                    
                    print("\n")
                    type.type(yellow("=== ROUND 2: THE KILL ==="))
                    print("\n")
                    type.type("Dawn approaches. You need to make your move. You've tracked your prey to a clearing. Other hunters are closing in - you can hear them.")
                    print("\n")
                    type.type("Do you rush in now, wait for the perfect moment, or try to sabotage another hunter?")
                    r2 = input("(rush/wait/sabotage): ").strip().lower()
                    
                    if r2 == "rush":
                        if random.random() < 0.4:
                            type.type("You burst into the clearing, knife raised. The animal bolts - but you're faster. You bring it down with a single strike.")
                            hunter_score += 2
                        else:
                            type.type("You rush in and spook everything. The animals scatter. Empty-handed.")
                    elif r2 == "wait":
                        if random.random() < 0.6:
                            type.type("Patience pays off. Another hunter rushes in, spooks the prey, and it runs directly into your path. Easy kill.")
                            hunter_score += 2
                        else:
                            type.type("You wait too long. Someone else makes the kill.")
                    else:
                        if random.random() < 0.5:
                            type.type("You throw a rock, mimicking an animal call. Another hunter takes the bait, chasing a phantom while you snag the real prize.")
                            hunter_score += 2
                        else:
                            type.type("The hunter you tried to trick isn't stupid. He catches on and now you've made an enemy.")
                            self.hurt(random.randint(10, 20))
                    
                    print("\n")
                    type.type(yellow("=== FINAL JUDGMENT ==="))
                    print("\n")
                    
                    if hunter_score >= 3:
                        type.type("The hunters gather as dawn breaks. You present your trophies. The scarred man nods, impressed.")
                        print("\n")
                        type.type(quote("We have a winner."))
                        print("\n")
                        winnings = random.randint(15000, 40000)
                        type.type("You collect " + green(bright("$" + str(winnings))) + " and the respect of the hunting community.")
                        self.change_balance(winnings)
                        self.add_item("Hunter's Mark")
                    elif hunter_score >= 1:
                        type.type("You didn't win, but you didn't embarrass yourself either. You place third and receive a consolation prize.")
                        winnings = random.randint(3000, 8000)
                        self.change_balance(winnings)
                    else:
                        type.type("You return empty-handed. The other hunters laugh. The scarred man shakes his head.")
                        print("\n")
                        type.type(quote("Stick to the city, friend."))
                    print("\n")
                else:
                    type.type("You don't have the entry fee. The scarred man waves you off dismissively.")
                    print("\n")
            
            elif action == "bet":
                type.type("You study the hunters - their gear, their posture, their eyes. One looks particularly dangerous.")
                print("\n")
                type.type("How much do you bet? ($1000 minimum)")
                try:
                    bet = int(input("Bet amount: $"))
                    if bet >= 1000 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        type.type("You place your bet and watch the hunt from the treeline...")
                        print("\n")
                        if random.random() < 0.45:
                            winnings = bet * 3
                            type.type("Your hunter wins! You collect " + green(bright("$" + str(winnings))) + "!")
                            self.change_balance(winnings)
                        else:
                            type.type("Your hunter comes up empty. There goes your money.")
                    else:
                        type.type("You can't afford that bet, or it's below the minimum.")
                except:
                    type.type("The betting window closes. You missed your chance.")
                print("\n")
            
            else:
                type.type("You watch from the shadows. The hunt is brutal, elegant, primal. You learn things about tracking you never knew.")
                self.add_status("Tracker's Eye")
                print("\n")
        
        elif event == "gigantic_bear":
            type.type("You hear it before you see it. Branches snapping. The ground shaking. ")
            type.type("Then it emerges from the darkness - a bear the size of a truck, its eyes glowing amber in the moonlight. ")
            type.type("This isn't a normal bear. This is something OLD.")
            print("\n")
            
            # Animal Whistle can befriend even legendary beasts
            if self.has_item("Animal Whistle") and not self.has_companion("Ursus"):
                type.type("The " + magenta(bright("Animal Whistle")) + " begins to glow, brighter than you've ever seen. ")
                type.type("The air hums with ancient power.")
                print("\n")
                type.type("The massive bear stops. Its glowing eyes fix on you, but there's no aggression - only recognition.")
                print("\n")
                type.type("It approaches slowly, each step making the earth tremble. When it reaches you, it lowers its enormous head.")
                print("\n")
                type.type("You place your hand on its snout. Warm. Real. Alive. The bear closes its eyes and makes a sound - ")
                type.type("deep and resonant, like the voice of the forest itself.")
                print("\n")
                type.type("You've just bonded with a bear of legend. You call it " + cyan(bright("Ursus")) + " - the Bear King.")
                print("\n")
                type.type("Ursus will walk with you now. Where you go, the wild things will know you. Where you sleep, nothing will dare harm you.")
                self.add_companion("Ursus", "Giant Bear")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                self.add_status("Beast Master")
                print("\n")
                return
            
            type.type(yellow("=== CONFRONTATION: THE BEAST ==="))
            print("\n")
            type.type("The bear rises on its hind legs. It must be twelve feet tall. It sniffs the air, then looks directly at you.")
            print("\n")
            type.type("What's your move?")
            print("\n")
            action = input("(fight/flee/offer/submit): ").strip().lower()
            
            if action == "fight":
                type.type("You've lost your mind. But here goes nothing.")
                print("\n")
                if self.has_item("Rope"):
                    type.type("You use the " + cyan(bright("Rope")) + " to lasso a branch and swing to higher ground before the bear reaches you.")
                    print("\n")
                    type.type("Fighting from above changes the equation. The bear can't use its full size against you.")
                    print("\n")
                if self.has_item("Pocket Knife") or self.has_item("Utility Blade") or self.has_item("Master Knife"):
                    knife_name = "Pocket Knife" if self.has_item("Pocket Knife") else ("Utility Blade" if self.has_item("Utility Blade") else "Master Knife")
                    type.type("The " + cyan(bright(knife_name)) + " finds a gap in the bear's thick hide — a nick behind the ear that draws blood.")
                    print("\n")
                    type.type("It roars. You've hurt it. Not enough — but enough to make it hesitate.")
                    evolved = self.track_item_use(knife_name)
                    if evolved:
                        print("\n")
                        type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
                    print("\n")
                if self.has_item("Scrap Armor") or self.has_item("Road Warrior Armor") or self.has_item("Plated Vest") or self.has_item("Road Warrior Plate"):
                    if self.has_item("Road Warrior Armor"):
                        armor_name = "Road Warrior Armor"
                    elif self.has_item("Road Warrior Plate"):
                        armor_name = "Road Warrior Plate"
                    elif self.has_item("Plated Vest"):
                        armor_name = "Plated Vest"
                    else:
                        armor_name = "Scrap Armor"
                    type.type("The " + cyan(bright(armor_name)) + " absorbs the first swipe. It saves your ribs.")
                    evolved = self.track_item_use(armor_name)
                    if evolved:
                        print("\n")
                        type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))
                    print("\n")
                type.type(yellow("=== BATTLE ==="))
                type.type("The bear charges. You have one chance.")
                print("\n")
                type.type("Do you go for the eyes, dodge and strike, or play dead at the last second?")
                attack = input("(eyes/dodge/dead): ").strip().lower()
                
                if attack == "eyes":
                    if random.random() < 0.15:
                        type.type("You lunge forward, jamming your fingers into its eyes. The bear ROARS and swipes blindly. You roll clear. Somehow, impossibly, you've hurt it.")
                        print("\n")
                        type.type("The bear backs off, shaking its massive head. It gives you one last look - respect? fear? - and disappears into the trees.")
                        print("\n")
                        type.type("You've earned the right to call yourself a monster slayer.")
                        self.add_item("Bear King's Respect")
                        self.add_status("Legend")
                    else:
                        type.type("You miss. The bear does not. Its claws tear through you like paper.")
                        self.hurt(random.randint(60, 90))
                        type.type("You wake up hours later, alive but BARELY. The bear is gone. Why didn't it finish you?")
                elif attack == "dodge":
                    if random.random() < 0.3:
                        type.type("You sidestep like a matador and slash at its flank as it passes. The bear roars in surprise. You've drawn blood from a god.")
                        print("\n")
                        type.type("The bear retreats, wounded in more than body - its pride is hurt. It leaves you a gift: a tooth, knocked loose in the scuffle.")
                        self.add_item("Giant Bear Tooth")
                        self.change_balance(random.randint(5000, 15000))
                    else:
                        type.type("You're not fast enough. The bear clips you, sending you spinning into a tree. Stars explode behind your eyes.")
                        self.hurt(random.randint(40, 70))
                else:
                    if random.random() < 0.5:
                        type.type("You drop and go limp. The bear sniffs you, its hot breath washing over your face. Don't move. Don't breathe.")
                        print("\n")
                        type.type("After an eternity, it loses interest and wanders off. You lie there until dawn, shaking, but alive.")
                    else:
                        type.type("The bear isn't fooled. It bats you around like a cat toy before getting bored and leaving. You're alive, but barely.")
                        self.hurt(random.randint(50, 80))
                if self.has_item("Nomad's Camp"):
                    type.type("The " + cyan(bright("Nomad's Camp")) + " provides everything — shelter, food, water.")
                    print("\n")
                    type.type("You rest mid-adventure. Full restoration.")
                    self.heal(100)
                    self.restore_sanity(15)
                    return
                if self.has_item("Wanderer's Rest"):
                    type.type("The " + cyan(bright("Wanderer's Rest")) + "'s roots are deep now. Even here, it sustains you.")
                    print("\n")
                    type.type("You will never want for anything again. Energy fully restored.")
                    self.heal(80)
                    self.restore_sanity(10)
                    return
                if self.has_item("Survival Bivouac"):
                    type.type("The " + cyan(bright("Survival Bivouac")) + " turns any rest into full recovery.")
                    print("\n")
                    self.heal(40)
                    self.restore_sanity(8)
                    return
                if self.has_item("First Aid Kit") and self.get_health() < 70:
                    self.use_item("First Aid Kit")
                    type.type("You dig out the " + cyan(bright("First Aid Kit")) + " and patch yourself up. Not pretty, but functional.")
                    self.heal(20)
                    print("\n")
                print("\n")
            
            elif action == "flee":
                type.type("You RUN. Branches whip your face. Roots grab your ankles. Behind you, the thunder of the bear's pursuit.")
                print("\n")
                type.type("You see a river ahead. A cliff to your left. A thick bramble patch to your right.")
                flee = input("(river/cliff/brambles): ").strip().lower()
                
                if flee == "river":
                    if random.random() < 0.6:
                        type.type("You dive in. The current is strong but you're a good swimmer. The bear stops at the bank, unwilling to follow. You wash up downstream, exhausted but alive.")
                    else:
                        type.type("The bear follows you into the water. You fight the current AND the beast. You barely make it out, waterlogged and bleeding.")
                        self.hurt(random.randint(30, 50))
                elif flee == "cliff":
                    if random.random() < 0.4:
                        type.type("You scramble down the cliff face. The bear is too heavy to follow. You escape, but your hands are torn to ribbons from the rocks.")
                        self.hurt(random.randint(15, 25))
                    else:
                        type.type("You slip. The fall is short but brutal. The bear watches from above as you limp away, broken but breathing.")
                        self.hurt(random.randint(40, 60))
                else:
                    if random.random() < 0.7:
                        type.type("You dive into the thorns. It hurts like hell, but the bear won't follow. You crawl through, bleeding from a hundred tiny cuts, and emerge victorious.")
                        self.hurt(random.randint(10, 20))
                    else:
                        type.type("The bear crashes through the brambles like they're nothing. You're trapped. But it just looks at you, snorts, and leaves. Like you're not worth the effort.")
                print("\n")
            
            elif action == "offer":
                type.type("You slowly reach for whatever food you have. A sandwich. Some jerky. You hold it out with a trembling hand.")
                print("\n")
                type.type(quote("Here. Take it. I don't want trouble."))
                print("\n")
                if random.random() < 0.5:
                    type.type("The bear approaches slowly, sniffs your offering, and... eats it. Delicately. Almost politely. Then it sits down next to you.")
                    print("\n")
                    type.type("You spend the next hour sitting with a bear. It's the most surreal experience of your life. ")
                    type.type("When it finally leaves, it drops something at your feet - a gold coin, old and worn. ")
                    type.type("Where did a bear get a gold coin?")
                    self.add_item("Bear's Gold Coin")
                    self.change_balance(random.randint(3000, 8000))
                else:
                    type.type("The bear sniffs your offering... and knocks it aside. It wants something else. You run while it's distracted, and don't look back.")
                print("\n")
            
            else:  # submit
                type.type("You drop to your knees and lower your head. Total submission. You acknowledge the bear as your superior in every way.")
                print("\n")
                if random.random() < 0.6:
                    type.type("The bear studies you for a long moment. Then it does something impossible - it nods. Like it understands. Like it respects you.")
                    print("\n")
                    type.type("It turns and walks away, disappearing into the forest. You feel like you've passed some kind of test.")
                    self.add_status("Forest Blessed")
                    self.heal(random.randint(20, 40))
                else:
                    type.type("The bear isn't interested in your submission. It cuffs you once, hard, sending you flying. Then it leaves.")
                    self.hurt(random.randint(20, 35))
                print("\n")
        
        elif event == "fountain_of_youth":
            type.type("Deep in the woods, where no trail leads, you find something impossible. ")
            type.type("A spring, bubbling up from between ancient stones, its waters glowing with soft golden light. ")
            type.type("The air around it is warm despite the cold night. ")
            type.type("Flowers bloom along its banks - flowers that shouldn't exist in this season.")
            print("\n")
            type.type(yellow("=== THE FOUNTAIN ==="))
            print("\n")
            type.type("You kneel at the water's edge. Your reflection looks... younger. Healthier. Is it a trick of the light?")
            print("\n")
            type.type("What do you do?")
            print("\n")
            action = input("(drink/wash/bottle/leave): ").strip().lower()
            
            if action == "drink":
                type.type("You cup the water in your hands and drink deeply. It's cold and sweet, like nothing you've ever tasted.")
                print("\n")
                type.type("Warmth spreads through your body. Old aches disappear. Scars fade. You feel... ALIVE.")
                self.heal(100)
                print("\n")
                side_effect = random.choice(["good", "bad", "neutral"])
                if side_effect == "good":
                    type.type("The effect lingers. You feel younger, stronger, luckier. Like the world has decided to give you a second chance.")
                    self.add_status("Youthful")
                    self.add_status("Blessed")
                elif side_effect == "bad":
                    type.type("But something else happens too. Your hair starts to gray. Your hands shake. ")
                    type.type("The fountain gives... but it also takes. ")
                    type.type("You've traded years of your future for this moment of healing.")
                    self.add_status("Time-Touched")
                else:
                    type.type("The effect is temporary, you can feel it. But for now, you feel incredible.")
                print("\n")
            elif action == "wash":
                type.type("You wash your face and hands in the water. Every cut, every bruise, every mark of your hard life washes away.")
                self.heal(random.randint(50, 75))
                print("\n")
                type.type("You don't look younger exactly, but you look... refreshed. Like you just woke up from the best sleep of your life.")
                print("\n")
            elif action == "bottle":
                type.type("You fill your canteen with the glowing water. As you seal it, the glow fades slightly, but the water still shimmers.")
                self.add_item("Fountain Water")
                print("\n")
                type.type("You have no idea what this will do when you drink it later. But you have a feeling it'll be worth something.")
                print("\n")
            else:
                type.type("You step back from the fountain. Something about it feels wrong. Too good. Nothing is free in this world.")
                print("\n")
                type.type("As you leave, you swear you hear laughter from the water. Did you make the right choice? You'll never know.")
                print("\n")
        
        elif event == "hermit_cabin":
            type.type("Smoke rises from a chimney you didn't expect. A cabin, hidden among the trees, so well-camouflaged you almost walked into the door.")
            print("\n")
            type.type("A sign hangs crooked: 'KNOCK OR DON'T. EITHER WAY, I KNOW YOU'RE THERE.'")
            print("\n")
            type.type("Do you knock, peek in the window, or leave?")
            action = input("(knock/peek/leave): ").strip().lower()
            
            if action == "knock":
                type.type("The door opens before your knuckles touch wood. An old woman stands there, wrapped in furs, eyes like chips of ice.")
                print("\n")
                type.type(quote("Took you long enough. Come in. I've been waiting."))
                print("\n")
                type.type("Inside, the cabin is filled with herbs, bones, books, and things you can't identify. She gestures to a chair.")
                print("\n")
                type.type(quote("I know why you're here. The gambling. The debt. The endless road. You want out, don't you?"))
                print("\n")
                answer = ask.yes_or_no("Tell her the truth?")
                if answer == "yes":
                    type.type("She nods slowly. " + quote("Honesty. Good. I can help you, but it'll cost you. Not money. Something else."))
                    print("\n")
                    type.type("She offers three options: your luckiest memory, a year of your life, or a favor to be named later.")
                    cost = input("(memory/year/favor): ").strip().lower()
                    if cost == "memory":
                        type.type("She reaches toward your forehead. A flash of light. ")
                        type.type("You can't remember... something. Something that used to make you happy. ")
                        type.type("But in exchange, you feel LUCKY. Deeply, impossibly lucky.")
                        self.add_status("Witch Lucky")
                        self.change_balance(random.randint(10000, 25000))
                    elif cost == "year":
                        type.type("She takes your hand. You feel a jolt, and suddenly you're... older. Just slightly. But in return, she gives you something - a bag that clinks with gold.")
                        self.change_balance(random.randint(15000, 35000))
                        self.add_status("Aged")
                    else:
                        type.type("She grins. " + quote("Smart. Or stupid. We'll see.") + " She gives you a coin - old, worn, glowing faintly. ")
                        type.type(quote("When you need help, flip this. I'll know."))
                        self.add_item("Witch's Favor")
                else:
                    type.type("She laughs. " + quote("A liar. I can work with that.") + " She hands you a vial of something dark. " + quote("Drink this. It won't kill you. Probably."))
                    self.add_item("Mystery Potion")
                print("\n")
            elif action == "peek":
                type.type("You creep to the window and peer inside. The old woman is sitting at a table, staring directly at you.")
                print("\n")
                type.type(quote("I can see you, fool."))
                print("\n")
                type.type("The door flies open. She doesn't look happy.")
                print("\n")
                type.type(quote("Peepers get what peepers deserve."))
                print("\n")
                if random.random() < 0.5:
                    type.type("She throws something in your face. Your vision goes dark. ")
                    type.type("When it clears, you're a mile away with no memory of how you got there. ")
                    type.type("But there's money in your pocket that wasn't there before. Witch logic.")
                    self.change_balance(random.randint(2000, 8000))
                else:
                    type.type("She curses you. You feel it settle into your bones like cold water.")
                    self.add_status("Witch Cursed")
                    self.hurt(random.randint(15, 30))
                print("\n")
            else:
                type.type("You back away from the cabin. Some doors are better left unknocked.")
                print("\n")
                type.type("As you leave, you hear her voice on the wind: " + quote("We'll meet again."))
                print("\n")
        
        else:
            type.type("The forest is quiet tonight. No adventures find you - or perhaps you weren't ready for them.")
            print("\n")
            type.type("You rest beneath an ancient oak, listening to the wind in the leaves. Sometimes the greatest adventure is simply being still.")
            if self.has_item("Binoculars") or self.has_item("Binocular Scope"):
                item_name = "Binocular Scope" if self.has_item("Binocular Scope") else "Binoculars"
                print("\n")
                type.type("You pull out your " + cyan(bright(item_name)) + " and scan the treeline. A hidden deer path runs along the ridge — and at the end of it, something glints.")
                print("\n")
                type.type("You follow it. Tucked under a root: an old tin with a handful of coins and a folded bill. Someone's forgotten stash.")
                found = random.randint(15, 45)
                type.type(" " + green(bright("$" + str(found))) + " well-spotted.")
                self.earn_money(found)
                self.restore_sanity(4)
            if self.has_item("Provider's Kit") or self.has_item("Fishing Rod"):
                fish_item = "Provider's Kit" if self.has_item("Provider's Kit") else "Fishing Rod"
                print("\n")
                type.type("You find a forest river and cast in your " + cyan(bright(fish_item)) + ".")
                print("\n")
                if self.has_item("Provider's Kit"):
                    type.type("The dual trap-and-rod setup turns the forest into a buffet. Within an hour you have more fish than you can carry.")
                    amount = random.randint(40, 100)
                else:
                    type.type("An hour later: two fish and a sense of calm that the casino never gives you.")
                    amount = random.randint(20, 60)
                type.type(" " + green(bright("$" + str(amount))) + " worth of fresh catch.")
                self.change_balance(amount)
                self.restore_sanity(5)
            self.heal(random.randint(15, 30))
            print("\n")

    def swamp_adventure(self):
        """
        Performs a random swamp adventure event, presenting narrative choices
        such as tortoise racing, ogre encounters, fairy wishes, mermaid
        interactions, and gator wrestling. Updates player stats, inventory, and
        status based on user decisions and random outcomes. Intended for
        interactive, text-based gameplay.
        """
        self.meet("Swamp Adventure Event")
        self.add_fatigue(random.randint(10, 18))  # Slogging through swamp muck
        type.type("The swamp stretches before you, endless and alive. ")
        type.type("Cypress trees draped in moss rise from black water like the fingers of drowned giants. ")
        type.type("Strange lights flicker in the distance. ")
        type.type("The air smells of decay and growth, death and life tangled together.")
        print("\n")
        type.type(yellow(bright("=== SWAMP ADVENTURE ===")))
        print("\n")
        if self.has_item("Hazmat Suit"):
            type.type("The " + cyan(bright("Hazmat Suit")) + " walks through the toxic zone like it's a spring morning.")
            print("\n")
            type.type("You access areas no one else can reach. The treasure is unguarded — no one else can get here.")
            self.change_balance(random.randint(200, 500))
            self.restore_sanity(5)
            return
        if self.has_item("Gas Mask"):
            type.type("Through the " + cyan(bright("Gas Mask")) + ", the toxic swamp air becomes just air. You breathe freely where others would be coughing.")
            print("\n")
        else:
            type.type("The rotten air settles in your lungs like a personal insult. You'll be tasting swamp for a week.")
            self.hurt(5)
            print("\n")
        if self.has_item("Water Purifier"):
            type.type("Your " + cyan(bright("Water Purifier")) + " sits ready to filter whatever questionable water you encounter. No swamp belly today.")
            print("\n")
        event = random.choice([
            "tortoise_racing", "ogre", "fairy_bottle", "disgusting_mermaid", "gator_wrestling", "casual_day"
        ])
        
        if event == "tortoise_racing":
            type.type("You hear cheering ahead - actual cheering, deep in the swamp. ")
            type.type("Following the sound, you emerge into a torchlit clearing where a crowd of swamp folk has gathered around a muddy track.")
            print("\n")
            type.type("They're racing TORTOISES. And betting HEAVILY.")
            print("\n")
            type.type(yellow("=== TORTOISE GRAND PRIX ==="))
            print("\n")
            type.type("A grizzled man with no teeth approaches you. " + quote("Stranger! You want action? Entry fee's $2,000 to race. Or you can bet on any turtle you like."))
            print("\n")
            type.type("The tortoises are lined up: Ol' Mossy (the favorite), Lightning Lou (young and fast), Shellshock Sally (unpredictable), and Mud Monster (the underdog).")
            print("\n")
            
            # Animal Whistle lets you befriend City Slicker after racing
            if self.has_item("Animal Whistle") and not self.has_companion("Speedy") and self.get_balance() >= 2000:
                type.type("The " + magenta(bright("Animal Whistle")) + " hums softly. The tortoises all poke their heads out and look at you.")
                print("\n")
                type.type("The toothless man notices. " + quote("Well I'll be. They like you. Tell ya what - race for free, and if City Slicker bonds with ya, he's yours to keep."))
                print("\n")
                type.type("You're handed City Slicker. He immediately extends his neck and gently bumps your hand.")
                print("\n")
                type.type("City Slicker has chosen you. You decide to call him " + cyan(bright("Speedy")) + " - ironically.")
                print("\n")
                type.type("Speedy becomes your companion. The man tips his hat. " + quote("He'll bring ya good luck, that one."))
                self.add_companion("Speedy", "Tortoise")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                self.add_status("Tortoise Luck")
                print("\n")
                return
            
            action = input("(race/bet/watch): ").strip().lower()
            
            if action == "race":
                if self.get_balance() >= 2000:
                    self.change_balance(-2000)
                    type.type("You're handed a tortoise named 'City Slicker' - apparently what they call any newcomer's turtle. It blinks at you slowly.")
                    print("\n")
                    type.type(yellow("=== RACE START ==="))
                    type.type("The tortoises are released! City Slicker immediately starts heading the wrong direction.")
                    print("\n")
                    type.type("Quick! How do you motivate your tortoise?")
                    r1 = input("(lettuce/yelling/poking): ").strip().lower()
                    
                    race_score = random.randint(0, 3)  # Base randomness
                    
                    if r1 == "lettuce":
                        if self.has_item("Lettuce") or random.random() < 0.3:
                            type.type("You wave lettuce in front of City Slicker's face. It SNAPS to attention and starts moving!")
                            if self.has_item("Lettuce"):
                                self.use_item("Lettuce")
                            race_score += 2
                        else:
                            type.type("You don't have lettuce! City Slicker continues his existential wandering.")
                    elif r1 == "yelling":
                        if random.random() < 0.4:
                            type.type("Your screaming seems to startle City Slicker into moving faster. Who knew tortoises responded to psychological warfare?")
                            race_score += 1
                        else:
                            type.type("City Slicker is unimpressed by your volume. He withdraws into his shell for a nap.")
                    else:
                        if random.random() < 0.5:
                            type.type("You poke City Slicker's rear. He gives you a look of pure betrayal but does start moving.")
                            race_score += 1
                        else:
                            type.type("City Slicker bites your finger. You deserve this.")
                            self.hurt(random.randint(1, 5))
                    
                    print("\n")
                    type.type("The race enters the final stretch! City Slicker is neck-and-neck with Shellshock Sally!")
                    print("\n")
                    type.type("Do you cheer, pray, or throw something to distract the other tortoises?")
                    r2 = input("(cheer/pray/throw): ").strip().lower()
                    
                    if r2 == "throw":
                        if random.random() < 0.5:
                            type.type("You throw a pebble near Sally. She veers off course! The crowd boos but you don't care!")
                            race_score += 2
                        else:
                            type.type("A swamp man catches your throw. " + quote("CHEATER!") + " They disqualify City Slicker.")
                            race_score = 0
                    elif r2 == "pray":
                        type.type("You close your eyes and pray to whatever swamp gods might be listening.")
                        if random.random() < 0.3:
                            type.type("The swamp gods answer. A gust of wind pushes City Slicker forward!")
                            race_score += 2
                        else:
                            type.type("The swamp gods are busy. Or don't exist. Probably both.")
                    else:
                        type.type("You cheer like a maniac. City Slicker seems to appreciate the support.")
                        race_score += 1
                    
                    print("\n")
                    type.type(yellow("=== FINISH LINE ==="))
                    print("\n")
                    
                    if race_score >= 5:
                        type.type("CITY SLICKER WINS! The crowd goes WILD. The toothless man looks stunned.")
                        print("\n")
                        type.type(quote("First time anyone ever won with that turtle..."))
                        print("\n")
                        winnings = random.randint(12000, 25000)
                        type.type("You collect " + green(bright("$" + str(winnings))) + " and the title of Tortoise Champion.")
                        self.change_balance(winnings)
                        self.add_item("Tortoise Trophy")
                    elif race_score >= 3:
                        type.type("City Slicker places second! Not bad for a newcomer.")
                        winnings = random.randint(4000, 8000)
                        type.type("You win " + green(bright("$" + str(winnings))) + ".")
                        self.change_balance(winnings)
                    else:
                        type.type("City Slicker finishes dead last. He seems proud of himself anyway.")
                        type.type("You leave with nothing but a newfound respect for tortoises.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. The toothless man shrugs sympathetically.")
                    print("\n")
            
            elif action == "bet":
                type.type("Which tortoise do you bet on?")
                type.type("1. Ol' Mossy (2:1 odds)")
                type.type("2. Lightning Lou (3:1 odds)")
                type.type("3. Shellshock Sally (5:1 odds)")
                type.type("4. Mud Monster (10:1 odds)")
                turtle = input("Pick a number (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["mossy", "mossy", "lou", "lou", "sally", "monster"])
                        
                        if turtle == "1" and winner == "mossy":
                            type.type("Ol' Mossy wins! You collect " + green(bright("$" + str(bet * 2))) + "!")
                            self.change_balance(bet * 2)
                        elif turtle == "2" and winner == "lou":
                            type.type("Lightning Lou blazes to victory! You win " + green(bright("$" + str(bet * 3))) + "!")
                            self.change_balance(bet * 3)
                        elif turtle == "3" and winner == "sally":
                            type.type("Shellshock Sally shocks everyone! You win " + green(bright("$" + str(bet * 5))) + "!")
                            self.change_balance(bet * 5)
                        elif turtle == "4" and winner == "monster":
                            type.type("MUD MONSTER WINS! THE UNDERDOG! You win " + green(bright("$" + str(bet * 10))) + "!!!")
                            self.change_balance(bet * 10)
                            self.add_status("Lucky Gambler")
                        else:
                            type.type("Your tortoise lost. Better luck next time.")
                    else:
                        type.type("You can't bet what you don't have.")
                except:
                    type.type("Betting closed. You missed your chance.")
                print("\n")
            
            else:
                type.type("You watch the race from the sidelines. Ol' Mossy wins. The crowd exchanges money. You learn something about patience and betting.")
                self.add_status("Swamp Wise")
                print("\n")
        
        elif event == "ogre":
            type.type("The ground shakes. Trees topple. And then you see it - ")
            type.type("an OGRE, three times your height, covered in moss and mud, carrying a club made from an entire tree trunk.")
            print("\n")
            type.type(yellow("=== BOSS ENCOUNTER: THE SWAMP OGRE ==="))
            print("\n")
            type.type("It sees you. Its tiny eyes narrow. Its massive mouth opens, revealing teeth like tombstones.")
            print("\n")
            type.type(quote("LITTLE THING IN OGRE'S SWAMP. OGRE NOT LIKE."))
            print("\n")
            action = input("(fight/bribe/riddle/run): ").strip().lower()
            
            if action == "fight":
                type.type(yellow("=== BATTLE: YOU VS. OGRE ==="))
                type.type("This is either very brave or very stupid. The ogre swings its club.")
                print("\n")
                if self.has_item("Rope"):
                    type.type("You use the " + cyan(bright("Rope")) + " to lasso the ogre's ankles before it can wind up a full swing.")
                    print("\n")
                    type.type("It stumbles. You've bought yourself a window.")
                    print("\n")
                if self.has_item("Pocket Knife"):
                    type.type("The " + cyan(bright("Pocket Knife")) + " finds a crack in the ogre's mossy hide — a thin line behind the knee that makes it flinch.")
                    print("\n")
                    type.type("It's not enough to stop it. But it's enough to slow it down.")
                    print("\n")
                if self.has_item("Scrap Armor") or self.has_item("Road Warrior Armor"):
                    armor_name = "Road Warrior Armor" if self.has_item("Road Warrior Armor") else "Scrap Armor"
                    type.type("The " + cyan(bright(armor_name)) + " takes the first glancing blow. You feel the impact but not the damage.")
                    print("\n")
                type.type("How do you attack?")
                attack = input("(kneecaps/climb/distract): ").strip().lower()
                
                if attack == "kneecaps":
                    type.type("You go low, slashing at its knees. The ogre HOWLS.")
                    if random.random() < 0.3:
                        type.type("It crumples! You've crippled a monster three times your size!")
                        print("\n")
                        type.type("The ogre crawls away, whimpering. In its nest, you find its hoard - gold, gems, and bones. You take the valuables and leave the bones.")
                        self.change_balance(random.randint(15000, 35000))
                        self.add_item("Ogre's Gemstone")
                    else:
                        type.type("But it doesn't go down. The backhand sends you flying into the swamp.")
                        self.hurt(random.randint(40, 70))
                elif attack == "climb":
                    type.type("You run up its leg like climbing a hairy tree. It swats at you but you're too fast.")
                    if random.random() < 0.25:
                        type.type("You reach its head and jam your knife into its ear! The ogre SCREAMS and throws you off, but it's hurt BAD.")
                        print("\n")
                        type.type("It stumbles away into the swamp, leaving behind a trail of blood and treasure it dropped.")
                        self.change_balance(random.randint(8000, 20000))
                    else:
                        type.type("It grabs you mid-climb and squeezes. You hear ribs cracking.")
                        self.hurt(random.randint(50, 80))
                else:
                    type.type("You throw mud in its eyes! " + quote("ARGH! OGRE NO SEE!"))
                    if random.random() < 0.5:
                        type.type("While it's blinded, you escape with some gold from its belt pouch.")
                        self.change_balance(random.randint(3000, 8000))
                    else:
                        type.type("It swings wildly - and connects. Blind luck, literally.")
                        self.hurt(random.randint(35, 60))
                if self.has_item("Nomad's Camp"):
                    type.type("The " + cyan(bright("Nomad's Camp")) + " provides everything — shelter, food, water.")
                    print("\n")
                    type.type("You rest mid-adventure. Full restoration.")
                    self.heal(100)
                    self.restore_sanity(15)
                    return
                if self.has_item("Wanderer's Rest"):
                    type.type("The " + cyan(bright("Wanderer's Rest")) + "'s roots are deep now. Even here, it sustains you.")
                    print("\n")
                    type.type("You will never want for anything again. Energy fully restored.")
                    self.heal(80)
                    self.restore_sanity(10)
                    return
                if self.has_item("Survival Bivouac"):
                    type.type("The " + cyan(bright("Survival Bivouac")) + " turns any rest into full recovery.")
                    print("\n")
                    self.heal(40)
                    self.restore_sanity(8)
                    return
                if self.has_item("First Aid Kit") and self.get_health() < 70:
                    self.use_item("First Aid Kit")
                    type.type("You dig out the " + cyan(bright("First Aid Kit")) + " and patch yourself up mid-swamp. It helps.")
                    self.heal(20)
                    print("\n")
                print("\n")
            
            elif action == "bribe":
                type.type(quote("Wait! I have gold! You like gold, right?"))
                print("\n")
                type.type("The ogre pauses. Its tiny brain processes this information.")
                print("\n")
                type.type(quote("OGRE... LIKE SHINY THINGS."))
                print("\n")
                type.type("How much do you offer? ($3000 minimum)")
                try:
                    bribe = int(input("Offer: $"))
                    if bribe >= 3000 and self.get_balance() >= bribe:
                        self.change_balance(-bribe)
                        if bribe >= 8000:
                            type.type("The ogre's eyes go wide. " + quote("MUCH SHINY! OGRE HAPPY!") + " It lets you pass AND gives you a 'gift' - a crusty but valuable gem from its pocket.")
                            self.add_item("Ogre's Gift")
                        else:
                            type.type("The ogre snatches the gold and counts it on its fingers. It lets you pass, but watches you until you're out of sight.")
                    else:
                        type.type("The ogre isn't impressed. " + quote("LITTLE THING TRY TRICK OGRE!") + " It swings its club.")
                        self.hurt(random.randint(30, 50))
                except:
                    type.type("The ogre grows impatient with your fumbling.")
                    self.hurt(random.randint(20, 40))
                print("\n")
            
            elif action == "riddle":
                type.type(quote("Wait! I challenge you to a battle of wits!"))
                print("\n")
                type.type("The ogre stops. Scratches its head.")
                print("\n")
                type.type(quote("OGRE... LIKE RIDDLES?"))
                print("\n")
                type.type("You pose a riddle: 'What walks on four legs in the morning, two at noon, and three in the evening?'")
                print("\n")
                type.type("The ogre thinks. Steam seems to come from its ears. Finally:")
                print("\n")
                type.type(quote("OGRE KNOW! IS... IS..."))
                if random.random() < 0.3:
                    type.type(quote("...HUMAN THING!"))
                    print("\n")
                    type.type("The ogre solved the riddle. It grins proudly. " + quote("NOW OGRE EAT YOU ANYWAY."))
                    self.hurt(random.randint(40, 60))
                else:
                    type.type(quote("...OGRE NO KNOW. OGRE HEAD HURT."))
                    print("\n")
                    type.type("The ogre sits down, defeated, holding its head. You slip past while it's having an existential crisis. On the way, you snag some gold from its belt.")
                    self.change_balance(random.randint(5000, 12000))
                print("\n")
            
            else:
                type.type("You RUN. The ogre gives chase, but you're faster and you know how to use the terrain.")
                if random.random() < 0.6:
                    type.type("You dive into water too deep for the ogre to follow. It roars in frustration as you swim away.")
                else:
                    type.type("It catches you by the ankle. The throw is spectacular - you land in a mud pit fifty feet away.")
                    self.hurt(random.randint(25, 45))
                print("\n")
        
        elif event == "fairy_bottle":
            type.type("Something glows in the hollow of a dead tree. You approach carefully - could be a trap, could be treasure, could be both.")
            print("\n")
            type.type("It's a bottle. Inside the bottle is a fairy, no bigger than your thumb, wings pressed against the glass. She looks FURIOUS.")
            print("\n")
            type.type(yellow("=== THE TRAPPED FAIRY ==="))
            print("\n")
            type.type("She pounds on the glass. Her tiny voice is muffled but you can make out: " + quote("LET ME OUT, YOU GIANT OAF!"))
            print("\n")
            action = input("(free/keep/negotiate/ignore): ").strip().lower()
            
            if action == "free":
                type.type("You uncork the bottle. The fairy shoots out like a tiny, angry bullet, circling your head.")
                print("\n")
                type.type(quote("Finally! I've been trapped in there for DECADES by that stupid witch!"))
                print("\n")
                type.type("She lands on your shoulder, catching her breath.")
                print("\n")
                type.type(quote("You freed me, so I owe you. THREE wishes. And before you ask - no immortality, no resurrection, no time travel. I'm a swamp fairy, not a god."))
                print("\n")
                for i in range(3):
                    type.type(f"Wish {i+1} of 3:")
                    wish = input("(money/luck/health/item/info): ").strip().lower()
                    if wish == "money":
                        amount = random.randint(5000, 15000)
                        type.type("The fairy waves her hand. Your pockets suddenly feel heavier. " + green(bright("$" + str(amount))) + " appears.")
                        self.change_balance(amount)
                    elif wish == "luck":
                        type.type("The fairy sprinkles dust on you. " + quote("You'll be lucky for a while. Don't waste it."))
                        self.add_status("Fairy Lucky")
                    elif wish == "health":
                        type.type("The fairy touches your forehead. Warmth spreads through you, healing old wounds.")
                        self.heal(random.randint(40, 60))
                    elif wish == "item":
                        type.type("The fairy conjures something from thin air - a glowing acorn.")
                        type.type(quote("Plant this somewhere and come back in a year. You'll like what grows."))
                        self.add_item("Magic Acorn")
                    else:
                        type.type("The fairy whispers a secret in your ear - the location of something valuable, hidden nearby.")
                        self.add_item("Fairy's Secret Map")
                    print("\n")
                
                type.type("The fairy stretches her wings. " + quote("We're square now. Don't let any witches catch you - they're vindictive."))
                print("\n")
                type.type("She disappears into the swamp, trailing sparkles.")
                self.add_status("Fairy Friend")
                print("\n")
            
            elif action == "keep":
                type.type("You pocket the bottle. The fairy goes BALLISTIC, screaming tiny curses at you.")
                print("\n")
                type.type(quote("YOU'LL REGRET THIS! MY SISTERS WILL FIND YOU!"))
                print("\n")
                type.type("But she's trapped. And fairies are worth a LOT to the right buyer.")
                self.add_item("Captured Fairy")
                self.add_status("Fairy Cursed")
                print("\n")
            
            elif action == "negotiate":
                type.type(quote("What's in it for me if I let you out?"))
                print("\n")
                type.type("The fairy stops pounding. She considers.")
                print("\n")
                type.type(quote("Freedom first. Then we talk. I'm not making promises from inside a bottle."))
                print("\n")
                type.type("Do you trust her?")
                trust = ask.yes_or_no()
                if trust == "yes":
                    type.type("You open the bottle. The fairy stretches her wings and sighs with relief.")
                    print("\n")
                    type.type(quote("Okay, fine. One wish. That's the deal."))
                    wish = input("(money/luck/health): ").strip().lower()
                    if wish == "money":
                        self.change_balance(random.randint(8000, 18000))
                        type.type("Gold appears from nowhere. " + quote("Happy now, greedy giant?"))
                    elif wish == "luck":
                        self.add_status("Negotiator's Luck")
                        type.type("She sighs and sprinkles dust on you.")
                    else:
                        self.heal(random.randint(50, 80))
                        type.type("She touches your heart. Pain fades away.")
                    print("\n")
                else:
                    type.type("You walk away, leaving her in the bottle. Her screams follow you for a long time.")
                print("\n")
            
            else:
                type.type("You leave the fairy where she is. Not your problem.")
                print("\n")
                type.type("As you walk away, you hear her sobbing. It almost makes you feel bad. Almost.")
                print("\n")
        
        elif event == "disgusting_mermaid":
            type.type("You see her sitting on a log in the middle of the swamp - a mermaid. But not the beautiful kind from stories.")
            print("\n")
            type.type("This mermaid is HIDEOUS. Covered in algae, barnacles growing on her scales, breath like rotting fish. She grins at you with teeth like broken bottles.")
            print("\n")
            type.type(yellow("=== THE SWAMP MERMAID ==="))
            print("\n")
            type.type(quote("Hello, handsome,") + " she rasps. " + quote("It's been sooooo long since I had company. How about a kiss?"))
            print("\n")
            action = input("(kiss/talk/run/insult): ").strip().lower()
            
            if action == "kiss":
                type.type("You close your eyes, hold your breath, and lean in. The kiss is... wet. Very wet. And cold. And it tastes like a fish market in summer.")
                print("\n")
                outcome = random.choice(["good", "bad", "weird"])
                if outcome == "good":
                    type.type("When you pull back, the mermaid is... beautiful? Was she always beautiful? You can't remember.")
                    print("\n")
                    type.type(quote("A brave soul! Take this gift, and remember: true beauty is seeing past the surface."))
                    print("\n")
                    self.add_item("Mermaid's Pearl")
                    self.change_balance(random.randint(10000, 25000))
                    self.add_status("Mermaid Kissed")
                elif outcome == "bad":
                    type.type("The mermaid's grip tightens. She tries to drag you into the water!")
                    print("\n")
                    type.type("You fight her off, barely escaping with your life and a collection of bruises.")
                    self.hurt(random.randint(25, 45))
                else:
                    type.type("The mermaid giggles and releases you. " + quote("That was nice. Here, have a fish."))
                    print("\n")
                    type.type("She hands you a literal fish. It's alive and flopping. Why did you kiss a swamp mermaid?")
                    self.add_item("Live Fish")
                print("\n")
            
            elif action == "talk":
                type.type(quote("So... how did you end up here?"))
                print("\n")
                type.type("The mermaid sighs, a sound like a drain unclogging.")
                print("\n")
                type.type(quote("I used to be beautiful, you know. Queen of the coral palace. "))
                type.type(quote("Then I made fun of a sea witch's nose. One curse later, here I am. Eternal ugliness, stuck in a swamp."))
                print("\n")
                type.type("She looks genuinely sad. Do you try to comfort her?")
                comfort = ask.yes_or_no()
                if comfort == "yes":
                    type.type(quote("Beauty fades anyway. At least you're still you."))
                    print("\n")
                    type.type("The mermaid stares at you. A tear rolls down her barnacled cheek.")
                    print("\n")
                    type.type(quote("That's... the nicest thing anyone's said to me in three hundred years."))
                    print("\n")
                    type.type("She gives you a handful of pearls from her hair. They're grimy, but real.")
                    self.change_balance(random.randint(5000, 12000))
                    self.add_status("Mermaid Friend")
                else:
                    type.type("The mermaid shrugs. " + quote("Yeah, I wouldn't comfort me either."))
                print("\n")
            
            elif action == "insult":
                type.type(quote("Wow, you're really ugly."))
                print("\n")
                type.type("The mermaid's face twists with rage.")
                print("\n")
                type.type(quote("HOW DARE YOU!"))
                print("\n")
                type.type("She lunges. You run. She can't follow on land, but she throws things - rocks, fish, profanities.")
                self.hurt(random.randint(10, 25))
                print("\n")
            
            else:
                type.type("You start backing away slowly. The mermaid's face falls.")
                print("\n")
                type.type(quote("Everyone always runs..."))
                print("\n")
                type.type("You feel a little bad, but not bad enough to stay.")
                print("\n")
        
        elif event == "gator_wrestling":
            type.type("A crowd of swamp folk stands around a muddy pit. Inside, a man is wrestling an ALLIGATOR. And winning.")
            print("\n")
            type.type("He pins the gator, and the crowd erupts. Money changes hands. A man with a megaphone spots you.")
            print("\n")
            type.type(quote("YOU THERE! Stranger! You look strong! Wanna try your luck against SALLY? Only $1,000 entry, winner takes the pot!"))
            print("\n")
            type.type(yellow("=== GATOR WRESTLING ==="))
            print("\n")
            action = input("(wrestle/bet/watch/nope): ").strip().lower()
            
            if action == "wrestle":
                if self.get_balance() >= 1000:
                    self.change_balance(-1000)
                    type.type("You climb into the pit. Sally the gator eyes you hungrily. She's twelve feet long and NOT happy.")
                    print("\n")
                    type.type(yellow("=== ROUND 1: THE STAREDOWN ==="))
                    type.type("Sally hisses. The crowd goes quiet. What's your opening move?")
                    r1 = input("(circle/charge/taunt): ").strip().lower()
                    
                    gator_score = 0
                    
                    if r1 == "circle":
                        type.type("You circle slowly, keeping Sally's eyes on you. She turns, watching, waiting.")
                        if random.random() < 0.6:
                            type.type("She lunges left - you dodge right. Good read!")
                            gator_score += 1
                        else:
                            type.type("She fakes left and catches your leg. You pull free, but you're bleeding.")
                            self.hurt(random.randint(10, 20))
                    elif r1 == "charge":
                        type.type("You CHARGE like a maniac, diving at Sally before she can react!")
                        if random.random() < 0.4:
                            type.type("You land on her back! The crowd ROARS!")
                            gator_score += 2
                        else:
                            type.type("She rolls. You miss. She doesn't. Her tail whips your legs out.")
                            self.hurt(random.randint(15, 25))
                    else:
                        type.type("You pound your chest and scream at the gator. Sally looks... confused? Insulted?")
                        if random.random() < 0.5:
                            type.type("The confusion gives you an opening!")
                            gator_score += 1
                        else:
                            type.type("Sally charges in pure anger. You barely dodge.")
                    
                    print("\n")
                    type.type(yellow("=== ROUND 2: THE GRAPPLE ==="))
                    type.type("Sally and you are tangled up in the mud. Her jaws are inches from your arm!")
                    r2 = input("(jaw_clamp/roll/escape): ").strip().lower()
                    
                    if r2 == "jaw_clamp":
                        type.type("You grab her jaws and HOLD THEM SHUT. Gators have weak jaw-opening muscles!")
                        if random.random() < 0.6:
                            type.type("IT WORKS! Sally struggles but can't open her mouth!")
                            gator_score += 2
                        else:
                            type.type("She's too strong. She snaps free and you only barely get your hands away.")
                    elif r2 == "roll":
                        type.type("You roll WITH her death roll, using momentum!")
                        if random.random() < 0.5:
                            type.type("Genius move! You end up on top!")
                            gator_score += 2
                        else:
                            type.type("You get disoriented and she lands on top of you. The crowd gasps.")
                            self.hurt(random.randint(15, 25))
                    else:
                        type.type("You slip free and create distance. Smart but not impressive.")
                        gator_score += 1
                    
                    print("\n")
                    type.type(yellow("=== FINAL: THE PIN ==="))
                    
                    if gator_score >= 4:
                        type.type("You've got Sally pinned! Her legs churn the mud but she can't escape! The referee counts to three - YOU WIN!")
                        winnings = random.randint(8000, 20000)
                        type.type("You collect " + green(bright("$" + str(winnings))) + " and the title of GATOR CHAMPION!")
                        self.change_balance(winnings)
                        self.add_item("Gator Tooth Necklace")
                    elif gator_score >= 2:
                        type.type("Neither you nor Sally can get the advantage. The referee calls it a draw!")
                        type.type("You get your entry fee back, plus a little extra for the entertainment.")
                        self.change_balance(2000)
                    else:
                        type.type("Sally pins YOU. Her jaws open wide - but the handlers pull her off. You lost, but you survived. That's something.")
                        self.lose_sanity(random.choice([3, 4, 5]))  # Near-death by gator
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. The announcer looks disappointed.")
                    print("\n")
            
            elif action == "bet":
                type.type("Who do you bet on? The current champion is Big Earl. The challenger is a tourist from Florida.")
                bet = random.randint(500, 2000)
                if self.get_balance() >= bet:
                    self.change_balance(-bet)
                    if random.random() < 0.5:
                        type.type("Big Earl wins! You collect " + green(bright("$" + str(bet * 2))) + "!")
                        self.change_balance(bet * 2)
                    else:
                        type.type("The tourist wins! Upset of the century! There goes your money.")
                else:
                    type.type("You don't have enough to bet.")
                print("\n")
            
            elif action == "watch":
                type.type("You watch match after match. People get bit, thrown, and occasionally victorious. It's the best worst entertainment you've ever seen.")
                self.add_status("Entertained")
                print("\n")
            
            else:
                type.type(quote("NOPE.") + " You walk away. Some experiences aren't worth having.")
                print("\n")
        
        else:
            type.type("Tonight, the swamp is quiet. ")
            type.type("You rest beneath the moss-draped trees, listening to the bullfrogs and the distant splash of gators. ")
            type.type("The dreams that come are strange and wild, but not unpleasant.")
            self.heal(random.randint(15, 30))
            print("\n")

    def beach_adventure(self):
        self.meet("Beach Adventure Event")
        self.add_fatigue(random.randint(5, 12))  # Beach night, breezy
        type.type("The moon hangs low over the endless sand. The beach is alive with laughter, music, and the crash of waves. ")
        type.type("Tiki torches line the shore. Tonight, anything could happen.")
        print("\n")
        type.type(yellow(bright("=== BEACH ADVENTURE ===")))
        print("\n")
        event = random.choice([
            "volleyball_tournament", "bonfire_ritual", "message_in_bottle", "crab_racing", "sandcastle_contest", "casual_day"
        ])
        
        if event == "volleyball_tournament":
            type.type("A crowd gathers around lit courts - the MIDNIGHT VOLLEYBALL CHAMPIONSHIP is happening!")
            print("\n")
            type.type(yellow("=== MIDNIGHT VOLLEYBALL TOURNAMENT ==="))
            print("\n")
            type.type("A buff guy with a clipboard approaches. " + quote("We need a fourth! Entry is $3,000, winner's pot is $50,000. You in?"))
            print("\n")
            action = input("(join/bet/watch/nope): ").strip().lower()
            
            if action == "join":
                if self.get_balance() >= 3000:
                    self.change_balance(-3000)
                    type.type("You're placed on Team Sunset - two surfer bros and a surprisingly athletic grandma.")
                    print("\n")
                    
                    # Match 1
                    type.type(yellow("=== ROUND 1: vs. THE BEACH BUMS ==="))
                    type.type("They look drunk. This should be easy.")
                    type.type("The serve comes your way! What do you do?")
                    m1 = input("(bump/spike/dive): ").strip().lower()
                    
                    team_score = random.randint(0, 2)
                    
                    if m1 == "spike":
                        if random.random() < 0.4:
                            type.type("You SLAM it down! The drunk guys don't even react in time!")
                            team_score += 2
                        else:
                            type.type("You swing and miss. The grandma sighs heavily.")
                    elif m1 == "bump":
                        if random.random() < 0.6:
                            type.type("Clean bump! Grandma sets it, surfer bro spikes it. POINT!")
                            team_score += 1
                        else:
                            type.type("You bump it into the net. Whoops.")
                    else:
                        if random.random() < 0.5:
                            type.type("Epic dive! You save an impossible shot! The crowd goes wild!")
                            team_score += 2
                        else:
                            type.type("You dive face-first into sand. You eat a lot of sand.")
                            self.hurt(random.randint(5, 10))
                    
                    print("\n")
                    
                    # Match 2
                    type.type(yellow("=== ROUND 2: vs. THE PROS ==="))
                    type.type("These guys are SERIOUS. Matching uniforms. Headbands. Game faces.")
                    type.type("It's match point. The pressure is ON. The ball's coming fast!")
                    m2 = input("(block/set/cheer): ").strip().lower()
                    
                    if m2 == "block":
                        if random.random() < 0.3:
                            type.type("You time it PERFECTLY. The spike bounces off your hands and down!")
                            team_score += 3
                        else:
                            type.type("Too slow. It rockets past you.")
                    elif m2 == "set":
                        if random.random() < 0.5:
                            type.type("Beautiful set! Grandma, where did she learn to spike like that?!")
                            team_score += 2
                        else:
                            type.type("Your set goes wild. The surfer bros look disappointed.")
                    else:
                        type.type("You cheer instead of playing. Your team loses the point, but appreciates the morale support.")
                        team_score += 1
                    
                    print("\n")
                    
                    # Finals
                    type.type(yellow("=== FINALS: vs. THE CHAMPIONS ==="))
                    type.type("The defending champions. They've won five years running. The grandma cracks her knuckles.")
                    type.type("Final play. Everything comes down to this!")
                    m3 = input("(trust_grandma/go_hero/teamwork): ").strip().lower()
                    
                    if m3 == "trust_grandma":
                        type.type("You set up the grandma. She leaps - higher than any grandma should - and DESTROYS the ball!")
                        team_score += 3
                    elif m3 == "go_hero":
                        if random.random() < 0.3:
                            type.type("You take the shot yourself. Time slows. The ball sails over the net... and IN!")
                            team_score += 4
                        else:
                            type.type("You go for glory and miss. The surfer bros shake their heads.")
                    else:
                        type.type("Perfect teamwork! Bump, set, spike chain. The champions look SHOCKED!")
                        team_score += 2
                    
                    print("\n")
                    type.type(yellow("=== TOURNAMENT RESULTS ==="))
                    
                    if team_score >= 9:
                        type.type("TEAM SUNSET WINS THE CHAMPIONSHIP! The crowd ERUPTS!")
                        print("\n")
                        type.type("Grandma high-fives you hard enough to leave a bruise.")
                        winnings = random.randint(15000, 35000)
                        type.type("You collect your share: " + green(bright("$" + str(winnings))) + "!")
                        self.change_balance(winnings)
                        self.add_item("Championship Medal")
                    elif team_score >= 6:
                        type.type("Second place! Not bad for a pickup team!")
                        winnings = random.randint(6000, 12000)
                        type.type("You win " + green(bright("$" + str(winnings))) + ".")
                        self.change_balance(winnings)
                    else:
                        type.type("You're eliminated early, but the grandma gives you her number. 'For training,' she says.")
                        self.add_item("Grandma's Number")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. Better luck next time.")
                    print("\n")
            
            elif action == "bet":
                type.type("Which team do you bet on?")
                type.type("1. The Champions (2:1)")
                type.type("2. Team Sunset (5:1)")
                type.type("3. The Pros (3:1)")
                type.type("4. The Beach Bums (15:1)")
                pick = input("Pick a number (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["champs", "champs", "sunset", "pros", "pros", "bums"])
                        
                        if pick == "1" and winner == "champs":
                            type.type("The Champions win, as expected. You collect " + green(bright("$" + str(bet * 2))) + ".")
                            self.change_balance(bet * 2)
                        elif pick == "2" and winner == "sunset":
                            type.type("The pickup team wins! " + green(bright("$" + str(bet * 5))) + "!")
                            self.change_balance(bet * 5)
                        elif pick == "3" and winner == "pros":
                            type.type("The Pros take it! " + green(bright("$" + str(bet * 3))) + "!")
                            self.change_balance(bet * 3)
                        elif pick == "4" and winner == "bums":
                            type.type("THE DRUNK GUYS WON?! IMPOSSIBLE! " + green(bright("$" + str(bet * 15))) + "!!!")
                            self.change_balance(bet * 15)
                            self.add_status("Chaos Gambler")
                        else:
                            type.type("Your team lost. The sand claims your money.")
                    else:
                        type.type("You don't have that kind of money.")
                except:
                    type.type("The betting window closes before you can decide.")
                print("\n")
            
            elif action == "watch":
                type.type("You watch the tournament unfold. The underdog team with the athletic grandma actually wins! You feel inspired by their story.")
                self.add_status("Inspired")
                print("\n")
            
            else:
                type.type("You decline and walk away. Volleyball isn't for everyone.")
                print("\n")
        
        elif event == "bonfire_ritual":
            type.type("A circle of strangers in flowing robes beckons you toward a massive bonfire. Sparks spiral into the stars. They're chanting something ancient.")
            print("\n")
            type.type(yellow("=== THE BONFIRE RITUAL ==="))
            print("\n")
            type.type("A woman with ocean eyes approaches. " + quote("Traveler, the flames call to you. Will you join our ceremony tonight?"))
            print("\n")
            action = input("(join/observe/sabotage/leave): ").strip().lower()
            
            if action == "join":
                type.type("You step into the circle. The warmth of the fire is immediate, almost alive. They give you herbs to hold.")
                print("\n")
                type.type("The chanting intensifies. What do you focus on?")
                focus = input("(wealth/love/power/peace): ").strip().lower()
                
                type.type("You throw your herbs into the flames. They burn green, then blue, then white.")
                print("\n")
                
                outcome = random.choice(["blessed", "cursed", "vision", "nothing"])
                
                if outcome == "blessed":
                    if focus == "wealth":
                        type.type("Gold light washes over you. You feel richer - and when you check your pockets, you ARE richer.")
                        self.change_balance(random.randint(8000, 20000))
                    elif focus == "love":
                        type.type("Pink light surrounds you. Someone across the fire catches your eye and smiles.")
                        self.add_status("Love Blessed")
                        self.add_item("Beach Romance Number")
                    elif focus == "power":
                        type.type("Red light pulses through you. You feel STRONG. Invincible.")
                        self.add_status("Fire Empowered")
                        self.heal(random.randint(30, 50))
                    else:
                        type.type("White light fills your mind. Every worry, every stress - gone.")
                        self.add_status("Enlightened")
                        self.heal(random.randint(20, 40))
                    print("\n")
                elif outcome == "cursed":
                    type.type("The flames turn black. The chanters go silent. Something went wrong.")
                    print("\n")
                    type.type("The woman with ocean eyes looks worried. " + quote("The spirits are displeased..."))
                    self.add_status("Fire Cursed")
                    self.hurt(random.randint(15, 30))
                elif outcome == "vision":
                    type.type("The world tilts. You see... things. The future? The past? Another reality?")
                    print("\n")
                    vision = random.choice(["treasure", "warning", "weird"])
                    if vision == "treasure":
                        type.type("You see a location - a place where something valuable is hidden. When you wake, you remember it clearly.")
                        self.add_item("Vision Map")
                    elif vision == "warning":
                        type.type("You see danger ahead. Something to avoid. You'll know it when you see it.")
                        self.add_status("Forewarned")
                    else:
                        type.type("You see a talking crab give a speech about tax law. You're not sure what it means but you feel changed.")
                        self.add_status("Confused but Wiser")
                else:
                    type.type("The ritual ends. You feel... the same? Maybe rituals aren't your thing.")
                    print("\n")
            
            elif action == "observe":
                type.type("You watch from outside the circle. The ritual is beautiful - fire, dance, and ancient words.")
                print("\n")
                type.type("When it ends, a robed figure approaches and hands you a small token.")
                print("\n")
                type.type(quote("For the respectful observer."))
                self.add_item("Ritual Token")
                print("\n")
            
            elif action == "sabotage":
                type.type("You wait for the right moment... then kick sand into the fire!")
                print("\n")
                if random.random() < 0.3:
                    type.type("CHAOS! The fire explodes with sparks. The chanters scatter. In the confusion, you grab some of their offerings.")
                    self.change_balance(random.randint(3000, 8000))
                else:
                    type.type("They're faster than they look. Several tackle you and drag you away.")
                    print("\n")
                    type.type(quote("You dare desecrate our fire?! YOU WILL PAY!"))
                    self.hurt(random.randint(25, 45))
                    self.add_status("Cultist Enemy")
                print("\n")
            
            else:
                type.type("You walk away, leaving the ritual to its mysteries. Some things are better left unknown.")
                print("\n")
        
        elif event == "message_in_bottle":
            type.type("Something glints in the moonlight - a bottle, half-buried in the sand, a rolled paper inside.")
            print("\n")
            type.type(yellow("=== THE MESSAGE IN A BOTTLE ==="))
            print("\n")
            action = input("(open/shake/throw_back/sell): ").strip().lower()
            
            if action == "open":
                type.type("You pop the cork and unroll the message. The paper is old, the ink faded...")
                print("\n")
                message = random.choice(["map", "love_letter", "warning", "code", "help"])
                
                if message == "map":
                    type.type("IT'S A TREASURE MAP! X marks a spot on this very beach!")
                    print("\n")
                    type.type("Do you follow it immediately?")
                    follow = ask.yes_or_no()
                    if follow == "yes":
                        type.type("You pace off the steps... 30 north... 15 east... you start digging.")
                        print("\n")
                        if random.random() < 0.6:
                            type.type("YOUR SHOVEL HITS SOMETHING! A chest! Inside: gold doubloons!")
                            self.change_balance(random.randint(10000, 30000))
                            self.add_item("Treasure Chest")
                        else:
                            type.type("You dig... and dig... and dig. Nothing. Either someone got here first, or it was a prank.")
                    else:
                        type.type("You save the map for later.")
                        self.add_item("Treasure Map")
                
                elif message == "love_letter":
                    type.type("It's a love letter, written decades ago. Passionate, desperate, beautiful.")
                    print("\n")
                    type.type("There's a name and address. Still legible.")
                    type.type("Do you try to find the recipient?")
                    find = ask.yes_or_no()
                    if find == "yes":
                        type.type("You track down the address - an elderly woman answers. She reads the letter with tears in her eyes.")
                        print("\n")
                        type.type(quote("He did love me... I thought he abandoned me. Thank you, stranger."))
                        print("\n")
                        type.type("She presses something into your hand - an antique ring.")
                        self.add_item("Antique Ring")
                        self.add_status("Good Karma")
                    else:
                        type.type("Some stories are better left unfinished.")
                
                elif message == "warning":
                    type.type("'BEWARE THE TWELFTH TIDE. THE SLEEPER WAKES. DO NOT BE ON THE BEACH WHEN THE MOON IS FULL.'")
                    print("\n")
                    type.type("You glance at the moon. It's... almost full. Almost.")
                    self.add_status("Paranoid")
                
                elif message == "code":
                    type.type("Numbers. Coordinates? A code? Gibberish?")
                    print("\n")
                    type.type("'13-15-14-5-25 2-21-18-9-5-4 21-14-4-5-18 16-9-5-18'")
                    type.type("Do you try to decode it?")
                    decode = ask.yes_or_no()
                    if decode == "yes":
                        type.type("You work it out... A=1, B=2... 'MONEY BURIED UNDER PIER'")
                        print("\n")
                        type.type("You rush to the pier and dig. There's a metal box!")
                        self.change_balance(random.randint(8000, 18000))
                    else:
                        type.type("You keep the code for later.")
                        self.add_item("Mysterious Code")
                
                else:
                    type.type("'HELP ME. STRANDED ON ISLAND. 1847.'")
                    print("\n")
                    type.type("...This message is over 150 years old. You hope they got rescued.")
                print("\n")
            
            elif action == "shake":
                type.type("You shake the bottle. Something rattles inside besides paper...")
                print("\n")
                type.type("You break the bottle open. A small key falls out!")
                self.add_item("Mysterious Key")
                type.type("The paper just says: 'For the vault.'")
                print("\n")
            
            elif action == "throw_back":
                type.type("You throw the bottle back into the sea. Let fate decide its next owner.")
                print("\n")
                if random.random() < 0.2:
                    type.type("A wave immediately throws it back at your feet. Okay, FINE.")
                    self.add_item("Persistent Bottle")
                print("\n")
            
            else:
                type.type("You find a collector on the beach who offers $500 for it, unopened.")
                self.change_balance(500)
                print("\n")
        
        elif event == "crab_racing":
            type.type("A crowd has gathered around a sandy track lit by tiki torches. They're racing CRABS. Big ones. Fast ones. Angry ones.")
            print("\n")
            type.type(yellow("=== CRAB RACING CHAMPIONSHIP ==="))
            print("\n")
            type.type("A sun-weathered man holds up a bucket. " + quote("$500 to race! Pick your crab! Winner takes the pot - $5,000!"))
            print("\n")
            
            # Animal Whistle lets you befriend a racing crab
            if self.has_item("Animal Whistle") and not self.has_companion("Deathclaw"):
                type.type("The " + magenta(bright("Animal Whistle")) + " hums. Every crab in the bucket stops moving and looks up at you.")
                print("\n")
                type.type("The man blinks. " + quote("Well I'll be damned. Never seen 'em do that before."))
                print("\n")
                type.type("A large purple crab climbs out of the bucket and scuttles over to you. It raises one claw - like a salute.")
                print("\n")
                type.type("You've been chosen by Deathclaw himself. The man whistles. " + quote("That crab's never taken to anyone. You must be special."))
                print("\n")
                type.type("Deathclaw becomes your companion. You decide to keep the name " + cyan(bright("Deathclaw")) + ".")
                print("\n")
                type.type("The man waves you off. " + quote("No charge. Consider it destiny."))
                self.add_companion("Deathclaw", "Racing Crab")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                print("\n")
                return
            
            action = input("(race/bet/catch_own/watch): ").strip().lower()
            
            if action == "race":
                if self.get_balance() >= 500:
                    self.change_balance(-500)
                    type.type("You reach into the bucket and pull out a crab. It's purple and VERY angry. The man nods approvingly.")
                    print("\n")
                    type.type(quote("That's Deathclaw. Good luck."))
                    print("\n")
                    type.type("The race starts! Crabs scatter in every direction except forward!")
                    print("\n")
                    type.type("How do you motivate Deathclaw?")
                    motivate = input("(yelling/food/poking/singing): ").strip().lower()
                    
                    if motivate == "food":
                        if self.has_item("Fish") or self.has_item("Live Fish"):
                            type.type("You dangle fish in front of Deathclaw. He ROCKETS forward!")
                            fish_item = "Fish" if self.has_item("Fish") else "Live Fish"
                            self.use_item(fish_item)
                            result = random.choice(["1st", "2nd", "1st", "1st"])
                        else:
                            type.type("You mime having food. Deathclaw is unimpressed.")
                            result = random.choice(["3rd", "4th", "2nd", "3rd"])
                    elif motivate == "singing":
                        type.type("You sing... a sea shanty? Deathclaw pauses. Then starts scuttling... rhythmically?")
                        result = random.choice(["1st", "2nd", "3rd", "2nd"])
                    elif motivate == "poking":
                        type.type("You poke Deathclaw. He turns and PINCHES you.")
                        self.hurt(random.randint(5, 10))
                        result = random.choice(["3rd", "4th", "4th", "3rd"])
                    else:
                        type.type("You scream at the crab. Several spectators look concerned for your sanity.")
                        result = random.choice(["2nd", "3rd", "4th", "2nd"])
                    
                    print("\n")
                    type.type(yellow("=== RACE RESULTS ==="))
                    
                    if result == "1st":
                        type.type("DEATHCLAW WINS! The crowd goes wild! You've never been prouder of a crustacean!")
                        self.change_balance(5000)
                        self.add_item("Crab Racing Trophy")
                    elif result == "2nd":
                        type.type("Second place. Deathclaw takes losing personally.")
                        self.change_balance(1500)
                    else:
                        type.type("Deathclaw gets distracted and wanders off. You lose.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee.")
                    print("\n")
            
            elif action == "bet":
                type.type("Which crab?")
                type.type("1. Pinchy Pete (2:1)")
                type.type("2. Lightning Larry (3:1)")
                type.type("3. Deathclaw (5:1)")
                type.type("4. Mr. Sideways (10:1)")
                pick = input("Pick (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["pete", "pete", "larry", "larry", "death", "sideways"])
                        
                        if pick == "1" and winner == "pete":
                            self.change_balance(bet * 2)
                            type.type("Pinchy Pete wins! " + green(bright("$" + str(bet * 2))) + "!")
                        elif pick == "2" and winner == "larry":
                            self.change_balance(bet * 3)
                            type.type("Lightning Larry lives up to his name! " + green(bright("$" + str(bet * 3))) + "!")
                        elif pick == "3" and winner == "death":
                            self.change_balance(bet * 5)
                            type.type("DEATHCLAW! " + green(bright("$" + str(bet * 5))) + "!")
                        elif pick == "4" and winner == "sideways":
                            self.change_balance(bet * 10)
                            type.type("MR. SIDEWAYS WINS! NOBODY SAW THAT COMING! " + green(bright("$" + str(bet * 10))) + "!")
                        else:
                            type.type("Your crab lost. Back to the ocean with your dreams.")
                    else:
                        type.type("You don't have that kind of money.")
                except:
                    type.type("Betting closed.")
                print("\n")
            
            elif action == "catch_own":
                type.type("You run to the water's edge and try to catch your own crab!")
                print("\n")
                if random.random() < 0.3:
                    type.type("You catch a MASSIVE crab! The regulars look intimidated!")
                    print("\n")
                    type.type("The man waives your entry fee. " + quote("Let's see what that monster can do."))
                    if random.random() < 0.5:
                        type.type("Your wild crab DOMINATES! You win the pot!")
                        self.change_balance(5000)
                    else:
                        type.type("Your crab immediately runs back into the ocean. Freedom > victory, apparently.")
                else:
                    type.type("You get pinched multiple times and catch nothing.")
                    self.hurt(random.randint(5, 15))
                print("\n")
            
            else:
                type.type("You watch the races. A crab named Mr. Sideways pulls off an upset. Good times.")
                print("\n")
        
        elif event == "sandcastle_contest":
            type.type("A sandcastle competition is underway! Elaborate fortresses dot the beach, each more impressive than the last.")
            print("\n")
            type.type(yellow("=== SANDCASTLE CHAMPIONSHIP ==="))
            print("\n")
            type.type("A judge approaches. " + quote("$200 entry. Grand prize is $8,000 and the Golden Shovel trophy!"))
            print("\n")
            action = input("(enter/judge/sabotage/watch): ").strip().lower()
            
            if action == "enter":
                if self.get_balance() >= 200:
                    self.change_balance(-200)
                    type.type("You're given a plot of sand and two hours. Go!")
                    print("\n")
                    type.type("What style do you build?")
                    style = input("(classic_castle/modern/weird/huge): ").strip().lower()
                    
                    score = random.randint(0, 3)
                    
                    if style == "classic_castle":
                        type.type("Towers, walls, a moat - you go traditional. The judges nod approvingly.")
                        score += 2
                    elif style == "modern":
                        type.type("You build a sand sculpture of... a car? A spaceship? It's avant-garde.")
                        if random.random() < 0.5:
                            type.type("The judges are impressed by your creativity!")
                            score += 3
                        else:
                            type.type("The judges are confused.")
                    elif style == "weird":
                        type.type("You build a giant sand crab. It's horrifying. People gather to stare.")
                        score += random.randint(1, 4)
                    else:
                        type.type("You go BIG. The biggest castle this beach has ever seen!")
                        if random.random() < 0.4:
                            type.type("It holds! It's MAGNIFICENT!")
                            score += 4
                        else:
                            type.type("It collapses halfway through. The crowd gasps.")
                            score = 0
                    
                    print("\n")
                    type.type(yellow("=== JUDGING ==="))
                    
                    if score >= 6:
                        type.type("FIRST PLACE! You win the Golden Shovel and " + green(bright("$8,000")) + "!")
                        self.change_balance(8000)
                        self.add_item("Golden Shovel")
                    elif score >= 4:
                        type.type("Second place! " + green(bright("$2,000")) + " and a Silver Bucket!")
                        self.change_balance(2000)
                    elif score >= 2:
                        type.type("Third place. You get a participation ribbon and your money back.")
                        self.change_balance(200)
                    else:
                        type.type("Disqualified for structural failure. Better luck next time.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee.")
                    print("\n")
            
            elif action == "judge":
                type.type("The head judge is sick! They ask you to fill in!")
                print("\n")
                type.type("You walk around judging castles. One builder slips you $500 to vote for them.")
                type.type("Do you take the bribe?")
                bribe = ask.yes_or_no()
                if bribe == "yes":
                    type.type("You pocket the cash and vote for their... mediocre castle. You feel slightly dirty.")
                    self.change_balance(500)
                    self.add_status("Corrupt Judge")
                else:
                    type.type("You judge fairly. A child wins with an adorable turtle sculpture. Heartwarming.")
                    self.add_status("Fair Judge")
                print("\n")
            
            elif action == "sabotage":
                type.type("You wait until no one's looking... then kick over the leading castle!")
                print("\n")
                if random.random() < 0.4:
                    type.type("Success! The builder screams. The crowd gasps. You slip away into the night.")
                    self.add_status("Sandcastle Villain")
                else:
                    type.type("A child sees you and screams " + quote("THAT PERSON KICKED THE CASTLE!"))
                    print("\n")
                    type.type("The crowd turns on you. You run. Someone throws a bucket. It hurts.")
                    self.hurt(random.randint(10, 20))
                print("\n")
            
            else:
                type.type("You watch the competition. Art takes many forms. Some of them are sand.")
                print("\n")
        
        else:
            type.type("Tonight, the beach is peaceful. You lie on the warm sand, watching shooting stars streak across the sky. The waves sing you to sleep.")
            self.heal(random.randint(20, 35))
            self.add_status("Beach Relaxed")
            print("\n")

    def underwater_adventure(self):
        self.meet("Underwater Adventure Event")
        self.add_fatigue(random.randint(12, 22))  # Diving is exhausting
        type.type("You don your gear and slip beneath the waves. The world above fades to silence. Down here, in the blue abyss, ancient secrets wait to be discovered.")
        print("\n")
        type.type(yellow(bright("=== UNDERWATER ADVENTURE ===")))
        print("\n")
        event = random.choice([
            "hunting_competition", "sunken_shipwreck", "giant_octopus", "mermaid_kingdom", "treasure_dive"
        ])
        
        if event == "hunting_competition":
            type.type("You find a gathering of underwater hunters - professional spearfishers preparing for the DEEP SEA HUNT.")
            print("\n")
            type.type(yellow("=== THE DEEP SEA HUNTING CHAMPIONSHIP ==="))
            print("\n")
            type.type("A grizzled hunter with a harpoon gun approaches. " + quote("Entry's $5,000. First prize is $50,000 and the Golden Trident. You in?"))
            print("\n")
            action = input("(compete/bet/sabotage/watch): ").strip().lower()
            
            if action == "compete":
                if self.get_balance() >= 5000:
                    self.change_balance(-5000)
                    type.type("You're given a spear and assigned to Zone 3 - shark territory. The timer starts.")
                    print("\n")
                    
                    # Round 1: Target Selection
                    type.type(yellow("=== ROUND 1: THE HUNT ==="))
                    type.type("You descend into the darkness. Three potential targets:")
                    type.type("- A massive GROUPER hiding in coral (easy, small points)")
                    type.type("- A fast TUNA swimming past (medium, medium points)")
                    type.type("- A legendary MARLIN in the distance (hard, huge points)")
                    print("\n")
                    target = input("(grouper/tuna/marlin): ").strip().lower()
                    
                    hunt_score = random.randint(0, 2)
                    
                    if target == "grouper":
                        type.type("You approach the grouper slowly... it doesn't see you coming...")
                        if random.random() < 0.8:
                            type.type("PERFECT SHOT! The grouper is yours!")
                            hunt_score += 2
                        else:
                            type.type("It spots you at the last second and vanishes into the coral!")
                    elif target == "tuna":
                        type.type("You chase the tuna, matching its speed...")
                        if random.random() < 0.5:
                            type.type("You lead the shot perfectly! The tuna is caught!")
                            hunt_score += 4
                        else:
                            type.type("Too fast! Your spear misses by inches!")
                    else:
                        type.type("You go for glory - the marlin. It's HUGE.")
                        if random.random() < 0.25:
                            type.type("THE SHOT OF A LIFETIME! YOU HIT THE MARLIN!")
                            hunt_score += 8
                        else:
                            type.type("The marlin is too fast, too far. You miss completely.")
                    
                    print("\n")
                    
                    # Round 2: Danger
                    type.type(yellow("=== ROUND 2: DANGER ==="))
                    type.type("A SHARK appears! It smells blood in the water!")
                    print("\n")
                    type.type("How do you handle this?")
                    shark = input("(fight/hide/bait/flee): ").strip().lower()
                    
                    if shark == "fight":
                        type.type("You turn and face the shark, spear ready...")
                        if random.random() < 0.3:
                            type.type("You SPEAR THE SHARK! Bonus points AND you're alive!")
                            hunt_score += 5
                        else:
                            type.type("The shark is faster. It bites your leg before you drive it off.")
                            self.hurt(random.randint(25, 45))
                    elif shark == "hide":
                        type.type("You duck into a crevice. The shark circles... circles...")
                        if random.random() < 0.6:
                            type.type("It loses interest and swims away. Safe!")
                        else:
                            type.type("It finds you! You escape but lose your catch!")
                            hunt_score = max(0, hunt_score - 2)
                    elif shark == "bait":
                        if hunt_score > 0:
                            type.type("You sacrifice your catch! The shark takes the bait!")
                            hunt_score = 0
                            type.type("You're alive but starting over.")
                        else:
                            type.type("You have nothing to bait with! The shark CHARGES!")
                            self.hurt(random.randint(20, 35))
                    else:
                        type.type("You swim for the surface as fast as you can!")
                        if random.random() < 0.5:
                            type.type("You escape! But you lose valuable hunting time.")
                            hunt_score = max(0, hunt_score - 1)
                        else:
                            type.type("The shark catches you before you can escape!")
                            self.hurt(random.randint(30, 50))
                    
                    print("\n")
                    
                    # Round 3: Final Push
                    type.type(yellow("=== ROUND 3: FINAL HUNT ==="))
                    type.type("Time is running out! One last chance to catch something!")
                    final = input("(deep_dive/surface_hunt/ambush): ").strip().lower()
                    
                    if final == "deep_dive":
                        type.type("You dive DEEP, into the darkness where monsters lurk...")
                        if random.random() < 0.3:
                            type.type("You find a GIANT SEA BASS! It's massive! You spear it!")
                            hunt_score += 6
                        else:
                            type.type("Too dark. You catch nothing and barely make it back up.")
                    elif final == "surface_hunt":
                        type.type("You stay shallow where the fish are plentiful...")
                        type.type("You catch several smaller fish!")
                        hunt_score += random.randint(2, 4)
                    else:
                        type.type("You set up an ambush near a reef...")
                        if random.random() < 0.5:
                            type.type("A beautiful reef fish swims right into your trap!")
                            hunt_score += 4
                        else:
                            type.type("Nothing takes the bait. The reef is empty today.")
                    
                    print("\n")
                    type.type(yellow("=== RESULTS ==="))
                    
                    if hunt_score >= 15:
                        type.type("YOU WIN THE CHAMPIONSHIP! Your catches are LEGENDARY!")
                        print("\n")
                        type.type("The Golden Trident is yours, along with " + green(bright("$50,000")) + "!")
                        self.change_balance(50000)
                        self.add_item("Golden Trident")
                    elif hunt_score >= 10:
                        type.type("Second place! Impressive hunting!")
                        self.change_balance(random.randint(12000, 20000))
                    elif hunt_score >= 5:
                        type.type("Third place. Not bad for the deep sea.")
                        self.change_balance(random.randint(6000, 10000))
                    else:
                        type.type("You didn't place. The ocean bested you today.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. Maybe next time.")
                    print("\n")
            
            elif action == "bet":
                type.type("Who do you bet on?")
                type.type("1. The Champion - Harpoon Harry (2:1)")
                type.type("2. The Newcomer - Sally Spear (4:1)")
                type.type("3. The Veteran - Old Man Sea (3:1)")
                type.type("4. The Wildcard - Crazy Ivan (8:1)")
                pick = input("Pick (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["harry", "harry", "sally", "sea", "sea", "ivan"])
                        
                        if pick == "1" and winner == "harry":
                            self.change_balance(bet * 2)
                            type.type("Harpoon Harry wins! " + green(bright("$" + str(bet * 2))) + "!")
                        elif pick == "2" and winner == "sally":
                            self.change_balance(bet * 4)
                            type.type("The newcomer shocks everyone! " + green(bright("$" + str(bet * 4))) + "!")
                        elif pick == "3" and winner == "sea":
                            self.change_balance(bet * 3)
                            type.type("Old Man Sea proves experience matters! " + green(bright("$" + str(bet * 3))) + "!")
                        elif pick == "4" and winner == "ivan":
                            self.change_balance(bet * 8)
                            type.type("CRAZY IVAN WINS! NOBODY SAW THAT COMING! " + green(bright("$" + str(bet * 8))) + "!")
                        else:
                            type.type("Your pick lost. Better luck next time.")
                    else:
                        type.type("You can't bet that much.")
                except:
                    type.type("Betting closed.")
                print("\n")
            
            elif action == "sabotage":
                type.type("You sneak around, looking for opportunities to cheat...")
                print("\n")
                type.type("You could cut someone's air hose, steal their catch, or release a shark near them.")
                sabotage = input("(airhose/steal/shark): ").strip().lower()
                
                if sabotage == "airhose":
                    if random.random() < 0.3:
                        type.type("You cut the champion's air hose! He has to surface early! Disqualified!")
                        type.type("The odds shift dramatically - you bet on the second favorite and WIN!")
                        self.change_balance(random.randint(8000, 15000))
                    else:
                        type.type("You're CAUGHT! The hunters don't take kindly to attempted murder!")
                        self.hurt(random.randint(40, 60))
                        self.add_status("Underwater Criminal")
                elif sabotage == "steal":
                    if random.random() < 0.5:
                        type.type("You grab a prize marlin from another hunter's line!")
                        self.add_item("Stolen Marlin")
                        self.change_balance(random.randint(5000, 10000))
                    else:
                        type.type("The hunter notices and attacks you with a spear!")
                        self.hurt(random.randint(25, 40))
                else:
                    type.type("You release chum to attract sharks near the other hunters...")
                    if random.random() < 0.4:
                        type.type("CHAOS! Sharks everywhere! The competition is called off!")
                        type.type("In the confusion, you grab abandoned catches.")
                        self.change_balance(random.randint(6000, 12000))
                    else:
                        type.type("The sharks find YOU first. Bad plan. Very bad plan.")
                        self.hurt(random.randint(35, 55))
                print("\n")
            
            else:
                type.type("You watch from a safe distance. Harpoon Harry wins again. The guy is legendary.")
                self.add_status("Oceanwise")
                print("\n")
        
        elif event == "sunken_shipwreck":
            type.type("Your light catches something massive on the ocean floor - the remains of an ancient ship, half-buried in sand.")
            print("\n")
            type.type(yellow("=== THE SUNKEN WRECK ==="))
            print("\n")
            type.type("The ship looks centuries old. Its cargo hold is partially exposed. Sharks circle lazily above.")
            print("\n")
            action = input("(explore/quick_loot/photograph/leave): ").strip().lower()
            
            if action == "explore":
                type.type("You descend carefully toward the wreck. The wood creaks even underwater.")
                print("\n")
                type.type("Where do you explore first?")
                area = input("(captains_quarters/cargo_hold/deck/hull): ").strip().lower()
                
                if area == "captains_quarters":
                    type.type("You squeeze through a broken window into the captain's quarters...")
                    print("\n")
                    type.type("A skeleton in a captain's uniform sits at a desk, a chest beside it.")
                    type.type("Do you open the chest?")
                    open_it = ask.yes_or_no()
                    if open_it == "yes":
                        if random.random() < 0.6:
                            type.type("GOLD COINS! The captain's personal fortune!")
                            self.change_balance(random.randint(15000, 35000))
                            self.add_item("Captain's Compass")
                        else:
                            type.type("A trap! The chest releases ink, blinding you! You barely escape!")
                            self.hurt(random.randint(15, 30))
                    else:
                        type.type("You leave the captain to his eternal rest.")
                
                elif area == "cargo_hold":
                    type.type("You swim into the cargo hold. Crates everywhere, most rotted away.")
                    print("\n")
                    if random.random() < 0.5:
                        type.type("You find crates of preserved spices - still valuable to collectors!")
                        self.change_balance(random.randint(8000, 15000))
                    else:
                        type.type("The floor gives way! You fall into a lower deck and get trapped!")
                        print("\n")
                        type.type("Your air is running low! How do you escape?")
                        escape = input("(break_hull/signal/calm): ").strip().lower()
                        if escape == "break_hull":
                            type.type("You smash through rotted wood and swim free!")
                            self.hurt(random.randint(10, 20))
                        elif escape == "signal":
                            if random.random() < 0.5:
                                type.type("Other divers see your signal! They pull you free!")
                            else:
                                type.type("No one sees. You have to break your way out anyway.")
                                self.hurt(random.randint(15, 25))
                        else:
                            type.type("You stay calm, conserve air, find a gap in the wood, and squeeze through.")
                
                elif area == "deck":
                    type.type("You explore the main deck. A cannon still points toward the enemy that sank this ship.")
                    print("\n")
                    type.type("You find cannonballs nearby - solid iron, valuable as antiques.")
                    self.change_balance(random.randint(5000, 10000))
                    if random.random() < 0.3:
                        type.type("Wait - there's something stuck in the cannon! A gem! Someone hid it there!")
                        self.add_item("Cannon Gem")
                
                else:
                    type.type("You explore the hull breach that sank this ship. Inside, you find skeletons of sailors.")
                    print("\n")
                    type.type("One still clutches a lockbox. Do you take it?")
                    take = ask.yes_or_no()
                    if take == "yes":
                        if self.has_item("Skeleton Key"):
                            type.type("The " + cyan(bright("Skeleton Key")) + " doesn't just open the lock — it opens the concept of locked.")
                            print("\n")
                            type.type("The door's lock explains why it was locked, what it's protecting, and thanks you for understanding.")
                            self.change_balance(random.randint(300, 800))
                            self.restore_sanity(5)
                            return
                        elif self.has_item("All-Access Pass"):
                            type.type("The " + cyan(bright("All-Access Pass")) + " reveals doors that don't exist on any map.")
                            print("\n")
                            type.type("Behind this one: legendary loot that no one else has reached.")
                            self.change_balance(random.randint(200, 600))
                            self.restore_sanity(3)
                            return
                        elif self.has_item("Master Key"):
                            type.type("You hold the " + cyan(bright("Master Key")) + " to the rusted lock. It opens in two seconds.")
                            print("\n")
                            type.type("Inside: gold doubloons and a gemstone that catches the light even down here.")
                            self.change_balance(random.randint(3000, 8000))
                        elif self.has_item("Lockpick Set"):
                            type.type("You work the " + cyan(bright("Lockpick Set")) + " on the rusted lock, careful and methodical even underwater.")
                            print("\n")
                            type.type("It opens. Inside: a handful of coins and a sealed letter in a language you don't recognize. Still valuable.")
                            self.change_balance(random.randint(1500, 4000))
                        elif self.has_item("Security Bypass"):
                            type.type("The lock has a corroded electronic mechanism — old ship tech. The " + cyan(bright("Security Bypass")) + " interfaces with it somehow.")
                            print("\n")
                            type.type("Access granted. Inside: navigational instruments in near-perfect condition. Rare finds.")
                            self.change_balance(random.randint(2000, 6000))
                        else:
                            type.type("You pry it from skeletal fingers. The lock is rusted shut.")
                            self.add_item("Sailor's Lockbox")
                    else:
                        type.type("You leave the dead in peace.")
                print("\n")
            
            elif action == "quick_loot":
                type.type("You grab what you can see quickly - no time for deep exploration.")
                if random.random() < 0.7:
                    type.type("You snag some coins and a silver chalice before a shark notices you.")
                    self.change_balance(random.randint(5000, 12000))
                else:
                    type.type("A shark charges! You drop everything and swim for your life!")
                    self.hurt(random.randint(15, 30))
                print("\n")
            
            elif action == "photograph":
                type.type("You photograph the wreck instead of looting it. This could be an archaeological find!")
                print("\n")
                type.type("Do you sell the photos to a museum or a treasure hunter?")
                sell = input("(museum/hunter): ").strip().lower()
                if sell == "museum":
                    type.type("The museum pays you a finder's fee.")
                    self.change_balance(random.randint(8000, 15000))
                    self.add_status("Archaeological Hero")
                else:
                    type.type("The treasure hunter pays WELL for the location.")
                    self.change_balance(random.randint(15000, 25000))
                    self.add_status("Morally Flexible")
                print("\n")
            
            else:
                type.type("You leave the wreck undisturbed. Some things are better left buried.")
                print("\n")
        
        elif event == "giant_octopus":
            type.type("The water grows dark. Something MASSIVE moves in the depths. Eight tentacles, each thicker than your body, unfurl from the abyss.")
            print("\n")
            
            # Animal Whistle can befriend even the Kraken
            if self.has_item("Animal Whistle") and not self.has_companion("Kraken"):
                type.type("The " + magenta(bright("Animal Whistle")) + " pulses with deep oceanic power. The water vibrates.")
                print("\n")
                type.type("The massive octopus stops. Its enormous eye fixes on you, but there's no hunger now - only curiosity.")
                print("\n")
                type.type("A tentacle extends, gently wrapping around your arm. Not threatening. Questioning.")
                print("\n")
                type.type("You place your hand on its rubbery skin. The kraken makes a sound - deep, resonant, almost... joyful?")
                print("\n")
                type.type("You've bonded with a legendary sea creature. You call it " + cyan(bright("Kraken")) + ".")
                print("\n")
                type.type("The Kraken will watch over your journeys from the deep. It gifts you a pearl of immense value before sinking away.")
                self.add_companion("Kraken", "Giant Octopus")
                self.increment_statistic("companions_befriended")
                self.unlock_achievement("first_friend")
                self.add_item("Kraken Pearl")
                self.change_balance(random.randint(40000, 70000))
                self.add_status("Kraken Friend")
                print("\n")
                return
            
            type.type(yellow("=== BOSS ENCOUNTER: THE KRAKEN ==="))
            print("\n")
            type.type("A giant octopus - ancient, intelligent, and HUNGRY. Its eye, the size of a dinner plate, focuses on YOU.")
            print("\n")
            action = input("(fight/communicate/flee/offer): ").strip().lower()
            
            if action == "fight":
                type.type(yellow("=== BATTLE: YOU VS. THE KRAKEN ==="))
                print("\n")
                type.type("You raise your spear. This is insane. This is suicide. This is... HAPPENING.")
                print("\n")
                type.type("The kraken attacks! A tentacle sweeps toward you!")
                attack1 = input("(dodge/cut/grab): ").strip().lower()
                
                kraken_damage = 0
                
                if attack1 == "dodge":
                    if random.random() < 0.6:
                        type.type("You twist away! The tentacle misses!")
                    else:
                        type.type("Too slow! It catches your leg!")
                        self.hurt(random.randint(20, 35))
                        kraken_damage -= 1
                elif attack1 == "cut":
                    if random.random() < 0.4:
                        type.type("Your blade bites deep! Ink clouds the water!")
                        kraken_damage += 2
                    else:
                        type.type("Your blade bounces off its rubbery skin!")
                else:
                    type.type("You GRAB the tentacle?! Bold move!")
                    if random.random() < 0.3:
                        type.type("You use its own momentum against it!")
                        kraken_damage += 1
                    else:
                        type.type("It wraps around you and SQUEEZES!")
                        self.hurt(random.randint(25, 40))
                
                print("\n")
                type.type("The kraken's beak snaps at you! Those jaws could crush a boat!")
                attack2 = input("(eyes/throat/retreat): ").strip().lower()
                
                if attack2 == "eyes":
                    if random.random() < 0.35:
                        type.type("You JAB at its eye! The kraken SCREAMS underwater! It releases you!")
                        kraken_damage += 3
                    else:
                        type.type("It blinks! Your attack deflects off its eyelid!")
                elif attack2 == "throat":
                    type.type("You dive for its beak, aiming for the soft throat...")
                    if random.random() < 0.25:
                        type.type("CRITICAL HIT! The kraken recoils in pain!")
                        kraken_damage += 4
                    else:
                        type.type("Its beak snaps shut, nearly taking your arm!")
                        self.hurt(random.randint(30, 45))
                else:
                    type.type("You create distance. The kraken pauses, considering you.")
                
                print("\n")
                
                if kraken_damage >= 5:
                    type.type("The kraken has had ENOUGH. It retreats into the depths, leaving behind... a PEARL.")
                    print("\n")
                    type.type("Not just any pearl - a KRAKEN PEARL. Priceless. Legendary.")
                    self.add_item("Kraken Pearl")
                    self.change_balance(random.randint(30000, 60000))
                elif kraken_damage >= 2:
                    type.type("The kraken considers you not worth the effort. It sinks away, leaving you alive.")
                else:
                    type.type("The kraken wraps you in tentacles and drags you deeper before you escape.")
                    self.hurt(random.randint(35, 55))
                print("\n")
            
            elif action == "communicate":
                type.type("You extend your arms in a non-threatening gesture. The kraken pauses.")
                print("\n")
                type.type("Its massive eye studies you. Intelligence sparkles within.")
                print("\n")
                if random.random() < 0.4:
                    type.type("It... understands? A tentacle gently touches your head. Images flood your mind.")
                    print("\n")
                    type.type("The location of treasure. Ancient secrets. The kraken shares its knowledge.")
                    self.add_item("Kraken's Memory")
                    self.add_status("Kraken Friend")
                    self.change_balance(random.randint(10000, 25000))
                else:
                    type.type("The kraken is not interested in communication. It simply... leaves.")
                    type.type("You're alive. That's more than most can say.")
                print("\n")
            
            elif action == "offer":
                type.type("You remember you have some fish. You offer them to the kraken.")
                print("\n")
                if self.has_item("Fish") or self.has_item("Live Fish") or self.has_item("Stolen Marlin"):
                    type.type("The kraken accepts your offering! It seems... grateful?")
                    print("\n")
                    type.type("It gently places something in your hands - a glowing stone from the deep.")
                    self.add_item("Deep Stone")
                    self.add_status("Kraken Respect")
                else:
                    type.type("You mime offering food. The kraken is unimpressed by your empty hands.")
                    type.type("It lets you go, but barely.")
                print("\n")
            
            else:
                type.type("You SWIM. Faster than you've ever swum. The kraken's tentacles reach for you...")
                print("\n")
                if random.random() < 0.5:
                    type.type("You reach your boat just in time! The tentacles slap the hull but you're SAFE!")
                else:
                    type.type("It catches your leg! You kick free but not without damage!")
                    self.hurt(random.randint(20, 40))
                print("\n")
        
        elif event == "mermaid_kingdom":
            type.type("You spot something impossible - lights in the deep. Buildings. A CITY beneath the waves.")
            print("\n")
            type.type(yellow("=== THE MERMAID KINGDOM ==="))
            print("\n")
            type.type("Mermaids swim through coral towers, going about their daily lives. One spots you and approaches.")
            print("\n")
            type.type("She's beautiful - iridescent scales, flowing hair, a voice like music even underwater.")
            print("\n")
            type.type(quote("A surface dweller! We haven't had a visitor in centuries! Will you join us for a feast?"))
            print("\n")
            action = input("(accept/decline/ask_questions/steal): ").strip().lower()
            
            if action == "accept":
                type.type("You follow the mermaid into the city. The architecture is breathtaking - made of coral and pearl.")
                print("\n")
                type.type("The feast is incredible - foods you've never seen, drinks that let you breathe underwater longer.")
                print("\n")
                type.type("After the feast, the Mermaid Queen approaches.")
                print("\n")
                type.type(quote("You've shown respect. Take this gift from our kingdom."))
                self.add_item("Mermaid Crown")
                self.change_balance(random.randint(15000, 30000))
                self.heal(random.randint(30, 50))
                print("\n")
            
            elif action == "ask_questions":
                type.type(quote("What is this place? How do you live down here?"))
                print("\n")
                type.type("The mermaid explains - they've lived here for millennia, hidden from the surface world.")
                print("\n")
                type.type(quote("We have treasures from every shipwreck. Knowledge from ages past. Would you like to see our library?"))
                library = ask.yes_or_no()
                if library == "yes":
                    type.type("The library holds ancient maps and secrets. One map shows treasure locations on land!")
                    self.add_item("Ancient Sea Map")
                    self.change_balance(random.randint(10000, 20000))
                else:
                    type.type("You decline politely. The mermaid looks disappointed but gives you a pearl for your respect.")
                    self.add_item("Mermaid Pearl")
                print("\n")
            
            elif action == "steal":
                type.type("You pretend interest while looking for valuables to grab...")
                print("\n")
                if random.random() < 0.3:
                    type.type("You snag a golden artifact and swim for the surface!")
                    self.change_balance(random.randint(12000, 22000))
                    self.add_status("Mermaid Enemy")
                else:
                    type.type("They catch you immediately. Mermaids are FAST.")
                    print("\n")
                    type.type("They don't kill you - they curse you instead.")
                    self.add_status("Sea Cursed")
                    self.hurt(random.randint(20, 35))
                print("\n")
            
            else:
                type.type("You politely decline and swim away. The mermaid looks sad but waves goodbye.")
                type.type("Some mysteries are better left unexplored.")
                print("\n")
        
        else:  # treasure_dive
            type.type("You found it - the coordinates from an old treasure map. X marks the spot, and you're directly above it.")
            print("\n")
            type.type(yellow("=== THE TREASURE DIVE ==="))
            print("\n")
            type.type("The dive will be deep - dangerous. But the treasure could be life-changing.")
            print("\n")
            action = input("(dive/hire_help/sell_map/abandon): ").strip().lower()
            
            if action == "dive":
                type.type("You take a deep breath and descend into the abyss...")
                print("\n")
                type.type("Deeper... darker... your flashlight barely cuts through the murk...")
                print("\n")
                type.type("There! A chest! But also... danger. A moray eel guards the spot.")
                eel = input("(fight_eel/distract/sneak): ").strip().lower()
                
                if eel == "fight_eel":
                    if random.random() < 0.5:
                        type.type("You spear the eel! The treasure is yours!")
                        self.change_balance(random.randint(25000, 50000))
                        self.add_item("Pirate Treasure")
                    else:
                        type.type("The eel bites you HARD. You grab some treasure and escape.")
                        self.hurt(random.randint(25, 40))
                        self.change_balance(random.randint(10000, 20000))
                elif eel == "distract":
                    type.type("You throw some bait away from the chest. The eel investigates...")
                    if random.random() < 0.7:
                        type.type("You grab the chest and SWIM! The treasure is yours!")
                        self.change_balance(random.randint(20000, 40000))
                    else:
                        type.type("The eel catches on and attacks! You escape with only a few coins.")
                        self.change_balance(random.randint(3000, 8000))
                        self.hurt(random.randint(15, 25))
                else:
                    type.type("You move slowly, silently, reaching for the chest...")
                    if random.random() < 0.4:
                        type.type("The eel never notices. You take the treasure and leave.")
                        self.change_balance(random.randint(25000, 45000))
                    else:
                        type.type("You bump the chest! The eel attacks!")
                        self.hurt(random.randint(20, 35))
                        self.change_balance(random.randint(5000, 12000))
                print("\n")
            
            elif action == "hire_help":
                type.type("You hire professional divers to help. Cost: $5,000.")
                if self.get_balance() >= 5000:
                    self.change_balance(-5000)
                    type.type("The team descends with you. Strength in numbers!")
                    print("\n")
                    type.type("They handle the eel, you grab the treasure. A clean operation.")
                    loot = random.randint(20000, 35000)
                    type.type("Total haul: " + green(bright("$" + str(loot))) + " after splitting with the crew.")
                    self.change_balance(loot)
                else:
                    type.type("You can't afford the help. You'll have to go alone or not at all.")
                print("\n")
            
            elif action == "sell_map":
                type.type("You sell the map's location to a collector.")
                self.change_balance(random.randint(8000, 15000))
                type.type("Easy money. No risk. But you'll always wonder what was really down there.")
                print("\n")
            
            else:
                type.type("Too dangerous. You keep the coordinates for another day.")
                self.add_item("Treasure Coordinates")
                print("\n")
        print("\n")

    def city_adventure(self):
        self.meet("City Adventure Event")
        self.add_fatigue(random.randint(8, 15))  # City nightlife
        type.type("The city at night is two worlds stacked on top of each other. ")
        type.type("Penthouses gleaming above, gutters rotting below. ")
        type.type("The rich don't look down. The poor can't look up.")
        print("\n")
        type.type(yellow(bright("=== CITY AFTER DARK ===")))
        print("\n")
        event = random.choice([
            "underground_den", "overdose_witness", "loan_shark", "homeless_camp",
            "crack_alley", "penthouse_party", "desperate_gambler", "bank_heist", "casual_night"
        ])
        
        if event == "underground_den":
            type.type("Down a stairwell that smells like piss and broken dreams, you find it. An underground gambling den. No windows. No exits except the one you came in.")
            print("\n")
            type.type("The air is thick with cigarette smoke and desperation. Men hunched over tables, eyes hollow, feeding bills into games they can't win.")
            print("\n")
            type.type("A woman in the corner is crying. Nobody looks at her. A man next to her bets his wedding ring.")
            print("\n")
            type.type(yellow("=== THE UNDERGROUND DEN ==="))
            print("\n")
            type.type("A bouncer with no neck approaches. " + quote("You play or you leave. House takes forty percent."))
            print("\n")
            action = input("(play/watch/help_woman/leave): ").strip().lower()
            
            if action == "play":
                type.type("You sit at a table. The game is rigged - you can tell immediately. The dealer's hands move too fast, the cards feel wrong.")
                print("\n")
                type.type("But you play anyway. Because that's what you do. That's what you are.")
                print("\n")
                type.type("How much do you put in?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        if random.random() < 0.25:  # House is rigged
                            winnings = int(bet * 1.5)
                            type.type("You win. " + green(bright("$" + str(winnings))) + ". The bouncer watches you closer now.")
                            self.change_balance(winnings)
                        else:
                            type.type("You lose. Of course you lose. The house always wins in places like this.")
                            type.type("The crying woman looks at you. Recognition in her eyes. She's been you. You're becoming her.")
                    else:
                        type.type("You don't have enough. The bouncer's hand is on your shoulder before you can explain.")
                        self.hurt(random.randint(10, 20))
                except:
                    type.type("The bouncer doesn't like hesitation. You're escorted out. Roughly.")
                    self.hurt(random.randint(5, 15))
                print("\n")
            
            elif action == "help_woman":
                type.type("You approach the crying woman. Up close, you can see track marks on her arms. She's young - too young for eyes that dead.")
                print("\n")
                type.type(quote("Please,") + " she whispers. " + quote("I just need enough to get home. He took everything. My phone, my shoes, everything."))
                print("\n")
                give = ask.yes_or_no("Give her money?")
                if give == "yes":
                    type.type("You press $200 into her hand. She doesn't say thank you. Just stares at the money like she's forgotten what it's for.")
                    self.change_balance(-200)
                    print("\n")
                    type.type("Then she walks to the table and bets it all.")
                    print("\n")
                    type.type("She loses.")
                    print("\n")
                    type.type("The crying starts again. You leave before you can watch anymore.")
                else:
                    type.type("You can't save everyone. You can barely save yourself.")
                    type.type("Her sobs follow you up the stairs and into the night.")
                print("\n")
            
            elif action == "watch":
                type.type("You stand in the corner and watch. This is what addiction looks like when the pretty wrapping comes off.")
                print("\n")
                type.type("A man wins $500 and immediately bets $600. A woman loses her third straight hand and asks for a 'loan' from a man in a pinstripe suit.")
                print("\n")
                type.type("You see the loan shark's eyes light up. Fresh meat.")
                print("\n")
                type.type("Nobody leaves this place richer. Not really. The money just moves around until the house takes it all.")
                print("\n")
                type.type("You learn something about yourself watching them. Something you didn't want to know.")
                self.add_status("Self-Aware")
                print("\n")
            
            else:
                type.type("You turn and leave. The bouncer calls after you: " + quote("You'll be back. They always come back."))
                print("\n")
                type.type("You tell yourself he's wrong.")
                print("\n")
                type.type("You're not sure you believe it.")
                print("\n")
        
        elif event == "overdose_witness":
            type.type("An alley. A body. At first you think they're dead.")
            print("\n")
            type.type("Then you see the chest move. Barely.")
            print("\n")
            type.type("A young man, maybe nineteen, foam at the corners of his mouth. A needle still in his arm. His lips are blue. His eyes are rolled back.")
            print("\n")
            type.type(yellow("=== THE OVERDOSE ==="))
            print("\n")
            type.type("You could call 911. You could try to help. You could walk away like everyone else.")
            print("\n")
            action = input("(call_911/help/narcan/leave): ").strip().lower()
            
            if action == "call_911":
                type.type("You dial. Your hands are shaking. The operator asks questions you don't know the answers to.")
                print("\n")
                type.type("Paramedics arrive. They push you aside, professional and tired. They've done this before. They'll do it again.")
                print("\n")
                if random.random() < 0.7:
                    type.type("He lives. Barely. They load him into the ambulance. One paramedic looks at you.")
                    print("\n")
                    type.type(quote("Most people just walk by. Thanks for not being most people."))
                    self.add_status("Decent Human")
                else:
                    type.type("They try. They really try. But he's been down too long.")
                    print("\n")
                    type.type("The paramedic shakes her head. " + quote("We'll take it from here."))
                    print("\n")
                    type.type("You walk away with death on your hands. Or maybe you just walk away.")
                print("\n")
            
            elif action == "help":
                type.type("You kneel beside him. You don't know what you're doing but you try - chest compressions, mouth to mouth, something you half-remember from a movie.")
                print("\n")
                type.type("His skin is cold. His heart is barely beating.")
                print("\n")
                if random.random() < 0.4:
                    type.type("He gasps. Coughs. Eyes flutter open. He looks at you like you're a stranger - because you are.")
                    print("\n")
                    type.type(quote("Don't call anyone,") + " he whispers. " + quote("Please. They'll lock me up again."))
                    print("\n")
                    type.type("You help him to his feet. He limps away into the darkness. You'll never know if he made it.")
                else:
                    type.type("Nothing works. You try until someone pulls you away - a woman in scrubs, running home from her night shift.")
                    print("\n")
                    type.type(quote("It's too late, honey. It was probably too late before you got here."))
                    print("\n")
                    type.type("You sit on the curb for a long time after they take the body away.")
                    self.hurt(random.randint(5, 10))  # Emotional damage
                print("\n")
            
            elif action == "narcan":
                if self.has_met("Dealer Narcan"):
                    type.type("You have Narcan. Why do you have Narcan? You don't ask yourself that question.")
                    print("\n")
                    type.type("You administer it. His eyes snap open. He gasps, panics, swings at you.")
                    print("\n")
                    type.type(quote("What the fuck? What the FUCK?"))
                    print("\n")
                    type.type("He doesn't thank you. He's angry. You just killed his high.")
                    print("\n")
                    type.type("He stumbles away. You'll see him again, in another alley, with another needle. Or you won't.")
                else:
                    type.type("You don't have Narcan. But you know where to get it - the woman at the convenience store keeps it behind the counter.")
                    print("\n")
                    type.type("By the time you get back, the alley is empty. Someone else found him. Or didn't.")
                print("\n")
            
            else:
                type.type("You keep walking. Like everyone else. Like you've always done.")
                print("\n")
                type.type("Someone else's problem. Someone else's son.")
                print("\n")
                type.type("The city swallows him. The city swallows everything.")
                print("\n")
        
        elif event == "loan_shark":
            type.type("He finds you. They always find you. A man in a nice suit with a smile that doesn't reach his eyes.")
            print("\n")
            type.type(quote("You look like someone who could use a little... liquidity."))
            print("\n")
            type.type(yellow("=== THE LOAN SHARK ==="))
            print("\n")
            type.type(quote("I'm Mr. Vincent. I help people like you. People who need money right now, no questions asked."))
            print("\n")
            type.type("His terms: any amount up to $50,000. Twenty percent interest. Per week.")
            print("\n")
            action = input("(borrow/refuse/threaten/ask_about_him): ").strip().lower()
            
            if action == "borrow":
                type.type("How much do you need?")
                try:
                    amount = int(input("Amount: $"))
                    if amount > 0 and amount <= 50000:
                        self.change_balance(amount)
                        type.type("He counts the money out. Slow. Deliberate. Making sure you see every bill.")
                        print("\n")
                        type.type(quote("You've got one week. After that, I add twenty percent. After two weeks, I send my associates."))
                        print("\n")
                        type.type("He hands you a card with just a phone number.")
                        print("\n")
                        type.type(quote("Don't make me come find you."))
                        self.add_status("Loan Shark Debt")
                        # Store the debt amount somewhere
                    else:
                        type.type(quote("Cute. Come back when you're serious."))
                except:
                    type.type(quote("Not in the mood for games. Find me when you grow up."))
                print("\n")
            
            elif action == "threaten":
                type.type(quote("I know people who eat loan sharks for breakfast."))
                print("\n")
                type.type("Vincent laughs. It's not a nice laugh.")
                print("\n")
                type.type(quote("Kid, I AM the people who eat people for breakfast."))
                print("\n")
                type.type("Two men materialize from the shadows. You didn't see them before. That's concerning.")
                print("\n")
                type.type(quote("Consider this a free lesson in manners."))
                self.hurt(random.randint(20, 40))
                self.change_balance(-random.randint(1000, 5000))
                print("\n")
            
            elif action == "ask_about_him":
                type.type(quote("What's your story, Vincent?"))
                print("\n")
                type.type("He seems surprised by the question. Nobody asks him questions.")
                print("\n")
                type.type(quote("I grew up in places like this.") + " He gestures at the street. ")
                type.type(quote("Watched my father gamble away everything. My mother worked three jobs until it killed her. I swore I'd never be poor again."))
                print("\n")
                type.type("He adjusts his cufflinks. Gold. Expensive.")
                print("\n")
                type.type(quote("Now I help people make the same mistakes my father made. Circle of life."))
                print("\n")
                type.type("He walks away without offering you money. You might have seen something human in him. Or maybe you imagined it.")
                print("\n")
            
            else:
                type.type(quote("I'm good."))
                print("\n")
                type.type(quote("Nobody's ever good,") + " he says. " + quote("But suit yourself. I'll be around when you change your mind."))
                print("\n")
        
        elif event == "homeless_camp":
            type.type("Under the overpass, a city within the city. Tents made of tarps. Shopping carts full of everything someone owns. A fire in a barrel.")
            print("\n")
            type.type("These are the people the penthouses don't see. The ones the city pretends don't exist.")
            print("\n")
            type.type(yellow("=== THE ENCAMPMENT ==="))
            print("\n")
            type.type("An old man waves you over. His beard is gray and matted. His eyes are surprisingly clear.")
            print("\n")
            type.type(quote("You lost?") + " he asks. " + quote("Or you one of us now?"))
            print("\n")
            action = input("(sit/give_money/share_food/ask_advice/leave): ").strip().lower()
            
            if action == "sit":
                type.type("You sit by the fire. Nobody asks questions. Nobody judges. For a while, you're just another body trying to stay warm.")
                print("\n")
                type.type("The old man tells stories. He used to be a banker. Lost it all to gambling - then the drinking started, then the divorce, then the street.")
                print("\n")
                type.type(quote("Funny thing is, I'm happier now than I ever was in that corner office. Got nothing left to lose."))
                print("\n")
                type.type("You don't know if that's wisdom or delusion. Maybe there's no difference.")
                self.heal(random.randint(10, 20))
                self.add_status("Humbled")
                print("\n")
            
            elif action == "give_money":
                amount = random.randint(100, 500)
                type.type("You hand over " + str(amount) + " dollars. The old man looks at it, then at you.")
                self.change_balance(-amount)
                print("\n")
                type.type(quote("You sure? Money like this won't fix nothing for us. It'll be gone by morning - booze, food, gone."))
                print("\n")
                type.type("He takes it anyway. Passes it around the camp. For one night, they eat well.")
                print("\n")
                type.type(quote("Thanks, stranger. Hope you find what you're looking for."))
                print("\n")
            
            elif action == "share_food":
                food_items = ["Turkey Sandwich", "Beef Jerky", "Granola Bar", "Hot Dog",
                              "Candy Bar", "Bread", "Cheese", "Cup Noodles", "Microwave Burrito"]
                shared_food = next((f for f in food_items if self.has_item(f)), None)
                if shared_food:
                    type.type("You share what you have. It's not much, but their gratitude is real.")
                    self.use_item(shared_food)
                else:
                    type.type("You don't have any food. But you sit with them while they eat what they have.")
                print("\n")
                type.type("A woman shows you a picture - a daughter somewhere, a life that used to be.")
                print("\n")
                type.type(quote("We're not that different, you and me. Just a few bad breaks apart."))
                print("\n")
            
            elif action == "ask_advice":
                type.type(quote("You look like you know things. What's the secret to surviving out here?"))
                print("\n")
                type.type("The old man laughs.")
                print("\n")
                type.type(quote("Secret? There ain't no secret. You just don't die. And some days that's harder than others."))
                print("\n")
                type.type("He points at your clothes, your shoes, the way you carry yourself.")
                print("\n")
                type.type(quote("You got a gambling problem. I can smell it on you. Here's my advice: stop. Just stop. Before you end up here."))
                print("\n")
                type.type(quote("But you won't. Nobody ever does. We just keep playing until we lose everything."))
                self.add_status("Warned")
                print("\n")
            
            else:
                type.type("You leave. The firelight fades behind you. Tomorrow, you'll forget they exist.")
                print("\n")
                type.type("That's how the city works. Out of sight, out of mind.")
                print("\n")
        
        elif event == "crack_alley":
            type.type("You took a wrong turn. Or maybe the right one, depending on what you're looking for.")
            print("\n")
            type.type("The alley is alive with shadows and whispers. The smell of burnt chemicals. Eyes watching from doorways.")
            print("\n")
            type.type(yellow("=== CRACK ALLEY ==="))
            print("\n")
            if self.has_item("Intelligence Dossier"):
                type.type("The " + cyan(bright("Intelligence Dossier")) + " has a full section on this block. You know who controls it and exactly how to avoid them.")
                print("\n")
                type.type("You take the long way around. No confrontation. No drama. Just the right route at the right time.")
                self.restore_sanity(5)
                print("\n")
                action = "skip_alley"
            else:
                type.type("A man approaches. His teeth are rotted. His hands shake. But his eyes are calculating.")
                print("\n")
                type.type(quote("You buying, selling, or lost?"))
                print("\n")
                action = input("(lost/curious/buy/run): ").strip().lower()
            
            if action == "lost":
                type.type(quote("Just lost. Wrong turn."))
                print("\n")
                type.type("He stares at you. Decides you're telling the truth.")
                print("\n")
                type.type(quote("Straight down, two rights, you're back on the main road. Don't come back here unless you mean to."))
                print("\n")
                type.type("You follow his directions. You feel his eyes on your back the whole way.")
                print("\n")
            
            elif action == "curious":
                type.type(quote("What goes on here?"))
                print("\n")
                type.type("He laughs. It turns into a cough.")
                print("\n")
                type.type(quote("What DOESN'T go on here? This is where the city sends everything it doesn't want to see. "))
                type.type(quote("Us. The junkies, the dealers, the runaways. We got our own economy down here."))
                print("\n")
                type.type("He gestures at the alley - the huddled forms, the quick transactions, the desperate faces.")
                print("\n")
                type.type(quote("You want something? Pills, powder, rock, whatever? Or maybe something else?") + " His eyes narrow. " + quote("Information?"))
                print("\n")
                if random.random() < 0.5:
                    type.type("He tells you about a high-stakes game three blocks over. Entry: $5,000. Pot: Whatever you can win.")
                    self.add_status("Underground Intel")
                else:
                    type.type("He tells you about a man who's been asking around about gamblers. A man with a glass eye.")
                    type.type("You don't know what to make of that.")
                print("\n")
            
            elif action == "buy":
                type.type("You don't know why you said that. Maybe you do.")
                print("\n")
                type.type("He names a price. You pay it before you can think.")
                self.change_balance(-random.randint(100, 500))
                print("\n")
                type.type("The high is immediate. Overwhelming. Everything feels possible.")
                print("\n")
                type.type("Then it fades. And you feel worse than before. Emptier.")
                self.add_status("Shame")
                self.heal(random.randint(5, 15))  # Temporary
                self.hurt(random.randint(10, 20))  # Comedown
                print("\n")
            
            elif action == "run":
                if self.has_item("Pepper Spray"):
                    type.type("You aim the " + cyan(bright("Pepper Spray")) + " directly at the man's face and sprint.")
                    print("\n")
                    type.type("He stumbles back, hands over his eyes. " + quote("WHAT THE—"))
                    print("\n")
                    type.type("Spray and sprint. The alley is yours. You're a block away before anyone reacts.")
                    self.use_item("Pepper Spray")
                    self.restore_sanity(5)
                else:
                    type.type("You run. Someone shouts behind you but you don't look back.")
                    print("\n")
                    type.type("You run until your lungs burn. Until the alley is far behind you.")
                    print("\n")
                    type.type("You tell yourself you'll never go back there.")
                    print("\n")
                    type.type("You're probably lying.")
                print("\n")
        
        elif event == "penthouse_party":
            type.type("The elevator goes up. And up. And up. You're not sure how you got the invitation, but here you are.")
            print("\n")
            type.type("The penthouse is everything the street below isn't. Crystal chandeliers. Champagne that costs more than your car. ")
            type.type("People who've never worried about money in their lives.")
            print("\n")
            type.type(yellow("=== THE PENTHOUSE ==="))
            print("\n")
            type.type("They look at you like you're entertainment. The gambling addict from the casino. The man who lives in his car. A curiosity.")
            print("\n")
            type.type("A woman in diamonds approaches. " + quote("You're the one who won big at Mortimer's place, aren't you? I've heard SO much about you."))
            print("\n")
            action = input("(play_along/be_honest/steal/leave): ").strip().lower()
            
            if action == "play_along":
                type.type("You play the part. The high roller. The winner. The man who's got it figured out.")
                print("\n")
                type.type("They eat it up. Pour you drinks. Introduce you to people with last names that appear on buildings.")
                print("\n")
                type.type("For one night, you're one of them. Or at least they let you pretend.")
                print("\n")
                if random.random() < 0.5:
                    type.type("A man slips you a card. " + quote("Private game. Tomorrow night. Big stakes. You interested?"))
                    self.add_status("VIP Connection")
                    self.change_balance(random.randint(1000, 5000))  # Someone "tips" you
                else:
                    type.type("By midnight, they've moved on to the next curiosity. You're escorted out gently but firmly.")
                print("\n")
            
            elif action == "be_honest":
                type.type(quote("I'm nobody. I live in my car and gamble because I can't stop."))
                print("\n")
                type.type("Silence. Then laughter. They think you're joking.")
                print("\n")
                type.type("When they realize you're not, the laughter dies. The diamond woman's smile freezes.")
                print("\n")
                type.type(quote("Security? Please escort our... guest... out."))
                print("\n")
                type.type("On the elevator down, you see the city lights. All those penthouses, all those people who'll never understand.")
                print("\n")
                type.type("Maybe that's for the best.")
                print("\n")
            
            elif action == "steal":
                type.type("So much money. So much excess. They wouldn't even notice if something went missing.")
                print("\n")
                type.type("You pocket what you can. A gold lighter. Cash from a purse. A watch from the bathroom counter.")
                print("\n")
                if random.random() < 0.4:
                    self.change_balance(random.randint(5000, 15000))
                    type.type("You slip out before anyone notices. Tomorrow, someone will wonder where their Rolex went.")
                    type.type("They'll buy another one without thinking twice.")
                else:
                    type.type("A hand on your shoulder. Security. " + quote("Empty your pockets. Now."))
                    print("\n")
                    type.type("They take back what you stole and throw you onto the street. Literally.")
                    self.hurt(random.randint(15, 25))
                    self.add_status("Blacklisted")
                print("\n")
            
            else:
                type.type("You don't belong here. You never did.")
                print("\n")
                type.type("The elevator down is quiet. Through the glass walls, you watch the city get smaller, then bigger.")
                print("\n")
                type.type("Back on the street, you breathe easier. This is where you belong. For better or worse.")
                print("\n")
        
        elif event == "desperate_gambler":
            type.type("You recognize him. Or maybe you recognize yourself in him.")
            print("\n")
            type.type("A man, your age, standing outside an ATM. His card has been declined. He's holding a picture - family, kids, a life that used to be.")
            print("\n")
            type.type(yellow("=== THE DESPERATE GAMBLER ==="))
            print("\n")
            type.type(quote("I just need one more game,") + " he says to no one. " + quote("One more hand. I can win it all back."))
            print("\n")
            type.type("He looks at you. Eyes desperate. " + quote("You got any cash? I swear I'll pay you back. I've got a system."))
            print("\n")
            action = input("(give_money/give_advice/take_picture/ignore): ").strip().lower()
            
            if action == "give_money":
                type.type("How much?")
                try:
                    amount = int(input("Amount: $"))
                    if amount > 0 and self.get_balance() >= amount:
                        self.change_balance(-amount)
                        type.type("He takes the money with shaking hands. " + quote("Thank you. Thank you. I'll pay you back, I swear."))
                        print("\n")
                        type.type("He walks toward the casino district. You know you'll never see that money again.")
                        print("\n")
                        type.type("You know, because you've been him. You are him.")
                    else:
                        type.type("You can't spare it. He nods, understanding. Fellow gamblers know the truth.")
                except:
                    type.type("You hesitate. He walks away. " + quote("Never mind. Forget it."))
                print("\n")
            
            elif action == "give_advice":
                type.type(quote("There is no system. There's no winning it back. I've been where you are."))
                print("\n")
                type.type("He laughs bitterly.")
                print("\n")
                type.type(quote("You think I don't know that? You think I don't know I'm destroying my life?"))
                print("\n")
                type.type("He holds up the picture. ")
                type.type(quote("My wife left. My kids won't talk to me. I've lost everything. All I have left is the hope that one more game will fix it."))
                print("\n")
                type.type(quote("Without that hope, I've got nothing."))
                print("\n")
                type.type("You don't have a response to that. Neither does he.")
                self.add_status("Haunted")
                self.lose_sanity(random.choice([1, 2, 3]))  # Seeing yourself in a broken man
                print("\n")
            
            elif action == "take_picture":
                type.type(quote("Can I see that?"))
                print("\n")
                type.type("He hands it over. A woman. Two kids. A backyard. Normalcy.")
                print("\n")
                type.type(quote("They're beautiful,") + " you say. " + quote("Is that why you gamble? To give them better?"))
                print("\n")
                type.type(quote("I told myself that at first. Now I gamble because I don't know how to stop."))
                print("\n")
                type.type("You hand the picture back. " + quote("Call them. Tonight. Before you play again."))
                print("\n")
                type.type("He looks at the picture for a long time. Then at you.")
                print("\n")
                type.type(quote("Maybe. Maybe I will."))
                print("\n")
                type.type("You both know he won't. But the lie feels nice.")
                print("\n")
            
            else:
                type.type("You walk past him. Like everyone else.")
                print("\n")
                type.type("His eyes follow you. Understanding. No judgment. Just recognition.")
                print("\n")
                type.type("One gambler recognizing another. Both of you pretending you're different.")
                print("\n")
        
        elif event == "bank_heist":
            type.type("You're walking past First National when you see them. Three figures in dark clothes, cutting through a side door. Professional. Silent.")
            print("\n")
            type.type("One of them spots you. For a moment, time freezes. Then she walks toward you - calm, deliberate. A woman with cold eyes and a colder smile.")
            print("\n")
            type.type(yellow("=== THE BANK HEIST ==="))
            print("\n")
            type.type(quote("Wrong place, wrong time, friend. But maybe right place, right time for you."))
            print("\n")
            type.type("She explains quickly: they're hitting the vault. Insider job. Security's paid off. They need a lookout - someone who doesn't look like a criminal.")
            print("\n")
            type.type(quote("You stand on the corner, smoke a cigarette, text us if cops show up. Easy money. Or...") + " She lets the alternative hang in the air.")
            print("\n")
            type.type("You could join them inside. You could call the cops. ")
            type.type("You could try to blackmail your way into a bigger cut. ")
            type.type("Or you could just watch from the shadows and see what falls off the truck.")
            print("\n")
            action = input("(join/report/blackmail/fight/watch): ").strip().lower()
            
            if action == "join":
                type.type("You're handed a mask and a bag. " + quote("Don't be stupid, don't be a hero. Just grab and go."))
                print("\n")
                type.type(yellow("=== THE HEIST ==="))
                type.type("You're inside the vault! Gold everywhere! How much do you take?")
                grab = input("(reasonable/greedy/pocket_stuff): ").strip().lower()
                
                if grab == "greedy":
                    type.type("You load up HEAVY. Your bag weighs a ton.")
                    if random.random() < 0.4:
                        type.type("You escape with the crew! Your cut is MASSIVE!")
                        self.change_balance(random.randint(40000, 80000))
                        self.add_status("Wanted Felon")
                    else:
                        type.type("Too slow! The cops arrive! You drop half the gold escaping!")
                        self.change_balance(random.randint(15000, 30000))
                        self.add_status("Wanted")
                elif grab == "pocket_stuff":
                    type.type("You pretend to fill your bag while pocketing small but VALUABLE gems.")
                    self.change_balance(random.randint(8000, 18000))
                    type.type("The crew doesn't notice. Smart. Safe.")
                else:
                    type.type("You take a reasonable amount and escape with the crew.")
                    self.change_balance(random.randint(20000, 40000))
                    self.add_status("Wanted")
                print("\n")
            
            elif action == "report":
                type.type("You back away slowly and call 911. The cops arrive in FORCE.")
                print("\n")
                if random.random() < 0.6:
                    type.type("The crew is caught! The city rewards you handsomely!")
                    self.change_balance(random.randint(10000, 25000))
                    self.add_item("Key to the City")
                else:
                    type.type("One robber escapes and sees your face. You're a target now.")
                    self.add_status("Marked")
                print("\n")
            
            elif action == "blackmail":
                type.type(quote("How about you cut me in, or I make a very loud phone call?"))
                print("\n")
                if random.random() < 0.5:
                    type.type("The masked figure considers, then tosses you a bag of gold.")
                    type.type(quote("Smart. But remember - we know your face too now."))
                    self.change_balance(random.randint(15000, 30000))
                    self.add_status("Criminal Contacts")
                else:
                    type.type("The masked figure pulls a gun. " + quote("Bad choice."))
                    self.hurt(random.randint(30, 50))
                print("\n")
            
            elif action == "fight":
                type.type("You attack the robber before they can react!")
                print("\n")
                if random.random() < 0.3:
                    type.type("You knock them out! The others flee! You're a HERO!")
                    self.change_balance(random.randint(15000, 30000))
                    self.add_item("Hero Medal")
                else:
                    type.type("The robber's friends don't appreciate that. They beat you severely.")
                    self.hurt(random.randint(40, 65))
                print("\n")
            
            else:
                type.type("You watch from the shadows as the heist unfolds.")
                print("\n")
                if random.random() < 0.3:
                    type.type("A bag falls off the van as they speed away. You grab it.")
                    self.change_balance(random.randint(5000, 15000))
                else:
                    type.type("The heist goes smoothly. You've witnessed history.")
                    self.add_status("Witness")
                print("\n")
        
        elif event == "free_ice_cream":
            type.type("A brightly colored truck plays cheerful music. 'FREE ICE CREAM!' the sign says. Too good to be true?")
            print("\n")
            type.type(yellow("=== THE ICE CREAM TRUCK ==="))
            print("\n")
            action = input("(get_ice_cream/suspicious/follow_truck/ignore): ").strip().lower()
            
            if action == "get_ice_cream":
                type.type("You approach the window. A jolly man hands you a cone.")
                print("\n")
                type.type(quote("Chocolate, vanilla, or mystery flavor?"))
                flavor = input("(chocolate/vanilla/mystery): ").strip().lower()
                
                if flavor == "mystery":
                    type.type("The mystery flavor is... actually incredible? Like nothing you've ever tasted.")
                    self.heal(random.randint(30, 50))
                    self.add_status("Mysteriously Refreshed")
                elif flavor == "chocolate":
                    type.type("Rich, creamy chocolate. You feel restored.")
                    self.heal(random.randint(20, 35))
                else:
                    type.type("Classic vanilla. Can't go wrong.")
                    self.heal(random.randint(15, 25))
                
                if random.random() < 0.2:
                    type.type("The ice cream man winks and slips you a $20 bill.")
                    type.type(quote("You look like you needed that."))
                    self.change_balance(20)
                print("\n")
            
            elif action == "suspicious":
                type.type("You investigate the truck. Something's off...")
                print("\n")
                if random.random() < 0.3:
                    type.type("It's a FRONT! The truck is actually selling weapons out the back!")
                    type.type("Do you report it or buy something?")
                    choice = input("(report/buy): ").strip().lower()
                    if choice == "buy":
                        type.type("You buy a suspicious item. Might come in handy.")
                        self.change_balance(-500)
                        self.add_item("Suspicious Package")
                    else:
                        type.type("You report it. The cops arrive and you get a reward.")
                        self.change_balance(random.randint(2000, 5000))
                else:
                    type.type("It's just... free ice cream. A local business doing charity. You feel paranoid.")
                    self.add_status("Paranoid")
                print("\n")
            
            elif action == "follow_truck":
                type.type("You follow the truck... it drives to a MANSION and parks.")
                print("\n")
                type.type("A wealthy-looking person gets out and goes inside. This is their PERSONAL ice cream truck.")
                if random.random() < 0.4:
                    type.type("They notice you following and invite you in for ice cream. You make a rich friend.")
                    self.add_item("Rich Friend's Number")
                    self.change_balance(random.randint(1000, 5000))
                else:
                    type.type("Security spots you. They're not happy.")
                    self.add_status("Trespasser")
                print("\n")
            
            else:
                type.type("Nothing is free in this city. You walk past.")
                type.type("A child happily eating ice cream waves at you. You feel a twinge of regret.")
                print("\n")
        
        elif event == "fighting_ring":
            type.type("Down a grimy stairwell, you hear the roar of a crowd. An underground FIGHTING RING.")
            print("\n")
            type.type(yellow("=== THE UNDERGROUND FIGHT CLUB ==="))
            print("\n")
            type.type("A bouncer blocks the door. " + quote("$500 entry. Or $2,000 to fight. Prize pot is $20,000."))
            print("\n")
            action = input("(fight/bet/watch/organize): ").strip().lower()
            
            if action == "fight":
                if self.get_balance() >= 2000:
                    self.change_balance(-2000)
                    type.type("You step into the ring. Your opponent is HUGE.")
                    print("\n")
                    type.type(yellow("=== ROUND 1 ==="))
                    type.type("He swings at your head! What do you do?")
                    r1 = input("(duck/block/counter): ").strip().lower()
                    
                    fight_score = random.randint(0, 2)
                    
                    if r1 == "duck":
                        if random.random() < 0.6:
                            type.type("You duck under and land a body shot!")
                            fight_score += 2
                        else:
                            type.type("You duck into his knee. Stars explode in your vision.")
                            self.hurt(random.randint(10, 20))
                    elif r1 == "block":
                        if random.random() < 0.7:
                            type.type("You block and push him back! Solid defense!")
                            fight_score += 1
                        else:
                            type.type("The force nearly breaks your arm!")
                            self.hurt(random.randint(15, 25))
                    else:
                        if random.random() < 0.4:
                            type.type("You counter with a DEVASTATING right hook!")
                            fight_score += 3
                        else:
                            type.type("He sees it coming and rocks you instead!")
                            self.hurt(random.randint(20, 30))
                    
                    print("\n")
                    type.type(yellow("=== ROUND 2 ==="))
                    type.type("You're in a clinch! He's trying to throw you!")
                    r2 = input("(knee/headbutt/trip): ").strip().lower()
                    
                    if r2 == "knee":
                        if random.random() < 0.5:
                            type.type("Knee to the ribs! He doubles over!")
                            fight_score += 2
                        else:
                            type.type("He catches your leg and slams you down!")
                            self.hurt(random.randint(15, 25))
                    elif r2 == "headbutt":
                        type.type("CRACK! You both see stars!")
                        self.hurt(random.randint(10, 15))
                        fight_score += 2
                    else:
                        if random.random() < 0.5:
                            type.type("You trip him! He goes DOWN!")
                            fight_score += 3
                        else:
                            type.type("He's too heavy! He uses your momentum against you!")
                            self.hurt(random.randint(15, 20))
                    
                    print("\n")
                    type.type(yellow("=== FINAL ROUND ==="))
                    type.type("Both of you are exhausted. One more exchange decides it!")
                    r3 = input("(all_in/defensive/taunt): ").strip().lower()
                    
                    if r3 == "all_in":
                        if random.random() < 0.4:
                            type.type("You throw EVERYTHING into one punch! HE GOES DOWN!")
                            fight_score += 4
                        else:
                            type.type("He catches you with a hook as you charge! You hit the mat!")
                            fight_score -= 2
                            self.hurt(random.randint(20, 30))
                    elif r3 == "defensive":
                        type.type("You survive to the bell! Decision time!")
                        fight_score += 1
                    else:
                        type.type("You taunt him! He charges blindly!")
                        if random.random() < 0.5:
                            type.type("You sidestep and counter! He's OUT!")
                            fight_score += 3
                        else:
                            type.type("His rage makes him STRONGER! Uh oh.")
                            self.hurt(random.randint(25, 35))
                    
                    print("\n")
                    type.type(yellow("=== DECISION ==="))
                    
                    if fight_score >= 8:
                        type.type("KNOCKOUT! YOU WIN! The crowd goes INSANE!")
                        type.type("You collect " + green(bright("$20,000")) + " and the respect of everyone here!")
                        self.change_balance(20000)
                        self.add_item("Fight Champion Belt")
                    elif fight_score >= 5:
                        type.type("Split decision - you win by points!")
                        self.change_balance(random.randint(10000, 15000))
                    elif fight_score >= 3:
                        type.type("Draw! You get your entry back.")
                        self.change_balance(2000)
                    else:
                        type.type("You lose. Badly. But you'll fight another day.")
                    print("\n")
                else:
                    type.type("You can't afford the entry fee. Maybe next time.")
                    print("\n")
            
            elif action == "bet":
                type.type("Who do you bet on?")
                type.type("1. The Champion - Iron Mike (2:1)")
                type.type("2. The Underdog - Scrappy Pete (5:1)")
                type.type("3. The Wildcard - Mama Bear (8:1)")
                type.type("4. The Newcomer - Some Kid (10:1)")
                pick = input("Pick (1-4): ").strip()
                
                type.type("How much do you bet?")
                try:
                    bet = int(input("Bet: $"))
                    if bet > 0 and self.get_balance() >= bet:
                        self.change_balance(-bet)
                        winner = random.choice(["mike", "mike", "mike", "pete", "mama", "kid"])
                        
                        if pick == "1" and winner == "mike":
                            self.change_balance(bet * 2)
                            type.type("Iron Mike destroys! " + green(bright("$" + str(bet * 2))) + "!")
                        elif pick == "2" and winner == "pete":
                            self.change_balance(bet * 5)
                            type.type("THE UNDERDOG WINS! " + green(bright("$" + str(bet * 5))) + "!")
                        elif pick == "3" and winner == "mama":
                            self.change_balance(bet * 8)
                            type.type("MAMA BEAR IS TERRIFYING! " + green(bright("$" + str(bet * 8))) + "!")
                        elif pick == "4" and winner == "kid":
                            self.change_balance(bet * 10)
                            type.type("THE KID KNOCKED OUT THE CHAMPION?! " + green(bright("$" + str(bet * 10))) + "!!!")
                        else:
                            type.type("Your fighter lost. The pit takes your money.")
                    else:
                        type.type("You can't bet that much.")
                except:
                    type.type("Betting closed.")
                print("\n")
            
            elif action == "organize":
                type.type("You approach the organizer. " + quote("I want to set up a fight. Big stakes."))
                print("\n")
                if self.get_balance() >= 10000:
                    type.type("The organizer grins. " + quote("You want to be a promoter? $10,000 investment, you keep 30% of the winnings."))
                    invest = ask.yes_or_no()
                    if invest == "yes":
                        self.change_balance(-10000)
                        if random.random() < 0.6:
                            earnings = random.randint(15000, 35000)
                            type.type("The fight is LEGENDARY! You earn " + green(bright("$" + str(earnings))) + "!")
                            self.change_balance(earnings)
                            self.add_status("Fight Promoter")
                        else:
                            type.type("The cops raid the place! You lose your investment!")
                            self.add_status("Raid Survivor")
                    else:
                        type.type("Smart. This business isn't for everyone.")
                else:
                    type.type("You don't have enough to be a promoter.")
                print("\n")
            
            else:
                if self.get_balance() >= 500:
                    self.change_balance(-500)
                    type.type("You watch the fights. Blood, sweat, glory. You feel tougher just being here.")
                    self.add_status("Fight Veteran")
                else:
                    type.type("You can't afford the entry. The bouncer doesn't let you in for free.")
                print("\n")
        
        elif event == "intense_mugging":
            type.type("An alley. Wrong turn. Three figures block the exit. Chains. Knives. Bad news.")
            print("\n")
            type.type(yellow("=== THE MUGGING ==="))
            print("\n")
            type.type("The leader steps forward. " + quote("Everything. Wallet, watch, whatever else you got."))
            print("\n")
            action = input("(fight/negotiate/surrender/distraction/run): ").strip().lower()
            
            if action == "fight":
                type.type("You're not going down without a fight!")
                print("\n")
                type.type("How do you attack?")
                attack = input("(leader/closest/wild_swing): ").strip().lower()
                
                if attack == "leader":
                    if random.random() < 0.3:
                        type.type("You drop the leader with one punch! The others hesitate!")
                        print("\n")
                        type.type("They run! You keep everything AND take the leader's wallet!")
                        self.change_balance(random.randint(500, 2000))
                    else:
                        type.type("The leader was ready. They beat you badly.")
                        self.hurt(random.randint(35, 55))
                        self.change_balance(-random.randint(5000, 15000))
                elif attack == "closest":
                    type.type("You swing at the nearest thug!")
                    if random.random() < 0.4:
                        type.type("He goes down! You escape in the chaos!")
                    else:
                        type.type("The others grab you. It's not a fair fight.")
                        self.hurt(random.randint(30, 45))
                        self.change_balance(-random.randint(3000, 10000))
                else:
                    type.type("You swing WILDLY in all directions!")
                    self.hurt(random.randint(20, 35))  # You get hit too
                    if random.random() < 0.35:
                        type.type("Chaotic, but it works! You escape!")
                    else:
                        type.type("They take you down eventually.")
                        self.change_balance(-random.randint(5000, 12000))
                print("\n")
            
            elif action == "negotiate":
                type.type(quote("Look, I've only got a few hundred. Take it, no trouble."))
                print("\n")
                if random.random() < 0.5:
                    type.type("The leader considers. " + quote("Fine. Dump your pockets."))
                    self.change_balance(-random.randint(500, 2000))
                    type.type("They take a small amount and let you go.")
                else:
                    type.type(quote("Liar.") + " They search you anyway and take more.")
                    self.change_balance(-random.randint(3000, 8000))
                print("\n")
            
            elif action == "surrender":
                type.type("You put your hands up. " + quote("Take it. All of it. Just don't hurt me."))
                print("\n")
                loss = min(self.get_balance(), random.randint(5000, 15000))
                self.change_balance(-loss)
                type.type("They take " + str(loss) + " dollars and disappear.")
                if random.random() < 0.3:
                    type.type("One of them drops something as they run. A gold watch!")
                    self.add_item("Stolen Watch")
                print("\n")
            
            elif action == "distraction":
                type.type(quote("COPS! BEHIND YOU!"))
                print("\n")
                if random.random() < 0.4:
                    type.type("They turn! You RUN! It works!")
                else:
                    type.type(quote("Nice try.") + " They beat you for the insult.")
                    self.hurt(random.randint(25, 40))
                    self.change_balance(-random.randint(5000, 12000))
                print("\n")
            
            else:
                type.type("You turn and SPRINT!")
                print("\n")
                if random.random() < 0.5:
                    type.type("You're faster! You escape!")
                else:
                    type.type("They catch you. Runners get extra punishment.")
                    self.hurt(random.randint(30, 50))
                    self.change_balance(-random.randint(5000, 15000))
                print("\n")
        
        elif event == "casino_heist":
            type.type("A woman in a red dress approaches you. " + quote("You look like someone who wants to get rich quick."))
            print("\n")
            type.type(yellow("=== THE CASINO HEIST ==="))
            print("\n")
            type.type("She explains: there's a high-stakes casino downtown. Security is tight, but she has a plan.")
            print("\n")
            type.type(quote("In and out. Forty thousand split. You in?"))
            print("\n")
            action = input("(join/refuse/betray/negotiate): ").strip().lower()
            
            if action == "join":
                type.type("You're in. She gives you a fake ID and a earpiece.")
                print("\n")
                type.type("Inside the casino, your job is to create a distraction. How?")
                distraction = input("(fight/fire_alarm/drunk_act/spill): ").strip().lower()
                
                if distraction == "fire_alarm":
                    type.type("You pull the alarm! Chaos erupts!")
                    if random.random() < 0.6:
                        type.type("The heist goes perfectly! She meets you outside with YOUR CUT!")
                        self.change_balance(random.randint(20000, 40000))
                    else:
                        type.type("Security catches HER. You barely escape. No money.")
                elif distraction == "drunk_act":
                    type.type("You pretend to be wasted and start a scene!")
                    if random.random() < 0.5:
                        type.type("Perfect! They're so focused on you, she empties the vault!")
                        self.change_balance(random.randint(15000, 30000))
                    else:
                        type.type("They just... escort you out. The heist fails.")
                elif distraction == "fight":
                    type.type("You start a fistfight with a random guy!")
                    self.hurt(random.randint(10, 20))
                    if random.random() < 0.5:
                        type.type("Maximum chaos! The heist succeeds!")
                        self.change_balance(random.randint(18000, 35000))
                    else:
                        type.type("You get detained. She escapes without you. No cut.")
                else:
                    type.type("You 'accidentally' spill a drink on a high roller!")
                    if random.random() < 0.4:
                        type.type("The argument draws security! Heist successful!")
                        self.change_balance(random.randint(15000, 30000))
                    else:
                        type.type("The high roller is too calm. Security stays alert. Heist fails.")
                print("\n")
            
            elif action == "betray":
                type.type("You agree... then call the cops.")
                print("\n")
                type.type("The heist is foiled! You get a reward!")
                self.change_balance(random.randint(5000, 12000))
                self.add_status("Informant")
                print("\n")
            
            elif action == "negotiate":
                type.type(quote("Sixty-forty. My way, or I walk."))
                print("\n")
                if random.random() < 0.5:
                    type.type("She smirks. " + quote("I like you. Deal."))
                    type.type("The heist succeeds! You get the bigger cut!")
                    self.change_balance(random.randint(25000, 45000))
                else:
                    type.type("She walks. You watch her disappear into the crowd.")
                print("\n")
            
            else:
                type.type(quote("I don't do crime."))
                print("\n")
                type.type("She shrugs. " + quote("Your loss.") + " She disappears into the night.")
                print("\n")
        
        else:
            type.type("Tonight, the city is quiet. The neon still flickers, the sirens still wail, but nothing touches you.")
            print("\n")
            type.type("You walk alone through streets that don't care if you live or die. Past people who don't see you. Past windows that glow with lives you'll never know.")
            print("\n")
            type.type("Some nights, the city is just a city. Empty. Indifferent. Waiting.")
            print("\n")
            type.type("You find a bench and sit. Watch the cars go by. Wonder what it would be like to just... stop.")
            print("\n")
            type.type("Stop gambling. Stop running. Stop pretending any of this means something.")
            print("\n")
            type.type("But morning will come, and you'll play again. Because that's who you are.")
            self.heal(random.randint(5, 15))
            print("\n")

    # RABBIT CHASE CHAIN - NEARLY THERE NIGHT (FINALE)
    def chase_the_last_rabbit(self):
        # Final rabbit chase - the cave, chance for great reward or death
        if self.get_rabbit_chase() != 5 or self.has_met("Caught Rabbit"):
            self.night_event()
            return
        
        type.type("You've finally cornered it. After all this time, all these chases across every corner of this town, ")
        type.type("the rabbit has led you here-to the mouth of a dark cave at the edge of the wilderness.")
        print("\n")
        type.type("The rabbit sits at the entrance, almost glowing in the moonlight. It looks at you one last time, then hops into the darkness.")
        print("\n")
        type.type("This is it. The final chase. But something about that cave fills you with dread.")
        print("\n")
        follow = ask.yes_or_no("Do you follow the rabbit into the cave?")
        
        if follow == "yes":
            type.type("You take a deep breath and step into the darkness. The cave swallows all light. You can hear the rabbit's footsteps echoing ahead.")
            print("\n")
            type.type("You stumble deeper and deeper, guided only by sound. The air grows cold. The walls seem to close in.")
            print("\n")

            if self.has_item("Night Scope"):
                type.type("The " + cyan(bright("Night Scope")) + " makes darkness transparent. You see every passage, every threat, every loot cache.")
                print("\n")
                type.type("Nothing is hidden. You take the optimal route.")
                self.change_balance(random.randint(100, 300))
                self.restore_sanity(5)
            elif self.has_item("Headlamp"):
                type.type("The " + cyan(bright("Headlamp")) + " cuts through the dark, hands free.")
                print("\n")
                type.type("You navigate confidently. No stumbles, no surprises.")
                self.restore_sanity(3)
            elif self.has_item("Flashlight") or self.has_item("Lantern") or self.has_item("Eternal Light"):
                light_name = "Flashlight" if self.has_item("Flashlight") else ("Lantern" if self.has_item("Lantern") else "Eternal Light")
                type.type("Your " + cyan(bright(light_name)) + " helps, though holding it limits your hands.")
                self.restore_sanity(2)
                evolved = self.track_item_use(light_name)
                if evolved:
                    print("\n")
                    type.type(cyan(bright(self.get_evolution_text(evolved[0], evolved[1]))))

            outcome = random.randrange(10)
            
            if outcome < 3:  # 30% - Great reward
                type.type("Then, suddenly-light! The cave opens into an enormous cavern, filled with glittering treasures. Gold coins, gems, artifacts from ages past.")
                print("\n")
                type.type("And there, sitting atop a mountain of wealth, is the rabbit. It looks at you and nods, as if to say " + quote("You earned this."))
                print("\n")
                type.type("Then, in a final burst of sparkles, it vanishes forever.")
                print("\n")
                type.type(green(bright("You've found the rabbit's treasure trove!")))
                coins = random.randint(50000, 100000)
                type.type("You stuff your pockets with " + green(bright("$" + str(coins))) + " worth of valuables.")
                self.change_balance(coins)
                self.add_item("Rabbit's Blessing")
                self.meet("Caught Rabbit")
            elif outcome < 7:  # 40% - Nothing, rabbit escapes
                type.type("You chase the sound of footsteps, but they lead nowhere. The cave twists and turns, and eventually...")
                print("\n")
                type.type("You find yourself back at the entrance. The rabbit is gone. Vanished, like it was never there at all.")
                print("\n")
                type.type(yellow("Maybe some things aren't meant to be caught. The hunt is over. You walk back to your wagon, somehow at peace."))
                self.meet("Caught Rabbit")  # Ends the chain
            else:  # 30% - Rabbit suicide / player death
                type.type("You follow the footsteps until they suddenly stop. Then you hear it-a rumble, deep within the earth.")
                print("\n")
                type.type("The ground beneath you gives way.")
                print("\n")
                type.type("You fall, and fall, and fall into the endless dark. The last thing you see is the rabbit, standing at the edge of the chasm above you, watching you plummet.")
                print("\n")
                type.slow(red(bright("Some mysteries are better left unsolved. The rabbit claimed its final victim. You should have let it go.")))
                print("\n")
                self.kill()
        else:
            type.type("You stand at the mouth of the cave for a long time. The rabbit doesn't come back out.")
            print("\n")
            type.type("Eventually, you turn around and walk away. Some chases have to end, even without a catch.")
            print("\n")
            type.type(yellow("You never see the rabbit again. But sometimes, late at night, you swear you can hear footsteps outside your wagon, and a soft, rhythmic thumping."))
            self.meet("Caught Rabbit")  # Ends the chain peacefully
            print("\n")

    # ==========================================

