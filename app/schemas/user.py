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
    pull_requests: list[PullRequestStatus]
