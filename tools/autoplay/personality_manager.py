# Dynamic Personality Manager for Autoplayer
# This module selects and loads the appropriate personality module based on the current strategic goal or game state.

import importlib

# Map strategic goals to personality module names
GOAL_TO_PERSONALITY = {
    "acquire_car": "car_strategist",
    "exploit_marvin": "aggressive",
    "restock_supplies": "conservative",
    "push_next_rank": "aggressive",
    # Add more mappings as needed
}

class PersonalityManager:
    def __init__(self):
        self._loaded = {}
        self._current = None

    def get_personality(self, goal: str):
        module_name = GOAL_TO_PERSONALITY.get(goal, "conservative")
        if module_name not in self._loaded:
            self._loaded[module_name] = importlib.import_module(f"tools.{module_name}")
        self._current = self._loaded[module_name]
        return self._current

# Singleton instance
personality_manager = PersonalityManager()
