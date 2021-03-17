"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():

    catalog =  { 'videos' : None, 'categoryId' : None, 'categoryName' : None,}
    
    catalog['videos'] =  lt.newList('ARRAY_LIST')
    

    catalog ['categoryId'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4.0
                                   )
    catalog ['categoryName'] = mp.newMap(100,
                                   maptype='CHAINING',
                                   loadfactor=4.0
                                  )
    
def newCategory(id, name):
    """
    Crea una nueva estructura para modelar los videos de
    una categoria, su nombre e id.
    """
    categorys = {'id': id, 'name': name.strip(), 'videos': None }
    
    categorys['videos'] = lt.newList('ARRAY_LIST')
    return categorys
    
def addVideo(catalog, video):
    
    lt.addLast(catalog['videos'],video)
    addVideoCategory(catalog, video['category_id'] , video)

def addVideoCategory(catalog, idCategory, video):
    categoryId = catalog['categoryId']
    existCategory = mp.contains(categoryId, idCategory)
    if existCategory:
        entry = mp.get(categoryId, idCategory)
        categoriaId = me.getValue(entry)

    else:
        categoria = newCategory(idCategory,'')
        mp.put(categoryId, idCategory , categoria)
        entry = mp.get(categoryId, idCategory)
        categoriaId = me.getValue(entry)

    lt.addLast(categoriaId['videos'], video)
    

def addCategory(catalog, category):

    nuevaCategoria = newCategory(int(category['id']), category['name'])
    mp.put(catalog['categoryId'], int(category['id']), nuevaCategoria)
    mp.put(catalog['categoryName'], int(category['name']), nuevaCategoria)
    



    
# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos


def getVideosByLikes(catalog, categoria, n):
    list_videos_pais = []
    dict = {}
    lista_videos_likes = []

    for video in lt.iterator(catalog["videos"]):
        if video["category"] == categoria:
            dict["id"] = video["video_id"]
            dict["title"] = video["title"]
            dict["cannel_title"] = video["channel_title"]
            dict["publish_time"] = video["publish_time"]
            dict["views"] = video["views"]
            dict["likes"] = video["likes"]
            dict["dislikes"] = video["dislikes"]
            dict["tags"] = video["tags"]
            dict["trending_date"] = video["trending_date"]
            lista_videos_likes.append((video["likes"],video["video_id"]))
            list_videos_pais.append(dict)
            dict = {}
    
    lista_videos_likes.sort()

    lista_id_elegido = []
    lista_likes_elegido = []

    pos = len(lista_videos_likes)- 1
    x = len(lista_videos_likes) - n

    if x > 0:
        while pos >= x and x >= 0:
            if lista_videos_likes[pos][1] not in lista_id_elegido:
                lista_id_elegido.append(lista_videos_likes[pos][1])
                lista_likes_elegido.append(lista_videos_likes[pos][0])
            else:
                x -= 1
            pos -= 1
            
    else:
        while pos >= 0:
            if lista_videos_likes[pos][1] not in lista_id_elegido:
                lista_id_elegido.append(lista_videos_likes[pos][1])
                lista_likes_elegido.append(lista_videos_likes[pos][0])
            pos -= 1

    respuesta = getInfoVideos(list_videos_pais, lista_id_elegido, lista_likes_elegido)
    return respuesta
    

def getInfoVideos(lista1, lista2, lista3):
    lista_final = []
    for elemento in range(0,len(lista2)):
        for d in range(0, len(lista1)):
            if lista1[d]["id"] == lista2[elemento] and lista1[d]["likes"] == lista3[elemento]:
                lista_final.append(lista1[d])
    
    return lista_final

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
