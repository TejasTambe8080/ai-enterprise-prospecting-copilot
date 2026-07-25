from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class PainPointAgent(BaseAgent):
    """Agent for identifying pain points and opportunities"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("pain_point", gemini_client)
        
        self.prompt_template = """
        You are a sales expert specializing in B2B sales technology. Analyze the following company and identify their likely pain points and opportunities.
        
        Company: {company_name}
        Industry: {industry}
        Employee Count: {employee_count}
        Description: {description}
        
        Identify:
        1. Pain Points: Top 3-5 business challenges they likely face
        2. Opportunities: Top 3-5 opportunities for growth or improvement
        3. Sales Enablement Needs: Specific needs related to sales operations
        4. Technology Gaps: Missing or inadequate technology solutions
        5. Competitive Pressures: Key competitive challenges
        
        For each pain point, provide:
        - Description of the pain
        - Impact on business
        - How FlytBase could help
        
        Return as JSON with the following structure:
        {{
            "pain_points": [{{"description": "", "impact": "", "flytbase_solution": ""}}],
            "opportunities": [{{"description": "", "potential": ""}}],
            "sales_enablement_needs": [],
            "technology_gaps": [],
            "competitive_pressures": []
        }}
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify pain points and opportunities"""
        
        company_data = input_data.get("company_data", {})
        industry_data = input_data.get("industry_data", {})
        
        prompt = self.generate_prompt(
            self.prompt_template,
            {
                "company_name": company_data.get("company_name", "Unknown"),
                "industry": industry_data.get("industry", company_data.get("industry", "Technology")),
                "employee_count": company_data.get("employee_count", "Unknown"),
                "description": company_data.get("description", "No description available")
            }
        )
        
        response = await self.gemini_client.generate_json(prompt)
        
        # Ensure required fields
        response["pain_points"] = response.get("pain_points", [])
        response["opportunities"] = response.get("opportunities", [])
        
        return response