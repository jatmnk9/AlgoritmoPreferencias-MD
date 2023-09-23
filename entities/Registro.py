import datetime
import json

file_path = "files/pedidos.json"
file_path2 = "files/productos.json"

class Registro:
    def __init__(self, numPedidos,monto):
        self._numPedidos = numPedidos
        self._monto = monto
        self._fecha = str(
            datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y %H:%M:%S")
        )

    def registrar(self):
        registran = dict(fecha=self._fecha,numPedidos=self._numPedidos,monto=self._monto)
        with open(file_path, "r") as f:
            data = json.load(f)
            
        data.append(registran)

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)

