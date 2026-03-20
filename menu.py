"""
menu.py — WORLDHATCH Interactive CLI Menu
══════════════════════════════════════════
Run this file to play WORLDHATCH in the terminal.

  python menu.py

Full playable loop:
  - Create a player
  - Explore regions and find eggs
  - Apply cards before hatching
  - Hatch eggs and see D20 stat rolls
  - View your creature collection
  - Battle your creatures
  - Trade with other players
  - Check the full Pokedex-style roster
"""

import os
import time
import random
from player   import Player
from creature import Creature, Egg, spawn_egg, CREATURE_REGISTRY
from regions  import REGIONS, list_regions
from cards    import CARDS, ABILITIES
from battle   import Battle, BattleCreature, roll_d20, get_roll_outcome, cross_train
from trading  import propose_trade
from roster   import FULL_ROSTER


# ─────────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────────

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner(text: str, char: str = "═", width: int = 54):
    line = char * width
    print(f"\n{line}")
    print(f"  {text}")
    print(f"{line}")

def pause(msg: str = "Press ENTER to continue..."):
    input(f"\n  {msg}")

def pick(prompt: str, options: list, allow_back: bool = True) -> int:
    """
    Show a numbered menu and return the chosen index (0-based).
    Returns -1 if user picks 'back'.
    """
    print()
    for i, opt in enumerate(options, 1):
        print(f"  [{i}] {opt}")
    if allow_back:
        print(f"  [0] Back")
    while True:
        try:
            raw = input(f"\n  {prompt} > ").strip()
            if raw == "0" and allow_back:
                return -1
            val = int(raw)
            if 1 <= val <= len(options):
                return val - 1
            print(f"  Enter 1-{len(options)}")
        except (ValueError, EOFError):
            print(f"  Enter a number.")

def roll_animation(label: str, roll: int, delay: float = 0.06):
    """Animate a D20 roll in the terminal."""
    print(f"\n  {label}")
    print("  Rolling D20", end="", flush=True)
    for _ in range(10):
        r = random.randint(1, 20)
        print(f"\r  Rolling D20... [{r:2}]", end="", flush=True)
        time.sleep(delay)
    outcome = get_roll_outcome(roll)
    print(f"\r  Rolling D20... [{roll:2}] — {outcome['label']}!     ")
    return outcome

def hp_bar(current: int, maximum: int, width: int = 20) -> str:
    filled = round((current / maximum) * width) if maximum > 0 else 0
    bar    = "█" * filled + "░" * (width - filled)
    pct    = round((current / maximum) * 100) if maximum > 0 else 0
    color  = "LOW" if pct < 25 else ("MID" if pct < 50 else "OK")
    return f"[{bar}] {current}/{maximum} {color}"

def energy_bar(current: int, width: int = 10) -> str:
    filled = round((current / 100) * width)
    bar    = "▓" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/100"


# ─────────────────────────────────────────────
#  GAME STATE
# ─────────────────────────────────────────────

class GameState:
    def __init__(self):
        self.players     = {}       # { name: Player }
        self.active_name = None

    @property
    def player(self) -> Player:
        return self.players.get(self.active_name)


G = GameState()


# ─────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────

def main_menu():
    while True:
        clear()
        banner("W O R L D H A T C H", "═", 54)
        print("  Creature Hatching & Trading")
        print(f"  Active Player: {G.active_name or '(none)'}")

        options = [
            "Create / Switch Player",
            "Explore Region  (find eggs)",
            "My Collection   (eggs & creatures)",
            "Hatch an Egg",
            "Battle",
            "Trade",
            "Pokedex         (full roster)",
            "Card Shop",
            "Quit",
        ]
        choice = pick("Choose", options, allow_back=False)

        if   choice == 0: menu_player()
        elif choice == 1: menu_explore()
        elif choice == 2: menu_collection()
        elif choice == 3: menu_hatch()
        elif choice == 4: menu_battle()
        elif choice == 5: menu_trade()
        elif choice == 6: menu_pokedex()
        elif choice == 7: menu_card_shop()
        elif choice == 8:
            print("\n  Thanks for playing WORLDHATCH!\n")
            break


# ─────────────────────────────────────────────
#  PLAYER MENU
# ─────────────────────────────────────────────

def menu_player():
    clear()
    banner("PLAYER SELECT")

    options = ["Create new player"] + list(G.players.keys())
    choice  = pick("Choose", options)
    if choice == -1:
        return

    if choice == 0:
        name = input("\n  Enter player name: ").strip()
        if not name:
            return
        print("\n  Choose your home region:")
        region_ids = list_regions()
        for i, rid in enumerate(region_ids, 1):
            r = REGIONS[rid]
            print(f"  [{i}] {r['display_name']:28} ({r['element'].upper()})")
        try:
            ri = int(input("\n  Region number > ").strip()) - 1
            home = region_ids[ri] if 0 <= ri < len(region_ids) else region_ids[0]
        except (ValueError, IndexError):
            home = region_ids[0]

        p = Player(name=name, home_region=home)
        # Give starter cards
        p.add_card("ember_gene",     qty=1)
        p.add_card("vitality_shard", qty=1)
        p.add_card("root_bind_card", qty=1)
        # Give a starter egg from home region
        egg = spawn_egg(home, p.player_id)
        p.add_egg(egg)
        G.players[name]  = p
        G.active_name    = name
        print(f"\n  Welcome, {name}! You received a starter egg and 3 cards.")
        pause()
    else:
        G.active_name = list(G.players.keys())[choice - 1]
        print(f"\n  Switched to {G.active_name}.")
        pause()


# ─────────────────────────────────────────────
#  EXPLORE MENU
# ─────────────────────────────────────────────

def menu_explore():
    if not G.player:
        print("\n  Create a player first!"); pause(); return

    clear()
    banner("EXPLORE REGIONS")
    print("  Travel to a region to find eggs.\n")

    region_ids = list_regions()
    options    = []
    for rid in region_ids:
        r = REGIONS[rid]
        options.append(f"{r['display_name']:28} — {r['element'].upper():8} ({r['real_world_ref']})")

    choice = pick("Choose region", options)
    if choice == -1:
        return

    region_id = region_ids[choice]
    region    = REGIONS[region_id]

    clear()
    banner(f"EXPLORING: {region['display_name'].upper()}")
    print(f"  {region['real_world_ref']}")
    print(f"  Dominant element: {region['element'].upper()}")
    print("\n  Searching for eggs", end="", flush=True)
    for _ in range(5):
        time.sleep(0.3)
        print(".", end="", flush=True)

    # 70% chance to find an egg, 30% chance of nothing
    if random.random() < 0.70:
        egg = spawn_egg(region_id, G.player.player_id)
        G.player.add_egg(egg)
        template = CREATURE_REGISTRY[egg.species_id]
        print(f"\n\n  *** EGG FOUND! ***")
        print(f"  {egg.display_name}")
        print(f"  Element : {template['element'].upper()}")
        print(f"  Rarity  : {template['rarity'].upper()}")
        print(f"  Region  : {region['display_name']}")
        print(f"\n  The egg has been added to your collection!")
    else:
        print(f"\n\n  No eggs found this time. Try again!")

    pause()


# ─────────────────────────────────────────────
#  COLLECTION MENU
# ─────────────────────────────────────────────

def menu_collection():
    if not G.player:
        print("\n  Create a player first!"); pause(); return

    p = G.player
    while True:
        clear()
        banner(f"COLLECTION — {p.name.upper()}")
        print(f"  Coins: {p.realm_coins} | Eggs: {len(p.eggs)} | Creatures: {len(p.creatures)}")
        print(f"  Cards: {sum(p.card_inventory.values())}")

        options = [
            f"View Eggs       ({len(p.eggs)})",
            f"View Creatures  ({len(p.creatures)})",
            f"View Cards      ({sum(p.card_inventory.values())})",
        ]
        choice = pick("Choose", options)
        if choice == -1:
            return
        elif choice == 0: view_eggs(p)
        elif choice == 1: view_creatures(p)
        elif choice == 2: view_cards(p)


def view_eggs(p: Player):
    clear()
    banner("MY EGGS")
    if not p.eggs:
        print("  No eggs yet — explore regions to find some!")
        pause(); return

    for i, egg in enumerate(p.eggs, 1):
        template = CREATURE_REGISTRY.get(egg.species_id, {})
        print(f"\n  [{i}] {egg.display_name}")
        print(f"       ID      : {egg.egg_id}")
        print(f"       Region  : {egg.region_id}")
        print(f"       Rarity  : {template.get('rarity','?').upper()}")
        print(f"       Element : {template.get('element','?').upper()}")
        if egg.cards_applied:
            print(f"       Cards   : {', '.join(egg.cards_applied)}")
    pause()


def view_creatures(p: Player):
    if not p.creatures:
        print("\n  No creatures yet — hatch some eggs!")
        pause(); return

    while True:
        clear()
        banner("MY CREATURES")
        options = [f"{c.name:25} Lv{c.level:2} | {c.element:7} | {c.rarity}" for c in p.creatures]
        choice  = pick("View details", options)
        if choice == -1:
            return
        clear()
        print(p.creatures[choice].summary())
        pause()


def view_cards(p: Player):
    clear()
    banner("MY CARDS")
    if not p.card_inventory:
        print("  No cards yet.")
        pause(); return
    for card_id, qty in p.card_inventory.items():
        card = CARDS.get(card_id, {})
        print(f"  {card.get('display_name', card_id):25} x{qty}  [{card.get('rarity','?')}]  {card.get('description','')[:50]}")
    pause()


# ─────────────────────────────────────────────
#  HATCH MENU
# ─────────────────────────────────────────────

def menu_hatch():
    if not G.player:
        print("\n  Create a player first!"); pause(); return

    p = G.player
    if not p.eggs:
        print("\n  No eggs to hatch! Explore regions first."); pause(); return

    clear()
    banner("HATCH AN EGG")

    options = []
    for egg in p.eggs:
        t = CREATURE_REGISTRY.get(egg.species_id, {})
        options.append(f"{egg.display_name:30} [{t.get('rarity','?'):9}] | {t.get('element','?').upper()}")

    choice = pick("Choose egg to hatch", options)
    if choice == -1:
        return

    egg = p.eggs[choice]

    # Card application
    if p.card_inventory:
        clear()
        banner("APPLY CARDS BEFORE HATCHING?")
        print("  Applying cards now can boost mutations and stats.\n")
        while True:
            card_options = [f"{CARDS[cid]['display_name']} x{qty}" for cid, qty in p.card_inventory.items()]
            card_options.append("Done — hatch now")
            ch = pick("Apply a card", card_options)
            if ch == -1 or ch == len(card_options) - 1:
                break
            card_id = list(p.card_inventory.keys())[ch]
            egg.apply_card(card_id)
            print(f"  Card '{CARDS[card_id]['display_name']}' staged on egg.")

    # Hatch with stat rolls
    clear()
    banner(f"HATCHING: {egg.display_name.upper()}")
    print("\n  Cracking open the egg", end="", flush=True)
    for _ in range(8):
        time.sleep(0.25)
        print(".", end="", flush=True)
    print("\n")

    # Show D20 stat rolls
    template = CREATURE_REGISTRY[egg.species_id]
    print("  STAT ROLLS (D20 determines final values):\n")
    rolled_stats = {}
    for stat, base in template["base_stats"].items():
        if isinstance(base, int) and base > 0:
            roll   = roll_d20()
            outcome = get_roll_outcome(roll)
            from battle import STAT_ROLL_TABLE
            mult = 1.0
            for (lo, hi), m in STAT_ROLL_TABLE.items():
                if lo <= roll <= hi:
                    mult = m
                    break
            final = max(1, round(base * mult))
            rolled_stats[stat] = final
            bar = "▓" * round(mult * 8) + "░" * (8 - round(mult * 8))
            print(f"  {stat:14} base={base:3}  roll={roll:2}  [{bar}]  → {final:3}  {outcome['label']}")
            time.sleep(0.2)
        else:
            rolled_stats[stat] = base

    print("\n  Hatching creature...")
    time.sleep(0.5)

    creature = p.hatch_egg(egg.egg_id, context={"is_nighttime": random.random() < 0.3})

    if creature:
        # Apply rolled stats
        for stat, val in rolled_stats.items():
            if stat in creature.stats:
                creature.stats[stat] = val
        creature.current_hp = creature.stats.get("hp", 50)

        print(f"\n  ✨ {creature.name} has hatched!")
        if creature.mutations_acquired:
            print(f"  Mutations: {', '.join(creature.mutations_acquired)}")
        print(f"\n  Final Stats:")
        for stat, val in creature.stats.items():
            print(f"    {stat:14}: {val}")

    pause()


# ─────────────────────────────────────────────
#  BATTLE MENU
# ─────────────────────────────────────────────

def menu_battle():
    if not G.player:
        print("\n  Create a player first!"); pause(); return
    if not G.player.creatures:
        print("\n  No creatures to battle! Hatch some eggs first."); pause(); return

    clear()
    banner("BATTLE")

    options = ["Battle a wild creature", "Battle another player's creature"]
    choice  = pick("Choose battle type", options)
    if choice == -1:
        return

    # Pick player creature
    print("\n  Choose YOUR creature:")
    p_opts  = [f"{c.name} Lv{c.level} [{c.element}]" for c in G.player.creatures]
    p_choice = pick("Your fighter", p_opts)
    if p_choice == -1:
        return
    player_creature = G.player.creatures[p_choice]

    if choice == 0:
        # Spawn a wild opponent from a random region
        region_id   = random.choice(list_regions())
        wild_egg    = spawn_egg(region_id)
        opp_creature = Creature(wild_egg.species_id, region_id)
        opp_creature.gain_xp(player_creature.level * 50)
    else:
        # Pick another player
        other_players = [name for name in G.players if name != G.active_name]
        if not other_players:
            print("\n  No other players exist yet. Create another player first.")
            pause(); return
        print("\n  Choose opponent player:")
        opp_choice = pick("Opponent", other_players)
        if opp_choice == -1:
            return
        opp_player = G.players[other_players[opp_choice]]
        if not opp_player.creatures:
            print("\n  That player has no creatures.")
            pause(); return
        print("\n  Choose OPPONENT creature:")
        o_opts = [f"{c.name} Lv{c.level} [{c.element}]" for c in opp_player.creatures]
        o_ch   = pick("Opponent fighter", o_opts)
        if o_ch == -1:
            return
        opp_creature = opp_player.creatures[o_ch]

    run_battle(player_creature, opp_creature)


def run_battle(player_c: Creature, opp_c: Creature):
    bc_player = BattleCreature(player_c, is_player=True)
    bc_opp    = BattleCreature(opp_c,    is_player=False)
    battle    = Battle(bc_player, bc_opp)

    clear()
    banner("⚔  BATTLE START  ⚔")
    print(f"\n  {player_c.name} (Lv{player_c.level} {player_c.element.upper()})")
    print(f"    vs")
    print(f"  {opp_c.name} (Lv{opp_c.level} {opp_c.element.upper()})")
    time.sleep(1)

    while not battle.is_over:
        clear()
        banner(f"TURN {battle.turn}")

        # Status display
        print(f"\n  OPPONENT: {bc_opp.creature.name}")
        print(f"  HP  {hp_bar(bc_opp.current_hp, bc_opp.max_hp)}")
        print(f"  Status: {bc_opp.status or 'none'}")

        print(f"\n  YOU: {bc_player.creature.name}")
        print(f"  HP  {hp_bar(bc_player.current_hp, bc_player.max_hp)}")
        print(f"  ⚡  {energy_bar(bc_player.energy.current)}")
        print(f"  Status: {bc_player.status or 'none'}")

        # It's player's turn
        if battle.active == bc_player:
            print(f"\n  YOUR TURN — Choose a move:")
            move_options = ["Base Attack"]
            move_ids     = ["base_attack"]
            for m in bc_player.moves:
                move_options.append(f"{m['display_name']:20} PWR:{m['power']:3}  {m['element'].upper()}")
                move_ids.append(m["id"])
            if bc_player.energy.is_full:
                move_options.append("⚡ SPECIAL MOVE (energy full!)")
                move_ids.append("__special__")

            ch = pick("Move", move_options)
            if ch == -1:
                ch = 0

            use_special = move_ids[ch] == "__special__"
            move_id     = "base_attack" if (ch == 0 or use_special) else move_ids[ch]

            # Roll animation
            atk_roll = roll_d20()
            roll_animation(f"  {player_c.name} attacks with {move_options[ch]}!", atk_roll)

            result = battle.execute_turn(
                move_id     = move_id,
                attack_roll = atk_roll,
                use_special = use_special,
            )
        else:
            # Opponent turn — auto roll
            print(f"\n  {bc_opp.creature.name}'s turn...")
            time.sleep(0.8)
            opp_roll = roll_d20()
            roll_animation(f"  {bc_opp.creature.name} attacks!", opp_roll)
            result = battle.execute_turn(
                move_id     = "base_attack",
                attack_roll = opp_roll,
            )

        # Show result
        print(f"\n  Damage dealt : {result.get('damage_dealt', 0)}")
        if result.get("type_bonus") == "super_effective":
            print("  Super effective!")
        elif result.get("type_bonus") == "not_effective":
            print("  Not very effective...")
        if result.get("status_effect", {}) and result["status_effect"].get("applied"):
            print(f"  Status applied: {result['status_effect']['type'].upper()}")

        if battle.is_over:
            break
        time.sleep(0.8)

    # Battle over
    clear()
    banner("BATTLE OVER")
    winner = battle.winner.creature if battle.winner else None
    if winner:
        print(f"\n  🏆 {winner.name} WINS!")
        if winner == player_c:
            xp = opp_c.level * 15
            player_c.gain_xp(xp)
            print(f"  {player_c.name} gained {xp} XP!")
    pause()


# ─────────────────────────────────────────────
#  TRADE MENU
# ─────────────────────────────────────────────

def menu_trade():
    if not G.player:
        print("\n  Create a player first!"); pause(); return

    other_players = [name for name in G.players if name != G.active_name]
    if not other_players:
        print("\n  No other players to trade with. Create a second player first.")
        pause(); return

    clear()
    banner("TRADE")

    print("\n  Choose a player to trade with:")
    opp_choice = pick("Player", other_players)
    if opp_choice == -1:
        return

    receiver   = G.players[other_players[opp_choice]]
    proposer   = G.player

    clear()
    banner(f"TRADE: {proposer.name} → {receiver.name}")

    # Build offer
    offer = {"creatures": [], "cards": {}, "coins": 0}
    if proposer.creatures:
        print(f"\n  YOUR creatures (pick one to offer, or skip):")
        opts = [f"{c.name} Lv{c.level} [{c.element}]" for c in proposer.creatures] + ["Skip"]
        ch   = pick("Offer creature", opts)
        if ch != -1 and ch < len(proposer.creatures):
            offer["creatures"].append(proposer.creatures[ch].creature_id)

    # Build request
    request = {"creatures": [], "cards": {}, "coins": 0}
    if receiver.creatures:
        print(f"\n  {receiver.name}'s creatures (pick one to request):")
        opts = [f"{c.name} Lv{c.level} [{c.element}]" for c in receiver.creatures] + ["Skip"]
        ch   = pick("Request creature", opts)
        if ch != -1 and ch < len(receiver.creatures):
            request["creatures"].append(receiver.creatures[ch].creature_id)

    if not offer["creatures"] and not request["creatures"]:
        print("\n  Nothing to trade."); pause(); return

    session = propose_trade(proposer, receiver, offer, request)

    print(f"\n  {receiver.name}, do you accept this trade?")
    ch = pick("Decision", ["Accept", "Reject"])
    if ch == 0:
        result = session.accept()
    else:
        result = session.reject()
    print(f"\n  {result['message']}")
    pause()


# ─────────────────────────────────────────────
#  POKEDEX MENU
# ─────────────────────────────────────────────

def menu_pokedex():
    while True:
        clear()
        banner("WORLDHATCH POKEDEX — 100 CREATURES")

        region_ids = list_regions()
        options    = []
        for rid in region_ids:
            r   = REGIONS[rid]
            cnt = len(FULL_ROSTER[rid]["creatures"])
            options.append(f"{r['display_name']:28} {r['element'].upper():8} — {cnt} creatures")
        options.append("Search by element")
        options.append("Search by rarity")

        choice = pick("Browse", options)
        if choice == -1:
            return
        elif choice < len(region_ids):
            show_region_dex(region_ids[choice])
        elif choice == len(region_ids):
            search_by_element()
        else:
            search_by_rarity()


def show_region_dex(region_id: str):
    clear()
    region = REGIONS[region_id]
    banner(f"{region['display_name'].upper()} CREATURES")
    creatures = FULL_ROSTER[region_id]["creatures"]

    for c in creatures:
        rarity_icon = {"common": "○", "uncommon": "◑", "rare": "●", "legendary": "★"}
        icon = rarity_icon.get(c["rarity"], "○")
        print(f"  {icon} {c['name']:28} [{c['element']:7}] {c['rarity'].upper()}")
        print(f"      {c['description'][:65]}...")
        print()
    pause()


def search_by_element():
    elements = ["fire","ice","nature","spirit","dark","storm","water","sand","magma","crystal"]
    clear()
    banner("SEARCH BY ELEMENT")
    ch = pick("Element", elements)
    if ch == -1:
        return
    elem = elements[ch]
    clear()
    banner(f"{elem.upper()} CREATURES")
    for region_id, region_data in FULL_ROSTER.items():
        for c in region_data["creatures"]:
            if c["element"] == elem:
                r = REGIONS[region_id]["display_name"]
                print(f"  {c['name']:28} [{r}] {c['rarity'].upper()}")
                print(f"    {c['description'][:65]}...")
                print()
    pause()


def search_by_rarity():
    rarities = ["common","uncommon","rare","legendary"]
    clear()
    banner("SEARCH BY RARITY")
    ch = pick("Rarity", rarities)
    if ch == -1:
        return
    rarity = rarities[ch]
    clear()
    banner(f"{rarity.upper()} CREATURES")
    for region_id, region_data in FULL_ROSTER.items():
        for c in region_data["creatures"]:
            if c["rarity"] == rarity:
                r = REGIONS[region_id]["display_name"]
                print(f"  {c['name']:28} [{c['element']:7}] {r}")
                print(f"    {c['description'][:65]}...")
                print()
    pause()


# ─────────────────────────────────────────────
#  CARD SHOP MENU
# ─────────────────────────────────────────────

def menu_card_shop():
    if not G.player:
        print("\n  Create a player first!"); pause(); return

    while True:
        clear()
        banner("CARD SHOP")
        p = G.player
        print(f"  Your coins: {p.realm_coins} 🪙\n")

        SHOP_PRICES = {
            "ember_gene":       30,
            "frost_gene":       30,
            "verdant_gene":     30,
            "shadow_gene":      50,
            "vitality_shard":   25,
            "power_fragment":   35,
            "scorchwave_card":  60,
            "glacial_slam_card":60,
            "root_bind_card":   40,
            "blaze_path_card": 120,
        }

        options = []
        card_ids = []
        for card_id, price in SHOP_PRICES.items():
            card = CARDS.get(card_id, {})
            owned = p.card_inventory.get(card_id, 0)
            options.append(
                f"{card.get('display_name','?'):25} {price:3}🪙  "
                f"[{card.get('rarity','?'):9}]  owned:{owned}"
            )
            card_ids.append(card_id)

        choice = pick("Buy card", options)
        if choice == -1:
            return

        card_id = card_ids[choice]
        price   = SHOP_PRICES[card_id]

        if p.realm_coins < price:
            print(f"\n  Not enough coins! Need {price}, have {p.realm_coins}.")
        else:
            p.realm_coins -= price
            p.add_card(card_id, qty=1)
            print(f"\n  Purchased {CARDS[card_id]['display_name']}!")
        pause()


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    clear()
    print("""
  ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗ ██╗  ██╗ █████╗ ████████╗ ██████╗██╗  ██╗
  ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗██║  ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║
  ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║███████║███████║   ██║   ██║     ███████║
  ╚████╔╝ ██║╚██████╔╝██║  ██║███████╗██████╔╝██╔══██║██╔══██║   ██║   ╚██████╗██╔══██║
   ╚═══╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝
    """)
    print("  Creature Hatching & Trading — v0.1 CLI")
    print("  10 Regions | 100 Creatures | D20 Battle System")
    pause("Press ENTER to start...")
    main_menu()
