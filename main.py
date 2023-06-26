from math import isclose
from tkinter import *
from tkinter import ttk
from turtle import bgcolor

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


import multiprocessing

peer_pipe_rcv, peer_pipe_snd = multiprocessing.Pipe(duplex=False)
state_rcv, state_snd = multiprocessing.Pipe(duplex=False)

def Func_1() -> None:
    print("func_1")
    peer_pipe_snd.send('FUNC_1')

def Func_2() -> None:
    print("func_2")
    peer_pipe_snd.send('FUNC_2')

def Update_Screen() -> bool:
    try:
        root.update()
    except:
        return False
    return True

root = Tk()

fig, ax = plt.subplots()

canvas = FigureCanvasTkAgg(fig, master=root)  
canvas.get_tk_widget().grid(column=0,row=0)

vet = []

for i in range (-10, 10):
    vet.append(i)

ax.plot(vet, vet)

root.configure(bg='white')

root.title('Projeto_Software')

#root.geometry("640x480")

root.resizable(False, False)

ttk.Label(root, text="Hello World!").grid(column=1,row=0)

ttk.Button(root,  command=Func_1, text="Função 1")\
    .grid(column=1,row=1)

ttk.Button(root, text="Função 2", command=Func_2).grid(column=1,row=2)

ttk.Button(root, text="Quit", command=root.destroy).grid(column=1,row=3)

def main() -> int:
    flag = True
    while flag:
        flag = Update_Screen()

main()