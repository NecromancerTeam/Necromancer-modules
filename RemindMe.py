# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team

import asyncio
import re
from datetime import datetime, timedelta
from .. import loader, utils

@loader.tds
class RemindMeMod(loader.Module):
    """⏰ Персональный напоминальщик с повторениями и сохранением"""

    strings = {
        "name": "RemindMe",
        "remind_set": "<b>✅ Напоминание установлено на {}.</b>",
        "remind_repeat_set": "<b>✅ Повторяющееся напоминание установлено каждые {} секунд.</b>",
        "remind_now": "<b>⚠️ Время указано в прошлом или слишком мало.</b>",
        "remind_list_empty": "<b>📭 У вас нет активных напоминаний.</b>",
        "remind_list_header": "<b>📝 Ваши напоминания:</b>",
        "remind_del_success": "<b>❎ Напоминание #{} удалено.</b>",
        "remind_del_fail": "<b>❌ Напоминание с таким номером не найдено.</b>",
        "usage_remind": "<b>Использование:</b> <code>.remind 10m Текст напоминания</code>",
        "usage_remindrepeat": "<b>Использование:</b> <code>.remindrepeat 10m Текст напоминания</code>",
        "usage_del": "<b>Использование:</b> <code>.reminddel Номер_напоминания</code>",
        "max_reminders": "<b>❗ Достигнуто максимальное количество напоминаний ({}).</b>",
        "invalid_time": "<b>❌ Неверный формат времени. Пример: 10s, 5m, 2h, 1d</b>",
        "all_cleared": "<b>🧹 Все напоминания удалены.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("max_reminders", 10, lambda: "Максимальное кол-во активных напоминаний"),
        )
        self.reminders = {}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        await self._load_reminders()

    async def _load_reminders(self):
        data = self.db.get("RemindMeMod", "reminders", {})
        self.reminders = data or {}
        for user_id, reminders in self.reminders.items():
            for r in reminders:
                r["task"] = asyncio.create_task(self._remind_worker(user_id, r))

    async def _save_reminders(self):
        data = {}
        for user_id, reminders in self.reminders.items():
            data[user_id] = []
            for r in reminders:
                r_copy = r.copy()
                r_copy.pop("task", None)
                data[user_id].append(r_copy)
        self.db.set("RemindMeMod", "reminders", data)

    def _parse_time(self, time_str):
        match = re.fullmatch(r"(\d+)([smhd])", time_str.lower())
        if not match:
            return None
        val, unit = int(match.group(1)), match.group(2)
        if unit == "s":
            return timedelta(seconds=val)
        elif unit == "m":
            return timedelta(minutes=val)
        elif unit == "h":
            return timedelta(hours=val)
        elif unit == "d":
            return timedelta(days=val)

    async def _remind_worker(self, user_id, reminder):
        while True:
            now = datetime.now()
            remind_time = datetime.fromisoformat(reminder["time"])
            delay = (remind_time - now).total_seconds()
            if delay > 0:
                try:
                    await asyncio.sleep(delay)
                except asyncio.CancelledError:
                    break

            chat_id = reminder["chat_id"]
            user_id_int = int(user_id)
            # Попытка получить имя пользователя (username) для упоминания
            try:
                user_entity = await self.client.get_entity(user_id_int)
                if hasattr(user_entity, "username") and user_entity.username:
                    mention = f"@{user_entity.username}"
                else:
                    mention = f"<a href=\"tg://user?id={user_id_int}\">{user_entity.first_name}</a>"
            except Exception:
                mention = "User"

            text = reminder["text"]
            await self.client.send_message(chat_id, f"<b>⏰ Напоминание для {mention}:</b> {text}", parse_mode="html")

            if reminder.get("repeat_seconds") is not None:
                next_time = remind_time + timedelta(seconds=reminder["repeat_seconds"])
                reminder["time"] = next_time.isoformat()
                await self._save_reminders()
            else:
                if user_id in self.reminders:
                    try:
                        self.reminders[user_id].remove(reminder)
                        await self._save_reminders()
                    except ValueError:
                        pass
                break

    @loader.command(ru_doc="Установить одноразовое напоминание")
    async def remindcmd(self, message):
        """Использование: .remind <время> <текст> (например, .remind 10m Сделать перерыв)"""
        args = utils.get_args_raw(message)
        if not args or " " not in args:
            return await utils.answer(message, self.strings("usage_remind"))

        time_str, text = args.split(" ", 1)
        delta = self._parse_time(time_str)
        if not delta:
            return await utils.answer(message, self.strings("invalid_time"))

        remind_time = datetime.now() + delta
        user = await utils.get_user(message)
        user_id = str(user.id)
        chat_id = utils.get_chat_id(message)

        if user_id not in self.reminders:
            self.reminders[user_id] = []

        if len(self.reminders[user_id]) >= self.config["max_reminders"]:
            return await utils.answer(message, self.strings("max_reminders").format(self.config["max_reminders"]))

        reminder = {
            "time": remind_time.isoformat(),
            "text": text,
            "chat_id": chat_id,
            "repeat_seconds": None,
        }
        reminder["task"] = asyncio.create_task(self._remind_worker(user_id, reminder))
        self.reminders[user_id].append(reminder)
        await self._save_reminders()

        await utils.answer(message, self.strings("remind_set").format(remind_time.strftime("%Y-%m-%d %H:%M:%S")))

    @loader.command(ru_doc="Установить повторяющееся напоминание")
    async def remindrepeatcmd(self, message):
        """Использование: .remindrepeat <время> <текст> (например, .remindrepeat 10m Выпить воды)"""
        args = utils.get_args_raw(message)
        if not args or " " not in args:
            return await utils.answer(message, self.strings("usage_remindrepeat"))

        time_str, text = args.split(" ", 1)
        delta = self._parse_time(time_str)
        if not delta:
            return await utils.answer(message, self.strings("invalid_time"))

        repeat_sec = int(delta.total_seconds())
        if repeat_sec <= 0:
            return await utils.answer(message, self.strings("remind_now"))

        remind_time = datetime.now() + delta
        user = await utils.get_user(message)
        user_id = str(user.id)
        chat_id = utils.get_chat_id(message)

        if user_id not in self.reminders:
            self.reminders[user_id] = []

        if len(self.reminders[user_id]) >= self.config["max_reminders"]:
            return await utils.answer(message, self.strings("max_reminders").format(self.config["max_reminders"]))

        reminder = {
            "time": remind_time.isoformat(),
            "text": text,
            "chat_id": chat_id,
            "repeat_seconds": repeat_sec,
        }
        reminder["task"] = asyncio.create_task(self._remind_worker(user_id, reminder))
        self.reminders[user_id].append(reminder)
        await self._save_reminders()

        await utils.answer(message, self.strings("remind_repeat_set").format(repeat_sec))

    @loader.command(ru_doc="Показать все активные напоминания")
    async def reminderscmd(self, message):
        """Показать список активных напоминаний"""
        user = await utils.get_user(message)
        user_id = str(user.id)
        if user_id not in self.reminders or not self.reminders[user_id]:
            return await utils.answer(message, self.strings("remind_list_empty"))

        lst = self.reminders[user_id]
        txt = [self.strings("remind_list_header")]
        for i, r in enumerate(lst, 1):
            time_ = datetime.fromisoformat(r["time"])
            repeat = f" (повторяется каждые {r['repeat_seconds']} сек)" if r.get("repeat_seconds") else ""
            txt.append(f"<b>{i}.</b> <code>{time_.strftime('%Y-%m-%d %H:%M:%S')}</code>{repeat} — {r['text']}")

        await utils.answer(message, "\n".join(txt))

    @loader.command(ru_doc="Удалить напоминание по номеру")
    async def reminddelcmd(self, message):
        """Удалить напоминание по номеру"""
        args = utils.get_args(message)
        if len(args) != 1 or not args[0].isdigit():
            return await utils.answer(message, self.strings("usage_del"))

        user = await utils.get_user(message)
        user_id = str(user.id)
        idx = int(args[0]) - 1

        if user_id not in self.reminders or idx >= len(self.reminders[user_id]) or idx < 0:
            return await utils.answer(message, self.strings("remind_del_fail"))

        reminder = self.reminders[user_id][idx]
        reminder["task"].cancel()
        del self.reminders[user_id][idx]
        await self._save_reminders()

        await utils.answer(message, self.strings("remind_del_success").format(idx + 1))

    @loader.command(ru_doc="Удалить все напоминания")
    async def remindclearcmd(self, message):
        """Удалить все активные напоминания пользователя"""
        user = await utils.get_user(message)
        user_id = str(user.id)
        if user_id in self.reminders:
            for r in self.reminders[user_id]:
                r["task"].cancel()
            self.reminders[user_id].clear()
            await self._save_reminders()
        await utils.answer(message, self.strings("all_cleared"))