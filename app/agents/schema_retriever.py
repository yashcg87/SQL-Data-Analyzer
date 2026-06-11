from state import State
from app.core.db_config import DB

db = DB()
store = db.get_vector_store()
class SchemaRetriever:
    def run(state : State):
        data = store.similarity_search(query=str(state["messages"][-1]),pre_filter={
        "table_name": {
            "$eq": state["route_data"].get("table_name")
        }
        })
        state["table_data"] = data[0]
        return state