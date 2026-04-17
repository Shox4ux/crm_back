# Stage 1: Builder
FROM python:3.10-slim as builder

RUN pip install poetry

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Do not create a virtualbox inside the container
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Stage 2: Final Image
FROM python:3.10-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

# Ensure the assets folder exists for your PDF
RUN mkdir -p assets

CMD ["bash"]
