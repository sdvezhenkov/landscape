from fastapi.security import OAuth2AuthorizationCodeBearer

from app.tools.essential.env.get_env import get_env

SCOPES = {
    'landscape:user_names:run': 'Run Get User Names',
    'landscape:user_names:show': 'Show User Names State',
    'landscape:post_titles:run': 'Run Get Post Titles',
    'landscape:post_titles:show': 'Show Post Titles State',
}

oauth2 = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f'{get_env("LSC_OIDC_ISSUER")}/protocol/openid-connect/auth',
    tokenUrl=f'{get_env("LSC_OIDC_ISSUER")}/protocol/openid-connect/token',
    scopes=SCOPES,
    scheme_name='OAuth2',
    auto_error=False,
)
