from fastapi import APIRouter, status

from app.api.depends import user_service_dp
from app.schemas.user import (
    PullRequestShort,
    UserReviewsResponse,
    UserUpdateActivity,
    UserUpdateActivityDetails,
    UserUpdateActivityResponse,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/setIsActive",
    status_code=status.HTTP_200_OK,
    response_model=UserUpdateActivityResponse,
)
async def update_user_activity(
    payload: UserUpdateActivity, user_service: user_service_dp
) -> UserUpdateActivityResponse:
    user = await user_service.update_user_activity(
        user_id=payload.user_id, is_active=payload.is_active
    )

    return UserUpdateActivityResponse(
        user=UserUpdateActivityDetails(
            user_id=user.id,
            username=user.username,
            team_name=user.team.name,
            is_active=user.is_active,
        )
    )


@router.get(
    "/getReview", status_code=status.HTTP_200_OK, response_model=UserReviewsResponse
)
async def get_user_reviews(
    user_id: str, user_service: user_service_dp
) -> UserReviewsResponse:
    pull_requests = await user_service.get_user_reviews(user_id)

    return UserReviewsResponse(
        user_id=user_id,
        pull_requests=[
            PullRequestShort(
                pull_request_id=pr.id,
                pull_request_name=pr.title,
                author_id=pr.author_id,
                status=pr.status,
            )
            for pr in pull_requests
        ],
    )
