# Use an official Python 3.11 image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first (for better layer caching)
COPY server/requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy the rest of your application code
COPY server/ ./server/

# Set the working directory for the runtime command
WORKDIR /app/server

# Command to run the application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT