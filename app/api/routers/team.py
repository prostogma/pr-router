from fastapi import APIRouter
from fastapi import status

from app.schemas.team import TeamCreate, TeamCreateResponse
from app.api.depends import team_service_dp

router = APIRouter(prefix="/team", tags=["Teams"])


@router.post(
    "/add", status_code=status.HTTP_201_CREATED, response_model=TeamCreateResponse
)
async def create_team_with_members(
    team_data: TeamCreate, team_service: team_service_dp
):
    return await team_service.create_team_with_members(team_data)
