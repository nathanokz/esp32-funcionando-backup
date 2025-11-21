import socket #bilbioteca utilizada para comunicação entre computadores

host = '192.168.1.105' #ip do servidor
porta = 5000 #porta do servidor 

clientes = {} #cria um dicionario de clientes

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #cria um socket udp
server.bind((host, porta)) #conecta o socket udp no host e porta especificados

print('aguardando mensagem...') #printa enquanto espera uma mensagem

while True: #inicia o loop
    data, ender = server.recvfrom(20000) #recebe mensagens de ate 1024 bytes 
    mensagem = data.decode().strip() #decodifica a mensagem recebida bytes -> string

    if ender not in clientes: #verifica se o endereço do cliente ai não esta no dicionario
        clientes[ender] = mensagem #adiciona o cliente ao dicionario
        print(f"novo cliente: {mensagem} - {ender}") #printa que um cliente se conectou
        for cliente_ender in clientes: #percorre todos os clientes do dicionario
            if cliente_ender != ender: #evita mandar a mensagem de entrada para o cliente para o proprio cliente
                server.sendto(f"servidor: {mensagem} entrou no chat.".encode(), cliente_ender) #envia uma mensagem de boas vindas
        continue #espera pela proxima mensagem

    nome = clientes[ender] #pega o nome do cliente do dicionario
    mensagem_completa = f"{nome}: {mensagem}" #formata a mensagem completa do cliente
    print(mensagem_completa) #printa a mensagem completa
    for cliente_ender in clientes: #percorre todos os clientes conectados
        if cliente_ender != ender: #evita mandar a mensagem de entrada para o cliente para o proprio cliente
            server.sendto(mensagem_completa.encode(), cliente_ender) #envia a mensagem para os clientes
