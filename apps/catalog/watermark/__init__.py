import os
from PIL import Image, ImageSequence
from django.conf import settings


def watermark_img(path):
    watermark_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    original = Image.open(path)
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
    frames = ImageSequence.all_frames(original, lambda i: place_watermark(i, watermark, x, y))
    if len(frames) > 1:
        watermark_animated(original, frames, path)
    else:
        watermark_static(frames[0], path)


def watermark_animated(img: Image, frames: list[Image.Image], path):

    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=img.info.get("duration", 100),
        timestamp=img.info.get("timestamp", 4100),
        loop=0,
        minimize_size=True,
    )


def watermark_static(img, path):

    try:
        img.save(path)
    except OSError as e:
        img = img.convert("RGB")
        img.save(path)


def place_watermark(frame, watermark, x, y):
    frame = frame.convert("RGBA")
    frame.paste(watermark, (x, y), watermark)
    return frame
