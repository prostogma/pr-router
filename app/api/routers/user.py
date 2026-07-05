from fastapi import APIRouter, status

from app.api.depends import user_service_dp
from app.schemas.user import (
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
