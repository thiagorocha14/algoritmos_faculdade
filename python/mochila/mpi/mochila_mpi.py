# Importando as bibliotecas
import random
import sys
import numpy as np
import math as m
#Importando MPI
from mpi4py import MPI

comm = MPI.COMM_WORLD

#Definindo o rank e o size
rank = comm.rank
size = comm.size
status = MPI.Status()

random.seed(1)

# Definições
TAM_LOJA     = int(sys.argv[1])
QTD_MAX_PROD = int(sys.argv[2])
VAL_MAX_PROD = int(sys.argv[3])
VOL_MAX_PROD = int(sys.argv[4])
CAP_MOCHILA  = int(sys.argv[5])

#Busca combinação pelo indice
def int_comb(valor, base):
    comb = []
    quo = valor
    base.reverse()
    for b in base:
        res = quo % (b+1)
        quo = quo // (b+1)
        comb.insert(0, res)
    base.reverse()
    return comb

#função para retornar um intervalo de valores com os melhores lucros
def int_combs(inicio, fim, loja):
    combs = []
    base = loja['Quantidade']
    for v in range (inicio, fim+1):
        comb = v, int_comb(v, base)
        comb = valor_comb(comb, loja)
        if comb[0] == inicio: # Primeiro valor precisa ser registrado
            combs.append(comb)
        elif comb[2] > combs[-1][2]:
            combs = []
            combs.append(comb)
        elif comb[2] == combs[-1][2] and comb[2]> -1:
            combs.append(comb)
    return combs


#função para retornar o valor da combinação
def valor_comb(comb, loja):
    valores = loja['Valor']
    valor = 0
    volumes = loja['Volume']
    vol = 0
    for i in range(len(valores)):
        valor += comb[1][i] * valores[i]
        vol += comb[1][i] * volumes[i]

    if vol > CAP_MOCHILA:
        valor = -1

    return comb[0], comb[1], valor

#Gerando a loja
def gera_loja(tam_loja, max_preco, max_vol, qtde_max_prod):
    random.seed(12)
    loja = {
        'Produto': [i for i in range(tam_loja)],
        'Valor': [random.randint(1, max_preco) for i in range(tam_loja)],
        'Volume': [random.randint(1, max_vol) for i in range(tam_loja)],
        'Quantidade': [random.randint(1, qtde_max_prod) for i in range(tam_loja)]
    }
    return loja

# Cálculo do custo e volume da combinação
def custo_vol(loja, comb):
    valores = loja['Valor']
    volumes = loja['Volume']
    custo = 0
    vol = 0
    for i in range(len(valores)):
        custo += valores[i] * comb[i]
        vol += volumes[i] * comb[i]
    return (custo, vol)


if rank == 0:

    #Gerando a loja no processo 0
    loja = gera_loja(TAM_LOJA, VAL_MAX_PROD, VOL_MAX_PROD, QTD_MAX_PROD)
    #Divindo o final do intervalo para os processos
    array_quantidade = [value + 1 for value in loja['Quantidade']]
    intervalo = np.prod(np.array(array_quantidade))
    print('Tamanho Intervalo: ', intervalo)
    print()

    intervalo_dividido = m.ceil(intervalo/(size))
    inicio_inicial = inicio = 0
    fim_inicial = fim = intervalo_dividido - 1
    #Enviando valores para gerar as combinações
    print('Processo 0 :', inicio_inicial, fim_inicial)
    for i in range(1, size):
        inicio = fim + 1
        fim = fim + intervalo_dividido
        if fim > intervalo:
            fim = intervalo
        print('Processo ', i, ':', inicio, fim)
        comm.send((inicio, fim, loja), dest=i)
    print()
    #Gerando as combinações
    comb = int_combs(inicio_inicial, fim_inicial, loja)
    print('Melhores combinacoes processo ', rank, ':' , comb)
    max_final = (0, 0)
    max_comb_final = []
    for teste in comb:
        resp = custo_vol(loja, teste[1])
        if resp[0] >= max_final[0] and resp[1] <= CAP_MOCHILA:
            max_final = resp
            max_comb_final = teste[1]

    #Recebendo maiores combinações dos outros processos e comparando com a do processo 0 e entre si
    for i in range(1, size):
        max, max_comb = comm.recv(source=i)
        if max > max_final:
            max_final = max
            max_comb_final = max_comb

    print()
    print('Loja:')
    print('Produtos:    ', loja['Produto'])
    print('Valores:     ', loja['Valor'])
    print('Volumes:     ', loja['Volume'])
    print('Quantidades: ', loja['Quantidade'])
    print()
    print('Combinação máxima:')
    print(max_comb_final)
    print()
    print('Valores Finais (Custo, Volume):')
    print(max_final)
else:
    #Recebendo valores para gerar as combinações
    inicio, fim, loja = comm.recv(source=0)

    #Gerando as combinações
    comb = int_combs(inicio, fim, loja)
    print('Melhores combinacoes processo ', rank, ':' , comb)
    max = (0, 0)
    max_comb = []
    for teste in comb:
        resp = custo_vol(loja, teste[1])
        if resp[0] >= max[0] and resp[1] <= CAP_MOCHILA:
            max = resp
            max_comb = teste[1]

    #Enviando valores para o processo 0
    comm.send((max, max_comb), dest=0)

