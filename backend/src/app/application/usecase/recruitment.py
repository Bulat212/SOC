from app.application.dto.recruitment import (
    GetRecruitmentsDTO,
    GetRecruitmentDTO,
    AddRecruitmentIDDTO,
)
from app.application.interface.gateway.recruitment import IRecruitmentDBGateway
from app.domain.service.recruitment import RecruitmentService


class RecruitmentUseCase:
    def __init__(
            self,
            recruitment_gateway: IRecruitmentDBGateway,
            recruitment_service: RecruitmentService,
    ) -> None:
        self.recruitment_gateway = recruitment_gateway
        self.recruitment_service = recruitment_service

    async def get_all(self) -> GetRecruitmentsDTO:
        recruitments = await self.recruitment_gateway.all()
        result = []
        for val in recruitments:
            data = self.recruitment_service.get_recruitment(val)
            result.append(GetRecruitmentDTO(**data))
        return GetRecruitmentsDTO(
            values=result,
        )

    async def get(self, request: AddRecruitmentIDDTO) -> GetRecruitmentDTO:
        recruitment = await self.recruitment_gateway.get(request.id)
        data = self.recruitment_service.get_recruitment(recruitment)
        return GetRecruitmentDTO(**data)
