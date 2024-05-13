"""Modele danych dla endpointów API"""

from typing import Optional
from pydantic import BaseModel, Field


class EndpointInputModel(BaseModel):
    """
    Model wejścia request body
    """
    input_field: Optional[str] = Field(description="Opis elementu wejścia")


class HealthCheck(BaseModel):
    """
    Model wyjścia endpointa health
    """
    status: str = Field(description="Server status")
    up_since: str = Field(description="Server initialization time in UTC")
    uptime: str = Field(description="Server running time")
