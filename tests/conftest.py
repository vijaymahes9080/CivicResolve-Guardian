import pytest
import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend"))

from app.main import app as fastapi_app
from app.db.base import Base
from app.db.session import get_db
import app.models
from app.models.user import User
from app.core.security import get_password_hash, create_access_token
from app.services.rag import rag_engine

TEST_DB_URL = "sqlite:///./test_civicresolve.db"
test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    
    db = TestingSessionLocal()
    # Index policies into test DB
    rag_engine.index_markdown_policies(db)
    
    # Create test users
    admin = User(
        id="usr-admin-001",
        email="test_admin@civicresolve.gov.in",
        hashed_password=get_password_hash("AdminPass123!"),
        full_name="Test Administrator",
        role="admin"
    )
    officer = User(
        id="usr-officer-001",
        email="test_officer@civicresolve.gov.in",
        hashed_password=get_password_hash("OfficerPass123!"),
        full_name="Test Officer",
        role="officer",
        department="Water Supply & Sewerage Board",
        ward="Ward 12"
    )
    citizen = User(
        id="usr-citizen-001",
        email="test_citizen@civicresolve.gov.in",
        hashed_password=get_password_hash("CitizenPass123!"),
        full_name="Test Citizen",
        role="citizen",
        ward="Ward 12"
    )
    db.add_all([admin, officer, citizen])
    db.commit()
    db.close()
    
    yield
    
    Base.metadata.drop_all(bind=test_engine)
    if os.path.exists("./test_civicresolve.db"):
        try:
            os.remove("./test_civicresolve.db")
        except Exception:
            pass

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as test_client:
        yield test_client
    fastapi_app.dependency_overrides.clear()

@pytest.fixture
def citizen_token():
    return create_access_token({"sub": "usr-citizen-001", "role": "citizen", "email": "test_citizen@civicresolve.gov.in"})

@pytest.fixture
def officer_token():
    return create_access_token({"sub": "usr-officer-001", "role": "officer", "email": "test_officer@civicresolve.gov.in"})

@pytest.fixture
def admin_token():
    return create_access_token({"sub": "usr-admin-001", "role": "admin", "email": "test_admin@civicresolve.gov.in"})
