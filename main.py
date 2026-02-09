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


# import os
# from typing import Optional

# from fastapi import FastAPI, Request
# from pydantic import BaseModel

# from telegram import Update, Bot
# from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler

# TOKEN = os.environ.get("TOKEN")

# app = FastAPI()

# class TelegramWebhook(BaseModel):
#     '''
#     Telegram Webhook Model using Pydantic for request body validation
#     '''
#     update_id: int
#     message: Optional[dict]
#     edited_message: Optional[dict]
#     channel_post: Optional[dict]
#     edited_channel_post: Optional[dict]
#     inline_query: Optional[dict]
#     chosen_inline_result: Optional[dict]
#     callback_query: Optional[dict]
#     shipping_query: Optional[dict]
#     pre_checkout_query: Optional[dict]
#     poll: Optional[dict]
#     poll_answer: Optional[dict]

# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

# def register_handlers(dispatcher):
#     start_handler = CommandHandler('start', start)
#     dispatcher.add_handler(start_handler)

# @app.post("/webhook")
# def webhook(webhook_data: TelegramWebhook):
#     '''
#     Telegram Webhook
#     '''
#     # Method 1
#     bot = Bot(token="8563640047:AAEefEsTrT9PaR7ONYff82StoUkQwYOOKWI")
#     update = Update.de_json(webhook_data.__dict__, bot) # convert the Telegram Webhook class to dictionary using __dict__ dunder method
#     dispatcher = Dispatcher(bot, None, workers=4)
#     register_handlers(dispatcher)

#     # handle webhook request
#     dispatcher.process_update(update)

#     # Method 2
#     # you can just handle the webhook request here without using python-telegram-bot
#     # if webhook_data.message:
#     #     if webhook_data.message.text == '/start':
#     #         send_message(webhook_data.message.chat.id, 'Hello World')

#     return {"message": "ok"}

# app = FastAPI()

# @app.get("/")
# def index():
#     return {"message": "Hello World"}

# # This is important for Vercel
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8001)#


# @app.get("/")
# def read_root():
#     return {"message": "Hello World from FastAPI on Vercel!"}

# @app.get("/api/health")
# def health_check():
#     return {"status": "healthy"}