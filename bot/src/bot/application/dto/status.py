from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class GetStatusDTO:
    id: str
    candidate_id: str
    status: str
