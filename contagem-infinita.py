"""
  O programa sempre fica contando, com a contagem anterior. O limite é o valor de overflow 
 da linguagem.
"""
from time import (sleep)
from random import (randint)

CONTAGEM = 0
# Valor expresso em milisegundos.
RITMO = randint(760, 2100) / 1000
BANCO_DE_DADOS = "data/atual-contagem.dat"


def salva_contagem():
    global CONTAGEM

    with open(BANCO_DE_DADOS, "wb") as stream:
        data = CONTAGEM.to_bytes(8, byteorder="little")
        stream.write(data)

def carrega_contagem() -> int:
    global CONTAGEM

    with open(BANCO_DE_DADOS, "rb") as stream:
        data = stream.read()
        CONTAGEM = int.from_bytes(data, byteorder="little")
    return CONTAGEM

def cria_um_arquivo_com_contagem_resetada():
    VALOR_INICIAL = b"00000000"

    arquivo = open(BANCO_DE_DADOS, "wb")
    arquivo.write(VALOR_INICIAL)
    arquivo.close()

def tenta_carregar_banco_de_dados():
    global CONTAGEM

    # Cria arquivo de atual contagem se não houver um.
    try: 
        CONTAGEM = carrega_contagem()
    except FileNotFoundError:
        cria_um_arquivo_com_contagem_resetada()
        print("Arquivo criado com sucesso.")
    finally:
        print("Leitura realizada.")



tenta_carregar_banco_de_dados()

while True:
    try:
        print(f"A contagem está em {CONTAGEM}")
        CONTAGEM += 1
        sleep(RITMO)
        # Chamada de sisteam que faz operação muito lenta de gravação:
        salva_contagem()

    except KeyboardInterrupt:
        print("Você pressionou <Ctrl + C> prá sair!")
        exit(0)

