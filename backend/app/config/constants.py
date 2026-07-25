"""Application constants"""

# MEDDPICC Framework Weights
MEDDPICC_WEIGHTS = {
    'metrics': 0.20,
    'economic_buyer': 0.15,
    'decision_criteria': 0.15,
    'decision_process': 0.15,
    'paper_process': 0.10,
    'internal_champion': 0.15,
    'competition': 0.10
}

# Lead Status
LEAD_STATUS = {
    "PENDING": "pending",
    "PROCESSING": "processing",
    "QUALIFIED": "qualified",
    "DISQUALIFIED": "disqualified",
    "ERROR": "error"
}

# GTM Motions
GTM_MOTIONS = {
    "DIRECT_AE": "direct_ae",
    "PARTNER_LED": "partner_led",
    "SDR_LED": "sdr_led"
}

# Agent Names
AGENT_NAMES = [
    "email_parser",
    "company_research",
    "industry_intel",
    "pain_point",
    "decision_maker",
    "lead_scoring",
    "case_study",
    "email_generation",
    "linkedin",
    "quality_checker",
    "summary"
]

# Case Study Categories
CASE_STUDY_CATEGORIES = [
    "sales_automation",
    "lead_generation",
    "pipeline_acceleration",
    "crm_integration",
    "ai_sales_assistant"
]