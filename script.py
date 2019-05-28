import os
import json
import re
from bs4 import BeautifulSoup, Comment
from recursivejson import extract_values

# Listar todos los archivos ubicados en la carpeta 'source'
files = os.listdir('source')

for file in files:
    extensionIndex = file.rfind(".")
    filename = file[:extensionIndex]
    print (file, filename)

    # En caso de que el fichero no tiene nombre
    # saltar al siguiente fichero(.gitignore)
    if not filename:
        print ('Skip file',file)
        continue
    
    # Abrir el fichero y cargar formato JSON
    source_file = open('./source/'+file, "r")
    data = json.load(source_file)

    # Extraer todas las respuestas del server,
    # únicamente los que contienen el código HTML
    responseText = extract_values(data, 'text')
    responseType = extract_values(data, 'mimeType')
    responseBody = []
    indices = [i for i, x in enumerate(responseType) if x == "text/html"]

    for textIndex in indices:
        responseBody.append(responseText[textIndex])

    # Preparar ficheros para escribir las lineas que se extraeran del HTML.
    # Los ficheros se podrán en la carpeta 'result'.
    result_file1 = open('./result/'+filename+"_1.txt","wb")
    result_file2 = open('./result/'+filename+"_2.txt","wb")

    # Parseamos el HTML que representa cada página que se carga.
    for idx, page in enumerate(responseBody):
        soup = BeautifulSoup(page, 'html.parser')
        
        # Eliminamos todos los comentarios dentro del códgo HTML.
        all_comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in all_comments]
        
        # Eliminamos las siguientes etiquetas que no contienen información relevante.
        # También eliminados la etiquetas que contienen la clas "Emphasis" y "personaje_teatro".
        tags_to_remove = ['br', 'em', 'head', 'i', 'input', 'textarea', 'style', 'o:p', re.compile("st1")]
        tags = soup.find_all(tags_to_remove)
        emphasis = soup.find_all(class_="Emphasis")
        personajes = soup.find_all(class_="personaje_teatro")

        all_tags = tags + emphasis + personajes
        for tag in all_tags:
            tag.decompose()

        # De las etiquetas restantes, extraemos el contenido de dentro
        # y limpiamos caracteres residuales y introducimos el contenido
        # como una linea en el fichero de salida
        for string in soup.stripped_strings:
            decodeStr = string.replace('[', '').replace(']', '')+'\n'
            resultLine = decodeStr.encode('utf-8')
            if idx % 2 == 0:
                result_file2.write(resultLine)
            else:
                result_file1.write(resultLine)

    # Cerramos los ficheros con los que hemos trabajado
    result_file1.close()
    result_file2.close()
    source_file.close()