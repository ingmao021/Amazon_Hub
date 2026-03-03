

import streamlit as st

from cola  import ColaDePedidos, Pedido
from pila  import PilaDelCamion, Paquete
from almacen import ArrayAlmacen,  ProductoEstanteria

from ui_components import (
    CSS_GLOBAL, CAT_COLORES,
    render_sidebar_metricas,
    render_estado_cola, render_historial_cola,
    render_pila_camion, render_historial_entregas,
    render_mapa_almacen, render_leyenda_categorias,
    render_resultados_busqueda,
)

# ── Configuración ───────────────────────────────
st.set_page_config(
    page_title="AMAZON HUB",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(CSS_GLOBAL, unsafe_allow_html=True)


# ── Estado de sesión (DIP: inyección de concretos) ──
def _inicializar_estado() -> None:
    if "cola"  not in st.session_state:
        st.session_state.cola  = ColaDePedidos()
    if "pila"  not in st.session_state:
        st.session_state.pila  = PilaDelCamion(capacidad=6)
    if "array" not in st.session_state:
        st.session_state.array = ArrayAlmacen(capacidad=12)

_inicializar_estado()

cola:  ColaDePedidos = st.session_state.cola
pila:  PilaDelCamion = st.session_state.pila
array: ArrayAlmacen  = st.session_state.array


# ── Encabezado ──────────────────────────────────
st.markdown('<div class="main-title" style="color:#ffffff"> Simulador de Logística y Rutas de Entrega</div>',
            unsafe_allow_html=True)



# ── Sidebar ─────────────────────────────────────
with st.sidebar:
    render_sidebar_metricas(cola, pila, array)
    st.markdown("---")
    st.markdown("### 🗑️ Reiniciar módulos")
    if st.button("🔄 Reiniciar Cola",    use_container_width=True):
        cola.limpiar();  st.rerun()
    if st.button("🔄 Reiniciar Camión",  use_container_width=True):
        pila.limpiar();  st.rerun()
    if st.button("🔄 Reiniciar Almacén", use_container_width=True):
        array.limpiar(); st.rerun()
    st.markdown("---")
    st.markdown("#### 📁 Archivos del proyecto")
    st.code(
        "cola.py          → SRP + OCP + LSP + ISP\n"
        "pila.py          → SRP + OCP + LSP + ISP\n"
        "array.py         → SRP + OCP + LSP + ISP\n"
        "ui_components.py → SRP + DIP\n"
        "main.py          → SRP + DIP",
        language="text",
    )


# ── Tabs ────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📦 Cola de Pedidos (FIFO)",
    "🚛 Carga del Camión (LIFO)",
    "🏭 Almacén (Array)",
])


# ══════════════════════════════════════════════
#  TAB 1 — COLA DE PEDIDOS
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-header sec-cola">📦 Cola de Recepción de Pedidos — FIFO</div>',
                unsafe_allow_html=True)
    st.info("Los pedidos se atienden **en orden de llegada** (FIFO). ")

    col_form, col_viz = st.columns([1, 1], gap="large")

    with col_form:
        st.markdown("#### ➕ Registrar nuevo pedido")
        cliente   = st.text_input("👤 Cliente",   placeholder="Ej: Ana García",      key="c_cliente")
        producto  = st.text_input("📦 Producto",  placeholder="Ej: Televisor 55'",   key="c_producto")
        destino   = st.text_input("📍 Destino",   placeholder="Ej: Calle 45 #12-30", key="c_destino")
        prioridad = st.selectbox("⚡ Prioridad", Pedido.PRIORIDADES_VALIDAS)

        if st.button("📥 Encolar pedido", use_container_width=True, type="primary"):
            if cliente and producto and destino:
                nuevo = cola.crear_pedido(cliente, producto, destino, prioridad)
                cola.encolar(nuevo)
                st.success(f"✅ {nuevo.id_pedido} añadido. Cola: {cola.tamano()} pedidos.")
                st.rerun()
            else:
                st.warning("⚠️ Completa todos los campos.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 🔄 Gestionar pedidos")
        if st.button("▶️ Despachar pedido ", use_container_width=True):
            despachado = cola.desencolar()
            if despachado:
                st.success(f"📤 Despachado: **{despachado.id_pedido}** — {despachado.cliente} → {despachado.producto}")
                st.rerun()
            else:
                st.warning("⚠️ Cola vacía.")

        frente = cola.ver_frente()
        
    with col_viz:
        st.markdown("#### 📊 Estado de la cola")
        render_estado_cola(cola)
        st.markdown("#### ✅ Últimos despachados")
        render_historial_cola(cola)


# ══════════════════════════════════════════════
#  TAB 2 — PILA DEL CAMIÓN
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-header sec-pila">🚛 Gestión de Carga del Camión — LIFO</div>',
                unsafe_allow_html=True)
    st.info("El último paquete en entrar es el primero en salir (LIFO).")

    col_ctrl, col_viz = st.columns([1, 1], gap="large")

    with col_ctrl:
        st.markdown("#### 📦 Cargar paquete")
        p_nombre = st.text_input("📦 Paquete",  placeholder="Ej: Caja Electrónica #5", key="p_nombre")
        p_dest   = st.text_input("📍 Destino",  placeholder="Ej: Barrio Centro Stop 3", key="p_dest")
        p_peso   = st.number_input("⚖️ Peso (kg)", min_value=0.1, max_value=500.0, value=5.0, step=0.1)

        if st.button("⬆️ Push - Apilar paquete", use_container_width=True, type="primary"):
            if pila.esta_llena():
                st.error(f"🚫 Camión lleno. Máximo: {pila.capacidad_maxima()} paquetes.")
            elif p_nombre and p_dest:
                nuevo_pkg = pila.crear_paquete(p_nombre, p_dest, p_peso)
                pila.apilar(nuevo_pkg)
                st.success(f"✅ {nuevo_pkg.id_paquete} cargado. Pila: {pila.tamano()}/{pila.capacidad_maxima()}")
                st.rerun()
            else:
                st.warning("⚠️ Completa nombre y destino.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 🚚 Gestionar entrega")
        if st.button("⬇️ POP — realizar entrega", use_container_width=True):
            entregado = pila.desapilar()
            if entregado:
                st.success(f"📬 Entregado: **{entregado.id_paquete}** → {entregado.destino} ({entregado.peso_kg} kg)")
                st.rerun()
            else:
                st.warning("⚠️ El camión está vacío.")

        tope = pila.ver_tope()
       

        st.markdown("#### ⚙️ Capacidad del camión")
        nueva_cap = st.slider("Máximo de paquetes", 3, 15, pila.capacidad_maxima())
        if nueva_cap != pila.capacidad_maxima():
            try:
                pila.set_capacidad(nueva_cap)
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    with col_viz:
        st.markdown("#### 🚚 Pila del camión (tope → base)")
        render_pila_camion(pila)
        st.markdown("#### 📬 Últimas entregas")
        render_historial_entregas(pila)


# ══════════════════════════════════════════════
#  TAB 3 — ALMACÉN (ARRAY)
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-header sec-array">🏭 Inventario del Almacén</div>',
                unsafe_allow_html=True)
    

    cap_arr = array.capacidad_total()
    col_ctrl, col_viz = st.columns([1, 1.4], gap="large")

    with col_ctrl:
        st.markdown("#### ➕ Agregar producto")
        a_idx     = st.number_input("📍 Posición", min_value=0, max_value=cap_arr - 1, step=1, key="a_idx")
        a_pasillo = st.text_input("🚦 Pasillo",   placeholder="Ej: B2", key="a_pasillo")
        a_prod    = st.text_input("📦 Producto",  placeholder="Ej: Tablet Samsung", key="a_prod")
        a_cat     = st.selectbox("🏷️ Categoría", ProductoEstanteria.CATEGORIAS_VALIDAS)

        if st.button("💾 Insertar", use_container_width=True, type="primary"):
            if a_pasillo and a_prod:
                existente = array.obtener(int(a_idx))
                if existente:
                    st.warning(f"⚠️ [{a_idx}] tenía **{existente.nombre}**. Reemplazado.")
                array.insertar(int(a_idx), ProductoEstanteria(a_pasillo, a_prod, a_cat))
                st.success(f"✅ '{a_prod}' guardado en [{a_idx}].")
                st.rerun()
            else:
                st.warning("⚠️ Completa pasillo y producto.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 🔍 Consultar posición ")
        s_idx = st.number_input("Índice", min_value=0, max_value=cap_arr - 1, step=1, key="s_idx")
        if st.button("🔎 Obtener por índice", use_container_width=True):
            celda = array.obtener(int(s_idx))
            if celda:
                st.success(f"[{s_idx}] → Pasillo **{celda.codigo_pasillo}** | {celda.nombre} | {celda.categoria}")
            else:
                st.info(f"📭 Posición [{s_idx}] vacía.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 🗑️ Liberar posición")
        d_idx = st.number_input("Índice a liberar", min_value=0, max_value=cap_arr - 1, step=1, key="d_idx")
        if st.button("❌ Eliminar del array", use_container_width=True):
            eliminado = array.eliminar(int(d_idx))
            if eliminado:
                st.success(f"🗑️ [{d_idx}] liberado (era: {eliminado.nombre}).")
                st.rerun()
            else:
                st.warning(f"⚠️ [{d_idx}] ya estaba vacía.")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("#### 🔎 Buscar por categoría")
        f_cat = st.selectbox("Filtrar", ["Todas"] + list(ProductoEstanteria.CATEGORIAS_VALIDAS), key="f_cat")
        render_resultados_busqueda(array.buscar_por_categoria(f_cat))

    with col_viz:
        st.markdown("#### 🗺️ Mapa del Almacén")
        render_mapa_almacen(array)
        st.markdown("#### 🏷️ Leyenda")
        render_leyenda_categorias()
        c1, c2, c3 = st.columns(3)
        c1.metric("Ocupadas", array.tamano())
        c2.metric("Vacías",   cap_arr - array.tamano())
        c3.metric("Total",    cap_arr)


