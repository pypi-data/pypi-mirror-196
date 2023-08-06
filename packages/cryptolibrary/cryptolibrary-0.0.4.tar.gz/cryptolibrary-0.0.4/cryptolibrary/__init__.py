import numpy as np

def para_one_hot(palavra):
    alfabeto = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()[}{];:",.<>/?\| '
    matriz = np.zeros((len(alfabeto), len(palavra)))
    palavra = palavra.lower()
    for i in range(len(palavra)):
        letra = palavra[i]
        indice = alfabeto.index(letra)
        matriz[indice][i] = 1
    return matriz

def para_string(matriz):
    alfabeto = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()[}{];:",.<>/?\| '
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
    C = np.dot(np.linalg.inv(P),matriz)
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
            letra = de_cifrar(letra, P)
            resposta += letra
        else:
            for u in range(indice):
                letra = de_cifrar(letra,E)
            letra = de_cifrar(letra, P)
            resposta += letra
        indice += 1
    return resposta

