# Manim MCP Dockerfile
FROM python:3.11-slim

WORKDIR /app/manim_mcp

# System packages needed by manim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libcairo2 \
    libpango1.0-0 \
    pkg-config \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY manim_mcp/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY manim_mcp .

ENV PYTHONUNBUFFERED=1
EXPOSE 9000
CMD ["python", "server.py", "--http", "--host", "0.0.0.0", "--port", "9000"]
