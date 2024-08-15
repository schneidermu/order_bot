import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import Database
from dotenv import find_dotenv, load_dotenv
from lexicon.lexicon import LEXICON_COMMANDS
from services.llm import chain

load_dotenv(find_dotenv())

router = Router()

logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def process_start_command(message: Message, db: Database):
    logger.info(
        f"Пользователь {message.from_user.username} начал диалог, код чата {message.chat.id}"
    )
    answer_text = LEXICON_COMMANDS.get("/start", "")
    await message.answer(answer_text)
    await db.add_user(
        id=message.from_user.id,
        username=message.from_user.username,
    )


@router.message(F.text)
async def send(message: Message):
    text = message.text
    if text is None:
        return
    else:
        try:
            result = await chain.ainvoke(
                {"input": text},
            )
            await message.answer(result, parse_mode="Markdown")
            logger.info(f'Пользователь {message.from_user.username} прислал текст: "{text}", получен ответ: "{result}"')
        except Exception as e:
            logger.error(e, exc_info=True)
            await message.answer("Произошла ошибка при генерации ответа")
