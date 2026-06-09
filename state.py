from typing import Annotated, TypedDict
from langgraph.graph import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    curr_node : str
    route_data: str
    table_data : dict
    sql_query : str
    validation : dict = None
    query_result : list
    
    