import os
import numpy as np
from PIL import Image
import math
from tkinter import Tk, filedialog, messagebox

def cargar_imagenes(route):

    """
    Carga imagenes en una carpeta, la cual transformara en matrices numpy
    y los devolvera en una lista
    route -> direccion absoluta donde se encuentran las imagenes
    images -> lista de matrices de numpy ndarray
    """

    imagenes = []
    directory = os.fsencode(route)
    os.chdir(route)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith((".jpg", ".jpeg")):
            img = Image.open(filename)
            img.load()
            data = np.asarray(img, dtype="uint8")
            print(data.shape)
            imagenes.append(data)
            continue
        else:
            continue
    print("Se cargaron", len(imagenes), "imágenes")
    return imagenes

def piezas(image, w, h):

    """
    Esta función se encarga de cortar una imagen (np.array) en partes, si las dimensiones de la imagenes miniaturas son divisibles entre las dimensiones de la imagen source.
    Devuelve una lista de imágenes con las partes
    """

    image = Image.fromarray(image)
    width, height = image.size
    partes = []
    for x in range(0, width, w):
        for y in range(0, height, h):
            partes.append((x, y, x + w, y + h))
    for i in range(len(partes)):
        partes[i] = image.crop(partes[i])
        partes[i] = np.array(partes[i])
    return partes

def unir(lista_de_miniaturas, w_miniatura, h_miniatura):

    """
    Este código se encarga de unir una lista de imagenes de w_miniatura de ancho, por h_miniaturas de alto.
    """

    for i in range(len(lista_de_miniaturas)):       ##Convierte tu lista de np.array de imagenes a formato PIL (image.fromarray)
        lista_de_miniaturas[i] = Image.fromarray(lista_de_miniaturas[i])
    p = int(round(math.sqrt(len(lista_de_miniaturas))))
    blanco = Image.new(size=(w_miniatura * p, h_miniatura * p), mode="RGB")    # Crea una base en donde pegar las images
    coordenadas = []
    for x in range(0, blanco.size[0], w_miniatura):
        for y in range(0, blanco.size[1], h_miniatura):
            coordenadas.append((x, y, x + w_miniatura, y + h_miniatura))
    for i in range(len(lista_de_miniaturas)):      # Pega las imagenes en la base
        blanco.paste(lista_de_miniaturas[i], (coordenadas[i][0], coordenadas[i][1]))
    return np.array(blanco, dtype=np.uint8)

def L1_Luminance_Color(a, b):
    """
    Calcula una combinación de la diferencia de color y luminancia, normalizando los valores.
    """
    color_distance = np.sum(np.abs(a - b)) / np.size(a)
    luminance_distance = abs(np.mean(a) - np.mean(b))
    return color_distance + luminance_distance

def escogerMiniatura(bloque, lista_miniaturas):
    """
    Compara un bloque de una imagen source con una lista de imagenes,
    usando la función L1 para obtener el valor más parecido (mínima diferencia)
    """
    candidatos = [L1_Luminance_Color(bloque, miniatura) for miniatura in lista_miniaturas]
    index = np.argmin(candidatos)
    return index


def escogerSegundaMiniatura(bloque, lista_miniaturas):
    """
    Compara un bloque de una imagen source con una lista de imágenes,
    usando la función L1 para obtener el índice de la segunda imagen más parecida.
    """
    # Calculamos las diferencias con todas las miniaturas
    candidatos = [L1_Luminance_Color(bloque, miniatura) for miniatura in lista_miniaturas]

    # Encontramos el índice del valor más pequeño (más parecido)
    index_primero = np.argmin(candidatos)

    # Reemplazamos el valor más pequeño con un número muy grande temporalmente
    candidatos[index_primero] = float('inf')

    # Encontramos el índice del segundo valor más pequeño
    index_segundo = np.argmin(candidatos)

    return index_segundo


def pixel_alert():

    """
        Prevents the same source image for nearby pixels
    """
    return 0

def listaRedim(A, w, h):
    """
    Cambia la altura y el ancho de una lista de imágenes del mismo tamaño por medio de la función vecinoProximo
    anteriormente nombrada
    """
    for i in range(len(A)):
        A[i] = vecinoProximo(A[i], w, h)
    return A

def vecinoProximo(A, w, h):
    """
    Toma las dimensiones de la imagen A y las divide entre las nuevas dimensiones dadas, w y h. A través de un bucle for
    """
    altura, ancho = A.shape[0], A.shape[1]
    new_image = [[A[int(altura * y / h)][int(ancho * x / w)]
                  for x in range(w)] for y in range(h)]
    return np.array(new_image)


def initMosaico(source, w, h, p):
    mAltura, mAncho = h * p, w * p
    return vecinoProximo(source, mAncho, mAltura)

def construirMosaico(source, miniaturas, p):

    """
    Construye una imagen como un mapa de bits de dos dimensiones (escala de grises) con una imagen base(source),
    una lista de miniaturas y la cantidad de miniaturas por lado (p).

    """

    source = np.array(source)
    for i in range(len(miniaturas)):
        miniaturas[i] = np.array(miniaturas[i])
    ejemplar = miniaturas[0]
    h, w, _ = ejemplar.shape
    source = initMosaico(source, w, h, p)
    bloques = piezas(source, w, h)  # Corta en bloques la imagen original(source)
    area = pow(p, 2)

    indices = []
    past_index = 0
    for bloque in bloques:

        index = escogerMiniatura(bloque, miniaturas)

        while index == past_index:

             index = escogerSegundaMiniatura(bloque, miniaturas)

        past_index = index

        indices.append(index)

    # Compara cada bloque con todos las imagenes miniatura y selecciona el orden el más parecido para cada bloque

    elegidas = [miniaturas[i] for i in indices] # las ordena
    mosaico = unir(elegidas, w, h)   # Une las elegidas y retorna el mosaico de imagenes

    return np.array(mosaico, dtype=np.uint8)

def seleccionar_carpeta():

    """
    Abre una ventana y seleccionas una carpeta, la cual debe contener a las imagenes
    """
    Tk().withdraw()  # Oculta la ventana raíz
    return filedialog.askdirectory(title="Selecciona una carpeta")

def seleccionar_imagen():
    """
    Abre una ventana y seleccionas una imagen, se debe usar askopenfilename y no askopenfile porque si no da error
    """

    Tk().withdraw()  # Oculta la ventana raíz
    return Image.open(filedialog.askopenfilename(title="Selecciona una imagen",
                                                 filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]))

def display_version():
    # Crear la ventana principal oculta
    Tk().withdraw()  # Ocultar la ventana principal
    # Mostrar un pop-up con el mensaje
    messagebox.showinfo("MOSAIC VERSION", "MOSAIC_V1.1 DISPLAYED")


source = seleccionar_imagen()
miniaturas = listaRedim(cargar_imagenes((seleccionar_carpeta())), 10, 10)

    # It is recommended to adjust the dimensions of the source images and the pixels of the resulting image
    # For example for a pictue of 2500 x 1875 use w:25, h:19 for 100 pixels.
    # For square pictures w=h

Mosaic = construirMosaico(source, miniaturas, 40)
Imagen = Image.fromarray(Mosaic)
print("MOSAIC_V1.1 DISPLAYED")
Imagen.show()

#   Nueva version Mosaico V1 con nueva funcion
#   Se agrega funcion, segunda miniatura que modifica construirmosaico para evitar que se repitan tantas miniaturas
#   Toma encuenta tanto distancia de color como luminancia (brillo). por eso hay color