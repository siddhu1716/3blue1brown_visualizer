# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app/frontend

# Install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy source
COPY frontend .

# Build Next.js app
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Expose and run
EXPOSE 3000
ENV NEXT_PUBLIC_BACKEND_URL=http://backend:8000
CMD ["npm", "run", "start"]
