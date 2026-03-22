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

class DayNumbersMixin:
    """Number events: number/stat triggered milestone encounters"""

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
        if self.has_item("Silver Flask") or self.has_item("Fancy Cigars"):
            item_name = "Silver Flask" if self.has_item("Silver Flask") else "Fancy Cigars"
            print("\n")
            type.type("You crack open the " + cyan(bright(item_name)) + " to mark the occasion. Some numbers deserve ceremony.")
            self.restore_sanity(5)
            self.heal(10)
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
        if self.has_item("Moonlit Fortune"):
            type.type("The " + cyan(bright("Moonlit Fortune")) + " bends probability. You knew the numbers before you scratched.")
            print("\n")
            self.change_balance(random.randint(500, 2000))
            self.restore_sanity(10)
            return
        if self.has_item("Gambler's Aura"):
            type.type(cyan(bright("Gambler's Aura")) + " — the universe bends. The numbers align.")
            print("\n")
            self.change_balance(random.randint(200, 800))
            self.restore_sanity(5)
            return
        if self.has_item("Fortune's Favor"):
            type.type("The " + cyan(bright("Fortune's Favor")) + " puts your luck into high gear.")
            print("\n")
            self.change_balance(random.randint(100, 400))
            self.restore_sanity(3)
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
        if (self.has_item("Lucky Penny") or self.has_item("Lucky Coin") or
                self.has_item("Lucky Charm Bracelet") or self.has_item("Lucky Medallion")):
            lucky_item = ("Lucky Medallion" if self.has_item("Lucky Medallion") else
                         "Lucky Charm Bracelet" if self.has_item("Lucky Charm Bracelet") else
                         "Lucky Coin" if self.has_item("Lucky Coin") else "Lucky Penny")
            print("\n")
            type.type("Your " + cyan(bright(lucky_item)) + " vibrates sympathetically. Four sevens and a lucky charm — the universe does not know what to do with this much luck.")
            print("\n")
            bonus = random.randint(50, 150)
            type.type("You find an extra " + green(bright("$" + str(bonus))) + " folded under the seat.")
            self.earn_money(bonus)
        print("\n")

    def exactly_13(self):
        # SECRET: Have exactly $13 - unlucky number
        if self.get_balance() != 13:
            self.day_event()
            return
        if self.has_item("Third Eye"):
            type.type("The " + cyan(bright("Third Eye")) + " saw this coming. You sidestepped before the bad luck landed.")
            print("\n")
            self.restore_sanity(5)
            return
        if self.has_item("Mind Shield"):
            type.type("The " + cyan(bright("Mind Shield")) + " blocks the psychic weight of the bad luck. Numbers are just numbers.")
            print("\n")
            self.restore_sanity(3)
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
        if self.has_item("Gambler's Grimoire") or self.has_item("Oracle's Tome"):
            tome = "Oracle's Tome" if self.has_item("Oracle's Tome") else "Gambler's Grimoire"
            print("\n")
            type.type("The " + cyan(bright(tome)) + " falls open to a page about luck and entropy. Thirteen isn't unlucky — it's prime. It's indivisible. The book says bad luck is just unread probability.")
            print("\n")
            type.type("The curse unravels like a bad hand folded before the flop.")
            self.remove_status("Cursed")
            self.restore_sanity(3)
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
        if self.has_item("Necronomicon"):
            type.type("The " + cyan(bright("Necronomicon")) + " turns its own pages in the moonlight. Something is very interested in this lunar cycle.")
            print("\n")
            type.type("You feel the darkness lean in, curious. Hungry. It knows you carry the book.")
            self.lose_sanity(5)
            print("\n")
        type.type("The morning light hits different today. Something in the air. You feel... different.")
        print("\n")
        type.type("More alive. More reckless. More HUNGRY.")
        print("\n")
        type.type("Not for food. For victory. For money. For the thrill of the game.")
        print("\n")
        type.type("Something inside you howls for action.")
        self.add_status("Lunar Frenzy")
        self.restore_sanity(10)
        if self.has_item("Dream Catcher"):
            type.type("The " + cyan(bright("Dream Catcher")) + "'s web catches the moonlight and holds it. The madness reaches you muffled, filtered, safe.")
            print("\n")
            self.restore_sanity(5)
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
        if self.has_item("Flask of No Bust"):
            print("\n")
            type.type("The " + cyan(bright("Flask of No Bust")) + " hums approval. Your health agrees — no busting today, no busting ever.")
            self.heal(5)
        if self.has_item("First Aid Kit"):
            print("\n")
            type.type("You inventory your " + cyan(bright("First Aid Kit")) + " out of habit. Everything looks good. Everything is good.")
            self.heal(3)
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
        if self.has_item("Gambler's Grimoire") or self.has_item("Oracle's Tome"):
            tome = "Oracle's Tome" if self.has_item("Oracle's Tome") else "Gambler's Grimoire"
            type.type("At 3am, you pull out the " + cyan(bright(tome)) + ". The equations make SENSE now. You annotate seventeen pages. When the sun comes up, you can't read your own handwriting — but somehow you feel like you understand probability better.")
            print("\n")
            if not self.has_status("Probability Edge"):
                self.add_status("Probability Edge")
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

