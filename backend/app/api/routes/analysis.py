import traceback
from time import perf_counter

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    status,
)
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.project import Project
from app.schemas.analysis_result import (
    AnalysisResultResponse,
    AnalysisStartResponse,
)
from app.services.analysis_result_service import (
    AnalysisResultService,
)
from app.services.analysis_service import AnalysisService
from app.services.analysis_task_service import (
    run_project_analysis_task,
)


router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


class ProjectAnalysisRequest(BaseModel):
    project_name: str | None = None
    building_type: str | None = None
    location: str | None = None
    orientation: str | None = None
    floors: int | None = None

    total_area_m2: float | None = None
    usable_area_m2: float | None = None
    floor_area_m2: float | None = None
    built_up_area_m2: float | None = None
    window_area_m2: float | None = None

    windows_count: int | None = None
    exits_count: int | None = None

    minimum_door_width_cm: float | None = None
    minimum_corridor_width_cm: float | None = None

    insulation: str | None = None
    glazing_type: str | None = None
    window_to_wall_ratio: float | None = None
    design_complexity: str | None = None

    shading_devices: bool = False
    solar_panels: bool = False
    green_space: bool = False
    rainwater_collection: bool = False
    water_saving_fixtures: bool = False
    recycled_materials: bool = False
    local_materials: bool = False

    natural_ventilation: bool = False
    natural_lighting: bool = False
    opposite_openings: bool = False
    operable_windows: bool = False
    courtyard: bool = False
    skylights: bool = False
    kitchen_exhaust: bool = False
    bathroom_exhaust: bool = False

    step_free_entrance: bool = False
    accessible_bathroom: bool = False
    accessible_parking: bool = False
    ramp: bool = False
    elevator: bool = False

    applicable_code: str | None = None
    cost_per_square_meter_sar: float | None = None

    internal_rooms_without_windows: list[str] = Field(
        default_factory=list
    )


# --------------------------------------------------
# Manual analysis endpoint
# يحتفظ بالـ endpoint القديم للتحليل من JSON مباشرة
# --------------------------------------------------
@router.post("")
async def run_analysis(
    request: ProjectAnalysisRequest,
):
    """
    Run GreenScape AI agents directly using request data.

    This endpoint does not require an uploaded project.
    """

    start_time = perf_counter()

    try:
        analysis_service = AnalysisService()

        project_data = request.model_dump()

        result = await analysis_service.analyze_project(
            project_data=project_data,
        )

        analysis_time = round(
            perf_counter() - start_time,
            2,
        )

        return {
            **result,
            "analysis_time_seconds": analysis_time,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error

    except Exception as error:
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error


# --------------------------------------------------
# Start project analysis
# Project -> Vision -> Design Analyzer -> Database
# --------------------------------------------------
@router.post(
    "/{project_id}/start",
    response_model=AnalysisStartResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def start_project_analysis(
    project_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Start analysis for an uploaded project.
    """

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    analysis_result = (
        AnalysisResultService.get_or_create(
            db=db,
            project_id=project_id,
        )
    )

    if analysis_result.status == "running":
        return AnalysisStartResponse(
            success=True,
            project_id=project_id,
            analysis_id=analysis_result.id,
            status="running",
            message="Analysis is already running.",
        )

    # Reset state when restarting a failed or completed analysis.
    AnalysisResultService.update_status(
        db=db,
        analysis_result=analysis_result,
        status="pending",
        current_stage="waiting",
        progress=0,
        error_message=None,
    )

    project.status = "analysis_pending"

    db.add(project)
    db.commit()
    db.refresh(project)

    background_tasks.add_task(
        run_project_analysis_task,
        project_id,
    )

    return AnalysisStartResponse(
        success=True,
        project_id=project_id,
        analysis_id=analysis_result.id,
        status="pending",
        message="Analysis started successfully.",
    )


# --------------------------------------------------
# Read stored analysis
# أزلنا الـ Mock Data وأصبح يقرأ من SQLite
# --------------------------------------------------
@router.get(
    "/{project_id}",
    response_model=AnalysisResultResponse,
)
async def get_project_analysis(
    project_id: str,
    db: Session = Depends(get_db),
):
    """
    Return the saved analysis state and results for a project.
    """

    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    analysis_result = (
        AnalysisResultService.get_by_project_id(
            db=db,
            project_id=project_id,
        )
    )

    if analysis_result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "No analysis exists for this project. "
                "Start the analysis first."
            ),
        )

    return AnalysisResultService.to_response_dict(
        analysis_result
    )