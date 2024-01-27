# Importando as bibliotecas
import random
import sys
import numpy as np

random.seed(1)

# Definições
TAM_LOJA     = int(sys.argv[1])       # 7
QTD_MAX_PROD = int(sys.argv[2])       # 9
VAL_MAX_PROD = int(sys.argv[3])       # 20
VOL_MAX_PROD = int(sys.argv[4])       # 10
CAP_MOCHILA  = int(sys.argv[5])       # 30

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

#gerando a loja
loja = gera_loja(TAM_LOJA, VAL_MAX_PROD, VOL_MAX_PROD, QTD_MAX_PROD)

array_quantidade = [value + 1 for value in loja['Quantidade']]
intervalo = np.prod(np.array(array_quantidade))

print('Tamanho Intervalo: ', intervalo)

comb = int_combs(0, intervalo, loja)

max = (0, 0)
max_comb = []
for teste in comb:
    resp = custo_vol(loja, teste[1])
    if resp[0] >= max[0] and resp[1] <= CAP_MOCHILA:
        max = resp
        max_comb = teste[1]

print()
print('Loja:')
print('Produtos:    ', loja['Produto'])
print('Valores:     ', loja['Valor'])
print('Volumes:     ', loja['Volume'])
print('Quantidades: ', loja['Quantidade'])
print()
print('Combinação máxima:')
print(max_comb)
print()
print('Valores Finais (Custo, Volume):')
print(max)
