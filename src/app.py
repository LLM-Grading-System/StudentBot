import asyncio
import logging
from typing import Annotated

from faststream import Depends
from faststream.kafka import KafkaBroker
from aiogram import Bot, Dispatcher
from src.handlers import basics_router, complaint_router, other_router, github_binding_router, statistics_router
from src.bootstrap import get_bootstrap
from src.infrastructure.faststream.events import COMPLAINT_ANSWER_TOPIC, COMPLAINT_ANSWER_CONSUMER_GROUP, \
    ComplaintAnswerEventSchema, CommentCreatedEventSchema, COMMENT_CREATED_TOPIC, COMMENT_CREATED_CONSUMER_GROUP
from src.services.student import StudentService, APIStudentService
from src.settings import app_settings

bot = Bot(token=app_settings.BOT_TOKEN)
dp = Dispatcher()

broker = KafkaBroker(app_settings.KAFKA_BOOTSTRAP_SERVERS)


TelegramBot = Annotated[Bot, Depends(lambda: bot)]
StudentService = Annotated[StudentService, Depends(lambda: APIStudentService())]

@broker.subscriber(COMPLAINT_ANSWER_TOPIC, group_id=COMPLAINT_ANSWER_CONSUMER_GROUP, auto_commit=False)
async def handle_new_submission(data: ComplaintAnswerEventSchema, telegram_bot: TelegramBot) -> None:
    text = f"*Ответ преподавателя:*\n\n{data.answer}"
    await telegram_bot.send_message(data.student_telegram_user_id, text, parse_mode='Markdown')


@broker.subscriber(COMMENT_CREATED_TOPIC, group_id=COMMENT_CREATED_CONSUMER_GROUP, auto_commit=False)
async def handle_comment_created(data: CommentCreatedEventSchema, telegram_bot: TelegramBot, student_service: StudentService) -> None:
    student = await student_service.get_student_by_github_username(data.username)
    text = f"*Комментарий к работе:*"
    text += f"\n\nПожалуйста проверьте комментарий к вашей работе: {data.pull_request_link}"
    await telegram_bot.send_message(student.telegram_user_id, text, parse_mode='Markdown')


async def stop_bot():
    await broker.close()


async def main():
    dp.include_routers(
        basics_router, complaint_router, github_binding_router, statistics_router,
        other_router
    )
    dp.shutdown.register(stop_bot)
    dp.workflow_data.update({"bootstrap": get_bootstrap()})
    async with broker:
        await broker.start()
        try:
            await dp.start_polling(bot)
        except Exception as ex:
            logging.error(f"Bot is shutdown with error: {ex}")
        finally:
            await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
