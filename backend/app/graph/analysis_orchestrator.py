import inspect
import logging
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.agents.design_analyzer.agent import DesignAnalyzerAgent
from app.agents.architecture_review.agent import ArchitectureReviewAgent
from app.agents.sustainability.agent import SustainabilityAgent
from app.agents.energy.agent import EnergyAgent
from app.agents.lighting.agent import LightingAgent
from app.agents.ventilation.agent import VentilationAgent
from app.agents.accessibility.agent import AccessibilityAgent
from app.agents.building_code.agent import BuildingCodeAgent
from app.agents.cost.agent import CostAgent
from app.agents.report_generator.agent import ReportGeneratorAgent



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

            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="architecture",
                progress=70,
                error_message=None,
            )

            project.status = "architecture_running"
            db.add(project)
            db.commit()

            architecture_agent = ArchitectureReviewAgent()

            architecture_result = await architecture_agent.analyze(
                project_data=project_data,
                design_analysis=design_analysis,
            )

            self.result_service.save_architecture_result(
                db=db,
                analysis_result=analysis_result,
                architecture_result=architecture_result,
            )


            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="sustainability",
                progress=80,
                error_message=None,
            )

            project.status = "sustainability_running"
            db.add(project)
            db.commit()

            sustainability_agent = SustainabilityAgent()

            sustainability_result = await sustainability_agent.analyze(
                project_data=project_data,
                design_analysis=design_analysis,
                architecture_result=architecture_result,
            )

            self.result_service.save_sustainability_result(
                db=db,
                analysis_result=analysis_result,
                sustainability_result=sustainability_result,
            )


            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="energy",
                progress=88,
                error_message=None,
            )

            project.status = "energy_running"
            db.add(project)
            db.commit()

            energy_agent = EnergyAgent()

            energy_result = await energy_agent.analyze(
                project_data=project_data,
                design_analysis=design_analysis,
                architecture_result=architecture_result,
                sustainability_result=sustainability_result,
            )

            self.result_service.save_energy_result(
                db=db,
                analysis_result=analysis_result,
                energy_result=energy_result,
            )




            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="lighting",
                progress=94,
                error_message=None,
            )

            project.status = "lighting_running"
            db.add(project)
            db.commit()

            lighting_agent = LightingAgent()

            lighting_result = await lighting_agent.analyze(
                project_data=project_data,
                design_analysis=design_analysis,
                architecture_result=architecture_result,
                sustainability_result=sustainability_result,
                energy_result=energy_result,
            )

            self.result_service.save_lighting_result(
                db=db,
                analysis_result=analysis_result,
                lighting_result=lighting_result,
            )

            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="ventilation",
                progress=96,
                error_message=None,
            )

            project.status = "ventilation_running"
            db.add(project)
            db.commit()

            ventilation_agent = VentilationAgent()

            ventilation_result = await ventilation_agent.analyze(
                project_data=project_data,
                design_analysis=design_analysis,
                architecture_result=architecture_result,
                sustainability_result=sustainability_result,
                energy_result=energy_result,
                lighting_result=lighting_result,
            )

            self.result_service.save_ventilation_result(
                db=db,
                analysis_result=analysis_result,
                ventilation_result=ventilation_result,
            )


            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="accessibility",
                progress=98,
                error_message=None,
            )

            project.status = "accessibility_running"
            db.add(project)
            db.commit()

            accessibility_agent = AccessibilityAgent()

            accessibility_result = await accessibility_agent.analyze(
                project_data=project_data,
                design_analysis=design_analysis,
                architecture_result=architecture_result,
                sustainability_result=sustainability_result,
                energy_result=energy_result,
                lighting_result=lighting_result,
                ventilation_result=ventilation_result,
            )

            self.result_service.save_accessibility_result(
                db=db,
                analysis_result=analysis_result,
                accessibility_result=accessibility_result,
            )


            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="building_code",
                progress=99,
                error_message=None,
            )

            project.status = "building_code_running"
            db.add(project)
            db.commit()

            building_code_agent = BuildingCodeAgent()

            building_code_result = await building_code_agent.analyze(
                project_data=project_data,
                design_analysis=design_analysis,
                architecture_result=architecture_result,
                sustainability_result=sustainability_result,
                energy_result=energy_result,
                lighting_result=lighting_result,
                ventilation_result=ventilation_result,
                accessibility_result=accessibility_result,
            )

            self.result_service.save_building_code_result(
                db=db,
                analysis_result=analysis_result,
                building_code_result=building_code_result,
            )


            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="cost",
                progress=99,
                error_message=None,
            )

            project.status = "cost_running"
            db.add(project)
            db.commit()

            cost_agent = CostAgent()

            cost_result = await cost_agent.analyze(
                project_data=project_data,
                design_analysis=design_analysis,
                architecture_result=architecture_result,
                sustainability_result=sustainability_result,
                energy_result=energy_result,
                lighting_result=lighting_result,
                ventilation_result=ventilation_result,
                accessibility_result=accessibility_result,
                building_code_result=building_code_result,
            )

            self.result_service.save_cost_result(
                db=db,
                analysis_result=analysis_result,
                cost_result=cost_result,
            )

            self.result_service.update_status(
                db=db,
                analysis_result=analysis_result,
                status="running",
                current_stage="report_generation",
                progress=100,
                error_message=None,
            )

            project.status = "report_generation_running"
            db.add(project)
            db.commit()

            report_agent = ReportGeneratorAgent()

            report_result = await report_agent.analyze(
                project_data=project_data,
                agent_results={
                    "design_analysis": design_analysis,
                    "architecture": architecture_result,
                    "sustainability": sustainability_result,
                    "energy": energy_result,
                    "lighting": lighting_result,
                    "ventilation": ventilation_result,
                    "accessibility": accessibility_result,
                    "building_code": building_code_result,
                    "cost": cost_result,
                },
            )

            self.result_service.save_report_result(
                db=db,
                analysis_result=analysis_result,
                report_result=report_result,
            )































            


            self.result_service.calculate_and_save_overall_score(
                db=db,
                analysis_result=analysis_result,
                architecture_result=architecture_result,
                sustainability_result=sustainability_result,
                energy_result=energy_result,
                lighting_result=lighting_result,
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

        result = await agent.analyze(
            project_data=project_data,
            file_path=file_path,
            vision_result=vision_result,
        )

        return AnalysisOrchestrator._normalize_result(
            result
        )

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