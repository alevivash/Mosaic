import os
import numpy as np
from PIL import Image
import math
from tkinter import Tk, filedialog, messagebox

def load_images(route):
    """
    Loads images from a folder, converts them to numpy arrays, and returns them as a list.
    route -> Absolute path where the images are located.
    images -> List of numpy ndarray arrays.
    """
    images = []
    directory = os.fsencode(route)
    os.chdir(route)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith((".jpg", ".jpeg")):
            img = Image.open(filename)
            img.load()
            data = np.asarray(img, dtype="uint8")
            print(data.shape)
            images.append(data)
            continue
        else:
            continue
    print("Loaded", len(images), "images\n")
    return images

def pieces(image, w, h):
    """
    This function cuts an image (np.array) into parts, given that the dimensions of the miniatures are divisible by the dimensions of the source image.
    It returns a list of images as parts.
    """
    image = Image.fromarray(image)
    width, height = image.size
    parts = []
    for x in range(0, width, w):
        for y in range(0, height, h):
            parts.append((x, y, x + w, y + h))
    for i in range(len(parts)):
        parts[i] = image.crop(parts[i])
        parts[i] = np.array(parts[i])
    return parts

def join_images(list_of_miniatures, w_miniature, h_miniature):
    """
    This code combines a list of images of width w_miniature and height h_miniature.
    """
    for i in range(len(list_of_miniatures)):  # Converts the list of np.array images to PIL format (image.fromarray)
        list_of_miniatures[i] = Image.fromarray(list_of_miniatures[i])
    p = int(round(math.sqrt(len(list_of_miniatures))))  # Calculate number of rows/columns in the mosaic
    white = Image.new(size=(w_miniature * p, h_miniature * p), mode="RGB")  # Create a blank canvas to paste the images
    coordinates = []
    for x in range(0, white.size[0], w_miniature):
        for y in range(0, white.size[1], h_miniature):
            coordinates.append((x, y, x + w_miniature, y + h_miniature))
    for i in range(len(list_of_miniatures)):  # Paste the images onto the blank canvas
        white.paste(list_of_miniatures[i], (coordinates[i][0], coordinates[i][1]))
    return np.array(white, dtype=np.uint8)

def choose_thumbnail(block, list_of_miniatures):
    """
    Compares a block from the source image with a list of images,
    using the L1 function to get the most similar (minimum difference) value.
    """
    candidates = [L2_color_luminance(block, miniature) for miniature in list_of_miniatures]
    index = np.argmin(candidates)
    return index

def resizeList(A, w, h):
    """
    Resizes a list of images to the specified width and height using the nearest neighbor method.
    """
    for i in range(len(A)):
        A[i] = nearest_neighbor(A[i], w, h)
    return A

def L2_color_luminance(a, b):  # Lenght between 2 points
    """
    Calcula una combinación de distancia euclidiana en el espacio de color y distancia Manhattan
    """
    color_distance = np.sqrt(np.sum((a - b) ** 2)) #L2
    luminance_distance = abs(np.mean(a) - np.mean(b)) #L1
    return color_distance + luminance_distance

def nearest_neighbor(A, w, h):
    """
    Resizes image A to the specified width and height using the nearest neighbor algorithm.
    """
    height, width = A.shape[0], A.shape[1]
    new_image = [[A[int(height * y / h)][int(width * x / w)]
                  for x in range(w)] for y in range(h)]
    return np.array(new_image)

def init_mosaic(source, w, h, p):
    """
    Initializes the mosaic by resizing the source image to the dimensions required for the mosaic.
    """
    mHeight, mWidth = h * p, w * p
    return nearest_neighbor(source, mWidth, mHeight)

def construct_mosaic(source, miniatures, p):
    """
    Builds an image as a 2D bitmap mosaic (grayscale) from a source image,
    a list of miniatures, and the number of miniatures per side (p).
    """
    source = np.array(source)
    for i in range(len(miniatures)):
        miniatures[i] = np.array(miniatures[i])
    exemplar = miniatures[0]
    h, w, _ = exemplar.shape
    source = init_mosaic(source, w, h, p)
    blocks = pieces(source, w, h)  # Cut the original source image into blocks
    area = pow(p, 2)
    indices = [choose_thumbnail(block, miniatures) for block in blocks]  # Compare each block with all miniatures and select the most similar for each block
    selected = [miniatures[i] for i in indices]
    mosaic = join_images(selected, w, h)  # Join the selected miniatures to create the final mosaic
    return np.array(mosaic, dtype=np.uint8)


def select_folder():
    """
    Opens a window to select a folder, which should contain the images
    """
    Tk().withdraw()  # Hides the root window
    return filedialog.askdirectory(title="Select a folder")

def select_image():
    """
    Opens a window where you can select an image. It uses askopenfilename instead of askopenfile to avoid errors.
    """
    Tk().withdraw()  # Hide the root window
    return Image.open(filedialog.askopenfilename(title="Select an image",
                                                 filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]))

def display_version():
    """
    Displays a pop-up with the version information.
    """
    Tk().withdraw()  # Hide the root window
    messagebox.showinfo("MOSAIC VERSION", "MOSAIC_V3.0 DISPLAYED")


source = select_image()
miniatures = resizeList(load_images((select_folder())), 10, 10)

    # It is recommended to adjust the dimensions of the source images and the pixels of the resulting image
    # For example, for a picture of 2500 x 1875, use w:25, h:19 for 100 pixels.
    # For square pictures, w=h

Mosaic = construct_mosaic(source, miniatures, 50)
Imagen = Image.fromarray(Mosaic)
print("MOSAIC_V3.0 DISPLAYED")
Imagen.show()

# Este es el que tiene mayor definicion la imagen, pero se ven menos los colores
# Se logra definir la imagen
# utiliza la suma de la distancias L1 y L2. L2 = distancia de color, L1 = luminancia brillo de color

