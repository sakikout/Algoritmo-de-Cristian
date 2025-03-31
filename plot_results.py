import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "sync_data.csv"  # Arquivo salvo pelo cliente

# Carregar os dados
df = pd.read_csv(CSV_FILE, parse_dates=["timestamp"])

# Criar os gráficos
plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(df["timestamp"], df["network_delay"], label="Atraso de Rede", color="blue")
plt.plot(df["timestamp"], df["client_delay"], label="Atraso no Cliente", color="red")
plt.ylabel("Atraso (s)")
plt.legend()
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(df["timestamp"], df["desvio"], label="Desvio do Relógio", color="green")
plt.ylabel("Desvio (s)")
plt.xlabel("Tempo")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
