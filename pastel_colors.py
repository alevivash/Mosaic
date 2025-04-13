from PIL import Image
import os
import random

os.makedirs("pastel_colors", exist_ok=True)

def generate_pastel_color():
    # Genera componentes RGB en el rango pastel (180-255)
    # Manteniendo valores similares para baja saturación
    base = random.randint(100, 240)
    variation = random.randint(0, 50)
    return (
        base + variation,
        base + random.randint(-0, 30),
        base + random.randint(-60, 100)
    )

for i in range(60):  # Generará 50 imágenes pastel
    # Crear imagen con color pastel
    color = generate_pastel_color()
    img = Image.new("RGB", (600, 600), color)

    # Guardar imagen
    img.save(f"pastel_colors/pastel_{i}.jpg")