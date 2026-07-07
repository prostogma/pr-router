from pydantic import BaseModel

from app.db.models import PullRequestStatus


class UserUpdateActivity(BaseModel):
    user_id: str
    is_active: bool


class UserUpdateActivityDetails(BaseModel):
    user_id: str
    username: str
    team_name: str
    is_active: bool


class UserUpdateActivityResponse(BaseModel):
    user: UserUpdateActivityDetails


class PullRequestShort(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PullRequestStatus


class UserReviewsResponse(BaseModel):
    user_id: str
    pull_requests: list[PullRequestShort]


# Схема для безопасного деактивирования пользователей команды
class UsersDeactivateRequest(BaseModel):
    user_ids: list[str]


class UsersDeactivateResponse(BaseModel):
    users: list[UserUpdateActivityDetails]
