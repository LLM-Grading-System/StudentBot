import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from faststream import FastStream
from faststream.redis import RedisBroker
from src.handlers import basics_router, complaint_router, other_router, github_binding_router, statistics_router
from src.bootstrap import get_test_bootstrap


load_dotenv()

# broker = RedisBroker(os.environ["REDIS_URL"])
# app = FastStream(broker)
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher()


class MessageData(BaseModel):
    text: str = Field(..., description="Message text")


# @broker.subscriber("incoming_messages")
# async def handle_message(data: MessageData):
#     print(f"Received message: {data.text}")


async def stop_bot():
    pass
    # await broker.close()


async def main():
    # await app.start()
    dp.include_routers(
        basics_router, complaint_router, github_binding_router, statistics_router,
        other_router
    )
    dp.shutdown.register(stop_bot)
    dp.workflow_data.update({"bootstrap": get_test_bootstrap()})
    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f"Bot is shutdown with error: {ex}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
