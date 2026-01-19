import pytest

from app.application.dto.answer import AddAnswerDTO, GetAnswerDTO, AnswerIDDTO


@pytest.mark.parametrize(
    "data", {
        "question_id": "123",
        "answer": "answer",
    },
)
def add_answer_dto(data: dict[str, str]) -> None:
    request = AddAnswerDTO(**data)
    for key, val in data.items():
        assert getattr(request, key) == val


@pytest.mark.parametrize(
    "data", {
        "id": "123",
        "question_id": "123",
        "answer": "answer",
    },
)
def test_get_answer_dto(data: dict[str, str]) -> None:
    request = GetAnswerDTO(**data)
    for key, val in data.items():
        assert getattr(request, key) == val


@pytest.mark.parametrize(
    "data", {
        "id": "123",
    },
)
def test_answer_id_dto(data: dict[str, str]) -> None:
    request = AnswerIDDTO(**data)
    for key, val in data.items():
        assert getattr(request, key) == val
