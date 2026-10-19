import csv
import os
from normalize import normalize_text

# Base directory points to project root (refusal.py resides in project root folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HAZARD_CSV_PATH = os.path.join(BASE_DIR, "data", "hazardous_items.csv")

_hazard_dict = None


def load_hazard_items():
    """
    Load hazardous item dataset from CSV file into global dictionary.
    Keys: normalized item names processed by normalize_text().
    Values: corresponding hazardous contact information.
    """
    global _hazard_dict
    _hazard_dict = {}
    with open(HAZARD_CSV_PATH, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_raw = row["item"]
            item_normalized = normalize_text(item_raw)
            _hazard_dict[item_normalized] = row["contact"]


def is_hazardous(normalized_str: str) -> tuple[bool, str]:
    """
    Check whether normalized input matches a hazardous item entry.
    Args:
        normalized_str: Normalized string processed via normalize_text()
    Returns:
        Tuple (is_hazard: bool, contact_info: str)
    """
    global _hazard_dict
    if _hazard_dict is None:
        load_hazard_items()

    if normalized_str in _hazard_dict:
        return True, _hazard_dict[normalized_str]
    return False, ""


def should_refuse(normalized_str: str, lookup_result: dict | None) -> tuple[bool, str]:
    """
    Hard-cutoff refusal logic:
    100% refusal for hazardous items; refuse all items not present in database.
    Rule: accept only exact match or synonym match, all other inputs are refused.
    Args:
        normalized_str: Normalized input string
        lookup_result: Result from lookup_item(); None if no matching record
    Returns:
        Tuple (refuse_flag: bool, message: str)
    """
    # Prioritize hazardous item check (hard cutoff exact match)
    is_haz, contact = is_hazardous(normalized_str)
    if is_haz:
        return True, f"Hazardous item! Please contact: {contact}"

    # Refuse items with no matching entry inside recycling database
    if lookup_result is None:
        return True, "Recycling information for this item cannot be found. When in doubt, ask building staff."

    return False, ""


def refusal_message(refuse_flag: bool, message: str) -> str:
    """
    Generate formatted refusal message for frontend rendering.
    Args:
        refuse_flag: Boolean flag from should_refuse()
        message: Raw message string from should_refuse()
    Returns:
        Formatted warning string; empty string if no refusal required
    """
    if not refuse_flag:
        return ""
    return f"⚠️ {message}"


def get_all_hazard_candidates() -> list[str]:
    """
    Return all normalized hazardous item keys as a public candidate list.
    Safely initializes the dataset if it has not been loaded yet.
    Returns:
        List of normalized hazardous item name strings
    """
    global _hazard_dict
    if _hazard_dict is None:
        load_hazard_items()
    return list(_hazard_dict.keys())
