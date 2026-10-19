"""Every answer that mentions a rule must cite the page declared for that item."""

import csv
import os
import re

import pytest

from lookup import lookup_bin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_CSV = os.path.join(BASE_DIR, "data", "recycling_rules.csv")

CITATION_PATTERN = re.compile(r"^HKU Recycling Guide p\.\d+$")


def load_rule_rows():
    with open(RULES_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def canonical_items():
    return [(row["item"], row["citation"]) for row in load_rule_rows()]


@pytest.mark.parametrize("item,expected_citation", canonical_items(), ids=lambda value: value if isinstance(value, str) else None)
def test_canonical_item_citation_matches_expected_page(item, expected_citation):
    result = lookup_bin(item)
    assert result["citation"] == expected_citation
    assert expected_citation in result["message"]


def test_every_citation_in_the_dataset_has_a_page_number():
    for row in load_rule_rows():
        assert CITATION_PATTERN.match(row["citation"]), f"bad citation for {row['item']}: {row['citation']!r}"


def test_no_answer_returns_a_bin_without_a_citation():
    """A bin without evidence would be an invented rule."""
    for row in load_rule_rows():
        for value in (row["item"], *(row["synonyms"] or "").split("|")):
            value = value.strip()
            if not value:
                continue
            result = lookup_bin(value)
            if result["bin"] is not None:
                assert result["citation"] is not None
                assert CITATION_PATTERN.match(result["citation"])


def test_citation_is_null_for_every_refusal_and_miss():
    for raw_input in ("battery", "unknown thing", "coca cola can", ""):
        result = lookup_bin(raw_input)
        if result["status"] in ("refused", "not_found", "empty"):
            assert result["citation"] is None
