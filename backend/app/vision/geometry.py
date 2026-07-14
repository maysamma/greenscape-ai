from __future__ import annotations

from dataclasses import asdict, dataclass
from math import hypot
from typing import Any

import cv2
import numpy as np


@dataclass(slots=True)
class WallSegment:
    x1: int
    y1: int
    x2: int
    y2: int
    length_pixels: float
    orientation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ScaleInformation:
    pixels_per_meter: float | None
    scale_text: str | None
    status: str
    source: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class GeometryAnalyzer:
    """
    Extract geometric information from processed floor-plan images.

    This class:
    - detects line segments representing possible walls
    - estimates orientation of each segment
    - attempts to read drawing scale from OCR text
    - never invents metric measurements when calibration is unavailable
    """

    def __init__(
        self,
        *,
        hough_threshold: int = 60,
        min_line_length: int = 40,
        max_line_gap: int = 12,
        merge_distance: int = 10,
    ) -> None:
        self.hough_threshold = hough_threshold
        self.min_line_length = min_line_length
        self.max_line_gap = max_line_gap
        self.merge_distance = merge_distance

    def detect_walls(
        self,
        line_mask: np.ndarray,
    ) -> list[WallSegment]:
        """
        Detect potential wall segments using the probabilistic
        Hough transform.
        """

        if line_mask is None:
            raise ValueError(
                "GeometryAnalyzer received an empty line mask."
            )

        gray = self._ensure_grayscale(
            line_mask,
        )

        lines = cv2.HoughLinesP(
            gray,
            rho=1,
            theta=np.pi / 180,
            threshold=self.hough_threshold,
            minLineLength=self.min_line_length,
            maxLineGap=self.max_line_gap,
        )

        if lines is None:
            return []

        wall_segments: list[WallSegment] = []

        for line in lines:
            coordinates = np.asarray(
                line
            ).reshape(-1)

            if coordinates.size != 4:
                continue

            x1, y1, x2, y2 = map(
                int,
                coordinates,
            )

            length = hypot(
                x2 - x1,
                y2 - y1,
            )

            if length < self.min_line_length:
                continue

            orientation = self._classify_orientation(
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
            )

            wall_segments.append(
                WallSegment(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    length_pixels=round(
                        float(length),
                        2,
                    ),
                    orientation=orientation,
                )
            )

        return self._remove_duplicate_segments(
            wall_segments
        )

    def estimate_scale(
        self,
        texts: list[Any],
    ) -> ScaleInformation:
        """
        Attempt to identify common architectural scale text such as:

        - 1:100
        - 1 / 50
        - Scale 1:200

        A ratio by itself does not provide pixels-per-meter unless a
        known printed or measured reference length is also available.
        Therefore pixels_per_meter remains None until true calibration.
        """

        for item in texts:
            text = self._extract_text_value(
                item
            )

            if not text:
                continue

            normalized = (
                text.lower()
                .replace(" ", "")
                .replace("scale", "")
            )

            ratio = self._parse_scale_ratio(
                normalized
            )

            if ratio is None:
                continue

            return ScaleInformation(
                pixels_per_meter=None,
                scale_text=f"1:{ratio}",
                status="scale_detected_not_calibrated",
                source="ocr",
            )

        return ScaleInformation(
            pixels_per_meter=None,
            scale_text=None,
            status="not_calibrated",
            source=None,
        )

    @staticmethod
    def pixel_length_to_meters(
        length_pixels: float,
        pixels_per_meter: float | None,
    ) -> float | None:
        """
        Convert a pixel length to meters only when calibration exists.
        """

        if (
            pixels_per_meter is None
            or pixels_per_meter <= 0
        ):
            return None

        return round(
            float(length_pixels)
            / float(pixels_per_meter),
            3,
        )

    @staticmethod
    def pixel_area_to_square_meters(
        area_pixels: float,
        pixels_per_meter: float | None,
    ) -> float | None:
        """
        Convert pixel area to square meters only when calibration exists.
        """

        if (
            pixels_per_meter is None
            or pixels_per_meter <= 0
        ):
            return None

        return round(
            float(area_pixels)
            / float(pixels_per_meter ** 2),
            3,
        )

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
    def _classify_orientation(
        *,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
    ) -> str:
        delta_x = abs(x2 - x1)
        delta_y = abs(y2 - y1)

        if delta_x >= delta_y * 3:
            return "horizontal"

        if delta_y >= delta_x * 3:
            return "vertical"

        return "diagonal"

    def _remove_duplicate_segments(
        self,
        segments: list[WallSegment],
    ) -> list[WallSegment]:
        unique_segments: list[WallSegment] = []

        sorted_segments = sorted(
            segments,
            key=lambda item: item.length_pixels,
            reverse=True,
        )

        for segment in sorted_segments:
            duplicate = any(
                self._segments_are_similar(
                    segment,
                    existing,
                )
                for existing in unique_segments
            )

            if not duplicate:
                unique_segments.append(
                    segment
                )

        return unique_segments

    def _segments_are_similar(
        self,
        first: WallSegment,
        second: WallSegment,
    ) -> bool:
        if first.orientation != second.orientation:
            return False

        direct_distance = (
            abs(first.x1 - second.x1)
            + abs(first.y1 - second.y1)
            + abs(first.x2 - second.x2)
            + abs(first.y2 - second.y2)
        )

        reverse_distance = (
            abs(first.x1 - second.x2)
            + abs(first.y1 - second.y2)
            + abs(first.x2 - second.x1)
            + abs(first.y2 - second.y1)
        )

        endpoint_distance = min(
            direct_distance,
            reverse_distance,
        )

        return endpoint_distance <= (
            self.merge_distance * 4
        )

    @staticmethod
    def _extract_text_value(
        item: Any,
    ) -> str:
        if item is None:
            return ""

        if isinstance(item, str):
            return item.strip()

        if isinstance(item, dict):
            value = (
                item.get("text")
                or item.get("value")
                or item.get("content")
                or ""
            )

            return str(value).strip()

        value = getattr(
            item,
            "text",
            "",
        )

        return str(value).strip()

    @staticmethod
    def _parse_scale_ratio(
        text: str,
    ) -> int | None:
        """
        Parse scale formats such as 1:100, 1/50, and 1-200.
        """

        separators = (
            ":",
            "/",
            "-",
        )

        for separator in separators:
            if separator not in text:
                continue

            left, right = text.split(
                separator,
                maxsplit=1,
            )

            if left != "1":
                continue

            numeric_right = "".join(
                character
                for character in right
                if character.isdigit()
            )

            if not numeric_right:
                continue

            ratio = int(
                numeric_right
            )

            if 10 <= ratio <= 5000:
                return ratio

        return None