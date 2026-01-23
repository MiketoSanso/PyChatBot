from abc import ABC


class Texts(ABC):
    def __init_subclass__(cls, **kwargs):
        attributes = [
            "start", "help", "get_number_ai", "get_prompt_ai", "input_language_ai",
            "ai_recreated", "get_number_ai_error", "get_prompt_ai_error",
            "ai_recreated_error", "successful_payment",
            "word_tokens", "transaction_tokens_title", "transaction_tokens_description",
            "get_name_ai", "change_ai", "change_ai_successful", "change_ai_error",
            "language_button_ru", "language_button_chi", "language_button_eng", "language_button_ger"
        ]
        for attribute in attributes:
            if not hasattr(cls, attribute):
                raise TypeError(
                    f"Класс {cls.__name__} должен определять атрибут '{attribute}'"
                )

