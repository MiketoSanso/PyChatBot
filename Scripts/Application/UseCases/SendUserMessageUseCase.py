import asyncio

from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests
from Scripts.Infrastructure.TechData.Constants import Constants


class SendUserMessageUseCase:

    def __init__(self, user_requests: UserRequests,
                 constants: Constants):
        self.constants = constants
        self.user_requests = user_requests

    async def execute(self, id: int, message: str) -> str:
        length_message = len(message)

        if length_message > self.constants.MAX_COUNT_CHARS_MESSAGE:
            return "Ошибка! Пользователь гей!"

        user_data = self.user_requests.get_user_data(id)

        ai_data = user_data.ai_data

        if len(ai_data.messages) > self.constants.MAX_COUNT_MESSAGES:
            ai_data.messages.popleft()

        ai_data.messages.append(message)

        message_to_ai = (f"{ai_data.prompt}\nЯзык: {ai_data.language}\n{message}\n\n\n"
                         f"ОТВЕТ ПИШИ НЕ ДЛИННЕЕ {self.constants.MAX_COUNT_CHARS_ANSWER}")

        return await self.sleep_and_give_answer(message_to_ai) #Переделать на OLLAMA (ии)

    async def sleep_and_give_answer(self, message: str) -> str:
        print(message)
        await asyncio.sleep(10)

        answer = "Это - предполагаемый ответ от бота.\nИгнорируйте структуру."
        length_answer = len(answer)

        if length_answer > self.constants.MAX_COUNT_CHARS_MESSAGE:
            print(message + f"ОТВЕТ ПИШИ НЕ ДЛИННЕЕ {self.constants.MAX_COUNT_CHARS_ANSWER}, НИ В КОЕМ СЛУЧАЕ НЕ ДЛИННЕЕ!!!!")
            await asyncio.sleep(10)

        answer = "Это - предполагаемый ответ от бота.\nИгнорируйте структуру."

        return answer

    #TODO: Добавить УБАВЛЕНИЕ токенов, а также ответ если AIMODEL не заполнена
