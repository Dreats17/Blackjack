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

class SystemsMixin:
    """Systems: Sanity, gambling stats, grimoire, achievements, statistics, companions, loan shark, pawn shop, dealer happiness, gift system"""

    def get_sanity(self):
        return self._sanity
    
    def lose_sanity(self, value):
        """Decrease sanity. The player will see this."""
        if self._is_broken:
            return  # Already broken, can't lose more sanity
        
        old_sanity = self._sanity
        self._sanity -= value
        # Floor at 0
        if self._sanity < 0:
            self._sanity = 0
        # Show warning message based on new threshold crossed
        if old_sanity > 75 and self._sanity <= 75:
            print("\n")
            type.slow(yellow("Your mind feels... foggy. Something isn't right."))
            print("\n")
        elif old_sanity > 50 and self._sanity <= 50:
            print("\n")
            type.slow(yellow(bright("The edges of your vision blur. Reality feels thin.")))
            print("\n")
        elif old_sanity > 25 and self._sanity <= 25:
            print("\n")
            type.slow(red(bright("Your thoughts are fracturing. The shadows are getting closer.")))
            print("\n")
        
        # Check if sanity hit zero - trigger madness ending or become broken
        if old_sanity > 0 and self._sanity <= 0:
            self.sanity_depleted()
    
    def restore_sanity(self, value):
        """Restore sanity through positive events"""
        old_sanity = self._sanity
        self._sanity += value
        if self._sanity > 100:
            self._sanity = 100
        # Show recovery message if crossing back above a threshold
        if old_sanity <= 50 and self._sanity > 50:
            print("\n")
            type.slow(green("A sense of clarity washes over you. The fog lifts, if only a little."))
            print("\n")
    
    def sanity_indicator(self):
        """Display current sanity level with color coding"""
        if self._is_broken:
            type.type("Your sanity: " + bright(red("BROKEN")))
        elif self._sanity > 75:
            type.type("Your current sanity: " + bright(green(str(self._sanity) + "%")))
        elif self._sanity > 50:
            type.type("Your current sanity: " + bright(yellow(str(self._sanity) + "%")))
        elif self._sanity > 25:
            type.type("Your current sanity: " + bright(magenta(str(self._sanity) + "%")))
        else:
            type.type("Your current sanity: " + bright(red(str(self._sanity) + "%")))
        print("\n")
    
    def get_sanity_description(self):
        """Get a text description of current sanity state"""
        if self._is_broken:
            return "shattered beyond repair"
        elif self._sanity > 90:
            return "clear-headed"
        elif self._sanity > 75:
            return "slightly unsettled"
        elif self._sanity > 60:
            return "anxious"
        elif self._sanity > 50:
            return "disturbed"
        elif self._sanity > 40:
            return "unstable"
        elif self._sanity > 25:
            return "fractured"
        elif self._sanity > 10:
            return "barely holding on"
        else:
            return "teetering on the edge of madness"
    
    def sanity_affects_gambling(self):
        """Returns a modifier based on sanity - low sanity makes gambling harder"""
        if self._sanity > 75:
            return 0  # No penalty
        elif self._sanity > 50:
            return 1  # Slight disadvantage
        elif self._sanity > 25:
            return 2  # Noticeable disadvantage  
        else:
            return 3  # Severe disadvantage
    
    def has_faced_madness(self):
        return self._faced_madness
    
    def set_faced_madness(self):
        self._faced_madness = True
    
    def should_show_sanity_effect(self):
        """Returns True if conditions are right for a sanity effect"""
        if self._sanity > 85:
            return False
        # Lower sanity = more frequent effects
        effect_chance = (100 - self._sanity) // 10
        if random.randrange(20) < effect_chance:
            self._sanity_warnings_shown += 1
            return True
        return False
    
    def get_sanity_effect(self):
        """Returns a description of the player's deteriorating mental state"""
        mild_effects = [
            "For a moment, you could have sworn the shadows moved.",
            "You hear whispers, but when you listen closer... nothing.",
            "Your reflection in the rearview mirror blinks before you do.",
            "The cards in your dreams are always face down. Always.",
            "You can't remember if you slept last night. Or the night before.",
            "Your hands are shaking. When did they start shaking?",
            "You count your money three times. You get a different number each time.",
            "Someone is watching you. You're certain of it. But there's no one there.",
            "You taste copper. There's nothing in your mouth.",
            "The trees outside your car window are too still. Unnaturally still.",
            "You find a note in your pocket. It's your handwriting, but you don't remember writing it.",
            "The sun seems dimmer today. Like it's further away than it should be.",
            "You hear your name called. The voice sounds like your own.",
        ]
        severe_effects = [
            "The world flickers, like a dying light bulb. Reality feels thin.",
            "You see yourself walking past your car window. You don't stop to look.",
            "The Dealer's jade eye appears everywhere. In reflections. In shadows. In the spaces between heartbeats.",
            "Your thoughts are echoing. Echoing. Echoing.",
            "Blood drips from the ceiling of your car. When you look up, it's gone.",
            "The radio turns on by itself. It plays a song that doesn't exist.",
            "You can't feel your heartbeat anymore. You check. It's still there. You think.",
            "The casino's neon sign flickers. It spells your name. Then it doesn't.",
            "The walls are breathing. You're sure of it.",
            "You forgot your own name for a moment. It came back. Eventually.",
        ]
        if self._sanity <= 50:
            return random.choice(mild_effects + severe_effects)
        return random.choice(mild_effects)
    
    def check_madness_confrontation(self):
        """Check if the madness confrontation should trigger (at low sanity)"""
        if self._faced_madness:
            return False
        if self._sanity > 40:  # Only triggers at 40 or below
            return False
        # 10% base chance at 40 sanity, scaling up as sanity drops
        trigger_chance = (50 - self._sanity) // 5
        return random.randrange(100) < trigger_chance

    def gambling_result(self, status, bet_amount):
        """Called after each blackjack hand to affect sanity and track stats"""
        # Update gambling stats
        self.update_gambling_stats(status, bet_amount)
        
        if status in ["Player Blackjack", "Player Wins", "Dealer Bust"]:
            # Winning restores a tiny bit of sanity
            if self._sanity < 100 and random.randrange(5) == 0:
                self._sanity = min(100, self._sanity + 1)
        elif status in ["Dealer Blackjack", "Dealer Wins", "Player Bust"]:
            # Losing big bets damages sanity
            bet_ratio = bet_amount / max(self._balance, 1)
            if bet_ratio >= 0.5:  # Lost half or more of your money
                self.lose_sanity(random.choice([2, 3, 4]))
            elif bet_ratio >= 0.25:  # Lost a quarter
                self.lose_sanity(random.choice([1, 2]))
            # Small losses occasionally chip away at sanity
            elif random.randrange(10) == 0:
                self.lose_sanity(1)

    def update_gambling_stats(self, status, bet_amount):
        """Track gambling statistics for the Gambler's Grimoire"""
        stats = self._gambling_stats
        stats["total_hands"] += 1
        
        old_best_streak = stats["best_win_streak"]
        old_worst_streak = stats["worst_loss_streak"]
        old_biggest_win = stats["biggest_win"]
        old_biggest_loss = stats["biggest_loss"]
        
        if status in ["Player Blackjack", "Player Wins", "Dealer Bust"]:
            stats["wins"] += 1
            winnings = bet_amount * 2 if status == "Player Blackjack" else bet_amount
            stats["total_won"] += winnings
            
            if status == "Player Blackjack":
                stats["blackjacks"] += 1
            
            # Track streak
            if stats["current_streak"] >= 0:
                stats["current_streak"] += 1
            else:
                stats["current_streak"] = 1
            
            if stats["current_streak"] > stats["best_win_streak"]:
                stats["best_win_streak"] = stats["current_streak"]
            
            if winnings > stats["biggest_win"]:
                stats["biggest_win"] = winnings
                
        elif status in ["Dealer Blackjack", "Dealer Wins", "Player Bust"]:
            stats["losses"] += 1
            stats["total_lost"] += bet_amount
            
            if status == "Player Bust":
                stats["busts"] += 1
            
            # Track streak (negative for losses)
            if stats["current_streak"] <= 0:
                stats["current_streak"] -= 1
            else:
                stats["current_streak"] = -1
            
            if abs(stats["current_streak"]) > stats["worst_loss_streak"]:
                stats["worst_loss_streak"] = abs(stats["current_streak"])
            
            if bet_amount > stats["biggest_loss"]:
                stats["biggest_loss"] = bet_amount
                
        else:  # Ties
            stats["ties"] += 1
            stats["current_streak"] = 0
        
        # Check for record breaks and announce if player has Grimoire
        self.check_grimoire_records(old_best_streak, old_worst_streak, old_biggest_win, old_biggest_loss)

    def check_grimoire_records(self, old_best_streak, old_worst_streak, old_biggest_win, old_biggest_loss):
        """Announce record-breaking moments if player has Gambler's Grimoire"""
        if not (self.has_item("Gambler's Grimoire") or self.has_item("Oracle's Tome")):
            return
        
        stats = self._gambling_stats
        records_broken = []
        
        if stats["best_win_streak"] > old_best_streak and stats["best_win_streak"] >= 3:
            records_broken.append(("win_streak", stats["best_win_streak"]))
        
        if stats["worst_loss_streak"] > old_worst_streak and stats["worst_loss_streak"] >= 3:
            records_broken.append(("loss_streak", stats["worst_loss_streak"]))
        
        if stats["biggest_win"] > old_biggest_win and old_biggest_win > 0:
            records_broken.append(("biggest_win", stats["biggest_win"]))
        
        if stats["biggest_loss"] > old_biggest_loss and old_biggest_loss > 0:
            records_broken.append(("biggest_loss", stats["biggest_loss"]))
        
        # Milestone checks
        if stats["total_hands"] in [10, 25, 50, 100, 250, 500, 1000]:
            records_broken.append(("milestone_hands", stats["total_hands"]))
        
        if stats["blackjacks"] in [1, 5, 10, 25, 50]:
            records_broken.append(("milestone_blackjacks", stats["blackjacks"]))
        
        for record_type, value in records_broken:
            self.grimoire_announcement(record_type, value)

    def grimoire_announcement(self, record_type, value):
        """Cheeky announcements from the Gambler's Grimoire"""
        print("\n")
        
        if self.has_item("Oracle's Tome"):
            book_name = "Oracle's Tome"
            book_color = cyan
        else:
            book_name = "Gambler's Grimoire"
            book_color = magenta
        
        type.fast("Your " + bright(book_color(book_name)) + " vibrates...")
        print()
        
        if record_type == "win_streak":
            messages = [
                f"\"Hot streak alert! {value} wins in a row! Don't let it go to your head. Actually, do. It's fun to watch.\"",
                f"\"{value} consecutive victories! The Dealer's eye is twitching. Beautiful.\"",
                f"\"You're on fire! {value} wins! This book hasn't seen action like this since... well, ever. I'm a book.\"",
            ]
        elif record_type == "loss_streak":
            messages = [
                f"\"Impressive! {value} losses in a row! That takes real commitment to failure.\"",
                f"\"New personal worst! {value} consecutive losses! I'm genuinely concerned for you.\"",
                f"\"{value} losses in a row. The Dealer is probably getting bored.\"",
            ]
        elif record_type == "biggest_win":
            messages = [
                f"\"NEW RECORD! Biggest single win: ${value:,}! I'm updating my pages as we speak.\"",
                f"\"${value:,} in one hand! Your grandmother would be so confused, yet proud!\"",
                f"\"Look at you, high roller! ${value:,} is your new personal best!\"",
            ]
        elif record_type == "biggest_loss":
            messages = [
                f"\"Congratulations? Biggest loss ever: ${value:,}. I'll... I'll write that down.\"",
                f"\"${value:,} gone in a single hand. A new low! Or high? Definitely a new something.\"",
                f"\"I've recorded ${value:,} as your worst single-hand loss. For posterity. You're welcome.\"",
            ]
        elif record_type == "milestone_hands":
            messages = [
                f"\"{value} hands played! You're really committed to this gambling lifestyle, huh?\"",
                f"\"Milestone reached: {value} total hands! Your fingers must be exhausted.\"",
                f"\"{value} hands! At this rate, you'll either be rich or homeless by next week.\"",
            ]
        elif record_type == "milestone_blackjacks":
            messages = [
                f"\"{value} blackjacks! The Dealer is starting to suspect you're cheating. You're not. You're just annoyingly lucky.\"",
                f"\"Blackjack count: {value}! That's {value} times you've made the Dealer question his career choices.\"",
                f"\"{value} blackjacks achieved! Keep going and they might name a card after you. Probably the Joker.\"",
            ]
        else:
            messages = ["\"Something noteworthy happened. I'll write it down eventually.\""]
        
        type.fast(book_color(random.choice(messages)))
        print()
        self.update_gamblers_grimoire_durability()

    def get_gambling_stats(self):
        """Return the gambling stats dictionary"""
        return self._gambling_stats

    def grimoire_full_report(self):
        """Display full statistics from the Gambler's Grimoire"""
        stats = self._gambling_stats
        
        if self.has_item("Oracle's Tome"):
            book_name = "Oracle's Tome"
            book_color = cyan
        else:
            book_name = "Gambler's Grimoire"
            book_color = magenta
        
        print("\n")
        type.fast("You open the " + bright(book_color(book_name)) + "...")
        print("\n")
        
        # Win rate calculation
        total = stats["wins"] + stats["losses"]
        win_rate = (stats["wins"] / total * 100) if total > 0 else 0
        
        type.fast(book_color("═══════════════════════════════════════"))
        print()
        type.fast(book_color("        YOUR GAMBLING LEGACY           "))
        print()
        type.fast(book_color("═══════════════════════════════════════"))
        print()
        
        type.fast(f"Total Hands Played: {bright(str(stats['total_hands']))}")
        print()
        type.fast(f"Wins: {green(str(stats['wins']))} | Losses: {red(str(stats['losses']))} | Ties: {yellow(str(stats['ties']))}")
        print()
        type.fast(f"Win Rate: {bright(f'{win_rate:.1f}%')}")
        print()
        type.fast(f"Blackjacks Hit: {bright(yellow(str(stats['blackjacks'])))}")
        print()
        type.fast(f"Times You Busted: {red(str(stats['busts']))}")
        print()
        print()
        type.fast(f"Total Won: {green(bright('${:,}'.format(stats['total_won'])))}")
        print()
        type.fast(f"Total Lost: {red(bright('${:,}'.format(stats['total_lost'])))}")
        print()
        net = stats['total_won'] - stats['total_lost']
        if net >= 0:
            type.fast(f"Net Profit: {green(bright('${:,}'.format(net)))}")
        else:
            type.fast(f"Net Loss: {red(bright('${:,}'.format(abs(net))))}")
        print()
        print()
        type.fast(f"Biggest Single Win: {green('${:,}'.format(stats['biggest_win']))}")
        print()
        type.fast(f"Biggest Single Loss: {red('${:,}'.format(stats['biggest_loss']))}")
        print()
        type.fast(f"Best Win Streak: {green(str(stats['best_win_streak']))}")
        print()
        type.fast(f"Worst Loss Streak: {red(str(stats['worst_loss_streak']))}")
        print()
        
        # Oracle's Tome special feature - snarky predictions
        if self.has_item("Oracle's Tome"):
            print()
            type.fast(cyan("═══════════════════════════════════════"))
            print()
            type.fast(cyan("        THE ORACLE SPEAKS...           "))
            print()
            if win_rate > 60:
                predictions = [
                    "\"Your luck is disgusting. I predict the Dealer will 'accidentally' spill something on you soon.\"",
                    "\"The stars align in your favor. Unfortunately, the Dealer's revolver aligns even better.\"",
                    "\"You're winning too much. The universe is taking notes. And not the good kind.\""
                ]
            elif win_rate > 40:
                predictions = [
                    "\"You're perfectly average. Congratulations on your mediocrity.\"",
                    "\"The cosmos are indifferent to your existence. As am I. Play on.\"",
                    "\"Your future holds... more gambling. Shocking prediction, I know.\""
                ]
            else:
                predictions = [
                    "\"I foresee... more losses. But hey, at least you're consistent!\"",
                    "\"The stars say you should maybe try a different hobby. Like knitting.\"",
                    "\"Your gambling future is cloudy. Mostly because of all the tears.\""
                ]
            type.fast(cyan(random.choice(predictions)))
            print()
        
        print()

    def update_gamblers_grimoire_durability(self, invincible=False):
        """Update durability for Gambler's Grimoire or Oracle's Tome"""
        has_base = self.has_item("Gambler's Grimoire")
        has_upgrade = self.has_item("Oracle's Tome")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[17] = -1
                
            if (self._item_durability[17] > 0):
                self._item_durability[17] -= random.choice([1, 2, 3])
                if self._item_durability[17] <= 0:
                    self._item_durability[17] = 0
                    if has_upgrade:
                        self.break_item("Oracle's Tome")
                        type.slow(red(bright("Your Oracle's Tome crumbles to dust!")))
                    else:
                        self.break_item("Gambler's Grimoire")
                        type.slow(red(bright("Your Gambler's Grimoire's pages have faded to illegibility!")))
                    print("\n")

            if (self._item_durability[17] == 0):
                self._item_durability[17] = 60 if has_base else 100  # Oracle's Tome lasts longer


    def update_gamblers_chalice_durability(self, invincible=False):
        """Update durability for Gambler's Chalice or Overflowing Goblet"""
        has_base = self.has_item("Gambler's Chalice")
        has_upgrade = self.has_item("Overflowing Goblet")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[13] = -1
                
            if (self._item_durability[13] > 0):
                self._item_durability[13] -= random.choice([1, 2, 3, 5])
                if self._item_durability[13] <= 0:
                    self._item_durability[13] = 0
                    if has_upgrade:
                        self.break_item("Overflowing Goblet")
                        type.slow(red(bright("Your Overflowing Goblet has shattered!")))
                    else:
                        self.break_item("Gambler's Chalice")
                        type.slow(red(bright("Your Gambler's Chalice has cracked!")))
                    print("\n")

            if (self._item_durability[13] == 0):
                self._item_durability[13] = 20 if has_base else 30  # Upgrade lasts longer


    def update_twins_locket_durability(self, invincible=False):
        """Update durability for Twin's Locket or Mirror of Duality"""
        has_base = self.has_item("Twin's Locket")
        has_upgrade = self.has_item("Mirror of Duality")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[14] = -1
                
            if (self._item_durability[14] > 0):
                self._item_durability[14] -= random.choice([1, 2, 3, 5])
                if self._item_durability[14] <= 0:
                    self._item_durability[14] = 0
                    if has_upgrade:
                        self.break_item("Mirror of Duality")
                        type.slow(red(bright("Your Mirror of Duality has cracked down the middle!")))
                    else:
                        self.break_item("Twin's Locket")
                        type.slow(red(bright("Your Twin's Locket snapped shut forever!")))
                    print("\n")

            if (self._item_durability[14] == 0):
                self._item_durability[14] = 18 if has_base else 28  # Upgrade lasts longer


    def update_white_feather_durability(self, invincible=False):
        """Update durability for White Feather or Phoenix Feather"""
        has_base = self.has_item("White Feather")
        has_upgrade = self.has_item("Phoenix Feather")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[15] = -1
                
            if (self._item_durability[15] > 0):
                self._item_durability[15] -= random.choice([1, 2, 3, 5])
                if self._item_durability[15] <= 0:
                    self._item_durability[15] = 0
                    if has_upgrade:
                        self.break_item("Phoenix Feather")
                        type.slow(red(bright("Your Phoenix Feather has burned away!")))
                    else:
                        self.break_item("White Feather")
                        type.slow(red(bright("Your White Feather has crumbled to dust!")))
                    print("\n")

            if (self._item_durability[15] == 0):
                self._item_durability[15] = 25 if has_base else 40  # Phoenix Feather lasts longer


    def update_dealers_grudge_durability(self, invincible=False):
        """Update durability for Dealer's Grudge or Dealer's Mercy"""
        has_base = self.has_item("Dealer's Grudge")
        has_upgrade = self.has_item("Dealer's Mercy")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[16] = -1
                
            if (self._item_durability[16] > 0):
                self._item_durability[16] -= random.choice([1, 2, 3, 5])
                if self._item_durability[16] <= 0:
                    self._item_durability[16] = 0
                    if has_upgrade:
                        self.break_item("Dealer's Mercy")
                        type.slow(red(bright("Your Dealer's Mercy has faded away!")))
                    else:
                        self.break_item("Dealer's Grudge")
                        type.slow(red(bright("Your Dealer's Grudge has lost its power!")))
                    print("\n")

            if (self._item_durability[16] == 0):
                self._item_durability[16] = 22 if has_base else 35  # Upgrade lasts longer


    def sanity_depleted(self):
        """Called when sanity hits 0 - either madness ending or become broken"""
        print("\n")
        type.slow(red(bright("===============================================")))
        type.slow(red(bright("         YOUR SANITY HAS SHATTERED           ")))
        type.slow(red(bright("===============================================")))
        print("\n")
        
        type.slow("Everything goes dark. The world folds in on itself.")
        print("\n")
        type.slow("You feel yourself slipping... falling... breaking...")
        print("\n")
        
        # 40% chance of madness ending, 60% chance of becoming broken
        if random.randrange(100) < 40:
            type.slow(red("The darkness swallows you whole."))
            print("\n")
            time.sleep(2)
            self.madness_ending()
        else:
            self.become_broken()
    
    def become_broken(self):
        """You survive the sanity break, but you're never the same"""
        type.slow("...")
        print("\n")
        time.sleep(1)
        type.slow("Something inside you... snaps.")
        print("\n")
        type.slow("But it doesn't kill you. Not physically, anyway.")
        print("\n")
        type.slow(cyan("You open your eyes. The world looks... wrong. Colors are too bright. Sounds are too loud. Everything has edges that shouldn't be there."))
        print("\n")
        type.slow(cyan("Your hands are shaking. They won't stop. You're not sure they ever will."))
        print("\n")
        type.slow(yellow(bright("You have become BROKEN.")))
        print("\n")
        type.slow(yellow("Your mind is shattered, but somehow you continue. The game goes on."))
        print("\n")
        type.slow(yellow("But nothing will ever be the same."))
        print("\n")
        
        self._is_broken = True
        self._sanity = 0  # Sanity stays at 0 forever
        self.meet("Broken Mind")
        
        ask.press_continue("Press any key to continue your broken existence...")
        print("\n")
    
    def is_broken(self):
        """Check if player has been broken"""
        return self._is_broken
    
    def get_broken_effect(self):
        """Get a random broken mind effect for gameplay"""
        effects = [
            "Your vision doubles. Which pile of money is real?",
            "You hear the cards laughing. They're always laughing now.",
            "Your fingers move on their own, betting before you can think.",
            "The Dealer's face keeps shifting. Is that really him?",
            "You forgot where you are. You remember. You forget again.",
            "The numbers don't make sense anymore. They never did.",
            "You see yourself sitting across the table. He waves.",
            "Time skips. Did you just play a hand? When?",
            "The chips feel like teeth in your hands.",
            "Someone is screaming. Oh. It's you. You stop.",
            "You can taste colors now. Green tastes like regret.",
            "Your reflection in the cards is smiling. You're not.",
            "The walls are too close. No, too far. Which is it?",
            "You blink and lose track of three hands.",
            "The Dealer said something. You laughed. You don't know why.",
        ]
        return random.choice(effects)
    
    def broken_gameplay_effect(self):
        """Apply a random broken effect during gameplay - returns what happened"""
        effect_type = random.randrange(10)
        
        if effect_type == 0:
            # Randomly lose some money
            loss = random.randint(1, min(100, self._balance // 10 + 1))
            self._balance -= loss
            return ("money_loss", loss, "You blink and some money is gone. Did you spend it? Did someone take it? Does it matter?")
        elif effect_type == 1:
            # Randomly gain a small amount (hallucinated winnings that turn out to be real?)
            gain = random.randint(1, 20)
            self._balance += gain
            return ("money_gain", gain, "You find money in your pocket. You don't remember putting it there. You don't question it anymore.")
        elif effect_type == 2:
            # Take damage from self-harm/accidents
            damage = random.randint(1, 5)
            self.hurt(damage)
            return ("self_harm", damage, "You notice blood on your hands. You don't remember how it got there.")
        elif effect_type == 3:
            # Heal slightly (dissociation numbs the pain)
            heal = random.randint(1, 3)
            self.heal(heal)
            return ("numb", heal, "You can't feel anything anymore. Maybe that's a blessing.")
        else:
            # Just a visual/text effect, no gameplay impact
            return ("hallucination", 0, self.get_broken_effect())

    # Item upgrade system (Oswald)
    # Index: 0=delight_indicator, 1=health_indicator, 2=dirty_old_hat, 3=golden_watch, 
    #        4=sneaky_peeky_shades, 5=quiet_sneakers, 6=faulty_insurance, 7=lucky_coin,
    #        8=worn_gloves, 9=tattered_cloak, 10=rusty_compass, 11=pocket_watch
    def get_upgraded_version(self, item):
        # Maps base items to their upgraded versions
        upgrades = {
            "Delight Indicator": "Delight Manipulator",
            "Health Indicator": "Health Manipulator", 
            "Dirty Old Hat": "Unwashed Hair",
            "Golden Watch": "Sapphire Watch",
            "Sneaky Peeky Shades": "Sneaky Peeky Goggles",
            "Quiet Sneakers": "Quiet Bunny Slippers",
            "Faulty Insurance": "Real Insurance",
            "Lucky Coin": "Lucky Medallion",
            "Worn Gloves": "Velvet Gloves",
            "Tattered Cloak": "Invisible Cloak",
            "Rusty Compass": "Golden Compass",
            "Pocket Watch": "Grandfather Clock",
            # New mystical items
            "Gambler's Chalice": "Overflowing Goblet",
            "Twin's Locket": "Mirror of Duality",
            "White Feather": "Phoenix Feather",
            "Dealer's Grudge": "Dealer's Mercy",
            "Gambler's Grimoire": "Oracle's Tome"
        }
        return upgrades.get(item, None)
    
    # Upgrade access based on mechanic visits
    def can_access_upgrades(self):
        """Player can access upgrades after 3+ mechanic visits and having at least 1 item"""
        return self._mechanic_visits >= 3 and len(self._inventory) >= 1
    
    def get_mechanic_visits(self):
        return self._mechanic_visits
    
    def is_upgraded_item(self, item):
        # Check if an item is an upgraded version
        upgraded_items = ["Delight Manipulator", "Health Manipulator", "Unwashed Hair",
                         "Sapphire Watch", "Sneaky Peeky Goggles", "Quiet Bunny Slippers",
                         "Real Insurance", "Lucky Medallion", "Velvet Gloves",
                         "Invisible Cloak", "Golden Compass", "Grandfather Clock",
                         "Overflowing Goblet", "Mirror of Duality", "Phoenix Feather",
                         "Dealer's Mercy", "Oracle's Tome"]
        return item in upgraded_items
    
    def can_upgrade(self, item):
        # Can only upgrade base items, and must own them
        return self.has_item(item) and self.get_upgraded_version(item) is not None
    
    def perform_upgrade(self, item):
        # Remove old item and add upgraded version
        upgraded = self.get_upgraded_version(item)
        if upgraded and self.has_item(item):
            self.use_item(item)
            self.add_item(upgraded)
            return upgraded
        return None
    
    def all_items_upgraded(self):
        # Check if player has all upgraded versions
        upgraded_items = ["Delight Manipulator", "Health Manipulator", "Unwashed Hair",
                         "Sapphire Watch", "Sneaky Peeky Goggles", "Quiet Bunny Slippers",
                         "Real Insurance", "Lucky Medallion", "Velvet Gloves",
                         "Invisible Cloak", "Golden Compass", "Grandfather Clock",
                         "Overflowing Goblet", "Mirror of Duality", "Phoenix Feather",
                         "Dealer's Mercy", "Oracle's Tome"]
        for item in upgraded_items:
            if not self.has_item(item):
                return False
        return True
    
    def meet(self, person):
        self._met.add(person)
        self._statistics["people_met"] += 1

    def has_met(self, person):
        return person in self._met

    # ==========================================
    # ACHIEVEMENT SYSTEM
    # ==========================================
    
    def unlock_achievement(self, achievement_id):
        """Unlock an achievement (silent - only shown on death)"""
        if achievement_id not in self._achievements:
            self._achievements.add(achievement_id)
    
    def has_achievement(self, achievement_id):
        return achievement_id in self._achievements
    
    def get_achievement_count(self):
        return len(self._achievements)
    
    def display_final_achievements(self):
        """Display all unlocked achievements on death"""
        if len(self._achievements) == 0:
            return
        
        print()
        type.slow(bright(yellow("═" * 50)))
        type.slow(bright(yellow("              ACHIEVEMENTS UNLOCKED")))
        type.slow(bright(yellow("═" * 50)))
        print()
        
        # Sort achievements by rarity (hardest first)
        achievement_order = self.get_sorted_achievements()
        
        for ach_id in achievement_order:
            if ach_id in self._achievements:
                ach_data = self._lists.get_achievement_data(ach_id)
                if ach_data:
                    rarity = self.get_achievement_rarity(ach_id)
                    rarity_color = self.get_rarity_color(rarity)
                    type.fast(rarity_color("★ ") + bright(ach_data["name"]) + rarity_color(" [" + rarity.upper() + "]"))
                    type.fast("  " + ach_data["description"])
                    print()
        
        total_achievements = self._lists.get_total_achievements()
        completion = (len(self._achievements) / total_achievements * 100) if total_achievements > 0 else 0
        
        print()
        type.slow(bright(f"Total: {len(self._achievements)}/{total_achievements} ({completion:.1f}%)"))
        print()
    
    def get_achievement_rarity(self, ach_id):
        """Return rarity tier for achievement"""
        # Legendary (hardest)
        legendary = ["year_survivor", "perfect_record", "lottery_winner", "death_defier", "item_master", 
                    "true_gambler", "philanthropist", "cursed_survival", "master_collector", "casino_legend",
                    "judas"]  # Dark ending
        # Epic
        epic = ["hundred_days", "half_million", "millionaire", "blackjack_legend", "win_streak_10", 
               "comeback_master", "near_miss", "full_house", "max_companions", "sanity_master", "debt_free",
               "noahs_ark", "disney_princess", "marine_biologist"]
        # Rare
        rare = ["month_survivor", "hundred_thousand", "blackjack_master", "hot_streak", "card_shark",
               "animal_lover", "cheated_death", "collector", "social_butterfly", "night_owl", "morning_person",
               "zookeeper"]
        # Uncommon
        uncommon = ["week_survivor", "first_ten_thousand", "comeback_kid", "first_friend", "clinging_to_life",
                   "treasure_hunter", "regular", "rock_bottom", "sanity_saved", "devils_deal", "broken_but_alive"]
        
        if ach_id in legendary:
            return "legendary"
        elif ach_id in epic:
            return "epic"
        elif ach_id in rare:
            return "rare"
        elif ach_id in uncommon:
            return "uncommon"
        return "common"
    
    def get_rarity_color(self, rarity):
        """Return color function for rarity"""
        if rarity == "legendary":
            return lambda x: magenta(bright(x))
        elif rarity == "epic":
            return lambda x: cyan(bright(x))
        elif rarity == "rare":
            return lambda x: yellow(bright(x))
        elif rarity == "uncommon":
            return lambda x: green(x)
        return lambda x: x  # common = white
    
    def get_sorted_achievements(self):
        """Return achievements sorted by rarity (rarest first)"""
        all_achievements = list(self._lists.get_all_achievement_ids())
        return sorted(all_achievements, key=lambda x: 
                     {"legendary": 0, "epic": 1, "rare": 2, "uncommon": 3, "common": 4}[self.get_achievement_rarity(x)])

    def check_achievements(self):
        """Check all achievement conditions and unlock any earned"""
        # Common - Money milestones
        if self._balance >= 1000 and not self.has_achievement("first_thousand"):
            self.unlock_achievement("first_thousand")
        if self._balance >= 10000 and not self.has_achievement("first_ten_thousand"):
            self.unlock_achievement("first_ten_thousand")
        if self._balance >= 50000 and not self.has_achievement("fifty_thousand"):
            self.unlock_achievement("fifty_thousand")
        if self._balance >= 100000 and not self.has_achievement("hundred_thousand"):
            self.unlock_achievement("hundred_thousand")
        if self._balance >= 250000 and not self.has_achievement("quarter_million"):
            self.unlock_achievement("quarter_million")
        if self._balance >= 500000 and not self.has_achievement("half_million"):
            self.unlock_achievement("half_million")
        if self._balance >= 900000 and not self.has_achievement("nine_hundred"):
            self.unlock_achievement("nine_hundred")
        if self._balance >= 1000000 and not self.has_achievement("millionaire"):
            self.unlock_achievement("millionaire")
        if self._balance >= 2000000 and not self.has_achievement("multi_millionaire"):
            self.unlock_achievement("multi_millionaire")
        
        # Common - Day milestones
        if self._day >= 3 and not self.has_achievement("three_days"):
            self.unlock_achievement("three_days")
        if self._day >= 7 and not self.has_achievement("week_survivor"):
            self.unlock_achievement("week_survivor")
        if self._day >= 14 and not self.has_achievement("two_weeks"):
            self.unlock_achievement("two_weeks")
        if self._day >= 30 and not self.has_achievement("month_survivor"):
            self.unlock_achievement("month_survivor")
        if self._day >= 100 and not self.has_achievement("hundred_days"):
            self.unlock_achievement("hundred_days")
        if self._day >= 200 and not self.has_achievement("two_hundred_days"):
            self.unlock_achievement("two_hundred_days")
        if self._day >= 365 and not self.has_achievement("year_survivor"):
            self.unlock_achievement("year_survivor")
        
        # Gambling milestones
        stats = self._gambling_stats
        if stats["blackjacks"] >= 1 and not self.has_achievement("first_blackjack"):
            self.unlock_achievement("first_blackjack")
        if stats["total_hands"] >= 10 and not self.has_achievement("ten_hands"):
            self.unlock_achievement("ten_hands")
        if stats["total_hands"] >= 50 and not self.has_achievement("fifty_hands"):
            self.unlock_achievement("fifty_hands")
        if stats["total_hands"] >= 100 and not self.has_achievement("card_shark"):
            self.unlock_achievement("card_shark")
        if stats["total_hands"] >= 200 and not self.has_achievement("two_hundred_hands"):
            self.unlock_achievement("two_hundred_hands")
        if stats["total_hands"] >= 500 and not self.has_achievement("five_hundred_hands"):
            self.unlock_achievement("five_hundred_hands")
        if stats["total_hands"] >= 1000 and not self.has_achievement("true_gambler"):
            self.unlock_achievement("true_gambler")
        
        if stats["blackjacks"] >= 10 and not self.has_achievement("blackjack_master"):
            self.unlock_achievement("blackjack_master")
        if stats["blackjacks"] >= 25 and not self.has_achievement("blackjack_legend"):
            self.unlock_achievement("blackjack_legend")
        if stats["blackjacks"] >= 50 and not self.has_achievement("fifty_blackjacks"):
            self.unlock_achievement("fifty_blackjacks")
        
        if stats["best_win_streak"] >= 3 and not self.has_achievement("three_streak"):
            self.unlock_achievement("three_streak")
        if stats["best_win_streak"] >= 5 and not self.has_achievement("hot_streak"):
            self.unlock_achievement("hot_streak")
        if stats["best_win_streak"] >= 10 and not self.has_achievement("win_streak_10"):
            self.unlock_achievement("win_streak_10")
        
        if stats["biggest_win"] >= 1000 and not self.has_achievement("big_bet"):
            self.unlock_achievement("big_bet")
        if stats["biggest_win"] >= 10000 and not self.has_achievement("high_roller"):
            self.unlock_achievement("high_roller")
        if stats["biggest_win"] >= 50000 and not self.has_achievement("big_spender"):
            self.unlock_achievement("big_spender")
        
        if stats["wins"] >= 1 and not self.has_achievement("first_win"):
            self.unlock_achievement("first_win")
        
        # Companion achievements
        if len(self._companions) >= 1 and not self.has_achievement("first_friend"):
            self.unlock_achievement("first_friend")
        if len(self._companions) >= 3 and not self.has_achievement("animal_lover"):
            self.unlock_achievement("animal_lover")
        if len(self._companions) >= 5 and not self.has_achievement("max_companions"):
            self.unlock_achievement("max_companions")
        
        # NEW COLLECTION ACHIEVEMENTS
        if len(self._companions) >= 10 and not self.has_achievement("zookeeper"):
            self.unlock_achievement("zookeeper")
        if len(self._companions) >= 20 and not self.has_achievement("noahs_ark"):
            self.unlock_achievement("noahs_ark")
        
        # Health/Survival achievements
        if self._statistics["near_death_experiences"] >= 3 and not self.has_achievement("cheated_death"):
            self.unlock_achievement("cheated_death")
        if self._statistics["near_death_experiences"] >= 10 and not self.has_achievement("death_defier"):
            self.unlock_achievement("death_defier")
        
        if self._health <= 10 and self._alive and not self.has_achievement("clinging_to_life"):
            self.unlock_achievement("clinging_to_life")
        if self._health <= 5 and self._alive and not self.has_achievement("near_death_survivor"):
            self.unlock_achievement("near_death_survivor")
        
        if self._is_broken and not self.has_achievement("broken_but_alive"):
            self.unlock_achievement("broken_but_alive")
        
        # Social achievements
        if len(self._met) >= 20 and not self.has_achievement("social_butterfly"):
            self.unlock_achievement("social_butterfly")
        
        if self.has_met("Suzy") and not self.has_achievement("meet_suzy"):
            self.unlock_achievement("meet_suzy")
        
        # Item achievements
        if len(self._inventory) >= 1 and not self.has_achievement("first_item"):
            self.unlock_achievement("first_item")
        if len(self._inventory) >= 5 and not self.has_achievement("five_items"):
            self.unlock_achievement("five_items")
        if len(self._inventory) >= 10 and not self.has_achievement("collector"):
            self.unlock_achievement("collector")
        if len(self._inventory) >= 15 and not self.has_achievement("item_hoarder"):
            self.unlock_achievement("item_hoarder")
        if len(self._inventory) >= 20 and not self.has_achievement("master_collector"):
            self.unlock_achievement("master_collector")
        
        # Track highest balance
        if self._balance > self._statistics["highest_balance"]:
            self._statistics["highest_balance"] = self._balance
        if self._balance < self._statistics["lowest_balance"]:
            self._statistics["lowest_balance"] = self._balance
    
    def show_achievements(self):
        """Display all unlocked achievements"""
        print("\n")
        type.fast(yellow(bright("═══════════════════════════════════════")))
        print()
        type.fast(yellow(bright("         YOUR ACHIEVEMENTS             ")))
        print()
        type.fast(yellow(bright("═══════════════════════════════════════")))
        print()
        
        if len(self._achievements) == 0:
            type.type("You haven't unlocked any achievements yet.")
            print("\n")
            return
        
        for achievement_id in sorted(self._achievements):
            achievement_data = self._lists.get_achievement_data(achievement_id)
            if achievement_data:
                type.fast(yellow("★ ") + bright(achievement_data["name"]))
                print()
        
        total = self._lists.get_total_achievements()
        type.type(f"\nUnlocked: {len(self._achievements)}/{total}")
        print("\n")

    # ==========================================
    # STATISTICS TRACKING SYSTEM
    # ==========================================
    
    def increment_statistic(self, stat_name, value=1):
        """Increment a statistic by value"""
        if stat_name in self._statistics:
            self._statistics[stat_name] += value
    
    def get_statistic(self, stat_name):
        """Get a specific statistic"""
        return self._statistics.get(stat_name, 0)
    
    def show_statistics(self):
        """Display full statistics report"""
        stats = self._statistics
        g_stats = self._gambling_stats
        
        print("\n")
        type.fast(cyan(bright("═══════════════════════════════════════")))
        print()
        type.fast(cyan(bright("         YOUR JOURNEY SO FAR           ")))
        print()
        type.fast(cyan(bright("═══════════════════════════════════════")))
        print()
        
        type.fast(f"Days Survived: {bright(yellow(str(self._day)))}")
        print()
        type.fast(f"Current Balance: {green(bright('${:,}'.format(self._balance)))}")
        print()
        type.fast(f"Highest Balance: {green('${:,}'.format(stats['highest_balance']))}")
        print()
        type.fast(f"Lowest Balance: {red('${:,}'.format(stats['lowest_balance']))}")
        print()
        print()
        type.fast(f"Total Hands Played: {bright(str(g_stats['total_hands']))}")
        print()
        type.fast(f"Casino Visits: {str(stats['casino_visits'])}")
        print()
        type.fast(f"People Met: {str(stats['people_met'])}")
        print()
        type.fast(f"Items Collected: {str(stats['items_collected'])}")
        print()
        type.fast(f"Items Sold: {str(stats['items_sold'])}")
        print()
        print()
        type.fast(f"Injuries Sustained: {red(str(stats['injuries_sustained']))}")
        print()
        type.fast(f"Illnesses Contracted: {yellow(str(stats['illnesses_contracted']))}")
        print()
        type.fast(f"Near Death Experiences: {red(bright(str(stats['near_death_experiences'])))}")
        print()
        type.fast(f"Doctor Visits: {str(stats['doctor_visits'])}")
        print()
        type.fast(f"Mechanic Visits: {str(stats['mechanic_visits'])}")
        print()
        print()
        type.fast(f"Companions Befriended: {green(str(len(self._companions)))}")
        print()
        type.fast(f"Loans Taken: {str(stats['loans_taken'])}")
        print()
        type.fast(f"Times Robbed: {red(str(stats['times_robbed']))}")
        print("\n")

    # ==========================================
    # COMPANION SYSTEM
    # ==========================================
    
    def add_companion(self, name, companion_type):
        """Add a new companion"""
        if name not in self._companions:
            self._companions[name] = {
                "type": companion_type,
                "status": "alive",
                "happiness": 50,
                "days_owned": 0,
                "fed_today": False,
                "bonded": False
            }
            self._statistics["companions_befriended"] += 1
            type.type(f"You have befriended " + bright(magenta(name)) + "!")
            print("\n")
    
    def has_companion(self, name):
        """Check if player has a specific companion"""
        return name in self._companions and self._companions[name]["status"] == "alive"
    
    def get_companion(self, name):
        """Get companion data"""
        return self._companions.get(name, None)
    
    def get_all_companions(self):
        """Get all living companions"""
        return {name: data for name, data in self._companions.items() if data["status"] == "alive"}
    
    def feed_companion(self, name, food_item=None):
        """Feed a companion to increase happiness"""
        if name in self._companions and self._companions[name]["status"] == "alive":
            companion = self._companions[name]
            if not companion["fed_today"]:
                companion["fed_today"] = True
                happiness_gain = 10 if food_item else 5
                companion["happiness"] = min(100, companion["happiness"] + happiness_gain)
                return True
        return False
    
    def pet_companion(self, name):
        """Pet a companion for small happiness boost"""
        if name in self._companions and self._companions[name]["status"] == "alive":
            self._companions[name]["happiness"] = min(100, self._companions[name]["happiness"] + 3)
            return True
        return False
    
    def update_companions_daily(self):
        """Called each day to update companion states"""
        for name, companion in self._companions.items():
            if companion["status"] == "alive":
                companion["days_owned"] += 1
                
                # Reset daily feeding
                if not companion["fed_today"]:
                    # Hunger penalty
                    companion["happiness"] = max(0, companion["happiness"] - 5)
                companion["fed_today"] = False
                
                # Check for bonding (high happiness for extended time)
                if companion["happiness"] >= 80 and companion["days_owned"] >= 7:
                    if not companion["bonded"]:
                        companion["bonded"] = True
                        print()
                        type.type(bright(magenta(name)) + " has bonded with you! Your friendship is unbreakable.")
                        print("\n")
                
                # Check for running away (very low happiness)
                if companion["happiness"] <= 10:
                    if random.randrange(3) == 0:
                        companion["status"] = "lost"
                        print()
                        type.slow(red(name + " has run away. They were too unhappy to stay."))
                        print("\n")
                        self.lose_sanity(10)
    
    def companion_dies(self, name, cause="unknown"):
        """Mark a companion as dead"""
        if name in self._companions:
            self._companions[name]["status"] = "dead"
            print()
            type.slow(red(bright(name + " has died.")))
            print("\n")
            self.lose_sanity(20)
    
    def apply_companion_day_bonuses(self):
        """Apply passive companion bonuses during the day"""
        living = self.get_all_companions()
        if len(living) == 0:
            return
        
        for name, data in living.items():
            comp_type = self._lists.get_companion_type(name)
            if not comp_type:
                continue
            bonuses = comp_type.get("bonuses", {})
            
            # Sanity restore - all companions with this bonus give passive sanity
            sanity_val = bonuses.get("sanity_restore", 0)
            if sanity_val > 0 and data["happiness"] >= 50:
                # Only restore if companion is reasonably happy
                if random.randrange(3) == 0:  # 33% chance per day
                    self.restore_sanity(sanity_val)
            
            # Find money chance (Mr. Pecks)
            find_money = bonuses.get("find_money_chance", 0)
            if find_money > 0 and data["happiness"] >= 40:
                if random.randrange(100) < find_money:
                    amount = random.randint(1, 20)
                    print()
                    type.type(bright(name) + " drops some coins at your feet. " + green("+${:,}".format(amount)))
                    print()
                    self.change_balance(amount)
            
            # Steal chance (Rusty)
            steal_val = bonuses.get("steal_chance", 0)
            if steal_val > 0 and data["happiness"] >= 50:
                if random.randrange(100) < steal_val:
                    amount = random.randint(2, 15)
                    print()
                    type.type(bright(name) + " drops something shiny in your lap. " + green("+${:,}".format(amount)))
                    print()
                    self.change_balance(amount)
            
            # Luck bonus (Hopper, Squirrelly) - small chance of finding extra money
            luck_val = bonuses.get("luck_bonus", 0)
            if luck_val > 0 and data["happiness"] >= 50:
                if random.randrange(100) < luck_val:
                    amount = random.randint(5, 25)
                    print()
                    type.type("Feeling lucky today... found " + green("+${:,}".format(amount)) + " on the ground!")
                    print()
                    self.change_balance(amount)
        
        # Show a random companion dialogue (small chance)
        if random.randrange(5) == 0 and len(living) > 0:
            name = random.choice(list(living.keys()))
            data = living[name]
            if data["happiness"] >= 70:
                mood = "bonded" if data.get("bonded") else "happy"
            elif data["happiness"] >= 40:
                mood = "neutral"
            else:
                mood = "sad"
            dialogue = self._lists.get_companion_dialogue(name, mood)
            if dialogue:
                print()
                type.type(cyan(dialogue))
                print()
    
    def apply_companion_night_bonuses(self):
        """Apply passive companion bonuses during the night"""
        living = self.get_all_companions()
        if len(living) == 0:
            return
        
        for name, data in living.items():
            comp_type = self._lists.get_companion_type(name)
            if not comp_type:
                continue
            bonuses = comp_type.get("bonuses", {})
            
            # Night bonus (Patches) - extra sanity at night, less fatigue
            if bonuses.get("night_bonus") and data["happiness"] >= 50:
                if random.randrange(3) == 0:
                    print()
                    type.type(cyan(bright(name) + " keeps watch while you rest. You feel safer."))
                    print()
                    self.restore_sanity(3)
                    self.add_fatigue(-1)  # Slightly less tired with a night guard
    
    def show_companions(self):
        """Display all companions"""
        living = self.get_all_companions()
        
        print("\n")
        type.fast(magenta(bright("═══════════════════════════════════════")))
        print()
        type.fast(magenta(bright("         YOUR COMPANIONS               ")))
        print()
        type.fast(magenta(bright("═══════════════════════════════════════")))
        print()
        
        if len(living) == 0:
            type.type("You have no companions. The road is lonely.")
            print("\n")
            return
        
        for name, data in living.items():
            happiness_color = green if data["happiness"] >= 70 else (yellow if data["happiness"] >= 40 else red)
            bonded_str = " ♥" if data["bonded"] else ""
            type.fast(f"{bright(name)}{bonded_str} ({data['type']})")
            print()
            type.fast(f"  Happiness: {happiness_color(str(data['happiness']) + '%')}")
            print()
            type.fast(f"  Days Together: {data['days_owned']}")
            print()
        print()
    
    def companion_afternoon_dialogue(self):
        """Interactive afternoon dialogue with all companions"""
        living_companions = self.get_all_companions()
        
        if len(living_companions) == 0:
            type.type("You have no companions to spend time with.")
            print("\n")
            self.start_night()
            return
        
        type.type(cyan(bright("═══ AFTERNOON WITH YOUR COMPANIONS ═══")))
        print("\n")
        
        # List all companions
        companion_names = list(living_companions.keys())
        for i, name in enumerate(companion_names, 1):
            companion = living_companions[name]
            happiness_indicator = "♥" if companion["happiness"] >= 80 else ("~" if companion["happiness"] >= 50 else "...")
            type.type(f"{i}. {bright(name)} ({companion['type']}) {happiness_indicator}")
        
        type.type(f"{len(companion_names) + 1}. Spend time with all of them")
        type.type(f"{len(companion_names) + 2}. Skip and head out")
        print("\n")
        
        choice = input("Who do you want to interact with? ").strip()
        
        try:
            choice_num = int(choice)
            if choice_num == len(companion_names) + 2:
                type.type("You wave goodbye to your companions and head out.")
                print("\n")
                self.start_night()
                return
            elif choice_num == len(companion_names) + 1:
                # Group activity
                type.type("You gather all your companions together. This is... quite a sight.")
                print("\n")
                if len(companion_names) >= 10:
                    type.type("You've basically got a zoo at this point. A traveling menagerie. A Disney Princess situation.")
                elif len(companion_names) >= 5:
                    type.type("The Noah's Ark energy is strong. You're collecting two of everything at this rate.")
                else:
                    type.type("Your little found family settles around you. Each one chose you. That means something.")
                print("\n")
                
                # Feed everyone
                type.type("You share what food you have. It's not much, but it's enough.")
                for name in companion_names:
                    self.feed_companion(name)
                    self.pet_companion(name)
                
                self.restore_sanity(10)
                self.heal(15)
                
                type.type("You spend the afternoon together - a strange, beautiful collection of souls. ")
                type.type("For a little while, you're not just a gambler on the run. You're someone who matters to others.")
                print("\n")
                
                # Check for collection achievements
                self.check_companion_achievements()
                
            elif 1 <= choice_num <= len(companion_names):
                name = companion_names[choice_num - 1]
                self.interact_with_companion(name)
            else:
                type.type("Not a valid choice.")
                print("\n")
        except:
            type.type("Not a valid choice.")
            print("\n")
        
        self.start_night()
    
    def interact_with_companion(self, name):
        """Detailed interaction with a specific companion"""
        companion = self.get_companion(name)
        if not companion:
            return
        
        type.type(f"You spend time with {cyan(bright(name))} the {companion['type']}.")
        print("\n")
        
        # Companion-specific dialogue
        companion_type = companion['type']
        happiness = companion['happiness']
        
        # Unique dialogue for each companion type
        if name == "Whiskers":
            if happiness >= 70:
                type.type("Whiskers purrs loudly and kneads your lap with their paws. They've chosen you as their human.")
            else:
                type.type("Whiskers sits just out of reach, tail swishing. Feed me, human.")
        
        elif name == "Lucky":
            if happiness >= 70:
                type.type("Lucky's tail wags so hard his whole body shakes. Despite having three legs, he spins in circles of pure joy.")
            else:
                type.type("Lucky limps over and whines softly. He's hungry.")
        
        elif name == "Chomper":
            if happiness >= 70:
                type.type("Chomper does that thing alligators do where they just float with their eyes above water, watching you protectively.")
                type.type("It should be creepy but it's... kind of sweet?")
            else:
                type.type("Chomper snaps their jaws once. Feed. Me. Now.")
        
        elif name == "Grace":
            if happiness >= 70:
                type.type("Grace and her fawns approach. She nuzzles your hand while the babies play around your feet.")
                type.type("This is the most peaceful you've felt in weeks.")
                self.restore_sanity(5)
            else:
                type.type("Grace keeps her distance, watchful. The fawns stay close to her.")
        
        elif name == "Bruno" or name == "Ursus":
            if happiness >= 70:
                type.type("The massive bear sits down next to you, close enough that you can feel the warmth radiating from their fur.")
                type.type("You lean against them. They let you. You're protected.")
            else:
                type.type("The bear grunts and huffs. Not aggressive, but not friendly either. Bears need food.")
        
        elif name == "Squawk":
            if happiness >= 70:
                type.type("FRIEND! FRIEND! MINE! Squawk lands on your head and makes happy seagull noises.")
                type.type("It's annoying. You love it.")
            else:
                type.type("FOOD! FOOD! MINE! Squawk pecks at your pockets demandingly.")
        
        elif name == "Deathclaw":
            if happiness >= 70:
                type.type("Deathclaw does a little sideways victory dance. For a crab, it's surprisingly endearing.")
            else:
                type.type("Deathclaw waves their pincers aggressively. Feed crab. Crab hungry.")
        
        elif name == "Speedy":
            if happiness >= 70:
                type.type("Speedy extends their head from their shell and makes a tiny satisfied squeak.")
                type.type("You pet their shell. They close their eyes contentedly. Time moves slower with tortoises. That's okay.")
            else:
                type.type("Speedy retreats into their shell. You'll have to earn their trust back.")
        
        elif name == "Noodle":
            if happiness >= 70:
                type.type("Noodle coils around your arm and flicks their tongue against your cheek. Snake kisses.")
            else:
                type.type("Noodle hisses softly. Not a threat, but a complaint. Hungry snake is grumpy snake.")
        
        elif name == "Squirrelly":
            if happiness >= 70:
                type.type("Squirrelly chitters excitedly and presents you with an acorn they found. It's a gift.")
                type.type("You pocket it solemnly. This is valuable squirrel currency.")
            else:
                type.type("Squirrelly throws an acorn at your head. Pay attention to me!")
        
        elif name == "Don Coo" or name == "General Quackers":
            if happiness >= 70:
                type.type(f"{name} struts proudly and gives you a respectful salute/bow.")
                type.type("You're the boss. They're the lieutenant. This is how it works.")
            else:
                type.type(f"{name} makes disapproving bird noises. The troops are restless. You need to lead better.")
        
        elif name == "Thunder":
            if happiness >= 70:
                type.type("Thunder nuzzles your shoulder and makes that soft horse sound - a nicker.")
                type.type("You run your hands through their mane. This is a bond that transcends words.")
            else:
                type.type("Thunder stamps their hooves and tosses their head. Horses need care, human.")
        
        elif name == "Betsy":
            if happiness >= 70:
                type.type("Betsy moos contentedly and lets you lean against her warm flank.")
                type.type("She smells like grass and sunshine. It's nice.")
            else:
                type.type("Betsy moos insistently and stares at your wallet. Old habits die hard.")
        
        elif name == "Scooter":
            if happiness >= 70:
                type.type("Scooter floats on their back and makes happy chirping noises while doing little flips.")
                type.type("Otters are the happiest creatures on earth and you'll fight anyone who says otherwise.")
            else:
                type.type("Scooter makes grumpy otter sounds and splashes water at you. Rude.")
        
        elif name == "Kraken":
            if happiness >= 70:
                type.type("A massive tentacle emerges from nearby water and gently pats your head.")
                type.type("You have befriended something ancient and terrible and it's... nice?")
                self.restore_sanity(8)
            else:
                type.type("You sense the Kraken's displeasure from the deep. Best not to anger a legend.")
        
        elif name == "Shellbert":
            if happiness >= 70:
                type.type("Shellbert extends their ancient head and gazes at you with wise, patient eyes.")
                type.type("In that moment, you understand: everything will be okay. Maybe not today. But eventually.")
                self.restore_sanity(6)
            else:
                type.type("Shellbert withdraws into their shell. Even ancient wisdom needs sustenance.")
        
        elif name == "Moonwhisker":
            if happiness >= 70:
                type.type("Moonwhisker hops in a circle around you, leaving glowing pawprints that fade after a few seconds.")
                type.type("The magical rabbit nuzzles your hand. You feel... blessed? Enchanted? Something good.")
                self.restore_sanity(7)
            else:
                type.type("Moonwhisker's glow is dim. Even magical creatures need care.")
        
        elif name == "Bubbles":
            if happiness >= 70:
                type.type("Bubbles swims in lazy circles in their bowl, scales shimmering like liquid gold.")
                type.type("Watching them is meditative. Peaceful. The world slows down.")
                self.restore_sanity(4)
            else:
                type.type("Bubbles floats at the bottom of the bowl, looking sad. Fish can look sad. Trust you.")
        
        elif name == "Hopper":
            if happiness >= 70:
                type.type("Hopper does little bunny binkies - those joyful jumps rabbits do when they're happy.")
                type.type("Their nose twitches. You boop it. Life is good.")
                self.restore_sanity(5)
            else:
                type.type("Hopper thumps their back leg - rabbit language for 'I'm displeased.' Point taken.")
        
        elif name == "Don":
            if happiness >= 70:
                type.type("Don the Raccoon Boss chitters approvingly and hands you a shiny bottlecap as tribute.")
                type.type("In raccoon culture, this is the highest honor. You're basically family now.")
                self.restore_sanity(6)
            else:
                type.type("Don crosses his little arms and chatters angrily. The mafia is not pleased.")
        
        elif name == "Echo":
            if happiness >= 70:
                type.type("Echo leaps from nearby water (how is there always water nearby?) and chirps happily.")
                type.type("Dolphins are possibly the smartest creatures on Earth. Echo knows exactly how much you needed this.")
                self.restore_sanity(10)
                self.heal(10)
            else:
                type.type("Echo's clicks sound... disappointed? Can dolphins be disappointed? Yes. Yes they can.")
        
        elif name == "Patches":
            if happiness >= 70:
                type.type("Patches waddles over and doesn't play dead. This is the highest form of trust for an opossum.")
                type.type("They climb onto your lap and make a weird purring sound. You feel blessed.")
                self.restore_sanity(5)
            else:
                type.type("Patches immediately plays dead. You're not fooled but it still hurts.")
        
        else:
            # Generic dialogue for any other companions
            if happiness >= 70:
                type.type(f"{name} seems genuinely happy to see you. The feeling is mutual.")
            else:
                type.type(f"{name} seems hungry and a bit distant. You should take better care of them.")
        
        print("\n")
        
        # Interaction options
        type.type("What would you like to do?")
        type.type("1. Feed them")
        type.type("2. Pet/Play with them")
        type.type("3. Just sit together")
        type.type("4. Leave them be")
        print("\n")
        
        action = input("Choose: ").strip()
        
        if action == "1":
            if self.feed_companion(name):
                type.type(f"You share your food with {name}. They eat happily.")
                self.heal(5)
            else:
                type.type(f"You've already fed {name} today. They're content.")
        elif action == "2":
            self.pet_companion(name)
            type.type(f"You spend time playing with {name}. Simple moments like these make life worth living.")
            self.restore_sanity(3)
        elif action == "3":
            type.type(f"You sit in comfortable silence with {name}. Sometimes that's enough.")
            self.restore_sanity(5)
            self.heal(10)
        else:
            type.type(f"You give {name} space. They understand.")
        
        print("\n")
    
    def check_companion_achievements(self):
        """Check and unlock companion collection achievements"""
        companions = self.get_all_companions()
        num_companions = len(companions)
        
        # Zookeeper (10 companions)
        if num_companions >= 10 and not self.has_achievement("zookeeper"):
            self.unlock_achievement("zookeeper")
            type.type(cyan(bright("🏆 ACHIEVEMENT UNLOCKED: Zookeeper - 10 companions!")))
            print("\n")
        
        # Noah's Ark (20 companions)
        if num_companions >= 20 and not self.has_achievement("noahs_ark"):
            self.unlock_achievement("noahs_ark")
            type.type(cyan(bright("🏆 EPIC ACHIEVEMENT: Noah's Ark - 20 companions!")))
            type.type("You're basically running an ark at this point. Where's the flood?")
            print("\n")
        
        # Check for themed achievements
        water_animals = ["Chomper", "Scooter", "Kraken", "Shellbert", "Deathclaw"]
        forest_animals = ["Grace", "Bruno", "Ursus", "Noodle", "Squirrelly"]
        
        # Marine Biologist (all water animals)
        water_count = sum(1 for name in water_animals if self.has_companion(name))
        if water_count >= len(water_animals) and not self.has_achievement("marine_biologist"):
            self.unlock_achievement("marine_biologist")
            type.type(cyan(bright("🏆 EPIC ACHIEVEMENT: Marine Biologist - All water creatures!")))
            print("\n")
        
        # Disney Princess (all forest animals)
        forest_count = sum(1 for name in forest_animals if self.has_companion(name))
        if forest_count >= len(forest_animals) and not self.has_achievement("disney_princess"):
            self.unlock_achievement("disney_princess")
            type.type(cyan(bright("🏆 EPIC ACHIEVEMENT: Disney Princess - All forest creatures!")))
            type.type("Birds land on your shoulders. Deer follow you. Squirrels present you with acorns. This is your life now.")
            print("\n")

    # ==========================================
    # LOAN SHARK SYSTEM
    # ==========================================
    
    def get_loan_shark_debt(self):
        return self._loan_shark_debt
    
    def take_loan(self, amount):
        """Take a loan from the loan shark - gives FRAUDULENT cash"""
        self._loan_shark_debt += amount
        self.add_fraudulent_cash(amount)
        self._loan_shark_days_overdue = 0
        self._statistics["loans_taken"] += 1
        type.type("Vinnie hands you " + yellow(bright("${:,}".format(amount))) + " in cash.")
        print()
        type.type("It feels... off. The bills are too smooth. Too perfect.")
        print()
        type.type(quote("Don't worry about it. Money is money. Just don't let anyone look too close."))
        print()
        type.type(quote("Gamble with it. Blend it in with your real cash. No one will know the difference."))
        print()
        type.type(quote("Oh, and the interest is 20% per week. Don't be late."))
        print("\n")
    
    def repay_loan(self, amount):
        """Repay part or all of the loan"""
        if amount >= self._loan_shark_debt:
            amount = self._loan_shark_debt
            self._loan_shark_debt = 0
            self._loan_shark_days_overdue = 0
            self._loan_shark_warning_level = 0
            self._statistics["loans_repaid"] += 1
            self._balance -= amount
            type.type("You've paid off your debt completely. Vinnie seems almost disappointed.")
            print("\n")
        else:
            self._loan_shark_debt -= amount
            self._balance -= amount
            type.type("You pay " + green(bright("${:,}".format(amount))) + ". ")
            type.type("You still owe " + red(bright("${:,}".format(self._loan_shark_debt))) + ".")
            print("\n")
    
    def update_loan_shark_daily(self):
        """Called each day to update loan shark status"""
        if self._loan_shark_debt <= 0:
            return
        
        self._loan_shark_days_overdue += 1
        
        # Add interest every 7 days
        if self._loan_shark_days_overdue % 7 == 0:
            interest = int(self._loan_shark_debt * 0.20)
            self._loan_shark_debt += interest
            print()
            type.type(red("Interest accrued on your loan: ") + red(bright("${:,}".format(interest))))
            print()
            type.type("You now owe Vinnie " + red(bright("${:,}".format(self._loan_shark_debt))) + ".")
            print("\n")
        
        # Escalate warnings
        if self._loan_shark_days_overdue >= 21 and self._loan_shark_warning_level < 4:
            self._loan_shark_warning_level = 4  # Death threat territory
        elif self._loan_shark_days_overdue >= 14 and self._loan_shark_warning_level < 3:
            self._loan_shark_warning_level = 3  # Violence
        elif self._loan_shark_days_overdue >= 7 and self._loan_shark_warning_level < 2:
            self._loan_shark_warning_level = 2  # Threat
        elif self._loan_shark_days_overdue >= 3 and self._loan_shark_warning_level < 1:
            self._loan_shark_warning_level = 1  # Warning
    
    def get_loan_shark_warning_level(self):
        return self._loan_shark_warning_level
    
    def check_loan_shark_event(self):
        """Check if a loan shark event should trigger"""
        if self._loan_shark_debt <= 0:
            return False
        
        # Higher warning level = higher chance of event
        if self._loan_shark_warning_level >= 4:
            return random.randrange(3) == 0  # 33% chance
        elif self._loan_shark_warning_level >= 3:
            return random.randrange(5) == 0  # 20% chance
        elif self._loan_shark_warning_level >= 2:
            return random.randrange(7) == 0  # 14% chance
        elif self._loan_shark_warning_level >= 1:
            return random.randrange(10) == 0  # 10% chance
        return False

    # ==========================================
    # PAWN SHOP SYSTEM
    # ==========================================
    
    def get_pawn_reputation(self):
        return self._pawn_shop_reputation
    
    def change_pawn_reputation(self, value):
        self._pawn_shop_reputation = max(0, min(100, self._pawn_shop_reputation + value))
    
    def get_pawn_price_modifier(self):
        """Get price modifier based on reputation (0.5 to 1.2)"""
        return 0.5 + (self._pawn_shop_reputation / 200)
    
    # ==========================================
    # FRAUDULENT CASH SYSTEM (Loan Shark)
    # ==========================================
    
    def get_fraudulent_cash(self):
        return self._fraudulent_cash
    
    def add_fraudulent_cash(self, amount):
        """Add fake money from loan shark"""
        self._fraudulent_cash += amount
    
    def blend_fraudulent_cash(self, amount):
        """Convert fake cash to real through gambling - track what Dealer gets"""
        if amount > self._fraudulent_cash:
            amount = self._fraudulent_cash
        self._fraudulent_cash -= amount
        self._dealer_fake_cash_total += amount
        return amount
    
    def get_dealer_fake_cash_total(self):
        return self._dealer_fake_cash_total
    
    def has_too_much_fake_cash(self):
        """Dealer stops gaining happiness if he has too much fake money - threshold based on rank"""
        # Lower ranks: Higher threshold (Dealer isn't sophisticated, doesn't notice)
        # Higher ranks: Lower threshold (Dealer is sharp, notices fake cash quickly)
        thresholds = {
            0: 50000,    # Poor - Dealer doesn't care much, it's all pennies to him
            1: 30000,    # Modest - Still fairly lenient
            2: 15000,    # Well-off - Starting to scrutinize
            3: 5000,     # Rich - Very attentive to larger sums
            4: 2000,     # Very Rich - Expert eye, notices quickly
            5: 500       # Almost Millionaire - Dealer VERY suspicious of high roller money
        }
        threshold = thresholds.get(self._rank, 15000)
        return self._dealer_fake_cash_total >= threshold
    
    # ==========================================
    # DEALER HAPPINESS SYSTEM
    # ==========================================
    
    def get_dealer_happiness(self):
        return self._dealer_happiness
    
    def change_dealer_happiness(self, amount):
        """Change dealer happiness (0-100)"""
        self._dealer_happiness = max(0, min(100, self._dealer_happiness + amount))
        if self._dealer_happiness <= 0:
            self.dealer_kills_you()
    
    def dealer_kills_you(self):
        """Dealer has had enough and kills you"""
        print("\n")
        type.slow(red(bright("═" * 50)))
        type.slow(red(bright("           THE DEALER'S JUDGMENT")))
        type.slow(red(bright("═" * 50)))
        print("\n")
        time.sleep(1)
        type.slow("The Dealer sets down the cards. Slowly. Deliberately.")
        print("\n")
        type.slow(red("\"Enough.\""))
        print("\n")
        type.slow("His jade eye catches the dim casino light. It doesn't blink.")
        print("\n")
        type.slow(red("\"You've tested my patience for the last time.\""))
        print("\n")
        time.sleep(2)
        type.slow("You try to stand. To leave. To run.")
        print("\n")
        type.slow("Your legs won't move.")
        print("\n")
        type.slow(red("\"The game is over. YOU are over.\""))
        print("\n")
        time.sleep(2)
        type.slow("The last thing you see is his hand reaching across the table.")
        print("\n")
        type.slow("Then darkness.")
        print("\n")
        type.slow("Then nothing.")
        print("\n")
        time.sleep(2)
        type.slow(red(bright("The Dealer does not forgive. The Dealer does not forget.")))
        print("\n")
        self.kill("The Dealer's wrath")
    
    # ==========================================
    # GIFT WRAPPING SYSTEM (Kyle's Store)
    # ==========================================
    
    def increment_store_purchases(self):
        self._convenience_store_purchases += 1
        # Unlock gift system after 3-5 purchases AND out of poor rank
        if not self._gift_system_unlocked:
            if self._convenience_store_purchases >= random.randint(3, 5) and self._rank >= 1:
                self._gift_system_unlocked = True
                return True  # Signal to show Kyle's dialogue
        return False
    
    def is_gift_system_unlocked(self):
        return self._gift_system_unlocked
    
    def has_gift_wrapped(self):
        return self._gift_wrapped_item is not None
    
    def wrap_item_as_gift(self, item_name, wrap_cost=10):
        """Wrap an item as a gift for the Dealer"""
        if self._gift_wrapped_item is not None:
            return False  # Already have a gift
        if not self.has_item(item_name):
            return False
        if self._balance < wrap_cost:
            return False
        
        self.use_item(item_name)
        self._gift_wrapped_item = item_name
        self._balance -= wrap_cost
        return True
    
    def get_wrapped_gift(self):
        return self._gift_wrapped_item
    
    def clear_wrapped_gift(self):
        self._gift_wrapped_item = None
    
    def deliver_gift_to_dealer(self):
        """Automatically deliver wrapped gift to Dealer at casino"""
        if not self._gift_wrapped_item:
            return
        
        item = self._gift_wrapped_item
        self._gift_wrapped_item = None
        
        print("\n")
        type.slow("You approach the table with a wrapped package.")
        print("\n")
        type.slow("The Dealer's jade eye fixes on it.")
        print("\n")
        type.slow(red("\"What is this?\""))
        print("\n")
        type.type("You slide the gift across the table.")
        print("\n")
        time.sleep(1)
        
        # Get reaction from lists.py
        reaction_data = self._lists.get_dealer_gift_reaction(item)
        
        # Display unwrapping
        type.slow("He unwraps it slowly. Deliberately.")
        print("\n")
        time.sleep(1)
        
        # Display the reveal
        type.slow(f"Inside: " + bright(yellow(item)))
        print("\n")
        time.sleep(1)
        
        # Display dealer reaction
        for line in reaction_data["dialogue"]:
            type.slow(red(line))
            print("\n")
            time.sleep(0.5)
        
        # Apply happiness change
        happiness_change = reaction_data["happiness"]
        if happiness_change != 0:
            self.change_dealer_happiness(happiness_change)
            if happiness_change > 0:
                type.slow(green(f"The Dealer seems... pleased? (Happiness +{happiness_change})"))
            else:
                type.slow(red(f"The Dealer does NOT look happy. (Happiness {happiness_change})"))
            print("\n")
        
        # Check if gift causes death
        if reaction_data.get("kills_you", False):
            time.sleep(2)
            type.slow(red(bright("His hand moves faster than you can see.")))
            print("\n")
            self.kill(f"The Dealer's reaction to {item}")
    

