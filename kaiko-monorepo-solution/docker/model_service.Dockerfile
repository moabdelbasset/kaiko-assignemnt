FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY 3rdparty/python/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY libs ./libs
COPY services/model_service ./services/model_service
ENV PYTHONPATH=/app

EXPOSE 8002
CMD ["uvicorn", "services.model_service.app.main:app", "--host", "0.0.0.0", "--port", "8002"]
