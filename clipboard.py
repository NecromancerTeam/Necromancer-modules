# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team

from .. import loader, utils
import json

@loader.tds
class ClipboardMod(loader.Module):
    """📋 Clipboard — буфер обмена: сохраняй, вставляй и управляй текстом"""

    strings = {
        "name": "Clipboard",
        "copyed": "📋 Текст сохранён в буфер <code>{}</code>",
        "pasted": "📋 Буфер <code>{}</code>:\n<code>{}</code>",
        "cleared": "🗑️ Буфер <code>{}</code> очищен",
        "not_found": "❌ Буфер <code>{}</code> не найден",
        "imported": "✅ Буферы успешно импортированы",
        "exported": "📦 Экспорт буферов:\n<code>{}</code>",
        "list": "📄 Список буферов:\n{}",
        "empty": "🚫 Нет буферов для отображения",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "default_name", "main",
                lambda: "Имя буфера по умолчанию"
            ),
            loader.ConfigValue(
                "log_copies", True,
                lambda: "Показывать сообщение после .copy"
            ),
        )
        self.clipboard = {}

    @loader.command(
        ru_doc="Сохранить текст в буфер. Пример: .copy заметка Привет!",
        description="Сохраняет текст под именем буфера"
    )
    async def copy(self, message):
        """Сохраняет текст в указанный буфер"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "❗ Использование: .copy [имя] <текст>")
        parts = args.split(maxsplit=1)
        if len(parts) == 1:
            name = self.config["default_name"]
            text = parts[0]
        else:
            name, text = parts
        self.clipboard[name] = text
        if self.config["log_copies"]:
            await utils.answer(message, self.strings("copyed").format(name))
        else:
            await utils.answer(message, "✅")

    @loader.command(
        ru_doc="Вставить текст из буфера. Пример: .paste заметка",
        description="Вставляет содержимое указанного буфера"
    )
    async def paste(self, message):
        """Вставляет текст из буфера"""
        name = utils.get_args_raw(message) or self.config["default_name"]
        if name not in self.clipboard:
            return await utils.answer(message, self.strings("not_found").format(name))
        await utils.answer(message, self.strings("pasted").format(name, self.clipboard[name]))

    @loader.command(
        ru_doc="Очистить буфер. Пример: .clearclip заметка",
        description="Удаляет указанный буфер"
    )
    async def clearclip(self, message):
        """Удаляет буфер из памяти"""
        name = utils.get_args_raw(message) or self.config["default_name"]
        if name in self.clipboard:
            del self.clipboard[name]
            await utils.answer(message, self.strings("cleared").format(name))
        else:
            await utils.answer(message, self.strings("not_found").format(name))

    @loader.command(
        ru_doc="Показать список всех буферов",
        description="Отображает все сохранённые буферы"
    )
    async def cliplist(self, message):
        """Список всех буферов"""
        if not self.clipboard:
            return await utils.answer(message, self.strings("empty"))
        out = "\n".join(f"• <b>{k}</b>: {len(v)} символов" for k, v in self.clipboard.items())
        await utils.answer(message, self.strings("list").format(out))

    @loader.command(
        ru_doc="Экспортировать буферы в JSON",
        description="Экспорт всех буферов в формате JSON"
    )
    async def clipexport(self, message):
        """Экспорт буферов в JSON"""
        if not self.clipboard:
            return await utils.answer(message, self.strings("empty"))
        data = json.dumps(self.clipboard)
        await utils.answer(message, self.strings("exported").format(data))

    @loader.command(
        ru_doc="Импортировать буферы из JSON (ответ на сообщение)",
        description="Импорт буферов из JSON"
    )
    async def clipimport(self, message):
        """Импорт буферов из JSON-ответа"""
        reply = await message.get_reply_message()
        if not reply or not reply.text:
            return await utils.answer(message, "❗ Ответь на сообщение с JSON-данными буферов")
        try:
            data = json.loads(reply.text)
            if isinstance(data, dict):
                self.clipboard = data
                await utils.answer(message, self.strings("imported"))
            else:
                raise ValueError
        except Exception:
            await utils.answer(message, "⚠️ Неверный формат JSON для импорта")

    @loader.command(
        ru_doc="Синхронизировать — вывести JSON буферов в чат",
        description="Показывает JSON всех буферов для синхронизации"
    )
    async def clipsync(self, message):
        """Показывает JSON буферов в чате"""
        if not self.clipboard:
            return await utils.answer(message, self.strings("empty"))
        await utils.answer(message, "<code>" + json.dumps(self.clipboard) + "</code>")

    @loader.command(
        ru_doc="Показать справку по модулю",
        description="Отображает список команд и их описание"
    )
    async def cliphelp(self, message):
        """Справка по командам модуля"""
        help_text = (
            "<b>📋 Clipboard Module — команды:</b>\n"
            ".copy [имя] <текст> — сохранить текст\n"
            ".paste [имя] — вставить текст из буфера\n"
            ".clearclip [имя] — удалить буфер\n"
            ".cliplist — список буферов\n"
            ".clipexport — экспорт буферов в JSON\n"
            ".clipimport — импорт буферов из JSON (ответ)\n"
            ".clipsync — показать JSON буферов в чате\n"
            ".cliphelp — эта справка"
        )
        await utils.answer(message, help_text)