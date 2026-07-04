from fastapi import FastAPI

from app.api.routers.team import router as team_router

app = FastAPI(title="Pull request router")
app.include_router(team_router)
