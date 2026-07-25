from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class SummaryAgent(BaseAgent):
    """Agent for generating AE handoff summary"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("summary", gemini_client)
        
        self.prompt_template = """
        You are a sales operations expert creating a handoff summary for an Account Executive.
        
        Lead: {lead_info}
        Company: {company_info}
        Scoring: {scoring_info}
        Pain Points: {pain_points}
        Case Study: {case_study}
        Emails: {emails}
        Quality: {quality}
        
        Create a comprehensive summary with:
        1. Executive Summary (2-3 sentences)
        2. Company Overview (industry, size, funding)
        3. Key Pain Points and Opportunities
        4. MEDDPICC Score Summary
        5. Recommended GTM Motion
        6. Key Decision Makers
        7. Next Steps (3-5 actions)
        8. Competitors and Market Position
        9. Value Proposition (How FlytBase can help)
        10. Timeline and Urgency
        
        Format as a professional handoff document.
        Return as JSON with structured sections.
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AE handoff summary"""
        
        lead = input_data.get("lead", {})
        company = input_data.get("company", {})
        scoring = input_data.get("scoring", {})
        pain_points = input_data.get("pain_points", {})
        case_study = input_data.get("case_study", {})
        emails = input_data.get("emails", {})
        quality = input_data.get("quality", {})
        
        prompt = self.generate_prompt(
            self.prompt_template,
            {
                "lead_info": f"{lead.get('first_name', '')} {lead.get('last_name', '')} - {lead.get('job_title', 'Unknown')}",
                "company_info": f"{company.get('company_name', 'Unknown')} - {company.get('industry', 'Unknown')} - {company.get('employee_count', 'Unknown')} employees",
                "scoring_info": f"Score: {scoring.get('total_score', 0)}/100 - {scoring.get('qualification', 'Unknown')}",
                "pain_points": ", ".join(pain_points.get("pain_points", [])[:3]),
                "case_study": case_study.get("title", "No case study matched"),
                "emails": ", ".join([e.get("subject", "") for e in emails.get("emails", [])[:2]]),
                "quality": f"Quality Score: {quality.get('overall_quality', 0)}/100"
            }
        )
        
        response = await self.gemini_client.generate_json(prompt)
        
        # Ensure minimum structure
        if not response:
            response = {
                "executive_summary": "Lead qualified for FlytBase solution.",
                "company_overview": "Company in technology sector.",
                "key_insights": ["Qualified lead with clear pain points"],
                "recommended_actions": ["Schedule discovery call"]
            }
        
        return response