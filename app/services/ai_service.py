import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from pydantic import BaseModel

class AIService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-1106-preview")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    async def get_structured_completion(self, prompt: str, response_model: type[BaseModel]) -> Any:
        if not self.client:
            # Mock or alternative for when no API key is provided
            return self._generate_mock_response(response_model)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return response_model.model_validate_json(response.choices[0].message.content)

    def _generate_mock_response(self, response_model: type[BaseModel]) -> Any:
        # Simplified mock for development that returns valid objects
        # This prevents crashes when iterating over list fields
        if hasattr(response_model, "model_json_schema"):
            # A more robust way to get a default object for pydantic models
            try:
                return response_model()
            except Exception:
                # If required fields exist without defaults
                return response_model.model_construct()
        return response_model.model_construct()
