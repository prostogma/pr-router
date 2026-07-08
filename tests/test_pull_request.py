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


async def test_merge(async_client):
    await async_client.post(
        "/team/add",
        json={
            "team_name": "backend",
            "members": [
                {"user_id": "u1", "username": "Alice", "is_active": True},
                {"user_id": "u2", "username": "Bob", "is_active": True},
            ],
        },
    )

    await async_client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": "pr1",
            "pull_request_name": "Feature",
            "author_id": "u1",
        },
    )

    response = await async_client.post(
        "/pullRequest/merge", json={"pull_request_id": "pr1"}
    )

    assert response.status_code == 200

    body = response.json()

    assert body["pr"]["status"] == "MERGED"
    assert body["pr"]["mergedAt"] is not None

    # идемпотентность

    response = await async_client.post(
        "/pullRequest/merge", json={"pull_request_id": "pr1"}
    )

    assert response.status_code == 200


async def test_reassign(async_client):
    await async_client.post(
        "/team/add",
        json={
            "team_name": "backend",
            "members": [
                {
                    "user_id": "u1",
                    "username": "Alice",
                    "is_active": True,
                },
                {
                    "user_id": "u2",
                    "username": "Bob",
                    "is_active": True,
                },
                {
                    "user_id": "u3",
                    "username": "John",
                    "is_active": True,
                },
                {
                    "user_id": "u4",
                    "username": "Mike",
                    "is_active": True,
                },
            ],
        },
    )

    response = await async_client.post(
        "/pullRequest/create",
        json={
            "pull_request_id": "pr1",
            "pull_request_name": "Feature",
            "author_id": "u1",
        },
    )

    reviewers = response.json()["pr"]["assigned_reviewers"]

    old = reviewers[0]

    response = await async_client.post(
        "/pullRequest/reassign",
        json={
            "pull_request_id": "pr1",
            "old_reviewer_id": old,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["replaced_by"] != old
    assert old not in body["pr"]["assigned_reviewers"]
    assert body["replaced_by"] in body["pr"]["assigned_reviewers"]
