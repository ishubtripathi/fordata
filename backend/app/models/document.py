from pydantic import BaseModel, Field
from typing import Any


class DocumentResponse(BaseModel):

    document_id: str

    filename: str

    file_type: str

    status: str

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    statistics: dict[str, Any] = Field(
        default_factory=dict
    )

    content: Any = None