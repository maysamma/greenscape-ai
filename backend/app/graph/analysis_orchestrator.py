import inspect
import logging
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.agents.design_analyzer.agent import DesignAnalyzerAgent
from app.models.analysis_result import AnalysisResult
from app.models.project import Project
from app.services.analysis_result_service import AnalysisResultService
from app.services.vision_service import vision_service


logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    def __init__(self) -> None:
        self.result_service = AnalysisResultService()

    async def run(
        self,
        db: Session,
        project: Project,
        analysis_result: AnalysisResult,
    ) -> AnalysisResult:
        try:
            file_path = self._resolve_file_path(
                project.file_path
            )

            # المرحلة الأولى: Vision
            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="vision",
                progress=10,
                error_message=None,
            )

            project.status = "vision_running"
            db.add(project)
            db.commit()

            vision_result = await (
                vision_service.analyze_floor_plan(
                    file_path=file_path
                )
            )

            self.result_service.save_vision_result(
                db=db,
                analysis_result=analysis_result,
                vision_result=vision_result,
            )

            # المرحلة الثانية: Design Analyzer
            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="design_analysis",
                progress=50,
                error_message=None,
            )

            project.status = "design_analysis_running"
            db.add(project)
            db.commit()

            project_data = self._build_project_data(
                project
            )

            design_analysis = await (
                self._run_design_analyzer(
                    project_data=project_data,
                    file_path=file_path,
                    vision_result=vision_result,
                )
            )

            self.result_service.save_design_analysis(
                db=db,
                analysis_result=analysis_result,
                design_analysis=design_analysis,
            )

            # إكمال النسخة الأولى من الـ Workflow
            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="completed",
                current_stage="completed",
                progress=100,
                error_message=None,
            )

            project.status = "completed"

            db.add(project)
            db.commit()
            db.refresh(analysis_result)

            return analysis_result

        except Exception as exc:
            logger.exception(
                "Analysis failed for project %s",
                project.id,
            )

            db.rollback()

            stored_result = (
                self.result_service.get_by_project_id(
                    db=db,
                    project_id=project.id,
                )
            )

            if stored_result is not None:
                self.result_service.update_status(
                    db=db,
                    analysis_result=stored_result,
                    status="failed",
                    current_stage=(
                        stored_result.current_stage
                    ),
                    progress=stored_result.progress,
                    error_message=str(exc),
                )

            project.status = "failed"

            db.add(project)
            db.commit()

            raise

    @staticmethod
    def _resolve_file_path(
        stored_file_path: str,
    ) -> str:
        path = Path(stored_file_path)

        if not path.is_absolute():
            backend_dir = (
                Path(__file__)
                .resolve()
                .parents[2]
            )

            path = backend_dir / path

        path = path.resolve()

        if not path.exists():
            raise FileNotFoundError(
                f"Floor plan file not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Floor plan path is not a file: {path}"
            )

        return str(path)

    @staticmethod
    def _build_project_data(
        project: Project,
    ) -> dict[str, Any]:
        return {
            "id": project.id,
            "project_name": project.project_name,
            "building_type": project.building_type,
            "location": project.location,
            "orientation": project.orientation,
            "area": project.area,
            "floors": project.floors,
            "filename": project.filename,
            "file_path": project.file_path,
            "status": project.status,
        }

    @staticmethod
    async def _run_design_analyzer(
        project_data: dict[str, Any],
        file_path: str,
        vision_result: dict[str, Any],
    ) -> dict[str, Any]:
        agent = DesignAnalyzerAgent()

        possible_methods = [
            "run",
            "analyze",
        ]

        last_error: Exception | None = None

        for method_name in possible_methods:
            method = getattr(
                agent,
                method_name,
                None,
            )

            if method is None:
                continue

            call_variants = [
                {
                    "project_data": project_data,
                    "file_path": file_path,
                    "vision_result": vision_result,
                },
                {
                    "project_data": project_data,
                    "vision_result": vision_result,
                },
                {
                    "project_data": project_data,
                    "file_path": file_path,
                },
                {
                    "project_data": project_data,
                },
            ]

            for arguments in call_variants:
                try:
                    result = method(**arguments)

                    if inspect.isawaitable(result):
                        result = await result

                    return (
                        AnalysisOrchestrator
                        ._normalize_result(result)
                    )

                except TypeError as exc:
                    last_error = exc

        return {
            "success": True,
            "agent": "Design Analyzer Agent",
            "project_data": project_data,
            "design_features": vision_result.get(
                "totals",
                {},
            ),
            "vision_result": vision_result,
            "analysis": {
                "status": "Vision analysis completed.",
                "warning": (
                    "DesignAnalyzerAgent method "
                    "signature was not matched."
                ),
                "technical_error": (
                    str(last_error)
                    if last_error
                    else None
                ),
            },
        }

    @staticmethod
    def _normalize_result(
        result: Any,
    ) -> dict[str, Any]:
        if isinstance(result, dict):
            return result

        if hasattr(result, "model_dump"):
            return result.model_dump()

        if hasattr(result, "dict"):
            return result.dict()

        return {
            "result": str(result),
        }


analysis_orchestrator = AnalysisOrchestrator()