from sqlalchemy import select

from app.adapter.db.gateway.base import BaseGateway
from app.adapter.db.model import InfoStorage
from app.domain.model import Info


class InfoDBGateway(BaseGateway[Info]):
    async def get(self) -> Info | None:
        stmt = (
            select(InfoStorage)
            .where(InfoStorage.is_info == True)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            return None
        return Info(
            id=model.id,
            about_us_url=model.about_us_url,
            is_info=model.is_info,
            telegram_channel_url=model.telegram_channel_url,
        )
