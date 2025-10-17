FROM python:3.12-slim
RUN pip install --upgrade uv

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install project's dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Installing project separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Download models which can be customized throuhg build arguments
ARG MCP_KEYPHRASES_EMBEDDINGS_MODEL
ARG MCP_KEYPHRASES_SPACY_TOKENIZER_MODEL
ENV MCP_KEYPHRASES_EMBEDDINGS_MODEL=${MCP_KEYPHRASES_EMBEDDINGS_MODEL}
ENV MCP_KEYPHRASES_SPACY_TOKENIZER_MODEL=${MCP_KEYPHRASES_SPACY_TOKENIZER_MODEL}
# Install model's dependencies
RUN uv run python src/main.py --download-models

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

RUN mkdir -p /app/documents

CMD ["python", "src/main.py", "--allowed-dir", "/app/documents", "--http"]

# docker build -f Dockerfile-deploy -t keyphrases-mcp .
# docker run --rm --name keyphrases-mcp-server -i -v <path_to_documents>:/app/documents -p 8000:8000 --gpus all keyphrases-mcp:latest
