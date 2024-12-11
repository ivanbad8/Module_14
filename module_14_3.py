from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
                                           KeyboardButton(text='Информация')],
                                           [KeyboardButton(text='Купить')]],
                                 resize_keyboard=True)


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    for i in range(1,5):
        with open(f'imeg14_3_{i}.jpg', 'rb') as img:
            await message.answer(f'Название: Product{i} | Описание: описание{i} | Цена: {i*100}')
            await message.answer_photo(photo=img)
    await message.answer('Выберите продукт для покупки:', reply_markup=kb_1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

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


@dp.message_handler()
async def all_massages(message):
    await message.answer('👉/start')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
