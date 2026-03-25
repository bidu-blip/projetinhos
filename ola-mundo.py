
if __debug__:
    import os
    print("PYTHON_PATH: %s" % os.getenv("PYTHONPATH"))

import time, random, sys
# [Para o desenvolvedor] Adicione o caminho da biblioteca na variável
# de ambiente 'PYTHONPATH'. Futuramente haverá um modo de exportar para
# outros usuários, além do desenvolver, rodar tal código.
from legivel import (tempo as tempo_legivel)


ORDEM = 1; 
AMOSTRA_DE_MENSAGENS = [
    "Olá Mundo", "O sol está bem vermelho", "Meter o pé na jaca", "Um dia bem cizento",
    "É muito comum tipo de pessoa", "Olá pessoal", "Olá galerinha na internet"
]
INICIO = time.time()

def print_animado(texto: str) -> None:
    RITMO = 0.080

    for caractere in texto:
        print(caractere, sep='', end='')
        sys.stdout.flush()
        time.sleep(RITMO)
    print("")

def espaca_no_comeco() -> None:
    # Espaço incial do começo de saída.
    if ORDEM == 1: print("")

def contabilizar_chamadas(rotina, argumento) -> None:
    global ORDEM
    M = 10

    if (ORDEM % M == 0):
        decorrido = time.time() - INICIO
        traducao = tempo_legivel(decorrido, acronomo=True)
        print(
            "\nForam feitos %d 'prints'; o total está em %d; já se passaram %s." 
            % (M, ORDEM, traducao), end='\n\n'
        )
        
    rotina(argumento)
    ORDEM += 1

def mensagem_aleatoria() -> str:
    quantia = len(AMOSTRA_DE_MENSAGENS)
    indice = random.randint(0, quantia - 1)

    return AMOSTRA_DE_MENSAGENS[indice]

while True:
    try:
        espaca_no_comeco()
        contabilizar_chamadas(print_animado, mensagem_aleatoria())
    except KeyboardInterrupt:
        print("Você saiu com <Ctrl + C>.")
        exit(0)