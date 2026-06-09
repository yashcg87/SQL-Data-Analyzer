from state import State
from app.core.llm_config import Model
import json
from app.agents.prompts import validator
llm  = Model().get_model()

class Validator:
    def run(state : State):
        try:
            print("sql query is ", state.get("validation"))
            result = llm.invoke(validator(str(state['messages'][-1]), state["sql_query"]))
            state['validation'] = json.loads(result.content)
            print("validation is ", result.content)
            return state
        except Exception as e:
            print("error occured in validator ",e)