import json
import os
import csv
from llm_client import call_llm
from refusal import get_all_hazard_candidates

CACHE_PATH = "llm_cache.json"
CONFIDENCE_THRESHOLD = 0.7

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_CSV_PATH = os.path.join(BASE_DIR, "data", "recycling_rules.csv")


def load_cache() -> dict:
    """
    Load cached LLM resolution results from local json file.
    Returns empty dict if cache file does not exist.
    """
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache_data: dict):
    """
    Write updated cache dictionary into local json cache file.
    Args:
        cache_data: Full cache dictionary to persist
    """
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=2)


def _get_main_recycling_items() -> list[str]:
    """
    Get only main recycling item names (no synonyms) for minimal candidate list.
    Optimized for small local models with limited selection capability.
    """
    items = []
    with open(RULES_CSV_PATH, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row["item"].strip().lower())
    return items


def resolve_item(normalized_input: str) -> dict | None:
    """
    Stage2 LLM resolver: closed set selection.
    Return resolved normalized item name only if confidence >= threshold and exists in candidate list.
    Otherwise return None.
    Args:
        normalized_input: Normalized user input string
    Returns:
        Dictionary with resolved_item and confidence if valid; None otherwise
    """
    cache = load_cache()
    if normalized_input in cache:
        cached = cache[normalized_input]
        return cached if cached["resolved_item"] is not None else None

    # Minimal candidate set: main recycling items + hazardous items
    recycling_main = _get_main_recycling_items()
    hazard_items = get_all_hazard_candidates()
    all_candidates = list(set(recycling_main + hazard_items))
    candidate_list = ", ".join(all_candidates)

    prompt = f"""
Find the closest match from the list below.
Only pick from this list: {candidate_list}

Input: {normalized_input}
Output only JSON: {{"resolved_item": "string or null", "confidence": 0.0}}

Examples:
Input: cola can
Output: {{"resolved_item": "aluminum can", "confidence": 0.9}}

Input: batterry
Output: {{"resolved_item": "battery", "confidence": 0.9}}
"""
    try:
        raw_reply = call_llm(prompt)

        # Clean markdown markers
        raw_reply = raw_reply.strip()
        if raw_reply.startswith("```"):
            raw_reply = raw_reply.strip("`")
            if raw_reply.lower().startswith("json"):
                raw_reply = raw_reply[4:]
        raw_reply = raw_reply.strip()

        parsed = json.loads(raw_reply)
        resolved_item = parsed.get("resolved_item")
        confidence = float(parsed.get("confidence", 0))
    except Exception as e:
        cache[normalized_input] = {"resolved_item": None, "confidence": 0.0}
        save_cache(cache)
        return None

    # White list + confidence check
    if (resolved_item is not None
        and confidence >= CONFIDENCE_THRESHOLD
        and resolved_item in all_candidates):
        result_data = {"resolved_item": resolved_item, "confidence": confidence}
        cache[normalized_input] = result_data
        save_cache(cache)
        return result_data
    else:
        cache[normalized_input] = {"resolved_item": None, "confidence": confidence}
        save_cache(cache)
        return None
