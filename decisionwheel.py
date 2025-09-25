# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team
import random
from .. import loader, utils

@loader.tds
class DecisionWheelMod(loader.Module):
    """🎡 Колесо решений"""
    strings = {
        "name": "DecisionWheel",
        "no_options": "❗ Укажите варианты через `;`\nПример: `.wheel Пойти; Поспать; Учиться`",
        "chosen": "🎡 Колесо решений выбрало:\n👉 <b>{}</b>"
    }

    @loader.command(ru_doc="Выбирает случайный вариант из списка через `;`\nПример: .wheel Пойти; Поспать; Поиграть")
    async def wheel(self, message):
        """Случайный выбор из списка"""
        args = utils.get_args_raw(message)
        if ";" not in args:
            await utils.answer(message, self.strings("no_options"))
            return

        options = [opt.strip() for opt in args.split(";") if opt.strip()]
        if not options:
            await utils.answer(message, self.strings("no_options"))
            return

        choice = random.choice(options)
        await utils.answer(message, self.strings("chosen").format(choice))