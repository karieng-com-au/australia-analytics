FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal-dev \
    libgeos-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dash_app/ dash_app/

ENV PORT=8080

CMD gunicorn dash_app.main:server --bind 0.0.0.0:$PORT --timeout 120
