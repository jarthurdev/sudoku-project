import random
from math import sqrt

def Validacao(matriz, linha, coluna, num, tamanho):
    tamanho_subgrade = int(sqrt(tamanho))

    # Verificar linha
    if num in matriz[linha]:
        return False
    
    # Verificar coluna
    if num in [matriz[x][coluna] for x in range(tamanho)]:
        return False
    
    # Verificar subgrade
    linha_inicial = linha - linha % tamanho_subgrade
    coluna_inicial = coluna - coluna % tamanho_subgrade

    for l in range(tamanho_subgrade):
        for c in range(tamanho_subgrade):
            if matriz[l + linha_inicial][c + coluna_inicial] == num:
                return False
    
    return True

def Preencher_matriz(matriz, linha, coluna, tamanho):
    if linha == tamanho:
        return True
    
    if coluna == tamanho:
        return Preencher_matriz(matriz, linha + 1, 0, tamanho)

    if matriz[linha][coluna] != 0:
        return Preencher_matriz(matriz, linha, coluna + 1, tamanho)

    for num in random.sample(range(1, tamanho + 1), tamanho):
        if Validacao(matriz, linha, coluna, num, tamanho):
            matriz[linha][coluna] = num
            if Preencher_matriz(matriz, linha, coluna + 1, tamanho):
                return True
            matriz[linha][coluna] = 0
    return False

def Gerar_sudoku(tamanho):
    matriz = [[0 for _ in range(tamanho)] for _ in range(tamanho)]
    Preencher_matriz(matriz, 0, 0, tamanho)
    return matriz

def Remover_nums(matriz, nums_faltando):
    n = len(matriz)
    posicao = [(l, c) for l in range(n) for c in range(n)]
    random.shuffle(posicao)
    for i in range(nums_faltando):
        linha, coluna = posicao[i]
        matriz[linha][coluna] = 0