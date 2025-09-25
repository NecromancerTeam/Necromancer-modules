# Necromanser modules
# © Copyright 2025
# Git Hub https://github.com/NecromancerTeam/Modules-Heroku
# N:modules https://t.me/Lptmiop
# By Lptm-iop $ Necromanser team
import random
from .. import loader, utils

@loader.tds
class MinesweeperMod(loader.Module):
    """🧨 Игра в сапёра прямо в Telegram"""

    strings = {"name": "Minesweeper"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue("rows", 8, lambda: "📐 Кол-во строк (минимум 3, максимум 15)"),
            loader.ConfigValue("cols", 8, lambda: "📏 Кол-во столбцов (минимум 3, максимум 15)"),
            loader.ConfigValue("mines", 10, lambda: "💣 Кол-во мин (должно быть < rows * cols)")
        )
        self.games = {}

    def _create_board(self, rows, cols, mines):
        board = [[0 for _ in range(cols)] for _ in range(rows)]
        mine_positions = set()

        while len(mine_positions) < mines:
            r = random.randint(0, rows - 1)
            c = random.randint(0, cols - 1)
            mine_positions.add((r, c))

        for r, c in mine_positions:
            board[r][c] = '💣'
            for i in range(max(0, r - 1), min(rows, r + 2)):
                for j in range(max(0, c - 1), min(cols, c + 2)):
                    if board[i][j] != '💣':
                        board[i][j] += 1

        return board, mine_positions

    def _render(self, state, revealed, flagged):
        rows, cols = len(state), len(state[0])
        result = ""
        for i in range(rows):
            for j in range(cols):
                if (i, j) in flagged:
                    result += "🚩"
                elif (i, j) not in revealed:
                    result += "⬜"
                else:
                    val = state[i][j]
                    if val == 0:
                        result += "⬛"
                    elif val == '💣':
                        result += "💣"
                    else:
                        result += str(val)
            result += "\n"
        return result

    def _reveal(self, state, revealed, r, c):
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            if (x, y) in revealed:
                continue
            revealed.add((x, y))
            if state[x][y] == 0:
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < len(state) and 0 <= ny < len(state[0]):
                            stack.append((nx, ny))

    @loader.command(ru_doc="Начать новую игру")
    async def mine(self, message):
        """Запуск сапёра"""
        uid = utils.get_chat_id(message)
        rows = self.config["rows"]
        cols = self.config["cols"]
        mines = self.config["mines"]
        if rows < 3 or cols < 3 or rows > 15 or cols > 15 or mines >= rows * cols:
            await utils.answer(message, "<b>❗ Некорректные параметры.</b>")
            return

        board, mine_pos = self._create_board(rows, cols, mines)
        self.games[uid] = {
            "board": board,
            "revealed": set(),
            "flagged": set(),
            "mines": mine_pos,
            "active": True,
        }

        await utils.answer(message, "<b>🧨 Игра началась!</b>\n\n" + self._render(board, set(), set()))

    @loader.command(ru_doc="Открыть ячейку .reveal <ряд> <колонка>")
    async def reveal(self, message):
        """Открыть ячейку"""
        args = utils.get_args(message)
        uid = utils.get_chat_id(message)
        if uid not in self.games or not self.games[uid]["active"]:
            return await utils.answer(message, "<b>❌ Игра не запущена.</b>")

        if len(args) != 2 or not all(x.isdigit() for x in args):
            return await utils.answer(message, "<b>📍 Используй: .reveal <ряд> <колонка></b>")

        r, c = int(args[0]) - 1, int(args[1]) - 1
        game = self.games[uid]
        board = game["board"]

        if not (0 <= r < len(board)) or not (0 <= c < len(board[0])):
            return await utils.answer(message, "<b>❗ Неверные координаты.</b>")

        if (r, c) in game["flagged"]:
            return await utils.answer(message, "<b>🚩 Там флаг. Сначала убери его.</b>")

        if board[r][c] == '💣':
            game["revealed"].add((r, c))
            game["active"] = False
            await utils.answer(message, "<b>💥 БУМ! Ты наступил на бомбу. Игра окончена — ты проиграл.</b>\n\n" + self._render(board, game["revealed"], game["flagged"]))
            return

        self._reveal(board, game["revealed"], r, c)
        await utils.answer(message, self._render(board, game["revealed"], game["flagged"]))

    @loader.command(ru_doc="Поставить флаг .flag <ряд> <колонка>")
    async def flag(self, message):
        """Поставить флаг"""
        args = utils.get_args(message)
        uid = utils.get_chat_id(message)
        if uid not in self.games or not self.games[uid]["active"]:
            return await utils.answer(message, "<b>❌ Игра не запущена.</b>")
        if len(args) != 2 or not all(x.isdigit() for x in args):
            return await utils.answer(message, "<b>📍 Используй: .flag <ряд> <колонка></b>")

        r, c = int(args[0]) - 1, int(args[1]) - 1
        game = self.games[uid]

        if (r, c) in game["flagged"]:
            return await utils.answer(message, "<b>⚠️ Там уже стоит флаг.</b>")

        game["flagged"].add((r, c))
        await utils.answer(message, self._render(game["board"], game["revealed"], game["flagged"]))

    @loader.command(ru_doc="Убрать флаг .unflag <ряд> <колонка>")
    async def unflag(self, message):
        """Убрать флаг"""
        args = utils.get_args(message)
        uid = utils.get_chat_id(message)
        if uid not in self.games or not self.games[uid]["active"]:
            return await utils.answer(message, "<b>❌ Игра не запущена.</b>")
        if len(args) != 2 or not all(x.isdigit() for x in args):
            return await utils.answer(message, "<b>📍 Используй: .unflag <ряд> <колонка></b>")

        r, c = int(args[0]) - 1, int(args[1]) - 1
        game = self.games[uid]

        if (r, c) in game["flagged"]:
            game["flagged"].remove((r, c))
            await utils.answer(message, self._render(game["board"], game["revealed"], game["flagged"]))
        else:
            await utils.answer(message, "<b>🚫 Там нет флага.</b>")

    @loader.command(ru_doc="Сбросить текущую игру")
    async def minereset(self, message):
        """Завершить игру"""
        uid = utils.get_chat_id(message)
        if uid in self.games:
            del self.games[uid]
        await utils.answer(message, "<b>🔄 Игра сброшена.</b>")