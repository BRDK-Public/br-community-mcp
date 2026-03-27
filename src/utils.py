"""Utility functions for the B&R Community MCP server."""

import re
from typing import Optional

import httpx

# Base URL for the B&R Community Discourse forum
BASE_URL = "https://community.br-automation.com"


def strip_html(html: str) -> str:
    """Remove HTML tags and clean up text."""
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", html)
    # Decode common HTML entities
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = text.replace("&#39;", "'")
    text = text.replace("&nbsp;", " ")
    # Clean up whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


async def make_request(endpoint: str, params: Optional[dict] = None) -> dict:
    """Make an HTTP request to the Discourse API."""
    url = f"{BASE_URL}{endpoint}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()


async def fetch_category_map() -> dict[int, str]:
    """Fetch a mapping of category ID to category name from the API."""
    data = await make_request("/categories.json")
    cat_map: dict[int, str] = {}
    for cat in data.get("category_list", {}).get("categories", []):
        cat_map[cat["id"]] = cat["name"]
    return cat_map
