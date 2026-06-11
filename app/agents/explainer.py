from app.agents.prompts import explainer
from state import State
from app.core.llm_config import Model
from langchain_core.messages import AIMessage
llm = Model().get_model()

class Explainer:
    def run(state : State):
        query = str(state["messages"][-1])
        query_result = state["query_result"]
        result = llm.invoke(explainer(query, query_result))
        ai_response_message = AIMessage(content=result.content.strip())
        state["messages"] = [ai_response_message]
        return state