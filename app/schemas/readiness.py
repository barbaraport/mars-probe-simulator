from pydantic import BaseModel


class ReadinessResponse(BaseModel):
    api: str
    database: str
