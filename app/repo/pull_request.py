from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import PullRequest, PullRequestReviewer


class PullRequestRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, pull_request: PullRequest) -> PullRequest:
        self.session.add(pull_request)
        return pull_request

    async def get_by_id(self, pr_id: str) -> PullRequest | None:
        stmt = (
            select(PullRequest)
            .where(PullRequest.id == pr_id)
            .options(
                selectinload(PullRequest.author), selectinload(PullRequest.reviewers)
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_reviewer(self, reviewer_id: str) -> list[PullRequest]:
        stmt = (
            select(PullRequest)
            .join(
                PullRequestReviewer,
                PullRequestReviewer.pull_request_id == PullRequest.id,
            )
            .where(PullRequestReviewer.id == reviewer_id)
            .options(selectinload(PullRequest.author))
        )

        result = await self.session.execute(stmt)
        return result.scalars().all()
