import sys
import os
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter
import numpy as np
from shapes import Punto, Triangulo
from delaunay import triangular

USAGE = "error: Espicifique un archivo imagen para realizar triangulación de delaunay"
MIN_PUNTO_DISTANCIA = 5
GRIS_CLARO = 20


def main():
    if len(sys.argv) <= 1:
        print(USAGE)
        return

    imagen_path = sys.argv[1]

    try:
        imagen_original = Image.open(imagen_path)
    except:
        print(f"No se podía encontrar la imagen '{imagen_path}'")
        return

    imagen_modificada = modificar_imagen(imagen_original)

    puntos = encontrar_puntos(imagen_modificada)
    triangulos = triangular(puntos)

    new_path = os.path.splitext(imagen_path)[0] + "-delaunay.png"
    draw_triangulacion(imagen_original, triangulos, new_path)


def modificar_imagen(imagen: Image) -> Image:
    imagen_modificada = imagen.convert('L') # greyscale
    imagen_modificada = imagen_modificada.filter(ImageFilter.FIND_EDGES) # encontrar bordes, la imangen sale muy oscura
    imagen_modificada = ImageEnhance.Brightness(imagen_modificada).enhance(10.0) # agrega brillo a la imagen
    imagen_modificada = imagen_modificada.filter(ImageFilter.GaussianBlur(1)) # blur

    return imagen_modificada


def draw_triangulacion(imagen: Image, triangulos: set[Triangulo], path: str):
    draw = ImageDraw.Draw(imagen)

    for tri in triangulos:
        for edge in tri.edges:
            draw.line([(edge.p1.x, edge.p1.y), (edge.p2.x, edge.p2.y)], fill="black", width=1)

    imagen.save(path)


def encontrar_puntos(imagen: Image) -> list[Punto]:
    pixeles = np.array(imagen)
    imagen_largo = len(pixeles)
    puntos: list[Punto] = []

    for y in range(0, imagen_largo, MIN_PUNTO_DISTANCIA):
        imagen_ancho = len(pixeles[y])
        for x in range(0, imagen_ancho, MIN_PUNTO_DISTANCIA):
            color_valor = pixeles[y][x]
            if color_valor >= GRIS_CLARO:
                puntos.append(Punto(x, y))

    return puntos


if __name__ == '__main__':
    main()
