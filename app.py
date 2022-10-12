from flask import Flask, request
app = Flask(__name__)
app.config["DEBUG"] = True

# Almacenamiento del pedido
# El cliente quiere un sistema de almacenamiento general de pedidos sin menus. Su idea es algo multiproposito ya que el restaurante tambien realiza cocina sobre pedido.

pedidos = [
  {
    "id":1,
    "pedido":"dos hamburguesas doble carne con pan",
    "valor_pagado":20000,
    "metodo_pago":"nequi",
    "fecha": "09-10-2022",
    "estado":"valido"
  },
  {
    "id":2,
    "pedido":"Una arroba de papas",
    "valor_pagado":30000,
    "metodo_pago":"efectivo",
    "fecha": "08-10-2022",
    "estado":"valido"
  },
  {
    "id":3,
    "pedido":"Mercado para apto 402",
    "valor_pagado":200000,
    "metodo_pago":"tarjeta debito",
    "fecha": "06-10-2022",
    "estado":"valido"
  }
]

# funciones generales

def obtener_id():
  tamanio = len(pedidos)
  id_mas_grande = 0
  for pedido in pedidos:
    if pedido["id"] > id_mas_grande:
      id_mas_grande = pedido["id"]
  if id_mas_grande == tamanio or tamanio > id_mas_grande:
    tamanio = tamanio + 1
    return tamanio
  elif id_mas_grande > tamanio:
    id_mas_grande = id_mas_grande + 1
    return id_mas_grande

# ENDPOINTS
# Creamos nuevos pedidos
@app.post("/pedido")
def nuevo_pedido():
  request_data = request.get_json()
  try:
    if request_data["pedido"] and request_data["valor_pagado"] and request_data["metodo_pago"] and request_data["fecha"] and request_data["estado"]:
      pedidos.append({
        "id": obtener_id(),
        "pedido": request_data["pedido"],
        "valor_pagado": request_data["valor_pagado"],
        "metodo_pago": request_data["metodo_pago"],
        "fecha": request_data["fecha"],
        "estado": request_data["estado"]
      })
      return request_data, 200
  except KeyError:
    return {"message": "informacion invalida"}, 400

# Obtienes todos los pedidos
@app.get("/pedidos")
def obtener_todos_pedidos():
  return {"pedidos":pedidos}, 200

# Obtienes un pedido en especifico
@app.get("/pedido/<int:id_pedido>")
def obtener_pedido(id_pedido):
  for pedido in pedidos:
      if pedido["id"] == id_pedido:
        return {
          "id": pedido["id"],
          "pedido":pedido["pedido"],
          "valor_pagado": pedido["valor_pagado"],
          "metodo_pago": pedido["metodo_pago"],
          "fecha": pedido["fecha"],
          "estado": pedido["estado"]
        }, 200
  return {"message": "id no encontrado"}, 404

# actualizas un pedido en especifico
@app.patch("/pedido/<int:id_pedido>")
def actualizar_pedido(id_pedido):
  request_data = request.get_json()
  try:
    if request_data["pedido"] and request_data["valor_pagado"] and request_data["metodo_pago"] and request_data["fecha"]:
      for pedido in pedidos:
        if pedido["id"] == id_pedido:
           pedido["pedido"] = request_data["pedido"]
           pedido["valor_pagado"] = request_data["valor_pagado"]
           pedido["metodo_pago"] = request_data["metodo_pago"]
           pedido["fecha"] = request_data["fecha"]
           pedido["estado"] = request_data["estado"]
      return request_data, 201
  except KeyError:
    return {"message": "informacion invalida"}, 400

# eliminar un pedido en especifico
@app.delete("/pedido/<int:id_pedido>")
def borrar_pedido(id_pedido):
  for pedido in pedidos:
    if pedido["id"] == id_pedido:
        pedido["estado"]= "invalido"
        return {"message": "Se ha ajustado el estado"}
    return {"message":"No se encuentra el id"}

