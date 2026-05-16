import pytest
from sqlalchemy import create_engine

from app.db.database import Base


TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(autouse=True)
def reset_test_database():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()
