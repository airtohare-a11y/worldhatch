"""
battle.py — WORLDHATCH Battle System
══════════════════════════════════════════════════════════════
Full turn-based battle engine with D20 RNG for all outcomes.

CIRCLE OF LIFE element system:
  Fire → Nature → Ice → Storm → Spirit → Dark → Fire
  (each beats the next, weak against the previous)

D20 ROLL OUTCOMES:
  1        = Critical Fail  (miss, lose energy)
  2-5      = Weak Hit       (25% power, low energy gain)
  6-10     = Normal Hit     (75% power, normal energy)
  11-15    = Strong Hit     (100% power, good energy)
  16-19    = Heavy Hit      (125% power, high energy)
  20       = Critical Hit   (200% power, full energy burst)

ENERGY BAR:
  - Fills on successful hits, counters, and high rolls
  - Drains on misses and critical fails
  - When full (100): Special Move becomes available
  - Special Move resets bar to 0

COUNTER SYSTEM:
  - Certain abilities unlock counter options
  - Counter roll beats opponent roll = bonus damage + energy
  - Counter roll fails = take extra damage

CROSS-TRAINING BONUSES:
  - Creatures trained in multiple regions gain type resistance
  - Rolled at training time with D20
  - High roll = strong cross-type bonus

REAL LIFE RULES (physical card play):
  - See REAL_LIFE_RULES dict at bottom of file
  - Players roll physical D20 dice and enter results
  - Same outcomes as digital version
"""

import random
from typing import Optional

# ─────────────────────────────────────────────
#  CIRCLE OF LIFE — ELEMENT MATCHUP TABLE
#  beats: element this type is strong against (1.5x damage)
#  weak:  element this type is weak against   (0.5x damage)
#  neutral: all others (1.0x damage)
# ─────────────────────────────────────────────

ELEMENT_CIRCLE = ["fire", "nature", "ice", "storm", "spirit", "dark"]
#  fire → nature → ice → storm → spirit → dark → fire (loops)

def get_type_multiplier(attacker_element: str, defender_element: str) -> float:
    """
    Returns damage multiplier based on Circle of Life.
    1.5x if attacker beats defender
    0.5x if attacker is weak to defender
    1.0x neutral
    """
    if attacker_element not in ELEMENT_CIRCLE or defender_element not in ELEMENT_CIRCLE:
        return 1.0  # unknown elements = neutral

    atk_idx = ELEMENT_CIRCLE.index(attacker_element)
    def_idx = ELEMENT_CIRCLE.index(defender_element)
    circle_len = len(ELEMENT_CIRCLE)

    # Attacker beats the element one step ahead in the circle
    if (atk_idx + 1) % circle_len == def_idx:
        return 1.5  # super effective
    # Attacker is weak to the element one step behind
    elif (atk_idx - 1) % circle_len == def_idx:
        return 0.5  # not very effective
    else:
        return 1.0  # neutral


# ─────────────────────────────────────────────
#  D20 ROLL SYSTEM
# ─────────────────────────────────────────────

ROLL_OUTCOMES = {
    "critical_fail":  {"range": (1,  1),  "power_mult": 0.0,  "energy_delta": -15, "label": "CRITICAL FAIL!",  "color": "red"},
    "weak_hit":       {"range": (2,  5),  "power_mult": 0.25, "energy_delta":  5,  "label": "Weak Hit",        "color": "orange"},
    "normal_hit":     {"range": (6,  10), "power_mult": 0.75, "energy_delta": 10,  "label": "Hit",             "color": "white"},
    "strong_hit":     {"range": (11, 15), "power_mult": 1.0,  "energy_delta": 15,  "label": "Strong Hit!",     "color": "cyan"},
    "heavy_hit":      {"range": (16, 19), "power_mult": 1.25, "energy_delta": 20,  "label": "Heavy Hit!!",     "color": "gold"},
    "critical_hit":   {"range": (20, 20), "power_mult": 2.0,  "energy_delta": 35,  "label": "CRITICAL HIT!!!", "color": "green"},
}

def roll_d20(manual_roll: int = None) -> int:
    """
    Roll a D20. If manual_roll is provided (real life mode), use that value.
    Returns integer 1-20.
    """
    if manual_roll is not None:
        if not 1 <= manual_roll <= 20:
            raise ValueError(f"Manual roll must be 1-20, got {manual_roll}")
        return manual_roll
    return random.randint(1, 20)


def get_roll_outcome(roll: int) -> dict:
    """Return the outcome dict for a given D20 roll."""
    for outcome_id, outcome in ROLL_OUTCOMES.items():
        low, high = outcome["range"]
        if low <= roll <= high:
            return {"outcome_id": outcome_id, **outcome}
    return {"outcome_id": "normal_hit", **ROLL_OUTCOMES["normal_hit"]}


# ─────────────────────────────────────────────
#  STAT ROLL SYSTEM (used at hatch time)
#  Each stat gets a D20 roll that modifies the base value.
# ─────────────────────────────────────────────

STAT_ROLL_TABLE = {
    # roll range: multiplier applied to base stat
    (1,  1):  0.50,   # terrible roll — half base
    (2,  4):  0.75,   # below average
    (5,  8):  0.90,   # slightly below
    (9,  12): 1.00,   # average — exact base
    (13, 16): 1.10,   # slightly above
    (17, 19): 1.25,   # above average
    (20, 20): 1.50,   # perfect roll — 150% base
}

def roll_stat(base_value: int, manual_roll: int = None) -> tuple[int, int, float]:
    """
    Roll a D20 to determine final stat value.
    Returns (final_value, roll, multiplier)
    """
    roll = roll_d20(manual_roll)
    multiplier = 1.0
    for (low, high), mult in STAT_ROLL_TABLE.items():
        if low <= roll <= high:
            multiplier = mult
            break
    final = max(1, round(base_value * multiplier))
    return final, roll, multiplier


def roll_all_stats(base_stats: dict) -> dict:
    """
    Roll D20 for every stat in base_stats.
    Returns dict of { stat: { final, roll, multiplier } }
    """
    results = {}
    for stat, base_val in base_stats.items():
        if isinstance(base_val, int) and base_val > 0:
            final, roll, mult = roll_stat(base_val)
            results[stat] = {
                "base":       base_val,
                "roll":       roll,
                "multiplier": mult,
                "final":      final,
                "outcome":    get_roll_outcome(roll)["label"],
            }
        else:
            results[stat] = {
                "base": base_val, "roll": 0,
                "multiplier": 1.0, "final": base_val, "outcome": "N/A"
            }
    return results


# ─────────────────────────────────────────────
#  ENERGY BAR
# ─────────────────────────────────────────────

class EnergyBar:
    """Tracks a creature's special move energy during battle."""

    MAX_ENERGY = 100

    def __init__(self):
        self.current  = 0
        self.is_full  = False

    def add(self, amount: int):
        self.current = min(self.MAX_ENERGY, self.current + amount)
        if self.current >= self.MAX_ENERGY:
            self.is_full = True

    def drain(self, amount: int):
        self.current = max(0, self.current - amount)
        self.is_full = False

    def use_special(self) -> bool:
        """Consume the full bar to use a special move. Returns True if available."""
        if self.is_full:
            self.current = 0
            self.is_full = False
            return True
        return False

    @property
    def percentage(self) -> int:
        return int((self.current / self.MAX_ENERGY) * 100)

    def __repr__(self):
        bar = "█" * (self.percentage // 10) + "░" * (10 - self.percentage // 10)
        return f"[{bar}] {self.current}/{self.MAX_ENERGY}"


# ─────────────────────────────────────────────
#  BATTLE CREATURE — wrapper for battle state
# ─────────────────────────────────────────────

class BattleCreature:
    """
    Wraps a Creature object with battle-specific state.
    HP, energy, status effects, and available moves.
    """

    def __init__(self, creature, is_player: bool = True):
        self.creature    = creature
        self.is_player   = is_player
        self.current_hp  = creature.stats["hp"]
        self.max_hp      = creature.stats["hp"]
        self.energy      = EnergyBar()
        self.status      = None         # "burned", "frozen", "rooted", None
        self.status_turns = 0
        self.counter_ready = False      # True if they have a counter ability queued
        self.cross_training_bonus = {}  # { element: resistance_mult } from training

        # Build move list from creature abilities
        self.moves = self._build_moves()

    def _build_moves(self) -> list:
        """Build the list of usable moves from creature's ability list."""
        from cards import ABILITIES
        moves = []
        for ability_id in self.creature.abilities:
            ability = ABILITIES.get(ability_id)
            if ability:
                moves.append({
                    "id":           ability_id,
                    "display_name": ability["display_name"],
                    "element":      ability["element"],
                    "power":        ability["power"],
                    "accuracy":     ability["accuracy"],
                    "effect":       ability.get("effect", None),
                    "is_special":   ability.get("is_special", False),
                })
        return moves

    def get_base_attack(self) -> dict:
        """
        Every creature has a guaranteed base attack tied to their
        home region and element — no cards needed.
        """
        from regions import get_region
        region = get_region(self.creature.home_region)
        element = self.creature.element
        power = self.creature.stats.get("attack", 10)

        return {
            "id":           f"{element}_strike",
            "display_name": f"{element.capitalize()} Strike",
            "element":      element,
            "power":        power,
            "accuracy":     0.95,
            "effect":       None,
            "is_special":   False,
            "is_base":      True,
        }

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, amount: int) -> int:
        """Apply damage, return actual damage dealt."""
        actual = min(self.current_hp, max(0, amount))
        self.current_hp -= actual
        return actual

    def apply_status(self, status: str, turns: int = 2):
        """Apply a status effect if not already affected."""
        if not self.status:
            self.status       = status
            self.status_turns = turns

    def tick_status(self) -> Optional[str]:
        """
        Process status effect at start of turn.
        Returns a message if something happened, else None.
        """
        if not self.status:
            return None

        msg = None
        if self.status == "burned":
            burn_dmg = max(1, self.max_hp // 10)
            self.current_hp = max(0, self.current_hp - burn_dmg)
            msg = f"{self.creature.name} is burned! -{burn_dmg} HP"
        elif self.status == "frozen":
            msg = f"{self.creature.name} is frozen and can't move!"
        elif self.status == "rooted":
            msg = f"{self.creature.name} is rooted — speed halved!"

        self.status_turns -= 1
        if self.status_turns <= 0:
            msg = (msg or "") + f" {self.creature.name} recovered from {self.status}!"
            self.status = None
            self.status_turns = 0

        return msg

    @property
    def hp_percentage(self) -> int:
        return int((self.current_hp / self.max_hp) * 100)


# ─────────────────────────────────────────────
#  BATTLE ENGINE
# ─────────────────────────────────────────────

class Battle:
    """
    Manages a full battle between two BattleCreatures.

    Turn structure:
      1. Roll D20 for initiative (who goes first)
      2. Active player picks a move (or special if energy full)
      3. Roll D20 for attack outcome
      4. Check for counter opportunity (if defender has counter skill)
      5. Apply damage, energy, and status effects
      6. Swap turns
      7. Repeat until one creature faints
    """

    def __init__(self, player_creature: BattleCreature,
                       opponent_creature: BattleCreature):
        self.player   = player_creature
        self.opponent = opponent_creature
        self.turn     = 1
        self.log      = []           # full battle log for display
        self.active   = None         # who goes first this turn
        self.inactive = None
        self.is_over  = False
        self.winner   = None

        # Roll for first turn initiative
        self._roll_initiative()

    def _roll_initiative(self):
        """D20 roll to decide who goes first. Tie = higher speed wins."""
        p_roll = roll_d20()
        o_roll = roll_d20()

        self._log(f"⚔  INITIATIVE ROLL")
        self._log(f"   {self.player.creature.name}: rolled {p_roll}")
        self._log(f"   {self.opponent.creature.name}: rolled {o_roll}")

        if p_roll > o_roll:
            self.active, self.inactive = self.player, self.opponent
        elif o_roll > p_roll:
            self.active, self.inactive = self.opponent, self.player
        else:
            # Tie — higher speed wins
            if self.player.creature.stats.get("speed", 0) >= \
               self.opponent.creature.stats.get("speed", 0):
                self.active, self.inactive = self.player, self.opponent
            else:
                self.active, self.inactive = self.opponent, self.player

        self._log(f"   → {self.active.creature.name} goes first!\n")
        return {"player_roll": p_roll, "opponent_roll": o_roll,
                "first": self.active.creature.name}

    def execute_turn(self, move_id: str,
                     attack_roll: int = None,
                     counter_roll: int = None,
                     use_special: bool = False) -> dict:
        """
        Execute one full turn of battle.

        Args:
            move_id:      ID of the move the active creature uses
                          (use "base_attack" for the guaranteed base move)
            attack_roll:  Manual D20 roll (real life mode), or None for auto
            counter_roll: Manual D20 roll for counter attempt, or None
            use_special:  True to attempt special move (needs full energy bar)

        Returns:
            Full turn result dict for UI rendering.
        """
        if self.is_over:
            return {"error": "Battle is already over."}

        result = {
            "turn":          self.turn,
            "attacker":      self.active.creature.name,
            "defender":      self.inactive.creature.name,
            "move_used":     None,
            "attack_roll":   None,
            "roll_outcome":  None,
            "damage_dealt":  0,
            "energy_gained": 0,
            "counter":       None,
            "status_effect": None,
            "type_bonus":    None,
            "log":           [],
            "battle_over":   False,
            "winner":        None,
        }

        # ── Status tick ───────────────────────
        status_msg = self.active.tick_status()
        if status_msg:
            result["log"].append(status_msg)
            self._log(status_msg)

        # Frozen = skip turn
        if self.active.status == "frozen":
            self._end_turn(result)
            return result

        # ── Select move ───────────────────────
        if use_special and self.active.energy.use_special():
            move = self._get_special_move(self.active)
        elif move_id == "base_attack":
            move = self.active.get_base_attack()
        else:
            move = next((m for m in self.active.moves if m["id"] == move_id), None)
            if not move:
                move = self.active.get_base_attack()

        result["move_used"] = move["display_name"]
        self._log(f"Turn {self.turn}: {self.active.creature.name} uses {move['display_name']}!")

        # ── Attack Roll ───────────────────────
        atk_roll    = roll_d20(attack_roll)
        outcome     = get_roll_outcome(atk_roll)
        result["attack_roll"]  = atk_roll
        result["roll_outcome"] = outcome

        self._log(f"   🎲 Attack roll: {atk_roll} — {outcome['label']}")

        # ── Energy update ─────────────────────
        self.active.energy.add(outcome["energy_delta"])
        if outcome["energy_delta"] < 0:
            self.active.energy.drain(abs(outcome["energy_delta"]))
        result["energy_gained"] = outcome["energy_delta"]
        self._log(f"   ⚡ Energy: {self.active.energy}")

        # ── Miss check ────────────────────────
        if outcome["outcome_id"] == "critical_fail":
            self._log(f"   💨 {self.active.creature.name} missed completely!")
            self._end_turn(result)
            return result

        # ── Type multiplier ───────────────────
        type_mult = get_type_multiplier(move["element"],
                                        self.inactive.creature.element)
        # Cross-training resistance
        cross_resist = self.inactive.cross_training_bonus.get(move["element"], 1.0)
        total_mult   = type_mult * cross_resist * outcome["power_mult"]

        if type_mult > 1.0:
            result["type_bonus"] = "super_effective"
            self._log(f"   🔥 Super effective! ({move['element']} vs {self.inactive.creature.element})")
        elif type_mult < 1.0:
            result["type_bonus"] = "not_effective"
            self._log(f"   💧 Not very effective...")

        # ── Base damage calculation ───────────
        atk_stat  = self.active.creature.stats.get("attack", 10)
        def_stat  = self.inactive.creature.stats.get("defense", 5)
        move_pwr  = move["power"]

        raw_damage = max(1, round(
            ((atk_stat * move_pwr) / (def_stat * 10)) * total_mult * 10
        ))

        # ── Counter check ─────────────────────
        counter_result = None
        if self._can_counter(self.inactive):
            c_roll     = roll_d20(counter_roll)
            c_outcome  = get_roll_outcome(c_roll)
            self._log(f"   🛡 {self.inactive.creature.name} attempts counter! Roll: {c_roll} — {c_outcome['label']}")

            if c_roll >= atk_roll:
                # Counter succeeds — reduce damage and deal back
                raw_damage     = max(1, raw_damage // 2)
                counter_dmg    = max(1, raw_damage // 3)
                self.active.take_damage(counter_dmg)
                self.inactive.energy.add(20)
                counter_result = {
                    "roll":    c_roll,
                    "success": True,
                    "damage":  counter_dmg,
                }
                self._log(f"   ✅ Counter SUCCESS! Damage halved. {self.active.creature.name} takes {counter_dmg} back!")
            else:
                # Counter fails — take extra damage
                raw_damage = round(raw_damage * 1.2)
                counter_result = {
                    "roll":    c_roll,
                    "success": False,
                }
                self._log(f"   ❌ Counter FAILED! Incoming damage increased!")

        result["counter"] = counter_result

        # ── Apply damage ──────────────────────
        actual_damage = self.inactive.take_damage(raw_damage)
        result["damage_dealt"] = actual_damage
        self._log(f"   💥 {self.inactive.creature.name} takes {actual_damage} damage! "
                  f"HP: {self.inactive.current_hp}/{self.inactive.max_hp}")

        # ── Status effect ─────────────────────
        if move.get("effect"):
            status_result = self._apply_move_effect(move["effect"], self.inactive, atk_roll)
            result["status_effect"] = status_result

        # ── Check faint ───────────────────────
        if not self.inactive.is_alive():
            self._log(f"\n💀 {self.inactive.creature.name} fainted!")
            self.is_over = True
            self.winner  = self.active
            result["battle_over"] = True
            result["winner"]      = self.active.creature.name
            self._log(f"🏆 {self.active.creature.name} wins!")

        self._end_turn(result)
        return result

    def _apply_move_effect(self, effect: str, target: BattleCreature,
                            roll: int) -> Optional[dict]:
        """Parse and apply a move's secondary effect based on roll."""
        if not effect:
            return None

        # e.g. "burn_chance_0.25"
        if "burn_chance" in effect:
            chance = float(effect.split("_")[-1])
            if random.random() < chance and roll >= 10:
                target.apply_status("burned", turns=3)
                self._log(f"   🔥 {target.creature.name} is burned!")
                return {"type": "burned", "applied": True}

        elif "freeze_chance" in effect:
            chance = float(effect.split("_")[-1])
            if random.random() < chance and roll >= 12:
                target.apply_status("frozen", turns=2)
                self._log(f"   🧊 {target.creature.name} is frozen!")
                return {"type": "frozen", "applied": True}

        elif "immobilize" in effect:
            if roll >= 8:
                target.apply_status("rooted", turns=1)
                self._log(f"   🌿 {target.creature.name} is rooted!")
                return {"type": "rooted", "applied": True}

        elif effect == "always_hits":
            return {"type": "always_hits", "applied": True}

        return {"applied": False}

    def _can_counter(self, creature: BattleCreature) -> bool:
        """Check if a creature has counter capability (from traits or abilities)."""
        return "shadow_dash" in creature.creature.abilities or \
               "counter_stance" in creature.creature.abilities or \
               "lone_wanderer" in creature.creature.trait_ids

    def _get_special_move(self, bc: BattleCreature) -> dict:
        """Get the most powerful move as the special, boosted."""
        if bc.moves:
            best = max(bc.moves, key=lambda m: m["power"])
            return {**best,
                    "display_name": f"⚡ SPECIAL: {best['display_name']}",
                    "power":        best["power"] * 2,
                    "is_special":   True}
        base = bc.get_base_attack()
        return {**base,
                "display_name": f"⚡ SPECIAL: {base['display_name']}",
                "power":        base["power"] * 2,
                "is_special":   True}

    def _end_turn(self, result: dict):
        """Swap active/inactive and increment turn counter."""
        result["log"] = self.log[-10:]   # last 10 entries for UI
        if not self.is_over:
            self.active, self.inactive = self.inactive, self.active
            self.turn += 1

    def _log(self, message: str):
        self.log.append(message)
        print(message)

    def get_state(self) -> dict:
        """Return full current battle state for UI rendering."""
        return {
            "turn":     self.turn,
            "is_over":  self.is_over,
            "winner":   self.winner.creature.name if self.winner else None,
            "player": {
                "name":       self.player.creature.name,
                "element":    self.player.creature.element,
                "hp":         self.player.current_hp,
                "max_hp":     self.player.max_hp,
                "hp_pct":     self.player.hp_percentage,
                "energy_pct": self.player.energy.percentage,
                "energy_full":self.player.energy.is_full,
                "status":     self.player.status,
                "moves":      self.player.moves,
                "can_special":self.player.energy.is_full,
            },
            "opponent": {
                "name":       self.opponent.creature.name,
                "element":    self.opponent.creature.element,
                "hp":         self.opponent.current_hp,
                "max_hp":     self.opponent.max_hp,
                "hp_pct":     self.opponent.hp_percentage,
                "energy_pct": self.opponent.energy.percentage,
                "status":     self.opponent.status,
            },
        }


# ─────────────────────────────────────────────
#  CROSS-TRAINING SYSTEM
# ─────────────────────────────────────────────

def cross_train(creature, training_region_id: str,
                manual_roll: int = None) -> dict:
    """
    Train a creature in a non-native region.
    D20 roll determines the strength of the cross-type resistance gained.

    Args:
        creature:           Creature object
        training_region_id: Region to train in
        manual_roll:        Manual D20 (real life mode)

    Returns:
        Result dict with roll, bonus gained, and element affected.
    """
    from regions import get_region
    region  = get_region(training_region_id)
    element = region["element"]

    roll = roll_d20(manual_roll)

    # Roll table for cross-training resistance
    if roll == 1:
        resistance = 1.15       # slight backfire — takes slightly more
        label = "Poor training — minimal gain"
    elif roll <= 5:
        resistance = 0.95
        label = "Basic training"
    elif roll <= 10:
        resistance = 0.85
        label = "Decent training"
    elif roll <= 15:
        resistance = 0.75
        label = "Good training — solid resistance"
    elif roll <= 19:
        resistance = 0.60
        label = "Excellent training!"
    else:  # 20
        resistance = 0.40
        label = "PERFECT TRAINING — strong resistance!"

    # Apply to creature's battle cross-training dict
    # (stored on creature for use in BattleCreature)
    if not hasattr(creature, "cross_training"):
        creature.cross_training = {}
    # Take the best resistance if already trained
    existing = creature.cross_training.get(element, 1.0)
    creature.cross_training[element] = min(existing, resistance)

    print(f"🏋 {creature.name} trained in {region['display_name']}!")
    print(f"   🎲 Roll: {roll} — {label}")
    print(f"   {element.upper()} resistance: {round((1-resistance)*100)}% reduction")

    return {
        "roll":       roll,
        "label":      label,
        "element":    element,
        "resistance": resistance,
        "region":     region["display_name"],
    }


# ─────────────────────────────────────────────
#  REAL LIFE RULES REFERENCE
#  Printed in the physical rulebook / README
# ─────────────────────────────────────────────

REAL_LIFE_RULES = """
╔══════════════════════════════════════════════════════════════╗
║           WORLDHATCH — REAL LIFE BATTLE RULES               ║
╚══════════════════════════════════════════════════════════════╝

WHAT YOU NEED:
  • Your physical WORLDHATCH creature cards
  • One D20 die per player
  • This rulebook

SETUP:
  1. Each player picks one creature card
  2. Both players roll D20 — higher roll goes first
     Tie: higher Speed stat on card wins
  3. Place cards face up on the table

TURN STRUCTURE:
  1. Active player announces their attack (base attack or ability)
  2. Active player rolls D20:
     • 1        = Critical Fail  — miss, lose 15 energy
     • 2-5      = Weak Hit       — 25% power, +5 energy
     • 6-10     = Normal Hit     — 75% power, +10 energy
     • 11-15    = Strong Hit     — 100% power, +15 energy
     • 16-19    = Heavy Hit      — 125% power, +20 energy
     • 20       = Critical Hit   — 200% power, +35 energy
  3. Defending player may attempt COUNTER (if they have counter ability):
     • Defender rolls D20
     • If counter roll >= attack roll: damage halved, deal back 1/3
     • If counter roll < attack roll: take 20% extra damage
  4. Calculate damage using card stats
  5. Track HP with dice or tokens
  6. Swap turns

ENERGY BAR:
  • Track with a D20 set aside — starts at 0
  • Add/subtract energy each turn per roll outcome above
  • When energy die reaches 20: SPECIAL MOVE available!
  • Announce special move, roll D20 with DOUBLE power
  • Reset energy die to 0 after special

ELEMENT CIRCLE OF LIFE:
  Fire → Nature → Ice → Storm → Spirit → Dark → Fire
  (arrow means beats — deals 1.5x damage)
  Reverse direction = 0.5x damage

TYPE DAMAGE:
  Super Effective (beating element): 1.5x damage
  Not Very Effective (weak element): 0.5x damage
  Neutral: 1.0x damage

DAMAGE FORMULA:
  Damage = (Attack × Move Power) ÷ (Defense × 10) × Type Mult × Roll Mult × 10

STATUS EFFECTS (from ability cards):
  Burned:  Lose 10% max HP per turn for 3 turns
  Frozen:  Skip next turn (2 turns)
  Rooted:  Speed halved for 1 turn

WINNING:
  First creature to reach 0 HP loses.
  Winner gains XP equal to opponent's level × 10.

CROSS-TRAINING BONUS (if card applied):
  Roll D20 when applying cross-training card.
  Result determines resistance % to that element type.
  Record on your creature card with a pencil note.

══════════════════════════════════════════════════════════════
"""
