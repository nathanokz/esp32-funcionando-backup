import socket #bilbioteca utilizada para comunicação entre computadores
import threading #biblioteca utilizada para executar multiplas tarefas ao mesmo tempo
import time

host = '192.168.1.105' #ip do servidor que o cliente vai se conectar
porta = 5000 #porta do servidor que o cliente vai se conectar

nome = "cliente_udp" #nome padrão do cliente

metodoSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #cria um socket tcp
metodoSocket.sendto(nome.encode(), (host, porta)) #conecta o socket tcp no host e porta especificados

def receber(): #serve para receber mensagens dos servidor
    while True: #cria um loop infinito
        try: #tenta realizar o bloco
            data, ender = metodoSocket.recvfrom(20000) #recebe mensagens de ate 1024 bytes
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
        metodoSocket.sendto(nome.encode(), (host, porta)) #envia a mensagem codificada para oservidor

    elif mensagem.startswith('/bench'): #se a mensagem começa com /bench
        try: #tenta executar o bloco
            tamanho = int(mensagem.split(' ')[1]) #pega o valor de bench e converte para inteiro
            print(f'enviando {tamanho} bytes...') #mostra quantos bytes esta enviando
            dados = b'-' * tamanho #cria um bloco de dados com o tamanho inserido
            inicio = time.time() #marca o inicio 
            metodoSocket.sendto(dados, (host, porta)) #envia os dados
            fim = time.time() #marca o fim
            print(f'envio conculido levou: {fim-inicio} segundos') #mostra quanto tempo levou
        except: #se nao conseguir executar o bloco cai aqui
            print('erro ao executar bench') #exibe erro
            continue #tenta novamente

    elif mensagem == "/sair": #se a mensagem for igual a /sair
        metodoSocket.sendto(f"{nome} saiu do servidor".encode(), (host, porta)) #envia a mensagem para o servidor dizendo que o cliente saiu
        break #finaliza o loop saindo do servidor

    else: #se não
        metodoSocket.sendto(f"{nome}: {mensagem}".encode(), (host, porta)) #envia a mensagem para o servidor

metodoSocket.close() #encerra o socket tcp
print("fechando conexão") #sai do servidor
