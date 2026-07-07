from typing import Annotated

from fastapi import APIRouter, Body, status

from app.schemas.pull_request import (
    PullRequestReassignReviewer,
    PullRequestCreate,
    PullRequestCreateResponse,
    PullRequestMergeResponse,
    PullRequestMergedResponse,
    PullRequestReassignReviewerResponse,
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


@router.post(
    "/merge", status_code=status.HTTP_200_OK, response_model=PullRequestMergedResponse
)
async def merge_pull_request(
    pull_request_id: Annotated[str, Body(embed=True)], pull_request_service: pull_request_service_dp
) -> PullRequestMergedResponse:
    pull_request = await pull_request_service.merge_pull_request(pull_request_id)

    return PullRequestMergedResponse(
        pr=PullRequestMergeResponse(
            pull_request_id=pull_request.id,
            pull_request_name=pull_request.title,
            author_id=pull_request.author_id,
            status=pull_request.status,
            assigned_reviewers=[
                reviewer.reviewer_id for reviewer in pull_request.reviewers
            ],
            mergedAt=pull_request.merged_at,
        )
    )


@router.post(
    "/reassign",
    status_code=status.HTTP_200_OK,
    response_model=PullRequestReassignReviewerResponse,
)
async def reassign_reviewer(
    payload: PullRequestReassignReviewer, pull_request_service: pull_request_service_dp
) -> PullRequestReassignReviewerResponse:
    pull_request, new_reviewer_id = await pull_request_service.reassign_reviewer(
        **payload.model_dump()
    )

    return PullRequestReassignReviewerResponse(
        pr=PullRequestResponse(
            pull_request_id=pull_request.id,
            pull_request_name=pull_request.title,
            author_id=pull_request.author_id,
            status=pull_request.status,
            assigned_reviewers=[
                reviewer.reviewer_id for reviewer in pull_request.reviewers
            ],
        ),
        replaced_by=new_reviewer_id,
    )
