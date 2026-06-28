from app.models.architecture import SystemArchitecture, CorrectedArchitecture, AgentReview
from app.services.ai_service import AIService
from typing import List

class CorrectionService:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def generate_corrected_architecture(
        self,
        original: SystemArchitecture,
        agent_reviews: List[AgentReview]
    ) -> CorrectedArchitecture:
        prompt = f"""
        As a Principal GCP Architect, generate a corrected, ideal cloud-native version of the following architecture.
        Address all findings identified by the review agents.

        Original Architecture:
        {original.model_dump_json(indent=2)}

        Agent Reviews:
        {[r.model_dump_json(indent=2) for r in agent_reviews]}

        Ensure you:
        - Replace legacy/wrong services with modern GCP services (Cloud Run, GKE, Pub/Sub, Spanner, etc.)
        - Add missing foundational elements (API Gateway, Load Balancers, Cloud Armor, etc.)
        - Fix all CRITICAL and HIGH severity issues.
        - Provide clear step-by-step migration_guidance from the original to this new architecture.
        - Output the result in the CorrectedArchitecture JSON format.

        JSON Schema:
        {CorrectedArchitecture.model_json_schema()}
        """

        return await self.ai_service.get_structured_completion(prompt, CorrectedArchitecture)
