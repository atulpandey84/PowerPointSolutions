import io
from pptx import Presentation
from typing import List, Dict, Any
from app.models.architecture import SystemArchitecture, ArchitectureComponent, DataFlow

class PPTXParser:
    def __init__(self, ocr_service=None):
        self.ocr_service = ocr_service

    def parse(self, file_content: bytes) -> Dict[str, Any]:
        prs = Presentation(io.BytesIO(file_content))
        slides_data = []

        for slide_num, slide in enumerate(prs.slides):
            slide_info = {
                "slide_index": slide_num + 1,
                "text_content": [],
                "images": []
            }

            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    slide_info["text_content"].append(shape.text)

                if shape.shape_type == 13:  # Picture
                    if self.ocr_service:
                        image_bytes = shape.image.blob
                        ocr_text = self.ocr_service.extract_text(image_bytes)
                        if ocr_text:
                            slide_info["text_content"].append(f"[OCR]: {ocr_text}")

            slides_data.append(slide_info)

        return slides_data

    def reconstruct_architecture(self, slides_data: List[Dict[str, Any]]) -> SystemArchitecture:
        # This is a placeholder for a more complex logic that would use LLM to reconstruct the graph
        # For now, it returns an empty skeleton to be filled by the AI Engine later
        return SystemArchitecture(
            system_name="Inferred System",
            components=[],
            data_flows=[],
            dependencies=[],
            assumptions=[],
            unknowns=["Architecture needs reconstruction from slide data"]
        )
