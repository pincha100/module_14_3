from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = ""
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главная клавиатура с кнопками "Купить", "Информация" и "Рассчитать"
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Купить"), KeyboardButton("Информация"), KeyboardButton("Рассчитать"))

# Inline меню для расчёта
calc_menu = InlineKeyboardMarkup(row_width=2)
calc_menu.add(
    InlineKeyboardButton("Рассчитать норму калорий", callback_data="calories"),
    InlineKeyboardButton("Формулы расчёта", callback_data="formulas")
)

buying_menu = InlineKeyboardMarkup(row_width=2)
for i in range(1, 5):
    buying_menu.add(InlineKeyboardButton(f"Product{i}", callback_data="product_buying"))

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие из меню:", reply_markup=main_menu)

@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    # Отправка информации о продуктах
    for i in range(1, 5):
        await message.answer_photo(
            photo=f"https://via.placeholder.com/150?text=Product{i}",
            caption=f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}"
        )
    # Отправка Inline меню
    await message.answer("Выберите продукт для покупки:", reply_markup=buying_menu)

# Хэндлер для кнопки "Рассчитать"
@dp.message_handler(text="Рассчитать")
async def main_menu_handler(message: types.Message):
    await message.answer("Выберите опцию:", reply_markup=calc_menu)

# Callback хэндлер для кнопки "Рассчитать норму калорий"
@dp.callback_query_handler(text="calories")
async def set_age(call: types.CallbackQuery):
    await call.message.answer("Введите ваш возраст для расчёта калорий:")
    await call.answer()  # Убираем "часики" на кнопке

# Callback хэндлер для кнопки "Формулы расчёта"
@dp.callback_query_handler(text="formulas")
async def get_formulas(call: types.CallbackQuery):
    formula = (
        "Формула Миффлина-Сан Жеора:\n"
        "Мужчины: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (лет) + 5\n"
        "Женщины: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (лет) − 161"
    )
    await call.message.answer(formula)
    await call.answer()

# Callback хэндлер для покупки продукта
@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()  # Убираем "часики" на кнопке

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
