import pytest

from app.application.dto.status import GetStatusDTO


@pytest.mark.parametrize(
    "data", (
            {
                "id": "1",
                "candidate_id": "1",
                "status": "test",
            },
    ),
)
def test_get_status_dto(data: dict[str, str]) -> None:
    status = GetStatusDTO(**data)
    for key, val in data.items():
        assert getattr(status, key) == val
