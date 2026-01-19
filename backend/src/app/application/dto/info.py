from dataclasses import dataclass


@dataclass(slots=True, kw_only=True)
class GetInfoDTO:
    id: str
    about_us_url: str | None
    telegram_channel_url: str | None
    is_info: bool
