import json
import datetime
from dataclasses import asdict

from bot.domain.model.delegate import Delegate
from faststream.rabbit.message import RabbitMessage

from bot.adapter.broker.gateway.base import BaseBrokerGateway
from bot.constants import TIMEOUT


class DelegateBrokerGateway(BaseBrokerGateway):
    async def get_delegate(self, telegram_id: str) -> Delegate | None:
        try:
            msg: RabbitMessage = await self.broker.request(
                message={
                    "telegram_id": telegram_id,
                },
                queue="get_delegate",
                timeout=TIMEOUT,
            )
        except TimeoutError:
            return None
        body = json.loads(msg.body)
        
        start_date_str = body.get("start_date")
        end_date_str = body.get("end_date")
        
        body["start_date"] = (
            datetime.datetime.fromisoformat(start_date_str).date()
            if start_date_str else None
        )
        body["end_date"] = (
            datetime.datetime.fromisoformat(end_date_str).date()
            if end_date_str else None
        )
        return Delegate(**body)


    async def update_delegate(self, delegate: Delegate) -> None:
        data = dict()
        for key, val in asdict(delegate).items():
            data[key] = val
        await self.broker.publish(
            message=data,
            queue="update_delegate",
        )

    
    async def add_delegate(self, delegate: Delegate) -> None:
        data = dict()
        for key, value in asdict(delegate).items():
            if key in ("start_date", "end_date") and value:
                
                data[key] = value.isoformat()
                continue
            data[key] = value
        await self.broker.publish(
            message=data,
            queue="add_delegate",
        )