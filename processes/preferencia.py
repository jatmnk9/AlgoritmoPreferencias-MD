import json 
import numpy

file_path = "files/productos.json"
file_path1 = "files/bebidas.json"
file_path2 = "files/comidas.json"
file_path11 = "files/bebidasTabla.json"
file_path22 = "files/comidasTabla.json"

class Preferencia:
    def solicitarCalificaciones(arreglo):
        calificaciones = []

        with open(file_path, "r") as f:
            productos = json.load(f)

        for element in productos:
            for elemento in arreglo:
                if element["ID"] == elemento:
                    califica=int(input("Ingrese la calificacion del 1-10 de "+str(element["Nombre"])+":"))
                    while califica<1 or califica>10:
                        print("Calificacion invalida. Ingrese nuevamente.")
                        califica=int(input("Ingrese la calificacion del 1-10 de "+str(element["Nombre"])+":"))
                    calificaciones.append(califica)
        return calificaciones

    def clasificarProductos(productosSeleccionados,tipoProducto):
        arregloBebidas = []
        arregloComidas = []
    
        for producto in productosSeleccionados:
            
            if tipoProducto == "bebida":
                with open(file_path1, "r") as f:
                    bebidas = json.load(f)
                for element in bebidas:
                    if producto == element:
                        arregloBebidas.append(producto)
            elif tipoProducto == "comida":
                with open(file_path2, "r") as f:
                    comidas = json.load(f)
                for element in comidas:
                    if producto == element:
                        arregloComidas.append(producto)

        if tipoProducto == "bebida":
            return arregloBebidas 
        else:
            return arregloComidas


    def definirMatrizMadre(tipoProducto):
        if tipoProducto == "bebida":
            with open(file_path11, "r") as f:
                data = json.load(f)
        else: 
            with open(file_path22, "r") as f:
                data = json.load(f)
        
        matrizMadre = numpy.array(data)
        return matrizMadre

    def definirMatrizSeleccionados(matrizMadre,arregloProductos):
        cantProductos = len(arregloProductos)
        matriz1 = numpy.arange(1,((6*cantProductos)+1)).reshape(cantProductos,6)
        for f in range(cantProductos):
            for m in range(len(matrizMadre)):
                if matrizMadre[m][0] == arregloProductos[f]:
                    for k in range(6):
                        matriz1[f][k] = matrizMadre[m][k+1]
        return matriz1

    def definirMatriz11(calificaProductos,arregloProductos,matriz1):
        cantProductos = len(arregloProductos)
        matriz11 = numpy.arange(1,((6*cantProductos)+1)).reshape(cantProductos,6)

        for i in range(len(calificaProductos)):
            for j in range(len(matriz1)):
                for k in range(6):
                    matriz11[i][k] = matriz1[i][k] * calificaProductos[i]
        return matriz11
    

    def definirSumaColumnasMatriz11(matriz1,matriz11):

        arreglo1 = []
        for i in range(6):
            suma = 0
            for k in range(len(matriz1)):
                suma += matriz11[k][i]
            arreglo1.append(suma)

        return arreglo1                     


    def definirArregloPonderado(arregloProductos,arreglo1):

        cantProductos = len(arregloProductos)
        arreglo11 = []
        sumaArreglo1 = 0
        for element in arreglo1:
            sumaArreglo1 += element

        for element in arreglo1:
            arreglo11.append(element/sumaArreglo1)

        return arreglo11

    def definirMatriz12(matrizMadre,arregloProductos):
        cantProductos = len(arregloProductos)
        matriz12 = numpy.copy(matrizMadre)
    
        for f in range(cantProductos):
            for m in range(len(matrizMadre)):
                if matriz12[m][0] == arregloProductos[f]:
                    matriz12[m][0] = 0
                    for i in range(7):
                        matriz12[m][i] = 0

        return matriz12


    def definirMatrizMultiplicada(matriz12,arreglo11):
        nuevo = numpy.delete(matriz12, 0, axis=1)
        arreglox = []
        for j in range(len(nuevo)):
            for k in range(6):
                arreglox.append(float(nuevo[j][k]) * arreglo11[k])
        matriz15 = numpy.array(arreglox).reshape(nuevo.shape[0], 6)
        return matriz15


    def definirArregloSumaTotal(matriz15):
        arreglo2 = []
        for k in range(len(matriz15)):
            suma = 0
            for i in range(6):
                suma += matriz15[k][i]
            arreglo2.append(suma)
        return arreglo2                

    def definirRecomendaciones(arreglo2,tipoProducto):
        arregloFinal = []
        mayor = 0
        posiciones = []

        for i in range(len(arreglo2)):
            if arreglo2[i] >= mayor:    
                mayor = arreglo2[i]

        for i in range(len(arreglo2)):
            if arreglo2[i] == mayor:    
                posiciones.append(i)

        if tipoProducto == "bebida":
            with open(file_path1, "r") as f:
                data = json.load(f)
        else:
            with open(file_path2, "r") as f:
                data = json.load(f)

        for element in data:
            arregloFinal.append(element)
        
        with open(file_path, "r") as f:
                productos = json.load(f)
        
        recomendaciones = []
        
        for element in productos:
            for posicion in posiciones:
                    if element["ID"] == arregloFinal[posicion]:
                        recomendaciones.append(element["Nombre"])

        return recomendaciones

    def calcularRecomendaciones(productosSeleccionados,tipoProducto,calificaProductos):
        arregloProductos = Preferencia.clasificarProductos(productosSeleccionados,tipoProducto)
        matrizMadre = Preferencia.definirMatrizMadre(tipoProducto)
        matriz1 = Preferencia.definirMatrizSeleccionados(matrizMadre,arregloProductos)
        matriz11 = Preferencia.definirMatriz11(calificaProductos,arregloProductos,matriz1)
        arreglo1 = Preferencia.definirSumaColumnasMatriz11(matriz1,matriz11)                
        arreglo11 = Preferencia.definirArregloPonderado(arregloProductos,arreglo1)
        matriz12 = Preferencia.definirMatriz12(matrizMadre,arregloProductos)
        matriz15 = Preferencia.definirMatrizMultiplicada(matriz12,arreglo11)
        arreglo2 = Preferencia.definirArregloSumaTotal(matriz15)               
        recomendaciones = Preferencia.definirRecomendaciones(arreglo2,tipoProducto)
        return recomendaciones

