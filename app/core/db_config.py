from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.config import Settings


settings = Settings()

class DB:
    def __init__(self):
        self.engine = create_async_engine(settings.PG_URI,echo=True)
        self.SessionLocal = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    async def get_db(self):
        async with self.SessionLocal() as session:
            yield session
    




    