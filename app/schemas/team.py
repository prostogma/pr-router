from pydantic import BaseModel, ConfigDict


class TeamMemberCreate(BaseModel):
    user_id: str
    username: str
    is_active: bool


class TeamCreate(BaseModel):
    team_name: str
    members: list[TeamMemberCreate]


class TeamMemberResponse(BaseModel):
    user_id: str
    username: str
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class TeamDetailsResponse(BaseModel):
    team_name: str
    members: list[TeamMemberResponse]

    model_config = ConfigDict(from_attributes=True)

class TeamCreateResponse(BaseModel):
    team: TeamDetailsResponse
