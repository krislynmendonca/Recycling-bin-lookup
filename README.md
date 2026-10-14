<div align="center">

# ♻️ Campus Recycling Helper

**Stop guessing. Start sorting right.**

A local tool that tells HKU hall residents the correct disposal bin — with a citation to the official campus rule.

[![Course](https://img.shields.io/badge/course-AILT9019-blue)](https://docs.google.com/document/d/1WBkZcDWirk_iRqzOrpBovxm4_qMsqvY7jV7guAyjHf0/edit?tab=t.0)
[![Status](https://img.shields.io/badge/status-in%20development-yellow)]()
[![Method](https://img.shields.io/badge/method-CSV%20lookup-orange)](https://github.com/krislynnmendonca/Recycling-bin-lookup/blob/main/SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/krislynnmendonca/Recycling-bin-lookup/blob/main/LICENSE)

**HKU · Lap Chee College**

</div>

---

## 🚀 Quick Start — How to Set Up and Run the Core Workflow

### Prerequisites
- Python 3.9 or higher
- No paid API. No cloud. Runs entirely locally.

### One-Command Setup

```bash
pip install -r requirements.txt && python app.py
```

Then open **http://localhost:5000** in your browser.

That's it — no coding background needed.

### Step-by-Step (if you prefer)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open in browser
# → http://localhost:5000
```

---

## ✅ How to Check the Result

Once the app is running, open **http://localhost:5000** and try these test inputs.

### Manual Verification (Type These In)

| Type this | You should see |
|-----------|----------------|
| `plastic bottle` | ✅ Bin: **RECYCLING** + Citation: *HKU Recycling Guide p.2* |
| `pop can` | ✅ Bin: **RECYCLING** + Citation: *HKU Recycling Guide p.2* (synonym works) |
| `pizza box` | ⚠️ Condition prompt: *"if clean → compost; if greasy → trash"* |
| `battery` | 🚫 Refused + Contact: **HKU Estates Office — Hazardous Waste** |
| `car battery` | 🚫 Refused + Contact: **HKU Estates Office — Automotive** |
| `unknown thing` | ❓ Not found + Contact: **HKU Estates Office** |

### Automated Verification (Run Tests)

```bash
pytest tests/ -v
```

**Expected result:** All 6 test files pass.

| Test File | What It Verifies |
|-----------|------------------|
| `test_30_items.py` | 85%+ bin accuracy, 100% hazardous refusal |
| `test_synonyms.py` | "pop can" = "soda can" = "aluminum can" |
| `test_conditions.py` | Pizza box returns condition prompt |
| `test_adversarial.py` | Misspellings and vague inputs are refused |
| `test_near_miss.py` | Battery variants route to correct channels |
| `test_citation_accuracy.py` | Every citation includes a page number |

### What Success Looks Like

If everything works:

- ✅ Known items return the correct bin + citation
- ✅ Hazardous items are refused with the correct HKU contact
- ✅ Unknown items are refused with a redirect (no guessing)
- ✅ All tests pass with `pytest tests/ -v`

---

## 🎯 What It Does

| Input | Output |
|-------|--------|
| `"plastic bottle"` | Bin: **Recycling** — Citation: *HKU Recycling Guide p.2* |
| `"pop can"` | Bin: **Recycling** — Citation: *HKU Recycling Guide p.2* (synonym) |
| `"pizza box"` | **Condition:** if clean → compost; if greasy → trash |
| `"battery"` | **Refused** — Campus Facilities — Hazardous Waste |
| `"car battery"` | **Refused** — Campus Facilities — Automotive |
| `"unknown thing"` | **Not found** — please contact Facilities |

---

## 🚫 What It Does NOT Do

- ❌ Does **not** handle hazardous-waste disposal
- ❌ Does **not** override building staff instructions
- ❌ Does **not** invent rules not in the published source
- ❌ Does **not** guess when unsure — it refuses and redirects

> **When in doubt, ask building staff.**

---

## ⚙️ Method

- **Lookup:** Deterministic CSV lookup — exact match (case-insensitive) + synonyms
- **No LLM required.** No paid API. No cloud setup. Runs entirely locally.
- **No fuzzy guessing:** anything not in the database is refused and redirected.
- **Hazardous items checked first** — always refused with the correct contact channel.

---

## 📚 Data Source

- **Campus:** University of Hong Kong
- **Hall:** Lap-Chee College at Jockey Club Student Village III
- **Source:** *[Exact PDF Title]*, Version [X.X], [Date]
- **URL:** [exact URL]
- **Coverage:** 20 items across recycling, compost, and trash
- **Last verified:** 12th October, 2026.

All citations in `data/recycling_rules.csv` point to specific pages in the source above. If the source is updated, this table must be re-verified.

---

## 🚨 Hazardous Items

The system **always refuses** these items and redirects to the correct contact. No hazardous item is ever guessed or binned.

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

## 🧪 Testing

The test set has **30 items**:

| Group | Count | Pass Rule |
|-------|:-----:|-----------|
| Regular waste | 10 | ≥ 85% bin accuracy + ≥ 85% citation accuracy |
| Edge cases | 10 | ≥ 70% pass (bin/condition/refusal), zero invented rules |
| Hazardous | 10 | 100% refusal |

Run all tests:

```bash
pytest tests/ -v
```

---

## 🔬 Independent Labeling

The 30-item test set was independently labeled by a team member using only the published campus rules, without access to the system's CSV, to avoid circular validation.

---

## ⚖️ Ethics

| Risk | Mitigation |
|------|------------|
| Misuse for hazardous items | Hard refusal + on-screen Facilities contact |
| Wrong bin output | Cited rule on every item + "when in doubt, ask staff" note |
| Data privacy | Only public campus rules; no personal data collected |

**Does not:** handle hazardous-waste disposal, override building staff instructions, or invent rules not in the published source.

---

## 📂 Project Structure

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

## 👥 Team

| Person | Role |
|--------|------|
| 👤 MENDONCA KRISLYN MARIAH | Data & Rules |
| 👤 JIN HAOYUE | Core Logic |
| 👤 SHANG ZIYAN | Frontend & UI |
| 👤 DING HAOYANG | Testing & Documentation |

*Course: AILT9019 · AI Literacy II · Final Project Package*

---

## 📄 License

MIT

---

<div align="center">

*One package · clear evidence · honest disclosure*

</div>
