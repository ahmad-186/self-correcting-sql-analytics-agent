from fastapi.testclient import TestClient

from main import app
from app.api.routes.analytics import graph


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"Status": "Healthy"}


def test_analytics_query_success(monkeypatch):

    def mock_graph_invoke(state):
        return {
            "final_response": {
                "question": state["question"],
                "summary": {
                    "summary": "Test summary",
                    "key_insights": [],
                },
                "chart": None,
                "result": [],
            }
        }

    monkeypatch.setattr(graph, "invoke", mock_graph_invoke)

    response = client.post(
        "/analytics/query",
        json={"question": "Show all customers"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "Show all customers"
    assert data["summary"]["summary"] == "Test summary"


def test_empty_question():
    response = client.post(
        "/analytics/query",
        json={"question": ""},
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"] == "VALIDATION_ERROR"


def test_missing_question():
    response = client.post(
        "/analytics/query",
        json={},
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"] == "VALIDATION_ERROR"