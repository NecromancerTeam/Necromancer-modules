# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team
import random
import aiohttp
from .. import loader, utils
from hikkatl.tl.types import Message

@loader.tds
class FunModule(loader.Module):
    """🎉 FunModule — забавные команды: 8ball, choose, fact"""

    strings = {
        "name": "FunModule",
        "answers_en": [
            "It is certain.", "Without a doubt.", "You may rely on it.",
            "Ask again later.", "Cannot predict now.", "Don't count on it.",
            "My sources say no.", "Very doubtful."
        ],
        "answers_ru": [
            "Бесспорно.", "Это точно.", "Можешь на это положиться.",
            "Спроси позже.", "Сейчас не ясно.", "Вряд ли.",
            "Мои источники говорят нет.", "Очень сомнительно."
        ],
        "no_question": "❗ <b>Укажи вопрос для 8ball.</b>\n<code>.8ball Будет ли завтра солнце?</code>",
        "eightball": "<b>🎱 8ball:</b>\n<blockquote>{}</blockquote>",
        "no_options": "❗ <b>Укажи варианты через <code>;</code>.</b>\n<code>.choose кофе;чай;вода</code>",
        "choose": "<b>🎲 Я выбираю:</b>\n<blockquote>{}</blockquote>",
        "fact_error": "⚠️ <b>Не удалось получить факт.</b>",
        "fact": "<b>🔎 Факт:</b>\n<blockquote>{}</blockquote>",
        "help": (
            "<b>🎉 FunModule — Справка:</b>\n\n"
            "<b>📌 Команды:</b>\n"
            "🔹 <code>.8ball &lt;вопрос&gt;</code> — ответ шара судьбы\n"
            "🔹 <code>.choose вариант1;вариант2</code> — случайный выбор\n"
            "🔹 <code>.fact</code> — случайный факт от numbersapi.com\n"
            "🔹 <code>.funhelp</code> — справка по модулю\n\n"
            "<i>Разработчик: @jdjskskskskkdkmodules</i>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "language", "en",
                "Язык ответов (en/ru)",
                validator=loader.validators.Choice(["en", "ru"])
            ),
            loader.ConfigValue(
                "fact_type", "trivia",
                "Тип факта (trivia/math/date/year)",
                validator=loader.validators.Choice(["trivia", "math", "date", "year"])
            ),
        )

    @loader.command(
        ru_doc="Шар судьбы. Пример: .8ball Будет ли дождь?",
        description="8ball — ответ на ваш вопрос"
    )
    async def eightballcmd(self, message: Message):
        text = utils.get_args_raw(message)
        if not text:
            return await utils.answer(message, self.strings("no_question"))
        lang = self.config["language"]
        answers = self.strings[f"answers_{lang}"]
        answer = random.choice(answers)
        await utils.answer(message, self.strings("eightball").format(answer))

    @loader.command(
        ru_doc="Выбор из списка. Пример: .choose a;b;c",
        description="choose — выбирает случайный вариант"
    )
    async def choosecmd(self, message: Message):
        raw = utils.get_args_raw(message)
        if ";" not in raw:
            return await utils.answer(message, self.strings("no_options"))
        opts = [o.strip() for o in raw.split(";") if o.strip()]
        if not opts:
            return await utils.answer(message, self.strings("no_options"))
        choice = random.choice(opts)
        await utils.answer(message, self.strings("choose").format(choice))

    @loader.command(
        ru_doc="Случайный факт. Пример: .fact",
        description="fact — получает факт по Numbers API"
    )
    async def factcmd(self, message: Message):
        url = f"http://numbersapi.com/random/{self.config['fact_type']}?json"
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url) as r:
                    data = await r.json()
            fact = data.get("text")
            await utils.answer(message, self.strings("fact").format(fact))
        except:
            await utils.answer(message, self.strings("fact_error"))

    @loader.command(
        ru_doc="Справка по FunModule",
        description=".funhelp — справка по модулю"
    )
    async def funhelpcmd(self, message: Message):
        await utils.answer(message, self.strings("help"))