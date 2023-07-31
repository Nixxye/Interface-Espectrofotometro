import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
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
        self.queue = asyncio.Queue()

        # Dados da calibração:
        self.static_data = []
        self.load_data()

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

        # Adicionar o gráfico translúcido como uma segunda curva no mesmo subplot:
        self.ax_background = self.ax.twinx()  # Cria um novo eixo compartilhando o mesmo eixo x
        self.ax_background.set_ylabel("índice")  # Ajusta o label do eixo y
        self.ax_background.set_ylim(800)  # Define o limite do eixo y
        self.ax_background.plot([], [], alpha=0.5)  # Plot inicial vazio com transparência (alpha=0.5)


        # Botões:
        self.abs_btn = tk.Button(self.calibration_frame, text='Absorbancia')
        self.abs_btn.pack(side=tk.TOP)
        self.tmt_btn = tk.Button(self.calibration_frame, text='Transmitancia')
        self.tmt_btn.pack(side=tk.TOP)
        self.smp_btn = tk.Button(self.calibration_frame, text='Valores lidos')
        self.smp_btn.pack(side=tk.TOP)

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

        self.save_btn = tk.Button(self.calibration_frame, text='Salvar', command=self.start_save_calibration_task)
        self.save_btn.pack()

        self.current_frame = self.menu_frame
        self.current_frame.pack()

    def load_data(self):
        try:
            with open("calibration_data.txt", 'r') as file:
                lines = file.readlines()
                self.static_data = [float(line.strip()) for line in lines]
        except FileNotFoundError:
            print("Arquivo de calibração não encontrado. Os dados do gráfico translúcido serão vazios.")


    def change_frame(self, new_frame):
        self.current_frame.pack_forget()
        self.current_frame = new_frame
        self.current_frame.pack()

    async def readData(self):
        while True:
            data = []
            for i in range(2094):
                data.append(randint(0, 800))
            self.queue.put_nowait(data)
            await asyncio.sleep(0.2)

    async def updateScreen(self):
        while True:
            try:
                data = self.queue.get_nowait()
                # Switch case
                if self.current_frame == self.main_frame:
                    self.ax.cla()
                    self.ax.plot(data)
                    self.canvas.draw()

                    # Gráfico de fundo:
                    if self.static_data:
                        self.ax_background.cla()  # Limpa o gráfico de fundo
                        self.ax_background.plot(self.static_data, alpha=0.5, color='red')  # Plota os dados de calibração
                        self.canvas.draw()  # Atualiza o canvas para exibir o gráfico translúcido

                elif self.current_frame == self.calibration_frame:
                    self.calibration_ax.cla()
                    self.calibration_ax.plot(data)
                    self.calibration_canvas.draw()
            except asyncio.QueueEmpty:
                pass
            await asyncio.sleep(0.2)

    def start(self):
        self.change_frame(self.main_frame)

    def start_save_calibration_task(self):
        # Iniciar uma task para a função saveCalibration usando o loop de eventos asyncio
        self.loop.create_task(self.saveCalibration())

    async def saveCalibration(self):

        data = await self.queue.get()

        with open("calibration_data.txt", 'w') as file:
            for number in data:
                file.write(str(number) + '\n')

        self.load_data()
        
        print("Calibration data saved to calibration_data.txt")

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
