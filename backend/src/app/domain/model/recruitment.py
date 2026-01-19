from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True)
class Recruitment:
    id: str | None = field(default=None)
    name: str
