from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_query_validation():

    response = client.post(
        "/api/v1/query",
        json={
            "query": "",
            "top_k": 5,
        },
    )

    assert response.status_code == 422

    print("Empty query validation: PASSED")


def test_invalid_top_k():

    response = client.post(
        "/api/v1/query",
        json={
            "query": "What is StarQ?",
            "top_k": 0,
        },
    )

    assert response.status_code == 422

    print("Invalid top_k validation: PASSED")


if __name__ == "__main__":

    test_query_validation()
    test_invalid_top_k()

    print("\n5.8 Query API Test: PASSED")