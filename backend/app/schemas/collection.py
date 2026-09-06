from pydantic import BaseModel, Field


class CollectionDocument(BaseModel):
    document_id: str
    filename: str
    file_type: str


class CollectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    documents: list[CollectionDocument] = Field(
        default_factory=list
    )


class CollectionResponse(BaseModel):
    collection_id: str
    name: str
    description: str
    documents: list[CollectionDocument] = Field(
        default_factory=list
    )