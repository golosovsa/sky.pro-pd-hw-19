from app.dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_data):
        return self.dao.create(user_data)

    def update(self, user_data):
        self.dao.update(user_data)
        return self.dao

    def delete(self, uid):
        self.dao.delete(uid)
