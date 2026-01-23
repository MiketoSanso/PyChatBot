from attr import dataclass

from Scripts.Domain.Interfaces.Texts import Texts


@dataclass(frozen=True)
class RussianTexts(Texts):
    start = "Добро пожаловать в ChatAI! Бла-бла-бла."
    help = ("Существующие команды:\n"
            "/start"
            "/help"
            "/account"
            "/change_language"
            "/change_ai"
            "/recreate_ai"
            "/buy_ai_place"
            "/buy_tokens")

    get_number_ai = "Введите номер ai, настройки которого будем менять:"
    get_name_ai = "Введите имя ai:"
    get_prompt_ai = "Введите промпт (данные вашего чата, обстановку, и прочее):"
    input_language_ai = "Выберите язык бота:"
    ai_recreated = "AI создан успешно!"

    get_number_ai_error = "Ошибка! Вы ввели число либо меньше 1, либо больше количества доступных ботов!"
    get_prompt_ai_error = "Ошибка! В вашем промпте символов больше, чем X!" #TODO: Решить, сколько символов будет.
    ai_recreated_error = "Произошла ошибка при пересоздании бота!"

    input_language_user = "Выберите язык:"

    successful_payment = ("✅ Платеж прошел успешно!\n"
                "Ваша подписка активирована на 30 дней.\n"
                f"Чек отправлен на")

    word_tokens = "Токенов"

    change_ai = "Введите номер вашего AI, которого хотите активировать:"
    change_ai_successful = "AI изменён!"
    change_ai_error = ("Произошла ошибка при изменении AI!\n"
                       "Возможные причины:\n\n"
                       "1) Введённое число меньше 1.\n"
                       "2) Введённое число больше количества доступных слотов.\n\n"
                       "Попробуйте снова!")

    transaction_tokens_title = "Токены"
    transaction_tokens_description = "Покупка токенов для работы AI",

    language_button_ru = "Русский"
    language_button_chi = "Китайский"
    language_button_eng = "Английский"
    language_button_ger = "Немецкий"
