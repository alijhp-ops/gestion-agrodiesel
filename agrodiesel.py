import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Agrodiesel Bruzual", layout="wide")

# --- TITULO ---
st.title("🛠️ Agrodiesel Bruzual: Gestión Pro")

# --- BASE DE DATOS SIMPLE (En memoria para la prueba) ---
if 'categorias' not in st.session_state:
    st.session_state.categorias = ["Bombas", "Inyectores", "Cabezote", "Tobera", "Bombante", "Arandelas", "Tornillos", "Válvulas", "Solenoide", "Kit de empacadura", "Mano de Obra"]

# --- MENÚ LATERAL ---
menu = st.sidebar.radio("Menú", ["Registrar Trabajo", "Inventario", "Cuentas por Cobrar", "Configuración"])

if menu == "Registrar Trabajo":
    st.header("📝 Nueva Orden de Servicio")
    with st.form("orden_form"):
        col1, col2 = st.columns(2)
        cliente = col1.text_input("Nombre del Cliente")
        telefono = col2.text_input("WhatsApp (ej: 584125555555)")
        
        cat = st.selectbox("Categoría", st.session_state.categorias)
        detalle = st.text_area("Descripción del trabajo / Repuesto")
        monto = st.number_input("Monto Total ($)", min_value=0.0)
        abono = st.number_input("Abono ($)", min_value=0.0)
        
        enviar = st.form_submit_button("Generar Recibo WhatsApp")
        
        if enviar:
            saldo = monto - abono
            texto_ws = f"*AGRODIESEL BRUZUAL* 🛠️\n\n*Cliente:* {cliente}\n*Trabajo:* {cat}\n*Detalle:* {detalle}\n*Total:* ${monto}\n*Abono:* ${abono}\n*Saldo:* ${saldo}\n\n_Gracias por su confianza._"
            link_ws = f"https://wa.me/{telefono}?text={urllib.parse.quote(texto_ws)}"
            st.success(f"Orden lista. Saldo pendiente: ${saldo}")
            st.markdown(f"### [📲 CLICK AQUÍ PARA ENVIAR A WHATSAPP]({link_ws})")

elif menu == "Configuración":
    st.header("⚙️ Ajustes")
    nueva_cat = st.text_input("Agregar nueva categoría")
    if st.button("Añadir"):
        st.session_state.categorias.append(nueva_cat)
        st.success(f"Añadida: {nueva_cat}")