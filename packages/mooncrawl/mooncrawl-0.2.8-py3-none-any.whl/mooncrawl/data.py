from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class StatsUpdateRequest(BaseModel):
    dashboard_id: str
    timescales: List[str]
    token: str


@dataclass
class DateRange:
    start_time: datetime
    end_time: datetime
    include_start: bool
    include_end: bool


class PingResponse(BaseModel):
    """
    Schema for ping response
    """

    status: str


class VersionResponse(BaseModel):
    """
    Schema for responses on /version endpoint
    """

    version: str


class NowResponse(BaseModel):
    """
    Schema for responses on /now endpoint
    """

    epoch_time: float


class QueryDataUpdate(BaseModel):
    file_type: str
    query: str
    params: Dict[str, Any] = Field(default_factory=dict)


class TokenURIs(BaseModel):
    token_id: str
    token_uri: str
    block_number: str
    block_timestamp: str
    address: str
