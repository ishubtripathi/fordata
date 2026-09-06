import time

from app.services.retrieval_service import (
    retrieve_relevant_chunks,
    format_retrieval_results,
)

from app.services.llm_service import generate_answer


# source builder function to build clean source information from retrieved document chunks.

def build_sources(
    retrieved_chunks: list[dict],
) -> list[dict]:
    """
    Build clean source information from
    retrieved document chunks.
    """

    sources = []

    for item in retrieved_chunks:

        source = item.get("source", {})

        source_data = {
            "filename": source.get("filename"),
            "file_type": source.get("file_type"),
            "page_number": source.get("page_number"),
            "row_number": source.get("row_number"),
            "distance": item.get("distance"),
        }

        sources.append(source_data)

    return sources


def process_query(
    query: str,
    top_k: int = 5,
    document_ids: list[str] | None = None,
) -> dict:

    start_time = time.time()

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    # 1. Retrieval
    retrieval_start = time.time()

    results = retrieve_relevant_chunks(
        query=query,
        top_k=top_k,
        document_ids=document_ids,
    )

    retrieval_time = time.time() - retrieval_start

    # 2. Format results
    retrieved_chunks = format_retrieval_results(results)

    if not retrieved_chunks:
        return {
            "query": query,
            "answer": (
                "The information was not found "
                "in the uploaded documents."
            ),
            "retrieved_chunks": [],
            "chunk_count": 0,
            "context": "",
            "sources": [],
        }

    # 3. Context
    context = build_context(retrieved_chunks)

    # 4. Prompt
    prompt = build_rag_prompt(
        query=query,
        context=context,
    )

    # 5. LLM
    llm_start = time.time()

    answer = generate_answer(prompt)

    llm_time = time.time() - llm_start

    # 6. Sources
    sources = build_sources(retrieved_chunks)

    total_time = time.time() - start_time

    print(
        f"""
QUERY PERFORMANCE
-----------------
Retrieval: {retrieval_time:.2f}s
LLM:       {llm_time:.2f}s
Total:     {total_time:.2f}s
"""
    )

    return {
        "query": query,
        "answer": answer,
        "retrieved_chunks": retrieved_chunks,
        "chunk_count": len(retrieved_chunks),
        "context": context,
        "sources": sources,
    }
    
def build_context(
    retrieved_chunks: list[dict],
) -> str:
    """
    Build a structured context from retrieved chunks.
    """

    if not retrieved_chunks:
        return ""

    context_parts = []

    for index, item in enumerate(
        retrieved_chunks,
        start=1,
    ):

        content = item.get("content", "")
        source = item.get("source", {})

        filename = source.get(
            "filename",
            "unknown",
        )

        page_number = source.get(
            "page_number"
        )

        row_number = source.get(
            "row_number"
        )

        if page_number is not None:

            source_info = (
                f"{filename}, Page {page_number}"
            )

        elif row_number is not None:

            source_info = (
                f"{filename}, Row {row_number}"
            )

        else:

            source_info = filename

        context_parts.append(
            f"[Source {index}: {source_info}]\n"
            f"{content}"
        )

    return "\n\n".join(context_parts)



def build_rag_prompt(
    query: str,
    context: str,
) -> str:
    """
    Build a grounded RAG prompt for the LLM.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if not context or not context.strip():
        context = "No relevant information was found."

    prompt = f"""
You are StarQ, a document question-answering assistant.

Answer the user's question using ONLY the information
provided in the context.

STRICT RULES:

1. Use only information from the provided context.
2. Do not use outside knowledge.
3. Do not invent or assume information.
4. If the answer cannot be found in the context, say:
   "The information was not found in the uploaded documents."
5. Give a direct and concise answer.
6. Use clean, natural language.
7. Do not use unnecessary Markdown.
8. Do not use asterisks (*) for emphasis.
9. Do not use headings unless they improve readability.
10. Do not repeat the question.
11. Do not mention "context", "chunks", embeddings, or the RAG system.
12. If the answer contains multiple points, use simple bullet points.
13. Do not include unnecessary symbols or formatting.

CONTEXT:
--------------------
{context}
--------------------

USER QUESTION:
{query}

ANSWER:
"""

    return prompt.strip()