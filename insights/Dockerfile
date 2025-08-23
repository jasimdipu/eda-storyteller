FROM python:3.11-slim
WORKDIR /app
COPY shared /app/shared
RUN pip install -e /app/shared
COPY insights /app/insights
RUN pip install -e /app/insights
EXPOSE 8002
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]