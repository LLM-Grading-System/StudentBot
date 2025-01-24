from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from src.constants import COMPLAINT_TEXT, GITHUB_TEXT, STATS_TEXT, MENU_COMMAND, LEADERBOARD_TEXT
from src.bootstrap import Bootstrap
from src.services import StudentNotFoundError

router = Router()


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


@router.message(CommandStart())
async def start_bot(message: Message,  state: FSMContext, bootstrap: Bootstrap) -> None:
    try:
        await bootstrap.student_service.get_student_by_telegram_user_id(message.from_user.id)
        await message.answer(
            text=f"Приветствую, {message.from_user.first_name}! Чем могу помочь?",
            reply_markup=main_menu_keyboard,
        )
    except StudentNotFoundError:
        tg_user = message.from_user
        await bootstrap.student_service.create_student(tg_user.id, tg_user.username)
        await message.answer(
            text="Добро пожаловать в систему оценивания!",
            reply_markup=main_menu_keyboard,
        )
    finally:
        await state.clear()


@router.message(Command(commands=MENU_COMMAND))
async def start_bot(message: Message,  state: FSMContext) -> None:
    await message.answer(
        text=f"Приветствую, {message.from_user.first_name}! Чем могу помочь?",
        reply_markup=main_menu_keyboard,
    )
    await state.clear()
