from .heartbeat import router as heartbeat_router
from .posts import router as posts_router
from .codes import router as codes_router

__all__ = ("heartbeat_router","posts_router","codes_router")

routers = (heartbeat_router,posts_router,codes_router)
