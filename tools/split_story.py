"""
Script to split story.py into mixin files.
Run once, then delete this file.
"""

# Define the splits: (filename, start_line, end_line, class_name, docstring)
# Lines are 1-indexed, inclusive on both ends

# First, read the whole file
with open('story.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

total = len(lines)
print(f"Read {total} lines from story.py")

# The header (imports, color helpers, etc.) is lines 1-55 (before class Player:)
# We need this in every mixin file
header_lines = lines[0:55]  # lines 1-55 (0-indexed: 0-54)
header = ''.join(header_lines)

# Build a reusable import block for mixin files
mixin_header = '''import random
import time
import sys
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\\n\\n"

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
    return ("\\"" + text)

def close_quote(text):
    return (text + "\\"")

def quote(text):
    return ("\\"" + text + "\\"")

def space_quote(text):
    return ("\\"" + text + "\\" ")

'''

# Define the splits by method ranges
# Format: (output_file, class_name, start_method_line, end_before_line, docstring)
splits = [
    # SYSTEMS: sanity, gambling, grimoire, achievements, stats, companions, loan shark, pawn, dealer, gift
    # Lines 625 (get_sanity) through 2383 (end of deliver_gift_to_dealer / sell_item_to_pawn)
    ("story/systems.py", "SystemsMixin", 625, 2365, 
     "Systems: Sanity, gambling stats, grimoire, achievements, statistics, companions, loan shark, pawn shop, dealer happiness, gift system"),
    
    # PAWN/LOAN/BALANCE/RANK: sell_item_to_pawn through update_story_event_prereqs
    # Lines 2365 through 17758
    # Actually this is too big - let's split differently
    
    # ECONOMY: sell_item_to_pawn, balance, rank, day/increment  
    # Lines 2365-2426
    ("story/economy.py", "EconomyMixin", 2365, 2427,
     "Economy: Balance, rank, selling"),
    
    # DAY CYCLE: end_day, first_setup, opening_lines, end_day variants, start_night variants
    # Lines 2427-2678
    ("story/day_cycle.py", "DayCycleMixin", 2427, 2679,
     "Day cycle: end_day, first_setup, opening_lines, start_night"),
    
    # DAY EVENTS: seat_cash through empty_event  
    # Lines 2679-17533
    ("story/events_day.py", "DayEventsMixin", 2679, 17534,
     "Day events: All random day events"),
    
    # MECHANICS: trusty_tom, filthy_frank, optimal_oswald, update_story_event_prereqs
    # Lines 17534-17758
    ("story/mechanics_intro.py", "MechanicsIntroMixin", 17534, 17759,
     "Mechanic intro events: Tom, Frank, Oswald story introductions"),
    
    # START_DAY + pest/car checks + mark_day + update systems
    # Lines 17759-18389
    ("story/game_flow.py", "GameFlowMixin", 17759, 18390,
     "Game flow: start_day, pest control, car trouble checks, day marking, status updates, adventure areas"),
    
    # AFTERNOON + LOCATIONS: afternoon, doctors, mechanics, shops
    # Lines 18390-22623
    ("story/locations.py", "LocationsMixin", 18390, 22624,
     "Locations: Afternoon choices, doctor, witch doctor, mechanics, convenience store, Marvin, pawn shop, loan shark"),
    
    # DURABILITY: All update_X_durability + get_item_desc
    # Lines 22624-23053
    ("story/durability.py", "DurabilityMixin", 22624, 23054,
     "Durability: All item/flask durability update methods, item descriptions"),
    
    # DAY_EVENT + NIGHT_EVENT dispatchers
    # Lines 23054-23119
    ("story/event_dispatch.py", "EventDispatchMixin", 23054, 23120,
     "Event dispatch: day_event() and night_event() random event dispatchers"),
    
    # ENDINGS: goodbye_tom through madness_ending
    # Lines 23120-25875
    ("story/endings.py", "EndingsMixin", 23120, 25876,
     "Endings: All game endings - mechanic endings, millionaire path, madness"),
    
    # MEDICAL: All contract_X, develop_X, injury methods
    # Lines 25876-27629
    ("story/medical.py", "MedicalMixin", 25876, 27630,
     "Medical: All illnesses, injuries, and medical conditions"),
    
    # CAR EVENTS: All car breakdown/repair events
    # Lines 27630-end
    ("story/car_events.py", "CarEventsMixin", 27630, total + 1,
     "Car events: All vehicle breakdown, repair, and consequence events"),
]

# Remove the economy entry that's too small, merge it into systems
# Actually let's keep it simple. Let me recalculate.

import os
os.makedirs("story", exist_ok=True)

# Write __init__.py for the story package
init_content = '''"""
story package - Player class split into mixin files.
Import Player from here.
"""
from story.player_core import Player
'''

with open("story/__init__.py", "w", encoding="utf-8") as f:
    f.write(init_content)

# Extract methods for each split
for output_file, class_name, start_line, end_line, docstring in splits:
    # Extract the lines (1-indexed to 0-indexed)
    chunk = lines[start_line - 1 : end_line - 1]
    
    content = mixin_header
    content += f'class {class_name}:\n'
    content += f'    """{docstring}"""\n\n'
    content += ''.join(chunk)
    content += '\n'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    line_count = len(chunk)
    print(f"Wrote {output_file}: {line_count} lines ({class_name})")

# Now write the core Player file that inherits from all mixins
# Core = lines 56-624 (class Player through has_cutting_tool / item effects)
core_chunk = lines[55:624]  # class Player: line through line 624

player_core = '''import random
import time
import sys
import lists
import typer
import msvcrt
from colorama import Fore, Back, Style, init
init(convert=True)

PAR = "\\n\\n"

"""
Below are all of the typing/color functions, used
for terminal outputs and making my text pretty
"""
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
    return ("\\"" + text)

def close_quote(text):
    return (text + "\\"")

def quote(text):
    return ("\\"" + text + "\\"")

def space_quote(text):
    return ("\\"" + text + "\\" ")

from story.systems import SystemsMixin
from story.economy import EconomyMixin
from story.day_cycle import DayCycleMixin
from story.events_day import DayEventsMixin
from story.mechanics_intro import MechanicsIntroMixin
from story.game_flow import GameFlowMixin
from story.locations import LocationsMixin
from story.durability import DurabilityMixin
from story.event_dispatch import EventDispatchMixin
from story.endings import EndingsMixin
from story.medical import MedicalMixin
from story.car_events import CarEventsMixin

'''

player_core += 'class Player(\n'
player_core += '    SystemsMixin,\n'
player_core += '    EconomyMixin,\n'
player_core += '    DayCycleMixin,\n'
player_core += '    DayEventsMixin,\n'
player_core += '    MechanicsIntroMixin,\n'
player_core += '    GameFlowMixin,\n'
player_core += '    LocationsMixin,\n'
player_core += '    DurabilityMixin,\n'
player_core += '    EventDispatchMixin,\n'
player_core += '    EndingsMixin,\n'
player_core += '    MedicalMixin,\n'
player_core += '    CarEventsMixin,\n'
player_core += '):\n'

# Now add the core methods (everything in lines 56-624)
# But we need to skip the "class Player:" line itself and the __slots__
# Actually, we need __init__ and all core accessors
player_core += ''.join(core_chunk)
player_core += '\n'

with open("story/player_core.py", "w", encoding="utf-8") as f:
    f.write(player_core)

print(f"\nWrote story/player_core.py: {len(core_chunk)} lines (core Player class)")
print("\nDone! Files created in story/ directory.")
print("\nNext steps:")
print("1. Update blackjackMain.py to import from story.player_core instead of story")
print("2. Test that everything works")
print("3. Delete the split_story.py script")
