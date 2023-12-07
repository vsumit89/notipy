from app.repositories.database import DatabaseService
from utils.config import get_settings
from utils.logger import CustomLogger
from app.models.event_manager import Event

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie


class MongoDBService(DatabaseService):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        super().__init__()
        self.client = None
        self.logger = CustomLogger(__name__)
        self.__initialized = True

    async def connect(self):
        try:
            self.logger.info("Connecting to MongoDB")

            # getting settings from config
            settings = get_settings()

            # creating mongo url of format: mongodb://<username>:<password>@<host>:<port>
            mongo_url = f"mongodb://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"

            self.client = AsyncIOMotorClient(mongo_url)
            await init_beanie(self.client[settings.DB_NAME], document_models=[Event])

            self.logger.info("Connected to MongoDB")
        except Exception as e:
            self.logger.error(f"Error connecting to MongoDB: {e}")

    def disconnect(self):
        pass

    def migrate(self):
        pass
