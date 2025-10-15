# Use official lightweight Python image
FROM python:3.10-slim

# Prevent Python from writing .pyc files & buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside container
WORKDIR /pro


# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY app/ ./app 

COPY alembic/ ./alembic
COPY /.env .env
COPY alembic.ini ./alembic.ini

# Run Alembic migrations before starting the app
# Replace `main.py` with your actual entry point
CMD ["sh", "-c", "uvicorn app/main:app --reload"]
