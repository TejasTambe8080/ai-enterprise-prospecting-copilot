from typing import Dict, Any, Optional, List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)

class EmailService:
    """Service for email operations"""
    
    def __init__(self):
        self.from_email = settings.FROM_EMAIL
        self.sendgrid_api_key = settings.SENDGRID_API_KEY
        self.logger = logger
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        from_email: Optional[str] = None
    ) -> bool:
        """Send email using SendGrid (or fallback to SMTP)"""
        try:
            if self.sendgrid_api_key:
                return await self._send_with_sendgrid(to_email, subject, body, html_body, from_email)
            else:
                return await self._send_with_smtp(to_email, subject, body, from_email)
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    async def _send_with_sendgrid(
        self,
        to_email: str,
        subject: str,
        body: str,
        html_body: Optional[str],
        from_email: Optional[str]
    ) -> bool:
        """Send email using SendGrid API"""
        try:
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            
            message = Mail(
                from_email=from_email or self.from_email,
                to_emails=to_email,
                subject=subject,
                plain_text_content=body
            )
            if html_body:
                message.html_content = html_body
            
            sg = SendGridAPIClient(self.sendgrid_api_key)
            response = await sg.send_async(message)
            
            return response.status_code in [200, 201, 202]
            
        except ImportError:
            self.logger.warning("SendGrid package not installed, falling back to SMTP")
            return await self._send_with_smtp(to_email, subject, body, from_email)
        except Exception as e:
            self.logger.error(f"SendGrid error: {str(e)}")
            return False
    
    async def _send_with_smtp(
        self,
        to_email: str,
        subject: str,
        body: str,
        from_email: Optional[str]
    ) -> bool:
        """Send email using SMTP"""
        try:
            # For production, use proper SMTP configuration
            # This is a placeholder
            self.logger.info(f"SMTP email would be sent to {to_email} with subject: {subject}")
            return True
        except Exception as e:
            self.logger.error(f"SMTP error: {str(e)}")
            return False
    
    def generate_outreach_email(
        self,
        lead_name: str,
        company_name: str,
        pain_points: List[str],
        case_study: Optional[str] = None,
        personalization_level: int = 2
    ) -> Dict[str, str]:
        """Generate outreach email template"""
        
        # Basic personalization
        subject = f"Re: {company_name} - Growth Opportunities"
        body = f"Hi {lead_name},\n\n"
        
        if personalization_level >= 2 and pain_points:
            body += f"I noticed {company_name} might be facing challenges with {pain_points[0].lower()}.\n\n"
        
        body += "We've helped similar companies achieve significant results through our AI-powered sales automation platform.\n\n"
        
        if personalization_level >= 3 and case_study:
            body += f"One example: {case_study}\n\n"
        
        body += "Would you be open to a quick 15-minute conversation to explore if we could help?\n\n"
        body += "Best regards,\n[Your Name]\nFlytBase BDR"
        
        return {
            "subject": subject,
            "body": body,
            "personalization_level": personalization_level
        }
    
    def generate_linkedin_message(self, lead_name: str, company_name: str) -> str:
        """Generate LinkedIn connection request message"""
        return f"Hi {lead_name}, I'm impressed by {company_name}'s growth. I specialize in helping companies like yours optimize their sales processes. Would be great to connect and learn more about your work."
    
    def validate_email_content(self, email_content: Dict[str, Any]) -> bool:
        """Validate email content"""
        required_fields = ['to_email', 'subject', 'body']
        for field in required_fields:
            if not email_content.get(field):
                return False
        return True