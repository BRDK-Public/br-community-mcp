# B&R Community MCP Server

An MCP (Model Context Protocol) server that provides tools to search and retrieve information from the [B&R Automation community forum](https://community.br-automation.com).

## Features

- **Search** - Full-text search across all forum posts and topics
- **Get Topic** - Retrieve detailed topic information including all posts
- **List Categories** - Browse all available forum categories
- **Latest Topics** - Get the most recent discussions
- **Top Topics** - Get popular topics by time period

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd br-community-mcp

# Install dependencies with uv
uv sync
```

## Usage

### Run with MCP Inspector (Development)

```bash
uv run mcp dev server.py
```

### Run directly (stdio transport)

```bash
uv run python server.py
```

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

Add to your GitHub Copilot configuration:

```json
{
  "servers": {
    "br-community": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/br-community-mcp", "python", "server.py"]
    }
  }
}
```

## License

MIT
