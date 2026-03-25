''' 
   Usando o máximo de CPU da máquina. O algoritmo consiste em simples
 contagem. O objetivo aqui é usar todo o potencial dela, e para isso, simples
 execuções de contagem em múltiplas threads realizam isso.
'''
import time, multiprocessing, os, threading

def contagem_infinita():
    contagem = 0
    INICIO  = time.time()
    final = INICIO
    ENV = os.getenv("TEMPO_DA_CONTAGEM")
    if ENV is not None:
        LIMITE = int(ENV) 
    else:
        LIMITE = 20 # Alguns segundos inicialmente.
    
    while (final - INICIO) < LIMITE :
        final = time.time()
        contagem += 1

def info_geral():
    global pool
    
    processos = pool
    contagem = 1
    
    while True:
        quantia = os.process_cpu_count()
        print(f"{quantia} CPUs estão sendo usados.")
        time.sleep(2.3)
        
        if contagem % 3 == 0 and len(processos) > 0:
            for item in processos:
                nome = item.name 
                rodando = item.is_alive()
                print(f"\t{nome} está rodando? {rodando}")
        contagem += 1
        
        if not (any(map(lambda obj: obj.is_alive(), pool))):
            print(f"Nenhuma contagem mais ativa!")
            break

if __name__ == "__main__":
    TOTAL_DE_CPUs = os.cpu_count()
    pool = []
    visualizacao = threading.Thread(target=info_geral)

    visualizacao.start()
    print(f"Há {os.cpu_count()} processadores lógicos no total.")

    for k in range(TOTAL_DE_CPUs):
        processo = multiprocessing.Process(
            target=contagem_infinita, 
            name=f"Thread[{k + 1}]"
        )
        pool.append(processo)

    for fio in pool: 
        print(f"{fio.name} foi iniciada.")
        fio.start()
        
    for fio in pool:
        fio.join()
        print(f"{fio.name} foi encerrada.")
    visualizacao.join()