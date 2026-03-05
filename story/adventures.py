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
    """Large adventure areas unlocked at Nearly There rank ($900,000+).
    
    Includes: Woodlands, Swamp, Beach, Underwater, City adventures
    and the final rabbit chase event.
    """

    # Nearly There Nights (900,000+)
    def woodlands_adventure(self):
        self.meet("Woodlands Adventure Event")
        self.add_fatigue(random.randint(8, 15))  # Trekking through the woods
        type.type("The forest is different tonight. Older. Deeper. The trees seem to lean in, listening. An owl hoots three times - an omen, the old folks say.")
        print("\n")
        type.type("You sense this night will be... significant.")
        print("\n")
        type.type(yellow(bright("=== WOODLANDS ADVENTURE ===")))
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
            self.heal(random.randint(15, 30))
            print("\n")



    def swamp_adventure(self):
        self.meet("Swamp Adventure Event")
        self.add_fatigue(random.randint(10, 18))  # Slogging through swamp muck
        type.type("The swamp stretches before you, endless and alive. ")
        type.type("Cypress trees draped in moss rise from black water like the fingers of drowned giants. ")
        type.type("Strange lights flicker in the distance. ")
        type.type("The air smells of decay and growth, death and life tangled together.")
        print("\n")
        type.type(yellow(bright("=== SWAMP ADVENTURE ===")))
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
                if self.has_item("Food"):
                    type.type("You share what you have. It's not much, but their gratitude is real.")
                    self.use_item("Food")
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

