import re
from pathlib import Path

# Path to the story output file
def analyze_doctor_visits(story_path):
    with open(story_path, encoding='utf-8') as f:
        lines = f.readlines()

    visits = []
    i = 0
    last_stats = {}
    while i < len(lines):
        line = lines[i]
        # Track current stats
        if 'Your current sanity:' in line:
            try:
                last_stats['sanity'] = int(re.search(r'(\d+)%', line).group(1))
            except Exception:
                last_stats['sanity'] = None
        if any(symptom in line for symptom in ['cough', 'mucus', 'bronchitis', 'broken ankle', 'pain', 'ill', 'poison', 'infection', 'vomit', 'fever', 'chest aches', 'raw', 'injur', 'panic attack', 'anxiety', 'insomnia']):
            last_stats['symptom'] = line.strip()
        # Detect Doctor's Office visit
        if 'drive to the Doctor' in line or 'drive to the Doctor\'s Office' in line:
            visit = {'line': i, 'stats': last_stats.copy(), 'context': []}
            # Look ahead for cost and doctor comment
            for j in range(i, min(i+20, len(lines))):
                if 'That will be $' in lines[j]:
                    visit['cost'] = int(re.search(r'\$(\d+)', lines[j]).group(1))
                if 'The Doctor will see you now.' in lines[j]:
                    visit['doctor_comment'] = lines[j+1:j+5]
            # Look back for recent symptoms
            for k in range(max(0, i-20), i):
                if any(symptom in lines[k] for symptom in ['cough', 'mucus', 'bronchitis', 'broken ankle', 'pain', 'ill', 'poison', 'infection', 'vomit', 'fever', 'chest aches', 'raw', 'injur', 'panic attack', 'anxiety', 'insomnia']):
                    visit['context'].append(lines[k].strip())
            visits.append(visit)
        i += 1

    # Analyze visits
    summary = []
    for idx, v in enumerate(visits):
        justified = False
        context = ' '.join(v.get('context', []))
        doctor_comment = ' '.join(v.get('doctor_comment', [])) if v.get('doctor_comment') else ''
        # Heuristic: justified if clear physical illness/injury
        if any(word in context.lower() for word in ['bronchitis', 'broken ankle', 'poison', 'infection', 'vomit', 'fever', 'pain', 'ill', 'injur', 'cough', 'mucus', 'chest aches', 'raw']):
            justified = True
        # Not justified if only stress, anxiety, insomnia, or no symptoms
        if any(word in context.lower() for word in ['panic attack', 'anxiety', 'insomnia']) and not justified:
            justified = False
        summary.append({
            'visit_num': idx+1,
            'cost': v.get('cost'),
            'justified': justified,
            'context': context,
            'doctor_comment': doctor_comment
        })
    # Print summary
    print('Doctor\'s Office Visit Analysis:')
    total_waste = 0
    for s in summary:
        print(f"Visit {s['visit_num']}: Cost ${s['cost']} - {'JUSTIFIED' if s['justified'] else 'WASTEFUL'}")
        print(f"  Context: {s['context']}")
        print(f"  Doctor: {s['doctor_comment']}")
        if not s['justified']:
            total_waste += s['cost'] or 0
    print(f"\nTotal potentially wasted on unjustified visits: ${total_waste}")

if __name__ == '__main__':
    analyze_doctor_visits('tools/story_out.txt')
