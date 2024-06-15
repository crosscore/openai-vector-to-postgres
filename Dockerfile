FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# デフォルトコマンドを無限ループに設定
#CMD ["sh", "-c", "while :; do sleep 2073600; done"]
CMD ["tail", "-f", "/dev/null"]
