# B&R Community MCP Server

An MCP (Model Context Protocol) server that provides tools to search and retrieve information from the [B&R Automation community forum](https://community.br-automation.com).

## Features

- **Search** - Full-text search across all forum posts and topics
- **Get Topic** - Retrieve detailed topic information including all posts
- **List Categories** - Browse all available forum categories
- **Latest Topics** - Get the most recent discussions
- **Top Topics** - Get popular topics by time period

## Prerequisites

- Docker Desktop installed and running (for Docker option)
- Python 3.14+ and uv (for UV option)
- VS Code with GitHub Copilot extension

## Demo

https://github.com/user-attachments/assets/14474af7-bc01-49b2-8d24-bdc8c1f0f38c

## Quick Start (VS Code)

Add to `.vscode/mcp.json` in your workspace:

### Option 1: Docker (Recommended)

```json
{
  "servers": {
    "br-community": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "ghcr.io/brdk-github/br-community-mcp:latest"
      ]
    }
  }
}
```

### Option 2: UV (Local Development)

```json
{
  "servers": {
    "br-community": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/br-community-mcp", "python", "src/server.py"]
    }
  }
}
```

Restart VS Code, then test in Copilot Chat: *"Search the B&R community for mappView"*

---

## Local Development Setup

### Option 1: UV (Recommended for development)

```bash
# Clone and install
git clone <repository-url>
cd br-community-mcp
uv sync --extra test --extra dev

# Run server
uv run python src/server.py
```

### Option 2: Docker Compose

```bash
# Local build
docker compose build

# Run the server
docker compose run --rm br-community-local
```

### Testing with MCP Inspector

The MCP Inspector provides a web UI for testing tools and prompts:

```bash
# With UV
uv run mcp dev src/server.py

# Opens browser at http://localhost:5173
```

Note: On Windows, use VS Code's Run and Debug panel instead (stdio transport issues with Inspector).

---

## Tools

| Tool | Description |
|------|-------------|
| `search_community` | Full-text search for topics and posts with optional category filter and solved-only flag |
| `get_topic` | Get detailed topic information including all posts |
| `list_categories` | List all available forum categories with descriptions |
| `get_latest_topics` | Get the most recent discussions with optional category filter |
| `get_top_topics` | Get popular topics by time period (daily, weekly, monthly, quarterly, yearly, all) |

