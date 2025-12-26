# ---------- Base image ----------
FROM python:3.11-slim

# Workdir inside the container
WORKDIR /app

# Install system dependencies (optional but useful)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Make Python output unbuffered
ENV PYTHONUNBUFFERED=1

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI (assuming app = FastAPI() is in main.py)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
