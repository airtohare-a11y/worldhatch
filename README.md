# WORLDHATCH — Game Engine Skeleton
### Creature Hatching & Trading | Python 3.10+

---

## ▶ Running on Replit
1. Upload all `.py` files into one Replit project (Python template)
2. Set the **Run** command to: `python worldhatch.py`
3. Hit **Run** — the demo session will print to console

No external packages required. Pure Python stdlib only.

---

## 📁 File Structure

| File | Purpose |
|---|---|
| `worldhatch.py` | Entry point — runs the demo |
| `game.py` | GameSession class + demo runner |
| `creature.py` | `Egg`, `Creature` classes + `CREATURE_REGISTRY` |
| `regions.py` | `REGIONS` dict + spawn tables |
| `traits.py` | `TRAITS` + `MUTATIONS` dicts + roll logic |
| `cards.py` | `CARDS` + `ABILITIES` dicts + apply logic |
| `player.py` | `Player` class (inventory, card use) |
| `trading.py` | `TradeProposal`, `TradeSession`, `propose_trade()` |

---

## 🧬 How to Add a New Creature Species

Open `creature.py`, find `CREATURE_REGISTRY`, and add:

```python
"your_creature_id": {
    "display_name":    "Your Creature Name",
    "home_region":     "region_id_here",
    "element":         "fire",          # fire | ice | nature | spirit | dark | storm
    "rarity":          "common",        # common | uncommon | rare | legendary
    "description":     "Flavor text.",
    "base_stats": {
        "hp": 80, "attack": 18, "defense": 12, "speed": 10,
        "fire_power": 15, "ice_power": 0,
    },
    "base_traits":         ["trait_id_1", "trait_id_2"],
    "starter_abilities":   ["ability_id"],
    "learnable_abilities": ["ability_id_2"],
    "evolution_paths": {
        "default": {"to": "evolved_species_id", "min_level": 10, "conditions": []},
    },
    "possible_mutations":  ["mutation_id_1"],
    "base_hatch_time":     30,
},
```

Then add it to the region's `spawn_table` in `regions.py`.

---

## 🗺 How to Add a New Region

Open `regions.py` and add to `REGIONS`:

```python
"your_region_id": {
    "display_name":    "Your Region Name",
    "real_world_ref":  "Real Geography",
    "biome":           "biome_type",
    "element":         "dominant_element",
    "climate":         "climate_type",
    "home_bonus":      {"hp": 10, "attack": 5, "speed": 3},
    "mutation_modifier": {"fire": 1.3, "ice": 0.7},
    "spawn_table":     {"creature_id": 40, "creature_id_2": 60},
    "egg_hatch_time_seconds": 30,
},
```

---

## 🃏 How to Add a New Card

Open `cards.py` and add to `CARDS`:

```python
"your_card_id": {
    "display_name": "Card Name",
    "card_type":    "gene",       # gene | ability | evolution | boost
    "rarity":       "common",
    "element":      "fire",
    "description":  "What it does.",
    "effects": {
        "mutation_boost":   {"mutation_id": 0.15},
        "stat_growth_bias": {"fire_power": 3},
        # OR: "grant_ability": "ability_id"
        # OR: "unlock_evolution_branch": "branch_name"
        # OR: "stat_boost": {"hp": 15}
    },
    "target_conditions": [],      # [] = any creature
    "consumable":        True,
},
```

---

## 🔮 Systems Summary

```
Egg ──hatch()──► Creature
  ↑                  ↑
Cards staged      Cards applied
(pre-hatch)       (post-hatch)
  │                  │
  └──► Mutations rolled on hatch
       (region modifier × card boosts × base chance)

Creature ──gain_xp()──► Level up ──evolve()──► New species form
Player ──propose_trade()──► TradeSession ──accept()──► Transfer
```

---

## 🌍 Current Regions
| ID | Name | Real World | Element |
|---|---|---|---|
| `suncrest_expanse` | Suncrest Expanse | US West Coast | Fire |
| `sakurami_highlands` | Sakurami Highlands | Japan | Spirit |
| `verdeluna_jungle` | Verdeluna Jungle | Brazil | Nature |
| `frostspire_reach` | Frostspire Reach | Norway | Ice |

---

*WORLDHATCH Engine Skeleton v0.1 — Ready for Replit*
