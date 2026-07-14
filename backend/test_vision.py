import json

from app.vision.pipeline import VisionPipeline

import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pipeline = VisionPipeline(
    yolo_model_path="models/floorplan_yolo.pt",
    tesseract_languages="eng+ara",
    pdf_dpi=300,
)

result = pipeline.analyze(
    "uploads/test-floor-plan.png",
)

print(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    )
)