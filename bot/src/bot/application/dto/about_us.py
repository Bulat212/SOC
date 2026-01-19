from dataclasses import dataclass


@dataclass(slots=True)
class GetAboutUsDTO:
    about_us_url: str
