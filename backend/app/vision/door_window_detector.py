from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import cv2
import numpy as np

from app.vision.detector import Detection


@dataclass(slots=True)
class Opening:
    opening_type: str
    confidence: float
    bbox: tuple[int, int, int, int]
    center: tuple[int, int]
    source: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DoorWindowDetector:
    """
    Detect doors and windows from:

    1. Custom YOLO architectural detections.
    2. OpenCV geometric heuristics when YOLO is unavailable.

    OpenCV heuristic detections are returned as unknown_opening unless
    there is reliable evidence identifying the opening type.
    """

    DOOR_LABELS = {
        "door",
        "single_door",
        "double_door",
        "sliding_door",
        "entrance",
    }

    WINDOW_LABELS = {
        "window",
        "single_window",
        "double_window",
        "sliding_window",
    }

    def __init__(
        self,
        min_opening_width: int = 12,
        max_opening_width: int = 180,
        min_opening_height: int = 4,
        max_opening_height: int = 80,
    ) -> None:
        self.min_opening_width = min_opening_width
        self.max_opening_width = max_opening_width
        self.min_opening_height = min_opening_height
        self.max_opening_height = max_opening_height

    def detect(
        self,
        binary_image: np.ndarray,
        line_mask: np.ndarray,
        yolo_detections: list[Detection] | list[dict[str, Any]] | None = None,
    ) -> list[Opening]:
        if binary_image is None:
            raise ValueError(
                "DoorWindowDetector received an empty binary image."
            )

        if line_mask is None:
            raise ValueError(
                "DoorWindowDetector received an empty line mask."
            )

        openings: list[Opening] = []

        openings.extend(
            self._from_yolo(
                yolo_detections or [],
            )
        )

        heuristic_openings = self._from_opencv(
            binary_image=binary_image,
            line_mask=line_mask,
        )

        for opening in heuristic_openings:
            if not self._overlaps_existing(
                opening=opening,
                existing=openings,
            ):
                openings.append(opening)

        return openings

    def _from_yolo(
        self,
        detections: list[Detection] | list[dict[str, Any]],
    ) -> list[Opening]:
        openings: list[Opening] = []

        for detection in detections:
            if isinstance(detection, Detection):
                label = detection.label
                confidence = detection.confidence
                bbox = detection.bbox
            elif isinstance(detection, dict):
                label = str(
                    detection.get("label", "")
                ).strip().lower()

                confidence = float(
                    detection.get("confidence", 0.0)
                )

                raw_bbox = detection.get(
                    "bbox",
                    (0, 0, 0, 0),
                )

                bbox = tuple(
                    int(value)
                    for value in raw_bbox
                )
            else:
                continue

            normalized_label = label.strip().lower()

            if normalized_label in self.DOOR_LABELS:
                opening_type = "door"
            elif normalized_label in self.WINDOW_LABELS:
                opening_type = "window"
            else:
                continue

            x1, y1, x2, y2 = bbox

            center = (
                int((x1 + x2) / 2),
                int((y1 + y2) / 2),
            )

            openings.append(
                Opening(
                    opening_type=opening_type,
                    confidence=round(
                        float(confidence),
                        4,
                    ),
                    bbox=(
                        int(x1),
                        int(y1),
                        int(x2),
                        int(y2),
                    ),
                    center=center,
                    source="yolo",
                )
            )

        return openings

    def _from_opencv(
        self,
        binary_image: np.ndarray,
        line_mask: np.ndarray,
    ) -> list[Opening]:
        binary = self._ensure_grayscale(
            binary_image,
        )

        walls = self._ensure_grayscale(
            line_mask,
        )

        inverted_walls = cv2.bitwise_not(
            walls,
        )

        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (15, 3),
        )

        vertical_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (3, 15),
        )

        horizontal = cv2.morphologyEx(
            walls,
            cv2.MORPH_OPEN,
            horizontal_kernel,
        )

        vertical = cv2.morphologyEx(
            walls,
            cv2.MORPH_OPEN,
            vertical_kernel,
        )

        wall_structure = cv2.bitwise_or(
            horizontal,
            vertical,
        )

        possible_gaps = cv2.bitwise_and(
            inverted_walls,
            binary,
        )

        nearby_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (11, 11),
        )

        expanded_walls = cv2.dilate(
            wall_structure,
            nearby_kernel,
            iterations=1,
        )

        candidates = cv2.bitwise_and(
            possible_gaps,
            expanded_walls,
        )

        cleanup_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (3, 3),
        )

        candidates = cv2.morphologyEx(
            candidates,
            cv2.MORPH_OPEN,
            cleanup_kernel,
        )

        contours, _ = cv2.findContours(
            candidates,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        image_height, image_width = binary.shape[:2]
        image_area = image_height * image_width

        minimum_area = max(
            20,
            int(image_area * 0.00001),
        )

        maximum_area = max(
            minimum_area + 1,
            int(image_area * 0.01),
        )

        openings: list[Opening] = []

        for contour in contours:
            x, y, width, height = cv2.boundingRect(
                contour,
            )

            area = width * height

            if area < minimum_area or area > maximum_area:
                continue

            horizontal_candidate = (
                self.min_opening_width
                <= width
                <= self.max_opening_width
                and self.min_opening_height
                <= height
                <= self.max_opening_height
            )

            vertical_candidate = (
                self.min_opening_width
                <= height
                <= self.max_opening_width
                and self.min_opening_height
                <= width
                <= self.max_opening_height
            )

            if not horizontal_candidate and not vertical_candidate:
                continue

            aspect_ratio = max(
                width,
                height,
            ) / max(
                1,
                min(width, height),
            )

            if aspect_ratio < 1.5:
                continue

            x1 = int(x)
            y1 = int(y)
            x2 = int(x + width)
            y2 = int(y + height)

            openings.append(
                Opening(
                    opening_type="unknown_opening",
                    confidence=0.25,
                    bbox=(x1, y1, x2, y2),
                    center=(
                        int(x + width / 2),
                        int(y + height / 2),
                    ),
                    source="opencv_heuristic",
                )
            )

        return openings

    @staticmethod
    def _ensure_grayscale(
        image: np.ndarray,
    ) -> np.ndarray:
        if len(image.shape) == 2:
            return image

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

    @staticmethod
    def _overlaps_existing(
        opening: Opening,
        existing: list[Opening],
        threshold: float = 0.35,
    ) -> bool:
        for current in existing:
            if DoorWindowDetector._intersection_over_union(
                opening.bbox,
                current.bbox,
            ) >= threshold:
                return True

        return False

    @staticmethod
    def _intersection_over_union(
        first: tuple[int, int, int, int],
        second: tuple[int, int, int, int],
    ) -> float:
        first_x1, first_y1, first_x2, first_y2 = first
        second_x1, second_y1, second_x2, second_y2 = second

        intersection_x1 = max(
            first_x1,
            second_x1,
        )
        intersection_y1 = max(
            first_y1,
            second_y1,
        )
        intersection_x2 = min(
            first_x2,
            second_x2,
        )
        intersection_y2 = min(
            first_y2,
            second_y2,
        )

        intersection_width = max(
            0,
            intersection_x2 - intersection_x1,
        )
        intersection_height = max(
            0,
            intersection_y2 - intersection_y1,
        )

        intersection_area = (
            intersection_width
            * intersection_height
        )

        if intersection_area == 0:
            return 0.0

        first_area = max(
            0,
            first_x2 - first_x1,
        ) * max(
            0,
            first_y2 - first_y1,
        )

        second_area = max(
            0,
            second_x2 - second_x1,
        ) * max(
            0,
            second_y2 - second_y1,
        )

        union_area = (
            first_area
            + second_area
            - intersection_area
        )

        if union_area <= 0:
            return 0.0

        return intersection_area / union_area