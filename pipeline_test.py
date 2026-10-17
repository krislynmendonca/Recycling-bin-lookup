from normalize import normalize_text
from lookup import lookup_item
from refusal import should_refuse, refusal_message


def full_pipeline(raw_input: str):
    """
    End-to-end pipeline to run the complete recycling lookup workflow.
    Steps: raw input normalization -> item lookup -> refuse rule evaluation -> message formatting.
    Detects condition prompts that require frontend user confirmation.
    Args:
        raw_input: original user input string
    Returns:
        tuple(refuse_flag: bool, message: str, lookup_res: dict | None)
    """
    print(f"\nRaw Input: {repr(raw_input)}")
    norm = normalize_text(raw_input)
    print(f"Normalized: {repr(norm)}")
    
    lookup_res = lookup_item(norm)
    
    # Check for conditional prompt, requires frontend button rendering for user selection
    if lookup_res and lookup_res.get("condition"):
        print(f"⚠️ Condition prompt detected: {lookup_res['condition']} (Frontend needs to render selection buttons)")
        
    refuse_flag, msg = should_refuse(norm, lookup_res)
    formatted_msg = refusal_message(refuse_flag, msg)
    
    print(f"Lookup Result: {lookup_res}")
    print(f"Refuse: {refuse_flag}, Message: {formatted_msg}")
    return refuse_flag, msg, lookup_res


if __name__ == "__main__":
    # Test cases covering punctuation cleanup, hazardous item, unknown item, synonym and conditional prompt
    full_pipeline("Pop Can!")
    full_pipeline("battery")
    full_pipeline("random unknown item")
    full_pipeline("Plastic Bottle!")
    # Test item with conditional requirement (e.g. clean/greasy pizza box check)
    full_pipeline("pizza box")
