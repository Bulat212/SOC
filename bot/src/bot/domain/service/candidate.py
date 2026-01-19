import datetime
from dataclasses import asdict

from bot.domain.exception.candidate import CandidateNotFound
from bot.domain.exception.recruitment import RecruitmentNotFound
from bot.domain.model import Recruitment
from bot.domain.model.candidate import Candidate


class CandidateService:
    def update_candidate(
            self,
            candidate: Candidate,
            **data: str | float | datetime.date,
    ) -> Candidate:
        data["birthdate"] = datetime.datetime.strptime(
            data.get("birthdate"),
            "%d.%m.%Y",
        ).isoformat()
        data["graduation_date"] = datetime.datetime.strptime(
            data.get("graduation_date"),
            "%d.%m.%Y",
        ).isoformat()
        for key, val in data.items():
            if val is None:
                continue
            setattr(candidate, key, val)
        return candidate

    def add_candidate(self, **data: str | float | datetime.date) -> Candidate:
        candidate = Candidate(**data)
        return candidate

    def get_candidate(
            self,
            recruitment: Recruitment | None,
            candidate: Candidate | None,
    ) -> dict[str, str | datetime.date | float | None]:
        if not recruitment:
            raise RecruitmentNotFound()
        if not candidate:
            raise CandidateNotFound()
        data = asdict(candidate)
        if "recruitment_id" in data:
            del data["recruitment_id"]
        if "username" in data:
            del data["username"]
        data["recruitment"] = recruitment.name
        return data
