from fastapi import APIRouter
from ....core.http_client import HttpClient
from ....core.config import settings
from ....schemas.exercise import ExerciseCreate, ExerciseUpdate

router = APIRouter(prefix="/exercises", tags=["exercises"])
client = HttpClient(settings.COURSE_SERVICE_URL)


@router.post("/")
async def create_exercise(exercise: ExerciseCreate):
    return await client.request("POST", "/exercises", json=exercise.model_dump())


@router.get("/")
async def list_exercises():
    return await client.request("GET", "/exercises")


@router.get("/{exercise_id}")
async def get_exercise(exercise_id: int):
    return await client.request("GET", f"/exercises/{exercise_id}")


@router.get("/lessons/{lesson_id}/exercises")
async def get_exercises_by_lesson(lesson_id: int):
    return await client.request("GET", f"/lessons/{lesson_id}/exercises")


@router.put("/{exercise_id}")
async def update_exercise(exercise_id: int, exercise: ExerciseUpdate):
    return await client.request("PUT", f"/exercises/{exercise_id}", json=exercise.model_dump())


@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: int):
    return await client.request("DELETE", f"/exercises/{exercise_id}")
