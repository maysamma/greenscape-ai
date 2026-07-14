from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import cv2
import numpy as np


@dataclass(slots=True)
class Room:
    room_id: int
    bbox: tuple[int, int, int, int]
    center: tuple[int, int]
    area_pixels: float
    perimeter_pixels: float
    label: str | None = None
    label_confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RoomDetector:
    """
    Detect enclosed room-like spaces from a floor-plan line mask.

    The detector relies on connected enclosed regions produced by
    the architectural wall structure. It does not invent room names.
    Labels can later be attached by the OCR TextDetector.
    """

    def __init__(
        self,
        *,
        min_area_ratio: float = 0.001,
        max_area_ratio: float = 0.85,
        min_width: int = 25,
        min_height: int = 25,
        wall_close_kernel: int = 7,
    ) -> None:
        self.min_area_ratio = min_area_ratio
        self.max_area_ratio = max_area_ratio
        self.min_width = min_width
        self.min_height = min_height
        self.wall_close_kernel = max(
            3,
            wall_close_kernel,
        )

    def detect(
        self,
        line_mask: np.ndarray,
    ) -> list[Room]:
        if line_mask is None:
            raise ValueError(
                "RoomDetector received an empty line mask."
            )

        gray = self._ensure_grayscale(
            line_mask
        )

        height, width = gray.shape[:2]
        image_area = height * width

        if image_area <= 0:
            return []

        wall_mask = self._strengthen_walls(
            gray
        )

        free_space = cv2.bitwise_not(
            wall_mask
        )

        flood_filled = free_space.copy()

        flood_mask = np.zeros(
            (height + 2, width + 2),
            dtype=np.uint8,
        )

        cv2.floodFill(
            flood_filled,
            flood_mask,
            seedPoint=(0, 0),
            newVal=0,
        )

        enclosed_regions = flood_filled

        cleanup_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (3, 3),
        )

        enclosed_regions = cv2.morphologyEx(
            enclosed_regions,
            cv2.MORPH_OPEN,
            cleanup_kernel,
            iterations=1,
        )

        contours, _ = cv2.findContours(
            enclosed_regions,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        minimum_area = max(
            100,
            int(image_area * self.min_area_ratio),
        )

        maximum_area = int(
            image_area * self.max_area_ratio
        )

        rooms: list[Room] = []

        for contour in contours:
            area = float(
                cv2.contourArea(contour)
            )

            if area < minimum_area:
                continue

            if area > maximum_area:
                continue

            x, y, room_width, room_height = (
                cv2.boundingRect(contour)
            )

            if room_width < self.min_width:
                continue

            if room_height < self.min_height:
                continue

            perimeter = float(
                cv2.arcLength(
                    contour,
                    closed=True,
                )
            )

            if perimeter <= 0:
                continue

            rectangularity = area / max(
                1.0,
                float(room_width * room_height),
            )

            if rectangularity < 0.20:
                continue

            center = self._calculate_center(
                contour=contour,
                fallback_bbox=(
                    x,
                    y,
                    room_width,
                    room_height,
                ),
            )

            rooms.append(
                Room(
                    room_id=0,
                    bbox=(
                        int(x),
                        int(y),
                        int(x + room_width),
                        int(y + room_height),
                    ),
                    center=center,
                    area_pixels=round(
                        area,
                        2,
                    ),
                    perimeter_pixels=round(
                        perimeter,
                        2,
                    ),
                )
            )

        rooms = self._remove_duplicates(
            rooms
        )

        rooms.sort(
            key=lambda room: (
                room.bbox[1],
                room.bbox[0],
            )
        )

        for index, room in enumerate(
            rooms,
            start=1,
        ):
            room.room_id = index

        return rooms

    def _strengthen_walls(
        self,
        line_mask: np.ndarray,
    ) -> np.ndarray:
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (
                self.wall_close_kernel,
                self.wall_close_kernel,
            ),
        )

        closed = cv2.morphologyEx(
            line_mask,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=2,
        )

        dilation_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (3, 3),
        )

        strengthened = cv2.dilate(
            closed,
            dilation_kernel,
            iterations=1,
        )

        _, binary = cv2.threshold(
            strengthened,
            1,
            255,
            cv2.THRESH_BINARY,
        )

        return binary

    @staticmethod
    def _calculate_center(
        *,
        contour: np.ndarray,
        fallback_bbox: tuple[int, int, int, int],
    ) -> tuple[int, int]:
        moments = cv2.moments(
            contour
        )

        if moments["m00"] != 0:
            center_x = int(
                moments["m10"]
                / moments["m00"]
            )

            center_y = int(
                moments["m01"]
                / moments["m00"]
            )

            return (
                center_x,
                center_y,
            )

        x, y, width, height = fallback_bbox

        return (
            int(x + width / 2),
            int(y + height / 2),
        )

    def _remove_duplicates(
        self,
        rooms: list[Room],
    ) -> list[Room]:
        unique_rooms: list[Room] = []

        sorted_rooms = sorted(
            rooms,
            key=lambda room: room.area_pixels,
            reverse=True,
        )

        for room in sorted_rooms:
            duplicate = any(
                self._intersection_over_union(
                    room.bbox,
                    existing.bbox,
                ) >= 0.70
                for existing in unique_rooms
            )

            if not duplicate:
                unique_rooms.append(
                    room
                )

        return unique_rooms

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

        if intersection_area <= 0:
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