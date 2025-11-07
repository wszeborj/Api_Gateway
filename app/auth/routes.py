from urllib.parse import quote_plus, urlencode

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse

from app.auth.config import oauth
from app.core.config import settings


auth_router = APIRouter()


@auth_router.get("/login")
async def login(request: Request) -> JSONResponse:
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    if 'id_token' in request.session:
        return JSONResponse(
            content={
                "status": "already_logged_in",
                "message": "You are already logged",
                "user": {
                    "email": request.session.get('userinfo', {}).get('email'),
                    "name": request.session.get('userinfo', {}).get('name')
                },
                "available_endpoints": {
                    "profile": "/profile",
                    "protected": "/protected",
                    "admin": "/admin",
                    "logout": "/logout"
                }
            },
            status_code=200
        )

    return await oauth.auth0.authorize_redirect( # type: ignore[no-any-return]
        request,
        redirect_uri=request.url_for("callback"),
        audience=settings.AUTH0_API_AUDIENCE
    )


@auth_router.get("/signup")
async def signup(request: Request) -> JSONResponse:
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    if 'id_token' in request.session:
        return JSONResponse(
            content={
                "status": "already_logged_in",
                "message": "Już jesteś zalogowany",
                "user": {
                    "email": request.session.get('userinfo', {}).get('email'),
                    "name": request.session.get('userinfo', {}).get('name')
                }
            },
            status_code=200
        )

    return await oauth.auth0.authorize_redirect( # type: ignore[no-any-return]
        request,
        redirect_uri=request.url_for("callback"),
        screen_hint="signup",
        audience=settings.AUTH0_API_AUDIENCE
    )


@auth_router.get("/logout")
def logout(request: Request) -> RedirectResponse:
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    request.session.clear()

    logout_url = (
            f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
            + urlencode({
        "returnTo": request.url_for("home"),
        "client_id": settings.AUTH0_CLIENT_ID
    }, quote_via=quote_plus)
    )

    return RedirectResponse(url=logout_url)


@auth_router.get("/callback")
async def callback(request: Request) -> JSONResponse:
    try:
        token = await oauth.auth0.authorize_access_token(request)
        # Store `access_token`, `id_token`, and `userinfo` in session
        request.session['access_token'] = token['access_token']
        request.session['id_token'] = token['id_token']
        request.session['userinfo'] = token['userinfo']

        return JSONResponse(
            content={
                "success": True,
                "message": "Succesfully logged!",
                "tokens": {
                    "access_token": token['access_token'],
                    "id_token": token['id_token'],
                },
                "userinfo": dict(token['userinfo'])
            },
            status_code=200,
        )
    except Exception as e:
        return JSONResponse(
            content={
                "success": False,
                "error": str(e),
                "hint": "Try again: /login"
            },
            status_code=400
        )