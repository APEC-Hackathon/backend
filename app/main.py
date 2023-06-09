from fastapi import FastAPI 
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.api.api_v1.sockets import socket_router
from app.core.config import settings


app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# if settings.BACKEND_CORS_ORIGINS:
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(socket_router, prefix='/ws')
app.include_router(api_router, prefix=settings.API_V1_STR)