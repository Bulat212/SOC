import datetime
import json
from dataclasses import asdict

from bot.presentation.schema.candidate import GetCandidateSchema
from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT
from bot.domain.model.candidate import Candidate
from bot.domain.model.document import Document, DocumentBuff


class CandidateBrokerGateway(BaseBrokerGateway):
    async def add_candidate(self, candidate: Candidate) -> GetCandidateSchema:
        data = dict()
        for key, value in asdict(candidate).items():
            if key in ("is_form", "is_statement", "is_approval"):
                continue
            if key in ("birthdate", "graduation_date"):
                data[key] = value.isoformat()
                continue
            data[key] = value
        # await self.broker.publish(
        #     message=data,
        #     queue="add_candidate",
        # )
        msg: GetCandidateSchema = await self.broker.request(
            message=data,
            queue="add_candidate",
            timeout=5,
        )
        body = json.loads(msg.body)
        return GetCandidateSchema(**body)

    async def get_candidate(self, telegram_id: str) -> Candidate | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "telegram_id": telegram_id,
                },
                queue="get_candidate",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        body = json.loads(msg.body)
        body["birthdate"] = datetime.datetime.fromisoformat(
            body.get("birthdate"),
        ).date()
        body["graduation_date"] = datetime.datetime.fromisoformat(
            body.get("graduation_date"),
        ).date()
        return Candidate(**body)

    async def load_candidates(self, recruitment_id: str, limit: int, offset: int):
        payload = {
            "recruitment_id": recruitment_id,
            "limit": limit,
            "offset": offset,
        }
        try:
            msg: RabbitMessage = await self.broker.request(
                message=payload,
                queue="get_candidates_by_recruitment",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None

        try:
            body = json.loads(msg.body)
        except Exception:
            return getattr(msg, "body", msg)

        return body

    async def update_candidate(self, candidate: Candidate) -> GetCandidateSchema:
        data = dict()
        for key, val in asdict(candidate).items():
            if val is None:
                continue
            if key in ("is_form", "is_statement", "is_approval"):
                continue
            data[key] = val
        # await self.broker.publish(
        #     message=data,
        #     queue="update_candidate",
        # )
        msg: GetCandidateSchema = await self.broker.request(
            message=data,
            queue="update_candidate",
            timeout=5,
        )
        body = json.loads(msg.body)
        return GetCandidateSchema(**body)

    async def get_candidate_document(
            self,
            telegram_id: str,
            name: str,
    ) -> Document | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "telegram_id": telegram_id,
                    "name": name,
                },
                queue="get_candidate_document",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        data = json.loads(msg.body)
        return Document(**data)

    async def add_or_update_form(
            self,
            document: DocumentBuff,
    ) -> None:
        await self._add_or_update_document(
            document=document,
            queue="add_or_update_form",
        )

    async def add_or_update_approval(
            self,
            document: DocumentBuff,
    ) -> None:
        await self._add_or_update_document(
            document=document,
            queue="add_or_update_approval",
        )

    async def add_or_update_statement(
            self,
            document: DocumentBuff,
    ) -> None:
        await self._add_or_update_document(
            document=document,
            queue="add_or_update_statement",
        )

    async def _add_or_update_document(
            self,
            document: DocumentBuff,
            queue: str,
    ) -> None:
        await self.broker.publish(
            message={
                "name": document.name,
                "file": document.file,
                "filename": document.filename,
                "candidate_id": document.candidate_id,
            },
            queue=queue,
        )

    async def delete(self, candidate_id: str, telegram_id: str):
        await self.broker.publish(
            message={
                "candidate_id": candidate_id,
                "telegram_id": telegram_id,
            },
            queue="delete_candidate"
        )

    async def new_registration_soc(
        self,
        form_data: Candidate,
    ) -> None:
        await self.broker.publish(
            message=asdict(form_data),
            queue="new_registration_queue",
        )