FROM python:3.13-slim
RUN pip install --upgrade uv

WORKDIR /app
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

RUN uv run keyphrases-mcp-server --download-models
RUN mkdir -p /app/documents

CMD ["uv", "run", "keyphrases-mcp-server", "--allowed-dir", "/app/documents", "--http"]

# docker build -f Dockerfile-deploy -t keyphrases-mcp .
# docker run --rm --name keyphrases-mcp-server -i -v ./embeddings_model:/app/embeddings_model -v <path_to_documents>:/app/documents -p 8000:8000 keyphrases-mcp:latest
