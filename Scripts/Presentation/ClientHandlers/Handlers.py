import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery

from Scripts.Application.UseCases.AddUserUseCase import AddUserUseCase
from Scripts.Application.UseCases.ChangeAiUseCase import ChangeAiUseCase
from Scripts.Application.UseCases.ChangeUserLanguageUseCase import ChangeUserLanguageUseCase
from Scripts.Application.UseCases.LoggingAccessPaymentUseCase import LoggingAccessPaymentUseCase
from Scripts.Application.UseCases.RecreateAiUseCase import RecreateAiUseCase
from Scripts.Application.UseCases.ReturnTextsUseCase import ReturnTextsUseCase
from Scripts.Domain.Data.AiData import AiData
from Scripts.Domain.Data.Languages import Languages
from Scripts.Domain.Data.UserData import UserData
from Scripts.Domain.States.ChangeAiStates import ChangeAiStates
from Scripts.Domain.States.CreatingAiStates import CreatingAiStates
from Scripts.Infrastructure.TextsData.RussianTexts import RussianTexts


class Handlers:

    def __init__(self,
                 add_user_usecase: AddUserUseCase,
                 change_ai_usecase: ChangeAiUseCase,
                 change_user_language_usecase: ChangeUserLanguageUseCase,
                 recreate_ai_usecase: RecreateAiUseCase,
                 logging_access_payment_usecase: LoggingAccessPaymentUseCase,
                 return_texts_usecase: ReturnTextsUseCase):
        BOT_TOKEN = "8588091640:AAGz9_NJxTciE7MszsJRccWq109ULyrJET8"

        self.add_user_usecase = add_user_usecase
        self.change_ai_usecase = change_ai_usecase
        self.change_user_language_usecase = change_user_language_usecase
        self.recreate_ai_usecase = recreate_ai_usecase
        self.logging_access_payment_usecase = logging_access_payment_usecase
        self.return_texts_usecase = return_texts_usecase

        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher()
        self.__register_handlers()

        asyncio.run(self.start_bot())

    async def start_bot(self):
        await self.dp.start_polling(self.bot)

    def __register_handlers(self):
        self.dp.message.register(self.help, Command("help"))
        self.dp.message.register(self.start, Command("start"))
        self.dp.message.register(self.change_ai, Command("account"))

        self.dp.message.register(self.change_ai, Command("start_change_ai"))
        self.dp.message.register(self.recreate_ai, Command("recreate_ai"))
        self.dp.message.register(self.buy_ai_place, Command("buy_ai_place"))
        self.dp.message.register(self.change_language, Command("change_language"))

        #trading
        self.dp.message.register(self.buy_tokens, Command("buy_tokens"))
        self.dp.pre_checkout_query.register(self.process_pre_checkout)
        self.dp.message.register(self.process_successful_payment, content_types=types.ContentType.SUCCESSFUL_PAYMENT)

    async def start(self, message: types.Message):
        user_language = message.from_user.language_code
        data = UserData()
        data.language = user_language
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.start)

        await self.add_user_usecase.execute(id, data)

    async def help(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.help)

    async def account(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(f"Токенов: {X}"
                             f"Количество слотов для ботов: {y}"
                             f"Язык: {z}"
                             f"") #TODO: Настроить текст аккаунта

    async def process_successful_payment(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        payment = message.successful_payment

        await self.logging_access_payment_usecase.execute(payment)

        if message.successful_payment == "month_sub":
            await message.answer(texts.successful_payment + {payment.order_info.email})

    async def process_pre_checkout(self, pre_checkout_query: PreCheckoutQuery):
        await self.bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout_query.id,
            ok=True,
            error_message=None
        )

    async def buy_tokens(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        # Создаем список цен (в минимальных единицах валюты)
        prices = [
            LabeledPrice(label=f"1000 {texts.word_tokens}", amount=15_000),
            LabeledPrice(label=f"3000 {texts.word_tokens}", amount=43_000),
            LabeledPrice(label=f"5000 {texts.word_tokens}", amount=65_000),
            LabeledPrice(label=f"10000 {texts.word_tokens}", amount=125_000),
            LabeledPrice(label=f"50000 {texts.word_tokens}", amount=600_000),
            LabeledPrice(label=f"200000 {texts.word_tokens}", amount=2500_000),
        ]

        TOKEN_PAYMENTS = "1744374395:TEST:e1139428288af4683452"

        await self.bot.send_invoice(
            chat_id=message.chat.id,
            title=texts.transaction_tokens_title,
            description=texts.transaction_tokens_description,
            payload="Tockens",
            provider_token=TOKEN_PAYMENTS,
            currency="RUB",
            prices=prices,
            start_parameter="premium_sub",
            photo_url="https://via.placeholder.com/150",
            photo_size=100,
            need_name=False,
            need_email=False,
            need_phone_number=False
        )

    async def start_change_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.change_ai)

        await state.set_state(ChangeAiStates.change_ai)

    async def change_ai(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        is_changed = self.change_ai_usecase.execute(id, message.text)

        if is_changed:
            await message.answer(texts.change_ai_successful)
        else:
            await message.answer(texts.change_ai_error)

        await state.clear()

    async def recreate_ai(self, message: types.Message, state: FSMContext):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.get_number_ai)

        await state.set_state(CreatingAiStates.number_bot)

    async def set_number_ai(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.get_name_ai)

        await state.update_data(number_ai=message.text)
        await state.set_state(CreatingAiStates.prompt)

    async def set_name_ai(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.get_prompt_ai)

        await state.update_data(number_ai=message.text)
        await state.set_state(CreatingAiStates.prompt)

    async def set_prompt_ai(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        await message.answer(texts.input_language_ai)

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
            await message.answer(texts.ai_recreated)
        else:
            await message.answer(texts.ai_recreated_error)

        await state.clear()

    async def buy_ai_place(self, message: types.Message):
        pass

    async def change_language(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        inline_kb = [
            [types.InlineKeyboardButton(text=texts.language_button_ru, callback_data="")],
            [types.InlineKeyboardButton(text="", callback_data="")],
            [types.InlineKeyboardButton(text="", callback_data="")],
            [types.InlineKeyboardButton(text="", callback_data="")]
        ]

        id = message.from_user.id

    def input_english(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        self.access_input_language(id, Languages.eng)  #TODO: Узнать, октуда берутся Languages и закинуть их # TODO: Зарегистрировать метод

    def input_russian(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        self.access_input_language(id, Languages.rus)

    def input_china(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        self.access_input_language(id, Languages.chi)

    def input_german(self, message: types.Message, state: FSMContext): # TODO: Зарегистрировать метод
        id = message.from_user.id
        self.access_input_language(id, Languages.ger)


    def access_input_language(self, id: int, language: Languages):
        self.change_user_language_usecase.execute(id, language)


