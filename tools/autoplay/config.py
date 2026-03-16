from __future__ import annotations


STORE_CAR_SURVIVAL_PRIORITIES: dict[str, int] = {
    "Spare Tire": 100,
    "Tire Patch Kit": 98,
    "Fix-a-Flat": 95,
    "Tool Kit": 93,
    "OBD Scanner": 84,
    "Portable Battery Charger": 80,
    "Jumper Cables": 78,
    "Motor Oil": 74,
    "Brake Fluid": 72,
    "Spare Fuses": 70,
}

STORE_PERSONAL_SURVIVAL_PRIORITIES: dict[str, int] = {
    "LifeAlert": 104,
    "First Aid Kit": 102,
    "Road Flares": 96,
    "Bug Spray": 92,
    "Flashlight": 88,
    "Duct Tape": 82,
    "Water Bottles": 78,
    "Pocket Knife": 74,
    "Binoculars": 40,
}

STORE_PROGRESSION_PRIORITIES: dict[str, int] = {
    "Worn Map": 56,
    "Signal Booster": 58,
    "Super Glue": 48,
    "Hand Warmers": 34,
    "Dog Whistle": 26,
    "Leather Gloves": 22,
    "Silver Flask": 20,
    "Fancy Pen": 18,
    "Vintage Wine": 16,
    "Lucky Rabbit Foot": 36,
    "Antique Pocket Watch": 20,
    "Lottery Ticket": 14,
    "Lucky Penny": 12,
    # Crafting ingredients (Car Workbench recipes) — verified from lists.py make_crafting_recipes
    # These items have priority 0 elsewhere and are therefore NEVER bought without this table.
    # With the crafting synergy boost in _store_item_priority, the effective priority
    # becomes recipe_priority + 4 (starting boost) or + 12 (completing boost), so an
    # ingredient for Emergency Blanket (74) reaches 78 or 86 respectively.
    # Base priorities here ensure items are considered even before the synergy fires.
    "Garbage Bag": 72,    # Emergency Blanket (74), Rain Collector (58), Smoke Signal Kit (60); all ranks
    "Plastic Wrap": 70,   # Feeding Station (78), Water Purifier (64), Rain Collector (58); all ranks
    "Fishing Line": 72,   # Lockpick Set (72), Improvised Trap (62), Fishing Rod (54); rank 2 store
    "Rope": 64,           # Fishing Rod (54), Splint (70), Snare Trap (52); all ranks car-maintenance store
    "Bungee Cords": 56,   # Car Alarm Rigging (66), Slingshot (46); all ranks car-maintenance store
    "Rubber Bands": 30,   # Dream Catcher (50), Slingshot (46); rank 0 store only
    "Breath Mints": 30,   # Smelling Salts (66) needs Hand Warmers + Breath Mints; rank 0 store only
}

STORE_MUST_HAVE_ITEMS: frozenset[str] = frozenset(
    {
        "Spare Tire",
        "Tire Patch Kit",
        "Fix-a-Flat",
        "Tool Kit",
        "First Aid Kit",
        "LifeAlert",
        "Road Flares",
        "Bug Spray",
        "Flashlight",
    }
)

MARVIN_ITEM_PRIORITIES: dict[str, int] = {
    "Faulty Insurance": 100,
    "Rusty Compass": 99,
    "Lucky Coin": 97,
    "Pocket Watch": 96,
    "White Feather": 95,
    "Gambler's Chalice": 94,
    "Sneaky Peeky Shades": 93,
    "Twin's Locket": 92,
    "Quiet Sneakers": 90,
    "Tattered Cloak": 90,
    "Worn Gloves": 91,
    "Dealer's Grudge": 89,
    "Marvin's Monocle": 18,
    "Health Indicator": 0,
    "Delight Indicator": 0,
    "Golden Watch": 88,
    "Gambler's Grimoire": 87,
    "Animal Whistle": 84,
    "Dirty Old Hat": 82,
    "Enchanting Silver Bar": 50,
}

MARVIN_PRICE_ESTIMATES: dict[str, int] = {
    # Minimum live-code Marvin prices from story/locations.py.
    "Delight Indicator": 6500,
    "Health Indicator": 6000,
    "Dirty Old Hat": 18000,
    "Golden Watch": 22000,
    "Faulty Insurance": 7500,
    "Enchanting Silver Bar": 7500,
    "Sneaky Peeky Shades": 26000,
    "Quiet Sneakers": 11000,
    "Lucky Coin": 9000,
    "Worn Gloves": 14000,
    "Tattered Cloak": 16000,
    "Rusty Compass": 6000,
    "Pocket Watch": 15000,
    "Marvin's Monocle": 10000,
    "Gambler's Chalice": 21000,
    "Twin's Locket": 26000,
    "White Feather": 11000,
    "Dealer's Grudge": 16000,
    "Gambler's Grimoire": 6000,
    "Animal Whistle": 40000,
}

MARVIN_ITEM_ORDER: tuple[str, ...] = (
    "Faulty Insurance",
    "Rusty Compass",
    "Lucky Coin",
    "Pocket Watch",
    "White Feather",
    "Quiet Sneakers",
    "Gambler's Chalice",
    "Sneaky Peeky Shades",
    "Twin's Locket",
    "Tattered Cloak",
    "Worn Gloves",
    "Dealer's Grudge",
    "Marvin's Monocle",
    "Gambler's Grimoire",
    "Health Indicator",
    "Delight Indicator",
    "Golden Watch",
    "Animal Whistle",
    "Dirty Old Hat",
    "Enchanting Silver Bar",
)

UPGRADE_ITEM_PRIORITIES: dict[str, int] = {
    "Pocket Watch": 100,
    "Worn Gloves": 98,
    "Lucky Coin": 96,
    "Tattered Cloak": 94,
    "Faulty Insurance": 92,
    "Gambler's Chalice": 90,
    "Sneaky Peeky Shades": 88,
    "Twin's Locket": 86,
    "White Feather": 84,
    "Dealer's Grudge": 82,
    "Rusty Compass": 80,
    "Gambler's Grimoire": 78,
    "Quiet Sneakers": 76,
    "Golden Watch": 74,
    "Dirty Old Hat": 62,
    "Health Indicator": 0,
    "Delight Indicator": 0,
}

UPGRADE_PRICE_ESTIMATES: dict[str, int] = {
    "Delight Indicator": 150000,
    "Health Indicator": 150000,
    "Dirty Old Hat": 200000,
    "Golden Watch": 300000,
    "Sneaky Peeky Shades": 400000,
    "Quiet Sneakers": 250000,
    "Faulty Insurance": 120000,
    "Lucky Coin": 200000,
    "Worn Gloves": 250000,
    "Tattered Cloak": 300000,
    "Rusty Compass": 160000,
    "Pocket Watch": 350000,
    "Gambler's Chalice": 350000,
    "Twin's Locket": 400000,
    "White Feather": 280000,
    "Dealer's Grudge": 320000,
    "Gambler's Grimoire": 250000,
}

WITCH_FLASK_PRIORITIES: dict[str, int] = {
    "No Bust": 98,
    "Second Chance": 96,
    "Dealer's Whispers": 94,
    "Bonus Fortune": 92,
    "Dealer's Hesitation": 88,
    "Split Serum": 86,
    "Pocket Aces": 84,
    "Imminent Blackjack": 82,
    "Anti-Virus": 58,
    "Anti-Venom": 54,
    "Fortunate Day": 62,
    "Fortunate Night": 60,
}

# Price estimates use minimum live-code values from visit_witch_doctor random.choice() ranges.
# Using the minimum lets the harness test whether a visit is worth attempting as soon as
# the cheapest roll is possible; if the actual roll is higher the bot can still decline.
WITCH_FLASK_PRICE_ESTIMATES: dict[str, int] = {
    "No Bust": 18000,
    "Imminent Blackjack": 30000,
    "Dealer's Whispers": 17000,
    "Bonus Fortune": 26000,
    "Anti-Venom": 18000,
    "Anti-Virus": 19000,
    "Fortunate Day": 8000,
    "Fortunate Night": 8000,
    "Second Chance": 21000,
    "Split Serum": 22000,
    "Dealer's Hesitation": 15000,
    "Pocket Aces": 34000,
}


RANK_TUNER_PROFILES: dict[int, dict[str, float | int]] = {
    0: {
        "bet_ratio": 0.17,
        "bet_ratio_safe": 0.12,
        "max_ratio": 0.26,
        "pressure_factor": 0.62,
        "surplus_push": 0.42,
        "floor_keep_base": 1.00,
        "floor_keep_mid": 0.97,
        "floor_keep_high": 0.92,
        "store_priority_min": 80,
        "store_balance_gate": 250,
        "store_health_gate": 60,
        "store_sanity_gate": 30,
        "marvin_min_balance": 3500,
        "marvin_floor_buffer": 1800,
        "upgrade_floor_buffer": 150000,
    },
    1: {
        "bet_ratio": 0.24,
        "bet_ratio_safe": 0.16,
        "max_ratio": 0.36,
        "pressure_factor": 0.72,
        "surplus_push": 0.54,
        "floor_keep_base": 1.00,
        "floor_keep_mid": 0.98,
        "floor_keep_high": 0.93,
        "store_priority_min": 84,
        "store_balance_gate": 600,
        "store_health_gate": 60,
        "store_sanity_gate": 28,
        "marvin_min_balance": 4000,
        "marvin_floor_buffer": 2000,
        "upgrade_floor_buffer": 180000,
    },
    2: {
        "bet_ratio": 0.28,
        "bet_ratio_safe": 0.18,
        "max_ratio": 0.42,
        "pressure_factor": 0.74,
        "surplus_push": 0.54,
        "floor_keep_base": 1.00,
        "floor_keep_mid": 0.96,
        "floor_keep_high": 0.90,
        "store_priority_min": 86,
        "store_balance_gate": 5000,
        "store_health_gate": 58,
        "store_sanity_gate": 26,
        "marvin_min_balance": 8000,
        "marvin_floor_buffer": 3500,
        "upgrade_floor_buffer": 140000,
    },
    3: {
        "bet_ratio": 0.31,
        "bet_ratio_safe": 0.27,
        "max_ratio": 0.50,
        "pressure_factor": 0.74,
        "surplus_push": 0.68,
        "floor_keep_base": 0.94,
        "floor_keep_mid": 0.88,
        "floor_keep_high": 0.80,
        "store_priority_min": 64,
        "store_balance_gate": 5000,
        "store_health_gate": 55,
        "store_sanity_gate": 24,
        "marvin_min_balance": 22000,
        "marvin_floor_buffer": 8000,
        "upgrade_floor_buffer": 120000,
    },
    4: {
        "bet_ratio": 0.30,
        "bet_ratio_safe": 0.24,
        "max_ratio": 0.50,
        "pressure_factor": 0.76,
        "surplus_push": 0.68,
        "floor_keep_base": 0.92,
        "floor_keep_mid": 0.86,
        "floor_keep_high": 0.78,
        "store_priority_min": 58,
        "store_balance_gate": 15000,
        "store_health_gate": 52,
        "store_sanity_gate": 22,
        "marvin_min_balance": 75000,
        "marvin_floor_buffer": 25000,
        "upgrade_floor_buffer": 100000,
    },
    5: {
        "bet_ratio": 0.24,
        "bet_ratio_safe": 0.20,
        "max_ratio": 0.46,
        "pressure_factor": 0.72,
        "surplus_push": 0.62,
        "floor_keep_base": 0.90,
        "floor_keep_mid": 0.84,
        "floor_keep_high": 0.76,
        "store_priority_min": 52,
        "store_balance_gate": 50000,
        "store_health_gate": 50,
        "store_sanity_gate": 20,
        "marvin_min_balance": 180000,
        "marvin_floor_buffer": 50000,
        "upgrade_floor_buffer": 90000,
    },
}


# Crafting recipe strategic priorities (higher = more worth crafting)
# Categories: companion items > remedies > survival > tools > traps > weapons > charms
CRAFTING_RECIPE_PRIORITIES: dict[str, int] = {
    # Companion items - high value when companions present
    "Companion Bed": 88,
    "Pet Toy": 72,
    "Feeding Station": 78,
    # Remedies - good when injured or sick
    "Home Remedy": 82,
    "Wound Salve": 84,
    "Splint": 70,
    "Smelling Salts": 66,
    # Survival - broad utility
    "Emergency Blanket": 74,
    "Fire Starter Kit": 68,
    "Water Purifier": 64,
    "Rain Collector": 58,
    "Smoke Signal Kit": 60,
    # Tools - utility
    "Binocular Scope": 76,
    "Lockpick Set": 72,
    "Fishing Rod": 54,
    "Signal Mirror": 48,
    # Traps - situational
    "Improvised Trap": 62,
    "Car Alarm Rigging": 66,
    "Snare Trap": 52,
    # Weapons - defensive
    "Road Flare Torch": 70,
    "Pepper Spray": 68,
    "Shiv": 56,
    "Slingshot": 46,
    # Charms - low direct utility
    "Lucky Charm Bracelet": 44,
    "Dream Catcher": 50,
    "Worry Stone": 40,
}

# Minimum strategic priority to bother crafting.
# Recipes with priority >= this threshold are considered worth crafting.
# Companion items receive a +18 bonus in quicktest.py when companions are present,
# which may push them above this threshold even if their base priority is below it.
CRAFTING_MIN_PRIORITY: int = 60

# At rank 2+, store visits only block adventure when the best store candidate has at
# least this priority — i.e., truly urgent items like Tool Kit (93), Spare Tire (100),
# Road Flares (96), or First Aid Kit (100).  Lower-priority items (Duct Tape ~62,
# crafting ingredients 54-72) should NOT cancel a valid adventure run.
CRITICAL_STORE_PRIORITY_THRESHOLD: int = 90

# Gift wrapping: dealer_happiness threshold below which gift-wrapping is worth doing.
# Keep this just below the first free-hand breakpoint so the bot actively tops up
# dealer happiness instead of waiting until the relationship has already fallen off.
GIFT_WRAP_HAPPINESS_THRESHOLD: int = 92

# Gift wrapping: minimum balance to spend on wrapping (wrapping costs a small amount)
GIFT_WRAP_MIN_BALANCE: int = 30

# Items worth gifting to the dealer (sorted by value to the gift system)
GIFT_WORTHY_ITEMS: tuple[str, ...] = (
    "Vintage Wine",
    "Fancy Pen",
    "Leather Gloves",
    "Lucky Rabbit Foot",
    "Antique Pocket Watch",
    "Silver Flask",
)

# Millionaire ending preference order by strategic weight (mechanic ending > airport by default)
# "mechanic" means visit chosen mechanic for the special ending
# "airport" means drive to the airport
MILLIONAIRE_ENDING_PREFERENCE: tuple[str, ...] = ("mechanic", "airport")


def get_rank_tuner(rank: int) -> dict[str, float | int]:
    normalized_rank = max(0, min(int(rank), max(RANK_TUNER_PROFILES)))
    return dict(RANK_TUNER_PROFILES[normalized_rank])


def get_store_base_priority(item_name: str) -> int:
    if item_name in STORE_PERSONAL_SURVIVAL_PRIORITIES:
        return STORE_PERSONAL_SURVIVAL_PRIORITIES[item_name]
    if item_name in STORE_CAR_SURVIVAL_PRIORITIES:
        return STORE_CAR_SURVIVAL_PRIORITIES[item_name]
    return STORE_PROGRESSION_PRIORITIES.get(item_name, 0)


def get_marvin_base_priority(item_name: str) -> int:
    return MARVIN_ITEM_PRIORITIES.get(item_name, 0)


def get_marvin_price_estimate(item_name: str) -> int:
    return MARVIN_PRICE_ESTIMATES.get(item_name, 10**9)


def get_upgrade_base_priority(item_name: str) -> int:
    return UPGRADE_ITEM_PRIORITIES.get(item_name, 0)


def get_upgrade_price_estimate(item_name: str) -> int:
    return UPGRADE_PRICE_ESTIMATES.get(item_name, 10**9)


def get_witch_flask_base_priority(flask_name: str) -> int:
    return WITCH_FLASK_PRIORITIES.get(flask_name, 0)


def get_crafting_recipe_priority(recipe_name: str) -> int:
    return CRAFTING_RECIPE_PRIORITIES.get(recipe_name, 0)


def get_witch_flask_price_estimate(flask_name: str) -> int:
    return WITCH_FLASK_PRICE_ESTIMATES.get(flask_name, 10**9)