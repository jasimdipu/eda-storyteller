FROM python:3.11-slim
WORKDIR /app
COPY shared /app/shared
RUN pip install -e /app/shared
COPY orchestrator /app/orchestrator
RUN pip install -e /app/orchestrator
EXPOSE 8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]