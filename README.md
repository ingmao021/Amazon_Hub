# 🚚 Simulador de Logística y Rutas de Entrega

Plataforma web interactiva desarrollada en **Python + Streamlit** que simula un sistema de logística aplicando las tres estructuras de datos principales: **Cola (FIFO)**, **Pila (LIFO)** y **Array**. El proyecto está construido siguiendo los principios de arquitectura de software **S.O.L.I.D**.

---

## 📋 Requisitos del sistema

| Herramienta | Versión mínima | Notas |
|---|---|---|
| Python | 3.10 o superior | Requerido para `match`, type hints modernos |
| pip | 22.0 o superior | Gestor de paquetes de Python |
| Streamlit | 1.43.2 | Única dependencia externa |

> ✅ **Compatible con:** Windows 10/11 · macOS 12+ · Ubuntu 20.04+

---

## 📁 Estructura del proyecto

```
simulador_logistica/
│
├── main.py             # Punto de entrada — orquesta la app (SRP + DIP)
├── interfaces.py       # Contratos abstractos ABC            (ISP + DIP)
├── cola.py             # Cola FIFO de pedidos de clientes    (SRP + OCP + LSP)
├── pila.py             # Pila LIFO de carga del camión       (SRP + OCP + LSP)
├── array.py            # Array de inventario del almacén     (SRP + OCP + LSP)
├── ui_components.py    # Componentes de renderizado Streamlit(SRP + DIP)
│
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Este archivo
```

---

## ⚙️ Instalación y ejecución paso a paso

### 1. Clonar o descargar el proyecto

Descarga todos los archivos y colócalos en una misma carpeta, por ejemplo:

```
C:\proyectos\simulador_logistica\     ← Windows
~/proyectos/simulador_logistica/      ← macOS / Linux
```

### 2. Abrir una terminal en la carpeta del proyecto

- **VS Code:** `Terminal → New Terminal`
- **PyCharm:** `View → Tool Windows → Terminal`
- **Windows:** Click derecho en la carpeta → *Abrir en terminal*

### 3. (Recomendado) Crear un entorno virtual

```bash
# Crear el entorno virtual
python -m venv venv

# Activarlo en Windows
venv\Scripts\activate

# Activarlo en macOS / Linux
source venv/bin/activate
```

> 💡 Sabrás que está activo porque verás `(venv)` al inicio de la línea en tu terminal.

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación

```bash
streamlit run main.py
```

La aplicación abrirá automáticamente en tu navegador en:
```
http://localhost:8501
```

---

## 🖥️ Configuración recomendada del IDE

### Visual Studio Code
Instala las siguientes extensiones para una mejor experiencia:

| Extensión | ID | Para qué sirve |
|---|---|---|
| Python | `ms-python.python` | Soporte completo de Python |
| Pylance | `ms-python.vscode-pylance` | Autocompletado e inferencia de tipos |
| Ruff | `charliermarsh.ruff` | Linter rápido |

Configuración sugerida en `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
  "editor.formatOnSave": true
}
```

### PyCharm
1. `File → Settings → Project → Python Interpreter`
2. Selecciona el intérprete dentro de la carpeta `venv/`
3. PyCharm detectará `requirements.txt` automáticamente y ofrecerá instalar las dependencias

---

## 🗂️ Descripción de cada archivo

### `interfaces.py`
Define los contratos abstractos (clases ABC) que deben implementar todas las estructuras de datos. Aplica los principios **ISP** (Interface Segregation) y **DIP** (Dependency Inversion).

- `EstructuraDeDatos` — contrato base con `esta_vacia()`, `tamano()`, `limpiar()`
- `InterfazCola` — contrato FIFO: `encolar()`, `desencolar()`, `ver_frente()`
- `InterfazPila` — contrato LIFO: `apilar()`, `desapilar()`, `ver_tope()`
- `InterfazArray` — contrato de índice: `insertar()`, `obtener()`, `eliminar()`

### `cola.py`
Implementa la **Cola FIFO** para la recepción de pedidos de clientes usando `collections.deque`.

- Clase `Pedido` — modelo de datos de un pedido
- Clase `ColaDePedidos` — implementación de `InterfazCola`
- Operaciones: `encolar()` O(1) · `desencolar()` O(1) · `ver_frente()` O(1)

### `pila.py`
Implementa la **Pila LIFO** para la gestión de carga del camión usando `list`.

- Clase `Paquete` — modelo de datos de un paquete
- Clase `PilaDelCamion` — implementación de `InterfazPila`
- Operaciones: `apilar()` O(1) · `desapilar()` O(1) · `ver_tope()` O(1)

### `array.py`
Implementa el **Array de posiciones fijas** para el inventario del almacén.

- Clase `ProductoEstanteria` — modelo de datos de un producto
- Clase `ArrayAlmacen` — implementación de `InterfazArray`
- Operaciones: `insertar()` O(1) · `obtener()` O(1) · `buscar_por_categoria()` O(n)

### `ui_components.py`
Contiene todas las funciones de renderizado de Streamlit. No contiene lógica de negocio. Depende de las interfaces abstractas, no de las clases concretas (**DIP**).

### `main.py`
Punto de entrada de la aplicación. Inicializa el estado de sesión, construye el layout con tabs y delega la lógica y el renderizado a los módulos correspondientes.

---

## 🧱 Principios S.O.L.I.D aplicados

| Principio | Descripción | Dónde se aplica |
|---|---|---|
| **S** Single Responsibility | Cada archivo tiene una única razón para cambiar | Todos los archivos |
| **O** Open/Closed | Las clases se extienden sin modificar su lógica base | `cola.py`, `pila.py`, `array.py` |
| **L** Liskov Substitution | Las clases concretas son sustituibles por sus interfaces | Los 3 módulos de datos |
| **I** Interface Segregation | Interfaces pequeñas y específicas por estructura | `interfaces.py` |
| **D** Dependency Inversion | La UI depende de abstracciones, no de implementaciones | `ui_components.py`, `main.py` |

---

## ⏱️ Complejidades algorítmicas

| Operación | Estructura | Complejidad |
|---|---|---|
| `encolar()` / `desencolar()` | Cola (`deque`) | **O(1)** |
| `ver_frente()` | Cola | **O(1)** |
| `apilar()` / `desapilar()` | Pila (`list`) | **O(1)** |
| `ver_tope()` | Pila | **O(1)** |
| `insertar()` / `obtener()` | Array (`list`) | **O(1)** |
| `eliminar()` | Array | **O(1)** |
| `buscar_por_categoria()` | Array | **O(n)** |

---

## 🐛 Solución de problemas comunes

**`ModuleNotFoundError: No module named 'streamlit'`**
```bash
pip install -r requirements.txt
```

**`streamlit: command not found`**
```bash
python -m streamlit run main.py
```

**La app no abre el navegador automáticamente**

Abre manualmente: `http://localhost:8501`

**Puerto 8501 ocupado**
```bash
streamlit run main.py --server.port 8502
```

---

## 👨‍💻 Tecnologías utilizadas

- **Python 3.10+** — lenguaje base
- **Streamlit 1.43.2** — framework de frontend web en Python
- **collections.deque** — implementación eficiente de la Cola
- **ABC (Abstract Base Classes)** — contratos e interfaces

---

*Actividad académica — Estructuras de Datos aplicadas a Logística*