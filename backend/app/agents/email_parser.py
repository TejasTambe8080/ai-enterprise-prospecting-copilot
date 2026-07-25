import re
from typing import Any, Dict, List
from email_validator import validate_email, EmailNotValidError

from app.agents.base_agent import BaseAgent
from app.integrations.gemini_client import GeminiClient

class EmailParserAgent(BaseAgent):
    """Agent for parsing and structuring inbound lead emails"""
    
    def __init__(self, gemini_client: GeminiClient):
        super().__init__("email_parser", gemini_client)
        
        self.prompt_template = """
        You are an expert lead parser for a B2B sales automation system. Parse the following email from a contact form submission.
        Extract structured information and determine the lead's intent with high accuracy.
        
        Email Content:
        {email_content}
        
        Extract the following fields and return as JSON:
        1. first_name: First name of the sender
        2. last_name: Last name of the sender
        3. email: Email address
        4. company: Company name
        5. company_domain: Domain from email or company website
        6. job_title: Job title/role
        7. phone: Phone number (if present)
        8. intent: Primary intent (Sales Inquiry, Support, Partnership, General, Other)
        9. urgency: How urgent is this request? (Low, Medium, High)
        10. message_summary: 1-2 sentence summary of the message
        11. key_topics: List of key topics mentioned
        12. confidence_score: How confident are you in this parsing? (0-100)
        
        Important Rules:
        - Only extract what's clearly present in the email
        - Do NOT hallucinate information
        - If a field is not found, use null
        - Extract company name from email signature or message context
        - Determine job title from email signature or context
        
        Return ONLY valid JSON, no additional text.
        """
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse email content and extract structured lead information"""
        
        email_content = input_data.get("email_content", "")
        if not email_content:
            raise ValueError("No email content provided")
        
        # Clean email content
        cleaned_content = self._clean_email(email_content)
        
        # Generate prompt
        prompt = self.generate_prompt(
            self.prompt_template,
            {"email_content": cleaned_content}
        )
        
        # Get AI response
        response = await self.gemini_client.generate_json(prompt)
        
        # Post-process response
        response = self._post_process(response)
        
        return response
    
    def _clean_email(self, content: str) -> str:
        """Clean and normalize email content"""
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove email signatures (basic patterns)
        signature_patterns = [
            r'--?\s*$',
            r'^Sent from my iPhone',
            r'^Get Outlook for',
            r'^Sent with',
            r'^Best regards,',
            r'^Regards,',
            r'^Thanks,',
            r'^Thank you,'
        ]
        for pattern in signature_patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE)
        
        # Remove quoted replies
        content = re.sub(r'^>.*$', '', content, flags=re.MULTILINE)
        
        return content.strip()
    
    def _post_process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Post-process parsed data"""
        
        # Validate email
        if data.get("email"):
            try:
                valid = validate_email(data["email"])
                data["email"] = valid.email
            except EmailNotValidError:
                data["email"] = None
        
        # Extract domain from email if not provided
        if data.get("email") and not data.get("company_domain"):
            match = re.search(r'@([\w.-]+)', data["email"])
            data["company_domain"] = match.group(1) if match else None
        
        # Clean company name
        if data.get("company"):
            data["company"] = data["company"].strip()
        
        # Ensure confidence score exists
        if "confidence_score" not in data:
            data["confidence_score"] = 70
        
        # Ensure key_topics exists
        if "key_topics" not in data or not data["key_topics"]:
            data["key_topics"] = []
        
        return data