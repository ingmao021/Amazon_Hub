# 🚚 Simulador de Logística y Rutas de Entrega

Plataforma web interactiva desarrollada en **Python + Streamlit** que simula un sistema de logística y rutas de entrega aplicando estructuras de datos.

---

## 📚 ¿Qué se usó en la actividad?

| Elemento | Descripción |
|---|---|
| **Cola (FIFO)** | Recepción de pedidos de clientes en orden de llegada |
| **Pila (LIFO)** | Gestión de carga en camiones — el último en entrar es el primero en salir |
| **Array** | Inventario de estanterías fijas del almacén con acceso por posición |
| **Principios S.O.L.I.D** | Aplicados en la arquitectura del proyecto |
| **Streamlit** | Framework para el frontend interactivo en Python puro |

---

## ▶️ Pasos para ejecutar el proyecto

**1. Tener Python 3.10 o superior instalado**

**2. Abrir una terminal en la carpeta del proyecto**

**3. Crear y activar un entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**4. Instalar las dependencias**
```bash
pip install -r requirements.txt
```

**5. Ejecutar la aplicación**
```bash
streamlit run main.py
```

La app se abrirá automáticamente en: `http://localhost:8501`