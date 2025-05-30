# Stage 1: Builder and Test Runner
FROM python:3.11-slim AS builder

WORKDIR /app

# Install all dependencies, including test dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and tests
COPY . .

# Set PYTHONPATH for tests to find project modules
ENV PYTHONPATH "."

# Run tests
# If tests fail, the build will stop here
RUN python -m pytest tests

# Stage 2: Final Runtime Image
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install only runtime dependencies
# Create a temporary requirements file without test libraries
# This assumes pytest, pytest-asyncio, pytest-mock are at the end of requirements.txt
# A more robust way would be to have separate requirements-dev.txt and requirements.txt
COPY requirements.txt .
RUN sed -e '/pytest/d' -e '/pytest-asyncio/d' -e '/pytest-mock/d' requirements.txt > req-runtime.txt && \
    pip install --no-cache-dir -r req-runtime.txt && \
    rm req-runtime.txt

# Copy application code from the builder stage
# This ensures we only copy code that has passed tests
COPY --from=builder /app/Ngunguruhoe /app/Ngunguruhoe
COPY --from=builder /app/main.py /app/main.py
COPY --from=builder /app/alerts.db /app/alerts.db # If you want to package a pre-initialized DB (usually not for prod)
                                                # Or ensure main.py creates it if not exists.
                                                # Current main.py does init_db, so alerts.db doesn't strictly need to be copied.

# Make port 8000 available
EXPOSE 8000

# Define environment variable for PYTHONPATH
ENV PYTHONPATH "."

# Environment variables for Alpaca API - Must be provided at runtime
# Example: docker run -e ALPACA_API_KEY="your_key" -e ALPACA_SECRET_KEY="your_secret" -e ALPACA_PAPER="true" ngunguruhoe_image

# Run main.py when the container launches
CMD ["python", "main.py"]
