import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Agrodiesel Bruzual", layout="wide", page_icon="⛽")

# --- BASE DE DATOS EN LA NUBE (Streamlit Cloud la mantiene viva) ---
if 'inventario' not in st.session_state:
    # Datos de ejemplo para que veas cómo funciona
    st.session_state.inventario = pd.DataFrame(columns=["Pieza", "Categoría", "Stock", "Costo", "Precio_Venta"])

if 'categorias' not in st.session_state:
    st.session_state.categorias = ["Bombas", "Inyectores", "Cabezote", "Tobera", "Bombante", "Arandelas", "Solenoide", "Kit de empacadura", "Mano de Obra"]

# --- FUNCIONES ---
def actualizar_stock(nombre_pieza, cantidad):
    idx = st.session_state.inventario[st.session_state.inventario['Pieza'] == nombre_pieza].index
    if not idx.empty:
        st.session_state.inventario.at[idx[0], 'Stock'] -= cantidad

# --- MENÚ ---
menu = st.sidebar.radio("MENÚ PRINCIPAL", ["📦 Inventario Real", "🔧 Nueva Reparación", "⚙️ Configuración"])

# --- 1. INVENTARIO REAL ---
if menu == "📦 Inventario Real":
    st.header("Control de Almacén y Costos")
    
    with st.expander("➕ Cargar Nuevo Repuesto"):
        with st.form("form_inv"):
            col1, col2 = st.columns(2)
            nombre = col1.text_input("Nombre del Repuesto (Modelo/Marca)")
            cat = col2.selectbox("Categoría", st.session_state.categorias)
            
            c1, c2, c3 = st.columns(3)
            stock_inicial = c1.number_input("Cantidad que entra", min_value=1, step=1)
            costo = c2.number_input("Costo de Compra ($)", min_value=0.0)
            margen = c3.slider("% de Ganancia deseado", 10, 100, 30)
            
            precio_sugerido = costo * (1 + (margen/100))
            st.info(f"Precio de venta calculado: ${precio_sugerido:,.2f}")
            
            if st.form_submit_button("Guardar en Nube"):
                nuevo = pd.DataFrame([[nombre, cat, stock_inicial, costo, precio_sugerido]], 
                                    columns=st.session_state.inventario.columns)
                st.session_state.inventario = pd.concat([st.session_state.inventario, nuevo], ignore_index=True)
                st.success("Pieza guardada exitosamente")
                st.rerun()

    st.subheader("Listado de Existencias")
    st.dataframe(st.session_state.inventario, use_container_width=True)

# --- 2. NUEVA REPARACIÓN (CON DESCUENTO AUTOMÁTICO) ---
elif menu == "🔧 Nueva Reparación":
    st.header("Informe Técnico y Recibo")
    
    with st.form("form_reparacion"):
        st.subheader("Datos del Equipo")
        c1, c2 = st.columns(2)
        cliente = c1.text_input("Nombre del Cliente / Finca")
        telf = c2.text_input("WhatsApp (ej: 584125555555)")
        
        c3, c4 = st.columns(2)
        equipo = c3.text_input("Tipo de Bomba / Inyector (ej: Bosch VE)")
        modelo_serial = c4.text_input("Modelo o Serial del equipo")
        
        st.divider()
        st.subheader("Repuestos y Mano de Obra")
        # Solo muestra piezas que tengan stock > 0
        lista_piezas = st.session_state.inventario[st.session_state.inventario['Stock'] > 0]['Pieza'].tolist()
        pieza_usada = st.selectbox("Seleccionar Repuesto usado", ["Ninguno (Solo mano de obra)"] + lista_piezas)
        
        detalles_adicionales = st.text_area("Informe Técnico (Falla encontrada, ajustes realizados...)")
        
        c5, c6 = st.columns(2)
        mano_obra = c5.number_input("Costo Mano de Obra ($)", min_value=0.0)
        abono = c6.number_input("Abono del cliente ($)", min_value=0.0)

        if st.form_submit_button("Finalizar y Generar WhatsApp"):
            precio_repuesto = 0
            if pieza_usada != "Ninguno (Solo mano de obra)":
                # Buscar el precio en el inventario
                precio_repuesto = st.session_state.inventario[st.session_state.inventario['Pieza'] == pieza_usada]['Precio_Venta'].values[0]
                actualizar_stock(pieza_usada, 1) # Descuenta 1 unidad
            
            total = precio_repuesto + mano_obra
            saldo = total - abono
            
            # Formatear mensaje de WhatsApp
            msg = (f"*AGRODIESEL BRUZUAL - INFORME TÉCNICO* 🛠️\n\n"
                   f"*Cliente:* {cliente}\n"
                   f"*Equipo:* {equipo}\n"
                   f"*Modelo/Serial:* {modelo_serial}\n"
                   f"----------------------------------\n"
                   f"*DETALLES:* {detalles_adicionales}\n"
                   f"----------------------------------\n"
                   f"*DESGLOSE:* \n"
                   f"- Repuesto ({pieza_usada}): ${precio_repuesto:.2f}\n"
                   f"- Mano de Obra: ${mano_obra:.2f}\n"
                   f"*TOTAL:* ${total:.2f}\n"
                   f"*ABONO:* ${abono:.2f}\n"
                   f"*SALDO PENDIENTE:* ${saldo:.2f}\n\n"
                   f"_Trabajo garantizado. Gracias por su confianza._")
            
            link = f"https://wa.me/{telf}?text={urllib.parse.quote(msg)}"
            st.success(f"¡Listo! Se descontó '{pieza_usada}' del inventario.")
            st.markdown(f"### [📲 ENVIAR INFORME DETALLADO]({link})")

# --- 3. CONFIGURACIÓN ---
elif menu == "⚙️ Configuración":
    st.header("Categorías")
    nueva = st.text_input("Añadir Categoría")
    if st.button("Agregar"):
        st.session_state.categorias.append(nueva)
        st.success("Añadida.")