# syntax=docker/dockerfile:1
FROM python:3.11-slim AS build
WORKDIR /app

# Instale ferramentas de build e construa as rodas (wheels) do python
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.11-slim AS runtime
WORKDIR /app

# Cria usuário não-root
RUN useradd -m appuser

# Copia e instala as dependências pré-compiladas
COPY --from=build /usr/src/app/wheels /wheels
COPY --from=build /app/requirements.txt .
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Copia o código com propriedade correta
COPY --chown=appuser:appuser . .

# Coleta arquivos estáticos
RUN SECRET_KEY=dummy \
    GET_INSTITUTIONS=dummy \
    GET_INSTITUTION=dummy \
    GET_INSTITUTIONS_BY_STATE=dummy \
    GET_INSTITUTIONS_BY_REGION=dummy \
    python manage.py collectstatic --noinput

USER appuser
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi:application"]
