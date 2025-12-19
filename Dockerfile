# Use stable Python
FROM python:3.11-slim

# Prevent Python buffering issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependency file first (for caching)
COPY requirements.txt .

# Upgrade pip & install deps
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Non-root user (security)
RUN useradd -m botuser
USER botuser

# Start bot
CMD ["python", "-m", "app.main"]
