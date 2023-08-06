import numpy as np
import random

alphabet = "abcdefghijklmnopqrstuvwxyz0123456789.,;:!?()[]{}-+*/=<>@#$%&'\"áàéíóúâêûôãõ "

def para_one_hot(msg: str):
    """
    Função que converte uma string em uma matriz one-hot,
    onde cada linha representa um caracter do alfabeto e cada coluna representa um caracter da mensagem.
    """
    char_to_index = {}

    for i, char in enumerate(alphabet):
        char_to_index[char] = i

    num_chars = len(alphabet)
    num_timesteps = len(msg)
    one_hot = np.zeros((num_chars, num_timesteps))
    for i, char in enumerate(msg.lower()):
        if char in char_to_index:
            one_hot[char_to_index[char], i] = 1
        else:
            one_hot[char_to_index["?"], i] = 1
    return one_hot


def para_string(M: np.array):
    """
    Função que converte uma matriz one-hot em uma string.
    """
    msg = ""
    for i in range(M.shape[1]):   # iterar através das colunas (caracteres) da matriz
        indices = np.where(M[:,i] == 1)[0]  # encontra os índices dos elementos igual a 1 na coluna atual
        if indices.size > 0:  # se houver um índice válido, adiciona a letra correspondente à mensagem
            msg += alphabet[indices[0]]
        else:  # se não houver um índice válido, adiciona um espaço em branco à mensagem
            msg += " "
    return msg


def cifrar(msg:str, P:np.array):
    """
    Função que aplica uma cifra de substituição simples a uma mensagem,
    consiste em substituir cada caracter da mensagem por um caracter de um alfabeto cifrador.
    Essa substituição é feita trocando o elemento n do alfabeto cifrador pelo elemento n do alfabeto original.
    Essa operação é feita multiplicando a matriz P (matriz permutação) pelo vetor M, onde P é a matriz one-hot do alfabeto cifrador,
    e M é a matriz one-hot da mensagem.
    """
    M = para_one_hot(msg)
    C = np.dot(P, M)

    return para_string(C)
    

def de_cifrar(msg: str, P:np.array):
    """
    Função que decifra uma mensagem cifrada com a função cifrar.
    Ou seja, recupera a mensagem original a partir da mensagem cifrada e da matriz P.
    """
    P_INV = np.linalg.inv(P)
    C = para_one_hot(msg)
    M_DECIFRADA = np.dot(P_INV, C)
    msg = para_string(M_DECIFRADA)
    return msg



def enigma(msg:str, seed:int = 40):
    """
    Função que aplica uma cifra semelhante à cifra da máquina Enigma,
    famosa máquina de criptografia usada pelos nazistas durante a Segunda Guerra Mundial.
    Consiste em aplicar uma cifra de substituição simples a cada caracter da mensagem,
    onde cada caracter da mensagem é substituído por um caracter de um alfabeto cifrador
    que é cifrado por um alfabeto auxiliar, a cada substituição.

    """

    ## Criação do alfabeto cifrador e do alfabeto auxiliar
    random.seed(seed)
    alfabeto_cifrador = list(alphabet)
    random.shuffle(list(alfabeto_cifrador))
    alfabeto_cifrador = "".join(alfabeto_cifrador)

    cifrador_aux = list(alfabeto_cifrador)
    random.shuffle(cifrador_aux)
    cifrador_aux = "".join(cifrador_aux)

    ## Transformação da mensagem e alfabetos em matriz one-hot
    M = para_one_hot(msg)
    P = para_one_hot(alfabeto_cifrador)
    E = para_one_hot(cifrador_aux)

    matriz_resposta = np.zeros((len(alphabet),len(msg)))

    ## Aplicação do algoritmo
    ## Segue a formula: R = E^i * P * M
    for i in range(len(msg)):
        matriz_resposta[:,i] = (np.linalg.matrix_power(E,i))@P@M[:,i]

    return para_string(matriz_resposta)



def de_enigma(msg:str, seed:int = 40):
    """
    Função que decifra uma mensagem cifrada com a função enigma.
    """
    random.seed(seed)
    alfabeto_cifrador = list(alphabet)
    random.shuffle(list(alfabeto_cifrador))
    alfabeto_cifrador = "".join(alfabeto_cifrador)

    cifrador_aux = list(alfabeto_cifrador)
    random.shuffle(cifrador_aux)
    cifrador_aux = "".join(cifrador_aux)

    M = para_one_hot(msg)
    P = para_one_hot(alfabeto_cifrador)
    E = para_one_hot(cifrador_aux)

    matriz_resposta = np.zeros((len(alphabet),len(msg)))
    for i in range(len(msg)):
        matriz_resposta[:,i] = np.linalg.inv(P)@(np.linalg.matrix_power(E,-i))@M[:,i]

    return para_string(matriz_resposta)
