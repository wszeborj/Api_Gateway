from fastapi import APIRouter
from ...api.v1.routes import courses, lessons, exercises

api_v1_router: APIRouter = APIRouter(prefix="/v1")

api_v1_router.include_router(courses.router)
api_v1_router.include_router(lessons.router)
api_v1_router.include_router(exercises.router)
