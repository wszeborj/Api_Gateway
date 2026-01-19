from fastapi import APIRouter

from ...api.v1.routes import courses, exercises, graphql, lessons, users

api_v1_router: APIRouter = APIRouter(prefix="/api/v1")

api_v1_router.include_router(courses.router)
api_v1_router.include_router(lessons.router)
api_v1_router.include_router(exercises.router)
api_v1_router.include_router(users.router)
api_v1_router.include_router(graphql.router)
