import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app.db.base import Base
from app.db.session import engine, SessionLocal
import app.models
from app.models.user import User
from app.models.complaint import ComplaintRecord
from app.core.security import get_password_hash
from app.core.pii import pii_engine
from app.services.rag import rag_engine
from app.services.triage_agent import triage_agent

def seed_database():
    print("Creating database schema...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        print("Indexing municipal policy documents...")
        rag_engine.index_markdown_policies(db)
        
        # 1. Create Default Users
        users_to_create = [
            {
                "email": "admin@civicresolve.gov.in",
                "password": "Admin@2026!",
                "full_name": "Dr. Arumugam IAS (Commissioner)",
                "role": "admin",
                "phone_number": "+91 9444011000",
                "preferred_language": "en"
            },
            {
                "email": "officer@civicresolve.gov.in",
                "password": "Officer@2026!",
                "full_name": "R. Selvaraj (Executive Engineer - GRO)",
                "role": "officer",
                "phone_number": "+91 9840155220",
                "preferred_language": "en",
                "department": "Water Supply & Sewerage Board",
                "ward": "Ward 12",
                "zone": "Zone 4 (Central)"
            },
            {
                "email": "citizen@civicresolve.gov.in",
                "password": "Citizen@2026!",
                "full_name": "Vijay Mahes",
                "role": "citizen",
                "phone_number": "+91 9840123456",
                "preferred_language": "en",
                "ward": "Ward 12",
                "zone": "Zone 4 (Central)"
            },
            {
                "email": "selvi@civicresolve.gov.in",
                "password": "Citizen@2026!",
                "full_name": "மு. செல்வி (Selvi)",
                "role": "citizen",
                "phone_number": "+91 9789012345",
                "preferred_language": "ta",
                "ward": "Ward 14",
                "zone": "Zone 5 (South)"
            }
        ]
        
        for u in users_to_create:
            existing = db.query(User).filter(User.email == u["email"]).first()
            if not existing:
                user = User(
                    email=u["email"],
                    hashed_password=get_password_hash(u["password"]),
                    full_name=u["full_name"],
                    role=u["role"],
                    phone_number=u["phone_number"],
                    preferred_language=u["preferred_language"],
                    department=u.get("department"),
                    ward=u.get("ward"),
                    zone=u.get("zone")
                )
                db.add(user)
                print(f"Created user: {u['email']} [{u['role']}]")
                
        db.commit()
        
        # 2. Seed Initial Sample Complaints
        citizen_en = db.query(User).filter(User.email == "citizen@civicresolve.gov.in").first()
        citizen_ta = db.query(User).filter(User.email == "selvi@civicresolve.gov.in").first()
        
        sample_complaints = [
            {
                "citizen_id": citizen_en.id,
                "content": "Severe drinking water contamination at Door No. 14/2, 4th Cross Street, Ward 12. Brown foul-smelling water since 3 days. Contact me at 9840123456.",
                "language": "en",
                "ward": "Ward 12",
                "zone": "Zone 4 (Central)"
            },
            {
                "citizen_id": citizen_ta.id,
                "content": "எங்கள் பகுதியில் கதவு எண் 45, நேதாஜி தெரு, வார்டு 14-ல் கடந்த மூன்று நாட்களாக குடிநீர் குழாய் உடைந்து பெருமளவில் வீணாகிறது. உடனடியாக சரிசெய்யவும். தொடர்பு எண் 9789012345.",
                "language": "ta",
                "ward": "Ward 14",
                "zone": "Zone 5 (South)"
            },
            {
                "citizen_id": citizen_en.id,
                "content": "Deep road crater and pothole near the Government Girls High School on Kamarajar Salai. Two motorcyclists skidded yesterday. Urgent bitumen patch needed.",
                "language": "en",
                "ward": "Ward 12",
                "zone": "Zone 4 (Central)"
            },
            {
                "citizen_id": citizen_en.id,
                "content": "Major street light failure on 2nd Main Road. Four consecutive poles have burnt LED fixtures. Complete darkness for women returning from bus stop after 8 PM.",
                "language": "en",
                "ward": "Ward 12",
                "zone": "Zone 4 (Central)"
            }
        ]
        
        existing_count = db.query(ComplaintRecord).count()
        if existing_count == 0:
            for sc in sample_complaints:
                redacted, _ = pii_engine.redact(sc["content"])
                complaint = ComplaintRecord(
                    citizen_id=sc["citizen_id"],
                    original_language=sc["language"],
                    raw_content=sc["content"],
                    redacted_content=redacted,
                    ward=sc["ward"],
                    zone=sc["zone"],
                    status="SUBMITTED",
                    priority="MEDIUM"
                )
                db.add(complaint)
                db.commit()
                db.refresh(complaint)
                
                # Auto-run triage recommendation
                rec = triage_agent.evaluate_complaint(db, complaint)
                db.add(rec)
                complaint.status = "TRIAGED_PENDING_APPROVAL"
                complaint.category = rec.suggested_category
                complaint.department = rec.suggested_department
                complaint.priority = rec.priority_score
                db.commit()
                print(f"Created sample complaint #{complaint.id[:8]} ({complaint.department}, Priority: {complaint.priority})")
                
        print("Database seed completed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
