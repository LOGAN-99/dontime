#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "quiz.html").read_text(encoding="utf-8")


def extract_array(name):
    marker = f"const {name}="
    pos = SOURCE.find(marker)
    if pos < 0:
        raise SystemExit(f"Missing array declaration: {name}")
    start = SOURCE.find("[", pos + len(marker))
    if start < 0:
        raise SystemExit(f"Missing array opener: {name}")
    depth = 0
    quote = None
    escaped = False
    end = -1
    for i in range(start, len(SOURCE)):
        ch = SOURCE[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in ('"', "'", "`"):
            quote = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end < 0:
        raise SystemExit(f"Unclosed array: {name}")
    raw = SOURCE[start:end]
    raw = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:) ', r'\1"\2"\3', raw) if False else raw
    raw = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)(\s*:)\s*', r'\1"\2"\3', raw)
    raw = re.sub(r',\s*([}\]])', r'\1', raw)
    try:
        return json.loads(raw)
    except Exception as exc:
        raise SystemExit(f"Unable to parse {name}: {exc}")


banks = {
    "general": (extract_array("generalQuestions"), "q", 154),
    "hanja": (extract_array("hanjaWords"), "h", 130),
    "hanmun": (extract_array("quotes"), "q", 204),
    "english": (extract_array("vocab"), "w", 159),
    "idiom": (extract_array("idioms"), "h", 176),
}
for name, (items, key, expected) in banks.items():
    actual = len({item.get(key) for item in items if item.get(key)})
    if actual != expected:
        raise SystemExit(f"{name} unique bank count mismatch: expected {expected}, got {actual}")

count_markers = ("154개 문제", "130개 문제", "204개 문제", "159개 문제", "176개 문제")
for marker in count_markers:
    if marker not in SOURCE:
        raise SystemExit(f"Missing active quiz count marker: {marker}")
if "Active unique banks audited 2026-11-20: general 154, hanja 130, hanmun 204, English 159, idioms 176." not in SOURCE:
    raise SystemExit("Missing current quiz-bank audit comment")
if "const quoteBank=quotes.filter" not in SOURCE:
    raise SystemExit("Hanmun deduplication bank is missing")

required_files = [
    "mystery.html", "deduction.html", "maze.html", "quiz.html", "sitemap.xml",
    "isdal-woman.html", "deduction-isdal.html", "maze6.html",
    "flannan-isles.html", "alcatraz-escape.html", "yuba-county-five.html",
    "deduction-yuba.html", "maze15.html", "maze16.html",
    "lars-mittank.html", "deduction-lars.html", "maze17.html",
    "assets/lars-mittank-cinematic.svg", "content/daily-2026-11-20.json",
]
for path in required_files:
    if not (ROOT / path).is_file():
        raise SystemExit(f"Missing or empty required file: {path}")
    if not (ROOT / path).stat().st_size:
        raise SystemExit(f"Empty required file: {path}")

case_page = (ROOT / "lars-mittank.html").read_text(encoding="utf-8")
case_quiz = (ROOT / "deduction-lars.html").read_text(encoding="utf-8")
maze_page = (ROOT / "maze17.html").read_text(encoding="utf-8")
mystery_index = (ROOT / "mystery.html").read_text(encoding="utf-8")
deduction_index = (ROOT / "deduction.html").read_text(encoding="utf-8")
maze_index = (ROOT / "maze.html").read_text(encoding="utf-8")
sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
for marker, text, label in [
    ("CASE 013", case_page, "CASE 013 documentary"),
    ("CASE 013", case_quiz, "CASE 013 quiz"),
    ("PART 17", maze_page, "PART 17 maze"),
]:
    if marker not in text:
        raise SystemExit(f"Missing marker in {label}: {marker}")
if len(re.findall(r'\{q:"', case_quiz)) != 8:
    raise SystemExit("CASE 013 deduction quiz must contain 8 questions")
if len(re.findall(r'"title":', maze_page)) != 14:
    raise SystemExit("PART 17 maze must contain 14 chapters")
if "CASE 013" not in mystery_index or "lars-mittank.html" not in mystery_index:
    raise SystemExit("CASE 013 is missing from mystery index")
if "deduction-lars.html" not in deduction_index:
    raise SystemExit("CASE 013 quiz is missing from deduction index")
if "maze17.html" not in maze_index or "lars-mittank.html" not in maze_index:
    raise SystemExit("PART 17 or CASE 013 is missing from maze index")
for url in ("lars-mittank.html", "deduction-lars.html", "maze17.html", "assets/lars-mittank-cinematic.svg"):
    if url not in sitemap:
        raise SystemExit(f"Missing sitemap URL: {url}")

daily = json.loads((ROOT / "content" / "daily-2026-11-20.json").read_text(encoding="utf-8"))
if (len(daily.get("general", [])), len(daily.get("hanja", [])), len(daily.get("hanmun", [])), len(daily.get("english", []))) != (50, 10, 12, 12):
    raise SystemExit("Daily content archive counts do not match expected additions")

print("Validated quiz banks: general=154, hanja=130, hanmun=204, english=159, idiom=176")
print("Validated CASE 013 documentary, 8-question quiz, PART 17, indexes, sitemap, and daily archive")
