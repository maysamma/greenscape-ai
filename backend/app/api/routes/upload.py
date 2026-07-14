from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.project import Project


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
}


@router.post("/upload")
async def upload_floor_plan(
    file: UploadFile = File(...),
    project_name: str = Form(...),
    building_type: str = Form(...),
    location: str = Form(...),
    orientation: str = Form(""),
    area: float = Form(0),
    db: Session = Depends(get_db),
):

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED:
        raise HTTPException(
            status_code=400,
            detail="Only PDF, PNG, JPG and JPEG are allowed.",
        )

    project_id = str(uuid4())[:8]

    filename = f"{project_id}_{file.filename}"

    save_path = UPLOAD_DIR / filename

    with open(save_path, "wb") as f:
        f.write(await file.read())

    project = Project(
        id=project_id,
        project_name=project_name,
        building_type=building_type,
        location=location,
        orientation=orientation,
        area=area,
        filename=filename,
        file_path=str(save_path),
        status="uploaded",
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "status": "success",
        "project_id": project.id,
        "project_name": project.project_name,
        "filename": project.filename,
        "message": "Project uploaded successfully.",
    }