from bot.application.dto.recruitment import (
    GetRecruitmentsDTO,
    GetRecruitmentDTO,
)
from bot.application.interface.broker.gateway.recruitment import (
    IRecruitmentBrokerGateway,
)


class RecruitmentUseCase:
    def __init__(
            self,
            recruitment_broker_gateway: IRecruitmentBrokerGateway,
    ) -> None:
        self.recruitment_broker_gateway = recruitment_broker_gateway

    async def all(self) -> GetRecruitmentsDTO:
        recruitments = await self.recruitment_broker_gateway.get_recruitments()
        return GetRecruitmentsDTO(
            values=[
                GetRecruitmentDTO(
                    id=val.id,
                    name=val.name,
                )
                for val in recruitments
            ],
        )

    async def check_recruitments(self) -> bool:
        # TODO: Добавить проверку наличия призыва
        return True
