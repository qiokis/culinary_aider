
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
from dotenv import load_dotenv
import emoji

from app.data.database import Database

load_dotenv('cfg/.env')

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())
bd = Database(os.environ.get('PG_USER'),
              os.environ.get('PG_PASSWORD'),
              os.environ.get('PG_DB'),
              os.environ.get('PG_HOST'),
              int(os.environ.get('PG_PORT')))


async def main():

    commands = [
        BotCommand(command='/start', description='Start app'),
        BotCommand(command='/done', description='Done'),
        BotCommand(command='/options', description='Options'),
        BotCommand(command='/secret', description=emoji.emojize('Secret'))
    ]

    await bot.set_my_commands(commands)

    import app.handlers

    await dp.start_polling()