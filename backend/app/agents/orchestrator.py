from typing import Dict, Any, List, Optional
import asyncio
from datetime import datetime
import logging

from app.agents.email_parser import EmailParserAgent
from app.agents.company_research import CompanyResearchAgent
from app.agents.industry_intel import IndustryIntelAgent
from app.agents.pain_point import PainPointAgent
from app.agents.decision_maker import DecisionMakerAgent
from app.agents.lead_scoring import LeadScoringAgent
from app.agents.case_study import CaseStudyAgent
from app.agents.email_generation import EmailGenerationAgent
from app.agents.linkedin import LinkedInAgent
from app.agents.quality_checker import QualityCheckerAgent
from app.agents.summary import SummaryAgent
from app.integrations.gemini_client import GeminiClient
from app.core.database import MongoDB
from app.models.lead import Lead

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orchestrates all AI agents in the pipeline"""
    
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.agents = self._initialize_agents()
        self.logger = logger
        self.processing_queue = []
    
    def _initialize_agents(self) -> Dict[str, Any]:
        """Initialize all specialized agents"""
        return {
            "email_parser": EmailParserAgent(self.gemini_client),
            "company_research": CompanyResearchAgent(self.gemini_client),
            "industry_intel": IndustryIntelAgent(self.gemini_client),
            "pain_point": PainPointAgent(self.gemini_client),
            "decision_maker": DecisionMakerAgent(self.gemini_client),
            "lead_scoring": LeadScoringAgent(self.gemini_client),
            "case_study": CaseStudyAgent(self.gemini_client),
            "email_generation": EmailGenerationAgent(self.gemini_client),
            "linkedin": LinkedInAgent(self.gemini_client),
            "quality_checker": QualityCheckerAgent(self.gemini_client),
            "summary": SummaryAgent(self.gemini_client)
        }
    
    async def process_lead(self, email_content: str, lead_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a lead through the entire agent pipeline"""
        
        self.logger.info(f"Starting lead processing pipeline for lead: {lead_id}")
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Parse email
            parsed_result = await self.agents["email_parser"].run(
                {"email_content": email_content}
            )
            
            if parsed_result["status"] == "error":
                return self._create_error_response(
                    f"Email parsing failed: {parsed_result.get('error', 'Unknown error')}",
                    lead_id
                )
            
            lead_data = parsed_result["data"]
            self.logger.info(f"Parsed lead: {lead_data.get('email')}")
            
            # Extract company info
            company_name = lead_data.get("company") or lead_data.get("company_name")
            domain = lead_data.get("company_domain") or lead_data.get("domain")
            
            # Step 2-5: Parallel processing for research
            research_tasks = [
                self.agents["company_research"].run(
                    {"company": company_name, "domain": domain}
                ),
                self.agents["industry_intel"].run(
                    {"company": company_name}
                ),
                self.agents["decision_maker"].run(
                    {"company": company_name}
                )
            ]
            
            research_results = await asyncio.gather(*research_tasks, return_exceptions=True)
            
            # Extract results
            company_research = research_results[0] if not isinstance(research_results[0], Exception) else {"status": "error", "data": {}}
            industry_intel = research_results[1] if not isinstance(research_results[1], Exception) else {"status": "error", "data": {}}
            decision_makers = research_results[2] if not isinstance(research_results[2], Exception) else {"status": "error", "data": {}}
            
            # Step 6: Identify pain points
            pain_points = await self.agents["pain_point"].run({
                "company_data": company_research.get("data", {}),
                "industry_data": industry_intel.get("data", {})
            })
            
            # Step 7: Score the lead
            scoring = await self.agents["lead_scoring"].run({
                "lead_data": lead_data,
                "company_data": company_research.get("data", {}),
                "pain_points": pain_points.get("data", {})
            })
            
            # Step 8: Match case study
            case_study = await self.agents["case_study"].run({
                "company_data": company_research.get("data", {}),
                "pain_points": pain_points.get("data", {}),
                "industry": industry_intel.get("data", {})
            })
            
            # Step 9: Generate emails
            emails = await self.agents["email_generation"].run({
                "lead": lead_data,
                "pain_points": pain_points.get("data", {}),
                "case_study": case_study.get("data", {}),
                "company": company_research.get("data", {})
            })
            
            # Step 10: Prepare LinkedIn
            linkedin = await self.agents["linkedin"].run({
                "lead": lead_data,
                "decision_makers": decision_makers.get("data", {})
            })
            
            # Step 11: Quality check
            quality = await self.agents["quality_checker"].run({
                "emails": emails.get("data", {}),
                "linkedin": linkedin.get("data", {}),
                "scoring": scoring.get("data", {})
            })
            
            # Step 12: Generate summary
            summary = await self.agents["summary"].run({
                "lead": lead_data,
                "company": company_research.get("data", {}),
                "scoring": scoring.get("data", {}),
                "pain_points": pain_points.get("data", {}),
                "case_study": case_study.get("data", {}),
                "emails": emails.get("data", {}),
                "quality": quality.get("data", {})
            })
            
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Combine all results
            final_result = {
                "status": "success",
                "lead": lead_data,
                "company_intelligence": company_research.get("data", {}),
                "industry_intelligence": industry_intel.get("data", {}),
                "pain_points": pain_points.get("data", {}),
                "decision_makers": decision_makers.get("data", {}),
                "meddpicc_scoring": scoring.get("data", {}),
                "case_study": case_study.get("data", {}),
                "email_drafts": emails.get("data", {}),
                "linkedin_message": linkedin.get("data", {}),
                "quality_check": quality.get("data", {}),
                "handoff_summary": summary.get("data", {}),
                "processing_time": processing_time,
                "agent_status": {
                    "email_parser": parsed_result["status"],
                    "company_research": company_research["status"],
                    "industry_intel": industry_intel["status"],
                    "pain_point": pain_points["status"],
                    "decision_maker": decision_makers["status"],
                    "lead_scoring": scoring["status"],
                    "case_study": case_study["status"],
                    "email_generation": emails["status"],
                    "linkedin": linkedin["status"],
                    "quality_checker": quality["status"],
                    "summary": summary["status"]
                }
            }
            
            # Save to database
            await self._save_lead_result(lead_id, final_result)
            
            self.logger.info(f"Lead processing completed in {processing_time:.2f}s")
            return final_result
            
        except Exception as e:
            self.logger.error(f"Lead processing failed: {str(e)}", exc_info=True)
            return self._create_error_response(str(e), lead_id)
    
    async def _save_lead_result(self, lead_id: Optional[str], result: Dict[str, Any]):
        """Save lead processing result to database"""
        if not lead_id:
            return
        
        try:
            db = await MongoDB.get_collection("leads")
            
            # Prepare update data
            update_data = {
                "company_data": result.get("company_intelligence", {}),
                "industry": result.get("industry_intelligence", {}).get("industry"),
                "meddpicc_score": result.get("meddpicc_scoring", {}),
                "pain_points": result.get("pain_points", {}).get("pain_points", []),
                "opportunities": result.get("pain_points", {}).get("opportunities", []),
                "personalized_emails": result.get("email_drafts", {}).get("emails", []),
                "linkedin_message": result.get("linkedin_message", {}),
                "matched_case_study": result.get("case_study", {}),
                "decision_makers": result.get("decision_makers", {}).get("decision_makers", []),
                "recommended_motion": result.get("meddpicc_scoring", {}).get("recommended_motion"),
                "motion_reasoning": result.get("meddpicc_scoring", {}).get("motion_reasoning"),
                "status": "qualified" if result.get("meddpicc_scoring", {}).get("total_score", 0) >= 60 else "pending",
                "processed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            await db.update_one(
                {"_id": lead_id},
                {"$set": update_data}
            )
            
            self.logger.info(f"Lead {lead_id} saved to database")
            
        except Exception as e:
            self.logger.error(f"Failed to save lead result: {str(e)}")
    
    def _create_error_response(self, error: str, lead_id: Optional[str] = None) -> Dict[str, Any]:
        """Create error response"""
        return {
            "status": "error",
            "message": error,
            "lead_id": lead_id,
            "timestamp": datetime.utcnow().isoformat()
        }