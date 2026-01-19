from abc import abstractmethod
from collections.abc import AsyncIterator
from typing import Protocol

from app.domain.model import (
    Candidate,
    CandidateQuote,
    CandidateDocument,
)


class ICandidateDBGateway(Protocol):
    @abstractmethod
    async def insert(self, candidate: Candidate) -> Candidate: ...

    @abstractmethod
    async def get(self,
            candidate_id: str | None,
            telegram_id: str | None,
    ) -> Candidate | None: ...

    @abstractmethod
    async def update(self, candidate: Candidate) -> Candidate: ...

    @abstractmethod
    async def get_total(self) -> int: ...

    @abstractmethod
    async def all(
            self,
            limit: int,
            offset: int,
    ) -> AsyncIterator[Candidate]: ...


    @abstractmethod
    async def get_by_recruitment_id(self, recruitment_id: str, limit: int, offset: int): ...
    
    @abstractmethod
    async def get_by_recruitment_id_all(self, recruitment_id: str): ...

    @abstractmethod
    async def delete(self, candidate_id: str): ...

class ICandidateQuoteGateway(Protocol):
    @abstractmethod
    async def insert(self, quote: CandidateQuote) -> CandidateQuote: ...

    @abstractmethod
    async def get(
            self,
            delegate_id: str,
    ) -> CandidateQuote: ...

    @abstractmethod
    async def update(self, quote: CandidateQuote) -> CandidateQuote: ...


class ICandidateFormDBGateway(Protocol):
    @abstractmethod
    async def insert(
            self,
            document: CandidateDocument,
    ) -> CandidateDocument: ...

    @abstractmethod
    async def get(
            self,
            candidate_id: str,
    ) -> CandidateDocument | None: ...

    @abstractmethod
    async def update(
            self,
            document: CandidateDocument,
    ) -> CandidateDocument: ...

    @abstractmethod
    async def delete(self, candidate_id: str): ...


class ICandidateStatementDBGateway(ICandidateFormDBGateway, Protocol):
    ...


class ICandidateApprovalDBGateway(ICandidateFormDBGateway, Protocol):
    ...


class ICandidateFormDBGateway(ICandidateFormDBGateway, Protocol):
    ...
