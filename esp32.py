import network
import socket
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import _thread

i2c = I2C(0, scl=Pin(4), sda=Pin(5))
oled = SSD1306_I2C(128, 64, i2c)

rede = network.WLAN(network.STA_IF)
rede.active(True)
rede.connect('Baco', 'maicon142020')

while not rede.isconnected():
    print('conectando ao wifi...')
    time.sleep(1)
print('conectado!')

host = '192.168.1.105'
porta = 9999

metodoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
metodoSocket.connect((host, porta))
print('conectado ao servidor tcp')

# Função para receber mensagens do servidor
def receber_mensagens():
    while True:
        try:
            data = metodoSocket.recv(1024)
            if not data:
                continue 
            mensagem = data.decode().strip().lower()
            print('mensagem recebida:', mensagem)
            
            if mensagem == '/led_on':
                oled.fill(1)
                oled.show()
                print("display ligado")
                
            elif mensagem == '/led_off':
                oled.fill(0)
                oled.show()
                print("display desligado")
                
        except:
            break

_thread.start_new_thread(receber_mensagens, ())

while True:
    time.sleep(1)  

