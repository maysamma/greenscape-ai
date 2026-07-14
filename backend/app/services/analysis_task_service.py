import logging

from app.database.session import SessionLocal
from app.graph.analysis_orchestrator import (
    analysis_orchestrator,
)
from app.models.project import Project
from app.services.analysis_result_service import (
    AnalysisResultService,
)


logger = logging.getLogger(__name__)


async def run_project_analysis_task(
    project_id: str,
) -> None:
    db = SessionLocal()

    try:
        project = (
            db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

        if project is None:
            logger.error(
                "Project not found: %s",
                project_id,
            )
            return

        analysis_result = (
            AnalysisResultService.get_or_create(
                db=db,
                project_id=project_id,
            )
        )

        await analysis_orchestrator.run(
            db=db,
            project=project,
            analysis_result=analysis_result,
        )

    except Exception:
        logger.exception(
            "Background analysis failed "
            "for project %s",
            project_id,
        )

    finally:
        db.close()