from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: str) -> User | None:
        return await self.session.get(User, user_id)

    async def get_by_id_with_team(self, user_id: str) -> User | None:
        stmt = select(User).where(User.id == user_id).options(selectinload(User.team))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_or_update(
        self, user_id: str, username: str, is_active: bool, team_id: UUID
    ) -> User:
        user = await self.get_by_id(user_id)

        if user:
            user.username = username
            user.is_active = is_active
            user.team_id = team_id
        else:
            user = User(
                id=user_id, username=username, is_active=is_active, team_id=team_id
            )
            self.session.add(user)

        return user

    async def get_active_users_by_team(self, team_id: UUID) -> list[User]:
        stmt = select(User).where(User.team_id == team_id, User.is_active.is_(True))
        result = await self.session.execute(stmt)
        return result.scalars().all()
