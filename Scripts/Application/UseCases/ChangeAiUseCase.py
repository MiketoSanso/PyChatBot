from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests


class ChangeAiUseCase():
    def __init__(self, user_requests: UserRequests):
        self.user_requests = user_requests

    def execute(self, id: int, number_ai: int) -> bool:
        data = self.user_requests.get_user_data(id)

        if data.count_ai >= number_ai and number_ai > 0:
            data.active_ai = number_ai
            self.user_requests.update_user_data(id, data)
            return True
        else:
            return False


