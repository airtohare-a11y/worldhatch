"""
traits.py — WORLDHATCH Trait & Mutation System
═══════════════════════════════════════════════
Traits are passive properties that define a creature's personality,
strengths, and weaknesses.

Mutations are acquired traits that can:
  - Appear at hatch (based on region modifiers)
  - Trigger during evolution (based on cards + conditions)
  - Stack with existing traits (some combinations unlock hidden effects)

TO ADD A NEW TRAIT:
  Add an entry to TRAITS dict. Give it a category, description,
  and any stat_modifiers or special_flags you need.

TO ADD A NEW MUTATION:
  Add an entry to MUTATIONS dict. Set trigger_conditions and effects.
  Reference mutation IDs in creature evolution paths (creature.py).
"""

import random


# ─────────────────────────────────────────────
#  TRAIT DEFINITIONS
#  Categories: "physical", "elemental", "behavioral", "rare"
# ─────────────────────────────────────────────

TRAITS = {

    # ── Physical ───────────────────────────────
    "tough_hide": {
        "display_name":  "Tough Hide",
        "category":      "physical",
        "description":   "Thick scales reduce incoming damage.",
        "stat_modifiers": {"defense": 8, "speed": -2},
        "special_flags":  [],
    },
    "hollow_bones": {
        "display_name":  "Hollow Bones",
        "category":      "physical",
        "description":   "Lightweight frame grants superior agility.",
        "stat_modifiers": {"speed": 10, "hp": -5},
        "special_flags":  ["can_glide"],
    },
    "iron_jaw": {
        "display_name":  "Iron Jaw",
        "category":      "physical",
        "description":   "Bite attacks deal extra damage.",
        "stat_modifiers": {"attack": 6},
        "special_flags":  ["bite_boost"],
    },

    # ── Elemental ──────────────────────────────
    "ember_core": {
        "display_name":  "Ember Core",
        "category":      "elemental",
        "description":   "Internal heat source boosts fire abilities.",
        "stat_modifiers": {"fire_power": 12, "ice_resist": -10},
        "special_flags":  ["fire_affinity"],
    },
    "frost_veins": {
        "display_name":  "Frost Veins",
        "category":      "elemental",
        "description":   "Icy blood slows attackers on contact.",
        "stat_modifiers": {"ice_power": 10, "fire_resist": -8},
        "special_flags":  ["chill_on_hit"],
    },
    "verdant_soul": {
        "display_name":  "Verdant Soul",
        "category":      "elemental",
        "description":   "Nature energy regenerates HP over time.",
        "stat_modifiers": {"hp_regen": 3},
        "special_flags":  ["nature_affinity", "regen"],
    },

    # ── Behavioral ─────────────────────────────
    "territorial": {
        "display_name":  "Territorial",
        "category":      "behavioral",
        "description":   "Stat boost when defending home region.",
        "stat_modifiers": {"attack": 5, "defense": 5},
        "special_flags":  ["home_region_bonus_amplified"],
    },
    "pack_instinct": {
        "display_name":  "Pack Instinct",
        "category":      "behavioral",
        "description":   "Grows stronger when allied creatures are present.",
        "stat_modifiers": {},
        "special_flags":  ["ally_buff"],
    },
    "lone_wanderer": {
        "display_name":  "Lone Wanderer",
        "category":      "behavioral",
        "description":   "Stronger when fighting alone; no allies needed.",
        "stat_modifiers": {"attack": 10, "defense": 5},
        "special_flags":  ["solo_boost"],
    },

    # ── Rare ───────────────────────────────────
    "worldborn": {
        "display_name":  "Worldborn",
        "category":      "rare",
        "description":   "Creature was born during a realm-wide event. Glows faintly.",
        "stat_modifiers": {"all_stats": 5},
        "special_flags":  ["rare_glow", "event_spawn"],
    },
    "mimic_scale": {
        "display_name":  "Mimic Scale",
        "category":      "rare",
        "description":   "Can temporarily copy a defeated creature's type.",
        "stat_modifiers": {},
        "special_flags":  ["type_copy"],
    },

    # ── Add more traits here ───────────────────
}


# ─────────────────────────────────────────────
#  MUTATION DEFINITIONS
#  Mutations are acquired during hatching or evolution.
#  trigger_conditions: list of strings checked by evolution logic
#  effects: dict of stat changes or flag additions
# ─────────────────────────────────────────────

MUTATIONS = {

    "inferno_crest": {
        "display_name":       "Inferno Crest",
        "element":            "fire",
        "description":        "A blazing crest erupts, amplifying fire power dramatically.",
        "trigger_conditions": ["has_ember_core", "fire_card_applied", "region_suncrest_expanse"],
        "base_chance":        0.15,          # 15% base chance if conditions met
        "effects": {
            "stat_modifiers": {"fire_power": 20, "hp": -5},
            "add_traits":     ["ember_core"],
            "add_ability":    "scorchwave",
            "visual_change":  "crest_flame",
        },
    },

    "glacial_mantle": {
        "display_name":       "Glacial Mantle",
        "element":            "ice",
        "description":        "Ice crystals form a protective shell.",
        "trigger_conditions": ["region_frostspire_reach", "ice_card_applied"],
        "base_chance":        0.20,
        "effects": {
            "stat_modifiers": {"defense": 15, "speed": -5},
            "add_traits":     ["frost_veins", "tough_hide"],
            "visual_change":  "ice_armor",
        },
    },

    "verdant_bloom": {
        "display_name":       "Verdant Bloom",
        "element":            "nature",
        "description":        "Flowers bloom across the creature's body, granting healing pulses.",
        "trigger_conditions": ["region_verdeluna_jungle", "nature_card_applied"],
        "base_chance":        0.25,
        "effects": {
            "stat_modifiers": {"hp": 20, "hp_regen": 5},
            "add_traits":     ["verdant_soul"],
            "visual_change":  "bloom_coat",
        },
    },

    "shadow_stripe": {
        "display_name":       "Shadow Stripe",
        "element":            "dark",
        "description":        "Dark energy stripes appear, granting stealth capability.",
        "trigger_conditions": ["nighttime_hatch", "dark_card_applied"],
        "base_chance":        0.10,
        "effects": {
            "stat_modifiers": {"speed": 12, "defense": -3},
            "add_traits":     ["lone_wanderer"],
            "add_ability":    "shadow_dash",
            "visual_change":  "dark_stripes",
        },
    },

    # ── Add more mutations here ────────────────
}


# ─────────────────────────────────────────────
#  TRAIT / MUTATION HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_trait(trait_id: str) -> dict:
    """Return a trait definition by ID."""
    trait = TRAITS.get(trait_id)
    if not trait:
        raise ValueError(f"Unknown trait: '{trait_id}'")
    return trait


def get_mutation(mutation_id: str) -> dict:
    """Return a mutation definition by ID."""
    mut = MUTATIONS.get(mutation_id)
    if not mut:
        raise ValueError(f"Unknown mutation: '{mutation_id}'")
    return mut


def roll_mutation(mutation_id: str, region_modifier: float, cards_applied: list) -> bool:
    """
    Roll to see if a mutation triggers.

    Args:
        mutation_id:       ID of the mutation to attempt
        region_modifier:   Float multiplier from region (e.g. 1.3 for fire in Suncrest)
        cards_applied:     List of card IDs applied to this creature/egg

    Returns:
        True if mutation fires, False otherwise.
    """
    mut = get_mutation(mutation_id)
    chance = mut["base_chance"] * region_modifier

    # Cards can further boost mutation chances
    # (Card system in cards.py adds "mutation_boost" effects)
    for card_id in cards_applied:
        # Placeholder: cards.py will implement get_card_mutation_boost()
        # For now just a pass-through
        pass

    chance = min(chance, 0.95)   # cap at 95%
    return random.random() < chance


def apply_trait_modifiers(stats: dict, trait_ids: list) -> dict:
    """
    Apply all trait stat modifiers to a stats dict.
    Returns a new dict with modifiers applied.
    """
    result = dict(stats)
    for tid in trait_ids:
        trait = TRAITS.get(tid)
        if not trait:
            continue
        for stat, delta in trait["stat_modifiers"].items():
            if stat == "all_stats":
                for key in result:
                    result[key] = result.get(key, 0) + delta
            else:
                result[stat] = result.get(stat, 0) + delta
    return result


def check_mutation_conditions(mutation_id: str, context: dict) -> bool:
    """
    Check whether ALL trigger conditions for a mutation are satisfied.

    context dict keys (all optional, default False/None):
      - region_id         : str
      - trait_ids         : list of current trait IDs
      - cards_applied     : list of card IDs
      - is_nighttime      : bool
    """
    mut = get_mutation(mutation_id)
    conditions = mut["trigger_conditions"]
    region_id     = context.get("region_id", "")
    trait_ids     = context.get("trait_ids", [])
    cards_applied = context.get("cards_applied", [])
    is_nighttime  = context.get("is_nighttime", False)

    for cond in conditions:
        if cond.startswith("region_"):
            # e.g. "region_suncrest_expanse"
            required_region = cond[len("region_"):]
            if region_id != required_region:
                return False
        elif cond.startswith("has_"):
            required_trait = cond[len("has_"):]
            if required_trait not in trait_ids:
                return False
        elif cond.endswith("_card_applied"):
            required_card_type = cond[: -len("_card_applied")]
            # Check if any applied card matches this type
            if not any(required_card_type in c for c in cards_applied):
                return False
        elif cond == "nighttime_hatch":
            if not is_nighttime:
                return False
        # Add more condition parsers here as needed

    return True
