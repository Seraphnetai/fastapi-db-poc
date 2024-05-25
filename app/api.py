"""Główny plik API"""

import os

from fastapi import FastAPI, status
from datetime import datetime, timezone
from fastapi.responses import Response, RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler

from app.utils import validate_input
from app.models import EndpointInputModel, HealthCheck
from app.config import APP_NAME, API_SUMMARY, logger, tags_metadata, SessionLocal, engine, Base
from app.crud import create_qdrant_collection

app_version = os.getenv("VERSION", "local")

Base.metadata.create_all(bind=engine)

# Ensure Qdrant collection is created
create_qdrant_collection()


app = FastAPI(
    title=APP_NAME,
    docs_url="/docs",
    description=API_SUMMARY,
    openapi_tags=tags_metadata,
    version=app_version,
    contact={'name': 'Dev', 'url': 'https://www.seraphnet.ai/', 'email': 'dev@seraphnet.ai'}
)
start_date = datetime.now(timezone.utc)
logger.info(f"Application {APP_NAME} started in version: {app_version}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    logger.error(f"Error {exc.status_code}: {str(exc.detail)}")
    return await http_exception_handler(request, exc)


@app.get(
    "/docs",
    summary="API documentation",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    tags=["docs"]
)
@app.get(
    "/",
    summary="Main site (redirect to API documentation)",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    response_class=Response,
)
async def redirect():
    return RedirectResponse("/docs")


@app.get("/health", summary="Healthcheck", response_model=HealthCheck, tags=["health"])
def health():
    return {
        "status": "Server available",
        "up_since": str(start_date),
        "uptime": str(datetime.now(timezone.utc) - start_date),
    }


@app.post("/test_endpoint", summary="Short endpoint description", tags=["test_endpoint"])
def test_endpoint(input_: EndpointInputModel):
    """
    Endpoint description

    Args:
        input_ (EndpointInputModel): input model

    Returns:
        status.HTTP_CODE: status code
    """
    logger.info("POST /test_endpoint called")

    if validate_input(input_):
        logger.info("Request accepted")
        return {"message": input_}
    else:
        logger.warning("Request not accepted")
        return status.HTTP_406_NOT_ACCEPTABLE
