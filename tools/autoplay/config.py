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
    # Priorities must exceed max(56, rank_store_priority_min - 16) = 68 at rank 1 to trigger store
    # visits when the item is the best available (rank tuner store_priority_min=84 at rank 1).
    "Garbage Bag": 72,    # Emergency Blanket (74), Rain Collector (58), Smoke Signal Kit (60); all ranks
    "Plastic Wrap": 70,   # Feeding Station (78), Water Purifier (64), Rain Collector (58); all ranks
    "Fishing Line": 72,   # Lockpick Set (72), Improvised Trap (62), Fishing Rod (54); rank 2 store
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
    "Pocket Watch": 96,
    "Lucky Coin": 92,
    "Gambler's Grimoire": 82,
    "Faulty Insurance": 90,
    "Dirty Old Hat": 72,
    "Golden Watch": 80,
    # Health Indicator ($8k-$9.5k): shows real-time HP — useful for planning doctor visits.
    # Delight Indicator ($8.5k-$10k): shows dealer/NPC happiness — feeds gift-wrap gate logic.
    # Both are the cheapest Marvin items alongside Rusty Compass and Gambler's Grimoire.
    "Health Indicator": 64,
    "Delight Indicator": 68,
    "Worn Gloves": 90,
    "Tattered Cloak": 86,
    "Gambler's Chalice": 84,
    "White Feather": 78,
    "Twin's Locket": 76,
    "Dealer's Grudge": 74,
    "Rusty Compass": 82,
    "Quiet Sneakers": 84,
    "Sneaky Peeky Shades": 86,
    "Enchanting Silver Bar": 56,
    "Animal Whistle": 72,
}

MARVIN_PRICE_ESTIMATES: dict[str, int] = {
    # Conservative estimates — deliberately set near the UPPER END of each item's
    # actual price range so the bot only visits Marvin when it can absorb any roll.
    # The actual game prices in locations.py were reduced ~25%, so this creates a
    # "pleasant discount" effect: the bot budgets for the high end and usually pays less.
    "Delight Indicator": 8500,
    "Health Indicator": 8000,
    "Dirty Old Hat": 25000,
    "Golden Watch": 29000,
    "Faulty Insurance": 10000,
    "Enchanting Silver Bar": 10000,
    "Sneaky Peeky Shades": 35000,
    "Quiet Sneakers": 15000,
    "Lucky Coin": 12000,
    "Worn Gloves": 18000,
    "Tattered Cloak": 22000,
    "Rusty Compass": 8000,
    "Pocket Watch": 20000,
    "Gambler's Chalice": 28000,
    "Twin's Locket": 35000,
    "White Feather": 15000,
    "Dealer's Grudge": 22000,
    "Gambler's Grimoire": 8000,
    "Animal Whistle": 50000,
}

MARVIN_ITEM_ORDER: tuple[str, ...] = (
    "Pocket Watch",
    "Lucky Coin",
    "Gambler's Grimoire",
    "Faulty Insurance",
    "Dirty Old Hat",
    "Golden Watch",
    "Worn Gloves",
    "Tattered Cloak",
    "Gambler's Chalice",
    "White Feather",
    "Twin's Locket",
    "Dealer's Grudge",
    "Rusty Compass",
    "Quiet Sneakers",
    "Sneaky Peeky Shades",
    "Enchanting Silver Bar",
    "Animal Whistle",
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
    "No Bust": 92,
    "Second Chance": 90,
    "Dealer's Whispers": 84,
    "Bonus Fortune": 80,
    "Split Serum": 76,
    "Dealer's Hesitation": 72,
    "Pocket Aces": 68,
    "Imminent Blackjack": 66,
    "Anti-Virus": 58,
    "Anti-Venom": 54,
    # Fortunate Day/Night are the cheapest flasks (min $12k each from code).
    # Raising their priorities enables the flask-only visit path at rank 2 ($10k+).
    "Fortunate Day": 58,    # was 44; gives all day events a positive tilt
    "Fortunate Night": 44,  # was 28; gives all night events a positive tilt
}

# Price estimates use minimum values from visit_witch_doctor random.choice() ranges.
# Using minimums means the bot will attempt a visit when it CAN afford the cheapest
# roll; if the actual roll is higher the bot will decline, but healing may still apply.
WITCH_FLASK_PRICE_ESTIMATES: dict[str, int] = {
    # Conservative estimates — set near the upper end of each flask's price range.
    # The actual game prices in locations.py were reduced ~25%, so visits are
    # triggered at the old balance threshold but the bot pays less on average.
    "No Bust": 25000,
    "Imminent Blackjack": 40000,
    "Dealer's Whispers": 23000,
    "Bonus Fortune": 35000,
    "Anti-Venom": 25000,
    "Anti-Virus": 26000,
    "Fortunate Day": 12000,
    "Fortunate Night": 12000,
    "Second Chance": 28000,
    "Split Serum": 30000,
    "Dealer's Hesitation": 20000,
    "Pocket Aces": 45000,
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
        "marvin_min_balance": 9000,
        "marvin_floor_buffer": 3000,
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
        "marvin_min_balance": 9500,
        "marvin_floor_buffer": 3000,
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
        "marvin_min_balance": 9500,
        "marvin_floor_buffer": 5000,
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

# Gift wrapping: dealer_happiness threshold below which gift-wrapping is worth doing
GIFT_WRAP_HAPPINESS_THRESHOLD: int = 78

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