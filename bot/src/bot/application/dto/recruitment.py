from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class GetRecruitmentDTO:
    id: str
    name: str


@dataclass(slots=True, kw_only=True)
class GetRecruitmentsDTO:
    values: list[GetRecruitmentDTO]
