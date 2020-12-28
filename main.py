import uvicorn

import settings
from fastapi import FastAPI, Header, HTTPException
from starlette.middleware.cors import CORSMiddleware

# v1
from src.v1.report import ReportRouter

app = FastAPI(
    title="Mock Project - Public Transportation Optimization",
    description="This is API documentation of PTO",
    version="1.0.0",
    docs_url="/v1/analytics/docs",
    openapi_url="/v1/analytics/openapi.json"
)

origins = [
    "http://localhost:3000",
    "http://localhost.com:3000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    ReportRouter,
    prefix="/v1/report",
    tags=['report'],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"},
    }
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
