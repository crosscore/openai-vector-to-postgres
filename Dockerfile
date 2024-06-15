FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN echo "alias ls='ls --color=auto'" >> ~/.bashrc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

#CMD ["sh", "-c", "while :; do sleep 2073600; done"]
CMD ["tail", "-f", "/dev/null"]
