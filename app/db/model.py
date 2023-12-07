from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Tag(Base):
    """
    Represents a tag associated with a review.
    """

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True, unique=True)


class ReviewTag(Base):
    """
    Represents a tag associated with a review, including additional information.
    """

    __tablename__ = "review_tags"

    id = Column(Integer, primary_key=True, index=True)
    is_ai_tag = Column(Boolean, nullable=False, default=False)
    tag_id = Column(Integer, ForeignKey("tags.id"))

    tag = relationship("Tag")
    review_review_tag = relationship("ReviewReviewTag", back_populates="review_tag")


class Review(Base):
    """
    Represents a review with optional tags.
    """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(2048))
    is_tagged = Column(Boolean, default=False)

    review_tags = relationship("ReviewReviewTag", back_populates="review")


class ReviewReviewTag(Base):
    """
    Represents the association between a review and a review tag.
    """

    __tablename__ = "review_review_tags"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"))
    review_tag_id = Column(Integer, ForeignKey("review_tags.id"))

    review = relationship("Review", back_populates="review_tags")
    review_tag = relationship("ReviewTag", back_populates="review_review_tag")
