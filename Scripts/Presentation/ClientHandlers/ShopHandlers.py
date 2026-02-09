from aiogram import Dispatcher, F, types
from aiogram.enums import ContentType, ParseMode
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery

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
                 constants: Constants):
        self.constants = constants
        self.get_user_data_usecase = get_user_data_usecase
        self.change_ai_usecase = change_ai_usecase
        self.change_user_language_usecase = change_user_language_usecase
        self.recreate_ai_usecase = recreate_ai_usecase
        self.logging_access_payment_usecase = logging_access_payment_usecase
        self.return_texts_usecase = return_texts_usecase

    def register_handlers(self, dp: Dispatcher):
        dp.message.register(self.buy_tokens, Command("buy_tokens"))
        dp.message.register(self.buy_ai_place, Command("buy_ai_place"))

        dp.pre_checkout_query.register(self.process_pre_checkout)
        dp.message.register(self.process_successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)

    async def process_successful_payment(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        payment = message.successful_payment

        await self.logging_access_payment_usecase.execute(payment)

        if message.successful_payment == "month_sub":
            await message.answer(texts.successful_payment + {payment.order_info.email}, parse_mode=ParseMode.HTML)

    async def process_pre_checkout(self, pre_checkout_query: PreCheckoutQuery):
        await self.bot.answer_pre_checkout_query(
            pre_checkout_query_id=pre_checkout_query.id,
            ok=True,
            error_message=None
        )

    async def buy_tokens(self, message: types.Message):
        id = message.from_user.id
        texts = self.return_texts_usecase.execute(id)

        prices = [
            LabeledPrice(label=f"1000 {texts.word_tokens}", amount=15_000),
            LabeledPrice(label=f"3000 {texts.word_tokens}", amount=43_000),
            LabeledPrice(label=f"5000 {texts.word_tokens}", amount=65_000),
            LabeledPrice(label=f"10000 {texts.word_tokens}", amount=125_000),
            LabeledPrice(label=f"50000 {texts.word_tokens}", amount=600_000),
            LabeledPrice(label=f"200000 {texts.word_tokens}", amount=2500_000),
        ]


        await self.bot.send_invoice(
            chat_id=message.chat.id,
            title=texts.transaction_tokens_title,
            description=texts.transaction_tokens_description,
            payload="Tockens",
            provider_token=self.constants.TOKEN_PAYMENTS,
            currency="RUB",
            prices=prices,
            start_parameter="premium_sub",
            photo_url="https://via.placeholder.com/150",
            photo_size=100,
            need_name=False,
            need_email=False,
            need_phone_number=False
        )

    async def buy_ai_place(self, message: types.Message):
        pass