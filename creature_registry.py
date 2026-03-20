"""
creature_registry.py — WORLDHATCH Full Creature Registry
══════════════════════════════════════════════════════════
Builds CREATURE_REGISTRY for all 100 creatures from roster.py.

Each creature gets:
  - base_stats scaled by element and rarity
  - traits assigned by element type
  - starter + learnable abilities by element
  - evolution path to a named evolved form
  - possible mutations based on element

This file is imported by creature.py.
Do NOT edit manually — edit roster.py and regenerate.
"""

from roster import FULL_ROSTER

# ─────────────────────────────────────────────
#  STAT TEMPLATES BY ELEMENT
#  Base stats are tuned per element archetype.
#  Rarity multiplier is applied on top.
# ─────────────────────────────────────────────

ELEMENT_STAT_TEMPLATE = {
    "fire":    {"hp": 75,  "attack": 20, "defense": 10, "speed": 14, "elem_power": 18},
    "ice":     {"hp": 85,  "attack": 18, "defense": 16, "speed": 11, "elem_power": 17},
    "nature":  {"hp": 95,  "attack": 16, "defense": 18, "speed": 9,  "elem_power": 14},
    "spirit":  {"hp": 65,  "attack": 14, "defense": 8,  "speed": 22, "elem_power": 16},
    "dark":    {"hp": 70,  "attack": 22, "defense": 12, "speed": 18, "elem_power": 15},
    "storm":   {"hp": 68,  "attack": 19, "defense": 10, "speed": 20, "elem_power": 16},
    "water":   {"hp": 80,  "attack": 15, "defense": 15, "speed": 14, "elem_power": 15},
    "sand":    {"hp": 78,  "attack": 17, "defense": 17, "speed": 13, "elem_power": 14},
    "magma":   {"hp": 100, "attack": 24, "defense": 20, "speed": 6,  "elem_power": 20},
    "crystal": {"hp": 90,  "attack": 14, "defense": 25, "speed": 8,  "elem_power": 18},
}

RARITY_MULTIPLIER = {
    "common":    1.0,
    "uncommon":  1.15,
    "rare":      1.35,
    "legendary": 1.65,
}

# ─────────────────────────────────────────────
#  TRAITS BY ELEMENT
# ─────────────────────────────────────────────

ELEMENT_TRAITS = {
    "fire":    ["ember_core", "tough_hide"],
    "ice":     ["frost_veins", "tough_hide"],
    "nature":  ["verdant_soul", "tough_hide"],
    "spirit":  ["hollow_bones", "lone_wanderer"],
    "dark":    ["lone_wanderer", "mimic_scale"],
    "storm":   ["hollow_bones", "pack_instinct"],
    "water":   ["verdant_soul", "pack_instinct"],
    "sand":    ["tough_hide", "territorial"],
    "magma":   ["tough_hide", "ember_core"],
    "crystal": ["tough_hide", "territorial"],
}

RARITY_BONUS_TRAITS = {
    "uncommon":  ["territorial"],
    "rare":      ["territorial", "pack_instinct"],
    "legendary": ["worldborn", "territorial"],
}

# ─────────────────────────────────────────────
#  ABILITIES BY ELEMENT
# ─────────────────────────────────────────────

ELEMENT_STARTER_ABILITY = {
    "fire":    "ember_bite",
    "ice":     "glacial_slam",
    "nature":  "root_bind",
    "spirit":  "shadow_dash",
    "dark":    "shadow_dash",
    "storm":   "scorchwave",
    "water":   "root_bind",
    "sand":    "ember_bite",
    "magma":   "scorchwave",
    "crystal": "glacial_slam",
}

ELEMENT_LEARNABLE = {
    "fire":    ["scorchwave", "root_bind"],
    "ice":     ["root_bind", "shadow_dash"],
    "nature":  ["scorchwave", "glacial_slam"],
    "spirit":  ["root_bind", "glacial_slam"],
    "dark":    ["root_bind", "glacial_slam"],
    "storm":   ["shadow_dash", "glacial_slam"],
    "water":   ["glacial_slam", "shadow_dash"],
    "sand":    ["scorchwave", "shadow_dash"],
    "magma":   ["ember_bite", "root_bind"],
    "crystal": ["root_bind", "scorchwave"],
}

# ─────────────────────────────────────────────
#  MUTATIONS BY ELEMENT
# ─────────────────────────────────────────────

ELEMENT_MUTATIONS = {
    "fire":    ["inferno_crest", "shadow_stripe"],
    "ice":     ["glacial_mantle", "shadow_stripe"],
    "nature":  ["verdant_bloom", "shadow_stripe"],
    "spirit":  ["shadow_stripe", "verdant_bloom"],
    "dark":    ["shadow_stripe", "glacial_mantle"],
    "storm":   ["shadow_stripe", "inferno_crest"],
    "water":   ["verdant_bloom", "glacial_mantle"],
    "sand":    ["inferno_crest", "verdant_bloom"],
    "magma":   ["inferno_crest", "glacial_mantle"],
    "crystal": ["glacial_mantle", "verdant_bloom"],
}

# ─────────────────────────────────────────────
#  HATCH TIMES BY RARITY
# ─────────────────────────────────────────────

RARITY_HATCH_TIME = {
    "common":    20,
    "uncommon":  40,
    "rare":      75,
    "legendary": 180,
}

# ─────────────────────────────────────────────
#  BUILD REGISTRY
# ─────────────────────────────────────────────

def _build_stats(element: str, rarity: str) -> dict:
    template = ELEMENT_STAT_TEMPLATE[element]
    mult     = RARITY_MULTIPLIER[rarity]
    elem_key = f"{element}_power"
    stats = {
        "hp":       round(template["hp"]      * mult),
        "attack":   round(template["attack"]  * mult),
        "defense":  round(template["defense"] * mult),
        "speed":    round(template["speed"]   * mult),
        elem_key:   round(template["elem_power"] * mult),
    }
    return stats


def _build_traits(element: str, rarity: str) -> list:
    traits = list(ELEMENT_TRAITS.get(element, ["tough_hide"]))
    bonus  = RARITY_BONUS_TRAITS.get(rarity, [])
    for t in bonus:
        if t not in traits:
            traits.append(t)
    return traits


def _build_evolution(creature_id: str, rarity: str) -> dict:
    """
    Build evolution paths.
    Every creature evolves to a named [creature_id]_evolved form.
    Legendaries don't evolve — they're already the apex.
    """
    if rarity == "legendary":
        return {}

    min_lvl = {"common": 10, "uncommon": 12, "rare": 15}[rarity]
    return {
        "default": {
            "to":         f"{creature_id}_evolved",
            "min_level":  min_lvl,
            "conditions": [],
        },
        "ancient": {
            "to":         f"{creature_id}_ancient",
            "min_level":  min_lvl + 5,
            "conditions": ["ancient_form_card"],
        },
    }


def build_creature_registry() -> dict:
    """
    Iterate over all 100 creatures in FULL_ROSTER and build
    a complete CREATURE_REGISTRY dict for use in creature.py.
    """
    registry = {}

    for region_id, region_data in FULL_ROSTER.items():
        for c in region_data["creatures"]:
            cid     = c["id"]
            element = c["element"]
            rarity  = c["rarity"]

            registry[cid] = {
                "display_name":       c["name"],
                "home_region":        region_id,
                "element":            element,
                "rarity":             rarity,
                "description":        c["description"],
                "base_stats":         _build_stats(element, rarity),
                "base_traits":        _build_traits(element, rarity),
                "starter_abilities":  [ELEMENT_STARTER_ABILITY[element]],
                "learnable_abilities": ELEMENT_LEARNABLE[element],
                "evolution_paths":    _build_evolution(cid, rarity),
                "possible_mutations": ELEMENT_MUTATIONS[element],
                "base_hatch_time":    RARITY_HATCH_TIME[rarity],
            }

    return registry


# Build once at import time
CREATURE_REGISTRY = build_creature_registry()


if __name__ == "__main__":
    print(f"Registry built: {len(CREATURE_REGISTRY)} creatures")
    legendaries = [v["display_name"] for v in CREATURE_REGISTRY.values()
                   if v["rarity"] == "legendary"]
    print(f"Legendaries ({len(legendaries)}): {legendaries}")
    sample = CREATURE_REGISTRY["inkfox"]
    print(f"\nSample — Inkfox:")
    for k, v in sample.items():
        print(f"  {k}: {v}")
