import handlers
import service_handlers
from aiogram import Bot, Dispatcher
from config import load_config

API_TOKEN: str = load_config().tg_bot.token

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

dp.include_router(serice_handlers.router)
dp.include_router(haders.router)


if __name__ == '__main__':
    dp.run_polling(bot)
