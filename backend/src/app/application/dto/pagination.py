from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class PaginationDTO:
    limit: int
    offset: int


@dataclass(slots=True, kw_only=True)
class GetCandidatesByRecruitmentDTO:
    recruitment_id: str
    limit: int
    offset: int