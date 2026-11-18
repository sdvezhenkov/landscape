from pathlib import Path
from typing import Any

from fastapi import APIRouter, FastAPI, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

from app.tools.essential.env.get_env import get_env


def get_docs_router(
        app: FastAPI,
) -> APIRouter:
    router = APIRouter()

    @router.get('/')
    async def root(request: Request) -> RedirectResponse:
        return RedirectResponse(url=request.url_for('swagger').path)

    @router.get('/favicon.ico')
    async def favicon() -> FileResponse:
        return FileResponse(Path(__file__).parent / 'static' / 'favicon.ico', media_type='image/x-icon')

    @router.get('/openapi.json')
    async def open_api(request: Request) -> dict[str, Any]:
        open_api = get_openapi(
            title=get_env('LSC_PROJECT_NAME'),
            version='1.0.0',
            routes=app.routes,
            servers=[{'url': request.scope.get('root_path') or '/'}],
        )
        open_api["security"] = [{"OAuth2": []}]
        return open_api

    @router.get('/docs')
    async def swagger(request: Request) -> HTMLResponse:
        swagger = get_swagger_ui_html(
            title=get_env('LSC_PROJECT_NAME'),
            openapi_url=request.url_for('open_api').path,
            swagger_favicon_url=request.url_for('favicon').path,
            oauth2_redirect_url=request.url_for('oauth_redirect').path,
            init_oauth={
                'clientId': get_env('LSC_OAUTH_CLIENT_ID'),
                'usePkceWithAuthorizationCodeGrant': True,
            },
        )
        return swagger

    @router.get('/docs/oauth2-redirect')
    async def oauth_redirect() -> HTMLResponse:
        return get_swagger_ui_oauth2_redirect_html()

    @router.get('/redoc')
    async def redoc(request: Request) -> HTMLResponse:
        redoc = get_redoc_html(
            title=get_env('LSC_PROJECT_NAME'),
            openapi_url=request.url_for('open_api').path,
            redoc_favicon_url=request.url_for('favicon').path,
        )
        return redoc

    return router
