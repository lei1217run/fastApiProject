import uvicorn
from app.config.config import config

if __name__ == "__main__":
    uvicorn.run(
        app="app.factory:create_app",
        host="0.0.0.0",
        port=8000,
        reload=config.app.debug,
        reload_dirs=["app"],
        factory=True
    )