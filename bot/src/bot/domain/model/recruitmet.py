from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class Recruitment:
    id: str
    name: str
