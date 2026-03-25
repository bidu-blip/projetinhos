'''
   Transferência de códigos da máquina Windows para o servidor Linux. O programa
 consiste nos seguintes passos: faz um arquivo compilado com todos arquivos do atual
 diretório; conecta-se ao servidor remoto; envia tal compilado prá ele; e remove o
 que foi enviado aqui; então fecha a coneção.
'''

from tarfile import TarFile
from pathlib import (Path)
from subprocess import (Popen)
from ftplib import (FTP)

# Primeira parte: Faz um compilado de todos os códigos no atual repositório do Windows.
# Ele será salva como 'todo-meu-codigo' dentro do diretório 'data'.
DESTINO = Path("data/todo-meu-código.tar")


with TarFile(name=DESTINO, mode="w") as arquivo:
    for caminho in Path().iterdir():
        arquivo.add(caminho)

servidor = FTP(
    user="root",
    passwd="SenaiEAD",
    source_address=("172.16.17.118", 21)
)
print(servidor)
servidor.connect(host=", port=21)
servidor.close()