"""
qr_generator.py — WORLDHATCH QR Code Generator
════════════════════════════════════════════════
Generates unique QR codes for physical card printing.

Each card gets one unique serial → one unique QR code.
Output options:
  - PNG image files (one per card)
  - A print sheet (multiple cards per page)
  - A CSV manifest of all serials in a batch

Requirements:
  pip install qrcode[pil] pillow

Run:
  python qr_generator.py

This will generate QR codes for all cards in a series
and save them to /output/qr/{series_id}/

TO GENERATE A SPECIFIC SERIES:
  Change GENERATE_SERIES at the bottom of this file.

TO GENERATE ONLY SPECIFIC CARD TYPES:
  Change GENERATE_CARDS list at the bottom.
"""

import os
import csv

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFont
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False
    print("⚠  qrcode/pillow not installed. Run: pip install qrcode[pil] pillow")
    print("   Serial generation will still work — just no image output.\n")

from cards_physical import SERIES_REGISTRY, build_serial


# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

OUTPUT_DIR      = "output/qr"       # where to save QR images
CARD_W          = 400               # card image width  (pixels)
CARD_H          = 560               # card image height (pixels)
QR_SIZE         = 280               # QR code size within card

# Colors
BG_COLOR        = "#1a1a2e"         # dark navy background
TEXT_COLOR      = "#f7c948"         # WORLDHATCH gold
BORDER_COLOR    = "#f7c948"

RARITY_COLORS = {
    "common":    "#aaaacc",
    "uncommon":  "#5aafff",
    "rare":      "#cc44ff",
    "legendary": "#ff9944",
}


# ─────────────────────────────────────────────
#  SERIAL GENERATION (no image dependencies)
# ─────────────────────────────────────────────

def generate_serials(series_id: str, card_short_ids: list = None) -> list:
    """
    Generate all serial strings for a series (or a subset of card types).
    Returns a list of serial strings.
    Does NOT require qrcode/pillow.

    Args:
        series_id:      e.g. "S1"
        card_short_ids: list of card types to generate, or None for all
    """
    series = SERIES_REGISTRY.get(series_id)
    if not series:
        raise ValueError(f"Unknown series: '{series_id}'")

    serials = []
    cards_to_gen = card_short_ids or list(series["cards"].keys())

    for short_id in cards_to_gen:
        card_entry = series["cards"].get(short_id)
        if not card_entry:
            print(f"  ⚠ '{short_id}' not found in {series_id}, skipping.")
            continue
        count = card_entry["print_count"]
        for i in range(1, count + 1):
            serials.append(build_serial(series_id, short_id, i))

    return serials


def export_manifest(series_id: str, serials: list, output_path: str = None):
    """
    Export a CSV manifest of all serials for record keeping.
    Useful for print shops and inventory tracking.
    """
    if not output_path:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, f"{series_id}_manifest.csv")

    with open(output_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["serial", "series", "card_short_id", "card_id",
                         "number", "rarity", "claimed"])
        series = SERIES_REGISTRY[series_id]
        for serial in serials:
            parts      = serial.split("-")
            short_id   = parts[2]
            number     = parts[3]
            card_entry = series["cards"].get(short_id, {})
            writer.writerow([
                serial,
                series_id,
                short_id,
                card_entry.get("card_id", ""),
                number,
                card_entry.get("rarity", ""),
                "NO",   # unclaimed at generation time
            ])

    print(f"  📋 Manifest saved: {output_path}")
    return output_path


# ─────────────────────────────────────────────
#  QR IMAGE GENERATION (requires qrcode/pillow)
# ─────────────────────────────────────────────

def generate_qr_image(serial: str, scan_base_url: str) -> "Image":
    """
    Generate a single QR code image for a serial.
    The QR encodes the full scan URL:
      e.g. https://yoursite.com/scan?code=WORLDHATCH-S1-EMBERGEN-00042
    """
    if not QR_AVAILABLE:
        raise RuntimeError("qrcode/pillow not installed.")

    scan_url = f"{scan_base_url}?code={serial}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=2,
    )
    qr.add_data(scan_url)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img


def generate_card_image(serial: str, scan_base_url: str) -> "Image":
    """
    Generate a full card image with QR code, serial number,
    card name, series, and rarity color border.
    """
    if not QR_AVAILABLE:
        raise RuntimeError("qrcode/pillow not installed.")

    parts      = serial.split("-")
    series_id  = parts[1]
    short_id   = parts[2]
    number     = parts[3]

    series     = SERIES_REGISTRY.get(series_id, {})
    card_entry = series.get("cards", {}).get(short_id, {})
    card_id    = card_entry.get("card_id", short_id)
    rarity     = card_entry.get("rarity", "common")
    rarity_color = RARITY_COLORS.get(rarity, "#aaaacc")

    # Base card
    card = Image.new("RGB", (CARD_W, CARD_H), BG_COLOR)
    draw = ImageDraw.Draw(card)

    # Rarity border
    border = 6
    draw.rectangle([0, 0, CARD_W-1, CARD_H-1],
                   outline=rarity_color, width=border)

    # Series label
    try:
        font_large  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_small  = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except Exception:
        font_large = font_medium = font_small = ImageFont.load_default()

    # WORLDHATCH title
    draw.text((CARD_W//2, 22), "WORLDHATCH",
              fill=TEXT_COLOR, font=font_large, anchor="mm")

    # Series name
    series_name = series.get("display_name", series_id)
    draw.text((CARD_W//2, 45), series_name,
              fill=rarity_color, font=font_small, anchor="mm")

    # Card name
    draw.text((CARD_W//2, 68), card_id.replace("_", " ").upper(),
              fill="#ffffff", font=font_medium, anchor="mm")

    # QR Code — centered
    qr_img    = generate_qr_image(serial, scan_base_url)
    qr_resized = qr_img.resize((QR_SIZE, QR_SIZE))
    qr_x      = (CARD_W - QR_SIZE) // 2
    qr_y      = 90
    card.paste(qr_resized, (qr_x, qr_y))

    # Serial number
    draw.text((CARD_W//2, qr_y + QR_SIZE + 18), serial,
              fill=TEXT_COLOR, font=font_small, anchor="mm")

    # Rarity label
    draw.text((CARD_W//2, qr_y + QR_SIZE + 38), f"◆ {rarity.upper()} ◆",
              fill=rarity_color, font=font_small, anchor="mm")

    # Scan instruction
    draw.text((CARD_W//2, CARD_H - 20),
              "Scan to redeem at WORLDHATCH",
              fill="#666688", font=font_small, anchor="mm")

    return card


def generate_batch(series_id: str,
                   scan_base_url: str,
                   card_short_ids: list = None,
                   images: bool = True):
    """
    Generate a full batch of QR codes for a series.

    Args:
        series_id:      e.g. "S1"
        scan_base_url:  your game's scan URL base
        card_short_ids: specific card types, or None for all
        images:         True = generate PNG files, False = manifest only
    """
    print(f"\n🃏 Generating batch for {series_id}...")
    serials = generate_serials(series_id, card_short_ids)
    print(f"   {len(serials)} cards to generate.")

    # Always export manifest
    export_manifest(series_id, serials)

    if not images or not QR_AVAILABLE:
        print("   Skipping image generation.")
        return serials

    # Generate card images
    out_dir = os.path.join(OUTPUT_DIR, series_id)
    os.makedirs(out_dir, exist_ok=True)

    for i, serial in enumerate(serials):
        try:
            img      = generate_card_image(serial, scan_base_url)
            filename = os.path.join(out_dir, f"{serial}.png")
            img.save(filename)
            if (i + 1) % 50 == 0:
                print(f"   Generated {i+1}/{len(serials)}...")
        except Exception as e:
            print(f"   ⚠ Failed {serial}: {e}")

    print(f"   ✅ Done! Cards saved to {out_dir}/")
    return serials


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    # ── Configure these before running ────────

    GENERATE_SERIES   = "S1"
    SCAN_BASE_URL     = "https://yoursite.com/scan"   # replace with real URL later

    # Set to a list like ["EMBERGEN", "FROSTGEN"] to generate only specific cards
    # Set to None to generate ALL cards in the series
    GENERATE_CARDS    = None

    # Set to False to skip image generation (manifest CSV only)
    GENERATE_IMAGES   = True

    # ── Run ───────────────────────────────────
    generate_batch(
        series_id      = GENERATE_SERIES,
        scan_base_url  = SCAN_BASE_URL,
        card_short_ids = GENERATE_CARDS,
        images         = GENERATE_IMAGES,
    )
