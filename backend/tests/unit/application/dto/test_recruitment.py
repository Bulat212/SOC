import pytest

from app.application.dto.recruitment import (
    GetRecruitmentDTO,
    GetRecruitmentsDTO, AddRecruitmentIDDTO,
)


@pytest.mark.parametrize(
    "data", (
            {
                "id": "1",
                "name": "",
            },
    ),
)
def test_get_recruitment_dto(data: dict[str, str]) -> None:
    request = GetRecruitmentDTO(**data)
    for key, val in data.items():
        assert getattr(request, key) == val


@pytest.mark.parametrize(
    "data", (
            [
                GetRecruitmentDTO(
                    id="1" * i,
                    name="test",
                ) for i in range(1, 10)
            ],
            [],
    ),
)
def test_get_recruitments_dto(data: list[GetRecruitmentDTO]) -> None:
    request = GetRecruitmentsDTO(values=data)
    assert isinstance(request.values, list)


@pytest.mark.parametrize(
    "data", (
            {
                "id": "1",
            },
    ),
)
def test_add_recruitment_id_dto(data: dict[str, str]) -> None:
    request = AddRecruitmentIDDTO(**data)
    for key, val in data.items():
        assert getattr(request, key) == val
