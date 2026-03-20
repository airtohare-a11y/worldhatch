"""
cards_physical.py — WORLDHATCH Physical Card System
════════════════════════════════════════════════════
Manages real-world printed cards with unique QR codes.

Each physical card has:
  - A unique serial number (no two cards are identical)
  - A batch/series ID (S1, S2, etc.)
  - A card type ID (links to CARDS in cards.py)
  - A claim status (unclaimed / claimed by player_id)

QR Code Format:
  WORLDHATCH-{SERIES}-{CARD_SHORT_ID}-{SERIAL}
  Example: WORLDHATCH-S1-EMBERGEN-00042

Flow:
  1. Admin generates a batch of QR codes (qr_generator.py)
  2. Codes are printed on physical cards
  3. Player scans → mobile browser → redeem_card()
  4. Card binds to player forever, effect fires immediately
  5. Serial marked as claimed — can never be claimed again

TO ADD A NEW SERIES:
  Add an entry to SERIES_REGISTRY below.
  Then use qr_generator.py to generate codes for that series.
"""

import json
import os
import hashlib
from datetime import datetime

# ─────────────────────────────────────────────
#  SERIES REGISTRY
#  Each series maps short card codes to full card IDs (from cards.py)
#  and defines how many cards were printed per type.
# ─────────────────────────────────────────────

SERIES_REGISTRY = {

    "S1": {
        "display_name":  "Series 1 — Origins",
        "release_date":  "2025-01-01",
        "description":   "The founding set. Fire, Ice, and Nature genes.",
        # card_short_id: { card_id, print_count, rarity }
        "cards": {
            "EMBERGEN":   {"card_id": "ember_gene",       "print_count": 500, "rarity": "common"},
            "FROSTGEN":   {"card_id": "frost_gene",       "print_count": 500, "rarity": "common"},
            "VERDGEN":    {"card_id": "verdant_gene",     "print_count": 500, "rarity": "common"},
            "SHADOWGEN":  {"card_id": "shadow_gene",      "print_count": 200, "rarity": "uncommon"},
            "VITALSHARD": {"card_id": "vitality_shard",   "print_count": 300, "rarity": "common"},
            "POWERFRAG":  {"card_id": "power_fragment",   "print_count": 300, "rarity": "uncommon"},
            "SCORCHWAVE": {"card_id": "scorchwave_card",  "print_count": 150, "rarity": "uncommon"},
            "GLACSLAM":   {"card_id": "glacial_slam_card","print_count": 150, "rarity": "uncommon"},
            "ROOTBIND":   {"card_id": "root_bind_card",   "print_count": 200, "rarity": "common"},
            "BLAZEPATH":  {"card_id": "blaze_path_card",  "print_count": 100, "rarity": "rare"},
            "ANCIFORM":   {"card_id": "ancient_form_card","print_count": 25,  "rarity": "legendary"},
        },
    },

    # Add Series 2, 3 etc. here following the same pattern
    # "S2": {
    #     "display_name": "Series 2 — Mutations",
    #     "cards": { ... }
    # },
}


# ─────────────────────────────────────────────
#  CLAIM DATABASE
#  In production this would be a real database.
#  For now we use a local JSON file: claimed_cards.json
#  Format: { "WORLDHATCH-S1-EMBERGEN-00042": { "player_id", "claimed_at" } }
# ─────────────────────────────────────────────

CLAIMS_FILE = "claimed_cards.json"


def _load_claims() -> dict:
    """Load the claims database from disk."""
    if not os.path.exists(CLAIMS_FILE):
        return {}
    with open(CLAIMS_FILE, "r") as f:
        return json.load(f)


def _save_claims(claims: dict):
    """Save the claims database to disk."""
    with open(CLAIMS_FILE, "w") as f:
        json.dump(claims, f, indent=2)


# ─────────────────────────────────────────────
#  QR CODE SERIAL FORMAT
# ─────────────────────────────────────────────

def build_serial(series_id: str, card_short_id: str, number: int) -> str:
    """
    Build a unique serial string for a physical card.
    Example: WORLDHATCH-S1-EMBERGEN-00042
    """
    return f"WORLDHATCH-{series_id}-{card_short_id}-{str(number).zfill(5)}"


def parse_serial(serial: str) -> dict:
    """
    Parse a scanned serial back into its components.
    Returns { game_id, series_id, card_short_id, number }
    or raises ValueError if malformed.
    """
    parts = serial.strip().upper().split("-")
    if len(parts) != 4 or parts[0] != "WORLDHATCH":
        raise ValueError(f"Invalid WORLDHATCH serial: '{serial}'")
    return {
        "game_id":       parts[0],
        "series_id":     parts[1],
        "card_short_id": parts[2],
        "number":        int(parts[3]),
    }


# ─────────────────────────────────────────────
#  CARD REDEMPTION
# ─────────────────────────────────────────────

def redeem_card(serial: str, player, creature=None) -> dict:
    """
    Main redemption function — called when a player scans a QR code.

    Args:
        serial:   The scanned serial string (e.g. WORLDHATCH-S1-EMBERGEN-00042)
        player:   Player object (from player.py)
        creature: Optional Creature object to apply the card to immediately.
                  If None, card goes to player's digital collection only.

    Returns:
        result dict: { success, message, card_id, effects_applied }
    """
    # ── Parse the serial ──────────────────────
    try:
        parsed = parse_serial(serial)
    except ValueError as e:
        return {"success": False, "message": str(e), "card_id": None}

    series_id     = parsed["series_id"]
    card_short_id = parsed["card_short_id"]

    # ── Validate series exists ────────────────
    series = SERIES_REGISTRY.get(series_id)
    if not series:
        return {"success": False,
                "message": f"Unknown series '{series_id}'.",
                "card_id": None}

    # ── Validate card type exists in series ───
    card_entry = series["cards"].get(card_short_id)
    if not card_entry:
        return {"success": False,
                "message": f"Card '{card_short_id}' not found in {series_id}.",
                "card_id": None}

    # ── Check if already claimed ──────────────
    claims = _load_claims()
    if serial in claims:
        claimed_by = claims[serial]["player_id"]
        if claimed_by == player.player_id:
            return {"success": False,
                    "message": "You already claimed this card.",
                    "card_id": None}
        else:
            return {"success": False,
                    "message": "This card has already been claimed by another player.",
                    "card_id": None}

    # ── Claim the card ────────────────────────
    card_id = card_entry["card_id"]
    claims[serial] = {
        "player_id":  player.player_id,
        "player_name": player.name,
        "card_id":    card_id,
        "claimed_at": datetime.now().isoformat(),
        "series":     series_id,
    }
    _save_claims(claims)

    # ── Add to player's digital collection ────
    player.add_card(card_id, qty=1)

    effects_applied = {}

    # ── Apply to creature if provided ─────────
    if creature:
        from cards import apply_card_to_creature
        result = apply_card_to_creature(card_id, creature)
        if result["success"]:
            effects_applied = result["changes"]
            # Remove from inventory since it was applied
            if player.card_inventory.get(card_id, 0) > 0:
                player.card_inventory[card_id] -= 1
                if player.card_inventory[card_id] == 0:
                    del player.card_inventory[card_id]

    msg = (f"✅ Card redeemed! '{card_id}' added to {player.name}'s collection."
           + (f" Applied to {creature.name}!" if creature and effects_applied else ""))

    return {
        "success":         True,
        "message":         msg,
        "card_id":         card_id,
        "series":          series_id,
        "rarity":          card_entry["rarity"],
        "effects_applied": effects_applied,
    }


def get_card_claim_status(serial: str) -> dict:
    """
    Check if a serial has been claimed without redeeming it.
    Useful for the web scan page to show status before committing.
    """
    claims = _load_claims()
    if serial in claims:
        return {"claimed": True, "by": claims[serial]["player_name"],
                "at": claims[serial]["claimed_at"]}
    return {"claimed": False}


def get_player_claimed_cards(player_id: str) -> list:
    """Return all serials claimed by a specific player."""
    claims = _load_claims()
    return [
        {"serial": serial, **data}
        for serial, data in claims.items()
        if data["player_id"] == player_id
    ]
