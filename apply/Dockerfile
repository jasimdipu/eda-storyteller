FROM python:3.11-slim
WORKDIR /app
COPY shared /app/shared
RUN pip install -e /app/shared
COPY apply /app/apply
RUN pip install -e /app/apply
EXPOSE 8003
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"]