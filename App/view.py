"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Videos con más likes para una categoría")

catalog = None

def initCatalog(tipo, factor):
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog(tipo,factor)

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    return controller.loadData(catalog)

def printLikesData(videos):
    size = len(videos)
    if size:
        print("\n Estos son los mejores videos: \n")
        for video in range (0, len(videos)):
            print(' \nTitulo: ' + videos[video]['title'] + ' \nCanal: ' + videos[video]['cannel_title'] +
                   ' \nTiempo de publicación: ' + videos[video]['publish_time'] +
                   ' \nVistas: ' +videos[video]['views'] + ' \nLikes: ' +videos[video]['likes'] + 
                   ' \nDislikes: ' + videos[video]['dislikes'] + ' \nTags: ' + videos[video]['tags'] + "\n")
    else:
        print('No se encontraron videos')


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        rta = input("Seleccione el tipo de carga:\n" + "1. PROBING\n" + "2. CHAINING\n")
        if(int(rta) == 1):
            tipo = 'PROBING'
        elif(int(rta) == 2):
            tipo = 'CHAINING'
        else:
            print("Fuera de rango.")
            sys.exit(0)
        factor = input("Digite el factor de carga:\n")
        print("Cargando información de los archivos ....")
        catalog = initCatalog(tipo, float(factor))
        respuesta = loadData(catalog)
        resultado = ('Videos cargados: ' + str(lt.size(catalog['videos'])))
        print(resultado)
        print("Tiempo [ms]: ", f"{respuesta[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{respuesta[1]:.3f}")

    elif int(inputs[0]) == 2:
        categoria = input("Ingrese la categoría a consultar: ")
        n = int(input("Ingrese el número de videos que quiere listar: "))
        mas_likes =  controller.getVideosByLikes(catalog, categoria, n)
        printLikesData(mas_likes)
    else:
        sys.exit(0)
sys.exit(0)
