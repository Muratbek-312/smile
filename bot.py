import logging
import requests
import aioschedule
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data.config import TOKEN
from states.position import Position, Position1
from keyboards import reply_key as rk



logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

id_usersname = {}
otchet, otchet1, otchet2, otchet3 = {}, {}, {}, {}
python_csv, python_even_csv, python_otchet= set(), set(), set()


async def python_file():
    try:
        f = open("user_id.csv", "r")
        f1 = f.readlines()
        for i in f1:
            python_csv.add(i)
    except Exception as e:
        print(e)


async def python_even_file():
    try:
        f = open("user_even.csv", "r")
        f1 = f.readlines()
        for i in f1:
            python_even_csv.add(i)
    except Exception as e:
        print(e)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    try:
        chat_id = str(message.chat.id)
        name = message.chat.first_name
        id_usersname.setdefault(chat_id, name)
        with open('otchet.csv', 'r') as f_otchet:
            reader = f_otchet.readlines()
            reader = [name.strip() for name in reader]
            faile = []
            print(reader)
            print(id_usersname)
            for name in id_usersname.keys():
                print(name)
                if name not in reader:
                    faile.append(name)
            if faile != []:
                await bot.send_message(message.chat.id, "Добро пожаловать 👋\nВыберите группу в которой вы учитесь👨‍💻",
                                       reply_markup=rk.key_group)
                await Position.Q1.set()
            else:
                await bot.send_message(message.chat.id, 'Вы уже прошли опрос😄')
    except Exception as e:
        print(e)


@dp.message_handler(state=Position.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Q1'] = message.text
        if message.text == 'Python vol. 10' or message.text == 'Python vol. 9' or message.text == 'JavaScript vol. 10' or message.text == 'JavaScript vol. 9':
            otchet[message.chat.first_name] = message.text
            await bot.send_message(message.chat.id, "С каким настроением вы пришли на учёбу?", reply_markup=rk.keyboard)
            await write_to_csv(message)
            await Position.Q2.set()
        elif message.text == 'Python-10. Even' or message.text == 'Python-9. Even':
            otchet[message.chat.first_name] = message.text
            await bot.send_message(message.chat.id, "С каким настроением вы пришли на учёбу?", reply_markup=rk.keyboard)
            await write_even_to_csv(message)
            await Position.Q2.set()
        else:
            await bot.send_message(message.chat.id, f'{message.chat.first_name}, не играйтесь!😠')
    except Exception as e:
        print(e)


@dp.message_handler(state=Position.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Q2'] = message.text
        if message.text == '👍 Классное':
            otchet1[message.chat.first_name] = message.text
            await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBvhdf9Ay4tuigZnJoA8YIYOja8VfExwACMwADWbv8JRUD_CxZVMH7HgQ', reply_markup=None)
            await bot.send_message(message.chat.id, 'Так держать👍, продолжай в том же темпе')
            await write_to_otchet(message)
            await state.finish()
        elif message.text == '👎 Плохое':
            otchet1[message.chat.first_name] = message.text
            await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBvklf9XOxPdPAq3IzhOGDozc5yFImwgACVgADWbv8JTjq2jGXNRjgHgQ', reply_markup=None)
            await bot.send_message(message.chat.id,
                                   'Хей, ничего страшного, сейчас тебе нужно больше трудиться и не опускать руки.\nХорошего и продуктивного дня Maker.')
            await write_to_otchet(message)
            await state.finish()
        elif message.text == '🤷‍♂ Так себе':
            otchet1[message.chat.first_name] = message.text
            await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBvktf9XPQk4xLCGoj4cDg7Ll3pHmCDAACVwQAAs7Y6Au9PhZttSyr2x4E', reply_markup=None)
            await bot.send_message(message.chat.id,
                                   'Скорее всего ты не выспался, но ничего страшного выпей кофе или чай и за работу.\nТебя ждут великие дела.')
            await write_to_otchet(message)
            await state.finish()
        else:
            await bot.send_message(message.chat.id, f'{message.chat.first_name}, не играйтесь!😠')
    except Exception as e:
        print(e)



async def answer_day():
    try:
        for i in python_csv:
            await bot.send_message(i, 'Давайте ещё раз пройдем опрос\n Нажмите на /standup', parse_mode='markdown')
    except Exception as e:
        print(e)


async def answer_even():
    try:
        for i in python_even_csv:
            await bot.send_message(i, 'Давайте ещё раз пройдем опрос\n Нажмите на /standup', parse_mode='markdown')
    except Exception as e:
        print(e)



@dp.message_handler(commands=['standup'])
async def answer_qw2(message: types.Message):
    try:
        chat_id = str(message.chat.id)
        name = message.chat.first_name
        id_usersname.setdefault(chat_id, name)
        with open('otchet.csv', 'r') as f_otchet:
            reader = f_otchet.readlines()
            reader = [name.strip() for name in reader]
            faile = []
            print(reader)
            print(id_usersname)
            for name in id_usersname.keys():
                print(name)
                if name not in reader:
                    faile.append(name)
            if faile != []:
                await bot.send_message(message.chat.id, "С каким настроением вы уходите домой?",
                                       reply_markup=rk.keyboard)
                await Position1.Q1.set()
            else:
                await bot.send_message(message.chat.id, 'Вы уже прошли опрос😄')
    except Exception as e:
        print(e)



@dp.message_handler(state=Position1.Q1)
async def answer_qw(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['Q1'] = message.text
        if message.text == '👍 Классное':
            otchet2[message.chat.first_name] = message.text
            await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBvhdf9Ay4tuigZnJoA8YIYOja8VfExwACMwADWbv8JRUD_CxZVMH7HgQ', reply_markup=None)
            await bot.send_message(message.chat.id, 'Так держать👍, продолжай в том же темпе')
            await write_to_otchet(message)
            await admin(message)
            await state.finish()
        elif message.text == '👎 Плохое':
            otchet2[message.chat.first_name] = message.text
            await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBvklf9XOxPdPAq3IzhOGDozc5yFImwgACVgADWbv8JTjq2jGXNRjgHgQ', reply_markup=None)
            await bot.send_message(message.chat.id,
                                   'Хей, ничего страшного, сейчас тебе нужно больше трудиться и не опускать руки.\nХорошего и продуктивного дня Maker.')
            await write_to_otchet(message)
            await admin(message)
            await state.finish()
        elif message.text == '🤷‍♂ Так себе':
            otchet2[message.chat.first_name] = message.text
            await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEBvktf9XPQk4xLCGoj4cDg7Ll3pHmCDAACVwQAAs7Y6Au9PhZttSyr2x4E', reply_markup=None)
            await bot.send_message(message.chat.id,
                                   'Скорее всего ты не выспался, но ничего страшного выпей кофе или чай и за работу.\nТебя ждут великие дела.')
            await write_to_otchet(message)
            await admin(message)
            await state.finish()
        else:
            await bot.send_message(message.chat.id, f'{message.chat.first_name}, не играйтесь!😠')
    except Exception as e:
        print(e)



async def admin(message):
    try:
        requests.post(url='http://34.64.233.41/api/up/', data={"group": otchet.get(message.chat.first_name), \
                                                               "user_name": message.chat.first_name, \
                                                               "before": otchet1.get(message.chat.first_name), \
                                                               "after": otchet2.get(message.chat.first_name)})
    except Exception as e:
        print(e)


async def write_to_csv(message):
    try:
        chat_id = str(message.chat.id)
        file_name = 'user_id.csv'
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write("%s\n"%(int(chat_id)))
    except Exception as e:
        print(e)



async def write_even_to_csv(message):
    try:
        chat_id = message.chat.id
        file_name = 'user_even.csv'
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write("%s\n"%(int(chat_id)))
    except Exception as e:
        print(e)



async def write_to_otchet(message):
    try:
        chat_id = str(message.chat.id)
        file_name = 'otchet.csv'
        with open(file_name, 'a+', encoding='utf-8') as f:
            f.write("%s\n"%(int(chat_id)))
    except Exception as e:
        print(e)


async def clear_otchet():
    try:
        with open('otchet.csv', 'w') as f_clear:
            clearer = f_clear.write('')
            return clearer
    except Exception as e:
        print(e)


async def python_to_run():
    try:
        for i in python_csv:
            await bot.send_message(i, 'Пришло время пройти /start', parse_mode='markdown')
    except Exception as e:
        print(e)


async def python_even_to_runun():
    try:
        for i in python_even_csv:
            await bot.send_message(i, 'Пришло время пройти /start', parse_mode='markdown')
    except Exception as e:
        print(e)


async def scheduler():
    try:
        aioschedule.every().day.at("04:08").do(clear_otchet)
        aioschedule.every().day.at("04:08").do(python_to_run)
        aioschedule.every().day.at("04:08").do(python_file)

        aioschedule.every().day.at("11:50").do(clear_otchet)
        aioschedule.every().day.at("11:50").do(answer_day)
        aioschedule.every().day.at("11:50").do(python_file)


        aioschedule.every().day.at("12:20").do(python_even_file)
        aioschedule.every().day.at("12:20").do(python_even_to_runun)
        aioschedule.every().day.at("12:20").do(clear_otchet)

        aioschedule.every().day.at("15:20").do(clear_otchet)
        aioschedule.every().day.at("15:20").do(python_even_file)
        aioschedule.every().day.at("15:20").do(answer_even)
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except Exception as e:
        print(e)


async def on_startup(x):
    try:
        asyncio.create_task(scheduler())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
