from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, problem, profile, collaboration

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])

api_router.include_router(problem.router, prefix="/problem", tags=["problem"])
api_router.include_router(collaboration.router, prefix="/collaboration", tags=["collaboration"])