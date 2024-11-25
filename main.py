from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = ""
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главная клавиатура с добавленной кнопкой "Купить"
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Купить"), KeyboardButton("Информация"))

# Inline меню для покупки
buying_menu = InlineKeyboardMarkup(row_width=2)
for i in range(1, 5):
    buying_menu.add(InlineKeyboardButton(f"Product{i}", callback_data="product_buying"))

# Хэндлер для команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие из меню:", reply_markup=main_menu)

# Хэндлер для кнопки "Купить"
@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    # Отправка информации о продуктах
    for i in range(1, 5):
        await message.answer_photo(
            photo=f"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQbgAaE0jW2E5IOry_ic_7SwLSs-Kt4TxdGvw&s{i}",
            caption=f"Название: Product{i} | Описание: описание {i} | Цена: {i * 100}"
        )
    # Отправка Inline меню
    await message.answer("Выберите продукт для покупки:", reply_markup=buying_menu)

# Callback хэндлер для покупки продукта
@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call: types.CallbackQuery):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()  # Убираем "часики" на кнопке

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
