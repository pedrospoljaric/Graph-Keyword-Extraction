<<<<<<< HEAD
'''
Processa arquivo texto, removendo pontuacao e stopwords e lematizando o texto
Como usar:
python procDeTexto.py arquivoTexto pastaSaida arquivoStopWords1 arquivoStopWords2 arquivoStopWords3 ...
    - Gera um arquivo de texto processado na pastaSaida
'''

import sys
import nltk
import os
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

# pylint: disable-msg=C0103

lsArgs = sys.argv # argumentos terminal

lem = WordNetLemmatizer()

posDic = {'JJ': 'a', 'JJR': 'a', 'JJS': 'a',
          'VB': 'v', 'VBD': 'v', 'VBG': 'v', 'VBN': 'v', 'VBP': 'v', 'VBZ': 'v',
          'NN': 'n', 'NNP': 'n', 'NNPS': 'n', 'NNS': 'n',
          'RB': 'r', 'RBR': 'r', 'RBS': 'r', 'WRB': 'r'}

#Funcoes--------------------------------------------------------------------------------------------

def RemoverPontuacao(txtIn):
    '''Remove todos os caracteres que nao forem letras (A-Z or a-z).'''
    txtOut = ''
    chAnterior = 32
    for char in txtIn:
        if char.isalpha() or (char.isspace() and chAnterior != 32) or char == "'":
            txtOut += char.lower()
        chAnterior = ord(char)
    return txtOut

def RemoverStopWords(txtIn, stopWords):
    '''Remove todas as palavras contidas na lista de stopwords.'''
    lsOut = []
    for word in txtIn:
        if (word.lower() + '\n') not in stopWords and word != '' and len(word) > 4 and not word.isdigit():
            lsOut.append(word)
    return lsOut

def Lematizar(txtIn):
    '''Lematiza as palavras restantes do texto.'''
    text = word_tokenize(txtIn.lower())
    taggedWords = nltk.pos_tag(text) #list of tuples of strings
    palavras = []

    for item in taggedWords:
        if item[1] in posDic:
            word = lem.lemmatize(item[0], posDic[item[1]])
        else:
            word = lem.lemmatize(item[0])
        palavras.append(word)
    return palavras

def Morphyzar(txtIn):
    palavras = []

    for item in txtIn.split(' '):
        palavra = str(wn.morphy(item))
        palavras.append(palavra if  palavra != 'None' else str(item))
    return palavras
    
#---------------------------------------------------------------------------------------------------

stopWords = []
for i in range(3, len(lsArgs)):
    file_stopWords = open(lsArgs[i], 'r') # arquivo com a lista de stopwords
    stopWords.extend(file_stopWords.readlines())
    file_stopWords.close()

file_in = open(lsArgs[1], 'r') # input
txtIn = file_in.read()
file_in.close()

#-----------------------------------------------------------------------------------

pastaSaida = lsArgs[2]

# filename_out = (lsArgs[1])[0:-4]
# filename_out += '_out.txt'
# file_out = open(filename_out, 'w') # output

aux = lsArgs[1].split('\\')
nomeArq = (aux[-1].split('.'))[0]
filename_out = pastaSaida + '\\' + nomeArq + '.txt'
file_out = open(filename_out, 'w')

#-----------------------------------------------------------------------------------

txtSemPont = RemoverPontuacao(txtIn)
txtSemPont = txtSemPont.replace('\n', ' ').replace('\r', '').replace('\t', '')

txtMorphy = Morphyzar(txtSemPont)

# txtFinal = Lematizar(txtSemStop)
txtFinal = RemoverStopWords(txtMorphy, stopWords)

for item in txtFinal[:-1]:
    if (len(item) > 1):
        file_out.write(item.upper() + ' ')
if (len(txtFinal[-1]) > 1):
    file_out.write(txtFinal[-1].upper())

file_out.close()

print 'OUTPUT: ' + filename_out
=======
'''
Processa arquivo texto, removendo pontuacao e stopwords e lematizando o texto
Como usar:
python procDeTexto.py arquivoTexto pastaSaida arquivoStopWords1 arquivoStopWords2 arquivoStopWords3 ...
    - Gera um arquivo de texto processado na pastaSaida
'''

import sys
import nltk
import os
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn

# pylint: disable-msg=C0103

lsArgs = sys.argv # argumentos terminal

lem = WordNetLemmatizer()

posDic = {'JJ': 'a', 'JJR': 'a', 'JJS': 'a',
          'VB': 'v', 'VBD': 'v', 'VBG': 'v', 'VBN': 'v', 'VBP': 'v', 'VBZ': 'v',
          'NN': 'n', 'NNP': 'n', 'NNPS': 'n', 'NNS': 'n',
          'RB': 'r', 'RBR': 'r', 'RBS': 'r', 'WRB': 'r'}

#Funcoes--------------------------------------------------------------------------------------------

def RemoverPontuacao(txtIn):
    '''Remove todos os caracteres que nao forem letras (A-Z or a-z).'''
    txtOut = ''
    chAnterior = 32
    for char in txtIn:
        if char.isalpha() or (char.isspace() and chAnterior != 32) or char == "'":
            txtOut += char.lower()
        chAnterior = ord(char)
    return txtOut

def RemoverStopWords(txtIn, stopWords):
    '''Remove todas as palavras contidas na lista de stopwords.'''
    lsOut = []
    for word in txtIn:
        if (word.lower() + '\n') not in stopWords and word != '' and len(word) > 4 and not word.isdigit():
            lsOut.append(word)
    return lsOut

def Lematizar(txtIn):
    '''Lematiza as palavras restantes do texto.'''
    text = word_tokenize(txtIn.lower())
    taggedWords = nltk.pos_tag(text) #list of tuples of strings
    palavras = []

    for item in taggedWords:
        if item[1] in posDic:
            word = lem.lemmatize(item[0], posDic[item[1]])
        else:
            word = lem.lemmatize(item[0])
        palavras.append(word)
    return palavras

def Morphyzar(txtIn):
    palavras = []

    for item in txtIn.split(' '):
        palavra = str(wn.morphy(item))
        palavras.append(palavra if  palavra != 'None' else str(item))
    return palavras
    
#---------------------------------------------------------------------------------------------------

stopWords = []
for i in range(3, len(lsArgs)):
    file_stopWords = open(lsArgs[i], 'r') # arquivo com a lista de stopwords
    stopWords.extend(file_stopWords.readlines())
    file_stopWords.close()

file_in = open(lsArgs[1], 'r') # input
txtIn = file_in.read()
file_in.close()

#-----------------------------------------------------------------------------------

pastaSaida = lsArgs[2]

# filename_out = (lsArgs[1])[0:-4]
# filename_out += '_out.txt'
# file_out = open(filename_out, 'w') # output

aux = lsArgs[1].split('\\')
nomeArq = (aux[-1].split('.'))[0]
filename_out = pastaSaida + '\\' + nomeArq + '.txt'
file_out = open(filename_out, 'w')

#-----------------------------------------------------------------------------------

txtSemPont = RemoverPontuacao(txtIn)
txtSemPont = txtSemPont.replace('\n', ' ').replace('\r', '').replace('\t', '')

txtMorphy = Morphyzar(txtSemPont)

# txtFinal = Lematizar(txtSemStop)
txtFinal = RemoverStopWords(txtMorphy, stopWords)

for item in txtFinal[:-1]:
    if (len(item) > 1):
        file_out.write(item.upper() + ' ')
if (len(txtFinal[-1]) > 1):
    file_out.write(txtFinal[-1].upper())

file_out.close()

print 'OUTPUT: ' + filename_out
>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
