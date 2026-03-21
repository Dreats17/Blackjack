# Bot Event Decision Audit

## Part 1: Current Bot Architecture

### Decision Flow
```
Player choice encountered
  → typer.Ask patched → quicktest.py decision function
    → event_policy.py (structured policy) checked FIRST
      → If returns answer → use it
      → If returns None → quicktest.py fallback logic
        → If no specific handler → final generic fallback
```

### Three Input Types

| Type | Patch Point | Policy Function | Fallback |
|------|------------|----------------|----------|
| **yes_or_no** | `_decide_yes_no()` | `choose_event_yes_no()` | threat check → companion → gift wrap → sell → witch → car → marvin → payment reserve → high/low resource default |
| **option** (numbered) | `_decide_option()` | `choose_event_option()` | first option |
| **raw input** (inline) | `_decide_raw_input()` | `choose_event_inline_choice()` | eat/save, drink/save/toss, drink/wash/bottle/leave handlers → `_choose_inline_choice()` |

### event_policy.py Coverage Summary

| Handler | Count | Coverage |
|---------|-------|----------|
| `always_yes` set | ~57 prompts | Exact prompt matching |
| `always_no` set | ~21 prompts | Exact prompt matching |
| Specific yes/no handlers | ~18 | Budget/context-gated |
| Exact option-list matches | ~26 | Exact normalized list matching |
| Inline `set_map` entries | ~24 | Frozen-set matching |
| Specific inline handlers | ~8 | Context/inventory-gated |
| **Total explicit handlers** | **~154** | |

### Generic Fallback Priority (options)
`_choose_generic_option()`: car triage → pay everything → low_resources safe keywords → preserving_run safe keywords → prioritized_keywords (help, join, enter, play...) → first non-risky → first option

### Generic Fallback Priority (inline)
`_choose_generic_inline()`: $1/free/$5 pricing → wish/money keywords → low_resources safe → preserving_run safe → prioritized_keywords → first non-risky → first choice

---

## Part 2: Complete Event Choice Catalog

### Legend
- ✅ = Has specific bot handler
- ⚠️ = Falls to generic/fallback (may pick wrong)
- ❌ = Falls to fallback AND likely picks wrong choice
- 🔄 = Handled by quicktest specialized code (stores, menus, etc.)

---

### adventures.py — 92 inline input() calls, **ZERO specific handlers**

All adventure choices fall to `_choose_generic_inline()` or `_choose_generic_option()`. This is the **single largest gap** in bot coverage.

#### road_adventure
| Choice | Options | Generic Pick | Correct? | Impact |
|--------|---------|-------------|----------|--------|
| ⚠️ street_dice | play/watch/leave | "play" (keyword) | Risky — gambling | Can lose money |
| ⚠️ street_dice bet | int input | Handled by quicktest | OK | |
| ⚠️ street_dice | double/walk | "walk" (keyword) | Safe | Misses upside |
| ⚠️ street_dice | again/leave | "leave" (keyword) | Safe | |
| ⚠️ hitchhiker | stop/honk/drive_past | "stop" (first non-risky) | OK | Good outcomes from stop |
| ⚠️ hitchhiker sub | drop_her_off/give_money/offer_food/talk_more | "talk" (keyword match "talk_more") | OK | |
| ❌ roadside_shrine | touch_stone/pray/leave_offering/read_symbols/walk_away | "leave" matches "leave_offering" NOT "walk_away" | **WRONG** | Loses offering money instead of walking away |
| ⚠️ broken_down_bus | help/sell_water/entertain/rob/ignore | "help" (keyword) | Good | Best outcome |
| ⚠️ broken_down_bus price | $1/free/$5 | "$1" or "free" | Good | Handled by pricing logic |
| ⚠️ road_dog | stop/toss_food/follow/drive_past | "follow" (keyword) | OK | |

#### woodlands_adventure
| Choice | Options | Generic Pick | Correct? | Impact |
|--------|---------|-------------|----------|--------|
| ⚠️ hunting | enter/bet/observe | "enter" (keyword) | Risky | Can lead to bear |
| ⚠️ hunting r1 | track/trap/climb | "track" (first non-risky) | OK | |
| ⚠️ hunting r2 | rush/wait/sabotage | "wait" (keyword) | Good | Safe choice |
| ❌ gigantic_bear | fight/flee/offer/submit | "help" → none, "join" → none, "enter" → none, "play" → none, "follow" → none, "accept" → none, "investigate" → none, "comply" → none, "talk" → none, "communicate" → none, "negotiate" → none → first non-risky = "flee" | **Correct by luck** | flee is actually safest |
| ⚠️ bear attack | eyes/dodge/dead | first non-risky = "eyes" | Risky | 50/50 |
| ⚠️ bear flee | river/cliff/brambles | first non-risky = "river" | OK | All risky |
| ⚠️ fountain | drink/wash/bottle/leave | "leave" (if preserving) or "drink" via generic | Context-dependent | Bottle is best for value |
| ⚠️ hermit | knock/peek/leave | "leave" (if preserving) or "peek" | Misses knock | knock → truth → gift |
| ⚠️ hermit cost | memory/year/favor | first non-risky = "memory" | Unknown | All have costs |

#### swamp_adventure
| Choice | Options | Generic Pick | Correct? | Impact |
|--------|---------|-------------|----------|--------|
| ⚠️ tortoise | race/bet/watch | "watch" (keyword) | Safe | Misses racing fun/profit |
| ⚠️ tortoise r1 | lettuce/yelling/poking | first non-risky = "lettuce" | Good | Lettuce is best (with item) |
| ⚠️ tortoise r2 | cheer/pray/throw | first non-risky = "cheer" | OK | |
| ⚠️ ogre | fight/bribe/riddle/run | "talk" → none, "negotiate" → "negotiate" not listed, → first non-risky = "bribe" | Costs money | riddle is free if you win |
| ⚠️ ogre attack | kneecaps/climb/distract | first non-risky | OK | |

#### beach_adventure
| Choice | Options | Generic Pick | Correct? | Impact |
|--------|---------|-------------|----------|--------|
| ❌ fairy_in_bottle | free/keep/negotiate/ignore | "ignore" (if preserving) | **WRONG** | Misses FREE WISH — huge missed value |
| ⚠️ fairy wish | money/luck/health/item/info | "health" (wish handler) | Good | Policy handles wish keywords |
| ❌ frog_prince | kiss/talk/run/insult | "talk" (keyword) | Unknown | kiss may give $500+ |
| ⚠️ gator_wrestle | wrestle/bet/watch/nope | "watch" (keyword) | Safe | |
| ⚠️ gator r1 | circle/charge/taunt | first non-risky = "circle" | OK | |
| ⚠️ gator r2 | jaw_clamp/roll/escape | first non-risky = "jaw_clamp" | Risky | escape may be safer |
| ⚠️ volleyball | join/bet/watch/nope | "join" (keyword) | Risky | Could lose health |
| ⚠️ volleyball moves | bump/spike/dive, block/set/cheer, trust_grandma/go_hero/teamwork | "teamwork" (keyword) | Good | |
| ⚠️ ritual | join/observe/sabotage/leave | "join" (keyword) or "leave" if preserving | Context-dependent | joining can be dangerous |
| ⚠️ ritual focus | wealth/love/power/peace | "peace" (wish handler) | Good | |
| ❌ message_bottle | open/shake/throw_back/sell | "open" → not in keywords. First non-risky = "open" | OK | open is usually fine |
| ⚠️ hermit_crab | race/bet/catch_own/watch | "watch" (keyword) | Safe | |
| ✅ sandcastle | enter/judge/sabotage/watch | "judge" (set_map) | Good | Best cashout |

#### underwater_adventure
| Choice | Options | Generic Pick | Correct? | Impact |
|--------|---------|-------------|----------|--------|
| ⚠️ fishing | compete/bet/sabotage/watch | "watch" if preserving, else "compete" | Safe | |
| ⚠️ fish target | grouper/tuna/marlin | first non-risky = "grouper" | OK | Each has different risk/reward |
| ⚠️ shark | fight/hide/bait/flee | "flee" avoided as non-risky? "hide" first non-risky? | Depends | |
| ⚠️ final fish | deep_dive/surface_hunt/ambush | first non-risky | OK | |
| ⚠️ sabotage | airhose/steal/shark | "steal" is risky keyword → "airhose" | OK | |
| ⚠️ shipwreck | explore/quick_loot/photograph/leave | "photograph" (keyword) or "leave" if preserving | Misses explore loot | |
| ⚠️ shipwreck area | captains_quarters/cargo_hold/deck/hull | first non-risky | OK | |
| ⚠️ escape | break_hull/signal/calm | "calm" (keyword) | Good | |
| ⚠️ sell artifact | museum/hunter | first non-risky = "museum" | OK | |
| ⚠️ sea_creature | fight/communicate/flee/offer | "communicate" (keyword) | Good | Best outcome |
| ⚠️ attack | dodge/cut/grab | first non-risky = "dodge" | OK | |
| ⚠️ merfolk | accept/decline/ask_questions/steal | "accept" (keyword) or "decline" if preserving | Context-dependent | |
| ⚠️ treasure | dive/hire_help/sell_map/abandon | "help" matches "hire_help" | Costs money but OK | |
| ⚠️ eel | fight_eel/distract/sneak | "fight" is risky → "distract" | OK | |

#### city_adventure
| Choice | Options | Generic Pick | Correct? | Impact |
|--------|---------|-------------|----------|--------|
| ⚠️ shell_game | play/watch/help_woman/leave | "help" (keyword) matches "help_woman" | Good | Helps woman, good outcome |
| ✅ overdose | call_911/help/narcan/leave | "call" or "call_911" (keyword) | Good | Best outcome |
| ⚠️ loan_shark | borrow/refuse/threaten/ask_about_him | "refuse" (keyword) or "ask" | Safe | |
| ⚠️ wise_homeless | sit/give_money/share_food/ask_advice/leave | "ask" matches "ask_advice" | Good | Advice is valuable |
| ⚠️ shop | lost/curious/buy/run | first non-risky = "lost" | OK | |
| ⚠️ con_artist | play_along/be_honest/steal/leave | "play" matches "play_along" or "leave" if preserving | Context-dependent | |
| ⚠️ performer | give_money/give_advice/take_picture/ignore | "ignore" if preserving, else first non-risky | OK | |
| ❌ heist | join/report/blackmail/fight/watch | "join" (keyword) | **WRONG for preserving runs** | Joins a heist! High risk |
| ⚠️ heist loot | reasonable/greedy/pocket_stuff | first non-risky = "reasonable" | Good | |
| ⚠️ ice_cream | get_ice_cream/suspicious/follow_truck/ignore | "follow" (keyword) matches "follow_truck" or "ignore" if preserving | OK | |
| ⚠️ flavor | chocolate/vanilla/mystery | first non-risky = "chocolate" | OK | mystery can be bad |
| ⚠️ sus ice cream | report/buy | "report" (keyword) | Good | |
| ⚠️ fight_club | fight/bet/watch/organize | "organize" (keyword) or "watch" if preserving | Safe | |
| ⚠️ fight rounds | duck/block/counter, knee/headbutt/trip, all_in/defensive/taunt | first non-risky each | OK | |
| ⚠️ ambush | fight/negotiate/surrender/distraction/run | "negotiate" (keyword) | Good | |
| ⚠️ ambush attack | leader/closest/wild_swing | first non-risky = "leader" | OK | |
| ⚠️ heist_join | join/refuse/betray/negotiate | "join" or "negotiate" | Risky | |
| ⚠️ distraction | fight/fire_alarm/drunk_act/spill | "fire_alarm" first non-risky? | OK | fight is risky |

---

### events_night.py — 48 choices

#### Yes/No Choices
| Line | Prompt | Bot Handler | Notes |
|------|--------|------------|-------|
| 142 | blank → "Do you search the body?" | ✅ blank_prompt_investigate_yes | |
| 319 | blank → "Do you approach the figure?" | ✅ blank_prompt_investigate_yes | |
| 346 | blank → "Do you open it?" | ✅ blank_prompt_investigate_yes | |
| 368 | blank → "Do you search it?" | ✅ blank_prompt_investigate_yes | |
| 440 | blank → "Do you search it?" | ✅ blank_prompt_investigate_yes | |
| 468 | blank → "Do you sit and listen?" | ✅ blank_prompt_listen_no | Returns "no" |
| 616 | blank → "Do you approach the witch's shack?" | ✅ blank_prompt_investigate_yes | |
| 626 | blank → eat soup | ⚠️ No specific handler | Falls to fallback |
| 664 | blank → search rowboat | ⚠️ "do you try to pull it up and search it?" | May or may not match |
| 844 | blank → investigate fishing shack | ✅ "do you swim over to investigate?" | |
| 850 | "Accept Earl's moonshine?" | ⚠️ No handler | Falls to fallback |
| 890 | blank → "Do you check on them?" | ✅ blank_prompt_investigate_yes | |
| 925 | blank → "Do you help him collect shells?" | ✅ blank_prompt_investigate_yes | |
| 946 | blank → "Do you join them?" | ✅ blank_prompt_investigate_yes | |
| 1006 | "Use the carrot to lure the rabbit?" | ⚠️ No handler | Falls to fallback — should always be "yes" |
| 1200 | blank | ⚠️ Context unknown | |
| 1517 | "Do you promise?" | ✅ always_yes | |
| 2380 | "Open it?" (Giant Oyster) | ⚠️ No handler | Falls to fallback |

#### Inline Choices
| Line | Options | Bot Handler | Correct? |
|------|---------|------------|----------|
| 423 | around/wait | ✅ set_map → "wait" | Good |
| 566 | pull/burn | ✅ fire_source_gate | Good |
| 586 | drink/save/toss | ✅ quicktest handler | Good |
| 734 | freeze/splash/swim | ❌ **NO HANDLER** → generic | Generic picks "freeze" — **WORST choice** for alligator |
| 771 | force/take | ✅ set_map → "force" | Good |
| 799 | help/buy/swim | ✅ set_map → "help" | Good |
| 818 | luck/love/revenge | ✅ set_map → "luck" | Good |
| 1065 | tough/beach | ✅ set_map → "beach" | Good |
| 1100 | fight/parallel/float | ✅ set_map → "parallel" | Good |
| 1176 | open/save | ✅ set_map → "open" | Good |
| 1213 | keep/return | ✅ set_map → "return" | Good |
| 1240 | swim/still/scare | ✅ set_map → "still" | Good |
| 1333 | accept/decline/scram | ✅ set_map → "decline" | Good |
| 1363 | pet/feed/ignore | ✅ tuna_gate | Good |
| 1398 | nice/cheap/skip | ✅ set_map → "skip" | Good |
| 1456 | listen/tip/walk | ✅ set_map → "listen" | Good |
| 1578 | help/run/sneak/film | ✅ set_map → "film" | Good |
| 1614 | help/love/dodge | ✅ set_map → "love" | Good |
| 1649 | fight/talk/comply/run | ✅ set_map → "comply" | Good |
| 1700 | tip/flinch/watch | ✅ set_map → "watch" | Good |
| 1720 | help/ignore/trick | ✅ set_map → "help" | Good |
| 1757 | feed/flee/dominance | ✅ set_map → "dominance" | Good |
| 1785 | sit/money/walk | ✅ set_map → "sit" | Good |
| 1821 | line/cut/resist | ✅ set_map → "line" | Good |
| 1867 | feed/skip/sit | ✅ set_map → "sit" | Good |
| 1893 | play/watch/decline | ✅ set_map → "watch" | Good |
| 1924 | approach/watch/leave | ✅ set_map → "watch" | Good |

---

### events_day_dark.py — 23 choices

| Line | Prompt/Options | Bot Handler | Notes |
|------|---------------|------------|-------|
| 74 | ["pay now", "beg for time", "refuse"] | ✅ pay_now/beg_for_time | Budget-gated |
| 148 | "Give him money?" | ✅ always_yes | |
| 200 | ["ride it out", "drive to casino anyway", "hurt yourself more"] | ✅ ride_it_out | |
| 245 | "Sell your kidney?" | ✅ always_no | |
| 280 | ["call for help", "try to help yourself", "walk away"] | ✅ call_for_help | |
| 350 | ["pay for treatment", "refuse treatment", "break down"] | ✅ pay/refuse by balance | |
| 407 | ["climb the railing", "call someone", "walk away"] | ✅ call_someone | |
| 475 | "Go back to the tables?" | ✅ always_no | |
| 538 | ["agree to leave", "offer money", "fight back"] | ✅ agree_to_leave | |
| 555 | "Pay $200,000?" | ✅ budget-gated | |
| 642 | "Listen to him?" | ✅ always_yes | |
| 851 | ["comply", "run", "fight"] | ✅ comply_default | |
| 1007 | ["comply", "hide", "hero"] | ✅ hide_robbery_cover | |
| 1319 | ["wrong person", "play along", "run"] | ✅ wrong_person | |
| 1354 | "Buy the drugs? ($500)" | ✅ always_no | |
| 1445 | ["step back", "stay", "call for help"] | ✅ stay_meets_bridge_angel | Best long-term value |
| 1685 | ["bail out", "investigate", "ignore it"] | ✅ bail_out | |
| 1989 | "Pay the mechanic? ($150)" | ⚠️ Falls to payment_reserve_gate | Works but not optimal |
| 2068 | "Buy the painkillers? ($100)" | ✅ always_no | |
| 2110 | "Buy more pills? ($150)" | ✅ always_no | |
| 2230 | ["try it", "sell it", "throw it away"] | ✅ sell_it | |
| 2365 | "Do the interview?" | ✅ always_yes | |
| 2396 | ["stick a pin in it", "burn it", "keep it safe"] | ❌ **NO HANDLER** → generic picks "stick a pin" | Should probably be "keep it safe" |

---

### events_day_people.py — 27 choices

| Line | Prompt | Bot Handler | Notes |
|------|--------|------------|-------|
| 186 | '"What was that?"' | ✅ always_yes | |
| 195 | name input | 🔄 quicktest | |
| 197 | "What was that?" | ✅ always_yes | |
| 233 | "Do you? Know this?" | ✅ always_yes | |
| 304 | "Do you applaud?" | ⚠️ Not in always_yes (but "applaud the performance?" IS) | **Prompt text mismatch** — may miss |
| 346 | "Accept the devil's offer?" | ✅ always_no | |
| 749 | "Pay him $50 for the info?" | ✅ always_no | |
| 779 | "Allow the photoshoot?" | ✅ always_yes | |
| 852 | "Did you? Read it?" | ✅ always_yes | |
| 929 | "Reply anyway?" | ✅ always_yes | |
| 1003 | "Give him some money to make him go away?" | ✅ street_musician_relief_gate | |
| 1051 | "Pay the ticket?" | ⚠️ Falls to payment_reserve_gate | Reasonable |
| 1069 | "Try to return it to the owner?" | ✅ always_yes | |
| 1097 | "Pick her up?" | ✅ always_yes | |
| 1145 | "Pay $20 for a prophecy?" | ✅ always_no | |
| 1287 | ["heads", "tails"] | ✅ heads | |
| 1375 | "Take the money?" (no loyalty context) | ⚠️ Falls to fallback | High resource → "no" **WRONG** — free money |
| 1404 | "Keep it?" | ⚠️ Falls to fallback | High resource → "no" — may be wrong |
| 1471 | "Join the game?" | ⚠️ Falls to fallback | |
| 1497 | "Hang up?" | ✅ always_no | |
| 1699 | ["violinist", "drummer", "neither"] | ✅ neither | |
| 1737 | "Buy yourself a cupcake?" | ✅ sanity_gate | |
| 1757 | "Attend the book club?" | ✅ sanity_gate | |
| 1814 | "Treat yourself to a feast? ($25)" | ⚠️ Payment reserve gate | Works |
| 1839 | "Stay and eat? ($200)" | ⚠️ Payment reserve gate | Works |
| 1862 | "Play along?" | ⚠️ Falls to fallback | High resource → "no" |
| 1895 | "Open it?" (mystery package) | ⚠️ Falls to fallback | High resource → "no" — misses $100-300 reward |

---

### events_day_items.py — 13 yes/no choices (excluding store menus)

| Line | Prompt | Bot Handler | Notes |
|------|--------|------------|-------|
| 1080 | "Use the Ritual Token?" | ⚠️ Fallback | High resource → "no" — may miss valuable outcome |
| 1190 | "Call them? Tell them you found the phone?" | ⚠️ Fallback | Should be "yes" for reward |
| 1628 | "Give them the flower?" | ⚠️ Fallback | Should be "yes" for sanity |
| 1748 | "Open it?" (Suspicious Package) | ⚠️ Fallback | High resource → "no" — misses $1K-5K |
| 1799 | "Give it back?" | ⚠️ Fallback | Context-dependent |
| 1845 | "Post 'found photos' flyers...?" | ⚠️ Fallback | Should be "yes" |
| 1907 | "Play?" | ⚠️ Fallback | |
| 1996 | "Plant it?" | ⚠️ Fallback | Should be "yes" |
| 2037 | "Follow it now?" | ⚠️ Fallback | Should be "yes" for adventure |
| 2088 | "Let it go?" | ⚠️ Fallback | Context-dependent |
| 2167 | "Work it out now?" | ⚠️ Fallback | Should be "yes" |
| 2216 | "Give it back?" | ⚠️ Fallback | Context-dependent |
| 2234 | "Sell it to him?" | ⚠️ Fallback | Context-dependent |

---

### events_day_wealth.py — 18 choices: ALL HANDLED ✅

All choices have explicit handlers or fall correctly to appropriate budget gates.

### events_day_casino.py — 2 choices: ALL HANDLED ✅

### events_day_companions.py — 11 choices

| Line | Prompt/Options | Bot Handler | Notes |
|------|---------------|------------|-------|
| 169 | ["use it", "throw it away", "return it"] | ✅ return | |
| 234 | ["keep the cash", "return it all"] | ✅ return_it_all | |
| 262 | ["sell it", "turn it in"] | ✅ turn_it_in | |
| 459 | ["take it", "leave it"] | ✅ take_it | |
| 482 | "Keep the kitten?" | ✅ always_yes | |
| 597, 711, 731, 1190, 1287 | "Choose:" companion menus | 🔄 quicktest | |
| 1118 | f"Try to befriend the {type}?" | ❌ **PARTIAL** — only "trash gremlin" exact match in always_yes | Other friend types (dog, cat, bird, etc.) **FALL TO FALLBACK** |

### events_day_surreal.py — 5 choices

| Line | Prompt/Options | Bot Handler | Notes |
|------|---------------|------------|-------|
| 67 | "Talk to... Dr. Socksworth?" | ✅ always_yes | |
| 107 | ["save the bird", "ignore your phone", "scream"] | ✅ ignore_phone | |
| 282 | ["not interested", "what are you offering", "souls?"] | ✅ not_interested | |
| 356 | "Accept the blood moon bargain?" | ✅ always_no | |
| 426 | Dance move options | ✅ moonwalk (if exact set matches) | |

### events_day_survival.py — 3 choices

| Line | Prompt | Bot Handler | Notes |
|------|--------|------------|-------|
| 1114 | "Pay for the repair? ($100)" | ⚠️ Payment reserve gate | Works |
| 1662 | "Throw it away?" | ⚠️ Fallback | High resource → "no" — correct (keep item) |
| 1721 | "Do you?" | ⚠️ Fallback (blank-ish) | |

### events_car.py — 1 choice

| Line | Prompt/Options | Bot Handler | Notes |
|------|---------------|------------|-------|
| 443 | ["pull it out", "leave it", "drive to shop"] | ✅ car_triage | Budget-gated |

### events_illness.py — 0 choices
No player choices. All automatic.

### locations.py — 37 choices
Most handled by quicktest specialized menu code (stores, pawn, loan, workbench, destinations, companions, witch flask).

---

## Part 3: Critical Bugs & Mishandled Events

### Priority 1 — Confirmed Wrong Decisions

| # | Event | Choice | Bot Picks | Should Pick | Fix |
|---|-------|--------|-----------|-------------|-----|
| 1 | **Night alligator** (events_night.py:734) | freeze/splash/swim | "freeze" (first non-risky) | "splash" or "swim" | Add to set_map |
| 2 | **Roadside shrine** (adventures.py:361) | touch_stone/pray/leave_offering/read_symbols/walk_away | "leave" matches "leave_offering" | "walk_away" or "pray" | Add specific handler |
| 3 | **Fairy in bottle** (adventures.py:1576) | free/keep/negotiate/ignore | "ignore" (preserving) | "free" — gives a FREE WISH | Add specific handler |
| 4 | **Voodoo doll** (events_day_dark.py:2396) | stick_a_pin/burn/keep_safe | "stick a pin" (first non-risky) | "keep it safe" | Add to option matches |
| 5 | **Take the money?** (events_day_people.py:1375) | "no" (high resource fallback) | "yes" — it's free money | Add to always_yes |
| 6 | **Open it?** (events_day_people.py:1895) | "no" (high resource fallback) | "yes" — expected value is positive | Add to always_yes |
| 7 | **Open it?** (events_day_items.py:1748) | "no" (high resource fallback) | "yes" — big potential reward ($1K-5K) | Add to always_yes |
| 8 | **Open it?** (events_night.py:2380) | "no" (high resource fallback) | "yes" — pearl potential | Add to always_yes |
| 9 | **Befriend dynamic companion** (events_day_companions.py:1118) | "no" (if not "trash gremlin") | "yes" — 67% chance to gain companion | Use partial match |
| 10 | **Heist opportunity** (adventures.py:3580) | "join" (keyword priority) | "report" or "watch" (preserving) | The preserving_run logic should catch this, but "join" is higher in prioritized_keywords |

### Priority 2 — Suboptimal But Not Catastrophic

| # | Event | Issue | Improvement |
|---|-------|-------|-------------|
| 11 | **Fountain of youth** (adventures.py:1174) | Picks "leave" when preserving | "bottle" gives permanent item to sell/use later |
| 12 | **Hermit cabin** (adventures.py:1219) | Picks "leave" when preserving | "knock" → truth → unique reward |
| 13 | **Street dice** (adventures.py:93) | Picks "play" (risky gambling) | "watch" is safer |
| 14 | **Ritual circle** (adventures.py:2034) | Picks "join" when not preserving | "observe" is safer |
| 15 | **Message in bottle** (adventures.py:2119) | "open" (first non-risky) | "sell" might be better value |
| 16 | **Gator jawclamp** (adventures.py:1786) | "jaw_clamp" (first non-risky) | "escape" is safer |
| 17 | **Shell game** (adventures.py:3069) | "help_woman" via keyword | "leave" if low resources |
| 18 | Item "Give/return" prompts | All fall to "no" (high resource) | Many should be "yes" for sanity/karma |
| 19 | "Use the Ritual Token?" | "no" (fallback) | Should be "yes" — tokens are single-use quest items |
| 20 | **"Do you applaud?"** (events_day_people.py:304) | May miss always_yes match | Prompt is "do you applaud?" but always_yes has "applaud the performance?" |

### Priority 3 — threat_context_refusal False Positives

The `threat_context_refusal` in quicktest.py checks recent text for words like "pistol", "gun", "badge", "questioning", "handcuffs", "police cruiser", "loan sharks", "freight truck", "blood covers", "move right now", "i'll be back" and auto-says "no". 

This fires BEFORE event_policy.py for any yes/no prompts that reach the quicktest fallback section, but AFTER event_policy returns None. So it only affects prompts not handled by event_policy. But it could cause problems for:
- Events where "gun" or "badge" appears in narrative but the choice isn't a threat
- Phil's interrogation events (partially fixed by adding "answer me" to always_yes)

---

## Part 4: Item Interaction Patterns in Events

### Items That Gate Event Outcomes (Auto-Used)

| Item | Event | Effect |
|------|-------|--------|
| Animal Whistle | road_dog, hunting_comp bear, tortoise racing, hermit_crab, sea_creature, fishing | Auto-befriends companion (Asphalt, Ursus, Speedy, Deathclaw, Kraken) |
| Cough Drops | sore_throat, companion sick | Prevents throat damage, heals companion |
| Pest Control | spider_bite, cockroach, ant_invasion, termites | Kills pests, prevents damage |
| Spare Tire | flat_tire | Fixes flat, preserves car |
| Bug Spray | mosquito_swarm | Prevents damage (consumed) |
| Cheap Sunscreen | scorching_sun | Prevents sun damage (consumed) |
| Umbrella | scorching_sun, sudden_downpour | Reduces damage (not consumed) |
| Plastic Poncho | sudden_downpour | Prevents rain damage (consumed) |
| Hand Warmers | freezing_night | Prevents freeze (consumed) |
| Blanket | freezing_night | Reduces freeze damage |
| Air Freshener | car_smell | Restores sanity (consumed) |
| Road Flares | roadside_breakdown | Gets help (consumed) |
| Super Glue / Duct Tape | broken_belonging | Fixes items (consumed) |
| Fancy Pen | important_document | Validates for $100-300 |
| Lighter / Monogrammed Lighter | need_fire, pull/burn leech | Fire source |
| Lucky Penny | penny_luck | Triggers lucky status |
| Rubber Bands | rubber_band_save | Utility save |
| Carrot | chase_the_third_rabbit | +20% catch chance |
| Lettuce | tortoise_racing | Racing boost |
| Fish/Live Fish | hermit_crab motivate, merfolk offer | Feeding bonus |
| Turkey Sandwich / Beef Jerky / Granola Bar | hitchhiker offer_food | Feed hitchhiker |
| Can of Tuna | stray cat pet/feed | Better outcome with feed |
| Tool Kit / Duct Tape | broken_down_bus help | Better repair |
| Deck of Cards | broken_down_bus entertain | Entertainment option |
| Water Bottles | fountain_of_youth wash | Healing option |

### Items Used in Car Repairs (events_car.py)

| Item | Car Problem | Effect |
|------|-------------|--------|
| Jumper Cables | Dead battery | Free fix |
| Portable Battery Charger | Dead battery | Free fix |
| Coolant / Antifreeze | Overheating | Free fix |
| Water Bottles | Overheating (fallback) | Temporary fix |
| OBD Scanner | Engine light | Free diagnosis |
| Spare Spark Plugs | Engine misfire | Free fix |
| Tool Kit | Various | Reduces repair cost |
| Serpentine Belt | Belt squeal | Free fix |
| Motor Oil | Oil leak | Temporary fix |
| Oil Stop Leak | Oil leak | Better fix |
| Tire Patch Kit | Tire problems | Free fix |
| Fix-a-Flat | Tire problems | Quick fix |
| Spare Tire | Flat tire | Free fix |
| Car Jack | Tire change helper | Required for some tire fixes |
| Spare Headlight Bulbs | Headlight out | Free fix |
| Spare Fuses | Electrical issues | Free fix |
| Brake Pads | Brake problems | Free fix |
| Brake Fluid | Brake problems | Temporary fix |

---

## Part 5: Recommended Fixes (Prioritized)

### Batch 1: High-Impact Quick Fixes (event_policy.py additions)

**1. Add to `always_yes`:**
```python
"take the money?",
"open it?",
"use the ritual token?",
"call them? tell them you found the phone?",
"give them the flower?",
"post 'found photos' flyers to reunite them?",
"plant it?",
"follow it now?",
"work it out now?",
"use the carrot to lure the rabbit?",
"play along?",
"do you applaud?",
"accept earl's moonshine?",
```

**2. Add to `choose_event_inline_choice()` set_map:**
```python
frozenset({"freeze", "splash", "swim"}): ("splash", "splash_alligator_escape"),
```

**3. Fix befriend prompt matching** — use `startswith` or `in` check:
```python
if "try to befriend" in prompt_lower:
    return "yes", _yes_no_trace(request, plan, "yes", "befriend_companion_always", 0.85)
```

**4. Add adventure-specific option handler for fairy_in_bottle:**
```python
frozenset({"free", "keep", "negotiate", "ignore"}): ("free", "free_fairy_wish"),
```

**5. Add to `choose_event_option()`:**
```python
elif normalized == ["stick a pin in it", "burn it", "keep it safe"]:
    chosen_index, reason = 2, "keep_voodoo_doll_safe"
```

### Batch 2: Adventure Handlers (new set_map entries)

```python
# roadside_shrine - walk_away instead of leave_offering
frozenset({"touch_stone", "pray", "leave_offering", "read_symbols", "walk_away"}): ("pray", "shrine_pray_safe"),

# fountain_of_youth - bottle the water
frozenset({"drink", "wash", "bottle", "leave"}): ("bottle", "fountain_bottle_value"),

# hermit_cabin - knock for reward
frozenset({"knock", "peek", "leave"}): ("knock", "hermit_knock_reward"),

# message_in_bottle
frozenset({"open", "shake", "throw_back", "sell"}): ("open", "open_bottle_default"),

# gator escape
frozenset({"jaw_clamp", "roll", "escape"}): ("escape", "gator_escape_safe"),
```

### Batch 3: Preserving-Run Override for Risky Adventures

The generic keyword priority puts "join" and "enter" before "watch" and "leave" at the non-low-resource/non-preserving tier. For adventures with high-risk combat, the bot should prefer safer options. Consider adding adventure-specific handlers for:
- fight_club → "watch"
- heist → "watch" or "report"  
- ritual_circle → "observe"
- gator_wrestling → "watch"
- ambush → "negotiate" or "run"

---

## Summary Statistics

| Category | Total Choices | Handled | Generic/Fallback | Likely Wrong |
|----------|:------------:|:-------:|:----------------:|:------------:|
| adventures.py | 92 | 2 | 90 | ~12 |
| events_night.py | 48 | 40 | 8 | 1 |
| events_day_dark.py | 23 | 21 | 2 | 1 |
| events_day_people.py | 27 | 19 | 8 | 3 |
| events_day_items.py | 16 | 3 | 13 | 5 |
| events_day_wealth.py | 18 | 18 | 0 | 0 |
| events_day_casino.py | 2 | 2 | 0 | 0 |
| events_day_companions.py | 11 | 9 | 2 | 1 |
| events_day_surreal.py | 5 | 5 | 0 | 0 |
| events_day_survival.py | 3 | 0 | 3 | 0 |
| events_car.py | 1 | 1 | 0 | 0 |
| events_illness.py | 0 | — | — | — |
| locations.py | 37 | 37 | 0 | 0 |
| **TOTAL** | **283** | **157** | **126** | **~23** |

**Coverage: 55%** of all player choices have specific handlers.  
**Error rate: ~8%** of all choices are likely producing wrong/harmful decisions.  
**Biggest gap:** adventures.py (92 choices, 2 handled = 2% coverage).
