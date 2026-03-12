"""
STORYLINE SYSTEM
================
Manages sequential multi-part story events that are separate from rank-based random pools.
These events fire during the day, before or instead of random events, with escalating probability.

Storylines are DAY EVENTS ONLY. Night events remain fully random + rabbit chase.

DESIGN PHILOSOPHY:
- Storyline events feel random but are guaranteed to eventually fire
- Minimum day gaps prevent story beats from stacking
- Escalating probability means you WILL see the next stage, just not exactly when
- Multiple storylines can be active simultaneously
- Only ONE storyline event fires per day (picked randomly from eligible ones)
- If no storyline fires, normal rank-based random event plays

CATEGORIES:
1. NARRATIVE ARCS - Multi-part NPC stories with choices and consequences
2. UNLOCK EVENTS - One-shot events that unlock shops/features
3. CONDITION ARCS - Multi-part events triggered by player state (addiction, etc.)

EVENT METHODS:
- All storyline events are standalone functions in this file
- They take (player, storyline_system) as arguments
- The system wraps them into lambdas when dispatching
"""

import random
import typer

type = typer.Type()
ask = typer.Ask()

from colorama import Fore, Style

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
def quote(text):
    return ("\"" + text + "\"")
def space_quote(text):
    return ("\"" + text + "\" ")
def open_quote(text=""):
    return ("\"" + text)
def close_quote(text=""):
    return (text + "\"")


class StorylineSystem:
    """
    Manages all storyline progression for the Player.
    Injected into Player at init. Checks each day for eligible storyline events.
    """

    def __init__(self, player):
        self.player = player
        
        # ==========================================
        # STORYLINE DEFINITIONS
        # ==========================================
        # Each storyline has:
        #   "stage": current stage (0 = not started)
        #   "day_started": day the current stage was set (for min gap)
        #   "completed": True when all stages done
        #   "failed": True if storyline was failed/abandoned
        #   "min_gap": minimum days between stages
        #   "base_chance": starting probability after min_gap
        #   "escalation": added to chance each day past min_gap
        #   "stages": list of (method_name, condition_func) tuples
        #   "max_stage": total number of stages
        
        self.storylines = {
            
            # ==========================================
            # EXISTING ARCS (promoted from rank pools)
            # ==========================================
            
            "suzy": {
                "stage": 0,  # 0=name known (color ready), 1=color answered, 2=animal answered, 3=complete
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 3,
                "base_chance": 0.15,
                "escalation": 0.10,
            },
            
            "phil": {
                "stage": 0,  # 0=not started, 1=interrogation, 2=further, 3=even_further, 4=final
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 4,
                "base_chance": 0.12,
                "escalation": 0.08,
            },
            
            "victoria": {
                "stage": 0,  # 0=not started, 1=the_rival, 2=victoria_returns
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 5,
                "base_chance": 0.15,
                "escalation": 0.10,
            },
            
            "betsy": {
                "stage": 0,  # 0=not started, 1=hungry_cow, 2=starving_cow, 3=cow_army
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 5,
                "base_chance": 0.10,
                "escalation": 0.08,
            },
            
            "stray_cat": {
                "stage": 0,  # 0=not met, 1=befriended, 2=sick, 3=resolved (dies or kittens)
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 3,
                "base_chance": 0.15,
                "escalation": 0.10,
            },
            
            "bridge_angel": {
                "stage": 0,  # 0=not started, 1=contemplation, 2=angel_returns, 3=call
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 4,
                "base_chance": 0.12,
                "escalation": 0.08,
            },
            
            "gas_station_hero": {
                "stage": 0,  # 0=not started, 1=robbery, 2=recognized, 3=interview, 4=media consequences
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 3,
                "base_chance": 0.15,
                "escalation": 0.10,
            },
            
            "painkiller": {
                "stage": 0,  # 0=not started, 1=chronic_pain, 2=addiction, 3=withdrawal/dealer/overdose
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 2,
                "base_chance": 0.20,
                "escalation": 0.12,
            },
            
            "collector": {
                "stage": 0,  # 0=not met, 1=intro, 2=small_favor, 3=payment, 4=real_offer
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 5,
                "base_chance": 0.10,
                "escalation": 0.08,
            },
            
            "mechanic_dreams": {
                "stage": 0,  # tracks overall dream progression (shared across Tom/Frank/Oswald)
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 3,
                "base_chance": 0.15,
                "escalation": 0.10,
            },
            
            # ==========================================
            # UNLOCK EVENTS (one-shot storylines)
            # ==========================================
            
            "grimy_gus": {
                "stage": 0,  # 0=not met, 1=discovered (done)
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 0,
                "base_chance": 0.15,
                "escalation": 0.10,
                "force_start_day": 9,  # Gus should surface in the early car-and-collectible game
            },

            "vinnie": {
                "stage": 0,  # 0=not met, 1=discovered (done)
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 0,
                "base_chance": 0.15,
                "escalation": 0.10,
                "force_start_day": 8,  # Vinnie should show up before low-bankroll car runs stall out
            },

            "marvin": {
                "stage": 0,  # 0=not unlocked, 1=map acquired (done)
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 0,
                "base_chance": 0.15,
                "escalation": 0.10,
                "force_start_day": 7,  # Marvin should become reachable before rank-2 runs flatten out
            },

            "witch": {
                "stage": 0,  # 0=not met, 1=introduced (done)
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 0,
                "base_chance": 0.12,
                "escalation": 0.08,
                "force_start_day": 10,  # The Witch should surface once the run has started taking damage
            },
            
            "mechanics": {
                "stage": 0,  # 0-2 = one mechanic intro per stage (random order); 3 = all introduced
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 2,
                "base_chance": 0.40,
                "escalation": 0.15,
                "force_start_day": 5,  # First mechanic shows up by day 5
            },
            
            # ==========================================
            # NEW NARRATIVE ARCS
            # ==========================================
            
            "kyle": {
                "stage": 0,  # 0=not started, 1=just_another_customer, 2=kyles_problem, 3=after_hours, 4=kyles_secret, 5=finale
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 3,
                "base_chance": 0.15,
                "escalation": 0.10,
            },
            
            "martinez": {
                "stage": 0,  # 0=not started, 1=license, 2=wellness, 3=favor, 4=resolution
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 4,
                "base_chance": 0.12,
                "escalation": 0.08,
            },
            
            "dr_feelgood": {
                "stage": 0,  # 0=not started, 1=first_pill, 2=feeling_better, 3=price_up, 4=rock_bottom, 5=resolution
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 2,
                "base_chance": 0.20,
                "escalation": 0.12,
            },
            
            "mime": {
                "stage": 0,  # 0=not started, 1=performance, 2=encore, 3=message, 4=behind_paint, 5=final_act
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 5,
                "base_chance": 0.10,
                "escalation": 0.08,
                "force_start_day": 12,  # The mime performs by day 12
            },
            
            "jameson": {
                "stage": 0,  # 0=not met, 1=carrot, 2=horse_trouble, 3=rustlers, 4=one_last_ride
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 5,
                "base_chance": 0.12,
                "escalation": 0.08,
                "force_start_day": 10,  # The lone cowboy rides through by day 10
            },
            
            "stuart": {
                "stage": 0,  # 0=not started, 1=side_hustle, 2=good_deal, 3=bad_deal, 4=oswald_finds_out
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 4,
                "base_chance": 0.12,
                "escalation": 0.08,
            },
            
            "grandma": {
                "stage": 0,  # 0=not started, 1=first_call, 2=recipe, 3=bad_news, 4=gift, 5=last_call
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 4,
                "base_chance": 0.12,
                "escalation": 0.08,
            },
            
            "lucky_dog": {
                "stage": 0,  # 0=not started, 1=befriended, 2=who_hurt_you, 3=previous_owner, 4=good_boy, 5=saves_your_life
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 3,
                "base_chance": 0.15,
                "escalation": 0.10,
            },
            
            "dealer_past": {
                "stage": 0,  # 0=not started, 1=photo, 2=journal, 3=question, 4=answer, 5=choice
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 5,
                "base_chance": 0.10,
                "escalation": 0.06,
            },
            
            "sleep_paralysis": {
                "stage": 0,  # 0=not started, 1=cant_move, 2=it_speaks, 3=the_offer, 4=resolution
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 4,
                "base_chance": 0.12,
                "escalation": 0.08,
            },
            
            "radio_signal": {
                "stage": 0,  # 0=not started, 1=static, 2=broadcast, 3=source, 4=whos_watching
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 4,
                "base_chance": 0.12,
                "escalation": 0.08,
            },
            
            "graveyard": {
                "stage": 0,  # 0=not started, 1=wandering, 2=digger, 3=your_plot, 4=edgars_request
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 5,
                "base_chance": 0.10,
                "escalation": 0.08,
            },
            
            "carnival": {
                "stage": 0,  # 0=not started, 1=lights, 2=fortune_teller, 3=the_game, 4=pack_up
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 1,  # Carnival is a limited-time event, fast pacing
                "base_chance": 0.40,
                "escalation": 0.25,
            },
            
            "lockbox": {
                "stage": 0,  # 0=not started, 1=the_box, 2=key_hunt, 3=who_left_it
                "day_started": 0,
                "completed": False,
                "failed": False,
                "min_gap": 3,
                "base_chance": 0.15,
                "escalation": 0.10,
            },
        }
    
    # ==========================================
    # CORE SYSTEM METHODS
    # ==========================================
    
    def check_for_storyline_event(self):
        """
        Called once per day in start_day(), before the random event pool.
        Returns a callable if a storyline event should fire, else None.
        Only ONE storyline event per day.

        Stage-0 start conditions live inline inside _get_stage_event() — returning
        None means "not ready yet." Pool arcs (whose intro events are existing Player
        methods that don't call sl.advance()) receive an auto-advance 0→1 after firing.
        Standalone-function arcs advance themselves via sl.advance() inside the event.
        """
        # Pool arcs: intro events are plain Player methods with no sl.advance() inside.
        # Must be auto-advanced to stage 1 after firing so follow-up stages can unlock.
        _POOL_ARCS = frozenset({
            "stray_cat", "jameson", "phil", "mime", "betsy",
            "gas_station_hero", "collector", "victoria", "grimy_gus", "vinnie", "marvin", "witch",
        })
        _SINGLE_SHOT_ARCS = frozenset({"collector", "grimy_gus", "vinnie", "marvin", "witch"})

        def _mark_started(name):
            sl = self.storylines[name]
            sl["stage"] = 1
            sl["day_started"] = day

        def _unlock_priority(name):
            p = self.player
            priorities = [
                ("mechanics", not p.has_item("Car")),
                ("marvin", not (p.has_item("Map") or p.has_item("Worn Map"))),
                ("witch", not p.has_met("Witch")),
                ("grimy_gus", not p.has_met("Grimy Gus")),
                ("vinnie", not p.has_met("Vinnie") and p.get_loan_shark_debt() <= 0),
            ]
            for index, (priority_name, needed) in enumerate(priorities):
                if name == priority_name and needed:
                    return index
            return None

        def _finalize_event(name, event):
            if name not in _SINGLE_SHOT_ARCS:
                return event

            def _run_once():
                event()
                sl = self.storylines[name]
                sl["stage"] = max(sl["stage"], 1)
                sl["day_started"] = self.player.get_day()
                if name == "collector" and self.player.has_met("The Collector"):
                    sl["completed"] = True
                elif name == "grimy_gus" and self.player.has_met("Grimy Gus"):
                    sl["completed"] = True
                elif name == "vinnie" and (
                    self.player.has_met("Vinnie") or self.player.get_loan_shark_debt() > 0
                ):
                    sl["completed"] = True
                elif name == "marvin" and (
                    self.player.has_item("Map") or self.player.has_item("Worn Map")
                ):
                    sl["completed"] = True
                elif name == "witch" and self.player.has_met("Witch"):
                    sl["completed"] = True

            return _run_once

        # Sync arcs whose stage-0 events may have fired via the random pool
        self._sync_pool_triggered_arcs()
        day = self.player.get_day()

        # ── Phase 1: Forced introductions ──────────────────────────────────────
        # Stage-0 arcs past their force_start_day take priority over the pool.
        # Conditions are embedded in _get_stage_event(); None = still not ready.
        forced = {}
        for name, sl in self.storylines.items():
            if sl["completed"] or sl["failed"] or sl["stage"] != 0:
                continue
            if day >= sl.get("force_start_day", 9999):
                event = self._get_stage_event(name)
                if event is not None:
                    forced[name] = event

        if forced:
            unlock_forced = [(priority, name) for name in forced if (priority := _unlock_priority(name)) is not None]
            if unlock_forced:
                chosen = min(unlock_forced)[1]
            else:
                chosen = random.choice(list(forced.keys()))
            event = forced[chosen]
            if chosen in _POOL_ARCS:
                _mark_started(chosen)
            return _finalize_event(chosen, event)

        # Keep car progression moving once the mechanics arc has started.
        mechanics = self.storylines.get("mechanics")
        if (
            mechanics is not None
            and not self.player.has_item("Car")
            and not mechanics["completed"]
            and not mechanics["failed"]
            and mechanics["stage"] > 0
        ):
            days_since = day - mechanics["day_started"]
            if days_since >= mechanics["min_gap"] and self._stage_conditions_met("mechanics"):
                event = self._get_stage_event("mechanics")
                if event is not None:
                    return event

        # ── Phase 2: Normal eligible check ─────────────────────────────────────
        eligible = {}
        for name, sl in self.storylines.items():
            if sl["completed"] or sl["failed"]:
                continue

            if sl["stage"] == 0:
                # Inline conditions in _get_stage_event() decide eligibility
                event = self._get_stage_event(name)
                if event is not None:
                    eligible[name] = event
                continue

            # Stage > 0: check day gap, stage conditions, escalating probability
            days_since = day - sl["day_started"]
            if days_since < sl["min_gap"]:
                continue
            if not self._stage_conditions_met(name):
                continue
            days_past_gap = days_since - sl["min_gap"]
            chance = sl["base_chance"] + (sl["escalation"] * days_past_gap)
            chance = min(chance, 0.95)
            if random.random() < chance:
                event = self._get_stage_event(name)
                if event is not None:
                    eligible[name] = event

        if not eligible:
            return None

        unlock_eligible = [(priority, name) for name in eligible if (priority := _unlock_priority(name)) is not None]
        if unlock_eligible:
            chosen = min(unlock_eligible)[1]
        else:
            chosen = random.choice(list(eligible.keys()))
        event = eligible[chosen]
        sl = self.storylines[chosen]
        # Auto-advance pool arcs (their intro events don't call sl.advance)
        if sl["stage"] == 0 and chosen in _POOL_ARCS:
            _mark_started(chosen)
        return _finalize_event(chosen, event)

    def _sync_pool_triggered_arcs(self):
        """
        Advance stage-0 storylines whose intro event already fired via the random pool.
        Called at the start of each day's storyline check to keep stage in sync with
        the old has_met tracking system. Without this, arcs could double-fire.
        """
        p = self.player
        single_shot_arcs = {"collector", "grimy_gus", "vinnie", "marvin", "witch"}
        self._sync_phil_storyline_state()
        self._sync_betsy_storyline_state()
        syncs = [
            ("stray_cat",        lambda: p.has_met("Stray Cat Fed")),
            ("jameson",          lambda: p.has_met("Cowboy")),
            ("mime",             lambda: p.has_met("Mime")),
            ("betsy",            lambda: p.has_met("Betsy")),
            ("gas_station_hero", lambda: p.has_met("Gas Station Hero")),
            ("collector",        lambda: p.has_met("The Collector")),
            ("victoria",         lambda: p.has_met("The Rival")),
            ("grimy_gus",        lambda: p.has_met("Grimy Gus")),
            ("vinnie",           lambda: p.has_met("Vinnie") or p.get_loan_shark_debt() > 0),
            ("marvin",           lambda: p.has_item("Map") or p.has_item("Worn Map")),
            ("witch",            lambda: p.has_met("Witch")),
        ]
        for name, met_fn in syncs:
            sl = self.storylines.get(name)
            if sl and sl["stage"] == 0 and not sl["completed"] and not sl["failed"] and met_fn():
                sl["stage"] = 1
                sl["day_started"] = p.get_day()
                if name in single_shot_arcs:
                    sl["completed"] = True

    def _sync_betsy_storyline_state(self):
        """
        Advance the betsy arc past stages whose gate-danger has been consumed.

        Neither hungry_cow nor starving_cow call sl.advance() themselves, so the
        stage stays at 1 forever once starving_cow fires (removing "Betsy Tractor").
        Calling this each day auto-advances based on which Betsy danger is active:

          stage 1 → 2  : starving_cow has already fired (Betsy Tractor gone, Betsy Army set)
          stage 2 → 3+ : cow_army has already fired    (Betsy Army gone)
        """
        p = self.player
        sl = self.storylines.get("betsy")
        if sl is None or sl["completed"] or sl["failed"]:
            return
        if not p.has_met("Betsy"):
            return

        day = p.get_day()
        if sl["stage"] == 1 and not p.has_danger("Betsy Tractor") and p.has_danger("Betsy Army"):
            # starving_cow has fired (it removes "Betsy Tractor" AND adds "Betsy Army").
            # Both conditions confirm starving_cow completed, not just that the danger vanished.
            # Advance to stage 2 so cow_army can fire when "Betsy Army" danger is present.
            sl["stage"] = 2
            sl["day_started"] = day
        elif sl["stage"] == 2 and not p.has_danger("Betsy Army"):
            # cow_army has fired (it removes "Betsy Army" at the top of the event).
            # Betsy arc is complete — all three stages done.
            sl["completed"] = True

    def _sync_phil_storyline_state(self):
        p = self.player
        sl = self.storylines.get("phil")
        if sl is None or sl["failed"]:
            return

        if not p.has_met("Interrogator"):
            return

        completed = False
        if p.has_danger("Final Interrogation"):
            stage = 3
        elif p.has_danger("Even Further Interrogation"):
            stage = 2
        elif p.has_danger("Further Interrogation"):
            stage = 1
        else:
            stage = 4
            completed = True

        if stage > sl["stage"]:
            sl["stage"] = stage
            sl["day_started"] = p.get_day()

        if completed:
            sl["completed"] = True

    def advance(self, name):
        """Advance a storyline to the next stage. Call from within event methods."""
        sl = self.storylines[name]
        sl["stage"] += 1
        sl["day_started"] = self.player.get_day()
    
    def complete(self, name):
        """Mark a storyline as completed."""
        self.storylines[name]["completed"] = True
    
    def fail(self, name):
        """Mark a storyline as failed (can't continue)."""
        self.storylines[name]["failed"] = True
    
    def get_stage(self, name):
        """Get current stage of a storyline."""
        return self.storylines[name]["stage"]
    
    def is_active(self, name):
        """Check if a storyline has started but isn't complete."""
        sl = self.storylines[name]
        return sl["stage"] > 0 and not sl["completed"] and not sl["failed"]
    
    def set_stage(self, name, stage):
        """Force a storyline to a specific stage (for migration from old system)."""
        self.storylines[name]["stage"] = stage
        self.storylines[name]["day_started"] = self.player.get_day()
    
    # ==========================================
    # STAGE CONDITIONS
    # ==========================================
    
    def _stage_conditions_met(self, name):
        """Check if conditions are met for the NEXT stage of an active storyline."""
        p = self.player
        sl = self.storylines[name]
        stage = sl["stage"]
        
        match name:
            case "suzy":
                if stage == 1:  # Color answered, animal question next
                    return p.get_favorite_color() is not None and p.get_favorite_animal() is None
                elif stage == 2:  # Animal answered, finale next
                    return p.get_favorite_animal() is not None and not p.has_met("Suzy Finale")
                return True
            
            case "mechanics":
                # Complete once all three mechanics have been introduced
                all_met = p.has_met("Tom Event") and p.has_met("Frank Event") and p.has_met("Oswald Event")
                if all_met:
                    self.complete("mechanics")
                    return False
                return True
            
            case "phil":
                return True  # Phil just needs day gap
            
            case "victoria":
                return True
            
            case "betsy":
                # Gate each stage on the presence of the danger set by the previous event.
                # This prevents re-triggering after the danger has been consumed.
                if stage == 1:
                    return p.has_danger("Betsy Tractor")  # hungry_cow sets this
                if stage == 2:
                    return p.has_danger("Betsy Army")     # starving_cow sets this
                return True
            
            case "stray_cat":
                if stage == 1:  # Cat needs to have been fed
                    return p.has_met("Stray Cat Fed")
                return True
            
            case "bridge_angel":
                if stage == 1:
                    return p.has_met("Bridge Angel Saved")
                return True
            
            case "gas_station_hero":
                if stage >= 1:
                    return p.has_met("Gas Station Hero")
                return True
            
            case "painkiller":
                if stage >= 2:
                    return p.has_danger("Painkiller Dependency")
                return True
            
            case "collector":
                return True
            
            case "mechanic_dreams":
                # Dreams progress based on existing counters
                return True
            
            case "kyle":
                return True
            
            case "martinez":
                return True
            
            case "dr_feelgood":
                return True
            
            case "mime":
                return True
            
            case "jameson":
                if stage == 2:  # Horse trouble needs Thunder companion
                    return p.has_companion("Thunder")
                return True
            
            case "stuart":
                return True
            
            case "grandma":
                return p.has_item("Grandma's Number")
            
            case "lucky_dog":
                return p.has_companion("Lucky")
            
            case "dealer_past":
                return True
            
            case "sleep_paralysis":
                return True
            
            case "radio_signal":
                return True
            
            case "graveyard":
                return True
            
            case "carnival":
                return True  # Carnival stages are fast (min_gap=1)
            
            case "lockbox":
                return True
        
        return True
    
    # ==========================================
    # STAGE → EVENT MAPPING
    # ==========================================
    
    def _get_stage_event(self, name):
        """
        Return a callable for the current stage of a storyline, or None if
        start conditions are not met (stage 0) or no event is defined.

        Stage-0 cases embed their own start conditions inline here — this is the
        single source of truth for when each arc can begin.
          - Pool arcs  → return getattr(p, method_name)  (existing Player method)
          - Standalone → return _wrap(function)           (function defined in this file)
        """
        p = self.player
        day = p.get_day()
        stage = self.storylines[name]["stage"]
        sl_sys = self

        def _wrap(func):
            return lambda: func(p, sl_sys)

        match name:

            # ── Pool arcs: stage-0 event is an existing Player method ──────────
            # These events can also fire randomly from the day pool (lists.py).
            # _sync_pool_triggered_arcs() advances the stage when the pool fires first.

            case "phil":
                # Stage 0: Phil starts investigating you a few days in
                if stage == 0:
                    if p.has_met("Interrogator") or day < 3 or random.random() > 0.12:
                        return None
                events = ["interrogation", "further_interrogation", "even_further_interrogation", "final_interrogation"]
                if stage < len(events):
                    return getattr(p, events[stage])

            case "victoria":
                # Stage 0: Victoria confronts you once you're succeeding ($50k+, day 10+)
                if stage == 0:
                    if p.has_met("The Rival") or p.get_balance() < 50000 or day < 10:
                        return None
                events = ["the_rival", "victoria_returns"]
                if stage < len(events):
                    return getattr(p, events[stage])

            case "betsy":
                # Stage 0: A stray cow wanders into your life.
                # hungry_cow ($100/round) = rank-1 affordable; but starving_cow ($10k/round) fires
                # as stage-1 and can hit a player who is still at rank 1.  Raising to rank >= 2
                # keeps the $10k demand inside the tier where it is actually affordable, and is
                # still consistent with the pool-event placement (hungry_cow appears in cheap-tier
                # but starving_cow appears in modest-tier / rank 2+).
                if stage == 0:
                    if p.has_met("Betsy") or day < 5 or p.get_rank() < 2 or random.random() > 0.10:
                        return None
                events = ["hungry_cow", "starving_cow", "cow_army"]
                if stage < len(events):
                    return getattr(p, events[stage])

            case "stray_cat":
                # Stage 0: A stray cat appears at your car after day 2
                if stage == 0:
                    if p.has_met("Stray Cat Fed") or day < 2 or random.random() > 0.15:
                        return None
                events = ["stray_cat", "stray_cat_sick"]
                if stage < len(events):
                    return getattr(p, events[stage])

            case "bridge_angel":
                # Stage 0: Despair brings you to the bridge (low health or sanity)
                if stage == 0:
                    if day < 7 or (p.get_health() >= 30 and p.get_sanity() >= 40):
                        return None
                events = ["bridge_contemplation", "bridge_angel_returns", "call_bridge_angel"]
                if stage < len(events):
                    return getattr(p, events[stage])

            case "gas_station_hero":
                # Stage 0: You witness a robbery once you've been around town a bit.
                if stage == 0:
                    if p.has_met("Gas Station Hero") or day < 5:
                        return None
                events = ["gas_station_robbery", "gas_station_hero_recognized", "gas_station_hero_interview"]
                if stage < len(events):
                    return getattr(p, events[stage])

            case "painkiller":
                # Stage 0: Chronic pain sets in once the shoulder is destroyed
                if stage == 0:
                    if not p.has_danger("Shoulder Destroyed"):
                        return None
                events = ["shoulder_chronic_pain", "shoulder_painkiller_addiction"]
                if stage < len(events):
                    return getattr(p, events[stage])

            case "collector":
                # Stage 0: The Collector finds you once you have real money ($100k+)
                if stage == 0:
                    if p.has_met("The Collector") or p.get_balance() < 100000 or day < 15:
                        return None
                events = ["the_collector"]
                if stage < len(events):
                    return getattr(p, events[stage])

            case "grimy_gus":
                # Stage 0: Gus can surface early even before the run is established.
                if stage == 0:
                    if not p.has_item("Car") or p.has_met("Grimy Gus") or day < 4:
                        return None
                    return getattr(p, "grimy_gus_discovery")

            case "vinnie":
                # Stage 0: Vinnie should become available early, not only in stalled runs.
                if stage == 0:
                    if not p.has_item("Car") or p.has_met("Vinnie") or p.get_loan_shark_debt() > 0 or day < 4:
                        return None
                    return getattr(p, "vinnie_referral_card")

            case "marvin":
                # Stage 0: unlock Marvin routes early; the harness decides when to shop.
                if stage == 0:
                    if not p.has_item("Car") or p.has_item("Map") or p.has_item("Worn Map") or day < 3:
                        return None

                    candidates = []
                    if day >= 3 and not p.has_met("Windblown Worn Map"):
                        candidates.append(getattr(p, "windblown_worn_map"))
                    if day >= 4 and not p.has_met("Flea Market Route Map"):
                        candidates.append(getattr(p, "flea_market_route_map"))
                    if day >= 7 and not p.has_met("Laundromat Bulletin Map"):
                        candidates.append(getattr(p, "laundromat_bulletin_map"))
                    if not candidates:
                        return None
                    return random.choice(candidates)

            case "witch":
                # Stage 0: introduce the Witch through daylight breadcrumbs before swamp content.
                if stage == 0:
                    if not p.has_item("Car") or p.has_met("Witch") or day < 6:
                        return None

                    candidates = []
                    if day >= 8 and not p.has_met("Witch Doctor Matchbook"):
                        candidates.append(getattr(p, "witch_doctor_matchbook"))
                    if day >= 12 and not p.has_met("Roadside Bone Chimes"):
                        candidates.append(getattr(p, "roadside_bone_chimes"))
                    if not candidates:
                        return None
                    return random.choice(candidates)

            case "mime":
                # Stage 0: A silent performer materializes after a few days
                if stage == 0:
                    if p.has_met("Mime") or day < 3 or random.random() > 0.08:
                        return None
                    return getattr(p, "the_mime")
                mime_events = [None, _wrap(storyline_mime_encore), _wrap(storyline_mime_message),
                              _wrap(storyline_mime_behind_paint), _wrap(storyline_mime_final_act)]
                if stage < len(mime_events) and mime_events[stage] is not None:
                    return mime_events[stage]

            case "jameson":
                # Stage 0: A lone cowboy rides through early game
                if stage == 0:
                    if p.has_met("Cowboy") or day < 2 or random.random() > 0.10:
                        return None
                    return getattr(p, "lone_cowboy")
                jameson_events = [None, _wrap(storyline_jameson_horse_trouble),
                                 _wrap(storyline_jameson_rustlers), _wrap(storyline_jameson_last_ride)]
                if stage < len(jameson_events) and jameson_events[stage] is not None:
                    return jameson_events[stage]

            # ── Mechanics intro arc ────────────────────────────────────────────

            case "mechanics":
                balance = p.get_balance()
                if balance < 200:
                    return None
                # Build a pool of eligible mechanics that haven't been introduced yet.
                # All eligible candidates get equal probability — the order is random,
                # not fixed (Tom → Frank → Oswald).
                available = []
                if not p.has_met("Tom Event"):
                    available.append(_wrap(storyline_mechanics_intro_tom))
                # Frank only drives out when the player has no car yet
                if not p.has_item("Car") and not p.has_met("Frank Event"):
                    available.append(_wrap(storyline_mechanics_intro_frank))
                # Oswald has no car requirement — he can visit even after the car is bought
                if not p.has_met("Oswald Event") and balance >= 850:
                    available.append(_wrap(storyline_mechanics_intro_oswald))
                if not available:
                    return None
                return random.choice(available)

            # ── Suzy arc ──────────────────────────────────────────────────────

            case "suzy":
                # Stage 0: Color question — fires once your name is known (from whats_my_name)
                if stage == 0:
                    if p.get_name() is None or p.has_met("Suzy Color"):
                        return None
                    return _wrap(storyline_suzy_color)
                elif stage == 1:
                    return _wrap(storyline_suzy_animal)
                elif stage == 2:
                    return _wrap(storyline_suzy_finale)

            # ── Mechanic dreams ────────────────────────────────────────────────

            case "mechanic_dreams":
                # Only begins after all three mechanics have been introduced
                if stage == 0 and not self.storylines["mechanics"]["completed"]:
                    return None
                return _wrap(storyline_mechanic_dream)

            # ── New narrative arcs (standalone functions) ──────────────────────

            case "kyle":
                # Stage 0: You notice the convenience store clerk is struggling (day 5+)
                if stage == 0 and day < 5:
                    return None
                kyle_events = [_wrap(storyline_kyle_regular), _wrap(storyline_kyle_problem),
                              _wrap(storyline_kyle_after_hours), _wrap(storyline_kyle_secret),
                              _wrap(storyline_kyle_finale)]
                if stage < len(kyle_events):
                    return kyle_events[stage]

            case "martinez":
                # Stage 0: Officer Martinez pulls you over a few days in
                if stage == 0 and (day < 4 or random.random() > 0.10):
                    return None
                martinez_events = [_wrap(storyline_martinez_license), _wrap(storyline_martinez_wellness),
                                  _wrap(storyline_martinez_favor), _wrap(storyline_martinez_resolution)]
                if stage < len(martinez_events):
                    return martinez_events[stage]

            case "dr_feelgood":
                # Stage 0: A sketchy doctor offers relief after a serious injury
                if stage == 0:
                    injuries = ["Broken Leg", "Broken Wrist", "Fractured Spine", "Severed Skin", "Deep Laceration"]
                    if day < 5 or not any(p.has_injury(i) for i in injuries):
                        return None
                feelgood_events = [_wrap(storyline_feelgood_first_pill), _wrap(storyline_feelgood_better),
                                  _wrap(storyline_feelgood_price_up), _wrap(storyline_feelgood_rock_bottom),
                                  _wrap(storyline_feelgood_resolution)]
                if stage < len(feelgood_events):
                    return feelgood_events[stage]

            case "stuart":
                # Stage 0: Stuart's scheme starts after you've met Oswald (day 10+)
                if stage == 0 and (not p.has_met("Oswald") or day < 10):
                    return None
                stuart_events = [_wrap(storyline_stuart_psst), _wrap(storyline_stuart_good_deal),
                                _wrap(storyline_stuart_bad_deal), _wrap(storyline_stuart_oswald_finds_out)]
                if stage < len(stuart_events):
                    return stuart_events[stage]

            case "grandma":
                # Stage 0: Grandma calls once you have her number
                if stage == 0 and not p.has_item("Grandma's Number"):
                    return None
                grandma_events = [_wrap(storyline_grandma_first_call), _wrap(storyline_grandma_recipe),
                                 _wrap(storyline_grandma_bad_news), _wrap(storyline_grandma_gift),
                                 _wrap(storyline_grandma_last_call)]
                if stage < len(grandma_events):
                    return grandma_events[stage]

            case "lucky_dog":
                # Stage 0: Lucky's story begins once he's your companion
                if stage == 0 and not p.has_companion("Lucky"):
                    return None
                lucky_events = [_wrap(storyline_lucky_who_hurt_you), _wrap(storyline_lucky_previous_owner),
                               _wrap(storyline_lucky_good_boy), _wrap(storyline_lucky_saves_your_life)]
                if stage < len(lucky_events):
                    return lucky_events[stage]

            case "dealer_past":
                # Stage 0: The dealer's past surfaces after many hands (day 15+, 30+ hands)
                if stage == 0 and (day < 15 or p.get_gambling_stat("total_hands") < 30):
                    return None
                dealer_events = [_wrap(storyline_dealer_photo), _wrap(storyline_dealer_journal),
                                _wrap(storyline_dealer_question), _wrap(storyline_dealer_answer),
                                _wrap(storyline_dealer_choice)]
                if stage < len(dealer_events):
                    return dealer_events[stage]

            case "sleep_paralysis":
                # Stage 0: Low sanity opens the door (sanity < 60, day 8+)
                if stage == 0 and (p.get_sanity() >= 60 or day < 8):
                    return None
                paralysis_events = [_wrap(storyline_paralysis_cant_move), _wrap(storyline_paralysis_speaks),
                                   _wrap(storyline_paralysis_offer), _wrap(storyline_paralysis_resolution)]
                if stage < len(paralysis_events):
                    return paralysis_events[stage]

            case "radio_signal":
                # Stage 0: Something strange on the radio catches your attention (day 6+, has Car)
                if stage == 0 and (day < 6 or not p.has_item("Car") or random.random() > 0.08):
                    return None
                radio_events = [_wrap(storyline_radio_static), _wrap(storyline_radio_broadcast),
                               _wrap(storyline_radio_source), _wrap(storyline_radio_whos_watching)]
                if stage < len(radio_events):
                    return radio_events[stage]

            case "graveyard":
                # Stage 0: You find yourself wandering the cemetery one night (day 12+)
                if stage == 0 and (day < 12 or random.random() > 0.08):
                    return None
                graveyard_events = [_wrap(storyline_graveyard_wandering), _wrap(storyline_graveyard_digger),
                                   _wrap(storyline_graveyard_your_plot), _wrap(storyline_graveyard_edgars_request)]
                if stage < len(graveyard_events):
                    return graveyard_events[stage]

            case "carnival":
                # Stage 0: The carnival rolls into town (day 8+, one-time)
                if stage == 0 and (day < 8 or p.has_met("Carnival") or random.random() > 0.06):
                    return None
                carnival_events = [_wrap(storyline_carnival_lights), _wrap(storyline_carnival_fortune),
                                  _wrap(storyline_carnival_game), _wrap(storyline_carnival_pack_up)]
                if stage < len(carnival_events):
                    return carnival_events[stage]

            case "lockbox":
                # Stage 0: You stumble onto a mysterious lockbox (day 4+)
                if stage == 0 and (day < 4 or random.random() > 0.08):
                    return None
                lockbox_events = [_wrap(storyline_lockbox_found), _wrap(storyline_lockbox_key_hunt),
                                 _wrap(storyline_lockbox_who_left_it)]
                if stage < len(lockbox_events):
                    return lockbox_events[stage]

        return None
    
    # ==========================================
    # MIGRATION HELPERS
    # ==========================================
    # These sync the storyline system with existing tracking variables
    # Call once at game start to migrate old save state
    
    def sync_with_existing_state(self):
        """Sync storyline stages with existing player variables (for migration)."""
        p = self.player
        
        # Suzy - check existing state (stage 0=color ready, 1=animal ready, 2=finale ready, 3=complete)
        if p.has_met("Suzy Finale"):
            self.storylines["suzy"]["stage"] = 3
            self.storylines["suzy"]["completed"] = True
        elif p.get_favorite_animal() is not None:
            self.storylines["suzy"]["stage"] = 2  # Animal answered, finale ready
        elif p.get_favorite_color() is not None:
            self.storylines["suzy"]["stage"] = 1  # Color answered, animal question ready
        elif p.get_name() is not None:
            self.storylines["suzy"]["stage"] = 0  # Name known, color question ready
        
        # Phil
        self._sync_phil_storyline_state()
        
        # Victoria
        if p.has_met("Victoria Confrontation"):
            self.storylines["victoria"]["stage"] = 2
            self.storylines["victoria"]["completed"] = True
        elif p.has_met("The Rival"):
            self.storylines["victoria"]["stage"] = 1
        
        # Betsy
        if p.has_met("Betsy"):
            if p.has_danger("Betsy Army"):
                self.storylines["betsy"]["stage"] = 2
            elif p.has_danger("Betsy Tractor"):
                self.storylines["betsy"]["stage"] = 1
            else:
                self.storylines["betsy"]["stage"] = 3
                self.storylines["betsy"]["completed"] = True
        
        # Grimy Gus
        if p.has_met("Grimy Gus"):
            self.storylines["grimy_gus"]["stage"] = 1
            self.storylines["grimy_gus"]["completed"] = True

        # Vinnie
        if p.has_met("Vinnie") or p.get_loan_shark_debt() > 0:
            self.storylines["vinnie"]["stage"] = 1
            self.storylines["vinnie"]["completed"] = True

        # Marvin
        if p.has_item("Map") or p.has_item("Worn Map"):
            self.storylines["marvin"]["stage"] = 1
            self.storylines["marvin"]["completed"] = True

        # Witch
        if p.has_met("Witch"):
            self.storylines["witch"]["stage"] = 1
            self.storylines["witch"]["completed"] = True
        
        # Mechanic dreams
        if p.get_tom_dreams() >= 3 and p.get_frank_dreams() >= 3 and p.get_oswald_dreams() >= 3:
            self.storylines["mechanic_dreams"]["completed"] = True
        
        # Mechanics intros (Tom/Frank/Oswald)
        met_count = sum([p.has_met("Tom Event"), p.has_met("Frank Event"), p.has_met("Oswald Event")])
        if met_count == 3:
            self.storylines["mechanics"]["stage"] = 3
            self.storylines["mechanics"]["completed"] = True
        elif met_count > 0:
            self.storylines["mechanics"]["stage"] = met_count
        
        # Cowboy / Jameson
        if p.has_met("Cowboy"):
            self.storylines["jameson"]["stage"] = 1
        
        # Mime
        if p.has_met("Mime"):
            self.storylines["mime"]["stage"] = 1
        
        # Collector
        if p.has_met("The Collector"):
            self.storylines["collector"]["stage"] = 1
        
        # Stray cat
        if p.has_met("Stray Cat Fed"):
            self.storylines["stray_cat"]["stage"] = 1
        
        # Gas station
        if p.has_met("Gas Station Hero"):
            self.storylines["gas_station_hero"]["stage"] = 1
        
        # Painkiller
        if p.has_danger("Painkiller Dependency"):
            self.storylines["painkiller"]["stage"] = 2
        elif p.has_danger("Shoulder Destroyed"):
            self.storylines["painkiller"]["stage"] = 0  # Ready to start


# =====================================================================
# =====================================================================
#
#   STORYLINE EVENT FUNCTIONS
#   Each function takes (player, sl) where sl is the StorylineSystem.
#   They handle all text, choices, effects, then call sl.advance/complete.
#
# =====================================================================
# =====================================================================


# =====================================================================
# MECHANICS INTRODUCTIONS - 3 wrapper events
# Tom, Frank, and Oswald each get a personal intro through the storyline
# system rather than the old _prereqs gate. Random order, 2-day min gap.
# Each wrapper calls sl.advance("mechanics") then fires the existing Player method.
# =====================================================================

def storyline_mechanics_intro_tom(p, sl):
    """Mechanics Intro: Trusty Tom appears for the first time."""
    sl.advance("mechanics")
    p.trusty_tom()

def storyline_mechanics_intro_frank(p, sl):
    """Mechanics Intro: Filthy Frank shows up on the road."""
    sl.advance("mechanics")
    p.filthy_frank()

def storyline_mechanics_intro_oswald(p, sl):
    """Mechanics Intro: Optimal Oswald makes his grand entrance."""
    sl.advance("mechanics")
    p.optimal_oswald()


# =====================================================================
# KYLE THE CLERK - 5 parts
# The convenience store clerk has his own problems.
# Stage 0: Just another customer (you notice Kyle is stressed)
# Stage 1: Kyle's problem (he confides in you)
# Stage 2: After hours (you find Kyle behind the store)
# Stage 3: Kyle's secret (he's been skimming the register)
# Stage 4: Finale (his boss finds out - your choice matters)
# =====================================================================

def storyline_kyle_regular(p, sl):
    """Kyle Part 1: You notice the convenience store clerk looks rough."""
    p.meet("Kyle")
    sl.advance("kyle")
    
    type.type("You stop by the convenience store for your usual run. The clerk behind the counter — ")
    type.type("you've seen him before, skinny kid, maybe 19, name tag says " + cyan(bright("KYLE")) + " — looks rough today.")
    print("\n")
    type.type("His eyes are red. His hands are shaking when he scans your items. He drops your change twice.")
    print("\n")
    type.type(quote("Sorry. Sorry about that. Long night."))
    print("\n")
    type.type("He tries to smile but it comes out wrong. Like he forgot how smiles work.")
    print("\n")
    answer = ask.yes_or_no("Do you ask if he's okay? ")
    if answer == "yes":
        type.type("Kyle blinks at you, surprised. Like nobody's asked him that in a while.")
        print("\n")
        type.type(quote("I'm... yeah. I'm fine. It's just... never mind. Thanks for asking though. Seriously."))
        print("\n")
        type.type("He gives you a real smile this time. Small, but real.")
        print("\n")
        type.type("You grab your bag and head out. Something tells you Kyle is not, in fact, fine.")
        p.meet("Kyle Asked")
    else:
        type.type("You take your change and leave. Not your problem.")
        print("\n")
        type.type("Through the window, you see Kyle put his head in his hands the moment you walk out.")
    print("\n")


def storyline_kyle_problem(p, sl):
    """Kyle Part 2: He confides in you about his situation."""
    sl.advance("kyle")
    
    type.type("You walk into the convenience store and Kyle's face lights up when he sees you.")
    print("\n")
    if p.has_met("Kyle Asked"):
        type.type(quote("Hey! You're the one who asked if I was okay the other day. That was... that meant a lot."))
        print("\n")
    else:
        type.type(quote("Hey, you're a regular now, right? I recognize the car outside. The, uh... the one you live in."))
        print("\n")
    type.type("The store is empty. Kyle leans over the counter and lowers his voice.")
    print("\n")
    type.type(quote("Can I tell you something? I don't really have anyone else to talk to."))
    print("\n")
    answer = ask.yes_or_no("Do you listen? ")
    if answer == "yes":
        type.type("Kyle takes a shaky breath.")
        print("\n")
        type.type(quote("My mom's sick. Like, really sick. Hospital bills are eating us alive. "))
        type.type(quote("I'm working double shifts here and it's still not enough. "))
        type.type(quote("The owner, Mr. Hendricks, he won't give me a raise because 'the economy' or whatever."))
        print("\n")
        type.type("He wipes his eye with his sleeve.")
        print("\n")
        type.type(quote("I've been thinking about doing something stupid. I just... I don't know what else to do."))
        print("\n")
        type.type("You don't say anything. Sometimes that's enough.")
        print("\n")
        type.type("Kyle slides you a free pack of gum across the counter. " + quote("For listening."))
        p.meet("Kyle Confided")
    else:
        type.type(quote("Yeah, no, you're right. Forget it. That'll be $4.50."))
        print("\n")
        type.type("Kyle goes back to stocking shelves. The conversation is over.")
    print("\n")


def storyline_kyle_after_hours(p, sl):
    """Kyle Part 3: You find Kyle behind the store after it closes."""
    sl.advance("kyle")
    
    type.type("It's late. You're heading back to your car when you spot a figure sitting behind the convenience store, ")
    type.type("leaning against the dumpster. It's Kyle.")
    print("\n")
    type.type("He's got a cigarette in one hand and a crumpled piece of paper in the other. ")
    type.type("He doesn't notice you at first.")
    print("\n")
    type.type("When he does, he jumps.")
    print("\n")
    type.type(quote("Jesus! You scared me. What are you doing back here?"))
    print("\n")
    type.type("You nod at the paper. It's a hospital bill. The number at the bottom has five digits.")
    print("\n")
    if p.has_met("Kyle Confided"):
        type.type(quote("It's mom's. Another one. They just keep coming."))
        print("\n")
        type.type("He crumples it up tighter.")
        print("\n")
        type.type(quote("I started doing it, by the way. The stupid thing I mentioned. "))
        type.type(quote("Skimming the register. Twenty here, forty there. Hendricks doesn't notice. He's never here."))
        print("\n")
    else:
        type.type("Kyle looks at the bill, then at you.")
        print("\n")
        type.type(quote("You wouldn't understand. Nobody does. I've been... taking money. From the register. "))
        type.type(quote("Small amounts. For my mom. She needs it more than Hendricks does."))
        print("\n")
    type.type("Kyle looks at you with desperate eyes.")
    print("\n")
    type.type(quote("You're not gonna tell anyone, right?"))
    print("\n")
    answer = ask.yes_or_no("Promise to keep his secret? ")
    if answer == "yes":
        type.type(quote("Thank you. Seriously. You're the only person who knows."))
        print("\n")
        type.type("Kyle offers you his cigarette. You decline. He shrugs and takes another drag.")
        print("\n")
        type.type(quote("I'll figure this out. I have to."))
        p.meet("Kyle Secret Kept")
    else:
        type.type("Kyle's face goes white.")
        print("\n")
        type.type(quote("Please. PLEASE don't. I'll lose everything. My mom will... she can't..."))
        print("\n")
        type.type("He starts to cry. Ugly crying. The kind you do behind a dumpster at midnight.")
        print("\n")
        type.type("You walk away. You haven't decided what to do yet.")
    print("\n")


def storyline_kyle_secret(p, sl):
    """Kyle Part 4: The skimming gets worse. Kyle offers you a cut."""
    sl.advance("kyle")
    
    type.type("Kyle flags you down the moment you walk in. The store is empty. He looks wired. Jittery.")
    print("\n")
    type.type(quote("Hey. Hey. Close the door."))
    print("\n")
    type.type("He pulls out a wad of cash from under the counter. It's not small anymore. ")
    type.type("This is hundreds of dollars.")
    print("\n")
    type.type(quote("Hendricks still hasn't noticed. He's got three stores, he barely checks the books. "))
    type.type(quote("I've been taking more. A lot more. Mom's doing better, she's got this new treatment..."))
    print("\n")
    type.type("He pushes some bills toward you.")
    print("\n")
    type.type(quote("Here. Take some. You've kept your mouth shut. You deserve it. Call it... ") + 
             quote("a loyalty bonus."))
    print("\n")
    type.type(quote("There's ") + green(bright("$200")) + quote(" on the counter."))
    print("\n")
    answer = ask.yes_or_no("Take the money? ")
    if answer == "yes":
        p.change_balance(200)
        type.type("You pocket the cash. Kyle grins.")
        print("\n")
        type.type(quote("See? We're in this together now. Partners."))
        print("\n")
        type.type("That word sits heavy in your stomach.")
        p.meet("Kyle Took Money")
        p.lose_sanity(2)
    else:
        type.type(quote("No? Fine. More for mom."))
        print("\n")
        type.type("He shoves the cash back under the counter. His hands are shaking again, ")
        type.type("but not from sadness this time. He's excited. That's worse.")
        print("\n")
        type.type("You leave with a bad feeling.")
    print("\n")


def storyline_kyle_finale(p, sl):
    """Kyle Part 5: Hendricks finds out. Your choices come to a head."""
    sl.advance("kyle")
    sl.complete("kyle")
    
    type.type("You pull up to the convenience store and something's wrong. ")
    type.type("There's a black SUV parked out front. The OPEN sign is off.")
    print("\n")
    type.type("Through the window, you can see a large man in a polo shirt jabbing his finger at Kyle. ")
    type.type("That's Hendricks. He found out.")
    print("\n")
    type.type("Kyle sees you through the window. His eyes go wide. Pleading.")
    print("\n")
    
    if p.has_met("Kyle Took Money"):
        type.type("You also notice Hendricks has a security camera printout in his hand. ")
        type.type("There's a grainy image of someone pocketing cash at the counter.")
        print("\n")
        type.type("Wait. That's not Kyle in the image. That's " + red(bright("you")) + ".")
        print("\n")
        type.type("Hendricks spots you and storms out.")
        print("\n")
        type.type(quote("YOU! You're the other one! Kyle told me everything! "))
        type.type(quote("I'm calling the cops on BOTH of you!"))
        print("\n")
        answer = ask.yes_or_no("Do you run? ")
        if answer == "yes":
            type.type("You bolt. Behind you, Kyle bolts too, in the other direction.")
            print("\n")
            type.type("Hendricks is yelling and fumbling for his phone. You don't look back.")
            print("\n")
            type.type("You'll have to avoid this part of town for a while. And Kyle... ")
            type.type("you hope he made it. You hope his mom is okay.")
            print("\n")
            type.type("You feel like a coward.")
            p.lose_sanity(5)
            p.add_danger("Hendricks Looking")
        else:
            type.type(quote("It was all me. Kyle didn't know."))
            print("\n")
            type.type("Hendricks stares at you. Kyle stares at you. The world holds its breath.")
            print("\n")
            type.type("Hendricks grabs you by the collar. " + quote("You're paying every cent back. "))
            type.type(quote("Every. Cent. Or I press charges."))
            print("\n")
            fine = min(500, p.get_balance())
            p.change_balance(-fine)
            type.type("You hand over " + red(bright("${:,}".format(fine))) + ". Hendricks takes it and shoves you out the door.")
            print("\n")
            type.type("Through the window, you see Kyle mouthing " + quote("thank you") + " with tears streaming down his face.")
            print("\n")
            type.type("Kyle keeps his job. His mom keeps her treatment. And you... you did something good today.")
            p.heal(10)
            p.restore_sanity(5)
    
    elif p.has_met("Kyle Secret Kept"):
        type.type("Do you go inside?")
        print("\n")
        answer = ask.yes_or_no("Stand up for Kyle? ")
        if answer == "yes":
            type.type("You push through the door. Hendricks wheels on you.")
            print("\n")
            type.type(quote("Who the hell are you?"))
            print("\n")
            type.type(quote("I'm a customer. Your best customer. And that kid works harder than anyone I've ever seen."))
            print("\n")
            type.type("Hendricks pauses. Kyle is frozen.")
            print("\n")
            type.type(quote("He's been working doubles for months, ") + 
                     quote("you don't even come in to check on this place. ") + 
                     quote("Maybe if you paid him enough, he wouldn't have to get creative."))
            print("\n")
            type.type("Hendricks opens his mouth. Closes it. Opens it again.")
            print("\n")
            type.type(quote("...I'll deal with this internally. Get out of my store."))
            print("\n")
            type.type("You leave. Kyle catches up to you outside five minutes later.")
            print("\n")
            type.type(quote("He's not pressing charges. He's... he's giving me a raise. A small one, but... "))
            type.type(quote("I can stop taking from the register. Thank you. I don't know how to thank you."))
            print("\n")
            type.type("Kyle shakes your hand. His grip is firm now. He's going to be alright.")
            p.heal(5)
            p.restore_sanity(3)
        else:
            type.type("You drive away. Not your fight.")
            print("\n")
            type.type("The next day, the convenience store has a new clerk. ")
            type.type("You never see Kyle again.")
            print("\n")
            type.type("You try not to think about it.")
            p.lose_sanity(3)
    
    else:
        type.type("You watch from outside. Hendricks fires Kyle on the spot. ")
        type.type("Kyle walks out with his head down, doesn't even see you.")
        print("\n")
        type.type("The store has a new clerk by the next day. You never see Kyle again.")
        print("\n")
        type.type("You feel... nothing. And that feeling of nothing feels bad.")
        p.lose_sanity(2)
    print("\n")


# =====================================================================
# OFFICER MARTINEZ - 4 parts
# A cop who keeps showing up. Is he harassing you or helping you?
# Stage 0: License and registration (routine stop that feels targeted)
# Stage 1: Wellness check (shows up at your car concerned)
# Stage 2: The favor (asks you to keep an eye on someone)
# Stage 3: Resolution (the truth about why he kept coming around)
# =====================================================================

def storyline_martinez_license(p, sl):
    """Martinez Part 1: License and registration."""
    p.meet("Martinez")
    sl.advance("martinez")
    
    type.type("You hear a knock on your window. Cop knock. The heavy, authoritative kind.")
    print("\n")
    type.type("You sit up and see a police officer standing outside your car. He's stocky, late 40s, ")
    type.type("with a thick mustache and a name tag that reads " + cyan(bright("MARTINEZ")) + ".")
    print("\n")
    type.type(quote("License and registration, please."))
    print("\n")
    type.type("You fumble around. You don't actually have a registration. You're not even sure where your license is.")
    print("\n")
    answer = ask.yes_or_no("Do you try to explain your situation? ")
    if answer == "yes":
        type.type(quote("Look, Officer, I'm between places right now. I know this looks bad—"))
        print("\n")
        type.type("Martinez holds up a hand.")
        print("\n")
        type.type(quote("I know what this looks like. I've been on patrol here for 22 years. "))
        type.type(quote("You're not the first person to sleep in their car on this stretch of road, and you won't be the last."))
        print("\n")
        type.type("He pulls out a small notepad and writes something down.")
        print("\n")
        type.type(quote("I'm not going to ticket you today. But I need you to know — technically, this is a violation. "))
        type.type(quote("Next time another officer comes by, they might not be as understanding."))
        print("\n")
        p.meet("Martinez Honest")
    else:
        type.type("You hand over a crumpled fast food receipt and hope for the best.")
        print("\n")
        type.type("Martinez stares at it. Stares at you. Back at the receipt.")
        print("\n")
        type.type(quote("This is a receipt for a cheeseburger."))
        print("\n")
        type.type(quote("...It was a good cheeseburger."))
        print("\n")
        type.type("Martinez sighs the sigh of a man who has seen everything.")
        print("\n")
        type.type(quote("I'm going to pretend this didn't happen. Don't make me regret it."))
    print("\n")
    type.type("He taps the roof of your car twice, gets back in his cruiser, and drives off.")
    print("\n")


def storyline_martinez_wellness(p, sl):
    """Martinez Part 2: He comes back. This time it's not official."""
    sl.advance("martinez")
    
    type.type("Officer Martinez's cruiser pulls up next to your car. But this time, he's not in uniform. ")
    type.type("He's wearing a flannel shirt and jeans. He's holding two cups of coffee.")
    print("\n")
    type.type("He knocks gently this time.")
    print("\n")
    type.type(quote("Hey. It's Martinez. Off duty. Thought you might want one of these."))
    print("\n")
    type.type("He holds up a coffee cup.")
    print("\n")
    answer = ask.yes_or_no("Accept the coffee? ")
    if answer == "yes":
        type.type("You take the coffee. It's hot. Real hot. Gas station coffee, but still.")
        print("\n")
        type.type("Martinez leans against your car and sips his own.")
        print("\n")
        type.type(quote("I've been thinking about you. Not in a weird way. In a... I drive past here every day. "))
        type.type(quote("I see your car. I see you. And I keep thinking — does anybody check on this person?"))
        print("\n")
        type.type("He pauses.")
        print("\n")
        type.type(quote("My brother lived in his car for two years. Before he... ") + 
                 quote("well. Nobody checked on him. So now I check."))
        print("\n")
        type.type("You don't know what to say. So you just drink your coffee.")
        print("\n")
        type.type(quote("You don't have to talk. Just... know someone gives a damn."))
        p.heal(5)
        p.restore_sanity(3)
        p.meet("Martinez Coffee")
    else:
        type.type(quote("Alright, fair enough. Can't trust a cop, even off duty. I get it."))
        print("\n")
        type.type("He sets the second coffee on your hood.")
        print("\n")
        type.type(quote("It's here if you change your mind. It'll get cold, but hey. Cold coffee's still coffee."))
        print("\n")
        type.type("He drives off. The coffee sits on your hood for an hour before you drink it. It's terrible. ")
        type.type("But you drink every drop.")
    print("\n")


def storyline_martinez_favor(p, sl):
    """Martinez Part 3: He asks you for a favor."""
    sl.advance("martinez")
    
    type.type("Martinez is back. This time he's in uniform and he's all business.")
    print("\n")
    type.type(quote("I need to ask you something, and I need you to be straight with me."))
    print("\n")
    type.type("He pulls out his phone and shows you a photo of a man in a red suit.")
    print("\n")
    if p.has_met("Interrogator"):
        type.type("You recognize him immediately. That's the man who interrogated you. The red suit guy.")
        print("\n")
        type.type(quote("You've seen him? I can tell by your face. You've seen him."))
    else:
        type.type(quote("This man's been reported bothering people who live on the margins. "))
        type.type(quote("Homeless folks, car sleepers, drifters. Harassing them. Intimidating them."))
    print("\n")
    type.type(quote("His name is Phil Dunmore. He's been making my job harder for three years. "))
    type.type(quote("I can't catch him doing anything technically illegal, but he's hurting people."))
    print("\n")
    type.type(quote("If you see him again, I need you to call me."))
    print("\n")
    type.type("He hands you a card with his personal number on it.")
    print("\n")
    answer = ask.yes_or_no("Take the card? ")
    if answer == "yes":
        p.add_item("Martinez's Card")
        type.type("You take " + item("Martinez's Card") + ". He nods.")
        print("\n")
        type.type(quote("Thanks. You're doing more than you know."))
        p.meet("Martinez Favor")
    else:
        type.type(quote("I understand. You don't want to get involved. That's smart."))
        print("\n")
        type.type("He pockets the card. But he leaves his number written on a napkin under your wiper blade anyway.")
        print("\n")
        p.add_item("Martinez's Card")
    print("\n")


def storyline_martinez_resolution(p, sl):
    """Martinez Part 4: The truth about Martinez."""
    sl.advance("martinez")
    sl.complete("martinez")
    
    type.type("Martinez's cruiser pulls up one last time. He gets out slowly. He looks tired. ")
    type.type("Not the tired of a long shift. The tired of a long life.")
    print("\n")
    type.type(quote("I owe you an explanation."))
    print("\n")
    type.type("He sits on the curb next to your car.")
    print("\n")
    type.type(quote("My brother, Danny. He lived in his car on a road just like this one. "))
    type.type(quote("Same situation as you. Down on his luck. Playing cards to make money. "))
    type.type(quote("I used to check on him, bring him coffee, same as I do with you."))
    print("\n")
    type.type("His voice cracks.")
    print("\n")
    type.type(quote("One day I got too busy. Skipped a week. Then two. "))
    type.type(quote("When I finally came back, Danny was gone. Car was still there, but Danny was gone."))
    print("\n")
    type.type("Long pause.")
    print("\n")
    type.type(quote("They found him three towns over. He'd gotten sick. Walked to a hospital but didn't make it."))
    print("\n")
    type.type("Martinez wipes his eyes. Badge and all, this man is just a brother who lost a brother.")
    print("\n")
    type.type(quote("I check on you because I couldn't check on him. That's the truth of it."))
    print("\n")
    if p.has_met("Martinez Coffee"):
        type.type("You put your hand on his shoulder. He nods. That's enough.")
        print("\n")
        type.type(quote("Take care of yourself out here. And..."))
        print("\n")
        type.type("He pulls out a folded envelope and hands it to you.")
        print("\n")
        type.type(quote("Danny would've wanted someone to have this."))
        print("\n")
        type.type("Inside is " + green(bright("$500")) + " and a photo of two brothers standing next to a beat-up Camaro, smiling.")
        p.change_balance(500)
        p.heal(10)
        p.restore_sanity(5)
    else:
        type.type("He stands up, dusts off his pants.")
        print("\n")
        type.type(quote("Anyway. That's it. That's the whole story. Stay safe out here."))
    print("\n")
    type.type("Martinez drives off. You have a feeling he'll still drive past. Just to check.")
    print("\n")


# =====================================================================
# THE MIME RETURNS - 4 new parts (expansion of existing mime event)
# After the initial mime encounter (stage 0, handled by existing the_mime)
# Stage 1: Encore performance
# Stage 2: The message
# Stage 3: Behind the paint
# Stage 4: The final act
# =====================================================================

def storyline_mime_encore(p, sl):
    """Mime Part 2: He's back, and his act has evolved."""
    sl.advance("mime")
    
    type.type("You're minding your own business when a familiar figure appears from behind a tree. ")
    type.type("Striped shirt. White face. The mime is back.")
    print("\n")
    type.type("This time, his act is different. More elaborate. He's set up an invisible stage ")
    type.type("with invisible curtains. He even does an invisible drum roll.")
    print("\n")
    type.type("The performance begins. He mimes waking up in a car. Your car. He mimes playing cards. ")
    type.type("Winning. Losing. He mimes meeting different people—")
    print("\n")
    
    if p.has_met("Cowboy"):
        type.type("Wait, is he doing Jameson? He's pretending to ride a horse. That's definitely Jameson.")
        print("\n")
    if p.has_met("Betsy"):
        type.type("Now he's being Betsy. He's on all fours going 'moo.' Well, mouthing 'moo.' He's still a mime.")
        print("\n")
    if p.has_met("Interrogator"):
        type.type("Oh no. He's straightening an invisible tie. That's the red suit guy. Phil. He nails the judgmental stare.")
        print("\n")
    
    type.type("The mime finishes with a new bit: he pulls an invisible rope and lifts himself off the ground, ")
    type.type("dangling in the air. Then he falls, catches himself, and takes a bow.")
    print("\n")
    type.type("He's sweating under the face paint. This guy takes his craft seriously.")
    print("\n")
    answer = ask.yes_or_no("Applaud the performance? ")
    if answer == "yes":
        type.type("The mime beams. He reaches behind your ear and produces a very real, very shiny quarter.")
        print("\n")
        type.type("Then another. And another. And another. This goes on for a while. ")
        type.type("By the time he stops, you've got " + green(bright("$15")) + " in quarters.")
        p.change_balance(15)
        type.type("The mime takes one final bow and moonwalks away.")
    else:
        type.type("The mime freezes. Slowly, dramatically, he turns to face you. ")
        type.type("He does the single tear thing again. But then he wags his finger.")
        print("\n")
        type.type("He'll be back. That finger wag promised it.")
    print("\n")


def storyline_mime_message(p, sl):
    """Mime Part 3: The mime tries to tell you something important."""
    sl.advance("mime")
    
    type.type("The mime appears again, but this time there's no performance. No invisible stage. ")
    type.type("He walks straight up to you with purpose.")
    print("\n")
    type.type("He's holding a real sign. It reads: " + bright(yellow("\"I CAN'T TALK. BUT I NEED TO TELL YOU SOMETHING.\"")))
    print("\n")
    type.type("He flips the sign over: " + bright(yellow("\"SOMEONE IS WATCHING YOU.\"")))
    print("\n")
    type.type("He points down the road. Points at the tree line. Points at a spot across the street ")
    type.type("where — was someone standing there? You look, but there's nobody now.")
    print("\n")
    type.type("The mime grabs your arm. His grip is surprisingly strong. His eyes, under all that white paint, ")
    type.type("are scared. Genuinely scared.")
    print("\n")
    type.type("He flips to a third sign: " + bright(yellow("\"BE CAREFUL. THEY DON'T LIKE WHAT YOU'RE DOING.\"")))
    print("\n")
    type.type("Before you can react, the mime hears something. He snaps his head to the left, ")
    type.type("drops the signs, and sprints away faster than any mime should be able to run.")
    print("\n")
    type.type("You pick up the signs. On the back of the last one, in small handwriting:")
    print("\n")
    type.type(italic("\"My name is Gerald. If they find out I told you, I'm done. -G\""))
    print("\n")
    p.lose_sanity(3)
    p.meet("Gerald")
    print("\n")


def storyline_mime_behind_paint(p, sl):
    """Mime Part 4: You find Gerald without his face paint."""
    sl.advance("mime")
    
    type.type("You're at the gas station filling up — or rather, pretending to while you use the bathroom — ")
    type.type("when you notice a man sitting at the bus stop across the street.")
    print("\n")
    type.type("No striped shirt. No white paint. Just a regular guy in a brown jacket. ")
    type.type("But you recognize the way he sits. The way he holds his hands. The way he watches everything.")
    print("\n")
    type.type("That's the mime. That's Gerald.")
    print("\n")
    type.type("You walk over. He sees you coming and tenses up, like he might run.")
    print("\n")
    type.type(quote("Please. Sit down. Don't make it obvious."))
    print("\n")
    type.type("His voice is quiet. Raspy. Like he hasn't used it in a long time.")
    print("\n")
    type.type(quote("I was a performer. A real one. Theaters, festivals, the whole thing. "))
    type.type(quote("Then I saw something I shouldn't have. Backstage at a casino. Money changing hands. "))
    type.type(quote("Important hands. The kind of hands that make people disappear."))
    print("\n")
    type.type(quote("The mime thing started as a disguise. Turns out, nobody looks twice at a mime. "))
    type.type(quote("You're invisible. The perfect hiding spot is where everyone can see you."))
    print("\n")
    type.type("He glances around nervously.")
    print("\n")
    type.type(quote("I've been watching you because you're in their territory. The gambling road. "))
    type.type(quote("They don't like people winning too much. Drawing attention."))
    print("\n")
    answer = ask.yes_or_no("Ask who 'they' are? ")
    if answer == "yes":
        type.type("Gerald shakes his head violently.")
        print("\n")
        type.type(quote("No. No. If I say the name, it's over. For both of us. "))
        type.type(quote("Just... keep your head down. Win enough to survive, not enough to matter."))
        print("\n")
        type.type("He stands up suddenly as a car drives past.")
        print("\n")
        type.type(quote("I have to go. Watch the tree line. If you see a black car with no plates, run."))
        p.meet("Gerald Warning")
    else:
        type.type("Gerald nods approvingly.")
        print("\n")
        type.type(quote("Smart. The less you know, the safer you are. Just... be careful."))
    print("\n")
    type.type("He walks away. No moonwalk this time. Just a scared man in a brown jacket.")
    print("\n")


def storyline_mime_final_act(p, sl):
    """Mime Part 5: Gerald's last performance."""
    sl.advance("mime")
    sl.complete("mime")
    
    type.type("There's something on your windshield. It's a note, written in the same ")
    type.type("small handwriting from Gerald's signs.")
    print("\n")
    type.type(italic("\"They found me. I have to leave. But I wanted to give you one last show. \""))
    print("\n")
    type.type(italic("\"Look under your passenger seat. -G\""))
    print("\n")
    type.type("You reach under the passenger seat and find a small box wrapped in newspaper.")
    print("\n")
    type.type("Inside is " + green(bright("$300")) + " in crumpled bills, a fake flower ")
    type.type("(the kind a magician would use), and a note:")
    print("\n")
    type.type(italic("\"The money is from my performances. People throw coins at mimes more than you'd think.\""))
    print("\n")
    type.type(italic("\"The flower is because you clapped when nobody else did.\""))
    print("\n")
    type.type(italic("\"I'm going somewhere they can't find me. A mime can be anyone. That's the beauty of it.\""))
    print("\n")
    type.type(italic("\"Be safe. Be loud. Be everything a mime can't be.\""))
    print("\n")
    type.type(italic("\"Your friend, Gerald\""))
    print("\n")
    p.change_balance(300)
    p.add_item("Fake Flower")
    
    if p.has_met("Gerald Warning"):
        type.type("You scan the tree line. No black cars. No watchers. Just the road, your car, ")
        type.type("and the memory of a mime who was braver than most men with voices.")
    else:
        type.type("You hold the fake flower. It smells like nothing. But it feels like something.")
    print("\n")
    type.type("Somewhere, somehow, you hope Gerald found his quiet place.")
    p.restore_sanity(5)
    p.heal(5)
    print("\n")


# =====================================================================
# SUZY STORYLINE VARIANTS - 3 new parts
# Pulled from night pools into day storyline system.
# Stage 1: Color question (was whats_my_color)
# Stage 2: Animal question (was whats_my_animal)
# Stage 3: Suzy finale (Suzy gives you her gift)
# =====================================================================

def storyline_suzy_color(p, sl):
    """Suzy Part 2: She comes back to ask your favorite color."""
    sl.advance("suzy")
    p.meet("Suzy Color")
    
    type.type("You hear the familiar sound of sneakers scraping against concrete, and the rhythmic ")
    type.type("slapping of a jump rope. It's Suzy.")
    print("\n")
    type.type(quote("Hey, ") + quote(str(p.get_name()) + "! Remember me? It's Suzy!"))
    print("\n")
    type.type(quote("I have a very important question for you today. VERY important."))
    print("\n")
    type.type(quote("What's your favorite color?"))
    print("\n")
    type.type("She stares at you with the intensity of someone who will remember this answer forever.")
    print("\n")
    color = ask.single_word("Tell her your favorite color: ")
    p.set_favorite_color(color)
    print()
    type.type(quote(color + "?! That's a GREAT color! I love " + color + "!"))
    print("\n")
    type.type(quote("I'm going to remember that forever. You like " + color + ". Got it."))
    print("\n")
    type.type("Suzy writes something in a tiny notebook she pulls from her pocket, ")
    type.type("nods seriously, then continues jump roping down the road.")
    print("\n")


def storyline_suzy_animal(p, sl):
    """Suzy Part 3: She comes back to ask your favorite animal."""
    sl.advance("suzy")
    
    type.type("Suzy appears again, jump roping from the opposite direction this time. ")
    type.type("She's wearing a backpack that's almost bigger than she is.")
    print("\n")
    type.type(quote("Hey " + str(p.get_name()) + "! Okay so I have ANOTHER very important question."))
    print("\n")
    type.type(quote("Even more important than the color one. Ready?"))
    print("\n")
    type.type(quote("What's your favorite animal?"))
    print("\n")
    animal = ask.single_word("Tell her your favorite animal: ")
    p.set_favorite_animal(animal)
    print()
    type.type(quote("A " + animal + "!! OH MY GOSH. I love " + animal + "s!"))
    print("\n")
    type.type(quote("You like " + str(p.get_favorite_color()) + " and " + animal + "s. That's so cool!"))
    print("\n")
    type.type(quote("Okay, I gotta go. But I'll be back! I'm making you something!"))
    print("\n")
    type.type("She scribbles furiously in her tiny notebook and skip-ropes away, ")
    type.type("humming a song that doesn't exist yet.")
    print("\n")


def storyline_suzy_finale(p, sl):
    """Suzy Part 4: Suzy brings you her handmade gift. Good ending: gift + sanity.
    Bad ending: player rejects it → suzy_the_snitch fires immediately → game over."""
    sl.advance("suzy")
    sl.complete("suzy")
    # NOTE: p.meet("Suzy Finale") is intentionally deferred to YES branch only.
    # Suzy_the_snitch checks that flag as its guard — leaving it unset lets the
    # bad-path call through cleanly.

    color = str(p.get_favorite_color())
    animal = str(p.get_favorite_animal())
    
    type.type("You hear the jump rope before you see her. But this time, the rhythm is slower. ")
    type.type("Careful. Like she's carrying something precious.")
    print("\n")
    type.type("Suzy walks up to your car with both hands behind her back. She's grinning so wide ")
    type.type("her cheeks might burst.")
    print("\n")
    type.type(quote("Close your eyes! You have to close your eyes!"))
    print("\n")
    type.type("You close your eyes.")
    print("\n")
    type.type("You feel something placed gently in your hands. It's light. Soft.")
    print("\n")
    type.type(quote("Okay! Open!"))
    print("\n")
    type.type("It's a handmade drawing. Crayon on construction paper. It shows a " + cyan(bright(color)) + 
             " " + cyan(bright(animal)) + " standing next to a car under a big yellow sun.")
    print("\n")
    type.type("Underneath, in wobbly letters, it says: " + bright(yellow("\"" + str(p.get_name()) + "'s " + animal + "\"")))
    print("\n")
    type.type("It's the worst drawing you've ever seen. It's also the best gift you've ever gotten.")
    print("\n")
    type.type(quote("Do you like it?! I made it myself! I used the good crayons!"))
    print("\n")
    answer = ask.yes_or_no("Do you like it? ")
    if answer == "yes":
        type.type("Suzy squeals and hugs you so tight your ribs hurt.")
        print("\n")
        type.type(quote("I KNEW you'd like it! You're my best friend, " + str(p.get_name()) + "!"))
        print("\n")
        type.type(quote("I have to go now. Mom says — well, she didn't say anything because she disappeared. "))
        type.type(quote("But I think she'd say it's time for dinner!"))
        print("\n")
        type.type("Suzy skip-ropes away, turning back to wave three separate times.")
        print("\n")
        type.type("You look at the drawing. You carefully fold it and put it somewhere safe.")
        p.meet("Suzy Finale")  # good ending — blocks suzy_the_snitch permanently
        p.add_item("Suzy's Gift")
        p.restore_sanity(10)
        p.heal(10)
    else:
        type.type("Suzy's lip quivers. But only for a second.")
        print("\n")
        type.type(quote("That's okay. Not everyone likes art. Mom didn't like my drawings either. "))
        type.type(quote("Before she disappeared."))
        print("\n")
        type.type("She takes the drawing back, folds it carefully, and puts it in her backpack.")
        print("\n")
        type.type(quote("Maybe I'll find someone who likes it."))
        print("\n")
        type.type("She jump ropes away. You feel like the worst person alive.")
        print("\n")
        # Suzy remembers everything. Cops arrive shortly after.
        p.suzy_the_snitch()


# =====================================================================
# MECHANIC DREAM ROUTER
# Delegates to the existing dream counter system on the Player.
# This just wraps the existing mechanic dream logic.
# =====================================================================

def storyline_mechanic_dream(p, sl):
    """Routes to the appropriate mechanic dream based on counters."""
    # Pick a mechanic whose dream counter is < 3
    candidates = []
    if p.has_met("Tom") and p.get_tom_dreams() < 3:
        candidates.append("tom")
    if p.has_met("Frank") and p.get_frank_dreams() < 3:
        candidates.append("frank")
    if p.has_met("Oswald") and p.get_oswald_dreams() < 3:
        candidates.append("oswald")
    
    if not candidates:
        sl.complete("mechanic_dreams")
        return
    
    chosen = random.choice(candidates)
    
    # Delegate to existing dream methods on Player
    if chosen == "tom":
        dream_stage = p.get_tom_dreams()
        events = ["tom_dream_1", "tom_dream_2", "tom_dream_3"]
        if dream_stage < len(events):
            method = getattr(p, events[dream_stage], None)
            if method:
                method()
    elif chosen == "frank":
        dream_stage = p.get_frank_dreams()
        events = ["frank_dream_1", "frank_dream_2", "frank_dream_3"]
        if dream_stage < len(events):
            method = getattr(p, events[dream_stage], None)
            if method:
                method()
    elif chosen == "oswald":
        dream_stage = p.get_oswald_dreams()
        events = ["oswald_dream_1", "oswald_dream_2", "oswald_dream_3"]
        if dream_stage < len(events):
            method = getattr(p, events[dream_stage], None)
            if method:
                method()
    
    # Advance the storyline stage counter
    sl.advance("mechanic_dreams")
    
    # Check if all dreams are now complete
    if p.get_tom_dreams() >= 3 and p.get_frank_dreams() >= 3 and p.get_oswald_dreams() >= 3:
        sl.complete("mechanic_dreams")


# =====================================================================
# DR. FEELGOOD - 5 parts
# A back-alley "doctor" who sells painkillers. Starts helpful, gets dark.
# Stage 0: First pill (he finds you hurting and offers relief)
# Stage 1: Feeling better (you seek him out this time)
# Stage 2: Price goes up (he knows you're hooked)
# Stage 3: Rock bottom (you can't afford it, desperate measures)
# Stage 4: Resolution (cold turkey, relapse, or unlikely rescue)
# =====================================================================

def storyline_feelgood_first_pill(p, sl):
    """Dr. Feelgood Part 1: A stranger offers relief from your pain."""
    p.meet("Dr. Feelgood")
    sl.advance("dr_feelgood")
    
    type.type("You're leaning against your car, wincing. Everything hurts. Your body has been through ")
    type.type("more punishment than it was designed for.")
    print("\n")
    type.type("A man appears from behind the gas station. He's wearing a wrinkled white coat over a Hawaiian shirt. ")
    type.type("He has a doctor's bag — the old-fashioned kind, black leather — and a smile that belongs ")
    type.type("on a used car salesman.")
    print("\n")
    type.type(quote("You look like a person in pain. I'm a person who fixes pain."))
    print("\n")
    type.type("He opens his bag. Inside are rows and rows of pill bottles, neatly organized.")
    print("\n")
    type.type(quote("Name's Dr. Feelgood. Not my real name, obviously. But nobody's using their real name ") +
             quote("out here, are they?"))
    print("\n")
    type.type("He holds up a single white pill between his thumb and forefinger.")
    print("\n")
    type.type(quote("First one's free. That's not a gimmick. I genuinely want to help. ") +
             quote("Think of it as a... demonstration."))
    print("\n")
    answer = ask.yes_or_no("Take the pill? ")
    if answer == "yes":
        type.type("You take the pill. Within minutes, the pain melts away like snow in summer.")
        print("\n")
        type.type("Your headache is gone. Your aching joints feel oiled. That throbbing in your side? Vanished.")
        print("\n")
        type.type(quote("Beautiful, right? That's the good stuff. Medical grade. None of that gas station garbage."))
        print("\n")
        type.type("He hands you a second pill in a tiny zip-lock bag.")
        print("\n")
        type.type(quote("For tomorrow. When it wears off. And it WILL wear off. Trust me."))
        print("\n")
        type.type("Dr. Feelgood tips an invisible hat and disappears back behind the gas station.")
        p.heal(20)
        p.add_item("Feelgood Pill")
        p.meet("Took First Pill")
    else:
        type.type(quote("Smart. Or stupid. Time will tell."))
        print("\n")
        type.type("He shrugs and walks away, humming. The bag full of pills clinking softly.")
        print("\n")
        type.type("The pain is still there. It's always there.")
    print("\n")


def storyline_feelgood_better(p, sl):
    """Dr. Feelgood Part 2: You seek him out. The relief was too good."""
    sl.advance("dr_feelgood")
    
    type.type("You've been thinking about Dr. Feelgood. You weren't going to, but the pain came back ")
    type.type("worse than before.")
    print("\n")
    if p.has_item("Feelgood Pill"):
        type.type("You took the second pill two days ago. It worked even better than the first. ")
        type.type("Now you're out. Now you want more.")
        p.use_item("Feelgood Pill")
    else:
        type.type("You turned him down before, but the pain hasn't stopped. It's getting worse. ")
        type.type("You keep remembering that smile. That pill.")
    print("\n")
    type.type("You find him in the same spot behind the gas station. He's sitting on a milk crate, ")
    type.type("reading a medical textbook that looks like it's from 1987.")
    print("\n")
    type.type(quote("Ah! My favorite patient! I knew you'd come back. They always come back."))
    print("\n")
    type.type("He opens the bag. Same rows of pills. Same smile.")
    print("\n")
    type.type(quote("Second visit is $50. Still a bargain. Hospital would charge you three grand ") +
             quote("and make you wait four hours."))
    print("\n")
    if p.get_balance() >= 50:
        answer = ask.yes_or_no("Pay $50 for the pills? ")
        if answer == "yes":
            p.change_balance(-50)
            type.type("You hand over the cash. He hands you a bottle with five pills inside.")
            print("\n")
            type.type(quote("Take one a day. NO MORE. I know what I'm doing. I went to medical school."))
            print("\n")
            type.type("He pauses.")
            print("\n")
            type.type(quote("Well. I went TO one. I was visiting a friend. But I watched a lot."))
            print("\n")
            type.type("You take the pills. The relief hits within minutes. God, it's good.")
            p.heal(15)
            p.add_item("Feelgood Bottle")
            p.add_danger("Feelgood Dependency")
            p.meet("Bought Pills")
        else:
            type.type(quote("Your call. Pain is free. Relief costs money. That's just economics."))
            print("\n")
    else:
        type.type("You don't have $50. You tell him.")
        print("\n")
        type.type(quote("Hmm. Tell you what. I'll float you this time. But next time, you pay double. Deal?"))
        print("\n")
        answer = ask.yes_or_no("Accept the credit? ")
        if answer == "yes":
            type.type("He hands you three pills.")
            print("\n")
            type.type(quote("I'm a generous man. Don't make me a foolish one."))
            p.heal(10)
            p.add_danger("Feelgood Owes")
            p.add_danger("Feelgood Dependency")
            p.meet("Bought Pills")
        else:
            type.type(quote("Suit yourself. You know where to find me."))
            print("\n")
    print("\n")


def storyline_feelgood_price_up(p, sl):
    """Dr. Feelgood Part 3: The price doubles. He knows you need it."""
    sl.advance("dr_feelgood")
    
    type.type("You find Dr. Feelgood in his usual spot. But something's different. ")
    type.type("He's not smiling today. He's counting money.")
    print("\n")
    type.type(quote("Bad news, friend. My supplier raised prices. Supply chain issues. ") +
             quote("Inflation. The usual excuses."))
    print("\n")
    if p.has_danger("Feelgood Owes"):
        type.type(quote("Also, you owe me from last time. So this visit is $200. ") +
                 quote("$100 for the pills, $100 for what you already owe."))
        cost = 200
    else:
        type.type(quote("New price is $150. I know. I know. But I'm still cheaper than a hospital."))
        cost = 150
    print("\n")
    type.type("Your hands are shaking. Not from the cold. From the need.")
    print("\n")
    if p.get_balance() >= cost:
        answer = ask.yes_or_no("Pay ${:,}? ".format(cost))
        if answer == "yes":
            p.change_balance(-cost)
            type.type("You pay. He hands you a bottle. Fewer pills this time. Four instead of five.")
            print("\n")
            type.type(quote("I'm not the bad guy here. I'm the only one keeping you functional."))
            print("\n")
            type.type("He's right. Without the pills, you can barely move in the morning. ")
            type.type("When did that start?")
            p.heal(10)
            if p.has_danger("Feelgood Owes"):
                p.lose_danger("Feelgood Owes")
            p.meet("Feelgood Price Up")
        else:
            type.type("You refuse. Dr. Feelgood shrugs.")
            print("\n")
            type.type(quote("You'll be back. The body wants what the body wants."))
            print("\n")
            type.type("He's probably right.")
            p.lose_sanity(3)
    else:
        type.type("You don't have enough. You tell him. Beg him.")
        print("\n")
        type.type(quote("I'm a businessman, not a charity. Come back when you've got the cash."))
        print("\n")
        type.type("He packs up his bag and walks away. The withdrawal hits within hours. ")
        type.type("Sweating. Shaking. Your body screaming for something it didn't need two weeks ago.")
        p.hurt(10)
        p.lose_sanity(5)
    print("\n")


def storyline_feelgood_rock_bottom(p, sl):
    """Dr. Feelgood Part 4: Rock bottom. You're desperate."""
    sl.advance("dr_feelgood")
    
    type.type("It's been days since your last pill. The pain is unbearable. Not just the original pain — ")
    type.type("the new pain. The withdrawal pain. Your body punishing you for teaching it a shortcut.")
    print("\n")
    type.type("You find Dr. Feelgood, but he's not behind the gas station anymore. ")
    type.type("He's in the parking lot of a motel, leaning against a van with tinted windows.")
    print("\n")
    type.type(quote("Prices went up again. $300. And before you say anything — ") +
             quote("look at yourself. You need this."))
    print("\n")
    type.type("He's not wrong. Your hands are shaking so bad you can barely open a car door.")
    print("\n")
    
    if p.get_balance() >= 300:
        type.type("You have the money. Barely.")
        print("\n")
        answer = ask.choose_an_option("What do you do? ", ["Pay $300 for the pills", "Walk away cold turkey", "Threaten him"])
        if answer == 1:
            p.change_balance(-300)
            type.type("You hand over the money with trembling hands. He gives you a bottle.")
            print("\n")
            type.type(quote("Good choice. Smart choice."))
            print("\n")
            type.type("You take a pill right there in the parking lot. The relief is immediate. But it's not ")
            type.type("as good as it used to be. It takes the edge off, but the pain underneath is still there.")
            print("\n")
            type.type("This isn't working anymore. But you can't stop.")
            p.heal(5)
            p.lose_sanity(5)
            p.meet("Still Using")
        elif answer == 2:
            type.type("You turn around and walk away. Every step hurts. Every step is a war.")
            print("\n")
            type.type(quote("You'll be back! ") + "he shouts. " + quote("THEY ALWAYS COME BACK!"))
            print("\n")
            type.type("You don't look back. You get in your car and grip the steering wheel until ")
            type.type("your knuckles go white. The shaking gets worse before it gets better.")
            print("\n")
            type.type("But it does get better. Eventually. A little.")
            p.hurt(15)
            p.lose_sanity(3)
            p.meet("Cold Turkey")
        else:
            type.type("You grab his coat. He doesn't flinch.")
            print("\n")
            type.type(quote("Really? You're going to threaten the only person who's been helping you? ") +
                     quote("Go ahead. Hit me. Then what? I'm the supply, genius."))
            print("\n")
            type.type("He's right. You let go.")
            print("\n")
            type.type(quote("Tell you what. I've got a friend who needs a driver. ") +
                     quote("One delivery. No questions. He pays $500. Plenty left over for pills."))
            print("\n")
            answer2 = ask.yes_or_no("Do the delivery? ")
            if answer2 == "yes":
                type.type("You do the delivery. You don't ask what's in the box. It's heavy. It smells metallic.")
                print("\n")
                type.type("The drop-off is in a dark parking garage. A man in a suit takes the box without a word ")
                type.type("and hands you an envelope with $500.")
                print("\n")
                type.type("You go back to Feelgood. Buy the pills. Take one immediately.")
                print("\n")
                type.type("You have " + green(bright("$200")) + " left over. And something ugly on your conscience.")
                p.change_balance(200)
                p.heal(5)
                p.lose_sanity(8)
                p.add_danger("Did Feelgood's Delivery")
                p.meet("Still Using")
            else:
                type.type(quote("Fine. Suffer then. Your call."))
                print("\n")
                type.type("You walk away. Empty-handed. Hurting. But at least you didn't do ")
                type.type("whatever that delivery was.")
                p.meet("Cold Turkey")
    else:
        type.type("You don't have the money. Not even close.")
        print("\n")
        type.type(quote("Then we don't have a deal. Unless..."))
        print("\n")
        type.type("He describes the delivery job. One box. One drop-off. $500.")
        print("\n")
        answer = ask.yes_or_no("Do the delivery? ")
        if answer == "yes":
            type.type("You do the delivery. You don't ask questions. The $500 feels heavy in your pocket.")
            print("\n")
            type.type("Feelgood takes $300 and gives you the pills. You take one right away.")
            print("\n")
            type.type("You have " + green(bright("$200")) + " left. And a terrible feeling in your gut.")
            p.change_balance(200)
            p.heal(5)
            p.lose_sanity(8)
            p.add_danger("Did Feelgood's Delivery")
            p.meet("Still Using")
        else:
            type.type(quote("Suit yourself. Enjoy the shakes."))
            print("\n")
            type.type("He drives off in the van. You sit on the curb for a long time, shaking.")
            p.hurt(15)
            p.lose_sanity(5)
            p.meet("Cold Turkey")
    print("\n")


def storyline_feelgood_resolution(p, sl):
    """Dr. Feelgood Part 5: Resolution - one way or another."""
    sl.advance("dr_feelgood")
    sl.complete("dr_feelgood")
    
    if p.has_met("Cold Turkey"):
        # Went cold turkey - recovery path
        type.type("It's been days since you last saw Dr. Feelgood. The withdrawal was hell. ")
        type.type("Sweating, shaking, every nerve on fire. But you survived it.")
        print("\n")
        type.type("You're sitting in your car when you notice something on the passenger seat. ")
        type.type("A pamphlet. You've never seen it before.")
        print("\n")
        type.type(bright(yellow("\"RECOVERY IS A ROAD, NOT A DESTINATION\"")))
        print("\n")
        type.type("On the back, someone has written in pen: " + italic("\"I'm proud of you. -M\""))
        print("\n")
        if p.has_met("Martinez"):
            type.type("Martinez. Of course. He must have seen what was happening.")
            print("\n")
            type.type("You hold the pamphlet for a long time. Then you fold it carefully and put it ")
            type.type("in your glove box. You might need it again someday.")
        else:
            type.type("You don't know who M is. But somebody was watching. Somebody cared enough.")
        print("\n")
        type.type("The pain is back. The real pain, the one Feelgood was covering up. ")
        type.type("But at least it's honest pain now.")
        p.restore_sanity(10)
        p.heal(5)
        if p.has_danger("Feelgood Dependency"):
            p.lose_danger("Feelgood Dependency")
        
    elif p.has_met("Still Using"):
        # Still on the pills - crash landing
        type.type("You go looking for Dr. Feelgood, but his usual spots are empty. Behind the gas station — ")
        type.type("nothing. The motel parking lot — just oil stains where the van used to be.")
        print("\n")
        type.type("Finally, you find the gas station attendant who knows something.")
        print("\n")
        type.type(quote("That fake doctor? Cops picked him up two nights ago. Found his van full of... ") +
                 quote("well, let's just say it wasn't all aspirin."))
        print("\n")
        type.type("Your blood runs cold. Not because of Feelgood. Because of what happens next.")
        print("\n")
        type.type("The withdrawal hits that night. It's the worst yet. You can't sleep. ")
        type.type("You can't eat. Your body is in open revolt against its own owner.")
        print("\n")
        if p.has_danger("Did Feelgood's Delivery"):
            type.type("And somewhere in the back of your mind, you wonder: if Feelgood got caught, ")
            type.type("did he mention the delivery driver?")
            print("\n")
            type.type("You spend two days looking over your shoulder before the paranoia fades.")
            p.lose_sanity(5)
            p.add_danger("Delivery Paranoia")
        print("\n")
        type.type("It takes a week, but the shaking stops. The cravings dim. The real pain returns, ")
        type.type("but you've survived worse.")
        print("\n")
        type.type("You find a crumpled $20 bill in your pocket. Drug money, probably. ")
        type.type("You spend it on a decent meal. First solid food in days.")
        p.hurt(10)
        p.lose_sanity(3)
        if p.has_danger("Feelgood Dependency"):
            p.lose_danger("Feelgood Dependency")
    
    else:
        # Never got hooked - brief follow-up
        type.type("You hear through the grapevine that the man who called himself Dr. Feelgood ")
        type.type("was arrested behind the gas station with a van full of unlicensed pharmaceuticals.")
        print("\n")
        type.type(quote("That fake doctor? Yeah, they got him. Turns out he was selling horse tranquilizers ") +
                 quote("mixed with aspirin. People got real sick."))
        print("\n")
        type.type("You think about the pill he offered you. The one you turned down. Smart call.")
        p.restore_sanity(2)
    print("\n")

# =====================================================================
# JAMESON EXPANSION - 3 new parts (expansion of existing lone_cowboy)
# After the initial cowboy encounter (stage 0, handled by existing lone_cowboy)
# Stage 1: Horse trouble (Thunder gets sick)
# Stage 2: Rustlers (someone tries to steal Thunder)
# Stage 3: One last ride (Jameson says goodbye)
# =====================================================================

def storyline_jameson_horse_trouble(p, sl):
    """Jameson Part 2: Thunder is sick. The old cowboy needs help."""
    sl.advance("jameson")
    
    type.type("You hear hooves on asphalt before you see him. Jameson comes riding in on Thunder, ")
    type.type("but something's wrong. The horse is moving slowly, head drooping.")
    print("\n")
    type.type("Jameson dismounts with effort. He looks ten years older than last time.")
    print("\n")
    type.type(quote("Thunder ain't right. Been off his feed for three days. Won't drink water. ") +
             quote("Keeps lying down when he shouldn't."))
    print("\n")
    type.type("The old cowboy's voice cracks. This horse is his whole world.")
    print("\n")
    type.type(quote("I can't afford a vet. Not a real one. Those highway robbery sons of—"))
    print("\n")
    type.type("He takes off his hat and holds it to his chest.")
    print("\n")
    type.type(quote("You know anything about horses? Or know anyone who does?"))
    print("\n")
    
    if p.has_met("Tom"):
        answer = ask.yes_or_no("Suggest Trusty Tom might be able to help? ")
        if answer == "yes":
            type.type(quote("A mechanic? For a horse?"))
            print("\n")
            type.type(quote("Well... Tom IS good with everything else. Maybe he knows someone."))
            print("\n")
            type.type("You give Jameson directions to Tom's garage. The cowboy tips his hat.")
            print("\n")
            type.type(quote("I owe you, friend. If Tom can help Thunder, I owe you everything."))
            p.meet("Jameson Tom Help")
        else:
            type.type("You tell him you're sorry but you don't know anyone.")
            print("\n")
            type.type("Jameson nods slowly. He didn't expect much. People like him are used to that.")
    elif p.has_met("Dr. Feelgood"):
        type.type("You briefly consider mentioning the pill guy, then think better of it. ")
        type.type("Horse tranquilizers in reverse is probably not a thing.")
    print("\n")
    
    type.type("Jameson leads Thunder away on foot. The horse nuzzles against his shoulder. ")
    type.type("Even sick, they trust each other completely.")
    print("\n")
    
    if p.get_balance() >= 100:
        answer = ask.yes_or_no("Give Jameson $100 for vet bills? ")
        if answer == "yes":
            p.change_balance(-100)
            type.type("You press the money into Jameson's hand. He stares at it. Stares at you.")
            print("\n")
            type.type(quote("I... nobody's just... in thirty years, nobody's just..."))
            print("\n")
            type.type("He can't finish the sentence. He puts his hat on to hide his face.")
            print("\n")
            type.type(quote("Thank you. God bless you."))
            p.meet("Gave Jameson Money")
            p.restore_sanity(3)
        else:
            type.type("You wish him luck. It's all you can afford right now.")
    print("\n")


def storyline_jameson_rustlers(p, sl):
    """Jameson Part 3: Someone tries to steal Thunder."""
    sl.advance("jameson")
    
    type.type("A horse is screaming. That's not a sound you forget.")
    print("\n")
    type.type("Scrambling out of your car, you see it: two men with a trailer, trying to load Thunder. ")
    type.type("Jameson is on the ground, holding his ribs. They hit him.")
    print("\n")
    type.type("Thunder is rearing, kicking, refusing to go in the trailer. One man has a rope, ")
    type.type("the other has a prod.")
    print("\n")
    type.type(quote("That horse is worth five grand easy!") + " one of them yells. " +
             quote("Just get him in!"))
    print("\n")
    
    answer = ask.choose_an_option("What do you do? ", ["Help Jameson - charge in", "Honk your horn to scare them off", "Stay hidden and watch"])
    if answer == 1:
        type.type("You run at the closest one and tackle him into the gravel. It's not graceful. ")
        type.type("It's not heroic. You just crash into a man twice your size and hope for the best.")
        print("\n")
        type.type("Thunder, freed from the rope, rears up and kicks at the second man. ")
        type.type("His boot connects with the trailer door. CLANG.")
        print("\n")
        type.type("The rustlers decide a horse and a lunatic aren't worth the trouble. ")
        type.type("They pile into the truck and peel out, gravel flying.")
        print("\n")
        type.type("Jameson crawls to Thunder and wraps his arms around the horse's neck. ")
        type.type("Thunder stands perfectly still, as if he knows.")
        print("\n")
        type.type(quote("You saved my boy. You saved my Thunder."))
        print("\n")
        type.type("Jameson reaches into his saddlebag and pulls out something wrapped in oilcloth.")
        print("\n")
        type.type(quote("My granddaddy's. Carried it through two wars. I want you to have it."))
        print("\n")
        type.type("He hands you a beautiful " + item("Silver Horseshoe") + ".")
        print("\n")
        type.type(quote("It's lucky. Trust me. Luckier than anything you'll find in a casino."))
        p.add_item("Silver Horseshoe")
        p.heal(5)
        p.restore_sanity(5)
        p.meet("Saved Thunder")
        p.hurt(10)  # You got banged up in the scuffle
    elif answer == 2:
        type.type("You lean on the horn. HOOOOOONK. The sound tears through the night.")
        print("\n")
        type.type("Headlights. Horn. You flip on your high beams for good measure.")
        print("\n")
        type.type("The rustlers panic. One drops the rope and sprints for the truck. ")
        type.type("The other follows. They're gone in seconds, trailer bouncing behind them.")
        print("\n")
        type.type("Thunder trots over to Jameson and stands guard over the old man like a sentinel.")
        print("\n")
        type.type("Jameson manages a smile from the ground.")
        print("\n")
        type.type(quote("Quick thinking. That's the car sleeper way."))
        print("\n")
        type.type("He reaches into his pocket and hands you " + green(bright("$75")) + ".")
        print("\n")
        type.type(quote("All I got. Take it. You earned it."))
        p.change_balance(75)
        p.restore_sanity(3)
        p.meet("Saved Thunder")
    else:
        type.type("You stay in your car, doors locked. You watch through the window as the men ")
        type.type("struggle with the horse.")
        print("\n")
        type.type("Thunder fights them off on his own. A kick sends one man flying into the trailer wall. ")
        type.type("They eventually give up and drive away.")
        print("\n")
        type.type("Jameson lies on the ground for a long time. When he finally gets up, ")
        type.type("he looks around. He sees your car. He knows you were there.")
        print("\n")
        type.type("He doesn't wave. He doesn't nod. He just leads Thunder away in silence.")
        print("\n")
        type.type("You feel the weight of what you didn't do.")
        p.lose_sanity(5)
    print("\n")


def storyline_jameson_last_ride(p, sl):
    """Jameson Part 4: The cowboy says goodbye."""
    sl.advance("jameson")
    sl.complete("jameson")
    
    type.type("You find Jameson sitting under a tree. Thunder is grazing nearby, looking healthy. ")
    if p.has_met("Jameson Tom Help"):
        type.type("Whatever Tom did, it worked.")
    else:
        type.type("The old horse recovered on his own. Stubborn, just like his owner.")
    print("\n")
    type.type("Jameson's got a small fire going. He pats the ground next to him.")
    print("\n")
    type.type(quote("Sit. I wanna tell you something."))
    print("\n")
    type.type("You sit. The fire crackles.")
    print("\n")
    type.type(quote("I've been riding this stretch of road for fifteen years. Before that, I was a rancher. ") +
             quote("Before that, I was a soldier. Before that, I was a kid who thought cowboys lived forever."))
    print("\n")
    type.type("He pokes the fire with a stick.")
    print("\n")
    type.type(quote("Cowboys don't live forever. Turns out, nobody does. But Thunder and me, ") +
             quote("we got some good years in. Rode every back road in the state. ") +
             quote("Slept under every star. Ate more gas station burritos than any human should survive."))
    print("\n")
    type.type("He laughs. It turns into a cough.")
    print("\n")
    type.type(quote("We're heading south. Mexico, maybe. Somewhere warm. Thunder's old bones ") +
             quote("don't like the cold anymore. Neither do mine."))
    print("\n")
    if p.has_met("Saved Thunder"):
        type.type("He looks at you with eyes that have seen everything.")
        print("\n")
        type.type(quote("You saved my horse. My best friend. I won't forget that as long as I live. ") +
                 quote("And Thunder won't either. Horses remember."))
        print("\n")
        type.type("He reaches into his saddlebag one last time.")
        print("\n")
        type.type(quote("Here. My riding jacket. It's old, it's beaten up, it smells like horse. ") +
                 quote("But it's warm and it's lucky."))
        print("\n")
        type.type("He hands you a worn leather " + item("Cowboy Jacket") + ".")
        p.add_item("Cowboy Jacket")
        p.restore_sanity(5)
    else:
        type.type(quote("Take care of yourself out here. The road's long but it ain't forever."))
    print("\n")
    type.type("Jameson mounts Thunder with the ease of a man who's done it ten thousand times. ")
    type.type("He tips his hat one last time.")
    print("\n")
    type.type(quote("Adios, friend. May your cards run lucky and your engine run clean."))
    print("\n")
    type.type("Man and horse ride south until they're just a silhouette against the sunset. ")
    type.type("Then they're gone.")
    print("\n")
    type.type("You sit by the dying fire for a long time, watching the last embers glow.")
    p.restore_sanity(3)
    p.heal(5)
    print("\n")

# =====================================================================
# STUART THE SHADY APPRENTICE - 4 parts
# Oswald's apprentice who's running side deals behind his back.
# Stage 0: Psst (Stuart approaches you with a deal)
# Stage 1: Good deal (it pays off, builds trust)
# Stage 2: Bad deal (he brings you something dangerous)
# Stage 3: Oswald finds out (the confrontation)
# =====================================================================

def storyline_stuart_psst(p, sl):
    """Stuart Part 1: Oswald's apprentice has a side hustle."""
    p.meet("Stuart")
    sl.advance("stuart")
    
    type.type("You're leaving Oswald's shop when someone hisses at you from the alley.")
    print("\n")
    type.type(quote("Psst! Hey! Over here!"))
    print("\n")
    type.type("A scrawny kid, maybe 17, wearing an oil-stained apron with " + cyan(bright("OSWALD'S AUTO")) + 
             " embroidered on it, waves you over.")
    print("\n")
    type.type(quote("You're one of Oswald's regulars, right? I'm Stuart. His apprentice. ") +
             quote("Well, 'apprentice.' He calls me that. I call myself an underpaid genius."))
    print("\n")
    type.type("He looks over his shoulder nervously.")
    print("\n")
    type.type(quote("Look, Oswald's prices are insane, right? I can get you the same parts for half the cost. ") +
             quote("Same quality, just... you know... through different channels."))
    print("\n")
    type.type(quote("Nothing illegal! Probably! Just... surplus. Excess. Fell-off-a-truck kind of stuff."))
    print("\n")
    answer = ask.yes_or_no("Are you interested? ")
    if answer == "yes":
        type.type("Stuart grins like a kid who just found a $20 bill.")
        print("\n")
        type.type(quote("I KNEW you were cool. Here, take my number."))
        print("\n")
        type.type("He scribbles a number on a receipt and hands it to you.")
        print("\n")
        type.type(quote("Don't tell Oswald. He'd kill me. Not literally. Well... actually, maybe literally."))
        p.add_item("Stuart's Number")
        p.meet("Stuart Deal")
    else:
        type.type(quote("Fine, fine. But when Oswald charges you $500 for a brake pad, ") +
                 quote("don't come crying to me."))
        print("\n")
        type.type("He slinks back into the alley. You notice he's wearing sneakers two sizes too big.")
    print("\n")


def storyline_stuart_good_deal(p, sl):
    """Stuart Part 2: His deal actually pays off."""
    sl.advance("stuart")
    
    type.type("Stuart catches you in the parking lot, practically vibrating with excitement.")
    print("\n")
    type.type(quote("Okay, okay, I got something good. Real good."))
    print("\n")
    type.type("He opens his jacket to reveal a car part you vaguely recognize. It's clean, shiny, ")
    type.type("and has a brand name on it that you've seen at Oswald's for triple the price.")
    print("\n")
    type.type(quote("This is a premium alternator belt. Oswald sells these for $200. I'm offering it ") +
             quote("to you for $50. FIFTY BUCKS. That's not a deal, that's a crime. Wait, no. ") +
             quote("It's NOT a crime. Poor choice of words."))
    print("\n")
    if p.get_balance() >= 50:
        answer = ask.yes_or_no("Buy it for $50? ")
        if answer == "yes":
            p.change_balance(-50)
            type.type("You hand over the cash. Stuart installs it right there in the parking lot, ")
            type.type("using tools he definitely borrowed from Oswald's shop.")
            print("\n")
            type.type("It works perfectly. Your car runs smoother than it has in weeks.")
            print("\n")
            type.type(quote("See? GENIUS. I told you. Underpaid genius."))
            print("\n")
            type.type("He pockets the money with a grin that could sell ice to an Eskimo.")
            p.meet("Stuart Bought Part")
            # Fix a random car danger if they have one
            for danger in ["Engine Knock", "Alternator Failing", "Strange Engine Noise"]:
                if p.has_danger(danger):
                    p.lose_danger(danger)
                    type.type("The new part fixed your " + red(danger) + " problem!")
                    print("\n")
                    break
        else:
            type.type(quote("Your loss. I'll sell it to someone with taste."))
    else:
        type.type("You don't have $50. Stuart's face falls.")
        print("\n")
        type.type(quote("Okay, rain check. I'll hold it for you. Maybe. No promises."))
    print("\n")


def storyline_stuart_bad_deal(p, sl):
    """Stuart Part 3: This time, the deal goes wrong."""
    sl.advance("stuart")
    
    type.type("Stuart is waiting by your car when you get back. He's pacing. Sweating.")
    print("\n")
    type.type(quote("Hey. Hey hey hey. I need a favor. Big favor."))
    print("\n")
    type.type("He opens the trunk of a car you've never seen before. Inside is a box that's making ")
    type.type("a low humming sound.")
    print("\n")
    type.type(quote("So remember when I said my stuff was surplus? Well, THIS surplus might be ") +
             quote("slightly more... industrial. Like, it might have come from a place that had ") +
             quote("security cameras."))
    print("\n")
    type.type("He wipes his forehead.")
    print("\n")
    type.type(quote("I need you to hold it for one day. Just ONE day. Then my buyer picks it up and ") +
             quote("we split the money. $500 for you. Easy."))
    print("\n")
    type.type("The box hums louder. Whatever is in there is probably worth more than your car.")
    print("\n")
    answer = ask.yes_or_no("Hold the box for Stuart? ")
    if answer == "yes":
        type.type("Stuart shoves the box into your back seat and sprints away before you can change your mind.")
        print("\n")
        type.type(quote("You're the BEST! I'll be back tomorrow! DON'T OPEN IT!"))
        print("\n")
        type.type("The box hums in your back seat all night. You don't sleep.")
        print("\n")
        type.type("True to his word, Stuart returns the next day. A man in a van takes the box. ")
        type.type("Stuart hands you " + green(bright("$500")) + ".")
        print("\n")
        type.type(quote("Pleasure doing business. We should do this more often."))
        print("\n")
        type.type("Something about the way he says 'more often' makes your stomach drop.")
        p.change_balance(500)
        p.lose_sanity(5)
        p.meet("Stuart Box")
        p.add_danger("Stuart's Partner")
    else:
        type.type(quote("Come ON! I thought we were partners!"))
        print("\n")
        type.type("Stuart grabs the box himself, grunting under its weight, and staggers off.")
        print("\n")
        type.type("You watch him try to fit it into the passenger seat of a Honda Civic. ")
        type.type("It takes him eleven minutes.")
        print("\n")
        type.type("Smart move. Probably.")
    print("\n")


def storyline_stuart_oswald_finds_out(p, sl):
    """Stuart Part 4: Oswald discovers Stuart's side business."""
    sl.advance("stuart")
    sl.complete("stuart")
    
    type.type("You pull into Oswald's shop for a routine visit and walk into a scene. ")
    type.type("Oswald is holding Stuart by the collar of his apron, lifting the kid clean off the ground.")
    print("\n")
    type.type("Oswald is a big man. Stuart is not.")
    print("\n")
    type.type(quote("You've been stealing from ME?! Using MY tools?! Selling parts out of MY shop?!"))
    print("\n")
    type.type("Stuart is dangling, feet kicking.")
    print("\n")
    type.type(quote("It wasn't— I didn't— it was SURPLUS—"))
    print("\n")
    type.type(quote("SURPLUS?! I COUNTED those parts, Stuart! You think I'm STUPID?!"))
    print("\n")
    type.type("Oswald sees you standing in the doorway. He sets Stuart down (roughly) ")
    type.type("and straightens his own shirt.")
    print("\n")
    
    if p.has_met("Stuart Box"):
        type.type(quote("You. You were part of this, weren't you? Stuart told me everything."))
        print("\n")
        type.type("Stuart, from the floor: " + quote("I did NOT—"))
        print("\n")
        type.type(quote("SHUT UP, Stuart."))
        print("\n")
        answer = ask.yes_or_no("Tell the truth about your involvement? ")
        if answer == "yes":
            type.type("You come clean. The parts, the box, the $500. All of it.")
            print("\n")
            type.type("Oswald stares at you for a long time. Then he sighs the deepest sigh ")
            type.type("you've ever heard from a human being.")
            print("\n")
            type.type(quote("You know what? At least you're honest. Stuart could learn from that."))
            print("\n")
            type.type("Stuart: " + quote("Hey—"))
            print("\n")
            type.type(quote("Stuart. You're fired. Get out. And leave my wrench."))
            print("\n")
            type.type("Stuart slinks away, leaving a greasy wrench on the counter.")
            print("\n")
            type.type("Oswald turns to you.")
            print("\n")
            type.type(quote("You owe me for those parts. But I respect the honesty. ") +
                     quote("We'll call it even if you bring me something useful next time you're in."))
            p.restore_sanity(3)
        else:
            type.type(quote("I don't know anything about Stuart's side deals."))
            print("\n")
            type.type("Oswald narrows his eyes. He doesn't believe you, but he can't prove it.")
            print("\n")
            type.type(quote("Fine. But if I find out otherwise..."))
            print("\n")
            type.type("He cracks his knuckles. Point made.")
            p.lose_sanity(2)
    elif p.has_met("Stuart Deal"):
        type.type(quote("You know this kid? He said you were one of his 'customers.'"))
        print("\n")
        answer = ask.yes_or_no("Defend Stuart? ")
        if answer == "yes":
            type.type(quote("He sold me one part. It was good quality. And he's just a kid trying to make a buck."))
            print("\n")
            type.type("Oswald loosens his grip on Stuart's collar.")
            print("\n")
            type.type(quote("...He's a good mechanic. I'll give him that. Best hands I've seen in twenty years."))
            print("\n")
            type.type("He lets go of Stuart completely.")
            print("\n")
            type.type(quote("Last chance, kid. ONE more stunt and you're done. Understand?"))
            print("\n")
            type.type("Stuart nods so fast his head might come off.")
            print("\n")
            type.type(quote("Thank you thank you thank you—"))
            print("\n")
            type.type(quote("And you're working Saturdays. For free. For six months."))
            print("\n")
            type.type("Stuart deflates. But he's still employed. He mouths " + quote("thank you") + " to you.")
            p.restore_sanity(3)
        else:
            type.type(quote("Never seen this kid before."))
            print("\n")
            type.type("Stuart's jaw drops. Betrayal.")
            print("\n")
            type.type("Oswald fires him on the spot. Stuart leaves without looking at you.")
    else:
        type.type("You're just a bystander watching a very large man yell at a very small teenager.")
        print("\n")
        type.type("Oswald fires Stuart. The kid walks out in silence, untying his apron as he goes.")
        print("\n")
        type.type("Oswald shakes his head.")
        print("\n")
        type.type(quote("Good mechanic. Terrible human being. Anyway, what can I fix for you today?"))
    print("\n")

# =====================================================================
# GRANDMA'S PHONE CALLS - 5 parts
# A phone number you found leads to a sweet old woman who thinks you're her grandson.
# You never correct her. She never asks.
# Stage 0: First call (you dial the number, she answers)
# Stage 1: The recipe (she reads you a recipe over the phone)
# Stage 2: Bad news (she's in the hospital)
# Stage 3: The gift (a package arrives)
# Stage 4: Last call (she says goodbye her way)
# =====================================================================

def storyline_grandma_first_call(p, sl):
    """Grandma Part 1: You dial the number. A sweet old woman answers."""
    p.meet("Grandma")
    sl.advance("grandma")
    
    type.type("You've been carrying " + item("Grandma's Number") + " around for a while now. ")
    type.type("A scrap of paper with a phone number and the words " + italic("\"Call me sometime. -G\""))
    print("\n")
    type.type("Something about it nags at you. You stare at it, sitting in your car, ")
    type.type("thumb hovering over your phone.")
    print("\n")
    answer = ask.yes_or_no("Call the number? ")
    if answer == "yes":
        type.type("The phone rings. Once. Twice. Three times. You're about to hang up when—")
        print("\n")
        type.type(quote("Hello? Who is this?"))
        print("\n")
        type.type("The voice is old. Warm. Like cinnamon and wool blankets.")
        print("\n")
        type.type(quote("...Tommy? Is that you? Oh, Tommy, I've been waiting for you to call! ") +
                 quote("It's been so long, sweetheart!"))
        print("\n")
        type.type("Your name isn't Tommy. But something about the way she says it — the relief, ")
        type.type("the love — makes you hesitate.")
        print("\n")
        answer2 = ask.yes_or_no("Do you correct her? ")
        if answer2 == "yes":
            type.type(quote("Ma'am, I'm not Tommy. I found this number and—"))
            print("\n")
            type.type("Long pause.")
            print("\n")
            type.type(quote("Oh. I see. Well... that's alright, dear. It's nice to hear a voice ") +
                     quote("either way. It gets quiet here."))
            print("\n")
            type.type("Somehow, that's worse.")
            print("\n")
            type.type(quote("Would you call again sometime? Even though you're not Tommy? ") +
                     quote("I don't mind. I just like the company."))
            p.meet("Grandma Honest")
        else:
            type.type(quote("...Yeah, Grandma. It's me."))
            print("\n")
            type.type(quote("OH! Oh, Tommy! I'm so happy! How are you, sweetheart? Are you eating? ") +
                     quote("You sound thin. I can hear it in your voice."))
            print("\n")
            type.type("You talk for twenty minutes. She tells you about her garden (tomatoes are coming in), ")
            type.type("her cat (Mr. Whiskers caught a bird), and her neighbor (Harold is noisy).")
            print("\n")
            type.type("You don't say much. You don't need to. She fills the silence with love.")
            p.restore_sanity(5)
        print("\n")
        type.type(quote("Call me again soon, okay? Promise me."))
        print("\n")
        type.type(quote("I promise."))
        print("\n")
        type.type("You hang up. Your car is quiet. But it feels less empty.")
    else:
        type.type("You put the number back in your pocket. Not today. Maybe tomorrow.")
        print("\n")
        type.type("Tomorrow you'll definitely call. Probably.")
    print("\n")


def storyline_grandma_recipe(p, sl):
    """Grandma Part 2: She reads you a recipe over the phone."""
    sl.advance("grandma")
    
    type.type("Your phone rings. Unknown number, but you recognize it.")
    print("\n")
    type.type(quote("Tommy? I know you're busy but I need to tell you something important."))
    print("\n")
    if p.has_met("Grandma Honest"):
        type.type("She knows you're not Tommy. She calls you Tommy anyway. You've stopped correcting her.")
        print("\n")
    type.type(quote("I found your grandfather's secret chili recipe. The one he never let anyone see. ") +
             quote("I want to read it to you before I forget where I put it."))
    print("\n")
    type.type("She starts reading. The recipe is absurdly complicated. It involves three kinds of peppers, ")
    type.type("a specific brand of tomato paste that went out of business in 1997, and — somehow — nutmeg.")
    print("\n")
    type.type(quote("Now this is the important part. You stir it counter-clockwise for exactly seven minutes. ") +
             quote("Your grandfather said clockwise makes it bitter. I don't know if that's true ") +
             quote("but he won the county fair fourteen years in a row, so who am I to argue?"))
    print("\n")
    answer = ask.yes_or_no("Write down the recipe? ")
    if answer == "yes":
        type.type("You scribble furiously on a napkin. She's going fast for an 87-year-old.")
        print("\n")
        type.type(quote("Did you get the part about the nutmeg? A PINCH, Tommy. Not a spoonful. ") +
                 quote("Your father ruined Thanksgiving '03 with too much nutmeg."))
        print("\n")
        type.type("You now have " + item("Grandpa's Chili Recipe") + " written on a gas station napkin.")
        p.add_item("Grandpa's Chili Recipe")
        p.meet("Got Recipe")
    else:
        type.type("You listen but don't write it down. It doesn't matter. The recipe isn't the point.")
        print("\n")
    type.type(quote("I wish you could come visit. I'd make it for you. The house smells like home ") +
             quote("when chili's on the stove."))
    print("\n")
    type.type("Silence. The kind that means something.")
    print("\n")
    type.type(quote("I love you, Tommy."))
    print("\n")
    type.type(quote("I love you too, Grandma."))
    print("\n")
    type.type("You mean it. And that surprises you more than anything else that's happened out here.")
    p.restore_sanity(5)
    p.heal(3)
    print("\n")


def storyline_grandma_bad_news(p, sl):
    """Grandma Part 3: Grandma's in the hospital."""
    sl.advance("grandma")
    
    type.type("Your phone rings. It's not Grandma's number. It's a hospital.")
    print("\n")
    type.type(quote("Hello, we're trying to reach family members of Eleanor Patterson. ") +
             quote("Your number was listed in her phone as 'Tommy.'"))
    print("\n")
    type.type("Your heart drops.")
    print("\n")
    type.type(quote("Mrs. Patterson had a fall. She's stable, but she's asking for Tommy. ") +
             quote("She's very insistent."))
    print("\n")
    type.type("You're not Tommy. You've never been Tommy. But Eleanor is lying in a hospital bed ")
    type.type("asking for someone and you're the only one answering.")
    print("\n")
    
    # Check if player has enough for a phone card / gas
    type.type("The hospital is three towns over. That's gas money you might not have.")
    print("\n")
    if p.get_balance() >= 100:
        answer = ask.yes_or_no("Drive to the hospital to visit her? ($100 gas money) ")
        if answer == "yes":
            p.change_balance(-100)
            type.type("You drive. It takes two hours. The hospital smells like bleach and regret.")
            print("\n")
            type.type("You find Eleanor in room 312. She's tiny in the bed. White hair spread on the pillow ")
            type.type("like a cloud. Mr. Whiskers' photo is taped to the side rail.")
            print("\n")
            type.type("She sees you and smiles. The biggest smile you've ever seen on a human face.")
            print("\n")
            type.type(quote("Tommy! You came! You actually came!"))
            print("\n")
            type.type("She reaches for your hand. Her fingers are cold but her grip is strong.")
            print("\n")
            type.type(quote("I knew you'd come. I told Harold's wife — he's in room 310, still noisy — ") +
                     quote("I said 'my Tommy will come.' And here you are."))
            print("\n")
            type.type("You hold her hand for an hour. She tells you about the fall (tripped on Mr. Whiskers), ")
            type.type("the food (terrible), and the nurses (lovely, except Sharon).")
            print("\n")
            type.type("When she falls asleep, you slip out quietly. A nurse stops you at the door.")
            print("\n")
            type.type(quote("Are you Tommy? Her son?"))
            print("\n")
            type.type(quote("...Yeah."))
            print("\n")
            type.type(quote("She talks about you all the time. She says you're a good boy."))
            print("\n")
            type.type("You walk to your car and sit there for a while. Breathing.")
            p.restore_sanity(8)
            p.heal(5)
            p.meet("Visited Grandma")
        else:
            type.type("You can't. You just can't. The gas, the time, the lie you'd have to maintain in person...")
            print("\n")
            type.type("You call the hospital back and ask them to put you through to her room.")
            print("\n")
            type.type(quote("Tommy? Is that you?"))
            print("\n")
            type.type(quote("Yeah, Grandma. I'm sorry I can't come. But I'm here. On the phone. I'm here."))
            print("\n")
            type.type("She talks until the nurse makes her rest. You listen to every word.")
            p.restore_sanity(3)
    else:
        type.type("You can't afford the gas. So you call the hospital and ask to be transferred.")
        print("\n")
        type.type(quote("Tommy? Oh, Tommy, I had a fall. Mr. Whiskers tripped me. Don't be mad at him."))
        print("\n")
        type.type(quote("I'm not mad at Mr. Whiskers, Grandma."))
        print("\n")
        type.type("You talk until visiting hours end. It's not the same as being there. But it's something.")
        p.restore_sanity(3)
    print("\n")


def storyline_grandma_gift(p, sl):
    """Grandma Part 4: A package arrives addressed to 'Tommy.'"""
    sl.advance("grandma")
    
    type.type("You find a package sitting on the hood of your car. Brown paper, twine, ")
    type.type("and the kind of handwriting that only exists on letters from grandparents.")
    print("\n")
    type.type(italic("\"To Tommy. From Grandma. Don't open until you need it.\""))
    print("\n")
    type.type("You open it immediately. You need it now.")
    print("\n")
    type.type("Inside is a hand-knitted " + item("Grandma's Scarf") + " in the worst color combination ")
    type.type("you've ever seen. Purple and orange stripes with little green stars. It's hideous.")
    print("\n")
    type.type("It's perfect.")
    print("\n")
    type.type("There's also an envelope. Inside: " + green(bright("$200")) + " in small bills, ")
    type.type("a photo of a young man standing next to a Buick, and a note:")
    print("\n")
    type.type(italic("\"The boy in the photo is the real Tommy. My son. He left twenty years ago ") +
             italic("and never called. I know you're not him. I've known since the first call.\""))
    print("\n")
    type.type(italic("\"I don't care. You called. You listened. You came when I fell.\"") if p.has_met("Visited Grandma")
             else italic("\"I don't care. You called. You listened. That's more than he ever did.\""))
    print("\n")
    type.type(italic("\"The scarf is warm. The money is for gas. The photo is so you know ") +
             italic("what kindness looks like when it grows up.\""))
    print("\n")
    type.type(italic("\"Love, Eleanor\""))
    print("\n")
    p.add_item("Grandma's Scarf")
    p.change_balance(200)
    p.restore_sanity(8)
    p.heal(5)
    
    if p.has_met("Got Recipe"):
        type.type("P.S. — " + italic("\"The real secret ingredient in the chili is love. ") +
                 italic("Your grandfather would have liked you.\""))
        print("\n")
    print("\n")


def storyline_grandma_last_call(p, sl):
    """Grandma Part 5: The last phone call."""
    sl.advance("grandma")
    sl.complete("grandma")
    
    type.type("Your phone rings. It's Grandma's number. But the voice on the other end isn't hers.")
    print("\n")
    type.type(quote("Hello? Is this Tommy?"))
    print("\n")
    type.type("It's a woman. Younger. Maybe a neighbor.")
    print("\n")
    type.type(quote("I'm Margaret. I live next door to Eleanor. She asked me to call you."))
    print("\n")
    type.type("Pause.")
    print("\n")
    type.type(quote("She's... she's not doing well, Tommy. She wanted me to tell you some things ") +
             quote("while she still can. She's right here. I'm going to hold the phone for her."))
    print("\n")
    type.type("Rustling. Then that voice. Weaker now, but still warm.")
    print("\n")
    type.type(quote("Tommy?"))
    print("\n")
    type.type(quote("I'm here, Grandma."))
    print("\n")
    type.type(quote("Good. Good. I need you to know something."))
    print("\n")
    type.type("She takes a breath that sounds like it costs her everything.")
    print("\n")
    type.type(quote("You are the best thing that happened to me in twenty years. ") +
             quote("I don't care what your real name is. To me, you're Tommy. ") +
             quote("My Tommy. The one who called. The one who listened."))
    print("\n")
    type.type("Your eyes are burning.")
    print("\n")
    type.type(quote("I want you to promise me something."))
    print("\n")
    type.type(quote("Anything."))
    print("\n")
    type.type(quote("Be kind. That's it. Just be kind. The world is full of people who forgot ") +
             quote("how to be kind. You didn't forget. Don't start now."))
    print("\n")
    type.type("Long silence. You can hear her breathing. Mr. Whiskers is purring in the background.")
    print("\n")
    type.type(quote("I love you, Tommy."))
    print("\n")
    type.type(quote("I love you too, Grandma."))
    print("\n")
    type.type("Click.")
    print("\n")
    type.type("Margaret calls you back a week later. Eleanor passed peacefully in her sleep. ")
    type.type("Mr. Whiskers was on the pillow next to her.")
    print("\n")
    
    if p.has_met("Visited Grandma"):
        type.type("In her will, she left everything to 'Tommy.' The house, the garden, Mr. Whiskers. ")
        type.type("Margaret is keeping the cat until you 'settle down.'")
        print("\n")
        type.type("You don't know if you'll ever settle down. But you keep Grandma's scarf around your neck ")
        type.type("and the recipe in your glove box, and somehow the road feels less lonely.")
    else:
        type.type("Margaret says Eleanor left you something in a safety deposit box. ")
        type.type("You can't get to it. But knowing it exists is enough.")
    print("\n")
    type.type("You pull over and sit for a while. The scarf smells like cinnamon.")
    p.restore_sanity(10)
    p.heal(10)
    print("\n")

# =====================================================================
# LUCKY DOG - 4 parts (after befriending Lucky as a companion)
# Stage 0: Who hurt you (Lucky has scars and a past)
# Stage 1: Previous owner (someone comes looking for Lucky)
# Stage 2: Good boy (Lucky learns to trust)
# Stage 3: Saves your life (Lucky returns the favor)
# =====================================================================

def storyline_lucky_who_hurt_you(p, sl):
    """Lucky Part 1: You notice Lucky's scars."""
    sl.advance("lucky_dog")
    
    type.type("You're petting Lucky when you notice something you've been trying to ignore. ")
    type.type("Scars. Under the fur. Old ones, healed over but raised and rough.")
    print("\n")
    type.type("Lucky flinches when you touch them. Not a pain flinch — a memory flinch.")
    print("\n")
    type.type("There are more on his belly. His back legs. Someone did this to him. ")
    type.type("Deliberately. Repeatedly.")
    print("\n")
    type.type("Lucky rolls over and looks at you with those big brown eyes. ")
    type.type("He doesn't understand why you stopped petting him. He just wants more.")
    print("\n")
    answer = ask.yes_or_no("Keep petting him? ")
    if answer == "yes":
        type.type("You pet him. Carefully. Around the scars. He closes his eyes and sighs — ")
        type.type("the deep, full-body sigh of an animal that's finally, FINALLY safe.")
        print("\n")
        type.type(quote("I don't know who hurt you, boy. But they're gone now. You're with me."))
        print("\n")
        type.type("Lucky licks your hand. His tail thumps against the ground like a heartbeat.")
        p.restore_sanity(3)
    else:
        type.type("You pull your hand back. Lucky whimpers. He thinks he did something wrong.")
        print("\n")
        type.type("You reach back out and scratch his ears. He forgives instantly. Dogs are better than people.")
    print("\n")
    type.type("You make a silent promise: whatever happened to this dog before, it's not happening again.")
    p.meet("Lucky Scars")
    print("\n")


def storyline_lucky_previous_owner(p, sl):
    """Lucky Part 2: Someone comes looking for their 'property.'"""
    sl.advance("lucky_dog")
    
    type.type("You're sitting in your car with Lucky curled up on the passenger seat when a truck ")
    type.type("pulls up alongside you. A big truck. Mud-splattered. Dog crates in the back.")
    print("\n")
    type.type("The driver rolls down his window. Thick neck, sunburned face, mean eyes.")
    print("\n")
    type.type(quote("Hey. That's my dog."))
    print("\n")
    type.type("Lucky, who was sleeping, is suddenly rigid. His ears go flat. His tail tucks. ")
    type.type("He pushes himself as far back in the seat as possible.")
    print("\n")
    type.type("He recognizes this man. And he's terrified.")
    print("\n")
    type.type(quote("That mutt ran off three months ago. I've been looking everywhere. ") +
             quote("Hand him over."))
    print("\n")
    type.type("Lucky is shaking. Full-body trembling. He's pressing against you like you're a wall ")
    type.type("between him and the worst thing in his world.")
    print("\n")
    
    answer = ask.choose_an_option("What do you do? ", ["Refuse - Lucky stays with you", "Tell him to prove it", "Give Lucky back"])
    if answer == 1:
        type.type(quote("He's not your dog anymore. He's mine."))
        print("\n")
        type.type("The man's face darkens.")
        print("\n")
        type.type(quote("Listen here, you little— I got papers. That's a registered fighting dog. ") +
                 quote("He's worth money."))
        print("\n")
        type.type("Fighting dog. Those scars make sense now.")
        print("\n")
        type.type(quote("He's not fighting anyone anymore. Get out of here."))
        print("\n")
        type.type("The man sizes you up. Lucky growls — low, rumbling, a sound you've never heard from him. ")
        type.type("The man sees the dog's teeth and remembers why he trained them to fight.")
        print("\n")
        type.type(quote("This ain't over."))
        print("\n")
        type.type("He drives off. Lucky stops shaking five minutes later. You hold him the whole time.")
        p.add_danger("Lucky's Owner")
        p.restore_sanity(5)
        p.meet("Protected Lucky")
    elif answer == 2:
        type.type(quote("Prove it. Show me the papers."))
        print("\n")
        type.type("The man sputters. He clearly doesn't have papers.")
        print("\n")
        type.type(quote("I don't need papers! That's MY dog! Look, he's got the scar on his left ear — ") +
                 quote("I know because I— because he got it in a—"))
        print("\n")
        type.type("He stops. He almost admitted to something. You stare at him. He stares back.")
        print("\n")
        type.type(quote("...Fine. Keep the mutt. He was useless anyway."))
        print("\n")
        type.type("He guns the engine and tears out of the parking lot. Gravel sprays everywhere.")
        print("\n")
        type.type("Lucky licks your face. Relief. Pure, tail-wagging relief.")
        p.restore_sanity(3)
        p.meet("Protected Lucky")
    else:
        type.type("You open the door. Lucky looks at you with those eyes. He knows what's happening.")
        print("\n")
        type.type("He doesn't move. He just looks at you. Asking you. Begging you.")
        print("\n")
        type.type("The man reaches for Lucky's collar—")
        print("\n")
        type.type("Lucky bites him. Hard. The man screams and jerks his hand back, bleeding.")
        print("\n")
        type.type(quote("CRAZY MUTT! Keep him! He's defective! Worthless!"))
        print("\n")
        type.type("He peels out, cradling his bleeding hand. Lucky is still sitting in your car, ")
        type.type("looking at you with an expression that says: " + italic("\"I chose you. Don't make me regret it.\""))
        print("\n")
        type.type("You close the door. You pet his head. You never try to give him away again.")
        p.lose_sanity(5)
        p.restore_sanity(3)
        p.meet("Protected Lucky")
    print("\n")


def storyline_lucky_good_boy(p, sl):
    """Lucky Part 3: Lucky learns to fully trust you."""
    sl.advance("lucky_dog")
    
    type.type("Lucky has changed. You can see it in the way he moves — less flinching, more trotting. ")
    type.type("His tail is up now. It used to stay tucked.")
    print("\n")
    type.type("Today, something new happens. You're eating lunch (gas station sandwich, again) ")
    type.type("when Lucky nudges his nose against your hand.")
    print("\n")
    type.type("He drops something at your feet. It's a rock. A smooth, flat, river stone.")
    print("\n")
    type.type("He looks at you. Tail wagging. Expectant.")
    print("\n")
    type.type("He wants you to throw it.")
    print("\n")
    answer = ask.yes_or_no("Throw the rock? ")
    if answer == "yes":
        type.type("You throw it. Lucky EXPLODES after it. Legs pumping, ears flying, tongue out. ")
        type.type("He's a rocket with fur.")
        print("\n")
        type.type("He brings it back. Drops it at your feet. Tail going so fast it's a blur.")
        print("\n")
        type.type("You throw it again. And again. And again. For thirty minutes, ")
        type.type("you're not a person living in their car. You're just a person playing with a dog.")
        print("\n")
        type.type("When he's finally tired, Lucky curls up next to you. Not on the other side of the car. ")
        type.type("Next to you. Touching. He's never done that before.")
        print("\n")
        type.type("He falls asleep with his head on your leg. The weight is warm and right.")
        p.restore_sanity(5)
        p.heal(5)
    else:
        type.type("You don't throw it. Lucky waits. Still wagging. Patient.")
        print("\n")
        type.type("Then he picks up the rock and very carefully places it in your lap. ")
        type.type("And waits again.")
        print("\n")
        type.type("You throw the rock. You were always going to throw the rock.")
        print("\n")
        type.type("Lucky bounds after it, ears flopping, absolutely ecstatic.")
        p.restore_sanity(3)
    print("\n")
    type.type("Later, you notice Lucky has stopped looking at every loud noise like it's going to hurt him. ")
    type.type("He still flinches at raised voices. But he doesn't run anymore.")
    print("\n")
    type.type("Healing isn't a straight line. But he's on the road. So are you.")
    p.meet("Lucky Trusts")
    print("\n")


def storyline_lucky_saves_your_life(p, sl):
    """Lucky Part 4: Lucky saves your life. The best boy."""
    sl.advance("lucky_dog")
    sl.complete("lucky_dog")
    
    type.type("Night. Dead of night. You're asleep in your car when Lucky starts barking. ")
    type.type("Not his normal bark — his " + red(bright("ALARM")) + " bark. The one that means danger.")
    print("\n")
    type.type("You wake up groggy, confused. Lucky is at the driver side window, losing his mind.")
    print("\n")
    type.type("Then you smell it. Smoke. Something under your car is on fire.")
    print("\n")
    
    if p.has_danger("Leaking Battery") or p.has_danger("Engine Oil Empty"):
        type.type("The leak you've been ignoring caught a spark. Your car is about to become a bonfire.")
    else:
        type.type("Something shorted out. Electrical fire. Your car is filling with smoke.")
    print("\n")
    
    type.type("You scramble out of the car. Lucky grabs your sleeve and PULLS — ")
    type.type("dragging you away from the vehicle with the strength of a dog ")
    type.type("who has decided you are NOT dying today.")
    print("\n")
    type.type("Twenty seconds later, something under the hood pops. Sparks fly. ")
    type.type("The engine compartment catches. If you were still inside...")
    print("\n")
    type.type("You're on the ground, fifty feet away, Lucky standing over you like a furry guardian angel. ")
    type.type("He's licking your face. Making sure you're alive.")
    print("\n")
    type.type(quote("Good boy. Good boy. The best boy. The best boy in the entire world."))
    print("\n")
    type.type("Lucky wags his tail so hard his whole body shakes.")
    print("\n")
    
    type.type("The fire burns itself out before it reaches the cabin. Your car is damaged but not destroyed. ")
    type.type("You're alive because a dog nobody wanted decided you were worth saving.")
    print("\n")
    
    if p.has_danger("Lucky's Owner"):
        type.type("You think about the man with the truck. The one who called Lucky 'worthless.' ")
        type.type("He was wrong. Lucky is worth more than everything you own.")
        p.lose_danger("Lucky's Owner")
    print("\n")
    
    type.type("You sit in the gravel, holding Lucky, watching the smoke clear. ")
    type.type("In the morning, you'll deal with the car. Right now, you just hold your dog.")
    print("\n")
    type.type("He saved your life. And somehow, you think he knows.")
    p.restore_sanity(10)
    p.heal(10)
    p.add_danger("Fire Damage")
    p.increment_statistic("near_death_experiences")
    print("\n")

# =====================================================================
# THE DEALER'S PAST - 5 parts
# You discover the Dealer had a life before the card table.
# Stage 0: The photo (you find a photo in the deck)
# Stage 1: The journal (a page falls out of his jacket)
# Stage 2: The question (you ask him about it)
# Stage 3: The answer (he tells you, reluctantly)
# Stage 4: The choice (he offers you something you can't take back)
# =====================================================================

def storyline_dealer_photo(p, sl):
    """Dealer Part 1: You find a photo tucked inside the deck."""
    sl.advance("dealer_past")
    p.meet("Dealer Photo")
    
    type.type("The Dealer shuffles the deck. A card slips out — but it's not a playing card. ")
    type.type("It's a photograph. Old. Faded. Wallet-sized.")
    print("\n")
    type.type("The Dealer snatches it up fast, but you've already seen it: a woman and a little girl ")
    type.type("standing in front of a yellow house. The woman is laughing. The girl is blowing out candles ")
    type.type("on a birthday cake.")
    print("\n")
    type.type("The Dealer tucks the photo into his vest pocket without a word. His hands, ")
    type.type("always perfectly steady, have the faintest tremor.")
    print("\n")
    answer = ask.yes_or_no("Ask about the photo? ")
    if answer == "yes":
        type.type("The Dealer stops shuffling. He looks at you with those dark eyes. ")
        type.type("For a moment, he's not the Dealer. He's just a man with a memory that hurts.")
        print("\n")
        type.type(quote("Some cards aren't meant to be played. Let's leave it at that."))
        print("\n")
        type.type("He resumes shuffling. The moment is over. But the tremor isn't.")
        p.meet("Asked About Photo")
    else:
        type.type("You say nothing. Some things you don't ask about. The Dealer nods, ")
        type.type("almost imperceptibly. He appreciates the silence.")
    print("\n")
    type.type("For the rest of the session, the Dealer plays differently. Quieter. ")
    type.type("Almost gentle with the cards.")
    print("\n")


def storyline_dealer_journal(p, sl):
    """Dealer Part 2: A journal page falls from his jacket."""
    sl.advance("dealer_past")
    
    type.type("The Dealer stands up after a hand and his jacket catches on the chair. ")
    type.type("A folded piece of paper floats to the ground.")
    print("\n")
    type.type("He doesn't notice. You do.")
    print("\n")
    answer = ask.yes_or_no("Pick it up? ")
    if answer == "yes":
        type.type("You pick it up. It's a page torn from a journal. The handwriting is careful, precise — ")
        type.type("the same precision as his card dealing.")
        print("\n")
        type.type(italic("\"Day 4,382. She would have been seventeen today. I counted the candles ") +
                 italic("like I always do. Seventeen invisible candles on an invisible cake ") +
                 italic("at a table with only one chair.\""))
        print("\n")
        type.type(italic("\"The road doesn't get shorter. You just learn to stop counting the miles.\""))
        print("\n")
        type.type("You fold the paper and slip it back onto the table where he'll find it. ")
        type.type("You don't mention it.")
        print("\n")
        type.type("The Dealer comes back, sees the paper, picks it up. Looks at you. ")
        type.type("You're studying your cards like nothing happened.")
        print("\n")
        type.type("He puts the paper in his pocket. Deals the next hand. Says nothing.")
        p.meet("Read Journal")
        p.lose_sanity(2)
    else:
        type.type("You leave it on the ground. The Dealer comes back and spots it.")
        print("\n")
        type.type("He picks it up quickly, checks if you saw. You're looking at your cards.")
        print("\n")
        type.type("He pockets it. The relief on his face lasts exactly one second.")
    print("\n")


def storyline_dealer_question(p, sl):
    """Dealer Part 3: You finally ask. He finally hears."""
    sl.advance("dealer_past")
    
    type.type("It's a slow day. No other players. Just you and the Dealer.")
    print("\n")
    type.type("He deals the cards with his usual perfection, but he's somewhere else. ")
    type.type("His eyes keep drifting to the empty passenger seat of his car — ")
    type.type("wait, does the Dealer have a car? You've never seen him arrive or leave.")
    print("\n")
    if p.has_met("Read Journal"):
        type.type("You've been carrying what you read in that journal entry. The daughter. ")
        type.type("The candles. You can't un-read it.")
        print("\n")
    type.type("The silence between hands stretches. It fills with things unsaid.")
    print("\n")
    answer = ask.yes_or_no("Ask the Dealer about his past? ")
    if answer == "yes":
        type.type(quote("Who were they? The woman and the girl in the photo."))
        print("\n")
        type.type("The Dealer's hands stop mid-shuffle. The cards fan out and stay perfectly still, ")
        type.type("suspended in his fingers like time stopped.")
        print("\n")
        type.type("Long silence. The longest silence that has ever existed between two people.")
        print("\n")
        type.type(quote("...You shouldn't have asked that."))
        print("\n")
        type.type("But he doesn't seem angry. He seems relieved. Like a man who's been holding his breath ")
        type.type("for ten years and someone finally told him he could exhale.")
        print("\n")
        type.type(quote("Not today. But... soon. I'll tell you soon. You've earned that much."))
        print("\n")
        type.type("He deals the next hand. His hands are steady again.")
        p.meet("Dealer Asked")
    else:
        type.type("You play in silence. Sometimes the kindest thing you can do is not ask.")
        print("\n")
        type.type("The Dealer looks at you when you're not looking. He's deciding something.")
        p.meet("Dealer Respected Space")
    print("\n")


def storyline_dealer_answer(p, sl):
    """Dealer Part 4: The Dealer tells you his story."""
    sl.advance("dealer_past")
    
    type.type("Before dealing, the Dealer reaches into his vest pocket and places the photograph ")
    type.type("face-up on the table between you. The woman. The girl. The yellow house.")
    print("\n")
    type.type(quote("Her name was Maria. Our daughter was Sofia."))
    print("\n")
    type.type("He says it like pulling a splinter — quick, to minimize the pain.")
    print("\n")
    type.type(quote("I was a math teacher. Can you believe that? ") +
             quote("I taught probability and statistics at a high school in Riverside. ") +
             quote("I was good at it. The kids liked me. I made math jokes. ") +
             quote("You know how hard it is to make a math joke land?"))
    print("\n")
    type.type("A smile flickers across his face. Ghost of a life.")
    print("\n")
    type.type(quote("Maria was a nurse. Sofia wanted to be a veterinarian. She loved animals. ") +
             quote("Every stray cat in the neighborhood ended up on our porch."))
    print("\n")
    type.type("His voice goes flat. The next part costs him everything.")
    print("\n")
    type.type(quote("Car accident. Both of them. I was at the school grading papers when I got the call. ") +
             quote("The hospital Maria worked at was the one they were taken to. ") +
             quote("Her own colleagues..."))
    print("\n")
    type.type("He can't finish that sentence. He doesn't need to.")
    print("\n")
    type.type(quote("I left everything. The house, the job, the life. Started driving. ") +
             quote("I knew cards — I'd been running poker night for the faculty for years. ") +
             quote("Turns out, when you understand probability, you make a decent dealer."))
    print("\n")
    type.type(quote("This road. Your car. These cards. It's all I have left. ") +
             quote("And the photo. I keep the photo."))
    print("\n")
    type.type("He picks up the photograph and holds it for a moment before putting it back.")
    print("\n")
    
    if p.has_met("Dealer Asked"):
        type.type(quote("You asked. So now you know. Does it change anything?"))
        print("\n")
        type.type(quote("...Yeah. It does."))
        print("\n")
        type.type("The Dealer nods. Maybe that's enough.")
    elif p.has_met("Dealer Respected Space"):
        type.type(quote("You didn't ask. I appreciate that. But I needed to tell someone. ") +
                 quote("Before I forget how to say their names out loud."))
    print("\n")
    type.type("He deals the next hand. The cards feel different in his hands. Lighter.")
    p.restore_sanity(5)
    p.meet("Dealer Opened Up")
    print("\n")


def storyline_dealer_choice(p, sl):
    """Dealer Part 5: The Dealer offers you something permanent."""
    sl.advance("dealer_past")
    sl.complete("dealer_past")
    
    type.type("The Dealer is waiting for you today, but he's not behind the table. ")
    type.type("He's standing next to it. Jacket off. Sleeves rolled up.")
    print("\n")
    type.type(quote("I've been thinking about what I told you. About Maria. Sofia. The old life."))
    print("\n")
    type.type("He picks up the deck and holds it out to you.")
    print("\n")
    type.type(quote("I want to teach you something. The real game. Not blackjack — ") +
             quote("that's just numbers. I want to teach you how to READ a table. ") +
             quote("The way I was taught. The way I taught my students."))
    print("\n")
    type.type(quote("Consider it a lesson in probability. From an ex-teacher to a full-time survivor."))
    print("\n")
    answer = ask.yes_or_no("Accept his lesson? ")
    if answer == "yes":
        type.type("He spends the next hour teaching you. Not tricks — principles. ")
        type.type("How to track which cards have been played. How to calculate odds in your head. ")
        type.type("How to read hesitation in a dealer's hands.")
        print("\n")
        type.type(quote("I can't change the cards. But I can change how you see them. ") +
                 quote("Maria always said I was a better teacher than a gambler. She was right."))
        print("\n")
        type.type("When he's done, he reaches into his pocket and pulls out something small. ")
        type.type("A silver " + item("Dealer's Coin") + " — worn smooth from years in his pocket.")
        print("\n")
        type.type(quote("Sofia gave me this. Found it on the beach when she was eight. ") +
                 quote("She said it was lucky. I don't believe in luck, but I believed in her."))
        print("\n")
        type.type(quote("I want you to have it. Not because it's lucky. Because she would have wanted ") +
                 quote("someone who plays at my table to carry it."))
        print("\n")
        p.add_item("Dealer's Coin")
        p.restore_sanity(10)
        p.heal(5)
        type.type("You take the coin. It's warm. Years of pocket warmth.")
        print("\n")
        type.type(quote("Now sit down. Let's play cards. And this time, try to beat me for real."))
    else:
        type.type(quote("Fair enough. Not everyone wants to learn. Some people just want to play."))
        print("\n")
        type.type("He puts his jacket back on. Rolls down his sleeves. Becomes the Dealer again.")
        print("\n")
        type.type(quote("But the offer stands. Teachers don't give up on students. Even stubborn ones."))
        print("\n")
        type.type("He deals the next hand. Business as usual. But something between you has shifted. ")
        type.type("The Dealer isn't just the Dealer anymore. He's a man. And that changes everything.")
        p.restore_sanity(5)
    print("\n")

# =====================================================================
# SLEEP PARALYSIS - 4 parts
# Something visits you at night when your sanity is low.
# Stage 0: Can't move (the first episode)
# Stage 1: It speaks (the shadow has a voice)
# Stage 2: The offer (it wants something)
# Stage 3: Resolution (you face it or it consumes you)
# =====================================================================

def storyline_paralysis_cant_move(p, sl):
    """Sleep Paralysis Part 1: You wake up and can't move."""
    sl.advance("sleep_paralysis")
    p.meet("Sleep Paralysis")
    
    type.type("Your eyes open. At least, you think they do.")
    print("\n")
    type.type("Your eyes are open. You can see the ceiling of your car. The streetlight outside ")
    type.type("casting its orange glow. Everything is normal.")
    print("\n")
    type.type("Except you can't move.")
    print("\n")
    type.type("Not paralyzed-numb. Paralyzed-" + red("trapped") + ". Your body is awake but it won't listen. ")
    type.type("Your arms are dead weight. Your legs won't respond. You can't even turn your head.")
    print("\n")
    type.type("Then you see it. In the corner of your vision. Something in the back seat.")
    print("\n")
    type.type("A shape. Darker than dark. It doesn't have edges — it has " + italic("suggestions") + " of edges. ")
    type.type("Like smoke that decided to sit down.")
    print("\n")
    type.type("It's watching you. You can feel it watching you even though it doesn't have eyes.")
    print("\n")
    type.type("Your breathing gets faster. Your heart is hammering. But you. Can't. Move.")
    print("\n")
    type.type("The shape leans forward. Closer. You can feel cold radiating off it like an open freezer.")
    print("\n")
    type.type("Then — snap — your body releases. You bolt upright, gasping. ")
    type.type("The back seat is empty. Nothing there. Just the dark.")
    print("\n")
    type.type("You don't sleep for the rest of the night. You sit with every light on and your eyes open, ")
    type.type("watching the back seat in the rearview mirror.")
    print("\n")
    type.type("Nothing comes. But the cold lingers.")
    p.lose_sanity(5)
    p.hurt(5)
    print("\n")


def storyline_paralysis_speaks(p, sl):
    """Sleep Paralysis Part 2: This time, the shadow talks."""
    sl.advance("sleep_paralysis")
    
    type.type("It happens again. Your eyes snap open. You can't move. The shape is back.")
    print("\n")
    type.type("But this time, it's closer. Not in the back seat — it's leaning over the center console, ")
    type.type("hovering above you. Close enough to touch, if you could move your arms.")
    print("\n")
    type.type("And this time, it speaks.")
    print("\n")
    type.type("Not words. Not out loud. The voice comes from inside your skull, ")
    type.type("like a thought that isn't yours.")
    print("\n")
    type.type(red(italic("\"You're tired.\"")) + "\n")
    type.type(red(italic("\"So tired.\"")) + "\n")
    type.type(red(italic("\"I can help with that.\"")) + "\n")
    print("\n")
    type.type("The cold intensifies. Your breath fogs. This shouldn't be happening. ")
    type.type("It's the middle of summer.")
    print("\n")
    type.type(red(italic("\"Stop fighting. Stop running. Stop playing their game. ") +
             italic("I can make it all go away.\"")) + "\n")
    print("\n")
    type.type("The pressure on your chest increases. It's hard to breathe. ")
    type.type("The shadow is heavy. Heavier than anything physical.")
    print("\n")
    type.type(red(italic("\"All you have to do is say yes.\"")) + "\n")
    print("\n")
    type.type("Your body snaps free again. You sit up, drenched in sweat. The car is empty. Warm. Normal.")
    print("\n")
    type.type("But this time, there's a mark on the inside of your windshield. ")
    type.type("Like someone drew a circle in the fog with their finger.")
    print("\n")
    type.type("The fog is on the INSIDE.")
    p.lose_sanity(8)
    p.hurt(5)
    p.meet("Shadow Spoke")
    print("\n")


def storyline_paralysis_offer(p, sl):
    """Sleep Paralysis Part 3: The shadow makes its offer clear."""
    sl.advance("sleep_paralysis")
    
    type.type("You've been fighting sleep for days. Coffee. Slapping yourself. Driving with the windows down.")
    print("\n")
    type.type("It doesn't matter. It comes when it wants to.")
    print("\n")
    type.type("This time, you don't even realize you've fallen asleep. One moment you're driving. ")
    type.type("The next, you're parked somewhere you don't recognize, engine off, and you can't move.")
    print("\n")
    type.type("The shadow fills the entire car. It's everywhere. In the mirrors, in the corners, ")
    type.type("in the gaps between the seats.")
    print("\n")
    type.type(red(italic("\"I'm not what you think I am.\"")) + "\n")
    print("\n")
    type.type(red(italic("\"I'm not a monster. I'm a door. Walk through me and the pain stops. ") +
             italic("The cold stops. The hunger, the loneliness, the endless, stupid cards — ") +
             italic("all of it. Gone.\"")) + "\n")
    print("\n")
    type.type(red(italic("\"I've been watching you lose for so long. I'm offering you the only ") +
             italic("guaranteed win.\"")) + "\n")
    print("\n")
    type.type("The cold is so intense your teeth are chattering. Or trying to — your jaw is locked.")
    print("\n")
    
    # This is the big choice
    type.type("Inside your head, you hear the question clearly:")
    print("\n")
    type.type(red(bright(italic("\"Do you accept?\""))) + "\n")
    print("\n")
    answer = ask.yes_or_no("Do you accept the shadow's offer? ")
    if answer == "yes":
        type.type("You think the word 'yes.' You don't say it — you can't — but you think it.")
        print("\n")
        type.type("The shadow rushes into you. Through you. The cold becomes absolute zero. ")
        type.type("You feel yourself dissolving, unraveling, becoming—")
        print("\n")
        type.type("—" + bright(yellow("HONK. HONK. HONK.")) + "—")
        print("\n")
        type.type("A truck horn. You're in the middle of the road. Your car has drifted. ")
        type.type("The truck swerves around you, horn blaring.")
        print("\n")
        type.type("You're awake. Moving. Alive. The shadow is gone.")
        print("\n")
        type.type("But something is different. You feel lighter. Not better — " + italic("lighter") + 
                 ". Like something was taken from you that you didn't know you had.")
        p.lose_sanity(15)
        p.hurt(10)
        p.add_danger("Shadow's Mark")
        p.meet("Accepted Shadow")
    else:
        type.type("No.")
        print("\n")
        type.type("Not a thought. A word. Your lips move even though your body is frozen. ")
        type.type("You force it out through locked teeth and a locked jaw.")
        print("\n")
        type.type(red(bright("\"No.\"")))
        print("\n")
        type.type("The shadow recoils. The cold retreats. For the first time, ")
        type.type("you hear something from it that isn't confidence.")
        print("\n")
        type.type(red(italic("\"...Interesting.\"")) + "\n")
        print("\n")
        type.type("Your body releases. You sit up. The car is normal. Warm. Silent.")
        print("\n")
        type.type("But in the rearview mirror, just for a second, you see it retreat into the shadows ")
        type.type("behind your headrest. And you could swear it's smiling.")
        p.lose_sanity(5)
        p.meet("Refused Shadow")
    print("\n")


def storyline_paralysis_resolution(p, sl):
    """Sleep Paralysis Part 4: The final night."""
    sl.advance("sleep_paralysis")
    sl.complete("sleep_paralysis")
    
    if p.has_met("Accepted Shadow"):
        type.type("You haven't slept well since the night you said yes. The shadow took something, ")
        type.type("and now there's a hollow space inside you that aches.")
        print("\n")
        type.type("Tonight, it comes back. But it's not the same. It's smaller. Weaker.")
        print("\n")
        type.type(red(italic("\"You lied. You're still fighting. You said you'd stop.\"")) + "\n")
        print("\n")
        type.type("You realize something. It fed on your surrender. Your 'yes' gave it power. ")
        type.type("But every day you kept going — waking up, playing cards, surviving — ")
        type.type("you took that power back.")
        print("\n")
        type.type("You look at the shadow. It's barely there. A suggestion of darkness. ")
        type.type("A smear of cold.")
        print("\n")
        type.type(quote("I changed my mind."))
        print("\n")
        type.type("The shadow flickers. Thins. Fades.")
        print("\n")
        type.type(red(italic("\"They all change their minds. Eventually.\"")) + "\n")
        print("\n")
        type.type("It vanishes. The cold leaves your car. The fog on the windows clears.")
        print("\n")
        type.type("You sleep through the night for the first time in weeks. ")
        type.type("No visitors. No voices. Just sleep.")
        p.restore_sanity(10)
        p.heal(10)
        if p.has_danger("Shadow's Mark"):
            p.lose_danger("Shadow's Mark")
        
    elif p.has_met("Refused Shadow"):
        type.type("The shadow comes one last time. You feel it arrive — the cold, the heaviness, ")
        type.type("the weight on your chest.")
        print("\n")
        type.type("But this time, you're not afraid. You're angry.")
        print("\n")
        type.type("You force your eyes open. Force your head to turn. Look directly at it.")
        print("\n")
        type.type("It's there. In the back seat. Waiting. Patient. Eternal.")
        print("\n")
        type.type("But you see it clearly now. It's not a monster. It's not a demon. ")
        type.type("It's " + italic("exhaustion") + ". It's every night you didn't sleep. ")
        type.type("Every meal you skipped. Every cold morning and hot afternoon and lonely hour. ")
        type.type("It's your body telling you it's had enough.")
        print("\n")
        type.type(quote("I hear you. But I'm not done yet."))
        print("\n")
        type.type("The shadow studies you. Then, slowly, it nods.")
        print("\n")
        type.type(red(italic("\"Fair enough.\"")) + "\n")
        print("\n")
        type.type("It dissolves. Not dramatically — just... gently. Like smoke in a breeze. ")
        type.type("The cold fades. The weight lifts.")
        print("\n")
        type.type("You sleep. Really sleep. The kind of sleep that fixes things.")
        p.restore_sanity(15)
        p.heal(15)
    
    else:
        # Somehow got here without either choice (shouldn't happen, but safety)
        type.type("The episodes stop. Whatever the shadow was, it moved on. Maybe it found someone ")
        type.type("else. Maybe you got strong enough that it couldn't reach you anymore.")
        print("\n")
        type.type("You sleep better now. Not great. But better.")
        p.restore_sanity(5)
    print("\n")

# =====================================================================
# RADIO SIGNAL - 4 parts
# Your car radio picks up something it shouldn't.
# Stage 0: Static (the radio turns on by itself)
# Stage 1: The broadcast (a voice is transmitting)
# Stage 2: The source (you find where it's coming from)
# Stage 3: Who's watching (the truth about the signal)
# =====================================================================

def storyline_radio_static(p, sl):
    """Radio Part 1: Your car radio turns on by itself."""
    sl.advance("radio_signal")
    p.meet("Radio Signal")
    
    type.type("You're driving when your car radio turns on. By itself.")
    print("\n")
    type.type("You haven't touched it. The button is right there, untouched. But the dial is glowing ")
    type.type("and static is pouring through the speakers.")
    print("\n")
    type.type("Not normal static. This static has a rhythm. A pulse. Like breathing.")
    print("\n")
    type.type("You reach for the dial to turn it off. The moment your finger touches it, the static stops. ")
    type.type("Clear silence. Then:")
    print("\n")
    type.type(italic("\"...eighty-seven... eighty-seven... eighty-seven...\""))
    print("\n")
    type.type("A voice. Robotic. Monotone. Repeating a number.")
    print("\n")
    type.type("Then it changes:")
    print("\n")
    type.type(italic("\"...fourteen... fourteen... fourteen...\""))
    print("\n")
    type.type("Then back to static. Then silence. The radio turns itself off.")
    print("\n")
    type.type("You sit in your car, hand still on the dial, heart pounding. The numbers echo: 87, 14.")
    print("\n")
    answer = ask.yes_or_no("Write down the numbers? ")
    if answer == "yes":
        type.type("You scribble " + bright(yellow("87-14")) + " on a receipt. You don't know why. ")
        type.type("Something tells you they mean something.")
        p.add_item("Radio Numbers")
        p.meet("Wrote Numbers")
    else:
        type.type("You let the numbers fade. Probably just some trucker frequency bleeding through.")
        print("\n")
        type.type("Probably.")
    print("\n")
    type.type("The radio stays off for the rest of the night. But the display flickers twice when you're not looking.")
    p.lose_sanity(2)
    print("\n")


def storyline_radio_broadcast(p, sl):
    """Radio Part 2: The broadcast gets personal."""
    sl.advance("radio_signal")
    
    type.type("The radio turns on again. 3:17 AM. You weren't sleeping — you never sleep well anymore — ")
    type.type("so you hear it clearly.")
    print("\n")
    type.type("This time, the voice is different. Not robotic. Human. Someone reading from a script.")
    print("\n")
    type.type(italic("\"Attention. This is a test of the Emergency Broadcast System. ") +
             italic("This is only a test.\""))
    print("\n")
    type.type("Normal enough. Except it keeps going.")
    print("\n")
    type.type(italic("\"The person in the car on Route 9 should know that we see them. ") +
             italic("We see the cards. We see the bets. We see the car with the bad transmission ") +
             italic("and the dog in the passenger seat.\""))
    print("\n")
    if p.has_companion("Lucky"):
        type.type("Lucky lifts his head and growls at the radio.")
        print("\n")
    type.type(italic("\"This is not a warning. This is a notification. ") +
             italic("You are being watched. For your own protection.\""))
    print("\n")
    type.type("Click. Static. Silence.")
    print("\n")
    type.type("Your hands are white-knuckled on the steering wheel. That broadcast described YOUR life. ")
    type.type("Your car. Your route. Your dog.")
    print("\n")
    answer = ask.yes_or_no("Try to tune to the frequency and listen for more? ")
    if answer == "yes":
        type.type("You spin the dial slowly. Station after station of normal radio — pop music, ")
        type.type("country, a preacher yelling about the end times (less scary than the broadcast). ")
        type.type("Nothing out of the ordinary.")
        print("\n")
        type.type("Until you hit 87.14 FM.")
        print("\n")
        if p.has_met("Wrote Numbers"):
            type.type(bright(yellow("87.14")) + ". The numbers from before. 87 and 14.")
            print("\n")
        type.type("Dead air. Not static — silence. Like an open microphone in an empty room. ")
        type.type("You can hear ambient sound: a hum, a clock ticking, someone breathing.")
        print("\n")
        type.type("Then: " + italic("\"Good. You found us.\""))
        print("\n")
        type.type("The radio turns itself off.")
        p.meet("Found Frequency")
    else:
        type.type("You turn the radio off and rip the dial. It comes off in your hand.")
        print("\n")
        type.type("The radio turns back on anyway.")
        print("\n")
        type.type(italic("\"You can't turn off what's always been on.\""))
        print("\n")
        type.type("THEN it goes silent. For real this time.")
    p.lose_sanity(5)
    print("\n")


def storyline_radio_source(p, sl):
    """Radio Part 3: You find where the signal is coming from."""
    sl.advance("radio_signal")
    
    type.type("You've been driving toward the signal. You don't know how you know which direction to go — ")
    type.type("the radio hums louder when you're heading the right way, softer when you're not.")
    print("\n")
    type.type("It leads you off the main road, down a dirt path, past a rusted fence, ")
    type.type("to a clearing in the woods.")
    print("\n")
    type.type("There's a tower. An old radio tower, fifty feet tall, barely standing. ")
    type.type("The metal is corroded, the guy wires are frayed, and the blinking red light at the top ")
    type.type("is the only sign it's still active.")
    print("\n")
    type.type("At the base of the tower is a small concrete building. The door is steel, rusted, ")
    type.type("and slightly ajar.")
    print("\n")
    answer = ask.yes_or_no("Go inside? ")
    if answer == "yes":
        type.type("You push the door open. It screams on its hinges.")
        print("\n")
        type.type("Inside is a single room. Concrete walls, no windows. A desk with radio equipment — ")
        type.type("old equipment, vacuum tubes and dials, mixed with modern components that shouldn't be here.")
        print("\n")
        type.type("A microphone sits on the desk. Next to it, a logbook.")
        print("\n")
        type.type("You open the logbook. Pages and pages of entries. Dates, frequencies, ")
        type.type("and descriptions of... people. Drivers. Drifters. People on the road.")
        print("\n")
        type.type("Your page is near the back. Your car's description. Your daily routine. ")
        type.type("Your gambling schedule. All documented in meticulous handwriting.")
        print("\n")
        type.type("At the bottom of your entry:")
        print("\n")
        type.type(italic("\"Subject shows resilience. Recommend continued observation. ") +
                 italic("Do not intervene. Let the road decide.\""))
        print("\n")
        type.type("The microphone crackles. A voice — the same voice from the broadcast — fills the room:")
        print("\n")
        type.type(italic("\"You found the tower. Most people don't get this far. ") +
                 italic("Now the question is: what are you going to do with what you've found?\""))
        print("\n")
        p.meet("Found Tower")
        p.lose_sanity(5)
        
        answer2 = ask.yes_or_no("Take the logbook? ")
        if answer2 == "yes":
            type.type("You grab the logbook and run. Behind you, the equipment sparks and hisses. ")
            type.type("By the time you reach your car, the red light on the tower goes dark.")
            p.add_item("Radio Logbook")
            p.meet("Took Logbook")
        else:
            type.type("You leave it. Some things are better left undiscovered.")
            print("\n")
            type.type("You walk back to your car. The tower light blinks faster, as if relieved.")
    else:
        type.type("You stand outside, looking at the tower, and decide that some mysteries ")
        type.type("are better left unsolved.")
        print("\n")
        type.type("You drive away. The radio stays silent the whole way back. ")
        type.type("But you swear the red light on the tower followed you until you turned the corner.")
        p.lose_sanity(3)
    print("\n")


def storyline_radio_whos_watching(p, sl):
    """Radio Part 4: The truth about who's behind the signal."""
    sl.advance("radio_signal")
    sl.complete("radio_signal")
    
    type.type("The radio comes on one final time. You're not surprised anymore. You're ready.")
    print("\n")
    
    if p.has_met("Found Tower"):
        type.type(italic("\"You found the tower. You read the book. You know we're watching. ") +
                 italic("Now let me tell you why.\""))
        print("\n")
        type.type("The voice is tired. Not menacing. Tired.")
        print("\n")
        type.type(italic("\"My name is Alan. I was an emergency dispatcher for 30 years. ") +
                 italic("I took calls from people in trouble — car accidents, fires, crimes. ") +
                 italic("I sent help. That was my job.\""))
        print("\n")
        type.type(italic("\"When I retired, I couldn't stop. Couldn't stop listening. ") +
                 italic("So I built the tower. I monitor the frequencies. I watch the roads. ") +
                 italic("I track the people who live on them.\""))
        print("\n")
        type.type(italic("\"Not to control. Not to harm. Just to make sure... ") +
                 italic("if something happens... someone notices.\""))
        print("\n")
        type.type(italic("\"You're not the only one I watch. There are dozens of you on this stretch. ") +
                 italic("Drifters, gamblers, runners. I keep logs so if one of you disappears, ") +
                 italic("I can tell someone where to start looking.\""))
        print("\n")
        if p.has_met("Took Logbook"):
            type.type(italic("\"You took my logbook. That's okay. I've got copies. ") +
                     italic("But you should know — your page has more notes than most. ") +
                     italic("You've survived things I've seen other people die from.\""))
            print("\n")
            type.type(italic("\"I'm rooting for you. For what it's worth.\""))
        else:
            type.type(italic("\"You didn't take the book. Smart. If someone found it on you, ") +
                     italic("they'd ask questions. I appreciate the discretion.\""))
        print("\n")
        type.type(italic("\"I'm going to stop broadcasting to you now. You know I'm here. ") +
                 italic("That's enough. If you ever need help — real help — tune to 87.14 and key the mic. ") +
                 italic("I'll hear it.\""))
        print("\n")
        type.type("The radio clicks off. The dial light fades.")
        print("\n")
        type.type("You're alone on the road. But for the first time, you don't feel alone. ")
        type.type("Somewhere in a concrete bunker, an old dispatcher is watching the roads, ")
        type.type("making sure the lost don't stay lost.")
        p.restore_sanity(10)
        p.heal(5)
    else:
        type.type(italic("\"You didn't come to the tower. That's alright. Not everyone wants to know.\""))
        print("\n")
        type.type(italic("\"I'll keep watching. That's what I do. Stay safe out there.\""))
        print("\n")
        type.type("The radio goes silent. Permanently, this time. The display goes dark.")
        print("\n")
        type.type("You never hear the voice again. But sometimes, late at night, ")
        type.type("you catch yourself reaching for the dial.")
        p.restore_sanity(5)
    print("\n")

# =====================================================================
# THE GRAVEYARD - 4 parts
# A cemetery on the edge of town holds more than dead people.
# Stage 0: Wandering (you end up at the graveyard by accident)
# Stage 1: The digger (you meet the gravedigger, Edgar)
# Stage 2: Your plot (Edgar shows you something unsettling)
# Stage 3: Edgar's request (the old man has one last thing to ask)
# =====================================================================

def storyline_graveyard_wandering(p, sl):
    """Graveyard Part 1: You end up at the cemetery."""
    sl.advance("graveyard")
    p.meet("Graveyard")
    
    type.type("You took a wrong turn. Or maybe the road took it for you.")
    print("\n")
    type.type("You end up at a cemetery. Old one. Iron fence, stone angels, headstones so weathered ")
    type.type("the names have worn to whispers.")
    print("\n")
    type.type("Your car dies at the gate. Engine just... stops. You turn the key. Nothing. ")
    type.type("You're stuck here until it decides to work again.")
    print("\n")
    answer = ask.yes_or_no("Walk through the cemetery while you wait? ")
    if answer == "yes":
        type.type("The gate swings open with a groan that echoes. Inside, the graves stretch out in rows, ")
        type.type("ordered and patient, like they've been waiting.")
        print("\n")
        type.type("Some have fresh flowers. Most don't. You read names as you walk:")
        print("\n")
        type.type(italic("\"Harold Mercer, 1942-2019. Beloved husband.\""))
        type.type(italic("\"Elaine Frye, 1955-2021. She sang every morning.\""))
        type.type(italic("\"Baby James, 2008-2008. Too good for this world.\""))
        print("\n")
        type.type("That last one stops you. You stand there for a while.")
        print("\n")
        type.type("You hear digging. Somewhere deeper in the cemetery, someone is working.")
        p.meet("Walked Graveyard")
    else:
        type.type("You sit in the car and wait. The engine comes back after twenty minutes. ")
        type.type("But through the windshield, you see something move between the headstones.")
        print("\n")
        type.type("Probably a groundskeeper. Probably.")
    p.lose_sanity(2)
    print("\n")


def storyline_graveyard_digger(p, sl):
    """Graveyard Part 2: You meet Edgar, the gravedigger."""
    sl.advance("graveyard")
    
    type.type("You end up at the cemetery again. Your car keeps pulling toward it — ")
    type.type("literally, the steering feels heavy when you try to pass it.")
    print("\n")
    type.type("This time, you see him. A man in overalls, standing waist-deep in a freshly dug hole, ")
    type.type("throwing dirt over his shoulder with the ease of someone who's done this ten thousand times.")
    print("\n")
    type.type("He sees you and leans on his shovel.")
    print("\n")
    type.type(quote("Well. You came back. They always come back."))
    print("\n")
    type.type("He climbs out of the hole. He's old — 70s maybe — but strong. Arms like ropes. ")
    type.type("His nametag says " + cyan(bright("EDGAR")) + ".")
    print("\n")
    type.type(quote("I'm Edgar. I dig the holes. Been digging 'em since 1978. ") +
             quote("Before that, my father dug 'em. And his father before him. ") +
             quote("Somebody's got to, right?"))
    print("\n")
    answer = ask.yes_or_no("Talk to Edgar? ")
    if answer == "yes":
        type.type("Edgar leans against a headstone (casually, like it's a fence post) and talks.")
        print("\n")
        type.type(quote("You know what most people get wrong about graveyards? They think it's sad. ") +
                 quote("It's not sad. It's just... quiet. And quiet ain't the same as sad."))
        print("\n")
        type.type(quote("The sad part is out THERE.") + " He gestures at the road. " +
                 quote("In here, everybody's done with the sad part."))
        print("\n")
        type.type("He points to the fresh hole.")
        print("\n")
        type.type(quote("This one's for Mrs. Chen. Ninety-three years old. Fourteen grandkids. ") +
                 quote("Died in her sleep with a cat on her chest. ") +
                 quote("That's about the best ending anyone can hope for."))
        print("\n")
        type.type(quote("What about you? You look like someone who's running FROM an ending, ") +
                 quote("not running TO one."))
        p.meet("Talked To Edgar")
    else:
        type.type("You nod at Edgar and walk past. He watches you go, leaning on his shovel.")
        print("\n")
        type.type(quote("I'll be here when you're ready to talk. I'm always here."))
    p.restore_sanity(2)
    print("\n")


def storyline_graveyard_your_plot(p, sl):
    """Graveyard Part 3: Edgar shows you something you weren't meant to see."""
    sl.advance("graveyard")
    
    type.type("Edgar is waiting for you at the gate. He has a thermos of coffee and two mugs.")
    print("\n")
    type.type(quote("I want to show you something. You're going to want that coffee first."))
    print("\n")
    type.type("He leads you to the back of the cemetery. The old section. The headstones here ")
    type.type("are pre-Civil War. Crumbling. Names barely visible.")
    print("\n")
    type.type("Past the old section, past the tool shed, past the compost pile, ")
    type.type("there's a corner you haven't noticed before.")
    print("\n")
    type.type("It's empty. No headstones. No markers. Just fresh-turned earth. ")
    type.type("And one hole, freshly dug, with no name.")
    print("\n")
    type.type(quote("That one's yours."))
    print("\n")
    type.type("You stop. Coffee cup frozen halfway to your mouth.")
    print("\n")
    type.type(quote("Not literally. Not yet. But I dug it the day I met you. ") +
             quote("I dig one for every drifter who passes through. Just in case. ") +
             quote("So nobody ends up in an unmarked grave somewhere."))
    print("\n")
    type.type(quote("If you die on this road, I want you to have a proper resting place. ") +
             quote("With your name on it. And flowers, when I can find 'em."))
    print("\n")
    type.type("He's serious. Dead serious. (Unfortunate phrasing, given the location.)")
    print("\n")
    answer = ask.yes_or_no("Ask Edgar how many of these 'just in case' graves he's dug? ")
    if answer == "yes":
        type.type("Edgar looks at the ground.")
        print("\n")
        type.type(quote("Forty-seven. Since I started keeping count. Twenty-three of them got filled."))
        print("\n")
        type.type("The weight of that number settles over you like dirt.")
        print("\n")
        type.type(quote("The other twenty-four... well. Some drove off. Some got better. ") +
                 quote("A few just vanished. I like to think they made it somewhere good."))
        p.lose_sanity(5)
        p.meet("Knows The Count")
    else:
        type.type("You don't ask. Some numbers are too heavy to carry.")
    print("\n")
    type.type(quote("I'm not trying to scare you. I'm trying to give you a reason to NOT end up here. ") +
             quote("Every morning you wake up and that hole stays empty, that's a win."))
    print("\n")
    type.type("You look at the empty grave. YOUR empty grave. And for some reason, ")
    type.type("it doesn't scare you. It motivates you.")
    p.restore_sanity(3)
    print("\n")


def storyline_graveyard_edgars_request(p, sl):
    """Graveyard Part 4: Edgar asks you for something."""
    sl.advance("graveyard")
    sl.complete("graveyard")
    
    type.type("Edgar calls you over to the shed. He's sitting on an overturned bucket, ")
    type.type("looking older than usual. The shovel is leaning against the wall. ")
    type.type("His hands are resting on his knees.")
    print("\n")
    type.type(quote("I need to ask you something. And I need you to be honest."))
    print("\n")
    type.type("He holds up an envelope. Yellow. Sealed. Your name is on it.")
    print("\n")
    type.type(quote("I wrote letters. For every drifter I've dug a hole for. ") +
             quote("Things I noticed about 'em. Things worth remembering. ") +
             quote("In case somebody comes looking someday."))
    print("\n")
    type.type(quote("This one's yours. Don't read it now. Read it when you leave this road. ") +
             quote("When you're done. If you're ever done."))
    print("\n")
    answer = ask.yes_or_no("Take the letter? ")
    if answer == "yes":
        p.add_item("Edgar's Letter")
        type.type("You take the envelope. It's heavier than paper should be.")
        print("\n")
        type.type(quote("Good. Now, my request."))
        print("\n")
        type.type("He stands up, creaking like the gate.")
        print("\n")
        type.type(quote("I'm retiring. Can't dig like I used to. My back, my knees, ") +
                 quote("everything's giving out. The cemetery board wants to hire a company ") +
                 quote("with backhoes and machines. No more hand-dug graves."))
        print("\n")
        type.type(quote("But here's the thing. The drifters' section — YOUR section — ") +
                 quote("they don't want to maintain it. 'Not cost-effective,' they said. ") +
                 quote("They want to bulldoze it for expansion."))
        print("\n")
        type.type("His jaw tightens.")
        print("\n")
        type.type(quote("Twenty-three people are buried back there. People nobody else remembers. ") +
                 quote("I remember all of them. I need someone else to know they existed."))
        print("\n")
        type.type("He hands you a second envelope. Inside is a list of names.")
        print("\n")
        type.type(quote("That's them. All twenty-three. If you ever make it big — ") +
                 quote("if those cards work out — maybe you buy some flowers once in a while."))
        print("\n")
        p.add_item("Edgar's List")
        p.restore_sanity(8)
        p.heal(5)
    else:
        type.type("You can't take it. Whatever's in that letter, you're not ready for it.")
        print("\n")
        type.type("Edgar nods. He understands.")
        print("\n")
        type.type(quote("That hole out back? I'm filling it in tomorrow. You don't need it. ") +
                 quote("I can tell. You're going to make it."))
        p.restore_sanity(5)
    print("\n")
    type.type("Edgar shakes your hand. His grip is the grip of a man who has carried the weight ")
    type.type("of other people's endings for forty-five years.")
    print("\n")
    type.type(quote("Go live, kid. That's the whole point."))
    print("\n")
    type.type("You drive away from the cemetery for the last time. Your car doesn't pull toward it anymore.")
    print("\n")

# =====================================================================
# THE CARNIVAL - 4 parts (fast-paced, limited-time event)
# A traveling carnival appears overnight. It wasn't on any map.
# Stage 0: The lights (you see it from the road)
# Stage 1: Fortune teller (she knows things she shouldn't)
# Stage 2: The game (a rigged game with real stakes)
# Stage 3: Pack up (the carnival disappears overnight)
# =====================================================================

def storyline_carnival_lights(p, sl):
    """Carnival Part 1: Lights appear on the horizon."""
    sl.advance("carnival")
    p.meet("Carnival")
    
    type.type("You see them from the road. Lights. Dozens of them. Colored bulbs strung on wires, ")
    type.type("ferris wheel silhouette against the night sky, the distant sound of calliope music.")
    print("\n")
    type.type("A carnival. In the middle of nowhere. On a Tuesday.")
    print("\n")
    type.type("There's a hand-painted sign at the entrance: " + 
             bright(yellow("\"PROFESSOR MIDNIGHT'S TRAVELING SPECTACULAR\"")))
    print("\n")
    type.type("Underneath, in smaller letters: " + italic("\"No refunds. No complaints. No escape.\""))
    print("\n")
    type.type("That last one is probably a joke.")
    print("\n")
    answer = ask.yes_or_no("Enter the carnival? ")
    if answer == "yes":
        type.type("The gates are open. No ticket booth. No admission fee. Just an archway of lights ")
        type.type("and the smell of cotton candy and engine grease.")
        print("\n")
        type.type("Inside, the carnival is alive. But something's off. The rides are running but nobody's ")
        type.type("on them. The game booths are staffed but the attendants don't blink. ")
        type.type("The cotton candy machine is spinning by itself.")
        print("\n")
        type.type("A man in a top hat and a coat covered in patches approaches you. His smile is too wide.")
        print("\n")
        type.type(quote("WELCOME, WELCOME! A new guest! How delightful! ") +
                 quote("I am Professor Midnight, and everything you see here is REAL. ") +
                 quote("The fun, the prizes, the danger — all REAL."))
        print("\n")
        type.type("He gestures grandly at the carnival.")
        print("\n")
        type.type(quote("Look around! Play a game! Visit the fortune teller! ") +
                 quote("But do it quickly — we leave at dawn. We always leave at dawn."))
        print("\n")
        type.type("He tips his hat and walks backward into the crowd, never turning around, ")
        type.type("never breaking eye contact, and then he's gone.")
        p.meet("Entered Carnival")
    else:
        type.type("You drive past. The lights fade in your rearview mirror.")
        print("\n")
        type.type("Something tugs at you. A feeling. Like the carnival noticed you driving by ")
        type.type("and was disappointed.")
        print("\n")
        type.type("The calliope music follows you for three more miles.")
    print("\n")


def storyline_carnival_fortune(p, sl):
    """Carnival Part 2: The fortune teller knows too much."""
    sl.advance("carnival")
    
    type.type("The carnival is still there. You're drawn back. The lights pulse in a rhythm ")
    type.type("that matches your heartbeat.")
    print("\n")
    type.type("This time, you head for the fortune teller's tent. Purple velvet. Gold tassels. ")
    type.type("A sign reads: " + bright(yellow("\"MADAME VERA SEES ALL. TIPS APPRECIATED.\"")))
    print("\n")
    type.type("Inside, a woman sits behind a crystal ball. She's ancient. Her eyes are milky white. ")
    type.type("The tent smells like incense and regret.")
    print("\n")
    type.type(quote("Sit. I've been expecting you."))
    print("\n")
    type.type("You sit. The crystal ball hums.")
    print("\n")
    type.type(quote("You live in your car. You play blackjack for money. You've met people who ") +
             quote("changed you and people who tried to break you."))
    print("\n")
    type.type("She's not guessing. She's " + italic("reading") + ".")
    print("\n")
    if p.has_met("Grandma"):
        type.type(quote("The old woman who calls you Tommy... she loves you. That's real. ") +
                 quote("Don't question it."))
        print("\n")
    if p.has_met("Martinez"):
        type.type(quote("The officer who brings coffee... he lost someone. He found you instead."))
        print("\n")
    if p.has_met("Gerald"):
        type.type(quote("The silent man with the painted face... he's safe now. Don't worry."))
        print("\n")
    type.type("Madame Vera leans forward.")
    print("\n")
    type.type(quote("You want to know if it gets better. That's what everyone asks."))
    print("\n")
    answer = ask.yes_or_no("Ask if it gets better? ")
    if answer == "yes":
        type.type("Madame Vera smiles. Her teeth are perfect.")
        print("\n")
        type.type(quote("Sometimes. For some people. For you..."))
        print("\n")
        type.type("She waves her hand over the crystal ball. The mist inside swirls.")
        print("\n")
        type.type(quote("...I see a road. A long one. With more bumps than smooth stretches. ") +
                 quote("But at the end of it, there's a door. And behind that door is something ") +
                 quote("you've been looking for without knowing it."))
        print("\n")
        type.type(quote("I can't tell you what it is. That would ruin it. And I don't do spoilers."))
        p.restore_sanity(5)
    else:
        type.type(quote("Smart. Some questions are better left unasked. The answer might disappoint you. ") +
                 quote("Or terrify you. Same thing, really."))
    print("\n")
    type.type("She reaches under the table and hands you a small coin. It's warm.")
    print("\n")
    type.type(quote("A carnival token. Good for one game at the Main Attraction. ") +
             quote("Use it wisely. Or don't. That's the fun part."))
    p.add_item("Carnival Token")
    p.meet("Fortune Told")
    print("\n")


def storyline_carnival_game(p, sl):
    """Carnival Part 3: The Main Attraction - a game with real stakes."""
    sl.advance("carnival")
    
    type.type("The Main Attraction is at the center of the carnival. A massive booth, bigger than the others, ")
    type.type("draped in red and black fabric. The sign reads:")
    print("\n")
    type.type(bright(red("\"THE WHEEL OF MODEST FORTUNE\"")))
    print("\n")
    type.type(bright(red("\"Spin the wheel. Win a prize. Risk a price.\"")))
    print("\n")
    type.type("Professor Midnight is running it. He's behind the booth, grinning that too-wide grin.")
    print("\n")
    type.type(quote("AH! A player! Do you have a TOKEN?"))
    print("\n")
    if p.has_item("Carnival Token"):
        type.type("You hold up the token. It glows faintly in the carnival lights.")
        print("\n")
        type.type(quote("WONDERFUL! Step right up!"))
        p.use_item("Carnival Token")
    else:
        type.type("You don't have a token. Professor Midnight shrugs.")
        print("\n")
        type.type(quote("No token? Cash works too! $100 to spin!"))
        if p.get_balance() >= 100:
            answer = ask.yes_or_no("Pay $100 to spin? ")
            if answer == "yes":
                p.change_balance(-100)
            else:
                type.type(quote("Then you're just a spectator! How boring!"))
                print("\n")
                return
        else:
            type.type("You can't afford it. Midnight waves you away.")
            print("\n")
            return
    print("\n")
    type.type("The wheel is massive. Ten sections, each a different color. You can't read what's ")
    type.type("written on them — the wheel is already spinning.")
    print("\n")
    type.type("CLICK. CLICK. CLICK. The wheel slows.")
    print("\n")
    
    result = random.randint(1, 10)
    if result <= 3:  # Big win
        prize_cash = random.choice([500, 750, 1000])
        type.type("The wheel lands on " + bright(green("GOLD")) + "!")
        print("\n")
        type.type(quote("JACKPOT! INCREDIBLE! STUPENDOUS!"))
        print("\n")
        type.type("Confetti explodes from somewhere. Professor Midnight hands you " + 
                 green(bright("${:,}".format(prize_cash))) + " in cash that smells like popcorn.")
        p.change_balance(prize_cash)
        p.meet("Carnival Won Big")
    elif result <= 6:  # Small win
        type.type("The wheel lands on " + bright(yellow("SILVER")) + "!")
        print("\n")
        type.type(quote("A modest victory! How appropriate for the Wheel of MODEST Fortune!"))
        print("\n")
        type.type("He hands you a stuffed animal. It's a bear wearing a tiny top hat. ")
        type.type("It's the " + item("Professor Bear") + ".")
        print("\n")
        type.type(quote("He's lucky. Or cursed. I forget which. Enjoy!"))
        p.add_item("Professor Bear")
    elif result <= 8:  # Neutral
        type.type("The wheel lands on " + bright(cyan("BRONZE")) + "!")
        print("\n")
        type.type(quote("Not a win! Not a loss! The most exciting form of nothing!"))
        print("\n")
        type.type("He hands you a cotton candy. It's purple. It might be glowing.")
        print("\n")
        type.type("You eat it. It tastes like Tuesday.")
        p.heal(5)
    else:  # Bad outcome
        type.type("The wheel lands on " + bright(red("BLACK")) + ".")
        print("\n")
        type.type("Professor Midnight's smile doesn't falter. If anything, it gets wider.")
        print("\n")
        type.type(quote("Ooh. Black. That's the interesting one."))
        print("\n")
        type.type("The lights in the carnival flicker. Every bulb, all at once. ")
        type.type("When they come back on, something is different. The air is colder. ")
        type.type("The calliope is playing a minor key.")
        print("\n")
        type.type(quote("The Black space means you owe the carnival a memory. ") +
                 quote("Don't worry — you won't miss it. You won't even remember having it."))
        print("\n")
        type.type("He touches your forehead with one finger. For a moment, everything goes white.")
        print("\n")
        type.type("When you blink, you're standing outside the booth. You can't remember ")
        type.type("what just happened. But you feel lighter. And emptier.")
        p.lose_sanity(10)
        p.meet("Carnival Lost Memory")
    print("\n")


def storyline_carnival_pack_up(p, sl):
    """Carnival Part 4: The carnival disappears overnight."""
    sl.advance("carnival")
    sl.complete("carnival")
    
    type.type("You drive past the carnival site at dawn. The lights should be on — ")
    type.type("Professor Midnight said they leave at dawn.")
    print("\n")
    type.type("But there's nothing there.")
    print("\n")
    type.type("Not packed up. Not moved. " + italic("Nothing") + ". The field is empty. No tire tracks. ")
    type.type("No trash. No indentations in the grass where the rides stood. ")
    type.type("Not even a flattened patch where the tent was.")
    print("\n")
    type.type("It's as if the carnival was never there.")
    print("\n")
    
    if p.has_item("Professor Bear"):
        type.type("You look at the stuffed bear on your dashboard. It's still there. It's real. ")
        type.type("Its tiny top hat is slightly crooked.")
        print("\n")
        type.type("So it WAS real. The bear proves it.")
    elif p.has_met("Carnival Won Big"):
        type.type("You check your wallet. The carnival cash is still there. ")
        type.type("It doesn't smell like popcorn anymore. It smells like regular money.")
    elif p.has_met("Carnival Lost Memory"):
        type.type("You try to remember what happened at the wheel. The memory is gone. ")
        type.type("You know you lost something, but you can't remember what.")
    print("\n")
    
    type.type("You get out of the car and walk to where the entrance was. The grass is normal. ")
    type.type("The ground is undisturbed.")
    print("\n")
    type.type("Except for one thing. In the center of where the Main Attraction stood, ")
    type.type("there's a card stuck in the ground. A playing card.")
    print("\n")
    type.type("The Joker.")
    print("\n")
    type.type("On the back, in gold ink:")
    print("\n")
    type.type(italic("\"Thanks for playing. See you next time. - P.M.\""))
    print("\n")
    type.type("There won't be a next time. Will there?")
    print("\n")
    type.type("You get back in your car. The calliope music plays for exactly three seconds ")
    type.type("from a radio station that doesn't exist. Then silence.")
    p.restore_sanity(3)
    print("\n")

# =====================================================================
# THE LOCKBOX - 3 parts
# You find a locked metal box under the driver's seat.
# It wasn't there yesterday. Someone put it there.
# Stage 0: Found the box
# Stage 1: Finding the key
# Stage 2: Who left it and why
# =====================================================================

def storyline_lockbox_found(p, sl):
    """Lockbox Part 1: You find a metal box under the driver's seat."""
    sl.advance("lockbox")
    p.meet("Lockbox")
    
    type.type("You're looking for a dropped quarter under the driver's seat when your hand ")
    type.type("touches something cold and hard. Metal.")
    print("\n")
    type.type("You pull it out. It's a lockbox. A real, proper lockbox. Steel. Heavy. About the size ")
    type.type("of a shoebox. There's a keyhole on the front and a combination dial on top.")
    print("\n")
    type.type("It's padlocked shut with a serious-looking Master lock.")
    print("\n")
    type.type("You shake it. Something slides around inside. Multiple somethings. ")
    type.type("They clink against each other like glass or metal.")
    print("\n")
    type.type("This wasn't here yesterday. You'd have noticed. Which means someone put it ")
    type.type("in your car while you were sleeping.")
    print("\n")
    type.type("On the bottom, scratched into the metal with something sharp:")
    print("\n")
    type.type(italic("\"DON'T OPEN UNTIL READY\""))
    print("\n")
    answer = ask.yes_or_no("Try to force it open? ")
    if answer == "yes":
        type.type("You wedge a screwdriver into the lock mechanism and twist.")
        print("\n")
        type.type("Nothing. This thing is solid. Whatever's inside, someone wanted it to stay inside ")
        type.type("until the right person had the right key.")
        print("\n")
        type.type("You try smashing it against the concrete. The concrete cracks. The box doesn't.")
        print("\n")
        type.type("Okay. You need the key.")
    else:
        type.type("Probably wise. You don't know what's in there. Could be valuables. ")
        type.type("Could be evidence. Could be somebody's ashes.")
        print("\n")
        type.type("Could be a lot of things.")
    print("\n")
    type.type("You put the lockbox in your trunk. You need to find whoever left it — ")
    type.type("or at least find the key.")
    p.add_item("Lockbox")
    print("\n")


def storyline_lockbox_key_hunt(p, sl):
    """Lockbox Part 2: Hunting for the key or combination."""
    sl.advance("lockbox")
    
    type.type("The lockbox is still in your trunk. You've been asking around, carefully, ")
    type.type("about whether anyone's missing a steel box.")
    print("\n")
    type.type("Nobody's claiming it. But someone's been leaving you clues.")
    print("\n")
    type.type("First: a note tucked under your windshield wiper. " + italic("\"Check the park bench.\""))
    print("\n")
    type.type("Second: at the park bench, another note taped underneath. " + 
             italic("\"The combination is a date. Think about when it changed.\""))
    print("\n")
    type.type("Third: carved into the bench itself, faded but readable. " + italic("\"Day one.\""))
    print("\n")
    type.type("Day one. The day you started... this. Living in your car. Playing blackjack.")
    print("\n")
    type.type("Someone knows your story. Someone's been watching since the beginning.")
    print("\n")
    
    answer = ask.choose_an_option("What do you do? ", ["Try the combination", "Ask around about who left the notes", "Leave it alone"])
    if answer == 1:  # Try combination
        type.type("You dig the lockbox out of the trunk. The combination dial has four numbers.")
        print("\n")
        type.type("Day one. You think. What was the date? You turn the dial.")
        print("\n")
        type.type("CLICK.")
        print("\n")
        type.type("The padlock falls open. Your hands are shaking.")
        print("\n")
        type.type("Inside the box:")
        print("\n")
        type.type(" • A thick envelope of cash")
        print("\n")
        type.type(" • A set of keys — house keys, by the look of them")
        print("\n")
        type.type(" • A letter, handwritten, sealed with wax")
        print("\n")
        type.type(" • A photograph of you, asleep in your car, taken from outside the window")
        print("\n")
        type.type("The photograph is the most disturbing part. It was taken at night. Recently. ")
        type.type("Whoever left this box has been close enough to watch you sleep.")
        print("\n")
        type.type("You open the envelope. " + green(bright("$2,000")) + " in crisp bills.")
        print("\n")
        p.change_balance(2000)
        p.meet("Opened Lockbox")
        type.type("You don't open the letter yet. You can't. Your hands won't stop shaking.")
    elif answer == 2:  # Ask around
        type.type("You show the notes to a few people you trust.")
        print("\n")
        if p.has_met("Tom"):
            type.type("Tom the mechanic studies the handwriting.")
            print("\n")
            type.type(quote("That's a woman's handwriting. Neat. Deliberate. Somebody who ") +
                     quote("plans things out. Not in a hurry."))
            p.meet("Tom Saw Notes")
        if p.has_met("Kyle"):
            print("\n")
            type.type("Kyle reads the notes and gets quiet.")
            print("\n")
            type.type(quote("Somebody cares about you, man. Like, really cares. ") +
                     quote("This isn't creepy. Well, the watching-you-sleep part is a little creepy. ") +
                     quote("But the rest of it... somebody's trying to help you."))
        print("\n")
        type.type("Nobody recognizes the handwriting. Nobody's seen anyone near your car at night. ")
        type.type("But you're closer. You know the combination now. You just need to decide to open it.")
        p.meet("Asked About Lockbox")
    else:  # Leave it alone
        type.type("Some boxes should stay closed. At least for now.")
        print("\n")
        type.type("But the curiosity is going to eat you alive.")
        p.lose_sanity(3)
    print("\n")


def storyline_lockbox_who_left_it(p, sl):
    """Lockbox Part 3: The truth about who left the box and why."""
    sl.advance("lockbox")
    sl.complete("lockbox")
    
    if not p.has_met("Opened Lockbox"):
        type.type("You finally open the lockbox. Inside: $2,000 in cash, a set of house keys, ")
        type.type("a sealed letter, and a photograph of you asleep in your car.")
        print("\n")
        p.change_balance(2000)
    
    type.type("You open the letter. The handwriting is the same as the notes — ")
    type.type("neat, deliberate, careful.")
    print("\n")
    type.type(open_quote() + "Dear stranger," + close_quote())
    print("\n")
    type.type(open_quote() + "I know you don't know who I am. That's okay. " + 
             "You don't need to." + close_quote())
    print("\n")
    type.type(open_quote() + "I was where you are three years ago. Same parking lot. " +
             "Same car seat. Same view of the same ceiling. I played cards too — " +
             "not blackjack, poker — but the principle is the same. Gambling to survive. " +
             "Surviving to gamble." + close_quote())
    print("\n")
    type.type(open_quote() + "Someone helped me. I never found out who. " +
             "They left me money and a chance and a note that said " +
             italic("'Pass it on.'") + close_quote())
    print("\n")
    type.type(open_quote() + "So I'm passing it on." + close_quote())
    print("\n")
    type.type(open_quote() + "The keys are to an apartment. Studio, nothing fancy. " +
             "Rent is paid through the end of the month. After that, it's up to you. " +
             "The address is on the keychain." + close_quote())
    print("\n")
    type.type(open_quote() + "I know what you're thinking. Is this real? " +
             "Is this a trap? Who does this?" + close_quote())
    print("\n")
    type.type(open_quote() + "People who remember." + close_quote())
    print("\n")
    type.type(open_quote() + "The photograph was just to prove I could have hurt you. " +
             "I didn't. I won't. I'm just someone who was you, once." + close_quote())
    print("\n")
    type.type(open_quote() + "Good luck. And when you can — pass it on." + close_quote())
    print("\n")
    type.type("It's unsigned.")
    print("\n")
    type.type("You sit in your car holding a letter from a stranger who was you three years ago, ")
    type.type("and you cry. Not because you're sad. Because someone remembered what it felt like ")
    type.type("and did something about it.")
    print("\n")
    
    answer = ask.yes_or_no("Check out the apartment? ")
    if answer == "yes":
        type.type("The address on the keychain leads to a building on the west side. ")
        type.type("Third floor. Unit 3B. The key fits.")
        print("\n")
        type.type("Inside: a studio apartment. Clean. Small. A bed, a kitchenette, a bathroom ")
        type.type("with hot water. A window that faces east — morning sun.")
        print("\n")
        type.type("On the kitchen counter, one more note:")
        print("\n")
        type.type(italic("\"The fridge has groceries. The bed has clean sheets. ") +
                 italic("Welcome home — for now.\""))
        print("\n")
        type.type("It's the nicest room you've been in since everything went wrong.")
        print("\n")
        type.type("You sit on the bed. You take off your shoes. You look at the ceiling, ")
        type.type("which is not the ceiling of your car.")
        print("\n")
        type.type("It's different up here.")
        p.add_item("Apartment Key")
        p.restore_sanity(25)
        p.heal(15)
        p.meet("Has Apartment")
    else:
        type.type("Not yet. It's too much. Too fast. You're not ready for walls and a door ")
        type.type("and a place that expects you to stay.")
        print("\n")
        type.type("But you keep the keys. Just in case.")
        p.add_item("Apartment Key")
        p.restore_sanity(10)
    
    type.type("You fold the letter and put it in your pocket. Maybe one day you'll pass it on too.")
    p.remove_item("Lockbox")
    print("\n")
