"""
Generates 350 gradient images (600x600px) with concentric circles.
Each image features:
1. A unique vertical color gradient background
2. 9 concentric black circles (1px outline) centered in the image
3. Saved as JPG files in a 'colors' directory
"""

from PIL import Image, ImageDraw
import os
import random

# Create output directory if it doesn't exist
os.makedirs("colors", exist_ok=True)

for i in range(350):
    # Initialize blank image and drawing context
    img = Image.new("RGB", (600, 600))
    draw = ImageDraw.Draw(img)

    # Generate two random colors for gradient
    color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Create vertical gradient by drawing horizontal lines
    for y in range(600):
        # Calculate gradient color at current y-position
        r = int(color1[0] + (color2[0] - color1[0]) * y / 600)
        g = int(color1[1] + (color2[1] - color1[1]) * y / 600)
        b = int(color1[2] + (color2[2] - color1[2]) * y / 600)
        draw.line([(0, y), (599, y)], fill=(r, g, b))

    # Draw concentric circles configuration
    center_x, center_y = 300, 300  # Image center point
    max_radius = 250  # Largest circle radius
    circle_count = 9  # Total number of circles

    # Draw each concentric circle
    for circle in range(1, circle_count + 1):
        current_radius = int(max_radius * circle / circle_count)
        # Calculate bounding box coordinates
        x1 = center_x - current_radius
        y1 = center_y - current_radius
        x2 = center_x + current_radius
        y2 = center_y + current_radius
        # Draw circle outline
        draw.ellipse([(x1, y1), (x2, y2)], outline=(0, 0, 0), width=1)

    # Save final image
    img.save(f"colors/color_gradient_circles_{i:03d}.jpg")