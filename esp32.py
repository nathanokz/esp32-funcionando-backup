import network
import socket
import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import _thread

# Configura o OLED
i2c = I2C(0, scl=Pin(4), sda=Pin(5))
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Aguardando...", 0, 0)
oled.show()

# Conecta ao Wi-Fi
rede = network.WLAN(network.STA_IF)
rede.active(True)
rede.connect('Baco', 'maicon142020')

while not rede.isconnected():
    print('Conectando ao Wi-Fi...')
    time.sleep(1)

print('Wi-Fi conectado! IP:', rede.ifconfig()[0])
oled.fill(0)
oled.text("Wi-Fi Conectado", 0, 0)
oled.show()

# Conecta ao servidor TCP
host = '192.168.1.105'
porta = 9999

try:
    metodoSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    metodoSocket.connect((host, porta))
    print('Conectado ao servidor TCP!')
    oled.fill(0)
    oled.text("Servidor TCP OK", 0, 0)
    oled.show()
except Exception as e:
    print('Erro ao conectar:', e)
    oled.fill(0)
    oled.text("Erro TCP", 0, 0)
    oled.show()
    raise SystemExit  # Sai do programa se não conectar

# Função para receber mensagens do servidor
def receber_mensagens():
    while True:
        try:
            data = metodoSocket.recv(1024)
            if not data:
                continue  # Sem dados, continua
            # Padroniza mensagem
            mensagem = data.decode().strip().lower()
            print('Mensagem recebida:', mensagem)
            
            # Comandos de LED no OLED
            if mensagem == 'led_on':
                oled.fill(1)
                oled.show()
                print("OLED ligado")
            elif mensagem == 'led_off':
                oled.fill(0)
                oled.show()
                print("OLED desligado")
        except Exception as e:
            print("Erro ao receber dados:", e)
            break

# Roda a função em uma thread separada
_thread.start_new_thread(receber_mensagens, ())

# Mantém o programa principal ativo
while True:
    time.sleep(1)  # Apenas evita que o programa termine

