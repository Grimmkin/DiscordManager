from collections import OrderedDict
from pathlib import Path

from BetterJSONStorage import BetterJSONStorage
from tinydb import Query, TinyDB, operations


class Database:
    def __init__(
        self, db_name, primary_key, schema: OrderedDict, checklist: list = []
    ) -> None:
        self.path = Path(f"db/{db_name}.db")
        self.primary_key = primary_key

        db = TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage)
        db.close()

    def get_count(self):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            count = len(db)

        return count

    def create(self, record: dict):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            db.insert(record)

    def delete(self, query):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.remove(query)

        return data

    def modify(self, query, update_info):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.update(operations.set(update_info[0], update_info[1]), query)

        return data

    def retrieve(self, query):
        with TinyDB(self.path, access_mode="r+", storage=BetterJSONStorage) as db:
            data = db.get(query)

        return data


if __name__ == "__main__":
    schema = {
        "name": "str",
        "nickname": "str",
        "specialisation": "str",
        "email": "email",
        "date_joined": "date",
        "cohort": "str",
        "teams": "list",
        "personal_projects": "list",
        "projects_done": "list",
        "projects_undertaking": "list",
    }
    primary_key = "nickname"
    database = Database("test_db", primary_key=primary_key, schema=schema)

    for i in range(5):
        database.create(
            record={
                "name": "john",
                "nickname": f"johnny_{i}",
                "email": "john@email.com",
                "date_joined": "01/2001",
            }
        )

    print(f"Created {database.get_count()} records.")

    User = Query()

    del_query = User.nickname == "johnny_4"
    print(f"Deleted: {database.delete(del_query)}")
    print(f"Count is now {database.get_count()}.")

    mod_query = User.nickname == "johnny_0"
    update_info = ("date_joined", "99/9999")
    print(f"Modified: {database.modify(mod_query, update_info)}")

    ret_query = User.nickname == "johnny_0"
    print(f"Retrieved: {database.retrieve(ret_query)}")