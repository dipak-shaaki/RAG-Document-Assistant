from fastapi import FastAPI
from app.api import ingest

app = FastAPI(title="RAG Backend")

app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])


@app.get("/")
def root():
    return {"message": "API is running"}