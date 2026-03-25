import math, time, os, shutil, sys


def largura_do_terminal() -> int:
    "Coordenadas linhas e colunas, respectivamente."
    try:
        COMPRIMENTO = os.get_terminal_size().columns
    except OSError:
        COMPRIMENTO = shutil.get_terminal_size().columns
    else: pass
    finally: pass
    return COMPRIMENTO

def desenha_linha(posicao: int):
    x = posicao
    LARGURA_DE_TELA = largura_do_terminal()
    LIMITE_DE_TELA = ( LARGURA_DE_TELA - 2)
    indice  = math.floor(x* math.sin(x) + x)

    if indice >= LIMITE_DE_TELA:
        raise OverflowError("passou a dimensão da tela.")
    print('.' * int(indice), '*')
    sys.stdout.flush()


def execucao_da_animacao():
    cursor = 1

    while True:
        try:
            desenha_linha(cursor)
            time.sleep(0.250)
        except OverflowError:
            print("Chegou ao final da tela.")
            break
        except KeyboardInterrupt:
            print("Você pressionou <Ctrl + C> prá sair.")
            exit(0)
        
        cursor += 1/4

execucao_da_animacao()