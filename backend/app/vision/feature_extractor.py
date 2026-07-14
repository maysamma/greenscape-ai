from __future__ import annotations

from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class FeatureExtractor:
    """
    Convert raw computer-vision detections into a serializable
    GreenScape Vision result.

    This class does not generate mock values. All counts and features
    are calculated from the objects detected by the pipeline.
    """

    def extract(
        self,
        *,
        page_number: int,
        image_width: int,
        image_height: int,
        rooms: list[Any],
        walls: list[Any],
        openings: list[Any],
        texts: list[Any],
        yolo_detections: list[Any],
        scale: dict[str, Any] | Any | None,
        yolo_available: bool,
    ) -> dict[str, Any]:
        """
        Build the final output for one floor-plan page.
        """

        serialized_rooms = [
            self._serialize_item(room)
            for room in rooms
        ]

        serialized_walls = [
            self._serialize_item(wall)
            for wall in walls
        ]

        serialized_openings = [
            self._serialize_item(opening)
            for opening in openings
        ]

        serialized_texts = [
            self._serialize_item(text)
            for text in texts
        ]

        serialized_objects = [
            self._serialize_item(detection)
            for detection in yolo_detections
        ]

        serialized_scale = self._serialize_scale(
            scale
        )

        room_labels = self._extract_room_labels(
            serialized_rooms,
            serialized_texts,
        )

        door_count = sum(
            1
            for opening in serialized_openings
            if self._opening_type(opening) == "door"
        )

        window_count = sum(
            1
            for opening in serialized_openings
            if self._opening_type(opening) == "window"
        )

        unknown_opening_count = sum(
            1
            for opening in serialized_openings
            if self._opening_type(opening)
            not in {"door", "window"}
        )

        metric_measurements_available = bool(
            serialized_scale.get("pixels_per_meter")
        )

        return {
            "page_number": int(page_number),
            "image": {
                "width": int(image_width),
                "height": int(image_height),
                "area_pixels": int(
                    image_width * image_height
                ),
            },
            "summary": {
                "room_count": len(serialized_rooms),
                "wall_segment_count": len(serialized_walls),
                "door_count": door_count,
                "window_count": window_count,
                "unknown_opening_count": (
                    unknown_opening_count
                ),
                "recognized_text_count": len(
                    serialized_texts
                ),
                "detected_object_count": len(
                    serialized_objects
                ),
                "recognized_room_labels": room_labels,
            },
            "rooms": serialized_rooms,
            "walls": serialized_walls,
            "openings": serialized_openings,
            "texts": serialized_texts,
            "objects": serialized_objects,
            "scale": serialized_scale,
            "quality": {
                "yolo_model_loaded": bool(
                    yolo_available
                ),
                "metric_measurements_available": (
                    metric_measurements_available
                ),
                "room_labels_detected": bool(
                    room_labels
                ),
                "ocr_text_detected": bool(
                    serialized_texts
                ),
            },
        }

    def merge_pages(
        self,
        source_file: str,
        pages: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Merge page-level results into one complete floor-plan result.
        """

        total_rooms = 0
        total_walls = 0
        total_doors = 0
        total_windows = 0
        total_unknown_openings = 0
        total_texts = 0
        total_objects = 0

        all_room_labels: list[str] = []

        for page in pages:
            summary = page.get(
                "summary",
                {},
            )

            total_rooms += self._safe_int(
                summary.get("room_count")
            )

            total_walls += self._safe_int(
                summary.get("wall_segment_count")
            )

            total_doors += self._safe_int(
                summary.get("door_count")
            )

            total_windows += self._safe_int(
                summary.get("window_count")
            )

            total_unknown_openings += self._safe_int(
                summary.get("unknown_opening_count")
            )

            total_texts += self._safe_int(
                summary.get("recognized_text_count")
            )

            total_objects += self._safe_int(
                summary.get("detected_object_count")
            )

            labels = summary.get(
                "recognized_room_labels",
                [],
            )

            if isinstance(labels, list):
                for label in labels:
                    if (
                        isinstance(label, str)
                        and label.strip()
                    ):
                        all_room_labels.append(
                            label.strip()
                        )

        unique_room_labels = list(
            dict.fromkeys(all_room_labels)
        )

        source_path = Path(source_file)

        return {
            "schema_version": "1.0.0",
            "success": True,
            "source_file": str(source_path),
            "source_filename": source_path.name,
            "file_type": source_path.suffix.lower(),
            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "page_count": len(pages),
            "totals": {
                "rooms": total_rooms,
                "walls": total_walls,
                "doors": total_doors,
                "windows": total_windows,
                "unknown_openings": (
                    total_unknown_openings
                ),
                "texts": total_texts,
                "objects": total_objects,
            },
            "recognized_room_labels": (
                unique_room_labels
            ),
            "pages": pages,
        }

    @staticmethod
    def _serialize_item(
        item: Any,
    ) -> dict[str, Any]:
        """
        Convert dataclasses, objects with to_dict(), or dictionaries
        into JSON-safe dictionaries.
        """

        if item is None:
            return {}

        if isinstance(item, dict):
            value = dict(item)

        elif hasattr(item, "to_dict"):
            value = item.to_dict()

        elif is_dataclass(item):
            value = asdict(item)

        elif hasattr(item, "__dict__"):
            value = {
                key: val
                for key, val in vars(item).items()
                if not key.startswith("_")
            }

        else:
            return {
                "value": FeatureExtractor._json_safe(
                    item
                )
            }

        return {
            str(key): FeatureExtractor._json_safe(
                val
            )
            for key, val in value.items()
        }

    @staticmethod
    def _serialize_scale(
        scale: dict[str, Any] | Any | None,
    ) -> dict[str, Any]:
        """
        Normalize scale information without inventing metric values.
        """

        if scale is None:
            return {
                "pixels_per_meter": None,
                "scale_text": None,
                "status": "not_calibrated",
            }

        serialized = FeatureExtractor._serialize_item(
            scale
        )

        pixels_per_meter = serialized.get(
            "pixels_per_meter"
        )

        if pixels_per_meter:
            serialized.setdefault(
                "status",
                "calibrated",
            )
        else:
            serialized.setdefault(
                "pixels_per_meter",
                None,
            )
            serialized.setdefault(
                "scale_text",
                None,
            )
            serialized.setdefault(
                "status",
                "not_calibrated",
            )

        return serialized

    @staticmethod
    def _extract_room_labels(
        rooms: list[dict[str, Any]],
        texts: list[dict[str, Any]],
    ) -> list[str]:
        labels: list[str] = []

        room_label_keys = {
            "label",
            "name",
            "room_name",
            "room_label",
            "text",
        }

        for room in rooms:
            for key in room_label_keys:
                value = room.get(key)

                if (
                    isinstance(value, str)
                    and value.strip()
                ):
                    labels.append(
                        value.strip()
                    )
                    break

        for text_item in texts:
            is_room_label = text_item.get(
                "is_room_label",
                False,
            )

            room_id = text_item.get(
                "room_id"
            )

            if not is_room_label and room_id is None:
                continue

            value = (
                text_item.get("text")
                or text_item.get("value")
                or text_item.get("content")
            )

            if (
                isinstance(value, str)
                and value.strip()
            ):
                labels.append(
                    value.strip()
                )

        return list(
            dict.fromkeys(labels)
        )

    @staticmethod
    def _opening_type(
        opening: dict[str, Any],
    ) -> str:
        value = (
            opening.get("opening_type")
            or opening.get("type")
            or opening.get("label")
            or "unknown_opening"
        )

        normalized = str(
            value
        ).strip().lower()

        if "door" in normalized:
            return "door"

        if "window" in normalized:
            return "window"

        return "unknown_opening"

    @staticmethod
    def _json_safe(
        value: Any,
    ) -> Any:
        """
        Convert tuples, paths, numpy scalars, and nested structures
        into JSON-safe values.
        """

        if value is None:
            return None

        if isinstance(
            value,
            (str, int, float, bool),
        ):
            return value

        if isinstance(value, Path):
            return str(value)

        if isinstance(value, tuple):
            return [
                FeatureExtractor._json_safe(item)
                for item in value
            ]

        if isinstance(value, list):
            return [
                FeatureExtractor._json_safe(item)
                for item in value
            ]

        if isinstance(value, dict):
            return {
                str(key): FeatureExtractor._json_safe(
                    item
                )
                for key, item in value.items()
            }

        if hasattr(value, "item"):
            try:
                return value.item()
            except (ValueError, TypeError):
                pass

        if is_dataclass(value):
            return FeatureExtractor._json_safe(
                asdict(value)
            )

        if hasattr(value, "to_dict"):
            return FeatureExtractor._json_safe(
                value.to_dict()
            )

        return str(value)

    @staticmethod
    def _safe_int(
        value: Any,
    ) -> int:
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0