import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

import asyncio

import multiprocessing


class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())
        await self.window.show();


class Window(tk.Tk):
    def __init__(self, loop):
        self.loop = loop
        self.root = tk.Tk()
        #self.animation = "░▒▒▒▒▒"
        #self.label = tk.Label(text="")
        #self.label.grid(row=0, columnspan=2, padx=(8, 8), pady=(16, 0))
        #self.progressbar = ttk.Progressbar(length=280)
        #self.progressbar.grid(row=1, columnspan=2, padx=(8, 8), pady=(16, 0))
        #button_block = tk.Button(text="Calculate Sync", width=10, command=self.calculate_sync)
        #button_block.grid(row=2, column=0, sticky=tk.W, padx=8, pady=8)
        button_non_block = tk.Button(text="Teste", width=10, command=lambda: self.loop.create_task(self.calculate_async()))
        button_non_block.grid(row=2, column=1, sticky=tk.W, padx=8, pady=8)
        
        peer_pipe_rcv, peer_pipe_snd = multiprocessing.Pipe(duplex=False)
        state_rcv, state_snd = multiprocessing.Pipe(duplex=False)

        root = tk.Tk()
        root.wm_title("Embedding in Tk")

        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        ax = fig.add_subplot()
        line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
        ax.set_xlabel("time [s]")
        ax.set_ylabel("f(t)")

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()

        # pack_toolbar=False will make it easier to use a layout manager later on.
        #toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
        #toolbar.update()

        canvas.mpl_connect(
            "key_press_event", lambda event: print(f"you pressed {event.key}"))
        canvas.mpl_connect("key_press_event", key_press_handler)
  
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
   
    async def show(self):
        while True:
            #self.label["text"] = self.animation
            #self.animation = self.animation[1:] + self.animation[0]
            self.root.update()
            await asyncio.sleep(.1)

            
    async def calculate_async(self):
        max = 3000000
        for i in range(1, max):
            #self.progressbar["value"] = i / max * 100
            if i % 1000 == 0:
                await asyncio.sleep(0)

asyncio.run(App().exec())