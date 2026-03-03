
from abc import ABC, abstractmethod
from typing import Any, Optional


# Contrato abstracto (ISP)
class InterfazPila(ABC):
    """ISP: Contrato exclusivo para estructuras LIFO."""

    @abstractmethod
    def esta_vacia(self) -> bool: ...

    @abstractmethod
    def tamano(self) -> int: ...

    @abstractmethod
    def limpiar(self) -> None: ...

    @abstractmethod
    def apilar(self, elemento: Any) -> None: ...

    @abstractmethod
    def desapilar(self) -> Optional[Any]: ...

    @abstractmethod
    def ver_tope(self) -> Optional[Any]: ...

    @abstractmethod
    def esta_llena(self) -> bool: ...

    @abstractmethod
    def capacidad_maxima(self) -> int: ...

    @abstractmethod
    def obtener_pila(self) -> list: ...

    @abstractmethod
    def obtener_historial_entregas(self) -> list: ...


# Modelo de datos 
class Paquete:
    """SRP: Solo representa la información de un paquete."""

    def __init__(self, id_paquete: str, nombre: str,
                 destino: str, peso_kg: float):
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor a 0 kg.")
        self.id_paquete = id_paquete
        self.nombre     = nombre
        self.destino    = destino
        self.peso_kg    = peso_kg
        self.estado     = "En camión"

    def a_dict(self) -> dict:
        return {
            "ID": self.id_paquete, "Paquete": self.nombre,
            "Destino": self.destino, "Peso (kg)": self.peso_kg,
            "Estado": self.estado,
        }

    def __repr__(self) -> str:
        return f"Paquete({self.id_paquete}, {self.nombre}, {self.peso_kg}kg)"


# Estructura de datos: Pila LIFO 
class PilaDelCamion(InterfazPila):
    """
    Implementación concreta de la Pila LIFO.
    apilar()    → O(1)
    desapilar() → O(1)
    ver_tope()  → O(1)
    """

    def __init__(self, capacidad: int = 6):
        if capacidad < 1:
            raise ValueError("La capacidad debe ser al menos 1.")
        self._pila: list[Paquete]             = []
        self._capacidad: int                  = capacidad
        self._historial_entregas: list[Paquete] = []

    def apilar(self, elemento: Paquete) -> None:
        if self.esta_llena():
            raise OverflowError(f"Camión lleno. Máximo: {self._capacidad}.")
        self._pila.append(elemento)

    def desapilar(self) -> Optional[Paquete]:
        if self.esta_vacia():
            return None
        paquete = self._pila.pop()
        paquete.estado = "Entregado ✅"
        self._historial_entregas.append(paquete)
        return paquete

    def ver_tope(self) -> Optional[Paquete]:
        return None if self.esta_vacia() else self._pila[-1]

    def esta_vacia(self) -> bool:
        return len(self._pila) == 0

    def esta_llena(self) -> bool:
        return len(self._pila) >= self._capacidad

    def capacidad_maxima(self) -> int:
        return self._capacidad

    def tamano(self) -> int:
        return len(self._pila)

    def limpiar(self) -> None:
        self._pila.clear()
        self._historial_entregas.clear()

    def crear_paquete(self, nombre: str, destino: str,
                      peso_kg: float) -> Paquete:
        """OCP: Fábrica extensible sin tocar la lógica LIFO base."""
        total = len(self._pila) + len(self._historial_entregas)
        return Paquete(
            id_paquete=f"PKG-{total + 1:03d}",
            nombre=nombre, destino=destino, peso_kg=peso_kg,
        )

    @property
    def peso_total_carga(self) -> float:
        return round(sum(p.peso_kg for p in self._pila), 2)

    def set_capacidad(self, nueva: int) -> None:
        if nueva < self.tamano():
            raise ValueError("No se puede reducir por debajo de la carga actual.")
        self._capacidad = nueva

    def obtener_pila(self) -> list[Paquete]:
        return list(self._pila)

    def obtener_historial_entregas(self) -> list[Paquete]:
        return list(self._historial_entregas)