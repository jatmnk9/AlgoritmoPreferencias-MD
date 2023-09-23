from entities.user import Usuario
import json
from werkzeug.security import check_password_hash
import pandas as pd 
from processes.preferencia import Preferencia              
import numpy

file_path = "files/adminDatos.json"
file_path1 = "files/pedidos.json"
file_path2 = "files/productos.json"
file_path3 = "files/bebidas.json"
file_path5 = "files/comidas.json"
file_path4 = "files/pagos.json"

class Administrador(Usuario):
    def __init__(self, usuario, contrasenia, nombre, apellido, correo, llaveMaestra):
        super().__init__(usuario, contrasenia, nombre, apellido, correo)
        self._llaveMaestra = llaveMaestra

    def verify_session(given_User, given_Password):
        with open(file_path, "r") as f:
            usuario = json.load(f)

        for element in usuario:
            if element["usuario"] == given_User and check_password_hash(
                element["contrasenia"], given_Password
            ):
                print("Bienvenido, " + element["nombre"])
                llave = input("Ingrese su llame maestra para continuar: ")
                while check_password_hash(element["llave_maestra"], llave) == False:
                    print("Llave maestra incorrecta, intentelo nuevamente, por favor")
                    llave = input("Ingrese su llame maestra para continuar: ")
                return Administrador(
                    element["usuario"],
                    element["contrasenia"],
                    element["nombre"],
                    element["apellido"],
                    element["correo"],
                    element["llave_maestra"]
                )

    def calcularVentaTotal():
        venta = 0
        with open(file_path4, "r") as f:
            pagos = json.load(f)
        for element in pagos:
            with open(file_path2, "r") as f:
                productos = json.load(f)
            for producto in productos:
                if element["ID"]==producto["ID"]:
                    venta = venta + producto["Precio"]    
        return venta

    def calcularVentaBebidas():
        venta = 0
        with open(file_path3, "r") as f:
            bebidas = json.load(f)
        for bebida in bebidas:   
            with open(file_path4, "r") as f:
                pagos = json.load(f)
            for element in pagos:
                    if element["ID"] == bebida:
                        with open(file_path2, "r") as f:
                            productos = json.load(f)
                        for producto in productos:
                            if producto["ID"] == element["ID"]:
                                venta += producto["Precio"]
        return venta

    def calcularVentaComidas():
        venta = 0
        with open(file_path5, "r") as f:
            comidas = json.load(f)
        for comida in comidas:   
            with open(file_path4, "r") as f:
                pagos = json.load(f)
            for element in pagos:
                    if element["ID"] == comida:
                        with open(file_path2, "r") as f:
                            productos = json.load(f)
                        for producto in productos:
                            if producto["ID"] == element["ID"]:
                                venta += producto["Precio"]
        return venta

    def calcularPorcentaje(total,subtotal):
        porcentaje = float(subtotal/total*100.00)
        return porcentaje

    def calcularBebidaPotencial():
        arregloTotal=[]
        with open(file_path4, "r") as f:
            pagos = json.load(f)
        for element in pagos:
            arregloTotal.append(element["ID"])
        tipo = "bebida"
        listaBebidas = Preferencia.clasificarProductos(arregloTotal,tipo)
        lista = pd.Series(listaBebidas) 
        resultados = pd.Series(lista.value_counts())
        arreglo = numpy.array(resultados)
        cantPotencial = arreglo[0]
        for element in listaBebidas:
            if listaBebidas.count(element) == cantPotencial:
                bebidaPotencial = element
        with open(file_path2, "r") as f:
            productos = json.load(f)
        for element in productos:
            if element["ID"]==bebidaPotencial:
                bebida = element["Nombre"]
                precio = element["Precio"]
        print("--> La bebida más vendida fue: "+str(bebida))
        return precio*cantPotencial

    def calcularComidaPotencial():
        arregloTotal=[]
        with open(file_path4, "r") as f:
            pagos = json.load(f)
        for element in pagos:
            arregloTotal.append(element["ID"])
        tipo = "comida"
        listaComidas = Preferencia.clasificarProductos(arregloTotal,tipo)
        lista = pd.Series(listaComidas) 
        resultados = pd.Series(lista.value_counts())
        arreglo = numpy.array(resultados)
        cantPotencial = arreglo[0]
        for element in listaComidas:
            if listaComidas.count(element) == cantPotencial:
                comidaPotencial = element
        with open(file_path2, "r") as f:
            productos = json.load(f)
        for element in productos:
            if element["ID"]==comidaPotencial:
                comida = element["Nombre"]
                precio = element["Precio"]
        print("--> La comida más vendida fue: "+str(comida))
        return precio*cantPotencial
    



