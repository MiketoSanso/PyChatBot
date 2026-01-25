import json

from Scripts.Domain.Data.UserData import UserData
from Scripts.Infrastructure.Database import Database


class UserRequests:
    def __init__(self, db: Database):
        self.db = db

    def add_user(self, id: int, data: UserData) -> bool:
        user_data = self.get_user_data(id)

        if user_data is None:
            user_data_json = json.dumps({"language": data.language})

            self.db.cursor.execute("INSERT INTO users "
                                   "(id, user_data) VALUES "
                                   "(%s, %s)",
                                   (id, user_data_json))

            self.db.conn.commit()
        else:
            return False

        return True

    def update_user_data(self, id: int, new_data: UserData):
        self.db.cursor.execute("UPDATE users SET user_data=%s WHERE id = %s", (new_data, id))

    def get_user_data(self, id: int) -> type[UserData]:
        return self.db.cursor.execute("SELECT user_data FROM users WHERE id = %s", (id,))