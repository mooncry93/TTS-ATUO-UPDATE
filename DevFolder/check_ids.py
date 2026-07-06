import re

with open("static/index.html", "r") as f:
    html = f.read()
    
# Extract all IDs from HTML
html_ids = set(re.findall(r"id=[\"']([^\"']+)[\"']", html))

with open("static/app.js", "r") as f:
    js = f.read()

# Extract all getElementById from JS
js_lines = js.split("\n")
missing = []
for i, line in enumerate(js_lines):
    match = re.search(r"getElementById\([\"']([^\"']+)[\"']\)", line)
    if match:
        js_id = match.group(1)
        if js_id not in html_ids:
            missing.append((i+1, js_id))

if missing:
    print("MISSING IDs causing JS crash:")
    for line_no, js_id in missing:
        print(f"Line {line_no}: {js_id}")
else:
    print("No missing getElementById calls!")
