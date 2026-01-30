import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery

from Scripts.Application.UseCases.AddUserUseCase import AddUserUseCase
from Scripts.Application.UseCases.ChangeAiUseCase import ChangeAiUseCase
from Scripts.Application.UseCases.ChangeUserLanguageUseCase import ChangeUserLanguageUseCase
from Scripts.Application.UseCases.GetUserDataUseCase import GetUserDataUseCase
from Scripts.Application.UseCases.LoggingAccessPaymentUseCase import LoggingAccessPaymentUseCase
from Scripts.Application.UseCases.RecreateAiUseCase import RecreateAiUseCase
from Scripts.Application.UseCases.ReturnTextsUseCase import ReturnTextsUseCase
from Scripts.Application.UseCases.SendUserMessageUseCase import SendUserMessageUseCase
from Scripts.Domain.Data.AiData import AiData
from Scripts.Domain.Data.Languages import Languages
from Scripts.Domain.Data.UserData import UserData
from Scripts.Domain.States.ChangeAiStates import ChangeAiStates
from Scripts.Domain.States.CreatingAiStates import CreatingAiStates


class BaseHandlers:

    def __init__(self,
                 add_user_usecase: AddUserUseCase,
                 change_ai_usecase: ChangeAiUseCase,
                 change_user_language_usecase: ChangeUserLanguageUseCase,
                 recreate_ai_usecase: RecreateAiUseCase,
                 logging_access_payment_usecase: LoggingAccessPaymentUseCase,
                 return_texts_usecase: ReturnTextsUseCase,
                 get_user_data_usecase: GetUserDataUseCase,
                 send_user_message_usecase: SendUserMessageUseCase):

        self.send_user_message_usecase = send_user_message_usecase
        self.get_user_data_usecase = get_user_data_usecase
        self.add_user_usecase = add_user_usecase
        self.change_ai_usecase = change_ai_usecase
        self.change_user_language_usecase = change_user_language_usecase
        self.recreate_ai_usecase = recreate_ai_usecase
        self.logging_access_payment_usecase = logging_access_payment_usecase
        self.return_texts_usecase = return_texts_usecase

    def register_handlers(self, dp: Dispatcher):
        dp.message.register(self.help, Command("help"))
        dp.message.register(self.start, Command("start"))
        dp.message.register(self.account, Command("account"))
        dp.message.register(self.start_change_ai, Command("change_ai"))

        dp.message.register(self.change_ai, ChangeAiStates.change_ai)

        dp.message.register(self.send_message, F.text,
                    ~F.text.startswith("/"),
                    StateFilter("default"))

    async def start(self, message: types.Message):
        user_language = message.from_user.language_code
        language = Languages.rus

        if user_language == "en":
            language = Languages.eng
        elif user_language == "chi":
            language = Languages.chi
        elif user_language == "de":
            language = Languages.de

        data = UserData()
        data.language = language
        id = message.from_user.id

        self.add_user_usecase.execute(id, data)

        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.start, parse_mode=ParseMode.HTML)

    async def help(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.help, parse_mode=ParseMode.HTML)

    async def account(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        data = self.get_user_data_usecase.execute(id)

        language_text = texts.language_ru

        if data.language == "en":
            language_text = texts.language_eng
        elif data.language == "chi":
            language_text = texts.language_chi
        elif data.language == "de":
            language_text = texts.language_de


        await message.answer(f"{texts.account_word}\n\n"
                             f"{texts.bold_word_tokens}: {data.tokens}\n"
                             f"{texts.count_bot_slots}: {data.count_ai}\n"
                             f"{texts.language_word}: {language_text}\n"
                             f"{texts.active_ai_text}: {data.active_ai}\n"
                             f"{texts.post_parameters_account}", parse_mode=ParseMode.HTML)

    async def start_change_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.change_ai, parse_mode=ParseMode.HTML)

        await state.set_state(ChangeAiStates.change_ai)

    async def change_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        is_changed = False

        try:
            is_changed = self.change_ai_usecase.execute(id, int(message.text))
        except ValueError:
            await message.answer(texts.change_ai_text_error, parse_mode=ParseMode.HTML)

        if is_changed:
            await message.answer(texts.change_ai_successful, parse_mode=ParseMode.HTML)
        else:
            await message.answer(texts.change_ai_error, parse_mode=ParseMode.HTML)

        await state.clear()

    async def send_message(self, message: types.Message):
        id = message.from_user.id
        answer = await self.send_user_message_usecase.execute(id, message.text)
        await message.answer(answer)