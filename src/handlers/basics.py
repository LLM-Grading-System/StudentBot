from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from src.infrastructure.aiogram.constants import MENU_COMMAND
from src.bootstrap import Bootstrap
from src.infrastructure.aiogram.keyboards import main_menu_keyboard
from src.services import StudentNotFoundError

router = Router()


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
