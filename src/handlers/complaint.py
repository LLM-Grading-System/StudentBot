from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.filters import StateFilter, or_f, and_f
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from src.constants import COMPLAINT_TEXT, CONFIRM_TEXT, EDIT_TEXT, EXIT_TEXT
from src.bootstrap import Bootstrap

router = Router()


class ComplaintState(StatesGroup):
    waiting_for_task = State()
    waiting_for_description = State()
    waiting_for_confirm = State()


def get_task_choice_keyboard(tasks: list[str]) -> ReplyKeyboardMarkup:
    buttons_rows = []
    for i in range(0, len(tasks), 2):
        row_tasks = tasks[i:i + 2]
        buttons_rows.append([KeyboardButton(text=task) for task in row_tasks])
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons_rows)
    return keyboard


ready_complaint_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=text) for text in [CONFIRM_TEXT, EDIT_TEXT, EXIT_TEXT]]],
    resize_keyboard=True
)


@router.message(
    or_f(F.text == COMPLAINT_TEXT, and_f(StateFilter(ComplaintState.waiting_for_confirm), F.text == EDIT_TEXT)))
async def start_complaint_process(message: Message, state: FSMContext, bootstrap: Bootstrap):
    tasks = await bootstrap.task_service.get_tasks()
    keyboard = get_task_choice_keyboard([task.name for task in tasks])
    await state.set_state(ComplaintState.waiting_for_task)
    text = "Пожалуйста, выберите задание, с оценкой которого вы не согласны"
    old_task = await state.get_value("task", None)
    if old_task:
        text = text + f"\n<b>Прошлый выбор</b>: {old_task}"
    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.message(StateFilter(ComplaintState.waiting_for_task), F.text)
async def choice_task(message: Message, state: FSMContext, bootstrap: Bootstrap) -> None:
    chosen_task = message.text
    tasks = await bootstrap.task_service.get_tasks()
    filtered_tasks = [task for task in tasks if task.name == chosen_task]
    if not filtered_tasks:
        keyboard = get_task_choice_keyboard([task.name for task in tasks])
        text = "Пожалуйста, выберите существующее задание"
        await message.answer(text, reply_markup=keyboard)
        return
    task_id = filtered_tasks[0].task_id
    await state.update_data(task=chosen_task, task_id=task_id)
    await state.set_state(ComplaintState.waiting_for_description)
    text = "Пожалуйста, опишите вашу ситуацию"
    old_description = await state.get_value("description", None)
    if old_description:
        text = text + f"\n<b>Прошлое описание</b>: {old_description}"
    await message.answer(text, reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")


@router.message(StateFilter(ComplaintState.waiting_for_description), F.text)
async def add_description(message: Message, state: FSMContext) -> None:
    description = message.text
    await state.update_data(description=description)
    await state.set_state(ComplaintState.waiting_for_confirm)
    state_data = await state.get_data()
    text = "Пожалуйста проверьте, что все верно, и подтвердите отправку\n"
    text += f"<b>Задание</b>: {state_data['task']}\n<b>Описание</b>: {state_data['description']}"
    await message.answer(text, reply_markup=ready_complaint_keyboard, parse_mode="HTML")


@router.message(StateFilter(ComplaintState.waiting_for_confirm), F.text == CONFIRM_TEXT)
async def confirm_complaint(message: Message, state: FSMContext, bootstrap: Bootstrap) -> None:
    state_data = await state.get_data()
    task_id = state_data["task_id"]
    description = state_data["description"]
    await bootstrap.task_service.create_complaint_by_task(task_id, description)
    text = "Ваша заявка успешно отправлена! \nПреподаватель ее скоро рассмотрит!"
    await state.clear()
    await message.answer(text, reply_markup=ReplyKeyboardRemove())


@router.message(
    StateFilter(ComplaintState.waiting_for_confirm) or StateFilter(ComplaintState.waiting_for_task)
    or StateFilter(ComplaintState.waiting_for_description)
)
async def handle_incorrect_type_sent_data(message: Message, state: FSMContext) -> None:
    text = "Похоже, что вы отправили что-то не то!\nПопробуйте еще раз"
    await message.answer(text)
