#!/usr/bin/env python3
"""
Crusader Queens — Localization Gender-Swap Script
==================================================
Scans CK3 vanilla localization .yml files and produces patched versions
with gendered language swapped (he↔she, king↔queen, etc.).

Usage:
    python3 tools/swap_localization.py \
        --vanilla "C:/Program Files (x86)/Steam/steamapps/common/Crusader Kings III/game/localization/english" \
        --output  "./localization/english/vanilla_patched"

The script uses a two-pass placeholder strategy so that swapping
"king" → "queen" doesn't then get caught by a "queen" → "king" pass.
"""

import argparse
import os
import re
import shutil
from pathlib import Path

# ── Swap table ────────────────────────────────────────────────────────────────
# Format: (pattern, replacement)
# Uses word-boundary regex (\b) to avoid partial matches.
# Order matters: longer/more-specific patterns come first.
# Placeholders (SWAP_PLACEHOLDER_N) are used between passes to avoid
# double-swapping (e.g. king→queen→king).

SWAP_PAIRS = [
    # Titles — uppercase
    ("Emperor",         "§EMPRESS§"),
    ("Empress",         "§EMPEROR§"),
    ("King",            "§QUEEN§"),
    ("Queen",           "§KING§"),
    ("Duke",            "§DUCHESS§"),
    ("Duchess",         "§DUKE§"),
    ("Count",           "§COUNTESS§"),
    ("Countess",        "§COUNT§"),
    ("Baron",           "§BARONESS§"),
    ("Baroness",        "§BARON§"),
    ("Prince",          "§PRINCESS§"),
    ("Princess",        "§PRINCE§"),
    ("Knight",          "§DAME§"),
    ("Dame",            "§KNIGHT§"),
    ("Lord",            "§LADY§"),
    ("Lady",            "§LORD§"),
    # Pronouns
    ("\\bHe\\b",        "§SHE§"),
    ("\\bShe\\b",       "§HE§"),
    ("\\bHim\\b",       "§HER_obj§"),
    ("\\bHer\\b",       "§HIM§"),
    ("\\bHis\\b",       "§HER_pos§"),
    ("\\bher\\b",       "§his§"),
    ("\\bhe\\b",        "§she§"),
    ("\\bshe\\b",       "§he§"),
    ("\\bhim\\b",       "§her_obj§"),
    ("\\bhis\\b",       "§her_pos§"),
    ("himself",         "§HERSELF§"),
    ("herself",         "§HIMSELF§"),
    # Family
    ("\\bFather\\b",    "§MOTHER§"),
    ("\\bMother\\b",    "§FATHER§"),
    ("\\bfather\\b",    "§mother§"),
    ("\\bmother\\b",    "§father§"),
    ("\\bSon\\b",       "§DAUGHTER§"),
    ("\\bDaughter\\b",  "§SON§"),
    ("\\bson\\b",       "§daughter§"),
    ("\\bdaughter\\b",  "§son§"),
    ("\\bBrother\\b",   "§SISTER§"),
    ("\\bSister\\b",    "§BROTHER§"),
    ("\\bbrother\\b",   "§sister§"),
    ("\\bsister\\b",    "§brother§"),
    ("Grandfather",     "§GRANDMOTHER§"),
    ("Grandmother",     "§GRANDFATHER§"),
    ("grandfather",     "§grandmother§"),
    ("grandmother",     "§grandfather§"),
    ("Grandson",        "§GRANDDAUGHTER§"),
    ("Granddaughter",   "§GRANDSON§"),
    ("grandson",        "§granddaughter§"),
    ("granddaughter",   "§grandson§"),
    ("\\bUncle\\b",     "§AUNT§"),
    ("\\bAunt\\b",      "§UNCLE§"),
    ("\\buncle\\b",     "§aunt§"),
    ("\\baunt\\b",      "§uncle§"),
    ("\\bNephew\\b",    "§NIECE§"),
    ("\\bNiece\\b",     "§NEPHEW§"),
    ("\\bnephew\\b",    "§niece§"),
    ("\\bniece\\b",     "§nephew§"),
    # Marriage
    ("\\bHusband\\b",   "§WIFE§"),
    ("\\bWife\\b",      "§HUSBAND§"),
    ("\\bhusband\\b",   "§wife§"),
    ("\\bwife\\b",      "§husband§"),
    # Men / Women
    ("\\bman\\b",       "§woman§"),
    ("\\bwoman\\b",     "§man§"),
    ("\\bMan\\b",       "§Woman§"),
    ("\\bWoman\\b",     "§Man§"),
    ("\\bmen\\b",       "§women§"),
    ("\\bwomen\\b",     "§men§"),
    ("\\bMen\\b",       "§Women§"),
    ("\\bWomen\\b",     "§Men§"),
]

# Resolve placeholders back to their final values
PLACEHOLDER_RESOLVE = {
    "§EMPRESS§":        "Empress",
    "§EMPEROR§":        "Emperor",
    "§QUEEN§":          "Queen",
    "§KING§":           "King",
    "§DUCHESS§":        "Duchess",
    "§DUKE§":           "Duke",
    "§COUNTESS§":       "Countess",
    "§COUNT§":          "Count",
    "§BARONESS§":       "Baroness",
    "§BARON§":          "Baron",
    "§PRINCESS§":       "Princess",
    "§PRINCE§":         "Prince",
    "§DAME§":           "Dame",
    "§KNIGHT§":         "Knight",
    "§LADY§":           "Lady",
    "§LORD§":           "Lord",
    "§SHE§":            "She",
    "§HE§":             "He",
    "§HER_obj§":        "Her",
    "§HIM§":            "Him",
    "§HER_pos§":        "Her",
    "§his§":            "his",     # NOTE: her (possessive) → his
    "§she§":            "she",
    "§he§":             "he",
    "§her_obj§":        "her",
    "§her_pos§":        "her",
    "§HERSELF§":        "herself",
    "§HIMSELF§":        "himself",
    "§MOTHER§":         "Mother",
    "§FATHER§":         "Father",
    "§mother§":         "mother",
    "§father§":         "father",
    "§DAUGHTER§":       "Daughter",
    "§SON§":            "Son",
    "§daughter§":       "daughter",
    "§son§":            "son",
    "§SISTER§":         "Sister",
    "§BROTHER§":        "Brother",
    "§sister§":         "sister",
    "§brother§":        "brother",
    "§GRANDMOTHER§":    "Grandmother",
    "§GRANDFATHER§":    "Grandfather",
    "§grandmother§":    "grandmother",
    "§grandfather§":    "grandfather",
    "§GRANDDAUGHTER§":  "Granddaughter",
    "§GRANDSON§":       "Grandson",
    "§granddaughter§":  "granddaughter",
    "§grandson§":       "grandson",
    "§AUNT§":           "Aunt",
    "§UNCLE§":          "Uncle",
    "§aunt§":           "aunt",
    "§uncle§":          "uncle",
    "§NIECE§":          "Niece",
    "§NEPHEW§":         "Nephew",
    "§niece§":          "niece",
    "§nephew§":         "nephew",
    "§WIFE§":           "Wife",
    "§HUSBAND§":        "Husband",
    "§wife§":           "wife",
    "§husband§":        "husband",
    "§woman§":          "woman",
    "§man§":            "man",
    "§Woman§":          "Woman",
    "§Man§":            "Man",
    "§women§":          "women",
    "§men§":            "men",
    "§Women§":          "Women",
    "§Men§":            "Men",
}


def swap_line(line: str) -> str:
    """Apply all swap pairs to a single line using placeholder strategy."""
    # Skip comment lines and empty lines
    stripped = line.strip()
    if stripped.startswith("#") or not stripped:
        return line

    # Pass 1: replace originals with placeholders
    for pattern, placeholder in SWAP_PAIRS:
        line = re.sub(pattern, placeholder, line)

    # Pass 2: resolve placeholders to final values
    for placeholder, final in PLACEHOLDER_RESOLVE.items():
        line = line.replace(placeholder, final)

    return line


def process_file(src: Path, dst: Path) -> int:
    """Process a single .yml file. Returns number of changed lines."""
    # CK3 localization files use UTF-8-BOM encoding
    try:
        text = src.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = src.read_text(encoding="latin-1")

    lines = text.splitlines(keepends=True)
    changed = 0
    new_lines = []

    for line in lines:
        new_line = swap_line(line)
        if new_line != line:
            changed += 1
        new_lines.append(new_line)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("".join(new_lines), encoding="utf-8-sig")
    return changed


def main():
    parser = argparse.ArgumentParser(
        description="Swap gendered language in CK3 localization files."
    )
    parser.add_argument(
        "--vanilla",
        required=True,
        help="Path to CK3 vanilla localization/english folder",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output folder for patched localization files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats without writing files",
    )
    args = parser.parse_args()

    src_root = Path(args.vanilla)
    dst_root = Path(args.output)

    if not src_root.exists():
        print(f"ERROR: Vanilla path not found: {src_root}")
        return 1

    yml_files = list(src_root.rglob("*_l_english.yml"))
    print(f"Found {len(yml_files)} localization file(s) in {src_root}\n")

    total_changed = 0
    for src in sorted(yml_files):
        rel = src.relative_to(src_root)
        dst = dst_root / rel

        if args.dry_run:
            # Just count changes
            try:
                text = src.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                text = src.read_text(encoding="latin-1")
            changed = sum(
                1 for line in text.splitlines() if swap_line(line) != line
            )
            print(f"  [dry-run] {rel}: {changed} line(s) would change")
        else:
            changed = process_file(src, dst)
            status = f"{changed} line(s) changed" if changed else "no changes"
            print(f"  {rel}: {status}")

        total_changed += changed

    print(f"\nDone. Total lines modified: {total_changed}")
    if not args.dry_run:
        print(f"Output written to: {dst_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
