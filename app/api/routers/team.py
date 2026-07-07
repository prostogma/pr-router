from fastapi import APIRouter
from fastapi import status

from app.schemas.team import (
    TeamCreate,
    TeamCreateResponse,
    TeamDetailsResponse,
    TeamMemberResponse,
)
from app.api.depends import team_service_dp

router = APIRouter(prefix="/team", tags=["Teams"])


@router.post(
    "/add", status_code=status.HTTP_201_CREATED, response_model=TeamCreateResponse
)
async def create_team_with_members(
    team_data: TeamCreate, team_service: team_service_dp
) -> TeamCreateResponse:
    team = await team_service.create_team_with_members(team_data)

    return TeamCreateResponse(
        team=TeamDetailsResponse(
            team_name=team.name,
            members=[
                TeamMemberResponse(
                    user_id=user.id,
                    username=user.username,
                    is_active=user.is_active,
                )
                for user in team.users
            ],
        )
    )


@router.get("/get", status_code=status.HTTP_200_OK, response_model=TeamDetailsResponse)
async def get_team_with_members_by_name(
    team_name: str, team_service: team_service_dp
) -> TeamDetailsResponse:
    team = await team_service.get_team_with_members_by_name(team_name)

    return TeamDetailsResponse(
        team_name=team.name,
        members=[
            TeamMemberResponse(
                user_id=user.id,
                username=user.username,
                is_active=user.is_active,
            )
            for user in team.users
        ],
    )
