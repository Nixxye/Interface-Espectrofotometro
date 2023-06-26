#Ler os dados e enviar para um pipe
#Mostrar na tela dos dados
#Imprimir os resultados obtidos
#Receber os inputs 

#3 processos: Ler os dados e ler os inputs e mostrar os dados na tela
import asyncio
import multiprocessing

# Função assíncrona que recebe mensagens do pipe
#Draw:
async def updateScreen(pipe):
    while True:
        message = pipe.recv()  # Recebe mensagem do pipe
        print(f"Receiver received: {message}")

# Função assíncrona que envia mensagens para o pipe
#Observer:
async def getInputs(pipe):
    for i in range(5):
        message = f"Message {i}"
        pipe.send(message)  # Envia mensagem para o pipe
        await asyncio.sleep(1)  # Aguarda 1 segundo entre as mensagens

# Função principal
def main():
    # Cria o pipe de comunicação
    parent_pipe, child_pipe = multiprocessing.Pipe()

    # Cria um processo para executar a função receiver
    receiver_process = multiprocessing.Process(target=receiver, args=(child_pipe,))
    receiver_process.start()

    # Cria uma task assíncrona para executar a função sender
    loop = asyncio.get_event_loop()
    sender_task = loop.create_task(sender(parent_pipe))

    # Executa o loop de eventos assíncronos até que a task seja concluída
    loop.run_until_complete(sender_task)

    # Encerra o processo do receiver
    receiver_process.terminate()

if __name__ == "__main__":
    main()

#Print:
#Read:
