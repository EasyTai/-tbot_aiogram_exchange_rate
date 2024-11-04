import logging
import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота
API_TOKEN = '7148115594:AAE-b2je0ts3wBzK119gekBfMf4bgl3aN74'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Функция для получения курса доллара
def get_usd_rub():
    try:
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        data = response.json()
        usd_rate = data['Valute']['USD']['Value']
        return round(usd_rate, 2)
    except Exception as e:
        logging.error(f"Error fetching exchange rate: {e}")
        return None

# Хэндлер на команду /start
@dp.message(Command('start'))
async def send_welcome(message: Message):
    await message.answer("Добрый день. Как вас зовут?")

# Хэндлер для обработки имени пользователя
@dp.message()
async def get_name(message: Message):
    name = message.text
    usd_rate = get_usd_rub()

    if usd_rate:
        response_message = f"Рад знакомству, {name}! Курс доллара сегодня {usd_rate}р."
    else:
        response_message = f"Рад знакомству, {name}! Не удалось получить курс доллара."

    await message.answer(response_message)

# Основная функция для запуска бота
async def main():
    # Удаляем вебхуки, если они есть, и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(main())
