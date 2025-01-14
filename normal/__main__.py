import uvicorn
from normal.config.config import config

if __name__ == "__main__":
    uvicorn.run(
        app="normal.factory:create_app",
        host="0.0.0.0",
        port=8001,
        reload=config.app.debug,
        reload_dirs=["app"],
        factory=True
    )