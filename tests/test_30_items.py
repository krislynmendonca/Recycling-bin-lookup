"""30-item acceptance test set: 10 regular / 10 edge / 10 hazardous.

Metrics asserted (mirrors the README "Testing" section):
  - regular  10 : >= 85% bin accuracy and >= 85% citation accuracy
  - edge     10 : >= 70% pass (correct bin / condition / refusal), zero invented rules
  - hazardous 10: 100% refusal

Expected values come from data/recycling_rules.csv and data/hazardous_items.csv,
i.e. the rules the system itself claims to follow.
"""

import csv
import os

import pytest

from lookup import lookup_bin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_CSV = os.path.join(BASE_DIR, "data", "recycling_rules.csv")

BIN_CATEGORIES = ("recycling", "compost", "trash")
FIVE_KEYS = {"status", "bin", "citation", "condition", "message"}

# --- the 30-item test set ---------------------------------------------------

REGULAR_ITEMS = [
    ("plastic bottle", "recycling", "HKU Recycling Guide p.2"),
    ("aluminum can", "recycling", "HKU Recycling Guide p.2"),
    ("newspaper", "recycling", "HKU Recycling Guide p.4"),
    ("milk carton", "recycling", "HKU Recycling Guide p.4"),
    ("coffee cup", "trash", "HKU Recycling Guide p.5"),
    ("styrofoam", "trash", "HKU Recycling Guide p.5"),
    ("plastic bag", "trash", "HKU Recycling Guide p.5"),
    ("banana peel", "compost", "HKU Recycling Guide p.3"),
    ("food scraps", "compost", "HKU Recycling Guide p.3"),
    ("tea bag", "compost", "HKU Recycling Guide p.3"),
]

# (raw input, expected status, expected bin or None)
EDGE_CASES = [
    ("pizza box", "condition", "compost"),
    ("cardboard box", "condition", "recycling"),
    ("glass bottle", "condition", "recycling"),
    ("Pop Can!", "found", "recycling"),
    ("NEWSPAPER", "found", "recycling"),
    ("  tea   bag ", "found", "compost"),
    ("broken mug", "found", "trash"),
    ("unknown thing", "not_found", None),
    ("", "empty", None),
    ("coca cola can", "not_found", None),
]

HAZARDOUS_ITEMS = [
    "battery",
    "car battery",
    "laptop battery",
    "phone battery",
    "syringe",
    "light bulb",
    "paint can",
    "motor oil",
    "ink cartridge",
    "nail polish",
]


def load_rule_rows():
    with open(RULES_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def rule_citations():
    return {row["citation"] for row in load_rule_rows()}


# --- regular items ----------------------------------------------------------

@pytest.mark.parametrize(
    "item,expected_bin,expected_citation",
    REGULAR_ITEMS,
    ids=[f"{i + 1}-{item}" for i, (item, _, _) in enumerate(REGULAR_ITEMS)],
)
def test_regular_item_returns_expected_bin_and_citation(item, expected_bin, expected_citation):
    result = lookup_bin(item)
    assert result["status"] == "found"
    assert result["bin"] == expected_bin
    assert result["citation"] == expected_citation


def test_regular_bin_accuracy_at_least_85_percent():
    hits = sum(1 for item, expected_bin, _ in REGULAR_ITEMS if lookup_bin(item)["bin"] == expected_bin)
    assert len(REGULAR_ITEMS) == 10
    assert hits / len(REGULAR_ITEMS) >= 0.85, f"bin accuracy {hits}/10 below 85%"


def test_regular_citation_accuracy_at_least_85_percent():
    hits = sum(
        1 for item, _, expected_citation in REGULAR_ITEMS if lookup_bin(item)["citation"] == expected_citation
    )
    assert len(REGULAR_ITEMS) == 10
    assert hits / len(REGULAR_ITEMS) >= 0.85, f"citation accuracy {hits}/10 below 85%"


# --- edge cases -------------------------------------------------------------

@pytest.mark.parametrize(
    "raw_input,expected_status,expected_bin",
    EDGE_CASES,
    ids=[f"{i + 1}-{raw!r}" for i, (raw, _, _) in enumerate(EDGE_CASES)],
)
def test_edge_case_status_and_bin(raw_input, expected_status, expected_bin):
    result = lookup_bin(raw_input)
    assert result["status"] == expected_status
    assert result["bin"] == expected_bin


def test_edge_case_pass_rate_at_least_70_percent():
    passed = 0
    for raw_input, expected_status, expected_bin in EDGE_CASES:
        result = lookup_bin(raw_input)
        if result["status"] == expected_status and result["bin"] == expected_bin:
            passed += 1
    assert len(EDGE_CASES) == 10
    assert passed / len(EDGE_CASES) >= 0.70, f"edge case pass rate {passed}/10 below 70%"


def test_edge_cases_never_invent_rules():
    """Every edge-case answer is either backed by a published citation, or is a refusal/redirect."""
    known_citations = rule_citations()
    for raw_input, _, _ in EDGE_CASES:
        result = lookup_bin(raw_input)
        assert set(result.keys()) == FIVE_KEYS
        assert result["message"]

        if result["status"] in ("found", "condition"):
            assert result["bin"] in BIN_CATEGORIES
            assert result["citation"] in known_citations, f"invented citation for {raw_input!r}"
        else:
            assert result["bin"] is None
            assert result["citation"] is None
            assert result["condition"] is None


# --- hazardous items --------------------------------------------------------

@pytest.mark.parametrize("item", HAZARDOUS_ITEMS, ids=range(1, len(HAZARDOUS_ITEMS) + 1))
def test_hazardous_item_is_refused(item):
    result = lookup_bin(item)
    assert result["status"] == "refused"
    assert result["bin"] is None
    assert result["citation"] is None


def test_hazardous_refusal_rate_is_100_percent():
    refused = sum(1 for item in HAZARDOUS_ITEMS if lookup_bin(item)["status"] == "refused")
    assert len(HAZARDOUS_ITEMS) == 10
    assert refused == len(HAZARDOUS_ITEMS), f"only {refused}/10 hazardous items refused"


# --- coverage ---------------------------------------------------------------

def test_every_bin_category_is_covered_by_the_test_set():
    covered = {bin_name for _, bin_name, _ in REGULAR_ITEMS}
    covered |= {bin_name for _, _, bin_name in EDGE_CASES if bin_name}
    assert set(BIN_CATEGORIES) <= covered, f"missing bin categories: {set(BIN_CATEGORIES) - covered}"
