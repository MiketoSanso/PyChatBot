from typing import Optional

from Scripts.Domain.Data.UserData import UserData
from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests


class GetUserDataUseCase:
    def __init__(self, user_requests: UserRequests):
        self.user_requests = user_requests

    def execute(self, id: int) -> Optional[UserData]:
        return self.user_requests.get_user_data(id)

