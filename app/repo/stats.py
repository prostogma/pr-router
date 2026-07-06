from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import PullRequestReviewer, User


class StatsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_reviewers_stats(self, limit: int, offset: int):
        stmt = (
            select(
                User.id,
                User.username,
                func.count(PullRequestReviewer.pull_request_id).label("assigned_count")
            )
            .outerjoin(
                PullRequestReviewer,
                User.id == PullRequestReviewer.reviewer_id
            )
            .group_by(User.id, User.username)
            .order_by(func.count(PullRequestReviewer.pull_request_id).desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await self.session.execute(stmt)
        
        return result.all()