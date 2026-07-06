from pydantic import BaseModel, Field


class ReviewerStatsItem(BaseModel):
    user_id: str
    username: str
    assigned_count: int


class ReviewerStatsResponse(BaseModel):
    reviewers: list[ReviewerStatsItem]


class StatsPaginationParams(BaseModel):
    limit: int = Field(
        default=30, ge=1, le=100, description="Количество элементов на странице"
    )
    offset: int = Field(default=0, ge=0, description="Смещение (пропуск элементов)")
