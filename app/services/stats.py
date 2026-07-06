from app.repo.stats import StatsRepository


class StatsService:
    def __init__(self, stats_repo: StatsRepository):
        self.stats_repo = stats_repo

    async def get_reviewers_stats(self, limit: int, offset: int):
        return await self.stats_repo.get_reviewers_stats(limit, offset)
