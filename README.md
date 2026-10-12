# Campus Recycling Helper

A local tool that tells university hall residents the correct disposal bin
for everyday items, with a citation to the official campus rule.

## Data Source

- **Campus:** [Your University]
- **Hall:** [Your Hall Name]
- **Source:** [Exact PDF Title], Version [X.X], [Date]
- **URL:** [exact URL]

## Hazardous Items

The system **always refuses** these items and redirects to the correct contact:

- syringe → Campus Health Services
- battery → Campus Facilities — Hazardous Waste
- car battery → Campus Facilities — Automotive
- laptop battery → Campus IT — E-Waste
- chemical waste → Campus Facilities — Hazardous Waste
- light bulb → Campus Facilities — Hazardous Waste
- paint can → Campus Facilities — Hazardous Waste
- motor oil → Campus Facilities — Automotive
- pesticide → Campus Facilities — Hazardous Waste
- medical waste → Campus Health Services

## What It Does NOT Do

- Does **not** handle hazardous-waste disposal
- Does **not** override building staff instructions
- Does **not** invent rules not in the published source
- Does **not** guess when unsure — it refuses and redirects

> **When in doubt, ask building staff.**

## Quick Start (Non-Coders Welcome)

### Prerequisites
- [Python 3.9+](https://www.python.org/downloads/)
- No paid API or cloud setup required — runs **locally**

### Setup — One Command

```bash
pip install -r requirements.txt && python app.py
