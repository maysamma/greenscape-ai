from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from app.vision.pipeline import VisionPipeline


class VisionService:
    def __init__(self) -> None:
        self.pipeline = VisionPipeline(
            yolo_model_path="models/floorplan_yolo.pt",
            tesseract_languages="eng+ara",
            pdf_dpi=300,
        )

    async def analyze_floor_plan(
        self,
        file_path: str | Path,
    ) -> dict[str, Any]:
        return await asyncio.to_thread(
            self.pipeline.analyze,
            file_path,
        )


vision_service = VisionService()