from dataclasses import dataclass
from Scripts.Domain.Interfaces.Texts import Texts


@dataclass(frozen=True)
class RussianTexts(Texts):
    start = ("<b>ChatAI</b>\n\n"
             "Добро пожаловать в <b>ChatAI!</b>\n"
             "Только в нашем боте ты сможешь создать <b>любое количество личностей</b> для своих ботов, прописать "
             "<b>любое количество сюжетов</b> и вести общение, не теряя <b>старые диалоги</b>!\n\n"
             "<b>Погрузись в мир фантазии вместе с AI!</b>")
    help = ("<b>Существующие команды:</b>\n"
            "<b>/start</b> - Перезапустить бота.\n"
            "<b>/help</b> - Посмотреть все возможные команды.\n"
            "<b>/account</b> - Посмотреть аккаунт.\n"
            "<b>/change_language</b> - Сменить язык.\n"
            "<b>/change_ai</b> - Сменить активный AI.\n"
            "<b>/recreate_ai</b> - Пересоздать AI.\n"
            "<b>/buy_ai_place</b> - Купить новую ячейку под новый диалог с AI\n"
            "<b>/buy_tokens</b> - Купить токены для общения.\n")

    get_number_ai = "Введите <b>номер ai</b>, настройки которого будем менять:"
    get_name_ai = "Введите <b>имя</b> ai:"
    get_prompt_ai = "Введите <b>промпт</b> (<b>данные</b> вашего чата, <b>обстановку</b>, и <b>прочее</b>):"
    input_language_ai = "Выберите <b>язык</b> бота:"
    ai_recreated = "AI создан <b>успешно</b>!"

    get_number_ai_error = "Ошибка! Вы ввели число <b>либо меньше 1</b>, <b>либо больше количества доступных</b> ботов!"
    get_prompt_ai_error = "Ошибка! В вашем промпте <b>символов больше, чем X</b>!"
    ai_recreated_error = "Произошла <b>ошибка</b> при пересоздании бота!"

    input_language_user = "<b>Выберите язык:</b>"
    language_changed = "<b>Язык сменен на:</b>"


    successful_payment_tokens = ("✅ Платеж прошел успешно!\n"
                "Токены зачислены на счёт.\n"
                "Чек отправлен на")

    successful_payment_tokens_without_mail = ("✅ Платеж прошел успешно!\n"
                                 "Токены зачислены на счёт.")

    change_ai = "Введите номер вашего AI, которого хотите активировать:"
    change_ai_successful = "AI изменён!"
    change_ai_text_error = "Введён текст а не число! Попробуйте ещё раз!"
    change_ai_error = ("Произошла <b>ошибка</b> при изменении AI!\n\n"
                       "<b>Возможные причины:</b>\n"
                       "<b>1)</b> Введённое число <b>меньше 1</b>.\n"
                       "<b>2)</b> Введённое число <b>больше количества доступных слотов</b>.\n\n"
                       "Попробуйте <b>снова</b>!")

    transaction_tokens_title = "Токены"
    description_tokens = "Покупка токенов, количество:"

    description_ai_cell = f"Покупка новой ячейки AI"
    transaction_ai_cell_title = "Ячейка"
    transaction_tokens_description = "Покупка токенов для работы AI"

    language_bold_ru = "<b>Русский</b>"
    language_bold_chi = "<b>Китайский</b>"
    language_bold_eng = "<b>Английский</b>"
    language_bold_de = "<b>Немецкий</b>"

    language_ru = "Русский"
    language_chi = "Китайский"
    language_eng = "Английский"
    language_de = "Немецкий"

    word_tokens = "Токенов"
    word_cell = "Ячейка"

    bold_word_tokens = "<b>Токенов</b>"
    account_word = "<b>АККАУНТ</b>"
    count_bot_slots = "<b>Количество слотов для ботов</b>"
    language_word = "<b>Язык</b>"
    active_ai_text = "<b>Номер активного ИИ</b>"
    post_parameters_account = ""