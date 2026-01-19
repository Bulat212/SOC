import pytest

from app.application.dto.user import (
    AddUserDTO,
    GetUserDTO,
    GetUserIDDTO,
    GetUsersIDDTO,
)


@pytest.mark.parametrize(
    "data", (
            {
                "telegram_id": "1",
                "username": "Username",
                "first_name": "FirstName",
                "last_name": "LastName",
                "role": "Role",
            },
            {
                "telegram_id": "1",
                "role": "role",
            },
    ),
)
def test_add_user_dto(data: dict[str, str]) -> None:
    user = AddUserDTO(**data)
    for key, val in data.items():
        assert getattr(user, key) == val


@pytest.mark.parametrize(
    "data", (
            {
                "id": "123",
                "telegram_id": "1",
                "username": "Username",
                "first_name": "FirstName",
                "last_name": "LastName",
                "role": "Role",
                "is_active": True,
            },
            {
                "id": "123",
                "telegram_id": "1",
                "role": "Role",
                "is_active": True,
            },
    ),
)
def test_get_user_dto(data: dict[str, str]) -> None:
    user = GetUserDTO(**data)
    for key, val in data.items():
        assert getattr(user, key) == val


@pytest.mark.parametrize(
    "data", (
            {
                "id": "123",
            },
            {
                "telegram_id": "1",
            },
    ),
)
def test_get_user_id_dto(data: dict[str, str]) -> None:
    user = GetUserIDDTO(**data)
    for key, val in data.items():
        assert getattr(user, key) == val


@pytest.mark.parametrize(
    "data", (
            {
                "id": "123",
                "telegram_id": "1",
            },
            {},
    ),
)
def test_invalid_get_user_id_dto(data: dict[str, str]) -> None:
    with pytest.raises(AttributeError):
        GetUserIDDTO(**data)


@pytest.mark.parametrize(
    "data", (
            [
                GetUserIDDTO(id="1" * i)
                for i in range(1, 10)
            ],
            [
                GetUserIDDTO(telegram_id="1" * 10)
                for i in range(1, 10)

            ],
            [],
    ),
)
def test_get_users_id_dto(data: list[GetUserIDDTO]) -> None:
    user = GetUsersIDDTO(values=data)
    assert isinstance(user.values, list)
