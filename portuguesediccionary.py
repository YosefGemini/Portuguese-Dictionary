# -*- coding: utf-8 -*-
pip install requests bs4 nltk pyphen xlsxwriter langid spacy

# importacion de librerias

import requests
from bs4 import BeautifulSoup
import nltk
# import csv
import xlsxwriter
import spacy
import spacy.cli
spacy.cli.download("pt_core_news_sm")
# from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import wordnet
# from nltk.tokenize import RegexpTokenizer
# nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('averaged_perceptron_tagger')
import pyphen
# import langid
import string

"""## Separacion en silabas"""

def portuguese_words_in_silabs(word):

  dict_hifenacion = pyphen.Pyphen(lang='pt')

  silab = dict_hifenacion.inserted(word)
  # print(silab)
  return silab
  # si deseo retornar en un nuevo arreglo
  # return sliab.split('-')

"""## Test de Silabilizado"""

# listado de lenguajes disponibles
print("lenguajes disponibles: \n", pyphen.LANGUAGES)
# palabra selparada en silabas
silab_word = portuguese_words_in_silabs('vagalume')
print("palabra vagalume en silabas: \n", silab_word)

"""## Clasificacion morfologica"""

def morfologic_label(word):
  #print('face 1')
  #wordnet.langs
  synsets = wordnet.synsets(word, lang='por')

  #print('fase 2',synsets)

  if synsets:
    #print ("synsets 0.pos: ", synsets[0].pos())
    #print ("synsets 0: ", synsets[0])
    morf = synsets[0].pos()

    if (morf == 'n'):return 'Sustantivo'
    if (morf == 'v'):return 'Verbo'
    if (morf == 'a'):return 'Adjetivo'
    if (morf == 'r'):return 'Adverbio'

  else:
    #word_token = nlp.ad
    # etiquetas_pos = nltk.pos_tag(word, lang='por')
    #print(etiquetas_pos)
    return None

"""## Test Clasificacion morfologica"""

#print("idiomas en wordnet \n", wordnet.langs)

morfolologic_label_word = morfologic_label('vagalume')

print("etiqueta morfologica", morfolologic_label_word)

"""## Verificacion de Palabra

"""

# def is_portuguese_word(word):
#     # Detectar el idioma principal de la palabra
#     lang, confidence = langid.classify(word)

#     # Verificar si el idioma detectado es portugués y la confianza es suficientemente alta
#     return lang == 'pt' and confidence > 0.5

"""## Extraccion de palabras"""

def extract_portuguese_words_2(url):
  response = requests.get(url)
  html = response.text

  soup = BeautifulSoup(html, 'html.parser')
  #print('fase 4')

  # obtengo el texto de la pagina web
  textContent = soup.get_text()

  #print('fase 5' , textContent[:20])

  nlp = spacy.load("pt_core_news_sm")

  doc = nlp(textContent)

  stop_words = set(stopwords.words('portuguese'))
  #portuguese_word = []
  portuguese_dict = []
  count = 1



  for token in doc:
    if not(token.pos_ =='PUNCT' or token.pos_=='SPACE' or token.pos_=='NUM'):
      silab = portuguese_words_in_silabs(token.text)
      #print(f"Palabra: {token.text}, POS Tag: {token.pos_}")
      portuguese_dict.append([count, token.text, silab, token.pos_])
      count = count + 1

  #filtered_words = set(portuguese_dict)

  #complete_dict = list(filtered_words)
  #result = list(filtered_repeated)
  return portuguese_dict

urlTest = 'https://www.dicio.com.br/lista-de-palavras/'
portuguese_dict = extract_portuguese_words_2(urlTest)


print('Primeras 20 palabras: \n ',portuguese_dict[:20])
print('tamaño de diccionario: \n ', len(portuguese_dict))

# def extract_portuguese_words(url):
#   # Obtengo el contenido de la Pasgina Web
#   #print('test Init')
#   response = requests.get(url)
#   #print('fase 1')
#   html = response.text
#   #print('fase 3')


#   # uso de BeautfulSoup para el analisis HTML
#   soup = BeautifulSoup(html, 'html.parser')
#   #print('fase 4')

#   # obtengo el texto de la pagina web
#   textContent = soup.get_text()
#   #print('fase 5')

#   # tokenizar el texto en palagras

#   #tokenizer = RegexpTokenizer(r'\w+')

#   words = word_tokenize(textContent, language='portuguese')
#   #print(words[:20])
#   #print('fase 6')
#   # filtrado de palabras

#   stop_words = set(stopwords.words('portuguese'))


#   #print('fase 7')
#   filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

#   filtered_repeated = set(filtered_words);

#   result = list(filtered_repeated)

#   return result

"""## Test de extraccion"""

# urlTest = 'https://www.dicio.com.br/lista-de-palavras/'
# portuguese_words = extract_portuguese_words(urlTest)


# print('Primeras 20 palabras: \n ',portuguese_words[:20])

"""## Exportacion a CSV"""

# with open("portuguese_dict.csv", "w") as csvfile:

#     # Crea un escritor CSV
#     writer = csv.writer(csvfile, delimiter=",")

#     # Escribe el arreglo de arreglos en el archivo CSV
#     for row in portuguese_dict:
#         writer.writerow(row)

"""## Exportacion a Excel"""

workbook = xlsxwriter.Workbook("portuguese_dict.xlsx")

# Crea una hoja de cálculo en el libro de trabajo
worksheet = workbook.add_worksheet()

# Escribe los encabezados en la hoja de cálculo

worksheet.write(0, 0, "Numero de palabra")
worksheet.write(0, 0, "Palabra")
worksheet.write(0, 1, "Silabas")
worksheet.write(0, 2, "Etiqueta Morfologica")

# Escribe el arreglo en la hoja de cálculo
for row in range(len(portuguese_dict)):
    for col in range(len(portuguese_dict[0])):
        worksheet.write(row + 1, col, portuguese_dict[row][col])

# Guarda el libro de trabajo de Excel
workbook.close()
