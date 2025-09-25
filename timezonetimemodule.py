# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team
from .. import loader, utils
import datetime
try:
    from zoneinfo import ZoneInfo
except ImportError:
    # Для старых версий Python
    from backports.zoneinfo import ZoneInfo

@loader.tds
class TimeZoneMod(loader.Module):
    """
    Модуль для показа времени в заданном часовом поясе.
    Сделано от https://t.me/Lptmiop
    """

    strings = {
        "name": "TimeZone",
        "time": "<b>Текущее время для</b> <code>{}</code>:\n<blockquote>{}</blockquote>",
        "error": "❗ <b>Ошибка:</b> {}",
        "help": (
            "<b>📖 Модуль TimeZone</b>\n\n"
            "• <code>.time</code> — показать время в часовом поясе из конфига или указанном аргументом\n"
            "    — пример: <code>.time Europe/London</code>\n\n"
            "<b>Настройки:</b> .config TimeZone\n"
            "• timezone — часовой пояс по умолчанию (например, Europe/Kiev)\n\n"
            "<b>Автор:</b> http://t.me/jdjskskskskkdkmodules"
        )
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "timezone", "Europe/Kiev",
                "Часовой пояс по умолчанию (например, Europe/Kiev)",
                validator=loader.validators.String()
            )
        )

    @loader.command()
    async def timecmd(self, message):
        """Показать текущее время в указанном или дефолтном часовом поясе"""
        args = utils.get_args_raw(message).strip()
        tz_name = args if args else self.config["timezone"]
        try:
            tz = ZoneInfo(tz_name)
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(utils.escape_html(str(e))))
            return

        now = datetime.datetime.now(tz)
        time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        await utils.answer(message, self.strings["time"].format(utils.escape_html(tz_name), time_str))

    @loader.command()
    async def timezonehelpcmd(self, message):
        """Справка по модулю TimeZone"""
        await utils.answer(message, self.strings["help"])