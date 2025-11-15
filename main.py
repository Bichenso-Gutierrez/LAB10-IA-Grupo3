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
# Obtener ruta absoluta del archivo main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construir ruta absoluta hacia productos.json dentro de la carpeta /chatbot
ruta_productos = os.path.join(BASE_DIR, "chatbot", "productos.json")

# Cargar productos desde JSON
with open(ruta_productos, "r", encoding="utf-8") as f:
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

    return "No encontré ese producto en el catálogo. Puedes consultar otros productos disponibles."

# ===============================
#  FUNCIÓN PRINCIPAL DEL CHAT
# ===============================
def obtener_respuesta(pregunta):
    texto = pregunta.lower().strip()

    # ================================
    # 1. Manejo de saludos
    # ================================
    saludos = ["hola", "holi", "buenas", "buenos días", "buenas tardes", "buenas noches", "hey", "que tal", "qué tal", "hi", "hello"]

    if any(s in texto for s in saludos):
        return """
👋 ¡Hola! ¿En qué puedo ayudarte hoy?
Puedo darte información sobre precios, características o disponibilidad de cualquier producto del catálogo.
"""

    # ================================
    # 2. Buscar producto en la base
    # ================================
    info_producto = buscar_producto(pregunta)

    if "No encontré ese producto" in info_producto:
        lista = "\n".join([f"• {p['nombre']}" for p in productos])
        return f"""
😕 No encontré ese producto en nuestro catálogo.

Aquí tienes lo que tenemos disponible ahora mismo:

{lista}

✨ Si deseas, pregúntame por uno en específico.
Ejemplo: _"¿Qué precio tiene el Mouse Gamer RGB?"_
"""

    # ================================
    # 3. Si se encontró el producto → generar respuesta amigable
    # ================================
    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
Eres un chatbot amable y profesional de una tienda virtual.
Responde utilizando SOLO la información del JSON.
Sé cálido, útil y directo. No inventes datos.
"""
            },
            {
                "role": "user",
                "content": (
                    f"El cliente pregunta: {pregunta}\n\n"
                    f"Información del producto:\n{info_producto}\n\n"
                    "Redáctalo de forma amigable."
                )
            }
        ]
    )

    return respuesta.choices[0].message.content




# ===============================
#  INTERFAZ TIPO CHAT
# ===============================
st.set_page_config(page_title="ChatBot de Tienda Virtual", page_icon="🛒")
st.title("🛒 ChatBot de Catálogo – Mi Tienda Virtual")


# ===============================
# MENSAJE DE BIENVENIDA AUTOMÁTICO
# ===============================
if "bienvenida" not in st.session_state:
    with st.chat_message("assistant"):
        st.write("""
👋 ¡Hola! Bienvenido a **Mi Tienda Virtual**.

Estoy aquí para ayudarte a encontrar:
- precios  
- características técnicas  
- disponibilidad  
- productos similares  

Puedes preguntarme algo como:
👉 *"¿Qué precio tiene la Laptop Lenovo i5?"*  
👉 *"Muéstrame las características del Mouse Gamer RGB"*  
👉 *"¿Tienes audífonos?"*

¿En qué puedo ayudarte hoy? 😊
""")
    st.session_state.bienvenida = True



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
