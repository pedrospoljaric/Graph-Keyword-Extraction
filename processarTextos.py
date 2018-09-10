<<<<<<< HEAD
'''
Executa o procDeTexto.py para todos os arquivos de uma pasta e armazena os textos processados em outra pasta
'''

import os
import glob

owd = os.getcwd() # ~/Programas

def Processar(pastaTextos, pastaSaida, extensaoArquivos, notInFile):
	os.chdir(pastaTextos)
	folders = glob.glob("*/")
	os.chdir(owd)
	if len(folders) > 0:
		for folder in folders:
			os.chdir(pastaTextos+'\\'+folder)
			files = glob.glob("*."+extensaoArquivos)
			os.chdir(owd)
			for file in files:
				if notInFile not in file:
					print file
					pastaEntrada = pastaTextos + '\\' + folder + '\\'
					os.system('python procDeTexto.py ' + pastaEntrada + file + ' ' + pastaSaida + ' ..\\..\\stopwords_ingles.txt ..\\..\\stopwords_adicionais.txt')

	else:
		os.chdir(pastaTextos)
		files = glob.glob("*."+extensaoArquivos)
		os.chdir(owd)
		for file in files:
			if notInFile not in file:
				print file
				pastaEntrada = pastaTextos + '\\'
				os.system('python procDeTexto.py ' + pastaEntrada + file + ' ' + pastaSaida + ' ..\\..\\stopwords_ingles.txt ..\\..\\stopwords_adicionais.txt')

pastaTextos = "..\\..\\Datasets\\Hulth2003\\Validation" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Hulth2003\\TextosProcessados"
extensaoArquivos = "abstr" # extensao dos arquivos de texto que serao processados
# Processar(pastaTextos, pastaSaida, extensaoArquivos, 'nenhumaRestricao')

pastaTextos = "..\\..\\Datasets\\Marujo2012\\CorpusAndCrowdsourcingAnnotations\\train" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Marujo2012\\TextosProcessados"
extensaoArquivos = "txt" # extensao dos arquivos de texto que serao processados
Processar(pastaTextos, pastaSaida, extensaoArquivos, 'justTitle')

pastaTextos = "..\\..\\Datasets\\Semeval2010\\test" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Semeval2010\\TextosProcessados"
extensaoArquivos = "final" # extensao dos arquivos de texto que serao processados
Processar(pastaTextos, pastaSaida, extensaoArquivos, 'nenhumaRestricao')
=======
'''
Executa o procDeTexto.py para todos os arquivos de uma pasta e armazena os textos processados em outra pasta
'''

import os
import glob

owd = os.getcwd() # ~/Programas

def Processar(pastaTextos, pastaSaida, extensaoArquivos, notInFile):
	os.chdir(pastaTextos)
	folders = glob.glob("*/")
	os.chdir(owd)
	if len(folders) > 0:
		for folder in folders:
			os.chdir(pastaTextos+'\\'+folder)
			files = glob.glob("*."+extensaoArquivos)
			os.chdir(owd)
			for file in files:
				if notInFile not in file:
					print file
					pastaEntrada = pastaTextos + '\\' + folder + '\\'
					os.system('python procDeTexto.py ' + pastaEntrada + file + ' ' + pastaSaida + ' ..\\..\\stopwords_ingles.txt ..\\..\\stopwords_adicionais.txt')

	else:
		os.chdir(pastaTextos)
		files = glob.glob("*."+extensaoArquivos)
		os.chdir(owd)
		for file in files:
			if notInFile not in file:
				print file
				pastaEntrada = pastaTextos + '\\'
				os.system('python procDeTexto.py ' + pastaEntrada + file + ' ' + pastaSaida + ' ..\\..\\stopwords_ingles.txt ..\\..\\stopwords_adicionais.txt')

pastaTextos = "..\\..\\Datasets\\Hulth2003\\Validation" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Hulth2003\\TextosProcessados"
extensaoArquivos = "abstr" # extensao dos arquivos de texto que serao processados
# Processar(pastaTextos, pastaSaida, extensaoArquivos, 'nenhumaRestricao')

pastaTextos = "..\\..\\Datasets\\Marujo2012\\CorpusAndCrowdsourcingAnnotations\\train" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Marujo2012\\TextosProcessados"
extensaoArquivos = "txt" # extensao dos arquivos de texto que serao processados
Processar(pastaTextos, pastaSaida, extensaoArquivos, 'justTitle')

pastaTextos = "..\\..\\Datasets\\Semeval2010\\test" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Semeval2010\\TextosProcessados"
extensaoArquivos = "final" # extensao dos arquivos de texto que serao processados
Processar(pastaTextos, pastaSaida, extensaoArquivos, 'nenhumaRestricao')
>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
