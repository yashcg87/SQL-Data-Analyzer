from state import State
from app.core.llm_config import Model
from langchain.messages import HumanMessage

llm = Model().get_model()

class GeneralQuery:
    def run(state : State):
        response = llm.invoke(state["messages"]).content
        state["messages"].append(HumanMessage(response))
        return state