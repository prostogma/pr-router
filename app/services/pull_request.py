from datetime import datetime, timezone
import random
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    NoReviewerCandidatesError,
    NotFoundError,
    PullRequestAlreadyExistsError,
    PullRequestMergedError,
    ReviewerNotAssignedError,
)
from app.db.models import PullRequest, PullRequestStatus, User
from app.repo.pull_request import PullRequestRepository
from app.repo.user import UserRepository


class PullRequestService:
    def __init__(
        self,
        session: AsyncSession,
        pr_repo: PullRequestRepository,
        user_repo: UserRepository,
    ):
        self.session = session
        self.pr_repo = pr_repo
        self.user_repo = user_repo

    async def create_pull_request_with_reviewers(
        self, pull_request_id: str, pull_request_name: str, author_id: str
    ) -> tuple[PullRequest, list[str]]:
        async with self.session.begin():
            pr = await self.pr_repo.get_by_id(pull_request_id)

            if pr:
                raise PullRequestAlreadyExistsError()

            author = await self.user_repo.get_by_id_with_team(author_id)

            if not author:
                raise NotFoundError()

            candidates = await self.user_repo.get_active_users_by_team(author.team_id)
            candidates = [user for user in candidates if user.id != author_id]

            # Простая логика с рандомным распределением
            reviewers = random.sample(candidates, k=min(2, len(candidates)))

            pull_request_model = PullRequest(
                id=pull_request_id, title=pull_request_name, author_id=author.id
            )

            pull_request = await self.pr_repo.create(pull_request_model)

            for reviewer in reviewers:
                await self.pr_repo.add_reviewer(pull_request.id, reviewer.id)

            return pull_request, [reviewer.id for reviewer in reviewers]

    async def merge_pull_request(self, pull_request_id: str) -> PullRequest:
        async with self.session.begin():
            pull_request = await self.pr_repo.get_by_id_with_reviewer(pull_request_id)

            if not pull_request:
                raise NotFoundError()

            if pull_request.status == PullRequestStatus.OPEN:
                pull_request.status = PullRequestStatus.MERGED
                pull_request.merged_at = datetime.now(timezone.utc)

            return pull_request

    async def reassign_reviewer(
        self, pull_request_id: str, old_reviewer_id: str
    ) -> tuple[PullRequest, str]:
        async with self.session.begin():
            pull_request = await self.pr_repo.get_by_id_with_reviewer(pull_request_id)

            if not pull_request:
                raise NotFoundError()

            if pull_request.status == PullRequestStatus.MERGED:
                raise PullRequestMergedError()

            old_reviewer = await self.user_repo.get_by_id(old_reviewer_id)

            if not old_reviewer:
                raise NotFoundError()

            pull_request_reviewers_ids = {
                reviewer.reviewer_id for reviewer in pull_request.reviewers
            }

            if old_reviewer.id not in pull_request_reviewers_ids:
                raise ReviewerNotAssignedError()

            candidates = await self.user_repo.get_active_users_by_team(
                old_reviewer.team_id
            )

            candidates = [
                user
                for user in candidates
                if user.id != old_reviewer.id
                and user.id != pull_request.author_id
                and user.id not in pull_request_reviewers_ids
            ]

            if not candidates:
                raise NoReviewerCandidatesError()

            new_reviewer = random.choice(candidates)

            reviewer_link = next(
                reviewer
                for reviewer in pull_request.reviewers
                if reviewer.reviewer_id == old_reviewer.id
            )

            reviewer_link.reviewer_id = new_reviewer.id

            return pull_request, new_reviewer.id
