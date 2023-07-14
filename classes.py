import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import multiprocessing
import threading
from random import randint

class GUI():
    def __init__(self):
        # Pipes de comunicação:
        self.peer_pipe_rcv, self.peer_pipe_snd = multiprocessing.Pipe(duplex=False)
        self.state_rcv, self.state_snd = multiprocessing.Pipe(duplex=False)

        # Janela principal:
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.wm_title("Teste com classes")

        # Frames:
        self.menu_frame = tk.Frame(self.root)
        self.main_frame = tk.Frame(self.root)
        self.calibration_frame = tk.Frame(self.root)

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
        self.stop = False

    def change_frame(self, new_frame):
        self.current_frame.pack_forget()
        self.current_frame = new_frame
        self.current_frame.pack()

    def readData(self):
        while not self.stop:
            data = []
            for i in range(2094):
                data.append(randint(0, 800))
            self.peer_pipe_snd.send(data)
            time.sleep(0.1)

    def start(self):
        self.change_frame(self.main_frame)
        # Processo de leitura de dados:
        reading_data = threading.Thread(target=self.readData)
        reading_data.start()
        # Processo de atualização do gráfico:
        updating = threading.Thread(target=self.updateScreen)
        updating.start()

    def saveCalibration(self):
        print("Saving Calibration")

    def calibrate(self):
        self.change_frame(self.calibration_frame)
        # Processo de leitura de dados:
        reading_data = threading.Thread(target=self.readData)
        reading_data.daemon = True #Encerra as threads quando o programa finaliza
        reading_data.start()
        # Processo de atualização do gráfico:
        updating = threading.Thread(target=self.updateScreen)
        updating.daemon = True
        updating.start()

    def updateScreen(self):
        while not self.stop:
            if self.peer_pipe_rcv.poll():
                try:
                    data = self.peer_pipe_rcv.recv()
                    #self.ax.cla()
                    #self.ax.plot(data)
                    if self.current_frame == self.calibration_frame:
                        self.calibration_ax.cla()
                        self.calibration_ax.plot(data)
                        self.calibration_canvas.draw()
                    else:
                        self.ax.cla()
                        self.ax.plot(data)
                        self.canvas.draw()
                    time.sleep(0.1)
                except EOFError:
                    return

    def run(self):
        self.current_frame.pack()
        self.root.mainloop()
        self.stop = True

if __name__ == '__main__':
    a = GUI()
    a.run()
