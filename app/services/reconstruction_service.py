from app.models.architecture import SystemArchitecture
from app.services.ai_service import AIService

class ReconstructionService:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def reconstruct(self, slides_data: list) -> SystemArchitecture:
        prompt = f"""
        Analyze the following text extracted from a PowerPoint architecture document and reconstruct the system architecture into a structured JSON graph format.

        Slides Data:
        {slides_data}

        Identify:
        - Components (name, type, description)
        - Data flows (source, target, protocol)
        - Dependencies
        - Assumptions
        - Unknowns

        Output must strictly follow the SystemArchitecture JSON schema.
        """
        return await self.ai_service.get_structured_completion(prompt, SystemArchitecture)
