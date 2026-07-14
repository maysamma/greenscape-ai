from __future__ import annotations

from pathlib import Path
from typing import Any

from app.services.vision_service import vision_service


async def inspect_floor_plan(
    file_path: str,
) -> dict[str, Any]:
    """
    Run the complete GreenScape Vision Pipeline.

    Supports:
    - PNG
    - JPG / JPEG
    - PDF
    - Multi-page PDF
    """

    path = Path(file_path)

    if not path.exists():
        return {
            "success": False,
            "error": "Floor plan file was not found.",
            "file_path": str(path),
        }

    supported_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tif",
        ".tiff",
        ".pdf",
    }

    if path.suffix.lower() not in supported_extensions:
        return {
            "success": False,
            "error": (
                "Unsupported floor plan format. "
                "Supported formats are PNG, JPG, JPEG, BMP, TIFF, and PDF."
            ),
            "file_path": str(path),
            "file_type": path.suffix.lower(),
        }

    try:
        vision_result = await vision_service.analyze_floor_plan(
            file_path=path,
        )

        return {
            "success": True,
            "file_path": str(path),
            "file_type": path.suffix.lower(),
            "vision_result": vision_result,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "file_path": str(path),
            "file_type": path.suffix.lower(),
        }