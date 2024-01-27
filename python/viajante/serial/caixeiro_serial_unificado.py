# Importação das bibliotecas
import random
import sys

# CONSTANTES DEFINIDAS NA EXECUÇÃO
QTD_CIDADES   = int(sys.argv[1])
DIST_MIN      = int(sys.argv[2])
DIST_MAX      = int(sys.argv[3])


def gerar_combinacoes(qtd_cidades, matriz):
    lista_inicial = list(range(1, qtd_cidades))
    combinacoes = permutacoes_calculada(lista_inicial, qtd_cidades, matriz)
    # combinacoes = permutacoes(lista_inicial)
    return combinacoes

def permutacoes(lista):
    if (len(lista) == 0):
      return[[]]
    combinacoes = []
    for i in range(len(lista)):
      valor_atual = lista[i]
      lista_pendente = lista[:i]+lista[i+1:]
      lista_permutacoes = permutacoes(lista_pendente)
      for permutacao in lista_permutacoes:
        combinacoes.append([valor_atual]+permutacao)
    return combinacoes

def permutacoes_calculada(lista, qtd_cidades, matriz):
    if (len(lista) == 0):
      return[[]]
    combinacoes = []
    melhor_comb = []
    melhor_custo = 0
    for i in range(len(lista)):
      valor_atual = lista[i]
      lista_pendente = lista[:i]+lista[i+1:]
      lista_permutacoes = permutacoes(lista_pendente)
      for permutacao in lista_permutacoes:
        combinacao = [valor_atual]+permutacao
        if (len(combinacao) == qtd_cidades-1):
          custo = calcular_custo(combinacao, matriz)
          if (custo < melhor_custo or melhor_custo == 0):
            melhor_custo = custo
            combinacoes = []
            combinacoes.append([combinacao, custo])
        else:
          combinacoes.append(combinacao)
    return combinacoes

def calcular_custo(comb, custo):
    valor = 0
    cidade_atual = 0
    comb.append(0)
    for cidade in comb:
      valor += custo[cidade_atual][cidade]
      cidade_atual = cidade
    comb.insert(0, 0)
    return valor

# Função geradora do custo (Matriz de Custo)
def gerar_matriz_distancia(qtd_cidades, dist_min, dist_max):
    random.seed(12)
    matriz_distancia = [[0 for x in range(qtd_cidades)] for y in range(qtd_cidades)]
    for cid_origem in range(qtd_cidades):
        for cid_destino in range(qtd_cidades):
            if cid_origem < cid_destino:
                valor = random.randint(dist_min, dist_max)
                matriz_distancia[cid_origem][cid_destino] = (valor)
                matriz_distancia[cid_destino][cid_origem] = (valor)
            else:
                matriz_distancia[cid_origem][cid_origem] = 0
    return matriz_distancia


def main():
    # Gerando a Matriz de distancia
    print('----------MATRIZ----------')
    matriz = gerar_matriz_distancia(QTD_CIDADES, DIST_MIN, DIST_MAX)
    print(" ", end = "  ")
    for x in range(0, QTD_CIDADES):
        print(x, end = "  ")

    print()
    for index, valores in enumerate(matriz):
      print(index, valores)

    #print('----------COMBINACOES----------')
    combinacoes = gerar_combinacoes(QTD_CIDADES, matriz)

    print()
    print('----------MELHOR COMBINACAO----------')
    for combinacao in combinacoes:
      print('Combinação:', combinacao[0], 'Valor:', combinacao[1])

if __name__ == '__main__':
    main()
