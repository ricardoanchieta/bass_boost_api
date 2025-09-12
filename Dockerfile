FROM python:3.11-slim

# Configurações de Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dependências do sistema (ffmpeg é necessário pelo pydub)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependências Python primeiro (melhor cache)
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar o restante do código
COPY . .

# Porta padrão; plataformas como Railway sobrescrevem via $PORT
ENV PORT=8000

EXPOSE 8000

# Iniciar a API
# Usamos shell form para permitir ${PORT:-8000}
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}


