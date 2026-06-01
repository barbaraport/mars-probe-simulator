from pydantic import BaseModel, Field

from app.schemas.probe import ProbeResponse


class CheckResponse(BaseModel):
    probes: list[ProbeResponse] = Field(..., description="List of all probes")
