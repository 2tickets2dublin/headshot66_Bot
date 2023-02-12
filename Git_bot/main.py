from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher()


@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer("Hello nigger")

@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer("Hello, its Help command")

@dp.message()
async def send_echo(message: Message):
    await message.reply(message.text)

if __name__ == "__main__":
    dp.run_polling(bot)