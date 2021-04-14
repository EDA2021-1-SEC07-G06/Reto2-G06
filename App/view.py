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
import model
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
    print("1- Inicializar Catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Video con más trending para una categoría")
    print("4- n videos con más views para un pais y categoria (req. 1)")
    print("5- video más trending para un país (req. 2)")
    print("0- Salir")


catalog = None

def initCatalog():
    """
    Inicializa el catalogo de videos
    """
    return controller.initCatalog(metodo, factor)

def loadData(catalog):
    """
    Carga los videos en la estructura de datos
    """
    controller.loadData(catalog)

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


def printCountryData(titulo, canal, country, dias_trending):
    print('Video encontrado: ' + titulo)
    print('Canal: ' + canal)
    print('País: ' + country)
    print('Número de días:' + str(dias_trending))

def printVideoData(video,catego, dias_trending):
    if video == None:
        print('Video encontrado: Ninguno')
        print('Canal: Ninguno')
    else: 
        print('Video encontrado: '+ str(video['title']) )
        print('Canal: ' + str(video['channel_title']))   
    
    print('Categoria: '+ str(catego))
    print('Numero de dias: '+ str(dias_trending))

"""
Menu principal
""" 
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 1:
        print("Inicializando Catálogo ....")
        predeterminado = input("¿Quiere usar el método y factor predeterminado? (si/no) ")
        if predeterminado == "si":
            metodo = "CHAINING"
            factor = int("4")
        elif predeterminado == "no":
            metodo = input("Ingrese el mecanismo de colisiones a utilizar (CHAINING/PROBING): ")
            factor = float(input("Ingrese el factor de carga: "))
        cont = controller.initCatalog(metodo, factor)
        catalog = cont 
        print("El catálogo fue inicializado")

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ...")

        answer = controller.loadData(cont)
        print('Videos cargados: ' + str(controller.videosSize(cont)))
        print('Categorias cargadas: ' + str(controller.categorySize(cont)))
        print("Tiempo [ms]: ", f"{answer[0]:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{answer[1]:.3f}")

    elif int(inputs[0]) == 3:
        categoria = input("Ingrese la categoría a consultar: ")
        mas_Trending =  controller.getTrendingVideo(catalog, categoria)
        printVideoData(mas_Trending[0], mas_Trending[1], mas_Trending[2])

    elif int(inputs[0]) == 4:
        country = input("Nombre del país: ")
        category_name = input("Categoría")
        n = input("Cantidad de videos")
        respuesta = controller.getTrendingViews(category_name, country, n)
        if respuesta == None:
            print("No se encontraron videos")
        else:
            printViewsData(respuesta)

    elif int(inputs[0]) == 5:
        country = input("Nombre del país: ")
        respuesta = controller.getTrendingCountry(cont, country)
        if respuesta == None:
            print("No se encontraron videos")
        else:
            printCountryData(respuesta)

    elif int(inputs[0]) == 6:
        model.prueba(catalog)

    else:
        sys.exit(0)
sys.exit(0)
