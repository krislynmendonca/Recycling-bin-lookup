import csv
import os
from normalize import normalize_text
from refusal import is_hazardous

# Base directory points to project root (lookup.py resides in project root folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_CSV_PATH = os.path.join(BASE_DIR, "data", "recycling_rules.csv")

_rule_dict = None


def load_recycling_rules():
    """
    Load recycling rules dataset from CSV into global hash map dictionary.
    Keys: normalized item name and normalized synonyms processed by normalize_text().
    Values: Dictionary containing bin type, citation source and condition prompt.
    """
    global _rule_dict
    _rule_dict = {}
    with open(RULES_CSV_PATH, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_name = normalize_text(row["item"])
            bin_type = row["bin"]
            citation = row["citation"]
            condition = row["condition"]

            # Register main item entry
            _rule_dict[item_name] = {
                "bin": bin_type,
                "citation": citation,
                "condition": condition
            }

            # Split synonyms using | separator and register each synonym entry
            synonyms_raw = row["synonyms"]
            if synonyms_raw:
                for syn in synonyms_raw.split("|"):
                    syn_clean = normalize_text(syn)
                    if syn_clean:
                        _rule_dict[syn_clean] = {
                            "bin": bin_type,
                            "citation": citation,
                            "condition": condition
                        }


def lookup_item(normalized_str: str) -> dict | None:
    """
    Search normalized input string inside recycling rule dictionary.
    Args:
        normalized_str: Normalized string processed via normalize_text()
    Returns:
        Dictionary with bin, citation and condition fields; None for no match
    """
    global _rule_dict
    if _rule_dict is None:
        load_recycling_rules()
    return _rule_dict.get(normalized_str, None)


def get_all_candidates() -> list[str]:
    """
    Return all normalized keys from recycling rule dict for LLM closed-set candidate list.
    """
    global _rule_dict
    if _rule_dict is None:
        load_recycling_rules()
    return list(_rule_dict.keys())


def lookup_bin(raw_input: str) -> dict:
    """
    Unified single entry point specified in SKILL.md.
    Pipeline: normalize -> hazardous hard-refusal -> exact/synonym lookup -> result shaping.
    Args:
        raw_input: Raw user input string
    Returns:
        Dictionary with exactly five keys: status, bin, citation, condition, message
        status is one of: found, condition, refused, not_found, empty
    """
    key = normalize_text(raw_input)
    if not key:
        return {
            "status": "empty",
            "bin": None,
            "citation": None,
            "condition": None,
            "message": "Please enter an item name.",
        }

    # Hazardous items are checked first and always refused (never binned)
    is_haz, contact = is_hazardous(key)
    if is_haz:
        return {
            "status": "refused",
            "bin": None,
            "citation": None,
            "condition": None,
            "message": f"⚠️ This item is hazardous. Contact: {contact}. When in doubt, ask building staff.",
        }

    result = lookup_item(key)
    if result is None:
        # No fuzzy matching: anything not in the database is redirected, never guessed
        return {
            "status": "not_found",
            "bin": None,
            "citation": None,
            "condition": None,
            "message": "❓ This item is not in the published HKU recycling rules. Please contact HKU Estates Office. When in doubt, ask building staff.",
        }

    condition = result.get("condition") or None
    if condition:
        return {
            "status": "condition",
            "bin": result["bin"],
            "citation": result["citation"],
            "condition": condition,
            "message": f"⚠️ This item depends on condition: {condition}. Citation: {result['citation']}. When in doubt, ask building staff.",
        }

    return {
        "status": "found",
        "bin": result["bin"],
        "citation": result["citation"],
        "condition": None,
        "message": f"Place in the {result['bin'].upper()} bin. Rule: {result['citation']}. When in doubt, ask building staff.",
    }


if __name__ == "__main__":
    load_recycling_rules()
    test_input = "aluminum can"
    res = lookup_item(test_input)
    print(f"Lookup '{test_input}' result: {res}")
    test_input2 = "plastic bottle"
    res2 = lookup_item(test_input2)
    print(f"Lookup '{test_input2}' result: {res2}")

    # Test candidate export
    candidates = get_all_candidates()
    print(f"Total candidate entries: {len(candidates)}")

    print(f"lookup_bin('pizza box') = {lookup_bin('pizza box')}")
    print(f"lookup_bin('battery') = {lookup_bin('battery')}")
    print(f"lookup_bin('unknown thing') = {lookup_bin('unknown thing')}")
