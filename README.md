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

## Available Tools

### `search_community`

Search the B&R Community forum for topics and posts.

**Parameters:**
- `query` (required): Search terms (e.g., "mappView widget", "ACOPOS error")
- `category` (optional): Category slug to filter results
- `solved_only` (optional): Only return topics with accepted answers

### `get_topic`

Get detailed information about a specific topic including its posts.

**Parameters:**
- `topic_id` (required): The numeric ID of the topic
- `max_posts` (optional): Maximum posts to retrieve (default: 10)

### `list_categories`

List all available categories in the forum.

### `get_latest_topics`

Get the latest topics from the forum.

**Parameters:**
- `category` (optional): Category slug to filter
- `page` (optional): Page number for pagination

### `get_top_topics`

Get the most popular topics.

**Parameters:**
- `period` (optional): One of "daily", "weekly", "monthly", "quarterly", "yearly", "all"

## Configuration for GitHub Copilot

Add one of these configurations to `.vscode/mcp.json` in your workspace:

### Docker (Production)

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

### UV (Development)

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

## Contributing

Interested in contributing? Please read our [Contributing Guidelines](CONTRIBUTING.md) for information about our development setup, coding standards, testing requirements, and how to submit pull requests.