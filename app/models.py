"""Modele danych dla endpointów API"""

from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer

from .config import Base


class ExampleModel(Base):
    """
    Example model
    """
    __tablename__ = "example_model"

    id = Column(Integer, primary_key=True, index=True)


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
