
import story
import lists

RANKS = [
    (0, "Poor"),
    (1, "Cheap"),
    (2, "Modest"),
    (3, "Rich"),
    (4, "Doughman"),
    (5, "Nearly There")
]
DAY_EVENT_LISTS = [
    "make_poor_day_events_list",
    "make_cheap_day_events_list",
    "make_modest_day_events_list",
    "make_rich_day_events_list",
    "make_doughman_day_events_list",
    "make_nearly_day_events_list"
]
NIGHT_EVENT_LISTS = [
    "make_poor_night_events_list",
    "make_cheap_night_events_list",
    "make_modest_night_events_list",
    "make_rich_night_events_list",
    "make_doughman_night_events_list",
    "make_nearly_night_events_list"
]

def get_event_names():
    # Gather all event names by rank and day/night
    event_dict = {"day": {}, "night": {}}
    dummy_player = story.Player()
    l = lists.Lists(dummy_player)
    for i, (rank, rank_name) in enumerate(RANKS):
        day_func = getattr(l, DAY_EVENT_LISTS[i])
        night_func = getattr(l, NIGHT_EVENT_LISTS[i])
        event_dict["day"][rank_name] = sorted(day_func())
        event_dict["night"][rank_name] = sorted(night_func())
    return event_dict

def choose(options, prompt):
    for i, opt in enumerate(options):
        print(f"{i+1}. {opt}")
    while True:
        choice = input(prompt)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print("Invalid selection. Try again.")


def get_min_balance_for_rank(rank_name):
    # Based on your event tiers
    return {
        "Poor": 0,
        "Cheap": 1000,
        "Modest": 10000,
        "Rich": 100000,
        "Doughman": 500000,
        "Nearly There": 900000
    }[rank_name]


def main():
    print("Blackjack Story Event Runner (Manual, Sorted, Direct)\n")
    event_dict = get_event_names()
    day_or_night = choose(["day", "night"], "Day or night events? ")
    rank = choose([r[1] for r in RANKS], "Choose rank: ")
    events = event_dict[day_or_night][rank]
    event = choose(events, f"Choose event to run for {rank} ({day_or_night}): ")

    player = story.Player()
    # Set rank and minimum balance for the event
    if hasattr(player, "_Player__rank"):
        setattr(player, "_Player__rank", [r[0] for r in RANKS if r[1] == rank][0])
    min_balance = get_min_balance_for_rank(rank)
    if hasattr(player, "set_balance"):
        player.set_balance(min_balance)
    elif hasattr(player, "_Player__balance"):
        setattr(player, "_Player__balance", min_balance)

    print(f"\nRunning event: {event}\n")
    if hasattr(player, event):
        getattr(player, event)()
    else:
        print(f"Player has no event '{event}'")

if __name__ == "__main__":
    main()
