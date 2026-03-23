# Example personality: Random

PERSONALITY_NAME = "random"
import random

def choose_blackjack_bet(game_state, min_bet, max_bet):
    return random.randint(min_bet, max_bet)

def choose_shop_option(menu_options, inventory):
    return random.choice(menu_options) if menu_options else None
