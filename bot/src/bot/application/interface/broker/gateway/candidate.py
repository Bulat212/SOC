from bot.domain.model.candidate import Candidate
from bot.domain.model.document import Document, DocumentBuff


class ICandidateBrokerGateway:
    async def add_candidate(self, candidate: Candidate) -> None: ...

    async def get_candidate(self, telegram_id: str) -> Candidate | None: ...
    
    async def load_candidates(self, recruitment_id: str, limit: int, offset: int): ...

    async def update_candidate(self, candidate: Candidate) -> None: ...

    async def get_candidate_document(
            self,
            telegram_id: str,
            name: str,
    ) -> Document | None: ...

    async def add_or_update_form(
            self,
            document: DocumentBuff,
    ) -> None: ...

    async def add_or_update_approval(
            self,
            document: DocumentBuff,
    ) -> None: ...

    async def add_or_update_statement(
            self,
            document: DocumentBuff,
    ) -> None: ...

    async def delete(self, candidate_id: str): ...