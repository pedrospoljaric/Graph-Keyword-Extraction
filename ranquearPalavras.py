<<<<<<< HEAD
'''
Executa o programa keyWordGen.py em todos os arquivos das pastas e armazena os arquivos com as palavras ranqueadas em outras pastas
'''

import os
import glob

owd = os.getcwd() # ~/Programas

def Ranquear(pastaTextos, pastaSaida):

	os.chdir(pastaTextos)
	files = glob.glob("*.txt")
	os.chdir(owd)
	# for file in files:
	for i in range(45, len(files)):
	# for i in range(len(files)-1-10, -1, -1):
		print files[i]
		pastaEntrada = pastaTextos + '\\'
		# print 'python keywordGen.py ' + pastaEntrada + files[i] + ' ' + pastaSaida
		os.system('python keywordGen.py ' + pastaEntrada + files[i] + ' ' + pastaSaida)

pastaTextos = "..\\..\\Datasets\\Hulth2003\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadas"
# Ranquear(pastaTextos, pastaSaida)

pastaTextos = "..\\..\\Datasets\\Marujo2012\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadas"
# Ranquear(pastaTextos, pastaSaida)

pastaTextos = "..\\..\\Datasets\\Semeval2010\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadas"
# Ranquear(pastaTextos, pastaSaida)

# Com palavras compostas
pastaTextos = "..\\..\\Datasets\\Hulth2003\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadasCompostas"
# Ranquear(pastaTextos, pastaSaida)

pastaTextos = "..\\..\\Datasets\\Marujo2012\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadasCompostas"
Ranquear(pastaTextos, pastaSaida)

pastaTextos = "..\\..\\Datasets\\Semeval2010\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadasCompostas"
=======
'''
Executa o programa keyWordGen.py em todos os arquivos das pastas e armazena os arquivos com as palavras ranqueadas em outras pastas
'''

import os
import glob

owd = os.getcwd() # ~/Programas

def Ranquear(pastaTextos, pastaSaida):

	os.chdir(pastaTextos)
	files = glob.glob("*.txt")
	os.chdir(owd)
	# for file in files:
	for i in range(22, len(files)):
	# for i in range(len(files)-1-10, -1, -1):
		print files[i]
		pastaEntrada = pastaTextos + '\\'
		# print 'python keywordGen.py ' + pastaEntrada + files[i] + ' ' + pastaSaida
		os.system('python keywordGen.py ' + pastaEntrada + files[i] + ' ' + pastaSaida)

pastaTextos = "..\\..\\Datasets\\Hulth2003\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadas"
Ranquear(pastaTextos, pastaSaida)

pastaTextos = "..\\..\\Datasets\\Marujo2012\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadas"
Ranquear(pastaTextos, pastaSaida)

pastaTextos = "..\\..\\Datasets\\Semeval2010\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadas"
Ranquear(pastaTextos, pastaSaida)

# Com palavras compostas
pastaTextos = "..\\..\\Datasets\\Hulth2003\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadasCompostas"
# Ranquear(pastaTextos, pastaSaida)

pastaTextos = "..\\..\\Datasets\\Marujo2012\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadasCompostas"
# Ranquear(pastaTextos, pastaSaida)

pastaTextos = "..\\..\\Datasets\\Semeval2010\\TextosProcessados"
pastaSaida = "..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadasCompostas"
>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
# Ranquear(pastaTextos, pastaSaida)