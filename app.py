from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class QueryRequest(BaseModel):
    query:str

@app.get("/query"):
#main
async def query_travel_agent(query:QueryRequest):
    