from state import State


class Fallback:
    def run(state : State):
        state["messages"] = "Maximum iteration is reached for the given query please try again"
        return state