from fastapi import APIRouter, Depends

from app.tools.essential.security.auth.dependencies import require_token_lifetime
from app.tools.router.post_titles import post_titles_router
from app.tools.router.user_names import user_names_router

router = APIRouter(dependencies=[Depends(require_token_lifetime)])
app_router = router

router.include_router(user_names_router, prefix='/user_names')
router.include_router(post_titles_router, prefix='/post_titles')
