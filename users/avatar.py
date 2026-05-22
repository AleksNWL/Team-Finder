import hashlib
import io

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

SLATE = (91, 107, 128)
OLIVE = (107, 128, 91)
TAN = (128, 107, 91)
TEAL = (91, 128, 107)
PURPLE = (107, 91, 128)
ROSE = (128, 91, 107)

PALETTE = [SLATE, OLIVE, TAN, TEAL, PURPLE, ROSE]

AVATAR_SIZE = 128
AVATAR_FONT_SIZE_RATIO = 0.5
AVATAR_TEXT_COLOR = (255, 255, 255)
AVATAR_ANCHOR_Y_OFFSET = 4
AVATAR_FALLBACK_FONT_SIZE = 64


def _background_color(name):
    digest = hashlib.md5(name.encode("utf-8")).hexdigest()
    return PALETTE[int(digest[:8], 16) % len(PALETTE)]


def _load_font(size):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default(size=size)


def build_avatar_file(name):
    letter = (name or "?")[0].upper()
    size = AVATAR_SIZE
    font_size = max(int(size * AVATAR_FONT_SIZE_RATIO), AVATAR_FALLBACK_FONT_SIZE)
    image = Image.new("RGB", (size, size), _background_color(name))
    draw = ImageDraw.Draw(image)
    font = _load_font(font_size)
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = (
        (size - text_width) / 2,
        (size - text_height) / 2 - AVATAR_ANCHOR_Y_OFFSET,
    )
    draw.text(position, letter, fill=AVATAR_TEXT_COLOR, font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"{letter.lower()}_avatar.png")
