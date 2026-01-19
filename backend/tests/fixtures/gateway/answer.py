from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_answer_db_gateway() -> AsyncMock:
    gateway = AsyncMock()
    gateway.insert = AsyncMock()
    gateway.get = AsyncMock()
    return gateway
