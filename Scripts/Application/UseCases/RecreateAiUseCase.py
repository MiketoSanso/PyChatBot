from Scripts.Domain.Data.AiData import AiData
from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests


class RecreateAiUseCase:
    def __init__(self, user_requests: UserRequests):
        self.user_requests = user_requests

    def execute(self, id: int, ai_data: AiData) -> bool:
        data = self.user_requests.get_user_data(id)
        data.ai_data = ai_data
        self.user_requests.update_user_data(id, data)
        return True