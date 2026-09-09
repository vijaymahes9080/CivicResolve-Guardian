"""
CivicResolve Guardian - Citizen Post-Resolution CSAT & Sentiment Analyzer
Evaluates post-resolution citizen feedback (bilingual Tamil தமிழ் and English),
detecting fraudulent closure reports and automatically triggering dispute reopenings.
"""

from typing import Dict, Any


DISSATISFIED_KEYWORDS_EN = ["fake", "not fixed", "still broken", "lies", "not cleared", "fraud", "worst", "unresolved", "terrible", "stinking", "pothole still there"]
DISSATISFIED_KEYWORDS_TA = ["பொய்", "சரிசெய்யப்படவில்லை", "அப்படியே உள்ளது", "மோசம்", "குப்பை எடுக்கவில்லை", "தண்ணீர் வரவில்லை", "ஏமாற்று"]

SATISFIED_KEYWORDS_EN = ["thank you", "fixed", "great work", "good job", "prompt", "resolved", "cleaned", "excellent", "appreciate"]
SATISFIED_KEYWORDS_TA = ["நன்றி", "சரிசெய்துவிட்டார்கள்", "நல்ல பணி", "பாராட்டுக்கள்", "சுத்தப்படுத்தப்பட்டது"]


class CitizenSentimentEvaluator:
    """Analyzes citizen feedback to safeguard against fabricated officer closures."""

    @classmethod
    def evaluate_feedback(
        cls,
        complaint_id: str,
        rating: int, # 1 to 5
        feedback_text: str,
    ) -> Dict[str, Any]:
        text_lower = feedback_text.lower()

        neg_hits_en = [w for w in DISSATISFIED_KEYWORDS_EN if w in text_lower]
        neg_hits_ta = [w for w in DISSATISFIED_KEYWORDS_TA if w in text_lower]
        pos_hits_en = [w for w in SATISFIED_KEYWORDS_EN if w in text_lower]
        pos_hits_ta = [w for w in SATISFIED_KEYWORDS_TA if w in text_lower]

        total_neg = len(neg_hits_en) + len(neg_hits_ta)
        total_pos = len(pos_hits_en) + len(pos_hits_ta)

        # Classify sentiment
        if rating <= 2 or total_neg > total_pos:
            sentiment = "NEGATIVE_DISPUTE"
            should_reopen = True
            reopen_reason = "Citizen indicates resolution was fabricated or grievance persists"
        elif rating >= 4 or total_pos > total_neg:
            sentiment = "POSITIVE_VERIFIED"
            should_reopen = False
            reopen_reason = None
        else:
            sentiment = "NEUTRAL"
            should_reopen = False
            reopen_reason = None

        csat_score_pct = round((rating / 5.0) * 100.0, 1)

        return {
            "complaint_id": complaint_id,
            "star_rating": rating,
            "csat_score_pct": csat_score_pct,
            "sentiment": sentiment,
            "detected_triggers": neg_hits_en + neg_hits_ta,
            "should_reopen_ticket": should_reopen,
            "reopen_reason": reopen_reason,
            "escalate_to_vigilance": should_reopen and ("fake" in text_lower or "பொய்" in text_lower),
        }
