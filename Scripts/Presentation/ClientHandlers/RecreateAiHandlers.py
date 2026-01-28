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
from Scripts.Domain.Data.UserData import UserData
from Scripts.Domain.States.ChangeAiStates import ChangeAiStates
from Scripts.Domain.States.CreatingAiStates import CreatingAiStates


class RecreateAiHandlers:

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
        dp.message.register(self.recreate_ai, Command("recreate_ai"))


    async def recreate_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.get_number_ai, parse_mode=ParseMode.HTML)

        await state.set_state(CreatingAiStates.number_bot)

    async def set_number_ai(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.get_name_ai, parse_mode=ParseMode.HTML)

        await state.update_data(number_ai=message.text)
        await state.set_state(CreatingAiStates.prompt)

    async def set_name_ai(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.get_prompt_ai, parse_mode=ParseMode.HTML)

        await state.update_data(number_ai=message.text)
        await state.set_state(CreatingAiStates.prompt)

    async def set_prompt_ai(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.input_language_ai, parse_mode=ParseMode.HTML)

        await state.update_data(prompt=message.text)
        await state.set_state(CreatingAiStates.language)

    async def set_language_ai(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        data = await state.get_data()
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        ai_data = AiData()
        ai_data.prompt = data["prompt"]
        ai_data.language = data["language"]

        is_recreated = self.recreate_ai_usecase.execute(id, ai_data)

        if is_recreated:
            await message.answer(texts.ai_recreated, parse_mode=ParseMode.HTML)
        else:
            await message.answer(texts.ai_recreated_error, parse_mode=ParseMode.HTML)

        await state.clear()
