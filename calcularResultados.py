<<<<<<< HEAD
'''
Calcula os resultados de precision e recall medios para os dados de uma pasta com os resultados individuas dos textos
'''

import os
import glob

owd = os.getcwd()

precDicMedidas = {'Degree':0, 'Closeness':0, 'Betweenness':0, 'Clustering_Coef':0,
                  'Page_Rank':0, 'Harmonic':0, 'Katz':0, 'Engenvector':0, 'Coreness':0,
                  'Eccentricity':0, 'Structural_Hole':0, 'Particula Browniana':0}
recallDicMedidas = {'Degree':0, 'Closeness':0, 'Betweenness':0, 'Clustering_Coef':0,
                    'Page_Rank':0, 'Harmonic':0, 'Katz':0, 'Engenvector':0, 'Coreness':0,
                    'Eccentricity':0, 'Structural_Hole':0, 'Particula Browniana':0}
f1DicMedidas = {'Degree':0, 'Closeness':0, 'Betweenness':0, 'Clustering_Coef':0,
                'Page_Rank':0, 'Harmonic':0, 'Katz':0, 'Engenvector':0, 'Coreness':0,
                'Eccentricity':0, 'Structural_Hole':0, 'Particula Browniana':0}


def splitNomeHulth(txtin):
    return "_".join((txtin.split('_'))[1:]).replace('.txt', '')

def splitNomeMarujo(txtIn):
    return "_".join((txtIn.replace('.txt', '').split('-')[1]).split('_')[1:])

def Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados):
    file_resultados = open(pastaDataset + '\\' + arquivoResultados, 'w')

    pastaPrecisionRecall = pastaDataset + pastaPrecRec
    os.chdir(pastaPrecisionRecall)
    folders = glob.glob("*/")
    os.chdir(owd)

    for folder in folders:
        print folder
        os.chdir(pastaPrecisionRecall + '\\' + folder)
        files = glob.glob("*.txt")
        os.chdir(owd)
        for arq in files:
            medida = metodoSplit(arq)
            # print arq.split('_')

            dados = open(pastaPrecisionRecall + '\\' + folder + '\\' + arq).read().split("\n")

            precDicMedidas[medida] += float(dados[3].split(' ')[1])
            recallDicMedidas[medida] += float(dados[4].split(' ')[1])
            f1DicMedidas[medida] += float(dados[5].split(' ')[1])

    total = totalArquivos
    for key in precDicMedidas:
        valorPres = precDicMedidas[key]/float(total)
        valorRecall = recallDicMedidas[key]/float(total)
        valorF1 = f1DicMedidas[key]/float(total)
        file_resultados.write(key + ':' + "".join([' ' for i in range(20-len(key))]) + str(valorPres) + "".join([' ' for i in range(20-len(str(valorPres)))]) + str(valorRecall) + "".join([' ' for i in range(20-len(str(valorRecall)))]) + str(valorF1) + '\n')
    file_resultados.write('\n')

# TODAS AS PALAVRAS SIMPLES ----------------------------------------------------------------------------------------
pastaDataset = '..\\..\\Datasets\\Hulth2003'
metodoSplit = splitNomeHulth
totalArquivos = 500
pastaPrecRec = '\\PrecisionRecallPorArquivo'
arquivoResultados = 'resultados.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Marujo2012'
metodoSplit = splitNomeMarujo
totalArquivos = 450
pastaPrecRec = '\\PrecisionRecallPorArquivo'
arquivoResultados = 'resultados.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Semeval2010'
metodoSplit = splitNomeHulth
totalArquivos = 100
pastaPrecRec = '\\PrecisionRecallPorArquivo'
arquivoResultados = 'resultados.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

# PALAVRAS SIMPLES QUE APARECEM ----------------------------------------------------------------------------------------
pastaDataset = '..\\..\\Datasets\\Hulth2003'
metodoSplit = splitNomeHulth
totalArquivos = 500
pastaPrecRec = '\\PrecisionRecallPorArquivoQueAparecem'
arquivoResultados = 'resultadosQueAparecem.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Marujo2012'
metodoSplit = splitNomeMarujo
totalArquivos = 450
pastaPrecRec = '\\PrecisionRecallPorArquivoQueAparecem'
arquivoResultados = 'resultadosQueAparecem.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Semeval2010'
metodoSplit = splitNomeHulth
totalArquivos = 100
pastaPrecRec = '\\PrecisionRecallPorArquivoQueAparecem'
arquivoResultados = 'resultadosQueAparecem.txt'
Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

# TODAS AS PALAVRAS COMPOSTAS ----------------------------------------------------------------------------------------
pastaDataset = '..\\..\\Datasets\\Hulth2003'
metodoSplit = splitNomeHulth
totalArquivos = 491
pastaPrecRec = '\\PrecisionRecallPorArquivoCompostas'
arquivoResultados = 'resultadosCompostas.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Marujo2012'
metodoSplit = splitNomeMarujo
totalArquivos = 450
pastaPrecRec = '\\PrecisionRecallPorArquivoCompostas'
arquivoResultados = 'resultadosCompostas.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Semeval2010'
metodoSplit = splitNomeHulth
totalArquivos = 96
pastaPrecRec = '\\PrecisionRecallPorArquivoCompostas'
arquivoResultados = 'resultadosCompostas.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

# PALAVRAS COMPOSTAS QUE APARECEM ----------------------------------------------------------------------------------------
pastaDataset = '..\\..\\Datasets\\Hulth2003'
metodoSplit = splitNomeHulth
totalArquivos = 491
pastaPrecRec = '\\PrecisionRecallPorArquivoQueAparecemCompostas'
arquivoResultados = 'resultadosQueAparecemCompostas.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Marujo2012'
metodoSplit = splitNomeMarujo
totalArquivos = 450
pastaPrecRec = '\\PrecisionRecallPorArquivoQueAparecemCompostas'
arquivoResultados = 'resultadosQueAparecemCompostas.txt'
# Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Semeval2010'
metodoSplit = splitNomeHulth
totalArquivos = 96
pastaPrecRec = '\\PrecisionRecallPorArquivoQueAparecemCompostas'
arquivoResultados = 'resultadosQueAparecemCompostas.txt'
Calcular(pastaDataset, metodoSplit, totalArquivos, pastaPrecRec, arquivoResultados)
=======
'''
Calcula os resultados de precision e recall medios para os dados de uma pasta com os resultados individuas dos textos
'''

import os
import glob

owd = os.getcwd()

precDicMedidas = {'Degree':0, 'Closeness':0, 'Betweenness':0, 'Clustering_Coef':0,
                  'Page_Rank':0, 'Harmonic':0, 'Katz':0, 'Engenvector':0, 'Coreness':0,
                  'Eccentricity':0, 'Structural_Hole':0, 'Particula Browniana':0}
recallDicMedidas = {'Degree':0, 'Closeness':0, 'Betweenness':0, 'Clustering_Coef':0,
                    'Page_Rank':0, 'Harmonic':0, 'Katz':0, 'Engenvector':0, 'Coreness':0,
                    'Eccentricity':0, 'Structural_Hole':0, 'Particula Browniana':0}
f1DicMedidas = {'Degree':0, 'Closeness':0, 'Betweenness':0, 'Clustering_Coef':0,
                'Page_Rank':0, 'Harmonic':0, 'Katz':0, 'Engenvector':0, 'Coreness':0,
                'Eccentricity':0, 'Structural_Hole':0, 'Particula Browniana':0}

pastaPrecRec = '\\PrecisionRecallPorArquivoQueAparecem'

def splitNomeHulth(txtin):
    return "_".join((txtin.split('_'))[1:]).replace('.txt', '')

def splitNomeMarujo(txtIn):
    return "_".join((txtIn.replace('.txt', '').split('-')[1]).split('_')[1:])

def Calcular(pastaDataset, metodoSplit, totalArquivos):
    file_resultados = open(pastaDataset + '\\resultadosQueAparecem.txt', 'w')

    pastaPrecisionRecall = pastaDataset + pastaPrecRec
    os.chdir(pastaPrecisionRecall)
    folders = glob.glob("*/")
    os.chdir(owd)

    for folder in folders:
        os.chdir(pastaPrecisionRecall + '\\' + folder)
        files = glob.glob("*.txt")
        os.chdir(owd)
        for arq in files:
            medida = metodoSplit(arq)
            # print arq.split('_')

            dados = open(pastaPrecisionRecall + '\\' + folder + '\\' + arq).read().split("\n")

            precDicMedidas[medida] += float(dados[3].split(' ')[1])
            recallDicMedidas[medida] += float(dados[4].split(' ')[1])
            f1DicMedidas[medida] += float(dados[5].split(' ')[1])

    total = totalArquivos
    for key in precDicMedidas:
        valorPres = precDicMedidas[key]/float(total)
        valorRecall = recallDicMedidas[key]/float(total)
        valorF1 = f1DicMedidas[key]/float(total)
        file_resultados.write(key + ':' + "".join([' ' for i in range(20-len(key))]) + str(valorPres) + "".join([' ' for i in range(20-len(str(valorPres)))]) + str(valorRecall) + "".join([' ' for i in range(20-len(str(valorRecall)))]) + str(valorF1) + '\n')
    file_resultados.write('\n')

pastaDataset = '..\\..\\Datasets\\Hulth2003'
metodoSplit = splitNomeHulth
totalArquivos = 500
Calcular(pastaDataset, metodoSplit, totalArquivos)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Marujo2012'
metodoSplit = splitNomeMarujo
totalArquivos = 450
Calcular(pastaDataset, metodoSplit, totalArquivos)

for item in precDicMedidas:
    precDicMedidas[item] = 0
for item in recallDicMedidas:
    recallDicMedidas[item] = 0
for item in f1DicMedidas:
    f1DicMedidas[item] = 0

pastaDataset = '..\\..\\Datasets\\Semeval2010'
metodoSplit = splitNomeHulth
totalArquivos = 100
Calcular(pastaDataset, metodoSplit, totalArquivos)
>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
