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
porta = 5000

metodoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
metodoSocket.connect((host, porta))
print('conectado ao servidor tcp')

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
            
            elif mensagem == '/enviar_dados':
                while True:
                    mensagemesp = '{"type": "data", "from": "esp32", "payload": {"temp": "25.3", "hum": "60}}"'
                    metodoSocket.send(mensagemesp.encode())
                    time.sleep(2)
                
        except:
            break

_thread.start_new_thread(receber_mensagens, ())

for i in range(0,5):
    oled.text('loading.',24,28)
    oled.fill_rect(25,40,26,8,1)
    oled.show()
    time.sleep(0.3)
    oled.fill(0)
    
    oled.text('loading..',24,28)
    oled.fill_rect(25,40,51,8,1)
    oled.show()
    time.sleep(0.3)
    oled.fill(0)
    
    oled.text('loading...',24,28)
    oled.fill_rect(25,40,76,8,1)
    oled.show()
    time.sleep(0.3)
    oled.fill(0)
    
for j in range(0,3):
    oled.text('preparando dados.',0,28)
    oled.show()
    time.sleep(0.5)
    oled.fill(0)

    oled.text('preparando dados..',0,28)
    oled.show()
    time.sleep(0.5)
    oled.fill(0)

    oled.text('preparando dados...',0,28)
    oled.show()
    time.sleep(0.5)
    oled.fill(0)

while True:
    oled.text('esp32_client.ino',0,0)
    oled.text('{"type": "data",',0,10)
    oled.text('"from": "esp32",',0,20)
    oled.text('"payload":',0,30)
    oled.text('{"temp": 25.3,',0,40)
    oled.text('"hum": 60}}',0,50)
    oled.show()
    time.sleep(1)  
