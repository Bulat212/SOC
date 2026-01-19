from dataclasses import asdict
from typing import Any

from app.domain.exception.recruitment import RecruitmentNotFound
from app.domain.model import Recruitment


class RecruitmentService:
    def get_recruitment(self, recruitment: Recruitment) -> dict[str, Any,]:
        if not recruitment:
            raise RecruitmentNotFound()
        return asdict(recruitment)
