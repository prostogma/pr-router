from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.db.models import User
from app.repo.user import UserRepository
from app.repo.pull_request import PullRequestRepository


class UserService:
    def __init__(
        self,
        session: AsyncSession,
        user_repo: UserRepository,
        pr_repo: PullRequestRepository,
    ):
        self.session = session
        self.user_repo = user_repo
        self.pr_repo = pr_repo

    async def update_user_activity(self, user_id: str, is_active: bool) -> User:
        async with self.session.begin():
            user = await self.user_repo.get_by_id_with_team(user_id)

            if not user:
                raise NotFoundError()

            user.is_active = is_active

            return user
