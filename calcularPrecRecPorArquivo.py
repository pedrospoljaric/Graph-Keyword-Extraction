<<<<<<< HEAD
'''
Calcula os resultados individuais de precision e recall por texto
'''

import os
import glob
import re
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
import math

owd = os.getcwd()

porter_stemmer = PorterStemmer()

#####################################

def RemoverPontuacao(txtIn):
    '''Remove todos os caracteres que nao forem letras (A-Z or a-z).'''
    txtOut = ''
    chAnterior = 32
    for char in txtIn:
        if char.isalpha() or (char.isspace() and chAnterior != 32) or char == "'":
            txtOut += char.lower()
        chAnterior = ord(char)
    return txtOut

def Morphyzar(txtIn):
    palavras = []

    for item in txtIn:
        # print item
        palavra = str(wn.morphy(item.lower()))
        palavras.append(RemoverPontuacao(palavra).upper() if  palavra != 'None' else str(RemoverPontuacao(item).upper()))
    return palavras

def Stemmizar(txtIn):
    palavras = []

    for item in txtIn:
        palavra = str(porter_stemmer.stem(item.lower()))
        palavras.append(palavra.upper() if  palavra != 'None' else str(item.upper()))
    return palavras

def CompararPalavras(palavrasHumano, palavrasPrograma, stem):
    palavrasHumanoSplit = set()
    palavrasProgramaSplit = set()

    for item in palavrasHumano:
        palavras = item.split(' ')
        for palavra in palavras:
            palavrasHumanoSplit.add(palavra.replace('\n', '').upper())

    palavrasHumanoSplit = Morphyzar(list(palavrasHumanoSplit))

    for item in palavrasPrograma:
        palavras = item.split(' ')
        for palavra in palavras:
            palavrasProgramaSplit.add(palavra.replace('\n', '').upper())

    totalPalavras = len(palavrasHumanoSplit)

    palavrasProgramaComparar = list(palavrasProgramaSplit)[0:totalPalavras]
    if stem: palavrasProgramaComparar = Stemmizar(palavrasProgramaComparar)
    # print palavrasProgramaComparar

    vp = len(set(palavrasHumanoSplit) & set(palavrasProgramaComparar))
    fp = len(palavrasProgramaComparar) - vp
    fn = len(palavrasHumanoSplit) - vp

    return vp, fp, fn

def CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, stem):
    os.chdir(pastaPalavrasChave)
    files = glob.glob("*.txt")
    os.chdir(owd)

    for arq in files:
        print arq
        try:
            file = open(pastaPalavrasChave + '\\' + arq, 'r')
            palavrasHumano = re.split(delimiters, file.read().replace('\n\t', ' '))

            pastaMedidas = pastaPalavrasRanqueadas + '\\' + arq.replace('.txt', '')
            os.chdir(pastaMedidas)
            filesMedidas = glob.glob("*.txt")
            os.chdir(owd)

            for arqM in filesMedidas:
                fileM = open(pastaMedidas + '\\' + arqM, 'r')
                palavrasPrograma = fileM.read().split(';')

                vp, fp, fn = CompararPalavras(palavrasHumano, palavrasPrograma, stem)
                precision = float(vp)/(vp+fp)
                recall = float(vp)/(vp+fn)
                f1 = 0 if (precision+recall)==0 else 2*((precision*recall)/(precision+recall))

                arqSaida = pastaSaidaPrecisionRecall + '\\' + arq.replace('.txt', '') + '\\' + arqM

                if os.path.exists(pastaSaidaPrecisionRecall + '\\' + arq.replace('.txt', '')) == False:
                    os.system("mkdir " + pastaSaidaPrecisionRecall + '\\' + arq.replace('.txt', ''))

                file_saida = open(arqSaida, 'w')

                file_saida.write("vp " + str(vp) + "\n")
                file_saida.write("fp " + str(fp) + "\n")
                file_saida.write("fn " + str(fn) + "\n")
                file_saida.write("precision " + str(precision) + "\n")
                file_saida.write("recall " + str(recall) + "\n")
                file_saida.write("f1 " + str(f1))
                file_saida.close()
        except WindowsError:
            print 'WindowsError'


pastaPalavrasChave = '..\\..\\Datasets\\Hulth2003\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Hulth2003\\PrecisionRecallPorArquivo'
delimiters = '; |;\t|;\n'
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Marujo2012\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Marujo2012\\PrecisionRecallPorArquivo'
delimiters = '\n'
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Semeval2010\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Semeval2010\\PrecisionRecallPorArquivo'
delimiters = ','
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, True)

# Apenas palavras chave que aparecem no texto
pastaPalavrasChave = '..\\..\\Datasets\\Hulth2003\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Hulth2003\\PrecisionRecallPorArquivoQueAparecem'
delimiters = ';'
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Marujo2012\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Marujo2012\\PrecisionRecallPorArquivoQueAparecem'
delimiters = ';'
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Semeval2010\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Semeval2010\\PrecisionRecallPorArquivoQueAparecem'
delimiters = ';'
CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, True)

# COMPOSTAS

pastaPalavrasChave = '..\\..\\Datasets\\Hulth2003\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadasCompostas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Hulth2003\\PrecisionRecallPorArquivoCompostas'
delimiters = '; |;\t|;\n'
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Marujo2012\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadasCompostas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Marujo2012\\PrecisionRecallPorArquivoCompostas'
delimiters = '\n'
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Semeval2010\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadasCompostas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Semeval2010\\PrecisionRecallPorArquivoCompostas'
delimiters = ','
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, True)

# Apenas palavras chave que aparecem no texto
pastaPalavrasChave = '..\\..\\Datasets\\Hulth2003\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadasCompostas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Hulth2003\\PrecisionRecallPorArquivoQueAparecemCompostas'
delimiters = ';'
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Marujo2012\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadasCompostas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Marujo2012\\PrecisionRecallPorArquivoQueAparecemCompostas'
delimiters = ';'
# CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Semeval2010\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadasCompostas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Semeval2010\\PrecisionRecallPorArquivoQueAparecemCompostas'
delimiters = ';'
CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, True)
=======
'''
Calcula os resultados individuais de precision e recall por texto
'''

import os
import glob
import re
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
import math

owd = os.getcwd()

porter_stemmer = PorterStemmer()

#####################################

def RemoverPontuacao(txtIn):
    '''Remove todos os caracteres que nao forem letras (A-Z or a-z).'''
    txtOut = ''
    chAnterior = 32
    for char in txtIn:
        if char.isalpha() or (char.isspace() and chAnterior != 32) or char == "'":
            txtOut += char.lower()
        chAnterior = ord(char)
    return txtOut

def Morphyzar(txtIn):
    palavras = []

    for item in txtIn:
        # print item
        palavra = str(wn.morphy(item.lower()))
        palavras.append(RemoverPontuacao(palavra).upper() if  palavra != 'None' else str(RemoverPontuacao(item).upper()))
    return palavras

def Stemmizar(txtIn):
    palavras = []

    for item in txtIn:
        palavra = str(porter_stemmer.stem(item.lower()))
        palavras.append(palavra.upper() if  palavra != 'None' else str(item.upper()))
    return palavras

def CompararPalavras(palavrasHumano, palavrasPrograma, stem):
    palavrasHumanoSplit = set()

    for item in palavrasHumano:
        palavras = item.split(' ')
        for palavra in palavras:
            palavrasHumanoSplit.add(palavra.replace('\n', '').upper())

    palavrasHumanoSplit = Morphyzar(list(palavrasHumanoSplit))

    totalPalavras = len(palavrasHumanoSplit)

    palavrasProgramaComparar = palavrasPrograma[0:totalPalavras]
    if stem: palavrasProgramaComparar = Stemmizar(palavrasProgramaComparar)
    # print palavrasProgramaComparar

    vp = len(set(palavrasHumanoSplit) & set(palavrasProgramaComparar))
    fp = len(palavrasProgramaComparar) - vp
    fn = len(palavrasHumanoSplit) - vp

    return vp, fp, fn

def CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, stem):
    os.chdir(pastaPalavrasChave)
    files = glob.glob("*.txt")
    os.chdir(owd)

    for arq in files:
        print arq
        file = open(pastaPalavrasChave + '\\' + arq, 'r')
        palavrasHumano = re.split(delimiters, file.read().replace('\n\t', ' '))

        pastaMedidas = pastaPalavrasRanqueadas + '\\' + arq.replace('.txt', '')
        os.chdir(pastaMedidas)
        filesMedidas = glob.glob("*.txt")
        os.chdir(owd)

        for arqM in filesMedidas:
            fileM = open(pastaMedidas + '\\' + arqM, 'r')
            palavrasPrograma = fileM.read().split(';')

            vp, fp, fn = CompararPalavras(palavrasHumano, palavrasPrograma, stem)
            precision = float(vp)/(vp+fp)
            recall = float(vp)/(vp+fn)
            f1 = 0 if (precision+recall)==0 else 2*((precision*recall)/(precision+recall))

            arqSaida = pastaSaidaPrecisionRecall + '\\' + arq.replace('.txt', '') + '\\' + arqM

            if os.path.exists(pastaSaidaPrecisionRecall + '\\' + arq.replace('.txt', '')) == False:
                os.system("mkdir " + pastaSaidaPrecisionRecall + '\\' + arq.replace('.txt', ''))

            file_saida = open(arqSaida, 'w')

            file_saida.write("vp " + str(vp) + "\n")
            file_saida.write("fp " + str(fp) + "\n")
            file_saida.write("fn " + str(fn) + "\n")
            file_saida.write("precision " + str(precision) + "\n")
            file_saida.write("recall " + str(recall) + "\n")
            file_saida.write("f1 " + str(f1))
            file_saida.close()


pastaPalavrasChave = '..\\..\\Datasets\\Hulth2003\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Hulth2003\\PrecisionRecallPorArquivo'
delimiters = '; |;\t|;\n'
CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Marujo2012\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Marujo2012\\PrecisionRecallPorArquivo'
delimiters = '\n'
CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Semeval2010\\PalavrasChave'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Semeval2010\\PrecisionRecallPorArquivo'
delimiters = ','
CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, True)

# Apenas palavras chave que aparecem no texto
pastaPalavrasChave = '..\\..\\Datasets\\Hulth2003\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Hulth2003\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Hulth2003\\PrecisionRecallPorArquivoQueAparecem'
delimiters = ';'
CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Marujo2012\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Marujo2012\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Marujo2012\\PrecisionRecallPorArquivoQueAparecem'
delimiters = ';'
CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, False)

pastaPalavrasChave = '..\\..\\Datasets\\Semeval2010\\PalavrasChaveQueAparecem'
pastaPalavrasRanqueadas = '..\\..\\Datasets\\Semeval2010\\PalavrasRanqueadas'
pastaSaidaPrecisionRecall = '..\\..\\Datasets\\Semeval2010\\PrecisionRecallPorArquivoQueAparecem'
delimiters = ';'
CalcularPrecRec(pastaPalavrasChave, pastaPalavrasRanqueadas, pastaSaidaPrecisionRecall, delimiters, True)
>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
