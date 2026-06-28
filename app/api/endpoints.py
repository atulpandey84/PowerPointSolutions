from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Any
from app.parsers.pptx_parser import PPTXParser
from app.utils.ocr import OCRService
from app.services.ai_service import AIService
from app.services.reconstruction_service import ReconstructionService
from app.agents import (
    SecurityAgent, ScalabilityAgent, ReliabilityAgent,
    GCPBestPracticesAgent, FinOpsAgent
)
from app.services.synthesis_service import SynthesisService
from app.services.correction_service import CorrectionService
from app.diagrams.generator import DiagramGenerator
from app.models.architecture import AnalysisResult

router = APIRouter()

# Initialize services (In a real app, use dependency injection)
ocr_service = OCRService()
pptx_parser = PPTXParser(ocr_service=ocr_service)
ai_service = AIService()
reconstruction_service = ReconstructionService(ai_service=ai_service)
synthesis_service = SynthesisService()
correction_service = CorrectionService(ai_service=ai_service)
diagram_generator = DiagramGenerator()

agents = [
    SecurityAgent(ai_service),
    ScalabilityAgent(ai_service),
    ReliabilityAgent(ai_service),
    GCPBestPracticesAgent(ai_service),
    FinOpsAgent(ai_service)
]

@router.post("/analyze", response_model=AnalysisResult)
async def analyze_architecture(file: UploadFile = File(...)):
    if not file.filename.endswith(".pptx"):
        raise HTTPException(status_code=400, detail="Only .pptx files are supported.")

    content = await file.read()

    # 1. Parse PPTX
    slides_data = pptx_parser.parse(content)

    # 2. Reconstruct Architecture
    original_arch = await reconstruction_service.reconstruct(slides_data)

    # 3. Run Agents
    agent_reviews = []
    for agent in agents:
        review = await agent.review(original_arch)
        agent_reviews.append(review)

    # 4. Synthesize
    synthesis_data = synthesis_service.synthesize(agent_reviews)

    # 5. Correct
    corrected_arch = await correction_service.generate_corrected_architecture(
        original_arch, agent_reviews
    )

    # 6. Generate Diagrams
    mermaid = diagram_generator.generate_mermaid(corrected_arch)
    graph_model = diagram_generator.generate_graph_model(corrected_arch)

    return AnalysisResult(
        original_architecture=original_arch,
        agent_reviews=agent_reviews,
        synthesis_report=synthesis_data["summary"],
        scores=synthesis_data["scores"],
        corrected_architecture=corrected_arch,
        mermaid_diagram=mermaid,
        graph_model=graph_model
    )
