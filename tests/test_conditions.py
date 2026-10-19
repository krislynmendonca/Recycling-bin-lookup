"""Items with a condition must return a condition prompt instead of a plain bin answer."""

import csv
import os

import pytest

from lookup import lookup_bin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_CSV = os.path.join(BASE_DIR, "data", "recycling_rules.csv")


def load_rule_rows():
    with open(RULES_CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def conditional_rows():
    return [row for row in load_rule_rows() if (row["condition"] or "").strip()]


def unconditional_rows():
    return [row for row in load_rule_rows() if not (row["condition"] or "").strip()]


def test_the_dataset_actually_contains_conditional_items():
    assert conditional_rows(), "no conditional items found in recycling_rules.csv"


@pytest.mark.parametrize("row", conditional_rows(), ids=lambda row: row["item"])
def test_conditional_item_returns_condition_prompt(row):
    result = lookup_bin(row["item"])
    expected_condition = row["condition"].strip()

    assert result["status"] == "condition"
    assert result["bin"] == row["bin"]
    assert result["citation"] == row["citation"]
    assert result["condition"] == expected_condition
    assert expected_condition in result["message"]


@pytest.mark.parametrize("row", conditional_rows(), ids=lambda row: row["item"])
def test_condition_prompt_offers_both_branches(row):
    """A condition must spell out at least one real branch (uses the CSV arrow notation)."""
    assert "→" in row["condition"]
    assert len(row["condition"].split("→")) >= 2


@pytest.mark.parametrize("row", unconditional_rows(), ids=lambda row: row["item"])
def test_unconditional_item_does_not_claim_a_condition(row):
    result = lookup_bin(row["item"])
    assert result["status"] == "found"
    assert result["condition"] is None


def test_pizza_box_documents_clean_and_greasy_branches():
    """README example: pizza box -> if clean compost; if greasy trash."""
    result = lookup_bin("pizza box")
    assert result["status"] == "condition"
    assert result["bin"] == "compost"
    assert "compost" in result["condition"]
    assert "trash" in result["condition"]
