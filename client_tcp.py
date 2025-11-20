import socket #bilbioteca utilizada para comunicação entre computadores
import threading #biblioteca utilizada para executar multiplas tarefas ao mesmo tempo

host = '192.168.1.105' #ip do servidor que o cliente vai se conectar
porta = 9999 #porta do servidor que o cliente vai se conectar

metodoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria um socket tcp
metodoSocket.connect((host, porta)) #conecta o socket tcp no host e porta especificados

nome = 'client_tcp'

def receber(): #serve para receber mensagens dos servidor
    while True: #cria um loop infinito
        try: #tenta realizar o bloco
            data = metodoSocket.recv(1024) #recebe mensagens de ate 1024 bytes 
            if not data: #se não receber nada
                print("servidor desconectado") #desconecta do servidor
                break #finaliza o loop
            print(data.decode()) #printa a mensagem recebida já decodificada byte -> string

        except: #se não conseguir realizar o bloco cai aqui
            break #finaliza o codigo

thread = threading.Thread(target=receber) #cria a thread que vai executar a função receber
thread.daemon = True # define a thread como daemon que vai parar automaticamente quando o programa principal terminar
thread.start() #inicia a thread

while True: #inicia o loop
    mensagem = input('digite uma mensagem: ') #pede para digitar uma mensagem

    if mensagem.startswith("/nick "): #verifica se a mensagem começa com /nick
        nome = mensagem.split(" ", 1)[1] #atualiza o nome do cliente para o nick inserido
        print("nome alterado para: ", nome) #mostra para qual nick o nome foi alterado

    elif mensagem == "/sair": #se a mensagem for igual a /sair
        metodoSocket.send(f"{nome} saiu do servidor".encode()) #envia a mensagem para o servidor dizendo que o cliente saiu
        break #finaliza o loop saindo do servidor

    elif mensagem == "/led_on" or mensagem == "/led_off" or mensagem == '/enviar_dados':
        metodoSocket.sendall(mensagem.encode()) #envia a mensagem para o servidor

    else: #se não
        metodoSocket.send(f"{nome}: {mensagem}".encode()) #envia a mensagem para o servidor

metodoSocket.close() #encerra o socket tcp
print("fechando conexão") #sai do servidor
