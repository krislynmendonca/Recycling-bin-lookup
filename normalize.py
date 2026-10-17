import string

def normalize_text(raw_input: str) -> str:
    """
    Normalize input string: convert to lowercase, strip whitespace, remove punctuation.
    Satisfies requirement example: normalize("Pop Can!") -> "pop can"
    Args:
        raw_input: Raw user input string
    Returns:
        Fully normalized cleaned string
    """
    if not isinstance(raw_input, str):
        return ""
    # Strip leading/trailing whitespace and convert all characters to lowercase
    cleaned = raw_input.strip().lower()
    # Remove all punctuation symbols from string
    cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
    return cleaned


if __name__ == "__main__":
    # Self test routine
    test_cases = [
        "Aluminum Can",
        "  Battery  ",
        "Plastic Bottle",
        "Pop Can!"
    ]
    for case in test_cases:
        print(f"raw: {repr(case)} -> normalized: {repr(normalize_text(case))}")
