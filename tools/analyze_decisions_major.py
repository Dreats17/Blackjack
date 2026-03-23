import json
import re
from pathlib import Path

def is_major_decision(request_type, context_tag, menu_options, raw_prompt, recent_text):
    # Heuristics for major world decisions (not blackjack, not routine gambling)
    if request_type in ["shop_menu", "route_choice", "doctor_visit", "location_choice", "event_choice", "companion_menu"]:
        return True
    # Heuristic: menu with locations, shops, or world events
    menu_str = ' '.join(menu_options).lower() if menu_options else ''
    if any(word in menu_str for word in ["doctor", "witch", "shop", "store", "pawn", "marvin", "route", "stay home", "convenience", "loan", "companion", "adventure", "location", "drive"]):
        return True
    # Heuristic: prompt or context mentions major world actions
    prompt_str = (raw_prompt or '').lower() + ' ' + ' '.join(recent_text or []).lower()
    if any(word in prompt_str for word in ["would you like to spend your day", "where do you want to go", "which shop", "which location", "doctor", "witch", "shop", "store", "pawn", "marvin", "route", "stay home", "loan", "companion", "adventure", "drive"]):
        return True
    return False

# Handler mapping for each major decision
def get_decision_handler(request_type, context_tag, menu_options, raw_prompt, recent_text):
    menu_str = ' '.join(menu_options).lower() if menu_options else ''
    prompt_str = (raw_prompt or '').lower() + ' ' + ' '.join(recent_text or []).lower()
    # Blackjack betting handler
    if request_type == "blackjack_bet" or context_tag == "blackjack_bet":
        return "blackjack_bet"
    # Direct request_type mapping
    if request_type == "doctor_visit" or "doctor" in menu_str or "doctor" in prompt_str:
        return "doctor"
    if "witch" in menu_str or "witch" in prompt_str:
        return "witch_doctor"
    if "marvin" in menu_str or "marvin" in prompt_str:
        return "marvin"
    if "pawn" in menu_str or "pawn" in prompt_str:
        return "pawn_shop"
    if "loan" in menu_str or "loan" in prompt_str:
        return "loan_shark"
    if any(m in menu_str for m in ["tom", "frank", "oswald", "mechanic"]):
        return "mechanic"
    if "convenience" in menu_str or "convenience" in prompt_str:
        return "convenience_store"
    if "airport" in menu_str or "airport" in prompt_str:
        return "airport"
    if "adventure" in menu_str or "adventure" in prompt_str:
        return "adventure"
    if "route" in menu_str or "route" in prompt_str:
        return "route_choice"
    if "stay home" in menu_str or "stay home" in prompt_str:
        return "stay_home"
    if "companion" in menu_str or "companion" in prompt_str:
        return "companion"
    if "shop" in menu_str or "shop" in prompt_str or request_type == "shop_menu":
        return "shop"
    if request_type == "event_choice":
        return "event"
    if request_type == "location_choice":
        return "location"
    # Fallback
    return "other"


def extract_major_decisions(json_path, output_path):
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    major_decisions = []
    for req in data.get('decision_requests', []):
        rt = req.get('request_type', '')
        tag = req.get('game_state', {}).get('current_context_tag', '')
        menu = [o.get('label', '') for o in req.get('normalized_options', [])]
        prompt = req.get('raw_prompt_text', '')
        recent = req.get('raw_recent_text', [])
        if is_major_decision(rt, tag, menu, prompt, recent):
            handler = get_decision_handler(rt, tag, menu, prompt, recent)
            major_decisions.append({
                'day': req.get('game_state', {}).get('day'),
                'context_tag': tag,
                'request_type': rt,
                'menu_options': menu,
                'raw_prompt_text': prompt,
                'raw_recent_text': recent,
                'handler': handler,
                'game_state': req.get('game_state', {}),
                'metadata': req.get('metadata', {}),
            })
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(major_decisions, out, indent=2, ensure_ascii=False)
    print(f"Extracted {len(major_decisions)} major decision points to {output_path}")

if __name__ == '__main__':
    extract_major_decisions('tools/test_out.json', 'tools/decision_points_major.json')
