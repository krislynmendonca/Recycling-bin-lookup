"""Flask web interface for the campus recycling lookup."""

import os

from flask import Flask, render_template, request

from lookup import lookup_bin
from normalize import normalize_text


app = Flask(__name__)


BIN_DETAILS = {
    "recycling": {
        "label": "Recycling",
        "icon": "♻️",
        "description": "Place this item in the blue recycling bin.",
    },
    "compost": {
        "label": "Compost",
        "icon": "🌱",
        "description": "Place this item in the food-waste or compost bin.",
    },
    "trash": {
        "label": "General waste",
        "icon": "🗑️",
        "description": "Place this item in the general-waste bin.",
    },
}


def parse_condition_branches(condition: str) -> list[dict[str, str]]:
    """Turn CSV conditions such as 'if clean → compost; if greasy → trash' into options."""
    branches = []
    for part in condition.split(";"):
        if "→" not in part:
            continue
        choice, bin_type = (piece.strip() for piece in part.split("→", 1))
        choice = choice.removeprefix("if ").strip()
        bin_type = bin_type.strip().lower()
        if not choice or not bin_type:
            continue
        branches.append(
            {
                "label": choice.title(),
                "value": normalize_text(choice),
                "bin": bin_type,
                "bin_label": bin_type.title(),
            }
        )
    return branches


def hazardous_contact() -> str:
    """Read the hazardous-waste contact from the shared data layer."""
    fallback = "HKU Estates Office — Hazardous Waste: chemical@hku.hk | (852) 3917-2402"
    chemical_waste = lookup_bin("chemical waste")
    message = chemical_waste.get("message", "")
    if "Contact: " in message:
        contact = message.split("Contact: ", 1)[1]
        return contact.split(". When in doubt", 1)[0]
    return fallback


def apply_condition_choice(
    result: dict, choice_value: str
) -> tuple[dict, bool]:
    """Resolve a selected condition branch without changing the core lookup API."""
    branches = parse_condition_branches(result.get("condition") or "")
    selected = next(
        (branch for branch in branches if branch["value"] == choice_value),
        None,
    )
    if selected is None:
        return result, False

    bin_type = selected["bin"]
    citation = result["citation"]
    if bin_type == "hazardous":
        return (
            {
                "status": "refused",
                "bin": None,
                "citation": citation,
                "condition": None,
                "message": (
                    f"This item is hazardous when {selected['label'].lower()}. "
                    f"Do not place it in a standard bin. Contact: {hazardous_contact()}. "
                    "When in doubt, ask building staff."
                ),
            },
            True,
        )

    bin_details = BIN_DETAILS.get(bin_type)
    if bin_details is None:
        return result, False

    return (
        {
            "status": "found",
            "bin": bin_type,
            "citation": citation,
            "condition": None,
            "message": (
                f"{selected['label']} item: place it in the "
                f"{bin_details['label'].lower()} bin."
            ),
        },
        True,
    )


@app.get("/")
def index():
    """Render the search page."""
    return render_template(
        "index.html",
        result=None,
        query="",
        bin_details=None,
        branches=[],
        resolved_condition=False,
    )


@app.post("/")
def lookup():
    """Process a search or a follow-up condition choice."""
    query = request.form.get("item", "").strip()
    choice_value = normalize_text(request.form.get("condition_option", ""))

    result = lookup_bin(query)
    branches = []
    resolved_condition = False

    if result["status"] == "condition":
        if choice_value:
            result, resolved_condition = apply_condition_choice(result, choice_value)
        if not resolved_condition:
            branches = parse_condition_branches(result.get("condition") or "")

    bin_details = BIN_DETAILS.get(result.get("bin")) if result.get("bin") else None
    return render_template(
        "index.html",
        result=result,
        query=query,
        bin_details=bin_details,
        branches=branches,
        resolved_condition=resolved_condition,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
