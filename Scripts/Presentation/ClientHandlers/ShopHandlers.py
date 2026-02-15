from aiogram import Dispatcher, F, types
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery

from Scripts.Application.UseCases.AddAiPlaceUseCase import AddAiPlaceUseCase
from Scripts.Application.UseCases.AddTokensUseCase import AddTokensUseCase
from Scripts.Application.UseCases.ChangeAiUseCase import ChangeAiUseCase
from Scripts.Application.UseCases.ChangeUserLanguageUseCase import ChangeUserLanguageUseCase
from Scripts.Application.UseCases.GetUserDataUseCase import GetUserDataUseCase
from Scripts.Application.UseCases.LoggingAccessPaymentUseCase import LoggingAccessPaymentUseCase
from Scripts.Application.UseCases.RecreateAiUseCase import RecreateAiUseCase
from Scripts.Application.UseCases.ReturnTextsUseCase import ReturnTextsUseCase
from Scripts.Infrastructure.TechData.Constants import Constants


class ShopHandlers:

    def __init__(self,
                 change_ai_usecase: ChangeAiUseCase,
                 change_user_language_usecase: ChangeUserLanguageUseCase,
                 recreate_ai_usecase: RecreateAiUseCase,
                 logging_access_payment_usecase: LoggingAccessPaymentUseCase,
                 return_texts_usecase: ReturnTextsUseCase,
                 get_user_data_usecase: GetUserDataUseCase,
                 add_tockens_usecase: AddTokensUseCase,
                 add_ai_place_usecase: AddAiPlaceUseCase,
                 constants: Constants):
        self.constants = constants
        self.get_user_data_usecase = get_user_data_usecase
        self.change_ai_usecase = change_ai_usecase
        self.change_user_language_usecase = change_user_language_usecase
        self.recreate_ai_usecase = recreate_ai_usecase
        self.logging_access_payment_usecase = logging_access_payment_usecase
        self.return_texts_usecase = return_texts_usecase
        self.add_tockens_usecase = add_tockens_usecase
        self.add_ai_place_usecase = add_ai_place_usecase

    def register_handlers(self, dp: Dispatcher):
        dp.message.register(self.buy_tokens, Command("buy_tokens"))
        dp.message.register(self.buy_ai_place, Command("buy_ai_place"))

        dp.callback_query.register(self.process_buy_tokens_callback, F.data.startswith("buy_"))

        dp.pre_checkout_query.register(self.process_pre_checkout)
        dp.message.register(self.process_successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)

    async def buy_tokens(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(text="1000 токенов - 150₽", callback_data="buy_1000")],
            [types.InlineKeyboardButton(text="3000 токенов - 430₽", callback_data="buy_3000")],
            [types.InlineKeyboardButton(text="5000 токенов - 650₽", callback_data="buy_5000")],
            [types.InlineKeyboardButton(text="10000 токенов - 1250₽", callback_data="buy_10000")],
            [types.InlineKeyboardButton(text="50000 токенов - 6000₽", callback_data="buy_50000")],
            [types.InlineKeyboardButton(text="200000 токенов - 25000₽", callback_data="buy_200000")],

        ])

        await message.answer("Выберите количество токенов:", reply_markup=keyboard)

    async def process_buy_tokens_callback(self, callback: types.CallbackQuery):
        texts = self.return_texts_usecase.execute(callback.from_user.id)

        amount_map = {
            "buy_1000": (1000, 15000),
            "buy_3000": (3000, 43000),
            "buy_5000": (5000, 65000),
            "buy_10000": (10000, 125000),
            "buy_50000": (50000, 600000),
            "buy_200000": (200000, 250000),

        }

        tokens, price = amount_map[callback.data]

        prices = [LabeledPrice(label=f"{tokens} {texts.word_tokens}", amount=price)]

        await callback.message.answer_invoice(
            title=texts.transaction_tokens_title,
            description= texts.description_tokens + tokens,
            payload=f"tokens_{tokens}",
            provider_token=self.constants.PAYMENTS,
            currency="RUB",
            prices=prices,
            start_parameter="buy_tokens",
            photo_url="https://via.placeholder.com/150",
            photo_size=100
        )

    async def process_pre_checkout(self, pre_checkout_query: PreCheckoutQuery):
        await pre_checkout_query.bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout_query.id,
            ok=True,
            error_message=None
        )

    async def process_successful_payment(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        payment = message.successful_payment

        await self.logging_access_payment_usecase.execute(payment)

        if payment.invoice_payload.startswith("tokens_"):
            tokens_amount = int(payment.invoice_payload.replace("tokens_", ""))
            self.add_tockens_usecase.execute(id, tokens_amount)
        elif payment.invoice_payload.startswith("ai_"):
            self.add_ai_place_usecase.execute(id)
        else:
            print("ERROR! ALERT! ProcessSuccessfulPayment don't have correct invoice payment")







    async def buy_ai_place(self, callback: types.CallbackQuery):
        texts = self.return_texts_usecase.execute(callback.from_user.id)

        count_places, price = 1, 35000

        prices = [LabeledPrice(label=f"{count_places} {texts.word_cell}", amount=price)]

        await callback.message.answer_invoice(
            title=texts.transaction_ai_cell_title,
            description=texts.description_ai_cell,
            payload=f"ai_{count_places}",
            provider_token=self.constants.PAYMENTS,
            currency="RUB",
            prices=prices,
            start_parameter="buy_ai_place",
            photo_url="https://via.placeholder.com/150",
            photo_size=100
        )