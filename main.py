import os
from dotenv import load_dotenv

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from gemini_request import extract_order

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await message.answer("Введіть текст замовлення в довільному вигляді, і бот розпарсить його для зручної взіємодії "
                         "у вигляді\nЗамовлення: номер\nДата: дата\nКлієнт: назва компанії")


@dp.message()
async def parse_order_message(message: Message) -> None:
    if message.text == "hello":
        await message.answer(f"Hello, I know that you are {html.bold(message.from_user.full_name)}!")
    else:
        res = await extract_order(message.text)
        if res is None:
            resp = "Бот не може відповісти в домовленому форматі."
        else:
            resp = f"Замовлення: {res.order_number}\nДата: {res.date}\nКлієнт: {res.client_name}"

        await message.answer(resp)


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())