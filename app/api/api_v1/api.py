from fastapi import APIRouter

from app.api.api_v1.endpoints import posts, auth

api_router = APIRouter()
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"]
                          )