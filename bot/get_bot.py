import asyncio
import logging
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from database import Base
from dotenv import find_dotenv, load_dotenv
from handlers import user_handlers
from logging_settings import logging_config
from middlewares import DatabaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

load_dotenv(find_dotenv())

logging.config.dictConfig(logging_config)
config: Config = load_config()


async def main():
    engine = create_async_engine(url=config.db_url, echo=True)
    session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    dp.include_router(user_handlers.router)
    dp.update.middleware(DatabaseMiddleware(session=session))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(322077458, "Я запустился")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
