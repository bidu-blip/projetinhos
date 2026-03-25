#python -OO
import sys, pprint, string, shutil

def ler_conteudo(caminho: str) -> str:
    assert isinstance(caminho, str)

    arquivo = open(caminho, "rt")
    conteudo = arquivo.read()
    arquivo.close()

    return conteudo

def processamento(conteudo: str) -> dict:
    assert isinstance(conteudo, str)

    distribuicao = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}

    for caractere in conteudo:
        char = caractere

        if (not char.isprintable()) or (not char.isalnum()):
            continue

        if caractere in distribuicao.keys():
            distribuicao[caractere] += 1
        else:
            distribuicao[caractere] = 0
    return distribuicao


def formatacao_do_cabecalho(MAXIMO_X, TITULO):
    assert isinstance(MAXIMO_X, int)
    assert isinstance(TITULO, str)

    print('\n', " " * ((MAXIMO_X - len(TITULO))// 2), TITULO, end='\n\n')

def visualizacao_da_distruicao(distribuicao: dict):
    assert (isinstance(distribuicao, dict))

    contagem = 1
    MARGEM = 10
    MAXIMO_X = shutil.get_terminal_size()
    LATERAL = MAXIMO_X.columns - MARGEM
    buffer = 0
    TABULAR = ' ' * 4

    formatacao_do_cabecalho(LATERAL, "Distribuição de Letras")

    for chave in distribuicao.keys():
        if buffer < LATERAL:
            fmt = f"{chave}: {distribuicao[chave]:^4d}"
            print(fmt, end=TABULAR)
            buffer += len(fmt) + len(TABULAR)
        else:
            print("")
            buffer = 0

if len(sys.argv) == 2:
    ARQUIVO = sys.argv[1]
    DADOS = ler_conteudo(ARQUIVO)
    
    print(f"Processando o arquivo: {ARQUIVO}")
    
    if __debug__:
        pprint.pprint(processamento(DADOS))
    else:
        visualizacao_da_distruicao(processamento(DADOS))
else:
    print("Sem argumentos.")