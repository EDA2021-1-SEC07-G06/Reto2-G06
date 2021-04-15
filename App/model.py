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
from DISClib.DataStructures import mapstructure as ms
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import quicksort as qs
from DISClib.DataStructures import listiterator as it
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog(metodo, factor):
    
    """ Inicializa el catálogo de videos

    Crea una lista vacia para guardar todos los videos

    Se crean indices (Maps) por los siguientes criterios:
    Videos
    Categorias
    Id de categoria
    Nombres de categorias
    Nombres de paises

    Retorna el catalogo inicializado.
    """

    catalog =  { 'videos' : None, 'categorys': None ,
                 'categoryId' : None, 'categoryName' : None,
                 'country_name' : None}
    
    catalog['videos'] =  lt.newList('ARRAY_LIST')
    catalog['categorys'] = lt.newList('ARRAY_LIST', cmpfunction = cmpByIdCategory)
    

    catalog['categoryId'] = mp.newMap(100,
                                   maptype= metodo,
                                   loadfactor= factor,
                                   comparefunction = compareCategoryIds)
    catalog['categoryName'] = mp.newMap(100,
                                   maptype= metodo,
                                   loadfactor= factor,
                                   comparefunction = compareCategoryName)
    catalog['country_name'] = mp.newMap(100,
                                   maptype= metodo,
                                   loadfactor= factor,
                                   comparefunction = compareCountryNames)
    return catalog

# Funciones para creacion de datos

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

def newCountry(pubcountry):
    """
    Esta funcion crea la estructura de videos asociados
    a un país.
    """
    entry = {'country': "", "videos": None}
    entry['country'] = pubcountry
    entry['videos'] = lt.newList('SINGLE_LINKED', compareCountries)
    return entry

# Funciones para agregar informacion al catalogo
    
def addVideo(catalog, video):
    
    lt.addLast(catalog['videos'],video)
  #  addVideoIdCategory(catalog, video)
    addVideoNameCategory(catalog, video)
    addVideoCountry(catalog, video)



def addVideoIdCategory(catalog, video):

    identificador = video['category_id']
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

def addVideoNameCategory(catalog, video):
        
    identificador = video['category_id']
    existeCate = existeCategoria(catalog, identificador) 
    categName  = catalog['categoryName']
    if existeCate > 0:
        categ = lt.getElement(catalog['categorys'], existeCate)
        nombre = categ['name']
        existName = mp.contains(categName,nombre)
        if existName:
            entry = mp.get(categName,nombre)
            valor = me.getValue(entry)
            lt.addLast(valor['videos'],video)
    else: 
        categ = newCategory(identificador, 'desconocida')
        lt.addLast(categ['videos'], video)
    
    
    
    
def addCategory(catalog, category):
   
    nuevaCategoria = newCategory(category['id'],category['name'])
    lt.addLast(catalog['categorys'], nuevaCategoria)
    mp.put(catalog['categoryId'], int(category['id']), nuevaCategoria)
    mp.put(catalog['categoryName'], category['name'].strip(), nuevaCategoria)

    
def addVideoCountry(catalog, video):
    """
    Esta funcion adiciona un video a la lista de videos de un pais especifico.
    Los paises se guardan en un Map, donde la llave es el pais
    y el valor la lista de videos de ese pais.
    """
    countries = catalog['country_name']
    pubcountry = video["country"]
    existcountries = mp.contains(countries, pubcountry)
    if existcountries:
        entry = mp.get(countries, pubcountry)
        country = me.getValue(entry)
    else:
        country = newCountry(pubcountry)
        mp.put(countries, pubcountry, country)
    lt.addLast(country['videos'], video)

def existeCategoria(catalog, identificador):

    categorys = catalog['categorys']
    categoryTosearch = newCategory(identificador, '')
    posCategory = lt.isPresent(categorys, categoryTosearch)
    return posCategory

def getInfoVideos(lista1, lista2, lista3):
    lista_final = []
    for elemento in range(0,len(lista2)):
        for d in range(0, len(lista1)):
            if lista1[d]["id"] == lista2[elemento] and lista1[d]["likes"] == lista3[elemento]:
                lista_final.append(lista1[d])
    
    return lista_final

# Funciones de consulta

def videosSize(catalog):
    """
    Número de videos en el catago
    """
    return lt.size(catalog['videos'])


def categorySize(catalog):
    """
    Número de videos en el catago
    """
    return lt.size(catalog['categoryId'])

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

def getTrendingVideo(catalog, category_name):
  
    categName  = catalog['categoryName']
    existName = mp.contains(categName,category_name.strip())
    masTrending = None
    Mayor = 0
    if existName:
        print('Lo encontro')
        entry = mp.get(categName,category_name.strip())
        valor = me.getValue(entry)
        videos = valor['videos']
        tamaño = lt.size(videos)
        pos = 0

        while tamaño > 0:
            pos1 = 0
            videoActual = lt.getElement(videos,pos)
            contador = 0 
            tamaño1 = lt.size(videos)   
            while tamaño1 > 0:
                videoComparado = lt.getElement(videos,pos1)

                if videoActual['title'] == videoComparado['title']:
                   contador += 1 
                
                pos1 += 1
                tamaño1 -= 1
                
            if contador > Mayor:
                   masTrending = videoActual
                   Mayor = contador
            contador = 0       
            pos += 1
            tamaño -= 1
    
    else:
        print('No se encontro la categoria.')
        resultado = {None,'n',0}
        
    resultado = masTrending, category_name.strip(), Mayor
    return resultado
        


# Funciones de ordenamiento

def getTrendingViews(catalog, category_name, country, n):
    videos_pais = mp.get(catalog['country_name'], country)
    videos_pais = me.getValue(videos_pais)
    videos_pais = videos_pais["videos"]
    lista_views = lt.newList('ARRAY_LIST')

    if videos_pais == None:
        return None
    else:
        iterador = it.newIterator(videos_pais)
        while it.hasNext(iterador):
            video = it.next(iterador)
            if int(video["category_id"]) == category_name:
                lt.addLast(lista_views, video)
                    
    lista_ordenada = qs.sort(lista_views, cmpVideosByViews)
    t_views = lt.size(lista_ordenada)
    
    if t_views <= n:
        listafinal = lt.subList(lista_ordenada,0,t_views)
    elif t_views > n:
        listafinal = lt.subList(lista_ordenada,0,n)
    return listafinal

def getTrendingCountry (catalog, country):
    videos_pais = mp.get(catalog['country_name'], country)
    videos_pais = me.getValue(videos_pais)
    videos_pais = videos_pais["videos"]
    #lista_id = lt.newList('ARRAY_LIST')
    lista_ids = lt.newList('ARRAY_LIST')
       
    if videos_pais == None:
        return None
    else:
        #iterador = it.newIterator(videos_pais)
        #while it.hasNext(iterador):
            #video = it.next(iterador)
            #if video not in mapa_id:
        #pos = 0
        for video in lt.iterator(videos_pais):
            lt.addLast(lista_ids, video["video_id"])
            #if int(lt.isPresent(lista_id, lista_ids[pos])) == 0:
                #lt.addLast(lista_id, video)
            #pos += 1

        lista_ordenada = qs.sort(lista_ids, compareCategoryIds)

            
        #recorrer la lista con un único id
        mas_trending = 0
        info_id = " "
        cont = 0
        infovideo = " "
        elemento = lt.firstElement(lista_ids)
        for video in lt.iterator(lista_ids):
            if elemento == video:
                cont += 1
            else:
                if cont > mas_trending:
                    mas_trending = cont
                    info_id = elemento
                    cont = 1
            elemento = video
        
        for video in lt.iterator(videos_pais):
            if info_id == video["video_id"]:
                infovideo = video
                
        return (mas_trending, infovideo)

        
    

def getTagCountry(catalog,country, pTag, num):
    countrys = catalog['country_name']
    existCountry  =  mp.contains(countrys,country.lower())
  
    lista = lt.newList('ARRAY_LIST')

    if existCountry:

        entry = mp.get(countrys, country.lower())
        valor = me.getValue(entry)

        videos = valor['videos']
        tamaño = lt.size(videos)
        pos = 0
        while tamaño > 0:
            videoActual = lt.getElement(videos, pos)
            tags = videoActual['tags'].lower()
            tags1 = tags.replace('"','')
            tags2 = tags1.replace('"','')     
            ltTags = tags2.split('|')

            tamTag = 0

            for t in ltTags:
               tamTag += 1

            posTag = 0
            while tamTag > 0:
                tag = ltTags[posTag]
                if tag == pTag:
                   lt.addLast(lista, videoActual)
                   tamTag = 0
                posTag += 1
                tamTag -= 1

            
            posTag = 0
            pos += 1
            tamaño -= 1
            
    else:
        print('El pais no esta registrado. ')
    
    if(lista == None):
        print('No se encontraron videos con el tag dado.')
    else:
        if(int(num) > lt.size(lista)):
            listaOrdenada = sa.sort(lista, cmpVideosByLikes)
            listaFinal = listaOrdenada
        else:
            
            listaOrdenada = sa.sort(lista, cmpVideosByLikes)
            listaFinal = lt.subList(listaOrdenada,0,int(num))
    
    
    return listaFinal

#  Funciones de comparación

def cmpVideosByViews(video1, video2):
    """ Devuelve verdadero (True) si los 'views' de video1 son mayores que los del video2 
    Args: video1: informacion del primer video que incluye su valor 'views'
          video2: informacion del segundo video que incluye su valor 'views' """
    return (float(video1['views']) > float(video2['views']))


def compareCategoryIds(id, entry):
    """
    Compara dos ids de categorias. 
    """
    identry = me.getKey(entry)
    if (int(id) == int(identry)):
        return 0
    elif (int(id) > int(identry)):
        return 1
    else:
        return -1

def compareCategoryName(keyname, name):
    """
    Compara dos nombres de categorias. El primero es una cadena
    y el segundo un entry de un map
    """
    namentry = me.getKey(name)
    if (keyname == namentry):
        return 0
    elif (keyname > namentry):
        return 1
    else:
        return -1


def compareCountryNames(name, country):
    """
    Compara dos nombres de paises. El primero es una cadena
    y el segundo un entry de un map
    """
    countentry = me.getKey(country)
    if (name == countentry):
        return 0
    elif (name > countentry):
        return 1
    else:
        return -1

def compareCountries(country1, country2):
    if country1 == country2:
        return 0
    elif country1 > country2:
        return 1
    else:
        return 0

def cmpVideosByLikes(video1, video2):
    """ Devuelve verdadero (True) si los 'likes' de video1 son menores que los del video2 
    Args: video1: informacion del primer video que incluye su valor 'likes'
          video2: informacion del segundo video que incluye su valor 'likes' """
    return (float(video1['likes']) > float(video2['likes']))
