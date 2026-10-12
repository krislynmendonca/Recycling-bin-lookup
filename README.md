<div align="center">

# ♻️ Campus Recycling Helper

**Stop guessing. Start sorting right.**

A local tool that tells HKU hall residents the correct disposal bin — with a citation to the official campus rule.

[![Course](https://img.shields.io/badge/course-AILT9019-blue)](https://docs.google.com/document/d/1WBkZcDWirk_iRqzOrpBovxm4_qMsqvY7jV7guAyjHf0/edit?tab=t.0)
[![Status](https://img.shields.io/badge/status-in%20development-yellow)]()
[![Method](https://img.shields.io/badge/method-CSV%20lookup-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/krislynmendonca/Recycling-bin-lookup/blob/main/LICENSE)

**HKU · Lap Chee College**

</div>

---

## 📖 Overview

Recycling guidelines are scattered across pages and posters. Residents guess — and contaminated streams are the result.

**This tool fixes that.** Enter an item, get the correct bin, see the official citation.

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt && python app.py
```

Then open **http://localhost:5000** in your browser.

> No coding background needed. No paid API. No cloud setup. Runs locally.

---

## 🎯 What It Does

| Input | Output |
|-------|--------|
| `"plastic bottle"` | ♻️ **Recycling** — *HKU Recycling Guide p.2* |
| `"pop can"` | ♻️ **Recycling** — *HKU Recycling Guide p.2* (synonym) |
| `"pizza box"` | ⚠️ **Condition:** if clean → compost; if greasy → trash |
| `"battery"` | 🚫 **Refused** — HKU Estates Office (Hazardous Waste) |
| `"car battery"` | 🚫 **Refused** — HKU Estates Office (Automotive) |
| `"unknown thing"` | ❓ **Not found** — contact HKU Estates Office |

---

## 🚫 What It Does NOT Do

| ❌ | ❌ | ❌ |
|:-:|:-:|:-:|
| Handle hazardous-waste disposal | Override building staff instructions | Invent rules not in the published source |
| **Guess when unsure** — it refuses and redirects | | |

> **When in doubt, ask building staff.**

---

## ⚙️ Method

| Component | Detail |
|-----------|--------|
| **Lookup** | Deterministic CSV lookup — exact match + synonyms |
| **LLM required?** | ❌ No — pure CSV + Python |
| **Fuzzy matching?** | ❌ No — exact match only, no guessing |
| **Hazardous handling** | ✅ Checked first, always refused with contact |
| **Local only?** | ✅ Yes — no paid API, no cloud |

---

## 📚 Data Source

| Field | Value |
|-------|-------|
| **Campus** | The University of Hong Kong (HKU) |
| **Hall** | Lap Chee College |
| **Source** | *HKU Recycling Guide*, Version [X.X], [Date] |
| **URL** | [exact URL] |
| **Coverage** | 20 items across recycling, compost, and trash |
| **Last verified** | October 12, 2026 |

All citations in `data/recycling_rules.csv` point to specific pages in the source above. If the source is updated, this table must be re-verified.

---

## 🚨 Hazardous Items

The system **always refuses** these items and redirects to the correct contact. No hazardous item is ever guessed or binned.

| Item | Contact |
|------|---------|
| 💉 syringe | HKU Health Service — uhealth@hku.hk \| (852) 2549-4686 |
| 🔋 battery | HKU Estates Office — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| 🚗 car battery | HKU Estates Office — Automotive: parking@hku.hk or eosecure@hku.hk\| (852) 3917-2882 or (852) 3917-2883 |
| 💻 laptop battery | HKU IT Services — E-Waste:ithelp@hku.hk \| (852) 3917-0123 |
| 📱 phone battery | HKU IT Services — E-Waste: ithelp@hku.hk \| (852) 3917-0123 |
| 🧪 chemical waste | HKU Estates Office — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| 💡 light bulb | HKU Estates Office — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| 🔆 fluorescent bulb | HKU Estates Office — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| 🎨 paint can | HKU Estates Office — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| 🛢️ motor oil | HKU Estates Office — Automotive:  parking@hku.hk or eosecure@hku.hk\| (852) 3917-2882 or (852) 3917-2883 |
| 🐜 pesticide | HKU Estates Office — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| 🩺 medical waste | HKU Health Service — uhealth@hku.hk \| (852) 2549-4686 |
| 💨 aerosol can | HKU Estates Office — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| 💅 nail polish | HKU Estates Office — Hazardous Waste: chemical@hku.hk \| (852) 3917-2402 |
| 🖨️ ink cartridge | HKU IT Services — E-Waste: ithelp@hku.hk \| (852) 3917-0123 |

**No hazardous item is ever guessed.** Every refusal includes a contact channel.

---

## 🧪 Testing

The test set has **30 items**:

| Group | Count | Pass Rule |
|-------|:-----:|-----------|
| ✅ Regular waste | 10 | ≥ 85% bin accuracy + ≥ 85% citation accuracy |
| ⚠️ Edge cases | 10 | ≥ 70% pass, zero invented rules |
| 🚫 Hazardous | 10 | 100% refusal |

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
| 🚫 Misuse for hazardous items | Hard refusal + on-screen Facilities contact |
| ⚠️ Wrong bin output | Cited rule on every item + "when in doubt, ask staff" note |
| 🔒 Data privacy | Only public campus rules; no personal data collected |

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

<div align="center">

**♻️ Campus Recycling Helper · HKU · Lap Chee College**

*One package · clear evidence · honest disclosure*

</div>
