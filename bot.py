import logging

from aiogram import Bot, Dispatcher, executor, types
from config import get_config


cfg = get_config()
logging.basicConfig(level=getattr(logging, cfg.LOG_LEVEL.upper(), logging.INFO))


def main():
	bot = Bot(token=cfg.BOT_TOKEN)
	dp = Dispatcher(bot)

	@dp.message_handler()
	async def echo(message: types.Message):
		await message.answer(message.text)

	executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
	main()

