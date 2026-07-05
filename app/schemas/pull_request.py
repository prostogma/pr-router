from datetime import datetime

from pydantic import BaseModel

from app.db.models import PullRequestStatus


class PullRequestCreate(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str

class PullRequestResponse(BaseModel):
    pull_request_id: str
    pull_request_name: str
    author_id: str
    status: PullRequestStatus
    assigned_reviewers: list[str]
    
class PullRequestMergeResponse(PullRequestResponse):
    mergedAt: datetime

class PullRequestCreateResponse(BaseModel):
    pr: PullRequestResponse

class PullRequestMergedResponse(BaseModel):
    pr: PullRequestMergeResponse
    


