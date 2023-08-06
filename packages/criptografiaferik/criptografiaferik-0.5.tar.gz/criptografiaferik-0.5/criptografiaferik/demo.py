from main import *
msg = 'Olá a todos!'
msg_onehot = para_one_hot(msg)
msg_texto = para_string(msg_onehot)
msg_cifrada = cifrar(msg_texto)
msg_decifrada = de_cifrar(msg_cifrada)
msg_enigma = enigma(msg_decifrada)
msg_enigma_resolvido = de_enigma(msg_enigma)
print(f'''
Exemplo 1:\nA mensagem de entrada é '{msg}'\n. . .
Transformando para one-hot...\n Mensagem OneHot: {msg_onehot}
Retornando para texto...\n Mensagem: {msg_texto}
Cifrando a mensagem...\n Mensagem cifrada: {msg_cifrada}
Decifrando a mensagem...\n Mensagem decifrada: {msg_decifrada}
Criando um enigma da mensagem...\n Enigma gerado: {msg_enigma}
Decifrando o enigma...\n Enigma decifrado: {msg_enigma_resolvido}
Finalizando testes.
''')

