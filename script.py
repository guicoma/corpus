import os
import json
import re
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup, Comment
from recursivejson import extract_values
from xml.dom.minidom import parse, parseString

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
        #raise Exception("Debug")

        # def iterator(parents, nested=False):
        #     for child in reversed(parents):
        #         if nested:
        #             if len(child) >= 1:
        #                 iterator(child, nested=True)
        #         if child.tag == 'textarea':
        #             parents.remove(child)
        #         elif child.tag == 'i':
        #             parents.remove(child)
        #         elif child.tag == 'em':
        #             parents.remove(child)
        #         elif 'class' in child.attrib:
        #             if 'Emphasis' in child.get('class'):
        #                 parents.remove(child)

        # string = unicode(soup)
        # stringSource = '<source>'+string+'</source>'
        # pageSanitized = stringSource.replace('\r\n', '').replace('[', '').replace(']', '').replace('<p', '\r\n<p').replace('<br>', '\r\n').replace('<br/>', '\r\n').strip().encode('utf-8')

        # try:
        #     root = ET.fromstring(pageSanitized)
        #     if len(list(root)) <= 0:
        #         raise Exception('Tag seems not to contain the text, perhaps it is an image:')
        #     #iterator(root, nested=True)
        #     resultText = ET.tostring(root, encoding='utf-8', method='text')
        #     print "----",idx,"----"
        #     if idx % 2 == 0:
        #         f2.write(resultText)
        #         # print "Spanish"
        #         # print resultText[0:20]
        #     else:
        #         f1.write(resultText)
        #         # print "English"
        #         # print resultText[0:20]
            
        # except ET.ParseError as p_error:
        #     print 'Parse error',pageSanitized
        #     print p_error
        #     continue
        # except Exception as g_error:
        #     print 'General error'
        #     print g_error
        #     continue
        # except:
        #     print 'Oops'
        #     continue


    # f1.close()
    # f2.close()
    # read_file.close()
    #print(resultText)
