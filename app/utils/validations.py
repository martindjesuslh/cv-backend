from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime


class DateRange(BaseModel):
    dates: List[str]

    @field_validator("dates")
    def validate_dates_order(cls, v):
        if len(v) != 2:
            raise ValueError("Exactly 2 dates required: [start, end]")
        try:
            start_date = datetime.fromisoformat(v[0].replace("Z", "+00:00"))
            end_date = datetime.fromisoformat(v[1].replace("Z", "+00:00"))
        except (ValueError, TypeError):
            raise ValueError("Dates must be in valid ISO 8601 format")

        if start_date >= end_date:
            raise ValueError("Start date must be before end date")

        return v
