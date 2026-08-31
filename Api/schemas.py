"""HTTP-facing request models.

Field names and types mirror `Engine.chart.BirthRecord` exactly (see that
module's own docstring for what each one means). This module adds no
astrology of its own -- it is the same input the CLI already takes as
`--date/--time/--tz/--lat/--lon/...`, given an HTTP shape.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class BirthInput(BaseModel):
    date: str = Field(..., description="YYYY-MM-DD, proleptic Gregorian")
    time: str = Field(..., description="HH:MM[:SS] local clock time")
    timezone: str = Field(..., description="IANA zone, e.g. Asia/Kolkata")
    latitude: float = Field(..., description="north positive")
    longitude: float = Field(..., description="east positive")
    place_name: str = ""
    name: str = ""
    time_precision: str = "minute"
    time_source: str = "unknown"
    sex: str = "unknown"
    ayanamsa: str = "lahiri"
    house_system: str = "whole_sign"


class CaseInput(BaseModel):
    label: str = Field(..., min_length=1)
    notes: str = ""
    birth: BirthInput
