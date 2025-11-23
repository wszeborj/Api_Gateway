from fastapi import APIRouter

from ....core.config import settings
from ....core.http_client import HttpClient
from ....schemas.lesson import LessonCreate, LessonUpdate

router = APIRouter(prefix="/lessons", tags=["lessons"])
client = HttpClient(settings.COURSE_SERVICE_URL)


@router.post("/")
async def create_lesson(lesson: LessonCreate):
    return await client.request("POST", "/lessons", json=lesson.model_dump())


@router.get("/")
async def list_lessons():
    return await client.request("GET", "/lessons")


@router.get("/{lesson_id}")
async def get_lesson(lesson_id: int):
    return await client.request("GET", f"/lessons/{lesson_id}")


@router.get("/courses/{course_id}/lessons")
async def get_lessons_by_course(course_id: int):
    return await client.request("GET", f"/courses/{course_id}/lessons")


@router.put("/{lesson_id}")
async def update_lesson(lesson_id: int, lesson: LessonUpdate):
    return await client.request(
        "PUT", f"/lessons/{lesson_id}", json=lesson.model_dump()
    )


@router.delete("/{lesson_id}")
async def delete_lesson(lesson_id: int):
    return await client.request("DELETE", f"/lessons/{lesson_id}")
