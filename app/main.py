from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging

from app.api.routers.team import router as team_router
from app.api.routers.user import router as user_router
from app.core.exceptions import AppError

logger = logging.getLogger(__name__)

app = FastAPI(title="Pull request router")
app.include_router(team_router)
app.include_router(user_router)


@app.exception_handler(AppError)
async def app_exception_handler(request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception occured: %s", exc, exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Unexpected error occured on the server",
            }
        },
    )
