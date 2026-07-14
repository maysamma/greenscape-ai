from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(slots=True)
class Detection:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int]
    class_id: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class YoloFloorPlanDetector:
    """
    Runs a custom YOLO model trained for architectural floor plans.

    A generic YOLO/COCO model is intentionally not used because its classes
    do not represent architectural symbols such as doors and windows.

    If the custom model is missing, the detector returns an empty list
    instead of generating fake detections.
    """

    def __init__(
        self,
        model_path: str | Path | None,
        confidence: float = 0.30,
        iou: float = 0.50,
        device: str | None = None,
    ) -> None:
        self.model_path = (
            Path(model_path).resolve()
            if model_path
            else None
        )

        self.confidence = confidence
        self.iou = iou
        self.device = device
        self._model = None

    @property
    def available(self) -> bool:
        """
        Return True only when the custom YOLO weights exist.
        """

        return (
            self.model_path is not None
            and self.model_path.is_file()
        )

    def _load_model(self) -> None:
        """
        Load the YOLO model only when it is needed.
        """

        if self._model is not None:
            return

        if not self.available:
            return

        try:
            from ultralytics import YOLO

        except ImportError as exc:
            raise RuntimeError(
                "The ultralytics package is not installed. "
                "Install it using: pip install ultralytics"
            ) from exc

        self._model = YOLO(
            str(self.model_path)
        )

    def detect(
        self,
        image: np.ndarray,
    ) -> list[Detection]:
        """
        Detect architectural objects in a floor-plan image.
        """

        if image is None:
            raise ValueError(
                "YOLO detector received an empty image."
            )

        if not isinstance(image, np.ndarray):
            raise TypeError(
                "YOLO detector expects an OpenCV numpy image."
            )

        if not self.available:
            return []

        self._load_model()

        if self._model is None:
            return []

        results = self._model.predict(
            source=image,
            conf=self.confidence,
            iou=self.iou,
            device=self.device,
            verbose=False,
        )

        detections: list[Detection] = []

        for result in results:
            if result.boxes is None:
                continue

            names = result.names

            boxes = (
                result.boxes.xyxy
                .cpu()
                .numpy()
            )

            confidences = (
                result.boxes.conf
                .cpu()
                .numpy()
            )

            classes = (
                result.boxes.cls
                .cpu()
                .numpy()
                .astype(int)
            )

            for box, score, class_id in zip(
                boxes,
                confidences,
                classes,
                strict=True,
            ):
                x1, y1, x2, y2 = map(
                    int,
                    box.tolist(),
                )

                label = str(
                    names[class_id]
                ).strip().lower()

                detections.append(
                    Detection(
                        label=label,
                        confidence=round(
                            float(score),
                            4,
                        ),
                        bbox=(
                            x1,
                            y1,
                            x2,
                            y2,
                        ),
                        class_id=int(class_id),
                    )
                )

        return detections