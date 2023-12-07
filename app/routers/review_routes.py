from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db.model import Review, ReviewReviewTag, ReviewTag, Tag

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.post("/review")
async def create_review(review_data: dict, db: Session = Depends(get_db)):
    """
    Create a new review.

    Parameters:
    - review_data (dict): A dictionary containing the data for the new review.
    - db (Session): The database session, obtained from the `get_db` dependency.

    Returns:
    - Review: The newly created review.
    """
    try:
        new_review = Review(**review_data)
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Failed to create review. Error: {str(e)}"
        )


@router.post("/tags")
async def create_tag(tag: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Create a new tag with the provided name.

    Args:
        tag (str): The name of the tag to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing a success message and the ID of the created tag.
    """
    if db.query(Tag).filter(Tag.name == tag).first():
        raise HTTPException(status_code=400, detail="Tag name already exists")

    new_tag = Tag(name=tag)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)

    response_data = {"message": "Tag created successfully", "tag_id": new_tag.id}
    return response_data


@router.delete("/tags/{tag_id}")
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Delete a tag and its associated review_tags.

    Parameters:
    - tag_id (int): The ID of the tag to be deleted.
    - db (Session): The SQLAlchemy database session.

    Returns:
    dict: A message indicating successful deletion.

    Raises:
    HTTPException: If the tag is not found.
    """

    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.query(ReviewTag).filter(ReviewTag.tag_id == tag_id).delete(
        synchronize_session=False
    )
    db.query(Tag).filter(Tag.id == tag_id).delete(synchronize_session=False)
    db.commit()
    return {"message": "Tag and associated review_tags deleted successfully"}


def get_reviews_with_tags(review):
    tags = []
    for tag in review.review_tags:
        if tag:
            tags.append(
                {"tag_id": tag.review_tag.tag_id, "is_ai_tag": tag.review_tag.is_ai_tag}
            )
    return {"review_id": review.id, "text": review.text, "tags": tags}


@router.get("/reviews", response_model=List[dict], tags=["reviews"])
async def get_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Get a list of reviews with optional pagination.

    :param skip: Number of reviews to skip.
    :param limit: Number of reviews to retrieve.
    :param db: Database session dependency.
    :return: List of reviews with associated tags.
    """
    reviews = db.query(Review).offset(skip).limit(limit).all()
    reviews_with_tags = [get_reviews_with_tags(review) for review in reviews if review]
    return reviews_with_tags


@router.post("/reviews/{review_id}/tags")
async def add_tags_to_review(
    review_id: int, tag_ids: List[int], db: Session = Depends(get_db)
):
    """
    Add tags to a specific review.

    Parameters:
    - review_id (int): The ID of the review to which tags will be added.
    - tag_ids (List[int]): List of tag IDs to be added to the review.
    - db (Session): SQLAlchemy database session.

    Returns:
    - dict: A dictionary with a success message.
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

    if len(tags) != len(tag_ids):
        raise HTTPException(status_code=404, detail="One or more tags not found")

    for tag in tags:
        review_tag = ReviewTag(is_ai_tag=False, tag_id=tag.id, tag=tag)
        review_review_tag = ReviewReviewTag(
            review_id=review.id, review_tag_id=review_tag.id, review_tag=review_tag
        )
        review.review_tags.append(review_review_tag)

    review.is_tagged = True
    db.commit()

    return {"message": "Tags added successfully"}
