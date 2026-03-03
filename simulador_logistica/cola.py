from abc import ABC, abstractmethod
from collections import deque
from typing import Any, Optional


class InterfazCola(ABC):
    """ISP: Contrato exclusivo para estructuras FIFO."""

    @abstractmethod
    def esta_vacia(self) -> bool: ...

    @abstractmethod
    def tamano(self) -> int: ...

    @abstractmethod
    def limpiar(self) -> None: ...

    @abstractmethod
    def encolar(self, elemento: Any) -> None: ...

    @abstractmethod
    def desencolar(self) -> Optional[Any]: ...

    @abstractmethod
    def ver_frente(self) -> Optional[Any]: ...

    @abstractmethod
    def obtener_cola(self) -> list: ...

    @abstractmethod
    def obtener_historial(self) -> list: ...


#Modelo de datos
class Pedido:

    PRIORIDADES_VALIDAS = ("Normal", "Alta", "Urgente")

    def __init__(self, id_pedido: str, cliente: str, producto: str,
                 destino: str, prioridad: str = "Normal"):
        if prioridad not in self.PRIORIDADES_VALIDAS:
            raise ValueError(f"Prioridad inválida: {prioridad}.")
        self.id_pedido = id_pedido
        self.cliente   = cliente
        self.producto  = producto
        self.destino   = destino
        self.prioridad = prioridad
        self.estado    = "En cola"

    def a_dict(self) -> dict:
        return {
            "ID": self.id_pedido, "Cliente": self.cliente,
            "Producto": self.producto, "Destino": self.destino,
            "Prioridad": self.prioridad, "Estado": self.estado,
        }

    def __repr__(self) -> str:
        return f"Pedido({self.id_pedido}, {self.cliente}, {self.prioridad})"


# Cola FIFO 
class ColaDePedidos(InterfazCola):


    def __init__(self):
        self._cola: deque[Pedido]     = deque()
        self._contador_id: int        = 1
        self._historial: list[Pedido] = []

    def encolar(self, elemento: Pedido) -> None:
        self._cola.append(elemento)

    def desencolar(self) -> Optional[Pedido]:
        if self.esta_vacia():
            return None
        pedido = self._cola.popleft()
        pedido.estado = "Despachado ✅"
        self._historial.append(pedido)
        return pedido

    def ver_frente(self) -> Optional[Pedido]:
        return None if self.esta_vacia() else self._cola[0]

    def esta_vacia(self) -> bool:
        return len(self._cola) == 0

    def tamano(self) -> int:
        return len(self._cola)

    def limpiar(self) -> None:
        self._cola.clear()
        self._historial.clear()
        self._contador_id = 1

    def crear_pedido(self, cliente: str, producto: str,
                     destino: str, prioridad: str = "Normal") -> Pedido:
       

        pedido = Pedido(
            id_pedido=f"PED-{self._contador_id:03d}",
            cliente=cliente, producto=producto,
            destino=destino, prioridad=prioridad,
        )
        self._contador_id += 1
        return pedido

    def obtener_cola(self) -> list[Pedido]:
        return list(self._cola)


    def obtener_historial(self) -> list[Pedido]:
        return list(self._historial)