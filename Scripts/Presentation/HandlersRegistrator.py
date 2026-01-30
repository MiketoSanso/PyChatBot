import asyncio

from aiogram import Bot, Dispatcher, types, F

from Scripts.Infrastructure.TechData.Constants import Constants
from Scripts.Presentation.ClientHandlers.ChangeLanguageHandlers import ChangeLanguageHandlers
from Scripts.Presentation.ClientHandlers.BaseHandlers import BaseHandlers
from Scripts.Presentation.ClientHandlers.RecreateAiHandlers import RecreateAiHandlers
from Scripts.Presentation.ClientHandlers.ShopHandlers import ShopHandlers


class HandlersRegistrator:

    def __init__(self, constants: Constants,
                 base_handlers: BaseHandlers,
                 change_language_handlers: ChangeLanguageHandlers,
                 recreate_ai_handlers: RecreateAiHandlers,
                 shop_handlers: ShopHandlers):

        self.bot = Bot(constants.BOT_TOKEN)
        self.dp = Dispatcher()

        base_handlers.register_handlers(self.dp)
        change_language_handlers.register_handlers(self.dp)
        recreate_ai_handlers.register_handlers(self.dp)
        shop_handlers.register_handlers(self.dp)

        asyncio.run(self.start_bot())

    async def start_bot(self):
        await self.register_keyboard()
        await self.dp.start_polling(self.bot)


    async def register_keyboard(self):
        commands = [
            types.BotCommand(command="/start", description="Запустить бота"),
            types.BotCommand(command="/help", description="Помощь"),
            types.BotCommand(command="/account", description="Аккаунт"),
            types.BotCommand(command="/change_language", description="Изменить язык"),

            types.BotCommand(command="/buy_tokens", description="Купить токены"),
            types.BotCommand(command="/buy_ai_place", description="Купить место под новый AI"),
            types.BotCommand(command="/recreate_ai", description="Пересоздать AI"),
            types.BotCommand(command="/change_ai", description="Сменить активный AI"),
        ]

        await self.bot.set_my_commands(
            commands=commands,
            scope=types.BotCommandScopeDefault()
        )