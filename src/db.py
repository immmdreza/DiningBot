from pymongo import MongoClient


class DB:

    def __init__(self, host: str = "127.0.0.1", port: int = 27017) -> None:
        self.db = MongoClient(host, int(port)).diningbotdb

    def add_user(self, user):
        self.db.users.insert_one(user)

    def add_food(self, food):
        self.db.foods.insert_one(food)

    def get_all_foods(self, name: bool = False, id: bool = False):
        return self.db.foods.find(
            projection={'_id': False, 'name': name, 'id': id}
            ).sort([('food_id', 1)])

    def set_user_food_priorities(self, user_id: str, priorities: list):
        self.db.users.update_one(
            {'user_id': user_id},
            {'$set': {'priorities': priorities}}
        )
