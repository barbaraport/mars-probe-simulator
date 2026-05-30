from pydantic import BaseModel

from app.schemas.probe import ProbeResponse


class CheckResponse(BaseModel):
    probes: list[ProbeResponse]
