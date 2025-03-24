from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from src.infrastructure.aiogram.constants import COMPLAINT_TEXT, GITHUB_TEXT, STATS_TEXT, LEADERBOARD_TEXT


main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=GITHUB_TEXT),
            KeyboardButton(text=STATS_TEXT),
        ],
        [
            KeyboardButton(text=COMPLAINT_TEXT),
            KeyboardButton(text=LEADERBOARD_TEXT),
        ]
    ],
    resize_keyboard=True,
)
