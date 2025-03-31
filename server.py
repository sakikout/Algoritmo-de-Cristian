import socket
import time
import ntplib
from datetime import datetime, timezone

# Função para obter a hora correta via NTP
def get_ntp_time():
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org', version=3) # Faz a requisição do tempo correto para o servidor NTP
        return datetime.utcfromtimestamp(response.tx_time).strftime('%Y-%m-%d %H:%M:%S.%f') # Tempo UTC
    except Exception as e:
        print(f"Erro ao obter tempo NTP: {e}")
        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f') # Caso haja uma falha, usa o tempo local

# Configura o servidor
HOST = '0.0.0.0' # Escuta em todas as interfaces
PORT = 12345

if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor de tempo rodando em {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexão recebida de {addr}")

        start_time = time.time()  # Momento que recebeu o pedido
        ntp_time = get_ntp_time()  # Obtém a hora correta
        end_time = time.time()  # Momento antes de enviar a resposta

        delay = end_time - start_time  # Calcula o delay
        response = f"{ntp_time},{delay}" # Formatação da resposta do servidor

        client_socket.sendall(response.encode())  # Envia a resposta para o cliente
        client_socket.close()
