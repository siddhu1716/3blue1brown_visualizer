# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app/backend

# System packages needed by manim/ffmpeg (used for placeholders) and general build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY backend .

ENV PYTHONUNBUFFERED=1
ENV MANIM_MCP_URL=http://manim_mcp:9000

EXPOSE 8000
CMD ["python", "main.py"]
