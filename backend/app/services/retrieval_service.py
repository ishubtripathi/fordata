from app.services.embedding_service import generate_embedding
from app.services.vector_service import search_similar_chunks


DEFAULT_DISTANCE_THRESHOLD = 0.85


def retrieve_relevant_chunks(
    query: str,
    top_k: int = 5,
    distance_threshold: float = DEFAULT_DISTANCE_THRESHOLD,
    document_ids: list[str] | None = None,
) -> dict:
    """
    Generate a query embedding and retrieve relevant
    document chunks from ChromaDB.

    If document_id is provided, retrieval is restricted
    to that document.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    if distance_threshold < 0:
        raise ValueError(
            "distance_threshold cannot be negative."
        )

    query_embedding = generate_embedding(query)

    results = search_similar_chunks(
        query_embedding=query_embedding,
        top_k=top_k,
        document_ids=document_ids,
    )

    return results


def format_retrieval_results(
    results: dict,
    distance_threshold: float = DEFAULT_DISTANCE_THRESHOLD,
) -> list[dict]:
    """
    Convert ChromaDB results into structured results
    and remove low-relevance chunks.
    """

    if not results:
        return []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    formatted_results = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances,
    ):
        if distance > distance_threshold:
            continue

        formatted_results.append(
            {
                "content": document,
                "source": {
                    "filename": metadata.get("filename"),
                    "file_type": metadata.get("file_type"),
                    "page_number": metadata.get("page_number"),
                    "row_number": metadata.get("row_number"),
                },
                "distance": distance,
            }
        )

    return formatted_results