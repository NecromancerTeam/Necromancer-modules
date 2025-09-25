# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team
from .. import loader, utils
import random

@loader.tds
class LuckRollMod(loader.Module):
    """Модуль для рандомных бросков, монетки, удачи и предсказаний."""

    strings = {
        "name": "LuckRoll",
        "cfg_lang": "✅ Язык установлен: {}",
        "cfg_emoji": "✅ Эмодзи: {}",
        "cfg_default_range": "✅ Диапазон по умолчанию: {}",
        "roll_usage": "Использование: .roll [до] или .roll [от] [до]",
        "roll_result": "🎲 Выпало: {}",
        "luck_result": "🌠 Уровень удачи: {}%",
        "coin_usage": "Использование: .coin",
        "coin_heads": "🪙 Орёл",
        "coin_tails": "🪙 Решка",
        "luckmsg_usage": "Использование: .luckmsg",
        "luck_messages": [
            "Сегодня ты найдёшь то, что потерял!",
            "Будь осторожен в решениях сегодня.",
            "Ожидай приятных новостей!",
            "День не будет простым, но ты справишься.",
            "Не жди чуда — будь им."
        ],
        "language_usage": "Использование: .language <ru/en>",
        "language_set": "✅ Язык изменён на: {}"
    }

    def __init__(self):
        # Конфигурация модуля
        self.config = loader.ModuleConfig(
            loader.ConfigValue("default_range", 6, lambda: self.strings("cfg_default_range")),
            loader.ConfigValue("emoji", True, lambda: self.strings("cfg_emoji")),
            loader.ConfigValue("language", "ru", lambda: self.strings("cfg_lang")),
        )

    @loader.command(ru_doc="Бросить кубик", description=".roll [до] или .roll [от] [до]")
    async def rollcmd(self, message):
        """Случайное число"""
        args = utils.get_args(message)
        emoji = "🎲 " if self.config["emoji"] else ""
        try:
            if len(args) == 0:
                low, high = 1, int(self.config["default_range"])
            elif len(args) == 1:
                low, high = 1, int(args[0])
            elif len(args) == 2:
                low, high = int(args[0]), int(args[1])
            else:
                return await utils.answer(message, self.strings("roll_usage"))
            if low > high:
                low, high = high, low
            result = random.randint(low, high)
            await utils.answer(message, f"{emoji}{self.strings('roll_result').split(': ')[0]}: {result}")
        except Exception:
            return await utils.answer(message, self.strings("roll_usage"))

    @loader.command(ru_doc="Уровень удачи", description=".luck — показать удачу")
    async def luckcmd(self, message):
        """Показывает уровень удачи"""
        result = random.randint(0, 100)
        emoji = "🌠 " if self.config["emoji"] else ""
        await utils.answer(message, f"{emoji}{self.strings('luck_result').split(': ')[0]}: {result}%")

    @loader.command(ru_doc="Случайное предсказание", description=".luckmsg — предсказание")
    async def luckmsgcmd(self, message):
        """Случайное сообщение удачи"""
        msg = random.choice(self.strings("luck_messages"))
        await utils.answer(message, msg)

    @loader.command(ru_doc="Подбросить монетку", description=".coin — орёл или решка")
    async def coincmd(self, message):
        """Имитирует подбрасывание монеты"""
        if random.choice([True, False]):
            await utils.answer(message, self.strings("coin_heads"))
        else:
            await utils.answer(message, self.strings("coin_tails"))

    @loader.command(ru_doc="Сменить язык", description=".language <ru/en> — смена языка")
    async def languagecmd(self, message):
        """Изменяет язык модуля"""
        arg = utils.get_args_raw(message).lower()
        if arg not in ["ru", "en"]:
            return await utils.answer(message, self.strings("language_usage"))
        self.config["language"] = arg
        await utils.answer(message, self.strings("language_set").format(arg))

