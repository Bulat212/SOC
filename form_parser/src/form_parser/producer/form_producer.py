from dto.form import FormDataDTO
from dataclasses import asdict


class FormProducer:

    def __init__(self, broker):
        self._broker = broker

    async def update_form_data(
        self,
        form_data: FormDataDTO,
    ) -> None:
        await self._broker.publish(
            message=asdict(form_data),
            queue="update_candidate_from_yandex",
        )
