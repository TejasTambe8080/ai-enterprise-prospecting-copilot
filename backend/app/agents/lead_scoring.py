from typing import Any, Dict, List

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient
from app.models.lead import MEDDPICCScore

class LeadScoringAgent(BaseAgent):
    """Agent for scoring leads using MEDDPICC framework"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("lead_scoring", gemini_client)
        
        self.prompt_template = """
        You are a senior sales director using the MEDDPICC framework to qualify leads.
        
        Lead Information:
        - Name: {first_name} {last_name}
        - Company: {company_name}
        - Industry: {industry}
        - Role: {job_title}
        - Employee Count: {employee_count}
        - Funding Stage: {funding_stage}
        
        Pain Points: {pain_points}
        
        Score each MEDDPICC dimension (0-100):
        
        1. Metrics (20% weight): Can the customer measure the impact?
           - 80-100: Clear measurable business impact
           - 50-79: Some measurable impact
           - 0-49: Unclear or no measurable impact
        
        2. Economic Buyer (15% weight): Access to decision maker?
           - 80-100: Direct access to economic buyer
           - 50-79: Access to influencer
           - 0-49: No access
        
        3. Decision Criteria (15% weight): Solution alignment?
           - 80-100: Perfect fit for needs
           - 50-79: Good fit
           - 0-49: Poor fit
        
        4. Decision Process (15% weight): Clear timeline?
           - 80-100: Clear process and timeline
           - 50-79: Some process
           - 0-49: No clear process
        
        5. Paper Process (10% weight): Procurement ease?
           - 80-100: Easy procurement
           - 50-79: Moderate complexity
           - 0-49: Complex procurement
        
        6. Internal Champion (15% weight): Advocate exists?
           - 80-100: Strong champion
           - 50-79: Some support
           - 0-49: No champion
        
        7. Competition (10% weight): Competitive position?
           - 80-100: Strong competitive position
           - 50-79: Moderate competition
           - 0-49: Weak competitive position
        
        Also provide:
        1. Recommended GTM Motion (direct_ae, partner_led, sdr_led)
        2. Motion Reasoning
        3. Key Strengths (top 3)
        4. Key Risks (top 3)
        
        Return as JSON with fields: metrics, economic_buyer, decision_criteria, decision_process, paper_process, internal_champion, competition, recommended_motion, motion_reasoning, strengths, risks
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Score lead using MEDDPICC framework"""
        
        lead_data = input_data.get("lead_data", {})
        company_data = input_data.get("company_data", {})
        pain_points = input_data.get("pain_points", {})
        
        prompt = self.generate_prompt(
            self.prompt_template,
            {
                "first_name": lead_data.get("first_name", ""),
                "last_name": lead_data.get("last_name", ""),
                "company_name": lead_data.get("company", "") or company_data.get("company_name", ""),
                "industry": company_data.get("industry", "Technology"),
                "job_title": lead_data.get("job_title", "Unknown"),
                "employee_count": company_data.get("employee_count", "Unknown"),
                "funding_stage": company_data.get("funding_stage", "Unknown"),
                "pain_points": ", ".join(pain_points.get("pain_points", [])[:3])
            }
        )
        
        response = await self.gemini_client.generate_json(prompt)
        
        # Create MEDDPICCScore object
        score = MEDDPICCScore(
            metrics=response.get("metrics", 50),
            economic_buyer=response.get("economic_buyer", 50),
            decision_criteria=response.get("decision_criteria", 50),
            decision_process=response.get("decision_process", 50),
            paper_process=response.get("paper_process", 50),
            internal_champion=response.get("internal_champion", 50),
            competition=response.get("competition", 50)
        )
        
        # Add additional data
        response["total_score"] = score.total_score
        response["qualification"] = score.qualification
        response["recommended_motion"] = response.get("recommended_motion", "sdr_led")
        response["motion_reasoning"] = response.get("motion_reasoning", "")
        response["strengths"] = response.get("strengths", [])
        response["risks"] = response.get("risks", [])
        
        return response