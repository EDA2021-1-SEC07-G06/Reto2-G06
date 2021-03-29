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
def newCatalog(metodo, factor):

    catalog =  { 'videos' : None, 'categorys': None , 'categoryId' : None, 'categoryName' : None,}
    
    catalog['videos'] =  lt.newList('ARRAY_LIST')
    catalog['categorys'] = lt.newList('ARRAY_LIST', cmpfunction = cmpByIdCategory)
    

    catalog ['categoryId'] = mp.newMap(100,
                                   maptype= metodo,
                                   loadfactor= factor
                                   )
    catalog ['categoryName'] = mp.newMap(100,
                                   maptype= metodo,
                                   loadfactor= factor
                                  )
    return catalog

def newCategory(id, name):
    """
    Crea una nueva estructura para modelar los videos de
    una categoria, su nombre e id.
    """
    categorys = {'id':'', 'name': '', 'videos': None }
    categorys['id'] = int(id)
    categorys['name'] = name.strip()
    categorys['videos'] = lt.newList('ARRAY_LIST')
    return categorys
    
def addVideo(catalog, video):
    
    lt.addLast(catalog['videos'],video)
    addVideoCategory(catalog, int(video['category_id']) , video)
    addVideoIdCategory(catalog, int(video['category_id']) , video)

def addVideoCategory(catalog, identificador, video):
    
    categorys = catalog['categorys']
    categoryTosearch = newCategory(identificador, '')
    posCategory = lt.isPresent(categorys, categoryTosearch)
    if posCategory > 0:
        
        categ = lt.getElement(categorys, posCategory)
        nombre = categ['name']
        categName  = catalog['categoryName']
        existName = mp.contains(categName,nombre)
        if existName:
            entry = mp.get(categName,nombre)
            valor = me.getValue(entry)
            lt.addLast(valor['videos'],video)
    else: 
        categ = newCategory(identificador, 'desconocida')
        lt.addLast(categorys, categ)
    lt.addLast(categ['videos'], video)

def addVideoIdCategory(catalog, identificador, video):
    categId = catalog['categoryId']
    existauthor = mp.contains(categId, identificador)
    if existauthor:
        entry = mp.get(categId, identificador)
        valor = me.getValue(entry)
        lt.addLast(valor['videos'],video)
    else: 
        nuevaCateg = newCategory(identificador, 'Sin nombre.')
        lt.addLast(nuevaCateg['videos'],video)
        mp.put(categId,identificador,nuevaCateg)


def addCategory(catalog, category):
   
    nuevaCategoria = newCategory(category['id'],category['name'])
    lt.addLast(catalog['categorys'], nuevaCategoria)
    mp.put(catalog['categoryId'], int(category['id']), nuevaCategoria)
    mp.put(catalog['categoryName'], category['name'], nuevaCategoria)
    



    
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

def cmpByIdCategory(cat1,cat2):

    idCat1 = cat1['id'] 
    idCat2 = cat2['id'] 
    if idCat1 == idCat2:
        return 0
    elif idCat1 < idCat2:
        return -1
    else:
        return 1


# Funciones de ordenamiento
