<<<<<<< HEAD
from operator import itemgetter
from igraph import *

global grafo
grafo = Graph(directed=True)
global contadorPalavras
contadorPalavras = {}
global lsWords
lsWords = []

def AdicionarVertice(posicao, palavra):
    """Cria um vertice ou adiciona CODIGO a sua lista de posicoes. Retorna o vertice."""
    vert = grafo.vs.select(word_eq=palavra)
    if not vert: # verifica se no ja existe
        grafo.add_vertices(1)
        grafo.vs[grafo.vcount()-1]["word"] = palavra
        if (posicao != -1):
            grafo.vs[grafo.vcount()-1]["posicoes"] = [posicao]
        else: 
            grafo.vs[grafo.vcount()-1]["posicoes"] = []
        vert = grafo.vs.find(word=palavra)
    else:
        vert = grafo.vs.find(word=palavra)
        if (posicao != -1):
            grafo.vs[vert.index]["posicoes"].append(posicao)
    return vert

def AdicionarPeso(origem, destino, pesos):
    """Adiciona PESOS na aresta origem-destino e cria a aresta caso ela nao exista."""
    codAresta = grafo.get_eid(origem, destino, directed=True, error=False)
    # error=False faz retornar -1 ao inves de uma excecao
    if codAresta == -1:
        if origem != destino and (pesos[0] >= 1 or pesos[1] >= 1 or pesos[2] >= 1):
            grafo.add_edges([(origem, destino)])
            grafo.es[grafo.ecount()-1]["weight"] = pesos
    else:
        grafo.es[codAresta]["weight"] = (pesos[0] + grafo.es[codAresta]["weight"][0],
                                         pesos[1] + grafo.es[codAresta]["weight"][1],
                                         pesos[2] + grafo.es[codAresta]["weight"][2])
        if grafo.es[codAresta]["weight"] == (0, 0, 0):
            grafo.delete_edges(codAresta)

def MesclarVertices(aresta):
    '''Mescla os vertices conectados pela ARESTA.'''
    codOrigem = aresta.source
    codDestino = aresta.target

    palavraOrigem = grafo.vs[codOrigem]["word"]
    palavraDestino = grafo.vs[codDestino]["word"]

    grafo.vs[codOrigem]["posicoes"].extend(grafo.vs[codDestino]["posicoes"])
    # Append das posicoes de target em source
    grafo.vs[codOrigem]["word"] = palavraOrigem + " " + palavraDestino
    contadorPalavras[grafo.vs[codOrigem]["word"]] = contadorPalavras[palavraOrigem]
    #del contadorPalavras[palavraOrigem]
    #del contadorPalavras[palavraDestino]

    arestasDestino = grafo.incident(codDestino, mode="out")

    for codAresta in arestasDestino:
        verticeIncidente = grafo.es[codAresta].target

        codOrigInc = grafo.get_eid(grafo.vs[codOrigem], grafo.vs[verticeIncidente], directed=True, error=False)
        destInc = grafo.es[codAresta]

        # origInc: aresta entre origem e incidente
        # destInc: aresta entre destino e incidente

        if codOrigInc != -1:
            origInc = grafo.es[codOrigInc]

            mediaforte = min(origInc["weight"][1], destInc["weight"][0])
            fracamedia = min(origInc["weight"][2], destInc["weight"][1])

            pesos = (destInc["weight"][0], destInc["weight"][1]-mediaforte, destInc["weight"][2]-fracamedia)

        else:
            pesos = (0, 0, destInc["weight"][2])

        AdicionarPeso(codOrigem, verticeIncidente, pesos)
    
    arestasDestino2 = grafo.incident(codDestino, mode="in")

    for codAresta in arestasDestino2:
        verticeIncidente = grafo.es[codAresta].source

        codOrigInc = grafo.get_eid(grafo.vs[verticeIncidente], grafo.vs[codOrigem], directed=True, error=False)
        destInc = grafo.es[codAresta]

        if codOrigInc != -1:
            origInc = grafo.es[codOrigInc]

            mediaforte = min(origInc["weight"][1], destInc["weight"][0])
            fracamedia = min(origInc["weight"][2], destInc["weight"][1])

            pesos = (destInc["weight"][0], destInc["weight"][1]-mediaforte, destInc["weight"][2]-fracamedia)

        else:
            pesos = (0, 0, destInc["weight"][2])
        
        AdicionarPeso(verticeIncidente, codOrigem, pesos)

    grafo.delete_vertices(codDestino)

    # print 'Merged ' + palavraOrigem + ' and ' + palavraDestino

    # if len(grafo.vs[codOrigem]["word"].split(' ')) > 3:
    #     ExcluirVertice(codOrigem)
    #     grafo.vs["label"] = grafo.vs["word"]
    #     plot(grafo, bbox = (1000, 1000), margin = 50)

    # # printEdges()

def AlterarVertice(vertice, aresta, wordList):
    '''Altera o VERTICE para se tornar VERTICE + ARESTA.target.'''
    codPrincipal = vertice.index
    codAdjacente = aresta.target

    palavraPrincipal = vertice["word"]
    palavraAdjacente = grafo.vs[codAdjacente]["word"]
    vertice["word"] = palavraPrincipal + " " + palavraAdjacente
    # contadorPalavras[palavraAdjacente] -= contadorPalavras[palavraPrincipal]

    posIniciais = []
    for i in vertice["posicoes"]:
        if i-1 not in vertice["posicoes"]:
            posIniciais.append(i)

    for i in posIniciais:
        _, _, _, _, vDir, posD1, vDir2, _ = EncontrarAdjacentes(i, wordList)

        if len(posD1) > 0 and posD1[0] in grafo.vs[vDir]["posicoes"]:
            for p in posD1:
                grafo.vs[vDir]["posicoes"].remove(p)
                vertice["posicoes"].append(p)
            if vDir2 >= 0:
                AdicionarPeso(vDir, vDir2, (-1, 0, 0))
                AdicionarPeso(codPrincipal, vDir2, (1, 0, 0))
                AdicionarPeso(codPrincipal, vDir, (-1, 0, 0))


    contadorPalavras[vertice["word"]] = contadorPalavras[palavraPrincipal]
    # del contadorPalavras[palavraPrincipal]
    # print 'Altered ' + palavraPrincipal + ' into ' + vertice["word"]

    #if len(grafo.incident(eId, mode="all")) > 1:
    # if len(vertice["word"].split(' ')) > 3:
    #     ExcluirVertice(codPrincipal)
    #     grafo.vs["label"] = grafo.vs["word"]
    #     plot(grafo, bbox = (1000, 1000), margin = 50)
    # # printEdges()

def CriarVertice(aresta, wordList):
    '''Cria um novo vertice utilizando a origem e o destino da ARESTA.'''
    codOrigem = aresta.source
    codDestino = aresta.target

    palavraOrigem = grafo.vs[codOrigem]["word"]
    palavraDestino = grafo.vs[codDestino]["word"]

    novaPalavra = palavraOrigem + " " + palavraDestino
    novoVertice = AdicionarVertice(len(lsWords), novaPalavra)

    contadorPalavras[novaPalavra] = 0

    posIniciais = []
    for pos in grafo.vs[codOrigem]["posicoes"]:
        if pos-1 not in grafo.vs[codOrigem]["posicoes"]:
            posIniciais.append(pos)
            contadorPalavras[novaPalavra] += 1

    for pos in posIniciais:
        _, _, vEsq, _, vDir, posD1, vDir2, _ = EncontrarAdjacentes(pos, wordList)
        # print vEsq, vDir, posD1, vDir2

        if vDir >= 0 and grafo.vs[vDir]["word"] == palavraDestino:
            grafo.vs[codOrigem]["posicoes"].remove(pos)
            novoVertice["posicoes"].append(pos)
            if posD1[0] in grafo.vs[vDir]["posicoes"]:
                for p in posD1:
                    grafo.vs[vDir]["posicoes"].remove(p)
                    novoVertice["posicoes"].append(p)
                if vEsq>=0:
                    AdicionarPeso(vEsq, codOrigem, (-1, 0, 0))
                    AdicionarPeso(vEsq, novoVertice.index, (1, 0, 0))
                if vDir2>=0:
                    AdicionarPeso(vDir, vDir2, (-1, 0, 0))
                    AdicionarPeso(novoVertice.index, vDir2, (1, 0, 0))
                # contadorPalavras[palavraOrigem] -= 1
                # contadorPalavras[palavraDestino] -= 1
                # contadorPalavras[novaPalavra] += 1

    # print 'New node ' + novaPalavra

    # if contadorPalavras[palavraOrigem] <= 0:
    #     ExcluirVertice(codOrigem)
    # if contadorPalavras[palavraDestino] <= 0:
    #     ExcluirVertice(codDestino)

    # if len(novaPalavra.split(' ')) > 3:
    #     ExcluirVertice(newId)
    #     grafo.vs["label"] = grafo.vs["word"]
    #     plot(grafo, bbox = (1000, 1000), margin = 50)

def ExcluirVertice(codigo):
    '''Exclui o vertice com determinado CODIGO.'''
    # print 'Deleted ' + grafo.vs[codigo]["word"]
    del contadorPalavras[grafo.vs[codigo]["word"]]
    grafo.delete_vertices(codigo)

def EncontrarAdjacentes(posicao, wordList):
    '''Encontra os vertices adjacentes a um vertice que esta numa POSICAO do texto.'''
    vEsq2 = -1
    vEsq = -1
    vDir = -1
    vDir2 = -1
    posE1 = []
    posE2 = []
    posD1 = []
    posD2 = []

    for j in grafo.vs.indices:
        if posicao in grafo.vs[j]["posicoes"]:
            meio = grafo.vs[j]

    m = posicao-1
    while m in meio["posicoes"]:
        m -= 1

    e1 = m
    for j in grafo.vs.indices:
        if e1 in grafo.vs[j]["posicoes"]:
            esq1 = grafo.vs[j]
            vEsq = j
    if e1 >= 0:
        if vEsq >= 0:
            while e1 in esq1["posicoes"]:
                posE1.append(e1)
                e1 -= 1

    e2 = e1
    for j in grafo.vs.indices:
        if e2 in grafo.vs[j]["posicoes"]:
            esq2 = grafo.vs[j]
            vEsq2 = j
    if e2 >= 0:
        if vEsq2 >= 0:
            while e2 in esq2["posicoes"]:
                posE2.append(e2)
                e2 -= 1

    m = posicao+1
    while m in meio["posicoes"]:
        m += 1

    d1 = m
    for j in grafo.vs.indices:
        if d1 in grafo.vs[j]["posicoes"]:
            dir1 = grafo.vs[j]
            vDir = j
    # print d1, 'in', dir1["posicoes"], 'vDir=', vDir

    # print 'len', len(wordList)

    if d1 < len(wordList):
        if vDir >= 0:
            # print 'entrou'
            while d1 in dir1["posicoes"]:
                posD1.append(d1)
                d1 += 1

    d2 = d1
    for j in grafo.vs.indices:
        if d2 in grafo.vs[j]["posicoes"]:
            dir2 = grafo.vs[j]
            vDir2 = j
    if d2 < len(wordList):
        if vDir2 >= 0:
            while d2 in dir2["posicoes"]:
                posD2.append(d2)
                d2 -= 1

    return vEsq2, posE2, vEsq, posE1, vDir, posD1, vDir2, posD2

def RanquearMedida(nomeMedida, listaValores, ordenar):
    '''Cria uma tupla com os nomes dos vertices e seus valores na medida determinada.
    Ordena de maneira ascendente(ordenar='False') ou descendente(ordenar='True').'''
    aux = sorted(zip(grafo.vs["word"], listaValores), key=itemgetter(1), reverse = ordenar)
    aux.insert(0, ('Node', nomeMedida))
    return aux

def PlotarGrafo():
    '''Plota o grafo e abre em formato de imagem.'''
    visual_style = {}

    lsArgs = sys.argv
    if len(lsArgs) > 2:
        lsArgs = sys.argv
        file_keywords = open(lsArgs[2], 'r')
        lsKeywords = file_keywords.read().split("; ")
        lsKeywordsSplit = []
        for w in lsKeywords:
            lsKeywordsSplit.extend(w.split(" "))
        file_keywords.close()

        lsColors = []
        for i in grafo.vs.indices:
            if grafo.vs[i]["word"].lower() in lsKeywordsSplit:
                lsColors.append("green")
            else:
                lsColors.append("blue")

        visual_style["vertex_color"] = lsColors
    else:
        visual_style["vertex_color"] = "blue"

    visual_style["vertex_label"] = grafo.vs["word"]
    # visual_style["vertex_label_angle"] =
    visual_style["vertex_label_color"] = "#000000"
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_label_size"] = 30
    # visual_style["vertex_order"] =
    visual_style["vertex_shape"] = "circle"
    visual_style["vertex_size"] = 50
    visual_style["edge_color"] = "#000000"
    #visual_style["edge_curved"] =
    # visual_style["edge_arrow_size"] =
    # visual_style["edge_arrow_width"] =
    visual_style["edge_width"] = 2
    visual_style["autocurve"] = True
    visual_style["bbox"] = (2000, 2000)
    visual_style["layout"] = grafo.layout_lgl()
    visual_style["margin"] = 100
    plot(grafo, **visual_style)

def PlotarGrafoTxt():
    lsArestas = []

    for i in grafo.es.indices:
        #if grafo.es[i]["weight"][0] > 0:
        lsArestas.append(str(grafo.vs[grafo.es[i].source]["word"]) + ' ' + str(grafo.vs[grafo.es[i].target]["word"]))

    return lsArestas

def RemoverDirecionamento():
    '''Soma pesos de arestas opostas e elimina uma delas para demover o direcionamento do grafo.'''
    for i in grafo.vs.indices:
        for j in grafo.vs.indices:
            codAresta1 = grafo.get_eid(i, j, directed=True, error=False)
            codAresta2 = grafo.get_eid(j, i, directed=True, error=False)
            if codAresta1 != -1:
                if codAresta2 != -1:
                    if grafo.es[codAresta1]["weight"][0] >= grafo.es[codAresta2]["weight"][0]:
                        p1 = grafo.es[codAresta1]["weight"][0] + grafo.es[codAresta2]["weight"][0]
                        p2 = grafo.es[codAresta1]["weight"][1] + grafo.es[codAresta2]["weight"][1]
                        p3 = grafo.es[codAresta1]["weight"][2] + grafo.es[codAresta2]["weight"][2]
                        grafo.es[codAresta1]["weight"] = (p1, p2, p3)
                        grafo.delete_edges(codAresta2)
                    else:
                        p1 = grafo.es[codAresta2]["weight"][0] + grafo.es[codAresta1]["weight"][0]
                        p2 = grafo.es[codAresta2]["weight"][1] + grafo.es[codAresta1]["weight"][1]
                        p3 = grafo.es[codAresta2]["weight"][2] + grafo.es[codAresta1]["weight"][2]
                        grafo.es[codAresta2]["weight"] = (p1, p2, p3)
                        grafo.delete_edges(codAresta1)

def HarmonicCentrality():
    '''Calcula a medida Harmonic Centrality dos vertices do grafo.'''
    distancias = grafo.shortest_paths_dijkstra(source=None, target=None, weights=None, mode='OUT')
    harmonic = []

    for i in grafo.vs.indices:
        harmonic.append(0)
        for j in grafo.vs.indices:
            if i != j:
                harmonic[i] += 1/float(distancias[i][j])

    return harmonic

def CrossCliqueCentrality():
    '''Calcula a medida Cross-clique Centrality dos vertices do grafo.'''
    xclique = [0] * len(grafo.vs.indices)
    allCliques = grafo.cliques(min=3, max=0)

    for c in allCliques:
        for v in c:
            xclique[v] += 1

    return xclique

def KatzCentrality(attenuationFactor, eigenScore):
    '''Calcula a medida Katz Centrality dos vertices do grafo.'''
    katz = [0] * len(grafo.vs.indices)

    m = grafo.get_adjacency(attribute=None, default=0, eids=False)

    for i in grafo.vs.indices:
        for j in grafo.vs.indices:
            katz[i] += int(m[i][j]) * (float(eigenScore[j]) + 1)
        katz[i] *= attenuationFactor
    
    return katz

def PercolationCentrality(infectedNodes):
    perc = [0] * len(grafo.vs.indices)

    for i in grafo.vs.indices:
        for j in grafo.vs.indices:
            if j != i:
                for k in grafo.vs.indices:
                    if k != j and k != i:
                        shPaths = grafo.get_all_shortest_paths(j, to=k, mode='ALL')
                        caminhosPassamPorI = 0
                        for caminho in shPaths:
                            if i in caminho:
                                caminhosPassamPorI += 1

                        aux1 = caminhosPassamPorI/len(shPaths)
                        aux2 = (1 if j in infectedNodes else 0)/(len(infectedNodes) - (1 if i in infectedNodes else 0))
                        perc[i] += aux1*aux2
        perc[i] *= 1/(len(grafo.vs.indices) - 2)
        
    return perc

def PrintArestas():
    print ' '
    for i in grafo.es.indices: 
        print str(grafo.vs[grafo.es[i].source]["word"]) + ' - ' + str(grafo.vs[grafo.es[i].target]["word"]) + ' - ' + str(grafo.es[i]["weight"])

def CalcularMedidas():
    w = []
    for i in grafo.es.indices:
        w.append(grafo.es[i]["weight"][0]
                + 0.5 * grafo.es[i]["weight"][1]
                + 0.25 * grafo.es[i]["weight"][2])

    # Calculo das medidas de centralidade____________________________#

    indice = grafo.vs.indices
    deg = grafo.degree(vertices=None, mode='ALL', loops=False)
    closeness = grafo.closeness(vertices=None, mode='OUT', cutoff=None, weights=w, normalized=False)
    betweenness = grafo.betweenness(vertices=None, directed=False, cutoff=None,
                                    weights=w, nobigint=True)
    clustering = grafo.transitivity_local_undirected(vertices=None, mode="zero", weights=w)
    pageRank = grafo.personalized_pagerank(vertices=None, directed=False, damping=0.85,
                                        reset=None, reset_vertices=None, weights=w,
                                        implementation="prpack")
    harmonic = HarmonicCentrality()
    eigenVector = grafo.eigenvector_centrality(directed=False, scale=True,
                                            weights=w, return_eigenvalue=False)
    katz = KatzCentrality(0.5, eigenVector)
    # crossClique = CrossCliqueCentrality()
    coreness = grafo.coreness(mode='ALL')
    eccentricity = grafo.eccentricity(vertices=None, mode='ALL')
    structuralHole = grafo.constraint(vertices=None, weights=w)

    matrizAdj = grafo.get_adjacency(attribute=None, default=0, eids=False)
    matrizAdj = matrizAdj._get_data()
    partBrowniana = ParticulaBrowniana(matrizAdj)

    ranks = []
    ranks.append(RanquearMedida('Indice', indice, True))
    ranks.append(RanquearMedida('Degree', deg, True))
    ranks.append(RanquearMedida('Closeness', closeness, True))
    ranks.append(RanquearMedida('Betweenness', betweenness, True))
    ranks.append(RanquearMedida('Clustering_Coef', clustering, False))
    ranks.append(RanquearMedida('Page_Rank', pageRank, True))
    ranks.append(RanquearMedida('Harmonic', harmonic, True))
    ranks.append(RanquearMedida('Katz', katz, True))
    ranks.append(RanquearMedida('Engenvector', eigenVector, True))
    # ranks.append(RanquearMedida('Cross-clique', crossClique))
    ranks.append(RanquearMedida('Coreness', coreness, True))
    ranks.append(RanquearMedida('Eccentricity', eccentricity, False))
    ranks.append(RanquearMedida('Structural_Hole', structuralHole, False))
    ranks.append(RanquearMedida('Particula Browniana', partBrowniana, True))

    return ranks

def invert(matriz):
    n = len(matriz)
    x = [[float(0) for i in range(n)] for j in range(n)]
    b = [[float(0) for i in range(n)] for j in range(n)]
    index = [0 for i in range(n)]
    for i in range(n):
        b[i][i] = float(1)

    # Transform the matrix into an upper triangle
    gaussian(matriz, index);

    # Update the matrix b[i][j] with the ratios stored
    for i in range(n-1):
        for j in range(i+1, n):
            for k in range(n):
                b[index[j]][k] -= matriz[index[j]][i]*b[index[i]][k]

    # Perform backward substitutions
    for i in range(n):
        x[n-1][i] = b[index[n-1]][i]/matriz[index[n-1]][n-1]
        for j in range(n-2, -1, -1):
            x[j][i] = b[index[j]][i]
            for k in range(j+1, n):
                x[j][i] -= matriz[index[j]][k]*x[k][i]
            x[j][i] /= matriz[index[j]][j]

    return x;

# Method to carry out the partial-pivoting Gaussian
# elimination.  Here index[] stores pivoting order.

def gaussian(matriz, index):
    n = len(index)
    c = [float(0) for x in range(n)]

    # Initialize the index
    for i in range(n):
        index[i] = i

    # Find the rescaling factors, one from each row
    for i in range(n):
        c1 = float(0)
        for j in range(n):
            c0 = abs(matriz[i][j])
            if (c0 > c1):
                c1 = c0
        c[i] = c1

    # Search the pivoting element from each column
    k = 0
    for j in range(n-1):
        pi1 = float(0)
        for i in range(j, n):
            pi0 = float(abs(matriz[index[i]][j]))
            pi0 /= c[index[i]]
            if (pi0 > pi1):
                pi1 = pi0
                k = i

        # Interchange rows according to the pivoting order

        itmp = index[j]
        index[j] = index[k]
        index[k] = itmp

        for i in range(j+1, n):
            pj = float(matriz[index[i]][j]/matriz[index[j]][j])
            matriz[index[i]][j] = pj

            for l in range(j+1, n):
                matriz[index[i]][l] -= pj*matriz[index[j]][l]

def ParticulaBrowniana(matrizInicial): # Matriz inicial = matriz de adjacencia
    numLinha = len(matrizInicial)
    numColuna = len(matrizInicial[0])

    matrizTransferencia = [[0 for x in range(numColuna)] for y in range(numLinha)] #n^2
    matrizTransferencia = calculaMatrizDeTransferencia(matrizInicial)
    
    matrizDistancia = [[0 for x in range(numColuna)] for y in range(numLinha)] #n^2
    matrizDistancia = calculaMatrizDeDistancia(matrizTransferencia)
    
    matrizDissimilaridade = [[0 for x in range(numColuna)] for y in range(numLinha)] #n^2
    matrizDissimilaridade = calculaMatrizDeDissimilaridade(matrizDistancia)

    # print 'Matriz inicial'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizInicial[k][l],
    #     # print

    # print 'Matriz transferencia'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizTransferencia[k][l],
    #     # print

    # print 'Matriz distancia'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizDistancia[k][l],
    #     # print

    # print 'Matriz dissimilaridade'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizDissimilaridade[k][l],
    #     # print
    
    return encontraOutlier(matrizDissimilaridade)
    
def calculaMatrizDeTransferencia(matrizInicial): # Matriz de transferencia: divide todos os valores da linha pela soma da linha
    numLinha = len(matrizInicial)
    numColuna = len(matrizInicial[0])
    matrizTransferencia = [[0 for x in range(numColuna)] for y in range(numLinha)]

    for i in range(numLinha):
        somaLinha = 0
        for j in range(numColuna):
            if(matrizInicial[i][j] == 1):
                somaLinha += 1
        for j in range(numColuna):
            if(matrizInicial[i][j] == 1):
                if(somaLinha != 0):
                    matrizTransferencia[i][j] = 1/float(somaLinha)

    # print 'Matriz Transferencia\n'
    # for k in range(numLinha):
    #     print '\n'
    #     for l in range(numColuna):
    #         print str(matrizTransferencia[k][l]), ' '
    
    return matrizTransferencia

def calculaMatrizDeDistancia(matrizTransferencia):
    numLinha = len(matrizTransferencia)
    numColuna = len(matrizTransferencia[0])

    matrizDistancia = [[float(0) for x in range(numColuna)] for y in range(numLinha)]
    matrizIdentidade = [[float(0) for x in range(numColuna)] for y in range(numLinha)]

    vetorUnitario = [float(1) for x in range(numColuna)]
    vetorDistancia = [float(0) for x in range(numColuna)]
    
    for i in range(numLinha):
        matrizIdentidade[i][i] = float(1)

    cont = 0;
    matrizSubtracao = [[float(0) for x in range(numColuna)] for y in range(numLinha)]
    copiaMatrizTransferencia = [[float(0) for x in range(numColuna)] for y in range(numLinha)]

    while(cont < numColuna):
        # atribui matriz transferencia para copiaMatrizTransferencia
        for i in range(numLinha):
            for j in range(numColuna):
                copiaMatrizTransferencia[i][j] = matrizTransferencia[i][j] #n^3
        
        # atribui 0 a j-esima coluna
        for i in range(numLinha):
            copiaMatrizTransferencia[i][cont] = float(0)
         
        for i in range(numLinha):
            for j in range(numColuna):
                matrizSubtracao[i][j] = matrizIdentidade[i][j] - copiaMatrizTransferencia[i][j] #n^3

        ################

        # print 'Matriz subtracao'
        # for k in range(numLinha):
        #     print ' '
        #     for l in range(numColuna):
        #         print matrizSubtracao[k][l],

        inversaMatrizSubtracao = invert(matrizSubtracao);

        # print 'Matriz inversa subtracao'
        # for k in range(numLinha):
        #     print ' '
        #     for l in range(numColuna):
        #         print inversaMatrizSubtracao[k][l],
    
        vetorDistancia = multiplicaMatrizes(vetorUnitario, inversaMatrizSubtracao)
        
        for i in range(numColuna):
            matrizDistancia[cont][i] = vetorDistancia[i]
        cont += 1
    
    return matrizDistancia

def multiplicaMatrizes(m2, m1):
    numLinha = len(m1)
    numColuna = len(m1[0])
    matriz = [0 for x in range(numColuna)]
    aux = 0;

    for i in range(numLinha):
        aux = 0
        for k in range(numColuna):
            aux += ((m2[k]) * (m1[k][i]))
        matriz[i] = aux

    return matriz

def calculaMatrizDeDissimilaridade(matrizDistancia):
    numLinha = len(matrizDistancia)
    numColuna = len(matrizDistancia[0])
    matrizDissimilaridade = [[float(0) for x in range(numColuna)] for y in range(numLinha)]
    somatorio = 0
    subtracao = 0
    vetorDissimilaridade = [0 for x in range(numLinha)]
    
    for i in range(numLinha):
        for j in range(numColuna):
            somatorio = 0
            for k in range(numLinha):
                if (k != i) and (k != j): #n^3
                    subtracao = matrizDistancia[i][k] - matrizDistancia[j][k]
                    if subtracao < 1:
                        somatorio += -subtracao
                    else:
                        somatorio += subtracao
            vetorDissimilaridade[j] = somatorio/(numLinha-2)

        for j in range(numColuna):
            matrizDissimilaridade[i][j] = vetorDissimilaridade[j]
    
    # print 'Matriz Dissimilaridade'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizDissimilaridade[k][l], ' '
    
    return matrizDissimilaridade

def encontraOutlier(matrizDissimilaridade):
    numLinha = len(matrizDissimilaridade)
    numColuna = len(matrizDissimilaridade[0])
    somaLinha = 0
    vetorOutlier = [float(0) for x in range(numLinha)]
    # vetorVertices = [0 for x in range(numLinha)]
    
    for i in range(numLinha):
        somaLinha = 0
        for j in range(numColuna):
            somaLinha += matrizDissimilaridade[i][j]
        vetorOutlier[i] = somaLinha
        # vetorVertices[i] = i + 1

    return vetorOutlier

    # for i in range(numLinha):
    #     for j in range(numLinha):
    #         if vetorOutlier[i] < vetorOutlier[j]:
    #             aux = vetorOutlier[j]
    #             vetorOutlier[j] = vetorOutlier[i]
    #             vetorOutlier[i] = aux

    #             aux2 = vetorVertices[j]
    #             vetorVertices[j] = vetorVertices[i]
    #             vetorVertices[i] = aux2
    
    # print 'Valores outlier'
    # for i in range(numLinha):
    #     print vetorOutlier[i]

    # print 'Vertices outlier'
    # for i in range(numLinha):
    #     print vetorVertices[i]

def encontraSimilaridade(matriz):
    lineNumber = len(matriz)
    collNumber = len(matriz[0])

    matrizDistanciaEuclidiana = [[float(0) for x in range(collNumber)] for y in range(lineNumber)]
    somaLinha = 0

    for k in range(lineNumber):
        for l in range(lineNumber):
            for m in range(collNumber-1):
                somaLinha += math.pow((matriz[k][m] - matriz[l][m]), 2) #n^3

            matrizDistanciaEuclidiana[k][l] = math.sqrt(somaLinha)
            somaLinha = 0

    # print 'Matriz Distancia euclidiana'
    # for k in range(lineNumber):
    #     print ' '
    #     for l in range(collNumber):
    #         print matrizDistanciaEuclidiana[k][l], ' '

    matrizOrdenada = [[0 for x in range(lineNumber)] for y in range(lineNumber)]
    menorValor = float(100000)
    cont = 1
    posicao = 0

    for n in range(lineNumber):
        while cont < lineNumber:
            for o in range(lineNumber):
                if (matrizDistanciaEuclidiana[n][o] < menorValor) and (matrizDistanciaEuclidiana[n][o] > 0.0): #n^3
                    menorValor = matrizDistanciaEuclidiana[n][o]
                    posicao = o

            matrizOrdenada[n][posicao] = cont
            matrizDistanciaEuclidiana[n][posicao] = 0
            cont += 1
            menorValor = 100

        cont = 1

    # print 'Matriz Distancia euclidiana ordenada'
    # for k in range(lineNumber):
    #     print ' '
    #     for l in range(collNumber):
    #         print matrizOrdenada[k][l], ' '
=======
from operator import itemgetter
from igraph import *

global grafo
grafo = Graph(directed=True)
global contadorPalavras
contadorPalavras = {}
global lsWords
lsWords = []

def AdicionarVertice(posicao, palavra):
    """Cria um vertice ou adiciona CODIGO a sua lista de posicoes. Retorna o vertice."""
    vert = grafo.vs.select(word_eq=palavra)
    if not vert: # verifica se no ja existe
        grafo.add_vertices(1)
        grafo.vs[grafo.vcount()-1]["word"] = palavra
        if (posicao != -1):
            grafo.vs[grafo.vcount()-1]["posicoes"] = [posicao]
        else: 
            grafo.vs[grafo.vcount()-1]["posicoes"] = []
        vert = grafo.vs.find(word=palavra)
    else:
        vert = grafo.vs.find(word=palavra)
        if (posicao != -1):
            grafo.vs[vert.index]["posicoes"].append(posicao)
    return vert

def AdicionarPeso(origem, destino, pesos):
    """Adiciona PESOS na aresta origem-destino e cria a aresta caso ela nao exista."""
    codAresta = grafo.get_eid(origem, destino, directed=True, error=False)
    # error=False faz retornar -1 ao inves de uma excecao
    if codAresta == -1:
        if origem != destino and (pesos[0] >= 1 or pesos[1] >= 1 or pesos[2] >= 1):
            grafo.add_edges([(origem, destino)])
            grafo.es[grafo.ecount()-1]["weight"] = pesos
    else:
        grafo.es[codAresta]["weight"] = (pesos[0] + grafo.es[codAresta]["weight"][0],
                                         pesos[1] + grafo.es[codAresta]["weight"][1],
                                         pesos[2] + grafo.es[codAresta]["weight"][2])
        if grafo.es[codAresta]["weight"] == (0, 0, 0):
            grafo.delete_edges(codAresta)

def MesclarVertices(aresta):
    '''Mescla os vertices conectados pela ARESTA.'''
    codOrigem = aresta.source
    codDestino = aresta.target

    palavraOrigem = grafo.vs[codOrigem]["word"]
    palavraDestino = grafo.vs[codDestino]["word"]

    grafo.vs[codOrigem]["posicoes"].extend(grafo.vs[codDestino]["posicoes"])
    # Append das posicoes de target em source
    grafo.vs[codOrigem]["word"] = palavraOrigem + " " + palavraDestino
    contadorPalavras[grafo.vs[codOrigem]["word"]] = contadorPalavras[palavraOrigem]
    #del contadorPalavras[palavraOrigem]
    #del contadorPalavras[palavraDestino]

    arestasDestino = grafo.incident(codDestino, mode="out")

    for codAresta in arestasDestino:
        verticeIncidente = grafo.es[codAresta].target

        codOrigInc = grafo.get_eid(grafo.vs[codOrigem], grafo.vs[verticeIncidente], directed=True, error=False)
        destInc = grafo.es[codAresta]

        # origInc: aresta entre origem e incidente
        # destInc: aresta entre destino e incidente

        if codOrigInc != -1:
            origInc = grafo.es[codOrigInc]

            mediaforte = min(origInc["weight"][1], destInc["weight"][0])
            fracamedia = min(origInc["weight"][2], destInc["weight"][1])

            pesos = (destInc["weight"][0], destInc["weight"][1]-mediaforte, destInc["weight"][2]-fracamedia)

        else:
            pesos = (0, 0, destInc["weight"][2])

        AdicionarPeso(codOrigem, verticeIncidente, pesos)
    
    arestasDestino2 = grafo.incident(codDestino, mode="in")

    for codAresta in arestasDestino2:
        verticeIncidente = grafo.es[codAresta].source

        codOrigInc = grafo.get_eid(grafo.vs[verticeIncidente], grafo.vs[codOrigem], directed=True, error=False)
        destInc = grafo.es[codAresta]

        if codOrigInc != -1:
            origInc = grafo.es[codOrigInc]

            mediaforte = min(origInc["weight"][1], destInc["weight"][0])
            fracamedia = min(origInc["weight"][2], destInc["weight"][1])

            pesos = (destInc["weight"][0], destInc["weight"][1]-mediaforte, destInc["weight"][2]-fracamedia)

        else:
            pesos = (0, 0, destInc["weight"][2])
        
        AdicionarPeso(verticeIncidente, codOrigem, pesos)

    grafo.delete_vertices(codDestino)

    # print 'Merged ' + palavraOrigem + ' and ' + palavraDestino

    # if len(grafo.vs[codOrigem]["word"].split(' ')) > 3:
    #     ExcluirVertice(codOrigem)
    #     grafo.vs["label"] = grafo.vs["word"]
    #     plot(grafo, bbox = (1000, 1000), margin = 50)

    # # printEdges()

def AlterarVertice(vertice, aresta, wordList):
    '''Altera o VERTICE para se tornar VERTICE + ARESTA.target.'''
    codPrincipal = vertice.index
    codAdjacente = aresta.target

    palavraPrincipal = vertice["word"]
    palavraAdjacente = grafo.vs[codAdjacente]["word"]
    vertice["word"] = palavraPrincipal + " " + palavraAdjacente
    # contadorPalavras[palavraAdjacente] -= contadorPalavras[palavraPrincipal]

    posIniciais = []
    for i in vertice["posicoes"]:
        if i-1 not in vertice["posicoes"]:
            posIniciais.append(i)

    for i in posIniciais:
        _, _, _, _, vDir, posD1, vDir2, _ = EncontrarAdjacentes(i, wordList)

        if len(posD1) > 0 and posD1[0] in grafo.vs[vDir]["posicoes"]:
            for p in posD1:
                grafo.vs[vDir]["posicoes"].remove(p)
                vertice["posicoes"].append(p)
            if vDir2 >= 0:
                AdicionarPeso(vDir, vDir2, (-1, 0, 0))
                AdicionarPeso(codPrincipal, vDir2, (1, 0, 0))
                AdicionarPeso(codPrincipal, vDir, (-1, 0, 0))


    contadorPalavras[vertice["word"]] = contadorPalavras[palavraPrincipal]
    # del contadorPalavras[palavraPrincipal]
    # print 'Altered ' + palavraPrincipal + ' into ' + vertice["word"]

    #if len(grafo.incident(eId, mode="all")) > 1:
    # if len(vertice["word"].split(' ')) > 3:
    #     ExcluirVertice(codPrincipal)
    #     grafo.vs["label"] = grafo.vs["word"]
    #     plot(grafo, bbox = (1000, 1000), margin = 50)
    # # printEdges()

def CriarVertice(aresta, wordList):
    '''Cria um novo vertice utilizando a origem e o destino da ARESTA.'''
    codOrigem = aresta.source
    codDestino = aresta.target

    palavraOrigem = grafo.vs[codOrigem]["word"]
    palavraDestino = grafo.vs[codDestino]["word"]

    novaPalavra = palavraOrigem + " " + palavraDestino
    novoVertice = AdicionarVertice(len(lsWords), novaPalavra)

    contadorPalavras[novaPalavra] = 0

    posIniciais = []
    for pos in grafo.vs[codOrigem]["posicoes"]:
        if pos-1 not in grafo.vs[codOrigem]["posicoes"]:
            posIniciais.append(pos)
            contadorPalavras[novaPalavra] += 1

    for pos in posIniciais:
        _, _, vEsq, _, vDir, posD1, vDir2, _ = EncontrarAdjacentes(pos, wordList)
        # print vEsq, vDir, posD1, vDir2

        if vDir >= 0 and grafo.vs[vDir]["word"] == palavraDestino:
            grafo.vs[codOrigem]["posicoes"].remove(pos)
            novoVertice["posicoes"].append(pos)
            if posD1[0] in grafo.vs[vDir]["posicoes"]:
                for p in posD1:
                    grafo.vs[vDir]["posicoes"].remove(p)
                    novoVertice["posicoes"].append(p)
                if vEsq>=0:
                    AdicionarPeso(vEsq, codOrigem, (-1, 0, 0))
                    AdicionarPeso(vEsq, novoVertice.index, (1, 0, 0))
                if vDir2>=0:
                    AdicionarPeso(vDir, vDir2, (-1, 0, 0))
                    AdicionarPeso(novoVertice.index, vDir2, (1, 0, 0))
                # contadorPalavras[palavraOrigem] -= 1
                # contadorPalavras[palavraDestino] -= 1
                # contadorPalavras[novaPalavra] += 1

    # print 'New node ' + novaPalavra

    # if contadorPalavras[palavraOrigem] <= 0:
    #     ExcluirVertice(codOrigem)
    # if contadorPalavras[palavraDestino] <= 0:
    #     ExcluirVertice(codDestino)

    # if len(novaPalavra.split(' ')) > 3:
    #     ExcluirVertice(newId)
    #     grafo.vs["label"] = grafo.vs["word"]
    #     plot(grafo, bbox = (1000, 1000), margin = 50)

def ExcluirVertice(codigo):
    '''Exclui o vertice com determinado CODIGO.'''
    # print 'Deleted ' + grafo.vs[codigo]["word"]
    del contadorPalavras[grafo.vs[codigo]["word"]]
    grafo.delete_vertices(codigo)

def EncontrarAdjacentes(posicao, wordList):
    '''Encontra os vertices adjacentes a um vertice que esta numa POSICAO do texto.'''
    vEsq2 = -1
    vEsq = -1
    vDir = -1
    vDir2 = -1
    posE1 = []
    posE2 = []
    posD1 = []
    posD2 = []

    for j in grafo.vs.indices:
        if posicao in grafo.vs[j]["posicoes"]:
            meio = grafo.vs[j]

    m = posicao-1
    while m in meio["posicoes"]:
        m -= 1

    e1 = m
    for j in grafo.vs.indices:
        if e1 in grafo.vs[j]["posicoes"]:
            esq1 = grafo.vs[j]
            vEsq = j
    if e1 >= 0:
        if vEsq >= 0:
            while e1 in esq1["posicoes"]:
                posE1.append(e1)
                e1 -= 1

    e2 = e1
    for j in grafo.vs.indices:
        if e2 in grafo.vs[j]["posicoes"]:
            esq2 = grafo.vs[j]
            vEsq2 = j
    if e2 >= 0:
        if vEsq2 >= 0:
            while e2 in esq2["posicoes"]:
                posE2.append(e2)
                e2 -= 1

    m = posicao+1
    while m in meio["posicoes"]:
        m += 1

    d1 = m
    for j in grafo.vs.indices:
        if d1 in grafo.vs[j]["posicoes"]:
            dir1 = grafo.vs[j]
            vDir = j
    # print d1, 'in', dir1["posicoes"], 'vDir=', vDir

    # print 'len', len(wordList)

    if d1 < len(wordList):
        if vDir >= 0:
            # print 'entrou'
            while d1 in dir1["posicoes"]:
                posD1.append(d1)
                d1 += 1

    d2 = d1
    for j in grafo.vs.indices:
        if d2 in grafo.vs[j]["posicoes"]:
            dir2 = grafo.vs[j]
            vDir2 = j
    if d2 < len(wordList):
        if vDir2 >= 0:
            while d2 in dir2["posicoes"]:
                posD2.append(d2)
                d2 -= 1

    return vEsq2, posE2, vEsq, posE1, vDir, posD1, vDir2, posD2

def RanquearMedida(nomeMedida, listaValores, ordenar):
    '''Cria uma tupla com os nomes dos vertices e seus valores na medida determinada.
    Ordena de maneira ascendente(ordenar='False') ou descendente(ordenar='True').'''
    aux = sorted(zip(grafo.vs["word"], listaValores), key=itemgetter(1), reverse = ordenar)
    aux.insert(0, ('Node', nomeMedida))
    return aux

def PlotarGrafo():
    '''Plota o grafo e abre em formato de imagem.'''
    visual_style = {}

    lsArgs = sys.argv
    if len(lsArgs) > 2:
        lsArgs = sys.argv
        file_keywords = open(lsArgs[2], 'r')
        lsKeywords = file_keywords.read().split("; ")
        lsKeywordsSplit = []
        for w in lsKeywords:
            lsKeywordsSplit.extend(w.split(" "))
        file_keywords.close()

        lsColors = []
        for i in grafo.vs.indices:
            if grafo.vs[i]["word"].lower() in lsKeywordsSplit:
                lsColors.append("green")
            else:
                lsColors.append("blue")

        visual_style["vertex_color"] = lsColors
    else:
        visual_style["vertex_color"] = "blue"

    visual_style["vertex_label"] = grafo.vs["word"]
    # visual_style["vertex_label_angle"] =
    visual_style["vertex_label_color"] = "#000000"
    visual_style["vertex_label_dist"] = 0
    visual_style["vertex_label_size"] = 30
    # visual_style["vertex_order"] =
    visual_style["vertex_shape"] = "circle"
    visual_style["vertex_size"] = 50
    visual_style["edge_color"] = "#000000"
    #visual_style["edge_curved"] =
    # visual_style["edge_arrow_size"] =
    # visual_style["edge_arrow_width"] =
    visual_style["edge_width"] = 2
    visual_style["autocurve"] = True
    visual_style["bbox"] = (2000, 2000)
    visual_style["layout"] = grafo.layout_lgl()
    visual_style["margin"] = 100
    plot(grafo, **visual_style)

def PlotarGrafoTxt():
    lsArestas = []

    for i in grafo.es.indices:
        #if grafo.es[i]["weight"][0] > 0:
        lsArestas.append(str(grafo.vs[grafo.es[i].source]["word"]) + ' ' + str(grafo.vs[grafo.es[i].target]["word"]))

    return lsArestas

def RemoverDirecionamento():
    '''Soma pesos de arestas opostas e elimina uma delas para demover o direcionamento do grafo.'''
    for i in grafo.vs.indices:
        for j in grafo.vs.indices:
            codAresta1 = grafo.get_eid(i, j, directed=True, error=False)
            codAresta2 = grafo.get_eid(j, i, directed=True, error=False)
            if codAresta1 != -1:
                if codAresta2 != -1:
                    if grafo.es[codAresta1]["weight"][0] >= grafo.es[codAresta2]["weight"][0]:
                        p1 = grafo.es[codAresta1]["weight"][0] + grafo.es[codAresta2]["weight"][0]
                        p2 = grafo.es[codAresta1]["weight"][1] + grafo.es[codAresta2]["weight"][1]
                        p3 = grafo.es[codAresta1]["weight"][2] + grafo.es[codAresta2]["weight"][2]
                        grafo.es[codAresta1]["weight"] = (p1, p2, p3)
                        grafo.delete_edges(codAresta2)
                    else:
                        p1 = grafo.es[codAresta2]["weight"][0] + grafo.es[codAresta1]["weight"][0]
                        p2 = grafo.es[codAresta2]["weight"][1] + grafo.es[codAresta1]["weight"][1]
                        p3 = grafo.es[codAresta2]["weight"][2] + grafo.es[codAresta1]["weight"][2]
                        grafo.es[codAresta2]["weight"] = (p1, p2, p3)
                        grafo.delete_edges(codAresta1)

def HarmonicCentrality():
    '''Calcula a medida Harmonic Centrality dos vertices do grafo.'''
    distancias = grafo.shortest_paths_dijkstra(source=None, target=None, weights=None, mode='OUT')
    harmonic = []

    for i in grafo.vs.indices:
        harmonic.append(0)
        for j in grafo.vs.indices:
            if i != j:
                harmonic[i] += 1/float(distancias[i][j])

    return harmonic

def CrossCliqueCentrality():
    '''Calcula a medida Cross-clique Centrality dos vertices do grafo.'''
    xclique = [0] * len(grafo.vs.indices)
    allCliques = grafo.cliques(min=3, max=0)

    for c in allCliques:
        for v in c:
            xclique[v] += 1

    return xclique

def KatzCentrality(attenuationFactor, eigenScore):
    '''Calcula a medida Katz Centrality dos vertices do grafo.'''
    katz = [0] * len(grafo.vs.indices)

    m = grafo.get_adjacency(attribute=None, default=0, eids=False)

    for i in grafo.vs.indices:
        for j in grafo.vs.indices:
            katz[i] += int(m[i][j]) * (float(eigenScore[j]) + 1)
        katz[i] *= attenuationFactor
    
    return katz

def PercolationCentrality(infectedNodes):
    perc = [0] * len(grafo.vs.indices)

    for i in grafo.vs.indices:
        for j in grafo.vs.indices:
            if j != i:
                for k in grafo.vs.indices:
                    if k != j and k != i:
                        shPaths = grafo.get_all_shortest_paths(j, to=k, mode='ALL')
                        caminhosPassamPorI = 0
                        for caminho in shPaths:
                            if i in caminho:
                                caminhosPassamPorI += 1

                        aux1 = caminhosPassamPorI/len(shPaths)
                        aux2 = (1 if j in infectedNodes else 0)/(len(infectedNodes) - (1 if i in infectedNodes else 0))
                        perc[i] += aux1*aux2
        perc[i] *= 1/(len(grafo.vs.indices) - 2)
        
    return perc

def PrintArestas():
    print ' '
    for i in grafo.es.indices: 
        print str(grafo.vs[grafo.es[i].source]["word"]) + ' - ' + str(grafo.vs[grafo.es[i].target]["word"]) + ' - ' + str(grafo.es[i]["weight"])

def CalcularMedidas():
    w = []
    for i in grafo.es.indices:
        w.append(grafo.es[i]["weight"][0]
                + 0.5 * grafo.es[i]["weight"][1]
                + 0.25 * grafo.es[i]["weight"][2])

    # Calculo das medidas de centralidade____________________________#

    indice = grafo.vs.indices
    deg = grafo.degree(vertices=None, mode='ALL', loops=False)
    closeness = grafo.closeness(vertices=None, mode='OUT', cutoff=None, weights=w, normalized=False)
    betweenness = grafo.betweenness(vertices=None, directed=False, cutoff=None,
                                    weights=w, nobigint=True)
    clustering = grafo.transitivity_local_undirected(vertices=None, mode="zero", weights=w)
    pageRank = grafo.personalized_pagerank(vertices=None, directed=False, damping=0.85,
                                        reset=None, reset_vertices=None, weights=w,
                                        implementation="prpack")
    harmonic = HarmonicCentrality()
    eigenVector = grafo.eigenvector_centrality(directed=False, scale=True,
                                            weights=w, return_eigenvalue=False)
    katz = KatzCentrality(0.5, eigenVector)
    # crossClique = CrossCliqueCentrality()
    coreness = grafo.coreness(mode='ALL')
    eccentricity = grafo.eccentricity(vertices=None, mode='ALL')
    structuralHole = grafo.constraint(vertices=None, weights=w)

    matrizAdj = grafo.get_adjacency(attribute=None, default=0, eids=False)
    matrizAdj = matrizAdj._get_data()
    partBrowniana = ParticulaBrowniana(matrizAdj)

    ranks = []
    ranks.append(RanquearMedida('Indice', indice, True))
    ranks.append(RanquearMedida('Degree', deg, True))
    ranks.append(RanquearMedida('Closeness', closeness, True))
    ranks.append(RanquearMedida('Betweenness', betweenness, True))
    ranks.append(RanquearMedida('Clustering_Coef', clustering, False))
    ranks.append(RanquearMedida('Page_Rank', pageRank, True))
    ranks.append(RanquearMedida('Harmonic', harmonic, True))
    ranks.append(RanquearMedida('Katz', katz, True))
    ranks.append(RanquearMedida('Engenvector', eigenVector, True))
    # ranks.append(RanquearMedida('Cross-clique', crossClique))
    ranks.append(RanquearMedida('Coreness', coreness, True))
    ranks.append(RanquearMedida('Eccentricity', eccentricity, False))
    ranks.append(RanquearMedida('Structural_Hole', structuralHole, False))
    ranks.append(RanquearMedida('Particula Browniana', partBrowniana, True))

    return ranks

def invert(matriz):
    n = len(matriz)
    x = [[float(0) for i in range(n)] for j in range(n)]
    b = [[float(0) for i in range(n)] for j in range(n)]
    index = [0 for i in range(n)]
    for i in range(n):
        b[i][i] = float(1)

    # Transform the matrix into an upper triangle
    gaussian(matriz, index);

    # Update the matrix b[i][j] with the ratios stored
    for i in range(n-1):
        for j in range(i+1, n):
            for k in range(n):
                b[index[j]][k] -= matriz[index[j]][i]*b[index[i]][k]

    # Perform backward substitutions
    for i in range(n):
        x[n-1][i] = b[index[n-1]][i]/matriz[index[n-1]][n-1]
        for j in range(n-2, -1, -1):
            x[j][i] = b[index[j]][i]
            for k in range(j+1, n):
                x[j][i] -= matriz[index[j]][k]*x[k][i]
            x[j][i] /= matriz[index[j]][j]

    return x;

# Method to carry out the partial-pivoting Gaussian
# elimination.  Here index[] stores pivoting order.

def gaussian(matriz, index):
    n = len(index)
    c = [float(0) for x in range(n)]

    # Initialize the index
    for i in range(n):
        index[i] = i

    # Find the rescaling factors, one from each row
    for i in range(n):
        c1 = float(0)
        for j in range(n):
            c0 = abs(matriz[i][j])
            if (c0 > c1):
                c1 = c0
        c[i] = c1

    # Search the pivoting element from each column
    k = 0
    for j in range(n-1):
        pi1 = float(0)
        for i in range(j, n):
            pi0 = float(abs(matriz[index[i]][j]))
            pi0 /= c[index[i]]
            if (pi0 > pi1):
                pi1 = pi0
                k = i

        # Interchange rows according to the pivoting order

        itmp = index[j]
        index[j] = index[k]
        index[k] = itmp

        for i in range(j+1, n):
            pj = float(matriz[index[i]][j]/matriz[index[j]][j])
            matriz[index[i]][j] = pj

            for l in range(j+1, n):
                matriz[index[i]][l] -= pj*matriz[index[j]][l]

def ParticulaBrowniana(matrizInicial): # Matriz inicial = matriz de adjacencia
    numLinha = len(matrizInicial)
    numColuna = len(matrizInicial[0])

    matrizTransferencia = [[0 for x in range(numColuna)] for y in range(numLinha)]
    matrizTransferencia = calculaMatrizDeTransferencia(matrizInicial)
    
    matrizDistancia = [[0 for x in range(numColuna)] for y in range(numLinha)]
    matrizDistancia = calculaMatrizDeDistancia(matrizTransferencia)
    
    matrizDissimilaridade = [[0 for x in range(numColuna)] for y in range(numLinha)]
    matrizDissimilaridade = calculaMatrizDeDissimilaridade(matrizDistancia)

    # print 'Matriz inicial'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizInicial[k][l],
    #     # print

    # print 'Matriz transferencia'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizTransferencia[k][l],
    #     # print

    # print 'Matriz distancia'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizDistancia[k][l],
    #     # print

    # print 'Matriz dissimilaridade'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizDissimilaridade[k][l],
    #     # print
    
    return encontraOutlier(matrizDissimilaridade)
    
def calculaMatrizDeTransferencia(matrizInicial): # Matriz de transferencia: divide todos os valores da linha pela soma da linha
    numLinha = len(matrizInicial)
    numColuna = len(matrizInicial[0])
    matrizTransferencia = [[0 for x in range(numColuna)] for y in range(numLinha)]

    for i in range(numLinha):
        somaLinha = 0
        for j in range(numColuna):
            if(matrizInicial[i][j] == 1):
                somaLinha += 1
        for j in range(numColuna):
            if(matrizInicial[i][j] == 1):
                if(somaLinha != 0):
                    matrizTransferencia[i][j] = 1/float(somaLinha)

    # print 'Matriz Transferencia\n'
    # for k in range(numLinha):
    #     print '\n'
    #     for l in range(numColuna):
    #         print str(matrizTransferencia[k][l]), ' '
    
    return matrizTransferencia

def calculaMatrizDeDistancia(matrizTransferencia):
    numLinha = len(matrizTransferencia)
    numColuna = len(matrizTransferencia[0])

    matrizDistancia = [[float(0) for x in range(numColuna)] for y in range(numLinha)]
    matrizIdentidade = [[float(0) for x in range(numColuna)] for y in range(numLinha)]

    vetorUnitario = [float(1) for x in range(numColuna)]
    vetorDistancia = [float(0) for x in range(numColuna)]
    
    for i in range(numLinha):
        matrizIdentidade[i][i] = float(1)

    cont = 0;
    matrizSubtracao = [[float(0) for x in range(numColuna)] for y in range(numLinha)]
    copiaMatrizTransferencia = [[float(0) for x in range(numColuna)] for y in range(numLinha)]

    while(cont < numColuna):
        # atribui matriz transferencia para copiaMatrizTransferencia
        for i in range(numLinha):
            for j in range(numColuna):
                copiaMatrizTransferencia[i][j] = matrizTransferencia[i][j]
        
        # atribui 0 a j-esima coluna
        for i in range(numLinha):
            copiaMatrizTransferencia[i][cont] = float(0)
         
        for i in range(numLinha):
            for j in range(numColuna):
                matrizSubtracao[i][j] = matrizIdentidade[i][j] - copiaMatrizTransferencia[i][j]

        ################

        # print 'Matriz subtracao'
        # for k in range(numLinha):
        #     print ' '
        #     for l in range(numColuna):
        #         print matrizSubtracao[k][l],

        inversaMatrizSubtracao = invert(matrizSubtracao);

        # print 'Matriz inversa subtracao'
        # for k in range(numLinha):
        #     print ' '
        #     for l in range(numColuna):
        #         print inversaMatrizSubtracao[k][l],
    
        vetorDistancia = multiplicaMatrizes(vetorUnitario, inversaMatrizSubtracao)
        
        for i in range(numColuna):
            matrizDistancia[cont][i] = vetorDistancia[i]
        cont += 1
    
    return matrizDistancia

def multiplicaMatrizes(m2, m1):
    numLinha = len(m1)
    numColuna = len(m1[0])
    matriz = [0 for x in range(numColuna)]
    aux = 0;

    for i in range(numLinha):
        aux = 0
        for k in range(numColuna):
            aux += ((m2[k]) * (m1[k][i]))
        matriz[i] = aux

    return matriz

def calculaMatrizDeDissimilaridade(matrizDistancia):
    numLinha = len(matrizDistancia)
    numColuna = len(matrizDistancia[0])
    matrizDissimilaridade = [[float(0) for x in range(numColuna)] for y in range(numLinha)]
    somatorio = 0
    subtracao = 0
    vetorDissimilaridade = [0 for x in range(numLinha)]
    
    for i in range(numLinha):
        for j in range(numColuna):
            somatorio = 0
            for k in range(numLinha):
                if (k != i) and (k != j):
                    subtracao = matrizDistancia[i][k] - matrizDistancia[j][k]
                    if subtracao < 1:
                        somatorio += -subtracao
                    else:
                        somatorio += subtracao
            vetorDissimilaridade[j] = somatorio/(numLinha-2)

        for j in range(numColuna):
            matrizDissimilaridade[i][j] = vetorDissimilaridade[j]
    
    # print 'Matriz Dissimilaridade'
    # for k in range(numLinha):
    #     print ' '
    #     for l in range(numColuna):
    #         print matrizDissimilaridade[k][l], ' '
    
    return matrizDissimilaridade

def encontraOutlier(matrizDissimilaridade):
    numLinha = len(matrizDissimilaridade)
    numColuna = len(matrizDissimilaridade[0])
    somaLinha = 0
    vetorOutlier = [float(0) for x in range(numLinha)]
    # vetorVertices = [0 for x in range(numLinha)]
    
    for i in range(numLinha):
        somaLinha = 0
        for j in range(numColuna):
            somaLinha += matrizDissimilaridade[i][j]
        vetorOutlier[i] = somaLinha
        # vetorVertices[i] = i + 1

    return vetorOutlier

    # for i in range(numLinha):
    #     for j in range(numLinha):
    #         if vetorOutlier[i] < vetorOutlier[j]:
    #             aux = vetorOutlier[j]
    #             vetorOutlier[j] = vetorOutlier[i]
    #             vetorOutlier[i] = aux

    #             aux2 = vetorVertices[j]
    #             vetorVertices[j] = vetorVertices[i]
    #             vetorVertices[i] = aux2
    
    # print 'Valores outlier'
    # for i in range(numLinha):
    #     print vetorOutlier[i]

    # print 'Vertices outlier'
    # for i in range(numLinha):
    #     print vetorVertices[i]

def encontraSimilaridade(matriz):
        lineNumber = len(matriz)
        collNumber = len(matriz[0])

        matrizDistanciaEuclidiana = [[float(0) for x in range(collNumber)] for y in range(lineNumber)]
        somaLinha = 0

        for k in range(lineNumber):
            for l in range(lineNumber):
                for m in range(collNumber-1):
                    somaLinha += math.pow((matriz[k][m] - matriz[l][m]), 2)

                matrizDistanciaEuclidiana[k][l] = math.sqrt(somaLinha)
                somaLinha = 0

        # print 'Matriz Distancia euclidiana'
        # for k in range(lineNumber):
        #     print ' '
        #     for l in range(collNumber):
        #         print matrizDistanciaEuclidiana[k][l], ' '

        matrizOrdenada = [[0 for x in range(lineNumber)] for y in range(lineNumber)]
        menorValor = float(100000)
        cont = 1
        posicao = 0

        for n in range(lineNumber):
            while cont < lineNumber:
                for o in range(lineNumber):
                    if (matrizDistanciaEuclidiana[n][o] < menorValor) and (matrizDistanciaEuclidiana[n][o] > 0.0):
                        menorValor = matrizDistanciaEuclidiana[n][o]
                        posicao = o

                matrizOrdenada[n][posicao] = cont
                matrizDistanciaEuclidiana[n][posicao] = 0
                cont += 1
                menorValor = 100

            cont = 1

        # print 'Matriz Distancia euclidiana ordenada'
        # for k in range(lineNumber):
        #     print ' '
        #     for l in range(collNumber):
        #         print matrizOrdenada[k][l], ' '
>>>>>>> 239fb183b9df7d5373544d809d37b10d266b6dfd
