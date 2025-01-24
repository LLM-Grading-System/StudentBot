from aiogram import types
from aiogram.fsm.state import default_state
from aiogram.types import ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from src.constants import EXIT_TEXT
from src.handlers.basics import main_menu_keyboard


router = Router()


@router.message(F.text == EXIT_TEXT)
async def send_answer(message: types.Message, state: FSMContext,) -> None:
    await state.clear()
    await message.answer(
        text="Вы в главном меню",
        reply_markup=main_menu_keyboard,
    )


@router.message(StateFilter(default_state))
async def send_answer(message: types.Message) -> None:
    await message.answer(
        text="Не представляю, что ответить на это!",
        reply_to_message_id=message.message_id,
        reply_markup=ReplyKeyboardRemove(),
    )
