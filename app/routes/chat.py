from fastapi import APIRouter, Body
from pydantic import BaseModel
from app.core.llm_config import Model
from typing import Annotated
from langchain_core.messages import HumanMessage
from app.agents.workflow import graph
from app.jobs.kb_update import sync_postgres_to_mongo_job

router = APIRouter()
model = Model()


class ChatRequest(BaseModel):
    query: str
    thread_id: str  

#routes
@router.get('/health_check')
def health_check():
    return "hello world"

@router.get('/model_check')
async def model_check():
    response = model.get_model().invoke("answer in one word").content
    return response

@router.post("/chat")
async def chat(request: ChatRequest):
    graph_input = {
        "messages": [HumanMessage(content=request.query)], "loop_count" : 0
    }
    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }
    
    result = await graph.ainvoke(graph_input, config=config)
    response = result["messages"][-1].content
    return response

@router.get("/sync-now")
def force_sync():
    """
    Manually trigger schema sync pipeline
    """
    sync_postgres_to_mongo_job()
    return {"message": "Manual schema sync completed"}
    