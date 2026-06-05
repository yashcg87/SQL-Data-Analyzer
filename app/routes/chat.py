from fastapi import APIRouter, Body
from app.core.llm_config import Model
from typing import Annotated
from langchain.messages import HumanMessage
from app.agents.workflow import graph
from app.jobs.kb_update import sync_postgres_to_mongo_job

router = APIRouter()
model = Model()

#routes
@router.get('/health_check')
def health_check():
    return "hello world"

@router.get('/model_check')
def model_check():
    response = model.get_model().invoke("answer in one word").content
    return response

@router.post("/chat")
def chat(query: Annotated[str, Body(embed=True)]):
    graph_input = {
        "messages": [HumanMessage(content = query)]
    }
    graph.invoke(graph_input)
    return query

@router.get("/sync-now")
def force_sync():
    """
    Manually trigger schema sync pipeline
    """
    sync_postgres_to_mongo_job()
    return {"message": "Manual schema sync completed"}
    