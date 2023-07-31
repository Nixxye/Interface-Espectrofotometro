import tkinter
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

import asyncio

import multiprocessing

peer_pipe_rcv, peer_pipe_snd = multiprocessing.Pipe(duplex=False)
state_rcv, state_snd = multiprocessing.Pipe(duplex=False)

'''
peer_pipe_rcv, peer_pipe_snd = multiprocessing.Pipe(duplex=False)
state_rcv, state_snd = multiprocessing.Pipe(duplex=False)


'''

async def func1():
    print("FUNC1")

async def func2():
    print("FUNC2")

async def run_tk(root, interval=0.1, label_state: tkinter.Label = None) -> None:
    try:
        while True:
            if state_rcv.poll():
                try:
                    new_state = state_rcv.recv()
                except EOFError:
                    return
                except:
                    raise

                #label_state.config(text=new_state)

            root.update()
            await asyncio.sleep(interval)
    except:
        print("Error")
    finally:
        return


async def main():
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")

    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    ax = fig.add_subplot()
    line, = ax.plot(t, 2 * np.sin(2 * np.pi * t))
    ax.set_xlabel("time [s]")
    ax.set_ylabel("f(t)")

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()

    canvas.mpl_connect(
        "key_press_event", lambda event: print(f"you pressed {event.key}"))
    canvas.mpl_connect("key_press_event", key_press_handler)
    '''
    root_obj = tkinter.Tk()

    root_obj.title('Multicast Peer')

    root_obj.geometry("320x320")
    root_obj.resizable(False, False)

    button_join = tkinter.Button(
        root_obj, width=25, activebackground='gold', text="Join Group", command=send_command_join)
    button_join.pack(side='top', expand=1)

    button_request = tkinter.Button(
        root_obj, width=25, activebackground='gold', text="Acquire Lock", command=send_command_acquire_lock)
    button_request.pack(side='top', expand=1)

    button_request = tkinter.Button(
        root_obj, width=25, activebackground='gold', text="Release Lock", command=send_command_release_lock)
    button_request.pack(side='top', expand=1)

    button_exit = tkinter.Button(
        root_obj, width=25, activebackground='gold', text="Close Connection", command=send_command_exit)
    button_exit.pack(side='top', expand=1)

    label_state = tkinter.Label(root_obj, bg='black', \
        fg='green', width=80, justify='center', pady=8, font=("Noto mono", 12))
    label_state.pack(side='top')
    '''
    await asyncio.gather(
        func1(),
        func2(),
        run_tk(root, 0.1)
    )

if __name__ == '__main__':
    asyncio.run(main())