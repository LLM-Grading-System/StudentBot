from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from src.constants import STATS_TEXT, EXIT_TEXT
from src.bootstrap import Bootstrap
from src.handlers.basics import main_menu_keyboard


router = Router()


class GithubBindingState(StatesGroup):
    waiting_github_username = State()


cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=text) for text in [EXIT_TEXT]]],
    resize_keyboard=True
)


@router.message(F.text == STATS_TEXT)
async def show_statistics(message: Message, bootstrap: Bootstrap):
    statistics = await bootstrap.statistics_service.get_statistics_by_telegram_user_id(message.from_user.id)
    text = ""
    for task in statistics.tasks:
        text += task.task_name + ": "
        if task.task_attempt == 0:
            text += "нет попыток"
        else:
            text += f"<b>{task.task_score:.2f}</b> (за {task.task_attempt} попытки)"
        text += "\n"
    await message.answer(text, reply_markup=cancel_keyboard, parse_mode="HTML")
