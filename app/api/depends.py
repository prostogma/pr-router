from typing import Annotated

from fastapi import Depends

from app.db.session import session_db
from app.repo.pull_request import PullRequestRepository
from app.repo.team import TeamRepository
from app.repo.user import UserRepository
from app.services.pull_request import PullRequestService
from app.services.team import TeamService
from app.services.user import UserService


async def get_team_repo(session: session_db) -> TeamRepository:
    return TeamRepository(session)


async def get_user_repo(session: session_db) -> UserRepository:
    return UserRepository(session)


async def get_pull_request_repo(session: session_db) -> PullRequestRepository:
    return PullRequestRepository(session)


async def get_team_service(
    session: session_db,
    team_repo: Annotated[TeamRepository, Depends(get_team_repo)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> TeamService:
    return TeamService(session, team_repo, user_repo)


async def get_user_service(
    session: session_db,
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
    pr_repo: Annotated[PullRequestRepository, Depends(get_pull_request_repo)],
) -> UserService:
    return UserService(session, user_repo, pr_repo)


async def get_pull_request_service(
    session: session_db,
    pr_repo: Annotated[PullRequestRepository, Depends(get_pull_request_repo)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> PullRequestService:
    return PullRequestService(session, pr_repo, user_repo)


team_service_dp = Annotated[TeamService, Depends(get_team_service)]

user_service_dp = Annotated[UserService, Depends(get_user_service)]

pull_request_service_dp = Annotated[
    PullRequestService, Depends(get_pull_request_service)
]
