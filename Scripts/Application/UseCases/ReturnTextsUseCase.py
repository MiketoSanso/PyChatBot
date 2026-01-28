from Scripts.Domain.Data.Languages import Languages
from Scripts.Domain.Interfaces.Texts import Texts
from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests
from Scripts.Infrastructure.TextsData.RussianTexts import RussianTexts


class ReturnTextsUseCase:

    def __init__(self, user_requests: UserRequests):
        self.user_requests = user_requests

    def execute(self, id: int) -> type[Texts] | None:
        data = self.user_requests.get_user_data(id)
        language = data.language

        if language == Languages.eng:
            return RussianTexts()
        elif language == Languages.rus:
            return RussianTexts()
        elif language == Languages.chi:
            return RussianTexts()
        elif language == Languages.de:
            return RussianTexts()

        return None
