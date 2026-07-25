from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class EmailGenerationAgent(BaseAgent):
    """Agent for generating personalized email drafts"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("email_generation", gemini_client)
        
        self.prompt_template = """
        You are a senior BDR writing personalized outreach emails.
        
        Lead: {first_name} {last_name}
        Company: {company_name}
        Role: {job_title}
        Industry: {industry}
        
        Pain Points: {pain_points}
        Case Study: {case_study_title}
        
        Generate 3 email drafts with different personalization levels:
        
        Level 1 (Basic): Personalized with name and company
        Level 2 (Medium): Adds pain point reference
        Level 3 (High): Adds case study + specific insight
        
        For each email:
        - Subject Line (attention-grabbing)
        - Body (2-3 paragraphs)
        - Call to Action (clear next step)
        
        Tone: Professional, consultative, value-focused
        Style: Conversational but business-appropriate
        
        Return as JSON with structure:
        {{
            "emails": [
                {{"level": 1, "subject": "", "body": "", "cta": ""}},
                {{"level": 2, "subject": "", "body": "", "cta": ""}},
                {{"level": 3, "subject": "", "body": "", "cta": ""}}
            ]
        }}
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized email drafts"""
        
        lead = input_data.get("lead", {})
        pain_points = input_data.get("pain_points", {})
        case_study = input_data.get("case_study", {})
        company = input_data.get("company", {})
        
        prompt = self.generate_prompt(
            self.prompt_template,
            {
                "first_name": lead.get("first_name", "There"),
                "last_name": lead.get("last_name", ""),
                "company_name": lead.get("company", "") or company.get("company_name", ""),
                "job_title": lead.get("job_title", ""),
                "industry": company.get("industry", "Technology"),
                "pain_points": ", ".join(pain_points.get("pain_points", [])[:3]),
                "case_study_title": case_study.get("title", "our recent success")
            }
        )
        
        response = await self.gemini_client.generate_json(prompt)
        
        # Ensure emails field exists
        if "emails" not in response:
            response["emails"] = []
        
        return response