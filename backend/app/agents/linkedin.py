from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class LinkedInAgent(BaseAgent):
    """Agent for preparing LinkedIn outreach"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("linkedin", gemini_client)
        
        self.prompt_template = """
        You are a BDR preparing LinkedIn outreach.
        
        Lead: {first_name} {last_name}
        Company: {company_name}
        Role: {job_title}
        
        Create:
        1. LinkedIn Connection Request (300 characters max)
        2. LinkedIn Follow-up Message (2-3 sentences)
        3. LinkedIn InMail (3-4 sentences)
        
        Return as JSON:
        {{
            "connection_request": "",
            "follow_up_message": "",
            "inmail": ""
        }}
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate LinkedIn outreach content"""
        
        lead = input_data.get("lead", {})
        decision_makers = input_data.get("decision_makers", {})
        
        prompt = self.generate_prompt(
            self.prompt_template,
            {
                "first_name": lead.get("first_name", "There"),
                "last_name": lead.get("last_name", ""),
                "company_name": lead.get("company", ""),
                "job_title": lead.get("job_title", "professional")
            }
        )
        
        response = await self.gemini_client.generate_json(prompt)
        
        return response