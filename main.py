from fastapi import FastAPI
from pydantic import BaseModel
from agent.agentic_workflow import GraphBuilder
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage
import os
import traceback


app = FastAPI()

# ---------------------------
# Build graph ONCE at startup
# ---------------------------
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "groq")

try:
    graph_builder = GraphBuilder(model_provider=MODEL_PROVIDER)
    react_app = graph_builder()
    print(f"✅ LangGraph initialized with provider: {MODEL_PROVIDER}")
except Exception as e:
    print("❌ Failed to initialize LangGraph")
    traceback.print_exc()
    react_app = None


class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    if react_app is None:
        return JSONResponse(
            status_code=500,
            content={"error": "Travel agent is not initialized."},
        )

    try:
        print("📥 User query:", query.query)

        messages = {
            "messages": [HumanMessage(content=query.query)]
        }

        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)

        return {"answer": final_output}

    except Exception as e:
        print("❌ Error during query execution")
        traceback.print_exc()

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error while processing your request."
            },
        )
