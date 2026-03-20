"""
regions.py — WORLDHATCH Region System
══════════════════════════════════════
10 regions, each with full spawn tables for all 10 creatures.
Spawn weights: Common=40, Uncommon=20, Rare=8, Legendary=2
"""

REGIONS = {

    "suncrest_expanse": {
        "display_name":    "Suncrest Expanse",
        "real_world_ref":  "United States West Coast",
        "biome":           "arid_coastal",
        "element":         "fire",
        "climate":         "warm_dry",
        "home_bonus":      {"hp": 10, "attack": 5, "speed": 3},
        "mutation_modifier": {"fire": 1.3, "magma": 1.2, "water": 0.7, "ice": 0.5},
        "spawn_table": {
            "emberback_rumbler": 40, "dustfin_drifter": 40,
            "tidewatcher": 40,       "fogcrawler": 40,
            "cinderclaw": 20,        "stormhawk": 20,
            "redshard_gecko": 20,    "sunshell_crawler": 8,
            "darkwood_stalker": 8,   "solarcrown_wyrm": 2,
        },
        "egg_hatch_time_seconds": 30,
    },

    "sakurami_highlands": {
        "display_name":    "Sakurami Highlands",
        "real_world_ref":  "Japan",
        "biome":           "temperate_forest",
        "element":         "spirit",
        "climate":         "temperate",
        "home_bonus":      {"hp": 8, "attack": 3, "speed": 8},
        "mutation_modifier": {"spirit": 1.4, "nature": 1.2, "crystal": 1.1, "fire": 0.8},
        "spawn_table": {
            "misthare": 40,              "blossomwing": 40,
            "bambooshell_tortoise": 40,  "tidepulse_jellyfish": 40,
            "inkfox": 20,                "stonepetal_wyrm": 20,
            "thunderkoi": 20,            "ashveil_crane": 8,
            "frostpetal_oni": 8,         "ryujin_serpent": 2,
        },
        "egg_hatch_time_seconds": 25,
    },

    "verdeluna_jungle": {
        "display_name":    "Verdeluna Jungle",
        "real_world_ref":  "Brazil / Amazon Basin",
        "biome":           "tropical_rainforest",
        "element":         "nature",
        "climate":         "hot_humid",
        "home_bonus":      {"hp": 15, "attack": 8, "speed": 2},
        "mutation_modifier": {"nature": 1.5, "water": 1.2, "dark": 1.1, "fire": 0.5},
        "spawn_table": {
            "thornback_brute": 40,   "mosswhisper": 40,
            "rivercoil_serpent": 40, "canopy_glider": 40,
            "venomcap_toad": 20,     "ruinglow_beetle": 20,
            "ashvine_creeper": 20,   "luminleaf_sprite": 8,
            "magmagrub": 8,          "verdant_colossus": 2,
        },
        "egg_hatch_time_seconds": 45,
    },

    "frostspire_reach": {
        "display_name":    "Frostspire Reach",
        "real_world_ref":  "Norway / Scandinavia",
        "biome":           "arctic_mountain",
        "element":         "ice",
        "climate":         "cold",
        "home_bonus":      {"hp": 12, "attack": 7, "speed": 5},
        "mutation_modifier": {"ice": 1.5, "storm": 1.2, "spirit": 1.1, "fire": 0.4},
        "spawn_table": {
            "glacierfang": 40,      "rimewolve": 40,
            "aurorawing": 40,       "fjordpup": 40,
            "coldcrest_raptor": 20, "stormtusk_boar": 20,
            "cavern_darkbear": 20,  "avalanche_golem": 8,
            "runefire_elk": 8,      "jormunveil": 2,
        },
        "egg_hatch_time_seconds": 60,
    },

    "ashenveil_steppe": {
        "display_name":    "Ashenveil Steppe",
        "real_world_ref":  "Central Asia / Kazakh Steppe",
        "biome":           "temperate_grassland",
        "element":         "storm",
        "climate":         "continental",
        "home_bonus":      {"hp": 8, "attack": 6, "speed": 10},
        "mutation_modifier": {"storm": 1.4, "sand": 1.3, "dark": 1.1, "water": 0.6},
        "spawn_table": {
            "dustmane_runner": 40,   "ashprowl_cat": 40,
            "cragback_tortoise": 40, "embervole": 40,
            "thunderhoof_bison": 20, "crater_lurker": 20,
            "voidstep_wolf": 20,     "sandwhirl_djinn": 8,
            "icevein_stallion": 8,   "stormfather_eagle": 2,
        },
        "egg_hatch_time_seconds": 35,
    },

    "coralhaven_shoals": {
        "display_name":    "Coralhaven Shoals",
        "real_world_ref":  "Pacific Islands / Southeast Asia",
        "biome":           "tropical_ocean",
        "element":         "water",
        "climate":         "tropical",
        "home_bonus":      {"hp": 10, "attack": 4, "speed": 9},
        "mutation_modifier": {"water": 1.5, "storm": 1.2, "spirit": 1.1, "fire": 0.4},
        "spawn_table": {
            "coralback_crab": 40,     "shimmerscale_fish": 40,
            "mangrove_toad": 40,      "riftglow_eel": 40,
            "stormcaller_manta": 20,  "phantom_seahorse": 20,
            "abyssal_hunter": 20,     "tidalcrystal_turtle": 8,
            "typhoon_serpent": 8,     "leviathan_bloom": 2,
        },
        "egg_hatch_time_seconds": 40,
    },

    "dunecrown_expanse": {
        "display_name":    "Dunecrown Expanse",
        "real_world_ref":  "Sahara / Middle East",
        "biome":           "hot_desert",
        "element":         "sand",
        "climate":         "arid",
        "home_bonus":      {"hp": 9, "attack": 7, "speed": 7},
        "mutation_modifier": {"sand": 1.5, "fire": 1.2, "spirit": 1.1, "ice": 0.3},
        "spawn_table": {
            "dune_skitter": 40,       "heatpulse_scorpion": 40,
            "oasis_spirit": 40,       "stargazer_moth": 40,
            "sandvault_beetle": 20,   "miragecat": 20,
            "thunderdust_hawk": 20,   "buried_colossus": 8,
            "nightcrystal_viper": 8,  "dunecrown_sphinx": 2,
        },
        "egg_hatch_time_seconds": 50,
    },

    "emberveil_depths": {
        "display_name":    "Emberveil Depths",
        "real_world_ref":  "Iceland / Volcanic Regions",
        "biome":           "volcanic",
        "element":         "magma",
        "climate":         "extreme_heat",
        "home_bonus":      {"hp": 14, "attack": 10, "speed": 3},
        "mutation_modifier": {"magma": 1.6, "fire": 1.3, "crystal": 1.1, "ice": 0.3},
        "spawn_table": {
            "lavapup": 40,              "obsidian_crab": 40,
            "steamvent_frog": 40,       "ashdrift_bird": 40,
            "magmahorn_ram": 20,        "voidflame_salamander": 20,
            "crystalite_mole": 20,      "cinder_wyvern": 8,
            "glacial_intruder": 8,      "magma_titan": 2,
        },
        "egg_hatch_time_seconds": 70,
    },

    "shadowmere_hollows": {
        "display_name":    "Shadowmere Hollows",
        "real_world_ref":  "Eastern Europe / Carpathian Mountains",
        "biome":           "dark_forest",
        "element":         "dark",
        "climate":         "cold_damp",
        "home_bonus":      {"hp": 10, "attack": 8, "speed": 6},
        "mutation_modifier": {"dark": 1.6, "spirit": 1.2, "ice": 1.1, "fire": 0.5},
        "spawn_table": {
            "marsh_lurker": 40,    "mirecat": 40,
            "hollowbat": 40,       "moonveil_moth": 40,
            "bog_golem": 20,       "stormcrow": 20,
            "frostshade_wolf": 20, "castle_wraith": 8,
            "bloodcrystal_bat": 8, "void_sovereign": 2,
        },
        "egg_hatch_time_seconds": 55,
    },

    "crystalpeak_range": {
        "display_name":    "Crystalpeak Range",
        "real_world_ref":  "Himalayas / Tibet",
        "biome":           "high_altitude",
        "element":         "crystal",
        "climate":         "alpine",
        "home_bonus":      {"hp": 11, "attack": 6, "speed": 6},
        "mutation_modifier": {"crystal": 1.6, "ice": 1.3, "spirit": 1.2, "dark": 0.6},
        "spawn_table": {
            "peakpuff": 40,           "crystalwing_dove": 40,
            "cliff_ibex": 40,         "starbreath_yak": 40,
            "voidpeak_eagle": 20,     "thundermonk_ape": 20,
            "emberpillar": 20,        "monastery_guardian": 8,
            "water_ascendant": 8,     "peak_sovereign": 2,
        },
        "egg_hatch_time_seconds": 65,
    },
}


def get_region(region_id: str) -> dict:
    region = REGIONS.get(region_id)
    if not region:
        raise ValueError(f"Unknown region: '{region_id}'. Valid: {list(REGIONS.keys())}")
    return region

def get_spawn_table(region_id: str) -> dict:
    return get_region(region_id)["spawn_table"]

def list_regions() -> list:
    return list(REGIONS.keys())

def get_home_bonus(region_id: str) -> dict:
    return get_region(region_id)["home_bonus"]

def get_mutation_modifier(region_id: str, element: str) -> float:
    return get_region(region_id).get("mutation_modifier", {}).get(element, 1.0)
