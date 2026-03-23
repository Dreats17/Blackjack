#!/usr/bin/env python3
"""Fix quote escaping issues in story.py and lists.py"""

import re

import os
script_dir = os.path.dirname(os.path.abspath(__file__))
lists_path = os.path.join(script_dir, '..', 'lists.py')
story_path = os.path.join(script_dir, '..', 'story', 'story.py')
# Fix lists.py
print("Fixing lists.py...")
with open(lists_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the entire problematic function
# Search for the function start
start_marker = "def get_dealer_gift_reaction(self, item_name):"
end_marker = "def make_quote_setup_list(self):"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # Replace the entire function with correct version
    new_function = '''def get_dealer_gift_reaction(self, item_name):
        """Return Dealer's reaction to gifts - mysterious, quick, eerie, aware"""
        reactions = {
            # POSITIVE REACTIONS (happiness gain)
            "Ace of Spades": {
                "dialogue": [
                    "\\"The Ace. The beginning and the end.\\"",
                    "\\"You understand the game better than I thought.\\"",
                    "\\"This pleases me.\\""
                ],
                "happiness": 25,
                "kills_you": False
            },
            "Dealer's Joker": {
                "dialogue": [
                    "\\"My card. Returned to me.\\"",
                    "\\"Interesting. You found what was lost.\\"",
                    "\\"The joker always comes home.\\""
                ],
                "happiness": 30,
                "kills_you": False
            },
            "Golden Compass": {
                "dialogue": [
                    "\\"Direction. Purpose. Meaning.\\"",
                    "\\"This points toward something I lost long ago.\\"",
                    "He stares at it for a long moment.",
                    "\\"Thank you.\\""
                ],
                "happiness": 20,
                "kills_you": False
            },
            "Mirror of Duality": {
                "dialogue": [
                    "\\"Two faces. Like mine.\\"",
                    "He looks into it. Both eyes—jade and human—stare back.",
                    "\\"You see too much.\\""
                ],
                "happiness": 15,
                "kills_you": False
            },
            
            # NEUTRAL REACTIONS (no happiness change, but interesting dialogue)
            "Lucky Coin": {
                "dialogue": [
                    "\\"Luck. The gambler's crutch.\\"",
                    "He flips it once. Catches it. Doesn't look at the result.",
                    "\\"Luck is a lie we tell ourselves.\\""
                ],
                "happiness": 0,
                "kills_you": False
            },
            "Pocket Watch": {
                "dialogue": [
                    "\\"Time. Always time with you people.\\"",
                    "\\"The casino has no clocks. Did you ever wonder why?\\"",
                    "\\"Time stops here. Only the cards move.\\""
                ],
                "happiness": 5,
                "kills_you": False
            },
            "Gambler's Grimoire": {
                "dialogue": [
                    "\\"A book of statistics. How quaint.\\"",
                    "He flips through it.",
                    "\\"The numbers never tell the whole story.\\""
                ],
                "happiness": 10,
                "kills_you": False
            },
            
            # NEGATIVE REACTIONS (happiness loss)
            "Cursed Coin": {
                "dialogue": [
                    "\\"You bring CURSES to my table?\\"",
                    "His jade eye flares.",
                    "\\"Bold. Foolish. But bold.\\""
                ],
                "happiness": -15,
                "kills_you": False
            },
            "Necronomicon": {
                "dialogue": [
                    "\\"Dark magic. Here. At MY table.\\"",
                    "The air grows cold.",
                    "\\"You're testing boundaries you don't understand.\\""
                ],
                "happiness": -20,
                "kills_you": False
            },
            "Voodoo Doll": {
                "dialogue": [
                    "\\"You think this works on ME?\\"",
                    "He crushes it in one hand.",
                    "\\"I am not bound by such trivial magic.\\""
                ],
                "happiness": -25,
                "kills_you": False
            },
            
            # DANGEROUS REACTIONS (might kill you)
            "Dealer's Grudge": {
                "dialogue": [
                    "\\"MY grudge. You bring MY grudge. To ME.\\"",
                    "The temperature drops.",
                    "\\"Did you think this was funny?\\""
                ],
                "happiness": -40,
                "kills_you": True
            },
            "Stolen Watch": {
                "dialogue": [
                    "\\"Stolen goods. At my table.\\"",
                    "\\"You insult me with theft.\\"",
                    "\\"We're done here.\\""
                ],
                "happiness": -50,
                "kills_you": True
            },
            
            # FOOD ITEMS (mostly neutral/slightly positive)
            "Sandwich": {
                "dialogue": [
                    "\\"Food. I don't... eat.\\"",
                    "He sets it aside.",
                    "\\"But the gesture is noted.\\""
                ],
                "happiness": 3,
                "kills_you": False
            },
            "Energy Drink": {
                "dialogue": [
                    "\\"Energy. As if I need more.\\"",
                    "\\"I haven't slept in... how long?\\"",
                    "He doesn't remember."
                ],
                "happiness": 2,
                "kills_you": False
            },
            
            # MYSTERIOUS ITEMS (cryptic reactions)
            "Mysterious Lockbox": {
                "dialogue": [
                    "\\"Locked. Like so many things.\\"",
                    "He doesn't try to open it.",
                    "\\"Some boxes should stay closed.\\""
                ],
                "happiness": 8,
                "kills_you": False
            },
            "Moon Shard": {
                "dialogue": [
                    "\\"From above. From beyond.\\"",
                    "It hums in his hand.",
                    "\\"The moon sees everything. Even this place.\\""
                ],
                "happiness": 15,
                "kills_you": False
            },
            
            # DEFAULT for unlisted items
            "_default": {
                "dialogue": [
                    "He examines it carefully.",
                    "\\"Curious.\\"",
                    "He sets it beside the deck of cards."
                ],
                "happiness": 5,
                "kills_you": False
            }
        }
        
        return reactions.get(item_name, reactions["_default"])
    
    '''
    
    content = content[:start_idx] + new_function + content[end_idx:]
    
    with open('lists.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("lists.py fixed!")
else:
    print("Could not find function markers in lists.py")

# Fix story.py
print("\nFixing story.py...")
with open('story.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Fix lines around 1868 and 1883
for i, line in enumerate(lines):
    # Fix line with \"Grace\"
    if 'elif name == \\"Grace\\"' in line:
        lines[i] = line.replace('\\"Grace\\"', '"Grace"')
        print(f"Fixed line {i+1}: Grace")
    
    # Fix lines with type.type(\"...
    if 'type.type(\\"' in line:
        lines[i] = line.replace('type.type(\\"', 'type.type("').replace('\\")', '")')
        print(f"Fixed line {i+1}: type.type quote")
    
    # Fix Squawk
    if 'elif name == \\"Squawk\\"' in line:
        lines[i] = line.replace('\\"Squawk\\"', '"Squawk"')
        print(f"Fixed line {i+1}: Squawk")

with open('story.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("story.py fixed!")

print("\nDone! All quote issues should be resolved.")
