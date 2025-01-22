from aiogram import Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import ReplyKeyboardRemove


router = Router()


@router.message(StateFilter(default_state))
async def send_answer(message: types.Message) -> None:
    await message.answer(
        text="Не представляю, что ответить на это!",
        reply_to_message_id=message.message_id,
        reply_markup=ReplyKeyboardRemove(),
    )
