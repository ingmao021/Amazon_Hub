
import streamlit as st
from cola  import InterfazCola
from pila  import InterfazPila
from almacen import InterfazArray


#Paleta visual
CAT_COLORES: dict[str, str] = {
    "Electrónica":  "#bfdbfe",
    "Muebles":      "#bbf7d0",
    "Alimentos":    "#fef08a",
    "Ropa":         "#fbcfe8",
    "Herramientas": "#fed7aa",
    "Farmacia":     "#c4b5fd",
    "Deportes":     "#99f6e4",
    "Otros":        "#e5e7eb",
}

PRIORIDAD_BADGE: dict[str, tuple] = {
    "Normal":  ("#e5e7eb", "#374151"),
    "Alta":    ("#bfdbfe", "#1e40af"),
    "Urgente": ("#fecaca", "#991b1b"),
}

CSS_GLOBAL = """
<style>
.main-title{font-size:2.3rem;font-weight:800;color:#1a1a2e;text-align:center;padding:.80rem 0 .7rem}
.subtitle{text-align:center;color:#6b7280;margin-bottom:1.2rem}
.sec-header{font-size:1.35rem;font-weight:700;padding:.4rem .9rem;border-radius:8px;margin-bottom:.8rem}
.sec-cola  {background:#dbeafe;color:#1d4ed8}
.sec-pila  {background:#dcfce7;color:#15803d}
.sec-array {background:#fef9c3;color:#a16207}
.badge{display:inline-block;padding:2px 9px;border-radius:999px;font-size:.76rem;font-weight:600;margin:2px}
.card{border:1px solid #000000;border-radius:10px;padding:10px 14px;margin-bottom:8px}
.card-top{border-color:#22c55e;background:#dcfce7}
.card-normal{background:#f9fafb}
.shelf{border:2px solid #d1d5db;border-radius:8px;padding:7px 4px;text-align:center;font-size:.8rem;font-weight:600;min-height:68px}
.shelf-occ{border-color:#f59e0b;background:#fef3c7;color:#92400e}
.shelf-emp{background:#f3f4f6;color:#9ca3af}
.divider{border-top:2px solid #e5e7eb;margin:1.2rem 0}
</style>
"""


# Renderizado: Cola 
def render_estado_cola(cola: InterfazCola) -> None:
    pedidos = cola.obtener_cola()
    if not pedidos:
        st.markdown('<div style="text-align:center;color:#9ca3af;padding:2rem;">🟦 Cola vacía</div>',
                    unsafe_allow_html=True)
        return
    for i, p in enumerate(pedidos):
        bg, fg   = PRIORIDAD_BADGE.get(p.prioridad, ("#0d0d0e", "#000000"))
        etiqueta = "⬆️ FRENTE (siguiente)" if i == 0 else f"#{i + 1}"
        card_cls = "card-top" if i == 0 else "card-normal"
        st.markdown(f"""
        <div class="card {card_cls}" style="color:#000000">
            <b>{etiqueta}</b> &nbsp;
            <span class="badge" style="background:{bg};color:{fg}">{p.prioridad}</span>
            <span class="badge" style="background:#dbeafe;color:#1e40af">{p.id_pedido}</span><br>
            <small>👤 {p.cliente} &nbsp;|&nbsp; 📦 {p.producto}</small><br>
            <small>📍 {p.destino}</small>
        </div>
        """, unsafe_allow_html=True)


def render_historial_cola(cola: InterfazCola, limite: int = 5) -> None:
    historial = cola.obtener_historial()
    if not historial:
        st.caption("Aún no se han procesado pedidos.")
        return
    for p in reversed(historial[-limite:]):
        st.markdown(
            f'<span class="badge" style="background:#bbf7d0;color:#166534">{p.id_pedido}</span> '
            f'<small>{p.cliente} → {p.producto}</small>',
            unsafe_allow_html=True,
        )


# Renderizado: Pila
def render_pila_camion(pila: InterfazPila) -> None:
    paquetes = pila.obtener_pila()
    cap      = pila.capacidad_maxima()
    usado    = pila.tamano()
    ratio    = usado / cap if cap > 0 else 0
    st.progress(ratio, text=f"Ocupación: {usado}/{cap} paquetes  |  Peso: {pila.peso_total_carga} kg")
    if not paquetes:
        st.markdown(
            '<div style="text-align:center;color:#9ca3af;padding:2rem;'
            'border:2px dashed #d1d5db;border-radius:12px;">Camión vacío</div>',
            unsafe_allow_html=True,
        )
        return
    for i, pkg in enumerate(reversed(paquetes)):
        is_top   = (i == 0)
        card_cls = "card-top" if is_top else "card-normal"
        etiqueta = "⬆️ TOPE — saldrá primero" if is_top else f"Posición {usado - i}"
        st.markdown(f"""
        <div class="card {card_cls}" style="color:#000000">
            <b>{etiqueta}</b><br>
            <span class="badge" style="background:#bbf7d0;color:#166534">{pkg.id_paquete}</span>
            <span class="badge" style="background:#e5e7eb;color:#374151">{pkg.peso_kg} kg</span><br>
            <small>📦 {pkg.nombre}</small><br>
            <small>📍 {pkg.destino}</small>
        </div>
        """, unsafe_allow_html=True)
   


def render_historial_entregas(pila: InterfazPila, limite: int = 5) -> None:
    historial = pila.obtener_historial_entregas()
    if not historial:
        st.caption("Sin entregas aún.")
        return
    for p in reversed(historial[-limite:]):
        st.markdown(
            f'<span class="badge" style="background:#bbf7d0;color:#166534">{p.id_paquete}</span> '
            f'<small>{p.nombre} → {p.destino}</small>',
            unsafe_allow_html=True,
        )


# Renderizado: Array
def render_mapa_almacen(array: InterfazArray) -> None:
    cap       = array.capacidad_total()
    contenido = array.obtener_array_completo()
    for fila in range((cap + 3) // 4):
        cols = st.columns(4)
        for col_i in range(4):
            idx = fila * 4 + col_i
            if idx >= cap:
                break
            with cols[col_i]:
                producto = contenido[idx]
                if producto:
                    bg = CAT_COLORES.get(producto.categoria, "#e5e7eb")
                    st.markdown(f"""
                    <div class="shelf shelf-occ" style="background:{bg};">
                        <div style="font-size:.62rem;color:#6b7280;">[{idx}] {producto.codigo_pasillo}</div>
                        <div style="font-size:.78rem;font-weight:700;">{producto.nombre[:14]}</div>
                        <div style="font-size:.62rem;">{producto.categoria}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="shelf shelf-emp">
                        <div style="font-size:.62rem;">[{idx}]</div>
                        <div style="font-size:1.1rem;">—</div>
                        <div style="font-size:.62rem;">Vacío</div>
                    </div>
                    """, unsafe_allow_html=True)


def render_leyenda_categorias() -> None:
    cols = st.columns(4)
    for i, (cat, color) in enumerate(CAT_COLORES.items()):
        with cols[i % 4]:
            st.markdown(
                f'<span style="background:{color};padding:2px 8px;'
                f'border-radius:6px;font-size:.74rem;color:#000000;">{cat}</span>',
                unsafe_allow_html=True,
            )


def render_resultados_busqueda(resultados: list) -> None:
    if not resultados:
        st.caption("No se encontraron productos.")
        return
    for idx, prod in resultados:
        st.markdown(
            f'<span class="badge" style="background:#fef08a;color:#854d0e">[{idx}]</span> '
            f'<b>{prod.nombre}</b> — {prod.codigo_pasillo} | {prod.categoria}',
            unsafe_allow_html=True,
        )


# Renderizado: Sidebar 
def render_sidebar_metricas(cola: InterfazCola, pila: InterfazPila, array: InterfazArray) -> None:
    st.markdown("### 📊 Estado del Sistema")
    st.metric("Pedidos en cola",     cola.tamano())
    st.metric("Paquetes en camión",  f"{pila.tamano()} / {pila.capacidad_maxima()}")
    st.metric("Peso en camión",      f"{pila.peso_total_carga} kg")
    st.metric("Estantes ocupados",   f"{array.tamano()} / {array.capacidad_total()}")
    st.metric("Pedidos procesados",  len(cola.obtener_historial()))
    st.metric("Entregas realizadas", len(pila.obtener_historial_entregas()))