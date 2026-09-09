from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.schemas.policy import PolicyCitation, PolicyDocumentOut
from app.models.policy import PolicyDocument
from app.services.rag import rag_engine

router = APIRouter(prefix="/policies", tags=["Policies"])

@router.get("/search", response_model=List[PolicyCitation])
def search_policies(
    query: str = Query(..., min_length=3, description="Grievance description or query"),
    department: Optional[str] = Query(None, description="Filter by department"),
    top_k: int = Query(3, ge=1, le=10),
    db: Session = Depends(get_db)
):
    results = rag_engine.search_policy(db, query=query, department=department, top_k=top_k)
    return results

@router.get("/documents", response_model=List[PolicyDocumentOut])
def list_policy_documents(db: Session = Depends(get_db)):
    docs = db.query(PolicyDocument).all()
    if not docs:
        rag_engine.index_markdown_policies(db)
        docs = db.query(PolicyDocument).all()
    return docs
