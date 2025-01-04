import os
import numpy as np
from PIL import Image
import math
from tkinter import Tk, filedialog, messagebox

def load_images(route):

    """
    Loads images from a folder, converts them to numpy arrays,
    and returns them as a list.
    route -> absolute path where the images are located
    images -> list of numpy ndarray matrices
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
    print("Loaded", len(images), "images")
    return images

def pieces(image, w, h):

    """
    This function splits an image (np.array) into pieces, if the dimensions of the thumbnail images
    are divisible by the dimensions of the source image.
    Returns a list of images with the pieces.
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

def merge(thumbnail_list, w_thumbnail, h_thumbnail):

    """
    This code merges a list of images of width w_thumbnail and height h_thumbnail.
    """

    for i in range(len(thumbnail_list)):       ##Convert your list of np.array images to PIL format (image.fromarray)
        thumbnail_list[i] = Image.fromarray(thumbnail_list[i])
    p = int(round(math.sqrt(len(thumbnail_list))))
    white = Image.new(size=(w_thumbnail * p, h_thumbnail * p), mode="RGB")    # Creates a base to paste the images
    coordinates = []
    for x in range(0, white.size[0], w_thumbnail):
        for y in range(0, white.size[1], h_thumbnail):
            coordinates.append((x, y, x + w_thumbnail, y + h_thumbnail))
    for i in range(len(thumbnail_list)):      # Paste the images onto the base
        white.paste(thumbnail_list[i], (coordinates[i][0], coordinates[i][1]))
    return np.array(white, dtype=np.uint8)

def L1_Luminance_Color(a, b):
    """
    Calculates a combination of the color difference and luminance, normalizing the values.
    """
    color_distance = np.sum(np.abs(a - b)) / np.size(a)
    luminance_distance = abs(np.mean(a) - np.mean(b))
    return color_distance + luminance_distance

def chooseThumbnail(block, thumbnail_list):
    """
    Compares a block of a source image with a list of images,
    using the L1 function to find the most similar (minimum difference)
    """
    candidates = [L1_Luminance_Color(block, thumbnail) for thumbnail in thumbnail_list]
    index = np.argmin(candidates)
    return index

def chooseSecondThumbnail(block, thumbnail_list):
    """
    Compares a block of a source image with a list of images,
    using the L1 function to get the index of the second most similar image.
    """
    # Calculate differences with all thumbnails
    candidates = [L1_Luminance_Color(block, thumbnail) for thumbnail in thumbnail_list]

    # Find the index of the smallest value (most similar)
    first_index = np.argmin(candidates)

    # Temporarily replace the smallest value with a very large number
    candidates[first_index] = float('inf')

    # Find the index of the second smallest value
    second_index = np.argmin(candidates)

    return second_index

def resizeList(A, w, h):
    """
    Changes the height and width of a list of images of the same size
    using the previously defined nearestNeighbor function
    """
    for i in range(len(A)):
        A[i] = nearestNeighbor(A[i], w, h)
    return A

def nearestNeighbor(A, w, h):
    """
    Takes the dimensions of image A and divides them by the new given dimensions, w and h, using a for loop.
    """
    height, width = A.shape[0], A.shape[1]
    new_image = [[A[int(height * y / h)][int(width * x / w)]
                  for x in range(w)] for y in range(h)]
    return np.array(new_image)

def initMosaic(source, w, h, p):
    mHeight, mWidth = h * p, w * p
    return nearestNeighbor(source, mWidth, mHeight)

def constructMosaic(source, thumbnails, p):

    """
    Builds an image as a 2D bitmap (grayscale) from a base image (source),
    a list of thumbnails, and the number of thumbnails per side (p).
    """

    source = np.array(source)
    for i in range(len(thumbnails)):
        thumbnails[i] = np.array(thumbnails[i])
    sample = thumbnails[0]
    h, w, _ = sample.shape
    source = initMosaic(source, w, h, p)
    blocks = pieces(source, w, h)  # Splits the original image (source) into blocks
    area = pow(p, 2)

    indices = []
    past_index = 0
    for block in blocks:

        index = chooseThumbnail(block, thumbnails)

        while index == past_index:

             index = chooseSecondThumbnail(block, thumbnails)

        past_index = index

        indices.append(index)

    # Compares each block with all the thumbnail images and selects the most similar for each block

    selected = [thumbnails[i] for i in indices] # orders them
    mosaic = merge(selected, w, h)   # Merges the selected ones and returns the image mosaic

    return np.array(mosaic, dtype=np.uint8)

def select_folder():
    """
    Opens a window to select a folder, which should contain the images
    """
    Tk().withdraw()  # Hides the root window
    return filedialog.askdirectory(title="Select a folder")

def select_image():
    """
    Opens a window to select an image, using askopenfilename instead of askopenfile to avoid errors
    """

    Tk().withdraw()  # Hides the root window
    return Image.open(filedialog.askopenfilename(title="Select an image",
                                                 filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]))

def display_version():
    # Create the hidden main window
    Tk().withdraw()  # Hide the main window
    # Show a pop-up with the message
    messagebox.showinfo("MOSAIC VERSION", "MOSAIC_V1.1 DISPLAYED")


source = select_image()
miniatures = resizeList(load_images((select_folder())), 10, 10)

    # It is recommended to adjust the dimensions of the source images and the pixels of the resulting image
    # For example, for a picture of 2500 x 1875, use w:25, h:19 for 100 pixels.
    # For square pictures, w=h

Mosaic = constructMosaic(source, miniatures, 50)
Image_Result = Image.fromarray(Mosaic)
print("MOSAIC_V1.1 DISPLAYED")
Image_Result.show()


#   Nueva version Mosaico V1 con nueva funcion
#   Se agrega funcion, segunda miniatura que modifica construirmosaico para evitar que se repitan tantas miniaturas
#   Toma encuenta tanto distancia de color como luminancia (brillo). por eso hay color