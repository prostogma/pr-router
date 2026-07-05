from fastapi import APIRouter, status

from app.schemas.pull_request import (
    PullRequestCreate,
    PullRequestCreateResponse,
    PullRequestResponse,
)
from app.api.depends import pull_request_service_dp

router = APIRouter(prefix="/pullRequest", tags=["PullRequests"])


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=PullRequestCreateResponse,
)
async def create_pull_request_with_reviewers(
    payload: PullRequestCreate, pull_request_service: pull_request_service_dp
) -> PullRequestCreateResponse:
    pull_request, reviewer_ids = (
        await pull_request_service.create_pull_request_with_reviewers(
            **payload.model_dump()
        )
    )

    return PullRequestCreateResponse(
        pr=PullRequestResponse(
            pull_request_id=pull_request.id,
            pull_request_name=pull_request.title,
            author_id=pull_request.author_id,
            status=pull_request.status,
            assigned_reviewers=reviewer_ids,
        )
    )
