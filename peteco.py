import asyncio
import tkinter
import multiprocessing
from random import randint

# Criação dos pipes para comunicação entre processos
peer_pipe_rcv, peer_pipe_snd = multiprocessing.Pipe(duplex=False)

# Função para leitura dos dados
async def readData():
    while True:
        # Envia dados através do peer_pipe_snd
        peer_pipe_snd.send(randint(0, 100))
        await asyncio.sleep(0.2)

# Função para atualização da tela
async def updateScreen():
    while True:
        if peer_pipe_rcv.poll():
            try:
                read = peer_pipe_rcv.recv()
            except EOFError:
                return
            print(read)
        await asyncio.sleep(0.1)


# Função principal
async def main():
    # Criação das tarefas assíncronas
    task_read = asyncio.create_task(readData())
    task_update = asyncio.create_task(updateScreen())

    # Aguarda o término das tarefas
    await asyncio.gather(task_read, task_update)

if __name__ == '__main__':
    # Execução do loop de eventos do asyncio
    asyncio.run(main())
