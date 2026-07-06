from typing import Annotated
from fastapi import APIRouter, Query, status

from app.api.depends import stats_service_dp
from app.schemas.stats import (
    ReviewerStatsItem,
    ReviewerStatsResponse,
    StatsPaginationParams,
)

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get(
    "/reviewers", status_code=status.HTTP_200_OK, response_model=ReviewerStatsResponse
)
async def get_reviewers_stats(
    stats_service: stats_service_dp,
    pagination: Annotated[StatsPaginationParams, Query()],
) -> ReviewerStatsResponse:
    reviewers_stats = await stats_service.get_reviewers_stats(**pagination.model_dump())

    return ReviewerStatsResponse(
        reviewers=[
            ReviewerStatsItem(
                user_id=reviewer_stats.id,
                username=reviewer_stats.username,
                assigned_count=reviewer_stats.assigned_count,
            )
            for reviewer_stats in reviewers_stats
        ]
    )
