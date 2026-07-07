import random

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, UsersFromDifferentTeamsError
from app.db.models import PullRequest, User
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

    async def deactivate_users(self, user_ids: list[str]) -> list[User]:
        async with self.session.begin():
            users = await self.user_repo.get_by_ids_with_team(user_ids)

            if len(users) != len(user_ids):
                raise NotFoundError()

            team_id = {user.team_id for user in users}

            if len(team_id) != 1:
                raise UsersFromDifferentTeamsError()

            deactivated_ids = set(user_ids)

            for user in users:
                pull_requests = await self.pr_repo.get_open_by_reviewer(user.id)

                for pull_request in pull_requests:
                    reviewer_ids = {
                        reviewer.reviewer_id for reviewer in pull_request.reviewers
                    }

                    candidates = await self.user_repo.get_active_users_by_team(
                        user.team_id
                    )

                    candidates = [
                        candidate
                        for candidate in candidates
                        if candidate.id != pull_request.author_id
                        and candidate.id not in reviewer_ids
                        and candidate.id not in deactivated_ids
                    ]

                    if not candidates:
                        continue

                    new_reviewer = random.choice(candidates)

                    reviewer_link = next(
                        reviewer
                        for reviewer in pull_request.reviewers
                        if reviewer.reviewer_id == user.id
                    )

                    reviewer_link.reviewer_id = new_reviewer.id

            for user in users:
                user.is_active = False

            return users

    async def get_user_reviews(self, user_id: str) -> list[PullRequest]:
        return await self.pr_repo.get_by_reviewer(user_id)
