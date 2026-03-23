# Example personality: Aggressive

PERSONALITY_NAME = "aggressive"

# This config or module can be imported by the harness or policy modules.
# You can define parameters, override functions, or provide a class.

# Example: Aggressive blackjack betting (always bet max allowed)
def choose_blackjack_bet(game_state, min_bet, max_bet):
    return max_bet

# Example: Aggressive shop policy (always buy Marvin items if possible)
def choose_shop_option(menu_options, inventory):
    for option in menu_options:
        if "marvin" in option.lower():
            return option
    return menu_options[0]  # fallback
