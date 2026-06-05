from langgraph.graph import StateGraph, MessagesState, START, END
from app.agents import AuditLogger, Executor, Explainer, GeneralQuery, QueryAnalyzer,  SchemaRetriever, SqlGenerator, Validator
from state import State


graph = StateGraph(MessagesState)
graph.add_node("audit_logger", AuditLogger.run)
graph.add_node("executor", Executor.run)
graph.add_node("explainer", Explainer.run)
graph.add_node("query_analyzer", QueryAnalyzer.run)
graph.add_node("schema_retriever", SchemaRetriever.run)
graph.add_node("sql_generator", SqlGenerator.run)
graph.add_node("validator", Validator.run)
graph.add_node("general_query", GeneralQuery.run)
    


graph.add_edge(START, "query_analyzer")
graph.add_conditional_edges("query_analyzer", lambda state : state["next_node"])
graph.add_edge("schema_retriever", "sql_generator")
graph.add_edge("sql_generator", "validator")
graph.add_edge("validator", "executor")
graph.add_edge("executor", "explainer")
graph.add_edge("explainer", END)
graph.add_edge("general_query", END)




graph.add_edge("general_query", END)

graph = graph.compile()
