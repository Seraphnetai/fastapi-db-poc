"""Główny plik API"""

import os
from fastapi import FastAPI, status
from datetime import datetime, timezone
from fastapi.responses import Response, RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.exception_handlers import http_exception_handler

from app.utils import validate_input
from app.models import EndpointInputModel, HealthCheck
from app.config import APP_NAME, API_SUMMARY, logger, tags_metadata

app_version = os.getenv("VERSION", "local")

app = FastAPI(
    title=APP_NAME,
    docs_url="/docs",
    description=API_SUMMARY,
    openapi_tags=tags_metadata,
    version=app_version,
    contact={'name': 'AIDA360', 'url': 'https://aida360.pl/', 'email': 'aida@polskapress.pl'}
)
start_date = datetime.now(timezone.utc)
logger.info(f"Application {APP_NAME} started in version: {app_version}")

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
)
instrumentator.instrument(app).expose(
    app,
    include_in_schema=True,
    should_gzip=True,
    tags=["health"],
    summary="metryki Prometheusa",
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    logger.error(f"Error {exc.status_code}: {str(exc.detail)}")
    return await http_exception_handler(request, exc)


@app.get(
    "/docs",
    summary="Dokumentacja",
    status_code=status.HTTP_200_OK,
    response_class=Response,
    tags=["docs"]
)
@app.get(
    "/",
    summary="Strona główna (przekierowanie /docs)",
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


@app.post("/test_endpoint", summary="Krótki opis endpointa", tags=["test_endpoint"])
def test_endpoint(input_: EndpointInputModel):
    """
    Opis endpointa

    Args:
        input_ (EndpointInputModel): opis wejścia

    Returns:
        status.HTTP_CODE: kod odpowiedzi HTTP
    """
    logger.info("Endpoint rozpoczął działanie")

    if validate_input(input_):
        logger.info("Request został zaakceptowany")
        return {"message": input_}
    else:
        logger.warning("Request nie został zaakceptowany")
        return status.HTTP_406_NOT_ACCEPTABLE
