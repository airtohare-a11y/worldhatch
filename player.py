"""
player.py — WORLDHATCH Player System
══════════════════════════════════════
A Player has:
  - A profile (ID, name, home region)
  - An inventory of eggs and creatures
  - A card collection
  - Trade history

TO EXPAND:
  - Add currency system (realm_coins)
  - Add region unlock progression
  - Add achievement tracking
"""

import uuid


class Player:
    """Represents a WORLDHATCH player and their inventory."""

    def __init__(self, name: str, home_region: str = "suncrest_expanse"):
        self.player_id   = str(uuid.uuid4())[:8]
        self.name        = name
        self.home_region = home_region

        # Inventories
        self.eggs          = []     # list of Egg objects
        self.creatures     = []     # list of Creature objects
        self.card_inventory = {}    # { card_id: quantity }

        # Progression
        self.realm_coins   = 200    # starting currency
        self.regions_visited = [home_region]

        print(f"👤 Player created: {self.name} [{self.player_id}] — {home_region}")

    # ── Egg & Creature Management ──────────────

    def add_egg(self, egg) -> None:
        self.eggs.append(egg)
        egg.owner_id = self.player_id
        print(f"  {self.name} received: {egg.display_name}")

    def add_creature(self, creature) -> None:
        self.creatures.append(creature)
        creature.owner_id = self.player_id
        print(f"  {self.name} now owns: {creature.name}")

    def remove_creature(self, creature_id: str):
        """Remove a creature from inventory (e.g. after a trade)."""
        before = len(self.creatures)
        self.creatures = [c for c in self.creatures if c.creature_id != creature_id]
        return len(self.creatures) < before

    def get_creature(self, creature_id: str):
        """Find a creature in inventory by ID."""
        for c in self.creatures:
            if c.creature_id == creature_id:
                return c
        return None

    def hatch_egg(self, egg_id: str, context: dict = None):
        """
        Hatch an egg in inventory by its ID.
        Automatically adds the resulting creature to inventory.
        """
        egg = next((e for e in self.eggs if e.egg_id == egg_id), None)
        if not egg:
            print(f"Egg '{egg_id}' not found in {self.name}'s inventory.")
            return None
        creature = egg.hatch(context or {})
        self.eggs.remove(egg)
        self.add_creature(creature)
        return creature

    # ── Card Management ────────────────────────

    def add_card(self, card_id: str, qty: int = 1) -> None:
        self.card_inventory[card_id] = self.card_inventory.get(card_id, 0) + qty
        print(f"  {self.name} received card: {card_id} x{qty}")

    def has_card(self, card_id: str) -> bool:
        return self.card_inventory.get(card_id, 0) > 0

    def use_card(self, card_id: str, creature_id: str) -> dict:
        """Apply a card from inventory to a creature."""
        if not self.has_card(card_id):
            return {"success": False, "message": f"No '{card_id}' in inventory."}

        creature = self.get_creature(creature_id)
        if not creature:
            return {"success": False, "message": f"Creature '{creature_id}' not found."}

        from cards import apply_card_to_creature, get_card
        card   = get_card(card_id)
        result = apply_card_to_creature(card_id, creature)

        if result["success"] and card.get("consumable", True):
            self.card_inventory[card_id] -= 1
            if self.card_inventory[card_id] == 0:
                del self.card_inventory[card_id]

        return result

    # ── Display ────────────────────────────────

    def inventory_summary(self) -> str:
        lines = [
            f"\n{'═'*40}",
            f"  PLAYER: {self.name}  [{self.player_id}]",
            f"  Home: {self.home_region}",
            f"  Coins: {self.realm_coins} 🪙",
            f"  {'─'*36}",
            f"  EGGS ({len(self.eggs)}):",
        ]
        for egg in self.eggs:
            lines.append(f"    • {egg.display_name} [{egg.egg_id}]"
                         f" | region={egg.region_id}"
                         f" | cards={egg.cards_applied}")
        lines.append(f"  CREATURES ({len(self.creatures)}):")
        for c in self.creatures:
            lines.append(f"    • {c.name} [{c.creature_id}]"
                         f" | lv{c.level} {c.element}"
                         f" | mutations={c.mutations_acquired}")
        lines.append(f"  CARDS:")
        if self.card_inventory:
            for cid, qty in self.card_inventory.items():
                lines.append(f"    • {cid} x{qty}")
        else:
            lines.append("    (none)")
        lines.append(f"{'═'*40}\n")
        return "\n".join(lines)

    def __repr__(self):
        return (f"<Player '{self.name}' | {self.player_id} | "
                f"eggs={len(self.eggs)} creatures={len(self.creatures)}>")
