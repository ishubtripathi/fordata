import chromadb # type: ignore


from app.models.chunk import DocumentChunk


CHROMA_PATH = "./data/chroma"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="starq_documents",
    metadata={
        "hnsw:space": "cosine"
    },
)


def get_collection():
    """
    Return the StarQ vector collection.
    """

    return collection


def search_similar_chunks(
    query_embedding: list[float],
    top_k: int = 5,
    document_ids: list[str] | None = None,
) -> dict:
    """
    Search ChromaDB for the most similar document chunks.

    If document_id is provided, retrieval is restricted
    to that document.
    """

    if not query_embedding:
        raise ValueError("Query embedding cannot be empty.")

    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    query_kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": [
            "documents",
            "metadatas",
            "distances",
        ],
    }

    if document_ids:
        query_kwargs["where"] = {
            "document_id": {
                "$in": document_ids
            }
        }

    results = collection.query(**query_kwargs)

    return results


def store_embeddings(
    embedded_chunks: list[dict],
) -> int:
    """
    Store document chunks and their embeddings
    in ChromaDB.
    """

    if not embedded_chunks:
        return 0

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for item in embedded_chunks:

        chunk: DocumentChunk = item["chunk"]

        ids.append(chunk.chunk_id)

        documents.append(chunk.content)

        embeddings.append(item["embedding"])

        metadata = {
            "document_id": chunk.document_id,
            "filename": chunk.filename,
            "file_type": chunk.file_type,
        }

        if chunk.page_number is not None:
            metadata["page_number"] = chunk.page_number

        if chunk.row_number is not None:
            metadata["row_number"] = chunk.row_number

        metadatas.append(metadata)

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return len(ids)