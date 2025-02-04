import math
from typing import Annotated
from pydantic import BaseModel, Field, field_validator
from typing import List


class RouteInput(BaseModel):
    """
    Model for validating route input.
    """

    start_lat: Annotated[float, Field(ge=-90, le=90)] = ...
    start_lon: Annotated[float, Field(ge=-180, le=180)] = ...
    end_lat: Annotated[float, Field(ge=-90, le=90)] = ...
    end_lon: Annotated[float, Field(ge=-180, le=180)] = ...

    @field_validator("start_lat", "start_lon", "end_lat", "end_lon")
    def no_nan(cls, v):
        if math.isnan(v):
            raise ValueError("Coordinates cannot be NaN.")
        return v


class RouteOutput(BaseModel):
    """
    Model for returning route results.
    """

    raw_nodes: List[int]
    text_instructions: str
