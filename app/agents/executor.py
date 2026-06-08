from state import State
from sqlalchemy import text
from app.core.db_config import DB

db_manager = DB()

class Executor:
    async def run(state : State):
        query = state["sql_query"]
        async with db_manager.SessionLocal() as session:
                result = await session.execute(text(query))
                rows = [dict(row._mapping) for row in result.fetchall()]
                state["query_result"] = rows
        
        print("result of the executor is ", rows)
        return state