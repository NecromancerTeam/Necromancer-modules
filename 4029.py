# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team
import random
from .. import loader, utils

@loader.tds
class RandomMod(loader.Module):
    """🎲 Простой модуль для случайных действий: число, выбор, монетка, пароль"""

    strings = {
        "name": "Random",
        "usage_num": "<b>Использование:</b> <code>.randnum <мин> <макс></code>",
        "usage_choice": "<b>Использование:</b> <code>.choice <вариант1> <вариант2> ...</code>",
        "usage_coin": "<b>Использование:</b> <code>.coin</code>",
        "usage_pass": "<b>Использование:</b> <code>.passgen <длина></code>",
        "coin_head": "🎉 Выпала: Орёл",
        "coin_tail": "😎 Выпала: Решка",
        "pass_invalid_len": "<b>❌ Длина должна быть числом от 4 до 64</b>",
    }

    @loader.command(ru_doc="Случайное число в диапазоне")
    async def randnumcmd(self, message):
        """.randnum <мин> <макс> — случайное число"""
        args = utils.get_args(message)
        if len(args) != 2 or not all(x.lstrip("-").isdigit() for x in args):
            return await utils.answer(message, self.strings("usage_num"))
        low, high = int(args[0]), int(args[1])
        if low > high:
            low, high = high, low
        num = random.randint(low, high)
        await utils.answer(message, f"🎲 Случайное число: <b>{num}</b>")

    @loader.command(ru_doc="Случайный выбор из списка")
    async def choicecmd(self, message):
        """.choice <вариант1> <вариант2> ... — случайный выбор"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("usage_choice"))
        choices = args.split()
        choice = random.choice(choices)
        await utils.answer(message, f"🔮 Выбор: <b>{choice}</b>")

    @loader.command(ru_doc="Подбросить монетку")
    async def coincmd(self, message):
        """.coin — подбросить монетку"""
        flip = random.choice(["head", "tail"])
        text = self.strings["coin_head"] if flip == "head" else self.strings["coin_tail"]
        await utils.answer(message, text)

    @loader.command(ru_doc="Сгенерировать случайный пароль")
    async def passgencmd(self, message):
        """.passgen <длина> — сгенерировать пароль"""
        args = utils.get_args(message)
        if len(args) != 1 or not args[0].isdigit():
            return await utils.answer(message, self.strings("usage_pass"))
        length = int(args[0])
        if length < 4 or length > 64:
            return await utils.answer(message, self.strings("pass_invalid_len"))
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+"
        password = "".join(random.choice(chars) for _ in range(length))
        await utils.answer(message, f"🔐 Сгенерированный пароль:\n<code>{password}</code>")