import pytest


async def test_create_pull_request(async_client):
    await async_client.post(
        "/team/add",
        json={
            "team_name": "backend",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True},
                {"user_id": "u3", "username": "John", "is_active": True},
            ],
        },
    )

    response = await async_client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": "pr1",
            "pull_request_name": "New feature",
            "author_id": "u1",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["pr"]["pull_request_id"] == "pr1"
    assert body["pr"]["status"] == "OPEN"

    reviewers = body["pr"]["assigned_reviewers"]
    
    assert len(reviewers) == 2

    assert "u1" not in reviewers
