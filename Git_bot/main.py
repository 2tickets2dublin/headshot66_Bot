from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    await message.answer("<strong><em>Hello! You are welkome to our BOT!</em></strong>", parse_mode="HTML")


@dp.message(Command(commands=["gives"]))
async def start_command(message: types.Message):
    await bot.send_sticker(message.from_user.id, sticker="CAACAgIAAxkBAAEHr-Nj56y2LCy6z4GHmv2Alq76izydjQACBQwAAqQp6Eva0HNoMuvnQi4E")
    await message.delete()


@dp.message()
async def send_emo(message: types.Message):
    await message.reply(message.text + " ❤️")


if __name__ == "__main__":
    dp.run_polling(bot)
