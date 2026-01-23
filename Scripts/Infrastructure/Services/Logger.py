import logging
from aiogram.types import SuccessfulPayment


class Logger:
    def __init__(self):
        pass

    def access_payment(self, success_pay: SuccessfulPayment):
        logging.info(f"Успешный платеж! ID: {success_pay.telegram_payment_charge_id}")
        logging.info(f"Payload: {success_pay.invoice_payload}")
        logging.info(f"Сумма: {success_pay.total_amount / 100} {success_pay.currency}")