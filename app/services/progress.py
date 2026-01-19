from fastapi import APIRouter

from ....core.config import settings
from ....core.graphql_client import GraphQLClient
from ....schemas.progress import (
    CreateAchievementInput,
    CreateCertificateInput,
    UpdateProgressInput,
)

router = APIRouter(prefix="/progress", tags=["progress"])
client = GraphQLClient(settings.PROGRESS_SERVICE_URL)

# ============ GET ============


# @router.get("/user/{user_id}/courses")
async def get_user_progress(user_id: int):
    query = """
    query GetUserProgress($userId: Int!) {
      getUserProgress(userId: $userId) {
        id
        courseId
        status
        completionPercentage
        totalTimeSpent
        lastAccessedAt
        startedAt
        completedAt
        notes
      }
    }
    """
    variables = {"userId": user_id}
    data = await client.query(query, variables)
    return data.get("getUserProgress", [])


@router.get("/user/{user_id}/course/{course_id}")
async def get_course_progress(user_id: int, course_id: int):
    query = """
    query GetProgress($userId: Int!, $courseId: Int!) {
      getProgress(userId: $userId, courseId: $courseId) {
        id
        courseId
        status
        completionPercentage
        totalTimeSpent
        lastAccessedAt
        startedAt
        completedAt
        notes
      }
    }
    """
    variables = {"userId": user_id, "courseId": course_id}

    data = await client.query(query, variables)
    return data.get("getProgress")


@router.get("/user/{user_id}/completed-courses")
async def get_completed_courses(user_id: int):
    query = """
    query GetCompletedCourses($userId: Int!) {
      getCompletedCourses(userId: $userId)
    }
    """
    variables = {"userId": user_id}

    data = await client.query(query, variables)
    return {"completed_course_ids": data.get("getCompletedCourses", [])}


@router.get("/user/{user_id}/achievements")
async def get_user_achievements(user_id: int, achievement_type: str | None = None):
    query = """
    query GetUserAchievements($userId: Int!, $type: String) {
      getUserAchievements(userId: $userId, achievementType: $type) {
        id
        achievementType
        achievementName
        description
        earnedAt
      }
    }
    """
    variables = {"userId": user_id, "type": achievement_type}

    data = await client.query(query, variables)
    return data.get("getUserAchievements", [])


@router.get("/user/{user_id}/certificates")
async def get_user_certificates(user_id: int):
    query = """
    query GetUserCertificates($userId: Int!) {
      getUserCertificates(userId: $userId) {
        id
        courseId
        finalScore
        grade
        completionTime
        expiresAt
        pdfUrl
      }
    }
    """

    variables = {"userId": user_id}

    data = await client.query(query, variables)
    return data.get("getUserCertificates", [])


@router.get("/user/{user_id}/certificate/{course_id}")
async def get_certificate(user_id: int, course_id: int):

    query = """
    query GetCertificate($userId: Int!, $courseId: Int!) {
      getCertificate(userId: $userId, courseId: $courseId) {
        id
        courseId
        finalScore
        grade
        completionTime
        pdfUrl
      }
    }
    """

    variables = {"userId": user_id, "courseId": course_id}

    data = await client.query(query, variables)
    return data.get("getCertificate")


@router.get("/user/{user_id}/statistics")
async def get_user_statistics(user_id: int):
    query = """
    query GetUserStatistics($userId: Int!) {
      getUserStatistics(userId: $userId) {
        userId
        totalCompletedLessons
        totalCoursesInProgress
        totalCompletedCourses
        totalCertificates
        totalAchievements
        totalTimeSpentSeconds
        averageCompletionPercentage
      }
    }
    """
    variables = {"userId": user_id}

    data = await client.query(query, variables)
    return data.get("getUserStatistics")


# ============ POST/PUT ENDPOINTS (Mutations) ============


@router.post("/user/{user_id}/progress")
async def create_progress(user_id: int, input_data: UpdateProgressInput):
    mutation = """
    mutation UpdateUserProgress($userId: Int!, $input: UpdateProgressInput!) {
      updateUserProgress(userId: $userId, input: $input) {
        id
        courseId
        status
        completionPercentage
        totalTimeSpent
        lastAccessedAt
      }
    }
    """

    input_dict = input_data.model_dump(by_alias=True, exclude_none=True)
    variables = {"userId": user_id, "input": input_dict}

    data = await client.query(mutation, variables)
    return data.get("updateUserProgress")


@router.put("/user/{user_id}/progress")
async def update_progress(user_id: int, input_data: UpdateProgressInput):
    return await create_progress(user_id, input_data)


@router.post("/user/{user_id}/achievement")
async def create_achievement(user_id: int, input_data: CreateAchievementInput):
    mutation = """
    mutation CreateAchievement($userId: Int!, $input: CreateAchievementInput!) {
      createAchievement(userId: $userId, input: $input) {
        id
        achievementType
        achievementName
        description
        earnedAt
      }
    }
    """
    input_dict = input_data.model_dump(by_alias=True, exclude_none=True)
    variables = {"userId": user_id, "input": input_dict}

    data = await client.query(mutation, variables)
    return data.get("createAchievement")


@router.post("/user/{user_id}/certificate")
async def create_certificate(user_id: int, input_data: CreateCertificateInput):

    mutation = """
    mutation CreateCertificate($userId: Int!, $input: CreateCertificateInput!) {
      createCertificate(userId: $userId, input: $input) {
        id
        courseId
        finalScore
        grade
        completionTime
        pdfUrl
      }
    }
    """
    input_dict = input_data.model_dump(by_alias=True, exclude_none=True)
    variables = {"userId": user_id, "input": input_dict}

    data = await client.query(mutation, variables)
    return data.get("createCertificate")
