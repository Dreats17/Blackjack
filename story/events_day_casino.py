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

class DayCasinoMixin:
    """Casino events: Dealer story beats and casino-specific encounters.
    Dream chain methods (remember_rebecca, dealers_anger, casino_bar, etc.)
    live in MechanicsStorylineMixin (mechanics_intro.py)."""

    def perfect_hand(self):
        # SECRET EVENT: The universe rewards you for having exactly $21 (Blackjack!)
        # TRIGGER: Balance must be exactly $21
        # EFFECTS: Adds "Lucky" status, adds "Ace of Spades" item
        # SECRET - Only triggers if you have EXACTLY 21 dollars
        if self.get_balance() != 21:
            self.day_event()
            return
        
        if self.has_item("Moonlit Fortune"):
            type.type("The " + cyan(bright("Moonlit Fortune")) + " glows beneath your shirt. You feel the next card before it's dealt. Ace of spades.")
            print("\n")
            type.type("Blackjack. The dealer can't explain it. Neither can physics.")
            self.change_balance(random.randint(500, 1500))
            self.restore_sanity(10)
            return
        if self.has_item("Master of Games"):
            type.type(cyan(bright("Master of Games")) + " at the table. The identity real, the insurance loaded. The dealer watches their own hands like they're betraying them.")
            print("\n")
            type.type("You own this table in every sense.")
            self.change_balance(random.randint(300, 800))
            self.restore_sanity(8)
            return
        if self.has_item("Gambler's Aura"):
            type.type("The " + cyan(bright("Gambler's Aura")) + " radiates. Triple luck. The dealer looks sick.")
            print("\n")
            type.type("Every card falls right. The house edge is your edge now.")
            self.change_balance(random.randint(200, 600))
            self.restore_sanity(5)
            return
        type.type("You count your money this morning and realize you have exactly " + green(bright("$21")) + ". Blackjack.")
        print("\n")
        type.type("As if on cue, a single playing card flutters down from nowhere and lands in your lap. The Ace of Spades.")
        print("\n")
        type.type("You look up. There's no one there. No birds, no trees. Just clear sky.")
        print("\n")
        type.type("On the back of the card, someone has written: " + quote("The universe deals you a winner."))
        print("\n")
        if self.has_item("Flask of Imminent Blackjack"):
            type.type("The " + cyan(bright("Flask of Imminent Blackjack")) + " is already open. You felt it before it happened. You always do.")
            print("\n")
            type.type("The flask is warm. The card is warm. The twenty-one dollars feel inevitable, like they were always going to be exactly this.")
            print("\n")
        if self.has_item("Eldritch Candle"):
            type.type("The " + cyan(bright("Eldritch Candle")) + " flickers green in your pocket. The cards translucent. You could see through the deck if you looked hard enough.")
            print("\n")
            type.type("You don't. Some advantages feel like cheating even when they're not.")
            self.restore_sanity(3)
            print("\n")
        type.type(yellow(bright("You feel inexplicably lucky today.")))
        self.add_status("Lucky")
        self.add_item("Ace of Spades")
        print("\n")

    # One-Time

    def high_stakes_feeling(self):
        # EVENT: Internal monologue about the weight and thrill of having $500k+
        # EFFECTS: Atmospheric only - builds tension as you approach the million dollar goal
        # Everytime - internal monologue
        if self.has_item("Flask of Dealer's Hesitation"):
            type.type("The " + cyan(bright("Flask of Dealer's Hesitation")) + " pulses against your chest.")
            print("\n")
            type.type("You can feel the Dealer's doubt from here. Every decision he makes, the flask makes him reconsider.")
            print("\n")
            type.type("The air at the table feels thick with hesitation. Like time is moving through honey.")
            self.restore_sanity(3)
            print("\n")
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
        elif variant == 3:
            type.type("You feel like you're in the final act of a movie. The climax is coming. You can feel it in your bones.")
            print("\n")
            type.type("Whether it's a happy ending or a tragedy... well. That's up to you.")
        if self.has_item("Flask of Imminent Blackjack"):
            print("\n")
            type.type("The " + cyan(bright("Flask of Imminent Blackjack")) + " hums in your pocket. The cards feel warmer. Closer. Like they WANT to come to you.")
            self.restore_sanity(2)
        if self.has_item("Flask of Second Chance"):
            print("\n")
            type.type("The " + cyan(bright("Flask of Second Chance")) + " shifts in your pocket. Time hiccups, just slightly.")
            print("\n")
            type.type("Whatever today deals you — you'll get one more shot at it. That's not nothing.")
        if self.has_item("Flask of No Bust"):
            print("\n")
            type.type("The " + cyan(bright("Flask of No Bust")) + " sits heavy in your jacket. Whatever hand you're dealt today — it won't break you. It literally cannot.")
            self.restore_sanity(3)
        if self.has_item("Cheater's Insurance"):
            print("\n")
            type.type("The " + cyan(bright("Cheater's Insurance")) + " rests under the seat. You're not going to use it. Probably not going to use it.")
            self.restore_sanity(2)
        print("\n")

    def casino_security(self):
        # EVENT: Security cars and surveillance suggest you're being watched
        # EFFECTS: Atmospheric paranoia - hints that the casino is tracking your wins
        # Everytime - paranoia event
        if self.has_item("Ghost Protocol"):
            type.type(cyan(bright("Ghost Protocol")) + " active. No camera catches your face. No pit boss remembers your name.")
            print("\n")
            type.type("You play and vanish. The security team watches the feed three times. Nothing.")
            self.restore_sanity(5)
            return
        if self.has_item("Cheater's Insurance"):
            type.type("The " + cyan(bright("Cheater's Insurance")) + " documents everything as legitimate play.")
            print("\n")
            type.type("Security reviews it. All clean. Provably clean. Embarrassingly clean.")
            self.restore_sanity(8)
            return
        if self.has_item("New Identity"):
            type.type("The " + cyan(bright("New Identity")) + " — they've got the wrong person. Different name, different face.")
            print("\n")
            type.type("The security team apologizes.")
            self.restore_sanity(5)
            return
        if self.has_item("Flask of Split Serum"):
            type.type("The " + cyan(bright("Flask of Split Serum")) + " vibrates at the card table.")
            print("\n")
            type.type("Your hand splits like a living thing. Two hands, twice the power. The Serum knows when the cards want to divide.")
            print("\n")
            type.type("The other players stare. " + quote("How does he always know when to split?"))
            self.restore_sanity(3)
            print("\n")
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
        if self.has_item("Flask of Pocket Aces"):
            print("\n")
            type.type("The " + cyan(bright("Flask of Pocket Aces")) + " pulses with twin heartbeats against your chest. Two aces, waiting.")
            print("\n")
            type.type("Whatever they're planning, you've got something they can't see coming.")
        if self.has_item("Flask of Dealer's Whispers"):
            print("\n")
            type.type("The " + cyan(bright("Flask of Dealer's Whispers")) + " vibrates against your hip. You swear you can hear the Dealer's voice, faint but clear: " + quote("Eighteen."))
            self.restore_sanity(2)
        if self.has_item("Radio Jammer"):
            print("\n")
            type.type("You flip the " + cyan(bright("Radio Jammer")) + " in your pocket. The surveillance van's radio dies. Backup never arrives.")
            print("\n")
            type.type("The security car circles once more, then gives up. No comms, no case.")
            self.restore_sanity(3)
        if self.has_item("EMP Device"):
            self.use_item("EMP Device")
            print("\n")
            type.type("The " + cyan(bright("EMP Device")) + " pulses. The electronic shuffler dies in a shower of sparks.")
            print("\n")
            type.type("Every camera in a fifty-foot radius goes dark. The guards stare at their dead screens, bewildered.")
            self.restore_sanity(4)
        print("\n")

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

    # Nearly There Days (900,000+)
    # ==========================================
    # NEW NEARLY DAY EVENTS - Everytime
    # ==========================================
    
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
        if self.has_item("Flask of Dealer's Hesitation"):
            print("\n")
            type.type("The " + cyan(bright("Flask of Dealer's Hesitation")) + " trembles. Somewhere, the Dealer paused mid-deal. Something about you makes even him uncertain.")
            self.restore_sanity(2)
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
            if self.has_item("Flask of Dealer's Whispers"):
                type.type("You uncap the " + cyan(bright("Flask of Dealer's Whispers")) + ". A voice, barely a breath: " + italic("Hit."))
                print("\n")
                type.type("You hit. It's perfect. He looks at your hand and laughs — a real laugh, the first one in weeks, the nurses say later.")
                print("\n")
                type.type(quote("How did you know?") + " You don't answer. You smile.")
                print("\n")
            else:
                type.type("You play. Slowly. The cards feel heavy. Important.")
                print("\n")
            if self.has_item("Deck of Cards"):
                type.type("You deal from your own " + cyan(bright("Deck of Cards")) + " for him — familiar cards, worn at the edges. He smiles. " + quote("These are good cards."))
                print("\n")
                self.restore_sanity(3)
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

