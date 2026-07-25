from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class DecisionMakerAgent(BaseAgent):
    """Agent for identifying key decision makers"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("decision_maker", gemini_client)
        
        self.prompt_template = """
        You are an executive researcher. Identify the key decision makers at the following company.
        
        Company: {company_name}
        Industry: {industry}
        Employee Count: {employee_count}
        
        Based on typical organizational structures in this industry, identify:
        1. C-Level Executives (CEO, CRO, CMO, CTO, etc.)
        2. VP-Level Leaders (VP of Sales, VP of Marketing, etc.)
        3. Director-Level Decision Makers
        
        For each decision maker, provide:
        - Full Name (if known) or Title
        - Role/Title
        - Likely Responsibilities
        - Decision-Making Authority (High/Medium/Low)
        - LinkedIn URL (if available)
        
        Return as JSON with structure:
        {{
            "decision_makers": [
                {{
                    "title": "",
                    "responsibilities": "",
                    "decision_authority": "",
                    "linkedin": ""
                }}
            ]
        }}
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify decision makers"""
        
        company = input_data.get("company")
        company_data = input_data.get("company_data", {})
        
        if not company:
            raise ValueError("Company name is required")
        
        prompt = self.generate_prompt(
            self.prompt_template,
            {
                "company_name": company,
                "industry": company_data.get("industry", "Technology"),
                "employee_count": company_data.get("employee_count", "Unknown")
            }
        )
        
        response = await self.gemini_client.generate_json(prompt)
        
        # Ensure required fields
        response["company"] = company
        response["decision_makers"] = response.get("decision_makers", [])
        
        return response