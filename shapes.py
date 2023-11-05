from __future__ import annotations
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True, eq=True)
class Punto:
    x: int
    y: int

    def distancia(self, otro: Punto) -> float:
        return sqrt((self.x - otro.x) ** 2 + (self.y - otro.y) ** 2)

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.x and self.y == __o.y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass(frozen=True, eq=True)
class Edge:
    p1: Punto
    p2: Punto

    def __eq__(self, __o: Edge) -> bool:
        return (self.p1 == __o.p1 and self.p2 == __o.p2) or (self.p1 == __o.p2 and self.p2 == __o.p1)


class Circulo:
    centro: Punto
    radio: float

    def __init__(self, triangulo: Triangulo) -> None:
        [a, b, c] = triangulo.puntos
        self.centro = calcular_centro(a, b, c)
        self.radio = calcular_radio(a, b, c)
        if self.radio == 0:
            raise Exception("triangulo invalido")

    def contiene_punto(self, punto: Punto) -> bool:
        return punto.distancia(self.centro) < self.radio


def calcular_centro(a: Punto, b: Punto, c: Punto) -> Punto:
    determinante = 2 * (a.x * (b.y - c.y) + b.x * (c.y - a.y) + c.x * (a.y - b.y))
    # if determinante == 0:
    #     return None

    circulo_x = (a.x**2 + a.y**2) * (b.y - c.y) + (b.x**2 + b.y**2) * (c.y - a.y) + (c.x**2 + c.y**2) * (a.y - b.y)
    circulo_y = (a.x**2 + a.y**2) * (c.x - b.x) + (b.x**2 + b.y**2) * (a.x - c.x) + (c.x**2 + c.y**2) * (b.x - a.x)

    return Punto(circulo_x / determinante, circulo_y / determinante)


def calcular_radio(a: Punto, b: Punto, c: Punto) -> float:
        ab = a.distancia(b)
        bc = b.distancia(c)
        ca = c.distancia(a)
        s = 0.5 * (ab + bc + ca)
        area = sqrt(s * (s - ab) * (s - bc) * (s - ca))
        if area == 0:
            return 0

        return (ab * bc * ca) / (4 * area)


class Triangulo:
    edges: list[Edge]
    puntos: tuple[Punto, Punto, Punto]
    circulo: Circulo

    def __repr__(self) -> str:
        # return f"{self.puntos[0]}, {self.puntos[1]}, {self.puntos[2]}"
        return f"{self.edges[0]}, {self.edges[1]}, {self.edges[2]}"

    def __init__(self, puntos: tuple[Punto, Punto, Punto]) -> None:
        self.edges = [
            Edge(puntos[0], puntos[1]),
            Edge(puntos[1], puntos[2]),
            Edge(puntos[2], puntos[0])
        ]
        self.puntos = puntos
        self.circulo = Circulo(self)


    def contiene_punto(self, punto: Punto) -> bool:
        pass
