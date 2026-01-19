from dataclasses import field, dataclass


@dataclass(slots=True, kw_only=True)
class Info:
    id: str | None = field(default=None)
    about_us_url: str | None
    telegram_channel_url: str | None
    is_info: bool
