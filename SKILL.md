# Skill: Recycling Bin Lookup

## Description
Given an item name, returns the correct campus recycling bin and citation.
Refuses hazardous and unlisted items. **No guessing.**

## Input
- `item` (string): The name of the waste item

## Output (JSON)
- `status` (string): `"found"` | `"condition"` | `"refused"` | `"not_found"` | `"empty"`
- `bin` (string | null): The correct bin category
- `citation` (string | null): The governing campus rule
- `condition` (string | null): Condition text if the item is conditional
- `message` (string): Human-readable guidance

## Lookup Rules

1. **Normalize** input: lowercase, trim, strip punctuation, collapse whitespace.
2. **Hazardous check first** → if in `hazardous_items.csv`, refuse with contact.
3. **Exact match** against `recycling_rules.csv` `item` column.
4. **Synonym match** against the `synonyms` column (pipe-separated).
5. **No fuzzy matching.** No guessing. Anything else → `not_found` + redirect.

## Examples

### Example 1 — Simple item
**Input:** `"plastic bottle"`

**Output:**
```json
{
  "status": "found",
  "bin": "recycling",
  "citation": "[SOURCE] p.2",
  "condition": null,
  "message": "Place in the RECYCLING bin. Rule: [SOURCE] p.2. When in doubt, ask building staff."
}
