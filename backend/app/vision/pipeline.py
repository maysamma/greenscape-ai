from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.vision.detector import YoloFloorPlanDetector
from app.vision.door_window_detector import DoorWindowDetector
from app.vision.feature_extractor import FeatureExtractor
from app.vision.geometry import GeometryAnalyzer
from app.vision.loader import FloorPlanLoader
from app.vision.preprocess import FloorPlanPreprocessor
from app.vision.room_detector import RoomDetector
from app.vision.text_detector import TextDetector


class VisionPipeline:
    def __init__(
        self,
        *,
        yolo_model_path: str | Path | None = "models/floorplan_yolo.pt",
        tesseract_languages: str = "eng+ara",
        pdf_dpi: int = 300,
        device: str | None = None,
    ) -> None:
        self.loader = FloorPlanLoader(
            pdf_dpi=pdf_dpi,
        )

        self.preprocessor = FloorPlanPreprocessor()

        self.detector = YoloFloorPlanDetector(
            yolo_model_path,
            device=device,
        )

        self.room_detector = RoomDetector()

        self.opening_detector = DoorWindowDetector()

        self.text_detector = TextDetector(
            languages=tesseract_languages,
        )

        self.geometry = GeometryAnalyzer()

        self.feature_extractor = FeatureExtractor()

    def analyze(
        self,
        file_path: str | Path,
    ) -> dict[str, Any]:
        """
        Run the complete vision pipeline on an uploaded floor plan.

        Supports:
        - Images
        - Single-page PDFs
        - Multi-page PDFs
        """

        loaded_pages = self.loader.load(
            file_path,
        )

        page_results: list[dict[str, Any]] = []

        for page in loaded_pages:
            processed = self.preprocessor.process(
                page.image,
            )

            yolo_detections = self.detector.detect(
                processed.original,
            )

            walls = self.geometry.detect_walls(
                processed.line_mask,
            )

            rooms = self.room_detector.detect(
                processed.line_mask,
            )

            texts = self.text_detector.detect(
                processed.text_image,
            )

            self.text_detector.attach_room_labels(
                rooms,
                texts,
            )

            openings = self.opening_detector.detect(
                processed.binary,
                processed.line_mask,
                yolo_detections,
            )

            scale = self.geometry.estimate_scale(
                texts,
            )

            page_result = self.feature_extractor.extract(
                page_number=page.page_number,
                image_width=processed.original.shape[1],
                image_height=processed.original.shape[0],
                rooms=rooms,
                walls=walls,
                openings=openings,
                texts=texts,
                yolo_detections=yolo_detections,
                scale=scale,
                yolo_available=self.detector.available,
            )

            page_results.append(
                page_result,
            )

        return self.feature_extractor.merge_pages(
            str(Path(file_path)),
            page_results,
        )

    def analyze_to_json(
        self,
        file_path: str | Path,
        output_path: str | Path,
    ) -> dict[str, Any]:
        """
        Run the pipeline and save its result as a JSON file.
        """

        result = self.analyze(
            file_path,
        )

        output = Path(
            output_path,
        )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output.write_text(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        return result