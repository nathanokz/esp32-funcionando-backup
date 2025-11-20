import socket #bilbioteca utilizada para comunicação entre computadores
import threading #biblioteca utilizada para executar multiplas tarefas ao mesmo tempo

host = '192.168.1.109' #ip do servidor que o cliente vai se conectar
porta = 5000 #porta do servidor que o cliente vai se conectar

nome = "cliente_udp" #nome padrão do cliente

cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #cria um socket tcp
cliente.sendto(nome.encode(), (host, porta)) #conecta o socket tcp no host e porta especificados

def receber(): #serve para receber mensagens dos servidor
    while True: #cria um loop infinito
        try: #tenta realizar o bloco
            data, ender = cliente.recvfrom(1024) #recebe mensagens de ate 1024 bytes
            print(data.decode()) #printa a mensagem recebida já decodificada byte -> string 
        
        except: #se não conseguir realizar o bloco cai aqui
            break #finaliza o loop

thread = threading.Thread(target=receber) #cria a thread que vai executar a função receber
thread.daemon = True # define a thread como daemon que vai parar automaticamente quando o programa principal terminar
thread.start() #inicia a thread

while True: #inicia o loop
    mensagem = input('digite uma mensagem: ') #pede para digitar uma mensagem

    if mensagem.startswith("/nick "): #verifica se a mensagem começa com /nick
        nome = mensagem.split(" ", 1)[1] #atualiza o nome do cliente para o nick inserido
        print("nome alterado para: ", nome) #mostra para qual nick o nome foi alterado
        cliente.sendto(nome.encode(), (host, porta)) #envia a mensagem codificada para oservidor

    elif mensagem == "/sair": #se a mensagem for igual a /sair
        cliente.sendto(f"{nome} saiu do servidor".encode(), (host, porta)) #envia a mensagem para o servidor dizendo que o cliente saiu
        break #finaliza o loop saindo do servidor

    else: #se não
        cliente.sendto(f"{nome}: {mensagem}".encode(), (host, porta)) #envia a mensagem para o servidor

cliente.close() #encerra o socket tcp
print("fechando conexão") #sai do servidor
