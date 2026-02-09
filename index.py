import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import get_config


cfg = get_config()
logging.basicConfig(level=getattr(logging, cfg.LOG_LEVEL.upper(), logging.INFO))


async def main():
    # Создаем бота с новым API aiogram 3.7.0+
    bot = Bot(
        token=cfg.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    @dp.message()
    async def echo(message: types.Message):
        await message.answer(message.text)

    # Запускаем бота
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


# import logging
# import asyncio

# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.utils.exceptions import BotBlocked
# from config import get_config


# cfg = get_config()
# logging.basicConfig(level=getattr(logging, cfg.LOG_LEVEL.upper(), logging.INFO))


# async def on_startup_notify(dp: Dispatcher):
#     """Отправляет сообщение при запуске бота"""
#     try:
#         # Отправка сообщения в конкретный чат (замените на нужный ID)
#         await dp.bot.send_message(
#             chat_id=cfg.ADMIN_CHAT_ID,  # Добавьте ADMIN_CHAT_ID в конфиг
#             text="🤖 Бот запущен и готов к работе!"
#         )
#     except BotBlocked:
#         logging.warning("Бот заблокирован пользователем")
#     except Exception as e:
#         logging.error(f"Не удалось отправить сообщение при запуске: {e}")


# def main():
#     bot = Bot(token=cfg.BOT_TOKEN)
#     dp = Dispatcher(bot)

#     @dp.message_handler()
#     async def echo(message: types.Message):
#         await message.answer(message.text)

#     # Запускаем бота с функцией on_startup
#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup_notify)


# if __name__ == '__main__':
#     main()
