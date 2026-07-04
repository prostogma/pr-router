from typing import Annotated

from fastapi import Depends

from app.db.session import session_db
from app.repo.team import TeamRepository
from app.repo.user import UserRepository
from app.services.team import TeamService


async def get_team_repo(session: session_db) -> TeamRepository:
    return TeamRepository(session)


async def get_user_repo(session: session_db) -> UserRepository:
    return UserRepository(session)


async def get_team_service(
    session: session_db,
    team_repo: Annotated[TeamRepository, Depends(get_team_repo)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> TeamService:
    return TeamService(session, team_repo, user_repo)


team_service_dp = Annotated[TeamService, Depends(get_team_service)]
