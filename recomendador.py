import pandas as pd

data = {
    "usuario": ["Luis", "Luis", "Ana", "Ana", "Carla"],
    "producto": ["Laptop", "Mouse", "Laptop", "Audífonos", "Mouse"]
}

df = pd.DataFrame(data)

def recomendar(usuario):
    productos_usuario = df[df["usuario"] == usuario]["producto"].unique()
    
    otros = df[df["usuario"] != usuario]
    recomendados = otros[~otros["producto"].isin(productos_usuario)]["producto"].unique()
    
    return recomendados

print("Recomendación para Luis:", recomendar("Luis"))
