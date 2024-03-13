import asyncio
import logging
import sys
from os import getenv
import config_lob
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

logging.basicConfig(level=logging.INFO)

#bot init
bot = Bot(token=config_lob.TOKEN)
LobbyHost = Dispatcher(bot)

count_loobby = 0

@LobbyHost.message_handler(content_types=["new_chat_members"])
async def player_join(message: types.Message):
    count_loobby += 1
    print("somebody join!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run()