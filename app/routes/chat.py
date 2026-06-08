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
async def model_check():
    response = model.get_model().invoke("answer in one word").content
    return response

@router.post("/chat")
async def chat(query: Annotated[str, Body(embed=True)]):
    graph_input = {
        "messages": query
    }
    result = await graph.ainvoke(graph_input)
    response = result["messages"][-1].content
    print("graph result is ", result)
    return response

@router.get("/sync-now")
def force_sync():
    """
    Manually trigger schema sync pipeline
    """
    sync_postgres_to_mongo_job()
    return {"message": "Manual schema sync completed"}
    