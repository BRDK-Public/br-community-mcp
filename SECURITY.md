# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in the B&R Community MCP Server, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **GitHub Security Advisories**: Use the [Security Advisories](https://github.com/BRDK-GitHub/br-community-mcp/security/advisories) feature to privately report the vulnerability.

2. **Email**: Contact the maintainers directly at the email addresses listed in the [pyproject.toml](pyproject.toml) file.

### What to Include

When reporting a vulnerability, please include:

- **Description**: A clear description of the vulnerability
- **Impact**: The potential impact of the vulnerability
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Affected Versions**: Which versions are affected
- **Suggested Fix**: If you have one, your suggested remediation

## Security Best Practices for Users

### Docker Deployment

1. **Use read-only mounts** for configuration:

   ```bash
   -v "/path/to/config:/app/config:ro"
   ```

2. **Use environment variables** for sensitive configuration (not mounted files)

3. **Pull from official registry** only:

   ```bash
   ghcr.io/brdk-github/br-community-mcp:latest
   ```

4. **Keep Docker updated** with latest security patches

### Local Development

1. **Never commit** `.env` files with credentials or tokens
2. **Use virtual environments** to isolate dependencies
3. **Keep dependencies updated**: Run `uv sync` regularly

## Known Security Considerations

### API Access

This MCP server communicates with the B&R Community forum:

- All connections use HTTPS
- Does not store authentication credentials locally
- Makes read-only requests to public forum data
- Does not execute any user-provided code

### Data Handling

The server:

- Only caches publicly available forum data
- Does not expose internal file system over network
- Uses secure JSON parsing
- Sanitizes all user inputs

## Dependencies

We regularly audit dependencies for vulnerabilities:

```bash
uv run pip-audit
uv run bandit -r src/
```

Our CI pipeline includes automated security scanning.
