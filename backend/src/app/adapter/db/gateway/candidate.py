from dataclasses import asdict

from sqlalchemy import insert, select, or_, update, delete

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import (
    CandidateStorage,
    CandidateFormStorage,
    CandidateStatementStorage,
    CandidateApprovalStorage,
    CandidateFormDataStorage,
)
from app.domain.model import Candidate, CandidateDocument, CandidateFormData


class CandidateDBGateway(BaseGateway[Candidate]):
    async def insert(self, candidate: Candidate) -> Candidate:
        data = dict()
        attrs = ("is_form", "is_statement", "is_approval")
        for key, val in asdict(candidate).items():
            if key in attrs:
                continue
            data[key] = val
        stmt = (
            insert(CandidateStorage)
            .values(**data)
        )
        await self.session.execute(stmt)
        return candidate

    async def get(self,
            candidate_id: str | None,
            telegram_id: str | None,
    ) -> Candidate | None:
        form_exists = (
            select(1)
            .where(CandidateFormStorage.candidate_id == CandidateStorage.id)
            .exists()
        )
        statement_exists = (
            select(1)
            .where(
                CandidateStatementStorage.candidate_id == CandidateStorage.id,
            )
            .exists()
        )
        approval_exists = (
            select(1)
            .where(
                CandidateApprovalStorage.candidate_id == CandidateStorage.id,
            )
            .exists()
        )
        stmt = (
            select(
                CandidateStorage,
                form_exists.label("is_form"),
                statement_exists.label("is_statement"),
                approval_exists.label("is_approval"),
            )
            .where(
                or_(
                    CandidateStorage.telegram_id == telegram_id,
                    CandidateStorage.id == candidate_id,
                ),
            )
        )

        result = await self.session.execute(stmt)
        row = result.fetchone()
        if not row:
            return None

        model = row[0]
        return Candidate(
            id=model.id,
            telegram_id=model.telegram_id,
            recruitment_id=model.recruitment_id,
            nationality=model.nationality,
            first_name=model.first_name,
            last_name=model.last_name,
            patronymic=model.patronymic,
            birthdate=model.birthdate,
            military_station=model.military_station,
            military_station_address=model.military_station_address,
            university=model.university,
            average_score=model.average_score,
            find_out=model.find_out,
            phone_number=model.phone_number,
            direction_training=model.direction_training,
            subject=model.subject,
            graduation_date=model.graduation_date,
            is_form=row.is_form,
            is_statement=row.is_statement,
            is_approval=row.is_approval,
        )

    async def update(self, candidate: Candidate) -> Candidate:
        data = dict()
        attrs = ("is_form", "is_statement", "is_approval", "id")
        for key, val in asdict(candidate).items():
            if key in attrs:
                continue
            data[key] = val
        stmt = (
            update(CandidateStorage)
            .values(**data)
            .where(CandidateStorage.id == candidate.id)
        )
        await self.session.execute(stmt)
        return candidate

    async def get_by_recruitment_id(self, recruitment_id: str, limit: int, offset: int):
        stmt = (select(CandidateStorage).where(CandidateStorage.recruitment_id == recruitment_id).limit(limit).offset(offset))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_recruitment_id_all(self, recruitment_id: str):
        stmt = (select(CandidateStorage).where(CandidateStorage.recruitment_id == recruitment_id))
        result = await self.session.execute(stmt)
        return result.scalars().all()  
    
    async def delete(self, candidate_id: str):
        stmt = (
            delete(CandidateStorage)
            .where(CandidateStorage.id == candidate_id)
        )
        await self.session.execute(stmt)


class CandidateYandexFormGateway(BaseGateway[CandidateFormData]):
    async def insert(self, candidate_form: CandidateFormData) -> CandidateFormData:
        data = dict()
        for key, val in asdict(candidate_form).items():
            data[key] = val
        stmt = (
            insert(CandidateFormDataStorage)
            .values(**data)
        )
        await self.session.execute(stmt)
        return candidate_form


    async def get(self,
            # candidate_id: str | None,
            telegram_id: str | None,
    ) -> CandidateFormData | None:
        stmt = (
            select(
                CandidateFormDataStorage,
            )
            .where(
                or_(
                    CandidateFormDataStorage.telegram_id == telegram_id,
                    # CandidateFormDataStorage.id == candidate_id,
                ),
            )
        )

        result = await self.session.execute(stmt)
        row = result.fetchone()
        if not row:
            return None

        model = row[0]
        return CandidateFormData(
            id=model.id,
            candidate_id=model.candidate_id,
            telegram_id=model.telegram_id,
            first_name=model.first_name,
            last_name=model.last_name,
            patronymic=model.patronymic,
            birthplace=model.birthplace,
            birthdate=model.birthdate,
            graduation_date=model.graduation_date,
            nationality=model.nationality,
            tg_username=model.tg_username,
            mail=model.mail,
            registration_address=model.registration_address,
            actual_address=model.actual_address,
            family_status=model.family_status,
            military_station=model.military_station,
            health_category=model.health_category,
            university=model.university,
            diploma=model.diploma,
            date_issue_diploma=model.date_issue_diploma,
            direction_training=model.direction_training,
            average_score=model.average_score,
            diploma_topic=model.diploma_topic,
            international_articles=model.international_articles,
            patents=model.patents,
            vac_articles=model.vac_articles,
            rationalization=model.rationalization,
            rinc_articles=model.rinc_articles,
            registration_certificates=model.registration_certificates,
            scientific_work_experience=model.scientific_work_experience,
            international_olympiads=model.international_olympiads,
            president_scholarship=model.president_scholarship,
            russian_olympiads=model.russian_olympiads,
            government_scholarship=model.government_scholarship,
            grant=model.grant,
            regional_olympiads=model.regional_olympiads,
            city_olympiads=model.city_olympiads,
            postgraduate_diploma=model.postgraduate_diploma,
            unused_academic_degree=model.unused_academic_degree,
            useful_academic_degree=model.useful_academic_degree,
            commercial_experience=model.commercial_experience,
            OPK_experience=model.OPK_experience,
            exp_research_assistant=model.exp_research_assistant,
            areas_research=model.areas_research,
            programming_languages=model.programming_languages,
            programs=model.programs,
            secret=model.secret,
            height=model.height,
            weight=model.weight,
            sporting_achievements=model.sporting_achievements,
            other_sporting_achievements=model.other_sporting_achievements,
            short_run=model.short_run,
            long_run=model.long_run,
            pull_ups=model.pull_ups,
            chronic_diseases=model.chronic_diseases,
            tattoos=model.tattoos,
            find_out=model.find_out,
        )
    

    async def update(self, candidate_form: CandidateFormData) -> CandidateFormData:
        data = dict()
        for key, val in asdict(candidate_form).items():
            data[key] = val
        stmt = (
            update(CandidateFormDataStorage)
            .values(**data)
            .where(CandidateFormDataStorage.id == candidate_form.id)
        )
        await self.session.execute(stmt)
        return candidate_form


class _BaseDocumentDBGateway:
    def __init__(
            self,
            cls: "CandidateFormDBGateway | CandidateApprovalDBGateway | CandidateStatementDBGateway",
    ) -> None:
        self.session = cls.session

    async def insert(
            self,
            document: CandidateDocument,
            storage: type[CandidateFormStorage
                          | CandidateApprovalStorage
                          | CandidateStatementStorage],
    ) -> CandidateDocument:
        stmt = (
            insert(storage)
            .values(**asdict(document))
        )
        await self.session.execute(stmt)
        return document

    async def get(
            self,
            candidate_id: str,
            storage: type[CandidateFormStorage
                          | CandidateApprovalStorage
                          | CandidateStatementStorage],
    ) -> CandidateDocument | None:
        stmt = (
            select(storage)
            .join(
                CandidateStorage,
                CandidateStorage.id == storage.candidate_id,
            )
            .where(
                or_(
                    CandidateStorage.id == candidate_id,
                    CandidateStorage.telegram_id == candidate_id,
                ),
            )
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return CandidateDocument(
            id=model.id,
            name=model.name,
            url=model.url,
            candidate_id=model.candidate_id,
        )

    async def update(
            self,
            document: CandidateDocument,
            storage: type[CandidateFormStorage
                          | CandidateApprovalStorage
                          | CandidateStatementStorage],
    ) -> CandidateDocument:
        stmt = (
            update(storage)
            .values(
                name=document.name,
                url=document.url,
            )
            .where(
                storage.candidate_id == document.candidate_id
                # select(CandidateStorage.id)
                # .where(
                #     or_(
                #         CandidateStorage.id == document.candidate_id,
                #         CandidateStorage.telegram_id == document.candidate_id,
                #     ),
                # )
                # .exists(),
            )
            
        )
        await self.session.execute(stmt)
        return document
    

    async def delete(
            self,
            candidate_id: str,
            storage: type[CandidateFormStorage
                          | CandidateApprovalStorage
                          | CandidateStatementStorage],
    ):
        stmt = (
            delete(storage)
            .where(storage.candidate_id == candidate_id)
        )
        await self.session.execute(stmt)


class CandidateFormDBGateway(BaseGateway[CandidateDocument]):
    async def insert(
            self,
            document: CandidateDocument,
    ) -> CandidateDocument:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.insert(document, CandidateFormStorage)
        return result

    async def get(
            self,
            candidate_id: str,
    ) -> CandidateDocument | None:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.get(candidate_id, CandidateFormStorage)
        return result

    async def update(
            self,
            document: CandidateDocument,
    ) -> CandidateDocument:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.update(document, CandidateFormStorage)
        return result
    
    async def delete(
            self,
            candidate_id: str,
    ):
        cls = _BaseDocumentDBGateway(self)
        await cls.delete(candidate_id, CandidateFormStorage)


class CandidateApprovalDBGateway(BaseGateway[CandidateDocument]):
    async def insert(
            self,
            document: CandidateDocument,
    ) -> CandidateDocument:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.insert(document, CandidateApprovalStorage)
        return result

    async def get(
            self,
            candidate_id: str,
    ) -> CandidateDocument | None:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.get(candidate_id, CandidateApprovalStorage)
        return result

    async def update(
            self,
            document: CandidateDocument,
    ) -> CandidateDocument:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.update(document, CandidateApprovalStorage)
        return result
    
    async def delete(
            self,
            candidate_id: str,
    ):
        cls = _BaseDocumentDBGateway(self)
        await cls.delete(candidate_id, CandidateApprovalStorage)


class CandidateStatementDBGateway(BaseGateway[CandidateDocument]):
    async def insert(
            self,
            document: CandidateDocument,
    ) -> CandidateDocument:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.insert(document, CandidateStatementStorage)
        return result

    async def get(
            self,
            candidate_id: str,
    ) -> CandidateDocument | None:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.get(candidate_id, CandidateStatementStorage)
        return result

    async def update(
            self,
            document: CandidateDocument,
    ) -> CandidateDocument:
        cls = _BaseDocumentDBGateway(self)
        result = await cls.update(document, CandidateStatementStorage)
        return result
    
    async def delete(
            self,
            candidate_id: str,
    ):
        cls = _BaseDocumentDBGateway(self)
        await cls.delete(candidate_id, CandidateStatementStorage)
