import traceback

from app.agents.prompts import executor_analysis
from state import State
from sqlalchemy import text
from app.core.db_config import DB
from app.core.llm_config import Model
from langchain.messages import HumanMessage

llm = Model().get_model()
db_manager = DB()

class Executor:
    async def run(state : State):
        try:
            query = state["sql_query"]
            async with db_manager.SessionLocal() as session:
                    result = await session.execute(text(query))
                    rows = [dict(row._mapping) for row in result.fetchall()]
                    state["query_result"] = rows
            
            return {
            "query_result": rows,
            "route_data": "explainer",
            "validation": {"pass": "YES", "feedback": ""}
            }
        
        except Exception as e:
            raw_error_trace = traceback.format_exc()
            llm_feedback = llm.invoke([HumanMessage(content=executor_analysis(raw_error_trace))]).content
            state["validation"] = {"pass":"NO", "feedback": llm_feedback}
            state["loop_count"] = 1
            return state