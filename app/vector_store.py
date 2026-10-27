import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings

chroma_client = chromadb.PersistentClient(
    path=settings.CHROMA_PERSIST_DIR,
    settings=ChromaSettings(allow_reset=True, anonymized_telemetry=False)
)

case_index = chroma_client.get_or_create_collection(
    name="missing_cases_collection",
    metadata={"description": "Vector store for missing cases and RAG retrieval"}
)

def add_case_vector(case_id: str, document_text: str, metadata: dict):
    case_index.upsert(
        ids=[case_id],
        documents=[document_text],
        metadatas=[metadata]
    )

def query_case_vectors(query_text: str, n_results: int = 5):
    return case_index.query(
        query_texts=[query_text],
        n_results=n_results
    )