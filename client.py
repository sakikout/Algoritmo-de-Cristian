import socket
import time
import random
import csv
import os
from datetime import datetime, timedelta, timezone

"""
192.168.1.10 servidor
192.168.1.11 cliente 1
192.168.1.12 cliente 2
192.168.1.13 cliente 3

"""
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12345
CSV_FILE = "sync_data.csv"

def artificial_delay():
    delay = random.uniform(0.1, 0.5)  # Atraso entre 100ms e 500ms
    time.sleep(delay)
    return delay

def request_time():
    # artificial_delay()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # client_socket.sendall(b"REQUEST TIME")
    server_response = client_socket.recv(1024).decode()

    # Obtém o tempo dado pelo servidor e o delay do processamento do servidor
    server_time_str, delay = server_response.split(",")
    server_time = datetime.strptime(server_time_str, '%Y-%m-%d %H:%M:%S.%f')
    delay = float(delay)

    client_socket.close()
    return server_time, delay

def synchronize_clock():
    request_time_sent = time.time()
    server_time, delay = request_time()
    request_time_received = time.time()

    # Calcula a latência da rede (Round-Trip Time / 2)
    network_delay = (request_time_received - request_time_sent - delay) / 2 # Metade do RTT
    adjusted_time = server_time +  timedelta(seconds=network_delay) # UTC + p

    current_time = datetime.now(timezone.utc).replace(tzinfo=None)
    desvio = (current_time - adjusted_time).total_seconds()  # Diferença entre relógio local e servidor


    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(timezone.utc), delay, network_delay, desvio])

    print(f"[CLIENT] Hora local: {current_time}")
    print(f"[CLIENT] Hora do servidor: {server_time}")

    if abs(desvio) < 0.1:
        print(f"[CLIENT] Diferença pequena para ajuste: {desvio:.6f}s")
    else: 
        new_time = adjusted_time.strftime('%H:%M:%S')
        new_date = adjusted_time.strftime('%Y-%m-%d')

        os.system(f"sudo date -s '{new_date} {new_time}'")

        print(f"[CLIENT] Tempo ajustado: {adjusted_time} (Atraso: {network_delay:.6f}s)")
        

if __name__ == "__main__":
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "client_delay", "network_delay", "desvio"])

    while True:
        synchronize_clock()
        time.sleep(5)  # Sincroniza a cada 5 segundos