from pydantic import BaseModel, Field


class ReadyResponse(BaseModel):
    api: bool = Field(default=False, description="API readiness status")
    database: bool = Field(default=False, description="Database readiness status")
