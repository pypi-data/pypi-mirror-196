import numpy as np
# criando uma lista com todos os caracteres permitidos
alfabeto =[ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','1','2','3','4','5','6','7','8','9','0','!','@','#','$','%','&','*','(',')','-','_','+','=','á', 'ã', 'â', 'é', 'ê', 'í', 'ó', ':', '.',',']

# criando duas matrizes 2D, ambas com a mesma quantidade de linhas e colunas do alfabeto, preenchidas com zeros
matriz = np.zeros((len(alfabeto),len(alfabeto)), dtype=int)
matriz2 = np.zeros((len(alfabeto),len(alfabeto)), dtype=int)

# preenchendo as matrizes com 1s de acordo com o método de cifra utilizado
for i in range(len(alfabeto)):
    matriz[i, (i+1)%len(alfabeto)] = 1
    matriz2[i, (i+2)%len(alfabeto)] = 1

# função auxiliar para validar a entrada de mensagem, levantando um erro se a mensagem estiver vazia
def valida_mensagem(msg):
    if msg == '':
            raise ValueError
    return True

def para_one_hot(msg):
    '''Uma função `para_one_hot(msg : str)` para codificar mensagens como uma matriz usando one-hot encoding'''
    try:
        # se a mensagem for válida
        if valida_mensagem(msg):
            # cria uma matriz com a mesma quantidade de linhas do alfabeto e a quantidade de colunas igual ao tamanho da mensagem
            matriz = np.zeros([len(alfabeto),len(msg)])
            msg = msg.lower()
            # preenche a matriz com 1s nas posições correspondentes aos caracteres da mensagem
            for j, letra in enumerate(msg):
                if letra in alfabeto:
                    i = alfabeto.index(letra)
                    matriz[i][j] = 1
                else:
                    if letra.isspace():
                        for coluna in range(len(alfabeto)):
                            matriz[coluna][j] = 0
                    else:
                        for coluna in range(len(alfabeto)):
                            matriz[coluna][j] = 1
        
    except:
        return {"erro": "Mensagem inválida, coloque uma string não vazia"}
    return matriz

def para_string(M):
    '''Uma função `para_string(M : np.array)` para converter mensagens da representação one-hot encoding para uma string legível'''
    msg = ''
    try:
        # Itera sobre as colunas da matriz transposta
        for coluna in M.T:
            # Inicia a quantidade de elementos iguais a 1 na coluna como zero
            quantidade = 0
            for i, elemento in enumerate(coluna):
                # Itera sobre cada elemento da coluna e verifica se é igual a 1
                # Caso seja, incrementa a quantidade e guarda o índice do elemento
                if elemento == 1:
                    quantidade+=1
                    indice = i
            # Caso a quantidade de elementos iguais a 1 na coluna seja maior que 1,
            # adiciona um ponto de interrogação na mensagem
            if quantidade > 1:
                msg += '?'
            # Caso a quantidade de elementos iguais a 1 na coluna seja igual a 1,
            # adiciona o caractere correspondente ao índice do elemento na mensagem
            elif quantidade == 1:
                msg += alfabeto[indice]
             # Caso não exista nenhum elemento igual a 1 na coluna, adiciona um espaço na mensagem
            else:
                msg += ' '
    except:
        return {"erro": "Mensagem inválida, coloque uma matriz (np.array)"}
    return msg



def cifrar(msg, P=matriz):
    '''Uma função `cifrar(msg : str, P : np.array)` que aplica uma cifra simples
        em uma mensagem recebida como entrada e retorna a mensagem cifrada. `P` é a
        matriz de permutação que realiza a cifra.'''
    try:
        # Verifica se a mensagem é válida
        if valida_mensagem(msg):
            # Converte a mensagem para uma matriz one-hot
            matriz_msg = para_one_hot(msg)
            # Realiza a multiplicação matricial da matriz one-hot pela matriz de cifragem
            result = P @ matriz_msg
            return para_string(result)
    # Trata qualquer exceção que possa ocorrer
    except:
        return {"erro":"Não há mensagem, ou a matriz P não é válida" }


def de_cifrar(msg, P=matriz):
    ''' Uma função `de_cifrar(msg : str, P : np.array)` que recupera uma mensagem
        cifrada, recebida como entrada, e retorna a mensagem original. `P` é a matriz de permutação que realiza a cifra.'''
    try:
        # Verifica se a mensagem é válida
        if  valida_mensagem(msg):
            # Converte a mensagem para uma matriz one-hot
            msg = para_one_hot(msg)
            # Realiza a multiplicação matricial da matriz one-hot pela inversa da matriz de cifragem
            result = np.linalg.inv(P) @ msg
            return para_string(result)
    # Trata qualquer exceção que possa ocorrer
    except:
        return {"erro": "Não há mensagem, ou a matriz P não é válida"}



def enigma(msg, P=matriz, E=matriz2):
    '''Função `enigma(msg : str, P : np.array, E : np.array)` que faz a cifra enigma na mensagem de entrada
        usando o cifrador `P` e o cifrador auxiliar `E`, ambos representados como matrizes de permutação.'''
    try:
        # Verifica se a mensagem é válida
        if valida_mensagem(msg):
            matriz = ''
            # Realiza a multiplicação matricial da matriz one-hot pela matriz de cifragem
            result1 = P@para_one_hot(msg)
            # Itera sobre as colunas da matriz transposta
            for indice, coluna in enumerate(result1.T):
                # Verifica se o índice da coluna é diferente de zero
                if indice != 0:
                    # Converte a coluna em um array
                    coluna = np.array([[x] for x in coluna])
                    # Realiza a multiplicação matricial da coluna pela matriz E
                    for i in range(indice):
                        coluna = E @ coluna
                    # Concatena a coluna na matriz
                    matriz = np.hstack((matriz, coluna))
                else:
                    # Converte a coluna em um array
                    matriz = np.array([[x] for x in coluna])
    except:
        return {'erro': 'Não há mensagem, ou a matriz P ou E não é válida'}
    return para_string(matriz)


def de_enigma(msg, P=matriz, E=matriz2):
    '''Uma função `de_enigma(msg : str, P : np.array, E : np.array)` que recupera uma mensagem cifrada como enigma
        assumindo que ela foi cifrada com o usando o cifrador `P` e o cifrador auxiliar `E`, ambos representados como matrizes de permutação.'''
    try:
        # Verifica se a mensagem é válida
        if valida_mensagem(msg):
            matriz = ''
            result1 = para_one_hot(msg)
            # Itera sobre as colunas da matriz transposta
            for indice, coluna in enumerate(result1.T):
                if indice != 0:
                    # Converte a coluna em um array
                    coluna = np.array([[x] for x in coluna])
                    # Realiza a multiplicação matricial da coluna pela inversa da matriz E
                    for i in range(indice):
                        # Realiza a multiplicação matricial da coluna pela inversa da matriz E
                        coluna = np.linalg.inv(E) @ coluna
                    # Concatena a coluna na matriz
                    coluna = np.linalg.inv(P) @ coluna
                    matriz = np.hstack((matriz, coluna))
                else:
                    matriz = np.array([[x] for x in coluna])
                    matriz = np.linalg.inv(P) @ matriz
    except:
        return {"erro":"Não há mensagem, ou a matriz P ou E não é válida"}
    return para_string(matriz)


