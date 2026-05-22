import hashlib
import io

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


PALETTE = [
    (91, 107, 128),
    (107, 128, 91),
    (128, 107, 91),
    (91, 128, 107),
    (107, 91, 128),
    (128, 91, 107),
]


def _background_color(name):
    digest = hashlib.md5(name.encode("utf-8")).hexdigest()
    return PALETTE[int(digest[:8], 16) % len(PALETTE)]


def build_avatar_file(name):
    letter = (name or "?")[0].upper()
    size = 128
    image = Image.new("RGB", (size, size), _background_color(name))
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 64)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size - text_width) / 2, (size - text_height) / 2 - 4)
    draw.text(position, letter, fill=(255, 255, 255), font=font)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"{letter.lower()}_avatar.png")
