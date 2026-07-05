from pydantic import BaseModel


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
