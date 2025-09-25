# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team
from .. import loader, utils
from hikkatl.tl.types import Message
import requests

@loader.tds
class Weather(loader.Module):
    """🌦 Weather — погода"""

    strings = {
        "name": "Weather",
        "no_location": "<b>⚠️ Не удалось определить местоположение.</b>",
        "error": "<b>❌ Ошибка запроса:</b> <code>{}</code>",
        "help": (
            "<b>🌍 Использование Weather:</b>\n"
            "<code>.weather [город]</code> — показать погоду и прогноз на 3 дня\n"
            "Если город не указан — определит по IP\n"
            "<code>.whelp</code> — справка"
        )
    }

    EMOJI_MAP = {
        "clear": "☀️",
        "sun": "☀️",
        "sunny": "☀️",
        "cloud": "☁️",
        "cloudy": "☁️",
        "rain": "🌧",
        "drizzle": "🌦",
        "shower": "🌦",
        "storm": "⛈",
        "thunder": "⛈",
        "snow": "❄️",
        "fog": "🌫",
        "mist": "🌫",
        "haze": "🌫",
        "wind": "💨",
    }

    def get_emoji(self, desc: str) -> str:
        desc = desc.lower()
        for key, emoji in self.EMOJI_MAP.items():
            if key in desc:
                return emoji
        return "🌈"

    @loader.command(ru_doc="Показать погоду с 3-дневным прогнозом. Пример: .weather Москва")
    async def weathercmd(self, message: Message):
        """Показать погоду по городу или по IP, если город не указан"""
        city = utils.get_args_raw(message).strip()
        if not city:
            # Определяем город по IP
            try:
                ip_data = requests.get("http://ip-api.com/json/").json()
                if ip_data.get("status") == "success":
                    city = ip_data.get("city")
                else:
                    await utils.answer(message, self.strings("no_location"), parse_mode="html")
                    return
            except Exception:
                await utils.answer(message, self.strings("no_location"), parse_mode="html")
                return

        try:
            url = f"https://wttr.in/{city}?format=j1"
            resp = requests.get(url)
            if resp.status_code != 200:
                raise Exception(f"HTTP {resp.status_code}")

            data = resp.json()

            current = data["current_condition"][0]
            desc = current["weatherDesc"][0]["value"]
            emoji = self.get_emoji(desc)

            temp_c = current["temp_C"]
            feels_like = current["FeelsLikeC"]
            humidity = current["humidity"]
            wind_kph = current["windspeedKmph"]

            result = f"🌍 <b>Погода в {city}:</b>\n" \
                     f"{emoji} {desc}\n" \
                     f"🌡 Температура: <b>{temp_c}°C</b> (ощущается как {feels_like}°C)\n" \
                     f"💧 Влажность: <b>{humidity}%</b>\n" \
                     f"💨 Ветер: <b>{wind_kph} км/ч</b>\n\n" \
                     f"<b>📅 Прогноз на 3 дня:</b>\n"

            for day in data["weather"][:3]:
                date = day["date"]
                maxtemp = day["maxtempC"]
                mintemp = day["mintempC"]
                day_desc = day["hourly"][4]["weatherDesc"][0]["value"]
                day_emoji = self.get_emoji(day_desc)
                result += f"{date}: {day_emoji} {day_desc}, {mintemp}°C…{maxtemp}°C\n"

            await utils.answer(message, result, parse_mode="html")

        except Exception as e:
            await utils.answer(message, self.strings("error").format(e), parse_mode="html")

    @loader.command(ru_doc="Показать справку по модулю Weather")
    async def whelpcmd(self, message: Message):
        """Показать справку по модулю"""
        await utils.answer(message, self.strings("help"), parse_mode="html")