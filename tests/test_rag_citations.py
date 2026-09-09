import pytest
from app.services.rag import rag_engine

def test_water_contamination_policy_search(db_session):
    query = "Drinking water contamination with sewage smell from tap"
    results = rag_engine.search_policy(db_session, query=query, top_k=2)
    
    assert len(results) > 0
    top = results[0]
    assert "WATER" in top["policy_id"]
    assert top["relevance_score"] >= 0.50
    assert "Section" in top["title"]
    assert len(top["excerpt"]) > 10

def test_pothole_regulations_search(db_session):
    query = "Road crater and deep pothole causing two-wheeler accidents"
    results = rag_engine.search_policy(db_session, query=query, top_k=2)
    
    assert len(results) > 0
    top = results[0]
    assert "ROAD" in top["policy_id"]
    assert "Pothole" in top["title"] or "Road" in top["title"]

def test_unrelated_query_insufficient_evidence(db_session):
    # An inquiry that has no municipal charter match
    query = "How do I build a spaceship to travel to Mars orbit?"
    results = rag_engine.search_policy(db_session, query=query, top_k=3)
    
    # Must reject false positive citations
    assert len(results) == 0
