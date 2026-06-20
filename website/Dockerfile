# Use uma imagem base com Python
FROM python:3.11-slim

# Defina o diretório de trabalho no container
WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y gcc && apt-get clean

# Copie os arquivos de requisitos para o container e instale as dependências
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto para o container
COPY . /app/

# Cria usuário não-root
RUN useradd -m appuser

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Define o usuário para rodar a aplicação
USER appuser

# Exponha a porta 8000
EXPOSE 8000

# Comando para rodar o Gunicorn no container
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
