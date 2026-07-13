from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Form, HTTPException

router = APIRouter(prefix="/api", tags=["Upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg"
}


@router.post("/upload")
async def upload_floor_plan(
    file: UploadFile = File(...),
    project_name: str = Form(...),
    building_type: str = Form(...),
    location: str = Form(...),
    orientation: str = Form(""),
    area: float = Form(0)
):

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG are allowed."
        )

    project_id = str(uuid4())[:8]

    filename = f"{project_id}_{file.filename}"

    save_path = UPLOAD_DIR / filename

    with open(save_path, "wb") as f:
        f.write(await file.read())

    return {
        "status": "success",
        "project_id": project_id,
        "project_name": project_name,
        "filename": filename,
        "message": "File uploaded successfully"
    }