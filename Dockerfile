    # Stage 1: Build Stage (for dependencies)
    # Changed from 'buster' to 'bullseye' (Debian 11) or 'bookworm' (Debian 12)
    FROM python:3.9-slim-bullseye as builder # Recommended: use bullseye, or try bookworm

    # Set the working directory inside the container for the build process.
    WORKDIR /app

    # Install build dependencies that might be needed for some Python packages.
    # These will NOT be in the final image due to the multi-stage build.
    RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        && rm -rf /var/lib/apt/lists/*

    # Copy requirements.txt first to leverage Docker's build cache.
    COPY requirements.txt .

    # Install Python dependencies.
    RUN pip install --no-cache-dir --compile-all -r requirements.txt

    # Stage 2: Final Image Stage (runtime)
    # Use the same base image as the builder stage for consistency in runtime.
    FROM python:3.9-slim-bullseye # Match the base image from Stage 1

    # Set the working directory for the application.
    WORKDIR /app

    # Copy only the installed Python packages and binaries from the builder stage.
    COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
    COPY --from=builder /usr/local/bin /usr/local/bin

    # Copy the rest of your Flask application code into the container.
    COPY . .

    # Expose the port your Flask application runs on.
    EXPOSE 5000

    # Define the command to run your Flask application when the container starts.
    CMD ["python", "app.py"]
    