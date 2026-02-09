import base64
import datetime
from dataclasses import asdict, fields

from app.domain.exception.candidate import (
    CandidateNotFound,
    CandidateQuoteNotFound,
)
from app.domain.exception.document import DocumentNotFound
from app.domain.model import Candidate, CandidateQuote, CandidateDocument, CandidateFormData


class CandidateService:
    def update_path(self, path: str, filename: str) -> str:
        new_path = f"{"/".join(path.split("/")[:-1])}/{filename}"
        return new_path

    def get_path(self, endpoint: str, url: str, bucket_name: str) -> str:
        path = url.replace(f"{endpoint}/", "").replace(f"{bucket_name}/", "")
        return path

    def get_file(self, file: str) -> bytes:
        return base64.b64decode(file)

    def get_document(self, document: CandidateDocument) -> dict[str, str]:
        if not document:
            raise DocumentNotFound()
        return asdict(document)

    def get_path_document(
            self,
            name: str,
            recruitment: str,
            **data: str | datetime.datetime,
    ) -> str:
        candidate_id = data.get("id")
        return (
            f"{recruitment}/{datetime.date.today().year}/"
            f"{data.get("last_name")} {data.get("first_name")} "
            f"{data.get("patronymic")} ({candidate_id[:6]})/"
            f"{name}"
        )

    def get_url(self, endpoint: str, bucket: str, path: str) -> str:
        return f"{endpoint}/{bucket}/{path}"

    def update_document(self,
            document: CandidateDocument,
            **data: str,
    ) -> CandidateDocument:
        context = dict()
        for val in fields(CandidateDocument):
            context[val.name] = data.get(val.name)

        for key, val in context.items():
            if not val:
                continue
            setattr(document, key, val)
        return document

    def add_document(self, **data: str) -> CandidateDocument:
        context = dict()
        for val in fields(CandidateDocument):
            context[val.name] = data.get(val.name)
        document = CandidateDocument(**context)
        return document

    def add_candidate(
            self,
            **data: str | float | datetime.date | None,
    ) -> Candidate:
        context = dict()
        for val in fields(Candidate):
            context[val.name] = data.get(val.name)

        candidate = Candidate(**context)
        return candidate
    
    def add_candidate_data_from_form(
            self,
            **data: str | float | datetime.date | None,
    ) -> CandidateFormData:
        context = dict()
        for val in fields(CandidateFormData):
            context[val.name] = data.get(val.name)

        candidate_form = CandidateFormData(**context)
        return candidate_form

    def get_candidate(
            self,
            candidate: Candidate,
    ) -> dict[str, str | float | datetime.date | None]:
        data = dict()
        for key, val in asdict(candidate).items():
            if key == "is_form" and val is None:
                data[key] = True
                continue
            if key in ("is_statement", "is_approval") and val is None:
                data[key] = False
                continue
            data[key] = val
        return data
    

    def get_candidate_from_form(
            self,
            candidate: Candidate,
    ) -> dict[str, str | float | datetime.date | None]:
        data = dict()
        for key, val in asdict(candidate).items():
            if key == "is_form" and val is None:
                data[key] = True
                continue
            if key in ("is_statement", "is_approval") and val is None:
                data[key] = False
                continue
            data[key] = val
        return data

    def get_candidate_id(self, candidate: Candidate) -> str:
        if not candidate:
            raise CandidateNotFound()
        return candidate.id

    def update_candidate(
            self,
            candidate: Candidate | None,
            **data: str | float | datetime.date | None,
    ) -> Candidate:
        if candidate is None:
            raise CandidateNotFound()

        for key, val in data.items():
            if val is None:
                continue
            # Проверяем, что атрибут существует в объекте candidate
            if not hasattr(candidate, key):
                continue
            
            setattr(candidate, key, val)

        return candidate
    
    def update_candidate_from_form(
            self,
            candidate: Candidate | None,
            **data: str | float | datetime.date | None,
    ):
        if candidate is None:
            raise CandidateNotFound()

        result = dict()

        for key, val in asdict(candidate).items():
            if key == "is_form" and val is None:
                result[key] = True
                continue
            if key in ("is_statement", "is_approval") and val is None:
                result[key] = False
                continue
            result[key] = val

        # Обновляем переданными значениями
        for key, value in data.items():
            if value is not None:
                result[key] = value    

        return result
    

    def update_candidate_form(
            self,
            candidate_form: CandidateFormData | None,
            **data: str | float | datetime.date | None,
    ) -> CandidateFormData:
        if candidate_form is None:
            raise CandidateNotFound()

        for key, val in data.items():
            if val is None:
                continue
            # Проверяем, что атрибут существует в объекте candidate_form
            if not hasattr(candidate_form, key):
                continue
            
            setattr(candidate_form, key, val)

        return candidate_form

class CandidateQuoteService:
    def add_candidate_quote(
            self,
            **data: str | int | datetime.date | None,
    ) -> CandidateQuote:
        quote = CandidateQuote(**data)
        return quote

    def get_candidate_quote(
            self,
            quote: CandidateQuote | None,
    ) -> dict[str, str | int | datetime.date | None]:
        if quote is None:
            raise CandidateQuoteNotFound()
        data = asdict(quote)
        return data

    def update_candidate_quote(
            self,
            quote: CandidateQuote | None,
            **data: str | int | datetime.date | None,
    ) -> CandidateQuote:
        if quote is None:
            raise CandidateQuoteNotFound()

        for key, val in data.items():
            if val is None:
                continue
            setattr(quote, key, val)

        return quote
