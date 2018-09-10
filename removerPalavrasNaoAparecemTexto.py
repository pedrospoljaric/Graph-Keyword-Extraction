<<<<<<< HEAD
'''
Criar arquivos apenas com as palavras chave que aparecem no texto processado
'''

import os
import glob
import re
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer

owd = os.getcwd() # ~/Programas

porter_stemmer = PorterStemmer()

def Morphyzar(txtIn):
    palavras = []

    for item in txtIn:
        # print item
        palavra = str(wn.morphy(item.lower()))
        palavras.append(palavra.upper() if  palavra != 'None' else str(item.upper()))
    return palavras

def RemoverPontuacao(txtIn):
	'''Remove todos os caracteres que nao forem letras (A-Z or a-z).'''
	txtOut = ''
	chAnterior = 32
	for char in txtIn:
		if char.isalpha() or (char.isspace() and chAnterior != 32) or char == "'":
			txtOut += char.lower()
		chAnterior = ord(char)
	return txtOut

def Stemmizar(txtIn):
    palavras = []

    for item in txtIn:
        palavra = str(porter_stemmer.stem(item.lower()))
        palavras.append(palavra.upper() if  palavra != 'None' else str(item.upper()))
    return palavras

def ModificarPalavrasChave(pastaPalavrasChave, pastaTextos, pastaSaida, delimiters, stem):
	os.chdir(pastaPalavrasChave)
	files = glob.glob("*.txt")
	os.chdir(owd)

	for arq in files:
		fileTexto = open(pastaTextos + '\\' + arq, 'r')
		palavrasTexto = re.split(' ', fileTexto.read().replace('\n\t', ' '))
		if stem: palavrasTexto = Stemmizar(palavrasTexto)
		# print palavrasTexto

		filePalavras = open(pastaPalavrasChave + '\\' + arq, 'r')
		palavrasChave = re.split(delimiters, filePalavras.read().replace('\n\t', ' '))

		palavrasChaveSplit = set()
		for item in palavrasChave:
			palavras = item.split(' ')
			for palavra in palavras:
				palavrasChaveSplit.add(RemoverPontuacao(palavra).replace('\n', '').upper())
		palavrasChaveSplit = list(palavrasChaveSplit)
		if not stem: palavrasChaveSplit = Morphyzar(palavrasChaveSplit)

		fileSaida = open(pastaSaida + '\\' + arq, 'w')

		textoSaida = []
		for palavra in palavrasChaveSplit:
			if palavra in palavrasTexto:
				textoSaida.append(palavra)
		# print arq, len(textoSaida), palavrasChaveSplit
		for i in range(len(textoSaida)-1):
			fileSaida.write(textoSaida[i] + ';')
		fileSaida.write(textoSaida[len(textoSaida)-1])

		fileSaida.close()

pastaPalavrasChave = '..\\..\\Datasets\\Hulth2003\\PalavrasChave'
pastaTextos = '..\\..\\Datasets\\Hulth2003\\TextosProcessados'
pastaSaida = '..\\..\\Datasets\\Hulth2003\\PalavrasChaveQueAparecem'
delimiters = '; |;\t|;\n'
# ModificarPalavrasChave(pastaPalavrasChave, pastaTextos, pastaSaida, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Marujo2012\\PalavrasChave'
pastaTextos = '..\\..\\Datasets\\Marujo2012\\TextosProcessados'
pastaSaida = '..\\..\\Datasets\\Marujo2012\\PalavrasChaveQueAparecem'
delimiters = '\n'
# ModificarPalavrasChave(pastaPalavrasChave, pastaTextos, pastaSaida, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Semeval2010\\PalavrasChave'
pastaTextos = '..\\..\\Datasets\\Semeval2010\\TextosProcessados'
pastaSaida = '..\\..\\Datasets\\Semeval2010\\PalavrasChaveQueAparecem'
delimiters = ','
ModificarPalavrasChave(pastaPalavrasChave, pastaTextos, pastaSaida, delimiters, True)
=======
'''
Criar arquivos apenas com as palavras chave que aparecem no texto processado
'''

import os
import glob
import re
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer

owd = os.getcwd() # ~/Programas

porter_stemmer = PorterStemmer()

def Morphyzar(txtIn):
    palavras = []

    for item in txtIn:
        # print item
        palavra = str(wn.morphy(item.lower()))
        palavras.append(palavra.upper() if  palavra != 'None' else str(item.upper()))
    return palavras

def RemoverPontuacao(txtIn):
	'''Remove todos os caracteres que nao forem letras (A-Z or a-z).'''
	txtOut = ''
	chAnterior = 32
	for char in txtIn:
		if char.isalpha() or (char.isspace() and chAnterior != 32) or char == "'":
			txtOut += char.lower()
		chAnterior = ord(char)
	return txtOut

def Stemmizar(txtIn):
    palavras = []

    for item in txtIn:
        palavra = str(porter_stemmer.stem(item.lower()))
        palavras.append(palavra.upper() if  palavra != 'None' else str(item.upper()))
    return palavras

def ModificarPalavrasChave(pastaPalavrasChave, pastaTextos, pastaSaida, delimiters, stem):
	os.chdir(pastaPalavrasChave)
	files = glob.glob("*.txt")
	os.chdir(owd)

	for arq in files:
		fileTexto = open(pastaTextos + '\\' + arq, 'r')
		palavrasTexto = re.split(' ', fileTexto.read().replace('\n\t', ' '))
		if stem: Stemmizar(palavrasTexto)
		# print palavrasTexto

		filePalavras = open(pastaPalavrasChave + '\\' + arq, 'r')
		palavrasChave = re.split(delimiters, filePalavras.read().replace('\n\t', ' '))

		palavrasChaveSplit = set()
		for item in palavrasChave:
			palavras = item.split(' ')
			for palavra in palavras:
				palavrasChaveSplit.add(RemoverPontuacao(palavra).replace('\n', '').upper())
		palavrasChaveSplit = list(palavrasChaveSplit)
		if not stem: palavrasChaveSplit = Morphyzar(palavrasChaveSplit)

		fileSaida = open(pastaSaida + '\\' + arq, 'w')

		textoSaida = []
		for palavra in palavrasChaveSplit:
			if palavra in palavrasTexto:
				textoSaida.append(palavra)
		# print arq, len(textoSaida), palavrasChaveSplit
		for i in range(len(textoSaida)-1):
			fileSaida.write(textoSaida[i] + ';')
		fileSaida.write(textoSaida[len(textoSaida)-1])

		fileSaida.close()

pastaPalavrasChave = '..\\..\\Datasets\\Hulth2003\\PalavrasChave'
pastaTextos = '..\\..\\Datasets\\Hulth2003\\TextosProcessados'
pastaSaida = '..\\..\\Datasets\\Hulth2003\\PalavrasChaveQueAparecem'
delimiters = '; |;\t|;\n'
ModificarPalavrasChave(pastaPalavrasChave, pastaTextos, pastaSaida, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Marujo2012\\PalavrasChave'
pastaTextos = '..\\..\\Datasets\\Marujo2012\\TextosProcessados'
pastaSaida = '..\\..\\Datasets\\Marujo2012\\PalavrasChaveQueAparecem'
delimiters = '\n'
ModificarPalavrasChave(pastaPalavrasChave, pastaTextos, pastaSaida, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Semeval2010\\PalavrasChave'
pastaTextos = '..\\..\\Datasets\\Semeval2010\\TextosProcessados'
pastaSaida = '..\\..\\Datasets\\Semeval2010\\PalavrasChaveQueAparecem'
delimiters = ','
ModificarPalavrasChave(pastaPalavrasChave, pastaTextos, pastaSaida, delimiters, True)
>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
