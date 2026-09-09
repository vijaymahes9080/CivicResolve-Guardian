import pytest
from app.services.sentiment_feedback import CitizenSentimentEvaluator

def test_sentiment_satisfied_english():
    res = CitizenSentimentEvaluator.evaluate_feedback(
        complaint_id="CMP-300",
        rating=5,
        feedback_text="Thank you very much, pothole was completely fixed in 24 hours! Great work!",
    )
    assert res["sentiment"] == "POSITIVE_VERIFIED"
    assert res["should_reopen_ticket"] is False
    assert res["csat_score_pct"] == 100.0

def test_sentiment_fake_closure_tamil():
    res = CitizenSentimentEvaluator.evaluate_feedback(
        complaint_id="CMP-301",
        rating=1,
        feedback_text="இது பொய்! குப்பை எடுக்கவில்லை, அப்படியே உள்ளது!",
    )
    assert res["sentiment"] == "NEGATIVE_DISPUTE"
    assert res["should_reopen_ticket"] is True
    assert res["escalate_to_vigilance"] is True
    assert "பொய்" in res["detected_triggers"]
