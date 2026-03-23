import re
from pathlib import Path

def extract_decisions(story_path, output_path):
    with open(story_path, encoding='utf-8') as f:
        lines = f.readlines()

    decisions = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Look for decision menus
        if re.match(r'Would you like to spend your day driving somewhere\?', line) or re.match(r'What would you like to do\?', line) or re.match(r'1\.', line.strip()):
            # Capture menu and player choice
            menu = []
            j = i
            while j < len(lines) and (lines[j].strip() == '' or re.match(r'\d+\.', lines[j].strip()) or 'Would you like' in lines[j] or 'What would you like' in lines[j]):
                menu.append(lines[j].strip())
                j += 1
            # Look for the next non-empty, non-menu line as the player's action
            while j < len(lines) and lines[j].strip() == '':
                j += 1
            action = lines[j].strip() if j < len(lines) else ''
            # Capture some context before the menu
            context = []
            for k in range(max(0, i-10), i):
                if lines[k].strip():
                    context.append(lines[k].strip())
            decisions.append({
                'line': i+1,
                'menu': menu,
                'action': action,
                'context': context[-5:] # last 5 lines of context
            })
            i = j
        i += 1
    # Write to output file
    import json
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(decisions, out, indent=2, ensure_ascii=False)
    print(f"Extracted {len(decisions)} decision points to {output_path}")

if __name__ == '__main__':
    extract_decisions('tools/story_out.txt', 'tools/decision_points.json')
