# Bot Event Policy — Complete Choice Audit

> Cross-reference of every player choice point in story events against  
> `tools/autoplay/policies/event_policy.py` handlers + generic fallbacks.

---

## How the Bot Decides

| Input Type | Method | Routing |
|---|---|---|
| `ask.yes_or_no("prompt")` | `choose_event_yes_no` | `always_yes` / `always_no` sets → specific handlers → **generic (untraced)** |
| `ask.option("prompt", [...])` | `choose_event_option` | Exact normalized-list match → millionaire menu → `_choose_generic_option` |
| `input("(a/b/c): ")` | `choose_event_inline_choice` | `set_map` frozen-set match → conditional handlers → `_choose_generic_inline` |
| `input("Your favorite X: ")` | `choose_event_inline_choice` | Hard-coded: color→"blue", animal→"dog" |
| `int(input())` | various | Shop/location menus — handled by other policies |

### Generic Fallback Priority

**When low_resources (HP<50 or sanity<25 or balance<50) or preserving_run (balance≥1000 or rank≥1):**  
Keywords: leave → walk → observe → watch → decline → refuse → ignore → save → wait → talk → comply → call → help → follow → peek

**Normal play:**  
Keywords: help → join → enter → play → follow → accept → investigate → comply → talk → negotiate → teamwork → report → return → apologize → call → ask → peek → photograph → observe → watch → leave

**Always avoided (risky):** rob, steal, betray, sabotage, insult, all_in, fight

---

## ⛔ CRITICAL — Generic Fallback Picks the WRONG Answer

These choices fall to generic and the fallback selects a demonstrably sub-optimal or harmful option.

### 1. `swamp_stroll` — Banjo Man (events_night.py ~L468)
- **Prompt:** `ask.yes_or_no()` (blank) — "Do you sit and listen?" in recent text  
- **Bot picks:** NO (matched by `blank_prompt_listen_no`)  
- **Optimal:** YES — sitting and listening gives **$50-150** free money  
- **Impact:** Loses guaranteed free income every encounter  
- **Fix:** Remove `"do you sit and listen?"` from `blank_prompt_listen_no`, or add it to `blank_prompt_investigate_yes`

### 2. `swamp_wade` — Witch Soup (events_night.py ~L626)
- **Prompt:** `ask.yes_or_no()` (blank) — "Do you eat her soup?" in recent text  
- **Bot picks:** Falls through all blank-prompt handlers (not in investigate list) → returns `None` → generic  
- **Optimal:** YES — heals **15-30 HP** + chance of Witch's Blessing status or Witch's Riddle item  
- **Fix:** Add `"do you eat her soup?"` to `blank_prompt_investigate_yes`

### 3. `swamp_wade` — Nectar (events_night.py ~L586)  
- **Choices:** `(drink/save/toss)`  
- **Bot picks:** "save" (generic keyword match)  
- **Optimal:** "drink" — **67% chance** of healing 10-50 HP vs saving a marginal item  
- **Fix:** Add `frozenset({"drink", "save", "toss"}): ("drink", "nectar_drink_heal")` to `set_map`

### 4. `roadside_shrine` (adventures.py ~L219)
- **Choices:** `(touch_stone/pray/leave_offering/read_symbols/walk_away)`  
- **Bot picks:** "leave_offering" (generic matches "leave" keyword inside "leave_offering")  
- **Optimal:** "pray" — free +5-15 HP heal, +3-5 sanity. "leave_offering" **costs $10-100**  
- **Impact:** Bot wastes money on a choice that should be free healing  
- **Fix:** Add to `set_map` or add special handling for shrine choices

### 5. `voodoo_doll_temptation` (events_day_dark.py ~L1450)
- **Choices:** `ask.option(["stick a pin in it", "burn it", "keep it safe"])`  
- **Bot picks:** "stick a pin in it" (first non-risky option — no keywords match)  
- **Optimal:** "burn it" (+5 sanity, cleanest outcome) or "keep it safe" (gets Voodoo Doll item)  
- **Impact:** "stick a pin" causes random NPC harm, narrative consequences  
- **Fix:** Add `["stick a pin in it", "burn it", "keep it safe"]` → `burn_it` or `keep_safe`

### 6. `midnight_gardener` — City Park (events_night.py ~L1924)
- **Choices:** `(approach/watch/leave)`  
- **Bot picks:** "watch" (from `set_map`)  
- **Optimal:** "approach" — gives **Midnight Rose item** (potentially valuable)  
- **Note:** set_map maps `{approach, watch, leave}` → "watch", but "approach" yields an item  
- **Fix:** Change set_map entry to `("approach", "midnight_gardener_item")`

### 7. `You gonna answer me?` — Phil the Phantom (events_day_wealth.py L699)
- **Prompt:** `ask.yes_or_no("You gonna answer me? ")`  
- **Bot picks:** Falls to generic (no match). Generic yes/no returns `None` → probably defaults to "no"  
- **Optimal:** Context-dependent but this is Phil's interrogation; needs specific handling  
- **Fix:** Add `"you gonna answer me?"` to always_yes or add specific handler

### 8. `Do you applaud?` — Mime Event (events_day_people.py L304)
- **Prompt:** `ask.yes_or_no("Do you applaud? ")`  
- **Bot picks:** Falls to generic — "do you applaud?" not in `always_yes` (which has "applaud the performance?" — wrong prompt)  
- **Optimal:** YES — gives **$20 + 5 HP heal**  
- **Fix:** Add `"do you applaud?"` to `always_yes`

---

## 🔶 HIGH PRIORITY — Unhandled Yes/No Choices

These yes/no prompts have no specific handler and fall to generic (which returns `None` for unrecognized yes/no, potentially causing errors or default behavior).

| # | File | Prompt | Optimal | Why |
|---|---|---|---|---|
| 1 | events_night.py L850 | `"Accept Earl's moonshine?"` | YES | Heals 10-25 HP + potential $100-300 or useful item |
| 2 | events_night.py L1006 | `"Use the carrot to lure the rabbit?"` | YES | 33% catch (vs 10% without), rabbit = $500-2000 |
| 3 | events_night.py L2380 | `"Open it?"` (Giant Oyster) | YES | Pearl chance + healing; the oyster is consumed either way |
| 4 | events_day_animals.py L707 | `"Offer it some [Birdseed/Bread]?"` | YES | Befriends Mr. Pecks companion. **`always_yes` has "offer it some food?" but actual prompt uses item name** |
| 5 | events_day_animals.py L790 | `"Try to catch it?"` (raccoon) | YES | 67% chance of Rusty companion |
| 6 | events_day_animals.py L1073 | `"Take the cat to a vet? ($200)"` | YES (if bal≥200) | Saves cat, +15 sanity, prevents cat death event |
| 7 | events_day_survival.py L1114 | `"Pay for the repair? ($100)"` | YES | Fixes carbon monoxide leak — **prevents death** |
| 8 | events_day_survival.py L1662 | `"Throw it away?"` (old photo) | NO | Keeping photo: neutral. Throwing: -5 sanity |
| 9 | events_day_survival.py L1721 | `'"Do you?"'` (Father Ezekiel) | Either | Religious flag has minor story effects |
| 10 | events_day_people.py L1051 | `"Pay the ticket?"` | YES (if affordable) | Avoids potential escalation |
| 11 | events_day_people.py L1375 | `"Take the money?"` (non-loyalty) | YES | Free money when not loyalty-bonus context |
| 12 | events_day_people.py L1404 | `"Keep it?"` | Context | Depends on what "it" is |
| 13 | events_day_people.py L1471 | `"Join the game?"` | Context | Could be gambling — risky |
| 14 | events_day_people.py L1814 | `"Treat yourself to a feast? ($25)"` | YES (low HP/sanity) | Healing for cheap |
| 15 | events_day_people.py L1839 | `"Stay and eat? ($200)"` | NO (expensive) | High cost, moderate healing |
| 16 | events_day_people.py L1862 | `"Play along?"` | YES | Usually harmless + reward |
| 17 | events_day_people.py L1895 | `"Open it?"` | YES | Usually contains reward |
| 18 | events_day_items.py L1080 | `"Use the Ritual Token?"` | YES | Token is consumable; using it has reward |
| 19 | events_day_items.py L1190 | `"Call them? Tell them you found the phone?"` | YES | Good-karma reward |
| 20 | events_day_items.py L1628 | `"Give them the flower?"` | YES | Reward/sanity |
| 21 | events_day_items.py L1748 | `"Open it?"` | YES | Mystery box = usually reward |
| 22 | events_day_items.py L1799 | `"Give it back?"` | YES | Karma reward |
| 23 | events_day_items.py L1845 | `"Post 'found photos' flyers..."` | YES | Reunites photos, +sanity |
| 24 | events_day_items.py L1907 | `"Play?"` | Context | Depends on the game |
| 25 | events_day_items.py L1996 | `"Plant it?"` | YES | Item use + growth event |
| 26 | events_day_items.py L2037 | `"Follow it now?"` | YES | Leads to reward |
| 27 | events_day_items.py L2088 | `"Let it go?"` | Context | Release vs keep |
| 28 | events_day_items.py L2167 | `"Work it out now?"` | YES | Resolve conflict |
| 29 | events_day_items.py L2216 | `"Give it back?"` | YES | Karma reward |
| 30 | events_day_items.py L2234 | `"Sell it to him?"` | Context | Depends on value |
| 31 | events_day_dark.py ~L1850 | `"Pay the mechanic? ($150)"` (fuel leak) | YES | Fixes fuel leak danger |
| 32 | events_day_wealth.py L699 | `"You gonna answer me?"` | YES | Phil— "yes" = 25% death vs "no" = 33% death |
| 33 | events_day_companions.py L1118 | `"Try to befriend the {type}?"` | YES | Dynamic prompt — only "trash gremlin" handled |

---

## 🟡 MEDIUM — Unhandled Inline Choices (Generic Picks Sub-Optimally)

| # | Event | Choices | Bot Picks | Optimal | Delta |
|---|---|---|---|---|---|
| 1 | `street_dice` (adventures) | play/watch/leave | "leave" (preserve) or "play" (normal) | "play" or "watch" depending on balance | Playing has +EV when balance allows |
| 2 | `hitchhiker` sub | drop_her_off/give_money/offer_food/talk_more | "drop_her_off" (first non-risky) | "talk_more" (+sanity, story) or "give_money" (+trust, later reward) | Minor |
| 3 | `fountain_of_youth` (adventures) | drink/wash/bottle/leave | "leave" (keyword priority) | "drink" or "bottle" (healing/item) | Missed healing/item |
| 4 | `tortoise_racing` (adventures) | race/bet/watch | "watch" (keyword) | "race" (chance of winning + fun) | Missed reward |
| 5 | `sunken_shipwreck` (adventures) | explore/quick_loot/photograph/leave | "photograph" (keyword) | "explore" (best loot from captain's quarters etc) | Missed best loot |
| 6 | `underground_den` (adventures) | play/watch/help_woman/leave | "play" (normal keyword) | "help_woman" (moral + story) | Minor |
| 7 | `chess_hustler` (city park night) | play/watch/decline | "watch" (set_map) | "play" if balance allows (30% of +$50-$20 = +EV) | Slight +EV missed |
| 8 | `wild_rat_attack` (animals) | kick it away/run/stand your ground | "run" (generic keyword) | "stand your ground" (lowest total damage: 5-10 HP, 1 sanity) | Minor HP loss |
| 9 | `dance_battle` (surreal) | dynamic moves list | Generic first non-risky | `["worm","robot","spin move","moonwalk","interpretive dance"]` handled → moonwalk. But OTHER move lists would be unhandled | Only matters for non-standard move sets |
| 10 | `hermit_cabin` truth | `ask.yes_or_no("Tell her the truth?")` | Falls to generic (`always_no` has "tell them the truth?" — **her ≠ them**) | YES (gives story progression + reward) | Prompt mismatch |

---

## ✅ LOW PRIORITY — Unhandled but Generic Picks Correctly

These fall to generic fallback but happen to get the right answer by keyword matching.

| Event | Choices | Bot Picks | Why It's Fine |
|---|---|---|---|
| `broken_down_bus` (adventures) | help/sell_water/entertain/rob/ignore | "help" | Best choice — unlocks mechanic bonus |
| `gigantic_bear` (adventures) | fight/flee/offer/submit | "flee" (first non-risky, fight is risky) | Correct — flee is safest |
| `hermit_cabin` (adventures) | knock/peek/leave | "peek" | Safe — avoids risk, still gets lore |
| `disgusting_mermaid` (adventures) | kiss/talk/run/insult | "talk" | Correct — insult is risky, talk → story |
| `bonfire_ritual` (adventures) | join/observe/sabotage/leave | "join" | Correct — unlocks wish sub-event |
| `bonfire wish` (adventures) | wealth/love/power/peace | "peace" (via wish handler) | Correct — safest wish |
| `giant_octopus` (adventures) | fight/communicate/flee/offer | "communicate" | Correct — diplomatic, best outcome |
| `mermaid_kingdom` (adventures) | accept/decline/ask_questions/steal | "accept" | Correct — coral crown reward |
| `overdose_witness` (adventures) | call_911/help/narcan/leave | "call_911" | Correct — safest, best karma |
| `bank_heist sub` (adventures) | reasonable/greedy/pocket_stuff | "reasonable" | Correct — safest split |
| `fairy_bottle` (adventures) | free/keep/negotiate/ignore | "free" (via $1/free handler) | Correct — 3 wishes |
| `fairy wishes` (adventures) | money/luck/health/item/info | "health" first (wish handler) | Correct — health priority when low |
| `swamp alligator` (night) | freeze/splash/swim | "freeze" (first non-risky; set_map doesn't match) | Accidentally correct — 65% success rate (best) |
| `beach check person` (night) | ask.yes_or_no() | YES (blank_prompt) | Correct |
| `woodlands dead body` (night) | ask.yes_or_no() | YES (blank_prompt) | Correct — $100-150 reward (75%) |

---

## 🔧 Item Interactions the Bot Doesn't Account For

The bot's generic fallback has no awareness of inventory. Only these item checks exist in `event_policy`:

| Handler | Items Checked | Used In |
|---|---|---|
| `pull/burn` inline | lighter, matches, road flares | swamp_wade leeches |
| `pet/feed/ignore` inline | can of tuna | city_streets stray cat |
| `car triage` generic | tire patch kit, spare tire | events_car nail |
| `companion sick` choose | cough drops | companion events |

### Missing Item-Aware Choices

| Event | Item | Effect | Bot Behavior |
|---|---|---|---|
| `crow_encounter` | Birdseed/Bread | Befriends Mr. Pecks | Prompt "Offer it some Birdseed?" **doesn't match** always_yes "offer it some food?" |
| `tortoise_racing` | Lettuce | Guaranteed race win bonus | Bot picks "watch" — never races |
| `crab_racing` sub | Fish/Live Fish | Better crab bait | Bot doesn't pick "food" |
| `broken_down_bus` | Duct Tape/Tool Kit | +$50-100 repair bonus | Bot picks "help" ✅ but doesn't know about item bonus |
| `broken_down_bus` | Deck of Cards | +$20-50 entertain bonus | Bot picks "help" — misses entertain with cards |
| `road_dog` | Food items | Better befriend chance | Bot picks "follow" — OK |
| `fountain_of_youth` | Any flask | Can "bottle" the water | Bot picks "leave" — misses item acquisition |
| `homeless_camp` | Food items | share_food bonus | Bot picks "ask_advice" |
| `swamp_wade nectar` | (none needed) | "save" gives Granny's Swamp Nectar item | Bot picks "save" — item is marginal vs drink heal |
| `woodlands_river` | Quiet Sneakers/Slippers | Avoids bear entirely | No choice needed — auto-triggers |
| All Animal Whistle events | Animal Whistle | Auto-befriends companions | No choice needed — auto-triggers before choice |

---

## 📊 Complete Handled-Choice Verification

### Yes/No — Confirmed Handled ✅

| Prompt | Handler | Answer |
|---|---|---|
| "Moo?" | Betsy budget-gate (context-aware) | Conditional on balance/stage |
| "sell your kidney?" | always_no | NO |
| "go back to the tables?" | always_no | NO |
| "buy the painkillers? ($100)" | always_no | NO |
| "buy more pills? ($150...)" | always_no | NO |
| "accept the blood moon bargain?" | always_no | NO |
| "accept the devil's offer?" | always_no | NO |
| "buy the drugs? ($500)" | always_no | NO |
| "lie and say yes?" | always_no | NO |
| "tell them the truth?" | always_no | NO |
| "accept the credit?" | always_no | NO |
| "hold the box for stuart?" | always_no | NO |
| "do you correct her?" | always_no | NO |
| "pay $100 to spin?" | always_no | NO |
| "hang up?" | always_no | NO |
| "pay him $50 for the info?" | always_no | NO |
| "pay $20 for a prophecy?" | always_no | NO |
| "accept his offer?" (always_no + contextual) | always_no / specific | NO / contextual |
| "give jameson $100 for vet bills?" | always_no | NO |
| "ask who 'they' are?" | always_no | NO |
| "do you accept the shadow's offer?" | always_no | NO |
| "take the pill?" | always_no | NO |
| "pay $50 for the pills?" | always_no | NO |
| "feed it some of your food?" | always_yes | YES |
| "take him in?" | always_yes | YES |
| "try to befriend the trash gremlin?" | always_yes | YES |
| "offer it some food?" | always_yes | YES |
| "take the rabbit with you?" | always_yes | YES |
| "follow the duck parade?" | always_yes | YES |
| "throw them some bread/money...?" | always_yes | YES |
| "keep the kitten?" | always_yes | YES |
| "visit him?" | always_yes | YES |
| "listen to him?" | always_yes | YES |
| "do the interview?" | always_yes | YES |
| "do you promise?" | always_yes | YES |
| "talk to... dr. socksworth?" | always_yes | YES |
| "grant the interview?" | always_yes | YES |
| "accept the vip treatment?" | always_yes | YES |
| "shake her hand?" | always_yes | YES |
| "agree to the documentary?" | always_yes | YES |
| "allow the photoshoot?" | always_yes | YES |
| "reply anyway?" | always_yes | YES |
| "try to return it to the owner?" | always_yes | YES |
| "pick her up?" | always_yes | YES |
| "give him money?" | always_yes | YES |
| "are you? gonna leave?" | always_yes | YES |
| "did you? read it?" | always_yes | YES |
| "do you? know this?" | always_yes | YES |
| '"what was that?"' | always_yes | YES |
| '"answer me. "' | always_yes | YES |
| "buy the gyro?" | specific: health/sanity gate | Conditional |
| "hire the bodyguard?" | specific: balance≥20k | Conditional |
| "donate $100 to charity?" | specific: surplus gate | Conditional |
| "pay the $500 fine?" | specific: reserve gate | Conditional |
| "pay to remove the boot?" | specific: reserve gate | Conditional |
| "pay to get your car back?" | specific: reserve gate | Conditional |
| "buy yourself a cupcake?" | specific: sanity gate | Conditional |
| "attend the book club?" | specific: sanity gate | Conditional |
| "$200,000?" (hitman) | specific: balance gate | Conditional |
| gift wrap prompts | specific: dealer happiness gate | Conditional |

### Option Lists — Confirmed Handled ✅

| Options | Handler | Picks |
|---|---|---|
| [pay now, beg for time, refuse] | loan_shark | pay if rich, else beg |
| [ride it out, drive to casino, hurt yourself] | withdrawal | ride_it_out |
| [call for help, try to help yourself, walk away] | overdose | call_for_help |
| [pay/refuse/break down] (cancer) | cancer_diagnosis | pay if rich, else refuse |
| [climb/call someone/walk away] (bridge) | bridge_call | call_someone |
| [agree to leave, offer money, fight back] | hitman | agree_to_leave |
| [comply, run, fight] | back_alley | comply |
| [comply, hide, hero] | gas_station | hide |
| [wrong person, play along, run] | drug_dealer | wrong_person |
| [step back, stay, call for help] | bridge_contemplation | stay (bridge angel chain) |
| [bail out, investigate, ignore] | car_explosion | bail_out |
| [try it, sell it, throw it away] | cocaine | sell_it |
| [eat it anyway, apologize, throw it] | sentient_sandwich | apologize (eat if low HP) |
| [use it, throw it away, return it] | companion find | return |
| [keep the cash, return it all] | companion cash | return_it_all |
| [sell it, turn it in] | companion evidence | turn_it_in |
| [take it, leave it] | companion gift | take_it |
| [heads, tails] | coin_flip | heads |
| [violinist, drummer, neither] | busker tip | neither |
| [confident, humble, no comment] | press interview | humble |
| [apologize, confront, ask for help] | wealth conflict | ask_for_help |
| [worm, robot, spin move, moonwalk, interpretive dance] | dance_battle | moonwalk |
| [save the bird, ignore your phone, scream] | surreal loop | ignore_phone |
| [not interested, what are you offering, souls?] | soul dealer | not_interested |
| [pill menu] | painkiller | cold_turkey |
| [jameson rescue] | jameson | help if HP≥65, else honk |
| [lucky prove] | lucky dispute | prove_it |
| [combination lock] | numbers | try_combination |
| [pull it out, leave it, drive to shop] | car triage (special generic) | drive_to_shop if bal≥25 |
| millionaire ending menu | millionaire handler | mechanic/airport per config |

### Inline Choices — Confirmed Handled via set_map ✅

| Choice Set | Picks | Event |
|---|---|---|
| {around, wait} | wait | swamp snake |
| {force, take} | force | swamp lockbox |
| {enter, judge, sabotage, watch} | judge | sandcastle contest |
| {help, buy, swim} | help | swamp witch boat |
| {luck, love, revenge} | luck | witch charms |
| {tough, beach} | beach | jellyfish |
| {fight, parallel, float} | parallel | riptide |
| {open, save} | open | oyster / lockbox |
| {keep, return} | return | underwater camera |
| {swim, still, scare} | still | shark encounter |
| {accept, decline, scram} | decline | city drug dealer |
| {nice, cheap, skip} | skip | rental bike |
| {listen, tip, walk} | listen | busker |
| {help, run, sneak, film} | film | bank robbery witness |
| {help, love, dodge} | love | dog walker |
| {fight, talk, comply, run} | comply | city mugging |
| {tip, flinch, watch} | watch | street performer |
| {help, ignore, trick} | help | lost tourist |
| {feed, flee, dominance} | dominance | pigeon park |
| {sit, money, walk} | sit | hobo joe |
| {line, cut, resist} | line | free pizza |
| {feed, skip, sit} | sit | park pond |
| {play, watch, decline} | watch | chess hustler |
| {approach, watch, leave} | watch | midnight gardener |
| {pull, burn} | conditional (inventory) | leeches |
| {pet, feed, ignore} | conditional (tuna) | stray cat |

---

## 🏆 Priority Fix List

### Tier 1 — Immediate Fixes (wrong answers / lost money / death risk)

1. **Add `"do you applaud?"` to `always_yes`** — loses $20 every mime encounter
2. **Remove `"do you sit and listen?"` from `blank_prompt_listen_no`** (or add to investigate_yes) — loses $50-150
3. **Add `"do you eat her soup?"` to `blank_prompt_investigate_yes`** — misses 15-30 HP heal + blessings
4. **Add `"pay for the repair? ($100)"` handler** — YES if bal≥100 (prevents carbon monoxide death)
5. **Add `"pay the mechanic? ($150)"` handler** — YES if bal≥150 (fixes fuel leak danger)
6. **Add `"you gonna answer me?"` to `always_yes`** — Phil's interrogation: YES = 25% death, NO = 33% death
7. **Add `"accept earl's moonshine?"` to `always_yes`** — heals + free money/items
8. **Add `"use the carrot to lure the rabbit?"` to `always_yes`** — 33% of $500-2000 reward
9. **Add `set_map` entry `{"drink", "save", "toss"}: ("drink", "nectar_drink_heal")`** — 67% chance of 10-50 HP heal
10. **Add `set_map` entry for roadside shrine** — stop bot from wasting money on "leave_offering" when "pray" is free healing
11. **Add voodoo_doll option handler** `["stick a pin in it", "burn it", "keep it safe"]` → "burn it" or "keep it safe"

### Tier 2 — Missed Opportunities (sub-optimal choices)

12. **Fix midnight gardener**: change `{approach, watch, leave}` → "approach" (gets Midnight Rose item)
13. **Add `"try to catch it?"` to `always_yes`** — raccoon 67% companion chance
14. **Add `"take the cat to a vet? ($200)"` handler** — YES if bal≥400 (saves cat + 15 sanity)
15. **Fix crow prompt mismatch**: `always_yes` has "offer it some food?" but actual prompt is "Offer it some Birdseed/Bread?" — add variants or use `in` matching
16. **Add `"open it?"` to `always_yes`** — covers Giant Oyster + misc item events
17. **Add hermit truth handler**: "Tell her the truth?" ≠ always_no's "tell them the truth?" — needs separate entry
18. **Add dynamic befriend handler**: `"try to befriend the"` substring match instead of exact "try to befriend the trash gremlin?"
19. **Improve adventure choices**: most adventure sub-events (street_dice, tortoise_racing, hunting_competition, shipwreck explore) fall to generic and pick conservative/wrong options

### Tier 3 — Nice to Have (minor EV improvements)

20. Add feast/meal handlers for events_day_people food choices
21. Add item-event handlers for events_day_items (ritual token, phone, flower, etc.)
22. Consider item-aware inline choices (Lettuce for tortoise, Deck of Cards for entertain, etc.)
23. Add `"throw it away?"` (old photo) to `always_no` — preserves sanity
24. Improve `"Do you?"` (Ezekiel) handling based on strategy

---

## 📈 Coverage Statistics

| Category | Total | Handled | Generic (correct) | Generic (wrong) | Unhandled |
|---|---|---|---|---|---|
| **Yes/No (always sets)** | ~80 | 55 (69%) | ~10 (12%) | 3 (4%) | 12 (15%) |
| **Option lists** | ~30 | 26 (87%) | 3 (10%) | 1 (3%) | 0 |
| **Inline (set_map)** | ~40 | 25 (63%) | 8 (20%) | 4 (10%) | 3 (7%) |
| **Inline (adventures)** | ~50 | 3 (6%) | 30 (60%) | 7 (14%) | 10 (20%) |
| **TOTAL** | **~200** | **109 (55%)** | **51 (25%)** | **15 (8%)** | **25 (12%)** |

> **Adventures.py is the biggest gap.** Only 3 of ~50 adventure inline choices have specific handlers;  
> the rest rely on generic keyword matching, which picks sub-optimally ~30% of the time.
