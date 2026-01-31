# Build Stage for Next.js
FROM node:20-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Final Stage: Python Backend
FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy everything else
COPY . .

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/frontend/out ./frontend/out

# Pre-download the AI model to save time during startup
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Set environment variables
ENV PORT=7860
ENV NODE_ENV=production

# Hugging Face Spaces uses 7860 by default
EXPOSE 7860

# Run the FastAPI server
# Since main.py serves static files, this will host both API and UI
CMD ["python", "backend/main.py"]
