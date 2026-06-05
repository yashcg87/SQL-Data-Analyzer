from state import State



class AuditLogger:
    
    def run(state: State):
        print("Audit Log:")
        print("User Message:", state["messages"][-1]["content"])
        return {"next_node": "db_analyzer"}
    