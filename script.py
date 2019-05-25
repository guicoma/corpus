import os
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from recursivejson import extract_values
from xml.dom.minidom import parse, parseString


def iterator(parents, nested=False):
    for child in reversed(parents):
        if nested:
            if len(child) >= 1:
                iterator(child, nested=True)
        if child.tag == 'textarea':
            parents.remove(child)
        elif child.tag == 'i':
            parents.remove(child)
        elif child.tag == 'em':
            parents.remove(child)
        elif child.tag == 'st1':
            parents.remove(child)
        elif 'class' in child.attrib:
            if 'Emphasis' in child.get('class'):
                parents.remove(child)

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
        all_inputs = soup.find_all('input')
        
        for t_input in all_inputs:
            t_input.decompose()

        pageSanitized = unicode(soup)

        string = '<source>'+pageSanitized+'</source>'
        string = string.replace('w:st', 'st').replace(':city', '').replace(':place', '').replace(':street', '').replace(':address', '').replace('\r\n', '').replace('[', '').replace(']', '').replace('<p', '\r\n<p').replace('<br>', '\r\n').strip().encode('utf-8')

        try:
            root = ET.fromstring(string)
            if len(list(root)) <= 0:
                raise Exception('Tag seems not to contain the text, perhaps it is an image:')
            iterator(root, nested=True)
            resultText = ET.tostring(root, encoding='utf-8', method='text')
            print "----",idx,"----"
            if idx % 2 == 0:
                f2.write(resultText)
                # print "Spanish"
                # print resultText[0:20]
            else:
                f1.write(resultText)
                # print "English"
                # print resultText[0:20]
            
        except ET.ParseError as p_error:
            print 'Parse error',string
            print p_error
            continue
        except Exception as g_error:
            print 'General error'
            print g_error
            continue
        except:
            print 'Oops'
            continue


    f1.close()
    f2.close()
    read_file.close()
    #print(resultText)
