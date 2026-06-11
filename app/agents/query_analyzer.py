import json
from state import State
from app.agents.prompts import query_analyzer_prompt
from app.core.llm_config import Model
# Fixed: LangChain messages reside under langchain_core
from langchain_core.messages import SystemMessage, HumanMessage 
from app.core.db_config import DB

llm = Model().get_model()
db = DB()

class QueryAnalyzer:
    @staticmethod
    async def run(state: State):
        tables = await db.get_tables()
        
        messages = [
            SystemMessage(content=query_analyzer_prompt(tables)), 
            HumanMessage(content=state["messages"][-1].content)
        ]
        
        response = await llm.ainvoke(messages)
        result = response.content
        
        route_data = json.loads(result)
        print("final state is ", state)
        
        return {'route_data': route_data, 'curr_node': 'query_analyzer'}
