from __future__ import annotations

import os
from typing import Any

from app.agents.base_agent import BaseAgent
from app.agents.design_analyzer.tools import inspect_floor_plan


class DesignAnalyzerAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(
            name="Design Analyzer Agent",
            prompt_file=os.path.join(
                os.path.dirname(__file__),
                "prompt.txt",
            ),
        )

    async def analyze(
        self,
        project_data: dict[str, Any],
        image_path: str | None = None,
    ) -> dict[str, Any]:
        """
        Analyze an uploaded architectural floor plan.

        Flow:
        1. Run the Vision Pipeline.
        2. Extract architectural features.
        3. Pass the extracted features to the BaseAgent.
        4. Return the AI analysis with the original vision result.
        """

        if not image_path:
            return {
                "success": False,
                "agent": self.name,
                "error": "No floor plan file path was provided.",
                "project_data": project_data,
            }

        inspection = await inspect_floor_plan(
            file_path=image_path,
        )

        if not inspection.get("success"):
            return {
                "success": False,
                "agent": self.name,
                "error": inspection.get(
                    "error",
                    "Vision analysis failed.",
                ),
                "project_data": project_data,
                "image_information": inspection,
            }

        vision_result = inspection["vision_result"]

        design_features = self._build_design_features(
            vision_result=vision_result,
        )

        agent_input = {
            "project_data": project_data,
            "design_features": design_features,
            "vision_result": vision_result,
        }

        agent_result = await self.run(agent_input)

        if not isinstance(agent_result, dict):
            agent_result = {
                "analysis": agent_result,
            }

        return {
            "success": True,
            "agent": self.name,
            "project_data": project_data,
            "design_features": design_features,
            "vision_result": vision_result,
            "analysis": agent_result,
        }

    @staticmethod
    def _build_design_features(
        vision_result: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert the detailed Vision Pipeline output into a concise
        structure that can be consumed by the remaining AI agents.
        """

        totals = vision_result.get(
            "totals",
            {},
        )

        pages = vision_result.get(
            "pages",
            [],
        )

        room_labels: list[str] = []
        rooms: list[dict[str, Any]] = []
        openings: list[dict[str, Any]] = []
        detected_objects: list[dict[str, Any]] = []
        scales: list[dict[str, Any]] = []

        yolo_model_loaded = False
        metric_measurements_available = False

        for page in pages:
            summary = page.get(
                "summary",
                {},
            )

            room_labels.extend(
                summary.get(
                    "recognized_room_labels",
                    [],
                )
            )

            rooms.extend(
                page.get(
                    "rooms",
                    [],
                )
            )

            openings.extend(
                page.get(
                    "openings",
                    [],
                )
            )

            detected_objects.extend(
                page.get(
                    "objects",
                    [],
                )
            )

            scale = page.get(
                "scale",
                {},
            )

            if scale:
                scales.append(scale)

            quality = page.get(
                "quality",
                {},
            )

            if quality.get("yolo_model_loaded"):
                yolo_model_loaded = True

            if quality.get(
                "metric_measurements_available"
            ):
                metric_measurements_available = True

        unique_room_labels = list(
            dict.fromkeys(
                label.strip()
                for label in room_labels
                if isinstance(label, str)
                and label.strip()
            )
        )

        return {
            "page_count": vision_result.get(
                "page_count",
                len(pages),
            ),
            "room_count": totals.get(
                "rooms",
                0,
            ),
            "wall_segment_count": totals.get(
                "walls",
                0,
            ),
            "door_count": totals.get(
                "doors",
                0,
            ),
            "window_count": totals.get(
                "windows",
                0,
            ),
            "unknown_opening_count": totals.get(
                "unknown_openings",
                0,
            ),
            "recognized_text_count": totals.get(
                "texts",
                0,
            ),
            "recognized_room_labels": unique_room_labels,
            "rooms": rooms,
            "openings": openings,
            "detected_objects": detected_objects,
            "scales": scales,
            "quality": {
                "yolo_model_loaded": yolo_model_loaded,
                "metric_measurements_available": (
                    metric_measurements_available
                ),
            },
        }