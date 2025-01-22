from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from src.constants import GITHUB_TEXT, EXIT_TEXT
from src.bootstrap import Bootstrap
from src.routers.basics import main_menu_keyboard


router = Router()


class GithubBindingState(StatesGroup):
    waiting_github_username = State()


cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=text) for text in [EXIT_TEXT]]],
    resize_keyboard=True
)


@router.message(F.text == GITHUB_TEXT)
async def start_github_binding_process(message: Message, state: FSMContext):
    await state.set_state(GithubBindingState.waiting_github_username)
    text = "Введите ваше имя пользователя на GitHub\n"
    text += "Пожалуйста добавьте на время верификации в своем GitHub-профиле в поле website ссылку на телеграм-аккаунт"
    await message.answer(text, reply_markup=cancel_keyboard, parse_mode="HTML")


@router.message(StateFilter(GithubBindingState.waiting_github_username), F.text != EXIT_TEXT)
async def handle_github_username(message: Message, state: FSMContext, bootstrap: Bootstrap) -> None:
    github_username = message.text
    is_verified = await bootstrap.github_service.is_verified(github_username, message.from_user.username)
    if is_verified:
        await state.clear()
        await bootstrap.student_service.set_github_username(message.from_user.id, github_username)
        text = "GitHub-аккаунт успешно подтвержден"
        keyboard = main_menu_keyboard
    else:
        text = "Попробуйте ввести имя пользователя на GitHub снова"
        keyboard = cancel_keyboard
    await message.answer(text, reply_markup=keyboard)


@router.message(StateFilter(GithubBindingState.waiting_github_username))
async def handle_incorrect_type_sent_data(message: Message) -> None:
    if message.text == EXIT_TEXT:
        text = "Вы вышли из режима привязки GitHub-аккаунта..."
        await message.answer(text, reply_markup=main_menu_keyboard)
        return

    text = "Похоже, что вы отправили что-то не то!\nПопробуйте еще раз"
    await message.answer(text)
