from math import isclose
from tkinter import *
from tkinter import ttk
import asyncio
from random import randint
from turtle import bgcolor

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import multiprocessing

Exit = False

# Criação dos pipes para comunicação entre processos
state_rcv, state_snd = multiprocessing.Pipe(duplex=False)
peer_pipe_rcv, peer_pipe_snd = multiprocessing.Pipe(duplex=False)

# Função para leitura dos dados
async def readData():
    while True:
        
        vet = []
        
        for i in range(2094):
            vet.append(0)
        for i in range(2094):
            vet[i] = randint(0, 100)

        # Envia dados através do peer_pipe_snd
        peer_pipe_snd.send(vet)

        await asyncio.sleep(0.2)

async def UpdateScreen(root):
    while True:
        try:
            root.update()
        except:
            state_snd.send('Close')
            await asyncio.sleep(0.3)
            
def Close(root):
    peer_pipe_rcv.close()
    peer_pipe_snd.close()
    state_rcv.close()
    state_snd.close()



def CloseCommand():
    state_snd.send('Close')


# Função para atualização da tela
async def UpdateGraph(root, ax, canvas):
    while True:
        if peer_pipe_rcv.poll():
            try:
                # Tenta ler dados através do peer_pipe_rcv
                read = peer_pipe_rcv.recv()
            except EOFError:
                return
    
        ax.cla()
        ax.plot(read)
        #seg fault acontece aqui
        canvas.draw()
        #-----------------------
        await asyncio.sleep(0.1)

def Func_1() -> None:
    print("func_1")
    state_snd.send('FUNC_1')

def Func_2() -> None:
    print("func_2")
    state_snd.send('FUNC_2')

async def main() -> int:
    root = Tk()

    fig, ax = plt.subplots()

    canvas = FigureCanvasTkAgg(fig, master=root)  
    canvas.get_tk_widget().grid(column=0,row=0)

    root.configure(bg='white')

    root.title('Projeto_Software')

    #root.geometry("640x480")

    root.resizable(False, False)

    ttk.Label(root, text="Hello World!").grid(column=1,row=0)

    ttk.Button(root,  command=Func_1, text="Função 1")\
        .grid(column=1,row=1)

    ttk.Button(root, text="Função 2", command=Func_2).grid(column=1,row=2)

    ttk.Button(root, text="Quit", command=CloseCommand).grid(column=1,row=3)

    # Criação das tarefas assíncronas
    task_read = asyncio.create_task(readData())
    task_update = asyncio.create_task(UpdateGraph(root, ax, canvas))
    task_window = asyncio.create_task(UpdateScreen(root))

    await asyncio.gather(
        task_read, 
        task_update,
        task_window
        )
    


if __name__ == '__main__':
    # Execução do loop de eventos do asyncio
    asyncio.run(main())    