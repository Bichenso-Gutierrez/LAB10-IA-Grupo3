import streamlit as st
import json
from dotenv import load_dotenv
from openai import OpenAI
import os
import difflib

# ===============================
#  CARGAR API KEY
# ===============================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if os.getenv("OPENAI_API_KEY") is None:
    st.error("❌ No se encontró la clave OPENAI_API_KEY en .env")

# ===============================
#  CARGAR PRODUCTOS DESDE JSON
# ===============================
with open("productos.json", "r", encoding="utf-8") as f:
    productos = json.load(f)

# Función para buscar info del producto
def buscar_producto(pregunta):
    texto = pregunta.lower()

    # crear lista de nombres
    nombres = [p["nombre"].lower() for p in productos]

    # buscar coincidencia aproximada
    coincidencia = difflib.get_close_matches(texto, nombres, n=1, cutoff=0.3)

    if coincidencia:
        nombre_encontrado = coincidencia[0]

        for p in productos:
            if p["nombre"].lower() == nombre_encontrado:
                specs = "\n".join([f"- {k}: {v}" for k, v in p["especificaciones"].items()])
                return f"""
📦 **{p['nombre']}**
💵 **Precio:** {p['precio']} soles  
📦 **Stock:** {p['stock']} unidades  
📝 **Especificaciones Técnicas:**  
{specs}
                """

    return "No encontré ese producto en el catálogo. Puedes consultar Laptop, Mouse Gamer, Audífonos Sony o Teclado Mecánico."

# ===============================
#  FUNCIÓN PRINCIPAL DEL CHAT
# ===============================
def obtener_respuesta(pregunta):
    info_producto = buscar_producto(pregunta)

    if info_producto is None:
        lista = "\n".join([f"- {p['nombre']}" for p in productos])
        return f"""
❌ No encontré ese producto en el catálogo.
📦 Estos son los productos disponibles:

{lista}

Pregunta por uno de la lista (por ejemplo: "Precio del Mouse Gamer RGB").
"""

    # llamar al modelo para mejorar la redacción
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
Eres un chatbot de TIENDA VIRTUAL.
Debes responder basándote exclusivamente en la información JSON proporcionada.
NO inventes productos, precios ni características.
Tu misión es explicar la información del producto de manera clara y amable.
"""
            },
            {
                "role": "user",
                "content": f"Pregunta del cliente: {pregunta}\n\nInformación del producto:\n{info_producto}"
            }
        ]
    )

    return respuesta.choices[0].message.content


# ===============================
#  INTERFAZ TIPO CHAT
# ===============================
st.set_page_config(page_title="ChatBot de Tienda Virtual", page_icon="🛒")
st.title("🛒 ChatBot de Catálogo – Comercio Electrónico")

# Historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for m in st.session_state.mensajes:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Input estilo chat
pregunta = st.chat_input("Pregunta por un producto: '¿Cuánto cuesta la laptop Lenovo?'")

if pregunta:
    # Mostrar usuario
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.write(pregunta)

    # Obtener respuesta
    respuesta = obtener_respuesta(pregunta)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.write(respuesta)
