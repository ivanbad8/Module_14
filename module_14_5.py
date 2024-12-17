from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from crud_functions import *

api = ('')
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb_1 = InlineKeyboardMarkup(row_width=4)
kb_1.add(InlineKeyboardButton(text='Product1', callback_data="product_buying"),
         InlineKeyboardButton(text='Product2', callback_data="product_buying"),
         InlineKeyboardButton(text='Product3', callback_data="product_buying"),
         InlineKeyboardButton(text='Product4', callback_data="product_buying"))

kb_2 = ReplyKeyboardMarkup()
start_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Рассчитать норму калорий'),
                                            KeyboardButton(text='Регистрация')],
                                           [KeyboardButton(text='Купить'),
                                            KeyboardButton(text='Информация')]],
                                 resize_keyboard=True)

get_all_products()


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    with open('imeg14_3_1.jpg', 'rb') as img1:
        await message.answer(
            f'Название: {get_all_products()[0][0]} | Описание:{get_all_products()[0][1]}  | Цена: {get_all_products()[0][2]}')
        await message.answer_photo(photo=img1)
    with open('imeg14_3_2.jpg', 'rb') as img2:
        await message.answer(
            f'Название: {get_all_products()[1][0]} | Описание:{get_all_products()[1][1]}  | Цена: {get_all_products()[1][2]}')
        await message.answer_photo(photo=img2)
    with open('imeg14_3_1.jpg', 'rb') as img3:
        await message.answer(
            f'Название: {get_all_products()[2][0]} | Описание:{get_all_products()[2][1]}  | Цена: {get_all_products()[2][2]}')
        await message.answer_photo(photo=img3)
    with open('imeg14_3_1.jpg', 'rb') as img4:
        await message.answer(
            f'Название: {get_all_products()[3][0]} | Описание:{get_all_products()[3][1]}  | Цена: {get_all_products()[3][2]}')
        await message.answer_photo(photo=img4)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_1)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text='/start')
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью', reply_markup=start_menu)


@dp.message_handler(text='Рассчитать норму калорий')
async def inform(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    await state.get_data()
    data = await state.get_data()
    age = int(data.get('age'))
    growth = int(data.get('growth'))
    weight = int(data.get('weight'))
    kal_ = 10 * weight + 6.25 * growth - 5 * age + 5
    await message.answer(f'Ваша норма калорий {kal_}.')
    await state.finish()


@dp.message_handler(text='Информация')
async def all_massages(message):
    await message.answer('В нашем боте вы можете заказать бады и витамины, а так же рассчитать Вашу норму калорий.')


class RegistrationState(UserState, StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text) is True:
        await message.answer("Пользователь существует, введите другое имя")
    else:
        await state.update_data(username=message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст:')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    await state.get_data()
    data = await state.get_data()
    username = data.get('username')
    email = data.get('email')
    age = data.get('age')
    add_user(username, email, age)
    await message.answer('Регистрация прошла успешно.')
    await state.finish()


@dp.message_handler()
async def start_bot(message):
    await message.answer('>>> /start <<<')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
