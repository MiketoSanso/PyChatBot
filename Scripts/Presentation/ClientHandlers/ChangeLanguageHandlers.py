import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery

from Scripts.Application.UseCases.AddUserUseCase import AddUserUseCase
from Scripts.Application.UseCases.ChangeAiUseCase import ChangeAiUseCase
from Scripts.Application.UseCases.ChangeUserLanguageUseCase import ChangeUserLanguageUseCase
from Scripts.Application.UseCases.GetUserDataUseCase import GetUserDataUseCase
from Scripts.Application.UseCases.LoggingAccessPaymentUseCase import LoggingAccessPaymentUseCase
from Scripts.Application.UseCases.RecreateAiUseCase import RecreateAiUseCase
from Scripts.Application.UseCases.ReturnTextsUseCase import ReturnTextsUseCase
from Scripts.Domain.Data.AiData import AiData
from Scripts.Domain.Data.Languages import Languages


class ChangeLanguageHandlers:

    def __init__(self,
                 add_user_usecase: AddUserUseCase,
                 change_ai_usecase: ChangeAiUseCase,
                 change_user_language_usecase: ChangeUserLanguageUseCase,
                 recreate_ai_usecase: RecreateAiUseCase,
                 logging_access_payment_usecase: LoggingAccessPaymentUseCase,
                 return_texts_usecase: ReturnTextsUseCase,
                 get_user_data_usecase: GetUserDataUseCase):

        self.get_user_data_usecase = get_user_data_usecase
        self.add_user_usecase = add_user_usecase
        self.change_ai_usecase = change_ai_usecase
        self.change_user_language_usecase = change_user_language_usecase
        self.recreate_ai_usecase = recreate_ai_usecase
        self.logging_access_payment_usecase = logging_access_payment_usecase
        self.return_texts_usecase = return_texts_usecase

    def register_handlers(self, dp: Dispatcher):
        dp.message.register(self.change_language, Command("change_language"))

        dp.callback_query.register(self.input_russian, F.data == str(Languages.rus))
        dp.callback_query.register(self.input_english, F.data == str(Languages.eng))
        dp.callback_query.register(self.input_china, F.data == str(Languages.chi))
        dp.callback_query.register(self.input_deutsch, F.data == str(Languages.de))

    async def change_language(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        inline_kb = [
            [types.InlineKeyboardButton(text=texts.language_ru, callback_data=str(Languages.rus))],
            [types.InlineKeyboardButton(text=texts.language_eng, callback_data=str(Languages.eng))],
            [types.InlineKeyboardButton(text=texts.language_chi, callback_data=str(Languages.chi))],
            [types.InlineKeyboardButton(text=texts.language_de, callback_data=str(Languages.de))]
        ]

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)

        await message.answer(
            text=texts.input_language_ai,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

    async def input_english(self, callback_query: types.CallbackQuery, state: FSMContext):
        id = callback_query.from_user.id
        await self.access_input_language(id, Languages.eng, callback_query)

    async def input_russian(self, callback_query: types.CallbackQuery, state: FSMContext):
        id = callback_query.from_user.id
        await self.access_input_language(id, Languages.rus, callback_query)

    async def input_china(self, callback_query: types.CallbackQuery, state: FSMContext):
        id = callback_query.from_user.id
        await self.access_input_language(id, Languages.chi, callback_query)

    async def input_deutsch(self, callback_query: types.CallbackQuery, state: FSMContext):
        id = callback_query.from_user.id
        await self.access_input_language(id, Languages.de, callback_query)

    async def access_input_language(self, id: int, language: Languages, callback_query: types.CallbackQuery):
        self.change_user_language_usecase.execute(id, language)
        texts = self.return_texts_usecase.execute(id)

        await callback_query.answer()

        try:
            await callback_query.message.edit_text(
                text=f"{texts.language_changed} {language}",
                parse_mode=ParseMode.HTML
            )
        except:
            await callback_query.message.answer(
                text=f"{texts.language_changed} {language}",
                parse_mode=ParseMode.HTML
            )