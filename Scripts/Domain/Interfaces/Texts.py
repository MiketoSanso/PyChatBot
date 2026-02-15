from abc import ABC


class Texts(ABC):
    def __init_subclass__(cls, **kwargs):
        attributes = [
            "start", "help", "get_number_ai", "get_prompt_ai", "input_language_ai",
            "ai_recreated", "get_number_ai_error", "get_prompt_ai_error",
            "ai_recreated_error", "successful_payment_tokens", "successful_payment_tokens_without_mail",
            "word_tokens", "word_cell", "transaction_tokens_title", "transaction_tokens_description",
            "get_name_ai", "change_ai", "change_ai_successful", "change_ai_error",
            "language_ru", "language_chi", "language_eng", "language_de",
            "language_bold_ru", "language_bold_eng", "language_bold_chi", "language_bold_de",
            "bold_word_tokens", "account_word", "count_bot_slots", "language_word", "active_ai_text",
            "post_parameters_account", "change_ai_text_error", "language_changed"
        ]
        for attribute in attributes:
            if not hasattr(cls, attribute):
                raise TypeError(
                    f"Класс {cls.__name__} должен определять атрибут '{attribute}'"
                )

