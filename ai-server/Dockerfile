FROM python:3.11-slim
WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --no-dev --frozen

RUN uv run python -c "\
from sentence_transformers import SentenceTransformer, CrossEncoder; \
print('Downloading SentenceTransformer...'); \
SentenceTransformer('all-MiniLM-L6-v2'); \
print('Downloading CrossEncoder...'); \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2'); \
print('Models downloaded successfully.')"

COPY src/ ./src/

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "rag_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
