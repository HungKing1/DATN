FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install production dependencies
RUN uv sync --no-dev --frozen

# Pre-download ML models vào image (giảm cold start)
# Models được cache trong HuggingFace cache dir
RUN uv run python -c "\
from sentence_transformers import SentenceTransformer, CrossEncoder; \
print('Downloading SentenceTransformer...'); \
SentenceTransformer('all-MiniLM-L6-v2'); \
print('Downloading CrossEncoder...'); \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2'); \
print('Models downloaded successfully.')"

# Copy source code
COPY src/ ./src/

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "rag_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
