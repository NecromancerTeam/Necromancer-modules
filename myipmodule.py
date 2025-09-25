# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team
from .. import loader, utils
from hikkatl.tl.types import Message
import requests

@loader.tds
class MyIP(loader.Module):
    """Модуль для получения вашего публичного IP-адреса"""

    strings = {
        "name": "MyIP",
        "fetch_error": "<b>❌ Не удалось получить IP-адрес.</b>",
        "ip_info": "<b>Ваш публичный IP-адрес:</b> <code>{}</code>",
        "help": (
            "<b>Использование:</b>\n"
            "<code>.myip</code> — показать ваш текущий публичный IP-адрес"
        )
    }

    @loader.command(ru_doc="Показать ваш текущий публичный IP-адрес")
    async def myipcmd(self, message: Message):
        """Показывает ваш текущий публичный IP-адрес"""
        try:
            response = requests.get("https://api.ipify.org?format=text", timeout=10)
            response.raise_for_status()
            ip = response.text.strip()
            await utils.answer(message, self.strings("ip_info").format(ip), parse_mode="html")
        except Exception:
            await utils.answer(message, self.strings("fetch_error"), parse_mode="html")

    @loader.command(ru_doc="Показать справку по модулю MyIP")
    async def myiphelpcmd(self, message: Message):
        """Показать справку по модулю"""
        await utils.answer(message, self.strings("help"), parse_mode="html")