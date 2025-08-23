FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY shared /app/shared
RUN pip install -e /app/shared
COPY worker /app/worker
RUN pip install -e /app/worker