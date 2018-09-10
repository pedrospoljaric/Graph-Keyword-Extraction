<<<<<<< HEAD
'''
Transforma textos em grafos, manipula, calculas medidas de centralidade e ranqueia as palavras
Como usar:
1) python keyWordGen.py arquivoTexto
    - Gera um arquivo .csv na mesma pasta do arquivoTexto com as medidas de centralidade ranqueadas
2) python keyWordGen.py arquivoTexto pastaSaida
    - Gera arquivos .txt para cada medida e coloca dentro de uma pasta dentro da pastaSaida
'''

from igraph import *
import numpy as np
from operator import itemgetter
import sys
import cairo
import os

from funcoes import *

# pylint: disable-msg=C0103
# pylint: disable-msg=E1137
# pylint: disable-msg=E1136
# pylint: disable-msg=W0621

grafo.vs["word"] = []
grafo.vs["posicoes"] = []
grafo.es["weight"] = []

lsArgs = sys.argv
file_txt = open(lsArgs[1], 'r')
lsWords = file_txt.read().split(" ")
file_txt.close()

# Insercao de nos e arestas no grafo

def InsercaoNosArestas():
    for i in range(len(lsWords)):

        if lsWords[i] not in contadorPalavras:
            contadorPalavras[lsWords[i]] = 1
        else: contadorPalavras[lsWords[i]] += 1

        AdicionarVertice(i, lsWords[i])

        if i > 0:
            v1 = grafo.vs.find(word=lsWords[i-1])
            v2 = grafo.vs.find(word=lsWords[i])
            AdicionarPeso(v1, v2, (1, 0, 0))

        # Pesos de grau 1 e 2
        if i > 1:
            v1 = grafo.vs.find(word=lsWords[i-2])
            v2 = grafo.vs.find(word=lsWords[i])
            AdicionarPeso(v1, v2, (0, 1, 0))

        if i > 2:
            v1 = grafo.vs.find(word=lsWords[i-3])
            v2 = grafo.vs.find(word=lsWords[i])
            AdicionarPeso(v1, v2, (0, 0, 1))
InsercaoNosArestas()

# PlotarGrafo()
# PrintArestas()

# ranks = CalcularMedidas()

# filename_out = (lsArgs[1])[0:-4]
# filename_out = filename_out + '_ranking1' + '.csv'
# file_out = open(filename_out, 'w')

# for v in range(len(grafo.vs.indices)+1):
#     for r in ranks:
#         file_out.write(str(r[v][0]) + ';' + str(r[v][1]).replace('.', ',') + ';')
#     file_out.write('\n')

# file_out.close()

#______________________________________________________________#

# Escrever arestas em arquivo

# aux = lsArgs[1].split('\\')
# filename_out = os.getcwd() + '\\Datasets\\Nguyen2007\\Grafos\\'
# nomeArq = (aux[-1].split('.'))[0]
# filename_out += nomeArq + 'arestas' + '.txt'
# file_out = open(filename_out, 'w')

# lsArestas = PlotarGrafoTxt()
# for a in lsArestas:
#     file_out.write(a + '\n')

# file_out.close()

#______________________________________________________________#

#Transformacao do grafo

def TransformacaoGrafo():
    vId = 0
    while vId < len(grafo.vs.indices):
        selection = grafo.incident(vId, mode="out") # all: vId = source/target
        for edgeId in selection:
            if edgeId in grafo.es.indices and vId in grafo.vs.indices:

                vertice = grafo.vs[vId]
                aresta = grafo.es[edgeId]
                v1 = grafo.vs[aresta.source]
                v2 = grafo.vs[aresta.target]
                freq1 = aresta["weight"][0]/float(contadorPalavras[v1["word"]])
                freq2 = aresta["weight"][0]/float(contadorPalavras[v2["word"]])

                if freq1 >= 1 and freq2 >= 1:
                    MesclarVertices(aresta)

        vId += 1

    ranks = CalcularMedidas()

    # filename_out = (lsArgs[1])[0:-4]
    # filename_out = filename_out + '_ranking2' + '.csv'
    # file_out = open(filename_out, 'w')

    # for v in range(len(grafo.vs.indices)+1):
    #     for r in ranks:
    #         file_out.write(str(r[v][0]) + ';' + str(r[v][1]).replace('.', ',') + ';')
    #     file_out.write('\n')

    # file_out.close()

    vId = 0
    while vId < len(grafo.vs.indices):
        selection = grafo.incident(vId, mode="out") # all: vId = source/target
        for edgeId in selection:
            if edgeId in grafo.es.indices and vId in grafo.vs.indices:

                vertice = grafo.vs[vId]
                aresta = grafo.es[edgeId]
                v1 = grafo.vs[aresta.source]
                v2 = grafo.vs[aresta.target]
                # print contadorPalavras
                freq1 = aresta["weight"][0]/float(contadorPalavras[v1["word"]])
                freq2 = aresta["weight"][0]/float(contadorPalavras[v2["word"]])

                if freq1 < 1 or freq2 < 1:
                    if freq1 >= 1:
                        AlterarVertice(vertice, aresta, lsWords)

                    elif freq1 >= 0.7 and freq2 >= 0.7:
                        CriarVertice(aresta, lsWords)

        vId += 1
TransformacaoGrafo()

# PlotarGrafo()
# PrintArestas()

#______________________________________________________________#

RemoverDirecionamento()
grafo.to_undirected(mode='each')

# Calculo dos pesos das arestas__________________________________#

ranks = CalcularMedidas()

if len(lsArgs) == 2:

    filename_out = (lsArgs[1])[0:-4]
    filename_out = filename_out + '_ranking3' + '.csv'
    file_out = open(filename_out, 'w')

    for v in range(len(grafo.vs.indices)+1):
        for r in ranks:
            file_out.write(str(r[v][0]) + ';' + str(r[v][1]).replace('.', ',') + ';')
        file_out.write('\n')

    file_out.close()

if len(lsArgs) == 3:

    pastaSaida = lsArgs[2] + '\\' + (lsArgs[1].split('\\')[-1])[0:-4]
    if os.path.exists(pastaSaida) == False:
        os.system("mkdir " + pastaSaida)

    filename_out = (pastaSaida + '\\' + lsArgs[1].split('\\')[-1])[0:-4]

    for item in range(1, len(ranks)):
        file_out = open(filename_out+'_'+ranks[item][0][1]+'.txt', 'w')

        for i in range(1, len(ranks[item])-1):
            file_out.write(ranks[item][i][0] + ';')
        file_out.write(ranks[item][len(ranks[item])-1][0])

=======
'''
Transforma textos em grafos, manipula, calculas medidas de centralidade e ranqueia as palavras
Como usar:
1) python keyWordGen.py arquivoTexto
    - Gera um arquivo .csv na mesma pasta do arquivoTexto com as medidas de centralidade ranqueadas
2) python keyWordGen.py arquivoTexto pastaSaida
    - Gera arquivos .txt para cada medida e coloca dentro de uma pasta dentro da pastaSaida
'''

from igraph import *
import numpy as np
from operator import itemgetter
import sys
import cairo
import os

from funcoes import *

# pylint: disable-msg=C0103
# pylint: disable-msg=E1137
# pylint: disable-msg=E1136
# pylint: disable-msg=W0621

grafo.vs["word"] = []
grafo.vs["posicoes"] = []
grafo.es["weight"] = []

lsArgs = sys.argv
file_txt = open(lsArgs[1], 'r')
lsWords = file_txt.read().split(" ")
file_txt.close()

# Insercao de nos e arestas no grafo

def InsercaoNosArestas():
    for i in range(len(lsWords)):

        if lsWords[i] not in contadorPalavras:
            contadorPalavras[lsWords[i]] = 1
        else: contadorPalavras[lsWords[i]] += 1

        AdicionarVertice(i, lsWords[i])

        if i > 0:
            v1 = grafo.vs.find(word=lsWords[i-1])
            v2 = grafo.vs.find(word=lsWords[i])
            AdicionarPeso(v1, v2, (1, 0, 0))

        # Pesos de grau 1 e 2
        if i > 1:
            v1 = grafo.vs.find(word=lsWords[i-2])
            v2 = grafo.vs.find(word=lsWords[i])
            AdicionarPeso(v1, v2, (0, 1, 0))

        if i > 2:
            v1 = grafo.vs.find(word=lsWords[i-3])
            v2 = grafo.vs.find(word=lsWords[i])
            AdicionarPeso(v1, v2, (0, 0, 1))
InsercaoNosArestas()

# PlotarGrafo()
# PrintArestas()

# ranks = CalcularMedidas()

# filename_out = (lsArgs[1])[0:-4]
# filename_out = filename_out + '_ranking1' + '.csv'
# file_out = open(filename_out, 'w')

# for v in range(len(grafo.vs.indices)+1):
#     for r in ranks:
#         file_out.write(str(r[v][0]) + ';' + str(r[v][1]).replace('.', ',') + ';')
#     file_out.write('\n')

# file_out.close()

#______________________________________________________________#

# Escrever arestas em arquivo

# aux = lsArgs[1].split('\\')
# filename_out = os.getcwd() + '\\Datasets\\Nguyen2007\\Grafos\\'
# nomeArq = (aux[-1].split('.'))[0]
# filename_out += nomeArq + 'arestas' + '.txt'
# file_out = open(filename_out, 'w')

# lsArestas = PlotarGrafoTxt()
# for a in lsArestas:
#     file_out.write(a + '\n')

# file_out.close()

#______________________________________________________________#

#Transformacao do grafo

def TransformacaoGrafo():
    vId = 0
    while vId < len(grafo.vs.indices):
        selection = grafo.incident(vId, mode="out") # all: vId = source/target
        for edgeId in selection:
            if edgeId in grafo.es.indices and vId in grafo.vs.indices:

                vertice = grafo.vs[vId]
                aresta = grafo.es[edgeId]
                v1 = grafo.vs[aresta.source]
                v2 = grafo.vs[aresta.target]
                freq1 = aresta["weight"][0]/float(contadorPalavras[v1["word"]])
                freq2 = aresta["weight"][0]/float(contadorPalavras[v2["word"]])

                if freq1 >= 1 and freq2 >= 1:
                    MesclarVertices(aresta)

        vId += 1

    ranks = CalcularMedidas()

    # filename_out = (lsArgs[1])[0:-4]
    # filename_out = filename_out + '_ranking2' + '.csv'
    # file_out = open(filename_out, 'w')

    # for v in range(len(grafo.vs.indices)+1):
    #     for r in ranks:
    #         file_out.write(str(r[v][0]) + ';' + str(r[v][1]).replace('.', ',') + ';')
    #     file_out.write('\n')

    # file_out.close()

    vId = 0
    while vId < len(grafo.vs.indices):
        selection = grafo.incident(vId, mode="out") # all: vId = source/target
        for edgeId in selection:
            if edgeId in grafo.es.indices and vId in grafo.vs.indices:

                vertice = grafo.vs[vId]
                aresta = grafo.es[edgeId]
                v1 = grafo.vs[aresta.source]
                v2 = grafo.vs[aresta.target]
                # print contadorPalavras
                freq1 = aresta["weight"][0]/float(contadorPalavras[v1["word"]])
                freq2 = aresta["weight"][0]/float(contadorPalavras[v2["word"]])

                if freq1 < 1 or freq2 < 1:
                    if freq1 >= 1:
                        AlterarVertice(vertice, aresta, lsWords)

                    elif freq1 >= 0.7 and freq2 >= 0.7:
                        CriarVertice(aresta, lsWords)

        vId += 1
# TransformacaoGrafo()

# PlotarGrafo()
# PrintArestas()

#______________________________________________________________#

RemoverDirecionamento()
grafo.to_undirected(mode='each')

# Calculo dos pesos das arestas__________________________________#

ranks = CalcularMedidas()

if len(lsArgs) == 2:

    filename_out = (lsArgs[1])[0:-4]
    filename_out = filename_out + '_ranking3' + '.csv'
    file_out = open(filename_out, 'w')

    for v in range(len(grafo.vs.indices)+1):
        for r in ranks:
            file_out.write(str(r[v][0]) + ';' + str(r[v][1]).replace('.', ',') + ';')
        file_out.write('\n')

    file_out.close()

if len(lsArgs) == 3:

    pastaSaida = lsArgs[2] + '\\' + (lsArgs[1].split('\\')[-1])[0:-4]
    if os.path.exists(pastaSaida) == False:
        os.system("mkdir " + pastaSaida)

    filename_out = (pastaSaida + '\\' + lsArgs[1].split('\\')[-1])[0:-4]

    for item in range(1, len(ranks)):
        file_out = open(filename_out+'_'+ranks[item][0][1]+'.txt', 'w')

        for i in range(1, len(ranks[item])-1):
            file_out.write(ranks[item][i][0] + ';')
        file_out.write(ranks[item][len(ranks[item])-1][0])

>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
        file_out.close()