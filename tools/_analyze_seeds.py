"""Quick analysis of test_out.json for win study."""
import json, sys

d = json.load(open('tools/test_out.json'))
rs = d['run_summary']
fs = d['final_state']
g = fs.get('gambling', {})
dt = d.get('decision_traces', [])
ds = d.get('decision_summary', {})
rc = ds.get('reason_code_counts', {})
modes = {k: v for k, v in rc.items() if k.startswith('bet:')}
ip = d.get('item_provenance', {})

lucky_day = car_day = None
for name, prov in ip.items():
    acq = prov.get('acquired', [])
    if 'Lucky' in name and acq:
        lucky_day = acq[0].get('day')
    if name == 'Car' and acq:
        car_day = acq[0].get('day')

by_day = {}
for t in dt:
    if isinstance(t, dict) and t.get('context') == 'blackjack_bet':
        gs_ = t.get('game_state_summary', {})
        day = t.get('day', 0)
        bal = gs_.get('balance', 0)
        by_day[day] = max(by_day.get(day, 0), bal)

pk = max(by_day.items(), key=lambda x: x[1]) if by_day else (0, 0)

seed = d.get('seed', '?')
print(f'=== SEED {seed} ===')
print(f'Outcome: {rs.get("result_note", "?")}')
print(f'Days: {rs["day"]}  Peak: ${rs["peak_balance"]:,}  End: ${rs["balance"]:,}  Death: {rs.get("death_cause", "none")}')
print(f'Car day: {car_day}  Lucky Coin day: {lucky_day}')
print(f'Hands: {g["total_hands"]}  W: {g["wins"]}  L: {g["losses"]}  BJ: {g["blackjacks"]}')
print(f'Won: ${g["total_won"]:,}  Lost: ${g["total_lost"]:,}  Net: ${g["total_won"] - g["total_lost"]:,}')
print(f'Biggest win: ${g["biggest_win"]:,}  Biggest loss: ${g["biggest_loss"]:,}')
print(f'Best streak: {g["best_win_streak"]}  Worst streak: {g["worst_loss_streak"]}')
print(f'Peak: Day {pk[0]} @ ${pk[1]:,}')
print(f'Bet modes: {json.dumps(modes)}')
print()

# Trajectory
print('TRAJECTORY:')
prev = 0
for day in sorted(by_day.keys()):
    b = by_day[day]
    marker = ''
    if prev > 1000 and b < prev * 0.5:
        marker = f' ** DROP from ${prev:,}'
    if b >= 5000 or (b >= 1000 and day % 10 == 0) or day % 20 == 0 or day <= 3 or marker:
        print(f'  Day {day:>3}: ${b:>8,}{marker}')
    prev = b

# Items timeline
print()
print('ITEMS ACQUIRED:')
for name, prov in sorted(ip.items(), key=lambda x: (x[1].get('acquired', [{}])[0].get('day', 999) if x[1].get('acquired') else 999)):
    acq = prov.get('acquired', [])
    if acq:
        print(f'  Day {acq[0].get("day", "?"):>3}: {name} from {acq[0].get("source", "?")}')
