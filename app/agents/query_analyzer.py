from state import State
from app.agents.prompts import QUERY_ANALYZER_PROMPT
from app.core.llm_config import Model
from langchain.messages import SystemMessage, HumanMessage

llm = Model().get_model()

class QueryAnalyzer:
    def run(state : State):
        messages = [SystemMessage(QUERY_ANALYZER_PROMPT), HumanMessage(state["messages"][-1].content)]
        result = llm.invoke(messages)
        return {'next_node' : result.content.strip(), 'curr_node': 'query_analyzer'}