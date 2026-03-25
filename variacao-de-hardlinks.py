"""
  O programa cria de forma aleatória, ao mesmo tempo que contabiliza-os,
hardlinks.
"""
from random import (randint, choice)
from pathlib import (Path)
from unittest import (TestCase)
from os import (makedirs, getenv)
from threading import (Thread)
import time

# Não usa mais, uma função geral tal caminho.
REPOSITORIO = Path("data/clonagens")


def escolhe_um_arquivo() -> Path:
    diretorio = Path(".")
    escolha = choice(list(diretorio.iterdir()))

    while escolha.is_dir() or escolha.is_symlink():
        escolha = choice(list(Path(".").iterdir()))
    return escolha

def incrementa_indice_na_string(In: str) -> str:
    (ABRE, FECHA) = ('(', ')')
    nome = In
    (a, b) = (nome.rfind(ABRE), nome.rfind(FECHA))

    if (ABRE in nome) and (FECHA in nome):    
        assert (a != -1) and (b != -1)
        # Copia trecho entre parênteses.
        trecho = nome[a:(b + 1)]
        valor = int(nome[(a + 1):b])
        novo_trecho = f"({valor + 1})"

        return nome.replace(trecho, novo_trecho)
    else:
        return nome + "(1)"

def faz_mais_um_hardlink(arquivo: Path) -> Path:
    repositorio = REPOSITORIO
    alvo = repositorio.joinpath(arquivo.name)

    makedirs(repositorio, exist_ok=True)
    try:
        alvo.hardlink_to(arquivo)
    except FileExistsError:
        numero = 1

        while True:
            try:
                alvo = alvo.parent.joinpath(incrementa_indice_na_string(alvo.name))
                alvo.hardlink_to(arquivo)
                break
            except FileExistsError:
                numero += 1
            
            if numero > 30:
                raise Exception("loop infinito!")
    return alvo

def faz_um_hardlink_arbitrario_dos_arquivos_locais() -> Path:
    Input = escolhe_um_arquivo()
    output = faz_mais_um_hardlink(Input)
    
    return output

def velocidade_de_criacao(inicio) -> float:
    decorrido = time.time() - inicio
    
    if decorrido < 7:
        return 1.01
    elif decorrido >= 7 and decorrido < 10:
        return 0.7
    elif decorrido >= 10 and decorrido < 30:
        return 0.5
    else:
        return 0.3

def cria_hardlinks_periodicamente(output: list[Path]):
    inicio = time.time()
    disparado = False
    
    while (len(output) > 0) or (not disparado):
        disparado = True
        caminho = faz_um_hardlink_arbitrario_dos_arquivos_locais()
        
        output.append(caminho)
        print(f"{caminho.name:.<60} [criado]")
        time.sleep(velocidade_de_criacao(inicio))

def velocidade_de_exclusao(inicio) -> float:
    decorrido = time.time() - inicio
    
    if decorrido < 7:
        return 1.2
    elif decorrido >= 7 and decorrido < 10:
        return 0.8
    elif decorrido >= 10 and decorrido < 30:
        return 0.6
    elif decorrido >= 30 and decorrido< 90:
        return 0.3
    else:
        return 0.1
    
def deleta_hardlinks_periodicamente(output: list[Path]):
    inicio = time.time()
    time.sleep(3)
    print("Deletações foi iniciado.")
    
    while len(output) > 0:
        quantia = len(output)
        escolha = randint(0, quantia - 1)
        caminho = output[escolha]
        
        caminho.unlink()
        output.pop(escolha)
        print(f"{caminho.name:.<60} [deletado]")
        time.sleep(velocidade_de_exclusao(inicio))

def monitorador_de_quantia(exclusoes: list):
    time.sleep(2)
    print("Monitor de hardlinks foi acionado.")
    
    while exclusoes != []:
        entries = REPOSITORIO.iterdir()
        quantia = len(list(entries))
        print(f"\tAinda {quantia} arquivos restantes.")
        time.sleep(2.7)
    print("O monitor foi desligado.")
    
def caminho_absoluto_repositorio() -> Path:
    ENV_VAR = getenv("LAURIE_CODES")
    NOME = __name__.strip(".py")
    
    return Path(ENV_VAR).joinpath(f"data/tests/{NOME}/clonagens")
    
if __name__ == "__main__":
    exclusoes = []
    # Nova atribuição, para algo mais robusto.
    REPOSITORIO = caminho_absoluto_repositorio()
    
    # Adicionando arquivos já existenstes no repositório.
    for caminho in REPOSITORIO.iterdir():
        exclusoes.append(caminho)
    print(f"Foram adicionados {len(exclusoes)} arquivos já no repositório")
    
    fio_criacao = Thread(target=cria_hardlinks_periodicamente, args=(exclusoes,))
    fio_deletacao = Thread(target=deleta_hardlinks_periodicamente, args=(exclusoes,))
    fio_monitorador = Thread(target=monitorador_de_quantia, args=(exclusoes,))
    
    fio_criacao.start()
    fio_deletacao.start()
    fio_monitorador.start()
    fio_deletacao.join()
    
"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                                    Testes Unitários
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
"""
class FormatacaoDeCaminho(TestCase):
    def runTest(self):
        resultado = caminho_absoluto_repositorio()

        print("\nResultado:", "\n\t\"", resultado, end="\"\n\n")
        self.assertTrue(resultado.exists())

class SelecaoArbitrariaDeArquivos(TestCase):
    def runTest(self):
        for _ in range(15):
            print(escolhe_um_arquivo())

class CriaUmHardlinqueDeUmArquivoArbitrario(TestCase):
    def tearDown(self):
        self.Out.unlink()
        print(f"Destruído: {self.Out}")

    def runTest(self):
        In = escolhe_um_arquivo()
        self.Out = faz_mais_um_hardlink(In)

        print(f"Criado: {self.Out}")

class TratandoColisoesDeNomes(TestCase):
    def setUp(self):
        self.Out = []

    def runTest(self):
        for _ in range(20):
            In = faz_mais_um_hardlink(escolhe_um_arquivo())
            self.Out.append(In)
            print(f"Criado: {In}")
    def tearDown(self):
        for caminho in self.Out:
            caminho.unlink()
            print(f"Destruído: {caminho.name}")
    
class IncrementacaoDeIndice(TestCase):
    def setUp(self):
        In = list(map(lambda X: X.name, Path().iterdir()))
        self.In = list(map(lambda X: f"{X}({choice([1, 2, 3])})",  In))

    def runTest(self):
        for item in self.In: 
            print(f"{item} ====> {incrementa_indice_na_string(item)}")

class FazUmHardlinkArbitrarioDosArquivosLocais(TestCase):
    def runTest(self):
        exclusoes = []
        
        for _ in range(13):
            caminho = faz_um_hardlink_arbitrario_dos_arquivos_locais()
            exclusoes.append(caminho)
            time.sleep(1.3)
        
        for item in exclusoes:
            item.unlink()
            print(f"'{item}' deletado.")
            time.sleep(0.8)
