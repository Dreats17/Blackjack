# Personality: Car Strategist

PERSONALITY_NAME = "car_strategist"

# This personality prioritizes getting a car and chooses mechanics according to optimal strategy.
# - Always tries to get Tom if possible (affordable and available)
# - Chooses Oswald only if affordable and Tom is not available
# - Avoids Frank unless no other option
# - Skips mechanic if can't afford Tom or Oswald, but will take Frank as last resort
# - Prioritizes car acquisition for location unlocks and story progression

def choose_mechanic_option(mechanic_options, game_state):
    # mechanic_options: list of dicts with 'name' and 'cost'
    # game_state: dict with at least 'balance'
    balance = game_state.get("balance", 0)
    tom = next((opt for opt in mechanic_options if "tom" in opt["name"].lower()), None)
    oswald = next((opt for opt in mechanic_options if "oswald" in opt["name"].lower()), None)
    frank = next((opt for opt in mechanic_options if "frank" in opt["name"].lower()), None)

    # Prefer Tom if affordable
    if tom and tom["cost"] <= balance:
        return tom["name"]
    # If Oswald is available and affordable, and Tom is not, take Oswald
    if oswald and oswald["cost"] <= balance:
        return oswald["name"]
    # If Frank is available and neither Tom nor Oswald are affordable, take Frank as last resort
    if frank and (not tom or tom["cost"] > balance) and (not oswald or oswald["cost"] > balance):
        return frank["name"]
    # Otherwise, skip mechanic (return None)
    return None

# Example: Always bet minimum unless car is owned, then bet more aggressively

def choose_blackjack_bet(game_state, min_bet, max_bet):
    if game_state.get("has_car", False):
        # With car, bet more aggressively
        return max(min_bet * 3, min(max_bet, game_state.get("balance", 0) // 10))
    return min_bet

# Example: Prioritize car-related purchases in shop

def choose_shop_option(menu_options, inventory):
    # If car-related item is available, buy it
    for option in menu_options:
        if "car" in option.lower() or "mechanic" in option.lower():
            return option
    # Otherwise, pick first affordable item
    return menu_options[0] if menu_options else None
