from aiogram import Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from Scripts.Application.UseCases.ChangeAiUseCase import ChangeAiUseCase
from Scripts.Application.UseCases.ChangeUserLanguageUseCase import ChangeUserLanguageUseCase
from Scripts.Application.UseCases.GetUserDataUseCase import GetUserDataUseCase
from Scripts.Application.UseCases.LoggingAccessPaymentUseCase import LoggingAccessPaymentUseCase
from Scripts.Application.UseCases.RecreateAiUseCase import RecreateAiUseCase
from Scripts.Application.UseCases.ReturnTextsUseCase import ReturnTextsUseCase
from Scripts.Domain.Data.AiData import AiData
from Scripts.Domain.Data.Languages import Languages
from Scripts.Domain.States.CreatingAiStates import CreatingAiStates


class RecreateAiHandlers:

    def __init__(self,
                 change_ai_usecase: ChangeAiUseCase,
                 change_user_language_usecase: ChangeUserLanguageUseCase,
                 recreate_ai_usecase: RecreateAiUseCase,
                 logging_access_payment_usecase: LoggingAccessPaymentUseCase,
                 return_texts_usecase: ReturnTextsUseCase,
                 get_user_data_usecase: GetUserDataUseCase):

        self.get_user_data_usecase = get_user_data_usecase
        self.change_ai_usecase = change_ai_usecase
        self.change_user_language_usecase = change_user_language_usecase
        self.recreate_ai_usecase = recreate_ai_usecase
        self.logging_access_payment_usecase = logging_access_payment_usecase
        self.return_texts_usecase = return_texts_usecase

    def register_handlers(self, dp: Dispatcher):
        dp.message.register(
            self.recreate_ai,
            Command("recreate_ai"),
            StateFilter(default_state)
        )

        #dp.message.register(self.cancel_recreate, Command("cancel")) #TODO: Добавить

        dp.message.register(self.set_number_ai, CreatingAiStates.number_bot)
        dp.message.register(self.set_name_ai, CreatingAiStates.name_bot)
        dp.message.register(self.set_prompt_ai, CreatingAiStates.prompt)

        dp.callback_query.register(
            self.set_language_ai,
            CreatingAiStates.language,
            F.data.in_([str(Languages.rus.value), str(Languages.eng.value),
                        str(Languages.chi.value), str(Languages.de.value)]))

    async def recreate_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.get_number_ai, parse_mode=ParseMode.HTML)

        await state.set_state(CreatingAiStates.number_bot)

    async def set_number_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)
        user_data = self.get_user_data_usecase.execute(id)

        if not message.text.isdigit():
            await message.answer("Ответ должен быть числом!")
            return
        elif user_data.count_ai < int(message.text) or int(message.text) < 1:
            await message.answer("Число вне допустимых значений!")
            return

        await message.answer(texts.get_name_ai, parse_mode=ParseMode.HTML)

        await state.update_data(number_ai=message.text)
        await state.set_state(CreatingAiStates.name_bot)

    async def set_name_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.get_prompt_ai, parse_mode=ParseMode.HTML)

        await state.update_data(number_ai=message.text)
        await state.set_state(CreatingAiStates.prompt)

    async def set_prompt_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        inline_kb = [
            [types.InlineKeyboardButton(text=texts.language_ru, callback_data=str(Languages.rus.value))],
            [types.InlineKeyboardButton(text=texts.language_eng, callback_data=str(Languages.eng.value))],
            [types.InlineKeyboardButton(text=texts.language_chi, callback_data=str(Languages.chi.value))],
            [types.InlineKeyboardButton(text=texts.language_de, callback_data=str(Languages.de.value))]
        ]

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)

        await message.answer(
            text=texts.input_language_ai,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

        await state.update_data(prompt=message.text)
        await state.set_state(CreatingAiStates.language)

    async def set_language_ai(self, callback_query: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        id = callback_query.from_user.id
        texts = self.return_texts_usecase.execute(id)
        callback_data = callback_query.data

        print(callback_data)

        ai_data = AiData()
        ai_data.prompt = data["prompt"]
        ai_data.language = Languages(callback_data)

        is_recreated = self.recreate_ai_usecase.execute(id, ai_data)




        if is_recreated:
            await callback_query.answer(texts.ai_recreated, parse_mode=ParseMode.HTML)
        else:
            await callback_query.answer(texts.ai_recreated_error, parse_mode=ParseMode.HTML)

        await state.clear()
