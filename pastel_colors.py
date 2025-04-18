"""
Generates 60 pastel-colored images (600x600px) with soft color variations.
Each image features:
1. A solid pastel color background (RGB values in specific ranges)
2. Colors maintain low saturation by keeping similar base values
3. Saved as JPG files in a 'pastel_colors' directory
"""

from PIL import Image
import os
import random

# Create output directory for pastel colors
os.makedirs("pastel_colors", exist_ok=True)


def generate_pastel_color():
    """
    Generates a random pastel color by:
    1. Starting with a base value (100-240)
    2. Adding controlled variations to each RGB channel
    3. Keeping values similar to maintain low saturation
    """
    base = random.randint(100, 240)  # Base color intensity
    variation = random.randint(0, 50)  # Primary variation
    return (
        base + variation,  # Red channel
        base + random.randint(0, 30),  # Green channel (smaller variation)
        base + random.randint(-60, 100)  # Blue channel (widest variation)
    )


# Generate 60 pastel color images
for i in range(60):
    # Create image with generated pastel color
    color = generate_pastel_color()
    img = Image.new("RGB", (600, 600), color)

    # Save image with sequential numbering
    img.save(f"pastel_colors/pastel_{i:02d}.jpg")  # 2-digit numbering