import json
from typing import Optional

from Scripts.Domain.Data.UserData import UserData
from Scripts.Infrastructure.Database import Database


class UserRequests:
    def __init__(self, db: Database):
        self.db = db

    def add_user(self, id: int, data: UserData) -> bool:
        user_data = self.get_user_data(id)

        if user_data is None:
            save_data = data.to_dict()
            user_data_json = json.dumps(save_data)


            self.db.cursor.execute("INSERT INTO users "
                                   "(id, user_data) VALUES "
                                   "(%s, %s)",
                                   (id, user_data_json))

            self.db.conn.commit()
        else:
            return False

        return True

    def update_user_data(self, id: int, new_data: UserData):
        save_data = new_data.to_dict()
        user_data_json = json.dumps(save_data)
        self.db.cursor.execute("UPDATE users SET user_data=%s WHERE id = %s", (user_data_json, id))
        self.db.conn.commit()

    def get_user_data(self, id: int) -> Optional[UserData]:
        self.db.cursor.execute("SELECT user_data FROM users WHERE id = %s", (id,))
        result = self.db.cursor.fetchone()

        if not result:
            return None

        return UserData.from_dict(result[0])
