import time, random

ORDEM = 1
RITMO = 0.200

while True:
    # Espaço incial do começo de saída.
    if ORDEM == 1: print("")

    try:
        SELECAO = random.randint(1, 100)
        print("%dº número sorteado: %d" % (ORDEM, SELECAO))
        time.sleep(RITMO)
        ORDEM += 1
    except KeyboardInterrupt:
        print("Você saiu com <Ctrl + C>.")
        exit(0)