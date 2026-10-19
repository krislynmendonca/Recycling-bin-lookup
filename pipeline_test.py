from normalize import normalize_text
from lookup import lookup_item
from refusal import should_refuse, refusal_message, is_hazardous
from resolver import resolve_item


def full_pipeline(raw_input: str):
    """
    Two-stage pipeline with Stage0 safety pre-check.
    Stage0: Hazardous item check on raw normalized input, block hazardous items before LLM.
    Stage1: Exact local lookup, no LLM. If match found, proceed directly.
    Stage2: Only trigger LLM resolver when Stage1 returns None.
    Final safety evaluation uses resolved item name from LLM if available.
    Args:
        raw_input: original user input string
    Returns:
        tuple(refuse_flag: bool, message: str, lookup_res: dict | None)
    """
    print(f"\nRaw Input: {repr(raw_input)}")
    norm = normalize_text(raw_input)
    print(f"Normalized: {repr(norm)}")

    # ===== Stage 0: Absolute safety red line, check hazardous item from original normalized input =====
    # Block hazardous items even before entering lookup or LLM flow
    is_haz_raw, _ = is_hazardous(norm)
    if is_haz_raw:
        print("Stage0: Hazardous item matched from raw normalized input, block immediately!")
        refuse_flag, msg = should_refuse(norm, None)
        print(f"Refuse: {refuse_flag}, Message: {refusal_message(refuse_flag, msg)}")
        return refuse_flag, msg, None

    # ===== Stage 1: Exact match lookup =====
    lookup_res = lookup_item(norm)
    final_item_name = norm  # Record item name for final hazard evaluation
    if lookup_res is not None:
        print("Stage1: Exact match found, skip LLM")
    else:
        print("Stage1: No exact match, activate LLM resolver (Stage2)")
        resolver_result = resolve_item(norm)
        if resolver_result is not None:
            llm_resolved_item = resolver_result["resolved_item"]
            print(f"Stage2: LLM resolved to: {llm_resolved_item}")
            lookup_res = lookup_item(llm_resolved_item)
            final_item_name = llm_resolved_item  # Update item name for final hazard check
        else:
            print("Stage2: LLM cannot resolve valid item")
            lookup_res = None

    # Check conditional prompt, requires frontend button rendering for user selection
    if lookup_res and lookup_res.get("condition"):
        print(f"⚠️ Condition prompt detected: {lookup_res['condition']} (Frontend needs to render selection buttons)")

    # ===== Final safety evaluation =====
    # Use resolved item name to check hazardous item as second layer of safety protection
    refuse_flag, msg = should_refuse(final_item_name, lookup_res)
    formatted_msg = refusal_message(refuse_flag, msg)

    print(f"Lookup Result: {lookup_res}")
    print(f"Refuse: {refuse_flag}, Message: {formatted_msg}")
    return refuse_flag, msg, lookup_res


if __name__ == "__main__":
    full_pipeline("Pop Can!")
    full_pipeline("battery")
    full_pipeline("batterry")  # Test misspelled hazardous item, must be blocked
    full_pipeline("fanda can")  # Test alias resolvable only via LLM stage2
    full_pipeline("random unknown item")
    full_pipeline("Plastic Bottle!")
    full_pipeline("pizza box")
