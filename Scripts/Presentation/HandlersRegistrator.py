import asyncio

from aiogram import Bot, Dispatcher, types, F

from Scripts.Presentation.ClientHandlers.ChangeLanguageHandlers import ChangeLanguageHandlers
from Scripts.Presentation.ClientHandlers.BaseHandlers import BaseHandlers
from Scripts.Presentation.ClientHandlers.RecreateAiHandlers import RecreateAiHandlers
from Scripts.Presentation.ClientHandlers.ShopHandlers import ShopHandlers


class HandlersRegistrator:

    def __init__(self, base_handlers: BaseHandlers,
                 change_language_handlers: ChangeLanguageHandlers,
                 recreate_ai_handlers: RecreateAiHandlers,
                 shop_handlers: ShopHandlers):
        BOT_TOKEN = "8588091640:AAGz9_NJxTciE7MszsJRccWq109ULyrJET8"

        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()

        base_handlers.register_handlers(self.dp)
        change_language_handlers.register_handlers(self.dp)
        recreate_ai_handlers.register_handlers(self.dp)
        shop_handlers.register_handlers(self.dp)

        asyncio.run(self.start_bot())

    async def start_bot(self):
        await self.dp.start_polling(self.bot)