import asyncio
import datetime
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode

TOKEN = "5817191373:AAG3bDIu46VjB17IRu96NaVmRNfZrc3a79s"
# Создание объекта бота
bot = Bot(TOKEN)

# Создание объекта диспетчера
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Отправляем приветственное сообщение
    await message.reply("Приветик, солнышко, выбери пункт, что ты сейчас будеф делать!",
                        reply_markup=get_food_menu())

# Функция для создания меню с выбором типа еды (завтрак, обед, ужин)
def get_food_menu():
    markup = types.InlineKeyboardMarkup(row_width=3)
    breakfast_button = types.InlineKeyboardButton("Завтракать 🍳", callback_data='завтракать')
    lunch_button = types.InlineKeyboardButton("Обедать 🍔", callback_data='обедать')
    dinner_button = types.InlineKeyboardButton("Ужинать 🍲", callback_data='ужинать')
    markup.add(breakfast_button, lunch_button, dinner_button)
    return markup

# Обработчик нажатия на кнопки с выбором типа еды (завтрак, обед, ужин)
@dp.callback_query_handler(lambda query: query.data in ['завтракать', 'обедать', 'ужинать'])
async def process_food_type(callback_query: types.CallbackQuery):
    food_type = callback_query.data
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Ты выбрала {food_type}. Теперь напиши фто мой котенок будет куфать:")

# Обработчик текстовых сообщений с заказом еды
@dp.message_handler(lambda message: True)
async def process_food_order(message: types.Message):
    # Проверяем, является ли сообщение названием еды
    order_text = message.text.strip()

    if order_text:
        # Форматируем текущую дату и время
        now = datetime.datetime.now().strftime("%d-%m %H:%M")
        # Отправляем сообщение с подтверждением заказа и временем отправки
        await message.answer(f"То что ты покушала, а именно '{order_text}'  было отправлено твоему мальчику в {now}",
                              reply_markup=types.ReplyKeyboardRemove())
        # Отправляем уведомление другому пользователю о новом заказе и времени отправки
        await bot.send_message(chat_id='963433317', text=f"Зайка ({message.from_user.full_name}) поела {order_text} в {now}")
# Обработчик ошибок
@dp.errors_handler(exception=Exception)
async def error_handler(update: types.Update, exception: Exception):
    print(f"Exception: {exception}")
    await update.message.reply("Произошла ошибка, попробуйте еще раз")

# Запускаем бота
if __name__ == '__main__':
    asyncio.run(dp.start_polling())