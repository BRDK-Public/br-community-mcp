# Build stage with uv for dependency management
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

WORKDIR /app

# Copy dependency files and source code
COPY pyproject.toml uv.lock ./
COPY src ./src

# Install dependencies using uv
RUN uv venv && \
    uv pip install --no-cache -r pyproject.toml

# Runtime stage
FROM python:3.14-slim-bookworm

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy source code
COPY --from=builder /app/src /app/src

# Set Python path to use venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src:$PYTHONPATH" \
    PYTHONUNBUFFERED=1

# Expose port for SSE mode (optional)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, '/app/src'); from server import mcp; print('OK')" || exit 1

# Run the MCP server
CMD ["python", "-u", "src/server.py"]
