from typing import Dict, Any, Optional

from app.models.lead import MEDDPICCScore
from app.core.logging import get_logger

logger = get_logger(__name__)

class ScoringService:
    """Service for MEDDPICC scoring operations"""
    
    def __init__(self):
        self.logger = logger
        self.weights = {
            'metrics': 0.20,
            'economic_buyer': 0.15,
            'decision_criteria': 0.15,
            'decision_process': 0.15,
            'paper_process': 0.10,
            'internal_champion': 0.15,
            'competition': 0.10
        }
    
    def calculate_score(self, scores: Dict[str, int]) -> Dict[str, Any]:
        """Calculate weighted MEDDPICC score"""
        try:
            # Validate scores
            for field, value in scores.items():
                if field in self.weights:
                    if not isinstance(value, (int, float)) or value < 0 or value > 100:
                        scores[field] = 50  # Default to middle score
            
            # Create score object
            score_obj = MEDDPICCScore(
                metrics=scores.get('metrics', 50),
                economic_buyer=scores.get('economic_buyer', 50),
                decision_criteria=scores.get('decision_criteria', 50),
                decision_process=scores.get('decision_process', 50),
                paper_process=scores.get('paper_process', 50),
                internal_champion=scores.get('internal_champion', 50),
                competition=scores.get('competition', 50)
            )
            
            total_score = score_obj.total_score
            qualification = score_obj.qualification
            
            # Determine recommended motion
            motion = self._get_recommended_motion(score_obj)
            
            return {
                "metrics": score_obj.metrics,
                "economic_buyer": score_obj.economic_buyer,
                "decision_criteria": score_obj.decision_criteria,
                "decision_process": score_obj.decision_process,
                "paper_process": score_obj.paper_process,
                "internal_champion": score_obj.internal_champion,
                "competition": score_obj.competition,
                "total_score": total_score,
                "qualification": qualification,
                "recommended_motion": motion["motion"],
                "motion_reasoning": motion["reasoning"],
                "score_breakdown": self._get_score_breakdown(score_obj)
            }
            
        except Exception as e:
            self.logger.error(f"Failed to calculate score: {str(e)}")
            return {
                "error": str(e),
                "total_score": 0,
                "qualification": "error"
            }
    
    def _get_recommended_motion(self, score: MEDDPICCScore) -> Dict[str, str]:
        """Determine recommended GTM motion based on score"""
        if score.total_score >= 70:
            return {
                "motion": "direct_ae",
                "reasoning": "High score indicates strong fit and clear opportunity"
            }
        elif score.total_score >= 50:
            return {
                "motion": "sdr_led",
                "reasoning": "Moderate score suggests SDR qualification needed"
            }
        else:
            return {
                "motion": "partner_led",
                "reasoning": "Low score may benefit from partner qualification"
            }
    
    def _get_score_breakdown(self, score: MEDDPICCScore) -> Dict[str, Any]:
        """Get detailed score breakdown with ratings"""
        breakdown = {}
        for field in self.weights.keys():
            value = getattr(score, field)
            breakdown[field] = {
                "value": value,
                "weight": self.weights[field],
                "weighted_score": round(value * self.weights[field], 1),
                "rating": self._get_rating(value)
            }
        return breakdown
    
    def _get_rating(self, score: int) -> str:
        """Get rating based on score"""
        if score >= 80:
            return "Strong"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Moderate"
        else:
            return "Weak"
    
    def get_recommendations(self, scoring: Dict[str, Any]) -> List[str]:
        """Get recommendations based on scoring gaps"""
        recommendations = []
        
        # Check each dimension for improvement opportunities
        dimensions = {
            'metrics': "Consider quantifying potential business impact",
            'economic_buyer': "Work on accessing the economic buyer",
            'decision_criteria': "Align solution more closely with decision criteria",
            'decision_process': "Clarify the decision-making process",
            'paper_process': "Understand procurement requirements",
            'internal_champion': "Identify and nurture an internal champion",
            'competition': "Differentiate from competitors"
        }
        
        for field, value in scoring.items():
            if field in dimensions and value < 50:
                recommendations.append(f"Improve {field.replace('_', ' ')}: {dimensions[field]}")
        
        return recommendations[:3]  # Top 3 recommendations