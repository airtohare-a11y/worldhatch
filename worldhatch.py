"""
╔══════════════════════════════════════════════════════════════╗
║                        W O R L D H A T C H                  ║
║          Creature Hatching & Trading — Game Engine           ║
║                     Core Systems Skeleton                    ║
╚══════════════════════════════════════════════════════════════╝

STRUCTURE:
  regions.py     → Region definitions and spawn tables
  traits.py      → Trait + Mutation definitions
  cards.py       → Card definitions and effect logic
  creature.py    → Creature + Egg classes
  player.py      → Player inventory + profile
  trading.py     → Trade proposal and resolution logic
  game.py        → Main game loop / session controller
  worldhatch.py  → THIS FILE — entry point + demo run

Tested on Replit (Python 3.10+). No external dependencies.
"""

from game import GameSession

if __name__ == "__main__":
    session = GameSession()
    session.run_demo()
