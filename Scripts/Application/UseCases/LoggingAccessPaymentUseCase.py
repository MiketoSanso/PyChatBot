from aiogram.types import SuccessfulPayment
from Scripts.Infrastructure.Services.Logger import Logger


class LoggingAccessPaymentUseCase:
    def __init__(self, logger: Logger):
        self.logger = logger

    async def execute(self, success_payment: SuccessfulPayment) -> bool:
        self.logger.access_payment(success_payment)
        return True
