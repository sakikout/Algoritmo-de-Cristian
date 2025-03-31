import socket
import time
import ntplib
import os
import threading
from datetime import datetime, timezone

"""
192.168.1.10 servidor

"""

# Função para obter a hora correta via NTP
def get_ntp_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3) # Faz a requisição do tempo correto para o servidor NTP
        requested_time = datetime.utcfromtimestamp(response.tx_time)

        return requested_time.strftime('%Y-%m-%d %H:%M:%S.%f') # Tempo UTC
    except Exception as e:
        print(f"[SERVER] Erro ao obter tempo NTP: {e}")
        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f') # Caso haja uma falha, usa o tempo local

def update_time():
    try:
        while True:
            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org', version=3) # Faz a requisição do tempo correto para o servidor NTP
            requested_time = datetime.utcfromtimestamp(response.tx_time)
     
            # Ajusta o próprio tempo ao horário obtido pelo NTP
            new_time= requested_time.strftime('%H:%M:%S')
            new_date = requested_time.strftime('%Y-%m-%d')

            # os.system(f"sudo date -s '{new_date} {new_time}'")
            print(f"[SERVER] Tempo ajustado para: {new_date} {new_time}")

    except Exception as error:
            print(f"[SERVER] Erro ao atualizar tempo: {error}")

    time.sleep(60)

# Configura o servidor
HOST = "0.0.0.0" # Escuta em todas as interfaces
PORT = 12345

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    threading.Thread(target=update_time, daemon=True).start()
    print(f"[SERVER] Servidor de tempo rodando em {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[SERVER] Conexão recebida de {addr}")

        start_time = time.time()  # Momento que recebeu o pedido
        ntp_time = get_ntp_time()  # Obtém a hora correta
        end_time = time.time()  # Momento antes de enviar a resposta

        delay = end_time - start_time  # Calcula o delay
        response = f"{ntp_time},{delay}" # Formatação da resposta do servidor

        client_socket.sendall(response.encode())  # Envia a resposta para o cliente

        client_socket.close()
