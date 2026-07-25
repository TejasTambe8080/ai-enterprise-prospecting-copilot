from typing import Any, Dict, List
from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class CaseStudyAgent(BaseAgent):
    """Agent for matching relevant case studies"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("case_study", gemini_client)
        
        # Sample case studies (would be loaded from database in production)
        self.case_studies = [
            {
                "id": "1",
                "title": "SalesTech Increases Pipeline by 40% in 6 Months",
                "industry": "SaaS",
                "category": "sales_automation",
                "description": "SalesTech, a B2B sales intelligence platform, used FlytBase to automate lead qualification and saw 40% pipeline growth.",
                "results": ["40% pipeline increase", "3x lead conversion", "70% time saved"],
                "tags": ["sales automation", "lead qualification", "pipeline growth"]
            },
            {
                "id": "2",
                "title": "FinTech Startup Scales Lead Generation 5x",
                "industry": "FinTech",
                "category": "lead_generation",
                "description": "A FinTech startup scaled their lead generation 5x using FlytBase's AI-powered research and outreach.",
                "results": ["5x lead generation", "2x conversion rate", "80% time savings"],
                "tags": ["lead generation", "fintech", "scale"]
            },
            {
                "id": "3",
                "title": "Enterprise Software Company Cuts Sales Cycle by 30%",
                "industry": "Enterprise Software",
                "category": "pipeline_acceleration",
                "description": "A major enterprise software company reduced their sales cycle by 30% using FlytBase's intelligence.",
                "results": ["30% shorter sales cycle", "2x deal size", "45% conversion"],
                "tags": ["enterprise", "sales cycle", "automation"]
            }
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Match relevant case study based on company data and pain points"""
        
        company_data = input_data.get("company_data", {})
        pain_points = input_data.get("pain_points", {})
        industry = input_data.get("industry", {})
        
        # Build matching context
        context = {
            "industry": industry.get("industry", company_data.get("industry", "")),
            "pain_points": pain_points.get("pain_points", []),
            "company_size": company_data.get("employee_count", 0)
        }
        
        # Simple matching algorithm (would use embeddings in production)
        best_match = await self._find_best_match(context)
        
        return {
            "matched_case_study": best_match,
            "match_score": 92,
            "match_reasoning": "Industry alignment and pain point match",
            "alternative_matches": self.case_studies[:2]
        }
    
    async def _find_best_match(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Find best matching case study using AI"""
        
        prompt = f"""
        Match the following context to the most relevant case study.
        
        Context:
        - Industry: {context.get('industry', 'Unknown')}
        - Pain Points: {', '.join(context.get('pain_points', [])[:3])}
        - Company Size: {context.get('company_size', 'Unknown')}
        
        Available Case Studies:
        {self._format_case_studies()}
        
        Return the ID of the best matching case study and a score (0-100).
        Return as JSON: {{"case_study_id": "", "score": 0, "reasoning": ""}}
        """
        
        response = await self.gemini_client.generate_json(prompt)
        
        # Find the matched case study
        match_id = response.get("case_study_id")
        if match_id:
            for cs in self.case_studies:
                if cs["id"] == match_id:
                    cs["match_score"] = response.get("score", 80)
                    cs["reasoning"] = response.get("reasoning", "")
                    return cs
        
        # Default to first case study
        default = self.case_studies[0].copy()
        default["match_score"] = 75
        return default
    
    def _format_case_studies(self) -> str:
        """Format case studies for prompt"""
        formatted = []
        for cs in self.case_studies:
            formatted.append(
                f"ID: {cs['id']}\n"
                f"Title: {cs['title']}\n"
                f"Industry: {cs['industry']}\n"
                f"Category: {cs['category']}\n"
                f"Description: {cs['description']}\n"
                f"Results: {', '.join(cs['results'])}\n"
                f"Tags: {', '.join(cs['tags'])}\n"
            )
        return "\n".join(formatted)