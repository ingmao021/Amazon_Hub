
from abc import ABC, abstractmethod
from typing import Any, Optional


class InterfazArray(ABC):

    @abstractmethod
    def esta_vacia(self) -> bool: ...

    @abstractmethod
    def tamano(self) -> int: ...

    @abstractmethod
    def limpiar(self) -> None: ...

    @abstractmethod
    def insertar(self, indice: int, elemento: Any) -> None: ...

    @abstractmethod
    def obtener(self, indice: int) -> Optional[Any]: ...

    @abstractmethod
    def eliminar(self, indice: int) -> Optional[Any]: ...

    @abstractmethod
    def buscar_por_categoria(self, categoria: str) -> list: ...

    @abstractmethod
    def capacidad_total(self) -> int: ...

    @abstractmethod
    def obtener_array_completo(self) -> list: ...


# Modelo de datos 
class ProductoEstanteria:

    CATEGORIAS_VALIDAS = (
        "Electrónica", "Muebles", "Alimentos",
        "Ropa", "Herramientas", "Farmacia", "Deportes", "Otros",
    )

    def __init__(self, codigo_pasillo: str, nombre: str, categoria: str):
        if categoria not in self.CATEGORIAS_VALIDAS:
            raise ValueError(f"Categoría '{categoria}' no válida.")
        self.codigo_pasillo = codigo_pasillo
        self.nombre         = nombre
        self.categoria      = categoria

    def a_dict(self) -> dict:
        return {
            "Pasillo": self.codigo_pasillo,
            "Producto": self.nombre,
            "Categoría": self.categoria,
        }

    def __repr__(self) -> str:
        return f"Producto({self.codigo_pasillo}, {self.nombre}, {self.categoria})"


# Array estático
class ArrayAlmacen(InterfazArray):
    """
    Implementación concreta del Array de posiciones fijas.
    insertar() → O(1)
    obtener()  → O(1)
    eliminar() → O(1)
    buscar_por_categoria() → O(n)
    """

    def __init__(self, capacidad: int = 12):
        if capacidad < 1:
            raise ValueError("La capacidad debe ser al menos 1.")
        self._capacidad: int = capacidad
        self._array: list[Optional[ProductoEstanteria]] = [None] * capacidad
        self._precargar_datos()

    def _precargar_datos(self) -> None:
        """OCP: Sobrescribible en subclases para distintos catálogos."""
        datos = [

        ]
        for i, (pasillo, nombre, cat) in enumerate(datos):
            self._array[i] = ProductoEstanteria(pasillo, nombre, cat)

    def insertar(self, indice: int, elemento: ProductoEstanteria) -> None:
        self._validar_indice(indice)
        self._array[indice] = elemento

    def obtener(self, indice: int) -> Optional[ProductoEstanteria]:
        self._validar_indice(indice)
        return self._array[indice]

    def eliminar(self, indice: int) -> Optional[ProductoEstanteria]:
        self._validar_indice(indice)
        producto = self._array[indice]
        self._array[indice] = None
        return producto

    def buscar_por_categoria(self, categoria: str) -> list:
        return [
            (i, p) for i, p in enumerate(self._array)
            if p is not None and (categoria == "Todas" or p.categoria == categoria)
        ]

    def esta_vacia(self) -> bool:
        return all(p is None for p in self._array)

    def tamano(self) -> int:
        return sum(1 for p in self._array if p is not None)

    def limpiar(self) -> None:
        self._array = [None] * self._capacidad

    def capacidad_total(self) -> int:
        return self._capacidad

    def obtener_array_completo(self) -> list:
        return list(self._array)

    def _validar_indice(self, indice: int) -> None:
        if not (0 <= indice < self._capacidad):
            raise IndexError(
                f"Índice {indice} fuera de rango. Rango válido: 0–{self._capacidad - 1}."
            )