from Scripts.Domain.Data.UserData import UserData
from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests


class AddUserUseCase:
    def __init__(self, user_requests: UserRequests):
        self.user_requests = user_requests

    async def execute(self, id: int, data: UserData) -> bool:
        is_authorized = self.user_requests.add_user(id, data)
        return is_authorized
