# Use a slim base image
FROM python:3.11-slim-buster as builder

# Set environment variables
ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VERSION=1.8.0

# Set the working directory to /app
WORKDIR /app

# Install poetry
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Install dependencies using poetry
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

# Final stage - production image
FROM python:3.11-slim-buster as runtime

# Set environment variables
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Set the working directory to /app
WORKDIR /app

# Copy requirements from builder stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy application code
COPY . /app

# Command to run the application
CMD ["gunicorn", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app.main:app"]
