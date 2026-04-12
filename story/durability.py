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

class DurabilityMixin:
    """Durability: All item/flask durability update methods, item descriptions"""

    def update_no_bust_durability(self, invincible=False):
        if (self.has_flask_effect("No Bust")):
            if invincible:
                self._flask_durability[0] = -1
            
            if (self._flask_durability[0] > 0):
                if not (self.has_item("Frank's Flask") and random.randrange(3) == 0):
                    self._flask_durability[0] -= random.choice([1, 2])
                if self._flask_durability[0] <= 0:
                    self._flask_durability[0] = 0
                    self.remove_flask_effect("No Bust")
                    print()
                    type.slow(red(bright("Your Flask of No Bust effect ran out!")))

            # Sets durability when you get the item, or if the item is fixed
            if (self._flask_durability[0] == 0):
                self._flask_durability[0] = 4

    def update_delight_indicator_durability(self, invincible=False):
        has_base = self.has_item("Delight Indicator")
        has_upgrade = self.has_item("Delight Manipulator")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[0] = -1
                
            if (self._item_durability[0] > 0):
                self._item_durability[0] -= random.choice([1, 2, 3, 5])
                if self._item_durability[0] <= 0:
                    self._item_durability[0] = 0
                    if has_upgrade:
                        self.break_item("Delight Manipulator")
                        type.slow(red(bright("Your Delight Manipulator malfunctioned!")))
                    else:
                        self.break_item("Delight Indicator")
                        type.slow(red(bright("Your Delight Indicator broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[0] == 0):
                self._item_durability[0] = 45 if has_base else 70  # Manipulator lasts longer


    def update_health_indicator_durability(self, invincible=False):
        has_base = self.has_item("Health Indicator")
        has_upgrade = self.has_item("Health Manipulator")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[1] = -1
                
            if (self._item_durability[1] > 0):
                self._item_durability[1] -= random.choice([1, 2, 3, 5])
                if self._item_durability[1] <= 0:
                    self._item_durability[1] = 0
                    if has_upgrade:
                        self.break_item("Health Manipulator")
                        type.slow(red(bright("Your Health Manipulator short-circuited!")))
                    else:
                        self.break_item("Health Indicator")
                        type.slow(red(bright("Your Health Indicator broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[1] == 0):
                self._item_durability[1] = 30 if has_base else 50  # Manipulator lasts longer


    def update_dirty_old_hat_durability(self, invincible=False):
        has_base = self.has_item("Dirty Old Hat")
        has_upgrade = self.has_item("Unwashed Hair")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[2] = -1
                
            if (self._item_durability[2] > 0):
                self._item_durability[2] -= random.choice([1, 2, 3, 5])
                if self._item_durability[2] <= 0:
                    self._item_durability[2] = 0
                    if has_upgrade:
                        self.break_item("Unwashed Hair")
                        type.slow(red(bright("Your Unwashed Hair... somehow became clean?!")))
                    else:
                        self.break_item("Dirty Old Hat")
                        type.slow(red(bright("Your Dirty Old Hat broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[2] == 0):
                self._item_durability[2] = 25 if has_base else 40  # Unwashed Hair lasts longer


    def update_golden_watch_durability(self, invincible=False):
        has_base = self.has_item("Golden Watch")
        has_upgrade = self.has_item("Sapphire Watch")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[3] = -1
                
            if (self._item_durability[3] > 0):
                self._item_durability[3] -= random.choice([1, 2, 3, 5])
                if self._item_durability[3] <= 0:
                    self._item_durability[3] = 0
                    if has_upgrade:
                        self.break_item("Sapphire Watch")
                        type.slow(red(bright("Your Sapphire Watch cracked!")))
                    else:
                        self.break_item("Golden Watch")
                        type.slow(red(bright("Your Golden Watch broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[3] == 0):
                self._item_durability[3] = 20 if has_base else 35  # Sapphire Watch lasts longer


    def update_sneaky_peeky_glasses_durability(self, invincible=False):
        # Works for both base (Shades) and upgraded (Goggles) versions
        has_shades = self.has_item("Sneaky Peeky Shades")
        has_goggles = self.has_item("Sneaky Peeky Goggles")
        
        if has_shades or has_goggles:
            if invincible:
                self._item_durability[5] = -1

            if (self._item_durability[5] > 0):
                self._item_durability[5] -= random.choice([1, 2, 3, 5])
                if self._item_durability[5] <= 0:
                    self._item_durability[5] = 0
                    if has_goggles:
                        self.break_item("Sneaky Peeky Goggles")
                        type.slow(red(bright("Your Sneaky Peeky Goggles broke!")))
                    else:
                        self.break_item("Sneaky Peeky Shades")
                        type.slow(red(bright("Your Sneaky Peeky Shades broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[5] == 0):
                self._item_durability[5] = 15 if has_shades else 25  # Goggles last longer


    def update_quiet_sneakers_durability(self, invincible=False):
        has_base = self.has_item("Quiet Sneakers")
        has_upgrade = self.has_item("Quiet Bunny Slippers")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[6] = -1

            if (self._item_durability[6] > 0):
                self._item_durability[6] -= random.choice([1, 2, 3, 5])
                if self._item_durability[6] <= 0:
                    self._item_durability[6] = 0
                    if has_upgrade:
                        self.break_item("Quiet Bunny Slippers")
                        type.slow(red(bright("Your Quiet Bunny Slippers fell apart!")))
                    else:
                        self.break_item("Quiet Sneakers")
                        type.slow(red(bright("Your Quiet Sneakers broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[6] == 0):
                self._item_durability[6] = 15 if has_base else 25  # Bunny Slippers last longer


    def update_faulty_insurance_durability(self, invincible=False):
        has_base = self.has_item("Faulty Insurance")
        has_upgrade = self.has_item("Real Insurance")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[7] = -1
                
            if (self._item_durability[7] > 0):
                self._item_durability[7] -= random.choice([1, 2, 3, 5])
                if self._item_durability[7] <= 0:
                    self._item_durability[7] = 0
                    if has_upgrade:
                        self.break_item("Real Insurance")
                        type.slow(red(bright("Your Real Insurance policy expired!")))
                    else:
                        self.break_item("Faulty Insurance")
                        type.slow(red(bright("Your Faulty Insurance broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[7] == 0):
                self._item_durability[7] = 15 if has_base else 30  # Real Insurance lasts longer


    def update_lucky_coin_durability(self, invincible=False):
        has_base = self.has_item("Lucky Coin")
        has_upgrade = self.has_item("Lucky Medallion")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[8] = -1
                
            if (self._item_durability[8] > 0):
                self._item_durability[8] -= random.choice([1, 2, 3, 5])
                if self._item_durability[8] <= 0:
                    self._item_durability[8] = 0
                    if has_upgrade:
                        self.break_item("Lucky Medallion")
                        type.slow(red(bright("Your Lucky Medallion lost its shine!")))
                    else:
                        self.break_item("Lucky Coin")
                        type.slow(red(bright("Your Lucky Coin broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[8] == 0):
                self._item_durability[8] = 20 if has_base else 35  # Lucky Medallion lasts longer


    def update_worn_gloves_durability(self, invincible=False):
        has_base = self.has_item("Worn Gloves")
        has_upgrade = self.has_item("Velvet Gloves")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[9] = -1
                
            if (self._item_durability[9] > 0):
                self._item_durability[9] -= random.choice([1, 2, 3, 5])
                if self._item_durability[9] <= 0:
                    self._item_durability[9] = 0
                    if has_upgrade:
                        self.break_item("Velvet Gloves")
                        type.slow(red(bright("Your Velvet Gloves got stained beyond repair!")))
                    else:
                        self.break_item("Worn Gloves")
                        type.slow(red(bright("Your Worn Gloves broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[9] == 0):
                self._item_durability[9] = 25 if has_base else 40  # Velvet Gloves last longer


    def update_tattered_cloak_durability(self, invincible=False):
        has_base = self.has_item("Tattered Cloak")
        has_upgrade = self.has_item("Invisible Cloak")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[10] = -1
                
            if (self._item_durability[10] > 0):
                self._item_durability[10] -= random.choice([1, 2, 3, 5])
                if self._item_durability[10] <= 0:
                    self._item_durability[10] = 0
                    if has_upgrade:
                        self.break_item("Invisible Cloak")
                        type.slow(red(bright("Your Invisible Cloak became visible... and then vanished!")))
                    else:
                        self.break_item("Tattered Cloak")
                        type.slow(red(bright("Your Tattered Cloak broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[10] == 0):
                self._item_durability[10] = 18 if has_base else 30  # Invisible Cloak lasts longer


    def update_rusty_compass_durability(self, invincible=False):
        has_base = self.has_item("Rusty Compass")
        has_upgrade = self.has_item("Golden Compass")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[11] = -1
                
            if (self._item_durability[11] > 0):
                self._item_durability[11] -= random.choice([1, 2, 3, 5])
                if self._item_durability[11] <= 0:
                    self._item_durability[11] = 0
                    if has_upgrade:
                        self.break_item("Golden Compass")
                        type.slow(red(bright("Your Golden Compass lost its way!")))
                    else:
                        self.break_item("Rusty Compass")
                        type.slow(red(bright("Your Rusty Compass broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[11] == 0):
                self._item_durability[11] = 22 if has_base else 35  # Golden Compass lasts longer


    def update_pocket_watch_durability(self, invincible=False):
        has_base = self.has_item("Pocket Watch")
        has_upgrade = self.has_item("Grandfather Clock")
        
        if has_base or has_upgrade:
            if invincible:
                self._item_durability[12] = -1
                
            if (self._item_durability[12] > 0):
                self._item_durability[12] -= random.choice([1, 2, 3, 5])
                if self._item_durability[12] <= 0:
                    self._item_durability[12] = 0
                    if has_upgrade:
                        self.break_item("Grandfather Clock")
                        type.slow(red(bright("Your Grandfather Clock stopped ticking!")))
                    else:
                        self.break_item("Pocket Watch")
                        type.slow(red(bright("Your Pocket Watch broke!")))
                    print()

            # Sets durability when you get the item, or if the item is fixed
            if (self._item_durability[12] == 0):
                self._item_durability[12] = 15 if has_base else 25  # Grandfather Clock lasts longer


    def update_second_chance_durability(self, invincible=False):
        if (self.has_flask_effect("Second Chance")):
            if invincible:
                self._flask_durability[8] = -1
                
            if (self._flask_durability[8] > 0):
                if not (self.has_item("Frank's Flask") and random.randrange(3) == 0):
                    self._flask_durability[8] -= random.choice([1, 2])
                if self._flask_durability[8] <= 0:
                    self._flask_durability[8] = 0
                    self.remove_flask_effect("Second Chance")
                    print()
                    type.slow(red(bright("Your Flask of Second Chance effect ran out!")))

            # Sets durability when you get the item
            if (self._flask_durability[8] == 0):
                self._flask_durability[8] = 4


    def update_split_serum_durability(self, invincible=False):
        if (self.has_flask_effect("Split Serum")):
            if invincible:
                self._flask_durability[9] = -1
                
            if (self._flask_durability[9] > 0):
                if not (self.has_item("Frank's Flask") and random.randrange(3) == 0):
                    self._flask_durability[9] -= random.choice([1, 2])
                if self._flask_durability[9] <= 0:
                    self._flask_durability[9] = 0
                    self.remove_flask_effect("Split Serum")
                    print()
                    type.slow(red(bright("Your Flask of Split Serum effect ran out!")))

            # Sets durability when you get the item
            if (self._flask_durability[9] == 0):
                self._flask_durability[9] = 4


    def update_dealers_hesitation_durability(self, invincible=False):
        if (self.has_flask_effect("Dealer's Hesitation")):
            if invincible:
                self._flask_durability[10] = -1
                
            if (self._flask_durability[10] > 0):
                if not (self.has_item("Frank's Flask") and random.randrange(3) == 0):
                    self._flask_durability[10] -= random.choice([1, 2])
                if self._flask_durability[10] <= 0:
                    self._flask_durability[10] = 0
                    self.remove_flask_effect("Dealer's Hesitation")
                    print()
                    type.slow(red(bright("Your Flask of Dealer's Hesitation effect ran out!")))

            # Sets durability when you get the item
            if (self._flask_durability[10] == 0):
                self._flask_durability[10] = 4
        

    def get_item_desc(self, item):
        if item == "Delight Indicator": return "A small gadget, with wires tangled around it, and a small meter that displays the Dealer's happiness before every round of Blackjack."
        elif item == "Health Indicator": return "A small gadget, with wires construed around it, and a small gauge that displays changes in your health. Your current health is " + bright(magenta(str(self._health) + "%")) + "."
        elif item == "Dirty Old Hat": return "A dark brown leather hat, covered in dirt and tears. It makes you look poor, and lowers the Dealer's minimum bet."
        elif item == "Golden Watch": return "A bright gold watch that glistens in any light. It makes you look rich, and increases the number of Blackjack rounds the Dealer lets you play."
        elif item == "Enchanting Silver Bar": return "A silver bar that slowly increases in worth every day. Sell this after 3 days to make a profit."
        elif item == "Sneaky Peeky Shades": return "A pair of glasses that allow you to sneak a peek at the next card in the deck once per night."
        elif item == "Quiet Sneakers": return "A pair of shoes that allows you to skip an unfavorable event during the day."
        elif item == "Faulty Insurance": return "A plastic card, with the company \'Super Real Insurance\' written on it. This card can be brought to the doctor's office for a chance of lowering bill fees."
        elif item == "Lucky Coin": return "A tarnished copper coin with a four-leaf clover etched on one side. Flip it before a hand to occasionally turn a loss into a push."
        elif item == "Worn Gloves": return "A pair of threadbare leather gloves that help you feel the cards better. Slightly increases your chances of getting a favorable card when hitting."
        elif item == "Tattered Cloak": return "A moth-eaten cloak that helps you blend into the shadows. The Dealer sometimes forgets to collect your bet when you lose."
        elif item == "Rusty Compass": return "An old compass with a cracked glass face. It points towards nearby opportunities, occasionally revealing a hidden shop or event."
        elif item == "Pocket Watch": return "A small brass pocket watch that's always a few minutes slow. It sometimes gives you an extra round at the Blackjack table."
        elif item == "Marvin's Monocle": return "A smoky monocle that reveals exactly how much of your visible bankroll is hot money. Vinnie hates that you know."
        elif item == "Marvin's Eye": return "A singular enchanted eye that reveals hidden outcomes before choices lock in. Fate hates being watched."
        elif item == "Bottle of Tomorrow": return "A bottle filled with stolen daylight. Drink it to skip forward to tomorrow with your body and mind restored."
        elif item == "Blank Check": return "A cursed blank check that can be exchanged for one free purchase from any shop."
        elif item == "The Last Card": return "A final trump card that guarantees the exact draw you need, once."

        elif item == "Delight Manipulator": return "A small gadget, embedded in your right arm, with wires sticking into your veins. Attached is a small antenna that elicits complete and absolute happiness in anyone around you."
        elif item == "Health Manipulator": return "A small gadget, embedded in your left arm, with wires construed throughout your veins and into your heart. The device pumps artificial blood with a syntetic heartbeat throught your body, ensuring that you're always perfectly healthy."
        elif item == "Unwashed Hair": return "An implant into your scalp, giving you a fake hairdo covered in grime and grease. It makes you look abysmally poor, and sets the Dealer's minimum bet to one measly dollar"
        elif item == "Sapphire Watch": return "A sparkling sapphire watch that lights up any room. It makes you look richer than everyone else in the room, and greatly increases the number of Blackjack rounds the Dealer lets you play."
        elif item == "Enchanting Gold Bar": return "A gold bar that quickly increases in worth every day. Sell this after 3 days to make a profit."
        elif item == "Sneaky Peeky Goggles": return "A pair of goggles that allow you to sneak a peek at the next card in the deck once per round."
        elif item == "Quiet Bunny Slippers": return "A pair of slippers that allows you to skip all unfavorable events during the day."
        elif item == "Real Insurance": return "A plastic card, with the company \'Super Duper Real Insurance\' written on it. This card can be brought to the doctor's office to cover all bill fees."
        elif item == "Lucky Medallion": return "A gleaming gold medallion with a shooting star carved into its center. Flip it before a hand to always turn a loss into a push."
        elif item == "Velvet Gloves": return "A pair of exquisite velvet gloves that make your hands feel one with the cards. Significantly increases your chances of getting a favorable card when hitting."
        elif item == "Invisible Cloak": return "A shimmering cloak woven from moonlight threads. It makes you completely unnoticeable, and the Dealer often forgets to collect your bet when you lose."
        elif item == "Golden Compass": return "A pristine compass made of solid gold, with a needle that glows faintly. It always points towards the best opportunities, guaranteeing a beneficial shop or event each day."
        elif item == "Grandfather Clock": return "A miniaturized grandfather clock that fits in your pocket and keeps perfect time. It guarantees extra rounds at every Blackjack table you visit."

        elif item == "No Bust": return "A flask holding a dark green potion. It's infused with the power to veto a hand that busts. It lasts a few days."
        elif item == "Imminent Blackjack": return "A flask holding a neon yellow potion. It's infused with the power to instantly give you a Blackjack after hitting your hand. It wears off after one use."
        elif item == "Dealer's Whispers": return "A flask holding a navy blue potion. It's infused with the power to reveal the Dealer's hidden card. It lasts a few days."
        elif item == "Bonus Fortune": return "A flask holding a shiny gold potion. It's infused with the power to let you double down after being dealt a hand. It lasts a few days."
        elif item == "Anti-Venom": return "A flask holding a sparkly orange potion. It's infused with the power to heal you when attacked by a venemous creature. It lasts until used."
        elif item == "Anti-Virus": return "A flask holding a flowing gray potion. It's infused with the power to heal you when affected by a disease. It lasts until used."
        elif item == "Fortunate Day": return "A flask holding a bright orange potion. It's infused with the luck of the sun, and makes your next morning lucky. It wears off after one use."
        elif item == "Fortunate Night": return "A flask holding a pretty magenta potion. It's infused with the luck of the stars, and makes your next evening lucky. It wears off after one use, and has no impact on gambling."
        elif item == "Second Chance": return "A flask holding a swirling silver potion. It's infused with the power to replay a losing hand once per night. It lasts a few days."
        elif item == "Split Serum": return "A flask holding a vibrant violet potion. It's infused with the power to split any pair, even when you normally couldn't. It lasts a few days."
        elif item == "Dealer's Hesitation": return "A flask holding a murky brown potion. It's infused with the power to make the Dealer draw one extra card. It lasts a few days."
        elif item == "Pocket Aces": return "A flask holding a pure white potion. It's infused with the power to guarantee your first card is an Ace. It wears off after one use."

        elif item == "Never Bust": return "A flask holding a glowing green potion. It's infused with the power to veto a hand that busts."
        elif item == "Guaranteed Blackjack": return "A flask holding a glowing yellow potion. It's infused with the power to instantly give you a Blackjack after hitting your hand."
        elif item == "Dealer's Thoughts": return "A flask holding a glowing blue potion. It's infused with the power to always reveal the Dealer's hidden card."
        elif item == "Endless Fortune": return "A flask holding a glowing gold potion. It's infused with the power randomly double your bet for free after being dealt a hand."
        elif item == "Anti-Pathogen": return "A flask holding a glowing orange potion. It's infused with the power to heal you from any status effect."
        elif item == "Fortunate Life": return "A flask holding a glowing red potion. It's infused with the luck of the sun and the moon, and fills your life with good fortune."
        elif item == "Infinite Chances": return "A flask holding a glowing silver potion. It's infused with the power to replay any losing hand as many times as you'd like."
        elif item == "Perfect Split": return "A flask holding a glowing violet potion. It's infused with the power to split any hand, and both hands receive optimal cards."
        elif item == "Dealer's Doom": return "A flask holding a glowing brown potion. It's infused with the power to force the Dealer to always bust."
        elif item == "Ace in the Hole": return "A flask holding a glowing white potion. It's infused with the power to guarantee both your starting cards are Aces."
        elif item == "Animal Whistle": return "A small silver whistle carved with intricate animal shapes. When blown, any animal will trust you completely. Collect enough companions to unlock a secret ending."
        elif item == "Tony's Gun": return "A heavy black pistol you took from Vinnie's enforcer. It smells like gun oil and bad decisions. Having this marks you as Vinnie's enemy."
        elif item == "Angel's Number": return "A crumpled piece of paper with a phone number. The woman who saved you on the bridge. Call her when things get dark."
        elif item == "High Roller Keycard": return "A sleek black card that grants access to the High Roller Lounge. Free drinks, higher limits, and people who pretend you matter."
        elif item == "Gus's Precious Grime": return "A small jar of dark, shimmering grime. Years of Gus's work, compressed into this single vessel. It pulses faintly. What does it do? Nobody knows. Maybe that's the point."


