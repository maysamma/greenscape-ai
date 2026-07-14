from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pytesseract

from app.vision.room_detector import Room
import pytesseract

from pathlib import Path


TESSERACT_PATH = Path(
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

if TESSERACT_PATH.exists():
    pytesseract.pytesseract.tesseract_cmd = str(
        TESSERACT_PATH
    )

@dataclass(slots=True)
class DetectedText:
    text: str
    confidence: float
    bbox: tuple[int, int, int, int]
    center: tuple[int, int]
    language_hint: str | None = None
    room_id: int | None = None
    is_room_label: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TextDetector:
    """
    OCR detector for architectural floor plans.

    It extracts text using Tesseract OCR, then links text labels
    to detected rooms when the text center falls inside a room.
    """

    def __init__(
        self,
        *,
        languages: str = "eng+ara",
        min_confidence: float = 35.0,
        psm: int = 11,
        tesseract_cmd: str | None = None,
    ) -> None:
        self.languages = languages
        self.min_confidence = min_confidence
        self.psm = psm

        configured_cmd = (
            tesseract_cmd
            or self._read_tesseract_environment()
        )

        if configured_cmd:
            pytesseract.pytesseract.tesseract_cmd = configured_cmd

    def detect(
        self,
        image: np.ndarray,
    ) -> list[DetectedText]:
        if image is None:
            raise ValueError(
                "TextDetector received an empty image."
            )

        if not isinstance(image, np.ndarray):
            raise TypeError(
                "TextDetector expects a numpy image."
            )

        self._validate_tesseract()

        prepared = self._prepare_image(
            image
        )

        config = (
            f"--oem 3 --psm {self.psm} "
            "-c preserve_interword_spaces=1"
        )

        try:
            data = pytesseract.image_to_data(
                prepared,
                lang=self.languages,
                config=config,
                output_type=pytesseract.Output.DICT,
            )
        except pytesseract.TesseractError as exc:
            raise RuntimeError(
                "Tesseract OCR failed. Ensure that the requested "
                f"languages are installed: {self.languages}"
            ) from exc

        texts: list[DetectedText] = []

        total_items = len(
            data.get("text", [])
        )

        for index in range(total_items):
            raw_text = str(
                data["text"][index]
            ).strip()

            if not raw_text:
                continue

            confidence = self._parse_confidence(
                data["conf"][index]
            )

            if confidence < self.min_confidence:
                continue

            left = int(
                data["left"][index]
            )
            top = int(
                data["top"][index]
            )
            width = int(
                data["width"][index]
            )
            height = int(
                data["height"][index]
            )

            if width <= 0 or height <= 0:
                continue

            x1 = left
            y1 = top
            x2 = left + width
            y2 = top + height

            normalized_text = self._normalize_text(
                raw_text
            )

            if not normalized_text:
                continue

            texts.append(
                DetectedText(
                    text=normalized_text,
                    confidence=round(
                        confidence / 100.0,
                        4,
                    ),
                    bbox=(
                        x1,
                        y1,
                        x2,
                        y2,
                    ),
                    center=(
                        int((x1 + x2) / 2),
                        int((y1 + y2) / 2),
                    ),
                    language_hint=self._detect_language_hint(
                        normalized_text
                    ),
                )
            )

        return self._merge_nearby_words(
            texts
        )

    def attach_room_labels(
        self,
        rooms: list[Room],
        texts: list[DetectedText],
    ) -> None:
        """
        Attach OCR text to the room containing its center point.

        This updates both:
        - Room.label
        - DetectedText.room_id
        """

        if not rooms or not texts:
            return

        for text in texts:
            matching_room = self._find_containing_room(
                text=text,
                rooms=rooms,
            )

            if matching_room is None:
                continue

            text.room_id = matching_room.room_id
            text.is_room_label = True

            if matching_room.label is None:
                matching_room.label = text.text
                matching_room.label_confidence = (
                    text.confidence
                )
                continue

            current_confidence = (
                matching_room.label_confidence
                or 0.0
            )

            if text.confidence > current_confidence:
                matching_room.label = text.text
                matching_room.label_confidence = (
                    text.confidence
                )

    @staticmethod
    def _prepare_image(
        image: np.ndarray,
    ) -> np.ndarray:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY,
            )
        else:
            gray = image.copy()

        if gray.dtype != np.uint8:
            gray = cv2.normalize(
                gray,
                None,
                0,
                255,
                cv2.NORM_MINMAX,
            ).astype(np.uint8)

        return gray

    @staticmethod
    def _normalize_text(
        text: str,
    ) -> str:
        cleaned = " ".join(
            text.replace("\n", " ")
            .replace("\t", " ")
            .split()
        )

        return cleaned.strip(
            " |_-.,;:"
        )

    @staticmethod
    def _parse_confidence(
        value: Any,
    ) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return -1.0

    @staticmethod
    def _detect_language_hint(
        text: str,
    ) -> str | None:
        contains_arabic = any(
            "\u0600" <= character <= "\u06ff"
            for character in text
        )

        contains_latin = any(
            character.isascii()
            and character.isalpha()
            for character in text
        )

        if contains_arabic and contains_latin:
            return "mixed"

        if contains_arabic:
            return "ara"

        if contains_latin:
            return "eng"

        return None

    @staticmethod
    def _find_containing_room(
        *,
        text: DetectedText,
        rooms: list[Room],
    ) -> Room | None:
        center_x, center_y = text.center

        containing_rooms: list[Room] = []

        for room in rooms:
            x1, y1, x2, y2 = room.bbox

            if (
                x1 <= center_x <= x2
                and y1 <= center_y <= y2
            ):
                containing_rooms.append(
                    room
                )

        if not containing_rooms:
            return None

        return min(
            containing_rooms,
            key=lambda room: room.area_pixels,
        )

    def _merge_nearby_words(
        self,
        texts: list[DetectedText],
    ) -> list[DetectedText]:
        """
        Merge OCR words that appear on the same line and are close
        to each other.
        """

        if not texts:
            return []

        sorted_texts = sorted(
            texts,
            key=lambda item: (
                item.bbox[1],
                item.bbox[0],
            ),
        )

        merged: list[DetectedText] = []

        for current in sorted_texts:
            if not merged:
                merged.append(current)
                continue

            previous = merged[-1]

            if self._should_merge(
                previous,
                current,
            ):
                merged[-1] = self._merge_pair(
                    previous,
                    current,
                )
            else:
                merged.append(current)

        return merged

    @staticmethod
    def _should_merge(
        first: DetectedText,
        second: DetectedText,
    ) -> bool:
        first_x1, first_y1, first_x2, first_y2 = (
            first.bbox
        )
        second_x1, second_y1, second_x2, second_y2 = (
            second.bbox
        )

        first_height = max(
            1,
            first_y2 - first_y1,
        )
        second_height = max(
            1,
            second_y2 - second_y1,
        )

        vertical_difference = abs(
            first.center[1] - second.center[1]
        )

        allowed_vertical_difference = max(
            first_height,
            second_height,
        ) * 0.6

        horizontal_gap = (
            second_x1 - first_x2
        )

        allowed_horizontal_gap = max(
            first_height,
            second_height,
        ) * 1.5

        same_line = (
            vertical_difference
            <= allowed_vertical_difference
        )

        close_enough = (
            -5
            <= horizontal_gap
            <= allowed_horizontal_gap
        )

        return same_line and close_enough

    @staticmethod
    def _merge_pair(
        first: DetectedText,
        second: DetectedText,
    ) -> DetectedText:
        x1 = min(
            first.bbox[0],
            second.bbox[0],
        )
        y1 = min(
            first.bbox[1],
            second.bbox[1],
        )
        x2 = max(
            first.bbox[2],
            second.bbox[2],
        )
        y2 = max(
            first.bbox[3],
            second.bbox[3],
        )

        combined_text = (
            f"{first.text} {second.text}"
        ).strip()

        confidence = (
            first.confidence
            + second.confidence
        ) / 2.0

        return DetectedText(
            text=combined_text,
            confidence=round(
                confidence,
                4,
            ),
            bbox=(
                x1,
                y1,
                x2,
                y2,
            ),
            center=(
                int((x1 + x2) / 2),
                int((y1 + y2) / 2),
            ),
            language_hint=TextDetector._detect_language_hint(
                combined_text
            ),
        )

    @staticmethod
    def _read_tesseract_environment() -> str | None:
        import os

        configured_path = os.getenv(
            "TESSERACT_CMD"
        )

        if not configured_path:
            return None

        path = Path(
            configured_path
        )

        return str(path)

    @staticmethod
    def _validate_tesseract() -> None:
        try:
            pytesseract.get_tesseract_version()
        except (
            pytesseract.TesseractNotFoundError,
            OSError,
        ) as exc:
            raise RuntimeError(
                "Tesseract OCR was not found. Install Tesseract "
                "and configure the TESSERACT_CMD environment variable."
            ) from exc