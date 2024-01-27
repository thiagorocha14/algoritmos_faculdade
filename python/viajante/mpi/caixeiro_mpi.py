# Importação das bibliotecas
import random
import sys
import math
#Importando MPI
from mpi4py import MPI

comm = MPI.COMM_WORLD

#Definindo o rank e o size
rank = comm.rank
size = comm.size
status = MPI.Status()

# CONSTANTES DEFINIDAS NA EXECUÇÃO
QTD_CIDADES   = int(sys.argv[1])
DIST_MAX      = int(sys.argv[2])
DIST_MIN      = int(sys.argv[3])
IMPRESSAO     = sys.argv[4]

qtd_processos = size
if qtd_processos > QTD_CIDADES:
    qtd_processos = QTD_CIDADES

# Cálculo de Custos
def calcular_custos(lista, matriz_custo):
    custo = 0
    for pos_dest in range(1,len(lista)):
        if lista[pos_dest] > lista[pos_dest-1]:
            custo += matriz_custo[lista[pos_dest-1]][lista[pos_dest]]
        else:
            custo += matriz_custo[lista[pos_dest]][lista[pos_dest-1]]
    return custo

def permutacoes(lista):
    if len(lista) == 0:
        return[[]]
    combinacoes = []
    for i in range(len(lista)):
        valor_atual = lista[i]
        lista_restante = lista[:i]+lista[i+1:]
        lista_permutacoes = permutacoes(lista_restante)
        for permutacao in lista_permutacoes:
            combinacoes.append([valor_atual]+permutacao)
    return combinacoes

def gerar_listas_e_enviar_pros_processos(lista_cidades, matriz_custo):
    matriz_informacoes = [x for x in range(1, qtd_processos)]
    for x in lista_cidades:
        process = x
        cidade_faltante = x

        lista_temp = lista_cidades.copy()
        lista_temp.remove(x)

        informacoes = (lista_temp, cidade_faltante)
        if process >= qtd_processos:
            process = process % qtd_processos + 1
            matriz_informacoes[process-1].append(informacoes)
        else:
            matriz_informacoes[process-1] = [informacoes]
    for i in range(0, qtd_processos-1):
        comm.send((matriz_custo, matriz_informacoes[i]), dest=i+1)



def gerar_combinacao_inicial(qtd_cidades):
    combinacao = [x for x in range(1, qtd_cidades)]
    return combinacao

# Função geradora do custo (Matriz de Custo)
def gera_matriz_custo(qtd_cidades, dist_max, dist_min):
    random.seed(12)
    matriz_custo = []
    for cid_origem in range(qtd_cidades):
        matriz_custo.append([])
        for cid_destino in range(qtd_cidades):
            if cid_origem < cid_destino:
                matriz_custo[cid_origem].append(random.randint(dist_max, dist_min))
            else:
                matriz_custo[cid_origem].append(0)

    print('** CIDADE **')
    for cid_origem in range(QTD_CIDADES):
        print(matriz_custo[cid_origem])
    return matriz_custo

def receber_combinacoes():
    melhores_combinacao_final = []
    for i in range(1, qtd_processos):
        melhores_combinacoes  = comm.recv(source=i)
        for combinacao in melhores_combinacoes:
            melhor_combinacao = combinacao
            if melhores_combinacao_final == []:
                melhores_combinacao_final = [melhor_combinacao]
            elif melhor_combinacao[1] < melhores_combinacao_final[0][1]:
                melhores_combinacao_final = [melhor_combinacao]
            elif melhor_combinacao[1] == melhores_combinacao_final[0][1]:
                melhores_combinacao_final.append(melhor_combinacao)
    return melhores_combinacao_final

def melhores_combinacoes(informacoes):
    melhores_combinacoes = []

    for info in informacoes:
        lista_cidades = info[0]
        cidade_faltante = info[1]
        combinacoes = permutacoes(lista_cidades)
        for combinacao in combinacoes:
            combinacao.insert(0, cidade_faltante)
            combinacao.insert(0,0)
            combinacao.append(0)
            custo = calcular_custos(combinacao, matriz_custo)
            if melhores_combinacoes == []:
                melhores_combinacoes = [[combinacao, custo]]
            elif custo < melhores_combinacoes[0][1]:
                melhores_combinacoes = [[combinacao, custo]]
            elif custo == melhores_combinacoes[0][1]:
                melhores_combinacoes.append([combinacao, custo])

    return melhores_combinacoes


if rank == 0:
    matriz_custo = gera_matriz_custo(QTD_CIDADES, DIST_MAX, DIST_MIN)
    combinacao_inicial = gerar_combinacao_inicial(QTD_CIDADES)
    gerar_listas_e_enviar_pros_processos(combinacao_inicial, matriz_custo)
    melhores_combinacoes = receber_combinacoes()
    print('Melhores Combinacoes:', melhores_combinacoes)
else:
    if rank < qtd_processos:
        matriz_custo, informacoes = comm.recv(source=0)
        melhores_combinacoes = melhores_combinacoes(informacoes)
        comm.send(melhores_combinacoes, dest=0)
