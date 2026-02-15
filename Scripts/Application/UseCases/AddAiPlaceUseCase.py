from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests


class AddAiPlaceUseCase:
    def __init__(self, user_requests: UserRequests):
        self.user_requests = user_requests

    def execute(self, id: int) -> bool:
        data = self.user_requests.get_user_data(id)

        if data is None:
            return False

        data.count_ai += 1

        self.user_requests.update_user_data(id, data)

        return True

