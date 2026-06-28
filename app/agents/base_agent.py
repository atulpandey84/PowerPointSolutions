from typing import List
from app.models.architecture import AgentReview, SystemArchitecture, Finding, Category, Severity
from app.services.ai_service import AIService

class BaseAgent:
    def __init__(self, ai_service: AIService, name: str, category: Category):
        self.ai_service = ai_service
        self.name = name
        self.category = category

    async def review(self, architecture: SystemArchitecture) -> AgentReview:
        prompt = self._build_prompt(architecture)
        return await self.ai_service.get_structured_completion(prompt, AgentReview)

    def _build_prompt(self, architecture: SystemArchitecture) -> str:
        return f"""
        As a Principal Cloud Architect, review the following system architecture for {self.category.value} issues.

        System Architecture:
        {architecture.model_dump_json(indent=2)}

        Provide your findings in a structured JSON format matching the AgentReview model.
        Include severity (CRITICAL, HIGH, MEDIUM, LOW), title, description, and recommendation for each finding.
        """

class SecurityAgent(BaseAgent):
    def __init__(self, ai_service: AIService):
        super().__init__(ai_service, "Security Agent", Category.SECURITY)

class ScalabilityAgent(BaseAgent):
    def __init__(self, ai_service: AIService):
        super().__init__(ai_service, "Scalability Agent", Category.SCALABILITY)

class ReliabilityAgent(BaseAgent):
    def __init__(self, ai_service: AIService):
        super().__init__(ai_service, "Reliability Agent", Category.RELIABILITY)

class GCPBestPracticesAgent(BaseAgent):
    def __init__(self, ai_service: AIService):
        super().__init__(ai_service, "GCP Best Practices Agent", Category.GCP_BEST_PRACTICES)

class FinOpsAgent(BaseAgent):
    def __init__(self, ai_service: AIService):
        super().__init__(ai_service, "FinOps Agent", Category.FINOPS)
