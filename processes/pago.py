
import json
import datetime

file_path1 = "files/pagos.json"

class Pago:
    def __init__(self, id, nombre):
        self._id = id
        self._nombre = nombre
        self._fecha = str(
            datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%Y %H:%M:%S")
        )

    def cambiarFormato(self):
        RegistroPago = dict(ID = self._id, Nombre = self._nombre, Fecha = self._fecha)
        return RegistroPago

    def registrarTransaccion(self):
        RegistroPago = self.cambiarFormato()
        with open(file_path1, "r") as f:
            data = json.load(f)

        data.append(RegistroPago)

        with open(file_path1, "w") as f:
            json.dump(data, f, indent=4)