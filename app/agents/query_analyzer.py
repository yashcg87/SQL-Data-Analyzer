from state import State
from app.agents.prompts import query_analyzer_prompt
from app.core.llm_config import Model
from langchain.messages import SystemMessage, HumanMessage
import json
llm = Model().get_model()

class QueryAnalyzer:
    def run(state : State):
        messages = [SystemMessage(query_analyzer_prompt(["employee", "users", "organizations"])), HumanMessage(state["messages"][-1].content)]
        result = llm.invoke(messages).content
        route_data = json.loads(result)
        print("this is json data", route_data)
        return {'route_data' : route_data, 'curr_node': 'query_analyzer'}