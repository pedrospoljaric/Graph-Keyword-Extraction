<<<<<<< HEAD
'''
Calcula a porcentagem de palavras chave compostas por base de dados
'''

import os
import glob
import re

totalPalavrasHulth = 0
totalCompostasHulth = 0

pastaInicial = os.getcwd()

pastaHulth = "..//..//Datasets//Hulth2003//Validation"
os.chdir(pastaHulth)
for arquivo in glob.glob("*.uncontr"):
	file = open(arquivo, 'r')
	# print arquivo
	palavras = re.split('; |;\t|;\n', file.read().replace('\n\t', ' '))
	for palavra in palavras:
		totalPalavrasHulth += 1
		if ' ' in palavra: totalCompostasHulth += 1
	file.close()

print 'Proporcao palavras compostas Hulth:', totalCompostasHulth/float(totalPalavrasHulth)
os.chdir(pastaInicial)

totalPalavrasMarujo = 0
totalCompostasMarujo = 0
pastaMarujo = "..//..//Datasets//Marujo2012//CorpusAndCrowdsourcingAnnotations//train"
os.chdir(pastaMarujo)
for arquivo in glob.glob("*.key"):
	file = open(arquivo, 'r')
	# print arquivo
	palavras = re.split('\n', file.read())
	for palavra in palavras:
		totalPalavrasMarujo += 1
		if ' ' in palavra: totalCompostasMarujo += 1
	file.close()

print 'Proporcao palavras compostas Marujo:', totalCompostasMarujo/float(totalPalavrasMarujo)
os.chdir(pastaInicial)

totalPalavrasSemeval = 0
totalCompostasSemeval = 0
pastaSemeval = "..//..//Datasets//Semeval2010//test_answer"
os.chdir(pastaSemeval)
file = open("test.combined.stem.final", 'r')

dados = re.split('\n| : ', file.read())

for i in range(len(dados)):
	if i % 2 == 1:
		palavras = dados[i].split(',')
		for palavra in palavras:
			totalPalavrasSemeval += 1
			if ' ' in palavra: totalCompostasSemeval += 1

file.close()

=======
'''
Calcula a porcentagem de palavras chave compostas por base de dados
'''

import os
import glob
import re

totalPalavrasHulth = 0
totalCompostasHulth = 0

pastaInicial = os.getcwd()

pastaHulth = "..//..//Datasets//Hulth2003//Validation"
os.chdir(pastaHulth)
for arquivo in glob.glob("*.uncontr"):
	file = open(arquivo, 'r')
	# print arquivo
	palavras = re.split('; |;\t|;\n', file.read().replace('\n\t', ' '))
	for palavra in palavras:
		totalPalavrasHulth += 1
		if ' ' in palavra: totalCompostasHulth += 1
	file.close()

print 'Proporcao palavras compostas Hulth:', totalCompostasHulth/float(totalPalavrasHulth)
os.chdir(pastaInicial)

totalPalavrasMarujo = 0
totalCompostasMarujo = 0
pastaMarujo = "..//..//Datasets//Marujo2012//CorpusAndCrowdsourcingAnnotations//train"
os.chdir(pastaMarujo)
for arquivo in glob.glob("*.key"):
	file = open(arquivo, 'r')
	# print arquivo
	palavras = re.split('\n', file.read())
	for palavra in palavras:
		totalPalavrasMarujo += 1
		if ' ' in palavra: totalCompostasMarujo += 1
	file.close()

print 'Proporcao palavras compostas Marujo:', totalCompostasMarujo/float(totalPalavrasMarujo)
os.chdir(pastaInicial)

totalPalavrasSemeval = 0
totalCompostasSemeval = 0
pastaSemeval = "..//..//Datasets//Semeval2010//test_answer"
os.chdir(pastaSemeval)
file = open("test.combined.stem.final", 'r')

dados = re.split('\n| : ', file.read())

for i in range(len(dados)):
	if i % 2 == 1:
		palavras = dados[i].split(',')
		for palavra in palavras:
			totalPalavrasSemeval += 1
			if ' ' in palavra: totalCompostasSemeval += 1

file.close()

>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
print 'Proporcao palavras compostas Semeval:', totalCompostasSemeval/float(totalPalavrasSemeval)