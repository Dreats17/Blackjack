# Example personality: Conservative

PERSONALITY_NAME = "conservative"

def choose_blackjack_bet(game_state, min_bet, max_bet):
    # Bet minimum unless bankroll is very high
    if game_state.get("balance", 0) > 1000:
        return max_bet // 2
    return min_bet

def choose_shop_option(menu_options, inventory):
    # Only buy if not already owned
    for option in menu_options:
        if "marvin" in option.lower() and option not in inventory:
            return option
    return None  # skip purchase if nothing needed
