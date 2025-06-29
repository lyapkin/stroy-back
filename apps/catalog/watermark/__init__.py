import os
from PIL import Image
from django.conf import settings


def watermark_img(path):
    watermark_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    original = Image.open(path).convert("RGBA")
    watermark = Image.open(watermark_logo_path).convert("RGBA")

    # Resize watermark if needed (example: resize to 20% of original image width)
    watermark_width = int(original.width * 0.2)
    watermark_height = int(watermark_width * (watermark.height / watermark.width))
    watermark = watermark.resize((watermark_width, watermark_height))

    # Apply opacity
    alpha = watermark.split()[3]
    alpha = Image.eval(alpha, lambda x: int(x * 0.3))
    watermark.putalpha(alpha)

    # Paste watermark
    x = (original.width - watermark.width) // 2
    y = (original.height - watermark.height) // 2
    original.paste(watermark, (x, y), watermark)
    try:
        original.save(path)
    except OSError as e:
        original = original.convert("RGB")
        original.save(path)
