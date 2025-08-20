# Stage 1: Build Stage (for dependencies)
# Using a specific Python version on a slim Debian base for a smaller image.
FROM python:3.9-slim-buster as builder

# Set the working directory inside the container for the build process.
WORKDIR /app

# Install build dependencies that might be needed for some Python packages (e.g., if they have C extensions).
# These will NOT be in the final image due to the multi-stage build, keeping it lean.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements.txt file.
# This allows Docker to cache the pip install step if requirements don't change,
# significantly speeding up subsequent builds.
COPY requirements.txt .

# Install Python dependencies.
# --no-cache-dir reduces the image size by not storing pip's cache.
# --compile-all compiles the Python packages during installation for potentially faster startup.
RUN pip install --no-cache-dir --compile-all -r requirements.txt

# Stage 2: Final Image Stage (runtime)
# Use a fresh, even smaller base image for the final runtime environment.
FROM python:3.9-slim-buster

# Set the working directory for the application.
WORKDIR /app

# Copy only the installed Python packages from the builder stage to the final image.
# This ensures that bulky build tools from Stage 1 are not included in your final deployable image.
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the rest of your Flask application code into the container.
# This includes app.py, the 'templates/' folder, and any other project files.
COPY . .

# Expose the port that your Flask application runs on.
# This serves as documentation and allows Docker to inspect port usage,
# but you still need to map the port when running the container (e.g., in docker-compose.yml).
EXPOSE 5000

# Define the command to run your Flask application when the container starts.
# The exec form (["executable", "param1"]) is preferred as it ensures proper signal handling,
# allowing graceful shutdowns (e.g., when 'docker stop' is used).
CMD ["python", "app.py"]
