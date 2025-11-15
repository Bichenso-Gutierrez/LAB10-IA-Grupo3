import pandas as pd

data = {
    "usuario": ["Luis", "Roy", "Ana", "Lucy", "Bichenso"],
    "producto": [
  "Laptop Lenovo i5",
  "Mouse Gamer RGB",
  "Audífonos Sony WH-CH520",
  "Teclado Mecánico Redragon",
  "Laptop HP Pavilion Ryzen 5",
  "Monitor LG UltraWide 29''",
  "SSD Kingston NV2 1TB",
  "Memoria RAM Corsair Vengeance 16GB",
  "Parlantes Logitech Z333",
  "Impresora Epson EcoTank L3250",
  "Router TP-Link Archer AX23",
  "Teclado Logitech K380 Bluetooth",
  "Mouse Inalámbrico Logitech M185",
  "Audífonos JBL Tune 510BT",
  "Smartwatch Amazfit Bip U",
  "Cámara Web Logitech C920",
  "Disco Duro Externo Seagate 2TB",
  "Laptop Acer Aspire 5 i7",
  "MicroSD Samsung EVO 128GB",
  "Tablet Lenovo M10 HD",
  "Silla Gamer Cougar Explore",
  "Monitor Samsung 24'' 75Hz",
  "Cargador Portátil Xiaomi 20000mAh",
  "Micrófono HyperX SoloCast"
]

}

df = pd.DataFrame(data)

def recomendar(usuario):
    productos_usuario = df[df["usuario"] == usuario]["producto"].unique()
    
    otros = df[df["usuario"] != usuario]
    recomendados = otros[~otros["producto"].isin(productos_usuario)]["producto"].unique()
    
    return recomendados

print("Recomendación para Luis:", recomendar("Luis"))
