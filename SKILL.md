# Skill: Recycling Bin Lookup

## Description
Given an item name, returns the correct campus recycling bin and citation.
Refuses hazardous and unlisted items. No guessing.

## Input
- `item` (string): The name of the waste item

## Output (JSON)
- `status` (string): "found" | "condition" | "refused" | "not_found" | "empty"
- `bin` (string | null): The correct bin category
- `citation` (string | null): The governing campus rule
- `condition` (string | null): Condition text if the item is conditional
- `message` (string): Human-readable guidance

## Example
Input: "pizza box"
Output:
{
  "status": "condition",
  "bin": "compost",
  "citation": "Campus Recycling Guide p.3",
  "condition": "if clean → compost; if greasy → trash",
  "message": "This item depends on condition: if clean → compost; if greasy → trash"
}

Input: "battery"
Output:
{
  "status": "refused",
  "bin": null,
  "citation": null,
  "condition": null,
  "message": "⚠️ This item is hazardous. Contact: Campus Facilities — Hazardous Waste: facilities@university.edu | (555) 123-4567"
}
