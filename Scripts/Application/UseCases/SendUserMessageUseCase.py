import asyncio

from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests
from Scripts.Infrastructure.TechData.Constants import Constants


class SendUserMessageUseCase:

    def __init__(self, user_requests: UserRequests,
                 constants: Constants):
        self.constants = constants
        self.user_requests = user_requests

    async def execute(self, id: int, message: str) -> str:
        data = self.user_requests.get_user_data(id)
        length_message = len(message)

        loosed_tokens = length_message / self.constants.COUNT_CHARS_BY_TOKEN
        count_tokens = data.tokens
        ai_model = data.ai_data

        if count_tokens < loosed_tokens:
            return ("Сообщение слишком длинное! Сократите его и повторите попытку.\n"
                    f"Требуется: {count_tokens} / Осталось: {loosed_tokens}")

        if ai_model.prompt == "":
            return ("Промпт пустой! Пересоздайте AI.\n")

        if length_message > self.constants.MAX_COUNT_CHARS_MESSAGE:
            return ("Сообщение слишком длинное! Сократите его и повторите попытку.\n"
                    f"Введено: {length_message} / Макс.: {self.constants.MAX_COUNT_CHARS_MESSAGE}")

        data.tokens -= loosed_tokens

        self.user_requests.update_user_data(id, data)

        if len(ai_model.messages) > self.constants.MAX_COUNT_MESSAGES:
            ai_model.messages.popleft()

        ai_model.messages.append(message)

        message_to_ai = (f"{ai_model.prompt}\nЯзык: {ai_model.language}\n{message}\n\n\n"
                         f"ОТВЕТ ПИШИ НЕ ДЛИННЕЕ {self.constants.MAX_COUNT_CHARS_ANSWER}")

        return await self.sleep_and_give_answer(message_to_ai) #Переделать на OLLAMA (ии)

    async def sleep_and_give_answer(self, message: str) -> str:
        await asyncio.sleep(10)

        answer = ("Это - предполагаемый ответ от бота.\n"
                  "Игнорируйте структуру.")
        length_answer = len(answer)

        if length_answer > self.constants.MAX_COUNT_CHARS_MESSAGE:
            print(message + f"ОТВЕТ ПИШИ НЕ ДЛИННЕЕ {self.constants.MAX_COUNT_CHARS_ANSWER}, НИ В КОЕМ СЛУЧАЕ НЕ ДЛИННЕЕ!!!!")
            await asyncio.sleep(10)

        answer = "Это - предполагаемый ответ от бота.\nИгнорируйте структуру."

        return answer