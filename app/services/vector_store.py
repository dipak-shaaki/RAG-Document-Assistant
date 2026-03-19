from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import uuid

# Initialize in-memory DB (no Docker needed)
client = QdrantClient(":memory:")

COLLECTION_NAME = "documents"


def create_collection(vector_size: int):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )


def store_embeddings(chunks: List[str], embeddings: List[List[float]]):
    points = []

    for chunk, embedding in zip(chunks, embeddings):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={"text": chunk}
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


def search(query_embedding: List[float], limit: int = 3):
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=limit
    )

    return [r.payload["text"] for r in results]