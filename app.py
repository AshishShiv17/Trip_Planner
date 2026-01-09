from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class QueryRequest(BaseModel):
    query:str
#aw
@app.get("/query"):

async def query_travel_agent(query:QueryRequest):
    