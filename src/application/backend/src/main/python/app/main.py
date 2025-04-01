from fastapi import FastAPI
from .api.endpoints import router as api_router

app = FastAPI(title="ANS Operators Search API")

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)