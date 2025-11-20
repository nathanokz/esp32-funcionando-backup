import socket
import threading

host = '192.168.1.105'  #  do servidor
porta = 9999             # Porta do servidor

clientes = []  # Lista de clientes conectados

# Função que trata cada cliente individual
def cliente(conn, ender):
    print(f"cliente conectado: {ender}")
    while True:
        try:
            data = conn.recv(1024)  # Recebe dados do cliente
            if not data:
                break  # Cliente desconectou
            
            mensagem = data.decode().strip()
            print(f"mensagem recebida de {mensagem}")

            # Envia a mensagem para todos os clientes conectados
            for cliente in clientes:
                try:
                    cliente.sendall(data)
                except:
                    pass

        except:
            break

    print(f"cliente desconectado: {ender}")
    conn.close()
    if conn in clientes:
        clientes.remove(conn)

# Criação do socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, porta))
server_socket.listen(5)  # Aceita até 5 conexões simultâneas

print('aguardando conexão...')

# Loop principal para aceitar clientes
while True:
    conn, ender = server_socket.accept()
    clientes.append(conn)
    thread = threading.Thread(target=cliente, args=(conn, ender))
    thread.start()
