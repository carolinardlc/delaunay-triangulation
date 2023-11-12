from shapes import Punto, Triangulo


MIN_PUNTO_DISTANCIA = 10


def triangular(puntos: list[Punto]) -> set[Triangulo]:
    super_triangulo, max_x, max_y = encontrar_super_triangulo(puntos)
    triangulacion: set[Triangulo] = set([super_triangulo])

    for punto in puntos:
        triangulos_invalidos: set[Triangulo] = set()
        polygon = set()

        for tri in triangulacion:
            if tri.circulo.contiene_punto(punto):
                triangulos_invalidos.add(tri)

        all_edges = []
        for tri in triangulos_invalidos:
            all_edges.extend(tri.edges)

        for edge in all_edges:
            if all_edges.count(edge) == 1:
                polygon.add(edge)

        for tri in triangulos_invalidos:
            triangulacion.remove(tri)
            
        for edge in polygon:
            try:
                new_tri = Triangulo((edge.p1, edge.p2, punto))
                triangulacion.add(new_tri)
            except:
                pass

    # no incluir triangulos con puntos al borde de la imagen
    triangulos_validos: list[Triangulo] = []
    for tri in triangulacion:
        if es_triangulo_valido(tri, max_x, max_y):
            triangulos_validos.append(tri)

    return triangulos_validos


def es_triangulo_valido(triangulo: Triangulo, max_x: int, max_y: int) -> bool:
    for punto in triangulo.puntos:
        if punto.x <= MIN_PUNTO_DISTANCIA or punto.y <= MIN_PUNTO_DISTANCIA:
            return False
        if punto.x >= max_x - MIN_PUNTO_DISTANCIA or punto.y >= max_y - MIN_PUNTO_DISTANCIA:
            return False

    return True


def encontrar_super_triangulo(puntos: list[Punto]) -> tuple[Triangulo, int, int]:
    xs = [p.x for p in puntos]
    ys = [p.y for p in puntos]
    max_x = max(xs)
    max_y = max(ys)

    return (Triangulo([Punto(0,0), Punto(max_x * 2, 0), Punto(0, max_y * 2)]), max_x, max_y)
