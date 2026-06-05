import os
import json
import hashlib
import logging
from typing import List
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field
from pymongo import MongoClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import Settings
from app.core.llm_config import Model

logging.basicConfig(level=logging.INFO)

model = Model()

client = MongoClient(Settings.MONGO_URI)
db = client["My_DB"]
collection = db["metadata_embeddings"]


async def fetch_pg_schema() -> dict:
    PG_DATABASE_URL = os.getenv("PG_URI")
    if not PG_DATABASE_URL:
        logging.error("PG_URI environment variable is missing.")
        return {}

    engine = create_async_engine(PG_DATABASE_URL)
    schema_map = {}

    def inspect_logic(sync_conn):
        inspector = inspect(sync_conn)
        tables = inspector.get_table_names(schema="SQL_ANALYZER")
        
        local_map = {}
        for table in tables:
            columns_data = inspector.get_columns(
                table_name=table,
                schema="SQL_ANALYZER"
            )
            local_map[table] = [col["name"] for col in columns_data]
        return local_map

    try:
        async with engine.connect() as conn:
            schema_map = await conn.run_sync(inspect_logic)
    except Exception as e:
        logging.error(f"Error fetching PG schema: {str(e)}")
    finally:
        await engine.dispose()

    return schema_map


def generate_hash(columns: List[str]) -> str:
    sorted_cols = sorted(columns)
    serialized = json.dumps(sorted_cols).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


async def sync_postgres_to_mongo_job():
    logging.info(f"[{datetime.now()}] Starting schema sync job...")

    try:
        pg_schema = await fetch_pg_schema()

        if not pg_schema:
            logging.warning("No tables found in the SQL_ANALYZER schema.")
            return

        embeddings_model = model.get_embedding_model()

        for table, columns in pg_schema.items():
            current_hash = generate_hash(columns)

            existing_doc = collection.find_one({"table_name": table})

            if existing_doc and existing_doc.get("schema_hash") == current_hash:
                logging.info(f"Table '{table}' unchanged. Skipping.")
                continue

            logging.info(f"Table '{table}' changed or new → generating embedding.")

            text = f"Table name: {table}. Columns: {', '.join(columns)}"

            embedding = embeddings_model.embed_query(text)

            if not embedding:
                logging.warning(f"Embedding generation failed for table '{table}'.")
                continue

            collection.update_one(
                {"table_name": table},
                {
                    "$set": {
                        "column_names": columns,
                        "schema_hash": current_hash,
                        "column_embedding": embedding,
                        "updated_at": datetime.utcnow(),
                    }
                },
                upsert=True
            )

            logging.info(f"Table '{table}' successfully synced to MongoDB.")

    except Exception as e:
        logging.error(f"Critical error in schema sync job: {str(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(sync_postgres_to_mongo_job, "interval", hours=1)
    scheduler.start()
    logging.info("AsyncIOScheduler running natively inside FastAPI's loop.")
    
    await sync_postgres_to_mongo_job()

    yield

    scheduler.shutdown()
    client.close()
    logging.info("Scheduler stopped and MongoDB connections severed cleanly.")