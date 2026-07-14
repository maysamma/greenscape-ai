from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(slots=True)
class PreprocessedFloorPlan:
    original: np.ndarray
    gray: np.ndarray
    denoised: np.ndarray
    binary: np.ndarray
    line_mask: np.ndarray
    text_image: np.ndarray
    skew_angle: float


class FloorPlanPreprocessor:
    """
    Prepare floor-plan images for:
    - wall detection
    - room detection
    - OCR
    - YOLO detection

    The preprocessing pipeline:
    1. validates the image
    2. normalizes size if necessary
    3. converts to grayscale
    4. removes noise
    5. corrects small skew angles
    6. creates an adaptive binary image
    7. extracts horizontal and vertical line structures
    8. creates an OCR-friendly image
    """

    def __init__(
        self,
        *,
        max_dimension: int = 4000,
        adaptive_block_size: int = 31,
        adaptive_constant: int = 15,
        horizontal_kernel_ratio: int = 40,
        vertical_kernel_ratio: int = 40,
    ) -> None:
        if max_dimension <= 0:
            raise ValueError(
                "max_dimension must be greater than zero."
            )

        if adaptive_block_size < 3:
            raise ValueError(
                "adaptive_block_size must be at least 3."
            )

        if adaptive_block_size % 2 == 0:
            adaptive_block_size += 1

        self.max_dimension = max_dimension
        self.adaptive_block_size = adaptive_block_size
        self.adaptive_constant = adaptive_constant
        self.horizontal_kernel_ratio = max(
            10,
            horizontal_kernel_ratio,
        )
        self.vertical_kernel_ratio = max(
            10,
            vertical_kernel_ratio,
        )

    def process(
        self,
        image: np.ndarray,
    ) -> PreprocessedFloorPlan:
        if image is None:
            raise ValueError(
                "FloorPlanPreprocessor received an empty image."
            )

        if not isinstance(image, np.ndarray):
            raise TypeError(
                "FloorPlanPreprocessor expects a numpy image."
            )

        normalized = self._resize_if_needed(
            image
        )

        original = self._ensure_bgr(
            normalized
        )

        gray = cv2.cvtColor(
            original,
            cv2.COLOR_BGR2GRAY,
        )

        denoised = cv2.bilateralFilter(
            gray,
            d=7,
            sigmaColor=50,
            sigmaSpace=50,
        )

        corrected, skew_angle = self._deskew(
            denoised
        )

        binary = cv2.adaptiveThreshold(
            corrected,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY_INV,
            blockSize=self.adaptive_block_size,
            C=self.adaptive_constant,
        )

        binary = self._remove_small_noise(
            binary
        )

        line_mask = self._extract_line_mask(
            binary
        )

        text_image = self._prepare_text_image(
            corrected
        )

        return PreprocessedFloorPlan(
            original=original,
            gray=corrected,
            denoised=corrected,
            binary=binary,
            line_mask=line_mask,
            text_image=text_image,
            skew_angle=round(
                float(skew_angle),
                3,
            ),
        )

    def _resize_if_needed(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        height, width = image.shape[:2]

        largest_dimension = max(
            height,
            width,
        )

        if largest_dimension <= self.max_dimension:
            return image.copy()

        scale = (
            self.max_dimension
            / float(largest_dimension)
        )

        new_width = max(
            1,
            int(width * scale),
        )

        new_height = max(
            1,
            int(height * scale),
        )

        return cv2.resize(
            image,
            (new_width, new_height),
            interpolation=cv2.INTER_AREA,
        )

    @staticmethod
    def _ensure_bgr(
        image: np.ndarray,
    ) -> np.ndarray:
        if len(image.shape) == 2:
            return cv2.cvtColor(
                image,
                cv2.COLOR_GRAY2BGR,
            )

        if len(image.shape) != 3:
            raise ValueError(
                "Unsupported image dimensions."
            )

        channels = image.shape[2]

        if channels == 3:
            return image.copy()

        if channels == 4:
            return cv2.cvtColor(
                image,
                cv2.COLOR_BGRA2BGR,
            )

        raise ValueError(
            f"Unsupported image channel count: {channels}"
        )

    def _deskew(
        self,
        gray: np.ndarray,
    ) -> tuple[np.ndarray, float]:
        edges = cv2.Canny(
            gray,
            threshold1=50,
            threshold2=150,
            apertureSize=3,
        )

        lines = cv2.HoughLines(
            edges,
            rho=1,
            theta=np.pi / 180,
            threshold=180,
        )

        if lines is None:
            return gray, 0.0

        angles: list[float] = []

        for line in lines[:80]:
            theta = float(
                line[0][1]
            )

            angle = (
                theta * 180.0 / np.pi
            ) - 90.0

            if -15.0 <= angle <= 15.0:
                angles.append(angle)

        if not angles:
            return gray, 0.0

        median_angle = float(
            np.median(angles)
        )

        if abs(median_angle) < 0.15:
            return gray, 0.0

        height, width = gray.shape[:2]

        center = (
            width / 2.0,
            height / 2.0,
        )

        rotation_matrix = cv2.getRotationMatrix2D(
            center,
            median_angle,
            1.0,
        )

        rotated = cv2.warpAffine(
            gray,
            rotation_matrix,
            (width, height),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )

        return rotated, median_angle

    @staticmethod
    def _remove_small_noise(
        binary: np.ndarray,
    ) -> np.ndarray:
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (2, 2),
        )

        opened = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            kernel,
            iterations=1,
        )

        closed = cv2.morphologyEx(
            opened,
            cv2.MORPH_CLOSE,
            kernel,
            iterations=1,
        )

        return closed

    def _extract_line_mask(
        self,
        binary: np.ndarray,
    ) -> np.ndarray:
        height, width = binary.shape[:2]

        horizontal_length = max(
            15,
            width // self.horizontal_kernel_ratio,
        )

        vertical_length = max(
            15,
            height // self.vertical_kernel_ratio,
        )

        horizontal_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (horizontal_length, 1),
        )

        vertical_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (1, vertical_length),
        )

        horizontal_lines = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            horizontal_kernel,
            iterations=1,
        )

        vertical_lines = cv2.morphologyEx(
            binary,
            cv2.MORPH_OPEN,
            vertical_kernel,
            iterations=1,
        )

        line_mask = cv2.bitwise_or(
            horizontal_lines,
            vertical_lines,
        )

        connector_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (3, 3),
        )

        line_mask = cv2.morphologyEx(
            line_mask,
            cv2.MORPH_CLOSE,
            connector_kernel,
            iterations=1,
        )

        return line_mask

    @staticmethod
    def _prepare_text_image(
        gray: np.ndarray,
    ) -> np.ndarray:
        enhanced = cv2.equalizeHist(
            gray
        )

        text_image = cv2.adaptiveThreshold(
            enhanced,
            maxValue=255,
            adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            thresholdType=cv2.THRESH_BINARY,
            blockSize=31,
            C=11,
        )

        cleanup_kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT,
            (2, 2),
        )

        text_image = cv2.morphologyEx(
            text_image,
            cv2.MORPH_OPEN,
            cleanup_kernel,
            iterations=1,
        )

        return text_image