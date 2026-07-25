import re
from typing import Any, Dict, List
import httpx
from bs4 import BeautifulSoup

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient
from app.config.settings import settings

class CompanyResearchAgent(BaseAgent):
    """Agent for researching companies using public data"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("company_research", gemini_client)
        
        self.prompt_template = """
        You are a business intelligence expert. Research and analyze the following company.
        
        Company Name: {company_name}
        Domain: {domain}
        
        Based on available information, provide:
        1. Company Description (2-3 sentences)
        2. Industry (specific industry vertical)
        3. Employee Count (estimate if not available)
        4. Year Founded (if known)
        5. Funding Stage (Bootstrapped, Seed, Series A, B, C, D, IPO)
        6. Total Funding Amount (in USD)
        7. Key Executives (CEO, CTO, etc.)
        8. Main Competitors (3-5 companies)
        9. Technology Stack (if known)
        10. Trust Signals (awards, certifications, partnerships)
        
        Return as JSON.
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Research company using multiple sources"""
        
        company = input_data.get("company")
        domain = input_data.get("domain")
        
        if not company and not domain:
            raise ValueError("Either company name or domain is required")
        
        # Try to gather data from public sources
        research_data = {}
        
        # If domain is provided, scrape website
        if domain:
            website_data = await self._scrape_website(domain)
            research_data.update(website_data)
        
        # Use Gemini to enrich and structure data
        if not research_data.get("description"):
            prompt = self.generate_prompt(
                self.prompt_template,
                {
                    "company_name": company or domain,
                    "domain": domain or ""
                }
            )
            
            structured_data = await self.gemini_client.generate_json(prompt)
            research_data.update(structured_data)
        
        # Combine and format
        return self._format_research(research_data)
    
    async def _scrape_website(self, domain: str) -> Dict[str, Any]:
        """Scrape company website for information"""
        data = {}
        
        try:
            # Ensure domain has protocol
            if not domain.startswith(('http://', 'https://')):
                domain = f'https://{domain}'
            
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(domain, follow_redirects=True)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Get title and meta description
                title = soup.find('title')
                if title:
                    data['title'] = title.get_text().strip()
                
                description = soup.find('meta', attrs={'name': 'description'})
                if description:
                    data['description'] = description.get('content', '').strip()
                
                # Look for company name in headers
                h1 = soup.find('h1')
                if h1:
                    data['h1'] = h1.get_text().strip()
                
                # Extract potential employee count from text
                text = soup.get_text()
                employee_patterns = [
                    r'(\d+)\+?\s*employees',
                    r'(\d+)\s*people',
                    r'team of (\d+)'
                ]
                for pattern in employee_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match:
                        data['employee_count'] = int(match.group(1))
                        break
                
        except Exception as e:
            self.logger.warning(f"Failed to scrape website {domain}: {str(e)}")
        
        return data
    
    def _format_research(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Format research data into standardized structure"""
        
        # Map fields to standard names
        formatted = {
            "company_name": data.get("company_name") or data.get("title", ""),
            "description": data.get("description") or data.get("h1", ""),
            "industry": data.get("industry", "Technology"),
            "employee_count": data.get("employee_count", 0),
            "founded_year": data.get("founded_year"),
            "funding_stage": data.get("funding_stage", "Unknown"),
            "total_funding": data.get("total_funding"),
            "executives": data.get("executives", []),
            "competitors": data.get("competitors", []),
            "tech_stack": data.get("tech_stack", []),
            "trust_signals": data.get("trust_signals", []),
            "domain": data.get("domain", ""),
            "source": "web_ai_combined"
        }
        
        # Clean and validate
        if not formatted["employee_count"]:
            formatted["employee_count"] = 0
        
        return formatted