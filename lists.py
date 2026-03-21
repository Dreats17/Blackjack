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
        # Companion daily dialogue lists
        self.__whiskers_happy_list = self.make_whiskers_happy_list()
        self.__whiskers_unhappy_list = self.make_whiskers_unhappy_list()
        self.__whiskers_weather_list = self.make_whiskers_weather_list()
        self.__whiskers_morning_list = self.make_whiskers_morning_list()
        self.__lucky_happy_list = self.make_lucky_happy_list()
        self.__lucky_unhappy_list = self.make_lucky_unhappy_list()
        self.__lucky_weather_list = self.make_lucky_weather_list()
        self.__lucky_morning_list = self.make_lucky_morning_list()
        self.__pecks_happy_list = self.make_pecks_happy_list()
        self.__pecks_unhappy_list = self.make_pecks_unhappy_list()
        self.__pecks_weather_list = self.make_pecks_weather_list()
        self.__pecks_morning_list = self.make_pecks_morning_list()
        self.__patches_happy_list = self.make_patches_happy_list()
        self.__patches_unhappy_list = self.make_patches_unhappy_list()
        self.__patches_weather_list = self.make_patches_weather_list()
        self.__patches_morning_list = self.make_patches_morning_list()
        self.__rusty_happy_list = self.make_rusty_happy_list()
        self.__rusty_unhappy_list = self.make_rusty_unhappy_list()
        self.__rusty_weather_list = self.make_rusty_weather_list()
        self.__rusty_morning_list = self.make_rusty_morning_list()
        self.__slick_happy_list = self.make_slick_happy_list()
        self.__slick_unhappy_list = self.make_slick_unhappy_list()
        self.__slick_weather_list = self.make_slick_weather_list()
        self.__slick_morning_list = self.make_slick_morning_list()
        self.__hopper_happy_list = self.make_hopper_happy_list()
        self.__hopper_unhappy_list = self.make_hopper_unhappy_list()
        self.__hopper_weather_list = self.make_hopper_weather_list()
        self.__hopper_morning_list = self.make_hopper_morning_list()
        self.__squirrelly_comp_happy_list = self.make_squirrelly_comp_happy_list()
        self.__squirrelly_comp_unhappy_list = self.make_squirrelly_comp_unhappy_list()
        self.__squirrelly_comp_weather_list = self.make_squirrelly_comp_weather_list()
        self.__squirrelly_comp_morning_list = self.make_squirrelly_comp_morning_list()
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
        self.__crafting_recipes = self.make_crafting_recipes()
        self.__crafted_item_descriptions = self.make_crafted_item_descriptions()
        self.__loan_shark_dialogue = self.make_loan_shark_dialogue()
        self.__dealer_betrayal_list = self.make_dealer_betrayal_dialogue_list()

    def _night_event_allowed(self, event_name):
        one_off_night_events = {
            "drowning_dream": "Drowning Dream",
        }
        met_name = one_off_night_events.get(event_name)
        if met_name is None:
            return True
        return not self.__player.has_met(met_name)

    def _pull_night_event(self, pool_name, factory):
        pool = getattr(self, pool_name)
        while True:
            while pool:
                event_name = pool.pop()
                if self._night_event_allowed(event_name):
                    setattr(self, pool_name, pool)
                    return event_name
            pool = factory()

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
            
            # Interconnected Chain Achievements
            "hermit_trail_complete": {"name": "The Hermit's Legacy", "description": "Find the Hollow Tree Stash at the end of the hermit's trail."},
            "hermit_daughter": {"name": "Edgar's Daughter", "description": "Give Diana her father's journal."},
            "radio_nowhere_member": {"name": "Radio Nowhere", "description": "Join the pirate radio station and meet Vera."},
            "radio_broadcast": {"name": "Your Voice in the Dark", "description": "Record and broadcast your story on Radio Nowhere."},
            "junkyard_apprentice": {"name": "Junkyard Apprentice", "description": "Learn to craft a Scrap Metal Rose from Gideon."},
            "junkyard_crowned": {"name": "Crowned in Scrap", "description": "Create the Junkyard Crown with Gideon."},
            "dog_hero": {"name": "Dog Hero", "description": "Rescue the missing dogs and attend the block party."},
            "rose_gifted": {"name": "Art is Giving", "description": "Give the Scrap Metal Rose to someone who needed it."},
            "all_chains_done": {"name": "Connected", "description": "Complete all four interconnected storyline chains."},
            "night_vision_used": {"name": "Eyes in the Dark", "description": "Use the Night Vision Scope to see what lurks at night."},
            "scrap_armor_crafted": {"name": "Junkyard Knight", "description": "Craft Scrap Armor on your own at the junkyard."},
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
                    "happy": [
                        "Squirrelly chatters happily on your dashboard.",
                        "Squirrelly does a little dance with an acorn.",
                        "Squirrelly buries an acorn in your cup holder. Saving for winter.",
                        "Squirrelly races up your arm, perches on your head, and chirps triumphantly.",
                        "Squirrelly presents you with the shiniest acorn you've ever seen. A gift.",
                        "Squirrelly is vibrating with happiness. Just pure uncontainable squirrel joy."
                    ],
                    "neutral": [
                        "Squirrelly watches you with curious eyes.",
                        "Squirrelly nibbles on something.",
                        "Squirrelly sits on the dashboard, tail twitching, judging your life choices.",
                        "Squirrelly reorganizes the acorn stash in your glove box. Important work.",
                        "Squirrelly stares at a tree outside with longing, then looks at you. Stays.",
                        "Squirrelly is doing squirrel math. You don't know what that means but they're focused."
                    ],
                    "sad": [
                        "Squirrelly looks at you with pleading eyes.",
                        "Squirrelly's tail droops sadly.",
                        "Squirrelly sits alone in the corner, clutching a single acorn like it's all they have left.",
                        "Squirrelly won't eat. Won't play. Just sits there, small and still.",
                        "Squirrelly buries their face in their tail. The world is too big.",
                        "Squirrelly flinches when you reach for them. That hurts more than you expected."
                    ],
                    "bonded": [
                        "Squirrelly falls asleep in your hand. Total trust. Total peace.",
                        "Squirrelly brings you an acorn every morning without fail. It's become a ritual between you two.",
                        "Squirrelly chatters at strangers who get too close to you. Protective little thing.",
                        "Squirrelly has built a tiny nest in your car. Made of receipts, napkins, and love."
                    ]
                }
            },
            "Whiskers": {
                "type": "Alley Cat",
                "description": "A scraggly but affectionate stray cat who senses danger before it arrives.",
                "favorite_food": "Cat Food",
                "bonuses": {"sanity_restore": 3, "danger_warning": True},
                "dialogue": {
                    "happy": [
                        "Whiskers purrs loudly in your lap.",
                        "Whiskers kneads your leg with contentment.",
                        "Whiskers headbutts your chin and purrs so hard their whole body vibrates.",
                        "Whiskers brings you a dead bug. It's a gift. Accept it graciously.",
                        "Whiskers curls into a perfect circle on your chest. You can feel each purr in your ribs.",
                        "Whiskers slow-blinks at you. In cat language, that's 'I love you.' You slow-blink back."
                    ],
                    "neutral": [
                        "Whiskers stares out the window.",
                        "Whiskers grooms themselves meticulously.",
                        "Whiskers knocks something off your dashboard. On purpose. Maintains eye contact.",
                        "Whiskers sits in a sunbeam, ignoring your existence with practiced elegance.",
                        "Whiskers stretches luxuriously. Front paws. Back paws. Full body yawn. It's a whole performance.",
                        "Whiskers watches a bird outside with the intensity of a trained assassin."
                    ],
                    "sad": [
                        "Whiskers meows plaintively.",
                        "Whiskers hides under the seat.",
                        "Whiskers sits with their back to you. The message is clear.",
                        "Whiskers won't purr. The silence is deafening.",
                        "Whiskers scratches at the door. They want to leave. That thought terrifies you.",
                        "Whiskers hisses when you reach out. The betrayal in those eyes cuts deep."
                    ],
                    "bonded": [
                        "Whiskers sleeps ON your face at night. It's inconvenient. It's the best thing ever.",
                        "Whiskers follows you everywhere now. Into the casino. Into trouble. Into life.",
                        "Whiskers hisses at anyone who looks at you wrong. Your personal bodyguard in a fur coat.",
                        "Whiskers brings you gifts every day. Bugs, leaves, once a dollar bill. They're providing for you."
                    ]
                }
            },
            "Lucky": {
                "type": "Three-Legged Dog",
                "description": "A resilient mutt who lost a leg but not his spirit. Will die for you.",
                "favorite_food": "Dog Food",
                "bonuses": {"sanity_restore": 5, "protection": True},
                "dialogue": {
                    "happy": [
                        "Lucky's tail wags so hard his whole body shakes.",
                        "Lucky licks your face enthusiastically.",
                        "Lucky does a three-legged zoomie around the parking lot. Missing a leg never slowed him down.",
                        "Lucky puts his head in your lap and sighs contentedly. This is his whole world.",
                        "Lucky brings you a stick. Then another stick. Then a rock. He's generous like that.",
                        "Lucky howls along with a passing ambulance. His singing voice is... unique."
                    ],
                    "neutral": [
                        "Lucky rests his head on your leg.",
                        "Lucky watches the world go by.",
                        "Lucky sniffs everything. Every. Single. Thing. He's conducting an investigation.",
                        "Lucky lies on his back with his three legs in the air. Living his best life.",
                        "Lucky tilts his head at you like he's trying to understand human problems.",
                        "Lucky guards the car while you're nearby. Nothing gets past him."
                    ],
                    "sad": [
                        "Lucky whimpers softly.",
                        "Lucky won't meet your eyes.",
                        "Lucky limps to the farthest corner and lies down facing the wall.",
                        "Lucky doesn't eat his food. Just stares at the bowl. Then at you.",
                        "Lucky licks his missing leg's stump. Phantom pain. He's hurting.",
                        "Lucky doesn't wag his tail when you say his name. That's how you know it's bad."
                    ],
                    "bonded": [
                        "Lucky would walk through fire for you. You know this with absolute certainty.",
                        "Lucky presses his whole body against yours when you're sad. He always knows.",
                        "Lucky growls at anyone who raises their voice near you. Protective to a fault.",
                        "Lucky sleeps across the car door like a furry barricade. Nothing gets to you while he's here."
                    ]
                }
            },
            "Mr. Pecks": {
                "type": "Crow",
                "description": "An intelligent crow who brings you shiny things and remembers every face.",
                "favorite_food": "Birdseed",
                "bonuses": {"find_money_chance": 5, "sanity_restore": 1},
                "dialogue": {
                    "happy": [
                        "Mr. Pecks caws proudly and drops a shiny coin in your lap.",
                        "Mr. Pecks preens on your shoulder.",
                        "Mr. Pecks does a little hop-dance on your car roof. Tap tap tap.",
                        "Mr. Pecks brings you a bottle cap, a button, and a paperclip. His treasure trove.",
                        "Mr. Pecks mimics the sound of your car horn perfectly. Scares the hell out of you.",
                        "Mr. Pecks gently pulls at your hair. Grooming you. You're part of his flock now."
                    ],
                    "neutral": [
                        "Mr. Pecks watches you with beady, intelligent eyes.",
                        "Mr. Pecks pecks at the window.",
                        "Mr. Pecks sits on the rearview mirror, cataloging every passerby. He remembers them all.",
                        "Mr. Pecks is having a conversation with other crows. About you, probably.",
                        "Mr. Pecks cocks his head sideways, studying you like a puzzle he hasn't solved yet.",
                        "Mr. Pecks drops a pebble in your coffee. You think it's an offering. Maybe it's a prank."
                    ],
                    "sad": [
                        "Mr. Pecks sits silently, feathers ruffled.",
                        "Mr. Pecks won't eat.",
                        "Mr. Pecks turns his back to you on the rooftop. A crow's cold shoulder.",
                        "Mr. Pecks hasn't brought you anything shiny in days. The gifts have stopped.",
                        "Mr. Pecks makes a low, mournful sound you've never heard before. Crow grief.",
                        "Mr. Pecks flies away and doesn't come back for hours. You worry the whole time."
                    ],
                    "bonded": [
                        "Mr. Pecks has recruited an entire murder of crows. They all know your face. They all watch out for you.",
                        "Mr. Pecks brings you actual money now. Bills. You don't ask where he gets them.",
                        "Mr. Pecks dive-bombs people who try to mess with you. Air support.",
                        "Mr. Pecks perches on your shoulder like you're a pirate. You've never felt cooler."
                    ]
                }
            },
            "Patches": {
                "type": "Opossum",
                "description": "A nocturnal friend who plays dead when scared but comes alive at night.",
                "favorite_food": "Garbage",
                "bonuses": {"night_bonus": True, "sanity_restore": 2},
                "dialogue": {
                    "happy": [
                        "Patches hangs from your rearview mirror by their tail.",
                        "Patches nuzzles your hand.",
                        "Patches shows you their babies riding on their back. A whole possum family.",
                        "Patches waddles over and DOESN'T play dead. The highest form of opossum trust.",
                        "Patches purrs. Yes, opossums purr. It sounds like a tiny motorboat.",
                        "Patches opens their mouth in that hissing smile. Terrifying to others. Adorable to you."
                    ],
                    "neutral": [
                        "Patches sleeps in a ball under the seat.",
                        "Patches watches you warily.",
                        "Patches hangs upside down from the sun visor. Just vibing.",
                        "Patches is nocturnal but stays awake to keep you company during the day. Sacrifice.",
                        "Patches eats a piece of garbage with the delicacy of a sommelier tasting fine wine.",
                        "Patches makes weird clicking sounds. Opossum communication. You nod like you understand."
                    ],
                    "sad": [
                        "Patches plays dead. You're pretty sure they're not actually dead.",
                        "Patches hisses when you get too close.",
                        "Patches curls into a tight ball and won't uncurl. The world is too much.",
                        "Patches drools more than usual. Stress response. Opossums are sensitive souls.",
                        "Patches retreats under the seat and won't come out. Not playing dead. Just hiding.",
                        "Patches bares all 50 teeth at you. More teeth than any other North American mammal. All angry."
                    ],
                    "bonded": [
                        "Patches sleeps in your lap during the day, trusting you completely. For a prey animal, that's everything.",
                        "Patches stays up all night watching over you while you sleep. Your nocturnal guardian.",
                        "Patches has stopped playing dead around you entirely. Total trust. Absolute vulnerability.",
                        "Patches carries their babies everywhere. They've decided you're family. All of you, together."
                    ]
                }
            },
            "Rusty": {
                "type": "Raccoon",
                "description": "A mischievous raccoon with clever paws who steals for you.",
                "favorite_food": "Anything",
                "bonuses": {"steal_chance": 3, "sanity_restore": 2},
                "dialogue": {
                    "happy": [
                        "Rusty chittered and washed their hands in your coffee cup.",
                        "Rusty brings you something shiny... is that someone's watch?",
                        "Rusty figured out how to open the glove box. And the center console. And your wallet.",
                        "Rusty stands on their hind legs and extends their tiny hands toward you. Hug request.",
                        "Rusty stacks objects into a tower. Knocks it down. Builds it again. Artist at work.",
                        "Rusty organized all the coins in your car by size. Raccoon OCD is real."
                    ],
                    "neutral": [
                        "Rusty rummages through your glove box.",
                        "Rusty watches you with their little bandit mask.",
                        "Rusty is washing something in the puddle outside. It's your phone. RUSTY, NO.",
                        "Rusty opens a bag of chips with surgical precision. Those dexterous little paws.",
                        "Rusty examines a coin, turns it over three times, then pockets it. Where? How?",
                        "Rusty makes eye contact, then deliberately knocks your sunglasses off the dashboard."
                    ],
                    "sad": [
                        "Rusty sulks in the corner.",
                        "Rusty won't come out of hiding.",
                        "Rusty stops stealing things. That's when you know something's really wrong.",
                        "Rusty washes their paws over and over. Stress behavior. They need comfort.",
                        "Rusty chatters softly in the dark. It sounds almost like crying.",
                        "Rusty returns everything they stole today. Neatly arranged. A peace offering you didn't need."
                    ],
                    "bonded": [
                        "Rusty has a network of raccoon informants across the city. You don't ask questions.",
                        "Rusty steals exclusively FOR you now. Wallets, jewelry, once a whole ham. Provider.",
                        "Rusty taught their babies to steal. You now have a raccoon crime family. Don Rusty.",
                        "Rusty sleeps in your hoodie pocket. A warm, furry lump of loyalty and larceny."
                    ]
                }
            },
            "Slick": {
                "type": "Rat",
                "description": "A surprisingly clean and clever rat who knows every escape route.",
                "favorite_food": "Cheese",
                "bonuses": {"danger_warning": True, "sanity_restore": 1},
                "dialogue": {
                    "happy": [
                        "Slick runs up your arm and perches on your shoulder.",
                        "Slick squeaks contentedly.",
                        "Slick does a tiny popcorning hop. Happy rat behavior. It's incredibly cute.",
                        "Slick grinds their teeth softly. Bruxing. Rat equivalent of purring.",
                        "Slick brings you a crumb of food. Sharing. From a rat, that means everything.",
                        "Slick crawls into your sleeve and falls asleep. Warm. Safe. Loved."
                    ],
                    "neutral": [
                        "Slick watches you from the dashboard.",
                        "Slick grooms their whiskers.",
                        "Slick explores every crack and crevice of the car. Mapping escape routes. Always.",
                        "Slick sits up on their haunches and sniffs the air. Something is on their mind.",
                        "Slick arranges their bedding material precisely. Nesting behavior. Making a home.",
                        "Slick stares at the wall for 30 seconds then looks at you like they solved the universe."
                    ],
                    "sad": [
                        "Slick hides in the glove box.",
                        "Slick won't eat.",
                        "Slick's ears are flat against their head. Fear. Sadness. Both.",
                        "Slick bites you gently. Not aggression. A cry for help.",
                        "Slick stays in the darkest corner. Hiding from the world. From you.",
                        "Slick's whiskers droop. You didn't know rat whiskers could droop. They can."
                    ],
                    "bonded": [
                        "Slick has memorized every exit, every alley, every hiding spot within a mile. Your personal GPS of survival.",
                        "Slick sleeps in your shirt pocket, right over your heart. You're their whole world.",
                        "Slick alerts you with specific squeaks for different threats. You've learned their language.",
                        "Slick has befriended every rat in the area. You have informants everywhere. The rat network."
                    ]
                }
            },
            "Hopper": {
                "type": "Rabbit",
                "description": "A lucky rabbit who brings good fortune wherever they hop.",
                "favorite_food": "Carrot",
                "bonuses": {"luck_bonus": 3, "sanity_restore": 2},
                "dialogue": {
                    "happy": [
                        "Hopper does little binkies around the car.",
                        "Hopper snuggles against your leg.",
                        "Hopper flops on their side dramatically. Rabbit body language for 'life is perfect.'",
                        "Hopper zooms around the car at impossible speed, then stops and looks smug.",
                        "Hopper lets you rub their belly. Rabbits almost never do this. You've been chosen.",
                        "Hopper grooms your hand with tiny licks. Cleaning you. You're one of their babies now."
                    ],
                    "neutral": [
                        "Hopper twitches their nose curiously.",
                        "Hopper lounges on the passenger seat.",
                        "Hopper rearranges the blankets into a nest. Very specific about comfort.",
                        "Hopper chinning everything. That's your stuff, that's your stuff, EVERYTHING is their stuff.",
                        "Hopper sits perfectly still, ears rotating like satellite dishes. Listening.",
                        "Hopper pushes their food bowl toward you. Then pulls it back. Sharing is complicated."
                    ],
                    "sad": [
                        "Hopper thumps their foot anxiously.",
                        "Hopper won't come out of hiding.",
                        "Hopper sits hunched in the corner, ears flat. A rabbit loaf of sadness.",
                        "Hopper grinds their teeth. Not the happy kind. The stressed kind. Sharp, rapid.",
                        "Hopper refuses all food. All treats. All comfort. Stubbornly sad.",
                        "Hopper lunges when you reach in. Scared. Not angry. But scared."
                    ],
                    "bonded": [
                        "Hopper binkies whenever they see you. Pure, stupid, wonderful joy.",
                        "Hopper has claimed the entire car as their territory. You're allowed to visit.",
                        "Hopper grooms your face every morning. You wake up to rabbit kisses. Life is good.",
                        "Hopper brings you luck you can almost feel. Things just... go right when they're nearby."
                    ]
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
    
    def get_companion_bonus(self, name, bonus_name):
        """Get a specific bonus value for a companion"""
        companion = self.__companion_types.get(name, None)
        if companion and "bonuses" in companion:
            return companion["bonuses"].get(bonus_name, None)
        return None

    def has_companion_with_bonus(self, player, bonus_name):
        """Check if any living companion has a specific bonus"""
        living = player.get_all_companions()
        for name in living:
            companion_type = self.__companion_types.get(name, None)
            if companion_type and "bonuses" in companion_type:
                if bonus_name in companion_type["bonuses"]:
                    return name
        return None

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
            # Convenience store items previously unsellable
            "Duct Tape": 4,
            "Water Bottles": 3,
            "Road Flares": 8,
            "Bug Spray": 5,
            "Binoculars": 20,
            "Garbage Bag": 1,
            "Plastic Wrap": 2,
            "Fishing Line": 6,
            "Super Glue": 4,
            "Hand Warmers": 3,
            "Rubber Bands": 1,
            "Breath Mints": 1,
            "Matches": 1,
            "Birdseed": 1,
            "Fish": 5,
            "Bread": 1,
            "Sandwich": 2,
            "Cheese": 1,
            "Baking Soda": 1,
            "Battery Terminal Cleaner": 3,
            "Cheap Sunscreen": 2,
            "Premium Sunscreen": 6,
            "Poncho": 4,
            "Running Shoes": 15,
            "Filled Locket": 25,
            
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
            
            # Crafted Items
            "Shiv": 35,
            "Slingshot": 20,
            "Road Flare Torch": 40,
            "Pepper Spray": 30,
            "Improvised Trap": 25,
            "Car Alarm Rigging": 30,
            "Snare Trap": 20,
            "Home Remedy": 20,
            "Wound Salve": 25,
            "Splint": 15,
            "Smelling Salts": 18,
            "Lockpick Set": 30,
            "Fishing Rod": 25,
            "Binocular Scope": 45,
            "Signal Mirror": 15,
            "Lucky Charm Bracelet": 10,
            "Dream Catcher": 15,
            "Worry Stone": 8,
            "Rain Collector": 10,
            "Emergency Blanket": 12,
            "Smoke Signal Kit": 20,
            "Fire Starter Kit": 15,
            "Water Purifier": 18,
            "Companion Bed": 15,
            "Pet Toy": 8,
            "Feeding Station": 10,
            
            # Chain Event Items
            "Worn Map": 5,
            "Hermit's Journal": 25,
            "Carved Walking Stick": 30,
            "Herbal Pouch": 20,
            "Strange Frequency Dial": 15,
            "Static Recorder": 20,
            "Tinfoil Hat": 5,
            "Pirate Radio Flyer": 10,
            "Welding Goggles": 25,
            "Scrap Metal Rose": 40,
            "Artisan's Toolkit": 60,
            "Junkyard Crown": 100,
            "Stack of Flyers": 2,
            "Dog Whistle": 15,
            "Torn Collar": 5,
            "Reunion Photo": 35,
            "Hollow Tree Stash": 50,
            "Night Vision Scope": 45,
            "Signal Booster": 30,
            "Scrap Armor": 55,
        }
    
    def get_pawn_price(self, item_name):
        return self.__pawn_shop_prices.get(item_name, 0)
    
    def get_sellable_items(self):
        """Returns list of items that can be sold at pawn shop"""
        return list(self.__pawn_shop_prices.keys())

    # ==========================================
    # CRAFTING RECIPE DATA (CAR WORKBENCH)
    # ==========================================

    def make_crafting_recipes(self):
        """All recipes craftable at the car workbench.
        Each recipe: name, ingredients list, description, pawn_value, category.
        Categories: weapon, trap, remedy, tool, charm, survival, companion"""
        return {
            # === WEAPONS ===
            "Shiv": {
                "ingredients": ["Duct Tape", "Pocket Knife"],
                "description": "A pocket knife taped to a stick. Crude, effective, terrifying.",
                "pawn_value": 35,
                "category": "weapon",
                "craft_text": "You wrap duct tape around the handle of your pocket knife until it feels right. It's ugly. It'll work.",
            },
            "Slingshot": {
                "ingredients": ["Rubber Bands", "Bungee Cords"],
                "description": "A Y-shaped branch with rubber pulled taut. David vs. Goliath energy.",
                "pawn_value": 20,
                "category": "weapon",
                "craft_text": "You find a forked stick outside, stretch the rubber bands between the prongs, and suddenly you're ten years old again. Except now you're armed.",
            },
            "Road Flare Torch": {
                "ingredients": ["Road Flares", "Duct Tape"],
                "description": "A road flare strapped to a stick. Lights the way and scares off threats.",
                "pawn_value": 40,
                "category": "weapon",
                "craft_text": "You duct-tape a road flare to an old car antenna. It's a torch. It's ridiculous. It's incredibly effective.",
            },
            "Pepper Spray": {
                "ingredients": ["Bug Spray", "Lighter"],
                "description": "Bug spray + flame = homemade deterrent. Not exactly legal. Very effective.",
                "pawn_value": 30,
                "category": "weapon",
                "craft_text": "You hold the lighter in front of the bug spray can. A quick test spray sends a fireball three feet out. You grin. This'll keep the creeps away.",
            },

            # === TRAPS ===
            "Improvised Trap": {
                "ingredients": ["Fishing Line", "Pocket Knife"],
                "description": "Trip wire connected to a noise maker. Alerts you to intruders while you sleep.",
                "pawn_value": 25,
                "category": "trap",
                "craft_text": "You string fishing line between the car's side mirrors, attach some cans, and set it at ankle height. Anyone who gets close, you'll hear them.",
            },
            "Car Alarm Rigging": {
                "ingredients": ["Bungee Cords", "Spare Fuses"],
                "description": "A jury-rigged alarm system for your wagon. Won't stop a thief, but it'll wake you up.",
                "pawn_value": 30,
                "category": "trap",
                "craft_text": "You wire the spare fuses into a loop with the bungee cords on the door handle. Open the door, circuit breaks, horn blasts. Genius or insanity. Same thing.",
            },
            "Snare Trap": {
                "ingredients": ["Rope", "Fishing Line"],
                "description": "A classic snare loop hidden in the grass. Catches small animals or trips big ones.",
                "pawn_value": 20,
                "category": "trap",
                "craft_text": "You tie a loop in the rope, thread the fishing line through, and set it near a rabbit trail. Primitive. Effective. You feel like a caveman.",
            },

            # === REMEDIES ===
            "Home Remedy": {
                "ingredients": ["First Aid Kit", "Cough Drops"],
                "description": "A DIY cold cure: crushed cough drops in warm water, bandages for comfort. Actually works.",
                "pawn_value": 20,
                "category": "remedy",
                "craft_text": "You crush the cough drops into a paste, mix them with clean bandage material from the first aid kit, and make a throat poultice. It looks disgusting. It works.",
            },
            "Wound Salve": {
                "ingredients": ["First Aid Kit", "Super Glue"],
                "description": "Medical-grade wound closure. Super glue was literally invented for this.",
                "pawn_value": 25,
                "category": "remedy",
                "craft_text": "Fun fact: super glue was originally designed for field surgery. You squeeze it along a clean bandage strip. Instant butterfly closure. You feel like a doctor. Sort of.",
            },
            "Splint": {
                "ingredients": ["Duct Tape", "Rope"],
                "description": "A rigid splint for sprains and fractures. Won't fix it, but it'll hold.",
                "pawn_value": 15,
                "category": "remedy",
                "craft_text": "You wrap rope around two straight sticks, reinforce with duct tape, and create a splint that a field medic would nod approvingly at. Probably.",
            },
            "Smelling Salts": {
                "ingredients": ["Hand Warmers", "Breath Mints"],
                "description": "Crushed mints in a warm pouch. One whiff clears the fog from your brain.",
                "pawn_value": 18,
                "category": "remedy",
                "craft_text": "You crush the mints to dust, pour them into a hand warmer pouch, and seal it. Crack it open near your nose. WHOOSH. You can see through time. Almost.",
            },

            # === TOOLS ===
            "Lockpick Set": {
                "ingredients": ["Pocket Knife", "Fishing Line"],
                "description": "A bent knife blade and tension wrench. Opens things that were meant to stay closed.",
                "pawn_value": 30,
                "category": "tool",
                "craft_text": "You heat the tip of the pocket knife blade with a lighter and bend it into a hook. Thread the fishing line through for tension. Your first lockpick set. Criminal? Maybe. Useful? Absolutely.",
            },
            "Fishing Rod": {
                "ingredients": ["Fishing Line", "Rope"],
                "description": "A proper fishing rig made from a car antenna and braided line. Fresh dinner awaits.",
                "pawn_value": 25,
                "category": "tool",
                "craft_text": "You snap the car antenna off (sorry, wagon), tie the fishing line to the tip, and braid the rope for a handle grip. Cast it into any body of water and hope for the best.",
            },
            "Binocular Scope": {
                "ingredients": ["Binoculars", "Duct Tape"],
                "description": "Binoculars taped to the car's sun visor. See danger before it sees you.",
                "pawn_value": 45,
                "category": "tool",
                "craft_text": "You duct-tape the binoculars to the sun visor at an angle. Now you can scan the horizon without even holding them. Surveillance state: population you.",
            },
            "Signal Mirror": {
                "ingredients": ["Broken Compass", "Super Glue"],
                "description": "The compass glass, polished and mounted. Flash it at passing cars, helicopters, or the sun itself.",
                "pawn_value": 15,
                "category": "tool",
                "craft_text": "You crack the compass open, extract the glass face, polish it on your jeans, and glue it to a flat piece of cardboard. It catches the light perfectly. SOS, baby.",
            },

            # === CHARMS / LUCKY ITEMS ===
            "Lucky Charm Bracelet": {
                "ingredients": ["Lucky Penny", "Fishing Line"],
                "description": "A penny on a string. Stupid, right? Then why does everything go better when you wear it?",
                "pawn_value": 10,
                "category": "charm",
                "craft_text": "You punch a hole in the lucky penny, thread the fishing line through, and tie it around your wrist. It's not magic. But also, it kind of is.",
            },
            "Dream Catcher": {
                "ingredients": ["Fishing Line", "Rubber Bands"],
                "description": "A web of line and bands stretched in a circle. Hangs from your rearview mirror. Catches bad dreams.",
                "pawn_value": 15,
                "category": "charm",
                "craft_text": "You bend a coat hanger into a circle, weave the fishing line through it, stretch rubber bands across in a web pattern, and hang it from the rearview mirror. It sways gently. Your dreams get softer.",
            },
            "Worry Stone": {
                "ingredients": ["Lucky Penny", "Hand Warmers"],
                "description": "A warm penny you rub between your fingers when the world gets loud. Anxiety tool. Free therapy.",
                "pawn_value": 8,
                "category": "charm",
                "craft_text": "You press the lucky penny into a hand warmer, let it heat up, and hold it in your palm. Rub it with your thumb. Smooth. Warm. The anxiety doesn't vanish, but it gets quieter.",
            },

            # === SURVIVAL ===
            "Rain Collector": {
                "ingredients": ["Plastic Wrap", "Garbage Bag"],
                "description": "A funnel system that collects rainwater into a bottle. Hydration on autopilot.",
                "pawn_value": 10,
                "category": "survival",
                "craft_text": "You stretch the plastic wrap over the mouth of a cut garbage bag, creating a funnel. Set it on the roof. When it rains, clean water drips right into your bottle. Survivalist mode: engaged.",
            },
            "Emergency Blanket": {
                "ingredients": ["Garbage Bag", "Duct Tape"],
                "description": "A garbage bag lined with tape for insulation. Ugly, crinkly, surprisingly warm.",
                "pawn_value": 12,
                "category": "survival",
                "craft_text": "You split the garbage bag open, layer duct tape across the inside for insulation, and fold it into a blanket. It looks like modern art. It keeps you alive.",
            },
            "Smoke Signal Kit": {
                "ingredients": ["Road Flares", "Garbage Bag"],
                "description": "Black smoke on demand. Signal for help or scare off wildlife. Your choice.",
                "pawn_value": 20,
                "category": "survival",
                "craft_text": "You shred the garbage bag into strips, wrap them around the road flare tip, and test it. Thick black smoke billows up. You could signal a helicopter. Or ruin someone's laundry day.",
            },
            "Fire Starter Kit": {
                "ingredients": ["Lighter", "Hand Warmers"],
                "description": "A lighter plus tinder in a sealed pouch. Start a campfire anywhere, any weather.",
                "pawn_value": 15,
                "category": "survival",
                "craft_text": "You crack open the hand warmers, pour the iron filings into a zip bag with the lighter, and seal it tight. Instant fire kit. You could survive in the wilderness. Probably. For a day.",
            },
            "Water Purifier": {
                "ingredients": ["Plastic Wrap", "Lighter"],
                "description": "Solar still in a bag. Put dirty water in, wait, get clean water out. Science is cool.",
                "pawn_value": 18,
                "category": "survival",
                "craft_text": "You set dirty water in a bowl, cover it with plastic wrap, and put a small weight in the center. The sun evaporates the water, condensation runs down the plastic, and drips into your cup. Clean water. You are a genius.",
            },

            # === COMPANION ITEMS ===
            "Companion Bed": {
                "ingredients": ["Blanket", "Duct Tape"],
                "description": "A cozy padded bed for your animal friend. Duct tape holds the shape, blanket holds the warmth.",
                "pawn_value": 15,
                "category": "companion",
                "craft_text": "You fold the blanket into a donut shape, tape the bottom so it stays put, and set it in the corner of the car. Your companion sniffs it. Circles three times. Lies down. Home.",
            },
            "Pet Toy": {
                "ingredients": ["Rope", "Rubber Bands"],
                "description": "A braided rope toy with rubber band squeakers. Hours of entertainment. Mostly for you.",
                "pawn_value": 8,
                "category": "companion",
                "craft_text": "You braid the rope into a thick knot, weave rubber bands through it so it makes a satisfying SNAP when squeezed. Your companion goes absolutely feral. Best toy ever.",
            },
            "Feeding Station": {
                "ingredients": ["Plastic Wrap", "Duct Tape"],
                "description": "A waterproof food bowl that sticks to the car floor. No more spillage. Finally.",
                "pawn_value": 10,
                "category": "companion",
                "craft_text": "You mold the plastic wrap into a bowl shape, reinforce it with duct tape, and stick it to the car floor. It's not pretty. But the food stays in the bowl. Revolutionary.",
            },
        }

    def get_crafting_recipes(self):
        """Returns all crafting recipes"""
        return self.__crafting_recipes

    def get_available_recipes(self, player):
        """Returns recipes the player currently has ingredients for"""
        available = {}
        for name, recipe in self.__crafting_recipes.items():
            if not player.has_item(name):  # Can't craft duplicates
                has_all = True
                for ingredient in recipe["ingredients"]:
                    if not player.has_item(ingredient):
                        has_all = False
                        break
                if has_all:
                    available[name] = recipe
        return available

    def get_all_recipe_names(self):
        """Returns list of all craftable item names"""
        return list(self.__crafting_recipes.keys())

    def get_recipe(self, name):
        """Returns a specific recipe by name"""
        return self.__crafting_recipes.get(name, None)

    def get_craftable_categories(self):
        """Returns list of unique categories"""
        categories = set()
        for recipe in self.__crafting_recipes.values():
            categories.add(recipe["category"])
        return sorted(list(categories))

    def get_recipes_by_category(self, category):
        """Returns recipes filtered by category"""
        return {name: recipe for name, recipe in self.__crafting_recipes.items() 
                if recipe["category"] == category}

    # ==========================================
    # CRAFTED ITEM DESCRIPTIONS (for workbench inspection)
    # ==========================================

    def make_crafted_item_descriptions(self):
        """Detailed descriptions shown when inspecting a crafted item at the workbench"""
        return {
            # Weapons
            "Shiv": "A crude blade made from a pocket knife and duct tape. Gives you +30% chance to win combat encounters and scares off muggers. Not pretty, but effective.",
            "Slingshot": "A handmade slingshot. Use it to hunt small game during adventures or pelt annoying NPCs with pebbles. +15% chance to hit targets in ranged encounters.",
            "Road Flare Torch": "A blazing torch that lights dark areas and terrifies nocturnal threats. Doubles as a weapon. +25% chance to scare off night attackers. Burns out after 3 uses.",
            "Pepper Spray": "Homemade pepper spray. Guarantees escape from any non-boss combat encounter. Single use, but what a use it is.",
            # Traps
            "Improvised Trap": "Trip wire alarm around your car. +40% chance to prevent theft events. Gives you early warning during night encounters.",
            "Car Alarm Rigging": "Jury-rigged car alarm. Prevents the 'car_break_in' event entirely. Also wakes you up during night attacks, giving you first-strike advantage.",
            "Snare Trap": "A snare that catches small animals. During adventures, +20% chance to find food. Can also trip pursuers in chase events.",
            # Remedies
            "Home Remedy": "Cures a Cold or Sore Throat instantly. One use. Better than suffering for three days.",
            "Wound Salve": "Closes wounds and prevents infection. Heals 15 HP and removes one injury. One use.",
            "Splint": "Stabilizes fractures and sprains. Removes the 'Broken Bone' injury. Reusable until your next injury.",
            "Smelling Salts": "Clears your head. Restores 8 sanity instantly. Single use. Like a slap to the brain, but pleasant.",
            # Tools
            "Lockpick Set": "Opens locked containers and doors. During adventures, unlocks alternate paths and hidden loot. Reusable but breaks after 5 uses.",
            "Fishing Rod": "Cast into any body of water during adventures. Catch fish for free food (heals 12 HP) or rare items. Reusable.",
            "Binocular Scope": "Mounted on your car visor. Reveals hidden details in events — sometimes exposes traps, shortcuts, or hidden NPCs. Passive effect.",
            "Signal Mirror": "Flash it during day events for a chance to attract help. +10% chance to receive assistance in dangerous situations. Passive.",
            # Charms
            "Lucky Charm Bracelet": "Worn on your wrist. +2% blackjack luck bonus. Small but consistent. Stacks with other luck items.",
            "Dream Catcher": "Hangs from rearview mirror. Night events have +10% chance to be positive. Bad dreams give less sanity damage.",
            "Worry Stone": "Carry it always. Passive: lose 1 less sanity from any sanity-draining event. Small comfort in a cruel world.",
            # Survival
            "Rain Collector": "Collects water during rain events. Automatically restores 5 HP on rainy days. Passive.",
            "Emergency Blanket": "Extra warmth at night. Reduces fatigue gained during night events by 15%. Passive.",
            "Smoke Signal Kit": "Create a smoke signal during adventures. +20% chance to be rescued in dangerous situations. Single use.",
            "Fire Starter Kit": "Start a fire anywhere. During camping events, restores 5 HP and 3 sanity. During cold events, prevents health damage. 3 uses.",
            "Water Purifier": "Clean water on demand. Restores 8 HP when used. 5 uses before it needs to be rebuilt.",
            # Companion
            "Companion Bed": "Your companion sleeps better. Companion happiness decay reduced by 25%. Passive.",
            "Pet Toy": "Play with your companion for bonus happiness. When used, restores 15 companion happiness. Reusable.",
            "Feeding Station": "Food lasts longer. Companion feeding restores +50% more happiness. Passive.",
        }

    def get_crafted_item_description(self, item_name):
        """Get the detailed description of a crafted item"""
        return self.__crafted_item_descriptions.get(item_name, "A mysterious crafted item. You're not sure what it does.")

    def is_crafted_item(self, item_name):
        """Check if an item is a crafted item"""
        return item_name in self.__crafting_recipes

    # ==========================================
    # LOAN SHARK DIALOGUE
    # ==========================================
    
    def make_loan_shark_dialogue_legacy(self):
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
        a_list.append("vinnie_referral_card")
        a_list.append("stray_cat")
        a_list.append("three_legged_dog")
        a_list.append("opossum_in_trash")
        a_list.append("raccoon_gang_raid")
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
        a_list.append("empty_event")
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
        # COMPANION DAY EVENTS
        a_list.append("lucky_guards_car")
        a_list.append("mr_pecks_treasure")
        a_list.append("whiskers_sixth_sense")
        a_list.append("slick_escape_route")
        a_list.append("hopper_lucky_day")
        a_list.append("patches_night_watch")
        a_list.append("squirrelly_stash")
        a_list.append("companion_sick_day")
        a_list.append("companion_hero_moment")
        a_list.append("companion_nightmare")
        a_list.append("companion_lost_adventure")
        a_list.append("companion_food_crisis")
        # CRAFTED ITEM EVENTS
        a_list.append("shiv_confrontation")
        a_list.append("lockpick_opportunity")
        a_list.append("fishing_day")
        a_list.append("trap_night_thief")
        a_list.append("dream_catcher_night")
        a_list.append("slingshot_bird_hunt")
        a_list.append("signal_mirror_rescue")
        a_list.append("rain_collector_bonus")
        a_list.append("fire_starter_campfire")
        a_list.append("companion_bed_bonus")
        a_list.append("worry_stone_moment")
        a_list.append("snare_trap_catch")
        a_list.append("binocular_scope_discovery")
        a_list.append("emergency_blanket_cold_night")
        a_list.append("lucky_charm_streak")
        a_list.append("water_purifier_use")
        a_list.append("pet_toy_playtime")
        a_list.append("home_remedy_illness")
        a_list.append("road_flare_torch_encounter")
        a_list.append("feeding_station_morning")
        a_list.append("splint_injury_event")
        # ITEM USE EVENTS - no-use item activation
        a_list.append("road_talisman_protection")
        a_list.append("silver_horseshoe_luck")
        a_list.append("mystery_potion_effect")
        a_list.append("feelgood_bottle_moment")
        a_list.append("persistent_bottle_refill")
        a_list.append("ritual_token_ceremony")
        a_list.append("council_feather_blessing")
        a_list.append("cowboy_jacket_encounter")
        a_list.append("found_phone_call")
        a_list.append("alien_crystal_event")
        a_list.append("dimensional_coin_flip")
        a_list.append("radio_numbers_broadcast")
        a_list.append("mysterious_envelope_reveal")
        a_list.append("lockbox_contents")
        a_list.append("hollow_tree_stash_find")
        a_list.append("vision_map_navigate")
        a_list.append("secret_route_shortcut")
        a_list.append("street_cat_ally_benefit")
        a_list.append("old_photograph_memory")
        a_list.append("beach_romance_call")
        a_list.append("apartment_key_visit")
        a_list.append("fake_flower_gift")
        a_list.append("empty_locket_memory")
        a_list.append("stack_of_flyers_opportunity")
        a_list.append("mysterious_key_lockbox_open")
        a_list.append("suspicious_package_open")
        a_list.append("stolen_watch_recognition")
        a_list.append("underwater_camera_photos")
        a_list.append("witch_ward_dark_protection")
        a_list.append("deck_of_cards_street_game")
        a_list.append("ace_of_spades_blackjack_omen")
        a_list.append("dealer_joker_revelation")
        a_list.append("magic_acorn_planting")
        a_list.append("treasure_map_follow")
        a_list.append("capture_fairy_release")
        a_list.append("lucky_lure_fishing")
        a_list.append("mysterious_code_decode")
        a_list.append("swamp_gold_attention")
        # Chain Starter Events
        a_list.append("hermit_trail_discovery")
        a_list.append("lost_dog_flyers_found")
        a_list.append("lost_dog_investigation")
        # Recurring Chain Item Events
        a_list.append("herbal_pouch_remedy")
        a_list.append("walking_stick_hike")
        a_list.append("tinfoil_hat_event")
        a_list.append("reunion_photo_comfort")
        # CAR TROUBLE EVENTS - Poor Tier (minor breakdowns, cheap/no fix)
        a_list.append("corroded_battery_terminals")
        a_list.append("fuse_blown")
        a_list.append("abs_light_on")
        a_list.append("slow_tire_leak")
        a_list.append("headlights_burned_out")
        a_list.append("starter_motor_grinding")
        a_list.append("windshield_cracked")
        a_list.append("hail_damage")
        a_list.append("key_wont_turn")
        a_list.append("window_wont_roll_up")
        a_list.append("trunk_wont_close")
        a_list.append("bald_tires_noticed")
        a_list.append("exhaust_leak_loud")
        a_list.append("thermostat_stuck")
        a_list.append("nail_in_tire")
        # CAR TROUBLE FOLLOW-UPS - Poor Tier
        a_list.append("nail_in_tire_blows")
        a_list.append("failing_starter_dies")
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
        a_list.append("stray_cat_dies")
        a_list.append("giant_oyster_opening")
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
        a_list.append("painkiller_withdrawal")
        a_list.append("painkiller_dealer_returns")
        a_list.append("painkiller_overdose")
        a_list.append("cocaine_temptation")
        a_list.append("cocaine_crash")
        a_list.append("cocaine_heart_attack")
        a_list.append("voodoo_doll_temptation")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("soulless_recognition")
        a_list.append("weakened_immune_cold")
        a_list.append("weakened_immune_pneumonia")
        a_list.append("unpaid_tickets_boot")
        a_list.append("booted_car_impound")
        a_list.append("mystery_car_problem_worsens")
        a_list.append("stray_cat_has_kittens")
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
        a_list.append("grimy_gus_discovery")
        a_list.append("vinnie_referral_card")
        a_list.append("windblown_worn_map")
        a_list.append("flea_market_route_map")
        a_list.append("laundromat_bulletin_map")
        a_list.append("witch_doctor_matchbook")
        a_list.append("roadside_bone_chimes")
        a_list.append("trusty_tom_coupon_mailer")
        a_list.append("filthy_frank_radio_giveaway")
        a_list.append("oswald_concierge_card")
        # Conditional
        a_list.append("got_a_cold")
        a_list.append("cold_gets_worse")
        a_list.append("empty_event")
        # One-Time
        a_list.append("turn_to_god")
        a_list.append("hungry_cow")
        a_list.append("ice_cream_truck")
        a_list.append("kid_on_bike")
        a_list.append("lost_tourist")
        a_list.append("the_hitchhiker")
        # Conditional
        a_list.append("mayas_luck")
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
        # COMPANION DAY EVENTS
        a_list.append("lucky_guards_car")
        a_list.append("mr_pecks_treasure")
        a_list.append("rusty_midnight_heist")
        a_list.append("whiskers_sixth_sense")
        a_list.append("slick_escape_route")
        a_list.append("hopper_lucky_day")
        a_list.append("patches_night_watch")
        a_list.append("squirrelly_stash")
        a_list.append("companion_sick_day")
        a_list.append("companion_rivalry")
        a_list.append("companion_hero_moment")
        a_list.append("companion_nightmare")
        a_list.append("companion_lost_adventure")
        a_list.append("companion_brings_friend")
        a_list.append("companion_food_crisis")
        a_list.append("companion_milestone")
        # CRAFTED ITEM EVENTS
        a_list.append("shiv_confrontation")
        a_list.append("lockpick_opportunity")
        a_list.append("fishing_day")
        a_list.append("trap_night_thief")
        a_list.append("dream_catcher_night")
        a_list.append("slingshot_bird_hunt")
        a_list.append("signal_mirror_rescue")
        a_list.append("rain_collector_bonus")
        a_list.append("fire_starter_campfire")
        a_list.append("companion_bed_bonus")
        a_list.append("worry_stone_moment")
        a_list.append("snare_trap_catch")
        a_list.append("binocular_scope_discovery")
        a_list.append("emergency_blanket_cold_night")
        a_list.append("lucky_charm_streak")
        a_list.append("water_purifier_use")
        a_list.append("pet_toy_playtime")
        a_list.append("home_remedy_illness")
        a_list.append("road_flare_torch_encounter")
        a_list.append("feeding_station_morning")
        a_list.append("splint_injury_event")
        # ITEM USE EVENTS - no-use item activation
        a_list.append("road_talisman_protection")
        a_list.append("silver_horseshoe_luck")
        a_list.append("mystery_potion_effect")
        a_list.append("feelgood_bottle_moment")
        a_list.append("persistent_bottle_refill")
        a_list.append("ritual_token_ceremony")
        a_list.append("council_feather_blessing")
        a_list.append("cowboy_jacket_encounter")
        a_list.append("found_phone_call")
        a_list.append("alien_crystal_event")
        a_list.append("dimensional_coin_flip")
        a_list.append("radio_numbers_broadcast")
        a_list.append("mysterious_envelope_reveal")
        a_list.append("lockbox_contents")
        a_list.append("hollow_tree_stash_find")
        a_list.append("vision_map_navigate")
        a_list.append("secret_route_shortcut")
        a_list.append("street_cat_ally_benefit")
        a_list.append("old_photograph_memory")
        a_list.append("beach_romance_call")
        a_list.append("apartment_key_visit")
        a_list.append("fake_flower_gift")
        a_list.append("empty_locket_memory")
        a_list.append("stack_of_flyers_opportunity")
        a_list.append("mysterious_key_lockbox_open")
        a_list.append("suspicious_package_open")
        a_list.append("stolen_watch_recognition")
        a_list.append("underwater_camera_photos")
        a_list.append("witch_ward_dark_protection")
        a_list.append("deck_of_cards_street_game")
        a_list.append("ace_of_spades_blackjack_omen")
        a_list.append("dealer_joker_revelation")
        a_list.append("magic_acorn_planting")
        a_list.append("treasure_map_follow")
        a_list.append("capture_fairy_release")
        a_list.append("lucky_lure_fishing")
        a_list.append("mysterious_code_decode")
        a_list.append("swamp_gold_attention")
        # Chain Starter Events
        a_list.append("hermit_trail_discovery")
        a_list.append("lost_dog_flyers_found")
        a_list.append("lost_dog_investigation")
        # Chain Progression Events
        a_list.append("hermit_camp_return")
        a_list.append("hermit_journal_study")
        a_list.append("midnight_radio_signal")
        a_list.append("midnight_radio_frequency")
        a_list.append("lost_dog_whistle_search")
        a_list.append("lost_dog_culprit")
        a_list.append("lost_dog_reunion")
        # Recurring Chain Item Events
        a_list.append("herbal_pouch_remedy")
        a_list.append("walking_stick_hike")
        a_list.append("tinfoil_hat_event")
        a_list.append("reunion_photo_comfort")
        a_list.append("junkyard_crown_moment")
        # CAR TROUBLE EVENTS - Cheap Tier (moderate breakdowns)
        a_list.append("dead_battery_afternoon")
        a_list.append("engine_oil_empty")
        a_list.append("oil_leak_spotted")
        a_list.append("brakes_squealing")
        a_list.append("ran_out_of_gas")
        a_list.append("car_alarm_malfunction")
        a_list.append("frozen_door_locks")
        a_list.append("parking_brake_stuck")
        a_list.append("clogged_fuel_filter")
        a_list.append("strange_engine_noise")
        a_list.append("check_engine_light_on")
        a_list.append("engine_overheating")
        a_list.append("car_wont_go_in_reverse")
        a_list.append("gas_pedal_sticking")
        a_list.append("wheel_alignment_off")
        a_list.append("suspension_creaking")
        a_list.append("nail_in_tire")
        # CAR TROUBLE FOLLOW-UPS - Cheap Tier
        a_list.append("leaking_battery_worsens")
        a_list.append("engine_knock_worsens")
        a_list.append("bald_tires_hydroplane")
        a_list.append("nail_in_tire_blows")
        a_list.append("failing_starter_dies")
        random.shuffle(a_list)
        return a_list
    
    def make_cheap_night_events_list(self):
        a_list = []
        a_list.append("woodlands_path")
        a_list.append("woodlands_river")
        a_list.append("woodlands_river")
        a_list.append("woodlands_field")
        a_list.append("woodlands_field")
        a_list.append("swamp_stroll")
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
        a_list.append("stray_cat_dies")
        a_list.append("stray_cat_has_kittens")
        a_list.append("giant_oyster_opening")
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
        a_list.append("vinnie_referral_card")
        a_list.append("grimy_gus_discovery")
        a_list.append("windblown_worn_map")
        a_list.append("flea_market_route_map")
        a_list.append("laundromat_bulletin_map")
        a_list.append("witch_doctor_matchbook")
        a_list.append("roadside_bone_chimes")
        a_list.append("trusty_tom_coupon_mailer")
        a_list.append("filthy_frank_radio_giveaway")
        a_list.append("oswald_concierge_card")
        a_list.append("forgotten_birthday")
        a_list.append("book_club_invite")
        a_list.append("car_compliment")
        a_list.append("dog_walker_collision")
        a_list.append("coffee_shop_philosopher")
        a_list.append("food_truck_festival")
        # Deadly Events
        a_list.append("back_alley_shortcut")
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
        a_list.append("painkiller_withdrawal")
        a_list.append("painkiller_dealer_returns")
        a_list.append("painkiller_overdose")
        a_list.append("cocaine_temptation")
        a_list.append("cocaine_crash")
        a_list.append("voodoo_doll_temptation")
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
        a_list.append("stray_cat_has_kittens")
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
        a_list.append("empty_event")
        a_list.append("starving_cow")
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
        # COMPANION DAY EVENTS
        a_list.append("lucky_guards_car")
        a_list.append("mr_pecks_treasure")
        a_list.append("rusty_midnight_heist")
        a_list.append("whiskers_sixth_sense")
        a_list.append("slick_escape_route")
        a_list.append("hopper_lucky_day")
        a_list.append("patches_night_watch")
        a_list.append("squirrelly_stash")
        a_list.append("companion_sick_day")
        a_list.append("companion_rivalry")
        a_list.append("companion_hero_moment")
        a_list.append("companion_death_sacrifice")
        a_list.append("companion_nightmare")
        a_list.append("companion_lost_adventure")
        a_list.append("companion_bonded_moment")
        a_list.append("companion_learns_trick")
        a_list.append("companion_brings_friend")
        a_list.append("companion_food_crisis")
        a_list.append("companion_milestone")
        # CRAFTED ITEM EVENTS
        a_list.append("shiv_confrontation")
        a_list.append("lockpick_opportunity")
        a_list.append("fishing_day")
        a_list.append("trap_night_thief")
        a_list.append("dream_catcher_night")
        a_list.append("slingshot_bird_hunt")
        a_list.append("signal_mirror_rescue")
        a_list.append("rain_collector_bonus")
        a_list.append("fire_starter_campfire")
        a_list.append("companion_bed_bonus")
        a_list.append("worry_stone_moment")
        a_list.append("snare_trap_catch")
        a_list.append("binocular_scope_discovery")
        a_list.append("emergency_blanket_cold_night")
        a_list.append("lucky_charm_streak")
        a_list.append("water_purifier_use")
        a_list.append("pet_toy_playtime")
        a_list.append("home_remedy_illness")
        a_list.append("road_flare_torch_encounter")
        a_list.append("feeding_station_morning")
        a_list.append("splint_injury_event")
        # ITEM USE EVENTS - no-use item activation
        a_list.append("road_talisman_protection")
        a_list.append("silver_horseshoe_luck")
        a_list.append("mystery_potion_effect")
        a_list.append("feelgood_bottle_moment")
        a_list.append("persistent_bottle_refill")
        a_list.append("ritual_token_ceremony")
        a_list.append("council_feather_blessing")
        a_list.append("cowboy_jacket_encounter")
        a_list.append("found_phone_call")
        a_list.append("alien_crystal_event")
        a_list.append("dimensional_coin_flip")
        a_list.append("radio_numbers_broadcast")
        a_list.append("mysterious_envelope_reveal")
        a_list.append("lockbox_contents")
        a_list.append("hollow_tree_stash_find")
        a_list.append("vision_map_navigate")
        a_list.append("secret_route_shortcut")
        a_list.append("street_cat_ally_benefit")
        a_list.append("old_photograph_memory")
        a_list.append("beach_romance_call")
        a_list.append("apartment_key_visit")
        a_list.append("fake_flower_gift")
        a_list.append("empty_locket_memory")
        a_list.append("stack_of_flyers_opportunity")
        a_list.append("mysterious_key_lockbox_open")
        a_list.append("suspicious_package_open")
        a_list.append("stolen_watch_recognition")
        a_list.append("underwater_camera_photos")
        a_list.append("witch_ward_dark_protection")
        a_list.append("deck_of_cards_street_game")
        a_list.append("ace_of_spades_blackjack_omen")
        a_list.append("dealer_joker_revelation")
        a_list.append("magic_acorn_planting")
        a_list.append("treasure_map_follow")
        a_list.append("capture_fairy_release")
        a_list.append("lucky_lure_fishing")
        a_list.append("mysterious_code_decode")
        a_list.append("swamp_gold_attention")
        # Hermit Chain
        a_list.append("hermit_trail_discovery")
        a_list.append("hermit_camp_return")
        a_list.append("hermit_journal_study")
        a_list.append("hermit_trail_stranger")
        a_list.append("hermit_hollow_oak")
        # Midnight Radio Chain
        a_list.append("midnight_radio_signal")
        a_list.append("midnight_radio_frequency")
        a_list.append("midnight_radio_pole")
        a_list.append("midnight_radio_visit")
        a_list.append("midnight_radio_broadcast")
        # Junkyard Artisan Chain
        a_list.append("junkyard_artisan_meet")
        a_list.append("junkyard_lesson_one")
        a_list.append("junkyard_lesson_two")
        # Lost Dog Chain
        a_list.append("lost_dog_flyers_found")
        a_list.append("lost_dog_investigation")
        a_list.append("lost_dog_whistle_search")
        a_list.append("lost_dog_culprit")
        a_list.append("lost_dog_reunion")
        # Recurring Chain Item Events
        a_list.append("herbal_pouch_remedy")
        a_list.append("walking_stick_hike")
        a_list.append("tinfoil_hat_event")
        a_list.append("reunion_photo_comfort")
        a_list.append("junkyard_crown_moment")
        a_list.append("scrap_armor_event")
        # Crossover Events
        a_list.append("crossover_night_vision_bonus")
        # CAR TROUBLE EVENTS - Modest Tier (expensive repairs)
        a_list.append("engine_wont_turn_over")
        a_list.append("tire_blowout")
        a_list.append("battery_acid_leak")
        a_list.append("alternator_failing")
        a_list.append("brake_fluid_leak")
        a_list.append("fuel_pump_whining")
        a_list.append("stuck_in_gear")
        a_list.append("radiator_leak")
        a_list.append("power_steering_failure")
        a_list.append("frozen_fuel_line")
        a_list.append("water_pump_failing")
        a_list.append("dead_battery_afternoon")
        a_list.append("engine_overheating")
        a_list.append("car_alarm_malfunction")
        # CAR TROUBLE FOLLOW-UPS - Modest Tier
        a_list.append("leaking_battery_worsens")
        a_list.append("engine_knock_worsens")
        a_list.append("bald_tires_hydroplane")
        a_list.append("failing_fuel_pump_dies")
        a_list.append("broken_ball_joint_breaks")
        a_list.append("failing_starter_dies")
        random.shuffle(a_list)
        return a_list
    
    def make_modest_night_events_list(self):
        a_list = []
        a_list.append("woodlands_path")
        a_list.append("swamp_wade")
        a_list.append("swamp_wade")
        a_list.append("swamp_swim")
        a_list.append("swamp_swim")
        a_list.append("woodlands_field")
        a_list.append("woodlands_river")
        a_list.append("swamp_stroll")
        a_list.append("beach_stroll")
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
        a_list.append("giant_oyster_opening")
        # One-Time (Rabbit)
        a_list.append("chase_the_third_rabbit")
        random.shuffle(a_list)
        return a_list
    

# Rich Events (100,000 - 400,000)
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
        a_list.append("painkiller_withdrawal")
        a_list.append("painkiller_dealer_returns")
        a_list.append("painkiller_overdose")
        a_list.append("cocaine_temptation")
        a_list.append("cocaine_crash")
        a_list.append("cocaine_heart_attack")
        a_list.append("voodoo_doll_temptation")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("soulless_recognition")
        a_list.append("burn_scars_stares")
        a_list.append("weakened_immune_cold")
        a_list.append("weakened_immune_pneumonia")
        a_list.append("mystery_car_problem_worsens")
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
        a_list.append("wild_rat_attack")
        a_list.append("hungry_termites")
        a_list.append("wealth_anxiety")
        a_list.append("tax_man")
        a_list.append("empty_event")
        a_list.append("even_further_interrogation")
        # One-Time
        a_list.append("the_rival")
        a_list.append("the_bodyguard_offer")
        a_list.append("high_roller_invitation")
        a_list.append("old_friend_recognition")
        a_list.append("grimy_gus_discovery")
        a_list.append("vinnie_referral_card")
        a_list.append("windblown_worn_map")
        a_list.append("flea_market_route_map")
        a_list.append("laundromat_bulletin_map")
        a_list.append("witch_doctor_matchbook")
        a_list.append("roadside_bone_chimes")
        a_list.append("trusty_tom_coupon_mailer")
        a_list.append("filthy_frank_radio_giveaway")
        a_list.append("oswald_concierge_card")
        a_list.append("the_gambler_ghost")
        # Secret Events
        a_list.append("exactly_250000")
        # COMPANION DAY EVENTS
        a_list.append("lucky_guards_car")
        a_list.append("mr_pecks_treasure")
        a_list.append("rusty_midnight_heist")
        a_list.append("whiskers_sixth_sense")
        a_list.append("slick_escape_route")
        a_list.append("hopper_lucky_day")
        a_list.append("patches_night_watch")
        a_list.append("squirrelly_stash")
        a_list.append("companion_sick_day")
        a_list.append("companion_rivalry")
        a_list.append("companion_hero_moment")
        a_list.append("companion_death_sacrifice")
        a_list.append("companion_nightmare")
        a_list.append("companion_lost_adventure")
        a_list.append("companion_bonded_moment")
        a_list.append("companion_learns_trick")
        a_list.append("companion_brings_friend")
        a_list.append("companion_food_crisis")
        a_list.append("companion_milestone")
        # CRAFTED ITEM EVENTS
        a_list.append("shiv_confrontation")
        a_list.append("lockpick_opportunity")
        a_list.append("fishing_day")
        a_list.append("trap_night_thief")
        a_list.append("dream_catcher_night")
        a_list.append("slingshot_bird_hunt")
        a_list.append("signal_mirror_rescue")
        a_list.append("rain_collector_bonus")
        a_list.append("fire_starter_campfire")
        a_list.append("companion_bed_bonus")
        a_list.append("worry_stone_moment")
        a_list.append("snare_trap_catch")
        a_list.append("binocular_scope_discovery")
        a_list.append("emergency_blanket_cold_night")
        a_list.append("lucky_charm_streak")
        a_list.append("water_purifier_use")
        a_list.append("pet_toy_playtime")
        a_list.append("home_remedy_illness")
        a_list.append("road_flare_torch_encounter")
        a_list.append("feeding_station_morning")
        a_list.append("splint_injury_event")
        # ITEM USE EVENTS - no-use item activation
        a_list.append("road_talisman_protection")
        a_list.append("silver_horseshoe_luck")
        a_list.append("mystery_potion_effect")
        a_list.append("feelgood_bottle_moment")
        a_list.append("persistent_bottle_refill")
        a_list.append("ritual_token_ceremony")
        a_list.append("council_feather_blessing")
        a_list.append("cowboy_jacket_encounter")
        a_list.append("found_phone_call")
        a_list.append("alien_crystal_event")
        a_list.append("dimensional_coin_flip")
        a_list.append("radio_numbers_broadcast")
        a_list.append("mysterious_envelope_reveal")
        a_list.append("lockbox_contents")
        a_list.append("hollow_tree_stash_find")
        a_list.append("vision_map_navigate")
        a_list.append("secret_route_shortcut")
        a_list.append("street_cat_ally_benefit")
        a_list.append("old_photograph_memory")
        a_list.append("beach_romance_call")
        a_list.append("apartment_key_visit")
        a_list.append("fake_flower_gift")
        a_list.append("empty_locket_memory")
        a_list.append("stack_of_flyers_opportunity")
        a_list.append("mysterious_key_lockbox_open")
        a_list.append("suspicious_package_open")
        a_list.append("stolen_watch_recognition")
        a_list.append("underwater_camera_photos")
        a_list.append("witch_ward_dark_protection")
        a_list.append("deck_of_cards_street_game")
        a_list.append("ace_of_spades_blackjack_omen")
        a_list.append("dealer_joker_revelation")
        a_list.append("magic_acorn_planting")
        a_list.append("treasure_map_follow")
        a_list.append("capture_fairy_release")
        a_list.append("lucky_lure_fishing")
        a_list.append("mysterious_code_decode")
        a_list.append("swamp_gold_attention")
        # Hermit Chain
        a_list.append("hermit_trail_discovery")
        a_list.append("hermit_camp_return")
        a_list.append("hermit_journal_study")
        a_list.append("hermit_trail_stranger")
        a_list.append("hermit_hollow_oak")
        # Midnight Radio Chain
        a_list.append("midnight_radio_signal")
        a_list.append("midnight_radio_frequency")
        a_list.append("midnight_radio_pole")
        a_list.append("midnight_radio_visit")
        a_list.append("midnight_radio_broadcast")
        # Junkyard Artisan Chain
        a_list.append("junkyard_artisan_meet")
        a_list.append("junkyard_lesson_one")
        a_list.append("junkyard_lesson_two")
        a_list.append("junkyard_gideon_story")
        a_list.append("junkyard_masterpiece")
        # Lost Dog Chain
        a_list.append("lost_dog_flyers_found")
        a_list.append("lost_dog_investigation")
        a_list.append("lost_dog_whistle_search")
        a_list.append("lost_dog_culprit")
        a_list.append("lost_dog_reunion")
        # Recurring Chain Item Events
        a_list.append("herbal_pouch_remedy")
        a_list.append("walking_stick_hike")
        a_list.append("tinfoil_hat_event")
        a_list.append("reunion_photo_comfort")
        a_list.append("junkyard_crown_moment")
        a_list.append("scrap_armor_event")
        # Crossover Events
        a_list.append("crossover_radio_hermit")
        a_list.append("crossover_artisan_rose_gift")
        a_list.append("crossover_night_vision_bonus")
        a_list.append("crossover_all_chains_complete")
        # CAR TROUBLE EVENTS - Rich Tier (catastrophic breakdowns)
        a_list.append("transmission_slipping")
        a_list.append("broken_ball_joint")
        a_list.append("catalytic_converter_stolen")
        a_list.append("flooded_engine")
        a_list.append("mystery_breakdown")
        a_list.append("tire_blowout")
        a_list.append("alternator_failing")
        a_list.append("brake_fluid_leak")
        a_list.append("water_pump_failing")
        # CAR TROUBLE FOLLOW-UPS - Rich Tier
        a_list.append("leaking_battery_worsens")
        a_list.append("engine_knock_worsens")
        a_list.append("bald_tires_hydroplane")
        a_list.append("failing_fuel_pump_dies")
        a_list.append("broken_ball_joint_breaks")
        random.shuffle(a_list)
        return a_list
    
    def make_rich_night_events_list(self):
        a_list = []
        a_list.append("swamp_stroll")
        a_list.append("swamp_wade")
        a_list.append("swamp_swim")
        a_list.append("beach_stroll")
        a_list.append("beach_swim")
        a_list.append("beach_swim")
        a_list.append("beach_dive")
        a_list.append("beach_dive")
        a_list.append("city_streets")
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


# Doughman Events (400,000 - 750,000)
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
        a_list.append("voodoo_doll_temptation")
        a_list.append("soulless_emptiness")
        a_list.append("soulless_mirror")
        a_list.append("soulless_recognition")
        a_list.append("weakened_immune_pneumonia")
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
        a_list.append("even_further_interrogation")
        a_list.append("cow_army")
        # One-Time Events
        a_list.append("likely_death")
        a_list.append("the_veteran")
        a_list.append("the_journalist")
        a_list.append("the_offer_refused")
        a_list.append("the_doppelganger")
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
        # COMPANION DAY EVENTS
        a_list.append("lucky_guards_car")
        a_list.append("mr_pecks_treasure")
        a_list.append("rusty_midnight_heist")
        a_list.append("whiskers_sixth_sense")
        a_list.append("slick_escape_route")
        a_list.append("hopper_lucky_day")
        a_list.append("patches_night_watch")
        a_list.append("squirrelly_stash")
        a_list.append("companion_sick_day")
        a_list.append("companion_rivalry")
        a_list.append("companion_hero_moment")
        a_list.append("companion_death_sacrifice")
        a_list.append("companion_nightmare")
        a_list.append("companion_lost_adventure")
        a_list.append("companion_bonded_moment")
        a_list.append("companion_learns_trick")
        a_list.append("companion_brings_friend")
        a_list.append("companion_food_crisis")
        a_list.append("companion_milestone")
        # CRAFTED ITEM EVENTS
        a_list.append("shiv_confrontation")
        a_list.append("lockpick_opportunity")
        a_list.append("fishing_day")
        a_list.append("trap_night_thief")
        a_list.append("dream_catcher_night")
        a_list.append("slingshot_bird_hunt")
        a_list.append("signal_mirror_rescue")
        a_list.append("rain_collector_bonus")
        a_list.append("fire_starter_campfire")
        a_list.append("companion_bed_bonus")
        a_list.append("worry_stone_moment")
        a_list.append("snare_trap_catch")
        a_list.append("binocular_scope_discovery")
        a_list.append("emergency_blanket_cold_night")
        a_list.append("lucky_charm_streak")
        a_list.append("water_purifier_use")
        a_list.append("pet_toy_playtime")
        a_list.append("home_remedy_illness")
        a_list.append("road_flare_torch_encounter")
        a_list.append("feeding_station_morning")
        a_list.append("splint_injury_event")
        # ITEM USE EVENTS - no-use item activation
        a_list.append("road_talisman_protection")
        a_list.append("silver_horseshoe_luck")
        a_list.append("mystery_potion_effect")
        a_list.append("feelgood_bottle_moment")
        a_list.append("persistent_bottle_refill")
        a_list.append("ritual_token_ceremony")
        a_list.append("council_feather_blessing")
        a_list.append("cowboy_jacket_encounter")
        a_list.append("found_phone_call")
        a_list.append("alien_crystal_event")
        a_list.append("dimensional_coin_flip")
        a_list.append("radio_numbers_broadcast")
        a_list.append("mysterious_envelope_reveal")
        a_list.append("lockbox_contents")
        a_list.append("hollow_tree_stash_find")
        a_list.append("vision_map_navigate")
        a_list.append("secret_route_shortcut")
        a_list.append("street_cat_ally_benefit")
        a_list.append("old_photograph_memory")
        a_list.append("beach_romance_call")
        a_list.append("apartment_key_visit")
        a_list.append("fake_flower_gift")
        a_list.append("empty_locket_memory")
        a_list.append("stack_of_flyers_opportunity")
        a_list.append("mysterious_key_lockbox_open")
        a_list.append("suspicious_package_open")
        a_list.append("stolen_watch_recognition")
        a_list.append("underwater_camera_photos")
        a_list.append("witch_ward_dark_protection")
        a_list.append("deck_of_cards_street_game")
        a_list.append("ace_of_spades_blackjack_omen")
        a_list.append("dealer_joker_revelation")
        a_list.append("magic_acorn_planting")
        a_list.append("treasure_map_follow")
        a_list.append("capture_fairy_release")
        a_list.append("lucky_lure_fishing")
        a_list.append("mysterious_code_decode")
        a_list.append("swamp_gold_attention")
        # Hermit Chain
        a_list.append("hermit_trail_discovery")
        a_list.append("hermit_camp_return")
        a_list.append("hermit_journal_study")
        a_list.append("hermit_trail_stranger")
        a_list.append("hermit_hollow_oak")
        # Midnight Radio Chain
        a_list.append("midnight_radio_signal")
        a_list.append("midnight_radio_frequency")
        a_list.append("midnight_radio_pole")
        a_list.append("midnight_radio_visit")
        a_list.append("midnight_radio_broadcast")
        # Junkyard Artisan Chain
        a_list.append("junkyard_artisan_meet")
        a_list.append("junkyard_lesson_one")
        a_list.append("junkyard_lesson_two")
        a_list.append("junkyard_gideon_story")
        a_list.append("junkyard_masterpiece")
        # Lost Dog Chain
        a_list.append("lost_dog_flyers_found")
        a_list.append("lost_dog_investigation")
        a_list.append("lost_dog_whistle_search")
        a_list.append("lost_dog_culprit")
        a_list.append("lost_dog_reunion")
        # Recurring Chain Item Events
        a_list.append("herbal_pouch_remedy")
        a_list.append("walking_stick_hike")
        a_list.append("tinfoil_hat_event")
        a_list.append("reunion_photo_comfort")
        a_list.append("junkyard_crown_moment")
        a_list.append("scrap_armor_event")
        # Crossover Events
        a_list.append("crossover_radio_hermit")
        a_list.append("crossover_artisan_rose_gift")
        a_list.append("crossover_night_vision_bonus")
        a_list.append("crossover_all_chains_complete")
        # CAR TROUBLE EVENTS - Doughman Tier
        a_list.append("catalytic_converter_stolen")
        a_list.append("transmission_slipping")
        a_list.append("mystery_breakdown")
        a_list.append("flooded_engine")
        a_list.append("broken_ball_joint")
        # CAR TROUBLE FOLLOW-UPS - Doughman Tier
        a_list.append("engine_knock_worsens")
        a_list.append("failing_fuel_pump_dies")
        a_list.append("broken_ball_joint_breaks")
        a_list.append("bald_tires_hydroplane")
        random.shuffle(a_list)
        return a_list
    
    def make_doughman_night_events_list(self):
        a_list = []
        a_list.append("beach_stroll")
        a_list.append("beach_swim")
        a_list.append("beach_dive")
        a_list.append("city_streets")
        a_list.append("city_stroll")
        a_list.append("city_stroll")
        a_list.append("city_park")
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

# Nearly There Events (750,000 +)
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
        a_list.append("media_known_documentary")
        a_list.append("high_roller_room_visit")
        a_list.append("high_roller_whale")
        # Random Small Events
        a_list.append("prayer_answered")
        a_list.append("prayer_ignored")
        # Conditional
        a_list.append("too_close_to_quit")
        a_list.append("cow_army")
        # One-Time
        a_list.append("the_warning")
        a_list.append("the_celebration")
        a_list.append("the_offer")
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
        # COMPANION DAY EVENTS
        a_list.append("lucky_guards_car")
        a_list.append("mr_pecks_treasure")
        a_list.append("rusty_midnight_heist")
        a_list.append("whiskers_sixth_sense")
        a_list.append("slick_escape_route")
        a_list.append("hopper_lucky_day")
        a_list.append("patches_night_watch")
        a_list.append("squirrelly_stash")
        a_list.append("companion_sick_day")
        a_list.append("companion_rivalry")
        a_list.append("companion_hero_moment")
        a_list.append("companion_death_sacrifice")
        a_list.append("companion_nightmare")
        a_list.append("companion_lost_adventure")
        a_list.append("companion_bonded_moment")
        a_list.append("companion_learns_trick")
        a_list.append("companion_brings_friend")
        a_list.append("companion_food_crisis")
        a_list.append("companion_milestone")
        # CRAFTED ITEM EVENTS
        a_list.append("shiv_confrontation")
        a_list.append("lockpick_opportunity")
        a_list.append("fishing_day")
        a_list.append("trap_night_thief")
        a_list.append("dream_catcher_night")
        a_list.append("slingshot_bird_hunt")
        a_list.append("signal_mirror_rescue")
        a_list.append("rain_collector_bonus")
        a_list.append("fire_starter_campfire")
        a_list.append("companion_bed_bonus")
        a_list.append("worry_stone_moment")
        a_list.append("snare_trap_catch")
        a_list.append("binocular_scope_discovery")
        a_list.append("emergency_blanket_cold_night")
        a_list.append("lucky_charm_streak")
        a_list.append("water_purifier_use")
        a_list.append("pet_toy_playtime")
        a_list.append("home_remedy_illness")
        a_list.append("road_flare_torch_encounter")
        a_list.append("feeding_station_morning")
        a_list.append("splint_injury_event")
        # ITEM USE EVENTS - no-use item activation
        a_list.append("road_talisman_protection")
        a_list.append("silver_horseshoe_luck")
        a_list.append("mystery_potion_effect")
        a_list.append("feelgood_bottle_moment")
        a_list.append("persistent_bottle_refill")
        a_list.append("ritual_token_ceremony")
        a_list.append("council_feather_blessing")
        a_list.append("cowboy_jacket_encounter")
        a_list.append("found_phone_call")
        a_list.append("alien_crystal_event")
        a_list.append("dimensional_coin_flip")
        a_list.append("radio_numbers_broadcast")
        a_list.append("mysterious_envelope_reveal")
        a_list.append("lockbox_contents")
        a_list.append("hollow_tree_stash_find")
        a_list.append("vision_map_navigate")
        a_list.append("secret_route_shortcut")
        a_list.append("street_cat_ally_benefit")
        a_list.append("old_photograph_memory")
        a_list.append("beach_romance_call")
        a_list.append("apartment_key_visit")
        a_list.append("fake_flower_gift")
        a_list.append("empty_locket_memory")
        a_list.append("stack_of_flyers_opportunity")
        a_list.append("mysterious_key_lockbox_open")
        a_list.append("suspicious_package_open")
        a_list.append("stolen_watch_recognition")
        a_list.append("underwater_camera_photos")
        a_list.append("witch_ward_dark_protection")
        a_list.append("deck_of_cards_street_game")
        a_list.append("ace_of_spades_blackjack_omen")
        a_list.append("dealer_joker_revelation")
        a_list.append("magic_acorn_planting")
        a_list.append("treasure_map_follow")
        a_list.append("capture_fairy_release")
        a_list.append("lucky_lure_fishing")
        a_list.append("mysterious_code_decode")
        a_list.append("swamp_gold_attention")
        # Hermit Chain
        a_list.append("hermit_trail_discovery")
        a_list.append("hermit_camp_return")
        a_list.append("hermit_journal_study")
        a_list.append("hermit_trail_stranger")
        a_list.append("hermit_hollow_oak")
        # Midnight Radio Chain
        a_list.append("midnight_radio_signal")
        a_list.append("midnight_radio_frequency")
        a_list.append("midnight_radio_pole")
        a_list.append("midnight_radio_visit")
        a_list.append("midnight_radio_broadcast")
        # Junkyard Artisan Chain
        a_list.append("junkyard_artisan_meet")
        a_list.append("junkyard_lesson_one")
        a_list.append("junkyard_lesson_two")
        a_list.append("junkyard_gideon_story")
        a_list.append("junkyard_masterpiece")
        # Lost Dog Chain
        a_list.append("lost_dog_flyers_found")
        a_list.append("lost_dog_investigation")
        a_list.append("lost_dog_whistle_search")
        a_list.append("lost_dog_culprit")
        a_list.append("lost_dog_reunion")
        # Recurring Chain Item Events
        a_list.append("herbal_pouch_remedy")
        a_list.append("walking_stick_hike")
        a_list.append("tinfoil_hat_event")
        a_list.append("reunion_photo_comfort")
        a_list.append("junkyard_crown_moment")
        a_list.append("scrap_armor_event")
        # Crossover Events
        a_list.append("crossover_radio_hermit")
        a_list.append("crossover_artisan_rose_gift")
        a_list.append("crossover_night_vision_bonus")
        a_list.append("crossover_all_chains_complete")
        # CAR TROUBLE EVENTS - Nearly There Tier
        a_list.append("mystery_breakdown")
        a_list.append("flooded_engine")
        a_list.append("catalytic_converter_stolen")
        # CAR TROUBLE FOLLOW-UPS - Nearly There Tier
        a_list.append("engine_knock_worsens")
        a_list.append("broken_ball_joint_breaks")
        a_list.append("failing_fuel_pump_dies")
        a_list.append("bald_tires_hydroplane")
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
    
# ============================================
# WEIGHTED DAY EVENT POOL
# ============================================

    # Events defined in events_illness.py — routed through random_illness() dispatcher.
    # Conditional illness follow-ups (knife_wound_infection, etc.) are NOT here;
    # they stay in the pool and self-guard via has_danger() checks.
    _ILLNESS_NAMES = frozenset({
        "contract_cold", "contract_flu", "contract_pneumonia", "contract_bronchitis",
        "contract_strep_throat", "contract_stomach_flu", "contract_ear_infection",
        "contract_sinus_infection", "contract_uti", "contract_pink_eye", "contract_mono",
        "contract_shingles", "contract_lyme_disease", "contract_ringworm", "contract_scabies",
        "contract_staph_infection", "contract_tetanus", "contract_rabies_scare",
        "contract_measles", "develop_diabetes_symptoms", "high_blood_pressure_crisis",
        "severe_allergic_reaction", "asthma_attack", "kidney_stones", "gallbladder_attack",
        "appendicitis_attack", "blood_clot_in_leg", "migraine_severe", "vertigo_episode",
        "seizure_episode", "pancreatitis_attack", "severe_burn_injury", "concussion_injury",
        "broken_ribs_injury", "dislocated_shoulder", "broken_hand", "broken_wrist",
        "broken_ankle", "torn_acl", "herniated_disc", "deep_laceration", "puncture_wound",
        "second_degree_burns", "frostbite", "heat_stroke", "hypothermia", "crush_injury",
        "chemical_burn", "electrical_burn", "whiplash_injury", "jaw_fracture", "skull_fracture",
        "collapsed_lung", "ruptured_spleen", "liver_laceration", "ruptured_eardrum",
        "detached_retina", "orbital_fracture", "broken_nose", "broken_collarbone",
        "tooth_abscess", "blood_poisoning", "severe_dehydration", "malnutrition",
        "nerve_damage", "tendon_rupture", "muscle_tear", "gangrene_infection",
        "severe_anxiety_attack", "severe_depression_episode", "insomnia_chronic",
        "ptsd_flashback", "dirty_needle_stick", "bad_oysters", "rat_bite", "bad_mushrooms",
        "unclean_water", "mold_exposure", "bee_sting_allergy", "lead_poisoning",
        "asbestos_exposure", "mercury_poisoning", "gym_accident", "slip_in_shower",
        "fall_down_stairs", "car_accident_minor", "construction_site_accident",
        "bar_fight_aftermath", "kitchen_accident", "grease_fire", "sports_injury",
        "motorcycle_crash", "dog_attack_severe", "pool_diving_accident", "chemical_spill",
        "electric_shock", "workplace_injury", "assault_aftermath", "caught_in_fire",
        "frozen_outdoors", "heat_exhaustion_collapse", "drug_overdose_survival",
        "allergic_reaction_restaurant", "botched_surgery", "dental_disaster", "gym_collapse",
        "food_truck_nightmare", "public_pool_infection", "hiking_disaster", "wasp_nest_encounter",
        "camping_tick_bite", "homeless_shelter_outbreak", "prison_shiv_wound", "daycare_plague",
        "bad_tattoo_infection", "mma_fight_aftermath", "covid_complications",
        "earthquake_injury", "carnival_ride_accident", "window_crash", "trampoline_disaster",
        "explosion_nearby", "botched_piercing", "weight_dropping", "bad_sushi",
        "coma_awakening", "stress_breakdown", "trauma_flashback", "sleep_deprivation_crisis",
    })

    # Events defined in events_car.py — routed through random_car_trouble() dispatcher.
    # Conditional follow-ups (leaking_battery_worsens, etc.) are NOT here;
    # they stay in the pool and self-guard via has_danger() checks.
    _CAR_TROUBLE_NAMES = frozenset({
        "dead_battery_afternoon", "corroded_battery_terminals", "battery_acid_leak",
        "engine_overheating", "check_engine_light_on", "engine_wont_turn_over",
        "strange_engine_noise", "engine_oil_empty", "oil_leak_spotted", "slow_tire_leak",
        "tire_blowout", "bald_tires_noticed", "nail_in_tire", "headlights_burned_out",
        "alternator_failing", "fuse_blown", "car_alarm_malfunction", "starter_motor_grinding",
        "brakes_squealing", "brake_fluid_leak", "abs_light_on", "ran_out_of_gas",
        "fuel_pump_whining", "clogged_fuel_filter", "transmission_slipping", "stuck_in_gear",
        "radiator_leak", "thermostat_stuck", "water_pump_failing", "power_steering_failure",
        "wheel_alignment_off", "suspension_creaking", "broken_ball_joint", "exhaust_leak_loud",
        "catalytic_converter_stolen", "hail_damage", "flooded_engine", "windshield_cracked",
        "frozen_door_locks", "frozen_fuel_line", "mystery_breakdown", "key_wont_turn",
        "car_wont_go_in_reverse", "window_wont_roll_up", "trunk_wont_close",
        "gas_pedal_sticking", "parking_brake_stuck",
    })

    _CAR_DEPENDENT_DAY_NAMES = _CAR_TROUBLE_NAMES | frozenset({
        "car_battery_dead", "flat_tire_again", "mystery_car_problem_worsens",
        "fuel_leak_fire", "fuel_leak_fixed", "damaged_exhaust_fixed",
        "damaged_exhaust_again", "unpaid_tickets_boot", "booted_car_impound",
    })

    # Tonal weight per event across the 6 ranks [poor, cheap, modest, rich, doughman, nearly].
    # Higher number = more copies in the pool = more likely to fire at that rank.
    # Default for unlisted events (conditionals, chains, companions, items) is [1,1,1,1,1,1].
    # Events with weight 0 at a rank are skipped even if the builder includes them.
    _DAY_EVENT_TONE = {

        # ── SILLY / GOOFY ───────────────────────────────────────────────────────
        # Playful, absurd, zero stakes. Dominant early, completely absent late.
        "duck_army":               [4, 3, 2, 1, 0, 0],
        "sentient_sandwich":       [4, 3, 2, 1, 0, 0],
        "motivational_raccoon":    [4, 3, 2, 1, 0, 0],
        "pigeon_mafia":            [4, 3, 2, 1, 0, 0],
        "sock_puppet_therapist":   [4, 3, 2, 1, 0, 0],
        "dance_battle":            [4, 3, 2, 1, 0, 0],
        "alien_abduction":         [3, 2, 1, 0, 0, 0],
        "hungry_cow":              [3, 3, 2, 1, 0, 0],
        "ice_cream_truck":         [3, 3, 2, 1, 0, 0],
        "kid_on_bike":             [3, 3, 2, 1, 0, 0],
        "the_mime":                [3, 2, 1, 0, 0, 0],
        "opossum_in_trash":        [4, 3, 2, 1, 0, 0],
        "raccoon_gang_raid":       [4, 3, 2, 1, 0, 0],
        "sewer_rat":               [3, 3, 2, 1, 0, 0],
        "raccoon_raid":            [3, 3, 2, 1, 0, 0],
        "raccoon_invasion":        [3, 3, 2, 1, 0, 0],

        # ── MUNDANE / PEACEFUL ──────────────────────────────────────────────────
        # Quiet slice-of-life colour. Rich to have, feels out of place at high stakes.
        "morning_stretch":         [3, 3, 2, 1, 0, 0],
        "cloud_watching":          [3, 3, 2, 1, 0, 0],
        "bird_droppings":          [3, 3, 2, 1, 0, 0],
        "car_alarm_symphony":      [3, 3, 2, 1, 0, 0],
        "lucky_penny":             [3, 3, 2, 1, 0, 0],
        "seagull_attack":          [3, 3, 2, 1, 0, 0],
        "motivational_graffiti":   [3, 3, 2, 1, 0, 0],
        "dropped_ice_cream":       [3, 3, 2, 1, 0, 0],
        "talking_to_yourself":     [3, 3, 2, 1, 0, 0],
        "wrong_number":            [3, 3, 2, 1, 0, 0],
        "trash_treasure":          [3, 3, 2, 1, 0, 0],
        "coin_flip_stranger":      [3, 3, 2, 1, 0, 0],
        "stray_cat":               [3, 3, 2, 1, 0, 0],
        "three_legged_dog":        [3, 3, 2, 1, 0, 0],
        "estranged_dog":           [3, 3, 2, 1, 0, 0],
        "radio_static":            [3, 3, 2, 1, 0, 0],
        "mysterious_note":         [3, 3, 2, 1, 0, 0],
        "ant_invasion":            [3, 3, 2, 1, 0, 0],
        "left_window_down":        [3, 3, 2, 1, 0, 0],
        "vending_machine_luck":    [3, 3, 2, 1, 0, 0],
        "conspiracy_theorist":     [3, 3, 2, 0, 0, 0],
        "freight_truck":           [3, 3, 2, 1, 0, 0],
        "roadkill_philosophy":     [3, 2, 1, 0, 0, 0],
        "street_musician":         [2, 2, 1, 0, 0, 0],
        "deja_vu_again":           [2, 2, 1, 0, 0, 0],
        "car_wash_encounter":      [2, 2, 1, 0, 0, 0],
        "mosquito_bite_infection": [3, 2, 1, 0, 0, 0],
        "got_a_tan":               [3, 3, 2, 1, 0, 0],

        # ── SMALL EVERYDAY STRUGGLES ────────────────────────────────────────────
        # Present at all ranks but clearly fading as stakes grow.
        "good_hair_day":           [2, 2, 2, 1, 1, 0],
        "bad_hair_day":            [2, 2, 2, 1, 1, 0],
        "nice_weather":            [2, 2, 2, 1, 1, 0],
        "terrible_weather":        [2, 2, 2, 1, 1, 0],
        "back_pain":               [2, 2, 2, 1, 1, 0],
        "stretching_helps":        [2, 2, 2, 1, 1, 0],
        "weird_noise":             [2, 2, 2, 1, 0, 0],
        "found_twenty":            [2, 2, 2, 1, 0, 0],
        "lost_wallet":             [2, 2, 2, 1, 0, 0],
        "sunburn":                 [2, 2, 2, 1, 0, 0],
        "flat_tire":               [2, 2, 1, 0, 0, 0],
        "flat_tire_again":         [2, 2, 1, 0, 0, 0],
        "car_battery_dead":        [2, 2, 1, 0, 0, 0],
        "found_gift_card":         [2, 2, 2, 1, 0, 0],
        "random_kindness":         [2, 2, 2, 1, 1, 0],
        "random_cruelty":          [2, 2, 2, 2, 1, 1],
        "someone_stole_your_stuff":[2, 2, 2, 1, 0, 0],
        "prayer_answered":         [2, 2, 2, 2, 2, 2],
        "prayer_ignored":          [2, 2, 2, 2, 2, 2],
        "found_old_photo":         [2, 2, 2, 1, 1, 1],
        "threw_out_old_photo":     [1, 1, 2, 2, 2, 1],
        "morning_fog":             [2, 2, 2, 1, 0, 0],
        "car_wont_start":          [2, 2, 1, 0, 0, 0],
        "strong_winds":            [2, 2, 2, 1, 0, 0],
        "beautiful_sunrise":       [2, 2, 2, 1, 1, 0],

        # ── POOR/CHEAP SPECIFIC ─────────────────────────────────────────────────
        # Events that only make thematic sense while broke.
        "seat_cash":               [3, 0, 0, 0, 0, 0],
        "sun_visor_bills":         [2, 3, 1, 0, 0, 0],
        "fortune_cookie":          [2, 2, 1, 0, 0, 0],
        "broken_atm":              [2, 2, 1, 0, 0, 0],
        "lottery_scratch":         [2, 2, 1, 0, 0, 0],
        "parking_lot_poker":       [2, 2, 1, 0, 0, 0],
        "free_sample_spree":       [2, 2, 1, 0, 0, 0],
        "phone_scam_call":         [2, 2, 1, 0, 0, 0],
        "yard_sale_find":          [2, 2, 1, 0, 0, 0],
        "friendly_drunk":          [2, 2, 1, 0, 0, 0],
        "completely_broke_wisdom": [3, 1, 0, 0, 0, 0],
        "rock_bottom":             [2, 2, 1, 0, 0, 0],
        "grimy_gus_discovery":     [1, 3, 3, 2, 0, 0],
        "vinnie_referral_card":    [3, 4, 3, 2, 1, 0],
        "windblown_worn_map":      [2, 5, 4, 2, 0, 0],
        "flea_market_route_map":   [1, 4, 4, 2, 0, 0],
        "laundromat_bulletin_map": [0, 3, 4, 2, 0, 0],
        "witch_doctor_matchbook": [0, 1, 2, 1, 0, 0],
        "roadside_bone_chimes":   [0, 1, 2, 1, 0, 0],
        "trusty_tom_coupon_mailer": [0, 2, 2, 1, 0, 0],
        "filthy_frank_radio_giveaway": [0, 1, 2, 1, 0, 0],
        "oswald_concierge_card":   [0, 1, 1, 1, 0, 0],

        # ── GRITTY DANGER ───────────────────────────────────────────────────────
        # Real consequence events. Rare early (player is scraping by), escalate
        # through mid game, then level off at endgame where tone shifts darker.
        "back_alley_shortcut":     [1, 1, 2, 3, 0, 0],
        "food_poisoning":          [1, 1, 2, 2, 1, 0],
        "attacked_by_dog":         [1, 1, 1, 0, 0, 0],
        "carbon_monoxide":         [1, 1, 2, 2, 2, 1],
        "gas_station_robbery":     [0, 1, 1, 1, 0, 0],
        "drug_dealer_encounter":   [0, 1, 2, 3, 3, 2],
        "electrocution_hazard":    [0, 1, 1, 1, 0, 0],
        "car_explosion":           [0, 1, 1, 2, 2, 1],
        "heart_attack_scare":      [0, 0, 1, 2, 3, 4],

        # ── DARK / HORROR ───────────────────────────────────────────────────────
        # Heavy, irreversible, life-threatening. Must feel EARNED by wealth.
        # Near-absent early, completely dominant at doughman/nearly.
        "blood_moon_bargain":      [0, 0, 1, 2, 3, 4],
        "the_empty_room":          [0, 0, 1, 2, 3, 4],
        "the_dying_dealer":        [0, 0, 0, 1, 3, 3],
        "the_high_roller_suicide": [0, 0, 0, 0, 2, 4],
        "casino_hitman":           [0, 0, 0, 0, 0, 4],
        "organ_harvester":         [0, 0, 0, 1, 3, 3],
        "the_bridge_call":         [0, 0, 0, 1, 3, 4],
        "the_relapse":             [0, 0, 0, 1, 3, 4],
        "cancer_diagnosis":        [0, 0, 0, 1, 3, 3],
        "casino_overdose":         [0, 0, 0, 1, 3, 3],
        "withdrawal_nightmare":    [0, 0, 0, 1, 3, 3],
        "the_desperate_gambler":   [0, 0, 0, 1, 3, 3],
        "loan_shark_visit":        [0, 0, 0, 1, 3, 3],
        "likely_death":            [0, 0, 0, 0, 3, 0],  # one-time, doughman only
        "the_confession":          [0, 0, 0, 1, 2, 3],
        "the_anniversary_loss":    [0, 0, 0, 1, 2, 3],
        "survivor_guilt":          [0, 0, 0, 1, 2, 3],
        "the_scar_story":          [0, 0, 0, 1, 2, 2],
        "the_winning_streak_paranoia": [0, 0, 0, 1, 2, 3],
        "old_gambling_buddy":      [0, 0, 0, 1, 2, 2],

        # ── SURREAL / EXISTENTIAL ───────────────────────────────────────────────
        # Tone escalates from quirky oddity to genuine dread as wealth grows.
        "time_loop":               [1, 1, 2, 2, 3, 3],
        "mirror_stranger":         [1, 1, 2, 2, 3, 3],
        "the_glitch":              [1, 1, 2, 2, 3, 3],
        "fourth_wall_break":       [1, 1, 2, 2, 3, 3],
        "wrong_universe":          [1, 1, 2, 2, 0, 0],  # too playful at endgame
        "the_collector":           [0, 0, 1, 2, 3, 3],
        # Existential events kept at 1 copy at rich — a whisper, not a shout.
        # They're conditional anyway (require prior status/danger) so mostly
        # they self-guard. The player feels them as a vague unease, nothing more.
        "soulless_emptiness":      [0, 0, 1, 1, 3, 3],
        "soulless_mirror":         [0, 0, 1, 1, 3, 3],
        "soulless_recognition":    [0, 0, 1, 1, 3, 3],
        "haunted_by_losses":       [0, 0, 1, 1, 3, 3],
        "wealth_anxiety":          [0, 0, 1, 1, 3, 3],
        "bridge_contemplation":    [0, 0, 1, 1, 3, 4],
        "devils_bargain_consequence": [0, 0, 0, 1, 3, 4],
        "insomniac_revelation":    [1, 1, 1, 2, 2, 2],
        "the_sleeping_stranger":   [2, 2, 1, 1, 0, 0],
        "the_cat_knows":           [1, 1, 1, 1, 1, 1],
        "rain_on_the_roof":        [1, 1, 1, 1, 1, 1],
        "found_old_photo":         [2, 2, 2, 1, 1, 1],
        "perfect_health_moment":   [1, 1, 1, 1, 1, 1],
        "first_sunrise":           [2, 1, 1, 1, 1, 0],
        "the_veteran_gambler":     [0, 1, 1, 1, 2, 2],
        "the_crow_council":        [0, 1, 1, 1, 2, 2],
        "birthday_forgotten":      [0, 0, 0, 1, 2, 2],
        "item_hoarder":            [0, 0, 1, 1, 2, 2],
        "companion_reunion":       [0, 1, 1, 1, 1, 1],
        # Nothing happens. Days disappear. Present everywhere; fades at top tiers
        # where you're too active (or too terrified) to waste a whole day doing nothing.
        "empty_event":             [2, 2, 2, 1, 1, 0],
        # ── CHAIN / CONDITIONAL ─────────────────────────────────────────────────
        # All self-guard via has_danger/has_met; weight just lets them surface
        # when their condition becomes active. [0] = excluded at that rank.
        "starving_cow":            [0, 1, 2, 0, 0, 0],  # Betsy chain pt.2 (modest peak)
        "cow_army":                [0, 0, 0, 0, 2, 1],  # Betsy finale — doughman/nearly
        "even_further_interrogation": [0, 0, 0, 1, 1, 0],  # Interrogation pt.3 — rich+

        # ── WEALTH-TIER MID (modest / rich) ─────────────────────────────────────
        # Rich tier is the calm before the storm — VIP events dominate, the world
        # is rewarding the player, everything feels almost too good. Darkness
        # starts at doughman; here it is only a whisper the player can ignore.
        "luxury_car_passes":       [0, 0, 2, 4, 2, 1],
        "paparazzi_mistake":       [0, 0, 2, 4, 2, 1],
        "imposter_syndrome":       [0, 0, 2, 4, 2, 1],
        "charity_opportunity":     [0, 0, 2, 4, 2, 1],
        "investment_opportunity":  [0, 0, 2, 4, 2, 1],
        "expensive_taste":         [0, 0, 2, 4, 2, 1],
        "autograph_request":       [0, 0, 1, 4, 2, 1],
        "casino_regular":          [0, 0, 1, 4, 2, 1],
        "mysterious_package":      [0, 0, 1, 3, 2, 1],
        "rich_persons_problems":   [0, 0, 1, 4, 2, 1],
        "investment_pitch":        [0, 0, 1, 4, 2, 1],
        "news_van":                [0, 0, 1, 3, 2, 1],
        "fancy_restaurant_mistake":[0, 0, 2, 4, 2, 1],
        "luxury_problems":         [0, 0, 2, 4, 2, 1],
        "left_trunk_open":         [0, 0, 1, 3, 2, 1],
        "classy_encounter":        [0, 0, 0, 4, 2, 1],
        "wine_and_dine":           [0, 0, 0, 4, 2, 1],
        "cigar_circle":            [0, 0, 0, 4, 2, 1],
        "lucky_rabbit_encounter":  [0, 0, 0, 4, 2, 1],
        "old_rival_encounter":     [0, 0, 1, 2, 2, 1],
        "media_known_harassed":    [0, 0, 1, 1, 2, 1],  # whisper at rich
        "media_known_documentary": [0, 0, 1, 1, 2, 1],  # whisper at rich
        "high_roller_room_visit":  [0, 0, 0, 3, 3, 2],
        "high_roller_whale":       [0, 0, 0, 3, 3, 2],

        # ── WEALTH-TIER HIGH (doughman / nearly) ────────────────────────────────
        # Endgame pressure events. The casino knows you. Everyone knows you.
        "reporters_found_you":     [0, 0, 0, 1, 3, 4],
        "casino_knows":            [0, 0, 0, 0, 3, 4],
        "casino_owner_meeting":    [0, 0, 0, 0, 3, 4],
        "almost_there":            [0, 0, 0, 0, 2, 4],
        "the_weight_of_wealth":    [0, 0, 0, 0, 3, 4],
        "wealth_paranoia":         [0, 0, 0, 1, 3, 4],
        "millionaire_fantasy":     [0, 0, 0, 0, 3, 3],
        "high_roller_room":        [0, 0, 0, 0, 3, 3],
        "last_stretch":            [0, 0, 0, 0, 0, 4],
        "strange_visitors":        [0, 0, 0, 0, 2, 4],
        "the_final_temptation":    [0, 0, 0, 0, 2, 4],
        "high_stakes_feeling":     [0, 0, 0, 0, 3, 4],
        "casino_security":         [0, 0, 0, 1, 3, 3],
        "wealthy_doubts":          [0, 0, 0, 1, 3, 3],
        "people_watching":         [0, 0, 0, 1, 2, 2],
        "money_counting_ritual":   [0, 0, 0, 0, 3, 3],
        "nervous_habits":          [0, 0, 0, 1, 3, 3],
        "millionaire_milestone":   [0, 0, 0, 0, 3, 3],
        "old_rival_returns":       [0, 0, 0, 1, 3, 2],
        "casino_comps":            [0, 0, 0, 0, 3, 3],
        "thunderstorm":            [0, 0, 0, 1, 3, 4],
        "too_close_to_quit":       [0, 0, 0, 0, 0, 3],
    }

    def make_weighted_day_pool(self, rank):
        """Build a shuffled and tonally weighted event pool for the given rank.

        Each event is looked up in _DAY_EVENT_TONE; the value at [rank] is the
        number of times it appears in the pool (0 = excluded at this rank).
        Unlisted events default to 1 copy — this covers conditional follow-ups,
        companion events, crafted-item events, chain events, and one-time story
        events (all of which self-guard via has_danger/has_met etc.).

        Illness and car-trouble names are stripped entirely and replaced by
        dispatcher entries ('random_illness', 'random_car_trouble') whose copy
        count escalates with rank, so danger naturally compounds with wealth.
        """
        builders = [
            self.make_poor_day_events_list,
            self.make_cheap_day_events_list,
            self.make_modest_day_events_list,
            self.make_rich_day_events_list,
            self.make_doughman_day_events_list,
            self.make_nearly_day_events_list,
        ]
        has_car = self.__player.has_item("Car")
        base_events = [
            e for e in builders[rank]()
            if e not in self._ILLNESS_NAMES
            and e not in self._CAR_TROUBLE_NAMES
            and (has_car or e not in self._CAR_DEPENDENT_DAY_NAMES)
        ]
        default = [1, 1, 1, 1, 1, 1]
        pool = []
        for e in base_events:
            copies = self._DAY_EVENT_TONE.get(e, default)[rank]
            if copies > 0:
                pool.extend([e] * copies)
        # Illness: rich tier drops to 3 — they can afford doctors.
        # Doughman spikes back to 5; stress and dark money take their toll.
        # Car: rich drops to 1 — valet, good mechanics, it's handled.
        illness_copies = [2, 2, 3, 3, 5, 5][rank]
        car_copies     = [3, 3, 3, 1, 2, 1][rank]
        pool += ["random_illness"] * illness_copies
        if has_car:
            pool += ["random_car_trouble"] * car_copies
        random.shuffle(pool)
        return pool

# Get Event
    def get_day_event(self):
        rank = self.__player.get_rank()
        match rank:
            case 0:
                if len(self.__poor_day_events) == 0:
                    self.__poor_day_events = self.make_weighted_day_pool(0)
                return self.__poor_day_events.pop()
            case 1:
                if len(self.__cheap_day_events) == 0:
                    self.__cheap_day_events = self.make_weighted_day_pool(1)
                return self.__cheap_day_events.pop()
            case 2:
                if len(self.__modest_day_events) == 0:
                    self.__modest_day_events = self.make_weighted_day_pool(2)
                return self.__modest_day_events.pop()
            case 3:
                if len(self.__rich_day_events) == 0:
                    self.__rich_day_events = self.make_weighted_day_pool(3)
                return self.__rich_day_events.pop()
            case 4:
                if len(self.__doughman_day_events) == 0:
                    self.__doughman_day_events = self.make_weighted_day_pool(4)
                return self.__doughman_day_events.pop()
            case 5:
                if len(self.__nearly_day_events) == 0:
                    self.__nearly_day_events = self.make_weighted_day_pool(5)
                return self.__nearly_day_events.pop()
    

    def get_night_event(self):
        rank = self.__player.get_rank()
        match rank:
            case 0:
                return self._pull_night_event("_Lists__poor_night_events", self.make_poor_night_events_list)
            case 1:
                return self._pull_night_event("_Lists__cheap_night_events", self.make_cheap_night_events_list)
            case 2:
                return self._pull_night_event("_Lists__modest_night_events", self.make_modest_night_events_list)
            case 3:
                return self._pull_night_event("_Lists__rich_night_events", self.make_rich_night_events_list)
            case 4:
                return self._pull_night_event("_Lists__doughman_night_events", self.make_doughman_night_events_list)
            case 5:
                return self._pull_night_event("_Lists__nearly_night_events", self.make_nearly_night_events_list)

    def make_shop_list(self, on_foot=False):
        a_list = []
        # There is no on-foot travel in this game.
        # Without a car the afternoon is skipped entirely (game calls night_event directly).
        if on_foot:
            return a_list
        if(not self.__player.has_danger("Doctor Ban")):
            a_list.append("Doctor's Office")
        if((not on_foot) and self.__player.has_met("Witch")):
            a_list.append("Witch Doctor's Tower")
        if(self.__player.has_met("Tom")):
            a_list.append("Trusty Tom's Trucks and Tires")
        if(self.__player.has_met("Frank")):
            a_list.append("Filthy Frank's Flawless Fixtures")
        if(self.__player.has_met("Oswald")):
            a_list.append("Oswald's Optimal Outoparts")
        if(not on_foot):
            a_list.append("Convenience Store")
        if((not on_foot) and (self.__player.has_item("Map") or self.__player.has_item("Worn Map"))):
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
        # Tanya's therapy office - unlocked by getting her number
        if(self.__player.has_item("Tanya's Number")):
            a_list.append("Tanya's Office")
        # Car Workbench - unlocked by owning a Tool Kit
        if((not on_foot) and self.__player.has_item("Tool Kit")):
            a_list.append("Car Workbench")
        # Airport unlocks when you're a millionaire
        if((not on_foot) and self.__player.get_balance() >= 1000000):
            a_list.append("Airport")
        return a_list

    def make_convenience_store_inventory(self):
        a_list = []
        rank = self.__player.get_rank()
        
        # === FOOD ITEMS (Always available, rotating selection) ===
        food_items = [
            ("Candy Bar", 5), ("Bag of Chips", 8), ("Turkey Sandwich", 15),
            ("Energy Drink", 12), ("Beef Jerky", 10), ("Cup Noodles", 7),
            ("Granola Bar", 6), ("Hot Dog", 8), ("Microwave Burrito", 9),
            ("Cheese", 4), ("Bread", 3), ("Sandwich", 8),
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
        if (self.__player.has_item("Tool Kit") or random.randrange(4) == 0) and not self.__player.has_item("Duct Tape"):
            a_list.append(("Duct Tape", 12))
        if (self.__player.has_item("Tool Kit") or random.randrange(5) == 0) and not self.__player.has_item("Pocket Knife"):
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
            if random.randrange(6) == 0 and not self.__player.has_item("Worn Map"):
                a_list.append(("Worn Map", 8))
            if random.randrange(4) == 0 and not self.__player.has_item("Matches"):
                a_list.append(("Matches", 2))
            if random.randrange(4) == 0 and not self.__player.has_item("Birdseed"):
                a_list.append(("Birdseed", 4))
            if random.randrange(5) == 0 and not self.__player.has_item("Baking Soda"):
                a_list.append(("Baking Soda", 3))
        
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
            if random.randrange(5) == 0 and not self.__player.has_item("Dog Whistle"):
                a_list.append(("Dog Whistle", 22))
            if random.randrange(4) == 0 and not self.__player.has_item("Premium Sunscreen"):
                a_list.append(("Premium Sunscreen", 18))
            if random.randrange(5) == 0 and not self.__player.has_item("Battery Terminal Cleaner"):
                a_list.append(("Battery Terminal Cleaner", 10))
            if random.randrange(4) == 0 and not self.__player.has_item("Poncho"):
                a_list.append(("Poncho", 12))
            if random.randrange(5) == 0 and not self.__player.has_item("Running Shoes"):
                a_list.append(("Running Shoes", 45))
        
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
            if (self.__player.has_item("Tool Kit") or random.randrange(4) == 0) and not self.__player.has_item("Fishing Line"):
                a_list.append(("Fishing Line", 18))
            if (self.__player.has_item("Tool Kit") or random.randrange(3) == 0) and not self.__player.has_item("Super Glue"):
                a_list.append(("Super Glue", 12))
            if random.randrange(4) == 0 and not self.__player.has_item("Hand Warmers"):
                a_list.append(("Hand Warmers", 10))
            if random.randrange(5) == 0 and not self.__player.has_item("Welding Goggles"):
                a_list.append(("Welding Goggles", 40))
            if random.randrange(6) == 0 and not self.__player.has_item("Signal Booster"):
                a_list.append(("Signal Booster", 55))
        
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
        if not self.__player.has_item("Tool Kit"):
            a_list.append(("Tool Kit", 85))
        if random.randrange(5) == 0 and not self.__player.has_item("WD-40"):
            a_list.append(("WD-40", 12))
        if (self.__player.has_item("Tool Kit") or random.randrange(6) == 0) and not self.__player.has_item("Bungee Cords"):
            a_list.append(("Bungee Cords", 15))
        if (self.__player.has_item("Tool Kit") or random.randrange(7) == 0) and not self.__player.has_item("Rope"):
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

        random_chance = random.randrange(5)
        if (random_chance<=1) and (not self.__player.has_item("Marvin's Monocle")):
            a_list.append("Marvin's Monocle")

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


    # ==========================================
    # WHISKERS (ALLEY CAT) DAILY DIALOGUE
    # ==========================================

    def make_whiskers_happy_list(self):
        a_list = []
        a_list.append("Whiskers stretches out across the dashboard, soaking up the morning sun like she owns the car. She probably does.")
        a_list.append("Whiskers brings you a dead moth she found under the seat. She drops it at your feet, looks up at you expectantly. This is love.")
        a_list.append("Whiskers headbutts your hand over and over until you scratch behind her ears. The purring is thunderous.")
        a_list.append("Whiskers is in a playful mood, batting at the dangling air freshener like it personally offended her.")
        a_list.append("Whiskers curls up on the warm spot where you were just sitting. She kneads the seat, purring, and falls asleep in seconds.")
        a_list.append("Whiskers slow-blinks at you from across the car. You slow-blink back. The ritual is complete.")
        a_list.append("Whiskers finds a stray shoelace and goes absolutely feral on it. Five minutes of chaos. Then she licks her paw like nothing happened.")
        a_list.append("Whiskers climbs onto your shoulder and nuzzles your ear. Her whiskers tickle. You don't dare move.")
        a_list.append("Whiskers catches a fly mid-air. She looks at you like, 'Did you see that?' You did. You're impressed.")
        a_list.append("Whiskers rolls onto her back, all four paws in the air. A belly trap? Or genuine trust? You risk a pet. She lets you. You've won today.")
        a_list.append("Whiskers grooms your eyebrows while you're trying to read. Apparently they were a mess.")
        a_list.append("Whiskers perches on the steering wheel and pretends to drive. She's a terrible driver. But she looks adorable.")
        random.shuffle(a_list)
        return a_list

    def get_whiskers_happy_update(self):
        if len(self.__whiskers_happy_list) == 0:
            self.__whiskers_happy_list = self.make_whiskers_happy_list()
        return self.__whiskers_happy_list.pop()

    def make_whiskers_unhappy_list(self):
        a_list = []
        a_list.append("Whiskers sits with her back to you. The cold shoulder is real.")
        a_list.append("Whiskers won't eat. She just stares at the food, then at you, then turns away.")
        a_list.append("Whiskers hides under the passenger seat and won't come out, no matter how many treats you offer.")
        a_list.append("Whiskers hisses at you when you reach for her. Okay. Message received.")
        a_list.append("Whiskers has been scratching the upholstery. Passive-aggressive redecorating.")
        a_list.append("Whiskers knocks your coffee off the dashboard. On purpose. While maintaining eye contact.")
        a_list.append("Whiskers sits in the window with her ears pinned back, watching the world like it failed her.")
        a_list.append("Whiskers is grooming excessively. Stress cleaning. She's not okay.")
        a_list.append("Whiskers meows at the door. She wants out. The thought of her leaving makes your chest hurt.")
        a_list.append("Whiskers swipes at your hand when you try to pet her. No claws. But the message is clear.")
        random.shuffle(a_list)
        return a_list

    def get_whiskers_unhappy_update(self):
        if len(self.__whiskers_unhappy_list) == 0:
            self.__whiskers_unhappy_list = self.make_whiskers_unhappy_list()
        return self.__whiskers_unhappy_list.pop()

    def make_whiskers_weather_list(self):
        a_list = []
        a_list.append("Whiskers presses herself flat against the floorboard. Thunder terrifies her.")
        a_list.append("Whiskers's ears rotate like radar dishes with every crack of thunder. She's on high alert.")
        a_list.append("Whiskers hides inside your jacket. You can feel her trembling against your chest.")
        a_list.append("Whiskers watches the rain hit the windshield, tracking each drop with laser focus. Hunting instinct never sleeps.")
        a_list.append("Whiskers curls into the tightest ball you've ever seen. The storm will pass. She'll survive it in a sphere.")
        random.shuffle(a_list)
        return a_list

    def get_whiskers_weather_update(self):
        if len(self.__whiskers_weather_list) == 0:
            self.__whiskers_weather_list = self.make_whiskers_weather_list()
        return self.__whiskers_weather_list.pop()

    def make_whiskers_morning_list(self):
        a_list = []
        a_list.append("Whiskers yawns, showing every single tiny fang. Good morning to you too.")
        a_list.append("Whiskers stretches — front paws out, butt in the air, back arched. The morning yoga routine.")
        a_list.append("Whiskers drops a dead bug on your chest to wake you up. Breakfast in bed, cat-style.")
        a_list.append("Whiskers is already awake, sitting perfectly still on the dashboard, silhouetted against the sunrise. She looks regal.")
        a_list.append("Whiskers paws at your face until you open your eyes. Then she walks away. She just wanted to know you were alive.")
        a_list.append("Whiskers demands breakfast by walking across your face. Repeatedly.")
        a_list.append("Whiskers sits on the hood of the car, watching the birds. Planning.")
        a_list.append("Whiskers has been grooming herself since before dawn. Looking sharp for another day of doing nothing.")
        random.shuffle(a_list)
        return a_list

    def get_whiskers_morning_update(self):
        if len(self.__whiskers_morning_list) == 0:
            self.__whiskers_morning_list = self.make_whiskers_morning_list()
        return self.__whiskers_morning_list.pop()

    # ==========================================
    # LUCKY (THREE-LEGGED DOG) DAILY DIALOGUE
    # ==========================================

    def make_lucky_happy_list(self):
        a_list = []
        a_list.append("Lucky does a three-legged zoomie around the parking lot. He's missing a leg but not a care in the world.")
        a_list.append("Lucky brings you a stick he found. Then he brings another. And another. Your car is filling with sticks.")
        a_list.append("Lucky puts his head in your lap and sighs the most contented sigh you've ever heard. This is his happy place.")
        a_list.append("Lucky's tail wags so hard it thumps against the car door like a drum. Ba-dum, ba-dum, ba-dum.")
        a_list.append("Lucky licks your hand for a solid thirty seconds. Then your face. Then your ear. He's thorough.")
        a_list.append("Lucky sees another dog through the window and loses his entire mind. FRIEND! FRIEND! FRIEND!")
        a_list.append("Lucky rolls in something questionable outside and comes back grinning. He smells terrible. He's so happy.")
        a_list.append("Lucky falls asleep mid-tail-wag. The tail just... stops. But his face is pure peace.")
        a_list.append("Lucky chases his own tail. Well, tries to. Three legs make it more of a spiral. He doesn't care.")
        a_list.append("Lucky digs a hole in the grass outside, buries absolutely nothing, and pats it down proudly. Job well done.")
        a_list.append("Lucky steals your sock and parades around with it like he won a trophy.")
        a_list.append("Lucky tries to fit on your lap. He does not fit. He doesn't care. He's on your lap now.")
        random.shuffle(a_list)
        return a_list

    def get_lucky_happy_update(self):
        if len(self.__lucky_happy_list) == 0:
            self.__lucky_happy_list = self.make_lucky_happy_list()
        return self.__lucky_happy_list.pop()

    def make_lucky_unhappy_list(self):
        a_list = []
        a_list.append("Lucky whimpers softly, pressing his nose into the corner of the seat.")
        a_list.append("Lucky won't eat. He just nudges the food bowl with his nose and walks away.")
        a_list.append("Lucky lies with his chin on his paws, eyes open, staring at nothing. The light in them is dim.")
        a_list.append("Lucky limps more than usual today. The phantom pain in his missing leg is acting up.")
        a_list.append("Lucky doesn't wag his tail when you say his name. That's never happened before.")
        a_list.append("Lucky tried to jump onto the seat and fell. He just lay there for a minute. You both pretended it didn't happen.")
        a_list.append("Lucky flinches when you raise your hand. Old scars. Old memories. You move slowly, gently.")
        a_list.append("Lucky looks at the door. Then at you. Then at the door. He's thinking about leaving. It breaks your heart.")
        a_list.append("Lucky howls softly at night. Not at the moon. At nothing. At everything.")
        a_list.append("Lucky licks the stump where his leg used to be. Over and over. Some wounds never fully heal.")
        random.shuffle(a_list)
        return a_list

    def get_lucky_unhappy_update(self):
        if len(self.__lucky_unhappy_list) == 0:
            self.__lucky_unhappy_list = self.make_lucky_unhappy_list()
        return self.__lucky_unhappy_list.pop()

    def make_lucky_weather_list(self):
        a_list = []
        a_list.append("Lucky hates thunder. He crawls under the steering column and won't come out.")
        a_list.append("Lucky presses his whole body against you during the storm. He's shaking. You hold him tight.")
        a_list.append("Lucky barks at the lightning. Defending you from the sky itself.")
        a_list.append("Lucky whines with every thunderclap, shoving his face deeper into your armpit.")
        a_list.append("Lucky pants heavily in the rain. Not heat — anxiety. You rub his ears and whisper that it's okay.")
        random.shuffle(a_list)
        return a_list

    def get_lucky_weather_update(self):
        if len(self.__lucky_weather_list) == 0:
            self.__lucky_weather_list = self.make_lucky_weather_list()
        return self.__lucky_weather_list.pop()

    def make_lucky_morning_list(self):
        a_list = []
        a_list.append("Lucky wakes you up by licking your entire face. Every inch. No corner untouched.")
        a_list.append("Lucky is already sitting by the door when you wake up. Tail wagging. Ready for the day. You're not.")
        a_list.append("Lucky stretches and yawns, tongue curling out impossibly far. Good morning, buddy.")
        a_list.append("Lucky nudges your hand with his cold, wet nose. Time to get up. Time to pet him.")
        a_list.append("Lucky stands guard by the window, watching the sunrise. Protecting you even from the morning.")
        a_list.append("Lucky wags his tail so hard the whole car rocks. He dreamed of you. You can tell.")
        a_list.append("Lucky brings you a shoe. Not because he fetched it. Because he wants you to get up and go outside with him.")
        a_list.append("Lucky makes little wuffing sounds in his sleep. Chasing dream rabbits. Living his best unconscious life.")
        random.shuffle(a_list)
        return a_list

    def get_lucky_morning_update(self):
        if len(self.__lucky_morning_list) == 0:
            self.__lucky_morning_list = self.make_lucky_morning_list()
        return self.__lucky_morning_list.pop()

    # ==========================================
    # MR. PECKS (CROW) DAILY DIALOGUE
    # ==========================================

    def make_pecks_happy_list(self):
        a_list = []
        a_list.append("Mr. Pecks perches on the rearview mirror and caws triumphantly. He found something. It's a button. He's never been more proud.")
        a_list.append("Mr. Pecks does a little hop-dance on the hood of the car. Left foot, right foot, spin. Encore!")
        a_list.append("Mr. Pecks drops a shiny bottle cap in your hand, then puffs up his chest. A worthy tribute, apparently.")
        a_list.append("Mr. Pecks mimics your car alarm perfectly. Scares the hell out of a passerby. He looks pleased.")
        a_list.append("Mr. Pecks brings you a french fry he stole from someone's plate at the diner. Still warm. Crime pays.")
        a_list.append("Mr. Pecks gently pulls at your hair. Not yanking. Grooming. You're part of his flock.")
        a_list.append("Mr. Pecks plays a game where he drops a pebble and catches it before it hits the ground. Over and over. He never misses.")
        a_list.append("Mr. Pecks sits on your shoulder, fluffs up his feathers, and closes his eyes. You're his favorite perch.")
        a_list.append("Mr. Pecks caws at other birds until they fly away. This is HIS human. Back off.")
        a_list.append("Mr. Pecks leaves a line of breadcrumbs leading to a quarter he found. Treasure map. X marks the spot.")
        a_list.append("Mr. Pecks learned to knock on the window with his beak. Tap-tap-tap. Let me in. It's freezing out here.")
        a_list.append("Mr. Pecks is having a full conversation with a group of crows outside. They keep looking at you. What are they saying?")
        random.shuffle(a_list)
        return a_list

    def get_pecks_happy_update(self):
        if len(self.__pecks_happy_list) == 0:
            self.__pecks_happy_list = self.make_pecks_happy_list()
        return self.__pecks_happy_list.pop()

    def make_pecks_unhappy_list(self):
        a_list = []
        a_list.append("Mr. Pecks sits on the roof with his back to you. Hasn't moved in hours.")
        a_list.append("Mr. Pecks drops a rock next to your head. Not AT you. Near you. A warning.")
        a_list.append("Mr. Pecks won't take food from your hand anymore. He eats it off the ground instead. The disrespect.")
        a_list.append("Mr. Pecks makes a low, guttural sound. Crow for 'I'm not happy with how things are going.'")
        a_list.append("Mr. Pecks flies away for hours. You sit there wondering if he's coming back. He does. Barely.")
        a_list.append("Mr. Pecks stops bringing you gifts. The shiny things dry up. The relationship is strained.")
        a_list.append("Mr. Pecks sits on a telephone wire, watching you from a distance. Close enough to see. Far enough to leave.")
        a_list.append("Mr. Pecks pecks at the window glass aggressively. Tap. Tap. TAP. Something's wrong.")
        a_list.append("Mr. Pecks caws at you in a tone you haven't heard before. It sounds angry. Disappointed. Both.")
        a_list.append("Mr. Pecks ruffles his feathers and looks small. He's not puffing up. He's deflating.")
        random.shuffle(a_list)
        return a_list

    def get_pecks_unhappy_update(self):
        if len(self.__pecks_unhappy_list) == 0:
            self.__pecks_unhappy_list = self.make_pecks_unhappy_list()
        return self.__pecks_unhappy_list.pop()

    def make_pecks_weather_list(self):
        a_list = []
        a_list.append("Mr. Pecks tucks his head under his wing. The rain makes his feathers heavy.")
        a_list.append("Mr. Pecks presses against the window from inside, watching the storm like it owes him money.")
        a_list.append("Mr. Pecks paces back and forth on the dashboard during thunder. Agitated. Alert.")
        a_list.append("Mr. Pecks fluffs up into a round ball of wet feathers. He looks miserable. And spherical.")
        a_list.append("Mr. Pecks caws at the thunder like he can argue with it. He can't. He tries anyway.")
        random.shuffle(a_list)
        return a_list

    def get_pecks_weather_update(self):
        if len(self.__pecks_weather_list) == 0:
            self.__pecks_weather_list = self.make_pecks_weather_list()
        return self.__pecks_weather_list.pop()

    def make_pecks_morning_list(self):
        a_list = []
        a_list.append("Mr. Pecks caws at sunrise. Every single morning. Your alarm clock has feathers.")
        a_list.append("Mr. Pecks is already awake, arranging his collection of shiny objects on the dashboard. Inventory day.")
        a_list.append("Mr. Pecks taps on the glass with his beak until you wake up. Persistent doesn't begin to describe it.")
        a_list.append("Mr. Pecks drops a worm on the windshield. Breakfast delivery. He's looking at you expectantly.")
        a_list.append("Mr. Pecks sits on the antenna, silhouetted against the dawn. He looks majestic. He knows it.")
        a_list.append("Mr. Pecks is having a morning briefing with two other crows on the fence. They disperse when you wake up. Suspicious.")
        a_list.append("Mr. Pecks preens his feathers methodically. Left wing. Right wing. Tail. A gentleman prepares for the day.")
        a_list.append("Mr. Pecks has been awake for hours. Crows don't sleep much. He's been watching over you the whole time.")
        random.shuffle(a_list)
        return a_list

    def get_pecks_morning_update(self):
        if len(self.__pecks_morning_list) == 0:
            self.__pecks_morning_list = self.make_pecks_morning_list()
        return self.__pecks_morning_list.pop()

    # ==========================================
    # PATCHES (OPOSSUM) DAILY DIALOGUE
    # ==========================================

    def make_patches_happy_list(self):
        a_list = []
        a_list.append("Patches waddles over to you with her mouth slightly open. That's an opossum smile. You've learned to love it.")
        a_list.append("Patches shows you her babies again. They're riding on her back, little pink noses poking out of her fur. A family.")
        a_list.append("Patches doesn't play dead when you reach for her. That's trust. That's everything.")
        a_list.append("Patches purrs in your lap. Yes, opossums purr. It sounds like a tiny outboard motor. It's perfect.")
        a_list.append("Patches hangs from the rearview mirror by her tail, swinging gently. Her version of a hammock.")
        a_list.append("Patches eats a piece of garbage you gave her like it's filet mignon. Closes her eyes. Savors it. Chef's kiss.")
        a_list.append("Patches grooms your fingers one by one. Gentle nibbles. She's cleaning you. You're filthy, apparently.")
        a_list.append("Patches does that thing where she opens her mouth and shows all 50 teeth. Terrifying to strangers. A smile to you.")
        a_list.append("Patches falls asleep on your chest. Her heartbeat is surprisingly fast. Like a little drum. Alive. Here. Yours.")
        a_list.append("Patches discovers a rotten banana and reacts like she's found the Holy Grail. Ecstatic. Euphoric. It's a banana.")
        a_list.append("Patches lets her babies climb on you. Tiny opossum feet on your arms, your shoulders, your head. You are a playground.")
        a_list.append("Patches sits in your palm and clicks her tongue happily. Opossum for 'I approve of you.'")
        random.shuffle(a_list)
        return a_list

    def get_patches_happy_update(self):
        if len(self.__patches_happy_list) == 0:
            self.__patches_happy_list = self.make_patches_happy_list()
        return self.__patches_happy_list.pop()

    def make_patches_unhappy_list(self):
        a_list = []
        a_list.append("Patches plays dead again. She hasn't done that around you in weeks. Something's wrong.")
        a_list.append("Patches drools more than usual. Stress drooling. Opossum anxiety is real.")
        a_list.append("Patches retreats under the seat, curled into a tight ball. Won't uncurl. Won't eat.")
        a_list.append("Patches bares all 50 teeth at you. This isn't a smile. You know the difference now.")
        a_list.append("Patches hisses when you open the car door. She's scared. Of you? Of the world? Both?")
        a_list.append("Patches hasn't come out since last night. Nocturnal by nature, but this feels different.")
        a_list.append("Patches's babies are clinging to her tighter than usual. They sense her distress.")
        a_list.append("Patches eats less than half her food. She pushes the rest away with her nose.")
        a_list.append("Patches sits in the dark corner, eyes wide and glassy. Playing dead emotionally.")
        a_list.append("Patches flinches at every sound. Hyper-alert. Her prey instincts are screaming.")
        random.shuffle(a_list)
        return a_list

    def get_patches_unhappy_update(self):
        if len(self.__patches_unhappy_list) == 0:
            self.__patches_unhappy_list = self.make_patches_unhappy_list()
        return self.__patches_unhappy_list.pop()

    def make_patches_weather_list(self):
        a_list = []
        a_list.append("Patches curls into a ball so tight she's basically a sphere. Rain is not her thing.")
        a_list.append("Patches sleeps through the entire storm. Nocturnal creatures give zero cares about daytime weather.")
        a_list.append("Patches's babies huddle closer to her during the thunder. A family staying warm.")
        a_list.append("Patches watches the rain from inside, nose twitching. She's not going out in THAT.")
        a_list.append("Patches finds the driest, warmest spot in the entire car and claims it. Under your blanket. Against your side.")
        random.shuffle(a_list)
        return a_list

    def get_patches_weather_update(self):
        if len(self.__patches_weather_list) == 0:
            self.__patches_weather_list = self.make_patches_weather_list()
        return self.__patches_weather_list.pop()

    def make_patches_morning_list(self):
        a_list = []
        a_list.append("Patches is just going to sleep as you're waking up. Ships passing in the night. Literally.")
        a_list.append("Patches yawns, showing every single one of those 50 teeth. It never stops being terrifying.")
        a_list.append("Patches stayed up all night watching over you. She's exhausted. But you're safe.")
        a_list.append("Patches's babies are already asleep, piled on top of each other like a opossum pancake stack.")
        a_list.append("Patches reluctantly opens one eye. The sun is her enemy. Mornings are an insult.")
        a_list.append("Patches has been busy all night. There are tiny footprints on the dashboard. Everywhere.")
        a_list.append("Patches found a stash of bugs during the night and left them for you. Breakfast. Thanks, Patches.")
        a_list.append("Patches drags herself to her sleeping spot with the gravity of someone who's worked a double shift. Good night, girl.")
        random.shuffle(a_list)
        return a_list

    def get_patches_morning_update(self):
        if len(self.__patches_morning_list) == 0:
            self.__patches_morning_list = self.make_patches_morning_list()
        return self.__patches_morning_list.pop()

    # ==========================================
    # RUSTY (RACCOON) DAILY DIALOGUE
    # ==========================================

    def make_rusty_happy_list(self):
        a_list = []
        a_list.append("Rusty washes a grape in a puddle before eating it. Hygienic king. He's better than you.")
        a_list.append("Rusty figured out how to unzip your bag. Again. He's rifling through it with those dexterous little paws.")
        a_list.append("Rusty stacks coins into a tower, admires it, then knocks it over. Raccoon economics.")
        a_list.append("Rusty brings you someone's wallet. 'Where did you get this, Rusty?' He says nothing. Because he's a raccoon.")
        a_list.append("Rusty opens a jar of peanut butter you SWORE was sealed. Twist-off, apparently. For raccoon hands.")
        a_list.append("Rusty stands on his hind legs and extends his tiny hands toward you. Arms up. Hug request. You oblige.")
        a_list.append("Rusty organized all the loose change in the cup holder by denomination. You owe him an accounting degree.")
        a_list.append("Rusty does the raccoon thing where he puts his hands on his face and looks at you through his fingers. Peek-a-boo.")
        a_list.append("Rusty steals a donut from a stranger's hand through the window. Doesn't even flinch. Professional.")
        a_list.append("Rusty has built a nest out of stolen napkins, receipts, and one very nice silk scarf. Where did the scarf come from, Rusty?")
        a_list.append("Rusty tries to wash a sugar cube and looks confused when it dissolves. The betrayal on his face is heartbreaking.")
        a_list.append("Rusty sits in your lap and holds your thumb with both paws. His hands are weirdly human. This is weirdly nice.")
        random.shuffle(a_list)
        return a_list

    def get_rusty_happy_update(self):
        if len(self.__rusty_happy_list) == 0:
            self.__rusty_happy_list = self.make_rusty_happy_list()
        return self.__rusty_happy_list.pop()

    def make_rusty_unhappy_list(self):
        a_list = []
        a_list.append("Rusty stops stealing things. That's how you know it's bad. The crimes are on hold.")
        a_list.append("Rusty chatters angrily and won't let you near his stash. He's hoarding. Stress behavior.")
        a_list.append("Rusty washes his paws compulsively. Over and over. It's not about being clean anymore.")
        a_list.append("Rusty knocks everything off every surface. This isn't playful. This is rage.")
        a_list.append("Rusty bites your finger. Not hard. But enough. A warning.")
        a_list.append("Rusty hides behind the spare tire with all his stolen goods. Fortress of solitude.")
        a_list.append("Rusty returns everything he stole today and lines it up neatly. It feels like a goodbye.")
        a_list.append("Rusty makes a sound you've never heard before. A low whine. Raccoon sadness sounds awful.")
        a_list.append("Rusty doesn't wash his food. He just eats it dirty. Something is deeply wrong.")
        a_list.append("Rusty sits in the dark, eyes reflecting like two green marbles. He doesn't blink.")
        random.shuffle(a_list)
        return a_list

    def get_rusty_unhappy_update(self):
        if len(self.__rusty_unhappy_list) == 0:
            self.__rusty_unhappy_list = self.make_rusty_unhappy_list()
        return self.__rusty_unhappy_list.pop()

    def make_rusty_weather_list(self):
        a_list = []
        a_list.append("Rusty doesn't mind the rain. He stands outside washing things in the puddles. Living his best raccoon life.")
        a_list.append("Rusty steals a passing stranger's umbrella. Drags it into the car. He's a problem solver.")
        a_list.append("Rusty chatters at the thunder like he's arguing with it. Spoiler: he's losing.")
        a_list.append("Rusty wraps himself in your jacket during the storm. The bandit mask pokes out from the collar. Adorable criminal.")
        a_list.append("Rusty discovered that rain puddles are perfect for washing things. He's been outside for an hour. Come back, Rusty.")
        random.shuffle(a_list)
        return a_list

    def get_rusty_weather_update(self):
        if len(self.__rusty_weather_list) == 0:
            self.__rusty_weather_list = self.make_rusty_weather_list()
        return self.__rusty_weather_list.pop()

    def make_rusty_morning_list(self):
        a_list = []
        a_list.append("Rusty is sitting on your chest when you wake up, holding a shiny coin an inch from your face. Morning offering.")
        a_list.append("Rusty was busy all night. Your glove box is open. Your wallet is empty. There's a neat pile of coins on the dashboard.")
        a_list.append("Rusty opens one eye, realizes it's morning, and goes back to sleep immediately. Raccoons are nocturnal. Respect it.")
        a_list.append("Rusty has organized the entire car overnight. Everything is in piles. Raccoon piles. You don't understand the system.")
        a_list.append("Rusty presents you with a breakfast he assembled: two crackers, a gummy bear, and a button. Gourmet.")
        a_list.append("Rusty yawns, and his little bandit face scrunches up. Even his yawns look sneaky.")
        a_list.append("Rusty already stole three things before you opened your eyes. His morning commute.")
        a_list.append("Rusty is washing a blueberry in the cupholder water. Breakfast prep. He takes nutrition seriously.")
        random.shuffle(a_list)
        return a_list

    def get_rusty_morning_update(self):
        if len(self.__rusty_morning_list) == 0:
            self.__rusty_morning_list = self.make_rusty_morning_list()
        return self.__rusty_morning_list.pop()

    # ==========================================
    # SLICK (RAT) DAILY DIALOGUE
    # ==========================================

    def make_slick_happy_list(self):
        a_list = []
        a_list.append("Slick does a tiny popcorning hop across the dashboard. Hop. Hop. Hop. Pure rat joy.")
        a_list.append("Slick bruxes so loud you can hear his teeth grinding from across the car. Happy rat purring.")
        a_list.append("Slick runs up your arm, across your shoulders, down the other arm, and back again. Rat highway.")
        a_list.append("Slick brings you a crumb. It's tiny. It's all he has. He's sharing it with you.")
        a_list.append("Slick crawls into your sleeve and falls asleep against your forearm. Warm. Safe. Home.")
        a_list.append("Slick boggling — his eyes are bulging in and out of his skull. It looks horrifying. It means he's ecstatic.")
        a_list.append("Slick grooms your thumbnail with his tiny pink tongue. You are clean now. You're welcome.")
        a_list.append("Slick plays with a ball of paper, tossing it in the air and catching it. Athlete of the year.")
        a_list.append("Slick makes a nest out of shredded receipts and curls up in it. Interior designer. Minimalist.")
        a_list.append("Slick sits on your shoulder and squeaks softly in your ear. He's telling you a secret. You'll never know what it is.")
        a_list.append("Slick hangs upside down from your finger by his tail, looking at the world from a new angle.")
        a_list.append("Slick learned to come when you whistle. He pokes his head out, whiskers twitching, then sprints to you.")
        random.shuffle(a_list)
        return a_list

    def get_slick_happy_update(self):
        if len(self.__slick_happy_list) == 0:
            self.__slick_happy_list = self.make_slick_happy_list()
        return self.__slick_happy_list.pop()

    def make_slick_unhappy_list(self):
        a_list = []
        a_list.append("Slick hides in the glove box and won't come out. You can hear him breathing fast.")
        a_list.append("Slick's ears are flat against his head. He's scared. Or sad. Probably both.")
        a_list.append("Slick won't eat his food. Pushes the crumbs away. Turns his back.")
        a_list.append("Slick bites you. Not hard. But he's never done that before. Something's wrong.")
        a_list.append("Slick stays in the darkest corner of the car. Won't come into the light.")
        a_list.append("Slick puffs up his fur. Making himself look bigger. But really he's just scared.")
        a_list.append("Slick chatters his teeth — not the happy kind. The anxious kind. Rapid. Clicking.")
        a_list.append("Slick grooms himself excessively. A bald spot is forming. Stress.")
        a_list.append("Slick freezes when you reach for him. Completely still. Survival instinct. He doesn't trust right now.")
        a_list.append("Slick squeaks in his sleep. Rat nightmares. You wish you could help.")
        random.shuffle(a_list)
        return a_list

    def get_slick_unhappy_update(self):
        if len(self.__slick_unhappy_list) == 0:
            self.__slick_unhappy_list = self.make_slick_unhappy_list()
        return self.__slick_unhappy_list.pop()

    def make_slick_weather_list(self):
        a_list = []
        a_list.append("Slick doesn't mind rain. He's a rat. Rats are built for weather. He sleeps through it.")
        a_list.append("Slick burrows deeper into his nest during the thunder. Not scared. Just... cautious.")
        a_list.append("Slick presses against your neck during the storm. His little heart is hammering.")
        a_list.append("Slick watches the rain from the window, nose twitching. Calculating the best routes through it.")
        a_list.append("Slick squeaks every time thunder cracks. A protest. He's filing a formal complaint with the sky.")
        random.shuffle(a_list)
        return a_list

    def get_slick_weather_update(self):
        if len(self.__slick_weather_list) == 0:
            self.__slick_weather_list = self.make_slick_weather_list()
        return self.__slick_weather_list.pop()

    def make_slick_morning_list(self):
        a_list = []
        a_list.append("Slick is nocturnal, but he adjusted his schedule for you. He's sitting on the dashboard, yawning. Morning, buddy.")
        a_list.append("Slick pokes his head out of your pocket. Pink nose twitching. Eyes barely open. Not a morning rat.")
        a_list.append("Slick already mapped three new escape routes while you were sleeping. Morning briefing accomplished.")
        a_list.append("Slick brings you a seed he's been saving. It's his breakfast. He wants you to have it.")
        a_list.append("Slick runs a perimeter check around the car. Checks every crack. Every hole. All clear, boss.")
        a_list.append("Slick stretches his whole body out flat, then curls back up. Rat version of hitting snooze.")
        a_list.append("Slick sits on the rearview mirror, cleaning his whiskers. Looking sharp for the day ahead.")
        a_list.append("Slick squeaks once when you wake up. Just once. Good morning. Efficient communication.")
        random.shuffle(a_list)
        return a_list

    def get_slick_morning_update(self):
        if len(self.__slick_morning_list) == 0:
            self.__slick_morning_list = self.make_slick_morning_list()
        return self.__slick_morning_list.pop()

    # ==========================================
    # HOPPER (RABBIT) DAILY DIALOGUE
    # ==========================================

    def make_hopper_happy_list(self):
        a_list = []
        a_list.append("Hopper does a binky — a full-body twist in mid-air. Rabbit for 'LIFE IS INCREDIBLE.'")
        a_list.append("Hopper flops on her side so dramatically you think she's dead. She's not. She's just... extremely content.")
        a_list.append("Hopper zooms around the car at top speed, bouncing off the seats. Bunny NASCAR. She's winning.")
        a_list.append("Hopper licks your hand over and over. Tiny sandpaper tongue. She's grooming you. You're her baby now.")
        a_list.append("Hopper lets you rub her belly. Rabbits NEVER do this. You are chosen. You are blessed.")
        a_list.append("Hopper nudges your hand with her nose until you pet her. Then she purrs. Yes, rabbits purr. Tooth purring.")
        a_list.append("Hopper leaves little poops everywhere. Territorial marking. Every surface is hers. Including you.")
        a_list.append("Hopper chinning your shoes, your bag, your jacket. Rubbing her scent on everything. You belong to Hopper.")
        a_list.append("Hopper discovered a patch of clover outside and lost her entire mind. CLOVER! THE BEST DAY!")
        a_list.append("Hopper sits in your lap, ears up, nose going a million miles an hour. Processing. Computing. Being rabbit.")
        a_list.append("Hopper stacks her food pellets into a little pyramid. Then eats the pyramid. Architecture and lunch.")
        a_list.append("Hopper binkies so hard she hits the ceiling. Not hurt. Just embarrassed. She looks at you. Say nothing.")
        random.shuffle(a_list)
        return a_list

    def get_hopper_happy_update(self):
        if len(self.__hopper_happy_list) == 0:
            self.__hopper_happy_list = self.make_hopper_happy_list()
        return self.__hopper_happy_list.pop()

    def make_hopper_unhappy_list(self):
        a_list = []
        a_list.append("Hopper thumps her back foot hard. Once. Twice. Danger signal. She's warning the warren. There is no warren. Just you.")
        a_list.append("Hopper won't eat. Not even the good pellets. Not even treats. She sits hunched, ears flat.")
        a_list.append("Hopper grinds her teeth — the bad kind. The stressed kind. It sounds like gravel crunching.")
        a_list.append("Hopper lunges when you reach into her space. Not trying to bite. Just scared. Back off.")
        a_list.append("Hopper hides behind the spare tire. You can only see her nose twitching in the dark.")
        a_list.append("Hopper digs at the car floor compulsively. Trying to burrow. Trying to escape. Trying to be anywhere but here.")
        a_list.append("Hopper sits perfectly still, eyes wide, ears back. Frozen. The prey response. The world is too dangerous.")
        a_list.append("Hopper stops binkying. No more flops. No more zooms. Just a still, small rabbit.")
        a_list.append("Hopper pushes her food bowl away. Flips it over. Statement made.")
        a_list.append("Hopper won't let you touch her. She flinches. You pull your hand back slowly. It hurts.")
        random.shuffle(a_list)
        return a_list

    def get_hopper_unhappy_update(self):
        if len(self.__hopper_unhappy_list) == 0:
            self.__hopper_unhappy_list = self.make_hopper_unhappy_list()
        return self.__hopper_unhappy_list.pop()

    def make_hopper_weather_list(self):
        a_list = []
        a_list.append("Hopper thumps at every thunderclap. Warning you. DANGER! IT'S DANGER! She's not wrong, technically.")
        a_list.append("Hopper burrows into your blanket so deep you can't find her. She'll come out when the sun does.")
        a_list.append("Hopper presses against your side, ears flat. Rabbits are prey animals. Storms feel like predators.")
        a_list.append("Hopper freezes completely during lightning. Statue mode. Even her nose stops twitching. That's serious.")
        a_list.append("Hopper digs at the car floor frantically. She wants underground. She wants a burrow. You are the burrow.")
        random.shuffle(a_list)
        return a_list

    def get_hopper_weather_update(self):
        if len(self.__hopper_weather_list) == 0:
            self.__hopper_weather_list = self.make_hopper_weather_list()
        return self.__hopper_weather_list.pop()

    def make_hopper_morning_list(self):
        a_list = []
        a_list.append("Hopper is already awake, nose twitching at 200 BPM. Rabbits are crepuscular. Dawn is her time.")
        a_list.append("Hopper binkies as the first light hits the car. Morning celebration. A new day! More clover!")
        a_list.append("Hopper nudges your face with her cold, wet nose until you wake up. Boop. Boop. BOOP.")
        a_list.append("Hopper rearranged her bedding during the night into the perfect nest. Martha Stewart of rabbits.")
        a_list.append("Hopper sits in the driver's seat watching the sunrise. Philosophical rabbit. Deep in thought. About carrots, probably.")
        a_list.append("Hopper leaves a trail of little poops from her bed to your face. Morning breadcrumbs. Thanks, Hopper.")
        a_list.append("Hopper tooth-purrs as you wake up. Rabbit for 'I'm happy you're still here.'")
        a_list.append("Hopper does three binkies before you even sit up. Morning energy levels: maximum.")
        random.shuffle(a_list)
        return a_list

    def get_hopper_morning_update(self):
        if len(self.__hopper_morning_list) == 0:
            self.__hopper_morning_list = self.make_hopper_morning_list()
        return self.__hopper_morning_list.pop()

    # ==========================================
    # SQUIRRELLY (COMPANION SYSTEM) DAILY DIALOGUE
    # ==========================================

    def make_squirrelly_comp_happy_list(self):
        a_list = []
        a_list.append("Squirrelly is vibrating on the dashboard. Not sitting. Vibrating. The acorn energy is overwhelming.")
        a_list.append("Squirrelly races around the car at impossible speed, leaping from seat to headrest to your shoulder to the mirror.")
        a_list.append("Squirrelly buried sixteen acorns in your car this morning. SIXTEEN. You found two of them.")
        a_list.append("Squirrelly presents you with the absolute perfect acorn. She inspected forty. This one made the cut.")
        a_list.append("Squirrelly does the happy chatter — that rapid-fire clicking sound that means all is right in squirrel world.")
        a_list.append("Squirrelly rides on your head while you walk. She likes the view from up there. You are a tree now.")
        a_list.append("Squirrelly finds a sunbeam on the dashboard and melts into a flat pancake of warm squirrel happiness.")
        a_list.append("Squirrelly climbs the outside of the car and sits on the roof. Queen of the world. King of the junkyard.")
        a_list.append("Squirrelly plays with a bottle cap, spinning it with her paws. Simple pleasures. Best pleasures.")
        a_list.append("Squirrelly stuffs her cheeks so full of seeds she can barely close her mouth. Storage capacity: maximum.")
        a_list.append("Squirrelly grooms your eyebrows. They needed work, apparently. Squirrel salon, open for business.")
        a_list.append("Squirrelly chirps at birds outside, and they chirp back. She's networking. Building connections.")
        random.shuffle(a_list)
        return a_list

    def get_squirrelly_comp_happy_update(self):
        if len(self.__squirrelly_comp_happy_list) == 0:
            self.__squirrelly_comp_happy_list = self.make_squirrelly_comp_happy_list()
        return self.__squirrelly_comp_happy_list.pop()

    def make_squirrelly_comp_unhappy_list(self):
        a_list = []
        a_list.append("Squirrelly sits alone in the cup holder, clutching one acorn. She won't eat it. Won't share it. Just holds it.")
        a_list.append("Squirrelly won't chatter. Won't chirp. Just sits there, tail limp, eyes empty.")
        a_list.append("Squirrelly digs frantically at the floor. Trying to bury something. There's nothing to bury. The instinct is all she has left.")
        a_list.append("Squirrelly flinches when you reach for her. Not because you hurt her. Because the world did.")
        a_list.append("Squirrelly stares at the trees outside for hours. You wonder if she'd be happier out there. The thought is a knife.")
        a_list.append("Squirrelly bites the inside of the glove box. Stress. Gnawing. Something's eating her and she's eating back.")
        a_list.append("Squirrelly pushed all her acorns into a pile and hasn't touched them. The stash means nothing right now.")
        a_list.append("Squirrelly's tail is puffed up. Not cute puffed. Scared puffed. Danger-alert puffed.")
        a_list.append("Squirrelly hides in your shoe and won't come out. The shoe is safety. You are not. That hurts.")
        a_list.append("Squirrelly makes a soft, sad squeak you've never heard before. It sounds like crying. Squirrels don't cry. Do they?")
        random.shuffle(a_list)
        return a_list

    def get_squirrelly_comp_unhappy_update(self):
        if len(self.__squirrelly_comp_unhappy_list) == 0:
            self.__squirrelly_comp_unhappy_list = self.make_squirrelly_comp_unhappy_list()
        return self.__squirrelly_comp_unhappy_list.pop()

    def make_squirrelly_comp_weather_list(self):
        a_list = []
        a_list.append("Squirrelly does NOT like storms. She's in your shirt. Against your chest. Shaking.")
        a_list.append("Squirrelly chatters angrily at the thunder. HOW DARE YOU. HOW DARE YOU RAIN ON MY ACORNS.")
        a_list.append("Squirrelly hides in the glove box and builds a barricade of acorns. Fort Squirrelly. No entry.")
        a_list.append("Squirrelly presses her whole body against the heater vent. Warmth is survival. Warmth is life.")
        a_list.append("Squirrelly buries herself in your blanket with just her nose poking out. Only her nose braves the storm.")
        random.shuffle(a_list)
        return a_list

    def get_squirrelly_comp_weather_update(self):
        if len(self.__squirrelly_comp_weather_list) == 0:
            self.__squirrelly_comp_weather_list = self.make_squirrelly_comp_weather_list()
        return self.__squirrelly_comp_weather_list.pop()

    def make_squirrelly_comp_morning_list(self):
        a_list = []
        a_list.append("Squirrelly drops an acorn on your face to wake you up. BONK. Good morning. Get up. It's acorn time.")
        a_list.append("Squirrelly is already racing around the car at 5 AM. Squirrels don't do slow mornings.")
        a_list.append("Squirrelly presents you with a perfectly arranged line of acorns. Your morning report. All acorns accounted for.")
        a_list.append("Squirrelly sits on the steering wheel, chattering at the sunrise. Morning prayers. To the acorn gods.")
        a_list.append("Squirrelly is reorganizing her stash. The acorn inventory must be updated daily. She takes this seriously.")
        a_list.append("Squirrelly chirps exactly twice. Her way of saying 'we made it through another night.' You chirp back.")
        a_list.append("Squirrelly is hanging upside down from the rearview mirror, eating a nut. Just absolutely living her best life.")
        a_list.append("Squirrelly scurries up your arm the second you move. She was waiting. She's always waiting for you.")
        random.shuffle(a_list)
        return a_list

    def get_squirrelly_comp_morning_update(self):
        if len(self.__squirrelly_comp_morning_list) == 0:
            self.__squirrelly_comp_morning_list = self.make_squirrelly_comp_morning_list()
        return self.__squirrelly_comp_morning_list.pop()


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
        if not a_list:
            a_list.append("Your body finally gives out. You collapse in the front seat of your car, staring at the ceiling, and that's that.")
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
    # SLEEP FLAVOR TEXT SYSTEM
    # ==========================================

    def get_sleep_text(self, quality):
        """Returns a random sleep flavor text based on sleep quality tier."""
        texts = {
            "refreshed": [
                "You slept like a baby. A big, grown baby in a car, but a baby nonetheless.",
                "That might have been the best sleep of your life. You feel incredible.",
                "You wake up feeling like a million bucks. Well, maybe a few thousand bucks. But still great.",
                "Your eyes pop open and you're ready to go. Did someone slip you a good dream? Because that was chef's kiss.",
                "You stretch out and feel every vertebra in your spine crack in the most satisfying way. Today is going to be good.",
                "You actually feel rested. Like, genuinely rested. This is what sleeping is supposed to feel like?",
                "The sun hits your face through the windshield and you don't even mind. That's how good you feel.",
                "You wake up smiling. When's the last time that happened? You can't remember, but it happened today.",
                "That was some quality sleep. Five stars. Would sleep again.",
                "You had a dream about winning at Blackjack. Then you woke up. But you still feel great.",
                "Your body feels like it got a factory reset overnight. Joints? Smooth. Back? Fine. Mood? Immaculate.",
                "You wake up and actually want to get out of the car. This is a historic moment.",
                "Best night's sleep in a long time. You even folded your blanket. Who are you?",
                "You slept so hard you forgot where you were for a second. That's the good kind of confusion.",
                "You yawn, stretch, and feel genuinely alive. Not just surviving. Actually alive.",
                "A bird is singing outside your car. You don't want to punch it. Progress.",
                "You wake up with energy. Like, real energy. Not 'I didn't die in my sleep' energy.",
                "Your neck doesn't hurt. Your back doesn't hurt. Nothing hurts. Is this a trap?",
                "You slept so well that you're suspicious. Something this good can't be free.",
                "You wake up refreshed and optimistic. The optimism will probably wear off by noon, but for now, you bask in it.",
            ],
            "well_rested": [
                "Not bad. You slept pretty well, all things considered.",
                "You wake up feeling fine. Not amazing, not terrible. Just... fine. And fine is fine.",
                "A solid night's rest. Your body thanks you by not hurting for once.",
                "You slept well enough to face whatever today throws at you. Probably.",
                "You open your eyes and think, 'Alright, I can do this.' That's more enthusiasm than usual.",
                "Decent sleep. You had one weird dream about a talking fish, but other than that, pretty standard.",
                "You wake up without any new aches or pains. You'll take that as a win.",
                "Your sleep was good. Not award-winning, but definitely a solid B+.",
                "The morning light doesn't feel aggressive today. That's always a good sign.",
                "You actually feel somewhat ready for the day. Miracles do happen.",
                "You slept through the whole night. No weird noises, no nightmares. Just sleep. Wonderful, boring sleep.",
                "You stretch and only one thing pops. That's a good ratio.",
                "Woke up on the right side of the car seat. It's going to be a decent day.",
                "Your dreams were forgettable, which is the best kind of dream when you live in a car.",
                "You feel alright. 'Alright' is severely underrated.",
                "Good enough sleep to not hate everything. That's the bar, and you cleared it.",
                "You slept like someone who's getting used to sleeping in a car. Which you are.",
                "Morning comes and you greet it without groaning. Small victories.",
                "You wake up feeling functional. Not inspired. Functional. That's plenty.",
                "Solid rest. You even had a pleasant dream, though you can't quite remember what it was about.",
            ],
            "decent": [
                "You wake up. That's about all there is to report.",
                "Sleep happened. You're alive. Moving on.",
                "Your sleep was exactly average. Not worth mentioning, really. And yet, here we are.",
                "You slept okay. Not great. Just okay. The most 'okay' sleep possible.",
                "You wake up feeling the same as you did yesterday. Consistency, baby.",
                "Another night in the car, another morning of existing. The cycle continues.",
                "You didn't sleep great, but you didn't sleep terribly. The Switzerland of sleep.",
                "Your body feels like it slept for exactly the amount it needed. Not a minute more.",
                "You wake up and stare at the ceiling of your car for a moment before deciding to exist.",
                "The sleep was there. It did its job. Barely.",
                "You had a dream but forgot it immediately. Your subconscious is on a need-to-know basis.",
                "You slept. That's the whole story. No drama. No excitement. Just sleep.",
                "Your neck has a slight crick in it, but nothing a few shoulder rolls can't sort out.",
                "An unremarkable night of sleep. You're becoming an expert at those.",
                "You wake up with a neutral expression and a neutral mood. Neutral is your whole thing right now.",
                "Sleep: completed. Enthusiasm: pending.",
                "You open your eyes and feel nothing in particular. Peak Wednesday energy.",
                "Your sleep was a solid C. Passing grade. Nothing to write home about.",
                "You wake up and your first thought is 'meh.' Which is, honestly, better than most days.",
                "The night passes without incident. You're alive and moderately functional. Good enough.",
            ],
            "restless": [
                "You tossed and turned all night. The car seat has a permanent imprint of your frustration.",
                "Sleep came in pieces. You'd doze off, wake up, doze off, wake up. Rinse and repeat.",
                "You woke up three times during the night. Once because of a noise. Twice because your brain hates you.",
                "Your sleep was choppy at best. You feel like you got about half the rest you needed.",
                "You wake up already tired. That shouldn't be possible, and yet.",
                "The night felt longer than it should have. Every hour crawled by like it had somewhere else to be.",
                "You didn't sleep so much as you laid there with your eyes closed, pretending to sleep.",
                "Your dreams kept waking you up. Rude of them, honestly.",
                "You wake up with the distinct feeling that you just fought something in your sleep.",
                "Sleep was... present? Technically? But not quality sleep. Dollar store sleep.",
                "You feel groggy. Not dangerously groggy. Just enough to make everything slightly annoying.",
                "Your pillow — well, your rolled-up jacket — did nothing for you last night.",
                "You keep yawning as you get up. Your body is making a statement.",
                "Last night's sleep was like a buffet where everything was slightly stale. Edible, but disappointing.",
                "You wake up and immediately want to go back to sleep. But the sun has other plans.",
                "Your eyes feel heavy. Your limbs feel heavier. Your motivation feels heaviest.",
                "You spent half the night staring at the roof of your car. You've memorized every scratch.",
                "Restless night. You're running on maybe 60% battery. That'll have to do.",
                "You feel like you slept, but your body feels like you didn't. Your body might be lying.",
                "The morning hits different when you're already exhausted. It hits worse.",
            ],
            "poor": [
                "You barely slept. Your eyes feel like they've been replaced with sandpaper.",
                "What even was last night? You're not sure you actually slept at all.",
                "You wake up more tired than when you went to sleep. That's a talent.",
                "Your body aches in places you didn't know could ache. The car seat is winning the war.",
                "Sleep? What sleep? You laid there for eight hours and got maybe two hours of actual rest.",
                "The bags under your eyes have bags. You look like a raccoon, and not the cute kind.",
                "You wake up with a headache that seems personally offended by the morning light.",
                "Last night was rough. Real rough. You feel like you got run over by a very slow, very persistent truck.",
                "You're exhausted. The kind of exhausted where blinking feels like a workout.",
                "Your brain is running on fumes. Coherent thought is a luxury you can't afford today.",
                "Every muscle in your body is filing a formal complaint about last night.",
                "You wake up and seriously consider whether 'just sleeping all day' is a viable life strategy.",
                "The sun is too bright. The birds are too loud. Everything is too much. You're too tired.",
                "You got up on the wrong side of the car. Both sides are wrong when you sleep this badly.",
                "Your spine is staging a revolution. Your neck is the ringleader.",
                "You feel like a phone at 8% battery. Functional, but don't push it.",
                "Sleep deprivation is a hell of a drug. You're currently overdosing on it.",
                "You stagger out of the car like a zombie. A zombie with joint pain. A geriatric zombie.",
                "Last night was a war between you and sleep. Sleep won. You lost. Everyone lost.",
                "You're so tired that you put your shirt on backwards and didn't notice until now.",
            ],
            "terrible": [
                "You didn't sleep. You just... existed horizontally for a while.",
                "Your body has entered survival mode. Sleep is a distant memory.",
                "You wake up — wait, were you even asleep? The line between conscious and unconscious has blurred.",
                "The sunrise is an insult. It's mocking you. 'Oh, you're still awake? Cool, here's MORE light.'",
                "You've been awake so long that your thoughts are starting to echo.",
                "Your eyes are open but nobody's home. The lights are on but the electricity bill hasn't been paid.",
                "You feel like a wrung-out dishrag. The world's most exhausted, car-dwelling dishrag.",
                "Getting up takes three attempts. The first two times, gravity wins.",
                "You're running on spite and whatever's left of yesterday's willpower. It's not much.",
                "Everything hurts. Not in a dramatic way. In a 'my entire body is begging for sleep' way.",
                "Your brain is buffering. Please wait. Please wait. Please wait.",
                "You look at yourself in the rearview mirror and genuinely don't recognize the person staring back.",
                "Sleep didn't happen. What happened was a prolonged argument with your own consciousness.",
                "You're so tired that the idea of standing up sounds like an extreme sport.",
                "Your hands are shaking slightly. Not from fear. From pure, unadulterated exhaustion.",
                "The car seat has betrayed you. The blanket has betrayed you. Your own eyelids have betrayed you.",
                "You're functioning on zero sleep and maximum stubbornness. Stubbornness is all you have left.",
                "You stare at the steering wheel for a full minute before remembering what it does.",
                "Is this what being a ghost feels like? Just floating through existence? Because that's where you're at.",
                "You're so exhausted that even your exhaustion is tired.",
            ],
            "wrecked": [
                "You're not even sure you're awake right now. This could be a dream. A terrible, terrible dream.",
                "Your body has gone on strike. Your brain is the lone scab crossing the picket line.",
                "You haven't slept in what feels like years. Time has lost all meaning.",
                "You see the sun rise and feel nothing. You are beyond feelings. You are a husk.",
                "Your thoughts come in fragments. Disconnected. Random. Was that a squirrel? Focus. Focus.",
                "You try to stand and your knees buckle. Not because they're weak. Because they've forgotten how.",
                "The world looks fuzzy. Not in a cute way. In a 'your brain is shutting down' way.",
                "You're running on negative sleep. You owe the universe hours of rest and it's collecting interest.",
                "You hear a ringing in your ears. It's either exhaustion or you're dying. Could be both.",
                "Your vision blurs and for a second, you think you see two suns. There's only one. Probably.",
                "You haven't blinked in six minutes. You know this because you've been counting. Why are you counting?",
                "Is the car moving? No. Is the ground moving? Also no. Then why is everything swaying?",
                "You open the car door and forget what you were going to do. This happens four more times.",
                "Sleep deprivation fact: after enough hours awake, your brain starts making stuff up. You're there.",
                "You try to remember your name and it takes way longer than it should.",
                "You're so tired that you hallucinated a bed. It was the car seat. It's always the car seat.",
                "Your body is a machine that hasn't been serviced in years. Everything squeaks. Everything groans.",
                "You contemplate whether it's possible to die of tiredness. The answer is yes, but you're too tired to die.",
                "The sunrise looks like it's pulsing. It isn't. Your eyes are just giving up.",
                "If exhaustion was currency, you'd be a millionaire. Unfortunately, it's not. You're still broke and tired.",
            ],
        }
        return random.choice(texts.get(quality, texts["decent"]))

    def get_fatigue_blocked_text(self):
        """Returns flavor text when fatigue prevents the player from experiencing a day event."""
        texts = [
            "You're too exhausted to do much of anything this morning. You just sit in your car and zone out.",
            "Your body refuses to cooperate. Whatever was about to happen, you're too tired for it.",
            "An opportunity passes you by while you're half-asleep in your car. Oh well.",
            "You see something interesting in the distance, but your legs refuse to carry you there.",
            "You try to get up and do something, but exhaustion pins you to the seat like a paperweight.",
            "Something happens nearby. You're too tired to even turn your head to look.",
            "The universe tries to throw you a bone. You're too exhausted to catch it.",
            "You spend the morning in a fog. Things happen around you. You are not part of them.",
            "Your eyelids are so heavy that the entire morning passes in a blur of half-consciousness.",
            "You had plans. Big plans. But exhaustion had bigger plans. Exhaustion won.",
            "A stranger waves at you from the road. By the time you process what's happening, they're gone.",
            "You miss something. You're not sure what, but you feel like you missed something.",
            "You wake up, blink, and suddenly it's afternoon. Did you sleep through the whole morning?",
            "Your brain is on power-saving mode. Only essential functions are available. Nothing is essential.",
            "You try to participate in the day, but your body vetoes the motion. Motion denied.",
            "The morning plays out like a movie you're watching through frosted glass. You're there, but you're not.",
            "You open the car door, stare at the outside world for thirty seconds, and close it again. Not today.",
            "Your body has entered 'do not disturb' mode. Nobody consulted you about this.",
            "The day is happening whether you're ready or not. Spoiler: you're not.",
            "You attempt consciousness. Consciousness politely declines.",
        ]
        return random.choice(texts)
    
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