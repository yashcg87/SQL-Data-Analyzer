from state import State
from app.core.db_config import DB

db = DB()
store = db.get_vector_store()
class SchemaRetriever:
    def run(state : State):
        print("this is schema retriver")
        print("this is the table name ", state["route_data"].get("table_name"))
        print("message is ", str(state["messages"][-1]))
        data = store.similarity_search(query=str(state["messages"][-1]),pre_filter={
        "table_name": {
            "$eq": state["route_data"].get("table_name")
        }
        })
        state["table_data"] = data[0]
        print("data returned from collection is", data[0])
        print("type of this data", type(data[0]))
        return state