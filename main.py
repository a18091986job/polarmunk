import os
import logging
from fastapi import FastAPI, Request, HTTPException
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота
TOKEN = os.environ.get("TOKEN", "8563640047:AAEefEsTrT9PaR7ONYff82StoUkQwYOOKWI")

# Создаем приложение FastAPI
app = FastAPI()

# Создаем бота и диспетчер
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("I'm a bot, please talk to me!")

@dp.message()
async def echo_message(message: types.Message):
    await message.answer(f"You said: {message.text}")

@app.post("/webhook")
async def webhook(request: Request):
    """
    Обработка вебхука от Telegram
    """
    try:
        # Получаем данные вебхука
        data = await request.json()
        
        # Создаем объект Update
        update = Update(**data)
        
        # Обрабатываем обновление
        await dp.feed_webhook_update(bot=bot, update=update)
        
        return {"message": "ok"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.get("/set_webhook")
async def set_webhook():
    """
    Установка вебхука
    """
    # Получаем URL из окружения или указываем вручную
    webhook_url = os.environ.get("WEBHOOK_URL", "https://your-app.vercel.app/webhook")
    
    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True
    )
    
    return {"message": f"Webhook set to {webhook_url}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)#


# curl 'https://api.telegram.org/bot8563640047:AAEefEsTrT9PaR7ONYff82StoUkQwYOOKWI/setWebhook?url=https://polarmunk.vercel.app/webhook'