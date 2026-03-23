"""Convert raw input() choice patterns to ask.option() across event files."""
import re

# The actual line looks like:
#   choice = input("(around/wait): ").strip().lower()
# We need to match the parens INSIDE the string literal
pattern = r'(\w+) = input\("\(([^)]+)\): "\)\.strip\(\)\.lower\(\)'

def make_replacement(match):
    var = match.group(1)
    opts_str = match.group(2)  # e.g. 'around/wait'
    opts = opts_str.split("/")
    # Pretty prompt: 'Around / Wait: '
    prompt = " / ".join(o.capitalize() for o in opts) + ": "
    # Options list: ["around", "wait"]
    opts_list = ", ".join('"' + o + '"' for o in opts)
    return f'{var} = ask.option("{prompt}", [{opts_list}])'

# Test line
test = '            choice = input("(around/wait): ").strip().lower()'
m = re.search(pattern, test)
if m:
    print("TEST MATCH:", m.groups())
    print("RESULT:", make_replacement(m))
else:
    print("NO TEST MATCH")
    print("Pattern:", repr(pattern))
    print("Test:", repr(test))

files = [
    "story/events_night.py",
    "story/events_day_casino.py",
    "story/events_day_wealth.py",
]

for f in files:
    with open(f, "r", encoding="utf-8") as fh:
        content = fh.read()
    new_content, count = re.subn(pattern, make_replacement, content)
    if count > 0:
        with open(f, "w", encoding="utf-8") as fh:
            fh.write(new_content)
        print(f"{f}: {count} conversions")
    else:
        print(f"{f}: no matches")
