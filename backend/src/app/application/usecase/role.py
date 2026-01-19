from app.application.interface.gateway.role import IRoleDBGateway


class RoleUseCase:
    def __init__(
            self,
            role_gateway: IRoleDBGateway,
    ) -> None:
        self.role_gateway = role_gateway
