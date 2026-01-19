from typing import Any

from app.domain.exception.role import RoleNotFound
from app.domain.model import Role


class RoleService:
    def get_role(self, role: Role) -> dict[str, Any]:
        if not role:
            raise RoleNotFound()
        return {
            "id": role.id,
            "name": role.name.value.lower(),
        }

    def get_role_id(self, role: Role) -> str:
        if not role:
            raise RoleNotFound()
        return role.id
