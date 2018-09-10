<<<<<<< HEAD
'''
Copia os arquivos de palavras chave para uma pasta para padronizar o processamento
'''

import os
import glob

owd = os.getcwd() # ~/Programas

def Organizar(pastaTextos, pastaSaida, extensaoArquivos, notInFile):
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
					# os.system('python procDeTexto.py ' + pastaEntrada + file + ' ' + pastaSaida + ' ..\\..\\stopwords_ingles.txt ..\\..\\stopwords_adicionais.txt')
					os.system('copy ' + pastaEntrada + file + ' ' + pastaSaida + '\\' + file.replace(extensaoArquivos, 'txt'))
	else:
		os.chdir(pastaTextos)
		files = glob.glob("*."+extensaoArquivos)
		os.chdir(owd)
		for file in files:
			if notInFile not in file:
				print file
				pastaEntrada = pastaTextos + '\\'
				# print 'copy ' + pastaEntrada + file + ' ' + pastaSaida + '\\' + file.replace(extensaoArquivos, 'txt')
				os.system('copy ' + pastaEntrada + file + ' ' + pastaSaida + '\\' + file.replace(extensaoArquivos, 'txt'))
				# os.system('python procDeTexto.py ' + pastaEntrada + file + ' ' + pastaSaida + ' ..\\..\\stopwords_ingles.txt ..\\..\\stopwords_adicionais.txt')

pastaTextos = "..\\..\\Datasets\\Hulth2003\\Validation" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Hulth2003\\PalavrasChave"
extensaoArquivos = "uncontr" # extensao dos arquivos de texto que serao processados
Organizar(pastaTextos, pastaSaida, extensaoArquivos, 'nenhumaRestricao')

pastaTextos = "..\\..\\Datasets\\Marujo2012\\CorpusAndCrowdsourcingAnnotations\\train" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Marujo2012\\PalavrasChave"
extensaoArquivos = "key" # extensao dos arquivos de texto que serao processados
Organizar(pastaTextos, pastaSaida, extensaoArquivos, 'nenhumaRestricao')

pastaTextos = "..\\..\\Datasets\\Semeval2010\\test_answer" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Semeval2010\\PalavrasChave"

def OrganizarSemeval():
	filePalavrasChave = open(pastaTextos + '\\' + 'test.combined.stem.final', 'r')
	lines = filePalavrasChave.read().split('\n')
	for line in lines:
		nomeTexto = line.split(' : ')[0]
		print nomeTexto
		print line
		palavrasChave = line.split(' : ')[1]
		# print nomeTexto, palavrasChave

		fileSaida = open(pastaSaida + '\\' + nomeTexto + '.txt', 'w')
		fileSaida.write(palavrasChave)
		fileSaida.close()
=======
'''
Copia os arquivos de palavras chave para uma pasta para padronizar o processamento
'''

import os
import glob

owd = os.getcwd() # ~/Programas

def Organizar(pastaTextos, pastaSaida, extensaoArquivos, notInFile):
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
					# os.system('python procDeTexto.py ' + pastaEntrada + file + ' ' + pastaSaida + ' ..\\..\\stopwords_ingles.txt ..\\..\\stopwords_adicionais.txt')
					os.system('copy ' + pastaEntrada + file + ' ' + pastaSaida + '\\' + file.replace(extensaoArquivos, 'txt'))
	else:
		os.chdir(pastaTextos)
		files = glob.glob("*."+extensaoArquivos)
		os.chdir(owd)
		for file in files:
			if notInFile not in file:
				print file
				pastaEntrada = pastaTextos + '\\'
				# print 'copy ' + pastaEntrada + file + ' ' + pastaSaida + '\\' + file.replace(extensaoArquivos, 'txt')
				os.system('copy ' + pastaEntrada + file + ' ' + pastaSaida + '\\' + file.replace(extensaoArquivos, 'txt'))
				# os.system('python procDeTexto.py ' + pastaEntrada + file + ' ' + pastaSaida + ' ..\\..\\stopwords_ingles.txt ..\\..\\stopwords_adicionais.txt')

pastaTextos = "..\\..\\Datasets\\Hulth2003\\Validation" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Hulth2003\\PalavrasChave"
extensaoArquivos = "uncontr" # extensao dos arquivos de texto que serao processados
Organizar(pastaTextos, pastaSaida, extensaoArquivos, 'nenhumaRestricao')

pastaTextos = "..\\..\\Datasets\\Marujo2012\\CorpusAndCrowdsourcingAnnotations\\train" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Marujo2012\\PalavrasChave"
extensaoArquivos = "key" # extensao dos arquivos de texto que serao processados
Organizar(pastaTextos, pastaSaida, extensaoArquivos, 'nenhumaRestricao')

pastaTextos = "..\\..\\Datasets\\Semeval2010\\test_answer" # local dos arquivos ou pastas com arquivos
pastaSaida = "..\\..\\Datasets\\Semeval2010\\PalavrasChave"

def OrganizarSemeval():
	filePalavrasChave = open(pastaTextos + '\\' + 'test.combined.stem.final', 'r')
	lines = filePalavrasChave.read().split('\n')
	for line in lines:
		nomeTexto = line.split(' : ')[0]
		print nomeTexto
		print line
		palavrasChave = line.split(' : ')[1]
		# print nomeTexto, palavrasChave

		fileSaida = open(pastaSaida + '\\' + nomeTexto + '.txt', 'w')
		fileSaida.write(palavrasChave)
		fileSaida.close()
>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
OrganizarSemeval()