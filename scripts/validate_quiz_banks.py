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
    "general": ("const generalQuestions=", "const generalBank=", "q", 640),
    "hanja": ("const hanjaWords=", "const hanjaBank=", "h", 190),
    "hanmun": ("const quotes=", "const quoteSeen", "q", 262),
    "english": ("const vocab=", "const vocabBank=", "w", 308),
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
    "alcatraz-escape.html",
    "deduction-alcatraz.html",
    "maze15.html",
    "assets/alcatraz-escape.svg",
    "yuba-county-five.html",
    "deduction-yuba.html",
    "maze16.html",
    "assets/yuba-county-five-cinematic.svg",
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

case11 = (ROOT / "alcatraz-escape.html").read_text(encoding="utf-8")
deduction11 = (ROOT / "deduction-alcatraz.html").read_text(encoding="utf-8")
maze15 = (ROOT / "maze15.html").read_text(encoding="utf-8")
if "CASE 011" not in case11 or "Federal Bureau of Investigation" not in case11:
    raise SystemExit("CASE 011 documentary content check failed")
if len(re.findall(r'"q":', deduction11)) != 8:
    raise SystemExit("CASE 011 deduction quiz must contain exactly 8 questions")
if len(re.findall(r'"title":', maze15)) != 14:
    raise SystemExit("PART 15 maze must contain exactly 14 chapters")


case12 = (ROOT / "yuba-county-five.html").read_text(encoding="utf-8")
deduction12 = (ROOT / "deduction-yuba.html").read_text(encoding="utf-8")
maze16 = (ROOT / "maze16.html").read_text(encoding="utf-8")
if "CASE 012" not in case12 or "Yuba County Sheriff's Office" not in case12:
    raise SystemExit("CASE 012 documentary content check failed")
if len(re.findall(r'"q":', deduction12)) != 8:
    raise SystemExit("CASE 012 deduction quiz must contain exactly 8 questions")
if len(re.findall(r'"title":', maze16)) != 14:
    raise SystemExit("PART 16 maze must contain exactly 14 chapters")

print("CASE 009, CASE 011 and CASE 012 pages, 8-question deduction quizzes, 14-chapter mazes and image assets passed.")
