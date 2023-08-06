import numpy as np

def para_one_hot(palavra):
    alfabeto = 'abcdefghijklmnopqrstuvwxyz '
    matriz = np.zeros((len(alfabeto), len(palavra)))
    palavra = palavra.lower()
    for i in range(len(palavra)):
        letra = palavra[i]
        indice = alfabeto.index(letra)
        matriz[indice][i] = 1
    return matriz

def para_string(matriz):
    alfabeto = 'abcdefghijklmnopqrstuvwxyz '
    palavra = ''
    for i in range(matriz.shape[1]):
        indice = np.argmax(matriz[:, i])
        letra = alfabeto[indice]
        palavra += letra
    return palavra

def cifrar(mensagem, P):
    matriz = para_one_hot(mensagem)
    C = np.dot(P, matriz)
    return para_string(C)

def de_cifrar(mensagem, P):
    matriz = para_one_hot(mensagem)
    C = np.dot(P, matriz)
    return para_string(C)

def enigma(mensagem, P, E):
    indice = 0
    resposta = ''
    for letra in mensagem:
        if indice == 0:
            resposta += cifrar(letra, P)
        else:
            letra_nova = cifrar(letra, P)
            for u in range(indice):
                letra_nova = cifrar(letra_nova,E)
            resposta += letra_nova
        indice += 1
    return resposta

def de_enigma(mensagem, P, E):
    indice = 0
    resposta = ''
    for letra in mensagem:
        if indice == 0:
            letra_cifrada = cifrar(letra, P)
            letra_cifrada = para_one_hot(letra_cifrada)
            matriz_cifrada = np.dot(np.linalg.inv(P),letra_cifrada)
            resposta += para_string(matriz_cifrada)
        else:
            letra_nova = cifrar(letra, P)
            letra_nova = para_one_hot(letra_nova)
            matriz_cifrada = np.dot(np.linalg.inv(P),letra_nova)
            for u in range(indice):
                letra_nova = para_string(letra_nova)
                letra_nova = cifrar(letra_nova,E)
                letra_cifrada = para_one_hot(letra_cifrada)
            matriz_cifrada = np.dot(np.linalg.inv(E),letra_cifrada)
            resposta += para_string(matriz_cifrada)
        indice += 1
    return resposta

