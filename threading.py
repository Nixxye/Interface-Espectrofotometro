import time
from tkinter import *

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure

import numpy as np

import threading

import multiprocessing

from random import randint

peer_pipe_rcv, peer_pipe_snd = multiprocessing.Pipe(duplex=False)
state_rcv, state_snd = multiprocessing.Pipe(duplex=False)

#Janela principal:
root = Tk()
root.wm_title("Teste")

#Menu:
menu_frame = Frame(root)
#menu_frame.pack_propagate(False)

#Gráfico:
main_frame = Frame(root)
#main_frame.pack_propagate(False)

fig = Figure(figsize=(5, 4), dpi=100)
t = np.arange(0, 3, .01)
ax = fig.add_subplot()
line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
ax.set_xlabel("valor")
ax.set_ylabel("índice")

canvas = FigureCanvasTkAgg(fig, master=main_frame)  # A tk.DrawingArea.
canvas.draw()

canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

def readData():
    global stop
    stop = False

    while not stop:
        data = randint(0, 100)
        peer_pipe_snd.send(data)
        time.sleep(0.1)

def updateScreen():
    global stop
    stop = False

    while not stop:
        data = peer_pipe_rcv.recv()
        y = 2 * np.sin(2 * np.pi * data * t) 
        line.set_data(t, y)
        canvas.draw()
        time.sleep(0.1)

def start():
    #Thread de leitura de dados:
    reading_data = threading.Thread(target=readData)
    reading_data.start()

    #Thread que atualiza o gráfico:
    draw = threading.Thread(target=updateScreen)
    draw.start()
    menu_frame.pack_forget()
    main_frame.pack()

def calibrate():
    print("Calibrando")

#Botões
calibration_btn = Button(menu_frame, text='Calibrar', command=calibrate)
calibration_btn.pack()
start_btn = Button(menu_frame, text='Começar', command=start)
start_btn.pack()

def main(): 
    global stop
    menu_frame.pack()
    #Loop principal da janela:
    root.mainloop()

    #Encerra o programa:
    stop = True
    #reading_data.join()
    #draw.join()

if __name__ == '__main__':
    main()