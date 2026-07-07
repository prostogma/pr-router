from fastapi import status


class AppError(Exception):
    """Базовое исключение для всего приложения"""

    message = "Internal server error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "INTERNAL_SERVER_ERROR"

    def __init__(self, message: str | None = None):
        self.message = message or self.message

        super().__init__(self.message)


class NotFoundError(AppError):
    message = "resource not found"
    status_code = 404
    code = "NOT_FOUND"


class TeamAlreadyExistsError(AppError):
    status_code = 400
    code = "TEAM_EXISTS"

    def __init__(self, name: str):
        super().__init__(f"{name} already exists")


class UsersFromDifferentTeamsError(AppError):
    status_code = 400
    code = "DIFFERENT_TEAMS"
    message = "All users selected for deactivation must belong the same team"


class PullRequestConflictError(AppError):
    status_code = 409
    code = "CONFLICT_ERROR"
    message = "Conflict with the current state of the resource"


class PullRequestAlreadyExistsError(PullRequestConflictError):
    message = "PR id already exists"
    code = "PR_EXISTS"


class PullRequestMergedError(PullRequestConflictError):
    message = "cannot reassign on merged PR"
    code = "PR_MERGED"


class ReviewerNotAssignedError(PullRequestConflictError):
    message = "reviewer is not assigned to this PR"
    code = "NOT_ASSIGNED"


class NoReviewerCandidatesError(PullRequestConflictError):
    message = "no active replacement candidate in team"
    code = "NO_CANDIDATE"
