"""
    Reduz os últimos comandos digitados no GitBash. Ele deixa apenas uma quantia
  dos últimos digitados. Está quantia fica ao desejo do executador da função oferece-la.
  O desenvolvedor definiu uma valor padrão, más pode ser alterado.
"""

from os       import (getenv, makedirs)
from pathlib  import (Path)
from queue    import (LifoQueue as Stack)
from shutil	  import (copy as CopyFile)
from unittest import (TestCase)
from io	  	  import (TextIOBase)

BASE = Path(getenv("HOMEPATH"))
CAMINHO = BASE.joinpath(".bash_history")

if __debug__:
	print(BASE, BASE.exists())
	print(CAMINHO, CAMINHO.exists())


def empilha_todas_suas_linhas(arquivo: TextIOBase) -> Stack:
	assert (isinstance(arquivo, TextIOBase))

	pilha = Stack()

	for line in arquivo:
		pilha.put(line)
	
	if __debug__:
		print("Terminado.")
	return pilha

def despejas_no_arquivo(pilha: Stack, arquivo: open) -> None:
	# Retirando todos, e colocando num arquivo, entretanto, agora pega
	# apenas a quantia definida 'LIMITE', e coloca os últimos.
	pilha_de_linhas = pilha
	contagem 		= 0
	LIMITE 			= 15

	while (not pilha_de_linhas.empty()):
		remocao = pilha_de_linhas.get_nowait()

		if __debug__:
			print(f"{contagem + 1}º. '{remocao.rstrip('\n')}'")
		arquivo.write(remocao)
		contagem += 1

		if contagem > LIMITE:
			break

#   O algoritimo funcionaria deste modo. Ele abre o arquivo(em modo de leitura) com histórico de 
# comandos, ler linha por linha. Cada linha desta lida, será empilhada numa pilha, isso porque 
# é preciso invertela a sequência coletada. Você ler no arquivo da primeira linha dele, no 
# entanto, você quer os últimos comandos. Aqui entra 'pilha', que empilha na ordem de leitura, 
# porém entrga os últimos valores(comportamento LIFO). Estas linhas lidas e empilhadas, serão 
# gravadas no mesmo arquivo, que será aberto agora em módo de gravação.
if __name__ == "__main__":

	with open(CAMINHO, "rt") as historico_leitura:
		# Pilha de linhas do arquivo com histórico.
		pilha = empilha_todas_suas_linhas(historico_leitura)
		print(f"Foram coletados {pilha.qsize()} linhas.")

	with open(CAMINHO, "wt") as historico_modificacao:
		despejas_no_arquivo(pilha, historico_modificacao)

"""
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
                                    Testes Unitários
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** 
"""
class EmpilhamentoDeLinhasDoBashHistory(TestCase):
	def runTest(self):
		# Colocando todos as linhas do arquivo de histórico numa 'pilha'.
		with open(CAMINHO, "rt") as arquivo:
			resultado = empilha_todas_suas_linhas(arquivo)
			total = 0

			while (not resultado.empty()):
				linha = resultado.get()
				print(linha)

				if total >= 20:
					break
				else:
					total += 1

class DespejaNoArquivo(TestCase):
	def setUp(self):
		self.diretorio = Path("./data/tests/reduz-os-comandos-digitados")

		# Cria diretório se não houver, e apenas continua se houver algum.
		try:
			makedirs(self.diretorio)
		except FileExistsError:
			print("Diretório já existe.")
		self.assertTrue(self.diretorio.exists())
		# Realiza uma cópia do arquivo original.
		self.historico = self.diretorio.joinpath("bash-history")

		if (not self.historico.exists()):
			CopyFile(CAMINHO, self.historico)
			self.assertTrue(self.historico.exists())
			print("Foi feita uma cópia de '.bash_history'.")
		else:
			print("Não precisa de cópia de '.bash_history', já existe.")

	def runTest(self):
		novo_arquivo = self.diretorio.joinpath("bash-history-modificado")

		with (
			open(self.historico, "rt") as historyfile, 
			open(novo_arquivo, "wt") as dumpsterfile
		):
			pilha = empilha_todas_suas_linhas(historyfile)
			print(f"Foram coletados {pilha.qsize()} linhas.")
			despejas_no_arquivo(pilha, dumpsterfile)