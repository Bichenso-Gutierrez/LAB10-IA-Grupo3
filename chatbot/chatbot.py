import json
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key="TU_API_KEY")

# Cargar productos
with open("productos.json", "r") as f:
    productos = json.load(f)

# Buscar información del producto
def buscar_producto(pregunta):
    for p in productos:
        if p["nombre"].lower() in pregunta.lower():
            return f"{p['nombre']} cuesta {p['precio']} soles y hay {p['stock']} unidades en stock."

    return "No encontré ese producto en la tienda."

st.title("🛒 Chatbot de Tienda Virtual")

pregunta = st.text_input("Haz tu consulta sobre productos:")

if pregunta:
    info = buscar_producto(pregunta)

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Cliente pregunta: {pregunta}. Info: {info}"
            }
        ]
    )

    st.write("🤖 Respuesta del chatbot:")
    st.success(respuesta.choices[0].message.content)
