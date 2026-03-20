"""
game.py — WORLDHATCH Game Session & Demo Runner
════════════════════════════════════════════════
GameSession ties all systems together.
run_demo() walks through a full example:
  - Two players created
  - Eggs spawned and cards applied
  - Eggs hatched, mutations rolled
  - Cards used on creatures
  - Evolution attempted
  - Trade proposed and completed

This is your Replit test entry point.
Run:  python worldhatch.py
"""

from creature import spawn_egg, Creature, CREATURE_REGISTRY
from player   import Player
from cards    import CARDS, get_card
from trading  import propose_trade


class GameSession:
    """
    Manages players and game state for a session.
    Expand this to handle multiplayer rooms, server state, etc.
    """

    def __init__(self):
        self.players = {}

    def add_player(self, player: Player):
        self.players[player.player_id] = player

    def get_player(self, player_id: str) -> Player:
        return self.players.get(player_id)

    # ──────────────────────────────────────────
    #  DEMO RUN
    #  Walks through all major systems with
    #  printed output so you can see it working.
    # ──────────────────────────────────────────

    def run_demo(self):
        print("\n" + "═"*54)
        print("  W O R L D H A T C H  —  Demo Session")
        print("═"*54)

        # ── 1. Create two players ──────────────

        print("\n── Step 1: Create Players ──────────────────────────")
        alice = Player(name="Alice", home_region="suncrest_expanse")
        bob   = Player(name="Bob",   home_region="frostspire_reach")
        self.add_player(alice)
        self.add_player(bob)

        # ── 2. Give starting cards ─────────────

        print("\n── Step 2: Distribute Starter Cards ───────────────")
        alice.add_card("ember_gene",    qty=2)
        alice.add_card("vitality_shard", qty=1)
        alice.add_card("blaze_path_card", qty=1)
        bob.add_card("frost_gene",      qty=2)
        bob.add_card("power_fragment",  qty=1)

        # ── 3. Spawn eggs ──────────────────────

        print("\n── Step 3: Spawn Region Eggs ───────────────────────")
        # Guaranteed starter for demo clarity
        from creature import Egg
        alice_egg = Egg(species_id="emberback_rumbler",
                        region_id="suncrest_expanse",
                        owner_id=alice.player_id)
        alice.add_egg(alice_egg)

        bob_egg = Egg(species_id="glacierfang",
                      region_id="frostspire_reach",
                      owner_id=bob.player_id)
        bob.add_egg(bob_egg)

        # Also spawn a random egg to show the weighted spawn system
        print("\n  [Random spawn demo]")
        spawn_egg(region_id="verdeluna_jungle")

        # ── 4. Apply cards to eggs ─────────────

        print("\n── Step 4: Apply Cards to Eggs ─────────────────────")
        alice_egg.apply_card("ember_gene")      # boosts inferno_crest chance
        bob_egg.apply_card("frost_gene")        # boosts glacial_mantle chance

        # ── 5. Hatch eggs ──────────────────────

        print("\n── Step 5: Hatch Eggs ──────────────────────────────")
        alice_creature = alice.hatch_egg(alice_egg.egg_id,
                                         context={"is_nighttime": False})
        bob_creature   = bob.hatch_egg(bob_egg.egg_id,
                                       context={"is_nighttime": False})

        # ── 6. Print creature summaries ────────

        print("\n── Step 6: Creature Summaries ──────────────────────")
        if alice_creature:
            print(alice_creature.summary())
        if bob_creature:
            print(bob_creature.summary())

        # ── 7. Use a card on hatched creature ──

        print("\n── Step 7: Apply Card to Hatched Creature ──────────")
        result = alice.use_card("vitality_shard", alice_creature.creature_id)
        print(f"  {result['message']}")
        print(f"  Alice's {alice_creature.name} HP is now: {alice_creature.stats['hp']}")

        # ── 8. Level up and try to evolve ──────

        print("\n── Step 8: Level Up + Evolution Attempt ────────────")
        print(f"  Giving {alice_creature.name} a lot of XP...")
        alice_creature.gain_xp(1200)   # fast-track to level 10+

        # Try default evolution
        print(f"\n  Attempting DEFAULT evolution branch...")
        alice_creature.evolve("default")

        # Try blaze_path evolution (needs the card applied first)
        # Let's give a second creature the blaze_path_card route
        print(f"\n  [Demo: blaze_path branch requires 'blaze_path_card' applied]")
        alice.add_card("blaze_path_card", qty=1)
        # For demo, we'll show the check logic (creature already evolved)
        ok, reason = alice_creature.can_evolve("blazeborn")
        print(f"  Can evolve 'blazeborn'? {ok}  ({reason if not ok else 'yes!'})")

        # ── 9. Trade demo ──────────────────────

        print("\n── Step 9: Player-to-Player Trade ──────────────────")
        if alice_creature and bob_creature:
            session = propose_trade(
                proposer = alice,
                receiver = bob,
                offer    = {
                    "creatures": [],
                    "cards":     {"ember_gene": 1},
                    "coins":     50,
                },
                request  = {
                    "creatures": [bob_creature.creature_id],
                    "cards":     {},
                    "coins":     0,
                }
            )
            result = session.accept()   # Bob accepts
            print(f"\n  Trade result: {result['message']}")

        # ── 10. Final inventory printout ───────

        print("\n── Step 10: Final Inventories ──────────────────────")
        print(alice.inventory_summary())
        print(bob.inventory_summary())

        print("═"*54)
        print("  Demo complete. Edit creature.py / regions.py")
        print("  to add new species and regions!")
        print("═"*54 + "\n")
