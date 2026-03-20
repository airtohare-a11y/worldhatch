
"""
creature.py — WORLDHATCH Creature & Egg Classes
════════════════════════════════════════════════
Core classes:
  Egg      → unhatched creature; holds applied cards and region origin
  Creature → fully realized creature with stats, traits, abilities

Creature Registry (CREATURE_REGISTRY):
  - Static data for each creature species (base stats, evolution paths, etc.)
  - Add new creatures here without touching class logic

TO ADD A NEW CREATURE SPECIES:
  Add an entry to CREATURE_REGISTRY. Define base_stats, evolution_paths,
  learnable_abilities, and which region it's native to.
"""

import uuid
import random
from traits   import (apply_trait_modifiers, check_mutation_conditions,
                       roll_mutation, MUTATIONS)
from regions  import get_home_bonus, get_mutation_modifier


# ─────────────────────────────────────────────
#  CREATURE SPECIES REGISTRY
#  This is the master list of all species.
#  Instances (Creature objects) are created FROM these templates.
# ─────────────────────────────────────────────

CREATURE_REGISTRY = {

    # ══ Suncrest Expanse (Fire) ═══════════════

    "emberback_rumbler": {
        "display_name":    "Emberback Rumbler",
        "home_region":     "suncrest_expanse",
        "element":         "fire",
        "rarity":          "common",
        "description":     (
            "A stocky, ember-spined creature that roams sun-scorched ridgelines. "
            "Its back glows when agitated."
        ),
        "base_stats": {
            "hp":         80,
            "attack":     18,
            "defense":    12,
            "speed":      10,
            "fire_power": 15,
            "ice_power":   0,
        },
        "base_traits":          ["tough_hide", "ember_core"],
        "starter_abilities":    ["ember_bite"],
        "learnable_abilities":  ["scorchwave", "root_bind"],
        "evolution_paths": {
            # branch_name: { to_species, min_level, conditions }
            "default":   {"to": "magmaback_colossus",  "min_level": 10, "conditions": []},
            "blazeborn": {"to": "blazehorn_ravager",   "min_level": 10,
                          "conditions": ["blaze_path_card"]},
            "ancient":   {"to": "primordial_cinder",   "min_level": 15,
                          "conditions": ["ancient_form_card"]},
        },
        "possible_mutations":   ["inferno_crest", "shadow_stripe"],
        "base_hatch_time":      30,
    },

    "dustfin_drifter": {
        "display_name":    "Dustfin Drifter",
        "home_region":     "suncrest_expanse",
        "element":         "fire",
        "rarity":          "common",
        "description":     "A slender gliding creature that rides thermals above canyon walls.",
        "base_stats": {
            "hp":       60, "attack": 14, "defense": 8,
            "speed":    20, "fire_power": 10, "ice_power": 0,
        },
        "base_traits":         ["hollow_bones"],
        "starter_abilities":   ["ember_bite"],
        "learnable_abilities": ["shadow_dash"],
        "evolution_paths": {
            "default": {"to": "cindersoar_titan", "min_level": 10, "conditions": []},
        },
        "possible_mutations":  ["shadow_stripe"],
        "base_hatch_time":     20,
    },

    # ══ Frostspire Reach (Ice) ════════════════

    "glacierfang": {
        "display_name":    "Glacierfang",
        "home_region":     "frostspire_reach",
        "element":         "ice",
        "rarity":          "common",
        "description":     "A fierce predator with crystalline fangs formed from permafrost.",
        "base_stats": {
            "hp":       90, "attack": 22, "defense": 15,
            "speed":    8,  "fire_power": 0, "ice_power": 18,
        },
        "base_traits":         ["iron_jaw", "frost_veins"],
        "starter_abilities":   ["glacial_slam"],
        "learnable_abilities": ["root_bind"],
        "evolution_paths": {
            "default": {"to": "blizzardwraith",  "min_level": 10, "conditions": []},
            "ancient": {"to": "glacier_ancient", "min_level": 15,
                        "conditions": ["ancient_form_card"]},
        },
        "possible_mutations":  ["glacial_mantle", "shadow_stripe"],
        "base_hatch_time":     60,
    },

    # ══ Verdeluna Jungle (Nature) ══════════════

    "thornback_brute": {
        "display_name":    "Thornback Brute",
        "home_region":     "verdeluna_jungle",
        "element":         "nature",
        "rarity":          "common",
        "description":     "A massive armored creature covered in venomous thorns.",
        "base_stats": {
            "hp":       120, "attack": 20, "defense": 20,
            "speed":    4,   "fire_power": 0, "ice_power": 0,
        },
        "base_traits":         ["tough_hide", "verdant_soul"],
        "starter_abilities":   ["root_bind"],
        "learnable_abilities": ["scorchwave"],
        "evolution_paths": {
            "default": {"to": "colossalvine_lord", "min_level": 12, "conditions": []},
        },
        "possible_mutations":  ["verdant_bloom"],
        "base_hatch_time":     45,
    },

    # ══ Sakurami Highlands (Spirit) ════════════

    "misthare": {
        "display_name":    "Misthare",
        "home_region":     "sakurami_highlands",
        "element":         "spirit",
        "rarity":          "common",
        "description":     "A nimble spirit-rabbit that phases briefly through solid objects.",
        "base_stats": {
            "hp":       55, "attack": 12, "defense": 6,
            "speed":    25, "fire_power": 0, "ice_power": 0,
        },
        "base_traits":         ["hollow_bones", "lone_wanderer"],
        "starter_abilities":   ["shadow_dash"],
        "learnable_abilities": ["root_bind"],
        "evolution_paths": {
            "default": {"to": "spectralform_hare", "min_level": 8, "conditions": []},
        },
        "possible_mutations":  ["shadow_stripe"],
        "base_hatch_time":     25,
    },

    # ══ Suncrest Expanse — Additional Species ════

    "cinderclaw": {
        "display_name":    "Cinderclaw",
        "home_region":     "suncrest_expanse",
        "element":         "fire",
        "rarity":          "uncommon",
        "description":     (
            "A quick-footed predator with superheated claws that leave scorch marks "
            "on everything it touches. Hunts at dusk when the canyon rocks radiate heat."
        ),
        "base_stats": {
            "hp":         70,
            "attack":     24,
            "defense":    8,
            "speed":      18,
            "fire_power": 20,
            "ice_power":  0,
        },
        "base_traits":         ["iron_jaw", "ember_core"],
        "starter_abilities":   ["ember_bite"],
        "learnable_abilities": ["scorchwave", "shadow_dash"],
        "evolution_paths": {
            "default":   {"to": "infernoclaw_apex",  "min_level": 11, "conditions": []},
            "blazeborn": {"to": "blazehorn_ravager",  "min_level": 11,
                          "conditions": ["blaze_path_card"]},
        },
        "possible_mutations":  ["inferno_crest", "shadow_stripe"],
        "base_hatch_time":     35,
    },

    "sunshell_crawler": {
        "display_name":    "Sunshell Crawler",
        "home_region":     "suncrest_expanse",
        "element":         "fire",
        "rarity":          "rare",
        "description":     (
            "A slow-moving creature encased in a brilliant golden shell that absorbs "
            "sunlight and converts it into defensive energy. Nearly impossible to crack."
        ),
        "base_stats": {
            "hp":         110,
            "attack":     10,
            "defense":    30,
            "speed":      4,
            "fire_power": 12,
            "ice_power":  0,
        },
        "base_traits":         ["tough_hide", "ember_core", "territorial"],
        "starter_abilities":   ["root_bind"],
        "learnable_abilities": ["scorchwave", "glacial_slam"],
        "evolution_paths": {
            "default": {"to": "solarvault_titan", "min_level": 14, "conditions": []},
            "ancient": {"to": "primordial_cinder", "min_level": 15,
                        "conditions": ["ancient_form_card"]},
        },
        "possible_mutations":  ["inferno_crest", "verdant_bloom"],
        "base_hatch_time":     50,
    },

    # ══ Frostspire Reach — Additional Species ════

    "rimewolve": {
        "display_name":    "Rimewolve",
        "home_region":     "frostspire_reach",
        "element":         "ice",
        "rarity":          "common",
        "description":     (
            "A pack predator with frost-laced fur that blends into blizzard conditions. "
            "Hunts in coordinated groups and shares body heat during arctic storms."
        ),
        "base_stats": {
            "hp":         75,
            "attack":     20,
            "defense":    10,
            "speed":      18,
            "fire_power": 0,
            "ice_power":  14,
        },
        "base_traits":         ["pack_instinct", "frost_veins"],
        "starter_abilities":   ["glacial_slam"],
        "learnable_abilities": ["root_bind", "shadow_dash"],
        "evolution_paths": {
            "default": {"to": "glacierwarden_alpha", "min_level": 10, "conditions": []},
        },
        "possible_mutations":  ["glacial_mantle", "shadow_stripe"],
        "base_hatch_time":     40,
    },

    "coldcrest_raptor": {
        "display_name":    "Coldcrest Raptor",
        "home_region":     "frostspire_reach",
        "element":         "ice",
        "rarity":          "uncommon",
        "description":     (
            "A swift aerial hunter with ice-crystal feathers sharp enough to shear rock. "
            "Dives from mountain peaks at terrifying speed."
        ),
        "base_stats": {
            "hp":         65,
            "attack":     26,
            "defense":    8,
            "speed":      24,
            "fire_power": 0,
            "ice_power":  16,
        },
        "base_traits":         ["hollow_bones", "frost_veins"],
        "starter_abilities":   ["glacial_slam"],
        "learnable_abilities": ["shadow_dash", "scorchwave"],
        "evolution_paths": {
            "default": {"to": "stormspire_falcon", "min_level": 10, "conditions": []},
            "ancient": {"to": "glacier_ancient",   "min_level": 15,
                        "conditions": ["ancient_form_card"]},
        },
        "possible_mutations":  ["glacial_mantle", "shadow_stripe"],
        "base_hatch_time":     45,
    },

    "avalanche_golem": {
        "display_name":    "Avalanche Golem",
        "home_region":     "frostspire_reach",
        "element":         "ice",
        "rarity":          "rare",
        "description":     (
            "An ancient construct of compacted glacier ice and mountain stone. "
            "Dormant for centuries until disturbed — then unstoppable."
        ),
        "base_stats": {
            "hp":         150,
            "attack":     28,
            "defense":    35,
            "speed":      3,
            "fire_power": 0,
            "ice_power":  22,
        },
        "base_traits":         ["tough_hide", "frost_veins", "territorial"],
        "starter_abilities":   ["glacial_slam", "root_bind"],
        "learnable_abilities": ["scorchwave"],
        "evolution_paths": {
            "default": {"to": "permafrost_colossus", "min_level": 15, "conditions": []},
        },
        "possible_mutations":  ["glacial_mantle"],
        "base_hatch_time":     90,
    },

    # ══ Verdeluna Jungle — Additional Species ════

    "mosswhisper": {
        "display_name":    "Mosswhisper",
        "home_region":     "verdeluna_jungle",
        "element":         "nature",
        "rarity":          "common",
        "description":     (
            "A small, elusive creature entirely covered in living moss. "
            "Nearly invisible on the jungle floor — you hear it before you see it."
        ),
        "base_stats": {
            "hp":         65,
            "attack":     12,
            "defense":    14,
            "speed":      16,
            "fire_power": 0,
            "ice_power":  0,
        },
        "base_traits":         ["verdant_soul", "lone_wanderer"],
        "starter_abilities":   ["root_bind"],
        "learnable_abilities": ["shadow_dash"],
        "evolution_paths": {
            "default": {"to": "canopyveil_stalker", "min_level": 9, "conditions": []},
        },
        "possible_mutations":  ["verdant_bloom", "shadow_stripe"],
        "base_hatch_time":     30,
    },

    "venomcap_toad": {
        "display_name":    "Venomcap Toad",
        "home_region":     "verdeluna_jungle",
        "element":         "nature",
        "rarity":          "uncommon",
        "description":     (
            "A bloated, brightly colored toad with toxic mushroom caps growing from "
            "its back. The caps release paralytic spores when threatened."
        ),
        "base_stats": {
            "hp":         95,
            "attack":     16,
            "defense":    18,
            "speed":      6,
            "fire_power": 0,
            "ice_power":  0,
        },
        "base_traits":         ["tough_hide", "verdant_soul"],
        "starter_abilities":   ["root_bind"],
        "learnable_abilities": ["glacial_slam"],
        "evolution_paths": {
            "default": {"to": "plague_toad_sovereign", "min_level": 12, "conditions": []},
        },
        "possible_mutations":  ["verdant_bloom", "shadow_stripe"],
        "base_hatch_time":     50,
    },

    "luminleaf_sprite": {
        "display_name":    "Luminleaf Sprite",
        "home_region":     "verdeluna_jungle",
        "element":         "nature",
        "rarity":          "rare",
        "description":     (
            "A delicate, bioluminescent creature whose leaf-like wings glow at night. "
            "Said to appear only when the jungle is in perfect ecological balance."
        ),
        "base_stats": {
            "hp":         50,
            "attack":     10,
            "defense":    8,
            "speed":      28,
            "fire_power": 0,
            "ice_power":  0,
        },
        "base_traits":         ["hollow_bones", "verdant_soul", "worldborn"],
        "starter_abilities":   ["root_bind", "shadow_dash"],
        "learnable_abilities": ["scorchwave"],
        "evolution_paths": {
            "default": {"to": "eternal_luminwing",  "min_level": 10, "conditions": []},
            "ancient": {"to": "primordial_cinder",  "min_level": 15,
                        "conditions": ["ancient_form_card"]},
        },
        "possible_mutations":  ["verdant_bloom", "shadow_stripe"],
        "base_hatch_time":     60,
    },

    # ══ Sakurami Highlands — Additional Species ══

    "blossomwing": {
        "display_name":    "Blossomwing",
        "home_region":     "sakurami_highlands",
        "element":         "spirit",
        "rarity":          "common",
        "description":     (
            "A graceful winged creature with petals woven into its feathers. "
            "Migrates with the cherry blossom season and leaves flower trails in its wake."
        ),
        "base_stats": {
            "hp":         58,
            "attack":     13,
            "defense":    9,
            "speed":      22,
            "fire_power": 0,
            "ice_power":  0,
        },
        "base_traits":         ["hollow_bones", "pack_instinct"],
        "starter_abilities":   ["root_bind"],
        "learnable_abilities": ["shadow_dash", "scorchwave"],
        "evolution_paths": {
            "default": {"to": "sakura_herald", "min_level": 9, "conditions": []},
        },
        "possible_mutations":  ["verdant_bloom", "shadow_stripe"],
        "base_hatch_time":     25,
    },

    "inkfox": {
        "display_name":    "Inkfox",
        "home_region":     "sakurami_highlands",
        "element":         "spirit",
        "rarity":          "uncommon",
        "description":     (
            "A fox-like creature whose fur shifts between deep black and shimmering silver. "
            "Leaves ink-like footprints that vanish after a few seconds."
        ),
        "base_stats": {
            "hp":         62,
            "attack":     18,
            "defense":    10,
            "speed":      24,
            "fire_power": 0,
            "ice_power":  0,
        },
        "base_traits":         ["lone_wanderer", "mimic_scale"],
        "starter_abilities":   ["shadow_dash"],
        "learnable_abilities": ["root_bind", "glacial_slam"],
        "evolution_paths": {
            "default": {"to": "voidpelt_phantom", "min_level": 10, "conditions": []},
            "ancient": {"to": "glacier_ancient",  "min_level": 15,
                        "conditions": ["ancient_form_card"]},
        },
        "possible_mutations":  ["shadow_stripe"],
        "base_hatch_time":     35,
    },

    "stonepetal_wyrm": {
        "display_name":    "Stonepetal Wyrm",
        "home_region":     "sakurami_highlands",
        "element":         "spirit",
        "rarity":          "rare",
        "description":     (
            "A long serpentine creature with stone-hard scales etched with floral patterns. "
            "Ancient Sakurami legends say it guards mountain shrines for centuries."
        ),
        "base_stats": {
            "hp":         105,
            "attack":     22,
            "defense":    25,
            "speed":      10,
            "fire_power": 0,
            "ice_power":  0,
        },
        "base_traits":         ["tough_hide", "territorial", "verdant_soul"],
        "starter_abilities":   ["root_bind", "glacial_slam"],
        "learnable_abilities": ["scorchwave"],
        "evolution_paths": {
            "default": {"to": "jade_serpent_ancient", "min_level": 14, "conditions": []},
            "ancient": {"to": "primordial_cinder",    "min_level": 15,
                        "conditions": ["ancient_form_card"]},
        },
        "possible_mutations":  ["verdant_bloom", "glacial_mantle"],
        "base_hatch_time":     70,
    },

    # ── Add more species here ──────────────────
    # Pattern: copy a block above and change the values.
    # The class logic never needs to change.
}


# ─────────────────────────────────────────────
#  EGG CLASS
# ─────────────────────────────────────────────

class Egg:
    """
    An unhatched creature.
    Eggs are tied to a region and species.
    Players can apply cards before hatching to influence mutations.
    """

    def __init__(self, species_id: str, region_id: str, owner_id: str = None):
        if species_id not in CREATURE_REGISTRY:
            raise ValueError(f"Unknown species: '{species_id}'")

        self.egg_id       = str(uuid.uuid4())[:8]
        self.species_id   = species_id
        self.region_id    = region_id              # where this egg was found
        self.owner_id     = owner_id
        self.cards_applied = []                    # card IDs applied before hatch
        self.is_hatched   = False

        species = CREATURE_REGISTRY[species_id]
        self.hatch_time   = species["base_hatch_time"]
        self.display_name = f"{species['display_name']} Egg"

    def apply_card(self, card_id: str) -> bool:
        """
        Stage a card to be applied at hatch time.
        Returns True if successfully queued.
        """
        if self.is_hatched:
            print("Egg already hatched — cannot apply cards.")
            return False
        self.cards_applied.append(card_id)
        print(f"Card '{card_id}' staged on egg {self.egg_id}.")
        return True

    def hatch(self, context: dict = None) -> "Creature":
        """
        Hatch the egg into a Creature.
        Applies staged cards and rolls mutations.

        context dict (optional, for mutation rolls):
          - is_nighttime: bool
        """
        if self.is_hatched:
            raise RuntimeError("Egg already hatched.")

        context = context or {}
        context["region_id"] = self.region_id

        # Build the creature
        creature = Creature(
            species_id  = self.species_id,
            region_id   = self.region_id,
            owner_id    = self.owner_id,
        )

        # Apply any staged cards
        from cards import apply_card_to_creature
        for card_id in self.cards_applied:
            result = apply_card_to_creature(card_id, creature)
            print(f"  [Card] {result['message']}")

        # Roll mutations
        creature._resolve_hatch_mutations(context)

        self.is_hatched = True
        print(f"\n🥚 Hatched! → {creature.display_name} [{creature.creature_id}]")
        return creature

    def __repr__(self):
        return (f"<Egg '{self.display_name}' | region={self.region_id} "
                f"| cards={self.cards_applied} | hatched={self.is_hatched}>")


# ─────────────────────────────────────────────
#  CREATURE CLASS
# ─────────────────────────────────────────────

class Creature:
    """
    A fully hatched creature with stats, traits, abilities, and mutation history.
    All species data comes from CREATURE_REGISTRY — the class itself is generic.
    """

    def __init__(self, species_id: str, region_id: str, owner_id: str = None):
        if species_id not in CREATURE_REGISTRY:
            raise ValueError(f"Unknown species: '{species_id}'")

        template = CREATURE_REGISTRY[species_id]

        # Identity
        self.creature_id   = str(uuid.uuid4())[:8]
        self.species_id    = species_id
        self.display_name  = template["display_name"]
        self.element       = template["element"]
        self.rarity        = template["rarity"]
        self.home_region   = template["home_region"]
        self.current_region = region_id
        self.owner_id      = owner_id

        # Progression
        self.level          = 1
        self.xp             = 0
        self.xp_to_next     = 100

        # Stats — copied from template base
        self.stats = dict(template["base_stats"])

        # Apply home region bonus if hatched in home region
        if region_id == self.home_region:
            bonus = get_home_bonus(region_id)
            for stat, val in bonus.items():
                self.stats[stat] = self.stats.get(stat, 0) + val

        # Traits — start with template base traits
        self.trait_ids = list(template["base_traits"])

        # Apply trait stat modifiers
        self.stats = apply_trait_modifiers(self.stats, self.trait_ids)

        # Derived special_flags (collected from all traits)
        self.special_flags = self._collect_special_flags()

        # Abilities
        self.abilities           = list(template["starter_abilities"])
        self.learnable_abilities = list(template["learnable_abilities"])

        # Evolution
        self.evolution_paths      = template["evolution_paths"]
        self.unlocked_evolutions  = []
        self.has_evolved          = False

        # Mutation & card tracking
        self.mutations_acquired   = []
        self.cards_applied        = []
        self.mutation_boosts      = {}      # { mutation_id: extra_chance }
        self.stat_growth_bias     = {}      # { stat: bonus_per_level }

        # Battle state (reset each fight)
        self.current_hp = self.stats["hp"]
        self.status     = None             # "burned", "frozen", etc.

        # Name — players can rename creatures
        self.name = self.display_name

    # ── Mutation Resolution ────────────────────

    def _resolve_hatch_mutations(self, context: dict):
        """Called during Egg.hatch(). Rolls all possible mutations."""
        template   = CREATURE_REGISTRY[self.species_id]
        region_id  = context.get("region_id", self.home_region)

        for mut_id in template["possible_mutations"]:
            # Check contextual conditions first
            context["trait_ids"]    = self.trait_ids
            context["cards_applied"] = self.cards_applied
            if not check_mutation_conditions(mut_id, context):
                continue

            # Get region element modifier
            mut_element = MUTATIONS[mut_id]["element"]
            region_mod  = get_mutation_modifier(region_id, mut_element)

            # Add any card-staged boosts
            extra_boost = self.mutation_boosts.get(mut_id, 0.0)
            total_mod   = region_mod + extra_boost  # additive bonus on top of base

            if roll_mutation(mut_id, total_mod, self.cards_applied):
                self._apply_mutation(mut_id)

    def _apply_mutation(self, mutation_id: str):
        """Apply a mutation's effects to this creature."""
        from traits import get_mutation
        mut     = get_mutation(mutation_id)
        effects = mut["effects"]

        # Stat modifiers
        for stat, delta in effects.get("stat_modifiers", {}).items():
            self.stats[stat] = self.stats.get(stat, 0) + delta

        # New traits
        for trait_id in effects.get("add_traits", []):
            if trait_id not in self.trait_ids:
                self.trait_ids.append(trait_id)

        # New ability
        if "add_ability" in effects:
            ability_id = effects["add_ability"]
            if ability_id not in self.abilities:
                self.abilities.append(ability_id)

        self.mutations_acquired.append(mutation_id)
        self.special_flags = self._collect_special_flags()
        print(f"  ✨ Mutation acquired: {mut['display_name']}!")

    # ── Trait Helpers ──────────────────────────

    def _collect_special_flags(self) -> list:
        """Rebuild the flat list of special_flags from all current traits."""
        from traits import TRAITS
        flags = []
        for tid in self.trait_ids:
            trait = TRAITS.get(tid, {})
            flags.extend(trait.get("special_flags", []))
        return list(set(flags))

    # ── Leveling ───────────────────────────────

    def gain_xp(self, amount: int):
        """Award XP and handle level-ups."""
        self.xp += amount
        while self.xp >= self.xp_to_next:
            self.xp        -= self.xp_to_next
            self.xp_to_next = int(self.xp_to_next * 1.4)
            self._level_up()

    def _level_up(self):
        """Apply level-up stat increases."""
        self.level += 1
        # Base growth
        self.stats["hp"]     += random.randint(3, 6)
        self.stats["attack"] += random.randint(1, 3)
        self.stats["defense"] += random.randint(1, 2)
        self.stats["speed"]   += random.randint(0, 2)

        # Bias from cards
        for stat, bias in self.stat_growth_bias.items():
            self.stats[stat] = self.stats.get(stat, 0) + bias

        self.current_hp = self.stats["hp"]   # full heal on level-up
        print(f"  ⬆ {self.name} reached level {self.level}!")

    # ── Evolution ─────────────────────────────

    def can_evolve(self, branch: str = "default") -> tuple[bool, str]:
        """Check if this creature meets evolution requirements for a branch."""
        path = self.evolution_paths.get(branch)
        if not path:
            return False, f"No evolution branch '{branch}' for this species."
        if self.level < path["min_level"]:
            return False, f"Need level {path['min_level']} (currently {self.level})."
        for cond in path.get("conditions", []):
            if cond.endswith("_card") and cond not in self.cards_applied:
                if branch not in self.unlocked_evolutions:
                    return False, f"Requires card: '{cond}'."
        return True, ""

    def evolve(self, branch: str = "default") -> bool:
        """
        Evolve into the next form along the given branch.
        Returns True if successful.
        """
        ok, reason = self.can_evolve(branch)
        if not ok:
            print(f"Cannot evolve: {reason}")
            return False

        path           = self.evolution_paths[branch]
        new_species_id = path["to"]

        if new_species_id not in CREATURE_REGISTRY:
            print(f"Evolution target '{new_species_id}' not yet implemented.")
            return False

        new_template   = CREATURE_REGISTRY[new_species_id]
        old_name       = self.name

        # Update species identity
        self.species_id    = new_species_id
        self.display_name  = new_template["display_name"]
        self.name          = new_template["display_name"]
        self.element       = new_template["element"]
        self.rarity        = new_template["rarity"]
        self.home_region   = new_template["home_region"]
        self.evolution_paths = new_template["evolution_paths"]

        # Merge in new base stats (take the higher of each)
        for stat, val in new_template["base_stats"].items():
            self.stats[stat] = max(self.stats.get(stat, 0), val)

        # Add new learnable abilities
        for ab in new_template["learnable_abilities"]:
            if ab not in self.learnable_abilities:
                self.learnable_abilities.append(ab)

        self.has_evolved = True
        self.current_hp  = self.stats["hp"]

        print(f"  🌟 {old_name} evolved into {self.name}!")
        return True

    # ── Display ────────────────────────────────

    def summary(self) -> str:
        lines = [
            f"╔══════════════════════════════════╗",
            f"  {self.name}  [{self.creature_id}]",
            f"  Species : {self.display_name}",
            f"  Element : {self.element.upper()}",
            f"  Region  : {self.current_region}  (Home: {self.home_region})",
            f"  Level   : {self.level}  (XP: {self.xp}/{self.xp_to_next})",
            f"  ── Stats ──────────────────────",
        ]
        for stat, val in self.stats.items():
            lines.append(f"    {stat:<14}: {val}")
        lines.append(f"  ── Traits ─────────────────────")
        lines.append(f"    {', '.join(self.trait_ids) or 'none'}")
        lines.append(f"  ── Mutations ──────────────────")
        lines.append(f"    {', '.join(self.mutations_acquired) or 'none'}")
        lines.append(f"  ── Abilities ──────────────────")
        lines.append(f"    {', '.join(self.abilities) or 'none'}")
        lines.append(f"  ── Evolution Paths ────────────")
        for branch, path in self.evolution_paths.items():
            lines.append(f"    [{branch}] → {path['to']} (lv{path['min_level']})")
        lines.append(f"╚══════════════════════════════════╝")
        return "\n".join(lines)

    def __repr__(self):
        return (f"<Creature '{self.name}' | {self.species_id} | "
                f"lv{self.level} | {self.element} | owner={self.owner_id}>")


# ─────────────────────────────────────────────
#  SPAWN HELPER
# ─────────────────────────────────────────────

def spawn_egg(region_id: str, owner_id: str = None) -> Egg:
    """
    Randomly spawn an egg appropriate for the given region,
    using the region's weighted spawn table.
    """
    from regions import get_spawn_table
    spawn_table = get_spawn_table(region_id)

    species_ids = list(spawn_table.keys())
    weights     = list(spawn_table.values())
    species_id  = random.choices(species_ids, weights=weights, k=1)[0]

    egg = Egg(species_id=species_id, region_id=region_id, owner_id=owner_id)
    print(f"🥚 An egg appeared in {region_id}! [{egg.display_name}]")
    return egg
