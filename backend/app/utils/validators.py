import re
from typing import Optional, Any
from email_validator import validate_email as validate_email_lib, EmailNotValidError

def validate_email(email: str) -> bool:
    """Validate email address format"""
    try:
        validate_email_lib(email)
        return True
    except EmailNotValidError:
        return False

def validate_phone(phone: str) -> bool:
    """Validate phone number format"""
    # Remove common formatting characters
    cleaned = re.sub(r'[\s\-\(\)\+\.]', '', phone)
    # Check if it's a valid phone number (basic check)
    return len(cleaned) >= 10 and len(cleaned) <= 15 and cleaned.isdigit()

def validate_company_name(name: str) -> bool:
    """Validate company name"""
    if not name or len(name) < 2:
        return False
    # Company name should not be just special characters
    cleaned = re.sub(r'[^a-zA-Z0-9\s\-\.&]', '', name)
    return len(cleaned.strip()) >= 2

def sanitize_input(text: str) -> str:
    """Sanitize input text to prevent injection"""
    if not text:
        return ""
    # Remove any potential harmful characters
    sanitized = re.sub(r'[<>"\'`]', '', text)
    return sanitized.strip()

def validate_url(url: str) -> bool:
    """Validate URL format"""
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url_pattern.match(url) is not None

def validate_lead_data(data: dict) -> dict:
    """Validate lead data structure"""
    errors = {}
    
    # Required fields
    required_fields = ['first_name', 'last_name', 'email', 'company_name']
    for field in required_fields:
        if not data.get(field):
            errors[field] = f"{field} is required"
    
    # Email validation
    if data.get('email') and not validate_email(data['email']):
        errors['email'] = "Invalid email format"
    
    # Phone validation (if provided)
    if data.get('phone') and not validate_phone(data['phone']):
        errors['phone'] = "Invalid phone number format"
    
    return errors

def validate_score_value(value: int, min_val: int = 0, max_val: int = 100) -> bool:
    """Validate score value is within range"""
    return isinstance(value, int) and min_val <= value <= max_val

def validate_meddpicc_scoring(scoring: dict) -> dict:
    """Validate MEDDPICC scoring data"""
    errors = {}
    
    required_fields = [
        'metrics', 'economic_buyer', 'decision_criteria',
        'decision_process', 'paper_process', 'internal_champion', 'competition'
    ]
    
    for field in required_fields:
        if field not in scoring:
            errors[field] = f"{field} is required"
        elif not validate_score_value(scoring[field]):
            errors[field] = f"{field} must be between 0 and 100"
    
    return errors