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
from DISClib.Algorithms.Sorting import quicksort as qs
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

def existeCategoria(catalog, identificador):

    categorys = catalog['categorys']
    categoryTosearch = newCategory(identificador, '')
    posCategory = lt.isPresent(categorys, categoryTosearch)
    return posCategory

    
def addVideoCountry(catalog, video):
    """
    Esta funcion adiciona un video a la lista de videos de un pais especifico.
    Los paises se guardan en un Map, donde la llave es el pais
    y el valor la lista de videos de ese pais.
    """
    try:
        countries = catalog['country_name']
        pubcountry = video["country"]
        existcountries = mp.contains(countries, pubcountry)
        if existcountries:
            entry = mp.get(countries, pubcountry)
            country = me.getValue(entry)
        else:
            country = newCountry(pubcountry)
            mp.put(countries, pubcountry, country)
        lt.addLast(country['video'], video)
    except Exception:
        return None

def newCountry(pubcountry):
    """
    Esta funcion crea la estructura de videos asociados
    a un país.
    """
    entry = {'country': "", "videos": None}
    entry['country'] = pubcountry
    entry['videos'] = lt.newList('SINGLE_LINKED', compareCountries)
    return entry

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
        
def prueba(catalog):
    
    cat = catalog['categoryName']
    print(mp.size(cat))


# Funciones de ordenamiento

def getTrendingViews(catalog, category_name, country, n):
    videos_pais = mp.get(catalog['country_name'], country)
    
    tamaño = mp.size(videos_pais)
    tamaño_map = size_mapa(tamaño)
    mapa_views = mp.newMap(tamaño_map, maptype= "CHAINING", loadfactor = 2)
    lista_views = lt.newList('ARRAY_LIST')

    if videos_pais == None:
        return None
    else:
        for video in videos_pais:
            if video["category"] == category_name:
                mp.put(mapa_views, video["video_id"], video)
                lt.addLast(lista_views, video["views"])
                    
    lista_ordenada = qs.sort(lista_views, cmpVideosByViews)
    t_views = lt.size(lista_ordenada)
    
    if t_views <= n:
        listafinal = lt.subList(lista_ordenada,0,t_views)
    elif t_views > n:
        listafinal = lt.subList(lista_ordenada,0,n)

    resultado = getdatosVideos(listafinal, mapa_views)
    
    return resultado 

def getdatosVideos(lista1, map):
    #crear el nuevo mapa de respuestas
    tamaño = mp.size(map)
    tamaño_map = size_mapa(tamaño)
    resultado = mp.newMap(tamaño_map, maptype= "CHAINING", loadfactor = 2)
    
    #buscar la info de los videos en el mapa, llenar el mapa y devolver un nuevo mapa
    for views in lista1:
        for video in map:
            if views == video["views"]:
                mp.put(resultado, video["views"], video)
    
    return resultado


def getTrendingCountry (catalog, country):
    #print("En getTrendingCountry "+country)
    videos_pais = mp.get(catalog['country_name'], country)
    #print(catalog)
    print("videos del pais")
    print(videos_pais)
    if videos_pais:
        tamaño = mp.size(videos_pais)
        tamaño_map = size_mapa(tamaño)
        mapa_id = mp.newMap(tamaño_map, type= "CHAINING", loadfactor = 2)

        for video in videos_pais:
            if video not in mapa_id:
                mp.put(mapa_id, video["video_id"], 1)
            else:
                resultado = mp.get(mapa_id, video["video_id"])
                mp.put(mapa_id, video["video_id"], (resultado[1]+ 1))
    else: 
        return None

    print("Tamanno "+ str(tamaño))
    mas_trending = ""
    dias_trending = 0
    for video in mapa_id:
        v = mp.get(mapa_id, video)
        if v[1] > dias_trending:
            dias_trending = v[1]
            mas_trending = v[0]

    for video in mapa_id:
        if video == mas_trending:
            titulo = video["title"]
            canal = video["cannel_title"]
            return (titulo, canal, country, dias_trending)

def es_primo (num):
    resultado = True
    for n in range(2,num):
        if num % n == 0:
            resultado = False
    return resultado

def size_mapa (num):
    size = (num*2) + 1
    terminar = 1

    while terminar > 0:
        if es_primo(size) == True:
            terminar = 0
        else:
            size += 1
    return size

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