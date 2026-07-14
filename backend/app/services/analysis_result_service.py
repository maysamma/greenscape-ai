import json
from typing import Any

from sqlalchemy.orm import Session

from app.models.analysis_result import AnalysisResult


class AnalysisResultService:
    @staticmethod
    def serialize_json(
        data: Any,
    ) -> str | None:
        if data is None:
            return None

        return json.dumps(
            data,
            ensure_ascii=False,
            default=str,
        )

    @staticmethod
    def deserialize_json(
        data: str | None,
    ) -> dict | None:
        if not data:
            return None

        try:
            result = json.loads(data)

            if isinstance(result, dict):
                return result

            return {
                "data": result,
            }

        except json.JSONDecodeError:
            return {
                "raw_data": data,
                "parse_error": True,
            }

    @staticmethod
    def get_by_project_id(
        db: Session,
        project_id: str,
    ) -> AnalysisResult | None:
        return (
            db.query(AnalysisResult)
            .filter(
                AnalysisResult.project_id
                == project_id
            )
            .first()
        )

    @staticmethod
    def get_or_create(
        db: Session,
        project_id: str,
    ) -> AnalysisResult:
        analysis_result = (
            AnalysisResultService.get_by_project_id(
                db=db,
                project_id=project_id,
            )
        )

        if analysis_result:
            return analysis_result

        analysis_result = AnalysisResult(
            project_id=project_id,
            status="pending",
            current_stage="waiting",
            progress=0,
        )

        db.add(analysis_result)
        db.commit()
        db.refresh(analysis_result)

        return analysis_result

    @staticmethod
    def update_status(
        db: Session,
        analysis_result: AnalysisResult,
        *,
        status: str,
        current_stage: str,
        progress: int,
        error_message: str | None = None,
    ) -> AnalysisResult:
        analysis_result.status = status
        analysis_result.current_stage = current_stage
        analysis_result.progress = max(
            0,
            min(progress, 100),
        )
        analysis_result.error_message = error_message

        db.add(analysis_result)
        db.commit()
        db.refresh(analysis_result)

        return analysis_result

    @staticmethod
    def save_vision_result(
        db: Session,
        analysis_result: AnalysisResult,
        vision_result: dict,
    ) -> AnalysisResult:
        analysis_result.vision_result_json = (
            AnalysisResultService.serialize_json(
                vision_result
            )
        )

        db.add(analysis_result)
        db.commit()
        db.refresh(analysis_result)

        return analysis_result

    @staticmethod
    def save_design_analysis(
        db: Session,
        analysis_result: AnalysisResult,
        design_analysis: dict,
    ) -> AnalysisResult:
        analysis_result.design_analysis_json = (
            AnalysisResultService.serialize_json(
                design_analysis
            )
        )

        db.add(analysis_result)
        db.commit()
        db.refresh(analysis_result)

        return analysis_result

    @staticmethod
    def build_agent_statuses(
        analysis_result: AnalysisResult,
    ) -> list[dict]:
        agents = [
            {
                "name": "Vision Agent",
                "stage": "vision",
                "result": (
                    analysis_result
                    .vision_result_json
                ),
            },
            {
                "name": "Design Analyzer Agent",
                "stage": "design_analysis",
                "result": (
                    analysis_result
                    .design_analysis_json
                ),
            },
            {
                "name": "Architecture Agent",
                "stage": "architecture",
                "result": (
                    analysis_result
                    .architecture_result_json
                ),
            },
            {
                "name": "Sustainability Agent",
                "stage": "sustainability",
                "result": (
                    analysis_result
                    .sustainability_result_json
                ),
            },
            {
                "name": "Energy Agent",
                "stage": "energy",
                "result": (
                    analysis_result
                    .energy_result_json
                ),
            },
            {
                "name": "Lighting Agent",
                "stage": "lighting",
                "result": (
                    analysis_result
                    .lighting_result_json
                ),
            },
            {
                "name": "Ventilation Agent",
                "stage": "ventilation",
                "result": (
                    analysis_result
                    .ventilation_result_json
                ),
            },
            {
                "name": "Accessibility Agent",
                "stage": "accessibility",
                "result": (
                    analysis_result
                    .accessibility_result_json
                ),
            },
            {
                "name": "Building Code Agent",
                "stage": "building_code",
                "result": (
                    analysis_result
                    .building_code_result_json
                ),
            },
            {
                "name": "Cost Agent",
                "stage": "cost",
                "result": (
                    analysis_result
                    .cost_result_json
                ),
            },
            {
                "name": "Report Generator",
                "stage": "report",
                "result": (
                    analysis_result
                    .report_result_json
                ),
            },
        ]

        result = []

        for agent in agents:
            if agent["result"]:
                agent_status = "Completed"

            elif (
                analysis_result.status == "failed"
                and analysis_result.current_stage
                == agent["stage"]
            ):
                agent_status = "Failed"

            elif (
                analysis_result.status == "running"
                and analysis_result.current_stage
                == agent["stage"]
            ):
                agent_status = "Running"

            else:
                agent_status = "Waiting"

            result.append({
                "name": agent["name"],
                "status": agent_status,
            })

        return result

    @staticmethod
    def to_response_dict(
        analysis_result: AnalysisResult,
    ) -> dict:
        service = AnalysisResultService

        return {
            "id": analysis_result.id,
            "project_id": (
                analysis_result.project_id
            ),
            "status": analysis_result.status,
            "current_stage": (
                analysis_result.current_stage
            ),
            "progress": analysis_result.progress,
            "error_message": (
                analysis_result.error_message
            ),
            "overall_score": (
                analysis_result.overall_score
            ),

            "vision_result": (
                service.deserialize_json(
                    analysis_result
                    .vision_result_json
                )
            ),

            "design_analysis": (
                service.deserialize_json(
                    analysis_result
                    .design_analysis_json
                )
            ),

            "architecture_result": (
                service.deserialize_json(
                    analysis_result
                    .architecture_result_json
                )
            ),

            "sustainability_result": (
                service.deserialize_json(
                    analysis_result
                    .sustainability_result_json
                )
            ),

            "energy_result": (
                service.deserialize_json(
                    analysis_result
                    .energy_result_json
                )
            ),

            "lighting_result": (
                service.deserialize_json(
                    analysis_result
                    .lighting_result_json
                )
            ),

            "ventilation_result": (
                service.deserialize_json(
                    analysis_result
                    .ventilation_result_json
                )
            ),

            "accessibility_result": (
                service.deserialize_json(
                    analysis_result
                    .accessibility_result_json
                )
            ),

            "building_code_result": (
                service.deserialize_json(
                    analysis_result
                    .building_code_result_json
                )
            ),

            "cost_result": (
                service.deserialize_json(
                    analysis_result
                    .cost_result_json
                )
            ),

            "report_result": (
                service.deserialize_json(
                    analysis_result
                    .report_result_json
                )
            ),

            "agents": (
                service.build_agent_statuses(
                    analysis_result
                )
            ),

            "created_at": (
                analysis_result.created_at
            ),
            "updated_at": (
                analysis_result.updated_at
            ),
        }