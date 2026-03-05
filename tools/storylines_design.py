"""
STORYLINE SYSTEM DESIGN DOCUMENT
=================================

CURRENT SYSTEM ANALYSIS:
- __tom_dreams, __frank_dreams, __oswald_dreams track dream stages (0-3)
- __rabbit_chase tracks rabbit events (0-6)
- __prereqs[0] gates mechanic intros (balance >= 200)
- __prereqs_done[0] = True once you have Car
- Mechanic intros run in start_day() with random selection
- Multi-part events are in random pools - they skip if prereqs not met

THE PROBLEM:
If "chase_the_second_rabbit" is in a pool and you haven't done "chase_the_rabbit",
it gets skipped. You might never see it again until the pool refills.

THE SOLUTION:
Create a STORYLINE QUEUE that forces story events when they're ready.

=================================
NEW ARCHITECTURE
=================================

Add to Player.__init__:

    self.__storylines = {
        "mechanic_intros": {
            "stage": 0,  # 0=none met, 1=met 1, 2=met 2, 3=all met
            "triggered": False,  # Did the intro sequence start?
            "day_last_intro": 0,  # Pace out intros
        },
        "tom": {
            "stage": 0,  # 0=intro done, 1=dream1, 2=dream2, 3=dream3, 4=ready for ending
            "day_last_event": 0,
        },
        "frank": {
            "stage": 0,
            "day_last_event": 0,
        },
        "oswald": {
            "stage": 0,
            "day_last_event": 0,
        },
        "rabbit": {
            "stage": 0,  # 0-6 (you already have __rabbit_chase)
            "day_last_event": 0,
        },
        "suzy": {
            "stage": 0,  # 0=not met, 1=met, 2=in trouble, 3=resolved
            "day_last_event": 0,
        },
    }

=================================
STORYLINE EVENTS BY STAGE
=================================

MECHANIC INTROS (Day Events - happen in morning):
- Prerequisites: balance >= 200, don't have car yet
- Pacing: 1-2 days apart
- Events: trusty_tom(), filthy_frank(), optimal_oswald()
- These START the mechanic storylines

TOM'S ARC (Night Events - dreams):
- Stage 0→1: 3+ days after meeting Tom, 40% chance → dealer dream 1
- Stage 1→2: 3+ days after dream 1, 40% chance → dealer dream 2
- Stage 2→3: 3+ days after dream 2, 40% chance → dealer dream 3
- Stage 3 + $1M + car: goodbye_tom() → salvation() / resurrection()

FRANK'S ARC (Night Events - dreams):
- Same pacing as Tom
- Stage 0→1: dealers_anger_dream (you already have this)
- Stage 1→2: dealers_scar_dream
- Stage 2→3: dealers_revolver_dream  
- Stage 3 + $1M: goodbye_frank() → destruction() / retribution()

OSWALD'S ARC (Night Events - philosophical musings):
- Slightly slower pacing (4+ days, 30% chance)
- Stage 0→1: casino_bar_dream (Oswald contemplating meaning)
- Stage 1→2: casino_table_dream
- Stage 2→3: casino_riches_dream
- Stage 3 + $1M: goodbye_oswald() → transcendence() / eternity()

RABBIT CHASE (Night Events):
- Stage 0→1: chase_the_rabbit (random chance at night)
- Stage 1→2: 5+ days, 20% → chase_the_second_rabbit
- Stage 2→3: 5+ days, 20% → chase_the_third_rabbit
- Stage 3→4: 5+ days, 20% → chase_the_fourth_rabbit
- Stage 4→5: 5+ days, 20% → chase_the_fifth_rabbit
- Stage 5→6: 5+ days, 20% → chase_the_last_rabbit

SUZY'S ARC (Day Events - emotional):
- Can only start AFTER meeting Tom
- Stage 0→1: suzy_encounter (meet her at Tom's)
- Stage 1→2: 3+ days, random event where she's in trouble
- Stage 2→3: Resolution (save her or fail)

=================================
IMPLEMENTATION APPROACH
=================================

Option A: Replace current system entirely (risky, lots of refactoring)

Option B: ADD storyline checks without removing current system (safer)
    - In start_day(), before day_event():
        story = self.get_pending_story_event()
        if story:
            story()
            return
    - In night_event(), before random:
        story = self.get_pending_night_story()
        if story:
            story()
            return

Option C: Just REMOVE multi-part events from pools, track via existing vars
    - Remove chase_the_second_rabbit etc from pools
    - Add explicit checks: if rabbit_chase == 1 and days > X: run it
    - Simplest approach, least code change

RECOMMENDED: Option C
- Uses your existing __rabbit_chase, __tom_dreams, etc trackers
- Just need to:
  1. Remove multi-part events from lists.py pools
  2. Add checks in start_day() / night_event() for story progression
  3. Track "day of last story event" per storyline

=================================
EVENTS TO REMOVE FROM POOLS
=================================

From lists.py, remove these (they'll be triggered by storyline system):

RABBIT (currently in night events):
- chase_the_rabbit  ← Keep this one for random trigger to START the arc
- chase_the_second_rabbit  ← REMOVE
- chase_the_third_rabbit   ← REMOVE
- chase_the_fourth_rabbit  ← REMOVE
- chase_the_fifth_rabbit   ← REMOVE
- chase_the_last_rabbit    ← REMOVE

MECHANIC DREAMS (if they're in pools):
- Any Tom/Frank/Oswald dream events ← REMOVE if present

SUZY (if multi-part):
- suzy_encounter ← Keep for random start
- suzy_* followups ← REMOVE

=================================
MINIMAL CODE CHANGES
=================================

1. In Player.__init__, add:
    self.__rabbit_last_day = 0
    self.__tom_dream_last_day = 0
    self.__frank_dream_last_day = 0
    self.__oswald_dream_last_day = 0

2. In night_event() after sanity checks, before random:
    # Check for rabbit storyline progression
    if self.__rabbit_chase > 0 and self.__rabbit_chase < 6:
        days_since = self.__day - self.__rabbit_last_day
        if days_since >= 5 and random.random() < 0.2:
            self.run_rabbit_stage(self.__rabbit_chase)
            return
    
    # Check for mechanic dream progression
    story_dream = self.check_mechanic_dreams()
    if story_dream:
        story_dream()
        return
    
    # Normal random night event
    nightEvent = getattr(self, self.__lists.get_night_event())
    nightEvent()

3. Remove multi-part events from lists.py pools

This is the MINIMAL change to make storylines work properly.
"""
