from Scripts.Domain.Data.Languages import Languages
from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests


class ChangeUserLanguageUseCase:

    def __init__(self, user_requests: UserRequests):
        self.user_requests = user_requests

    def execute(self, id: int, language: Languages) -> bool:
        data = self.user_requests.get_user_data(id)
        data.language = language
        self.user_requests.update_user_data(id, data)
        return True