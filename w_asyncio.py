import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import multiprocessing
import asyncio
from random import randint


class App(tk.Tk):
    
    def __init__(self, loop, interval=1/120):
        super().__init__()

        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.tasks = []
        self.tasks.append(loop.create_task(self.updater(interval)))
        self.tasks.append(loop.create_task(self.updateScreen()))
        self.tasks.append(loop.create_task(self.readData()))

        # Pipes de comunicação:
        #self.peer_pipe_rcv, self.peer_pipe_snd = multiprocessing.Pipe(duplex=False)
        self.queue = asyncio.Queue()
        # Janela principal:
        self.geometry("800x600")
        self.wm_title("Teste com classes")

        # Frames:
        self.menu_frame = tk.Frame(self)
        self.main_frame = tk.Frame(self)
        self.calibration_frame = tk.Frame(self)

        # Gráfico principal:
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        self.ax.set_xlabel("valor")
        self.ax.set_ylabel("índice")
        self.ax.set_ylim(800)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Gráfico de calibração:
        self.calibration_fig = Figure(figsize=(5, 4), dpi=100)
        self.calibration_ax = self.calibration_fig.add_subplot()
        self.calibration_ax.set_xlabel("valor")
        self.calibration_ax.set_ylabel("índice")
        self.calibration_ax.set_ylim(800)
        self.calibration_canvas = FigureCanvasTkAgg(self.calibration_fig, master=self.calibration_frame)
        self.calibration_canvas.draw()
        self.calibration_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Botões:
        self.calibration_btn = tk.Button(self.menu_frame, text='Calibrar', command=self.calibrate)
        self.calibration_btn.pack()
        self.start_btn = tk.Button(self.menu_frame, text='Começar', command=self.start)
        self.start_btn.pack()
        self.save_btn = tk.Button(self.calibration_frame, text='Salvar', command=self.saveCalibration)
        self.save_btn.pack()

        self.current_frame = self.menu_frame
        self.current_frame.pack()

    def change_frame(self, new_frame):
        self.current_frame.pack_forget()
        self.current_frame = new_frame
        self.current_frame.pack()
    '''
    async def readData(self):
        while True:
            data = []
            for i in range(2094):
                data.append(randint(0, 800))
            self.peer_pipe_snd.send(data)
            await asyncio.sleep(0.2)

    async def updateScreen(self):
        while True:
            if self.peer_pipe_rcv.poll():
                try:
                    data = self.peer_pipe_rcv.recv()
                    if self.current_frame == self.main_frame:
                        self.ax.cla()
                        self.ax.plot(data)
                        self.canvas.draw()
                    elif self.current_frame == self.calibration_frame:
                        self.calibration_ax.cla()
                        self.calibration_ax.plot(data)
                        self.calibration_canvas.draw()
                    await asyncio.sleep(0.2)
                except EOFError:
                    return
    '''
    async def readData(self):
        while True:
            data = []
            for i in range(2094):
                data.append(randint(0, 800))
            #self.peer_pipe_snd.send(data)
            self.queue.put_nowait(data)
            await asyncio.sleep(0.2)

    async def updateScreen(self):
        while True:
            #if self.peer_pipe_rcv.poll():
            try:
                #data = self.peer_pipe_rcv.recv()
                data = self.queue.get_nowait()
                if self.current_frame == self.main_frame:
                    self.ax.cla()
                    self.ax.plot(data)
                    self.canvas.draw()
                elif self.current_frame == self.calibration_frame:
                    self.calibration_ax.cla()
                    self.calibration_ax.plot(data)
                    self.calibration_canvas.draw()
            except asyncio.QueueEmpty:
                pass
            await asyncio.sleep(0.2)

    def start(self):
        self.change_frame(self.main_frame)

    def saveCalibration(self):
        print("Saving Calibration")

    def calibrate(self):
        self.change_frame(self.calibration_frame)

    async def updater(self, interval):
        while True:
            self.update()
            await asyncio.sleep(interval)

    def close(self):
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()

loop = asyncio.get_event_loop()
app = App(loop)
loop.run_forever()
loop.close()
