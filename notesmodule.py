# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team

from hikkatl.tl.types import Message
from .. import loader, utils
import asyncio

@loader.tds
class NotesModule(loader.Module):
    """📝 Simple notes manager"""

    strings = {
        "name": "NotesModule",
        "note_added": "<b>✅ Note added:</b> <code>{}</code>",
        "notes_empty": "<b>ℹ️ You have no notes.</b>",
        "notes_list": "<b>🗒 Your notes:</b>\n{}",
        "note_deleted": "<b>✅ Note #{}</b> deleted.",
        "invalid_index": "<b>❌ Invalid note number.</b>",
        "no_args": "<b>❗ Please provide note text or note number.</b>",
        "help_text": (
            "<b>📝 Notes Module Commands:</b>\n"
            "<code>.addnote &lt;text&gt;</code> — add a new note\n"
            "<code>.notes</code> — list all notes\n"
            "<code>.delnote &lt;number&gt;</code> — delete note by number\n"
            "<code>.nothelp</code> — show this help message"
        )
    }

    def __init__(self):
        self.notes = []

    @loader.command()
    async def addnotecmd(self, message: Message):
        """Add a note. Usage: .addnote text"""
        text = utils.get_args_raw(message)
        if not text:
            await utils.answer(message, self.strings("no_args"), parse_mode="html")
            return
        self.notes.append(text)
        await utils.answer(message, self.strings("note_added").format(text), parse_mode="html")

    @loader.command()
    async def notescmd(self, message: Message):
        """Show all notes"""
        if not self.notes:
            await utils.answer(message, self.strings("notes_empty"), parse_mode="html")
            return
        notes_text = ""
        for i, note in enumerate(self.notes, 1):
            notes_text += f"<b>{i}.</b> {note}\n"
        await utils.answer(message, self.strings("notes_list").format(notes_text), parse_mode="html")

    @loader.command()
    async def delnotecmd(self, message: Message):
        """Delete note by number. Usage: .delnote 1"""
        arg = utils.get_args_raw(message)
        if not arg or not arg.isdigit():
            await utils.answer(message, self.strings("no_args"), parse_mode="html")
            return
        index = int(arg) - 1
        if index < 0 or index >= len(self.notes):
            await utils.answer(message, self.strings("invalid_index"), parse_mode="html")
            return
        deleted = self.notes.pop(index)
        await utils.answer(message, self.strings("note_deleted").format(index + 1), parse_mode="html")

    @loader.command()
    async def nothelpcmd(self, message: Message):
        """Show help"""
        await utils.answer(message, self.strings("help_text"), parse_mode="html")