from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.rag_service import process_query


router = APIRouter(
    prefix="/api/v1/query",
    tags=["Query"],
)


class QueryRequest(BaseModel):
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    document_ids: list[str] | None = Field(
    default=None,
    min_length=1,
    )


@router.post("")
async def query_documents(
    request: QueryRequest,
):

    try:

        result = process_query(
            query=request.query,
            top_k=request.top_k,
            document_ids=request.document_ids,
        )

        return result

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        print("QUERY ERROR:", exc)

        raise HTTPException(
            status_code=500,
            detail="Failed to process query.",
        )