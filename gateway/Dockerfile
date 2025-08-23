FROM python:3.11-slim
WORKDIR /app
COPY shared /app/shared
RUN pip install --no-cache-dir -e /app/shared
COPY gateway /app/gateway
RUN pip install --no-cache-dir -e /app/gateway
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
