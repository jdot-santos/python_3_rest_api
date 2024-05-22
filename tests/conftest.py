# conftest.py has a special meaning for pytest.
# This will be executed before all of the tests and we can use it to setup fixtures
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from globoticket.api import app, get_session
from globoticket.models import Base, DBCategory, DBEvent

# for the test DB, we're creating a SQLite DB
test_db = sqlalchemy.create_engine(
    "sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, echo=True
)

# creating a session maker specifically for the test DB
test_sessionmaker = sessionmaker(bind=test_db)


def setup_test_db():
    Base.metadata.create_all(bind=test_db)
    session = Session(test_db)
    mock_category = DBCategory(name="t")
    mock_event = DBEvent(
        id=1,
        product_code="123456",
        price=5.50,
        date=date(2024, 5, 1),
        category=mock_category,
    )
    session.add(mock_category)
    session.add(mock_event)
    session.commit()


def get_test_session():
    """Create a DB session for a single test
    Once test is complete, close the session and drop all tables"""
    setup_test_db()
    session = test_sessionmaker()
    try:
        yield session
    finally:
        session.close()
        # ensures test isolation, so that each test will have a clean set of data
        Base.metadata.drop_all(bind=test_db)


# unit tests can request to use this fixture then they need a test client
@pytest.fixture()
def client():
    """Create a TestClient that uses the test database"""

    # see https://fastapi.tiangolo.com/advanced/testing-database/
    # tells FastAPI to override the get_session dependency with get_test_session
    app.dependency_overrides[get_session] = get_test_session
    # TestClient is from starlette.testclient, and is included with FastAPI
    # TestClient behaves almost exactly when you would do a call to an API with
    # requests.
    yield TestClient(app)
    del app.dependency_overrides[get_session]


# This fixture replaces the value at FRONTMATTER_DIRECTORY with the
#   directory of the test files.
# autouse=True means that this fixture will run automatically without any
#   unit test having to explicitly request it
# scope=session means that it will run only once for the entire testing
#   session.
@pytest.fixture(autouse=True, scope="session")
def test_frontmatter():
    """Override the location of frontmatter files."""
    # this encapsulates all the unit tests that will run inside this block
    with patch(
        "globoticket.frontmatter.FRONTMATTER_DIRECTORY",
        new=Path(__file__).parent / "product_info",
    ):
        yield
