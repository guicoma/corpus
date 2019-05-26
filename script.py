import os
import json
import re
from bs4 import BeautifulSoup, Comment
from recursivejson import extract_values

files = os.listdir('source')

for file in files:
    extensionIndex = file.rfind(".")
    filename = file[:extensionIndex]
    print (file, filename)
    
    if not filename:
        print ('Skip file',file)
        continue
    
    with open('source/'+file, "r") as read_file:
        data = json.load(read_file)

    responseText = extract_values(data, 'text')
    responseType = extract_values(data, 'mimeType')
    responseBody = []
    indices = [i for i, x in enumerate(responseType) if x == "text/html"]

    for textIndex in indices:
        responseBody.append(responseText[textIndex])

    f1 = open('./result/'+filename+"_1.txt","wb")
    f2 = open('./result/'+filename+"_2.txt","wb")

    for idx, page in enumerate(responseBody):
        soup = BeautifulSoup(page, 'html.parser')
        
        all_comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in all_comments]
        
        all_br = soup.find_all('br')
        all_em = soup.find_all('em')
        all_emphasis = soup.find_all(class_="Emphasis")
        all_personajes = soup.find_all(class_="personaje_teatro")
        all_heads = soup.find_all('head')
        all_i = soup.find_all('i')
        all_inputs = soup.find_all('input')
        all_ops = soup.find_all('o:p')
        all_stds = soup.find_all(re.compile("st1"))
        all_styles = soup.find_all('style')
        all_txtareas = soup.find_all('textarea')

        all_tags = all_br + all_em + all_emphasis + all_i + all_inputs + all_heads + all_ops + all_personajes + all_stds + all_styles + all_txtareas

        for tag in all_tags:
            tag.decompose()

        for string in soup.stripped_strings:
            decodeStr = string.replace('[', '').replace(']', '')+'\n'
            resultLine = decodeStr.encode('utf-8')
            if idx % 2 == 0:
                f2.write(resultLine)
            else:
                f1.write(resultLine)

    f1.close()
    f2.close()
    read_file.close()