# WORLDHATCH

A creature-hatching and trading game engine written in pure Python 3.

## Overview

WORLDHATCH is a game engine skeleton for a creature-hatching and trading game. It provides core logic for managing eggs, creatures (with stats and mutations), regions, players, and a trading system.

## Running the Project

```
python worldhatch.py
```

This runs a full demo session showcasing all major systems.

## Project Structure

| File | Purpose |
|------|---------|
| `worldhatch.py` | Main entry point — runs the demo session |
| `game.py` | `GameSession` class orchestrating players, state, and demo walkthrough |
| `creature.py` | `Egg` and `Creature` classes, stat calculations, and `CREATURE_REGISTRY` (all species data) |
| `regions.py` | World region definitions (biomes, elements, spawn tables, environmental modifiers) |
| `player.py` | `Player` class managing inventories (cards, eggs, creatures) and coin balances |
| `cards.py` | Consumable card logic (modifies egg hatch rates, boosts stats, unlocks evolution paths) |
| `traits.py` | `TRAITS` and `MUTATIONS` definitions with rolling logic for hatching |
| `trading.py` | `TradeProposal` and `TradeSession` for exchanging items and creatures between players |

## Tech Stack

- **Language:** Python 3.12
- **Dependencies:** None — pure Python standard library only

## Game Systems

- **Hatching System:** Eggs spawned in regions; cards applied before hatching influence mutations
- **Mutation & Traits:** Creatures born with base traits; mutations rolled based on regional modifiers and cards
- **Evolution:** Creatures evolve based on level requirements and specific conditions
- **Trading:** Formal trade system allows players to swap creatures, cards, and coins

## Regions

- `suncrest_expanse` — Fire region (US West Coast)
- `frostspire_reach` — Ice region (Norway / Scandinavia)
- `verdeluna_jungle` — Nature region (Brazil / Amazon Basin)
- `sakurami_highlands` — Spirit region (Japan)

## Adding Content

- **New species:** Add an entry to `CREATURE_REGISTRY` in `creature.py`
- **New regions:** Add an entry to `REGIONS` in `regions.py` with a spawn table
- **New cards:** Add an entry to `CARDS` in `cards.py`
- **New traits/mutations:** Add entries to `TRAITS` / `MUTATIONS` in `traits.py`

## Workflow

- **Start application** — `python worldhatch.py` (console output)
