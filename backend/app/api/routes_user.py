from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.dependencies.database import get_db
from app.models.submission import Submission
from app.services.analytics_service import get_analysis, get_progress
from app.services.codeforces_service import fetch_user_submissions
from app.services.submission import process_submission

router = APIRouter(prefix="/user", tags=["User"])


def _fetch_and_store(handle: str, db: Session) -> list[Submission]:
    """Fetch submissions from Codeforces and persist new ones."""
    try:
        raw = fetch_user_submissions(handle)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Codeforces API error: {exc}",
        )

    for item in raw[:200]:
        tags = item["problem"].get("tags", [])
        pid = str(item["problem"]["contestId"]) + item["problem"]["index"]
        verdict = item.get("verdict", "")

      
        if not verdict:
            continue 
        actual_date = datetime.utcfromtimestamp(
            item["creationTimeSeconds"]
        ).date()
        process_submission(db, handle, pid, tags, verdict,actual_date)

    db.commit()

    return db.query(Submission).filter_by(handle=handle).all()


@router.get("/analysis/{handle}")
def analysis(handle: str, db: Session = Depends(get_db)):
    subs = _fetch_and_store(handle, db)

    return {
        "analysis": get_analysis(subs),
        "progress": get_progress(subs),
    }


@router.get("/progress/{handle}")
def progress(handle: str, db: Session = Depends(get_db)):
    """
    Return the daily accuracy progress for a given Codeforces handle.
    Fetches fresh submissions if not already cached.
    """
    subs = _fetch_and_store(handle, db)
    return get_progress(subs)
