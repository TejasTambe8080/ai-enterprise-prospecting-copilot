from typing import Dict, Any, Optional, List
import httpx
from bs4 import BeautifulSoup
import re

from app.core.logging import get_logger
from app.integrations.gemini_client import GeminiClient

logger = get_logger(__name__)

class ResearchService:
    """Service for company research operations"""
    
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.logger = logger
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    async def research_company(self, company_name: str, domain: Optional[str] = None) -> Dict[str, Any]:
        """Research a company using multiple sources"""
        try:
            research_data = {
                "company_name": company_name,
                "domain": domain
            }
            
            # Scrape website if domain provided
            if domain:
                website_data = await self._scrape_website(domain)
                research_data.update(website_data)
            
            # Use Gemini to enrich
            enriched_data = await self._enrich_with_ai(company_name, research_data)
            research_data.update(enriched_data)
            
            # Get news
            news_data = await self._get_company_news(company_name)
            research_data["recent_news"] = news_data
            
            # Get competitors
            competitors = await self._get_competitors(company_name)
            research_data["competitors"] = competitors
            
            return research_data
            
        except Exception as e:
            self.logger.error(f"Failed to research company: {str(e)}")
            return {
                "company_name": company_name,
                "domain": domain,
                "error": str(e)
            }
    
    async def _scrape_website(self, domain: str) -> Dict[str, Any]:
        """Scrape company website for information"""
        data = {}
        try:
            if not domain.startswith(('http://', 'https://')):
                domain = f'https://{domain}'
            
            response = await self.http_client.get(domain, follow_redirects=True)
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
            headers = soup.find_all(['h1', 'h2'])
            for header in headers:
                if header.get_text().strip():
                    data['h1'] = header.get_text().strip()
                    break
            
            # Extract employee count
            text = soup.get_text()
            employee_patterns = [
                r'(\d+)\+?\s*employees',
                r'(\d+)\s*people',
                r'team of (\d+)',
                r'(\d+)\+?\s*staff'
            ]
            for pattern in employee_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    data['employee_count'] = int(match.group(1))
                    break
            
            # Find social links
            social_links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                if any(social in href.lower() for social in ['linkedin', 'twitter', 'facebook']):
                    social_links.append(href)
            if social_links:
                data['social_links'] = social_links
            
        except Exception as e:
            self.logger.warning(f"Failed to scrape website {domain}: {str(e)}")
        
        return data
    
    async def _enrich_with_ai(self, company_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich company data using AI"""
        prompt = f"""
        You are a business intelligence expert. Enrich the following company data:
        
        Company: {company_name}
        Current Data: {data}
        
        Provide additional insights:
        1. Industry classification (specific sub-industry)
        2. Estimated revenue range
        3. Key products/services
        4. Target market
        5. Competitive advantages
        6. Recent developments
        
        Return as JSON.
        """
        
        try:
            result = await self.gemini_client.generate_json(prompt)
            return result
        except Exception as e:
            self.logger.error(f"AI enrichment failed: {str(e)}")
            return {}
    
    async def _get_company_news(self, company_name: str) -> List[Dict[str, Any]]:
        """Get recent news about the company"""
        # In production, use News API
        # For now, return sample news
        return [
            {
                "title": f"{company_name} Announces New Product Launch",
                "date": "2024-01-15",
                "source": "TechCrunch",
                "summary": "Company announced a new product line targeting enterprise customers."
            }
        ]
    
    async def _get_competitors(self, company_name: str) -> List[str]:
        """Get main competitors"""
        prompt = f"""
        Identify the top 5 competitors for {company_name}.
        Return as a list of company names.
        """
        
        try:
            result = await self.gemini_client.generate_json(prompt)
            if isinstance(result, list):
                return result[:5]
            return []
        except Exception as e:
            self.logger.error(f"Failed to get competitors: {str(e)}")
            return []
    
    async def close(self):
        """Close HTTP client"""
        await self.http_client.aclose()