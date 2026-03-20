"""
regions.py — WORLDHATCH Region System
══════════════════════════════════════
Each Region maps a fictional in-game name to a real-world geography.
Regions define:
  - Biome type (affects creature type affinities)
  - Spawn table (which creatures can appear here, with weights)
  - Home bonuses (stat boosts for home-region creatures)
  - Environmental modifiers (affects mutations)

TO ADD A NEW REGION:
  1. Add a new entry to REGIONS dict.
  2. Add its creature names to the spawn_table.
  3. Reference it in creature definitions (creature.py).
"""

# ─────────────────────────────────────────────
#  REGION DEFINITIONS
# ─────────────────────────────────────────────

REGIONS = {

    # ── North America ──────────────────────────────────────────
    "suncrest_expanse": {
        "display_name":    "Suncrest Expanse",
        "real_world_ref":  "United States West Coast",
        "biome":           "arid_coastal",
        "element":         "fire",           # dominant element of this region
        "climate":         "warm_dry",
        "home_bonus": {
            "hp":      10,                   # flat HP bonus for home creatures
            "attack":  5,
            "speed":   3,
        },
        "mutation_modifier": {
            "fire":    1.3,                  # 30% higher chance of fire mutations
            "water":   0.7,
        },
        # spawn_table: { creature_id: weight }  (higher = more common)
        "spawn_table": {
            "emberback_rumbler": 40,
            "dustfin_drifter":   30,
            "cinderclaw":        20,
            "sunshell_crawler":  10,
        },
        "egg_hatch_time_seconds": 30,        # demo value; scale as needed
    },

    # ── East Asia ──────────────────────────────────────────────
    "sakurami_highlands": {
        "display_name":    "Sakurami Highlands",
        "real_world_ref":  "Japan",
        "biome":           "temperate_forest",
        "element":         "spirit",
        "climate":         "temperate",
        "home_bonus": {
            "hp":      8,
            "attack":  3,
            "speed":   8,                    # fast creatures here
        },
        "mutation_modifier": {
            "spirit": 1.4,
            "nature": 1.2,
            "fire":   0.8,
        },
        "spawn_table": {
            "misthare":         35,
            "blossomwing":      35,
            "inkfox":           20,
            "stonepetal_wyrm":  10,
        },
        "egg_hatch_time_seconds": 25,
    },

    # ── South America ──────────────────────────────────────────
    "verdeluna_jungle": {
        "display_name":    "Verdeluna Jungle",
        "real_world_ref":  "Brazil / Amazon Basin",
        "biome":           "tropical_rainforest",
        "element":         "nature",
        "climate":         "hot_humid",
        "home_bonus": {
            "hp":      15,                   # tanks of the game
            "attack":  8,
            "speed":   2,
        },
        "mutation_modifier": {
            "nature":  1.5,
            "water":   1.2,
            "fire":    0.5,
        },
        "spawn_table": {
            "thornback_brute":  30,
            "mosswhisper":      30,
            "venomcap_toad":    25,
            "luminleaf_sprite": 15,
        },
        "egg_hatch_time_seconds": 45,
    },

    # ── Scandinavia ────────────────────────────────────────────
    "frostspire_reach": {
        "display_name":    "Frostspire Reach",
        "real_world_ref":  "Norway / Scandinavia",
        "biome":           "arctic_mountain",
        "element":         "ice",
        "climate":         "cold",
        "home_bonus": {
            "hp":      12,
            "attack":  7,
            "speed":   5,
        },
        "mutation_modifier": {
            "ice":     1.5,
            "storm":   1.2,
            "fire":    0.4,
        },
        "spawn_table": {
            "glacierfang":      35,
            "rimewolve":        30,
            "coldcrest_raptor": 25,
            "avalanche_golem":  10,
        },
        "egg_hatch_time_seconds": 60,
    },

    # ── Add more regions below following the same pattern ──────
    # "ashenveil_steppe":  { ... },    # Central Asia
    # "coralhaven_shoals": { ... },    # Southeast Asia / Pacific
    # "dunecrown_expanse": { ... },    # Sahara / Middle East
}


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_region(region_id: str) -> dict:
    """Return a region dict by its ID. Raises if not found."""
    region = REGIONS.get(region_id)
    if not region:
        raise ValueError(f"Unknown region: '{region_id}'. "
                         f"Valid regions: {list(REGIONS.keys())}")
    return region


def get_spawn_table(region_id: str) -> dict:
    """Return the weighted spawn table for a region."""
    return get_region(region_id)["spawn_table"]


def list_regions() -> list:
    """Return a list of all region IDs."""
    return list(REGIONS.keys())


def get_home_bonus(region_id: str) -> dict:
    """Return the stat bonus dict for creatures in their home region."""
    return get_region(region_id)["home_bonus"]


def get_mutation_modifier(region_id: str, element: str) -> float:
    """
    Return the mutation chance multiplier for a given element in a region.
    Defaults to 1.0 (no modifier) if the element isn't listed.
    """
    modifiers = get_region(region_id).get("mutation_modifier", {})
    return modifiers.get(element, 1.0)
