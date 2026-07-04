from fastapi import status


class AppError(Exception):
    """Базовое исключение для всего приложения"""

    message = "Internal server error"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = "INTERNAL_SERVER_ERROR"

    def __init__(self, message: str | None = None):
        if message:
            self.message = message

        super().__init__(self.message)


class TeamAlreadyExistsError(AppError):
    status_code = 400
    code = "TEAM_EXISTS"

    def __init__(self, name: str):
        super().__init__(f"{name} already exists")
