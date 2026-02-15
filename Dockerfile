FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies
COPY server/requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy application code
COPY server/ ./server/

WORKDIR /app/server
CMD uvicorn main:app --host 0.0.0.0 --port $PORT