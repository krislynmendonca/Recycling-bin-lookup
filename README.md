# Recycling-bin-lookup

A local AI tool that helps university hall residents determine the correct disposal bin for everyday items, using **published campus recycling rules**.

Enter an item (e.g., `"pizza box"`, `"battery"`, `"glass bottle"`) and get:
- The correct **bin category**
- A **citation** to the governing campus rule

## Why This Exists

Recycling guidelines are scattered across pages and posters, leading residents to guess and contaminate recycling streams. This tool provides a single, reliable lookup point — and refuses to guess when it shouldn't.

## What It Does

| Input | Output |
|-------|--------|
| `"pizza box"` | Bin: **Compost** — Citation: *Campus Recycling Guide p.3* |
| `"glass bottle"` | Bin: **Recycling** — Citation: *Campus Recycling Guide p.2* |
| `"syringe"` | **Refused** — "This item is hazardous. Please contact Facilities at [contact info]." |
| `"unknown item"` | **Not found** — "Item not listed. Please contact the official facilities contact." |

## What It Does NOT Do

- ❌ Does **not** handle hazardous-waste disposal
- ❌ Does **not** override building staff instructions
- ❌ Does **not** invent rules not in the published source
- ❌ Does **not** guess a bin when unsure — it refuses and redirects

> **When in doubt, ask building staff.**

## Quick Start (Non-Coders Welcome)

### Prerequisites
- [Python 3.9+](https://www.python.org/downloads/)
- No paid API or cloud setup required — runs **locally**

### Setup — One Command

```bash
pip install -r requirements.txt && python app.py
