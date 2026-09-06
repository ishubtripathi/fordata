
import os
import tempfile

from fastapi import (
    APIRouter,
    File,
    UploadFile,
    HTTPException,
)

from app.models.document import DocumentResponse

from app.services.pdf_service import (
    validate_pdf,
    extract_pdf_text,
    extract_pdf_metadata,
)

from app.services.csv_service import (
    validate_csv,
    parse_csv,
    detect_csv_schema,
    profile_csv_data,
)

from app.services.content_service import (
    create_document_chunks,
)

from app.services.embedding_service import (
    generate_chunk_embeddings,
)

from app.services.vector_service import (
    store_embeddings,
)




# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


# ==========================================================
# CONSTANTS
# ==========================================================

ALLOWED_FILE_TYPES = {
    "application/pdf",
    "text/csv",
}

CHUNK_SIZE = 1024 * 1024  # 1 MB


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

async def save_uploaded_file(
    file: UploadFile,
    suffix: str,
) -> str:
    """
    Save an uploaded file to a temporary location.

    The file is written in chunks so large files do not
    need to be loaded completely into memory.
    """

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
        mode="wb",
    ) as temp_file:

        temp_file_path = temp_file.name

        while True:

            chunk = await file.read(CHUNK_SIZE)

            if not chunk:
                break

            temp_file.write(chunk)

    return temp_file_path


def process_pdf_file(
    file: UploadFile,
    temp_file_path: str,
) -> dict:
    """
    Validate, extract, chunk, embed and store a PDF.
    """

    # ------------------------------------------------------
    # Validate PDF
    # ------------------------------------------------------

    validation_result = validate_pdf(
        temp_file_path
    )

    if not validation_result["valid"]:
        raise ValueError(
            validation_result["error"]
        )

    # ------------------------------------------------------
    # Extract PDF text
    # ------------------------------------------------------

    pages = []

    for page in extract_pdf_text(
        temp_file_path
    ):
        pages.append(page)

    # ------------------------------------------------------
    # Extract metadata/statistics
    # ------------------------------------------------------

    document_info = extract_pdf_metadata(
        temp_file_path
    )

    # ------------------------------------------------------
    # Create document chunks
    # ------------------------------------------------------

    chunks = create_document_chunks(
        filename=file.filename or "unknown.pdf",
        file_type="pdf",
        content=pages,
    )

    # ------------------------------------------------------
    # Generate embeddings
    # ------------------------------------------------------

    embedded_chunks = generate_chunk_embeddings(
        chunks
    )

    # ------------------------------------------------------
    # Store embeddings in ChromaDB
    # ------------------------------------------------------

    stored_count = store_embeddings(
        embedded_chunks
    )

    # ------------------------------------------------------
    # Build response
    # ------------------------------------------------------

    return {
        "filename": file.filename,
        "file_type": "pdf",
        "status": "processed",
        "metadata": document_info["metadata"],
        "statistics": {
            **document_info["statistics"],
            "chunk_count": len(chunks),
            "embedded_chunk_count": len(
                embedded_chunks
            ),
            "stored_chunk_count": stored_count,
        },
        "content": pages,
    }


def process_csv_file(
    file: UploadFile,
    temp_file_path: str,
) -> dict:
    """
    Validate, parse, profile, chunk, embed and store a CSV.
    """

    # ------------------------------------------------------
    # Validate CSV
    # ------------------------------------------------------

    validation_result = validate_csv(
        temp_file_path
    )

    if not validation_result["valid"]:
        raise ValueError(
            validation_result["error"]
        )

    # ------------------------------------------------------
    # Parse CSV
    # ------------------------------------------------------

    parsed_data = parse_csv(
        temp_file_path
    )

    # ------------------------------------------------------
    # Detect CSV schema
    # ------------------------------------------------------

    schema = detect_csv_schema(
        parsed_data["rows"],
        parsed_data["headers"],
    )

    # ------------------------------------------------------
    # Profile CSV data
    # ------------------------------------------------------

    profile = profile_csv_data(
        parsed_data["rows"],
        schema,
    )

    # ------------------------------------------------------
    # Create document chunks
    # ------------------------------------------------------

    chunks = create_document_chunks(
        filename=file.filename or "unknown.csv",
        file_type="csv",
        content=parsed_data["rows"],
    )

    # ------------------------------------------------------
    # Generate embeddings
    # ------------------------------------------------------

    embedded_chunks = generate_chunk_embeddings(
        chunks
    )

    # ------------------------------------------------------
    # Store embeddings in ChromaDB
    # ------------------------------------------------------

    stored_count = store_embeddings(
        embedded_chunks
    )

    # ------------------------------------------------------
    # Build response
    # ------------------------------------------------------

    return {
        "filename": file.filename,
        "file_type": "csv",
        "status": "processed",
        "metadata": {
            "delimiter": validation_result[
                "delimiter"
            ],
        },
        "statistics": {
            "row_count": parsed_data[
                "row_count"
            ],
            "column_count": validation_result[
                "column_count"
            ],
            "schema": schema,
            "profile": profile,
            "chunk_count": len(chunks),
            "embedded_chunk_count": len(
                embedded_chunks
            ),
            "stored_chunk_count": stored_count,
        },
        "content": parsed_data["rows"],
    }


# ==========================================================
# SINGLE DOCUMENT UPLOAD
# ==========================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    """
    Upload and process a single PDF or CSV document.

    Pipeline:

        Upload
          ↓
        Validate
          ↓
        Extract / Parse
          ↓
        Create Chunks
          ↓
        Generate Embeddings
          ↓
        Store in ChromaDB
    """

    # ------------------------------------------------------
    # Validate file type
    # ------------------------------------------------------

    if file.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and CSV files are supported.",
        )

    temp_file_path = None

    try:

        # --------------------------------------------------
        # Determine file type
        # --------------------------------------------------

        if file.content_type == "application/pdf":

            file_type = "pdf"
            suffix = ".pdf"

        else:

            file_type = "csv"
            suffix = ".csv"

        # --------------------------------------------------
        # Save temporary file
        # --------------------------------------------------

        temp_file_path = await save_uploaded_file(
            file=file,
            suffix=suffix,
        )

        # --------------------------------------------------
        # Process document
        # --------------------------------------------------

        if file_type == "pdf":

            result = process_pdf_file(
                file=file,
                temp_file_path=temp_file_path,
            )

        else:

            result = process_csv_file(
                file=file,
                temp_file_path=temp_file_path,
            )

        # --------------------------------------------------
        # Return response
        # --------------------------------------------------

        return DocumentResponse(
            document_id=result["filename"],
            filename=result["filename"],
            file_type=result["file_type"],
            status=result["status"],
            metadata=result["metadata"],
            statistics=result["statistics"],
            content=result["content"],
        )

    except HTTPException:
        raise

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        print(
            f"DOCUMENT PROCESSING ERROR: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process document.",
        )

    finally:

        # --------------------------------------------------
        # Delete temporary file
        # --------------------------------------------------

        if (
            temp_file_path
            and os.path.exists(temp_file_path)
        ):
            os.remove(temp_file_path)


# ==========================================================
# MULTIPLE DOCUMENT UPLOAD
# ==========================================================

@router.post("/upload-multiple")
async def upload_multiple_documents(
    files: list[UploadFile] = File(...)
):
    """
    Upload and process multiple PDF and CSV documents.

    Each document is processed independently.

    If one document fails, the other documents will
    still be processed.
    """

    # ------------------------------------------------------
    # Validate files
    # ------------------------------------------------------

    if not files:
        raise HTTPException(
            status_code=400,
            detail="At least one file is required.",
        )

    results = []

    processed_files = 0
    failed_files = 0

    # ------------------------------------------------------
    # Process every uploaded file
    # ------------------------------------------------------

    for file in files:

        temp_file_path = None

        try:

            # --------------------------------------------------
            # Validate file type
            # --------------------------------------------------

            if file.content_type not in ALLOWED_FILE_TYPES:

                failed_files += 1

                results.append({
                    "filename": file.filename,
                    "file_type": None,
                    "status": "failed",
                    "error": (
                        "Only PDF and CSV files "
                        "are supported."
                    ),
                })

                continue

            # --------------------------------------------------
            # Determine file type
            # --------------------------------------------------

            if file.content_type == "application/pdf":

                file_type = "pdf"
                suffix = ".pdf"

            else:

                file_type = "csv"
                suffix = ".csv"

            # --------------------------------------------------
            # Save temporary file
            # --------------------------------------------------

            temp_file_path = await save_uploaded_file(
                file=file,
                suffix=suffix,
            )

            # --------------------------------------------------
            # Process PDF
            # --------------------------------------------------

            if file_type == "pdf":

                result = process_pdf_file(
                    file=file,
                    temp_file_path=temp_file_path,
                )

            # --------------------------------------------------
            # Process CSV
            # --------------------------------------------------

            else:

                result = process_csv_file(
                    file=file,
                    temp_file_path=temp_file_path,
                )

            # --------------------------------------------------
            # Successful document
            # --------------------------------------------------

            processed_files += 1

            results.append({
                "filename": result["filename"],
                "file_type": result["file_type"],
                "status": result["status"],
                "metadata": result["metadata"],
                "statistics": result["statistics"],
            })

        except ValueError as exc:

            failed_files += 1

            results.append({
                "filename": file.filename,
                "file_type": None,
                "status": "failed",
                "error": str(exc),
            })

        except Exception as exc:

            failed_files += 1

            print(
                f"DOCUMENT PROCESSING ERROR "
                f"[{file.filename}]: {exc}"
            )

            results.append({
                "filename": file.filename,
                "file_type": None,
                "status": "failed",
                "error": (
                    "Failed to process document."
                ),
            })

        finally:

            # --------------------------------------------------
            # Delete temporary file
            # --------------------------------------------------

            if (
                temp_file_path
                and os.path.exists(temp_file_path)
            ):
                os.remove(temp_file_path)

    # ------------------------------------------------------
    # Return batch result
    # ------------------------------------------------------

    return {
        "total_files": len(files),
        "processed_files": processed_files,
        "failed_files": failed_files,
        "documents": results,
    }
