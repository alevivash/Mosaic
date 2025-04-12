from PIL import Image, ImageDraw
import os, random

os.makedirs("colors", exist_ok=True)

for i in range(225):
    # Crear imagen y objeto para dibujar
    img = Image.new("RGB", (600, 600))
    draw = ImageDraw.Draw(img)

    # Generar colores aleatorios para el degradado
    color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Dibujar degradado vertical
    for y in range(600):
        r = int(color1[0] + (color2[0] - color1[0]) * y / 600)
        g = int(color1[1] + (color2[1] - color1[1]) * y / 600)
        b = int(color1[2] + (color2[2] - color1[2]) * y / 600)
        draw.line([(0, y), (599, y)], fill=(r, g, b))

    # 2. Dibujar círculos concéntricos
    center_x, center_y = 300, 300  # Centro de la imagen (600x600)
    max_radius = 300# Radio máximo (ajustable)
    num_circles = 15 # Número de círculos concéntricos

    for circle in range(1, num_circles + 1):
        radius = int(max_radius * circle / num_circles)  # Radio actual
        # Coordenadas del rectángulo delimitador (elipse)
        x1, y1 = center_x - radius, center_y - radius
        x2, y2 = center_x + radius, center_y + radius
        # Color del círculo (negro en este caso)
        draw.ellipse([(x1, y1), (x2, y2)], outline=(0, 0, 0), width=3)

    # Guardar imagen
    img.save(f"colors/color_gradient_noise_{i}.jpg")