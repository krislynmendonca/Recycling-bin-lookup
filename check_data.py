"""Validate data/*.csv against the rules documented in data/README.md.

Run from the project root:

    python check_data.py

Exits with status 1 when any rule is violated, so it can be used as a pre-commit
or CI gate before the CSVs are committed.
"""

import csv
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_CSV = os.path.join(BASE_DIR, "data", "recycling_rules.csv")
HAZARDS_CSV = os.path.join(BASE_DIR, "data", "hazardous_items.csv")

ALLOWED_BINS = ("recycling", "compost", "trash")
CITATION_PATTERN = re.compile(r"^HKU Recycling Guide p\.\d+$")

problems = []


def fail(message):
    problems.append(message)


def read_csv(path, expected_columns):
    if not os.path.exists(path):
        fail(f"{os.path.basename(path)}: file not found")
        return []
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        missing = [column for column in expected_columns if column not in (reader.fieldnames or [])]
        if missing:
            fail(f"{os.path.basename(path)}: missing column(s) {missing}")
            return []
        return list(reader)


def check_rules():
    rows = read_csv(RULES_CSV, ["item", "synonyms", "bin", "citation", "condition"])
    seen_keys = {}

    for line_number, row in enumerate(rows, start=2):
        item = row["item"]
        where = f"recycling_rules.csv line {line_number} ({item!r})"

        if not item:
            fail(f"{where}: empty item name")
            continue
        if item != item.strip().lower():
            fail(f"{where}: item must be lowercase and trimmed")

        if row["bin"] not in ALLOWED_BINS:
            fail(f"{where}: bin {row['bin']!r} not in {ALLOWED_BINS}")

        if not CITATION_PATTERN.match(row["citation"]):
            fail(f"{where}: citation {row['citation']!r} must match 'HKU Recycling Guide p.X'")

        raw_synonyms = row["synonyms"] or ""
        if raw_synonyms != raw_synonyms.replace(" |", "|").replace("| ", "|"):
            fail(f"{where}: synonyms must not have spaces around the '|' separator")

        condition = (row["condition"] or "").strip()
        if condition and "→" not in condition:
            fail(f"{where}: condition {condition!r} should document its branches with '→'")

        keys = [item] + [s.strip() for s in raw_synonyms.split("|") if s.strip()]
        for key in keys:
            if key in seen_keys:
                fail(f"{where}: key {key!r} already claimed by {seen_keys[key]!r}")
            else:
                seen_keys[key] = item

    return rows


def check_hazards(rule_rows):
    rows = read_csv(HAZARDS_CSV, ["item", "contact"])
    rule_items = {row["item"] for row in rule_rows}

    for line_number, row in enumerate(rows, start=2):
        item = row["item"]
        where = f"hazardous_items.csv line {line_number} ({item!r})"

        if not item:
            fail(f"{where}: empty item name")
            continue
        if item in rule_items:
            fail(f"{where}: item also appears in recycling_rules.csv, which is ambiguous")
        if not (row["contact"] or "").strip():
            fail(f"{where}: contact channel must not be empty")
        elif "HKU" not in row["contact"]:
            fail(f"{where}: contact should name the HKU department")

    return rows


def main():
    rule_rows = check_rules()
    hazard_rows = check_hazards(rule_rows)

    print(f"recycling_rules.csv : {len(rule_rows)} items")
    print(f"hazardous_items.csv : {len(hazard_rows)} items")

    if problems:
        print(f"\nFAILED - {len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print("\nOK - all data checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
