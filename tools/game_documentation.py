"""
BLACKJACK GAME DOCUMENTATION GENERATOR
========================================
This module generates comprehensive documentation of the entire game ecosystem.
It exports all events, mechanics, items, and their effects to a text file.

The documentation includes:
- All events organized by wealth tier and time of day
- Requirements and conditions for each event
- Effects and outcomes
- Calculated odds based on the event pools
- All items, status effects, injuries, and dangers
- The complete game flow and mechanics
"""

import random
import time
from datetime import datetime


class GameDocumentationGenerator:
    """Generates comprehensive documentation for the Blackjack game."""
    
    def __init__(self, player_class=None, lists_class=None):
        self.player_class = player_class
        self.lists_class = lists_class
        
    def generate_full_documentation(self, output_path="game_ecosystem_documentation.txt"):
        """
        Generates a complete documentation file of the entire game ecosystem.
        This includes all events, their odds, requirements, effects, and outcomes.
        """
        
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("BLACKJACK: THE COMPLETE GAME ECOSYSTEM DOCUMENTATION")
        lines.append("=" * 80)
        lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("This document contains a comprehensive breakdown of every event,")
        lines.append("mechanic, item, and system in the game. Use this as a reference")
        lines.append("to understand the full scope of what can happen during gameplay.")
        lines.append("")
        lines.append("=" * 80)
        lines.append("")
        
        # Table of Contents
        lines.append("TABLE OF CONTENTS")
        lines.append("-" * 40)
        lines.append("1. Game Overview")
        lines.append("2. Wealth Tiers & Balance Ranges")
        lines.append("3. Day Events by Tier")
        lines.append("4. Night Events by Tier")
        lines.append("5. Secret Events & Hidden Triggers")
        lines.append("6. One-Time Story Events")
        lines.append("7. Conditional Events")
        lines.append("8. Medical Events & Conditions")
        lines.append("9. Car Trouble Events")
        lines.append("10. Ending Paths")
        lines.append("11. Items & Collectibles")
        lines.append("12. Status Effects & Injuries")
        lines.append("13. Companions System")
        lines.append("14. Achievement System")
        lines.append("15. Sanity System")
        lines.append("16. Locations & Shops")
        lines.append("17. NPC Encyclopedia")
        lines.append("18. Event Odds Calculator")
        lines.append("")
        
        # Section 1: Game Overview
        lines.extend(self._generate_game_overview())
        
        # Section 2: Wealth Tiers
        lines.extend(self._generate_wealth_tiers())
        
        # Section 3: Day Events
        lines.extend(self._generate_day_events())
        
        # Section 4: Night Events  
        lines.extend(self._generate_night_events())
        
        # Section 5: Secret Events
        lines.extend(self._generate_secret_events())
        
        # Section 6: One-Time Events
        lines.extend(self._generate_onetime_events())
        
        # Section 7: Conditional Events
        lines.extend(self._generate_conditional_events())
        
        # Section 8: Medical Events
        lines.extend(self._generate_medical_events())
        
        # Section 9: Car Trouble
        lines.extend(self._generate_car_trouble_events())
        
        # Section 10: Endings
        lines.extend(self._generate_endings())
        
        # Section 11: Items
        lines.extend(self._generate_items_list())
        
        # Section 12: Status Effects
        lines.extend(self._generate_status_effects())
        
        # Section 13: Companions
        lines.extend(self._generate_companions_info())
        
        # Section 14: Achievements
        lines.extend(self._generate_achievements())
        
        # Section 15: Sanity System
        lines.extend(self._generate_sanity_system())
        
        # Section 16: Locations
        lines.extend(self._generate_locations())
        
        # Section 17: NPCs
        lines.extend(self._generate_npc_encyclopedia())
        
        # Section 18: Odds Calculator
        lines.extend(self._generate_odds_calculator())
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"Documentation generated: {output_path}")
        return output_path
    
    def _generate_game_overview(self):
        """Generate the game overview section."""
        lines = []
        lines.append("=" * 80)
        lines.append("1. GAME OVERVIEW")
        lines.append("=" * 80)
        lines.append("")
        lines.append("PREMISE:")
        lines.append("-" * 40)
        lines.append("You are a gambler living in your station wagon, trying to win $1,000,000")
        lines.append("at the local casino's blackjack table. Each day consists of:")
        lines.append("")
        lines.append("  MORNING/AFTERNOON: Random events occur based on your current wealth tier")
        lines.append("  EVENING: You travel to the casino (if you have a working car)")  
        lines.append("  NIGHT: You play blackjack against The Dealer")
        lines.append("  LATE NIGHT: Night events can occur as you return to your car")
        lines.append("")
        lines.append("CORE MECHANICS:")
        lines.append("-" * 40)
        lines.append("  - HEALTH (0-100): Your physical wellbeing. Reaches 0 = Death")
        lines.append("  - SANITY (0-100): Your mental state. Low sanity causes hallucinations")
        lines.append("  - BALANCE ($): Your current money. Goal is $1,000,000")
        lines.append("  - INVENTORY: Items that provide benefits or are required for events")
        lines.append("  - STATUS EFFECTS: Temporary conditions affecting gameplay")
        lines.append("  - INJURIES: Physical wounds that may require medical attention")
        lines.append("  - COMPANIONS: Pets that provide bonuses and restore sanity")
        lines.append("")
        lines.append("WIN CONDITION: Reach $1,000,000")
        lines.append("LOSE CONDITIONS: Health reaches 0, certain bad endings, giving up")
        lines.append("")
        return lines
    
    def _generate_wealth_tiers(self):
        """Generate wealth tier documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("2. WEALTH TIERS & BALANCE RANGES")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Your current balance determines which tier of events you experience.")
        lines.append("Higher tiers have more dramatic events with bigger risks and rewards.")
        lines.append("")
        lines.append("TIER              | BALANCE RANGE        | DESCRIPTION")
        lines.append("-" * 70)
        lines.append("POOR              | $1 - $1,000          | Scraping by, desperate survival")
        lines.append("CHEAP             | $1,000 - $10,000     | Getting somewhere, still struggling")
        lines.append("MODEST            | $10,000 - $100,000   | Comfortable, but not safe")
        lines.append("RICH              | $100,000 - $500,000  | Living well, high stakes")
        lines.append("DOUGHMAN          | $500,000 - $900,000  | Almost there, maximum pressure")
        lines.append("NEARLY THERE      | $900,000 - $999,999  | The final stretch, destiny awaits")
        lines.append("")
        lines.append("NOTE: Each tier has its own unique pool of events. Events from lower")
        lines.append("tiers may still occur occasionally at higher tiers.")
        lines.append("")
        return lines
    
    def _generate_day_events(self):
        """Generate day events documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("3. DAY EVENTS BY TIER")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Day events occur every morning/afternoon. They are selected randomly")
        lines.append("from your current wealth tier's event pool.")
        lines.append("")
        
        # Document each tier's day events
        tiers = [
            ("POOR ($1 - $1,000)", self._get_poor_day_events()),
            ("CHEAP ($1,000 - $10,000)", self._get_cheap_day_events()),
            ("MODEST ($10,000 - $100,000)", self._get_modest_day_events()),
            ("RICH ($100,000 - $500,000)", self._get_rich_day_events()),
            ("DOUGHMAN ($500,000 - $900,000)", self._get_doughman_day_events()),
            ("NEARLY THERE ($900,000+)", self._get_nearly_day_events()),
        ]
        
        for tier_name, events in tiers:
            lines.append("-" * 70)
            lines.append(f"TIER: {tier_name}")
            lines.append("-" * 70)
            lines.append(f"Total Events in Pool: {len(events)}")
            lines.append(f"Base Odds per Event: 1/{len(events)} = {100/len(events):.2f}%")
            lines.append("")
            
            # Categorize events
            everytime = [e for e in events if self._is_everytime_event(e)]
            conditional = [e for e in events if self._is_conditional_event(e)]
            onetime = [e for e in events if self._is_onetime_event(e)]
            secret = [e for e in events if self._is_secret_event(e)]
            
            if everytime:
                lines.append("  EVERYTIME EVENTS (can repeat):")
                for event in sorted(everytime):
                    lines.append(f"    • {self._format_event_name(event)}")
                lines.append("")
            
            if conditional:
                lines.append("  CONDITIONAL EVENTS (require specific conditions):")
                for event in sorted(conditional):
                    lines.append(f"    • {self._format_event_name(event)}")
                lines.append("")
            
            if onetime:
                lines.append("  ONE-TIME EVENTS (story events, only happen once):")
                for event in sorted(onetime):
                    lines.append(f"    • {self._format_event_name(event)}")
                lines.append("")
            
            if secret:
                lines.append("  SECRET EVENTS (hidden triggers):")
                for event in sorted(secret):
                    lines.append(f"    • {self._format_event_name(event)}")
                lines.append("")
        
        return lines
    
    def _generate_night_events(self):
        """Generate night events documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("4. NIGHT EVENTS BY TIER")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Night events occur after the casino, as you return to your car.")
        lines.append("These tend to be more atmospheric and sometimes more dangerous.")
        lines.append("")
        
        tiers = [
            ("POOR ($1 - $1,000)", self._get_poor_night_events()),
            ("CHEAP ($1,000 - $10,000)", self._get_cheap_night_events()),
            ("MODEST ($10,000 - $100,000)", self._get_modest_night_events()),
            ("RICH ($100,000 - $500,000)", self._get_rich_night_events()),
            ("DOUGHMAN ($500,000 - $900,000)", self._get_doughman_night_events()),
            ("NEARLY THERE ($900,000+)", self._get_nearly_night_events()),
        ]
        
        for tier_name, events in tiers:
            lines.append("-" * 70)
            lines.append(f"TIER: {tier_name}")
            lines.append("-" * 70)
            lines.append(f"Total Events in Pool: {len(events)}")
            if len(events) > 0:
                lines.append(f"Base Odds per Event: 1/{len(events)} = {100/len(events):.2f}%")
            lines.append("")
            
            for event in sorted(events):
                lines.append(f"  • {self._format_event_name(event)}")
            lines.append("")
        
        return lines
    
    def _generate_secret_events(self):
        """Generate secret events documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("5. SECRET EVENTS & HIDDEN TRIGGERS")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Secret events are triggered by specific conditions, often related to")
        lines.append("your exact balance or meeting certain hidden requirements.")
        lines.append("")
        lines.append("-" * 70)
        lines.append("BALANCE-TRIGGERED SECRETS:")
        lines.append("-" * 70)
        lines.append("")
        lines.append("  $21 exactly:        'Perfect Hand' - Blackjack reference")
        lines.append("  $50 exactly:        'Fifty Fifty' - Coin flip event")
        lines.append("  $100 exactly:       'Benjamin's Blessing' - Hundred dollar bonus")
        lines.append("  $111 exactly:       'Triple Ones' - Lucky angel numbers")
        lines.append("  $666 exactly:       'Devil's Deal' - Dark bargain opportunity")
        lines.append("  $777 exactly:       'Triple Sevens' - Slot machine luck")
        lines.append("  $1,000 exactly:     'Milestone' - Wealth tier celebration")
        lines.append("  $1,111 exactly:     'Angel Numbers' - Spiritual encounter")
        lines.append("  $7,777 exactly:     'Lucky Seven Grand' - Major luck event")
        lines.append("  $10,000 exactly:    'Five Figures' - Milestone event")
        lines.append("  $13,013 exactly:    'Unlucky Number' - Bad omen event")
        lines.append("  $21,000 exactly:    'Blackjack Jackpot' - Special bonus")
        lines.append("  $50,000 exactly:    'Halfway There' - Major milestone")
        lines.append("  $100,000 exactly:   'Six Figures' - Life-changing threshold")
        lines.append("  $250,000 exactly:   'Quarter Million' - The Offer event")
        lines.append("  $500,000 exactly:   'Half Million' - Doughman initiation")
        lines.append("  $777,777 exactly:   'Lucky Sevens Jackpot' - Ultimate luck")
        lines.append("  $999,999 exactly:   'One Dollar Away' - Dramatic finale trigger")
        lines.append("")
        lines.append("-" * 70)
        lines.append("CONDITION-TRIGGERED SECRETS:")
        lines.append("-" * 70)
        lines.append("")
        lines.append("  All 3 Dream Sequences Complete: 'All Dreams Complete' - Full backstory")
        lines.append("  Sanity below 25 for 5+ days:    'Madness Confrontation' - Battle yourself")
        lines.append("  Met all NPCs:                   'Social Butterfly' achievement event")
        lines.append("  5 Companions at once:           'Noah's Ark' - Animal gathering")
        lines.append("  Rabbit chase 5+ attempts:       'The Mystical Rabbit' - Final catch")
        lines.append("  Suzy storyline complete:        'Gift From Suzy' or 'Suzy the Snitch'")
        lines.append("")
        return lines
    
    def _generate_onetime_events(self):
        """Generate one-time story events documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("6. ONE-TIME STORY EVENTS")
        lines.append("=" * 80)
        lines.append("")
        lines.append("These events only happen once per playthrough and typically involve")
        lines.append("meeting important NPCs or experiencing key story moments.")
        lines.append("")
        
        story_events = {
            "POOR TIER": [
                ("lone_cowboy", "Meet a lone cowboy with tales of the road"),
                ("whats_my_name", "Suzy introduces herself and asks your name"),
                ("interrogation", "The Interrogator in the red suit questions you"),
                ("old_man_jenkins", "Old Man Jenkins shares his wisdom"),
                ("the_mime", "A mysterious mime appears with a message"),
            ],
            "CHEAP TIER": [
                ("tom_the_mechanic", "Meet Tom at his Trucks & Tires shop"),
                ("whats_my_favorite_color", "Suzy asks about your favorite color"),
                ("the_bridge_angel", "Save someone at the bridge (affects ending)"),
                ("stray_cat_adopt", "Adopt a stray cat as companion"),
            ],
            "MODEST TIER": [
                ("frank_the_bartender", "Meet Frank at the Watering Hole"),
                ("whats_my_favorite_animal", "Suzy asks about your favorite animal"),
                ("the_photographer", "A photographer documents your journey"),
                ("street_performer_friend", "Befriend a street performer"),
            ],
            "RICH TIER": [
                ("the_rival", "Victoria challenges you as a rival gambler"),
                ("high_roller_invitation", "Get invited to a high stakes room"),
                ("luxury_car_offer", "Someone offers to buy your story"),
            ],
            "DOUGHMAN TIER": [
                ("the_veteran", "Meet a veteran gambler with advice"),
                ("the_journalist", "A journalist wants to interview you"),
                ("victoria_returns", "The Rival returns for round 2"),
            ],
            "NEARLY THERE TIER": [
                ("the_warning", "A prophet warns about your path"),
                ("the_offer", "A mysterious offer to double your money"),
                ("final_dream", "The ultimate dream sequence"),
                ("gift_from_suzy", "Suzy's final gift (good path)"),
                ("suzy_the_snitch", "Suzy betrays you (bad path)"),
            ],
        }
        
        for tier, events in story_events.items():
            lines.append(f"-" * 70)
            lines.append(f"{tier}")
            lines.append(f"-" * 70)
            for event_name, description in events:
                lines.append(f"  • {self._format_event_name(event_name)}")
                lines.append(f"    → {description}")
            lines.append("")
        
        return lines
    
    def _generate_conditional_events(self):
        """Generate conditional events documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("7. CONDITIONAL EVENTS")
        lines.append("=" * 80)
        lines.append("")
        lines.append("These events only trigger if specific conditions are met.")
        lines.append("If conditions aren't met, another event is selected instead.")
        lines.append("")
        
        conditional_events = [
            ("sore_throat", "Status: No 'Sore Throat'", "Get sick with a sore throat"),
            ("spider_bite", "Danger: 'Spider' present", "Get bitten by a car spider"),
            ("hungry_cockroach", "Danger: 'Cockroach' present", "Cockroach eats your money"),
            ("ant_bite", "Danger: 'Ants' present", "Ant infestation bites you"),
            ("knife_wound_infection", "Injury: 'Knife Wound'", "Wound gets infected"),
            ("stray_cat_sick", "Companion: Stray Cat, 7+ days", "Cat gets sick"),
            ("stray_cat_dies", "Companion: Sick Cat, 3+ days", "Cat dies if untreated"),
            ("cow_army", "Met: 'Betsy', Danger: 'Betsy Army'", "Army of cows attack"),
            ("final_interrogation", "Met: 'Interrogator', Danger: 'Final Interrogation'", "Phil's final confrontation"),
            ("painkiller_withdrawal", "Status: 'Addicted to Painkillers', No pills", "Suffer withdrawal"),
            ("cocaine_crash", "Status: 'Cocaine High' expired", "Crash after cocaine high"),
            ("soulless_emptiness", "Status: 'Soulless'", "Feel empty inside"),
            ("victoria_returns", "Met: 'The Rival'", "Rival gambler returns"),
        ]
        
        lines.append("EVENT NAME".ljust(30) + "REQUIREMENT".ljust(35) + "EFFECT")
        lines.append("-" * 100)
        
        for event, requirement, effect in conditional_events:
            lines.append(f"{self._format_event_name(event).ljust(30)}{requirement.ljust(35)}{effect}")
        
        lines.append("")
        return lines
    
    def _generate_medical_events(self):
        """Generate medical events documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("8. MEDICAL EVENTS & CONDITIONS")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Medical events add various illnesses, injuries, and conditions.")
        lines.append("Many require visiting the Doctor to cure or treat.")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("INFECTIOUS DISEASES:")
        lines.append("-" * 70)
        diseases = [
            ("Pneumonia", "-15 HP, -2 Sanity", "Rest + Doctor"),
            ("Bronchitis", "-8 HP", "Rest + Medicine"),
            ("Strep Throat", "-10 HP", "Antibiotics required"),
            ("Stomach Flu", "-12 HP, -1 Sanity", "Time + Fluids"),
            ("Ear Infection", "-5 HP", "Antibiotics"),
            ("Sinus Infection", "-6 HP", "Time or Antibiotics"),
            ("UTI", "-8 HP", "Antibiotics required"),
            ("Pink Eye", "-3 HP", "Eye drops"),
            ("Mononucleosis", "-20 HP, -3 Sanity", "Rest (months)"),
            ("Shingles", "-18 HP, -2 Sanity", "Antivirals"),
            ("Lyme Disease", "-15 HP, -2 Sanity", "Antibiotics ASAP"),
            ("Tetanus", "-25 HP, -3 Sanity", "Antitoxin required"),
            ("Measles", "-18 HP, -2 Sanity", "Quarantine + Time"),
        ]
        
        lines.append("CONDITION".ljust(20) + "EFFECT".ljust(25) + "CURE")
        lines.append("-" * 70)
        for condition, effect, cure in diseases:
            lines.append(f"{condition.ljust(20)}{effect.ljust(25)}{cure}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("INJURIES:")
        lines.append("-" * 70)
        injuries = [
            ("Broken Ribs", "-20 HP, -2 Sanity", "6+ weeks rest"),
            ("Broken Ankle", "-15 HP, -2 Sanity", "Cast + Crutches"),
            ("Broken Wrist", "-12 HP, -1 Sanity", "Cast"),
            ("Broken Hand", "-15 HP, -2 Sanity", "Surgery likely"),
            ("Concussion", "-15 HP, -4 Sanity", "Rest + Monitoring"),
            ("Torn ACL", "-20 HP, -3 Sanity", "Surgery + Rehab"),
            ("Herniated Disc", "-18 HP, -3 Sanity", "Rest or Surgery"),
            ("Dislocated Shoulder", "-18 HP, -2 Sanity", "Reduction needed"),
            ("Deep Laceration", "-22 HP", "Stitches"),
            ("Skull Fracture", "-40 HP, -6 Sanity", "Emergency Surgery"),
            ("Ruptured Spleen", "-35 HP, -4 Sanity", "Emergency Surgery"),
        ]
        
        lines.append("INJURY".ljust(20) + "EFFECT".ljust(25) + "TREATMENT")
        lines.append("-" * 70)
        for injury, effect, treatment in injuries:
            lines.append(f"{injury.ljust(20)}{effect.ljust(25)}{treatment}")
        lines.append("")
        
        return lines
    
    def _generate_car_trouble_events(self):
        """Generate car trouble events documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("9. CAR TROUBLE EVENTS")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Car trouble can waste your entire afternoon, preventing travel.")
        lines.append("Having the right items can fix problems instantly.")
        lines.append("")
        
        car_events = [
            ("dead_battery_afternoon", "Jumper Cables, Portable Charger", "Wastes afternoon if no items"),
            ("engine_overheating", "Coolant, Antifreeze, Water Bottles", "$200 repair without items"),
            ("tire_blowout", "Spare Tire + Car Jack", "$150 tow without items"),
            ("alternator_failing", "None (must pay $350)", "Car dies completely"),
            ("ran_out_of_gas", "Gas Can", "$35 + 2 hours without item"),
            ("brake_fluid_leak", "Brake Fluid", "Cannot drive without fix"),
            ("radiator_leak", "Radiator Stop Leak", "$200-400 repair"),
            ("frozen_door_locks", "Lock De-Icer, Lighter", "1 hour delay"),
            ("catalytic_converter_stolen", "None (must replace)", "$1000-2500 replacement"),
            ("transmission_slipping", "Transmission Fluid", "Thousands to repair"),
        ]
        
        lines.append("EVENT".ljust(30) + "ITEMS THAT HELP".ljust(35) + "CONSEQUENCE")
        lines.append("-" * 100)
        for event, items, consequence in car_events:
            lines.append(f"{self._format_event_name(event).ljust(30)}{items.ljust(35)}{consequence}")
        lines.append("")
        
        return lines
    
    def _generate_endings(self):
        """Generate endings documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("10. ENDING PATHS")
        lines.append("=" * 80)
        lines.append("")
        lines.append("The game has multiple endings based on your choices and conditions.")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("GOOD ENDINGS:")
        lines.append("-" * 70)
        lines.append("")
        lines.append("  SALVATION (Best Ending)")
        lines.append("    Requirement: Call Rebecca at Tom's, choose to go home")
        lines.append("    Outcome: Return to family, live a full life, watch kids grow")
        lines.append("")
        lines.append("  MILLIONAIRE (Goal Ending)")
        lines.append("    Requirement: Reach $1,000,000")
        lines.append("    Outcome: Achieve your goal, various epilogues possible")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("NEUTRAL ENDINGS:")
        lines.append("-" * 70)
        lines.append("")
        lines.append("  RESURRECTION")
        lines.append("    Requirement: Refuse to go home when given the chance")
        lines.append("    Outcome: Continue gambling forever, outcome unknown")
        lines.append("")
        lines.append("  THE OFFER ACCEPTED")
        lines.append("    Requirement: Accept the mysterious offer at $900k+")
        lines.append("    Outcome: Get double your money, but banned from casinos")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("BAD ENDINGS:")
        lines.append("-" * 70)
        lines.append("")
        lines.append("  DEATH (Multiple Causes)")
        lines.append("    - Health reaches 0")
        lines.append("    - Killed by NPCs (Cow Army, Phil, Loan Shark)")
        lines.append("    - Medical emergencies untreated")
        lines.append("    - Car accidents")
        lines.append("    - Random deadly events")
        lines.append("")
        lines.append("  MADNESS ENDING")
        lines.append("    Requirement: Fail the Madness Confrontation at low sanity")
        lines.append("    Outcome: Your mind shatters, something else takes control")
        lines.append("    Note: This is a secret ending with extensive narrative")
        lines.append("")
        lines.append("  SUZY THE SNITCH")
        lines.append("    Requirement: Complete Suzy storyline on bad path")
        lines.append("    Outcome: Suzy reports you to police, arrested")
        lines.append("")
        
        return lines
    
    def _generate_items_list(self):
        """Generate items documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("11. ITEMS & COLLECTIBLES")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("HEALING ITEMS:")
        lines.append("-" * 70)
        items = [
            ("First Aid Kit", "+30 HP", "Convenience Store"),
            ("Bandages", "+15 HP", "Convenience Store"),
            ("Pain Killers", "+10 HP, Risk of Addiction", "Convenience Store"),
            ("Energy Drink", "+5 HP, Temporary Energy", "Convenience Store"),
            ("Sandwich", "+10 HP", "Random events"),
            ("Granny's Swamp Nectar", "+25-50 HP (random)", "Swamp events"),
        ]
        for item, effect, source in items:
            lines.append(f"  {item.ljust(25)} {effect.ljust(30)} Source: {source}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("CAR REPAIR ITEMS:")
        lines.append("-" * 70)
        items = [
            ("Jumper Cables", "Fix dead battery", "Tom's Shop"),
            ("Spare Tire", "Fix flat tire", "Tom's Shop"),
            ("Motor Oil", "Refill empty oil", "Gas Station"),
            ("Coolant", "Fix overheating", "Gas Station"),
            ("Tool Kit", "DIY repairs", "Tom's Shop"),
            ("Gas Can", "Emergency fuel", "Gas Station"),
            ("WD-40", "Fix stuck parts", "Convenience Store"),
        ]
        for item, effect, source in items:
            lines.append(f"  {item.ljust(25)} {effect.ljust(30)} Source: {source}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("COLLECTIBLES (Sell to Gus):")
        lines.append("-" * 70)
        collectibles = [
            ("Golden Trident", "$80,000"),
            ("Kraken Pearl", "$100,000"),
            ("Mermaid's Scale", "$50,000"),
            ("Captain's Compass", "$45,000"),
            ("Pirate's Eye Patch", "$10,000"),
            ("Treasure Map", "$35,000"),
            ("Ancient Coin", "$20,000"),
            ("Crystal Skull", "$75,000"),
            ("Dragon's Tooth", "$90,000"),
        ]
        for item, value in collectibles:
            lines.append(f"  {item.ljust(25)} Value: {value}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("SPECIAL/UNIQUE ITEMS:")
        lines.append("-" * 70)
        special_items = [
            ("Grandfather Clock", "Running joke item, Dealer comments on it"),
            ("Suzy's Gift", "Heartwarming stuffed animal from Suzy"),
            ("Witch's Favor", "Met marker (witch grants Lucky status)"),
            ("Map", "Unlocks Marvin's Mystical Merchandise"),
            ("Quiet Sneakers", "Avoid bear attacks, has durability"),
            ("Gambler's Charm", "Luck bonus at blackjack"),
            ("Gator Tooth Necklace", "Gators respect you in swamp"),
            ("Bear King's Respect", "Met marker (earned by defeating giant bear)"),
        ]
        for item, effect in special_items:
            lines.append(f"  {item.ljust(25)} {effect}")
        lines.append("")
        
        return lines
    
    def _generate_status_effects(self):
        """Generate status effects documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("12. STATUS EFFECTS & INJURIES")
        lines.append("=" * 80)
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("POSITIVE STATUS EFFECTS:")
        lines.append("-" * 70)
        positive = [
            ("Lucky", "Increased blackjack win chance"),
            ("At Peace", "Sanity restores faster"),
            ("Energized", "Temporary health regeneration"),
            ("Witch's Blessing", "Good fortune in events"),
            ("Lucky", "20% push-on-loss from various events (fairy, witch, mermaid, etc.)"),
            ("Dog Blessed", "Companion bonuses enhanced"),
        ]
        for status, effect in positive:
            lines.append(f"  {status.ljust(25)} {effect}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("NEGATIVE STATUS EFFECTS:")
        lines.append("-" * 70)
        negative = [
            ("Sore Throat", "Minor discomfort"),
            ("Spider Bite", "Slow health drain"),
            ("Hepatitis", "Serious illness, needs treatment"),
            ("Addicted to Painkillers", "Withdrawal if no pills"),
            ("Soulless", "Random sanity effects"),
            ("Marked", "Bad luck from witch"),
            ("Paranoid", "Extra negative events"),
        ]
        for status, effect in negative:
            lines.append(f"  {status.ljust(25)} {effect}")
        lines.append("")
        
        return lines
    
    def _generate_companions_info(self):
        """Generate companions documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("13. COMPANIONS SYSTEM")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Companions provide sanity restoration and special bonuses.")
        lines.append("They need to be fed their favorite food to stay happy.")
        lines.append("")
        
        companions = [
            ("Squirrelly", "Squirrel", "Bag of Acorns", "+2 Sanity/day, +1 Luck"),
            ("Whiskers", "Alley Cat", "Cat Food", "+3 Sanity/day, Danger Warning"),
            ("Lucky", "Three-Legged Dog", "Dog Food", "+5 Sanity/day, Protection"),
            ("Mr. Pecks", "Crow", "Birdseed", "+1 Sanity/day, Finds Money"),
            ("Patches", "Opossum", "Garbage", "+2 Sanity/day, Night Bonus"),
            ("Rusty", "Raccoon", "Anything", "+2 Sanity/day, Steal Chance"),
            ("Slick", "Rat", "Cheese", "+1 Sanity/day, Danger Warning"),
            ("Hopper", "Rabbit", "Carrot", "+2 Sanity/day, +3 Luck"),
        ]
        
        lines.append("NAME".ljust(15) + "TYPE".ljust(20) + "FOOD".ljust(15) + "BONUSES")
        lines.append("-" * 80)
        for name, type_, food, bonuses in companions:
            lines.append(f"{name.ljust(15)}{type_.ljust(20)}{food.ljust(15)}{bonuses}")
        lines.append("")
        
        lines.append("COMPANION HAPPINESS:")
        lines.append("  - Happiness decreases if not fed")
        lines.append("  - Unhappy companions may leave")
        lines.append("  - Bonding increases over time with feeding")
        lines.append("  - Max bond unlocks special events")
        lines.append("")
        
        return lines
    
    def _generate_achievements(self):
        """Generate achievements documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("14. ACHIEVEMENT SYSTEM")
        lines.append("=" * 80)
        lines.append("")
        
        achievements = {
            "MONEY MILESTONES": [
                ("Baby Steps", "Reach $1,000"),
                ("Getting Somewhere", "Reach $10,000"),
                ("Big Spender", "Reach $100,000"),
                ("Almost There", "Reach $500,000"),
                ("The Dream", "Reach $1,000,000"),
            ],
            "SURVIVAL": [
                ("Still Kicking", "Survive 7 days"),
                ("Stubborn", "Survive 30 days"),
                ("The Long Road", "Survive 100 days"),
                ("Clinging to Life", "Survive with 10 HP"),
            ],
            "GAMBLING": [
                ("Blackjack Master", "Hit 10 blackjacks"),
                ("Hot Streak", "Win 5 hands in a row"),
                ("Card Shark", "Play 100 hands"),
                ("High Roller", "Win $10,000+ in one hand"),
            ],
            "COMPANIONS": [
                ("First Friend", "Get first companion"),
                ("Animal Lover", "Have 3+ companions"),
                ("Best Friends", "Max bond with companion"),
            ],
            "SPECIAL": [
                ("Rock Bottom", "Lose all money and recover"),
                ("Devil's Deal", "Make deal with devil"),
                ("Debt Free", "Pay off loan shark"),
            ],
        }
        
        for category, achs in achievements.items():
            lines.append(f"-" * 70)
            lines.append(f"{category}")
            lines.append(f"-" * 70)
            for name, description in achs:
                lines.append(f"  [{name}] - {description}")
            lines.append("")
        
        return lines
    
    def _generate_sanity_system(self):
        """Generate sanity system documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("15. SANITY SYSTEM")
        lines.append("=" * 80)
        lines.append("")
        lines.append("Sanity ranges from 0-100 and affects your perception of events.")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("SANITY THRESHOLDS:")
        lines.append("-" * 70)
        lines.append("  100-76: Normal - No effects")
        lines.append("  75-51:  Uneasy - Occasional unsettling thoughts")
        lines.append("  50-26:  Disturbed - Hallucinations, altered perception")
        lines.append("  25-1:   Broken - Severe effects, madness confrontation risk")
        lines.append("  0:      Catatonic - Cannot function")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("SANITY EFFECTS:")
        lines.append("-" * 70)
        lines.append("  - Low sanity changes event descriptions")
        lines.append("  - Hallucinations appear as fake events")
        lines.append("  - Companions may appear to speak")
        lines.append("  - The Dealer's dialogue becomes more sinister")
        lines.append("  - At very low sanity, the Madness Confrontation occurs")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("RESTORING SANITY:")
        lines.append("-" * 70)
        lines.append("  - Companions restore sanity daily")
        lines.append("  - Positive events can restore sanity")
        lines.append("  - Good sleep restores sanity")
        lines.append("  - Certain items restore sanity")
        lines.append("  - The Doctor can prescribe treatment")
        lines.append("")
        
        return lines
    
    def _generate_locations(self):
        """Generate locations documentation."""
        lines = []
        lines.append("=" * 80)
        lines.append("16. LOCATIONS & SHOPS")
        lines.append("=" * 80)
        lines.append("")
        
        locations = [
            ("The Casino", "Main gameplay location, blackjack tables"),
            ("Your Wagon", "Home base, where events occur"),
            ("Tom's Trucks & Tires", "Car repairs, story events with Tom"),
            ("The Watering Hole", "Bar with Frank, story events"),
            ("Gus's Pawn Shop", "Sell collectibles, buy items"),
            ("Marvin's Mystical Merchandise", "Secret shop, requires Map"),
            ("The Doctor", "Heal injuries, cure illnesses"),
            ("Convenience Store", "Basic supplies"),
            ("Gas Station", "Fuel, car supplies"),
            ("Vinnie's Corner", "Loan shark, desperate measures"),
        ]
        
        for location, description in locations:
            lines.append(f"-" * 70)
            lines.append(f"{location}")
            lines.append(f"-" * 70)
            lines.append(f"  {description}")
            lines.append("")
        
        return lines
    
    def _generate_npc_encyclopedia(self):
        """Generate NPC encyclopedia."""
        lines = []
        lines.append("=" * 80)
        lines.append("17. NPC ENCYCLOPEDIA")
        lines.append("=" * 80)
        lines.append("")
        
        npcs = [
            ("The Dealer", "Antagonist", "The mysterious casino dealer with a jade eye and a dark past"),
            ("Tom", "Friendly", "Owner of Tom's Trucks & Tires, has 3 dream sequences"),
            ("Frank", "Neutral", "Bartender at The Watering Hole, has 3 dream sequences"),
            ("Oswald", "Mysterious", "Strange figure, has 3 dream sequences about the casino"),
            ("Suzy", "Innocent", "Jump-roping girl with a storyline that can end good or bad"),
            ("Victoria", "Rival", "Fellow gambler who challenges you at higher tiers"),
            ("Phil/Interrogator", "Antagonist", "Man in red suit who harasses homeless people"),
            ("Betsy", "Animal", "A cow who becomes an army leader if wronged"),
            ("Vinnie", "Loan Shark", "Provides loans with escalating consequences"),
            ("Gus", "Merchant", "Pawn shop owner who buys collectibles"),
            ("Marvin", "Mysterious", "Runs secret mystical shop, sells unusual items"),
            ("Rebecca", "Family", "Your wife, crucial to the Salvation ending"),
            ("Nathan", "Family", "Your son, learned to walk, first word was 'Dada'"),
        ]
        
        for name, role, description in npcs:
            lines.append(f"  {name} ({role})")
            lines.append(f"    {description}")
            lines.append("")
        
        return lines
    
    def _generate_odds_calculator(self):
        """Generate dynamic odds calculator section."""
        lines = []
        lines.append("=" * 80)
        lines.append("18. EVENT ODDS CALCULATOR")
        lines.append("=" * 80)
        lines.append("")
        lines.append("This section shows the probability of encountering each event type.")
        lines.append("Odds are calculated based on event pool sizes.")
        lines.append("")
        
        # Calculate odds for each tier
        tiers_data = [
            ("POOR", self._get_poor_day_events(), self._get_poor_night_events()),
            ("CHEAP", self._get_cheap_day_events(), self._get_cheap_night_events()),
            ("MODEST", self._get_modest_day_events(), self._get_modest_night_events()),
            ("RICH", self._get_rich_day_events(), self._get_rich_night_events()),
            ("DOUGHMAN", self._get_doughman_day_events(), self._get_doughman_night_events()),
            ("NEARLY", self._get_nearly_day_events(), self._get_nearly_night_events()),
        ]
        
        for tier_name, day_events, night_events in tiers_data:
            lines.append(f"-" * 70)
            lines.append(f"{tier_name} TIER ODDS:")
            lines.append(f"-" * 70)
            
            day_count = len(day_events)
            night_count = len(night_events)
            
            if day_count > 0:
                lines.append(f"  Day Events Pool: {day_count} events")
                lines.append(f"  Base odds per day event: 1/{day_count} = {100/day_count:.2f}%")
            
            if night_count > 0:
                lines.append(f"  Night Events Pool: {night_count} events")
                lines.append(f"  Base odds per night event: 1/{night_count} = {100/night_count:.2f}%")
            
            lines.append("")
            lines.append("  NOTE: Conditional events may redirect if conditions not met,")
            lines.append("  effectively increasing odds of other events.")
            lines.append("")
        
        lines.append("-" * 70)
        lines.append("SECRET EVENT ODDS:")
        lines.append("-" * 70)
        lines.append("  Balance-triggered secrets: 100% when exact balance is reached")
        lines.append("  Madness Confrontation: Triggers when sanity < 25 for 5+ consecutive days")
        lines.append("  Dream sequences: 1/10 chance when conditions met")
        lines.append("  Rare event variants: Typically 3-5% chance")
        lines.append("")
        
        return lines
    
    # Helper methods for event categorization
    def _get_poor_day_events(self):
        return ["seat_cash", "left_window_down", "estranged_dog", "freight_truck", 
                "morning_stretch", "ant_invasion", "bird_droppings", "flat_tire",
                "mysterious_note", "radio_static", "sore_throat", "spider_bite", 
                "hungry_cockroach", "lone_cowboy", "whats_my_name", "interrogation"]
    
    def _get_cheap_day_events(self):
        return ["sun_visor_bills", "strong_winds", "morning_fog", "car_wont_start",
                "raccoon_raid", "beautiful_sunrise", "fortune_cookie", "tom_the_mechanic",
                "whats_my_favorite_color", "the_bridge_angel", "stray_cat_adopt"]
    
    def _get_modest_day_events(self):
        return ["street_performer", "the_photographer", "frank_the_bartender",
                "whats_my_favorite_animal", "mosquito_swarm", "scorching_sun"]
    
    def _get_rich_day_events(self):
        return ["luxury_car_passes", "the_rival", "high_roller_invitation",
                "the_investor", "paparazzi_encounter"]
    
    def _get_doughman_day_events(self):
        return ["high_stakes_feeling", "the_veteran", "the_journalist",
                "final_preparation", "victoria_returns"]
    
    def _get_nearly_day_events(self):
        return ["the_surveillance", "last_stretch", "strange_visitors",
                "too_close_to_quit", "the_warning", "the_celebration",
                "final_dream", "the_offer", "gift_from_suzy", "suzy_the_snitch"]
    
    def _get_poor_night_events(self):
        return ["ditched_wallet", "went_jogging", "woodlands_path",
                "stargazing", "chase_the_rabbit"]
    
    def _get_cheap_night_events(self):
        return ["woodlands_river", "woodlands_field", "swamp_stroll",
                "whats_my_favorite_color", "chase_the_second_rabbit"]
    
    def _get_modest_night_events(self):
        return ["swamp_wade", "swamp_swim", "beach_stroll",
                "chase_the_third_rabbit"]
    
    def _get_rich_night_events(self):
        return ["beach_swim", "beach_dive", "city_streets",
                "whats_my_favorite_animal", "chase_the_fourth_rabbit"]
    
    def _get_doughman_night_events(self):
        return ["city_stroll", "city_park", "chase_the_fifth_rabbit"]
    
    def _get_nearly_night_events(self):
        return ["woodlands_adventure", "swamp_adventure", "beach_adventure"]
    
    def _is_everytime_event(self, event_name):
        everytime = ["seat_cash", "left_window_down", "estranged_dog", "freight_truck",
                    "morning_stretch", "ant_invasion", "bird_droppings", "flat_tire",
                    "ditched_wallet", "went_jogging"]
        return event_name in everytime
    
    def _is_conditional_event(self, event_name):
        conditional = ["sore_throat", "spider_bite", "hungry_cockroach", "ant_bite",
                      "knife_wound_infection", "stray_cat_sick", "cow_army"]
        return event_name in conditional
    
    def _is_onetime_event(self, event_name):
        onetime = ["lone_cowboy", "whats_my_name", "interrogation", "tom_the_mechanic",
                  "the_bridge_angel", "frank_the_bartender", "the_rival", "the_veteran"]
        return event_name in onetime
    
    def _is_secret_event(self, event_name):
        secret = ["midnight_visitor", "perfect_hand", "devils_deal", "exactly_999999",
                 "all_dreams_complete", "triple_sevens", "lucky_seven_grand"]
        return event_name in secret
    
    def _format_event_name(self, event_name):
        """Convert snake_case to Title Case."""
        return event_name.replace("_", " ").title()


def generate_documentation():
    """Main function to generate documentation."""
    generator = GameDocumentationGenerator()
    output_path = generator.generate_full_documentation()
    print(f"\nDocumentation has been generated!")
    print(f"File saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_documentation()
