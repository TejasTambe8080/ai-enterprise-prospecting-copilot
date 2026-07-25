from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class QualityCheckerAgent(BaseAgent):
    """Agent for quality checking all outputs"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("quality_checker", gemini_client)
        
        self.prompt_template = """
        You are a quality assurance expert. Review the following outputs for quality.
        
        Emails: {emails}
        LinkedIn Message: {linkedin}
        Scoring: {scoring}
        
        Check for:
        1. Hallucinations (false information)
        2. Grammar and spelling
        3. Personalization quality (0-100)
        4. Relevance to lead context
        5. Professional tone
        
        Return as JSON:
        {{
            "hallucination_detected": false,
            "hallucination_details": "",
            "grammar_score": 0-100,
            "personalization_score": 0-100,
            "relevance_score": 0-100,
            "tone_score": 0-100,
            "overall_quality": 0-100,
            "issues": [],
            "suggestions": []
        }}
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Check quality of all outputs"""
        
        emails = input_data.get("emails", {})
        linkedin = input_data.get("linkedin", {})
        scoring = input_data.get("scoring", {})
        
        prompt = self.generate_prompt(
            self.prompt_template,
            {
                "emails": str(emails.get("emails", [])),
                "linkedin": str(linkedin),
                "scoring": str(scoring)
            }
        )
        
        response = await self.gemini_client.generate_json(prompt)
        
        # Ensure all fields exist
        defaults = {
            "hallucination_detected": False,
            "hallucination_details": "",
            "grammar_score": 80,
            "personalization_score": 80,
            "relevance_score": 80,
            "tone_score": 80,
            "overall_quality": 80,
            "issues": [],
            "suggestions": []
        }
        
        for key, default in defaults.items():
            if key not in response:
                response[key] = default
        
        return response