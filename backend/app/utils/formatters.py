from typing import Dict, Any, Optional, List
from datetime import datetime
import re

def format_lead_data(lead: Dict[str, Any]) -> Dict[str, Any]:
    """Format lead data for display"""
    formatted = {
        "id": str(lead.get("_id", "")),
        "full_name": f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip(),
        "email": lead.get("email", ""),
        "company": lead.get("company_name", ""),
        "status": lead.get("status", "pending"),
        "score": lead.get("meddpicc_score", {}).get("total_score", 0),
        "created_at": format_datetime(lead.get("created_at")),
        "industry": lead.get("industry", "N/A"),
        "job_title": lead.get("job_title", "N/A"),
    }
    return formatted

def format_company_data(company: Dict[str, Any]) -> Dict[str, Any]:
    """Format company data for display"""
    formatted = {
        "name": company.get("company_name", company.get("name", "")),
        "domain": company.get("domain", ""),
        "industry": company.get("industry", "N/A"),
        "employee_count": company.get("employee_count", 0),
        "description": truncate_text(company.get("description", ""), 200),
        "funding_stage": company.get("funding_stage", "Unknown"),
        "total_funding": format_currency(company.get("total_funding")),
        "founded_year": company.get("founded_year"),
        "headquarters": company.get("headquarters", ""),
    }
    return formatted

def format_meddpicc_score(scoring: Dict[str, Any]) -> Dict[str, Any]:
    """Format MEDDPICC score for display"""
    if not scoring:
        return {}
    
    formatted = {
        "metrics": scoring.get("metrics", 0),
        "economic_buyer": scoring.get("economic_buyer", 0),
        "decision_criteria": scoring.get("decision_criteria", 0),
        "decision_process": scoring.get("decision_process", 0),
        "paper_process": scoring.get("paper_process", 0),
        "internal_champion": scoring.get("internal_champion", 0),
        "competition": scoring.get("competition", 0),
        "total_score": scoring.get("total_score", 0),
        "qualification": scoring.get("qualification", "Unknown"),
        "recommended_motion": scoring.get("recommended_motion", ""),
        "motion_reasoning": scoring.get("motion_reasoning", ""),
        "strengths": scoring.get("strengths", []),
        "risks": scoring.get("risks", []),
    }
    
    # Add score bars for visualization
    formatted["score_bars"] = {
        field: {
            "value": value,
            "percentage": f"{value}%",
            "color": get_score_color(value)
        }
        for field, value in formatted.items()
        if field in ['metrics', 'economic_buyer', 'decision_criteria', 
                    'decision_process', 'paper_process', 'internal_champion', 'competition']
    }
    
    return formatted

def format_handoff_summary(summary: Dict[str, Any]) -> Dict[str, Any]:
    """Format handoff summary for AE"""
    formatted = {
        "executive_summary": summary.get("executive_summary", ""),
        "company_overview": summary.get("company_overview", ""),
        "key_pain_points": summary.get("key_pain_points", []),
        "opportunities": summary.get("opportunities", []),
        "meddpicc_summary": summary.get("meddpicc_summary", {}),
        "recommended_motion": summary.get("recommended_motion", ""),
        "decision_makers": summary.get("decision_makers", []),
        "next_steps": summary.get("next_steps", []),
        "value_proposition": summary.get("value_proposition", ""),
        "timeline_urgency": summary.get("timeline_urgency", ""),
        "generated_at": datetime.utcnow().isoformat(),
    }
    return formatted

def format_datetime(dt: Optional[datetime]) -> str:
    """Format datetime for display"""
    if not dt:
        return "N/A"
    if isinstance(dt, str):
        try:
            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
        except:
            return dt
    return dt.strftime("%b %d, %Y %I:%M %p")

def format_currency(amount: Optional[float]) -> str:
    """Format currency amount"""
    if not amount:
        return "N/A"
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    if amount >= 1_000:
        return f"${amount / 1_000:.1f}K"
    return f"${amount:.0f}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + suffix

def to_slug(text: str) -> str:
    """Convert text to URL-friendly slug"""
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace spaces with hyphens
    text = re.sub(r'[\s-]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text

def get_score_color(score: int) -> str:
    """Get color based on score value"""
    if score >= 80:
        return "success"
    elif score >= 60:
        return "warning"
    elif score >= 40:
        return "info"
    else:
        return "error"

def format_email_template(template: str, context: Dict[str, Any]) -> str:
    """Format email template with context"""
    try:
        return template.format(**context)
    except KeyError as e:
        # Handle missing keys gracefully
        return template

def extract_domain_from_email(email: str) -> Optional[str]:
    """Extract domain from email address"""
    match = re.search(r'@([\w.-]+)', email)
    return match.group(1) if match else None

def parse_company_from_email(domain: str) -> Optional[str]:
    """Parse company name from email domain"""
    if not domain:
        return None
    # Remove TLD and common prefixes
    parts = domain.split('.')
    if len(parts) >= 2:
        # Remove common prefixes like www, mail, etc.
        name = parts[-2] if len(parts) >= 2 else parts[0]
        # Capitalize first letter
        return name.title()
    return None