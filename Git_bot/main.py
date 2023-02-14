import random
import json
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command, Text
from config import TOKEN_API

bot = Bot(TOKEN_API)
dp = Dispatcher()

ATTEMPTS: int = 6
users: dict = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    return random.randint(1, 100)

# Этот хэндлер будет срабатывать на текст "girl"
@dp.message(Text(text=["girl"]))
async def fuck_girl(message: Message):
    rand_file = random.choice(os.listdir("girls"))
    sex = os.path.join("girls", rand_file)
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(sex), caption="<strong>Победителя поздравляет <em>косплей баба!!!</em></strong>", parse_mode='HTML')

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}!\nДавай сыграем в игру "Угадай число"?\n\n'
                         'Чтобы получить правила игры и список доступных '
                         'команд - отправь команду /help')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'attempts': None,
                                       'total_games': 0,
                                       'wins': 0}

# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=["help"]))
async def process_start_command(message: Message):
    await message.answer(f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
                         f'а тебе нужно его угадать\nУ тебя есть {ATTEMPTS} '
                         f'попыток\n\nДоступные команды:\n/help - правила '
                         f'игры и список команд\n/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\nДавай сыграем, говнюк?')

# Этот хэндлер будет реагировать на команду "/stat"
@dp.message(Command(commands=['stat']))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
                         f'Игр выиграно: {users[message.from_user.id]["wins"]}')

# Этот хэндлер будет реагировать на команду "/cancel"
@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Ну и проваливай!')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('Сейчас игра остановлена вообще-то')

# Этот хэндлер будет реагировать на согласие пользователя сыграть в игру
@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра', 'Играть', 'Хочу играть', 'lf'], ignore_case=True))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Ура!\n\nЯ загадал число от 1 до 100, '
                             'попробуй угадать!')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 100 '
                             'и команды /cancel и /stat')

# Этот хэндлер будет реагировать на отказ пользователя сыграть в игру
@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Не буду'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотишь поиграть - просто '
                             'напиши об этом')
    else:
        await message.answer('Мы же сейчас с тобой играем.'
                             'Присылай, числа от 1 до 100')

# Этот хэндлер будет реагировать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Ура!!! Ты угадал число!\n\n'
                                 'Может, сыграем еще, засранец?\n'
                                 'Или, можешь посмотреть статистику /stat')
            rand_file = random.choice(os.listdir("girls"))
            sex = os.path.join("girls", rand_file)
            await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile(sex), caption="<strong>Победителя поздравляет <em>косплей баба!!!</em></strong>", parse_mode='HTML') ### скрипт вывода фоточек
            with open('data.txt', 'w') as outfile:
                json.dump(users, outfile)
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Нифига, Мое число меньше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Нифига, Мое число больше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer(f'К сожалению, у тебя больше не осталось '
                                 f'попыток. Ты проиграл :(\n\nМое число '
                                 f'было {users[message.from_user.id]["secret_number"]}\n\nДавай '
                                 f'сыграем еще?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            with open('data.txt', 'w') as outfile:
                json.dump(users, outfile)
    else:
        await message.answer('Мы еще не играем. Хотишь сыграть?')

# Этот хэндлер будет реагировать на остальные текстовые мессаджи
@dp.message()
async def process_other_text_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас с тобой играем. '
                             'Присылай числа от 1 до 100')
    else:
        await message.answer('Просто пришли ДА или НЕТ. Хватит отправлять мне всякую хрень')


if __name__ == '__main__':
    dp.run_polling(bot)
