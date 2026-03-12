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

class DayWealthMixin:
    """Wealth events: wealth-tier progression and millionaire milestones"""

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

