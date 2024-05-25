# crud.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from .config import QDRANT_URL

qdrant_client = QdrantClient(QDRANT_URL)


# Create collection if it doesn't exist
def create_qdrant_collection():
    try:
        qdrant_client.get_collection("vector_collection")
    except:
        qdrant_client.create_collection(
            collection_name="vector_collection",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # Adjust size according to vector size
        )
