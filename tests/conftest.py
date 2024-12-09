import pytest
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models.user import User


@pytest.fixture
def test_app():
    """
    Creates and configures the app for testing.
    Sets up an in-memory SQLite database for isolation.
    """
    app = create_app(testing=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use in-memory DB
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    app.config["SECRET_KEY"] = "test_secret_key"  # Test secret key
    app.url_map.strict_slashes = False  # Disable strict slashes

    with app.app_context():
        db.create_all()  # Set up tables
        yield app
        db.session.remove()  # Clean up DB session
        db.drop_all()  # Drop all tables after test


@pytest.fixture
def client(test_app):
    """
    Provides a test client for making requests to the app.
    """
    return test_app.test_client()


@pytest.fixture
def setup_user(test_app):
    """
    Creates a test user in the database for testing purposes.
    """
    with test_app.app_context():
        user = User(username="testuser", password=generate_password_hash("password123"))
        db.session.add(user)
        db.session.commit()


@pytest.fixture
def logged_in_client(client, setup_user):
    client.post("/login", data={"username": "testuser", "password": "password123"})
    return client
