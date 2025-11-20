import socket #bilbioteca utilizada para comunicação entre computadores
import threading #biblioteca utilizada para executar multiplas tarefas ao mesmo tempo

host = '192.168.1.105' #ip do servidor
porta = 5000 #porta do servidor 

clientes = [] #lista de clientes conectados

def cliente(conn, ender): #função para comunicação com o cliente
    print(f"cliente conectado: {ender}") #mostra o cliente que se conectou
    while True: #inicia o loop
        try: #tenta realizar o bloco
            data = conn.recv(1024) #recebe mensagens de ate 1024 bytes 
            if not data: #se não receber nada
                break #finaliza o loop
            mensagem = data.decode().strip() #decodifica a mensagem do cliente byte -> string
            print(f"mensagem recebida de {mensagem}") #exibe a mensagem decodificada
            #envia a mensagem para todos os clientes conectados
            for cliente in clientes: #para todo cliente que estiver na lista de clientes
                try: #tenta executar o bloco
                    cliente.sendall(data) #envia a mensagem para todos os clientes
                except: #se não conseguir realizar o bloco cai aqui
                    pass #continua o código

        except: #se não conseguir realizar o bloco acima cai aqui
            break #finaliza o codigo

    print(f"cliente desconectado: {ender}")  #mostra caso o cliente tenha se desconectado
    conn.close() #fecha a conexão
    if conn in clientes: #se estiver na lista de clientes 
        clientes.remove(conn) #remove o cliente da lista de clientes

# Criação do socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria um socket tcp
server_socket.bind((host, porta)) #conecta o socket tcp no host e porta especificados
server_socket.listen(5)  #aceita até 5 conexões simultâneas

print('aguardando conexão...') #printa enquando aguarda alguem se conectar

while True: #inicia o loop
    conn, ender = server_socket.accept() #aceita a conexão tcp do cliente
    clientes.append(conn) #acumula o cliente dentro da lista clientes
    thread = threading.Thread(target=cliente, args=(conn, ender)) #cria a thread que vai executar a função cliente
    thread.start() #inicia a thread
