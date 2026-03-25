import time, threading, sys
import legivel

class BarraProgresso:
    def __init__(self, LIMITE) -> None:
        self.atual: int = 0
        self.TOTAL: int = LIMITE

    def percentual(self) -> float:
        return self.atual / self.TOTAL

    def __iadd__(self, X: int):
        if X + self.atual <= self.TOTAL:
            self.atual += X
        return self

    def __str__(self) -> str:
        (CHEIO, VAZIO) = ('#', '.')
        COMPRIMENTO = 42
        preenchido = int(self.percentual() * COMPRIMENTO)
        preenchimento = CHEIO * preenchido
        vacuo = (COMPRIMENTO - preenchido) * VAZIO
        final = legivel.valor_grande_legivel(self.TOTAL)

        return "[" + preenchimento + vacuo + "] " + f"{self.atual:^8d} / {final}"
    
    def __repr__(self):
        return self.__str__()


def barra_de_progresso(atual, TOTAL): pass

def visualizacao_da_barra(obj: BarraProgresso):
    finalizado = abs(1.0 - obj.percentual()) < 0.001

    while (not finalizado):
        print(str(obj), end='\n')
        sys.stdout.flush()
        time.sleep(1.1)
        finalizado = abs(1.0 - obj.percentual()) < 0.001
    
    # Impressão final.
    print(str(obj), end='')
    sys.stdout.flush()


barra = BarraProgresso(6e7)
tredi = threading.Thread(target=visualizacao_da_barra, args=(barra,))

tredi.start()
while barra.percentual() < 1.0:
    barra += 1
tredi.join()