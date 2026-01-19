import re
from typing import Any, Optional

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

APP_STATS_OPERATIONS: set[str] = {
    "",
}


def extract_operation_name(query: str) -> Optional[str]:
    """
    Extracts GraphQL operation name from query.
    Supports:
    - query Name(...)
    - mutation Name(...)
    """
    if not query:
        return None

    pattern = re.compile(
        r"""
        (query|mutation|subscription)
        \s+
        (?P<name>[A-Za-z_][A-Za-z0-9_]*)
        """,
        re.VERBOSE | re.MULTILINE,
    )

    match = pattern.search(query)
    if not match:
        return None

    return match.group("name")


@router.post("")
async def graphql_proxy(request: Request) -> Any:
    body: dict[str, Any] = await request.json()
    query: str = body.get("query", "")

    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing GraphQL query",
        )

    operation_name = extract_operation_name(query)

    print("RAW QUERY:", query)
    print("EXTRACTED OPERATION:", operation_name)
    if operation_name in PROGRESS_OPERATIONS:
        service_url = settings.PROGRESS_SERVICE_URL

    if operation_name in APP_STATS_OPERATIONS:
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
