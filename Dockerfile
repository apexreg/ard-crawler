FROM python:3.11-slim

WORKDIR /app

# Install system deps for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY crawler/ ./crawler/
COPY config/ ./config/

ENV PYTHONPATH=/app

CMD ["python", "-m", "crawler.main"]
