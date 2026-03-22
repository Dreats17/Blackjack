import random
import deckOfCards
from colorama import Fore, Back, Style
import time
import sys
import msvcrt
import typer

PAUSE = .25

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""

type = typer.Type()

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



class Blackjack:
    __slots__=["__balance", "__bet", "__min_bet", "__dealer_happiness", "__deck", "__hand", "__dealer_hand", "__player", "__used_peek", "__dealer_warning", "__free_hand", "__used_second_chance", "__used_pocket_aces", "__lucky_coin_triggered", "__used_double_down", "__used_split", "__split_hand", "__used_surrender", "__insurance_bet", "__bust_streak", "__min_bet_bust_count", "__dealer_forced_min_bet", "__dealer_forced_all_in", "__fraudulent_portion"]

    def __init__(self, player):
        self.__balance = 50
        self.__bet = 0
        self.__min_bet = 1
        self.__dealer_happiness = 45
        self.__deck = deckOfCards.Deck()
        self.__hand = Hand("Player")
        self.__dealer_hand = Hand("Dealer")
        self.__player = player
        self.__used_peek = False
        self.__dealer_warning = False
        self.__free_hand = False
        self.__used_second_chance = False
        self.__used_pocket_aces = False
        self.__lucky_coin_triggered = False
        # New item flags
        self.__used_double_down = False
        self.__used_split = False
        self.__split_hand = None
        self.__used_surrender = False
        self.__insurance_bet = 0
        self.__bust_streak = 0
        self.__min_bet_bust_count = 0
        self.__fraudulent_portion = 0   # fake-cash portion of the current bet (reset each hand)

    def update_player(self):
        self.__balance = self.__player.get_balance()
        self.__player.update_rank()
        if self.__player.has_item("Golden Watch") or self.__player.has_item("Sapphire Watch") or self.__player.has_item("Grandfather Clock"):
            self.__player.set_rounds(4)
        elif self.__player.has_item("Pocket Watch"):
            random_chance = random.randrange(3)
            if random_chance < 2:  # 66% chance
                self.__player.set_rounds(4)
        self.__used_peek = False
        self.__used_second_chance = False
        self.__used_pocket_aces = False
        # Reset new item flags for the session
        self.__used_double_down = False
        self.__used_split = False
        self.__split_hand = None
        self.__used_surrender = False
        self.__insurance_bet = 0
        self.__fraudulent_portion = 0

    def play_round(self, count=None):
        # Tanya therapy skip - player is staying in their car tonight
        if self.__player._skip_blackjack_tonight:
            self.__player._skip_blackjack_tonight = False
            return

        # Updates the player
        self.update_player()

        # Sets number of rounds played, if not specified. Mainly for testing
        if count==None:
            count = self.__player.get_rounds()

        # Resets the deck
        self.hard_reset()

        # Broken state effects at start of gambling session
        if self.__player.is_broken():
            broken_effects = [
                "The cards are looking at you. All of them. Even the ones still in the deck.",
                "You sit down. Or did you? You're sitting. You think.",
                "The felt on the table is the wrong color. It was green. Now it's green. But differently.",
                "The Dealer has too many hands. Count them. One. Two. One. Just one.",
                "You can hear your heartbeat in the cards. Thump. Thump. Hit. Stand. Thump.",
                "Time is moving wrong. The clock says one thing. Your body says another.",
                "Everything is fine. Everything is fine. Everything is fine. Is everything fine?"
            ]
            type.fast(red(random.choice(broken_effects)))
            print("\n")

        # Tells player that their golden watch is noticed by the Dealer
        if self.__player.has_item("Sapphire Watch"):
            type.fast("Your " + bright(cyan("Sapphire Watch")) + " shimmers brilliantly. The Dealer is mesmerized and lets you play an extra round.")
            print("\n")
        elif self.__player.has_item("Golden Watch"):
            type.fast("Your " + bright(magenta("Golden Watch")) + " glistens in the light hanging above the betting table. The Dealer will let you play an extra round.")
            print("\n")

        if self.__player.has_item("Unwashed Hair"):
            type.fast("Your " + bright(cyan("Unwashed Hair")) + " is absolutely revolting. The Dealer lowers minimum bets just to get you out faster.")
            print("\n")
        elif self.__player.has_item("Dirty Old Hat"):
            type.fast("The " + bright(magenta("Dirty Old Hat")) + " on your head sends dust in the air, and reeks of poverty. Minimum bets are lowered.")
            print("\n")

        if self.__player.has_item("Grandfather Clock"):
            type.fast("Your " + bright(cyan("Grandfather Clock")) + " chimes ominously. Time bends to your will, guaranteeing an extra round.")
            print("\n")
            self.__player.update_pocket_watch_durability()
        elif self.__player.has_item("Pocket Watch") and self.__player.get_rounds() == 4:
            type.fast("Your " + bright(magenta("Pocket Watch")) + " ticks slowly, buying you extra time. The Dealer lets you play an extra round.")
            print("\n")
            self.__player.update_pocket_watch_durability()

        if self.__player.has_item("Velvet Gloves"):
            type.fast("Your " + bright(cyan("Velvet Gloves")) + " feel impossibly soft. The cards practically shuffle themselves into your favor.")
            print("\n")
        elif self.__player.has_item("Worn Gloves"):
            type.fast("Your " + bright(magenta("Worn Gloves")) + " fit snugly on your hands. You feel more in tune with the cards.")
            print("\n")

        if self.__player.has_item("Invisible Cloak"):
            type.fast("Your " + bright(cyan("Invisible Cloak")) + " renders you nearly unseen. The Dealer keeps forgetting you're there.")
            print("\n")
        elif self.__player.has_item("Tattered Cloak"):
            type.fast("Your " + bright(magenta("Tattered Cloak")) + " rustles quietly. The Dealer barely notices you.")
            print("\n")

        if (self.__player.has_item("Lucky Penny") and self.__player.has_item("Lucky Coin")
                and self.__player.has_item("Lucky Charm Bracelet")):
            type.fast(yellow(bright("Three lucky charms in your pocket simultaneously.")))
            print("\n")
            type.fast("You feel it before the cards are dealt. The table tilts. Imperceptibly. In your favor.")
            print("\n")
        elif self.__player.has_item("Lucky Medallion"):
            type.fast("Your " + bright(cyan("Lucky Medallion")) + " pulses with ancient fortune. Luck bends around you.")
            print("\n")
        elif self.__player.has_item("Lucky Coin"):
            type.fast("Your " + bright(magenta("Lucky Coin")) + " feels warm in your pocket.")
            print("\n")

        # Makes the dealer a bit happier, as a new day has started
        # BUT NOT if he has too much fake cash from the player
        if not self.__player.has_too_much_fake_cash():
            self.calm_dealer(random.choice([5, 7, 10]), False)
            if self.__player.has_item("Delight Manipulator"):
                type.fast("Your " + bright(cyan("Delight Manipulator")) + " hums with power.")
                print()
                type.fast("The Dealer has calmed down since you've last seen him!")
                print()
                self.delight_indicator()
                print("\n")
            elif self.__player.has_item("Delight Indicator"):
                type.fast("Your " + bright(magenta("Delight Indicator")) + " begins to flash.")
                print()
                type.fast("The Dealer has calmed down since you've last seen him!")
                print()
                self.delight_indicator()
                print("\n")
        else:
            type.fast(yellow("The Dealer looks at you strangely. His jade eye narrows."))
            print()
            type.fast(yellow("He does NOT seem pleased to see you tonight."))
            print("\n")
        
        # GIFT DELIVERY SYSTEM - Automatically give gift if player has one
        if self.__player.has_gift_wrapped():
            self.__player.deliver_gift_to_dealer()
            print("\n")

        # Tells the player their balance.
        type.fast("You have " + green(bright("${:,}".format(self.__balance))))
        if self.__player.can_see_fraudulent_cash() and self.__player.visible_fraudulent_cash() > 0:
            type.fast(yellow(" (" + "${:,}".format(self.__player.visible_fraudulent_cash()) + " hot)"))
        print()

        for _ in range(count):
            while(True):
                self.__player.status()
                print()

                # Checks the dealer's happiness, which could lead to effects
                self.dealer_status()

                if(self.__player.has_item("Dirty Old Hat") or self.__player.has_item("Unwashed Hair")):
                    self.set_min_bet(int(self.__balance/4))
                else:
                    self.set_min_bet(self.__balance)

                # Angry dealer can override the min bet
                if self.__dealer_forced_min_bet > 0 and self.__dealer_forced_min_bet > self.__min_bet:
                    self.__min_bet = self.__dealer_forced_min_bet

                if(not self.__free_hand):
                    # Dealer forced all-in — no choice
                    if self.__dealer_forced_all_in:
                        self.__bet = self.__balance
                        type.slow(red(bright("You push everything to the center. " + green("${:,}".format(self.__bet)) + red(bright(". All of it.")))))
                        print("\n")
                        self.__dealer_forced_all_in = False  # Only forced once
                    else:
                        player_betting = False
                        while(not player_betting):
                            player_betting = self.bet()

                if self.__player.is_religious():
                    type.fast(self.__player.lists().get_prayer())
                    print()
                self.first_deal()

                # Checks if either player was dealt blackjack
                if(self.is_game_over(False)):
                    break

                # Main loop for player hitting their hand
                # will continue until they choose to stand or is_game_over detects their hand's value >= 21
                player_standing = False
                while(not player_standing):
                    player_standing = self.hit_or_stand()
                    breakloop = self.is_game_over(False)
                    if breakloop:
                        break

                # Breaks main loop if smaller loop broke from the game ending
                if breakloop:
                    break

                print("\n")

                self.print_draw("Dealer", "second", self.__dealer_hand.get_card(1))
                print()

                type.fast(str(self.__dealer_hand))
                print()

                # The loop that has the dealer hit until their value is >= 17
                # At that point, they stand, or the game ends
                # regardless, is_game_over will be true after this loop
                dealer_standing = False
                while(not dealer_standing):
                    dealer_standing = self.dealer_hit()
                    breakloop = self.is_game_over(dealer_standing)
                    if breakloop:
                        break

                # Breaks main loop if smaller loop broke from the game ending
                if breakloop:
                    break

            self.reset()

        # Prints a line after all rounds of blackjack have finished
        print()

    def anger_dealer(self, value, message=True):
        if(self.__dealer_happiness - value <= 0):
            self.__dealer_happiness = 0
        else:
            self.__dealer_happiness -= value
        if (self.__player.has_item("Delight Indicator") or self.__player.has_item("Delight Manipulator")) and message == True:
            print("\n")
            type.fast("The Dealer has been angered!")
            print()
            self.delight_indicator()

    def calm_dealer(self, value, message=True):
        if(self.__dealer_happiness + value >= 100):
            self.__dealer_happiness = 100
        else:
            self.__dealer_happiness += value
        if (self.__player.has_item("Delight Indicator") or self.__player.has_item("Delight Manipulator")) and message==True:
            print("\n")
            type.fast("The Dealer has calmed down!")
            print()
            self.delight_indicator()


    def dealer_status(self):
                # Dealer happiness effects
                self.__free_hand = False
                self.__dealer_forced_all_in = False
                self.__dealer_forced_min_bet = 0
                if self.__dealer_happiness == 100:
                    random_chance = random.randrange(3)
                    if random_chance == 0:
                        lo = max(1, int(self.__balance/18))
                        hi = max(lo + 1, int(self.__balance/8))
                        self.__bet = random.randrange(lo, hi)
                        type.slow(bright(yellow("The Dealer's in a good mood. Here's a ") + green("${:,}".format(self.__bet)) + yellow(" hand, on the house!")))
                        print("\n")
                        self.__free_hand = True
                elif self.__dealer_happiness > 95:
                    random_chance = random.randrange(10)
                    if random_chance == 0:
                        lo = max(1, int(self.__balance/20))
                        hi = max(lo + 1, int(self.__balance/10))
                        self.__bet = random.randrange(lo, hi)
                        type.slow(bright(yellow("The Dealer's in a good mood. Here's a ") + green("${:,}".format(self.__bet)) + yellow(" hand, on the house!")))
                        print("\n")
                        self.__free_hand = True
                elif self.__dealer_happiness > 90:
                    random_chance = random.randrange(10)
                    if random_chance == 0:
                        lo = max(1, int(self.__balance/25))
                        hi = max(lo + 1, int(self.__balance/15))
                        self.__bet = random.randrange(lo, hi)
                        type.slow(bright(yellow("The Dealer's in a good mood. Here's a ") + green("${:,}".format(self.__bet)) + yellow(" hand, on the house!")))
                        print("\n")
                        self.__free_hand = True

                # Dealer anger effects
                if self.__dealer_happiness > 30:
                    self.__dealer_warning = False

                # === ANGRY DEALER: FORCED ALL-IN (happiness 0) ===
                if self.__dealer_happiness == 0:
                    random_chance = random.randrange(3)
                    if random_chance == 0:
                        # Force all-in instead of outright kill
                        type.slow(red(bright("The Dealer slams his fist on the table. The whole room goes quiet.")))
                        print("\n")
                        type.slow(red(bright("He leans in close. You can see the veins in his neck pulsing.")))
                        print()
                        type.slow(red(bright('"You think this is a game? ALL. IN. Every last cent. Right now."')))
                        print("\n")
                        type.slow(red(bright("The Dealer isn\'t asking. He\'s telling.")))
                        print("\n")
                        self.__dealer_forced_all_in = True
                    elif random_chance == 1:
                        type.slow(red(bright("The Dealer's had it with you. He gets up from his chair, and fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body.")))
                        self.__player.kill()
                    else:
                        type.slow(red(bright("The Dealer's had it with you. He points aggressively towards the door. Scared to question his authority, you scurry out. It seems you just dodged a bullet.")))
                        self.__player.add_danger("Angry Dealer")
                        print("\n")
                        return
                elif self.__dealer_happiness < 5:
                    random_chance = random.randrange(6)
                    if random_chance == 0:
                        # Force all-in
                        type.slow(red(bright('The Dealer locks eyes with you. "You know what? Let\'s make this interesting."')))
                        print("\n")
                        type.slow(red(bright('"Everything. On the table. Now."')))
                        print("\n")
                        self.__dealer_forced_all_in = True
                    elif random_chance == 1:
                        type.slow(red(bright("The Dealer's had it with you. He gets up from his chair, and fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body.")))
                        self.__player.kill()
                    elif random_chance == 2:
                        type.slow(red(bright("The Dealer's had it with you. He points aggressively towards the door. Scared to question his authority, you scurry out. It seems you just dodged a bullet.")))
                        self.__player.add_danger("Angry Dealer")
                        print("\n")
                        return
                    else:
                        # Angry min bet increase
                        self.__dealer_forced_min_bet = self._calculate_angry_min_bet()
                elif self.__dealer_happiness < 10:
                    random_chance = random.randrange(10)
                    if random_chance == 0:
                        type.slow(red(bright("The Dealer's had it with you. He gets up from his chair, and fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body.")))
                        self.__player.kill()
                    elif random_chance < 3:
                        type.slow(red(bright("The Dealer's had it with you. He points aggressively towards the door. Scared to question his authority, you scurry out. It seems you just dodged a bullet.")))
                        self.__player.add_danger("Angry Dealer")
                        print("\n")
                        return
                    elif random_chance < 5:
                        # Angry min bet increase
                        self.__dealer_forced_min_bet = self._calculate_angry_min_bet()
                elif self.__dealer_happiness < 20:
                    # Moderate anger: chance to raise min bet
                    if random.randrange(4) == 0:
                        self.__dealer_forced_min_bet = self._calculate_angry_min_bet()

                if self.__dealer_happiness < 20 and not self.__dealer_warning:
                    self.__dealer_warning = True
                    type.slow(red(bright("The Dealer is visibly pissed. Perhaps you've been getting too lucky.")))


    def delight_indicator(self):
        if self.__dealer_happiness > 66:
            type.fast("Dealer's current happiness: " + bright(green(str(self.__dealer_happiness) + "%")))
        elif self.__dealer_happiness > 33:
            type.fast("Dealer's current happiness: " + bright(yellow(str(self.__dealer_happiness) + "%")))
        else:
            type.fast("Dealer's current happiness: " + bright(red(str(self.__dealer_happiness) + "%")))
        self.__player.update_delight_indicator_durability()



    def _calculate_angry_min_bet(self):
        """Calculate an inflated min bet based on dealer anger level."""
        # The angrier the dealer, the higher the forced min bet
        if self.__dealer_happiness < 5:
            # Extreme anger: 40-60% of balance
            multiplier = random.uniform(0.4, 0.6)
            anger_messages = [
                '"You wanna play small? Not anymore."',
                '"I set the rules. And the rules just changed."',
                '"You think you can nickel-and-dime ME?"',
                '"Oh, you\'ll bet big tonight. Trust me."'
            ]
        elif self.__dealer_happiness < 10:
            # Very angry: 25-40% of balance
            multiplier = random.uniform(0.25, 0.4)
            anger_messages = [
                '"The minimum just went up. Way up."',
                '"I don\'t like your attitude. Bet bigger."',
                '"Consider this a... tax. On my patience."'
            ]
        elif self.__dealer_happiness < 20:
            # Angry: 15-25% of balance
            multiplier = random.uniform(0.15, 0.25)
            anger_messages = [
                '"Let\'s raise the stakes a little, shall we?"',
                '"I\'m feeling generous. Your minimum just doubled."',
                '"Higher bets. Now."'
            ]
        else:
            return 0

        forced_min = max(int(self.__balance * multiplier), self.__min_bet + 1)
        type.slow(red(bright(random.choice(anger_messages))))
        print("\n")
        type.slow(red("The Dealer sets your minimum bet to " + bright("${:,}".format(forced_min))))
        print("\n")
        return forced_min

    def set_min_bet(self, balance):
        balance = int(balance)  # guard against float balance (e.g. 0.0, 109.0)
        if balance <= 0:
            self.__min_bet = 1
            return

        balance_str = str(balance)
        balance_len = len(balance_str)
        if balance_len == 1:
            self.__min_bet = 1
        elif balance_len == 2:
            self.__min_bet = int(balance_str[0])
        else:
            new_balance_str = balance_str[0] + balance_str[1]
            for _ in range(balance_len-3):
                new_balance_str += "0"
            self.__min_bet = int(new_balance_str)

    def bet(self):
        bet = None
        total_available = self.__balance
        
        while bet is None:
            type.fast("The Dealer expects you to bet at least " + green(bright("${:,}".format(self.__min_bet))))
            print("")
            type.fast("How much would you like to bet? ")
            try:
                bet = int(input(""))
            except ValueError:
                print("")
                type.fast(red("The Dealer looks at you confused. Perhaps he didn't hear you."))
                print("\n")

        print("")

        if(self.__min_bet<=int(bet)<=total_available):
            self.__bet = bet
            fake_available = self.__player.get_fraudulent_cash()
            self.__fraudulent_portion = 0
            if fake_available > 0:
                self.__fraudulent_portion = min(bet, fake_available)
                self.__player.blend_fraudulent_cash(self.__fraudulent_portion)
            return True
        elif((int(bet) < self.__min_bet)):
            if self.__dealer_happiness >= 30: type.slow(red("The Dealer doesn't like that bet."))
            elif self.__dealer_happiness >= 25: type.slow(red("The Dealer looks at you with an aggressive eye. Maybe try betting more cash!"))
            elif self.__dealer_happiness >= 20: type.slow(red("The Dealer is infuriated. You've insulted him. You should bet more cash."))
            elif self.__dealer_happiness >= 15: type.slow(red("The Dealer gets up from his chair and charges his revolver. Bet more cash. You'll regret it if you don't."))
            elif self.__dealer_happiness >= 0: 
                type.slow(red(bright("THAT'S NOT ENOUGH MONEY. ")))
                type.slow(red("The Dealer fires three shots into your chest. You bleed out, and as you fade from reality, you see the Dealer reach into your pockets, and take every last penny from your lifeless body."))
                self.__player.kill()
            self.anger_dealer(5)
            print("\n")

        else:
            type.fast(red("The dealer looks at you confused. You don't have that much money."))
            print("\n")


    def first_deal(self):
        # Pocket Aces effect: guarantee first card is an Ace
        if self.__player.has_flask_effect("Pocket Aces") and not self.__used_pocket_aces:
            # Find an ace in the deck and move it to the top
            ace_found = self.__deck.find_and_move_ace_to_top()
            if ace_found:
                type.fast(magenta(bright("Your Pocket Aces potion tingles... You feel lucky!")))
                print()
                self.__used_pocket_aces = True
                # Remove the effect after use (one-time use)
                self.__player.remove_flask_effect("Pocket Aces")
        
        # Deal first card to Player
        card = self.draw(self.__hand)
        self.print_draw("Player", "first", card)
        print()

        # Deal first card to Dealer
        card = self.draw(self.__dealer_hand)
        self.print_draw("Dealer", "first", card)
        print("\n")

        # Saves dealer hand value, as it's the only card the player sees
        known_value = self.__dealer_hand.value()

        # Deal second card to Player
        card = self.draw(self.__hand)
        self.print_draw("Player", "second", card)
        print()

        # Deal second card to Dealer, which might be face down, if value<21
        card = self.draw(self.__dealer_hand)
        if(self.__dealer_hand.value()==21):
            self.print_draw("Dealer", "second", card)
        else:
            type.fast(red("The Dealer's second card is face down"))
            time.sleep(PAUSE)
            if self.__player.has_flask_effect("Dealer's Whispers"):
                print()
                type.fast(cyan(bright("Your Dealer's Whispers potion murmurs the hidden truth...")))
                print()
                if card.value() in [1, 8]:
                    type.fast(cyan("The hidden card is an " + bright(str(card))))
                else:
                    type.fast(cyan("The hidden card is a " + bright(str(card))))
                print()
        print("\n")

        # Prints Dealer's starting hand value. This is a special case (known value or 21 with a wink).
        if((self.__dealer_hand.value()!=21) & (known_value==1)):
            type.fast(red("As of now, the Dealer's hand has a known value of " + bright(str(1)) + ", or " + bright(str(11)) + ", since they have an ace"))
            time.sleep(PAUSE)
        elif(self.__dealer_hand.value()==21):
            type.fast(red("The Dealer's hand has a value of " + bright(str(21)) + " ;)"))
        else:
            type.fast(red("As of now, the Dealer's hand has a known value of " + bright(str(known_value))))

        print()

        # Prints player's starting hand value.
        type.fast(str(self.__hand))
        if self.__hand.has_ace():
            time.sleep(PAUSE)
        print()
        
        # Offer insurance if dealer shows an Ace and player has the item
        if known_value == 1:  # Dealer's first card is an Ace
            self.offer_insurance()

    def offer_insurance(self):
        """Offer insurance side-bet if player has Dealer's Grudge or Dealer's Mercy"""
        can_insure = (self.__player.has_item("Dealer's Grudge") or self.__player.has_item("Dealer's Mercy"))
        if not can_insure:
            return
        
        insurance_cost = self.__bet // 2
        if self.__balance < insurance_cost:
            print()
            type.fast(cyan("Your insurance item glows, but you lack funds for the side-bet..."))
            print()
            return
        
        print()
        if self.__player.has_item("Dealer's Mercy"):
            type.fast("Your " + magenta(bright("Dealer's Mercy")) + " pulses with protective energy...")
        else:
            type.fast("Your " + magenta(bright("Dealer's Grudge")) + " grows cold in your pocket...")
        print()
        type.fast(cyan("The Dealer shows an Ace. Would you like to buy insurance for " + green("${:,}".format(insurance_cost)) + "? (yes/no) "))
        choice = input().lower()
        
        if choice in ["y", "yes"]:
            self.__insurance_bet = insurance_cost
            self.__player.spend_balance(insurance_cost, dealer_receives_fraud=True)
            self.__balance = self.__player.get_balance()
            self.__player.set_balance(self.__balance)
            print()
            type.fast(cyan("You've placed an insurance bet of " + green("${:,}".format(insurance_cost))))
            print()
            if not self.__player.has_item("Dealer's Mercy"):
                self.__player.update_dealers_grudge_durability()
        else:
            print()
            type.fast(cyan("You decline the insurance."))
            print()

    def hit_or_stand(self):
        # Build options string based on available items
        options = ["hit", "stand"]
        options_display = "hit or stand"
        
        # Peek option (Sneaky Peeky Shades or Goggles upgrade)
        can_peek = (self.__player.has_item("Sneaky Peeky Shades") or self.__player.has_item("Sneaky Peeky Goggles"))
        if can_peek and not self.__used_peek:
            options.append("peek")
        
        # Double Down option (Gambler's Chalice) - only on first action with 2 cards
        can_double = (self.__player.has_item("Gambler's Chalice") or self.__player.has_item("Overflowing Goblet") or self.__player.has_flask_effect("Bonus Fortune"))
        if can_double and len(self.__hand) == 2 and not self.__used_double_down:
            options.append("double")
        
        # Split option (Twin's Locket or Split Serum flask) - only with a pair and 2 cards
        can_split = (self.__player.has_item("Twin's Locket") or self.__player.has_item("Mirror of Duality") or self.__player.has_flask_effect("Split Serum"))
        if can_split and len(self.__hand) == 2 and not self.__used_split:
            card1 = self.__hand.get_card(0)
            card2 = self.__hand.get_card(1)
            if card1.value() == card2.value():
                options.append("split")
        
        # Surrender option (White Feather)
        can_surrender = (self.__player.has_item("White Feather") or self.__player.has_item("Phoenix Feather"))
        if can_surrender and len(self.__hand) == 2 and not self.__used_surrender:
            options.append("surrender")
        
        # Build display string
        extra_options = [o for o in options if o not in ["hit", "stand"]]
        if extra_options:
            options_display = "hit, stand, or " + "/".join(extra_options)
        
        # Dealer commentary based on game state
        player_val = self.__hand.value()
        if self.__hand.possible_hands() == 2:
            player_val = self.__hand.ace_value()
        happiness = self.__player.get_dealer_happiness()
        
        dealer_comment = ""
        roll = random.randrange(5)  # 1 in 5 chance of a comment
        if roll == 0:
            if player_val >= 19:
                comments = [
                    "The Dealer glances at your hand. A flicker of something crosses his face. Respect? Fear? Indigestion? ",
                    "The Dealer drums his fingers on the table. He knows your hand is strong. You can tell by the way he's not making eye contact. ",
                    "The Dealer's smile tightens. Just a fraction. You're sitting pretty and he knows it. ",
                ]
                dealer_comment = random.choice(comments)
            elif player_val >= 15 and player_val <= 16:
                comments = [
                    "The Dealer raises an eyebrow. The danger zone. Where heroes are made and fools are buried. ",
                    "The Dealer watches you with interest. Fifteen-sixteen is where the sweat starts. He can smell it. ",
                    "The Dealer leans forward, just barely. This is the hand that separates the gamblers from the pretenders. ",
                ]
                dealer_comment = random.choice(comments)
            elif player_val <= 11:
                comments = [
                    "The Dealer waits patiently. You've got room to work with and he knows it. ",
                    "The Dealer stifles a yawn. Low hand. Nothing exciting yet. Wake him up when it gets interesting. ",
                ]
                dealer_comment = random.choice(comments)
            elif happiness < 20:
                comments = [
                    "The Dealer stares at you. Not blinking. Just... staring. Make your choice. ",
                    "The Dealer's jaw is clenched. He's not in the mood for deliberation. ",
                    "The Dealer taps the table. Once. Twice. Impatiently. ",
                ]
                dealer_comment = random.choice(comments)
        
        if dealer_comment:
            type.type(dealer_comment)
            print()
        
        type.fast("Would you like to " + options_display + "? ")
        choice = input().lower()
        
        # Hit
        if choice in ["h", "hit"]:
            self.hit()
            return False
        
        # Stand
        elif choice in ["s", "stand"]:
            self.__hand.get_final_value()
            print()
            type.fast("You decided to stand at a value of " + green(bright(str(self.__hand.value()))))
            return True
        
        # Peek
        elif choice in ["p", "peek"] and "peek" in options:
            self.__used_peek = True
            next_card = self.__deck.peek()
            print()
            # Use the correct item name based on what they have
            if self.__player.has_item("Sneaky Peeky Goggles"):
                peek_item = "Sneaky Peeky Goggles"
            else:
                peek_item = "Sneaky Peeky Shades"
            if (next_card.value()==1) or (next_card.value()==8):
                type.fast("Using your " + magenta(bright(peek_item)) + ", you notice that the top card is an " + bright(magenta(str(next_card))))
            else:
                type.fast("Using your " + magenta(bright(peek_item)) + ", you notice that the top card is a " + bright(magenta(str(next_card))))
            print("\n")
            self.__player.update_sneaky_peeky_glasses_durability()
            return False  # Continue playing
        
        # Double Down
        elif choice in ["d", "double"] and "double" in options:
            return self.double_down()
        
        # Split
        elif choice in ["split"] and "split" in options:
            return self.split_hand()
        
        # Surrender
        elif choice in ["surrender", "sur"] and "surrender" in options:
            return self.surrender()
        
        else:
            print()
            type.fast(red("I didn't quite catch that."))
            time.sleep(PAUSE)
            print("\n")
            return False

    def double_down(self):
        """Double the bet, take exactly one more card, then stand"""
        if self.__balance < self.__bet:
            print()
            type.fast(red("You don't have enough money to double down!"))
            print("\n")
            return False
        
        print()
        if self.__player.has_item("Overflowing Goblet"):
            type.fast("Your " + magenta(bright("Overflowing Goblet")) + " glows as you double your bet!")
        else:
            type.fast("Your " + magenta(bright("Gambler's Chalice")) + " glows as you double your bet!")
            self.__used_double_down = True
            self.__player.update_gamblers_chalice_durability()
        
        # Double the bet
        extra_bet = self.__bet
        extra_fake = self.__player.spend_balance(extra_bet, dealer_receives_fraud=True)
        self.__balance = self.__player.get_balance()
        self.__fraudulent_portion += extra_fake
        self.__bet *= 2
        self.__player.set_balance(self.__balance)
        
        print()
        type.fast("Your bet is now " + green(bright("${:,}".format(self.__bet))))
        print()
        
        # Draw exactly one card
        card = self.draw(self.__hand)
        self.print_draw("Player", "final", card)
        print()
        type.fast(str(self.__hand))
        print()
        
        # Must stand after double down
        self.__hand.get_final_value()
        type.fast("You must stand at " + green(bright(str(self.__hand.value()))))
        return True

    def split_hand(self):
        """Split a pair into two hands"""
        print()
        if self.__player.has_item("Mirror of Duality"):
            type.fast("Your " + magenta(bright("Mirror of Duality")) + " shimmers as your cards separate!")
        else:
            type.fast("Your " + magenta(bright("Twin's Locket")) + " clicks open as your cards separate!")
            self.__used_split = True
            self.__player.update_twins_locket_durability()
        
        # For now, implement a simplified split - play first hand, then second
        card1 = self.__hand.get_card(0)
        card2 = self.__hand.get_card(1)
        
        # Create two new hands
        self.__hand = Hand("Player")
        self.__hand.add(card1)
        self.__split_hand = Hand("Player Split")
        self.__split_hand.add(card2)
        
        # Deal one card to each hand
        new_card1 = self.draw(self.__hand)
        print()
        type.fast("First hand:")
        print()
        self.print_draw("Player", "second", new_card1)
        print()
        type.fast(str(self.__hand))
        print()
        
        new_card2 = self.__deck.draw()
        self.__split_hand.add(new_card2)
        print()
        type.fast("Second hand:")
        print()
        if (new_card2.value()==1) or (new_card2.value()==8):
            type.fast("Your second card is an " + bright(magenta(str(new_card2))))
        else:
            type.fast("Your second card is a " + bright(magenta(str(new_card2))))
        print()
        type.fast("Split hand value: " + green(bright(str(self.__split_hand.value()))))
        print("\n")
        
        type.fast(yellow("Playing first hand..."))
        print("\n")
        
        return False  # Continue playing first hand

    def surrender(self):
        """Surrender the hand and lose half the bet"""
        print()
        if self.__player.has_item("Phoenix Feather"):
            type.fast("Your " + magenta(bright("Phoenix Feather")) + " glows warmly as you raise it in defeat...")
            # Phoenix Feather: 25% chance to get full bet back instead
            if random.randrange(4) == 0:
                print()
                type.fast(yellow(bright("The feather bursts into flame and reforms! Your bet is fully returned!")))
                print()
                type.fast("Your balance remains " + green(bright("${:,}".format(self.__balance))))
                self.__used_surrender = True
                return True
        else:
            type.fast("You wave the " + magenta(bright("White Feather")) + " in defeat...")
            self.__used_surrender = True
            self.__player.update_white_feather_durability()
        
        # Lose half the bet
        half_bet = self.__bet // 2
        self.__player.spend_balance(half_bet, dealer_receives_fraud=True)
        self.__balance = self.__player.get_balance()
        self.__bet = 0
        self.__player.set_balance(self.__balance)
        
        print()
        type.fast(cyan("You surrender, losing half your bet: " + red("${:,}".format(half_bet))))
        print()
        type.fast("Your balance is now " + green(bright("${:,}".format(self.__balance))))
        print()
        
        # Update stats
        stats = self.__player.get_gambling_stats()
        stats["surrenders_used"] += 1
        
        return True  # End the hand

    def hit(self):
        # Hits a player's hand, then types their hand's value
        print()

        if self.__player.has_flask_effect("Imminent Blackjack"):
            hard_total = self.__hand.value()
            soft_total = self.__hand.ace_value() if self.__hand.possible_hands() == 2 else 0
            target_values = set()
            for running_total in [hard_total, soft_total]:
                if running_total <= 0 or running_total >= 21:
                    continue
                needed_value = 21 - running_total
                if 1 <= needed_value <= 10:
                    target_values.add(needed_value)
                if running_total == 10:
                    target_values.add(1)
            if target_values and self.__deck.find_and_move_value_to_top(target_values):
                type.fast(magenta(bright("Your Imminent Blackjack potion crackles with certainty...")))
                print()
            self.__player.remove_flask_effect("Imminent Blackjack")
        
        # Worn Gloves effect: occasionally redraw if the card would bust
        card = self.draw(self.__hand)
        has_worn_gloves = self.__player.has_item("Worn Gloves")
        has_velvet_gloves = self.__player.has_item("Velvet Gloves")
        if has_worn_gloves or has_velvet_gloves:
            # Check if this card would cause a bust
            if self.__hand.value() > 21:
                # Velvet Gloves have 50% chance, Worn Gloves have 25% chance
                chance_threshold = 2 if has_velvet_gloves else 1
                if random.randrange(4) < chance_threshold:
                    # Remove the card that was just drawn
                    self.__hand.remove_last_card()
                    # Draw a new card
                    card = self.draw(self.__hand)
                    if has_velvet_gloves:
                        type.fast(cyan(bright("Your Velvet Gloves caress the deck as the perfect card slides into your hand!")))
                    else:
                        type.fast(magenta(bright("Your Worn Gloves tingle as the cards shift in your favor!")))
                    print()
                    self.__player.update_worn_gloves_durability()

        if self.__hand.value() > 21 and self.__player.has_flask_effect("No Bust"):
            self.__hand.remove_last_card()
            type.fast(magenta(bright("Your Flask of No Bust rejects the draw and spares your hand!")))
            print()
            self.__player.update_no_bust_durability()
            if card.value() in [1, 8]:
                type.fast(cyan("The " + bright(str(card)) + cyan(" fizzles out before it can bust you.")))
            else:
                type.fast(cyan("The " + bright(str(card)) + cyan(" fizzles out before it can bust you.")))
            print()
            type.fast(str(self.__hand))
            print()
            return
        
        self.print_draw("Player", "next", card)
        if self.__hand.has_ace():
            time.sleep(PAUSE)
        print()
        type.fast(str(self.__hand))
        print()

    def dealer_hit(self):
        # Checks if the dealer has a hand that can be hit (value less than 17)
        # if it can, the hand will be hit, and the value will be typed
        
        # Dealer's Hesitation effect: force dealer to hit once more when they would normally stand
        hesitation_forced_hit = False
        if self.__player.has_flask_effect("Dealer's Hesitation") and self.__dealer_hand.value() >= 17 and self.__dealer_hand.value() < 21:
            random_chance = random.randrange(3)
            if random_chance < 2:  # 66% chance to force extra hit
                hesitation_forced_hit = True
                type.fast(magenta(bright("Your Dealer's Hesitation potion kicks in! The Dealer hesitates and draws another card!")))
                print()
                self.__player.update_dealers_hesitation_durability()
        
        if(self.__dealer_hand.value()>=17) and not hesitation_forced_hit:
            self.__dealer_hand.get_final_value()
            print()
            type.fast(red("The Dealer stands at " + bright(str(self.__dealer_hand.value()))))
            print()
            return True
        elif(self.__dealer_hand.possible_hands()==2) and not hesitation_forced_hit:
            if(self.__dealer_hand.ace_value()>=17):
                self.__dealer_hand.get_final_value()
                print()
                type.fast(red("The Dealer stands at " + bright(str(self.__dealer_hand.value()))))
                print()
                return True
        print()
        if(len(self.__dealer_hand)>2):
            type.fast(red("The Dealer hits"))
            # Occasional dealer commentary on subsequent hits
            if random.randrange(4) == 0:
                dealer_val = self.__dealer_hand.value()
                if dealer_val >= 15:
                    comments = [
                        " — a bold choice. He's pushing it.",
                        ". He doesn't look happy about it.",
                        ". His hand hovers over the deck for just a moment too long before drawing.",
                        ". Living dangerously. You almost respect it.",
                    ]
                    type.type(random.choice(comments))
                else:
                    comments = [
                        " — no hesitation.",
                        ". Mechanical. Practiced. He's done this a million times.",
                        ". The card slides off the deck like it was waiting for him.",
                    ]
                    type.type(random.choice(comments))
            time.sleep(PAUSE)
        else:
            type.fast(red("The Dealer's hand has a value under 17 so they hit"))
            time.sleep(PAUSE)
        card = self.draw(self.__dealer_hand)
        print()
        self.print_draw("Dealer", "next", card)
        if len(self.__dealer_hand)>1:
            time.sleep(PAUSE)
        print()
        type.fast(str(self.__dealer_hand))
        print()
        return False

    def is_game_over(self, dealer_standing):
        # Checks if the game is over
        # If true, passes a string to end_round explaining the method of victory/defeat
        player_value = self.__hand.value()
        if(self.__hand.possible_hands()==2):
            player_value = self.__hand.ace_value()

        dealer_value = self.__dealer_hand.value()
        if(self.__dealer_hand.possible_hands()==2):
            dealer_value = self.__dealer_hand.ace_value()

        if(player_value>21):
            return self.end_round("Player Bust")
        elif(dealer_value>21):
            return self.end_round("Dealer Bust")
        elif(player_value==21)&(dealer_value==21):
            return self.end_round("Tie Blackjack")
        elif(player_value==21):
            return self.end_round("Player Blackjack")
        elif(dealer_value==21):
            return self.end_round("Dealer Blackjack")
        elif(player_value>dealer_value)&(dealer_standing):
            return self.end_round("Player Wins")
        elif(player_value==dealer_value)&(dealer_standing):
            return self.end_round("Tie")
        elif(player_value<dealer_value)&(dealer_standing):
            return self.end_round("Dealer Wins")
        else:
            return False
        
    def end_round(self, status):
        print()

        # Second Chance flask: replay a losing hand once per session
        if (self.__player.has_flask_effect("Second Chance") and 
            not self.__used_second_chance and 
            status in ["Dealer Wins", "Dealer Blackjack", "Player Bust"]):
            print()
            type.fast(yellow(bright("Your Flask of Second Chance glimmers! Would you like to replay this hand? (y/n) ")))
            choice = input().lower()
            if choice in ["y", "yes"]:
                self.__used_second_chance = True
                type.fast(yellow(bright("Time seems to rewind... The cards dissolve and reform...")))
                print("\n")
                self.__player.update_second_chance_durability()
                return False  # Return False to continue playing (replays the hand)

        # Lucky Coin effect: occasionally turn a loss into a push/tie
        has_lucky_coin = self.__player.has_item("Lucky Coin")
        has_lucky_medallion = self.__player.has_item("Lucky Medallion")
        has_triple_luck = (self.__player.has_item("Lucky Penny") and has_lucky_coin
                           and self.__player.has_item("Lucky Charm Bracelet"))
        has_oswalds_luck = self.__player.has_status("Oswald's Luck")
        if (has_lucky_coin or has_lucky_medallion or has_triple_luck or has_oswalds_luck) and status in ["Dealer Wins", "Dealer Blackjack", "Player Bust"]:
            # Lucky Medallion always works; Triple Luck has 35% chance; Lucky Coin / Oswald's Luck has 20% chance
            if has_lucky_medallion:
                triggered = True
            elif has_triple_luck:
                triggered = random.randrange(100) < 35
            else:
                triggered = random.randrange(5) < 1
            if triggered:
                if has_triple_luck and not has_lucky_medallion:
                    type.fast(yellow(bright("Three charms resonate at once — the loss bends to your will!")))
                elif has_lucky_medallion:
                    type.fast(cyan(bright("Your Lucky Medallion blazes with power! The loss turns into a push!")))
                elif has_oswalds_luck and not has_lucky_coin:
                    type.fast(yellow(bright("Oswald's weighted dice tip the scales — the loss becomes a push!")))
                else:
                    type.fast(magenta(bright("Your Lucky Coin glows! The loss turns into a push!")))
                print("\n")
                self.__player.update_lucky_coin_durability()
                self.__lucky_coin_triggered = True
                status = "Tie"
        
        # Tattered Cloak effect: dealer sometimes forgets to collect losing bet
        tattered_cloak_saved = False
        has_tattered_cloak = self.__player.has_item("Tattered Cloak")
        has_invisible_cloak = self.__player.has_item("Invisible Cloak")
        if (has_tattered_cloak or has_invisible_cloak) and status in ["Dealer Wins", "Dealer Blackjack", "Player Bust"]:
            # Invisible Cloak has 50% chance, Tattered Cloak has 25% chance
            chance_threshold = 2 if has_invisible_cloak else 1
            if random.randrange(4) < chance_threshold:
                tattered_cloak_saved = True
                self.__player.update_tattered_cloak_durability()

        match status:
            case "Player Blackjack": 
                message = random.randrange(8)
                if message==0: type.fast(yellow(bright("You got a Blackjack! You Win! Yay!")))
                if message==1: type.fast(yellow(bright("Blackjack! What a moment! Mom, get the camera!")))
                if message==2: type.fast(yellow(bright("WOOOOOOO!!! Blackjack!!! WOOOOOOOO!!!")))
                if message==3: type.fast(yellow(bright("You hit Blackjack! What's cooking, good looking?")))
                if message==4: type.fast(yellow(bright("Oh lord have mercy, you got a Blackjack!")))
                if message==5: type.fast(yellow(bright("Twenty-one on the nose. The cards love you today.")))
                if message==6: type.fast(yellow(bright("Blackjack! The Dealer's eye twitches. Beautiful.")))
                if message==7: type.fast(yellow(bright("Natural 21. Clean. Surgical. The Dealer didn't even get to play.")))
                print()
                if self.__free_hand:
                    type.fast(yellow(bright("You had " + green("${:,}".format(self.__balance)) + yellow(", and with a free bet of ") + green("${:,}".format(self.__bet)) + yellow(", you've tripled it!"))))
                else:
                    type.fast(yellow(bright("You had " + green("${:,}".format(self.__balance)) + yellow(", and with a bet of ") + green("${:,}".format(self.__bet)) + yellow(", you've tripled it!"))))
                print("\n")
                type.fast(yellow(bright("Your new balance is " + green("${:,}".format(self.__balance) + " + ${:,}".format(self.__bet*2) + " = ${:,}".format(self.__balance+self.__bet*2)))))
                self.__balance += 2*self.__bet

            case "Player Wins":
                message = random.randrange(8)
                if message==0: type.fast(magenta(bright("Congrats! You Win! Get REKT, Dealer!")))
                if message==1: type.fast(magenta(bright("You topple the Dealer! Are we witnessing a heist?")))
                if message==2: type.fast(magenta(bright("You outplayed the Dealer to victory! Nice moves.")))
                if message==3: type.fast(magenta(bright("You win...this time.")))
                if message==4: type.fast(magenta(bright("Winner winner chicken dinner! Must be tasty.")))
                if message==5: type.fast(magenta(bright("Your hand wins! The Dealer collects the cards without looking at you.")))
                if message==6: type.fast(magenta(bright("You beat the house. For now. Enjoy it while it lasts.")))
                if message==7: type.fast(magenta(bright("Victory! Small, fragile, temporary. But yours.")))
                print()
                if self.__free_hand:
                    type.fast(magenta(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a free bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've doubled it!"))))
                else:
                    type.fast(magenta(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've doubled it!"))))
                print("\n")
                type.fast(magenta(bright("Your new balance is " + green("${:,}".format(self.__balance) + " + ${:,}".format(self.__bet) + " = ${:,}".format(self.__balance+self.__bet)))))
                self.__balance += self.__bet

            case "Dealer Bust":
                message = random.randrange(8)
                if message==0: type.fast(magenta(bright("The Dealer went over 21! Bust! You Win!")))
                if message==1: type.fast(magenta(bright("Dealer's hand busts! Victory is yours!")))
                if message==2: type.fast(magenta(bright("Dealer goes kaboom! Were they trying to bake a number cake?")))
                if message==3: type.fast(magenta(bright("Dealer hand goes bust! You're one lucky lucy.")))
                if message==4: type.fast(magenta(bright("The Dealer's over 21, which means you are the winner! Dope.")))
                if message==5: type.fast(magenta(bright("The Dealer overcooked it. Busted! Karma is REAL.")))
                if message==6: type.fast(magenta(bright("Bust! The Dealer slams the table. You pretend not to notice.")))
                if message==7: type.fast(magenta(bright("Over 21. The Dealer exhales through his nose like a dragon who just lost a bet. Oh wait.")))
                print()
                if self.__free_hand:
                    type.fast(magenta(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a free bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've doubled it!"))))
                else:
                    type.fast(magenta(bright("You had " + green("${:,}".format(self.__balance)) + magenta(", and with a bet of ") + green("${:,}".format(self.__bet)) + magenta(", you've doubled it!"))))
                print("\n")
                type.fast(magenta(bright("Your new balance is " + green("${:,}".format(self.__balance) + " + ${:,}".format(self.__bet) + " = ${:,}".format(self.__balance+self.__bet)))))
                self.__balance += self.__bet

            case "Dealer Blackjack":
                message = random.randrange(8)
                if message==0: type.fast(red(bright("The Dealer gets a Blackjack and wins! Too bad! So sad! Get good, kiddo!")))
                if message==1: type.fast(red(bright("Dealer secures Blackjack! Game over for you, loser!")))
                if message==2: type.fast(red(bright("Dealer's Blackjack! Well, butter my biscuit, what a surprise!")))
                if message==3: type.fast(red(bright("HAHA you suck buddy. Living infinite money glitch.")))
                if message==4: type.fast(red(bright("You just witnessed greatness. You only wish you were this good.")))
                if message==5: type.fast(red(bright("Natural 21 for the house. The Dealer doesn't even celebrate. This is Tuesday for him.")))
                if message==6: type.fast(red(bright("Dealer Blackjack. He flips the cards like he's bored. He IS bored. You're entertainment.")))
                if message==7: type.fast(red(bright("21. No effort. No suspense. Just the house being the house.")))
                print()
                if self.__free_hand:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your free bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your balance is still " + green("${:,}".format(self.__balance)))))
                elif self.__balance - self.__bet <= 0:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + "${:,}".format(self.__balance) + " - ${:,}".format(self.__bet) + " = ${:,}".format(self.__balance-self.__bet))))
                    self.__balance -= self.__bet
                else:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + green("${:,}".format(self.__balance) + red(" - ${:,}".format(self.__bet)) + green(" = ${:,}".format(self.__balance-self.__bet))))))
                    self.__balance -= self.__bet

            case "Dealer Wins":
                message = random.randrange(8)
                if message==0: type.fast(red(bright("The Dealer wins! Too bad! So sad! Stay mad!")))
                if message==1: type.fast(red(bright("Dealer wins with the higher hand! Not your day, huh?")))
                if message==2: type.fast(red(bright("You simply got outplayed on this one.")))
                if message==3: type.fast(red(bright("Your hand is inferior to the Dealer's. Which means you lose.")))
                if message==4: type.fast(red(bright("Dealer's number is higher, so I guess you lost. Unfortunate.")))
                if message==5: type.fast(red(bright("The Dealer wins. He sweeps your chips away like crumbs off a table.")))
                if message==6: type.fast(red(bright("Close, but close only counts in horseshoes. And this ain't horseshoes.")))
                if message==7: type.fast(red(bright("The house always wins. Today, you're the proof.")))
                print()
                if self.__free_hand:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your free bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your balance is still " + green("${:,}".format(self.__balance)))))
                elif self.__balance - self.__bet <= 0:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + "${:,}".format(self.__balance) + " - ${:,}".format(self.__bet) + " = ${:,}".format(self.__balance-self.__bet))))
                    self.__balance -= self.__bet
                else:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + green("${:,}".format(self.__balance) + red(" - ${:,}".format(self.__bet)) + green(" = ${:,}".format(self.__balance-self.__bet))))))
                    self.__balance -= self.__bet

            case "Player Bust":
                message = random.randrange(8)
                if message==0: type.fast(red(bright("Bust! The Dealer wins! Too bad! So sad! You suuuuck!")))
                if message==1: type.fast(red(bright("Bust city! Did your cards get too excited?")))
                if message==2: type.fast(red(bright("Busted! Did you think this was a game of 'who can count the highest'?")))
                if message==3: type.fast(red(bright("Bust! Should've stopped while you were ahead.")))
                if message==4: type.fast(red(bright("You busted! How'd it feel?")))
                if message==5: type.fast(red(bright("Over 21. You flew too close to the sun. Icarus would be proud. And also broke.")))
                if message==6: type.fast(red(bright("BUST. The most satisfying word in the Dealer's vocabulary.")))
                if message==7: type.fast(red(bright("You busted. The Dealer barely glances at your cards. He already knew.")))
                print()

                if self.__free_hand:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your free bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your balance is still " + green("${:,}".format(self.__balance)))))
                elif self.__balance - self.__bet <= 0:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + "${:,}".format(self.__balance) + " - ${:,}".format(self.__bet) + " = ${:,}".format(self.__balance-self.__bet))))
                    self.__balance -= self.__bet
                else:
                    type.fast(red(bright("You had " + green("${:,}".format(self.__balance)) + red(" and lost your bet of ") + green("${:,}".format(self.__bet)))))
                    print("\n")
                    type.fast(red(bright("Your new balance is " + green("${:,}".format(self.__balance) + red(" - ${:,}".format(self.__bet)) + green(" = ${:,}".format(self.__balance-self.__bet))))))
                    self.__balance -= self.__bet

            case "Tie":
                message = random.randrange(8)
                if message==0: type.fast(cyan(bright("You and the Dealer have the same value. It's a draw. So, so very lame.")))
                if message==1: type.fast(cyan(bright("Standoff! Equal hands, no winner!")))
                if message==2: type.fast(cyan(bright("Twinsies! You and the Dealer are matchy-matchy!")))
                if message==3: type.fast(cyan(bright("Welp. Those numbers are the same. So much for that round.")))
                if message==4: type.fast(cyan(bright("The lamest outcome possible, and yet here we are.")))
                if message==5: type.fast(cyan(bright("Push. Nobody wins. Nobody loses. The universe yawns.")))
                if message==6: type.fast(cyan(bright("A tie. The Dealer shrugs. You shrug. Everyone shrugs. Moving on.")))
                if message==7: type.fast(cyan(bright("Same number, different people. The philosophical implications are staggering. And boring.")))
                print()
                if self.__free_hand:
                    type.fast(cyan(bright("You had " + green("${:,}".format(self.__balance)) + cyan(", and since this hand was free, your balance hasn't changed"))))
                else:
                    type.fast(cyan(bright("You had " + green("${:,}".format(self.__balance)) + cyan(", and you win back your bet of ") + green("${:,}".format(self.__bet)))))
                print("\n")
                type.fast(cyan(bright("Your balance is still " + green("${:,}".format(self.__balance)))))

            case "Tie Blackjack":
                message = random.randrange(8)
                if message==0: type.fast(cyan(bright("You and the Dealer both got a Blackjack. How boring.")))
                if message==1: type.fast(cyan(bright("Stalemate with matching Blackjacks! Who coulda guessed?")))
                if message==2: type.fast(cyan(bright("Double Blackjacks! What are the odds? (Don't answer that.)")))
                if message==3: type.fast(cyan(bright("It's a Blackjack draw! Did you both use your one-time miracle for this?")))
                if message==4: type.fast(cyan(bright("21 = 21. Sorry.")))
                if message==5: type.fast(cyan(bright("Matching Blackjacks. The Dealer and you lock eyes. Respect? Contempt? Yes.")))
                if message==6: type.fast(cyan(bright("Both 21. Both perfect. Both pointless. The house always finds a way to bore you.")))
                if message==7: type.fast(cyan(bright("A draw at 21. The most exciting unexciting thing that can happen.")))
                print()
                if self.__free_hand:
                    type.fast(cyan(bright("You had " + green("${:,}".format(self.__balance)) + cyan(", and since this hand was free, your balance hasn't changed"))))
                else:
                    type.fast(cyan(bright("You had " + green("${:,}".format(self.__balance)) + cyan(", and you win back your bet of ") + green("${:,}".format(self.__bet)))))
                print("\n")
                type.fast(cyan(bright("Your balance is still " + green("${:,}".format(self.__balance)))))

        # Tattered Cloak effect: refund the bet if triggered
        if tattered_cloak_saved and status in ["Dealer Wins", "Dealer Blackjack", "Player Bust"]:
            print("\n")
            if has_invisible_cloak:
                type.fast(cyan(bright("Your Invisible Cloak shimmers... The Dealer completely forgot you were even playing!")))
            else:
                type.fast(magenta(bright("Your Tattered Cloak rustles... The Dealer seems to have forgotten to collect your bet!")))
            self.__balance += self.__bet  # Refund the bet
            print()
            if has_invisible_cloak:
                type.fast(cyan(bright("Your balance is restored to " + green("${:,}".format(self.__balance)))))
            else:
                type.fast(magenta(bright("Your balance is restored to " + green("${:,}".format(self.__balance)))))

        # Insurance payout: 2:1 if dealer had blackjack
        if self.__insurance_bet > 0:
            if status == "Dealer Blackjack":
                payout = self.__insurance_bet * 2
                self.__balance += self.__insurance_bet + payout  # Return bet + 2:1 payout
                print("\n")
                if self.__player.has_item("Dealer's Mercy"):
                    type.fast(magenta(bright("Your Dealer's Mercy shines! Insurance pays out " + green("${:,}".format(payout)) + "!")))
                else:
                    type.fast(magenta(bright("Your Dealer's Grudge pays off! Insurance pays out " + green("${:,}".format(payout)) + "!")))
                print()
                type.fast(magenta(bright("Your balance is now " + green("${:,}".format(self.__balance)))))
                # Update stats
                stats = self.__player.get_gambling_stats()
                stats["insurance_won"] = stats.get("insurance_won", 0) + 1
            else:
                print("\n")
                type.fast(cyan("Your insurance bet of " + red("${:,}".format(self.__insurance_bet)) + cyan(" is lost...")))
                # Update stats
                stats = self.__player.get_gambling_stats()
                stats["insurance_lost"] = stats.get("insurance_lost", 0) + 1

        self.__player.set_balance(self.__balance)
        self.__player.gambling_result(status, self.__bet)  # Sanity effects from gambling
        self.__player.status()
        self._check_hot_money_noticed()
        self.end_round_dealer_happiness(status)

        print()
        return True

    def end_round_dealer_happiness(self, status):
        bet_ratio = self.__bet / max(self.__balance, 1)
        if self.__player.get_rank() == 0:
            modifier = 0
        elif self.__player.get_rank() == 1:
            modifier = 1
        elif self.__player.get_rank() == 2:
            modifier = 2
        elif self.__player.get_rank() == 3:
            modifier = 3
        elif self.__player.get_rank() == 4:
            modifier = 4
        elif self.__player.get_rank() == 5:
            modifier = 5

        # === BUST STREAK DETECTION ===
        if status == "Player Bust":
            self.__bust_streak += 1

            # Check for min-bet busting (throwing hands cheaply)
            was_min_bet = (self.__bet <= self.__min_bet * 1.1)  # Within 10% of min bet
            if was_min_bet:
                self.__min_bet_bust_count += 1
                if self.__min_bet_bust_count >= 3:
                    # Dealer gets suspicious of cheap throwing
                    print("\n")
                    suspicious_lines = [
                        '"You keep busting on minimum bets. You think I\'m stupid?"',
                        '"Three min-bet busts in a row. You\'re either terrible or you\'re trying something."',
                        '"I\'ve seen hustlers try this before. Lose small, keep me happy. Cute. Real cute."',
                        '"You\' re tanking on purpose. I can smell it. You reek of strategy."'
                    ]
                    type.slow(red(bright(random.choice(suspicious_lines))))
                    print("\n")
                    self.anger_dealer(25)
                    self.__min_bet_bust_count = 0  # Reset after punishment
            else:
                self.__min_bet_bust_count = 0  # Reset if bust wasn't at min bet

            # 10 busts in a row — dealer thinks you're throwing
            if self.__bust_streak == 10:
                print("\n")
                type.slow(red(bright("The Dealer leans back in his chair and stares at you. Hard.")))
                print()
                type.slow(red(bright('"Ten busts. In a row. TEN."')))
                print()
                type.slow(red(bright('"You\'re either the worst card player I\'ve ever seen, or you\'re throwing hands on purpose."')))
                print()
                type.slow(red(bright('"Either way, I don\'t like it."')))
                print("\n")
                self.__dealer_happiness = 20
                if self.__player.has_item("Delight Indicator") or self.__player.has_item("Delight Manipulator"):
                    self.delight_indicator()
                    print()

            # 11th bust — dealer snaps
            elif self.__bust_streak >= 11:
                print("\n")
                type.slow(red(bright('"Eleven. ELEVEN. You know what? I\'m done playing nice."')))
                print("\n")
                self.__dealer_happiness = 0
                self.__bust_streak = 0  # Reset streak
                if self.__player.has_item("Delight Indicator") or self.__player.has_item("Delight Manipulator"):
                    self.delight_indicator()
                    print()
        else:
            # Any non-bust result resets both streaks
            self.__bust_streak = 0
            self.__min_bet_bust_count = 0

        match status:
            case "Player Blackjack": 
                if bet_ratio >= 0.9:
                    value = 20
                elif bet_ratio >= 0.6:
                    value = 10
                elif bet_ratio >= 0.3:
                    value = 7
                else:
                    value = 5

            case "Player Wins":
                if bet_ratio >= 0.9:
                    value = 10
                elif bet_ratio >= 0.6:
                    value = 7
                elif bet_ratio >= 0.3:
                    value = 4
                else:
                    value = 2

            case "Dealer Bust":
                if bet_ratio >= 0.9:
                    value = 12
                elif bet_ratio >= 0.6:
                    value = 8
                elif bet_ratio >= 0.3:
                    value = 4
                else:
                    value = 2

            case "Dealer Blackjack":
                if bet_ratio >= 0.9:
                    value = -25
                elif bet_ratio >= 0.6:
                    value = -15
                elif bet_ratio >= 0.3:
                    value = -7
                else:
                    value = -5

            case "Dealer Wins":
                if bet_ratio >= 0.9:
                    value = -10
                elif bet_ratio >= 0.6:
                    value = -6
                elif bet_ratio >= 0.3:
                    value = -3
                else:
                    value = -2

            case "Player Bust":
                if bet_ratio >= 0.9:
                    value = -12
                elif bet_ratio >= 0.6:
                    value = -7
                elif bet_ratio >= 0.3:
                    value = -3
                else:
                    value = -2

            case "Tie":
                if bet_ratio >= 0.9:
                    value = 3
                elif bet_ratio >= 0.6:
                    value = 2
                elif bet_ratio >= 0.3:
                    value = 1
                else:
                    value = 1

            case "Tie Blackjack":
                if bet_ratio >= 0.9:
                    value = 4
                elif bet_ratio >= 0.6:
                    value = 3
                elif bet_ratio >= 0.3:
                    value = 1
                else:
                    value = 1

        if value > 0: self.anger_dealer(int(value) + modifier)
        elif value < 0: self.calm_dealer(-int(value))

    def _check_hot_money_noticed(self):
        """Per-hand check: did the dealer notice hot (loan) money in this bet?

        The loan shark's money is convincing, but every dollar run through the dealer
        raises their suspicion.  The chance of being caught scales with:
          - The fraction of the bet that was fake (more fake = more suspicious).
          - How much total fake cash the dealer has already processed this session
            (approaching the has_too_much_fake_cash threshold = near-certain notice).

        Consequences range from a suspicious squint (dealer anger spike) to having the
        hot bills confiscated outright.  Refusing to cooperate makes things worse.
        """
        if self.__fraudulent_portion <= 0:
            return

        fake_ratio = self.__fraudulent_portion / max(1, self.__bet)
        # Base chance: 4-20% per hand, scaled by how much of the bet is hot.
        notice_chance = max(4, int(fake_ratio * 20))
        danger_level = self.__player.get_dealer_fake_cash_danger_level()
        if danger_level > 0:
            notice_chance = min(95, notice_chance + danger_level * 15)

        if random.randrange(100) >= notice_chance:
            return  # The Dealer didn't notice — this time.

        # --- Dealer noticed ---
        print()
        severity = random.randrange(3)

        if severity == 0:
            # Mild: a suspicious glance, nothing more.
            msg = random.randrange(3)
            if msg == 0: type.fast(yellow("The Dealer pauses, turning one of your bills over slowly in his hand."))
            if msg == 1: type.fast(yellow("The Dealer holds a bill up briefly, squinting at the serial number."))
            if msg == 2: type.fast(yellow("The Dealer glances at one of your notes, then back at you."))
            print()
            type.fast(yellow('"Funny-looking paper," he mutters, then slides it back without a word.'))
            self.anger_dealer(8, message=True)

        elif severity == 1:
            # Moderate: the Dealer pockets a bill and docks your balance.
            msg = random.randrange(3)
            if msg == 0: type.fast(red("The Dealer holds a bill up to the light, then sets it aside with a flat look."))
            if msg == 1: type.fast(red("The Dealer examines one of your bills closely, then tucks it under the table."))
            if msg == 2: type.fast(red("The Dealer pulls a bill from the pile and studies it with narrowed eyes."))
            print()
            type.fast(red('"I don\'t take hot money," he says. He keeps the bill.'))
            self.anger_dealer(15, message=True)
            # Confiscate half the fake portion from real balance as a "silence fee".
            penalty = min(self.__balance, self.__fraudulent_portion // 2)
            if penalty > 0:
                self.__player.spend_balance(penalty, dealer_receives_fraud=True)
                self.__balance = self.__player.get_balance()
                self.__player.set_balance(self.__balance)
                print()
                type.fast(red(f"${penalty:,} taken. The Dealer doesn't ask questions. He takes answers."))

        else:
            # Severe: the Dealer makes a scene and takes the full fake amount.
            msg = random.randrange(3)
            if msg == 0: type.fast(red(bright("The Dealer slams his hand on the table.")))
            if msg == 1: type.fast(red(bright("The Dealer stands up, staring hard at your money.")))
            if msg == 2: type.fast(red(bright("The Dealer goes very still. The table goes very quiet.")))
            print()
            type.fast(red(bright('"YOU. Are using HOT MONEY."')))
            print()
            type.fast(red("He reaches across and grabs a fistful of your bills. The whole table goes quiet."))
            self.anger_dealer(30, message=True)
            penalty = min(self.__balance, self.__fraudulent_portion)
            if penalty > 0:
                self.__player.spend_balance(penalty, dealer_receives_fraud=True)
                self.__balance = self.__player.get_balance()
                self.__player.set_balance(self.__balance)
                print()
                type.fast(red(f"${penalty:,} confiscated. Call it a tax on bad decisions."))
        print()

    def draw(self, hand):
        card = self.__deck.draw()
        hand.add(card)
        return card
    
    def print_draw(self, name, position, card):
        # Prints the drawn card, for either the player or dealer
        # Can specify first, second, or next card drawn (could be any word)
        if name == "Player":
            if((card.value()==1) or card.value()==8):
                type.fast("Your " + position + " card is an " + bright(magenta(str(card))))
            else:
                type.fast("Your " + position + " card is a " + bright(magenta(str(card))))

        elif name == "Dealer":
            if((card.value()==1) or card.value()==8):
                type.fast(red("The Dealer's " + position + " card is an " + bright(str(card))))
            else:
                type.fast(red("The Dealer's " + position + " card is a " + bright(str(card))))
    
    def reset(self):
        # Resets hands
        self.__hand = Hand("Player")
        self.__dealer_hand = Hand("Dealer")
        self.__fraudulent_portion = 0

    def hard_reset(self):
        # Resets hands, deck, and possibly anything else I can think of
        self.reset()
        self.__deck.reset()



class Hand:
    __slots__ = ["__cards", "__value", "__name"]

    def __init__(self, name):
        self.__name = name
        self.__cards = []
        self.__value = [0]

    def __repr__(self):
        # Prints for dealer's hand without an ace
        if ((len(self.__value)==1) & (self.__name == "Dealer")):
            hand_string = red(
                "The Dealer's hand has a value of " + bright(str(self.__value[0]))
                )
        
        # Prints for dealer's hand with an ace
        elif ((len(self.__value)==2) & (self.__name == "Dealer")):
            hand_string = red(
                "The Dealer's hand has a value of " + bright(str((self.__value[0]))) + 
                ", or " + bright(str(self.__value[1])) + " since they have an ace"
                )
            
        # Prints for player's hand without an ace
        elif ((len(self.__value)==1) & (self.__name == "Player")):
            hand_string = "Your hand has a value of " + green(bright(str(self.__value[0])))

        elif ((len(self.__value)==2) & (self.__name == "Player")):
            hand_string = ("Your hand has a value of " + green(bright(str(self.__value[0]))) + 
                           ", or " + green(bright(str(self.__value[1]))) + " since you have an ace")

        # for potential debugging purposes. 
        # This intentionally leaves room for additional players
        else:
            hand_string = "This player does not exist. How are you real?"

        return hand_string

    def __len__(self):
        return len(self.__cards)
    
    def has_ace(self):
        return len(self.__value)==2

    def add(self, card):
        # Adds cards to hand, then checks if aces affect the value

        self.__cards.append(card)
        self.__value[0] += card.value()
        if(len(self.__value)==2):
            self.__value[1] += card.value()

        # If the card is an ace, and there's no other aces in the hand
        # This only happens if the hand's value is less than 12, as a
        # hand that's value is 12 + 10 = 22, so the ace must be a 1
        if((card.value()==1) & (len(self.__value)==1) & (self.__value[0]<12)):
            self.__value.append(self.__value[0] + 10)

        # checks the value of the hand if an ace is 11
        # will pop the value if it's greater than 21
        # will set hand value to 21 if it's equal to 21
        if(len(self.__value)==2):
            if(self.__value[1] > 21):
                self.__value.pop()
            elif(self.__value[1] == 21):
                self.__value.pop()
                self.__value[0] = 21

    def value(self):
        return self.__value[0]
    
    def possible_hands(self):
        return len(self.__value)
    
    def get_final_value(self):
        if len(self.__value)==2:
            self.__value[0] = self.__value[1]
    
    def get_card(self, index):
        return self.__cards[index]
    
    def ace_value(self):
        if len(self.__value) == 2:
            return self.__value[1]
        else:
            return 0

    def remove_last_card(self):
        # Remove the last card from the hand and recalculate value
        if len(self.__cards) > 0:
            removed_card = self.__cards.pop()
            # Recalculate the hand value from scratch
            self.__value = [0]
            for card in self.__cards:
                self.__value[0] += card.value()
                if(len(self.__value)==2):
                    self.__value[1] += card.value()
                if((card.value()==1) & (len(self.__value)==1) & (self.__value[0]<12)):
                    self.__value.append(self.__value[0] + 10)
                if(len(self.__value)==2):
                    if(self.__value[1] > 21):
                        self.__value.pop()
                    elif(self.__value[1] == 21):
                        self.__value.pop()
                        self.__value[0] = 21
            return removed_card
        return None