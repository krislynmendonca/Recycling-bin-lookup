# 📂 Data Files

This folder contains the raw data used by the recycling lookup system.

## 📄 `recycling_rules.csv`

Main lookup table for non-hazardous items.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `item` | string | Canonical item name (lowercase) | `plastic bottle` |
| `synonyms` | string | Pipe-separated alternates | `water bottle\|soda bottle` |
| `bin` | string | One of: `recycling`, `compost`, `trash` | `recycling` |
| `citation` | string | Specific page reference | `HKU Recycling Guide p.2` |
| `condition` | string | Optional condition (blank if unconditional) | `if clean → compost` |

## 📄 `hazardous_items.csv`

Items that must **always be refused** with a contact channel.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `item` | string | Hazardous item name (lowercase) | `battery` |
| `contact` | string | Department + email + phone | `HKU Estates Office — ...` |

## 🔄 How to Update

1. Open the CSV in a text editor or spreadsheet app
2. Add new rows following the column structure
3. Save as **UTF-8** (no BOM)
4. Run `python check_data.py` to verify
5. Commit with a clear message

## 🚨 Rules

- **Every row** must have a citation with a page number (`p.X`)
- **Synonyms** use `|` (pipe) — no spaces around the pipe
- **Conditions** are blank if the item is unconditional
- **No fuzzy matching data** — only exact items and synonyms

---

*Part of Campus Recycling Helper · HKU · Lap Chee College*
