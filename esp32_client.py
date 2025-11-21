import network #biblioteca para controlar a rede
import socket #bilbioteca utilizada para comunicação entre computadores
import time #biblioteca de funções relacionadas a tempo
from machine import Pin, I2C #biblioteca para controlar a esp
from ssd1306 import SSD1306_I2C #biblioteca para display oled
import _thread #biblioteca utilizada para executar multiplas tarefas ao mesmo tempo

i2c = I2C(0, scl=Pin(4), sda=Pin(5)) #cria uma interface no barramento
oled = SSD1306_I2C(128, 64, i2c) #inicia o display oled

rede = network.WLAN(network.STA_IF) #cria uma interface de rede
rede.active(True) #ativa a interface
rede.connect('Baco', 'maicon142020') #tenta conectar com nome e senha

while not rede.isconnected(): #enquanto a rede não se conectar
    print('conectando ao wifi...') #printa conectando...
    time.sleep(1) #espera 1 segundo para printar novamente
print('conectado!') #quando conectar printa conectado

host = '192.168.1.105' #ip do servidor
porta = 5000 #porta do servidor

metodoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #cria um socket tcp
metodoSocket.connect((host, porta)) #conecta o socket tcp no host e porta especificados
print('conectado ao servidor tcp') #quando conectar printa conectado

def receber_mensagens(): #serve para receber mensagens dos servidor
    while True: #cria um loop infinito
        try: #tenta realizar o bloco
            data = metodoSocket.recv(20000) #recebe mensagens de ate 20000 bytes 
            if not data: #se não receber nada
                continue #tenta novamente
            mensagem = data.decode().strip().lower() #decodifica
            print('mensagem recebida:', mensagem) #printa a mensagem ja decodificada
            
            if mensagem == '/led_on': #se a mensagem for /led_on
                oled.fill(1) #liga a tela
                oled.show() #mostra a tela ligada
                print("display ligado") #printa display ligado no terminal
                
            elif mensagem == '/led_off': #se a mensagem for /led_off
                oled.fill(0) #desliga a tela
                oled.show() #mostra a tela desligada
                print("display desligado") #printa display desligado
            
            elif mensagem == '/enviar_dados': #se a mensagem for /enviar_dados
                while True: #inicia um loop
                    mensagemesp = '{"type": "data", "from": "esp32", "payload": {"temp": "25.3", "hum": "60}}"' #cria os dados
                    metodoSocket.send(mensagemesp.encode()) #envia os dados para o servidor
                    time.sleep(2) #espera 2 segundos para enviar novamente
                
        except: #se não conseguir executar o bloco
            break #finaliza o loop

_thread.start_new_thread(receber_mensagens, ()) #inicia um thread em receber_mensagens

for i in range(0,5): #faz um loop que roda 5 vezes
    oled.text('loading.',24,28) #cria loading na tela
    oled.fill_rect(25,40,26,8,1) #cria um retangulo na tela
    oled.show() #mostra ambos na tela 
    time.sleep(0.3) #espera 0.3 segundos
    oled.fill(0) #apaga a tela
    
    oled.text('loading..',24,28) #cria loading na tela
    oled.fill_rect(25,40,51,8,1) #cria um retangulo na tela
    oled.show() #mostra ambos na tela 
    time.sleep(0.3) #espera 0.3 segundos
    oled.fill(0) #apaga a tela
    
    oled.text('loading...',24,28) #cria loading na tela
    oled.fill_rect(25,40,76,8,1) #cria um retangulo na tela
    oled.show() #mostra ambos na tela 
    time.sleep(0.3) #espera 0.3 segundos
    oled.fill(0) #apaga a tela
    
for j in range(0,3): #cria um loop que roda 3 vezes
    oled.text('preparando dados.',0,28) #cria um preparando dados na tela
    oled.show() #mostra na tela
    time.sleep(0.5) #espera 0.5 segundos
    oled.fill(0) #apaga a tela

    oled.text('preparando dados..',0,28) #cria um preparando dados na tela
    oled.show() #mostra na tela
    time.sleep(0.5) #espera 0.5 segundos
    oled.fill(0) #apaga a tela

    oled.text('preparando dados...',0,28) #cria um preparando dados na tela
    oled.show() #mostra na tela
    time.sleep(0.5) #espera 0.5 segundos
    oled.fill(0) #apaga a tela

while True: #cria um loop
    oled.text('esp32_client.ino',0,0) #escreve na tela
    oled.text('{"type": "data",',0,10) #escreve na tela
    oled.text('"from": "esp32",',0,20) #escreve na tela
    oled.text('"payload":',0,30) #escreve na tela
    oled.text('{"temp": 25.3,',0,40) #escreve na tela
    oled.text('"hum": 60}}',0,50) #escreve na tela
    oled.show() #mostra na tela
    time.sleep(1) #espera 1 segundo para fazer novamente
