from database.mongodb.database import MongoDBService


def getDB(dbStore):
    match dbStore:
        case "mongodb":
            return MongoDBService()
        case _:
            raise Exception("Database not supported")
