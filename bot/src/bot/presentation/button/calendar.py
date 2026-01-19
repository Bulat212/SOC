import datetime

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import (
    Calendar,
    CalendarScope,
    CalendarUserConfig,
)
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarScopeView,
    CalendarYearsView,
    CalendarMonthView,
    CalendarDaysView,
)
from aiogram_dialog.widgets.text import Text, Format
from babel.dates import get_month_names, get_day_names

SELECTED_DAYS_KEY = "selected_dates"


class WeekDay(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: datetime.date = data["date"]
        locale = manager.event.from_user.language_code
        return get_day_names(
            width="short", context="stand-alone", locale=locale,
        )[selected_date.weekday()].title()


class Month(Text):
    async def _render_text(self, data, manager: DialogManager) -> str:
        selected_date: datetime.date = data["date"]
        locale = manager.event.from_user.language_code
        return get_month_names(
            "wide", context="stand-alone", locale=locale,
        )[selected_date.month].title()


class RegistrationCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        return {
            CalendarScope.YEARS: CalendarYearsView(
                self._item_callback_data,
                year_text=Format("{date:%Y}"),
                this_year_text=Format("🟢{date:%Y}"),
                next_page_text=Format("{date:%Y} ➡️"),
                prev_page_text=Format("⬅️ {date:%Y}"),
            ),
            CalendarScope.MONTHS: CalendarMonthView(
                self._item_callback_data,
                month_text=Month(),
                this_month_text="🟢" + Month(),
                next_year_text=Format("{date:%Y} ➡️"),
                prev_year_text=Format("⬅️ {date:%Y}"),
            ),
            CalendarScope.DAYS: CalendarDaysView(
                self._item_callback_data,
                today_text=Format("🟢{date:%d}"),
                header_text=Month(),
                weekday_text=WeekDay(),
                next_month_text=Month() + " ➡️",
                prev_month_text="⬅️ " + Month(),
            ),
        }

    async def _get_user_config(
            self,
            data: dict,
            manager: DialogManager,
    ) -> CalendarUserConfig:
        current_date = datetime.date.today()
        min_date = current_date.replace(year=current_date.year - 30)
        return CalendarUserConfig(
            min_date=min_date,
            max_date=current_date,
        )


class GraduationCalendar(RegistrationCalendar):
    async def _get_user_config(
            self,
            data: dict,
            manager: DialogManager,
    ) -> CalendarUserConfig:
        return CalendarUserConfig()
