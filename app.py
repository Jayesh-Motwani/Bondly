from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from love_guru import QueryPipeline
import logging

logging.basicConfig(level=logging.INFO)

pipeline = QueryPipeline()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/query")
def query_rag(req: QueryRequest):
    try:
        logging.info(f"Query: {req.query}")

        result = pipeline.retrieval_chain(req.query)

        logging.info(f"Response: {str(result)[:100]}")

        return {
            "answer": result,
            "sources": [],
            "category": None
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))