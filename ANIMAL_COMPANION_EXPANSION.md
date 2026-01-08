# Animal Companion System Expansion Guide

## Changes Completed:
✅ **Achievements now display on ALL endings** (bliss, sanctuary, Frank paths, Oswald paths, madness ending)

## Remaining Work: Make ALL Animals Befriendable

### Current Companions (Already Implemented):
1. **Whiskers** - Alley Cat (stray_cat)
2. **Lucky** - Three-Legged Dog (three_legged_dog)
3. **Mr. Pecks** - Crow (crow_encounter)
4. **Patches** - Opossum (opossum_in_trash)
5. **Rusty** - Raccoon (raccoon_raid)
6. **Hopper** - Rabbit (garden_rabbit)
7. **Squirrely** - Squirrel (special companion, Bag of Acorns event)

### Animal Whistle System:
- **Item**: "Animal Whistle" (from Witch Doctor)
- **Effect**: Auto-befriends ANY animal encounter
- **Secret Ending**: With 5+ companions + Animal Whistle → Sanctuary ending

---

## Animals to Add as Companions

### DAY EVENTS:
1. **Estranged Dog** (line 2194 - estranged_dog)
   - Current: Just an encounter
   - Add: befriend option with Animal Whistle
   - Companion Type: "Stray Dog"
   - Name suggestion: "Buddy" or "Scout"

2. **Raccoon Raid** (line 3013 - raccoon_raid)
   - Current: Raccoon mafia encounter
   - Add: befriend the boss raccoon with Animal Whistle
   - Companion Type: "Raccoon Boss"
   - Name suggestion: "Don" or "Boss"

3. **Lucky Rabbit Encounter** (line 3545 - lucky_rabbit_encounter)
   - Current: Just observes you
   - Add: befriend with Animal Whistle + Carrot
   - Companion Type: "Lucky Rabbit"
   - Name suggestion: "Clover"

4. **Rat** (line 4371 - rat_bite)
   - Current: Bites you
   - Add: befriend the laughing rat with Animal Whistle
   - Companion Type: "Rat"
   - Name suggestion: "Slick" or "Nibbles"

5. **Crow (Day Events)** (line 2558)
   - Different from crow companion
   - Add: befriend pooping crow
   - Companion Type: "Sassy Crow"
   - Name suggestion: "Caw"

### NIGHT ADVENTURE EVENTS:

#### SWAMP ADVENTURES:
6. **Alligator** (swamp_swim line 6635+, swamp_adventure line 8183+)
   - Wrestle encounter or deep water encounter
   - Companion Type: "Swamp Gator"
   - Name: "Chomper" or "Snapper"

7. **Bullfrog** (swamp encounters mentioned multiple times)
   - Companion Type: "Bullfrog"
   - Name: "Croaker"

8. **Snake** (swamp_stroll line 6355+)
   - Encounter in swamp
   - Companion Type: "Water Moccasin"
   - Name: "Hiss" or "Scales"

9. **Turtle** (implied in swamp descriptions)
   - Companion Type: "Snapping Turtle"
   - Name: "Shell" or "Snap"

10. **Swamp Frog Racer** (swamp_adventure ~line 8254)
    - The frog racing event
    - Companion Type: "Racing Frog"
    - Name: "Speedster" or "Jumper"

#### BEACH ADVENTURES:
11. **Seagull** (beach events)
    - Companion Type: "Seagull"
    - Name: "Squawk" or "Sandy"

12. **Crab** (beach_stroll line 6798+)
    - Companion Type: "Hermit Crab"
    - Name: "Pinchy" or "Shell"

13. **Dolphin** (beach_dive line 7039+)
    - Deep water encounter
    - Companion Type: "Dolphin"
    - Name: "Splash" or "Flipper"

14. **Seal** (beach encounters)
    - Companion Type: "Harbor Seal"
    - Name: "Whiskers" (different from cat) or "Blubbery"

15. **Pelican** (beach encounters)
    - Companion Type: "Pelican"
    - Name: "Pelly" or "Scoops"

16. **Fish** (various fishing events)
    - Companion Type: "Lucky Fish"
    - Name: "Finn" or "Bubbles"

17. **Octopus** (underwater events)
    - Companion Type: "Octopus"
    - Name: "Eight" or "Inky"

18. **Starfish** (beach collections)
    - Companion Type: "Starfish"
    - Name: "Star" or "Patrick"

#### FOREST ADVENTURES:
19. **Deer** (forest encounters, night_event ~line 7808+)
    - Companion Type: "Forest Deer"
    - Name: "Buck" or "Doe"

20. **Owl** (forest night events line 7808)
    - Three hoots mentioned
    - Companion Type: "Wise Owl"
    - Name: "Hoot" or "Professor"

21. **Wolf** (forest encounters line 8049)
    - The test animal
    - Companion Type: "Lone Wolf"
    - Name: "Shadow" or "Fang"

22. **Bear** (forest events)
    - Companion Type: "Black Bear"
    - Name: "Bruno" or "Berr"

23. **Fox** (forest encounters)
    - Companion Type: "Red Fox"
    - Name: "Sly" or "Russet"

24. **Squirrel** (different from Squirrely)
    - Forest squirrel encounters
    - Companion Type: "Forest Squirrel"
    - Name: "Nutkin" or "Scurry"

25. **Chipmunk** (forest events)
    - Companion Type: "Chipmunk"
    - Name: "Chip" or "Alvin"

26. **Skunk** (forest encounters)
    - Companion Type: "Skunk"
    - Name: "Stripe" or "Stinky"

27. **Porcupine** (forest events)
    - Companion Type: "Porcupine"
    - Name: "Quill" or "Spike"

28. **Bat** (night forest events)
    - Companion Type: "Fruit Bat"
    - Name: "Flutter" or "Sonar"

29. **Moth** (night events with lights)
    - Companion Type: "Luna Moth"
    - Name: "Luna" or "Glow"

#### MOUNTAIN/OTHER ADVENTURES:
30. **Mountain Goat** (if mountain adventures exist)
    - Companion Type: "Mountain Goat"
    - Name: "Billy" or "Cliff"

31. **Eagle** (mountain/sky events)
    - Companion Type: "Bald Eagle"
    - Name: "Freedom" or "Talon"

32. **Hawk** (day hunting events)
    - Companion Type: "Red-Tailed Hawk"
    - Name: "Hunter" or "Sharp-Eye"

33. **Vulture** (desert/death events)
    - Companion Type: "Vulture"
    - Name: "Mort" or "Carrion"

34. **Armadillo** (if southwestern events)
    - Companion Type: "Armadillo"
    - Name: "Armor" or "Dillo"

35. **Groundhog** (spring events if any)
    - Companion Type: "Groundhog"
    - Name: "Phil" or "Shadow"

---

## Implementation Steps:

### 1. Update each animal encounter function:

```python
def example_animal_encounter(self):
    # ... existing encounter logic ...
    
    # Animal Whistle auto-befriend
    if self.has_item("Animal Whistle"):
        type.type("The " + magenta(bright("Animal Whistle")) + " hums softly.")
        print()
        type.type("The animal's eyes soften. It approaches you cautiously, then nuzzles your hand.")
        print()
        self.add_companion("Name", "Type")
        return
    
    # Regular encounter options
    type.type("Would you like to try befriending it?")
    # ... rest of encounter ...
```

### 2. Add afternoon companion interactions:

In the `afternoon()` function, add a section that lets you interact with each companion:

```python
# COMPANION INTERACTION MENU
living_companions = self.get_all_companions()
if len(living_companions) > 0:
    type.type("Your companions:")
    for i, (name, data) in enumerate(living_companions.items()):
        type.type(f"{i+1}. {name} the {data['type']}")
    type.type(f"{len(living_companions)+1}. Skip")
    
    choice = ask.option(f"Interact with a companion? ", 1, len(living_companions)+1)
    if choice <= len(living_companions):
        selected = list(living_companions.keys())[choice-1]
        self.companion_afternoon_dialogue(selected)
```

### 3. Create companion afternoon dialogue:

```python
def companion_afternoon_dialogue(self, name):
    """Unique afternoon dialogue for each companion"""
    companion = self.get_companion(name)
    comp_type = companion["type"]
    
    if comp_type == "Alley Cat":
        type.type(f"{name} purrs and rubs against your leg.")
        # ... unique interactions ...
    elif comp_type == "Three-Legged Dog":
        type.type(f"{name} wags his tail excitedly, hopping on three legs.")
        # ... unique interactions ...
    # ... etc for ALL 35+ animals ...
```

### 4. Add companion-specific endings:

Each companion type should have unique dialogue in:
- `bliss()` ending
- `sanctuary()` ending  
- Mechanic endings (Tom/Frank/Oswald)

Example:
```python
if self.has_companion("Chomper"):  # Alligator
    type.slow("Chomper splashes in the river, finally free in clean water.")
```

### 5. Achievement additions:

Add achievements for collecting specific animal types:
- "Zookeeper" - 10 companions
- "Noah's Ark" - 20 companions
- "Disney Princess" - All forest animals
- "Marine Biologist" - All beach/water animals
- "Swamp Lord" - All swamp animals
- "Pack Leader" - All canines
- "Bird Watcher" - All birds
- "Rodent King" - All rodents

---

## Search Terms for Finding Animals:

```bash
# In story.py, search for these patterns:
- "animal"
- "creature"
- specific animal names (dog, cat, crow, etc.)
- "befriend"
- "Wildlife"
- "forest"
- "swamp"
- "beach"
- "underwater"
- "bird"
- "fish"
- Adventure event functions
```

---

## Notes:
- The Animal Whistle should be the UNIVERSAL befriending tool
- Each companion needs: unique name, type, happiness system, feeding requirements
- Companions should comment on major story events
- Some companions might have conflicts (cat vs rat, crow vs owl, etc.)
- Consider "family dynamics" where certain companion combinations trigger special dialogue
- Dead companions should be memorialized in endings

---

## File Locations:
- Main companion system: story.py lines 1621-1760
- Afternoon function: story.py line 17388+
- Endings: story.py lines 22000-24200
- Achievements: story.py lines 1300-1520
- Animal encounters: Scattered throughout story.py (search by event name)
