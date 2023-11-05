from copy import copy
from shapes import Edge, Punto, Triangulo


def triangular(puntos: list[Punto]) -> set[Triangulo]:
        super_triangulo = encontrar_super_triangulo(puntos)
        triangulacion: set[Triangulo] = set([super_triangulo])
        puntos_restantes = copy(puntos)

        for punto in puntos:
            puntos_restantes.remove(punto)
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

        # Remove all edges containing points from the super triangle
        tris = set(triangulacion)
        hull = []
        for tri in triangulacion:
            for p in super_triangulo.puntos:
                if tri.contiene_punto(p) and tri in tris:

                    # Create the convex hull of the triangulation
                    points = tri.puntos
                    i = points.index(p)
                    ps = points[:i] + points[i+1:]
                    hull.append(Edge(*ps))

                    # Remove triangle from triangulation if it includes a vertex from the super tri
                    tris.remove(tri)

        # Remove the last of the edges in the convex hull. i.e. the edges in tris where two of the verts were in the supertriangle
        h = set(hull)
        for e in hull:
            if e.p1 in super_triangulo.puntos or e.p2 in super_triangulo.puntos:
                h.remove(e)

        # Return final triangulation
        return tris


def encontrar_super_triangulo(puntos: list[Punto]) -> Triangulo:
    xs = [p.x for p in puntos]
    ys = [p.y for p in puntos]

    return Triangulo([Punto(0,0), Punto(max(xs) * 2, 0), Punto(0, max(ys) * 2)])
