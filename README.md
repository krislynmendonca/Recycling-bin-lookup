# ♻️ Campus Recycling Helper

A local tool that tells university hall residents the correct disposal bin
for everyday items, with a citation to the official campus rule.

**No guessing. No hallucinated rules. Just the published campus guide.**

---

## Quick Start

```bash
pip install -r requirements.txt && python app.py
```

Then open **http://localhost:5000** in your browser.

That's it — no coding background needed.

---

## What It Does

| Input | Output |
|-------|--------|
| `"plastic bottle"` | Bin: **Recycling** — Citation: *Campus Recycling Guide p.2* |
| `"pop can"` | Bin: **Recycling** — Citation: *Campus Recycling Guide p.2* (synonym) |
| `"pizza box"` | **Condition:** if clean → compost; if greasy → trash |
| `"battery"` | **Refused** — Campus Facilities — Hazardous Waste |
| `"car battery"` | **Refused** — Campus Facilities — Automotive |
| `"unknown thing"` | **Not found** — please contact Facilities |

---

## What It Does NOT Do

- ❌ Does **not** handle hazardous-waste disposal
- ❌ Does **not** override building staff instructions
- ❌ Does **not** invent rules not in the published source
- ❌ Does **not** guess when unsure — it refuses and redirects

> **When in doubt, ask building staff.**

---

## Method

- **Lookup:** Deterministic CSV lookup — exact match (case-insensitive) + synonyms
- **No LLM required.** No paid API. No cloud setup. Runs entirely locally.
- **No fuzzy guessing:** anything not in the database is refused and redirected.
- **Hazardous items checked first** — always refused with the correct contact channel.

---

## Data Source

- **Campus:** University of Hong Kong
- **Hall:** Lap-Chee College at Jockey Club Student Village III
- **Source:** *[Exact PDF Title]*, Version [X.X], [Date]
- **URL:** [exact URL]
- **Coverage:** 20 items across recycling, compost, and trash
- **Last verified:** 12th October, 2026.

All citations in `data/recycling_rules.csv` point to specific pages in the
source above. If the source is updated, this table must be re-verified.

---

## Hazardous Items

The system **always refuses** these items and redirects to the correct contact.
No hazardous item is ever guessed or binned.

| Item | Contact |
|------|---------|
| syringe | Campus Health Services — uhealth@hku.hk \| (852) 2549-4686 |
| battery | Campus Facilities — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| car battery | Campus Facilities — Automotive: parking@hku.hk or eosecure@hku.hk \| (852) 3917-2882 or (852) 3917-2883 |
| laptop battery | Campus IT — E-Waste: ithelp@hku.hk \| (852) 3917-0123 |
| phone battery | Campus IT — E-Waste: ithelp@hku.hk \| (852) 3917-0123 |
| chemical waste | Campus Facilities — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| light bulb | Campus Facilities — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| fluorescent bulb | Campus Facilities — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| paint can | Campus Facilities — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| motor oil | Campus Facilities — Automotive: parking@hku.hk or eosecure@hku.hk \| (852) 3917-2882 or (852) 3917-2883 |
| pesticide | Campus Facilities — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| medical waste | Campus Health Services — uhealth@hku.hk \| (852) 2549-4686 |
| aerosol can | Campus Facilities — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| nail polish | Campus Facilities — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| ink cartridge | Campus IT — E-Waste: ithelp@hku.hk \| (852) 3917-0123 |

**No hazardous item is ever guessed.** Every refusal includes a contact channel.

---

## Testing

The test set has **30 items**:

| Group | Count | Pass Rule |
|-------|-------|-----------|
| Regular waste | 10 | ≥ 85% bin accuracy + ≥ 85% citation accuracy |
| Edge cases | 10 | ≥ 70% pass (bin/condition/refusal), zero invented rules |
| Hazardous | 10 | 100% refusal |

Run all tests:

```bash
pytest tests/ -v
```

---

## Independent Labeling

The 30-item test set was independently labeled by a team member using only
the published campus rules, without access to the system's CSV, to avoid
circular validation.

---

## Ethics

| Risk | Mitigation |
|------|------------|
| Misuse for hazardous items | Hard refusal + on-screen Facilities contact |
| Wrong bin output | Cited rule on every item + "when in doubt, ask staff" note |
| Data privacy | Only public campus rules; no personal data collected |

**Does not:** handle hazardous-waste disposal, override building staff
instructions, or invent rules not in the published source.

---

## Project Structure

```
campus-recycling-helper/
├── README.md
├── requirements.txt
├── SKILL.md
├── .gitignore
├── app.py
├── lookup.py
├── refusal.py
├── normalize.py
├── data/
│   ├── recycling_rules.csv
│   └── hazardous_items.csv
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    ├── test_30_items.py
    ├── test_synonyms.py
    ├── test_conditions.py
    ├── test_adversarial.py
    ├── test_near_miss.py
    └── test_citation_accuracy.py
```

---

## Team

| Person | Role |
|--------|------|
| MENDONCA KRISLYN MARIAH | Data & Rules |
| Person B | Core Logic |
| Person C | Frontend & UI |
| Person D | Testing & Documentation |

*Course: AILT9019 · AI Literacy II · Final Project Package*

---

## License

MIT

---

*One package · clear evidence · honest disclosure*
