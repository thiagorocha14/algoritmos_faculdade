import random
import sys
from threading import Thread

def gerar_combinacao_inicial(qtd_cidades):
    combinacao = [x for x in range(1, qtd_cidades)]
    return combinacao

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
    for cid_origem in range(qtd_cidades):
        print(matriz_custo[cid_origem])
    return matriz_custo

def melhor_combinacao(melhores_combinacoes):
    melhor_combinacao = melhores_combinacoes[0][0]
    melhor_custo = melhores_combinacoes[0][1]
    combinacoes = []
    for combinacao in melhores_combinacoes:
        if combinacao[1] < melhor_custo:
            melhor_custo = combinacao[1]
            melhor_combinacao = combinacao[0]
            combinacoes = [combinacao]
        elif combinacao[1] == melhor_custo:
            combinacoes.append(combinacao)
    return combinacoes

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


class Th(Thread):
    def __init__(self, matriz_custo, lista_cidades, cidade_faltante, tid):
        Thread.__init__(self)
        self.matriz_custo = matriz_custo
        self.lista_cidades = lista_cidades
        self.cidade_faltante = cidade_faltante
        self.tid = tid

    def run(self):
        melhores_combinacoes = []
        lista_cidades = self.lista_cidades
        cidade_faltante = self.cidade_faltante
        combinacoes = permutacoes(lista_cidades)
        for combinacao in combinacoes:
            combinacao.insert(0, cidade_faltante)
            combinacao.insert(0, 0)
            combinacao.append(0)
            custo = calcular_custos(combinacao, self.matriz_custo)
            if melhores_combinacoes == []:
                melhores_combinacoes = [[combinacao, custo, self.tid]]
            elif custo < melhores_combinacoes[0][1]:
                melhores_combinacoes = [[combinacao, custo, self.tid]]
            elif custo == melhores_combinacoes[0][1]:
                melhores_combinacoes.append([combinacao, custo, self.tid])
        self.melhores_combinacoes = melhores_combinacoes

    def retorna_melhores_combinacoes(self):
        return self.melhores_combinacoes


def main():
    QTD_CIDADES = int(sys.argv[1])
    DIST_MAX = int(sys.argv[2])
    DIST_MIN = int(sys.argv[3])
    IMPRESSAO = sys.argv[4]

    matriz_custo = gera_matriz_custo(QTD_CIDADES, DIST_MAX, DIST_MIN)
    combinacao_inicial = gerar_combinacao_inicial(QTD_CIDADES)

    threads = []
    for i in range(1, QTD_CIDADES):
        lista_cidades = combinacao_inicial[:i-1]+combinacao_inicial[i:]
        cidade_faltante = i
        threads.append(Th(matriz_custo, lista_cidades, cidade_faltante, i-1))
        threads[i-1].start()

    melhores_combinacoes = []
    for t in threads:
        t.join()
        melhores_combinacoes += t.retorna_melhores_combinacoes()

    melhores_combinacoes = melhor_combinacao(melhores_combinacoes)

    print()
    if IMPRESSAO == "'True'":
        print('** MELHORES COMBINACOES **')
        for combinacao in melhores_combinacoes:
            print('Combinacao: ', combinacao[0], 'Custo: ', combinacao[1], 'Thread: ', combinacao[2])


if __name__ == "__main__":
    main()
