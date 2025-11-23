from fastapi import APIRouter

from ....core.config import settings
from ....core.http_client import HttpClient
from ....schemas.course import CourseCreate, CourseUpdate

router = APIRouter(prefix="/courses", tags=["courses"])
client = HttpClient(settings.COURSE_SERVICE_URL)


@router.post("/")
async def create_course(course: CourseCreate):
    return await client.request("POST", "/courses", json=course.model_dump())


@router.get("/")
async def list_courses():
    return await client.request("GET", "/courses")


@router.get("/{course_id}")
async def get_course(course_id: int):
    return await client.request("GET", f"/courses/{course_id}")


@router.put("/{course_id}")
async def update_course(course_id: int, course: CourseUpdate):
    return await client.request(
        "PUT", f"/courses/{course_id}", json=course.model_dump()
    )


@router.delete("/{course_id}")
async def delete_course(course_id: int):
    return await client.request("DELETE", f"/courses/{course_id}")
