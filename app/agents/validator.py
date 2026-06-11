from state import State
from app.core.llm_config import Model
import json
from app.agents.prompts import validator
llm  = Model().get_model()

class Validator:
    def run(state : State):
        try:
            result = llm.invoke(validator(str(state['messages'][-1]), state["sql_query"]))
            state['validation'] = json.loads(result.content)
            if state["validation"].get("pass") == "YES":
                return state
            else:
                state["loop_count"] = 1
            return state
        except Exception as e:
            print("error occured in validator ",e)