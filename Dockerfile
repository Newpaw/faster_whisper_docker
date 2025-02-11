# Use an official Python runtime as a parent image.
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files and enable unbuffered logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory.
WORKDIR /app

# Install system dependencies (including ffmpeg for audio decoding).
RUN apt-get update && \
    apt-get install -y gcc ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip and install required Python packages.
# Since we are not using a proper requirements.txt here, we'll install the minimal dependencies.
RUN pip install --upgrade pip && \
    pip install fastapi uvicorn python-dotenv faster-whisper python-multipart

# Copy the project files into the container.
COPY . .

# Expose port 8000 for the FastAPI app.
EXPOSE 8000

# Run the application with uvicorn.
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
