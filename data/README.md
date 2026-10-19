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

## 🧠 LLM Optional Resolver Module

### Design Overview
The system implements a **two-stage lookup pipeline** following a reliability-first principle:
1. **Stage 1 – Exact Match (Core)**: Dictionary-based lookup using the CSV datasets above, delivering 100% deterministic, accurate results for all standard inputs.
2. **Stage 2 – LLM Resolution (Enhanced)**: Closed-set selection powered by a local large language model, triggered *only* when exact match fails. Intended for edge cases such as spelling typos.

### Core Principle: Zero-Guess Cutoff
Aligned with the system's safety-first design, all LLM outputs must pass **dual validation**:
- Whitelist verification against the `item` fields from both CSV files
- Minimum confidence threshold of `0.7`

Any result failing either check is rejected, and the system falls back to the standard "not found" prompt. This mechanism eliminates false classification by design.

### Capabilities & Limitations
| Supported Scenarios | Limitations & Boundaries |
|---------------------|--------------------------|
| English spelling correction (e.g. `batterry` → `battery`) | Pinyin-mixed input or strong semantic association tasks are not supported |
| Common synonym and phrasing variant matching | The local 3B quantized model is optimized for lightweight offline operation, with limited recognition capacity |
| Case and punctuation normalization | Recognition failure automatically falls back to the core rejection logic — this is intended behavior, not a defect |

### Deployment Notes
- Core lookup functionality operates fully without an Ollama environment. LLM call failures degrade gracefully by design.
- To switch to a cloud-hosted larger model, only the `.env` configuration needs to be updated; no changes to business logic are required.
- The LLM candidate pool is derived exclusively from the `item` columns of `recycling_rules.csv` and `hazardous_items.csv`.
