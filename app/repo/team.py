from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import TeamAlreadyExistsError
from app.db.models import Team


class TeamRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, team: Team) -> Team:
        try:
            self.session.add(team)
            await self.session.flush()
            return team
        except IntegrityError as e:
            raise TeamAlreadyExistsError(name=team.name) from e

    async def get_team_by_name(self, team_name: str) -> Team | None:
        stmt = (
            select(Team).where(Team.name == team_name).options(selectinload(Team.users))
        )
        result = await self.session.execute(stmt)
        team = result.scalar_one_or_none()

        return team
