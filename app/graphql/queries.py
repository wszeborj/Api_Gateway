from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Request, status

from app.core.config import settings

router = APIRouter(prefix="/graphql", tags=["graphql"])

PROGRESS_OPERATIONS: set[str] = {
    "GetUserProgress",
    "GetProgress",
    "GetCompletedCourses",
    "GetUserAchievements",
    "GetUserAchievementsByType",
    "GetUserCertificates",
    "GetCertificate",
    "GetUserStatistics",
    "UpdateUserProgress",
    "CreateAchievement",
    "CreateAchievement",
    "CreateCertificate",
}


def extract_operation_names(query: str) -> set[str]:
    return {
        word.strip()
        for word in query.replace("{", " ").replace("}", " ").split()
        if word.isidentifier()
    }


@router.post("")
async def graphql_proxy(request: Request) -> Any:
    body: dict[str, Any] = await request.json()
    query: str = body.get("query", "")

    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing GraphQL query",
        )

    operation_names = extract_operation_names(query)

    if operation_names & PROGRESS_OPERATIONS:
        service_url = settings.PROGRESS_SERVICE_URL
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown GraphQL operation",
        )

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            service_url,
            json=body,
            headers={
                "Content-Type": "application/json",
            },
        )

    return response.json()


# @app.post("/graphql")
# async def graphql_proxy(request: Request):
#     body = await request.json()
#     query = body.get("query", "")
#
#     if any(option in query for option in PROGRESS_OPERATIONS):
#         service_url = ...
#
#     else:
#         return {'errors': [{'message': 'unknown graphql operation'}]}
#     async with httpx.AsyncClient() as client:
#         respnse = await client.post(
#
#             service_url,
#             json=body,
#         return response.json()
#     )
