# Contributing to B&R Community MCP

Thank you for your interest in contributing to the B&R Community MCP Server! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (for testing Docker builds and Docker Compose setup)
- Git

### Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/BRDK-GitHub/br-community-mcp.git
   cd br-community-mcp
   ```

2. **Install dependencies:**

   ```bash
   uv sync --extra test --extra dev
   ```

3. **Set up pre-commit hooks (optional but recommended):**
   ```bash
   uv run pre-commit install
   ```

4. **Verify your setup by running tests:**

   ```bash
   uv run pytest tests/ -v
   ```

## Making Changes

### Branch Naming

Use descriptive branch names:

- `feature/add-category-filtering`
- `fix/search-query-handling`
- `docs/update-setup-guide`
- `refactor/simplify-api-calls`

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:

- `feat(search): add category filtering to search_community`
- `fix(integration): handle HTTP errors gracefully`
- `docs(readme): clarify Docker setup instructions`
- `test(search): improve search test coverage`

## Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** with appropriate tests
3. **Run the test suite locally:**
   ```bash
   uv run pytest tests/ -v
   ```
4. **Run linting and formatting:**
   ```bash
   uv run ruff check src tests
   uv run ruff format src tests
   ```
5. **Run type checking:**
   ```bash
   uv run mypy src
   ```
6. **Check code quality metrics:**
   ```bash
   uv run radon mi src/
   uv run bandit -r src/
   ```
7. **Push your branch** and create a Pull Request
8. **Fill out the PR template** completely
9. **Wait for CI checks** to pass
10. **Address review feedback** if any

### PR Requirements

- All CI checks must pass
- Code coverage should not decrease
- At least one maintainer approval required
- No merge conflicts with `main`
- Type hints should be present for all public functions

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) with line length of 120
- Use type hints for function parameters and returns
- Use docstrings for public functions and classes
- Follow the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) conventions

### Linting

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check for issues
uv run ruff check src tests

# Auto-fix issues
uv run ruff check --fix src tests

# Format code
uv run ruff format src tests
```

### Type Checking

```bash
uv run mypy src
```

### Code Complexity

```bash
# Check maintainability index
uv run radon mi src/

# Check for security issues
uv run bandit -r src/
```

## Testing

### Test Structure

```
tests/
├── unit/           # Fast, isolated tests with mocked HTTP calls
└── integration/    # Tests with real community forum API calls
```

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run only unit tests (fast)
uv run pytest tests/unit -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/unit/test_utils.py -v

# Run tests matching a pattern
uv run pytest tests/ -k "search" -v
```

### Writing Tests

- Use `pytest` and `pytest-asyncio` for async code
- Use `respx` to mock HTTP calls (don't hit the real API in tests)
- Mock external dependencies (HTTP calls, file system)
- Aim for >80% code coverage on new code
- Include both success and failure cases
- Test error handling and edge cases

### Test Example

```python
import pytest
from unittest.mock import AsyncMock
import respx
from httpx import Response

@pytest.mark.asyncio
async def test_search_community_success():
    """Test successful community search."""
    with respx.mock:
        # Mock the HTTP response
        respx.get("https://api.example.com/search").mock(
            return_value=Response(200, json={
                "results": [{"id": 1, "title": "Test Topic"}]
            })
        )
        
        # Your test code here
        results = await search_community("test query")
        assert len(results) > 0
```

## Reporting Issues

Please use our [GitHub issue tracker](https://github.com/BRDK-GitHub/br-community-mcp/issues) to report bugs or request features. When you create a new issue, you will be prompted to choose from several templates that ensure all necessary information is provided.

### Bug Reports

When reporting bugs using the provided template, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Minimal steps to reproduce
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - OS and version
   - Python version
   - How you're running the server (Docker, UV, etc.)
6. **Logs**: Relevant error messages or stack traces

### Feature Requests

When submitting feature requests using the provided template, please include:

1. **Use Case**: Why you need this feature
2. **Proposed Solution**: Your suggested approach
3. **Alternatives**: Other solutions you've considered

## Development Workflow

### Testing Your Changes with VS Code

To test your changes with GitHub Copilot:

1. **Using UV (development setup):**
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

2. **Using MCP Inspector (for debugging tools):**
   ```bash
   uv run mcp dev src/server.py
   ```

3. **Using Docker Compose (for production-like testing):**
   ```bash
   docker compose build
   docker compose run --rm br-community-local
   ```

## Security

If you discover a security vulnerability, please follow our [Security Policy](SECURITY.md) and report it privately rather than opening a public issue.

## Questions?

If you have questions about contributing, feel free to:

- Open a [Discussion](https://github.com/BRDK-GitHub/br-community-mcp/discussions)
- Ask in the issue tracker with the `question` label
- Check existing issues and discussions for similar questions

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [B&R Automation Community](https://community.br-automation.com/)

Thank you for contributing to making the B&R Community MCP Server better!
