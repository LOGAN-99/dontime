from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "quiz.html").read_text(encoding="utf-8")


def bank_values(start_marker: str, end_marker: str, key: str) -> list[str]:
    start = source.find(start_marker)
    end = source.find(end_marker, start)
    if start < 0 or end < 0:
        raise SystemExit(f"Missing bank marker: {start_marker} / {end_marker}")
    block = source[start:end]
    pattern = re.compile(r'"?' + re.escape(key) + r'"?\s*:\s*"((?:\\\\.|[^"\\\\])*)"', re.S)
    values = []
    for match in pattern.finditer(block):
        values.append(json.loads('"' + match.group(1) + '"'))
    return values


expected = {
    "general": ("const generalQuestions=", "const generalBank=", "q", 540),
    "hanja": ("const hanjaWords=", "const hanjaBank=", "h", 170),
    "hanmun": ("const quotes=", "const quoteSeen", "q", 238),
    "english": ("const vocab=", "const vocabBank=", "w", 284),
    "idioms": ("const idioms=", "const idiomBank=", "h", 180),
}
for name, (start, end, key, target) in expected.items():
    values = bank_values(start, end, key)
    actual = len(set(values))
    if actual != target:
        raise SystemExit(f"{name} unique bank count mismatch: expected {target}, got {actual}")
    print(f"{name}: {actual} unique entries")

required_files = [
    "brianna-maitland.html",
    "deduction-maitland.html",
    "maze13.html",
    "assets/brianna-maitland-road.svg",
]
for item in required_files:
    path = ROOT / item
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f"Missing or empty new content asset: {item}")

case = (ROOT / "brianna-maitland.html").read_text(encoding="utf-8")
deduction = (ROOT / "deduction-maitland.html").read_text(encoding="utf-8")
maze = (ROOT / "maze13.html").read_text(encoding="utf-8")
if "CASE 009" not in case or "FBI" not in case:
    raise SystemExit("CASE 009 documentary content check failed")
if len(re.findall(r'"q":', deduction)) != 8:
    raise SystemExit("CASE 009 deduction quiz must contain exactly 8 questions")
if len(re.findall(r'"title":', maze)) != 14:
    raise SystemExit("PART 13 maze must contain exactly 14 chapters")

print("CASE 009 pages, 8-question deduction quiz, 14-chapter maze and image asset passed.")
