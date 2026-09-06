from pydantic import BaseModel


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    file_type: str
    content: str
    page_number: int | None = None
    row_number: int | None = None