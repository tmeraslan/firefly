# conftest.py (בתיקיית השורש של firefly או בתיקיית tests)
import os, pytest, requests

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL") or os.getenv("FIREFLY_URL") or "http://localhost:8080"

@pytest.fixture(scope="session")
def api_token() -> str:
    return os.getenv("API_TOKEN") or os.getenv("FIREFLY_API_TOKEN") or ""

@pytest.fixture(scope="session")
def api_session(api_token):
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    if api_token:
        s.headers.update({"Authorization": f"Bearer {api_token}"})
    return s
