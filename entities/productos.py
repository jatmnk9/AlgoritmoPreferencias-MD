import json

file_path = "files/productos.json"
file_path2 = "files/pedidos.json"

class Producto:
    def __init__(self, nombre, id, stock, categorias):
        self._nombre = nombre
        self._id = id
        self._stock = stock
        self._categorias = categorias
    
    def mostrarProducto():
        with open(file_path, "r") as f:
            productos = json.load(f)
        for element in productos:
            if element["Stock"] > 0:
                print()
                print("------------------------------------------------------")
                print("Nombre: " + element["Nombre"])
                print("Id: " + str(element["ID"]))
                print("Precio: " + str(element["Precio"]))
                print("------------------------------------------------------")

    def cambiarStock(numPedidos):
        for pedido in numPedidos:
            with open(file_path, "r") as f:
                data = json.load(f)
            for element in data:
                if element["ID"] == pedido:
                    element["Stock"] =  element["Stock"]-1

            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
