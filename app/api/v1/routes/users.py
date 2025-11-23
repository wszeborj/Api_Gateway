from typing import Any, Dict

from fastapi import APIRouter

from ....core.config import settings
from ....core.http_client import HttpClient
from ....schemas.user import (
    UserCreate,
    UserUpdate,
)

router = APIRouter(prefix="/users", tags=["users"])
client = HttpClient(settings.USER_SERVICE_URL)


@router.post("/", response_model=Dict[str, Any])
async def create_user(user: UserCreate) -> Dict[str, Any]:
    return await client.request(
        "POST",
        "/users",
        json=user.model_dump(),
    )


@router.get("/", response_model=Dict[str, Any])
async def get_users() -> Dict[str, Any]:
    return await client.request("GET", "/users")


@router.get("/{user_id}", response_model=Dict[str, Any])
async def get_user(user_id: int) -> Dict[str, Any]:
    return await client.request("GET", f"/users/{user_id}")


@router.get("/auth0/{auth0_id}", response_model=Dict[str, Any])
async def get_user_by_auth0_id(auth0_id: int) -> Dict[str, Any]:
    return await client.request("GET", f"/users/auth0/{auth0_id}")


@router.get("/role/{role}", response_model=Dict[str, Any])
async def get_users_by_role(role: str) -> Dict[str, Any]:
    return await client.request("GET", f"/users/role/{role}")


@router.put("/{user_id}", response_model=Dict[str, Any])
async def update_user(user_id: int, user: UserUpdate) -> Dict[str, Any]:
    return await client.request(
        "PUT",
        f"/users/{user_id}",
        json=user.model_dump(),
    )


@router.delete("/{user_id}", response_model=Dict[str, Any])
async def delete_user(user_id: int) -> Dict[str, Any]:
    return await client.request("DELETE", f"/users/{user_id}")
