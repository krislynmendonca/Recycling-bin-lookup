<div align="center">

# ♻️ Recycling Bin Lookup

**A skill for agents and apps to determine the correct HKU recycling bin — with citations, no guessing.**

[![Status](https://img.shields.io/badge/status-stable-brightgreen)]()
[![Data](https://img.shields.io/badge/data-CSV-blue)]()
[![Method](https://img.shields.io/badge/method-deterministic-orange)]()

</div>

---

## 📖 Description

Given an item name, this skill returns:

- ✅ The correct **HKU recycling bin**
- 📖 A **citation** to the governing HKU rule
- ⚠️ A **hard refusal** for hazardous items (with contact info)
- ❓ A **safe redirect** for items not in the database

> **No guessing. No hallucinated rules. Ever.**

---

## 📥 Input

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `item` | `string` | ✅ | The name of the waste item |

---

## 📤 Output

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | One of: `found`, `condition`, `refused`, `not_found`, `empty` |
| `bin` | `string \| null` | Bin category (`recycling`, `compost`, `trash`) or `null` |
| `citation` | `string \| null` | Governing HKU rule reference, or `null` |
| `condition` | `string \| null` | Condition text if the item is conditional, else `null` |
| `message` | `string` | Human-readable guidance |

---

## 🔍 Lookup Rules

| # | Rule | Action |
|:-:|------|--------|
| 1 | **Normalize input** | Lowercase, trim, strip punctuation, collapse whitespace |
| 2 | **Hazardous check first** | If in `data/hazardous_items.csv` → refuse with contact |
| 3 | **Exact match** | Against `item` column in `data/recycling_rules.csv` |
| 4 | **Synonym match** | Against `synonyms` column (pipe-separated) |
| 5 | **No fuzzy matching** | Anything else → `not_found` + redirect |

---

## 📚 Status Codes

| Status | Meaning | `bin` | `citation` |
|--------|---------|:-----:|:----------:|
| ✅ `found` | Item in database | ✅ | ✅ |
| ⚠️ `condition` | Item depends on condition | ✅ | ✅ |
| 🚫 `refused` | Hazardous item | ❌ | ❌ |
| ❓ `not_found` | Item not in database | ❌ | ❌ |
| ⬜ `empty` | No input provided | ❌ | ❌ |

---

## 💡 Examples

### ✅ Example 1 — Simple item (`found`)

**Input:**
```json
{ "item": "plastic bottle" }
```

**Output:**
```json
{
  "status": "found",
  "bin": "recycling",
  "citation": "HKU Recycling Guide p.2",
  "condition": null,
  "message": "Place in the RECYCLING bin. Rule: HKU Recycling Guide p.2. When in doubt, ask building staff."
}
```

---

### ⚠️ Example 2 — Conditional item (`condition`)

**Input:**
```json
{ "item": "pizza box" }
```

**Output:**
```json
{
  "status": "condition",
  "bin": "compost",
  "citation": "HKU Recycling Guide p.3",
  "condition": "if clean → compost; if greasy → trash",
  "message": "This item depends on condition: if clean → compost; if greasy → trash. Citation: HKU Recycling Guide p.3. When in doubt, ask building staff."
}
```

---

### 🔄 Example 3 — Synonym input (`found`)

**Input:**
```json
{ "item": "pop can" }
```

**Output:**
```json
{
  "status": "found",
  "bin": "recycling",
  "citation": "HKU Recycling Guide p.2",
  "condition": null,
  "message": "Place in the RECYCLING bin. Rule: HKU Recycling Guide p.2. When in doubt, ask building staff."
}
```

> 💡 `"pop can"` maps to `"aluminum can"` via the synonyms column.

---

### 🚫 Example 4 — Hazardous item (`refused`)

**Input:**
```json
{ "item": "battery" }
```

**Output:**
```json
{
  "status": "refused",
  "bin": null,
  "citation": null,
  "condition": null,
  "message": "⚠️ This item is hazardous. Contact: HKU Estates Office — Hazardous Waste. When in doubt, ask building staff."
}
```

---

### ❓ Example 5 — Not found (`not_found`)

**Input:**
```json
{ "item": "unknown widget" }
```

**Output:**
```json
{
  "status": "not_found",
  "bin": null,
  "citation": null,
  "condition": null,
  "message": "❓ This item is not in the published HKU recycling rules. Please contact HKU Estates Office. When in doubt, ask building staff."
}
```

---

### ⬜ Example 6 — Empty input (`empty`)

**Input:**
```json
{ "item": "" }
```

**Output:**
```json
{
  "status": "empty",
  "bin": null,
  "citation": null,
  "condition": null,
  "message": "Please enter an item name."
}
```

---

## 🛡️ Safety Guarantees

| Guarantee | How It's Enforced |
|-----------|-------------------|
| 🚫 **Hazardous items always refused** | Checked first, before any matching |
| 📖 **Never invents rules** | Only reads from `data/recycling_rules.csv` |
| ❓ **Never guesses** | Exact match only — no fuzzy logic |
| 📎 **Every answer includes evidence** | Citation (found) or contact (refused) |

---

## 📂 Data Files Required

| File | Columns | Purpose |
|------|---------|---------|
| `data/recycling_rules.csv` | `item, synonyms, bin, citation, condition` | Main lookup table |
| `data/hazardous_items.csv` | `item, contact` | Refusal list with contacts |

---

## 🔌 Integration

### Python
```python
from lookup import lookup_bin

result = lookup_bin("pizza box")
print(result["status"])   # "condition"
print(result["bin"])      # "compost"
print(result["citation"]) # "HKU Recycling Guide p.3"
```

### HTTP (Flask)
```bash
POST http://localhost:5000/
Content-Type: application/x-www-form-urlencoded

item=pizza+box
```

### Other Agents
Other agents can call this skill via MCP by pointing to `lookup_bin()`.

---

<div align="center">

**♻️ Campus Recycling Helper · HKU · Lap Chee College**

*One skill · clear evidence · honest disclosure*

</div>
