from langchain_mongodb import MongoDBAtlasVectorSearch
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import Settings
from app.core.llm_config import Model
from app.jobs.kb_update import collection
from sqlalchemy import text, inspect

settings = Settings()
model = Model()
class DB:
    def __init__(self):
        self.engine = create_async_engine(settings.PG_URI,echo=True)
        self.SessionLocal = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.collection = collection
        self.index = settings.INDEX
        self.embedding_model = model.get_embedding_model()

    async def get_db(self):
        async with self.SessionLocal() as session:
            yield session
    
    
    def get_vector_store(self):
        vector_store = MongoDBAtlasVectorSearch(
        collection=self.collection,
        embedding=self.embedding_model,
        index_name=self.index,
        embedding_key="column_embedding",
        text_key="table_name"
        )
        return vector_store
    
    async def get_tables(self) -> list[str]:
        """
        Asynchronously inspects the PostgreSQL database and returns a list 
        of all table names present in the public schema.
        """
        async with self.SessionLocal() as session:
            connection = await session.connection()
            
            tables = await connection.run_sync(
                lambda conn: inspect(conn).get_table_names(schema="SQL_ANALYZER")
            )
            return tables
        




    