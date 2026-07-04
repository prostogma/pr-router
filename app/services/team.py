from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Team, User
from app.repo.team import TeamRepository
from app.repo.user import UserRepository
from app.schemas.team import (
    TeamCreate,
    TeamCreateResponse,
    TeamDetailsResponse,
    TeamMemberResponse,
)


class TeamService:
    def __init__(
        self,
        session: AsyncSession,
        team_repo: TeamRepository,
        user_repo: UserRepository,
    ):
        self.session = session
        self.team_repo = team_repo
        self.user_repo = user_repo

    async def create_team_with_members(self, team_data: TeamCreate) -> Team:
        async with self.session.begin():
            team = await self.team_repo.create(Team(name=team_data.team_name))

            for member in team_data.members:
                await self.user_repo.create_or_update(
                    user_id=member.user_id,
                    username=member.username,
                    is_active=member.is_active,
                    team_id=team.id,
                )

            team = await self.team_repo.get_by_id_with_users(team.id)

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
