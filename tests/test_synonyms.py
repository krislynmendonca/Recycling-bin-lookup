"""Every synonym variant must resolve to the same bin as its canonical item.

The expected values are read straight from data/recycling_rules.csv, so this test
also proves the loader registers each pipe-separated synonym as its own key.
"""

import csv
import os

import pytest

from lookup import lookup_bin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_CSV = os.path.join(BASE_DIR, "data", "recycling_rules.csv")


def load_rule_rows():
    with open(RULES_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def synonym_cases():
    cases = []
    for row in load_rule_rows():
        for synonym in (row["synonyms"] or "").split("|"):
            synonym = synonym.strip()
            if synonym:
                cases.append((synonym, row["item"], row["bin"], row["citation"]))
    return cases


@pytest.mark.parametrize(
    "synonym,canonical_item,expected_bin,expected_citation",
    synonym_cases(),
    ids=[f"{syn}->{item}" for syn, item, _, _ in synonym_cases()],
)
def test_synonym_resolves_like_canonical_item(synonym, canonical_item, expected_bin, expected_citation):
    by_synonym = lookup_bin(synonym)
    by_item = lookup_bin(canonical_item)

    assert by_synonym["bin"] == expected_bin
    assert by_synonym["citation"] == expected_citation
    assert by_synonym["bin"] == by_item["bin"]
    assert by_synonym["citation"] == by_item["citation"]
    assert by_synonym["condition"] == by_item["condition"]


def test_synonym_set_is_not_empty():
    assert len(synonym_cases()) > 0


def test_can_synonyms_are_interchangeable():
    """Explicit README example: "pop can" == "soda can" == "aluminum can"."""
    pop_can = lookup_bin("pop can")
    soda_can = lookup_bin("soda can")
    aluminum_can = lookup_bin("aluminum can")

    assert pop_can["bin"] == soda_can["bin"] == aluminum_can["bin"] == "recycling"
    assert pop_can["citation"] == soda_can["citation"] == aluminum_can["citation"]


def test_synonym_lookup_survives_normalization():
    """Case and punctuation differences must not break synonym matching."""
    assert lookup_bin("POP CAN!")["bin"] == lookup_bin("pop can")["bin"]
    assert lookup_bin("  Soda   Can  ")["bin"] == lookup_bin("soda can")["bin"]
