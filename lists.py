import random

class Lists:
    def __init__(self, player):
        self.__player = player
        self.__quote_list = self.make_quote_list()
        self.__cheers_list = self.make_cheers_list()
        self.__advice_list = self.make_advice_list()
        self.__dealer_welcome_list = self.make_dealer_welcome_list()
        self.__prayers_list = self.make_prayers_list()
        self.__fed_squirrely_list = self.make_fed_squirrely_list()
        self.__hungry_squirrely_list = self.make_hungry_squirrely_list()
        self.__quote_setup_list = self.make_quote_setup_list()
        self.__poor_day_events = self.make_poor_day_events_list()
        self.__cheap_day_events = self.make_cheap_day_events_list()
        self.__modest_day_events = self.make_modest_day_events_list()
        self.__rich_day_events = self.make_rich_day_events_list()
        self.__doughman_day_events = self.make_doughman_day_events_list()
        self.__nearly_day_events = self.make_nearly_day_events_list()
        self.__poor_night_events = self.make_poor_night_events_list()
        self.__cheap_night_events = self.make_cheap_night_events_list()
        self.__modest_night_events = self.make_modest_night_events_list()
        self.__rich_night_events = self.make_rich_night_events_list()
        self.__doughman_night_events = self.make_doughman_night_events_list()
        self.__nearly_night_events = self.make_nearly_night_events_list()
        self.__shop_list = self.make_shop_list()
        self.__marvins_adjectives_list = self.make_marvins_adjectives_list()
        self.__achievements = self.make_achievements_dict()
        self.__companion_types = self.make_companion_types()
        self.__pawn_shop_prices = self.make_pawn_shop_prices()
        self.__loan_shark_dialogue = self.make_loan_shark_dialogue()
        self.__dealer_betrayal_list = self.make_dealer_betrayal_dialogue_list()

    # ==========================================
    # ACHIEVEMENT SYSTEM DATA
    # ==========================================
    
    def make_achievements_dict(self):
        """All achievements in the game"""
        return {
            # Common - Money Milestones (easy)
            "first_thousand": {"name": "Baby Steps", "description": "Reach $1,000 for the first time."},
            "first_ten_thousand": {"name": "Getting Somewhere", "description": "Reach $10,000 for the first time."},
            "fifty_thousand": {"name": "Halfway to Modest", "description": "Reach $50,000."},
            
            # Common - Survival Milestones (easy)
            "three_days": {"name": "The Third Day", "description": "Survive 3 days."},
            "week_survivor": {"name": "Still Kicking", "description": "Survive 7 days."},
            
            # Common - Basic Gambling (easy)
            "first_blackjack": {"name": "Twenty-One!", "description": "Hit your first blackjack."},
            "ten_hands": {"name": "Getting the Hang of It", "description": "Play 10 hands of blackjack."},
            "first_win": {"name": "Beginner's Luck", "description": "Win your first hand."},
            
            # Common - Social (easy)
            "meet_suzy": {"name": "Hello, Suzy", "description": "Meet Suzy for the first time."},
            "first_mechanic": {"name": "Roadside Assistance", "description": "Visit a mechanic."},
            "first_shop": {"name": "Window Shopping", "description": "Visit any shop."},
            
            # Uncommon - Money (medium)
            "hundred_thousand": {"name": "Big Spender", "description": "Reach $100,000 for the first time."},
            "quarter_million": {"name": "Getting Serious", "description": "Reach $250,000."},
            "broke_to_rich": {"name": "Rags to Riches", "description": "Go from under $100 to over $10,000 in one day."},
            
            # Uncommon - Survival (medium)
            "two_weeks": {"name": "Fortnight Fighter", "description": "Survive 14 days."},
            "month_survivor": {"name": "Stubborn", "description": "Survive 30 days."},
            "near_death_survivor": {"name": "Not Today, Death", "description": "Survive with less than 5 health."},
            
            # Uncommon - Gambling (medium)
            "fifty_hands": {"name": "Card Counter", "description": "Play 50 hands of blackjack."},
            "card_shark": {"name": "Card Shark", "description": "Play 100 hands of blackjack."},
            "blackjack_master": {"name": "Blackjack Master", "description": "Hit 10 blackjacks."},
            "three_streak": {"name": "Triple Threat", "description": "Win 3 hands in a row."},
            "comeback_kid": {"name": "Comeback Kid", "description": "Win after having less than $100."},
            "big_bet": {"name": "High Roller Moment", "description": "Win a hand worth $1,000+."},
            
            # Uncommon - Items & Collection (medium)
            "first_item": {"name": "Packrat Begins", "description": "Acquire your first item."},
            "five_items": {"name": "Starting Collection", "description": "Collect 5 different items."},
            "first_flask": {"name": "Alchemist's Apprentice", "description": "Use your first flask."},
            "treasure_hunter": {"name": "Treasure Hunter", "description": "Sell 5 collectibles to Gus."},
            
            # Uncommon - Companions (medium)
            "first_friend": {"name": "First Friend", "description": "Befriend your first companion."},
            "companion_bond": {"name": "Bonding Time", "description": "Reach 50 happiness with any companion."},
            
            # Uncommon - Misc (medium)
            "rock_bottom": {"name": "Rock Bottom", "description": "Lose all your money and recover."},
            "sanity_saved": {"name": "Sanity Saved", "description": "Recover from below 25 sanity to above 75."},
            "broken_but_alive": {"name": "Broken But Breathing", "description": "Survive the broken state."},
            "devils_deal": {"name": "Devil's Deal", "description": "Make a deal with the devil and survive."},
            
            # Rare - Money (hard)
            "half_million": {"name": "Almost There", "description": "Reach $500,000 for the first time."},
            "nine_hundred": {"name": "So Close", "description": "Reach $900,000."},
            "yo_yo": {"name": "Economic Yo-Yo", "description": "Gain and lose $100,000 multiple times."},
            
            # Rare - Survival (hard)
            "hundred_days": {"name": "The Long Road", "description": "Survive 100 days."},
            "injured_survival": {"name": "Walking Wounded", "description": "Survive 7 days with an injury."},
            "sick_survival": {"name": "Plague Bearer", "description": "Survive 7 days while sick."},
            "cheated_death": {"name": "Cheated Death", "description": "Survive 3 near-death experiences."},
            "clinging_to_life": {"name": "Clinging to Life", "description": "Survive with 10 or less health."},
            "scarred_survivor": {"name": "Scarred Survivor", "description": "Have 5 different injuries at once."},
            
            # Rare - Gambling (hard)
            "hot_streak": {"name": "Hot Streak", "description": "Win 5 hands in a row."},
            "blackjack_legend": {"name": "Natural Master", "description": "Hit 25 blackjacks."},
            "two_hundred_hands": {"name": "Veteran Player", "description": "Play 200 hands."},
            "high_roller": {"name": "High Roller", "description": "Win a single hand worth $10,000+."},
            "blackjack_streak": {"name": "Natural Streak", "description": "Hit 3 blackjacks in 10 hands."},
            "comeback_master": {"name": "Phoenix Rising", "description": "Win 5 hands in a row after a 5-loss streak."},
            
            # Rare - Collection (hard)
            "collector": {"name": "Collector", "description": "Collect 10 different items."},
            "flask_connoisseur": {"name": "Flask Connoisseur", "description": "Use 10 different flask types."},
            "item_hoarder": {"name": "Hoarder", "description": "Have 15 items at once."},
            
            # Rare - Companions (hard)
            "animal_lover": {"name": "Animal Lover", "description": "Have 3 or more companions."},
            "best_friends": {"name": "Best Friends", "description": "Reach 90 happiness with a companion."},
            "loyal_companion": {"name": "Loyal Companion", "description": "Keep a companion for 30 days."},
            "pet_cemetery": {"name": "They All Leave Eventually", "description": "Have 3 companions run away."},
            
            # Rare - Social & Events (hard)
            "social_butterfly": {"name": "Social Butterfly", "description": "Meet 20 different people."},
            "regular": {"name": "Regular", "description": "Visit the casino 50 times."},
            "night_owl": {"name": "Night Owl", "description": "Experience 20 night events."},
            "morning_person": {"name": "Morning Person", "description": "Experience 20 morning events."},
            "event_collector": {"name": "Story Seeker", "description": "Experience 50 unique events."},
            
            # Rare - Specific Events (hard)
            "rabbit_chaser": {"name": "Down the Rabbit Hole", "description": "Complete all rabbit chase events."},
            "dream_walker": {"name": "Dream Walker", "description": "Experience all three dream sequences."},
            "suzy_story": {"name": "Pigtails and Promises", "description": "Complete Suzy's full story arc."},
            
            # Epic - Money (very hard)
            "millionaire": {"name": "The Dream", "description": "Reach $1,000,000 and complete your goal."},
            "multi_millionaire": {"name": "Overachiever", "description": "Reach $2,000,000."},
            "near_miss": {"name": "So Close Yet So Far", "description": "Reach $950,000 and then go broke."},
            
            # Epic - Survival (very hard)
            "two_hundred_days": {"name": "Endless Grind", "description": "Survive 200 days."},
            "low_health_master": {"name": "Living on the Edge", "description": "Survive 10 days under 25 health."},
            "sanity_master": {"name": "Mind Over Matter", "description": "Survive 20 days under 30 sanity."},
            "debt_free": {"name": "Debt Free", "description": "Pay off a loan shark debt of $30,000+."},
            "beaten_and_bloody": {"name": "Beaten and Bloody", "description": "Survive all loan shark violence tiers."},
            
            # Epic - Gambling (very hard)
            "win_streak_10": {"name": "Unstoppable", "description": "Win 10 hands in a row."},
            "five_hundred_hands": {"name": "Gambling Addiction", "description": "Play 500 hands of blackjack."},
            "fifty_blackjacks": {"name": "Card Counting Suspicion", "description": "Hit 50 blackjacks."},
            "big_spender": {"name": "Whale Status", "description": "Win a single hand worth $50,000+."},
            "no_bust_streak": {"name": "Perfect Control", "description": "Play 20 hands without busting."},
            
            # Epic - Collection (very hard)
            "master_collector": {"name": "Museum Curator", "description": "Collect 20 different items."},
            "full_house": {"name": "Full House", "description": "Own every collectible item at once."},
            "flask_master": {"name": "Potion Master", "description": "Have 5 active flask effects at once."},
            "item_master": {"name": "Item Master", "description": "Use every item in the game."},
            
            # Epic - Companions (very hard)
            "max_companions": {"name": "Noah's Wagon", "description": "Have 5 companions at once."},
            "companion_loyalty": {"name": "Unbreakable Bond", "description": "Keep a companion for 60 days."},
            "sanctuary_finder": {"name": "The Animal Shepherd", "description": "Find the secret companion sanctuary ending."},
            
            # NEW COMPANION ACHIEVEMENTS
            "zookeeper": {"name": "Zookeeper", "description": "Befriend 10 different animals."},
            "noahs_ark": {"name": "Noah's Ark", "description": "Befriend 20 different animals."},
            "disney_princess": {"name": "Disney Princess", "description": "Befriend all forest creatures."},
            "marine_biologist": {"name": "Marine Biologist", "description": "Befriend all water creatures."},
            
            # Epic - Misc (very hard)
            "iron_will": {"name": "Iron Will", "description": "Never drop below 50 sanity."},
            "doctor_regular": {"name": "Medical Marvel", "description": "Visit the doctor 20 times."},
            "mechanic_loyal": {"name": "Mechanic Loyalty", "description": "Visit the same mechanic 15 times."},
            
            # Legendary - Ultimate Challenges (extremely rare)
            "year_survivor": {"name": "The Long Con", "description": "Survive 365 days."},
            "perfect_record": {"name": "Perfect Record", "description": "Reach $100,000 without losing a hand."},
            "lottery_winner": {"name": "Against All Odds", "description": "Win the lottery jackpot."},
            "death_defier": {"name": "Death Defier", "description": "Survive 10 near-death experiences."},
            "true_gambler": {"name": "True Gambler", "description": "Play 1,000 hands of blackjack."},
            "philanthropist": {"name": "Robin Hood", "description": "Give away $100,000 in total."},
            "cursed_survival": {"name": "Cursed But Alive", "description": "Survive 30 days with a cursed item."},
            "casino_legend": {"name": "Casino Legend", "description": "Visit the casino 200 times."},
            "all_endings": {"name": "Fate Collector", "description": "Experience all game endings."},
            "speedrunner": {"name": "Speedrunner", "description": "Reach $1,000,000 in under 30 days."},
            
            # Secret/Dark Endings - The Betrayal Path
            "first_sale": {"name": "First Blood", "description": "Sell your first companion to Gus."},
            "three_sales": {"name": "The Product", "description": "Sell 3 companions. Learn about the processing plant."},
            "five_sales": {"name": "Meat Cubes", "description": "Sell 5 companions. Learn the truth about what happens to them."},
            "seven_sales": {"name": "The Menu", "description": "Sell 7 companions. Gus describes the flavors."},
            "ten_sales": {"name": "Production Run", "description": "Sell 10 companions. Receive the factory's business card."},
            "cube_master": {"name": "The Factory", "description": "Sell 15 companions. Become part of the machine."},
            
            # Gift System & Dealer Happiness
            "gift_giver": {"name": "Bearer of Gifts", "description": "Give your first gift to the Dealer."},
            "perfect_gift": {"name": "Perfect Gift", "description": "Give a gift that increases Dealer happiness by 25+."},
            "death_wish": {"name": "Death Wish", "description": "Give the Dealer a gift that kills you."},
            "dealer_pleased": {"name": "In His Good Graces", "description": "Reach 100 Dealer happiness."},
            "dealer_furious": {"name": "On Thin Ice", "description": "Drop Dealer happiness to 10 or below."},
            
            # Fraudulent Cash System
            "money_launderer": {"name": "Money Launderer", "description": "Successfully blend $10,000 in fraudulent cash."},
            "master_launderer": {"name": "Master Launderer", "description": "Blend $100,000 in fraudulent cash total."},
            "caught_red_handed": {"name": "Caught Red-Handed", "description": "Have the Dealer stop gaining happiness due to fake cash."},
            "vinnie_regular": {"name": "Vinnie's Best Customer", "description": "Take 5 loans from the loan shark."},
            
            # Pawn Shop
            "first_garble": {"name": "Into the Machine", "description": "Garble your first collectible."},
            "grime_addict": {"name": "Grime Addict", "description": "Garble 20 collectibles."},
            "gus_trusted": {"name": "Gus Trusts You", "description": "Reach 75+ reputation at the pawn shop."},
            
            # Specific Item Discoveries
            "animal_whisperer": {"name": "Animal Whisperer", "description": "Find the Animal Whistle."},
            "grimoire_keeper": {"name": "Keeper of Records", "description": "Acquire the Gambler's Grimoire."},
            "oracle_ascended": {"name": "Oracle Ascended", "description": "Upgrade to Oracle's Tome."},
            "fully_upgraded": {"name": "Maximum Upgrade", "description": "Have 5 fully upgraded items at once."},
            
            # Unique Deaths
            "dealer_executed": {"name": "The Dealer's Justice", "description": "Be killed by the Dealer for angering him."},
            "tony_visited": {"name": "Tony's Collection", "description": "Survive a visit from Tony the enforcer."},
            "madness_consumed": {"name": "Lost to Madness", "description": "Die from the madness ending."},
            
            # Social Achievements
            "suzy_romance": {"name": "Suzy's Heart", "description": "Complete Suzy's full storyline."},
            "all_mechanics": {"name": "Mechanic Connoisseur", "description": "Visit all three mechanics."},
            "marvin_customer": {"name": "Believer in Magic", "description": "Purchase from Marvin's shop."},
            "kyle_regular": {"name": "Kyle's Buddy", "description": "Purchase 10 items from the convenience store."},
            
            # Rare Events
            "rabbit_chaser": {"name": "Down the Rabbit Hole", "description": "Complete all rabbit chase events."},
            "kraken_encounter": {"name": "Leviathan's Blessing", "description": "Befriend the Kraken."},
            "moon_touched": {"name": "Moonlit", "description": "Experience the moon rabbit event."},
            "mermaid_met": {"name": "Song of the Sea", "description": "Meet the mermaid."},
            "witch_wisdom": {"name": "Witch's Wisdom", "description": "Complete witch doctor's riddle."},
            
            # Gameplay Mastery
            "never_bust": {"name": "Controlled Gambler", "description": "Win 50 hands without busting once."},
            "insurance_expert": {"name": "Insurance Expert", "description": "Collect insurance 10 times."},
            "split_master": {"name": "Split Master", "description": "Win both hands of a split 5 times."},
            "double_down_king": {"name": "Double Down King", "description": "Win 20 double downs."},
            "surrender_survivor": {"name": "Strategic Retreat", "description": "Surrender 10 hands."},
            "blackjack_natural": {"name": "Natural Talent", "description": "Get 10 natural blackjacks."},
            "perfect_split": {"name": "Perfect Split", "description": "Get blackjack on both split hands."},
            "high_roller_bet": {"name": "High Roller", "description": "Bet $50,000 on a single hand."},
            "all_in_win": {"name": "All In", "description": "Bet your entire balance and win."},
            "comeback_king": {"name": "The Comeback", "description": "Go from under $100 to over $10,000 in one session."},
            
            # Money Extremes
            "penny_pincher": {"name": "Penny Pincher", "description": "Survive 10 days with under $100."},
            "zero_balance": {"name": "Rock Bottom", "description": "Reach exactly $0."},
            "money_hoarder": {"name": "Dragon's Hoard", "description": "Hold $500,000 without spending."},
            "big_spender": {"name": "Big Spender", "description": "Spend $100,000 at shops in total."},
            "never_shop": {"name": "Minimalist", "description": "Reach day 50 without buying anything."},
            "debt_collector": {"name": "In the Red", "description": "Owe $100,000 to the loan shark."},
            
            # Companion Variety
            "cat_person": {"name": "Cat Person", "description": "Have 5 cat companions at once."},
            "dog_person": {"name": "Dog Person", "description": "Have 5 dog companions at once."},
            "aquarium": {"name": "Living Aquarium", "description": "Have 10 aquatic companions."},
            "aviary": {"name": "Aviary Keeper", "description": "Have 10 bird companions."},
            "mythical_menagerie": {"name": "Mythical Menagerie", "description": "Have 5 mythical creature companions."},
            "lone_wolf": {"name": "Lone Wolf", "description": "Reach day 100 without any companions."},
            
            # Death & Failure
            "first_death": {"name": "First Blood (Yours)", "description": "Die for the first time."},
            "death_collector": {"name": "Death Collector", "description": "Die 10 different ways."},
            "quick_death": {"name": "Speed Run (Death%)", "description": "Die within 5 days."},
            "serial_dier": {"name": "Glutton for Punishment", "description": "Die 50 times total."},
            "loan_shark_victim": {"name": "Sleeping with the Fishes", "description": "Be killed by the loan shark."},
            
            # Location Mastery
            "casino_rat": {"name": "Casino Rat", "description": "Visit the casino 100 times."},
            "shop_hopper": {"name": "Window Shopping", "description": "Visit all shops in one day."},
            "hermit": {"name": "Hermit", "description": "Stay at camp for 20 days straight."},
            "nomad": {"name": "Nomad", "description": "Visit 5 different locations in one day."},
            
            # Special Card Combinations
            "lucky_sevens": {"name": "Lucky Sevens", "description": "Get three 7s in one hand."},
            "unlucky_thirteen": {"name": "Unlucky Thirteen", "description": "Bust with exactly 13."},
            "twenty_one_push": {"name": "So Close", "description": "Push with 21 five times."},
            "dealer_bust_streak": {"name": "Dealer's Nightmare", "description": "Win 10 hands in a row by dealer bust."},
            
            # Rare Item Interactions
            "cursed_collector": {"name": "Cursed Collector", "description": "Own 5 cursed items at once."},
            "blessing_hoarder": {"name": "Blessed Beyond Measure", "description": "Have 10 active blessings."},
            "trinket_master": {"name": "Trinket Master", "description": "Collect every trinket type."},
            "weapon_dealer": {"name": "Armed and Dangerous", "description": "Own 5 weapons at once."},
            
            # NPC Relationships
            "dealer_friend": {"name": "The Dealer's Equal", "description": "Maintain 90+ happiness for 20 days."},
            "gus_partner": {"name": "Business Partners", "description": "Reach max reputation with Gus."},
            "oswald_masterwork": {"name": "Oswald's Masterpiece", "description": "Have Oswald upgrade an item 10 times."},
            "marvin_believer": {"name": "True Believer", "description": "Buy everything from Marvin."},
            "kyle_confidant": {"name": "Late Night Talks", "description": "Visit Kyle 50 times."},
            
            # Time-Based
            "speedrunner_rich": {"name": "Speedrunner", "description": "Reach $100,000 before day 30."},
            "marathon_man": {"name": "Marathon Man", "description": "Survive 200 days."},
            "centurion": {"name": "Centurion", "description": "Play 100 sessions."},
            "time_loop": {"name": "Déjà Vu", "description": "Experience the same event 3 days in a row."},
            
            # Secret/Meta
            "fourth_wall": {"name": "Breaking the Fourth Wall", "description": "Discover a meta secret."},
            "completionist": {"name": "Completionist", "description": "Unlock 90% of all achievements."},
            "achievement_hunter": {"name": "Achievement Hunter", "description": "Check your achievements 100 times."},
            "true_ending": {"name": "True Ending", "description": "Find the secret true ending."},
            "new_game_plus": {"name": "New Game+", "description": "Start a new run after getting all endings."},
            
            # Insane Challenges
            "lose_streak": {"name": "Professional Loser", "description": "Lose 50 hands in a row."},
            "bust_master": {"name": "Bust Master", "description": "Bust 100 times."},
            "million_lost": {"name": "Burning Money", "description": "Lose $1,000,000 total."},
            "no_item_millionaire": {"name": "Pure Skill", "description": "Reach $1,000,000 without buying any items."},
            "cursed_millionaire": {"name": "Cursed Millionaire", "description": "Reach $1,000,000 while holding only cursed items."},
            "zero_happiness_survivor": {"name": "Edge of Death", "description": "Survive 10 days with Dealer happiness under 5."},
            "fake_money_king": {"name": "Counterfeit King", "description": "Have $500,000 in fraudulent cash at once."},
            "debt_spiral": {"name": "Debt Spiral", "description": "Take a loan to pay off another loan 5 times."},
            "broke_millionaire": {"name": "Broke Millionaire", "description": "Reach $1,000,000 then lose it all to $0."},
            "bankruptcy_expert": {"name": "Bankruptcy Expert", "description": "Go from $100,000+ to $0 in one day."},
            
            # Absurd Combinations
            "zoo_betrayal": {"name": "The Ultimate Betrayal", "description": "Befriend 30 companions then sell them all."},
            "gift_of_death": {"name": "Gift of Death", "description": "Give the Dealer 5 gifts that lower his happiness."},
            "happiness_rollercoaster": {"name": "Emotional Rollercoaster", "description": "Change Dealer happiness by 100+ points in one day."},
            "all_shops_one_day": {"name": "Shopping Spree", "description": "Buy from every shop in a single day."},
            "item_hoarder": {"name": "Hoarder", "description": "Own 50 items at once."},
            "collector_betrayer": {"name": "Collector Betrayer", "description": "Collect every animal type then sell them all."},
            
            # Dark Humor
            "meat_cube_connoisseur": {"name": "Meat Cube Connoisseur", "description": "After The Factory ending, eat a meat cube."},
            "dealer_tormentor": {"name": "Dealer Tormentor", "description": "Lower Dealer happiness to 0 five times."},
            "loan_shark_best_friend": {"name": "Vinnie's Soulmate", "description": "Take 50 loans total."},
            "tony_survivor": {"name": "Tony's Punching Bag", "description": "Survive Tony's visits 10 times."},
            "death_tourist": {"name": "Death Tourist", "description": "Experience all unique death scenes."},
            "suicide_gambler": {"name": "Suicide Gambler", "description": "Bet your last dollar 100 times."},
            
            # Extreme Grinds
            "ten_thousand_hands": {"name": "Card Counter", "description": "Play 10,000 hands of blackjack."},
            "millennium_survivor": {"name": "Millennium Bug", "description": "Survive 1,000 days."},
            "every_item": {"name": "Item Encyclopedia", "description": "Own every item in the game at least once."},
            "every_companion": {"name": "Zookeeper Supreme", "description": "Befriend every companion type."},
            "all_endings_perfect": {"name": "Fate Master", "description": "Get all endings with perfect conditions."},
            "max_everything": {"name": "Perfection", "description": "Max out all stats, relationships, and money."},
            
            # Specific Insanity
            "split_inception": {"name": "Split Inception", "description": "Win a split where both hands also split."},
            "twenty_one_loss": {"name": "The Impossible Loss", "description": "Lose with 21 against Dealer's 21 five times."},
            "dealer_blackjack_victim": {"name": "Dealer's Blackjack Victim", "description": "Lose to Dealer blackjack 50 times."},
            "insurance_failure": {"name": "Insurance Scam", "description": "Take insurance when Dealer doesn't have blackjack 20 times."},
            "surrender_addiction": {"name": "Surrender Addiction", "description": "Surrender 100 hands."},
            "push_master": {"name": "Push Master", "description": "Push 100 hands."},
            
            # Self-Imposed Handicaps
            "pacifist_run": {"name": "Pacifist", "description": "Reach day 100 without owning any weapons."},
            "vegan_run": {"name": "Vegan", "description": "Complete the game without eating any meat items."},
            "no_loans": {"name": "Debt Free", "description": "Reach $1,000,000 without ever taking a loan."},
            "no_gifts": {"name": "No Presents", "description": "Reach day 100 without giving the Dealer any gifts."},
            "casino_only": {"name": "Casino Purist", "description": "Reach $100,000 visiting only the casino."},
            "minimum_bet": {"name": "Minimum Bet Master", "description": "Reach $100,000 betting minimum only."},
            
            # Ridiculous Feats
            "one_million_bet": {"name": "YOLO", "description": "Bet $1,000,000 on a single hand."},
            "win_million_hand": {"name": "Whale Victory", "description": "Win a hand worth $1,000,000+."},
            "perfect_day": {"name": "Perfect Day", "description": "Win every hand in a day (minimum 10 hands)."},
            "worst_day": {"name": "Worst Day Ever", "description": "Lose every hand in a day (minimum 10 hands)."},
            "all_naturals": {"name": "All Naturals", "description": "Get 5 blackjacks in a row."},
            "all_busts": {"name": "All Busts", "description": "Bust 10 hands in a row."},
            "companion_army": {"name": "Companion Army", "description": "Have 50 companions at once."},
            "item_minimalist": {"name": "Empty Pockets", "description": "Reach $1,000,000 with 0 items in inventory."},
        }
    
    def get_achievement_data(self, achievement_id):
        return self.__achievements.get(achievement_id, None)
    
    def get_total_achievements(self):
        return len(self.__achievements)
    
    def get_all_achievement_ids(self):
        """Return list of all achievement IDs"""
        return list(self.__achievements.keys())

    # ==========================================
    # COMPANION SYSTEM DATA
    # ==========================================
    
    def make_companion_types(self):
        """All companion types and their data"""
        return {
            "Squirrelly": {
                "type": "Squirrel",
                "description": "A friendly squirrel who loves acorns.",
                "favorite_food": "Bag of Acorns",
                "bonuses": {"sanity_restore": 2, "luck_bonus": 1},
                "dialogue": {
                    "happy": ["Squirrelly chatters happily on your dashboard.", "Squirrelly does a little dance with an acorn."],
                    "neutral": ["Squirrelly watches you with curious eyes.", "Squirrelly nibbles on something."],
                    "sad": ["Squirrelly looks at you with pleading eyes.", "Squirrelly's tail droops sadly."]
                }
            },
            "Whiskers": {
                "type": "Alley Cat",
                "description": "A scraggly but affectionate stray cat.",
                "favorite_food": "Cat Food",
                "bonuses": {"sanity_restore": 3, "danger_warning": True},
                "dialogue": {
                    "happy": ["Whiskers purrs loudly in your lap.", "Whiskers kneads your leg with contentment."],
                    "neutral": ["Whiskers stares out the window.", "Whiskers grooms themselves meticulously."],
                    "sad": ["Whiskers meows plaintively.", "Whiskers hides under the seat."]
                }
            },
            "Lucky": {
                "type": "Three-Legged Dog",
                "description": "A resilient mutt who lost a leg but not his spirit.",
                "favorite_food": "Dog Food",
                "bonuses": {"sanity_restore": 5, "protection": True},
                "dialogue": {
                    "happy": ["Lucky's tail wags so hard his whole body shakes.", "Lucky licks your face enthusiastically."],
                    "neutral": ["Lucky rests his head on your leg.", "Lucky watches the world go by."],
                    "sad": ["Lucky whimpers softly.", "Lucky won't meet your eyes."]
                }
            },
            "Mr. Pecks": {
                "type": "Crow",
                "description": "An intelligent crow who brings you shiny things.",
                "favorite_food": "Birdseed",
                "bonuses": {"find_money_chance": 5, "sanity_restore": 1},
                "dialogue": {
                    "happy": ["Mr. Pecks caws proudly and drops a shiny coin in your lap.", "Mr. Pecks preens on your shoulder."],
                    "neutral": ["Mr. Pecks watches you with beady, intelligent eyes.", "Mr. Pecks pecks at the window."],
                    "sad": ["Mr. Pecks sits silently, feathers ruffled.", "Mr. Pecks won't eat."]
                }
            },
            "Patches": {
                "type": "Opossum",
                "description": "A nocturnal friend who plays dead when scared.",
                "favorite_food": "Garbage",
                "bonuses": {"night_bonus": True, "sanity_restore": 2},
                "dialogue": {
                    "happy": ["Patches hangs from your rearview mirror by their tail.", "Patches nuzzles your hand."],
                    "neutral": ["Patches sleeps in a ball under the seat.", "Patches watches you warily."],
                    "sad": ["Patches plays dead. You're pretty sure they're not actually dead.", "Patches hisses when you get too close."]
                }
            },
            "Rusty": {
                "type": "Raccoon",
                "description": "A mischievous raccoon with clever paws.",
                "favorite_food": "Anything",
                "bonuses": {"steal_chance": 3, "sanity_restore": 2},
                "dialogue": {
                    "happy": ["Rusty chittered and washed their hands in your coffee cup.", "Rusty brings you something shiny... is that someone's watch?"],
                    "neutral": ["Rusty rummages through your glove box.", "Rusty watches you with their little bandit mask."],
                    "sad": ["Rusty sulks in the corner.", "Rusty won't come out of hiding."]
                }
            },
            "Slick": {
                "type": "Rat",
                "description": "A surprisingly clean and clever rat.",
                "favorite_food": "Cheese",
                "bonuses": {"danger_warning": True, "sanity_restore": 1},
                "dialogue": {
                    "happy": ["Slick runs up your arm and perches on your shoulder.", "Slick squeaks contentedly."],
                    "neutral": ["Slick watches you from the dashboard.", "Slick grooms their whiskers."],
                    "sad": ["Slick hides in the glove box.", "Slick won't eat."]
                }
            },
            "Hopper": {
                "type": "Rabbit",
                "description": "A lucky rabbit who brings good fortune.",
                "favorite_food": "Carrot",
                "bonuses": {"luck_bonus": 3, "sanity_restore": 2},
                "dialogue": {
                    "happy": ["Hopper does little binkies around the car.", "Hopper snuggles against your leg."],
                    "neutral": ["Hopper twitches their nose curiously.", "Hopper lounges on the passenger seat."],
                    "sad": ["Hopper thumps their foot anxiously.", "Hopper won't come out of hiding."]
                }
            }
        }
    
    def get_companion_type(self, name):
        return self.__companion_types.get(name, None)
    
    def get_all_companion_names(self):
        return list(self.__companion_types.keys())
    
    def get_companion_dialogue(self, name, mood):
        companion = self.__companion_types.get(name, None)
        if companion and "dialogue" in companion:
            return random.choice(companion["dialogue"].get(mood, ["Your companion looks at you."]))
        return "Your companion is with you."

    # ==========================================
    # PAWN SHOP PRICE DATA
    # ==========================================
    
    def make_pawn_shop_prices(self):
        """Prices for selling items at the pawn shop (base prices)"""
        return {
            # Common Items (low value)
            "Flashlight": 5,
            "Pocket Knife": 10,
            "Lighter": 3,
            "Matches": 1,
            "Water Bottle": 2,
            "First Aid Kit": 15,
            "Blanket": 8,
            "Sunglasses": 5,
            "Umbrella": 4,
            "Phone Charger": 8,
            "Snacks": 2,
            "Energy Drink": 3,
            "Coffee Thermos": 10,
            "Road Map": 3,
            
            # Car Items
            "Jumper Cables": 20,
            "Portable Battery Charger": 50,
            "Spare Fuses": 5,
            "Spare Headlight Bulbs": 10,
            "Motor Oil": 12,
            "Coolant": 8,
            "Brake Fluid": 6,
            "Power Steering Fluid": 7,
            "Transmission Fluid": 10,
            "Fix-a-Flat": 6,
            "Tire Patch Kit": 10,
            "Car Jack": 30,
            "Gas Can": 12,
            "Tool Kit": 40,
            "WD-40": 5,
            "Bungee Cords": 6,
            "Rope": 8,
            "Exhaust Tape": 7,
            "Radiator Stop Leak": 10,
            "Oil Stop Leak": 8,
            "Lock De-Icer": 3,
            "Fuel Line Antifreeze": 5,
            "OBD Scanner": 70,
            "Spare Spark Plugs": 15,
            "Serpentine Belt": 25,
            "Fuel Filter": 10,
            "Thermostat": 12,
            "Brake Pads": 40,
            
            # Valuable Items
            "Gold Chain": 150,
            "Diamond Ring": 500,
            "Vintage Wine": 75,
            "Fancy Cigars": 50,
            "Designer Watch": 200,
            "Laptop": 150,
            "Camera": 80,
            "Jewelry Box": 100,
            "Antique Coin": 75,
            "Silver Bar": 200,
            
            # Special Items (can't sell most of these, but just in case)
            "Bag of Acorns": 5,
            "Cat Food": 5,
            "Dog Food": 5,
            "Birdseed": 3,
            "Cheese": 2,
            "Carrot": 1,
        }
    
    def get_pawn_price(self, item_name):
        return self.__pawn_shop_prices.get(item_name, 0)
    
    def get_sellable_items(self):
        """Returns list of items that can be sold at pawn shop"""
        return list(self.__pawn_shop_prices.keys())

    # ==========================================
    # LOAN SHARK DIALOGUE
    # ==========================================
    
    def make_loan_shark_dialogue(self):
        """Vinnie the loan shark's various dialogue options"""
        return {
            "greeting": [
                "Vinnie's smile doesn't reach his eyes. " + "\"What can I do for you, friend?\"",
                "Vinnie cracks his knuckles. " + "\"Back again, huh?\"",
                "Vinnie leans against his black sedan. " + "\"Money troubles?\""
            ],
            "offer": [
                "\"I can help you out. Interest is reasonable. 20% a week.\"",
                "\"How much you need? I got cash. Just remember to pay it back. On time.\"",
                "\"I'm a businessman. You need money, I got money. Simple.\""
            ],
            "warning_1": [
                "\"Hey, just a friendly reminder. You owe me money. Don't forget.\"",
                "\"Payment's due soon. I know you're good for it, right?\"",
                "\"Tick tock, friend. Tick tock.\""
            ],
            "warning_2": [
                "\"I'm starting to get concerned. You haven't forgotten about me, have you?\"",
                "\"My associate Tony is starting to ask questions. You don't want to meet Tony.\"",
                "\"Interest is adding up. Might want to address that.\""
            ],
            "threat": [
                "\"We need to talk. And by talk, I mean you need to pay. Now.\"",
                "\"Tony's getting antsy. I can only hold him back so long.\"",
                "\"You're testing my patience. That's not smart.\""
            ],
            "violence": [
                "\"This is your last warning. Next time, I won't be so friendly.\"",
                "\"Tony's in the car. He wants to say hello. Do you want Tony to say hello?\"",
                "\"Your kneecaps look healthy. Shame if something happened to them.\""
            ],
            "collecting": [
                "\"Time's up.\"",
                "\"You should have paid.\"",
                "\"Nothing personal. Just business.\""
            ]
        }
    
    def make_loan_shark_greeting_list(self):
        a_list = []
        a_list.append("Back so soon? The cash is calling you, huh?")
        a_list.append("Fresh face looking for fresh money. I can work with that.")
        a_list.append("You got the look of someone who needs capital. Lucky for you, I got capital.")
        a_list.append("Money problems? Vinnie's got solutions. Expensive solutions, but solutions.")
        a_list.append("You need cash, I got cash. Simple transaction between friends.")
        random.shuffle(a_list)
        return a_list
    
    def make_loan_shark_warning_list(self):
        a_list = []
        a_list.append("Hey, uh, you're a little behind on payments. Not a big deal... yet.")
        a_list.append("Look, I like you, but the interest is adding up. Just saying.")
        a_list.append("The clock's ticking on that debt, friend. Tick tock.")
        a_list.append("You're overdue. I'm being nice about it now. Won't always be nice.")
        a_list.append("Debt doesn't just go away. It grows. Like a tumor. A very expensive tumor.")
        random.shuffle(a_list)
        return a_list
    
    def make_loan_shark_threat_list(self):
        a_list = []
        a_list.append("You're testing my patience. And Tony's. Especially Tony's.")
        a_list.append("I've been MORE than reasonable. That generosity? It's running out.")
        a_list.append("You know what happens to people who don't pay? Bad things. Creative bad things.")
        a_list.append("The interest is compounding. So is my frustration.")
        a_list.append("Pay up soon, or we're gonna have to have a different kind of conversation.")
        random.shuffle(a_list)
        return a_list
    
    def make_loan_shark_violence_list(self):
        a_list = []
        a_list.append("Tony sends his regards. And by regards, I mean his fists. Soon.")
        a_list.append("You've crossed the line. Tony's getting his tools ready.")
        a_list.append("I tried to be nice. You didn't listen. Now? Now it gets ugly.")
        a_list.append("Last warning. Next time I see you, Tony's with me.")
        a_list.append("You think you can just avoid me? Tony will find you. He always does.")
        random.shuffle(a_list)
        return a_list
    
    def make_loan_shark_collecting_list(self):
        a_list = []
        a_list.append("Tony's here. You see him? Yeah. He sees you too.")
        a_list.append("Too late for words. Way too late. Tony, do your thing.")
        a_list.append("You had your chances. All of them. Tony's gonna collect now.")
        a_list.append("Payment time. And Tony prefers to be paid in pain.")
        a_list.append("I gave you every opportunity. Now? Now we take it from you.")
        random.shuffle(a_list)
        return a_list
    
    def make_loan_shark_dialogue(self):
        """Central dialogue dictionary for loan shark"""
        return {
            "greeting": self.make_loan_shark_greeting_list(),
            "warning_1": self.make_loan_shark_warning_list(),
            "warning_2": self.make_loan_shark_warning_list(),
            "threat": self.make_loan_shark_threat_list(),
            "violence": self.make_loan_shark_violence_list(),
            "collecting": self.make_loan_shark_collecting_list()
        }
    
    def get_loan_shark_dialogue(self, dialogue_type):
        dialogue_list = self.__loan_shark_dialogue.get(dialogue_type, None)
        if dialogue_list and len(dialogue_list) > 0:
            return dialogue_list.pop(0)
        # If list is empty, remake it
        if dialogue_type == "greeting":
            self.__loan_shark_dialogue["greeting"] = self.make_loan_shark_greeting_list()
            return self.__loan_shark_dialogue["greeting"].pop(0)
        elif dialogue_type in ["warning_1", "warning_2"]:
            self.__loan_shark_dialogue[dialogue_type] = self.make_loan_shark_warning_list()
            return self.__loan_shark_dialogue[dialogue_type].pop(0)
        elif dialogue_type == "threat":
            self.__loan_shark_dialogue["threat"] = self.make_loan_shark_threat_list()
            return self.__loan_shark_dialogue["threat"].pop(0)
        elif dialogue_type == "violence":
            self.__loan_shark_dialogue["violence"] = self.make_loan_shark_violence_list()
            return self.__loan_shark_dialogue["violence"].pop(0)
        elif dialogue_type == "collecting":
            self.__loan_shark_dialogue["collecting"] = self.make_loan_shark_collecting_list()
            return self.__loan_shark_dialogue["collecting"].pop(0)
        return "Vinnie stares at you."


# This is a lot of similar code, but each list is a unique set of events
# That happen in each rank.
        
# If the list is empty, it recreates the list.
# Each event specifically has a chance of not triggering if certain
# conditions arent met
        
# Poor Events (1 - 1,000)
    def make_poor_day_events_list(self):
        a_list = []
        # Everytime
        a_list.append("seat_cash")
        a_list.append("left_window_down")
        a_list.append("estranged_dog")
        a_list.append("freight_truck")
        a_list.append("morning_stretch")
        a_list.append("ant_invasion")
        a_list.append("bird_droppings")
        a_list.append("flat_tire")
        a_list.append("mysterious_note")
        a_list.append("radio_static")
        a_list.append("vending_machine_luck")
        a_list.append("talking_to_yourself")
        a_list.append("wrong_number")
        a_list.append("cloud_watching")
        a_list.append("car_alarm_symphony")
        a_list.append("trash_treasure")
        a_list.append("coin_flip_stranger")
        a_list.append("seagull_attack")
        a_list.append("lucky_penny")
        a_list.append("stray_cat")
        a_list.append("three_legged_dog")
        a_list.append("opossum_in_trash")
        a_list.append("sewer_rat")
        a_list.append("conspiracy_theorist")
        a_list.append("dropped_ice_cream")
        a_list.append("motivational_graffiti")
        # Deadly Events
        a_list.append("back_alley_shortcut")
        a_list.append("food_poisoning")
        a_list.append("attacked_by_dog")
        a_list.append("carbon_monoxide")
        # MEDICAL EVENTS - Poor Tier
        a_list.append("contract_cold")
        a_list.append("contract_flu")
        a_list.append("contract_strep_throat")
        a_list.append("contract_ear_infection")
        a_list.append("contract_sinus_infection")
        a_list.append("contract_pink_eye")
        a_list.append("contract_ringworm")
        a_list.append("contract_scabies")
        a_list.append("rat_bite")
        a_list.append("dirty_needle_stick")
        a_list.append("unclean_water")
        a_list.append("mold_exposure")
        a_list.append("lead_poisoning")
        a_list.append("bad_oysters")
        a_list.append("homeless_shelter_outbreak")
        a_list.append("bad_tattoo_infection")
        a_list.append("public_pool_infection")
        a_list.append("food_truck_nightmare")
        # INJURY EVENTS - Poor Tier
        a_list.append("slip_in_shower")
        a_list.append("fall_down_stairs")
        a_list.append("kitchen_accident")
        a_list.append("bar_fight_aftermath")
        a_list.append("broken_nose")
        a_list.append("broken_wrist")
        a_list.append("deep_laceration")
        a_list.append("whiplash_injury")
        a_list.append("dog_attack_severe")
        a_list.append("assault_aftermath")
        # MENTAL HEALTH - Poor Tier
        a_list.append("severe_anxiety_attack")
        a_list.append("severe_depression_episode")
        a_list.append("insomnia_chronic")
        a_list.append("stress_breakdown")
        a_list.append("trauma_flashback")
        a_list.append("sleep_deprivation_crisis")
        # Conditional
        a_list.append("sore_throat")
        a_list.append("spider_bite")
        a_list.append("hungry_cockroach")
        a_list.append("ant_bite")
        a_list.append("knife_wound_infection")
        a_list.append("gut_wound_complications")
        a_list.append("dog_bite_rabies_scare")
        a_list.append("fuel_leak_fire")
        a_list.append("fuel_leak_fixed")
        a_list.append("damaged_exhaust_fixed")
        a_list.append("damaged_exhaust_again")
        a_list.append("atm_theft_police")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("painkiller_withdrawal")
        a_list.append("unpaid_tickets_boot")
        a_list.append("booted_car_impound")
        a_list.append("mystery_car_problem_worsens")
        # Random Small Events
        a_list.append("found_twenty")
        a_list.append("lost_wallet")
        a_list.append("sunburn")
        a_list.append("mosquito_bite_infection")
        a_list.append("good_hair_day")
        a_list.append("bad_hair_day")
        a_list.append("found_gift_card")
        a_list.append("car_battery_dead")
        a_list.append("flat_tire_again")
        a_list.append("nice_weather")
        a_list.append("terrible_weather")
        a_list.append("weird_noise")
        a_list.append("back_pain")
        a_list.append("stretching_helps")
        a_list.append("random_kindness")
        a_list.append("random_cruelty")
        a_list.append("someone_stole_your_stuff")
        a_list.append("prayer_answered")
        a_list.append("prayer_ignored")
        a_list.append("found_old_photo")
        a_list.append("got_a_tan")
        # One-Time
        a_list.append("lone_cowboy")
        a_list.append("whats_my_name")
        a_list.append("interrogation")
        a_list.append("old_man_jenkins")
        a_list.append("the_mime")
        # Secret Events
        a_list.append("midnight_visitor")
        a_list.append("perfect_hand")
        # NEW CREATIVE EVENTS - SILLY
        a_list.append("duck_army")
        a_list.append("sentient_sandwich")
        a_list.append("motivational_raccoon")
        a_list.append("pigeon_mafia")
        a_list.append("sock_puppet_therapist")
        a_list.append("dance_battle")
        # NEW CREATIVE EVENTS - WEIRD
        a_list.append("time_loop")
        a_list.append("mirror_stranger")
        a_list.append("the_glitch")
        a_list.append("fourth_wall_break")
        a_list.append("wrong_universe")
        # NEW CREATIVE EVENTS - DARK
        a_list.append("the_collector")
        a_list.append("the_empty_room")
        a_list.append("blood_moon_bargain")
        # NEW CREATIVE EVENTS - GOOFY
        a_list.append("alien_abduction")
        # NEW SECRET EVENTS
        a_list.append("exactly_100")
        a_list.append("exactly_420")
        a_list.append("exactly_13")
        a_list.append("day_palindrome")
        a_list.append("prime_day")
        a_list.append("same_as_health")
        # NON-NUMBER SECRET EVENTS
        a_list.append("first_sunrise")
        a_list.append("perfect_health_moment")
        a_list.append("rock_bottom")
        a_list.append("completely_broke_wisdom")
        a_list.append("the_cat_knows")
        a_list.append("rain_on_the_roof")
        a_list.append("the_sleeping_stranger")
        random.shuffle(a_list)
        return a_list
    
    def make_poor_night_events_list(self):
        a_list = []
        a_list.append("ditched_wallet")
        a_list.append("went_jogging")
        a_list.append("woodlands_path")
        a_list.append("stargazing")
        a_list.append("stray_cat_returns")
        a_list.append("midnight_walk")
        a_list.append("raccoon_invasion")
        a_list.append("insomnia_night")
        a_list.append("peaceful_night")
        a_list.append("nightmare_of_losing")
        a_list.append("dream_of_winning")
        a_list.append("drowning_dream")
        a_list.append("nice_dream")
        a_list.append("nightmare")
        # Conditional Night
        a_list.append("stray_cat_sick")
        a_list.append("stray_cat_dies")
        # One-Time (Rabbit)
        a_list.append("chase_the_rabbit")
        random.shuffle(a_list)
        return a_list

# Cheap Events (1,000 - 10,000)
    def make_cheap_day_events_list(self):
        a_list = []
        # Everytime
        a_list.append("sun_visor_bills")
        a_list.append("strong_winds")
        a_list.append("morning_fog")
        a_list.append("car_wont_start")
        a_list.append("raccoon_raid")
        a_list.append("beautiful_sunrise")
        a_list.append("fortune_cookie")
        a_list.append("deja_vu_again")
        a_list.append("street_musician")
        a_list.append("roadkill_philosophy")
        a_list.append("yard_sale_find")
        a_list.append("broken_atm")
        a_list.append("friendly_drunk")
        a_list.append("car_wash_encounter")
        a_list.append("lottery_scratch")
        a_list.append("free_sample_spree")
        a_list.append("parking_lot_poker")
        a_list.append("phone_scam_call")
        # Companion Events
        a_list.append("crow_encounter")
        a_list.append("garden_rabbit")
        a_list.append("three_legged_dog")
        # Deadly Events
        a_list.append("gas_station_robbery")
        a_list.append("drug_dealer_encounter")
        a_list.append("electrocution_hazard")
        a_list.append("car_explosion")
        # MEDICAL EVENTS - Cheap Tier
        a_list.append("contract_bronchitis")
        a_list.append("contract_stomach_flu")
        a_list.append("contract_uti")
        a_list.append("contract_mono")
        a_list.append("contract_staph_infection")
        a_list.append("bee_sting_allergy")
        a_list.append("asthma_attack")
        a_list.append("migraine_severe")
        a_list.append("vertigo_episode")
        a_list.append("tooth_abscess")
        a_list.append("severe_dehydration")
        a_list.append("malnutrition")
        a_list.append("camping_tick_bite")
        a_list.append("daycare_plague")
        a_list.append("botched_piercing")
        a_list.append("bad_sushi")
        # INJURY EVENTS - Cheap Tier
        a_list.append("car_accident_minor")
        a_list.append("construction_site_accident")
        a_list.append("grease_fire")
        a_list.append("sports_injury")
        a_list.append("gym_accident")
        a_list.append("electric_shock")
        a_list.append("broken_ankle")
        a_list.append("broken_hand")
        a_list.append("dislocated_shoulder")
        a_list.append("concussion_injury")
        a_list.append("broken_ribs_injury")
        a_list.append("second_degree_burns")
        a_list.append("hiking_disaster")
        a_list.append("trampoline_disaster")
        a_list.append("weight_dropping")
        # Conditional Deadly
        a_list.append("knife_wound_infection")
        a_list.append("gut_wound_complications")
        a_list.append("dog_bite_rabies_scare")
        a_list.append("fuel_leak_fire")
        a_list.append("fuel_leak_fixed")
        a_list.append("damaged_exhaust_fixed")
        a_list.append("damaged_exhaust_again")
        a_list.append("atm_theft_police")
        a_list.append("heart_condition_flare")
        a_list.append("shoulder_chronic_pain")
        a_list.append("shoulder_painkiller_addiction")
        a_list.append("painkiller_withdrawal")
        a_list.append("painkiller_dealer_returns")
        a_list.append("painkiller_overdose")
        a_list.append("cocaine_temptation")
        a_list.append("cocaine_crash")
        a_list.append("cocaine_heart_attack")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("soulless_recognition")
        a_list.append("burn_scars_stares")
        a_list.append("burn_scars_infection")
        a_list.append("weakened_immune_cold")
        a_list.append("weakened_immune_pneumonia")
        a_list.append("unpaid_tickets_boot")
        a_list.append("booted_car_impound")
        a_list.append("mystery_car_problem_worsens")
        a_list.append("stray_cat_sick")
        a_list.append("stray_cat_has_kittens")
        a_list.append("bridge_angel_returns")
        a_list.append("call_bridge_angel")
        # Random Small Events
        a_list.append("found_twenty")
        a_list.append("lost_wallet")
        a_list.append("sunburn")
        a_list.append("mosquito_bite_infection")
        a_list.append("good_hair_day")
        a_list.append("bad_hair_day")
        a_list.append("found_gift_card")
        a_list.append("car_battery_dead")
        a_list.append("flat_tire_again")
        a_list.append("nice_weather")
        a_list.append("terrible_weather")
        a_list.append("weird_noise")
        a_list.append("back_pain")
        a_list.append("stretching_helps")
        a_list.append("random_kindness")
        a_list.append("random_cruelty")
        a_list.append("someone_stole_your_stuff")
        a_list.append("prayer_answered")
        a_list.append("prayer_ignored")
        a_list.append("found_old_photo")
        a_list.append("threw_out_old_photo")
        a_list.append("got_a_tan")
        # Item-Using Events
        a_list.append("mosquito_swarm")
        a_list.append("scorching_sun")
        a_list.append("sudden_downpour")
        a_list.append("freezing_night")
        a_list.append("car_smell")
        a_list.append("roadside_breakdown")
        a_list.append("broken_belonging")
        a_list.append("social_encounter")
        a_list.append("rubber_band_save")
        a_list.append("penny_luck")
        # Conditional
        a_list.append("got_a_cold")
        a_list.append("cold_gets_worse")
        # One-Time
        a_list.append("turn_to_god")
        a_list.append("hungry_cow")
        a_list.append("ice_cream_truck")
        a_list.append("kid_on_bike")
        a_list.append("lost_tourist")
        a_list.append("the_hitchhiker")
        # Conditional
        a_list.append("mayas_luck")
        # One-Time Conditional (Dreams)
        a_list.append("remember_rebecca")
        a_list.append("dealers_anger")
        a_list.append("casino_bar")
        # Secret Events
        a_list.append("deja_vu")
        a_list.append("exactly_1111")
        # NEW CREATIVE EVENTS - Cheap Tier
        a_list.append("duck_army")
        a_list.append("sentient_sandwich")
        a_list.append("motivational_raccoon")
        a_list.append("pigeon_mafia")
        a_list.append("sock_puppet_therapist")
        a_list.append("dance_battle")
        a_list.append("time_loop")
        a_list.append("mirror_stranger")
        a_list.append("the_glitch")
        a_list.append("fourth_wall_break")
        a_list.append("wrong_universe")
        a_list.append("the_collector")
        a_list.append("alien_abduction")
        a_list.append("blood_moon_bargain")
        # NEW SECRET EVENTS
        a_list.append("exactly_1234")
        a_list.append("day_palindrome")
        a_list.append("prime_day")
        a_list.append("same_as_health")
        # NON-NUMBER SECRET EVENTS
        a_list.append("the_veteran_gambler")
        a_list.append("perfect_health_moment")
        a_list.append("rock_bottom")
        a_list.append("companion_reunion")
        a_list.append("the_cat_knows")
        a_list.append("the_crow_council")
        a_list.append("insomniac_revelation")
        a_list.append("rain_on_the_roof")
        a_list.append("the_sleeping_stranger")
        random.shuffle(a_list)
        return a_list
    
    def make_cheap_night_events_list(self):
        a_list = []
        a_list.append("woodlands_river")
        a_list.append("woodlands_field")
        a_list.append("swamp_stroll")
        a_list.append("midnight_snack_run")
        a_list.append("stargazing")
        a_list.append("stray_cat_returns")
        a_list.append("midnight_walk")
        a_list.append("raccoon_invasion")
        a_list.append("police_checkpoint")
        a_list.append("satellite_falling")
        a_list.append("peaceful_night")
        a_list.append("insomnia_night")
        a_list.append("drowning_dream")
        a_list.append("carbon_monoxide")
        a_list.append("nice_dream")
        a_list.append("nightmare")
        # Conditional Night
        a_list.append("stray_cat_sick")
        a_list.append("stray_cat_dies")
        a_list.append("stray_cat_has_kittens")
        # One-Time Conditional (Suzy)
        a_list.append("whats_my_favorite_color")
        # One-Time (Rabbit)
        a_list.append("chase_the_second_rabbit")
        random.shuffle(a_list)
        return a_list
    
# Modest Events (10,000 - 100,000)
    def make_modest_day_events_list(self):
        a_list = []
        # Everytime
        a_list.append("left_door_open")
        a_list.append("fancy_coffee")
        a_list.append("parking_ticket")
        a_list.append("found_phone")
        a_list.append("street_performer_duel")
        a_list.append("compliment_stranger")
        a_list.append("forgotten_birthday")
        a_list.append("book_club_invite")
        a_list.append("car_compliment")
        a_list.append("dog_walker_collision")
        a_list.append("coffee_shop_philosopher")
        a_list.append("food_truck_festival")
        # Deadly Events
        a_list.append("back_alley_shortcut")
        a_list.append("gas_station_robbery")
        a_list.append("heart_attack_scare")
        a_list.append("drug_dealer_encounter")
        # MEDICAL EVENTS - Modest Tier
        a_list.append("contract_pneumonia")
        a_list.append("contract_shingles")
        a_list.append("contract_lyme_disease")
        a_list.append("contract_tetanus")
        a_list.append("contract_rabies_scare")
        a_list.append("develop_diabetes_symptoms")
        a_list.append("high_blood_pressure_crisis")
        a_list.append("severe_allergic_reaction")
        a_list.append("kidney_stones")
        a_list.append("gallbladder_attack")
        a_list.append("appendicitis_attack")
        a_list.append("blood_clot_in_leg")
        a_list.append("seizure_episode")
        a_list.append("pancreatitis_attack")
        a_list.append("blood_poisoning")
        a_list.append("asbestos_exposure")
        a_list.append("mercury_poisoning")
        a_list.append("dental_disaster")
        a_list.append("allergic_reaction_restaurant")
        a_list.append("wasp_nest_encounter")
        a_list.append("gym_collapse")
        a_list.append("ptsd_flashback")
        # INJURY EVENTS - Modest Tier
        a_list.append("severe_burn_injury")
        a_list.append("broken_collarbone")
        a_list.append("torn_acl")
        a_list.append("herniated_disc")
        a_list.append("puncture_wound")
        a_list.append("frostbite")
        a_list.append("heat_stroke")
        a_list.append("hypothermia")
        a_list.append("chemical_burn")
        a_list.append("electrical_burn")
        a_list.append("jaw_fracture")
        a_list.append("orbital_fracture")
        a_list.append("nerve_damage")
        a_list.append("tendon_rupture")
        a_list.append("muscle_tear")
        a_list.append("motorcycle_crash")
        a_list.append("pool_diving_accident")
        a_list.append("chemical_spill")
        a_list.append("workplace_injury")
        a_list.append("caught_in_fire")
        a_list.append("frozen_outdoors")
        a_list.append("heat_exhaustion_collapse")
        a_list.append("mma_fight_aftermath")
        # Conditional Deadly
        a_list.append("knife_wound_infection")
        a_list.append("gut_wound_complications")
        a_list.append("bridge_contemplation")
        a_list.append("dog_bite_rabies_scare")
        a_list.append("fuel_leak_fire")
        a_list.append("fuel_leak_fixed")
        a_list.append("heart_condition_flare")
        a_list.append("shoulder_chronic_pain")
        a_list.append("shoulder_painkiller_addiction")
        a_list.append("painkiller_withdrawal")
        a_list.append("painkiller_dealer_returns")
        a_list.append("painkiller_overdose")
        a_list.append("cocaine_temptation")
        a_list.append("cocaine_crash")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("soulless_recognition")
        a_list.append("burn_scars_stares")
        a_list.append("burn_scars_infection")
        a_list.append("weakened_immune_cold")
        a_list.append("weakened_immune_pneumonia")
        a_list.append("unpaid_tickets_boot")
        a_list.append("booted_car_impound")
        a_list.append("mystery_car_problem_worsens")
        a_list.append("stray_cat_sick")
        a_list.append("stray_cat_has_kittens")
        a_list.append("bridge_angel_returns")
        a_list.append("call_bridge_angel")
        a_list.append("gas_station_hero_recognized")
        a_list.append("gas_station_hero_interview")
        a_list.append("old_rival_encounter")
        a_list.append("media_known_harassed")
        a_list.append("media_known_documentary")
        # Random Small Events
        a_list.append("found_twenty")
        a_list.append("lost_wallet")
        a_list.append("sunburn")
        a_list.append("good_hair_day")
        a_list.append("bad_hair_day")
        a_list.append("nice_weather")
        a_list.append("terrible_weather")
        a_list.append("back_pain")
        a_list.append("stretching_helps")
        a_list.append("random_kindness")
        a_list.append("random_cruelty")
        a_list.append("prayer_answered")
        a_list.append("prayer_ignored")
        # One-Time
        a_list.append("the_prophet")
        # Conditional
        a_list.append("unpaid_ticket_consequence")
        a_list.append("mayas_luck")
        a_list.append("street_performer")
        a_list.append("power_outage_area")
        a_list.append("construction_noise")
        # Item-Using Events
        a_list.append("important_document")
        a_list.append("caught_fishing")
        a_list.append("robbery_attempt")
        a_list.append("photo_opportunity")
        a_list.append("need_fire")
        # Conditional
        a_list.append("another_spider_bite")
        a_list.append("squirrel_invasion")
        a_list.append("homeless_network")
        # One-Time
        a_list.append("the_photographer")
        a_list.append("the_food_truck")
        # One-Time Conditional
        a_list.append("further_interrogation")
        # One-Time Conditional (Dreams)
        a_list.append("remember_nathan")
        a_list.append("dealers_scar")
        a_list.append("casino_table")
        # Secret Events
        a_list.append("exactly_50000")
        # NEW CREATIVE EVENTS - Modest Tier
        a_list.append("duck_army")
        a_list.append("sentient_sandwich")
        a_list.append("motivational_raccoon")
        a_list.append("pigeon_mafia")
        a_list.append("dance_battle")
        a_list.append("time_loop")
        a_list.append("mirror_stranger")
        a_list.append("the_glitch")
        a_list.append("fourth_wall_break")
        a_list.append("wrong_universe")
        a_list.append("the_collector")
        a_list.append("the_empty_room")
        a_list.append("alien_abduction")
        a_list.append("blood_moon_bargain")
        # NEW SECRET EVENTS
        a_list.append("exactly_69420")
        a_list.append("day_palindrome")
        a_list.append("prime_day")
        # NON-NUMBER SECRET EVENTS
        a_list.append("the_veteran_gambler")
        a_list.append("perfect_health_moment")
        a_list.append("companion_reunion")
        a_list.append("haunted_by_losses")
        a_list.append("the_cat_knows")
        a_list.append("the_crow_council")
        a_list.append("insomniac_revelation")
        a_list.append("item_hoarder")
        a_list.append("rain_on_the_roof")
        random.shuffle(a_list)
        return a_list
    
    def make_modest_night_events_list(self):
        a_list = []
        a_list.append("swamp_wade")
        a_list.append("swamp_swim")
        a_list.append("beach_stroll")
        a_list.append("mysterious_lights")
        a_list.append("midnight_snack_run")
        a_list.append("midnight_walk")
        a_list.append("peaceful_night")
        a_list.append("insomnia_night")
        a_list.append("nightmare_of_losing")
        a_list.append("dream_of_winning")
        a_list.append("drowning_dream")
        a_list.append("nice_dream")
        a_list.append("nightmare")
        # Conditional Night
        a_list.append("stray_cat_has_kittens")
        # One-Time (Rabbit)
        a_list.append("chase_the_third_rabbit")
        random.shuffle(a_list)
        return a_list
    

# Rich Events (100,000 - 500,000)
    def make_rich_day_events_list(self):
        a_list = []
        # Everytime
        a_list.append("left_trunk_open")
        a_list.append("luxury_car_passes")
        a_list.append("paparazzi_mistake")
        a_list.append("luxury_problems")
        a_list.append("imposter_syndrome")
        a_list.append("charity_opportunity")
        a_list.append("investment_opportunity")
        a_list.append("expensive_taste")
        a_list.append("news_van")
        a_list.append("fancy_restaurant_mistake")
        a_list.append("autograph_request")
        a_list.append("casino_regular")
        a_list.append("mysterious_package")
        a_list.append("rich_persons_problems")
        a_list.append("investment_pitch")
        # Deadly Events
        a_list.append("back_alley_shortcut")
        a_list.append("heart_attack_scare")
        a_list.append("drug_dealer_encounter")
        a_list.append("car_explosion")
        # MEDICAL EVENTS - Rich Tier
        a_list.append("contract_measles")
        a_list.append("skull_fracture")
        a_list.append("collapsed_lung")
        a_list.append("ruptured_spleen")
        a_list.append("liver_laceration")
        a_list.append("detached_retina")
        a_list.append("crush_injury")
        a_list.append("gangrene_infection")
        a_list.append("drug_overdose_survival")
        a_list.append("botched_surgery")
        a_list.append("covid_complications")
        a_list.append("earthquake_injury")
        a_list.append("carnival_ride_accident")
        a_list.append("window_crash")
        a_list.append("explosion_nearby")
        a_list.append("coma_awakening")
        a_list.append("prison_shiv_wound")
        a_list.append("bad_mushrooms")
        # Conditional Deadly
        a_list.append("knife_wound_infection")
        a_list.append("gut_wound_complications")
        a_list.append("bridge_contemplation")
        a_list.append("heart_condition_flare")
        a_list.append("shoulder_chronic_pain")
        a_list.append("painkiller_withdrawal")
        a_list.append("painkiller_dealer_returns")
        a_list.append("painkiller_overdose")
        a_list.append("cocaine_temptation")
        a_list.append("cocaine_crash")
        a_list.append("cocaine_heart_attack")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("soulless_recognition")
        a_list.append("burn_scars_stares")
        a_list.append("weakened_immune_cold")
        a_list.append("weakened_immune_pneumonia")
        a_list.append("mystery_car_problem_worsens")
        a_list.append("bridge_angel_returns")
        a_list.append("call_bridge_angel")
        a_list.append("gas_station_hero_recognized")
        a_list.append("gas_station_hero_interview")
        a_list.append("old_rival_encounter")
        a_list.append("media_known_harassed")
        a_list.append("media_known_documentary")
        a_list.append("high_roller_room_visit")
        a_list.append("high_roller_whale")
        # Random Small Events
        a_list.append("found_twenty")
        a_list.append("lost_wallet")
        a_list.append("good_hair_day")
        a_list.append("bad_hair_day")
        a_list.append("nice_weather")
        a_list.append("terrible_weather")
        a_list.append("back_pain")
        a_list.append("stretching_helps")
        a_list.append("prayer_answered")
        a_list.append("prayer_ignored")
        # Item-Using Events (Premium)
        a_list.append("classy_encounter")
        a_list.append("wine_and_dine")
        a_list.append("cigar_circle")
        a_list.append("lucky_rabbit_encounter")
        # Conditional
        a_list.append("rat_bite")
        a_list.append("hungry_termites")
        a_list.append("wealth_anxiety")
        a_list.append("tax_man")
        # One-Time
        a_list.append("the_rival")
        a_list.append("the_bodyguard_offer")
        a_list.append("high_roller_invitation")
        a_list.append("old_friend_recognition")
        a_list.append("grimy_gus_discovery")
        a_list.append("the_gambler_ghost")
        # One-Time Conditional
        a_list.append("starving_cow")
        # Secret Events
        a_list.append("exactly_250000")
        a_list.append("dealer_in_dreams")
        random.shuffle(a_list)
        return a_list
    
    def make_rich_night_events_list(self):
        a_list = []
        a_list.append("beach_swim")
        a_list.append("beach_dive")
        a_list.append("city_streets")
        a_list.append("late_night_radio")
        a_list.append("mysterious_lights")
        a_list.append("midnight_walk")
        a_list.append("peaceful_night")
        a_list.append("insomnia_night")
        a_list.append("nightmare_of_losing")
        a_list.append("dream_of_winning")
        a_list.append("drowning_dream")
        a_list.append("nice_dream")
        a_list.append("nightmare")
        # One-Time Conditional (Suzy)
        a_list.append("whats_my_favorite_animal")
        # One-Time (Rabbit)
        a_list.append("chase_the_fourth_rabbit")
        random.shuffle(a_list)
        return a_list


# Doughman Events (500,000 - 900,000)
    def make_doughman_day_events_list(self):
        a_list = []
        # Everytime
        a_list.append("thunderstorm")
        a_list.append("high_stakes_feeling")
        a_list.append("casino_security")
        a_list.append("wealthy_doubts")
        a_list.append("people_watching")
        a_list.append("money_counting_ritual")
        a_list.append("nervous_habits")
        a_list.append("millionaire_fantasy")
        a_list.append("wealth_paranoia")
        a_list.append("high_roller_room")
        a_list.append("old_rival_returns")
        a_list.append("casino_comps")
        a_list.append("millionaire_milestone")
        # Deadly Events
        a_list.append("heart_attack_scare")
        a_list.append("drug_dealer_encounter")
        # MEDICAL EVENTS - Doughman Tier
        a_list.append("skull_fracture")
        a_list.append("collapsed_lung")
        a_list.append("ruptured_spleen")
        a_list.append("liver_laceration")
        a_list.append("detached_retina")
        a_list.append("ruptured_eardrum")
        a_list.append("gangrene_infection")
        a_list.append("drug_overdose_survival")
        a_list.append("botched_surgery")
        a_list.append("earthquake_injury")
        a_list.append("explosion_nearby")
        a_list.append("assault_aftermath")
        a_list.append("pool_diving_accident")
        a_list.append("coma_awakening")
        a_list.append("stress_breakdown")
        a_list.append("sleep_deprivation_crisis")
        # Conditional Deadly
        a_list.append("knife_wound_infection")
        a_list.append("gut_wound_complications")
        a_list.append("bridge_contemplation")
        a_list.append("devils_bargain_consequence")
        a_list.append("heart_condition_flare")
        a_list.append("painkiller_withdrawal")
        a_list.append("painkiller_dealer_returns")
        a_list.append("painkiller_overdose")
        a_list.append("cocaine_crash")
        a_list.append("cocaine_heart_attack")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("soulless_recognition")
        a_list.append("weakened_immune_pneumonia")
        a_list.append("bridge_angel_returns")
        a_list.append("call_bridge_angel")
        a_list.append("old_rival_encounter")
        a_list.append("media_known_harassed")
        a_list.append("media_known_documentary")
        a_list.append("high_roller_room_visit")
        a_list.append("high_roller_whale")
        # Random Small Events
        a_list.append("good_hair_day")
        a_list.append("bad_hair_day")
        a_list.append("nice_weather")
        a_list.append("terrible_weather")
        a_list.append("prayer_answered")
        a_list.append("prayer_ignored")
        # Conditional
        a_list.append("the_temptation")
        # One-Time Events
        a_list.append("likely_death")
        a_list.append("the_veteran")
        a_list.append("the_journalist")
        a_list.append("the_offer_refused")
        a_list.append("the_doppelganger")
        # One-Time Conditional
        a_list.append("even_further_interrogation")
        # One-Time Conditional (Dreams)
        a_list.append("remember_johnathan")
        a_list.append("dealers_revolver")
        a_list.append("casino_riches")
        # Secret Events
        a_list.append("exactly_777777")
        # NEW CREATIVE EVENTS - Doughman Tier
        a_list.append("time_loop")
        a_list.append("mirror_stranger")
        a_list.append("the_glitch")
        a_list.append("fourth_wall_break")
        a_list.append("the_collector")
        a_list.append("the_empty_room")
        a_list.append("blood_moon_bargain")
        # NEW SECRET EVENTS
        a_list.append("exactly_7777")
        a_list.append("day_palindrome")
        a_list.append("prime_day")
        a_list.append("full_moon_madness")
        # NON-NUMBER SECRET EVENTS
        a_list.append("the_veteran_gambler")
        a_list.append("companion_reunion")
        a_list.append("haunted_by_losses")
        a_list.append("the_crow_council")
        a_list.append("insomniac_revelation")
        a_list.append("item_hoarder")
        a_list.append("birthday_forgotten")
        a_list.append("rain_on_the_roof")
        # DRASTIC DOUGHMAN EVENTS - Violence/Medical/Mental Health
        a_list.append("loan_shark_visit")
        a_list.append("the_desperate_gambler")
        a_list.append("withdrawal_nightmare")
        a_list.append("organ_harvester")
        a_list.append("casino_overdose")
        a_list.append("cancer_diagnosis")
        a_list.append("the_bridge_call")
        a_list.append("the_relapse")
        a_list.append("the_confession")
        a_list.append("the_high_roller_suicide")
        a_list.append("the_dying_dealer")
        # MORE SECRET EVENTS
        a_list.append("the_anniversary_loss")
        a_list.append("survivor_guilt")
        a_list.append("the_scar_story")
        a_list.append("the_winning_streak_paranoia")
        a_list.append("old_gambling_buddy")
        random.shuffle(a_list)
        return a_list
    
    def make_doughman_night_events_list(self):
        a_list = []
        a_list.append("city_stroll")
        a_list.append("city_park")
        a_list.append("midnight_walk")
        a_list.append("peaceful_night")
        a_list.append("insomnia_night")
        a_list.append("nightmare_of_losing")
        a_list.append("dream_of_winning")
        a_list.append("drowning_dream")
        a_list.append("nice_dream")
        a_list.append("nightmare")
        # One-Time (Rabbit)
        a_list.append("chase_the_fifth_rabbit")
        random.shuffle(a_list)
        return a_list

# Nearly There Events (900,000 +)
    def make_nearly_day_events_list(self):
        a_list = []
        # Everytime
        a_list.append("almost_there")
        a_list.append("the_weight_of_wealth")
        a_list.append("casino_knows")
        a_list.append("last_stretch")
        a_list.append("strange_visitors")
        a_list.append("the_final_temptation")
        a_list.append("reporters_found_you")
        a_list.append("casino_owner_meeting")
        # Deadly Events
        a_list.append("heart_attack_scare")
        # MEDICAL EVENTS - Nearly Tier (Severe, Life-Threatening)
        a_list.append("skull_fracture")
        a_list.append("liver_laceration")
        a_list.append("ruptured_spleen")
        a_list.append("collapsed_lung")
        a_list.append("crush_injury")
        a_list.append("gangrene_infection")
        a_list.append("blood_poisoning")
        a_list.append("drug_overdose_survival")
        a_list.append("botched_surgery")
        a_list.append("explosion_nearby")
        a_list.append("assault_aftermath")
        a_list.append("coma_awakening")
        a_list.append("stress_breakdown")
        a_list.append("sleep_deprivation_crisis")
        a_list.append("trauma_flashback")
        # Conditional Deadly
        a_list.append("knife_wound_infection")
        a_list.append("gut_wound_complications")
        a_list.append("bridge_contemplation")
        a_list.append("devils_bargain_consequence")
        a_list.append("heart_condition_flare")
        a_list.append("painkiller_overdose")
        a_list.append("cocaine_heart_attack")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("soulless_recognition")
        a_list.append("call_bridge_angel")
        a_list.append("media_known_documentary")
        a_list.append("high_roller_room_visit")
        a_list.append("high_roller_whale")
        # Random Small Events
        a_list.append("prayer_answered")
        a_list.append("prayer_ignored")
        # Conditional
        a_list.append("too_close_to_quit")
        a_list.append("victoria_returns")
        # One-Time
        a_list.append("the_warning")
        a_list.append("the_celebration")
        a_list.append("final_dream")
        a_list.append("the_offer")
        # One-Time Conditional
        a_list.append("cow_army")
        a_list.append("final_interrogation")
        # One-Time Conditional (Suzy Finale)
        a_list.append("gift_from_suzy")
        # Secret Events
        a_list.append("exactly_999999")
        a_list.append("all_dreams_complete")
        # NEW CREATIVE EVENTS - Nearly There Tier
        a_list.append("the_glitch")
        a_list.append("fourth_wall_break")
        a_list.append("the_collector")
        a_list.append("the_empty_room")
        a_list.append("blood_moon_bargain")
        # NEW SECRET EVENTS
        a_list.append("day_palindrome")
        a_list.append("prime_day")
        a_list.append("full_moon_madness")
        # NON-NUMBER SECRET EVENTS
        a_list.append("the_veteran_gambler")
        a_list.append("companion_reunion")
        a_list.append("haunted_by_losses")
        a_list.append("insomniac_revelation")
        a_list.append("item_hoarder")
        a_list.append("birthday_forgotten")
        a_list.append("rain_on_the_roof")
        # DRASTIC NEARLY THERE EVENTS - Violence/Medical/Mental Health/Death
        a_list.append("loan_shark_visit")
        a_list.append("the_desperate_gambler")
        a_list.append("withdrawal_nightmare")
        a_list.append("casino_overdose")
        a_list.append("cancer_diagnosis")
        a_list.append("the_bridge_call")
        a_list.append("the_relapse")
        a_list.append("casino_hitman")
        a_list.append("the_confession")
        a_list.append("the_high_roller_suicide")
        a_list.append("the_dying_dealer")
        # MORE SECRET EVENTS
        a_list.append("the_anniversary_loss")
        a_list.append("survivor_guilt")
        a_list.append("the_scar_story")
        a_list.append("the_winning_streak_paranoia")
        a_list.append("old_gambling_buddy")
        random.shuffle(a_list)
        return a_list
    
    def make_nearly_night_events_list(self):
        a_list = []
        a_list.append("woodlands_adventure")
        a_list.append("swamp_adventure")
        a_list.append("beach_adventure")
        a_list.append("underwater_adventure")
        a_list.append("city_adventure")
        a_list.append("midnight_walk")
        a_list.append("peaceful_night")
        a_list.append("insomnia_night")
        a_list.append("nightmare_of_losing")
        a_list.append("dream_of_winning")
        a_list.append("drowning_dream")
        a_list.append("nice_dream")
        a_list.append("nightmare")
        # One-Time (Rabbit Finale)
        a_list.append("chase_the_last_rabbit")
        random.shuffle(a_list)
        return a_list
    
# Get Event
    def get_day_event(self):
        rank = self.__player.get_rank()
        match rank:
            case 0:
                if len(self.__poor_day_events)==0:
                    self.__poor_day_events = self.make_poor_day_events_list()
                return self.__poor_day_events.pop()
            case 1:
                if len(self.__cheap_day_events)==0:
                    self.__cheap_day_events = self.make_cheap_day_events_list()
                return self.__cheap_day_events.pop()
            case 2:
                if len(self.__modest_day_events)==0:
                    self.__modest_day_events = self.make_modest_day_events_list()
                return self.__modest_day_events.pop()
            case 3:
                if len(self.__rich_day_events)==0:
                    self.__rich_day_events = self.make_rich_day_events_list()
                return self.__rich_day_events.pop()
            case 4:
                if len(self.__doughman_day_events)==0:
                    self.__doughman_day_events = self.make_doughman_day_events_list()
                return self.__doughman_day_events.pop()
            case 5:
                if len(self.__nearly_day_events)==0:
                    self.__nearly_day_events = self.make_nearly_day_events_list()
                return self.__nearly_day_events.pop()
    

    def get_night_event(self):
        rank = self.__player.get_rank()
        match rank:
            case 0:
                if len(self.__poor_night_events)==0:
                    self.__poor_night_events = self.make_poor_night_events_list()
                return self.__poor_night_events.pop()
            case 1:
                if len(self.__cheap_night_events)==0:
                    self.__cheap_night_events = self.make_cheap_night_events_list()
                return self.__cheap_night_events.pop()
            case 2:
                if len(self.__modest_night_events)==0:
                    self.__modest_night_events = self.make_modest_night_events_list()
                return self.__modest_night_events.pop()
            case 3:
                if len(self.__rich_night_events)==0:
                    self.__rich_night_events = self.make_rich_night_events_list()
                return self.__rich_night_events.pop()
            case 4:
                if len(self.__doughman_night_events)==0:
                    self.__doughman_night_events = self.make_doughman_night_events_list()
                return self.__doughman_night_events.pop()
            case 5:
                if len(self.__nearly_night_events)==0:
                    self.__nearly_night_events = self.make_nearly_night_events_list()
                return self.__nearly_night_events.pop()

    def make_shop_list(self):
        a_list = []
        if(not self.__player.has_danger("Doctor Ban")):
            a_list.append("Doctor's Office")
        if(self.__player.has_met("Witch")):
            a_list.append("Witch Doctor's Tower")
        if(self.__player.has_met("Tom")):
            a_list.append("Trusty Tom's Trucks and Tires")
        if(self.__player.has_met("Frank")):
            a_list.append("Filthy Frank's Flawless Fixtures")
        if(self.__player.has_met("Oswald")):
            a_list.append("Oswald's Optimal Outoparts")
        a_list.append("Convenience Store")
        if(self.__player.has_item("Map")):
            a_list.append("Marvin's Mystical Merchandise")
        # Pawn Shop - unlocked by meeting Grimy Gus
        if(self.__player.has_met("Grimy Gus")):
            a_list.append("Grimy Gus's Pawn Emporium")
        # Loan Shark - unlocked by meeting Vinnie or owing money
        if(self.__player.has_met("Vinnie") or self.__player.get_loan_shark_debt() > 0):
            a_list.append("Vinnie's Back Alley Loans")
        # Phone calls - only show if you have at least one number
        if(self.__player.has_item("Grandma's Number") or 
           self.__player.has_item("Beach Romance Number") or 
           self.__player.has_item("Rich Friend's Number")):
            a_list.append("Make a Phone Call")
        # Airport unlocks when you're a millionaire
        if(self.__player.get_balance() >= 1000000):
            a_list.append("Airport")
        return a_list

    def make_convenience_store_inventory(self):
        a_list = []
        rank = self.__player.get_rank()
        
        # === FOOD ITEMS (Always available, rotating selection) ===
        food_items = [
            ("Candy Bar", 5), ("Bag of Chips", 8), ("Turkey Sandwich", 15),
            ("Energy Drink", 12), ("Beef Jerky", 10), ("Cup Noodles", 7),
            ("Granola Bar", 6), ("Hot Dog", 8), ("Microwave Burrito", 9)
        ]
        random.shuffle(food_items)
        for i in range(min(3, len(food_items))):  # 3 random food items
            a_list.append(food_items[i])
        
        # === COMMON ITEMS (Always available) ===
        if not self.__player.has_item("Pest Control"):
            a_list.append(("Pest Control", 25))
        if not self.__player.has_item("Deck of Cards"):
            a_list.append(("Deck of Cards", 9))
        
        # === UNCOMMON ITEMS (Random chance to appear) ===
        if random.randrange(3) == 0 and not self.__player.has_item("Cough Drops"):
            a_list.append(("Cough Drops", 15))
        if random.randrange(3) == 0 and not self.__player.has_item("Dog Treat"):
            a_list.append(("Dog Treat", 8))
        if random.randrange(4) == 0 and not self.__player.has_item("Spare Tire"):
            a_list.append(("Spare Tire", 75))
        if random.randrange(3) == 0 and not self.__player.has_item("Flashlight"):
            a_list.append(("Flashlight", 20))
        if random.randrange(3) == 0 and not self.__player.has_item("First Aid Kit"):
            a_list.append(("First Aid Kit", 45))
        if random.randrange(4) == 0 and not self.__player.has_item("Umbrella"):
            a_list.append(("Umbrella", 18))
        if random.randrange(4) == 0 and not self.__player.has_item("Sunglasses"):
            a_list.append(("Sunglasses", 22))
        if random.randrange(5) == 0 and not self.__player.has_item("Lighter"):
            a_list.append(("Lighter", 5))
        if random.randrange(4) == 0 and not self.__player.has_item("Duct Tape"):
            a_list.append(("Duct Tape", 12))
        if random.randrange(5) == 0 and not self.__player.has_item("Pocket Knife"):
            a_list.append(("Pocket Knife", 35))
        
        # === RANK 0 (Poor): Basic survival items ===
        if rank == 0:
            if random.randrange(3) == 0 and not self.__player.has_item("Lottery Ticket"):
                a_list.append(("Lottery Ticket", 5))
            if random.randrange(4) == 0 and not self.__player.has_item("Lucky Penny"):
                a_list.append(("Lucky Penny", 1))
            if random.randrange(3) == 0 and not self.__player.has_item("Cheap Sunscreen"):
                a_list.append(("Cheap Sunscreen", 8))
            if random.randrange(4) == 0 and not self.__player.has_item("Plastic Poncho"):
                a_list.append(("Plastic Poncho", 6))
            if random.randrange(3) == 0 and not self.__player.has_item("Breath Mints"):
                a_list.append(("Breath Mints", 3))
            if random.randrange(4) == 0 and not self.__player.has_item("Rubber Bands"):
                a_list.append(("Rubber Bands", 2))
        
        # === RANK 1 (Cheap): More options ===
        if rank == 1:
            if random.randrange(3) == 0 and not self.__player.has_item("Bag of Acorns"):
                a_list.append(("Bag of Acorns", 10))
            if random.randrange(5) == 0 and not self.__player.has_item("Necronomicon"):
                a_list.append(("Necronomicon", 666))  # TRAP ITEM
            if random.randrange(4) == 0 and not self.__player.has_item("Can of Tuna"):
                a_list.append(("Can of Tuna", 8))
            if random.randrange(3) == 0 and not self.__player.has_item("Bug Spray"):
                a_list.append(("Bug Spray", 15))
            if random.randrange(4) == 0 and not self.__player.has_item("Disposable Camera"):
                a_list.append(("Disposable Camera", 20))
            if random.randrange(3) == 0 and not self.__player.has_item("Road Flares"):
                a_list.append(("Road Flares", 25))
            if random.randrange(4) == 0 and not self.__player.has_item("Air Freshener"):
                a_list.append(("Air Freshener", 7))
        
        # === RANK 2 (Modest): Quality items ===
        if rank == 2:
            if random.randrange(3) == 0 and not self.__player.has_item("LifeAlert"):
                a_list.append(("LifeAlert", 120))
            if random.randrange(4) == 0 and not self.__player.has_item("Binoculars"):
                a_list.append(("Binoculars", 65))
            if random.randrange(4) == 0 and not self.__player.has_item("Lettuce"):
                a_list.append(("Lettuce", 4))
            if random.randrange(3) == 0 and not self.__player.has_item("Padlock"):
                a_list.append(("Padlock", 30))
            if random.randrange(4) == 0 and not self.__player.has_item("Fishing Line"):
                a_list.append(("Fishing Line", 18))
            if random.randrange(3) == 0 and not self.__player.has_item("Super Glue"):
                a_list.append(("Super Glue", 12))
            if random.randrange(4) == 0 and not self.__player.has_item("Hand Warmers"):
                a_list.append(("Hand Warmers", 10))
        
        # === RANK 3 (Rich): Premium items ===
        if rank == 3:
            if random.randrange(3) == 0 and not self.__player.has_item("Expensive Cologne"):
                a_list.append(("Expensive Cologne", 150))
            if random.randrange(4) == 0 and not self.__player.has_item("Fancy Cigars"):
                a_list.append(("Fancy Cigars", 200))
            if random.randrange(5) == 0 and not self.__player.has_item("Gold Chain"):
                a_list.append(("Gold Chain", 500))
            if random.randrange(3) == 0 and not self.__player.has_item("Leather Gloves"):
                a_list.append(("Leather Gloves", 180))
            if random.randrange(4) == 0 and not self.__player.has_item("Silver Flask"):
                a_list.append(("Silver Flask", 250))
            if random.randrange(4) == 0 and not self.__player.has_item("Fancy Pen"):
                a_list.append(("Fancy Pen", 120))
        
        # === RANK 4+ (Doughman/Nearly): Exclusive items ===
        if rank >= 4:
            if random.randrange(3) == 0 and not self.__player.has_item("Vintage Wine"):
                a_list.append(("Vintage Wine", 800))
            if random.randrange(4) == 0 and not self.__player.has_item("Lucky Rabbit Foot"):
                a_list.append(("Lucky Rabbit Foot", 1000))
            if random.randrange(5) == 0 and not self.__player.has_item("Cursed Coin"):
                a_list.append(("Cursed Coin", 13))  # TRAP ITEM - cheap but cursed
            if random.randrange(3) == 0 and not self.__player.has_item("Silk Handkerchief"):
                a_list.append(("Silk Handkerchief", 350))
            if random.randrange(4) == 0 and not self.__player.has_item("Monogrammed Lighter"):
                a_list.append(("Monogrammed Lighter", 500))
            if random.randrange(5) == 0 and not self.__player.has_item("Antique Pocket Watch"):
                a_list.append(("Antique Pocket Watch", 1200))
        
        # === CAR MAINTENANCE ITEMS (Available at all ranks, varying chances) ===
        # Battery/Electrical
        if random.randrange(5) == 0 and not self.__player.has_item("Jumper Cables"):
            a_list.append(("Jumper Cables", 45))
        if random.randrange(6) == 0 and not self.__player.has_item("Portable Battery Charger"):
            a_list.append(("Portable Battery Charger", 120))
        if random.randrange(8) == 0 and not self.__player.has_item("Spare Fuses"):
            a_list.append(("Spare Fuses", 15))
        if random.randrange(10) == 0 and not self.__player.has_item("Spare Headlight Bulbs"):
            a_list.append(("Spare Headlight Bulbs", 25))
        
        # Fluids
        if random.randrange(4) == 0 and not self.__player.has_item("Motor Oil"):
            a_list.append(("Motor Oil", 30))
        if random.randrange(5) == 0 and not self.__player.has_item("Coolant"):
            a_list.append(("Coolant", 20))
        if random.randrange(5) == 0 and not self.__player.has_item("Brake Fluid"):
            a_list.append(("Brake Fluid", 15))
        if random.randrange(6) == 0 and not self.__player.has_item("Power Steering Fluid"):
            a_list.append(("Power Steering Fluid", 18))
        if random.randrange(6) == 0 and not self.__player.has_item("Transmission Fluid"):
            a_list.append(("Transmission Fluid", 25))
        if random.randrange(5) == 0 and not self.__player.has_item("Water Bottles"):
            a_list.append(("Water Bottles", 8))
        
        # Tire/Wheel
        if random.randrange(6) == 0 and not self.__player.has_item("Fix-a-Flat"):
            a_list.append(("Fix-a-Flat", 15))
        if random.randrange(7) == 0 and not self.__player.has_item("Tire Patch Kit"):
            a_list.append(("Tire Patch Kit", 25))
        if random.randrange(8) == 0 and not self.__player.has_item("Car Jack"):
            a_list.append(("Car Jack", 65))
        
        # Emergency/Repair
        if random.randrange(6) == 0 and not self.__player.has_item("Gas Can"):
            a_list.append(("Gas Can", 25))
        if random.randrange(7) == 0 and not self.__player.has_item("Tool Kit"):
            a_list.append(("Tool Kit", 85))
        if random.randrange(5) == 0 and not self.__player.has_item("WD-40"):
            a_list.append(("WD-40", 12))
        if random.randrange(6) == 0 and not self.__player.has_item("Bungee Cords"):
            a_list.append(("Bungee Cords", 15))
        if random.randrange(7) == 0 and not self.__player.has_item("Rope"):
            a_list.append(("Rope", 20))
        if random.randrange(8) == 0 and not self.__player.has_item("Exhaust Tape"):
            a_list.append(("Exhaust Tape", 18))
        if random.randrange(9) == 0 and not self.__player.has_item("Radiator Stop Leak"):
            a_list.append(("Radiator Stop Leak", 22))
        if random.randrange(9) == 0 and not self.__player.has_item("Oil Stop Leak"):
            a_list.append(("Oil Stop Leak", 20))
        
        # Cold Weather Items
        if random.randrange(8) == 0 and not self.__player.has_item("Lock De-Icer"):
            a_list.append(("Lock De-Icer", 8))
        if random.randrange(10) == 0 and not self.__player.has_item("Fuel Line Antifreeze"):
            a_list.append(("Fuel Line Antifreeze", 12))
        
        # Window/Cover Items
        if random.randrange(4) == 0 and not self.__player.has_item("Garbage Bag"):
            a_list.append(("Garbage Bag", 3))
        if random.randrange(6) == 0 and not self.__player.has_item("Plastic Wrap"):
            a_list.append(("Plastic Wrap", 5))
        
        # Advanced Parts (rarer, more expensive)
        if random.randrange(12) == 0 and not self.__player.has_item("OBD Scanner"):
            a_list.append(("OBD Scanner", 150))
        if random.randrange(15) == 0 and not self.__player.has_item("Spare Spark Plugs"):
            a_list.append(("Spare Spark Plugs", 35))
        if random.randrange(18) == 0 and not self.__player.has_item("Serpentine Belt"):
            a_list.append(("Serpentine Belt", 55))
        if random.randrange(15) == 0 and not self.__player.has_item("Fuel Filter"):
            a_list.append(("Fuel Filter", 25))
        if random.randrange(20) == 0 and not self.__player.has_item("Thermostat"):
            a_list.append(("Thermostat", 30))
        if random.randrange(25) == 0 and not self.__player.has_item("Brake Pads"):
            a_list.append(("Brake Pads", 85))
        
        # === RARE SPECIAL ITEMS (Very low chance, any rank) ===
        if random.randrange(20) == 0 and not self.__player.has_item("Mysterious Envelope"):
            a_list.append(("Mysterious Envelope", 50))
        if random.randrange(25) == 0 and not self.__player.has_item("Old Photograph"):
            a_list.append(("Old Photograph", 25))
        if random.randrange(30) == 0 and not self.__player.has_item("Broken Compass"):
            a_list.append(("Broken Compass", 15))
        
        random.shuffle(a_list)
        return a_list
    
    def make_witch_inventory(self):
        a_list = []
        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("No Bust")):
            a_list.append("No Bust")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Imminent Blackjack")):
            a_list.append("Imminent Blackjack")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Dealer's Whispers")):
            a_list.append("Dealer's Whispers")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Bonus Fortune")):
            a_list.append("Bonus Fortune")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Anti-Venom")):
            a_list.append("Anti-Venom")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Anti-Virus")):
            a_list.append("Anti-Virus")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Fortunate Day")):
            a_list.append("Fortunate Day")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Fortunate Night")):
            a_list.append("Fortunate Night")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Second Chance")):
            a_list.append("Second Chance")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Split Serum")):
            a_list.append("Split Serum")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Dealer's Hesitation")):
            a_list.append("Dealer's Hesitation")

        random_chance = random.randrange(3)
        if(random_chance < 2) and (not self.__player.has_flask_effect("Pocket Aces")):
            a_list.append("Pocket Aces")

        return a_list

    def make_broken_items_list(self):
        a_list = []
        if(self.__player.has_broken_item("Delight Indicator")):
            a_list.append("Delight Indicator")
        if(self.__player.has_broken_item("Health Indicator")):
            a_list.append("Health Indicator")
        if(self.__player.has_broken_item("Dirty Old Hat")):
            a_list.append("Dirty Old Hat")
        if(self.__player.has_broken_item("Golden Watch")):
            a_list.append("Golden Watch")
        if(self.__player.has_broken_item("Faulty Insurance")):
            a_list.append("Faulty Insurance")
        if(self.__player.has_broken_item("Sneaky Peeky Shades")):
            a_list.append("Sneaky Peeky Shades")
        if(self.__player.has_broken_item("Quiet Sneakers")):
            a_list.append("Quiet Sneakers")
        if(self.__player.has_broken_item("Lucky Coin")):
            a_list.append("Lucky Coin")
        if(self.__player.has_broken_item("Worn Gloves")):
            a_list.append("Worn Gloves")
        if(self.__player.has_broken_item("Tattered Cloak")):
            a_list.append("Tattered Cloak")
        if(self.__player.has_broken_item("Rusty Compass")):
            a_list.append("Rusty Compass")
        if(self.__player.has_broken_item("Pocket Watch")):
            a_list.append("Pocket Watch")
        if(self.__player.has_broken_item("Gambler's Chalice")):
            a_list.append("Gambler's Chalice")
        if(self.__player.has_broken_item("Twin's Locket")):
            a_list.append("Twin's Locket")
        if(self.__player.has_broken_item("White Feather")):
            a_list.append("White Feather")
        if(self.__player.has_broken_item("Dealer's Grudge")):
            a_list.append("Dealer's Grudge")
        if(self.__player.has_broken_item("Gambler's Grimoire")):
            a_list.append("Gambler's Grimoire")
        return a_list
    
    def make_repairing_items_list(self):
        a_list = []
        if(self.__player.is_repairing_item("Delight Indicator")):
            a_list.append("Delight Indicator")
        if(self.__player.is_repairing_item("Health Indicator")):
            a_list.append("Health Indicator")
        if(self.__player.is_repairing_item("Dirty Old Hat")):
            a_list.append("Dirty Old Hat")
        if(self.__player.is_repairing_item("Golden Watch")):
            a_list.append("Golden Watch")
        if(self.__player.is_repairing_item("Faulty Insurance")):
            a_list.append("Faulty Insurance")
        if(self.__player.is_repairing_item("Sneaky Peeky Shades")):
            a_list.append("Sneaky Peeky Shades")
        if(self.__player.is_repairing_item("Quiet Sneakers")):
            a_list.append("Quiet Sneakers")
        if(self.__player.is_repairing_item("Lucky Coin")):
            a_list.append("Lucky Coin")
        if(self.__player.is_repairing_item("Worn Gloves")):
            a_list.append("Worn Gloves")
        if(self.__player.is_repairing_item("Tattered Cloak")):
            a_list.append("Tattered Cloak")
        if(self.__player.is_repairing_item("Rusty Compass")):
            a_list.append("Rusty Compass")
        if(self.__player.is_repairing_item("Pocket Watch")):
            a_list.append("Pocket Watch")
        if(self.__player.is_repairing_item("Gambler's Chalice")):
            a_list.append("Gambler's Chalice")
        if(self.__player.is_repairing_item("Twin's Locket")):
            a_list.append("Twin's Locket")
        if(self.__player.is_repairing_item("White Feather")):
            a_list.append("White Feather")
        if(self.__player.is_repairing_item("Dealer's Grudge")):
            a_list.append("Dealer's Grudge")
        if(self.__player.is_repairing_item("Gambler's Grimoire")):
            a_list.append("Gambler's Grimoire")
        return a_list

    def make_marvin_inventory(self):
        a_list = []
        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Delight Indicator")):
            a_list.append("Delight Indicator")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Health Indicator")):
            a_list.append("Health Indicator")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Dirty Old Hat")):
            a_list.append("Dirty Old Hat")
        
        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Golden Watch")):
            a_list.append("Golden Watch")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Faulty Insurance")):
            a_list.append("Faulty Insurance")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Enchanting Silver Bar")):
            a_list.append("Enchanting Silver Bar")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Sneaky Peeky Shades")):
            a_list.append("Sneaky Peeky Shades")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Quiet Sneakers")):
            a_list.append("Quiet Sneakers")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Lucky Coin")):
            a_list.append("Lucky Coin")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Worn Gloves")):
            a_list.append("Worn Gloves")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Tattered Cloak")):
            a_list.append("Tattered Cloak")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Rusty Compass")):
            a_list.append("Rusty Compass")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Pocket Watch")):
            a_list.append("Pocket Watch")

        # New mystical gambling items
        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Gambler's Chalice")) and (not self.__player.has_item("Overflowing Goblet")):
            a_list.append("Gambler's Chalice")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Twin's Locket")) and (not self.__player.has_item("Mirror of Duality")):
            a_list.append("Twin's Locket")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("White Feather")) and (not self.__player.has_item("Phoenix Feather")):
            a_list.append("White Feather")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Dealer's Grudge")) and (not self.__player.has_item("Dealer's Mercy")):
            a_list.append("Dealer's Grudge")

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Gambler's Grimoire")) and (not self.__player.has_item("Oracle's Tome")):
            a_list.append("Gambler's Grimoire")

        # SECRET ITEM - Animal Whistle (very rare, enables companion secret ending)
        random_chance = random.randrange(10)
        if (random_chance == 0) and (not self.__player.has_item("Animal Whistle")):
            a_list.append("Animal Whistle")

        random.shuffle(a_list)
        return a_list
    
    def make_marvins_adjectives_list(self):
        a_list = []
        a_list.append("stupendous")
        a_list.append("magical")
        a_list.append("majestic")
        a_list.append("superb")
        a_list.append("fantastical")
        a_list.append("all mighty")
        a_list.append("one-of-a-kind")
        a_list.append("terrific")
        a_list.append("super duper")
        a_list.append("ingenious")
        a_list.append("kinda mediocre but still awesome")
        a_list.append("never before seen")
        a_list.append("crazy wacky")
        random.shuffle(a_list)
        return a_list

    def get_marvin_adjective(self):
        if len(self.__marvins_adjectives_list) == 0:
            self.__marvins_adjectives_list = self.make_marvins_adjectives_list()
        return self.__marvins_adjectives_list.pop()
    
    def make_dealer_welcome_list(self):
        a_list = []
        a_list.append("Back again? Let's get this show on the road.")
        a_list.append("Welcome, welcome. Have a seat, and we can begin.")
        a_list.append("Come, sit down, we have a game to play.")
        a_list.append("Are you ready to play some Blackjack?")
        a_list.append("Nightfall again, huh? Well, you know what's next.")
        a_list.append("Another night. Another dance with chance.")
        a_list.append("The cards have been waiting for you.")
        a_list.append("You keep coming back. Interesting.")
        a_list.append("Sit. Let's see what fate has in store tonight.")
        a_list.append("The table is set. The cards are ready. Are you?")
        a_list.append("Night falls. The game begins.")
        a_list.append("You look... determined. Or desperate. Hard to tell.")
        a_list.append("Still alive? Good. The cards would be disappointed otherwise.")
        a_list.append("Another gambler. Another story waiting to unfold.")
        a_list.append("The casino never sleeps. Neither do you, it seems.")
        a_list.append("Take your seat. The wheel of fortune turns for no one.")
        a_list.append("You smell like daylight and poor decisions. Sit.")
        a_list.append("Back for more? The cards appreciate your persistence.")
        a_list.append("The night is young. Your wallet, however...")
        a_list.append("Ready to play? The question is always yes, isn't it?")
        a_list.append("You've got that look in your eye. Hope. Or madness. Sometimes they're the same.")
        a_list.append("The green felt remembers you. So do I.")
        a_list.append("Shuffle. Deal. Win. Lose. Repeat. Shall we?")
        a_list.append("Each night you return. Each night, the cards wait.")
        a_list.append("Welcome back to the only place that never judges your choices.")
        random.shuffle(a_list)
        return a_list
    
    def get_dealer_welcome(self):
        if len(self.__dealer_welcome_list)==0:
            self.__dealer_welcome_list = self.make_dealer_welcome_list()
        return self.__dealer_welcome_list.pop()
    
    def make_dealer_betrayal_dialogue_list(self):
        """Dealer's reactions to player selling companions - varied and haunting"""
        a_list = []
        a_list.append("You reek of it.")
        a_list.append("Betrayal. Blood. Industrial processing. The stench is unmistakable.")
        a_list.append("The cards can smell what you've done. So can I.")
        a_list.append("Fifteen souls. Ground into cubes. Packaged. Sold. Consumed.")
        a_list.append("Don't. There's nothing to say. You know what you are.")
        a_list.append("Some people play cards. Some people chase money. And some people... some people feed the machine.")
        a_list.append("The game continues. It always does. But you're not playing anymore.")
        a_list.append("You're just... existing. In the space between the factory and the table.")
        a_list.append("I've seen many things in this casino. But you... you're something different.")
        a_list.append("Every creature had a name. You remember their names, don't you?")
        a_list.append("The van comes at night. You know the schedule now. You're part of the supply chain.")
        a_list.append("Cube Processing Inc. sends their regards. And their gratitude.")
        a_list.append("They trusted you. All of them. That makes it worse, you know.")
        a_list.append("The business card in your pocket is burning a hole. You can feel it, can't you?")
        a_list.append("You've crossed a threshold most people don't even know exists.")
        random.shuffle(a_list)
        return a_list
    
    def get_dealer_betrayal_dialogue(self):
        if len(self.__dealer_betrayal_list)==0:
            self.__dealer_betrayal_list = self.make_dealer_betrayal_dialogue_list()
        return self.__dealer_betrayal_list.pop()
    
    def make_prayers_list(self):
        a_list = []
        a_list.append("You look up to the roof, with your hands together, praying He is watching. Amen.")
        a_list.append("You close your eyes, and pray to Jesus that this next hand's a winner. Amen.")
        a_list.append("With eyes closed, you send a prayer up to God, that you'll double your winnings. Amen.")
        a_list.append("You put your hands together and pray, hoping that this next will make you rich. Amen.")
        a_list.append("Closing your eyes, you pray to Jesus that you won't bust this next hand. Amen.")
        a_list.append("You put your hands together, and pray to God that you're dealt a Blackjack. Amen.")
        a_list.append("'Dear God', you think, 'just let me win this next one.' Amen.")
        a_list.append("You look up, and pray. If God is real, he'll let you win the next hand. Amen.")
        a_list.append("You close your eyes, and put your hands together. If Jesus really did die for our sins, then a Blackjack is inevitable. Amen.")
        a_list.append("Closing your eyes, you begin to pray. God speaks back, telling you to hit your next hand, but only once. Amen.")
        a_list.append("You pray to Jesus, and feel his presence. He smiles, as though saying, 'stand with the hand you're dealt.' Amen.")
        a_list.append("You look up to the sky, and pray. If you win this next hand, maybe a spot in Heaven is waiting for you. Amen.")
        a_list.append("You pray to Jesus that the demons leave you be, if only for this next hand. Amen.")
        random.shuffle(a_list)
        return a_list

    def get_prayer(self):
        if len(self.__prayers_list)==0:
            self.__prayers_list = self.make_prayers_list()
        return self.__prayers_list.pop()
    
    def make_fed_squirrely_list(self):
        a_list = []
        a_list.append("Squirrely just can't stop smiling today. It's super duper cute!")
        a_list.append("Squirrely is in a super cuddly mood today. Not that you're complaining.")
        a_list.append("Squirrely climbs up and down your arms, over and over. You couldn't stop him if you tried.")
        a_list.append("You try to be extra quiet, as Squirrely is sleeping in your lap.")
        a_list.append("Squirrely is extra cheery today, and he's currently lounging in your hair.")
        a_list.append("You've never had a pet quite as silly as Squirrely, and he can't stop making faces at you, sticking his tongue out, winking his eyes.")
        a_list.append("Of all the Squirrels you've seen before, Squirrely must be the softest. You pet him, and he makes a happy squeak!")
        a_list.append("Looking around, you can't find Squirrely anywhere. But, as you keep looking, you realize that he's just hiding in your shoe!")
        a_list.append("Squirrely curls up in your arms, as it's the place where he's the warmest!")
        a_list.append("Squirrely can't help but keep opening and closing your glovebox.")
        random.shuffle(a_list)
        return a_list
    
    def get_fed_squirrely_update(self):
        if len(self.__fed_squirrely_list)==0:
            self.__fed_squirrely_list = self.make_fed_squirrely_list()
        return self.__fed_squirrely_list.pop()

    def make_hungry_squirrely_list(self):
        a_list = []
        a_list.append("Squirrely looks a bit hungry today.")
        a_list.append("Squirrely isn't as jumpy today as he usually is.")
        a_list.append("Squirrely has been sleeping all day. You're starting to get worried.")
        a_list.append("Squirrely tries to look happy, but it's clear he's just not feeling it.")
        a_list.append("Squirrely climbs onto your shoulder, sighs, then sleeps.")
        a_list.append("Looking around, you can't find Squirrely anywhere. Is he hiding from you?")
        a_list.append("Squirrely sits on your dashboard, and looks longingly out the window at other squirrels.")
        a_list.append("While you're holding Squirrely in your hands, you feel his tummy rumble.")
        random.shuffle(a_list)
        return a_list

    def get_hungry_squirrely_update(self):
        if len(self.__hungry_squirrely_list)==0:
            self.__hungry_squirrely_list = self.make_hungry_squirrely_list()
        return self.__hungry_squirrely_list.pop()
    

    def make_worried_squirrely_list(self):
        a_list = []
        a_list.append("Squirrely shakes in your arms. The outside world is scaring him.")
        if self.__player.has_travel_restriction("Rain"):
            a_list.append("Squirrely has been hiding under the passenger seat all day. It seems he's scared of lightning.")
        random.shuffle(a_list)
        return a_list

    def get_worried_squirrely_update(self):
        if len(self.__worried_squirrely_list)==0:
            self.__worried_squirrely_list = self.make_worried_squirrely_list()
        return self.__worried_squirrely_list.pop()
    

    def make_sickness_list(self):
        a_list = []
        a_list.append("You're sick, you just know it.")
        if self.__player.has_status("Cold"):
            a_list.append("You sneeze, and snot fills your hands. This makes you want to cry.")
            a_list.append("You can't breathe through your nose, as it's completely clogged.")
        if self.__player.has_status("Sore Throat"):
            a_list.append("Your throat feels like it's on fire.")
            a_list.append("The pain in your throat cannot be put into words. Mainly because you're having trouble speaking.")
        if self.__player.has_status("Hepatitis"):
            a_list.append("You have a seriously high fever, and feel like puking.")
            a_list.append("Your kidneys hurt really bad. That can't be good.")
        random.shuffle(a_list)
        return a_list
    
    def get_sickness_update(self):
        sickness_update = self.make_sickness_list()
        return sickness_update.pop()

    def get_sickness_death(self):
        a_list = []
        if self.__player.has_status("Cold"):
            a_list.append("As you sneeze, you feel your heart stop beating in your chest. You clench it, before collapsing in your wagon.")
        if self.__player.has_status("Sore Throat"):
            a_list.append("You cough, then keep coughing. After each convulsion in your body, you try to catch your breath, only to cough even more. Trying desperately to get some air, you stick your head out the window, and directly into the freight truck that's driving by.")
        if self.__player.has_status("Hepatitis"):
            a_list.append("The side of your body gives out a sharp pain. You reach for it, before screaming in agony. As you spit out blood, you watch as the world around you starts to darken.")
        random.shuffle(a_list)
        return a_list.pop()

    def make_injury_list(self):
        a_list = []
        a_list.append("Something's definitely wrong with your body. That's for certain.")
        if self.__player.has_injury("Broken Leg"):
            a_list.append("Your leg is purple and bruised, like badly.")
            a_list.append("Your leg is broken. It just is. Has to be.")
        if self.__player.has_injury("Fractured Spine"):
            a_list.append("It's so hard to even sit up straight. That's not normal.")
            a_list.append("Your back feels like it's being torn apart.")
        if self.__player.has_injury("Severed Skin"):
            a_list.append("The cuts all over your body means it's very hard to enjoy existing.")
            a_list.append("It's incredible that your skin is still fully intact.")
        if self.__player.has_injury("Scraped Knee"):
            a_list.append("Your knee has seen better days. Much, much better days.")
            a_list.append("Looking at your skinned knee, you swear you can see the bone.")
        random.shuffle(a_list)
        return a_list

    def get_injury_update(self):
        injury_update = self.make_injury_list()
        return injury_update.pop()

    def make_quote_list(self):
        a_list = []
        a_list.append("\"Stars aren't far away. They're just really small. They're so small that all 17 of them could fit into the earth. That's why we can't get to them. They move away so the planet doesn't eat them and only show up at night when the earth is sleeping.\"")
        a_list.append("\"You may have breathed the same air a dinosaur breathed 1000s of years ago. If you don't think that's the tightest shit then get out of my face.\"")
        a_list.append("\"Don't be afraid to fail. Be afraid to get emotionally invested and then fail.\"")
        a_list.append("\"Every corpse on Everest was once an extremely motivated person.\"")
        a_list.append("\"I honest to God thought Santa Claus was real for the longest time. Mom and Dad just never told me. My parents are fucking cruel.\"")
        a_list.append("\"Every tattoo is a temporary tattoo, because we are all slowly dying.\"")
        a_list.append("\"The reason you have to follow your dreams is because even your dreams are trying to get away from you.\"")
        a_list.append("\"If you give up on your dreams, that may free up some time to get some actual stuff done\"")
        a_list.append("\"If you hate yourself, remember that you are not alone. A lot of other people hate you too.\"")
        a_list.append("\"The trash gets picked up tomorrow. Be ready.\"")
        a_list.append("\"I'm not your fucking therapist, stop using me for emotional advice.\"")
        a_list.append("\"No matter how many motivational quotes you know, you will remain a pathetic loser. Yesterday, today, and tomorrow. No matter how much you make, what degree you earn or what lie you tell yourself. A big flop at life you will remain. Don't doubt it for a minute. That's not even addressing your disgustinly deformed physique.\"")
        a_list.append("\"Good Moms have sticky floors, messy kitchens, laundry piles, dirty ovens, and happy kids.\"")
        a_list.append("\"Before you can love someone else you have to learn to love yourself so there's no chance of that happening.\"")
        a_list.append("\"There was a safety meeting at work today. They asked me, 'What steps would you take in the event of a fire?' 'Fucking big ones' was the wrong answer.\"")
        a_list.append("\"I walk around like everything's fine, but deep down, inside my shoe, my sock is sliding off.\"")
        a_list.append("\"Life would be a lot easier if it wasn't so hard.\"")
        a_list.append("\"I can't brain today. I have the dumb.\"")
        a_list.append("\"If you don't want to be mistaken for a doormat, get off the damn floor.\"")
        a_list.append("\"You know it's cold outside when you go outside and it's cold.\"")
        a_list.append("\"If I had to rate you from 1 to 10, I'd give you a 9, because I'm the 1 you're missing.\"")
        a_list.append("\"Have you ever wondered why you can't taste your tongue?\"")
        a_list.append("\"Freedom means the right to yell, \"THEATRE!\" in a crowded fire.\"")
        a_list.append("\"Whatever you're doing, always give 100 percent. Unless you're donating blood.\"")
        a_list.append("\"Would you believe that my neighbor came ringing my doorbell at 2:00 this morning? Luckily for him, I was still up playing bagpipes.\"")
        a_list.append("\"If a man said he'll fix it, he'll fix it. There is no need to nag him every 6 months about it.\"")
        a_list.append("\"Every form has its own meaning. Every man creates his meaning and form and goal. Why is it so important - what others have done? Why does it become sacred by the mere fact of not being your own? Why is anyone and everyone right - so long as it's not yourself? Why does the number of those others take the place of truth? Why is truth made a mere matter of arithmetic - and only of addition at that? Why is everything twisted out of all sense to fit everything else? There must be some reason. I don't know. I've never known it. I'd like to understand.\"")
        a_list.append("\"Grief, I've learned, is really just love. It's all the love you want to give, but cannot. All that unspent love gathers up in the corners of your eyes, the lump in your throat, and in that hollow part of your chest. Grief is just love with no place to go.\"")
        a_list.append("\"Bananas! Bananas! Bananas! Bananas! Bananas! Bananas! Bananas! Bananas!\"")
        a_list.append("\"Remember, if you can't convince them, confuse them. It's like playing chess with a pigeon; no matter how good you are, the bird is going to knock over the pieces and strut around like it's victorious.\"")
        a_list.append("\"Why go the extra mile when you can just complain about the first one? After all, life is not about the journey or the destination; it's about finding a good parking spot.\"")
        a_list.append("\"Always borrow money from pessimists - they don't expect it back. Plus, it's a great way to test your invisibility cloak when they come to collect.\"")
        a_list.append("\"Remember, if at first you don't succeed, skydiving is not for you. Stick to ground-based failures where the stakes are low and the embarrassment is your only injury.\"")
        a_list.append("\"If life gives you lemons, keep them, because hey, free lemons. But if life gives you melons, you might be dyslexic.\"")
        a_list.append("\"Never do anything half-heartedly; always use your full heart, even if it's misguided, wrong, or downright bizarre. Full-hearted mistakes make the best stories.\"")
        a_list.append("\"Eat a live frog first thing in the morning, and nothing worse will happen to you the rest of the day. Except, of course, the haunting realization that you started your day by eating a live frog.\"")
        a_list.append("\"If you think nobody cares if you're alive, try missing a couple of car payments. Better yet, see how many friends you have left when you ask them to help you move.\"")
        a_list.append("\"If you can't beat them, dress better than them. If you can't dress better, at least be funnier. If you can't be funnier, just hide in the closet until they leave.\"")
        a_list.append("\"When one door closes, just open it again. It's a door; that's how they work. If it doesn't open, congratulations, you've found a wall.\"")
        a_list.append("\"Keep your friends close, your enemies closer, and receipts for all major purchases. You never know when you'll need to return something, or someone.\"")
        a_list.append("\"Remember, it's not paranoia if your plants are actually plotting against you. Keep them in check by pretending to water them with vinegar.\"")
        a_list.append("\"If you find yourself at a loss for words, try using someone else's. Plagiarism is just sharing with extra steps.\"")
        a_list.append("\"Why put off until tomorrow what you can avoid entirely? Remember, procrastination is not the problem, it's the solution.\"")
        a_list.append("\"Remember, if you can't handle me at my worst, then fair enough, I'm really unpleasant.\"")
        a_list.append("\"If life knocks you down, stay there and take a nap. The floor is already familiar with your failures; let it be your comfort.\"")
        a_list.append("\"A clear conscience is usually the sign of a bad memory. Keep forgetting your mistakes, and you'll achieve eternal peace.\"")
        a_list.append("\"Why walk when you can dance? Unless dancing is just walking with style, in which case, why not moonwalk everywhere and reverse your way through life's problems?\"")
        a_list.append("\"If at first you don't succeed, redefine success. Because if success is waking up at noon on a Wednesday thinking it's a Saturday, then congratulations, you've made it.\"")
        a_list.append("\"If a tree falls in the forest and no one is around to hear it, does it make a sound? More importantly, if a tree falls in your living room, can you blame it on the dog?\"")
        a_list.append("\"Life is short. Smile while you still have teeth.\"")
        a_list.append("\"Sometimes I wish I was a bird. So I could fly over certain people and poop on their heads.\"")
        a_list.append("\"In the grand tapestry of existence, one must consider the intricate dance of the cosmos, where each celestial body moves in perfect harmony, except when they don't, which is most of the time, really, leading one to ponder whether the stars are just freestyling it. This brings to mind the importance of breakfast, the most important meal of a day that is itself a construct, much like the notion that socks should always match or that cats have any respect for personal space, which is to say, it's all a matter of perspective, isn't it? And speaking of perspective, have you ever noticed how small a plane looks in the sky, which is itself a vast canvas of blue, or gray, or black, depending on the time, which, as we've established, is a construct?\"")
        a_list.append("\"Consider, if you will, the humble potato: a tuber, a starch, a veritable chameleon of the culinary world, which, much like our own journey through the winding corridors of life, starts underground, in the dark, unaware of its potential to become fries, mashed, or a gratin, which is really just a fancy way of saying 'baked with cheese.' And isn't that just like us? Starting out as raw potential, only to be shaped by our experiences, our trials, and yes, our cooking methods, until we emerge, golden.\"")
        a_list.append("\"Let's embark on a journey, a meandering path not unlike the serpentine wanderings of a leaf caught in a capricious autumn breeze, which, as it dances to the silent music of nature, reminds us of the unpredictable choreography of existence. This leaf, let's call it Gerald, flutters with an elegance borne of happenstance, a fragile vessel for the whims of the wind. Gerald's journey is not linear, nor is it bound by the rigid expectations of society's ceaselessly grinding gears. Instead, Gerald twirls, dips, and soars, embracing the chaos with a grace we can only aspire to. Now, consider the ant, industrious and steadfast, a creature of purpose and communal toil. Our ant, whom we'll name Beatrice, marches diligently on her quest for sustenance, her life a testament to the virtues of hard work and persistence. Yet, in the grand tapestry of the cosmos, what is Beatrice but a speck, a mere blip on the infinite canvas of the universe? And yet, does her insignificance in the face of the vast unknown render her efforts moot? I posit that it does not, for in the grand scheme, all actions, large and small, contribute to the intricate mosaic of existence. But back to Gerald, who by now has traversed the convoluted landscapes of our imagination, touching upon the existential questions that haunt the periphery of our consciousness. What can we learn from Gerald and Beatrice? Is it their resilience, their unyielding will to persist in the face of the insurmountable odds stacked against them by the very nature of their existence? Or is it, perhaps, the simple beauty of their dance, a reminder that life, in all its complexity and confusion, offers moments of sublime beauty, fleeting and precious, to be cherished and remembered? As Gerald finally comes to rest upon the earth, joining Beatrice in the eternal cycle of life and death, we are reminded that all journeys, whether they be of leaves or ants or the human heart, are interconnected in the grand, bewildering dance of the cosmos. So, what was the point of this story, you may ask? Well, that, my friend, is entirely up to you.\"")
        a_list.append("\"If the sky is the limit, then why is there footprints on the moon? Because sometimes cheese can fly, especially when clocks are melting and rabbits wear hats.\"")
        a_list.append("\"Why use a door when you can enter through an imaginary pineapple? Remember, only invisible keys can unlock hidden broccoli forests.\"")
        a_list.append("\"When life throws potatoes at you, make a spaceship. Because nothing says 'adventure' like a tuber in zero gravity, especially when sunglass-wearing fish pilot the craft.\"")
        a_list.append("\"If time is a circle, then are we all just rolling along like doughnuts in a bakery of eternity? Beware of the square bagels, they're time travelers in disguise.\"")
        a_list.append("\"Whisper to the rain and listen to the wind, for they tell tales of square watermelons and the secret life of shadows who are afraid of the dark.\"")
        a_list.append("\"Remember, if you ever get lost in the forest, turn left at the talking mushroom and wave hello to the sky. It's rude not to greet the blue, especially when it's wearing its fancy clouds.\"")
        a_list.append("\"Why ponder the meaning of life when you can dance with the whimsical ants under the moonlit spaghetti? It's all about finding the rhythm in the chaos of cereal whispers.\"")
        random.shuffle(a_list)
        return a_list

    def get_quote(self):
        if len(self.__quote_list)==0:
            self.__quote_list = self.make_quote_list()
        return self.__quote_list.pop()
    
    def make_cheers_list(self):
        a_list = []
        a_list.append("Congrats!")
        a_list.append("Hurray!")
        a_list.append("Yippee!")
        a_list.append("Woo-hoo!")
        a_list.append("Yessir!")
        a_list.append("Yesss!")
        a_list.append("Well done!")
        a_list.append("Bravo!")
        a_list.append("Fantastic!")
        a_list.append("Amazing!")
        a_list.append("Great job!")
        a_list.append("Excellent!")
        a_list.append("Superb!")
        a_list.append("Outstanding!")
        a_list.append("Impressive!")
        a_list.append("Keep it up!")
        a_list.append("Way to go!")
        a_list.append("You nailed it!")
        random.shuffle(a_list)
        return a_list

    def get_cheer(self):
        if len(self.__cheers_list)==0:
            self.__cheers_list = self.make_cheers_list()
        return self.__cheers_list.pop()
    
    def make_advice_list(self):
        a_list = []
        a_list.append("Good progress so far, pal. Keep it up.")
        a_list.append("For what it's worth, I think you're doing alright.")
        a_list.append("I mean, you could definitely make more money, but hey it's a good start.")
        a_list.append("Congrats on all the hard work so far. It's nice to know you're still alive.")
        a_list.append("I would probably wipe that smile off that face if I were you. Just kidding, you're awesome.")
        a_list.append("Do you think maybe you could be a bit better at Blackjack? Just think about it.")
        a_list.append("I like your work ethic. Your grandma would be proud.")
        a_list.append("If there's one thing I've learned, it's that you must never back down, and never give up.")
        a_list.append("Your efforts haven't gone unnoticed. They're just not always mentioned.")
        a_list.append("Just so you know, your perseverance is more impressive than perfection.")
        a_list.append("Life's a garden, dig it. You're doing just that, and it's admirable.")
        a_list.append("You've got a unique path, and honestly, it's thrilling to watch it unfold.")
        a_list.append("Keep pushing the boundaries, even if it's just by a little every day.")
        a_list.append("Oh, look at you, making small changes like you're actually going to finish something. Adorable.")
        a_list.append("Look at you, using your full potential - just kidding, but seriously, nice effort today.")
        a_list.append("You might not be winning the race, but at least you're in the running, right? Sort of?")
        a_list.append("Your unique approach to life's challenges is so...inspiring? Yeah, let's go with that.")
        random.shuffle(a_list)
        return a_list

    def get_advice(self):
        if len(self.__advice_list)==0:
            self.__advice_list = self.make_advice_list()
        return self.__advice_list.pop()
    
    def make_rank_comment_list(self, rank):
        """Varied comments for each wealth rank"""
        a_list = []
        if rank == 0:  # Poor ($1-1,000)
            a_list.append("Let's not get too far ahead of ourselves though, you're still quite poor.")
            a_list.append("You're basically living paycheck to paycheck. Except there's no paycheck.")
            a_list.append("Poor? Yes. Defeated? Not yet.")
            a_list.append("Hey, at least you can afford... some things. Not many things. But some.")
            a_list.append("You're in the 'ramen noodle' tax bracket.")
        elif rank == 1:  # Modest ($1,001-10,000)
            a_list.append("You definitely have some money. The keyword is 'some'.")
            a_list.append("Not rich, not poor. Perfectly mediocre.")
            a_list.append("You've got a cushion now. A very small, uncomfortable cushion.")
            a_list.append("Middle class in a wagon. Living the dream.")
            a_list.append("You're doing okay. And okay is honestly pretty good these days.")
        elif rank == 2:  # Well-off ($10,001-100,000)
            a_list.append("You've amassed significant earnings. Nicely done.")
            a_list.append("Look at you, making money moves. Actual money. Not just coins.")
            a_list.append("You're starting to look like someone who's got their life together. Don't worry, it's an illusion.")
            a_list.append("Five figures. Not bad for someone living in a car.")
            a_list.append("You've got 'treat yourself to gas station sushi' money now.")
        elif rank == 3:  # Rich ($100,001-500,000)
            a_list.append("You must have some heavy pockets, huh.")
            a_list.append("Six figures. In a wagon. The duality of man.")
            a_list.append("You're rich enough to fix the car. But you won't. Because you're you.")
            a_list.append("This is 'I could stay at a hotel but I won't' money.")
            a_list.append("Wealthy and homeless. An interesting combination.")
        elif rank == 4:  # Very Rich ($500,001-899,999)
            a_list.append("Where do you even keep all that?")
            a_list.append("That's a down payment on a house. Too bad you live in a car.")
            a_list.append("Half a million dollars. Still sleeping in a wagon. Fascinating life choices.")
            a_list.append("You're basically Scrooge McDuck, but with worse real estate.")
            a_list.append("This is 'the car is a choice, not a necessity' money. Right? ...Right?")
        elif rank == 5:  # Almost Millionaire ($900,000-999,999)
            a_list.append("So close to being a millionaire! Can you do it?")
            a_list.append("The millionaire's club is within reach. You can almost taste it.")
            a_list.append("Nine hundred thousand. One more good night and you've made it.")
            a_list.append("You're knocking on the millionaire's door. Will it open?")
            a_list.append("This is it. This is the home stretch. Don't blow it now.")
        random.shuffle(a_list)
        return a_list
    
    def get_rank_comment(self, rank):
        return random.choice(self.make_rank_comment_list(rank))
    
    # ==========================================
    # DEALER GIFT REACTION SYSTEM
    # ==========================================
    
    def get_dealer_gift_reaction(self, item_name):
        """Return Dealer's reaction to gifts - mysterious, quick, eerie, aware"""
        reactions = {
            # POSITIVE REACTIONS (happiness gain)
            "Ace of Spades": {
                "dialogue": [
                    "\"The Ace. The beginning and the end.\"",
                    "\"You understand the game better than I thought.\"",
                    "\"This pleases me.\""
                ],
                "happiness": 25,
                "kills_you": False
            },
            "Dealer's Joker": {
                "dialogue": [
                    "\"My card. Returned to me.\"",
                    "\"Interesting. You found what was lost.\"",
                    "\"The joker always comes home.\""
                ],
                "happiness": 30,
                "kills_you": False
            },
            "Golden Compass": {
                "dialogue": [
                    "\"Direction. Purpose. Meaning.\"",
                    "\"This points toward something I lost long ago.\"",
                    "He stares at it for a long moment.",
                    "\"Thank you.\""
                ],
                "happiness": 20,
                "kills_you": False
            },
            "Mirror of Duality": {
                "dialogue": [
                    "\"Two faces. Like mine.\"",
                    "He looks into it. Both eyes—jade and human—stare back.",
                    "\"You see too much.\""
                ],
                "happiness": 15,
                "kills_you": False
            },
            
            # NEUTRAL REACTIONS (no happiness change, but interesting dialogue)
            "Lucky Coin": {
                "dialogue": [
                    "\"Luck. The gambler's crutch.\"",
                    "He flips it once. Catches it. Doesn't look at the result.",
                    "\"Luck is a lie we tell ourselves.\""
                ],
                "happiness": 0,
                "kills_you": False
            },
            "Pocket Watch": {
                "dialogue": [
                    "\"Time. Always time with you people.\"",
                    "\"The casino has no clocks. Did you ever wonder why?\"",
                    "\"Time stops here. Only the cards move.\""
                ],
                "happiness": 5,
                "kills_you": False
            },
            "Gambler's Grimoire": {
                "dialogue": [
                    "\"A book of statistics. How quaint.\"",
                    "He flips through it.",
                    "\"The numbers never tell the whole story.\""
                ],
                "happiness": 10,
                "kills_you": False
            },
            
            # NEGATIVE REACTIONS (happiness loss)
            "Cursed Coin": {
                "dialogue": [
                    "\"You bring CURSES to my table?\"",
                    "His jade eye flares.",
                    "\"Bold. Foolish. But bold.\""
                ],
                "happiness": -15,
                "kills_you": False
            },
            "Necronomicon": {
                "dialogue": [
                    "\"Dark magic. Here. At MY table.\"",
                    "The air grows cold.",
                    "\"You're testing boundaries you don't understand.\""
                ],
                "happiness": -20,
                "kills_you": False
            },
            "Voodoo Doll": {
                "dialogue": [
                    "\"You think this works on ME?\"",
                    "He crushes it in one hand.",
                    "\"I am not bound by such trivial magic.\""
                ],
                "happiness": -25,
                "kills_you": False
            },
            
            # DANGEROUS REACTIONS (might kill you)
            "Dealer's Grudge": {
                "dialogue": [
                    "\"MY grudge. You bring MY grudge. To ME.\"",
                    "The temperature drops.",
                    "\"Did you think this was funny?\""
                ],
                "happiness": -40,
                "kills_you": True
            },
            "Stolen Watch": {
                "dialogue": [
                    "\"Stolen goods. At my table.\"",
                    "\"You insult me with theft.\"",
                    "\"We're done here.\""
                ],
                "happiness": -50,
                "kills_you": True
            },
            
            # FOOD ITEMS (mostly neutral/slightly positive)
            "Sandwich": {
                "dialogue": [
                    "\"Food. I don't... eat.\"",
                    "He sets it aside.",
                    "\"But the gesture is noted.\""
                ],
                "happiness": 3,
                "kills_you": False
            },
            "Energy Drink": {
                "dialogue": [
                    "\"Energy. As if I need more.\"",
                    "\"I haven't slept in... how long?\"",
                    "He doesn't remember."
                ],
                "happiness": 2,
                "kills_you": False
            },
            
            # MYSTERIOUS ITEMS (cryptic reactions)
            "Mysterious Lockbox": {
                "dialogue": [
                    "\"Locked. Like so many things.\"",
                    "He doesn't try to open it.",
                    "\"Some boxes should stay closed.\""
                ],
                "happiness": 8,
                "kills_you": False
            },
            "Moon Shard": {
                "dialogue": [
                    "\"From above. From beyond.\"",
                    "It hums in his hand.",
                    "\"The moon sees everything. Even this place.\""
                ],
                "happiness": 15,
                "kills_you": False
            },
            
            # DEFAULT for unlisted items
            "_default": {
                "dialogue": [
                    "He examines it carefully.",
                    "\"Curious.\"",
                    "He sets it beside the deck of cards."
                ],
                "happiness": 5,
                "kills_you": False
            }
        }
        
        return reactions.get(item_name, reactions["_default"])
    
    def make_quote_setup_list(self):
        a_list = []
        a_list.append("I'll leave you with a quote: ")
        a_list.append("Here's a little bit of inspiration for you: ")
        a_list.append("Here's a quote my dad used to say: ")
        a_list.append("This quote always gets me going: ")
        a_list.append("Something to ponder on your journey: ")
        a_list.append("If you ever feel lost, just remember: ")
        a_list.append("Take a moment to reflect on this: ")
        a_list.append("For those who enjoy a bit of bathroom philosophy: ")
        a_list.append("Don't forget what the bible taught you: ")
        a_list.append("If aliens could talk, they'd probably say: ")
        a_list.append("I read this once in a magazine: ")
        a_list.append("This one's straight from the fortune cookie in my lunch: ")
        a_list.append("Here's what my cat whispered to me last night: ")
        a_list.append("You know what you need right now? A quote, from the heart: ")
        a_list.append("As I tried to parallel park for the 10th time, I remember a passerby that yelled: ")
        a_list.append("As my doctor was putting me under, he whispered into my ear: ")
        random.shuffle(a_list)
        return a_list

    def get_quote_setup(self):
        if len(self.__quote_setup_list)==0:
            self.__quote_setup_list = self.make_quote_setup_list()
        return self.__quote_setup_list.pop()