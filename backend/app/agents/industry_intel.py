from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class IndustryIntelAgent(BaseAgent):
    """Agent for analyzing industry trends and market intelligence"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("industry_intel", gemini_client)
        
        self.prompt_template = """
        You are an industry analyst. Analyze the following company and its industry.
        
        Company: {company_name}
        Industry: {industry}
        
        Provide comprehensive industry intelligence:
        1. Industry: Specific industry vertical
        2. Market Size: Estimated market size (USD)
        3. Growth Rate: Annual growth rate (%)
        4. Key Trends: 3-5 major trends in the industry
        5. Challenges: 3-5 major challenges
        6. Opportunities: 3-5 emerging opportunities
        7. Competitive Landscape: Description of competition
        8. Regulatory Environment: Key regulations affecting the industry
        9. Technology Adoption: Key technologies being adopted
        10. Industry Outlook: 1-2 sentence outlook
        
        Return as JSON.
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze industry intelligence"""
        
        company_name = input_data.get("company_name", "")
        industry = input_data.get("industry") or input_data.get("company_data", {}).get("industry")
        
        if not company_name:
            raise ValueError("Company name is required")
        
        prompt = self.generate_prompt(
            self.prompt_template,
            {
                "company_name": company_name,
                "industry": industry or "Technology"
            }
        )
        
        response = await self.gemini_client.generate_json(prompt)
        
        # Ensure required fields
        response["company"] = company_name
        response["timestamp"] = "2024-01-15T00:00:00Z"
        
        return response