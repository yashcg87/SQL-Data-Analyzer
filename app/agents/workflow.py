from langgraph.graph import StateGraph, MessagesState, START, END
from app.agents import AuditLogger, Executor, Explainer, GeneralQuery, QueryAnalyzer,  SchemaRetriever, SqlGenerator, Validator, Fallback
from state import State
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
graph = StateGraph(MessagesState)

#nodes
graph.add_node("audit_logger", AuditLogger.run)
graph.add_node("executor", Executor.run)
graph.add_node("explainer", Explainer.run)
graph.add_node("query_analyzer", QueryAnalyzer.run)
graph.add_node("schema_retriever", SchemaRetriever.run)
graph.add_node("sql_generator", SqlGenerator.run)
graph.add_node("validator", Validator.run)
graph.add_node("general_query", GeneralQuery.run)
graph.add_node("max_reached", Fallback.run)
    
#conditional functions    
def route_executor(state: State):
    if state.get("loop_count", 0) >= 3:
        return "MAX_REACHED"
    
    validation_dict = state.get("validation", {})
    return validation_dict.get("pass", "NO") 


def route_validator(state: State):
    if state.get("loop_count", 0) >= 3:
        return "MAX_REACHED"
        
    validation_dict = state.get("validation", {})
    return validation_dict.get("pass", "NO") 


#edges
graph.add_edge(START, "query_analyzer")
graph.add_conditional_edges("query_analyzer", lambda state : state["route_data"].get("next_node"))
graph.add_edge("schema_retriever", "sql_generator")
graph.add_edge("sql_generator", "validator")
graph.add_conditional_edges("validator",route_validator, {
    "YES": "executor",
    "NO":"sql_generator",
    "MAX_REACHED" : "max_reached"
})
graph.add_conditional_edges("executor",route_executor, {
    "YES" : "explainer",
    "NO" : "sql_generator",
    "MAX_REACHED" : "max_reached"
})
graph.add_edge("explainer", END)
graph.add_edge("general_query", END)




graph.add_edge("general_query", END)

graph = graph.compile(checkpointer = memory)
