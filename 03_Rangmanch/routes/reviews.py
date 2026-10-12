from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select

from database import get_session
from models import Review, ReviewCreate, ReviewRead, ReviewUpdate

router = APIRouter(prefix="/review", tags=["reviews"])


@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    db_review = Review(**review.model_dump())
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


@router.get("/", response_model=list[ReviewRead])
def list_reviews(
    play_name: str | None = Query(None, description="Filer by play name"),
    skip: int = Query(0, ge=0, description="Number of reviews to skip"),
    limit: int = Query(10, ge=1, le=50, description="Max reviews to return "),
    session: Session = Depends(get_session),
):
    query = select(Review)

    if play_name:
        query = query.where(Review.play_name == play_name)

    query = query.offset(skip).limit(limit)
    reviews = session.exec(query).all()
    return reviews


@router.get("/average/{play_name}")
def get_average_rating(play_name: str, session: Session = Depends(get_session)):
    result = session.exec(
        select(func.avg(Review.rating), func.count(Review.id)).where(  # type: ignore
            Review.play_name == play_name
        )
    ).first()

    avg_raing, total_reviews = result  # type: ignore

    if total_reviews == 0:
        raise HTTPException(status_code=404, detail=f"No Review found for {play_name}")

    return {
        "play_name": play_name,
        "average_rating": round(avg_raing, 2),
        "total_reviews": total_reviews,
    }


@router.get("/{review_id}", response_model=ReviewRead)
def get_review(  # type: ignore
    review_id: int, session: Session = Depends(get_session)
):  # pyright: ignore[reportRedeclaration]
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="No review")
    return review


@router.patch("/{review_id}", response_model=ReviewRead)
def get_review(
    review_id: int, update: ReviewUpdate, session: Session = Depends(get_session)
):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="No review")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_date.items():  # noqa: F821
        setattr(review, key, value)

    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@router.delete("/{review_id}")
def delete_review(
    review_id: int, update: ReviewUpdate, session: Session = Depends(get_session)
):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="No review")

    session.delete(review)
    session.commit()
    return {"message": "Review delted"}
