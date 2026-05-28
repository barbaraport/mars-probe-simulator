from app.schemas.setup import SetupRequest, SetupResponse
from app.repositories.probe import ProbeRepository


class SetupService:
    def __init__(
        self,
        repository: ProbeRepository,
    ) -> None:
        self.repository = repository

    def process(
        self,
        setup: SetupRequest,
    ) -> SetupResponse:
        return self.repository.setup(setup)
