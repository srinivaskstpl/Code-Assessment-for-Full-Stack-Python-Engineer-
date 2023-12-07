from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_create_review():
    review_data = {"text": "Test review text"}
    response = client.post("/review", json=review_data)
    assert response.status_code == 200
    assert "id" in response.json()


def test_create_tag():
    tag_name = "TestTagGGG"
    response = client.post(f"/tags?tag={tag_name}")
    assert response.status_code == 200
    assert "tag_id" in response.json()
    client.delete(f"/tags/{response.json().get('tag_id')}")


def test_delete_tag():
    tag_name = "TestTagToDelete"
    create_response = client.post(f"/tags?tag={tag_name}")
    tag_id = create_response.json()["tag_id"]

    response = client.delete(f"/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Tag and associated review_tags deleted successfully"
    }


def test_get_reviews():
    response = client.get("/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_tags_to_review():
    review_data = {"text": "Test review text"}
    create_review_response = client.post("/review", json=review_data)
    review_id = create_review_response.json()["id"]

    tag_name = "TestTagGGGToAdd"
    create_tag_response = client.post(f"/tags?tag={tag_name}")
    tag_id = create_tag_response.json()["tag_id"]

    response = client.post(f"/reviews/{review_id}/tags", json=[tag_id])
    assert response.status_code == 200
    assert response.json() == {"message": "Tags added successfully"}
    client.delete(f"/tags/{create_tag_response.json().get('tag_id')}")
