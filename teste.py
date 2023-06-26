import asyncio
import multiprocessing
import keyboard
import tkinter

peer_pipe_rcv, peer_pipe_snd = multiprocessing.Pipe(duplex=False)
state_rcv, state_snd = multiprocessing.Pipe(duplex=False)

async def readData() -> None:
    while True:
        peer_pipe_snd.send(1)

async def updateScreen() -> None:
    while True:
        data = peer_pipe_rcv.recv()
        print(data)

async def getInputs() -> None:
    while True:
        if keyboard.is_pressed('space'):
            exit
        if keyboard.is_pressed('s'):
            saveData()

def saveData() -> None:
    print("Saved")

async def main():

    root_obj = tkinter.Tk()

    root_obj.title('Multicast Peer')

    root_obj.geometry("320x320")
    root_obj.resizable(False, False)

    button_join = tkinter.Button(
        root_obj, width=25, activebackground='gold', text="Join Group")
    button_join.pack(side='top', expand=1)

    button_request = tkinter.Button(
        root_obj, width=25, activebackground='gold', text="Acquire Lock")
    button_request.pack(side='top', expand=1)

    button_request = tkinter.Button(
        root_obj, width=25, activebackground='gold', text="Release Lock")
    button_request.pack(side='top', expand=1)

    button_exit = tkinter.Button(
        root_obj, width=25, activebackground='gold', text="Close Connection")
    button_exit.pack(side='top', expand=1)

    label_state = tkinter.Label(root_obj, bg='black', \
        fg='green', width=80, justify='center', pady=8, font=("Noto mono", 12))
    label_state.pack(side='top')

    await asyncio.gather(
        readData(),
        updateScreen(),
        getInputs()
        #run_tk(root_obj, 0.1, label_state)
    )

if __name__ == "__main__":
    asyncio.run(main())
