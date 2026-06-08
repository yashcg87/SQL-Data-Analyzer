from app.agents.prompts import sql_generator
from state import State
from app.core.llm_config import Model


model = Model()
llm = model.get_model()
class SqlGenerator:
    def run(state : State):
        result = llm.invoke(sql_generator(str(state["messages"][-1]), state["table_data"]))
        state["sql_query"] = result.content
        return state