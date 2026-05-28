from uuid import uuid4

from app.schemas.setup import SetupRequest, SetupResponse


class ProbeRepository:
    def setup(
        self,
        position: SetupRequest,
    ) -> SetupResponse:
        return SetupResponse(
            id=uuid4(),
            x=0,
            y=0,
            direction=position.direction,
        )
