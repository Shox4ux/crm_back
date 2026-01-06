FROM python:3.10-slim

# Prevent Python from writing .pyc files & buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory inside container
WORKDIR /crm


# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy Alembic from your actual project (must be in GitHub)
COPY alembic/ ./alembic
COPY alembic.ini ./alembic.ini

# Copy environment only if needed
# COPY  .env .env

# Run Alembic migrations before starting the app
COPY ./app /crm/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--http","h11"]
