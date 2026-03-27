"""Tests for MCP server tools."""

import pytest
import respx
from httpx import Response

from src.server import (
    get_latest_topics,
    get_topic,
    get_top_topics,
    list_categories,
    search_community,
)
from src.utils import BASE_URL


@respx.mock
@pytest.mark.asyncio
async def test_search_community() -> None:
    """Test search_community returns correct results."""
    mock_response = {
        "posts": [
            {
                "id": 1,
                "topic_id": 100,
                "username": "testuser",
                "created_at": "2024-01-15T10:30:00Z",
                "blurb": "This is about mappView widgets",
                "post_number": 1,
                "like_count": 5,
            }
        ],
        "topics": [{"id": 100, "title": "mappView Widget Question"}],
    }

    respx.get(f"{BASE_URL}/search.json").mock(
        return_value=Response(200, json=mock_response)
    )

    result = await search_community("mappView")

    assert result.query == "mappView"
    assert result.total_posts == 1
    assert len(result.posts) == 1
    assert result.posts[0].id == 1
    assert result.posts[0].topic_title == "mappView Widget Question"
    assert result.posts[0].username == "testuser"


@respx.mock
@pytest.mark.asyncio
async def test_search_community_with_category() -> None:
    """Test search_community with category filter."""
    mock_response = {"posts": [], "topics": []}

    route = respx.get(f"{BASE_URL}/search.json").mock(
        return_value=Response(200, json=mock_response)
    )

    await search_community("test", category="ask-questions")

    # Verify the query includes the category (URL-encoded)
    assert route.called
    # ##ask-questions is URL-encoded as %23%23ask-questions
    assert "%23%23ask-questions" in str(route.calls[0].request.url)


@respx.mock
@pytest.mark.asyncio
async def test_search_community_solved_only() -> None:
    """Test search_community with solved_only filter."""
    mock_response = {"posts": [], "topics": []}

    route = respx.get(f"{BASE_URL}/search.json").mock(
        return_value=Response(200, json=mock_response)
    )

    await search_community("test", solved_only=True)

    # Verify the query includes status:solved (URL-encoded)
    assert route.called
    # status:solved is URL-encoded as status%3Asolved
    assert "status%3Asolved" in str(route.calls[0].request.url)


@respx.mock
@pytest.mark.asyncio
async def test_get_topic() -> None:
    """Test get_topic returns correct topic details."""
    mock_topic_response = {
        "id": 123,
        "title": "Test Topic",
        "slug": "test-topic",
        "created_at": "2024-01-15T10:30:00Z",
        "posts_count": 2,
        "views": 100,
        "like_count": 10,
        "has_accepted_answer": True,
        "category_id": 5,
        "tags": ["mappView", "widgets"],
        "post_stream": {
            "posts": [
                {
                    "id": 1,
                    "post_number": 1,
                    "username": "author",
                    "created_at": "2024-01-15T10:30:00Z",
                    "cooked": "<p>Question content</p>",
                    "like_count": 3,
                    "accepted_answer": False,
                },
                {
                    "id": 2,
                    "post_number": 2,
                    "username": "helper",
                    "created_at": "2024-01-15T11:00:00Z",
                    "cooked": "<p>Answer content</p>",
                    "like_count": 5,
                    "accepted_answer": True,
                },
            ]
        },
    }

    mock_categories_response = {
        "category_list": {"categories": [{"id": 5, "name": "Ask Questions"}]}
    }

    respx.get(f"{BASE_URL}/t/123.json").mock(
        return_value=Response(200, json=mock_topic_response)
    )
    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(200, json=mock_categories_response)
    )

    result = await get_topic(123)

    assert result.id == 123
    assert result.title == "Test Topic"
    assert result.posts_count == 2
    assert result.has_accepted_answer is True
    assert result.category_name == "Ask Questions"
    assert len(result.posts) == 2
    assert result.posts[1].is_accepted_answer is True


@respx.mock
@pytest.mark.asyncio
async def test_get_topic_max_posts() -> None:
    """Test get_topic respects max_posts parameter."""
    mock_response = {
        "id": 1,
        "title": "Test",
        "slug": "test",
        "created_at": "2024-01-01",
        "posts_count": 5,
        "post_stream": {
            "posts": [
                {
                    "id": i,
                    "post_number": i,
                    "username": "user",
                    "created_at": "2024-01-01",
                    "cooked": "<p>Content</p>",
                }
                for i in range(1, 6)
            ]
        },
    }

    respx.get(f"{BASE_URL}/t/1.json").mock(
        return_value=Response(200, json=mock_response)
    )
    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(200, json={"category_list": {"categories": []}})
    )

    result = await get_topic(1, max_posts=3)

    assert len(result.posts) == 3


@respx.mock
@pytest.mark.asyncio
async def test_get_topic_handles_object_tags() -> None:
    """Test get_topic normalizes tag objects from newer Discourse versions."""
    mock_topic_response = {
        "id": 456,
        "title": "Topic With Object Tags",
        "slug": "topic-with-object-tags",
        "created_at": "2024-06-01T08:00:00Z",
        "posts_count": 1,
        "views": 10,
        "like_count": 0,
        "has_accepted_answer": False,
        "tags": [
            {"id": 179, "name": "as6-conversion-tool", "slug": "as6-conversion-tool"},
            {"id": 180, "name": "as6-migration-script", "slug": "as6-migration-script"},
            {"id": 142, "name": "automation-studio-6", "slug": "automation-studio-6"},
        ],
        "post_stream": {
            "posts": [
                {
                    "id": 1,
                    "post_number": 1,
                    "username": "author",
                    "created_at": "2024-06-01T08:00:00Z",
                    "cooked": "<p>Content</p>",
                }
            ]
        },
    }

    respx.get(f"{BASE_URL}/t/456.json").mock(
        return_value=Response(200, json=mock_topic_response)
    )
    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(200, json={"category_list": {"categories": []}})
    )

    result = await get_topic(456)

    assert result.tags == [
        "as6-conversion-tool",
        "as6-migration-script",
        "automation-studio-6",
    ]


@respx.mock
@pytest.mark.asyncio
async def test_list_categories() -> None:
    """Test list_categories returns all categories."""
    mock_response = {
        "category_list": {
            "categories": [
                {
                    "id": 1,
                    "name": "Ask Questions",
                    "slug": "ask-questions",
                    "description": "<p>Ask your questions here</p>",
                    "topic_count": 100,
                },
                {
                    "id": 2,
                    "name": "Share Knowledge",
                    "slug": "share-knowledge",
                    "description": "<p>Share your expertise</p>",
                    "topic_count": 50,
                },
                {
                    "id": 3,
                    "name": "Sub Category",
                    "slug": "sub-category",
                    "parent_category_id": 1,
                    "topic_count": 20,
                },
            ]
        }
    }

    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(200, json=mock_response)
    )

    result = await list_categories()

    # Should only return top-level categories
    assert len(result.categories) == 2
    assert result.categories[0].name == "Ask Questions"
    assert result.categories[0].subcategories == ["Sub Category"]


@respx.mock
@pytest.mark.asyncio
async def test_get_latest_topics() -> None:
    """Test get_latest_topics returns latest topics."""
    mock_response = {
        "topic_list": {
            "topics": [
                {
                    "id": 1,
                    "title": "Latest Topic 1",
                    "slug": "latest-topic-1",
                    "created_at": "2024-01-15T10:30:00Z",
                    "last_posted_at": "2024-01-15T12:00:00Z",
                    "posts_count": 3,
                    "views": 50,
                    "category_id": 1,
                },
                {
                    "id": 2,
                    "title": "Latest Topic 2",
                    "slug": "latest-topic-2",
                    "created_at": "2024-01-14T09:00:00Z",
                    "posts_count": 1,
                    "category_id": 2,
                },
            ]
        },
    }

    mock_categories_response = {
        "category_list": {
            "categories": [
                {"id": 1, "name": "Ask Questions"},
                {"id": 2, "name": "Share Knowledge"},
            ]
        }
    }

    respx.get(f"{BASE_URL}/latest.json").mock(
        return_value=Response(200, json=mock_response)
    )
    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(200, json=mock_categories_response)
    )

    result = await get_latest_topics()

    assert len(result.topics) == 2
    assert result.topics[0].title == "Latest Topic 1"
    assert result.topics[0].category_name == "Ask Questions"


@respx.mock
@pytest.mark.asyncio
async def test_get_latest_topics_with_category() -> None:
    """Test get_latest_topics with category filter."""
    mock_response = {"topic_list": {"topics": []}}

    route = respx.get(
        f"{BASE_URL}/latest.json", params={"category": "ask-questions"}
    ).mock(return_value=Response(200, json=mock_response))
    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(200, json={"category_list": {"categories": []}})
    )

    await get_latest_topics(category="ask-questions")

    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_get_top_topics() -> None:
    """Test get_top_topics returns top topics."""
    mock_response = {
        "topic_list": {
            "topics": [
                {
                    "id": 1,
                    "title": "Popular Topic",
                    "slug": "popular-topic",
                    "created_at": "2024-01-01T00:00:00Z",
                    "posts_count": 50,
                    "views": 1000,
                    "like_count": 100,
                    "has_accepted_answer": True,
                    "category_id": 1,
                }
            ]
        },
    }

    respx.get(f"{BASE_URL}/top.json", params={"period": "monthly"}).mock(
        return_value=Response(200, json=mock_response)
    )
    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(
            200,
            json={
                "category_list": {"categories": [{"id": 1, "name": "Ask Questions"}]}
            },
        )
    )

    result = await get_top_topics()

    assert len(result.topics) == 1
    assert result.topics[0].title == "Popular Topic"
    assert result.topics[0].views == 1000


@respx.mock
@pytest.mark.asyncio
async def test_get_top_topics_with_period() -> None:
    """Test get_top_topics with different period."""
    mock_response = {"topic_list": {"topics": []}}

    route = respx.get(f"{BASE_URL}/top.json", params={"period": "yearly"}).mock(
        return_value=Response(200, json=mock_response)
    )
    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(200, json={"category_list": {"categories": []}})
    )

    await get_top_topics(period="yearly")

    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_get_top_topics_invalid_period() -> None:
    """Test get_top_topics falls back to monthly for invalid period."""
    mock_response = {"topic_list": {"topics": []}}

    route = respx.get(f"{BASE_URL}/top.json", params={"period": "monthly"}).mock(
        return_value=Response(200, json=mock_response)
    )
    respx.get(f"{BASE_URL}/categories.json").mock(
        return_value=Response(200, json={"category_list": {"categories": []}})
    )

    await get_top_topics(period="invalid")

    assert route.called
