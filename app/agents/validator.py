from state import State
from app.core.llm_config import Model
from app.agents.prompts import validator
llm  = Model().get_model()

class Validator:
    def run(state : State):
        result = llm.invoke(validator(str(state['messages'][-1]), state["sql_query"]))
        state['validation'] = result.content
        print(result.content)
        return state