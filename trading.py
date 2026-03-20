"""
trading.py — WORLDHATCH Trading System
════════════════════════════════════════
Handles player-to-player trades of creatures, eggs, and cards.

Trade Flow:
  1. Player A proposes a trade (TradeProposal)
  2. Player B reviews and accepts or rejects
  3. If accepted, TradeSession.execute() transfers assets

Rules enforced:
  - You can only offer things you own
  - Trades can include coins as a balancer
  - Creatures from their home region get a note (collectors love them)
  - A trade log is kept for history

TO EXPAND:
  - Add an auction system
  - Add region-locked trades (some creatures can only trade in their home region)
  - Add trade cooldowns
"""

import uuid
from datetime import datetime


# ─────────────────────────────────────────────
#  TRADE PROPOSAL
# ─────────────────────────────────────────────

class TradeProposal:
    """
    Represents an offer from one player to another.
    Either player can offer creatures, eggs, cards, and/or coins.
    """

    def __init__(self,
                 proposer,           # Player object
                 receiver,           # Player object
                 offer: dict,        # what proposer offers
                 request: dict):     # what proposer wants
        """
        offer / request format:
        {
            "creatures": ["creature_id1", ...],
            "eggs":      ["egg_id1", ...],
            "cards":     {"card_id": qty, ...},
            "coins":     int
        }
        """
        self.trade_id    = str(uuid.uuid4())[:8]
        self.proposer    = proposer
        self.receiver    = receiver
        self.offer       = offer
        self.request     = request
        self.status      = "pending"    # pending | accepted | rejected | cancelled
        self.created_at  = datetime.now().isoformat()

    def describe(self) -> str:
        """Human-readable trade summary."""
        def fmt_side(player, side):
            lines = [f"  [{player.name} offers]"]
            for cid in side.get("creatures", []):
                c = player.get_creature(cid)
                label = f"{c.name} lv{c.level}" if c else cid
                home  = " 🏠" if (c and c.home_region == c.current_region) else ""
                lines.append(f"    🐾 {label}{home}")
            for eid in side.get("eggs", []):
                e = next((eg for eg in player.eggs if eg.egg_id == eid), None)
                label = e.display_name if e else eid
                lines.append(f"    🥚 {label}")
            for card_id, qty in side.get("cards", {}).items():
                lines.append(f"    🃏 {card_id} x{qty}")
            coins = side.get("coins", 0)
            if coins:
                lines.append(f"    🪙 {coins} realm coins")
            return "\n".join(lines)

        return (
            f"\n┌── TRADE PROPOSAL [{self.trade_id}] ──────────────────\n"
            f"{fmt_side(self.proposer, self.offer)}\n"
            f"  ──── FOR ────\n"
            f"{fmt_side(self.receiver, self.request)}\n"
            f"└──────────────────────────────────────────────────\n"
        )

    def validate(self) -> tuple[bool, str]:
        """
        Check that both sides actually own what they're offering/being asked for.
        Returns (True, "") or (False, reason).
        """
        # Proposer has their offered items
        for cid in self.offer.get("creatures", []):
            if not self.proposer.get_creature(cid):
                return False, f"Proposer doesn't own creature '{cid}'."
        for eid in self.offer.get("eggs", []):
            if not any(e.egg_id == eid for e in self.proposer.eggs):
                return False, f"Proposer doesn't own egg '{eid}'."
        for card_id, qty in self.offer.get("cards", {}).items():
            if self.proposer.card_inventory.get(card_id, 0) < qty:
                return False, f"Proposer doesn't have enough '{card_id}'."
        if self.offer.get("coins", 0) > self.proposer.realm_coins:
            return False, "Proposer doesn't have enough coins."

        # Receiver has their requested items
        for cid in self.request.get("creatures", []):
            if not self.receiver.get_creature(cid):
                return False, f"Receiver doesn't own creature '{cid}'."
        for eid in self.request.get("eggs", []):
            if not any(e.egg_id == eid for e in self.receiver.eggs):
                return False, f"Receiver doesn't own egg '{eid}'."
        for card_id, qty in self.request.get("cards", {}).items():
            if self.receiver.card_inventory.get(card_id, 0) < qty:
                return False, f"Receiver doesn't have enough '{card_id}'."
        if self.request.get("coins", 0) > self.receiver.realm_coins:
            return False, "Receiver doesn't have enough coins."

        return True, ""


# ─────────────────────────────────────────────
#  TRADE SESSION — executes the actual transfer
# ─────────────────────────────────────────────

class TradeSession:
    """
    Manages the lifecycle of a single trade between two players.
    """

    # Global trade log (in production, this would be a DB)
    trade_log = []

    def __init__(self, proposal: TradeProposal):
        self.proposal = proposal

    def accept(self) -> dict:
        """
        Called by the receiver to accept the trade.
        Validates ownership then transfers all assets.
        Returns a result dict.
        """
        prop = self.proposal

        valid, reason = prop.validate()
        if not valid:
            prop.status = "invalid"
            return {"success": False, "message": f"Trade invalid: {reason}"}

        # ── Transfer proposer → receiver ──────────
        self._transfer_creatures(prop.proposer, prop.receiver,
                                 prop.offer.get("creatures", []))
        self._transfer_eggs(prop.proposer, prop.receiver,
                            prop.offer.get("eggs", []))
        self._transfer_cards(prop.proposer, prop.receiver,
                             prop.offer.get("cards", {}))
        self._transfer_coins(prop.proposer, prop.receiver,
                             prop.offer.get("coins", 0))

        # ── Transfer receiver → proposer ──────────
        self._transfer_creatures(prop.receiver, prop.proposer,
                                 prop.request.get("creatures", []))
        self._transfer_eggs(prop.receiver, prop.proposer,
                            prop.request.get("eggs", []))
        self._transfer_cards(prop.receiver, prop.proposer,
                             prop.request.get("cards", {}))
        self._transfer_coins(prop.receiver, prop.proposer,
                             prop.request.get("coins", 0))

        prop.status = "accepted"
        log_entry = {
            "trade_id":   prop.trade_id,
            "proposer":   prop.proposer.player_id,
            "receiver":   prop.receiver.player_id,
            "completed":  datetime.now().isoformat(),
        }
        TradeSession.trade_log.append(log_entry)

        msg = (f"✅ Trade [{prop.trade_id}] completed! "
               f"{prop.proposer.name} ↔ {prop.receiver.name}")
        print(msg)
        return {"success": True, "message": msg}

    def reject(self) -> dict:
        self.proposal.status = "rejected"
        msg = f"❌ Trade [{self.proposal.trade_id}] rejected by {self.proposal.receiver.name}."
        print(msg)
        return {"success": False, "message": msg}

    def cancel(self) -> dict:
        self.proposal.status = "cancelled"
        msg = f"🚫 Trade [{self.proposal.trade_id}] cancelled by {self.proposal.proposer.name}."
        print(msg)
        return {"success": False, "message": msg}

    # ── Internal Transfer Helpers ──────────────

    @staticmethod
    def _transfer_creatures(sender, recipient, creature_ids: list):
        for cid in creature_ids:
            creature = sender.get_creature(cid)
            if creature:
                sender.remove_creature(cid)
                recipient.add_creature(creature)
                print(f"  🔄 {creature.name} → {recipient.name}")

    @staticmethod
    def _transfer_eggs(sender, recipient, egg_ids: list):
        for eid in egg_ids:
            egg = next((e for e in sender.eggs if e.egg_id == eid), None)
            if egg:
                sender.eggs.remove(egg)
                recipient.add_egg(egg)
                print(f"  🔄 {egg.display_name} → {recipient.name}")

    @staticmethod
    def _transfer_cards(sender, recipient, cards: dict):
        for card_id, qty in cards.items():
            if sender.card_inventory.get(card_id, 0) >= qty:
                sender.card_inventory[card_id] -= qty
                if sender.card_inventory[card_id] == 0:
                    del sender.card_inventory[card_id]
                recipient.add_card(card_id, qty)
                print(f"  🔄 {card_id} x{qty} → {recipient.name}")

    @staticmethod
    def _transfer_coins(sender, recipient, amount: int):
        if amount > 0:
            sender.realm_coins    -= amount
            recipient.realm_coins += amount
            print(f"  🔄 {amount} coins → {recipient.name}")


# ─────────────────────────────────────────────
#  CONVENIENCE FUNCTION
# ─────────────────────────────────────────────

def propose_trade(proposer, receiver, offer: dict, request: dict) -> TradeSession:
    """
    Shorthand to create a trade proposal and return a TradeSession ready to accept/reject.

    Example:
        session = propose_trade(
            proposer = alice,
            receiver = bob,
            offer    = {"creatures": [alice_creature.creature_id], "coins": 50},
            request  = {"creatures": [bob_creature.creature_id]}
        )
        print(session.proposal.describe())
        session.accept()   # or session.reject()
    """
    proposal = TradeProposal(proposer, receiver, offer, request)
    print(proposal.describe())
    return TradeSession(proposal)
