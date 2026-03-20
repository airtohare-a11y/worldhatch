"""
cards.py — WORLDHATCH Card System
══════════════════════════════════
Cards are genetic modifiers and ability injectors.
Players apply cards to eggs or creatures to:
  - Influence which mutations appear at hatch
  - Unlock evolution branches
  - Grant new active abilities
  - Boost specific stat lines

Card Rarities: common, uncommon, rare, legendary

Card Types:
  "gene"      → affects mutation probability and stat growth
  "ability"   → injects an active ability into the creature
  "evolution" → unlocks a specific evolution branch
  "boost"     → one-time flat stat increase

TO ADD A NEW CARD:
  Add an entry to CARDS dict. Give it a type, rarity, effects block,
  and optionally target_conditions (creature types, regions, etc.)
"""


# ─────────────────────────────────────────────
#  CARD DEFINITIONS
# ─────────────────────────────────────────────

CARDS = {

    # ══ GENE CARDS ════════════════════════════

    "ember_gene": {
        "display_name":  "Ember Gene",
        "card_type":     "gene",
        "rarity":        "common",
        "element":       "fire",
        "description":   "Infuses fire genetic markers. Boosts fire mutation chances.",
        "effects": {
            "mutation_boost":    {"inferno_crest": 0.15},   # +15% on top of base
            "stat_growth_bias":  {"fire_power": 3},          # +3 per level-up in fire_power
        },
        "target_conditions":  [],                            # no restrictions
        "consumable":         True,                          # destroyed on use
    },

    "frost_gene": {
        "display_name":  "Frost Gene",
        "card_type":     "gene",
        "rarity":        "common",
        "element":       "ice",
        "description":   "Injects cold-climate genetic code. Boosts ice mutations.",
        "effects": {
            "mutation_boost":    {"glacial_mantle": 0.12},
            "stat_growth_bias":  {"ice_power": 3},
        },
        "target_conditions":  [],
        "consumable":         True,
    },

    "verdant_gene": {
        "display_name":  "Verdant Gene",
        "card_type":     "gene",
        "rarity":        "common",
        "element":       "nature",
        "description":   "Nature strand encoding. Boosts healing mutations.",
        "effects": {
            "mutation_boost":    {"verdant_bloom": 0.18},
            "stat_growth_bias":  {"hp_regen": 2, "hp": 5},
        },
        "target_conditions":  [],
        "consumable":         True,
    },

    "shadow_gene": {
        "display_name":  "Shadow Gene",
        "card_type":     "gene",
        "rarity":        "uncommon",
        "element":       "dark",
        "description":   "Rare dark-element strand. Only activates under certain conditions.",
        "effects": {
            "mutation_boost":    {"shadow_stripe": 0.20},
            "stat_growth_bias":  {"speed": 4},
        },
        "target_conditions":  ["nighttime_only"],
        "consumable":         True,
    },

    # ══ ABILITY CARDS ═════════════════════════

    "scorchwave_card": {
        "display_name":  "Scorchwave",
        "card_type":     "ability",
        "rarity":        "uncommon",
        "element":       "fire",
        "description":   "Teaches the creature Scorchwave — a wide fire burst.",
        "effects": {
            "grant_ability": "scorchwave",
        },
        "target_conditions":  ["has_fire_affinity"],         # only fire-affinity creatures
        "consumable":         True,
    },

    "glacial_slam_card": {
        "display_name":  "Glacial Slam",
        "card_type":     "ability",
        "rarity":        "uncommon",
        "element":       "ice",
        "description":   "Teaches Glacial Slam — freezes target on impact.",
        "effects": {
            "grant_ability": "glacial_slam",
        },
        "target_conditions":  ["has_ice_affinity"],
        "consumable":         True,
    },

    "root_bind_card": {
        "display_name":  "Root Bind",
        "card_type":     "ability",
        "rarity":        "common",
        "element":       "nature",
        "description":   "Teaches Root Bind — immobilizes an opponent briefly.",
        "effects": {
            "grant_ability": "root_bind",
        },
        "target_conditions":  [],
        "consumable":         True,
    },

    # ══ EVOLUTION CARDS ═══════════════════════

    "blaze_path_card": {
        "display_name":  "Blaze Path",
        "card_type":     "evolution",
        "rarity":        "rare",
        "element":       "fire",
        "description":   "Unlocks the Blazeborn evolution branch for fire creatures.",
        "effects": {
            "unlock_evolution_branch": "blazeborn",
        },
        "target_conditions":  ["element_fire", "level_10_plus"],
        "consumable":         True,
    },

    "ancient_form_card": {
        "display_name":  "Ancient Form",
        "card_type":     "evolution",
        "rarity":        "legendary",
        "element":       "neutral",
        "description":   "Unlocks a secret ancient evolution branch. Works on any creature.",
        "effects": {
            "unlock_evolution_branch": "ancient",
        },
        "target_conditions":  ["level_15_plus"],
        "consumable":         True,
    },

    # ══ BOOST CARDS ═══════════════════════════

    "vitality_shard": {
        "display_name":  "Vitality Shard",
        "card_type":     "boost",
        "rarity":        "common",
        "element":       "neutral",
        "description":   "One-time permanent HP boost.",
        "effects": {
            "stat_boost": {"hp": 15},
        },
        "target_conditions":  [],
        "consumable":         True,
    },

    "power_fragment": {
        "display_name":  "Power Fragment",
        "card_type":     "boost",
        "rarity":        "uncommon",
        "element":       "neutral",
        "description":   "One-time permanent attack boost.",
        "effects": {
            "stat_boost": {"attack": 10},
        },
        "target_conditions":  [],
        "consumable":         True,
    },

    # ── Add more cards below ───────────────────
}


# ─────────────────────────────────────────────
#  ABILITY DEFINITIONS (referenced by cards)
#  These are the actual active moves creatures learn.
# ─────────────────────────────────────────────

ABILITIES = {
    "scorchwave": {
        "display_name": "Scorchwave",
        "element":      "fire",
        "power":        55,
        "accuracy":     0.90,
        "description":  "A wide blast of fire. May leave a burn.",
        "effect":       "burn_chance_0.25",
    },
    "glacial_slam": {
        "display_name": "Glacial Slam",
        "element":      "ice",
        "power":        60,
        "accuracy":     0.85,
        "description":  "Slams target with an ice pillar. May freeze.",
        "effect":       "freeze_chance_0.20",
    },
    "root_bind": {
        "display_name": "Root Bind",
        "element":      "nature",
        "power":        30,
        "accuracy":     0.95,
        "description":  "Roots the target in place for 1 turn.",
        "effect":       "immobilize_1_turn",
    },
    "shadow_dash": {
        "display_name": "Shadow Dash",
        "element":      "dark",
        "power":        45,
        "accuracy":     1.00,
        "description":  "Unavoidable dark-speed strike.",
        "effect":       "always_hits",
    },
    "ember_bite": {
        "display_name": "Ember Bite",
        "element":      "fire",
        "power":        40,
        "accuracy":     0.95,
        "description":  "A searing bite. Starter move for fire creatures.",
        "effect":       "burn_chance_0.15",
    },
    # Add more abilities here
}


# ─────────────────────────────────────────────
#  CARD HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_card(card_id: str) -> dict:
    """Return a card definition by ID."""
    card = CARDS.get(card_id)
    if not card:
        raise ValueError(f"Unknown card: '{card_id}'")
    return card


def get_ability(ability_id: str) -> dict:
    """Return an ability definition by ID."""
    ability = ABILITIES.get(ability_id)
    if not ability:
        raise ValueError(f"Unknown ability: '{ability_id}'")
    return ability


def check_card_target_conditions(card_id: str, creature) -> tuple[bool, str]:
    """
    Check if a card can be applied to a specific creature.

    Args:
        card_id:  ID of the card to check
        creature: Creature instance (from creature.py)

    Returns:
        (True, "") if valid, or (False, reason_string) if invalid
    """
    card = get_card(card_id)
    conditions = card.get("target_conditions", [])

    for cond in conditions:
        if cond == "has_fire_affinity":
            if "fire_affinity" not in creature.special_flags:
                return False, "Creature needs fire affinity."
        elif cond == "has_ice_affinity":
            if "ice_affinity" not in creature.special_flags:
                return False, "Creature needs ice affinity."
        elif cond.startswith("element_"):
            required_elem = cond[len("element_"):]
            if creature.element != required_elem:
                return False, f"Creature must be {required_elem} type."
        elif cond.startswith("level_") and cond.endswith("_plus"):
            required_level = int(cond[len("level_"):-len("_plus")])
            if creature.level < required_level:
                return False, f"Creature must be level {required_level}+."
        elif cond == "nighttime_only":
            # Game session would pass time context; placeholder here
            pass

    return True, ""


def apply_card_to_creature(card_id: str, creature) -> dict:
    """
    Apply a card's effects to a creature.
    Returns a result dict: { "success": bool, "message": str, "changes": dict }
    Mutates the creature object in place.
    """
    valid, reason = check_card_target_conditions(card_id, creature)
    if not valid:
        return {"success": False, "message": reason, "changes": {}}

    card    = get_card(card_id)
    effects = card["effects"]
    changes = {}

    # ── Gene: mutation boost ──────────────────
    if "mutation_boost" in effects:
        for mut_id, boost in effects["mutation_boost"].items():
            creature.mutation_boosts[mut_id] = (
                creature.mutation_boosts.get(mut_id, 0) + boost
            )
        changes["mutation_boosts_added"] = effects["mutation_boost"]

    # ── Gene: stat growth bias ────────────────
    if "stat_growth_bias" in effects:
        for stat, val in effects["stat_growth_bias"].items():
            creature.stat_growth_bias[stat] = (
                creature.stat_growth_bias.get(stat, 0) + val
            )
        changes["stat_growth_biases_added"] = effects["stat_growth_bias"]

    # ── Ability: grant ability ────────────────
    if "grant_ability" in effects:
        ability_id = effects["grant_ability"]
        if ability_id not in creature.abilities:
            creature.abilities.append(ability_id)
            changes["ability_granted"] = ability_id

    # ── Evolution: unlock branch ──────────────
    if "unlock_evolution_branch" in effects:
        branch = effects["unlock_evolution_branch"]
        if branch not in creature.unlocked_evolutions:
            creature.unlocked_evolutions.append(branch)
            changes["evolution_unlocked"] = branch

    # ── Boost: flat stat boost ────────────────
    if "stat_boost" in effects:
        for stat, val in effects["stat_boost"].items():
            creature.stats[stat] = creature.stats.get(stat, 0) + val
        changes["stats_boosted"] = effects["stat_boost"]

    # Mark card as applied
    creature.cards_applied.append(card_id)

    msg = f"Card '{card['display_name']}' applied to {creature.name}."
    return {"success": True, "message": msg, "changes": changes}
