# Usa a imagem oficial do Python
FROM python:3.9

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala dependências (se houver)
RUN pip install ntplib

# Define o comando padrão para os contêineres
CMD ["python", "server.py"]
