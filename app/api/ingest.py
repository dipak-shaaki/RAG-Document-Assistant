from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from app.services.file_parser import extract_text
from app.services.chunking import chunk_text

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    strategy: str = Query("fixed", enum=["fixed", "sentence"])
):
    try:
        content = await file.read()
        text = extract_text(file.filename, content)

        chunks = chunk_text(text, strategy)

        return {
            "filename": file.filename,
            "num_chunks": len(chunks),
            "sample_chunks": chunks[:3]
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")