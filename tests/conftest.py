from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    # Provide a reusable HTTP client for calling FastAPI endpoints in tests.
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    # Snapshot in-memory data before each test and restore it afterward
    # so test cases remain isolated from each other's mutations.
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(deepcopy(original_activities))
