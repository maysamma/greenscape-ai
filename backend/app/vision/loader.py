from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


@dataclass(slots=True)
class LoadedPage:
    page_number: int
    image: np.ndarray
    source_path: str
    width: int
    height: int


class FloorPlanLoader:
    """
    Load architectural floor plans from image files or PDFs.

    Supported formats:
    - PNG
    - JPG / JPEG
    - BMP
    - TIFF
    - PDF
    """

    SUPPORTED_IMAGE_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tif",
        ".tiff",
    }

    def __init__(
        self,
        *,
        pdf_dpi: int = 300,
    ) -> None:
        if pdf_dpi <= 0:
            raise ValueError(
                "pdf_dpi must be greater than zero."
            )

        self.pdf_dpi = pdf_dpi

    def load(
        self,
        file_path: str | Path,
    ) -> list[LoadedPage]:
        path = Path(file_path).resolve()

        if not path.exists():
            raise FileNotFoundError(
                f"Floor plan file was not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"The supplied path is not a file: {path}"
            )

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return self._load_pdf(path)

        if suffix in self.SUPPORTED_IMAGE_EXTENSIONS:
            return [
                self._load_image(
                    path=path,
                    page_number=1,
                )
            ]

        raise ValueError(
            "Unsupported floor plan format. "
            "Supported formats are PNG, JPG, JPEG, BMP, TIFF, and PDF."
        )

    def _load_image(
        self,
        *,
        path: Path,
        page_number: int,
    ) -> LoadedPage:
        image = cv2.imread(
            str(path),
            cv2.IMREAD_COLOR,
        )

        if image is None:
            raise ValueError(
                f"The image could not be decoded: {path}"
            )

        height, width = image.shape[:2]

        return LoadedPage(
            page_number=page_number,
            image=image,
            source_path=str(path),
            width=int(width),
            height=int(height),
        )

    def _load_pdf(
        self,
        path: Path,
    ) -> list[LoadedPage]:
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError(
                "PyMuPDF is required to read PDF floor plans. "
                "Install it using: pip install PyMuPDF"
            ) from exc

        try:
            document = fitz.open(
                str(path)
            )
        except Exception as exc:
            raise ValueError(
                f"The PDF could not be opened: {path}"
            ) from exc

        pages: list[LoadedPage] = []

        try:
            if document.page_count == 0:
                raise ValueError(
                    "The PDF does not contain any pages."
                )

            zoom = self.pdf_dpi / 72.0

            matrix = fitz.Matrix(
                zoom,
                zoom,
            )

            for page_index in range(
                document.page_count
            ):
                page = document.load_page(
                    page_index
                )

                pixmap = page.get_pixmap(
                    matrix=matrix,
                    alpha=False,
                )

                image = self._pixmap_to_bgr(
                    pixmap
                )

                height, width = image.shape[:2]

                pages.append(
                    LoadedPage(
                        page_number=page_index + 1,
                        image=image,
                        source_path=str(path),
                        width=int(width),
                        height=int(height),
                    )
                )

        finally:
            document.close()

        return pages

    @staticmethod
    def _pixmap_to_bgr(
        pixmap,
    ) -> np.ndarray:
        """
        Convert a PyMuPDF Pixmap into an OpenCV BGR image.
        """

        channels = pixmap.n

        image = np.frombuffer(
            pixmap.samples,
            dtype=np.uint8,
        ).reshape(
            pixmap.height,
            pixmap.width,
            channels,
        )

        if channels == 1:
            return cv2.cvtColor(
                image,
                cv2.COLOR_GRAY2BGR,
            )

        if channels == 3:
            return cv2.cvtColor(
                image,
                cv2.COLOR_RGB2BGR,
            )

        if channels == 4:
            return cv2.cvtColor(
                image,
                cv2.COLOR_RGBA2BGR,
            )

        raise ValueError(
            f"Unsupported PDF image channel count: {channels}"
        )